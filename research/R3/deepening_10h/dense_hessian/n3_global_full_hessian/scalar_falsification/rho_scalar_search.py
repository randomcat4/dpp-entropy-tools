#!/usr/bin/env python3
"""
D10-U10c scalar rho falsification scout for the n=3 full-Hessian reduction.

This is an author-side falsification search, not a verifier and not a theorem.
It deliberately does not import the U8 author/search/gate modules.  The rho
implementation below rebuilds the eight exact Möbius atoms, the event Fisher
matrix, N, A, eta and the Schur scalar directly from the definitions recorded
in U8.

Outputs, written next to this script:
  - search_ledger.json
  - near_threshold_candidates.json
  - run_log.md
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import random
import sys
import time
from dataclasses import dataclass
from decimal import Decimal, getcontext, localcontext
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

# Avoid accidental BLAS thread fan-out before numpy is imported.
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

import numpy as np


BASE = Path(__file__).resolve().parent
ATOM_NAMES = ["0", "1", "2", "3", "12", "13", "23", "123"]
COORD_NAMES = ["11", "22", "33", "12", "13", "23"]
SEED = 202609081003
TOP_KEEP = 80


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def basis_mats_float() -> List[np.ndarray]:
    out = []
    for k in range(6):
        M = np.zeros((3, 3), dtype=float)
        if k == 0:
            M[0, 0] = 1.0
        elif k == 1:
            M[1, 1] = 1.0
        elif k == 2:
            M[2, 2] = 1.0
        elif k == 3:
            M[0, 1] = M[1, 0] = 1.0
        elif k == 4:
            M[0, 2] = M[2, 0] = 1.0
        elif k == 5:
            M[1, 2] = M[2, 1] = 1.0
        out.append(M)
    return out


BASIS_FLOAT = basis_mats_float()


def sym_from_coords(v: Sequence[float]) -> np.ndarray:
    return np.array(
        [[v[0], v[3], v[4]], [v[3], v[1], v[5]], [v[4], v[5], v[2]]],
        dtype=float,
    )


def eig_margins(K: np.ndarray) -> Tuple[float, float, np.ndarray]:
    vals = np.linalg.eigvalsh((K + K.T) / 2.0)
    return float(vals[0]), float(1.0 - vals[-1]), vals


def connected_support(K: np.ndarray, tol: float = 1e-13) -> bool:
    edges = [abs(K[0, 1]) > tol, abs(K[0, 2]) > tol, abs(K[1, 2]) > tol]
    return sum(edges) >= 2


def atoms_and_grads_float(K: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    x, y, z = K[0, 0], K[1, 1], K[2, 2]
    a, b, c = K[0, 1], K[0, 2], K[1, 2]

    q12 = x * y - a * a
    q13 = x * z - b * b
    q23 = y * z - c * c
    r = x * y * z + 2 * a * b * c - x * c * c - y * b * b - z * a * a

    gq12 = np.array([y, x, 0.0, -2 * a, 0.0, 0.0])
    gq13 = np.array([z, 0.0, x, 0.0, -2 * b, 0.0])
    gq23 = np.array([0.0, z, y, 0.0, 0.0, -2 * c])
    gr = np.array(
        [
            y * z - c * c,
            x * z - b * b,
            x * y - a * a,
            2 * b * c - 2 * z * a,
            2 * a * c - 2 * y * b,
            2 * a * b - 2 * x * c,
        ]
    )

    vals = np.array(
        [
            1 - x - y - z + q12 + q13 + q23 - r,
            x - q12 - q13 + r,
            y - q12 - q23 + r,
            z - q13 - q23 + r,
            q12 - r,
            q13 - r,
            q23 - r,
            r,
        ],
        dtype=float,
    )
    grads = np.vstack(
        [
            np.array([-1.0, -1.0, -1.0, 0.0, 0.0, 0.0]) + gq12 + gq13 + gq23 - gr,
            np.array([1.0, 0.0, 0.0, 0.0, 0.0, 0.0]) - gq12 - gq13 + gr,
            np.array([0.0, 1.0, 0.0, 0.0, 0.0, 0.0]) - gq12 - gq23 + gr,
            np.array([0.0, 0.0, 1.0, 0.0, 0.0, 0.0]) - gq13 - gq23 + gr,
            gq12 - gr,
            gq13 - gr,
            gq23 - gr,
            gr,
        ]
    )
    return vals, grads


@dataclass
class EvalResult:
    ok: bool
    status: str
    rho: Optional[float] = None
    K: Optional[np.ndarray] = None
    atoms: Optional[np.ndarray] = None
    eigvals: Optional[np.ndarray] = None
    min_atom: Optional[float] = None
    min_atom_name: Optional[str] = None
    eigmin_K: Optional[float] = None
    eigmin_IK: Optional[float] = None
    min_eig_N: Optional[float] = None
    min_eig_A: Optional[float] = None
    detN: Optional[float] = None
    Lambda: Optional[float] = None
    bad_direction: Optional[np.ndarray] = None
    Hpp_bad: Optional[float] = None


def evaluate_float(K: np.ndarray) -> EvalResult:
    K = (np.array(K, dtype=float) + np.array(K, dtype=float).T) / 2.0
    if not np.all(np.isfinite(K)):
        return EvalResult(False, "nonfinite_K")
    eigK, eigIK, vals = eig_margins(K)
    if eigK <= 0 or eigIK <= 0:
        return EvalResult(False, "not_strict_spectrum")
    if not connected_support(K):
        return EvalResult(False, "disconnected_support")
    atoms, grads = atoms_and_grads_float(K)
    if (not np.all(np.isfinite(atoms))) or np.min(atoms) <= 0:
        return EvalResult(False, "nonpositive_atom")

    try:
        p0, p1, p2, p3, p12, p13, p23, p123 = atoms
        l12 = math.log((p0 * p12) / (p1 * p2))
        l13 = math.log((p0 * p13) / (p1 * p3))
        l23 = math.log((p0 * p23) / (p2 * p3))
        Lambda = math.log((p123 * p1 * p2 * p3) / (p0 * p12 * p13 * p23))
    except (ValueError, ZeroDivisionError, OverflowError):
        return EvalResult(False, "log_failure")
    N = np.diag([-l23, -l13, -l12]) - Lambda * K
    N = (N + N.T) / 2.0
    try:
        evalN = np.linalg.eigvalsh(N)
    except np.linalg.LinAlgError:
        return EvalResult(False, "N_eig_failure")
    if evalN[0] <= 0 or (not np.all(np.isfinite(evalN))):
        return EvalResult(False, "N_not_PD")
    detN = float(np.linalg.det(N))
    if detN <= 0 or not math.isfinite(detN):
        return EvalResult(False, "detN_bad")
    try:
        Ninv = np.linalg.inv(N)
    except np.linalg.LinAlgError:
        return EvalResult(False, "N_inverse_failure")
    F = grads.T @ (grads / atoms[:, None])
    G = np.empty((6, 6), dtype=float)
    eta = np.empty(6, dtype=float)
    for i, Ei in enumerate(BASIS_FLOAT):
        eta[i] = float(np.trace(Ninv @ Ei))
        for j, Ej in enumerate(BASIS_FLOAT):
            G[i, j] = float(np.trace(Ninv @ Ei @ Ninv @ Ej))
    A = (F + detN * G + (F + detN * G).T) / 2.0
    try:
        evalA = np.linalg.eigvalsh(A)
    except np.linalg.LinAlgError:
        return EvalResult(False, "A_eig_failure")
    if evalA[0] <= 0 or not np.all(np.isfinite(evalA)):
        return EvalResult(False, "A_not_PD")
    try:
        d = np.linalg.solve(A, eta)
    except np.linalg.LinAlgError:
        return EvalResult(False, "A_solve_failure")
    rho = float(detN * (eta @ d))
    if not math.isfinite(rho):
        return EvalResult(False, "rho_nonfinite")
    B = A - detN * np.outer(eta, eta)
    Hpp_bad = -float(d @ B @ d)
    min_idx = int(np.argmin(atoms))
    return EvalResult(
        True,
        "ok",
        rho=rho,
        K=K,
        atoms=atoms,
        eigvals=vals,
        min_atom=float(atoms[min_idx]),
        min_atom_name=ATOM_NAMES[min_idx],
        eigmin_K=eigK,
        eigmin_IK=eigIK,
        min_eig_N=float(evalN[0]),
        min_eig_A=float(evalA[0]),
        detN=detN,
        Lambda=Lambda,
        bad_direction=d,
        Hpp_bad=Hpp_bad,
    )


class Recorder:
    def __init__(self, keep: int = TOP_KEEP):
        self.keep = keep
        self.stats: Dict[str, Dict[str, int]] = {}
        self.best: List[Dict[str, Any]] = []
        self.accepted = 0
        self.attempted = 0
        self.small_atom_hits = {name: 0 for name in ATOM_NAMES}

    def note(self, route: str, status: str) -> None:
        d = self.stats.setdefault(route, {})
        d[status] = d.get(status, 0) + 1
        self.attempted += 1
        if status == "ok":
            self.accepted += 1

    def try_K(self, K: np.ndarray, route: str, params: Dict[str, Any]) -> Optional[EvalResult]:
        res = evaluate_float(K)
        self.note(route, res.status)
        if not res.ok:
            return None
        for name, p in zip(ATOM_NAMES, res.atoms):
            if p < 1e-8:
                self.small_atom_hits[name] += 1
        rec = {
            "rho_float": res.rho,
            "one_minus_rho_float": 1.0 - float(res.rho),
            "route": route,
            "params": params,
            "K": np.asarray(res.K).tolist(),
            "atoms": {n: float(v) for n, v in zip(ATOM_NAMES, res.atoms)},
            "min_atom": res.min_atom,
            "min_atom_name": res.min_atom_name,
            "eigvals": np.asarray(res.eigvals).tolist(),
            "eigmin_K": res.eigmin_K,
            "eigmin_IK": res.eigmin_IK,
            "min_eig_N": res.min_eig_N,
            "min_eig_A": res.min_eig_A,
            "detN": res.detN,
            "Lambda": res.Lambda,
            "Hpp_bad_float": res.Hpp_bad,
        }
        self.best.append(rec)
        self.best.sort(key=lambda r: r["rho_float"], reverse=True)
        if len(self.best) > self.keep:
            self.best.pop()
        return res


def rotation_from_angles(ang: Sequence[float]) -> np.ndarray:
    ax, ay, az = ang
    cx, sx = math.cos(ax), math.sin(ax)
    cy, sy = math.cos(ay), math.sin(ay)
    cz, sz = math.cos(az), math.sin(az)
    Rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]], dtype=float)
    Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]], dtype=float)
    Rz = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]], dtype=float)
    Q = Rz @ Ry @ Rx
    return Q


def random_rotation(rng: np.random.Generator) -> np.ndarray:
    M = rng.normal(size=(3, 3))
    Q, R = np.linalg.qr(M)
    signs = np.sign(np.diag(R))
    signs[signs == 0] = 1.0
    Q = Q * signs
    if np.linalg.det(Q) < 0:
        Q[:, 0] *= -1
    return Q


def K_from_eigs(Q: np.ndarray, lam: Sequence[float]) -> np.ndarray:
    K = Q @ np.diag(np.array(lam, dtype=float)) @ Q.T
    return (K + K.T) / 2.0


def orthonormal_from_u(u: Sequence[float], phi: float = 0.0) -> np.ndarray:
    u = np.array(u, dtype=float)
    u = u / np.linalg.norm(u)
    idx = int(np.argmin(np.abs(u)))
    e = np.zeros(3)
    e[idx] = 1.0
    v = e - u * float(u @ e)
    v /= np.linalg.norm(v)
    w = np.cross(u, v)
    v2 = math.cos(phi) * v + math.sin(phi) * w
    w2 = -math.sin(phi) * v + math.cos(phi) * w
    Q = np.column_stack([v2, w2, u])
    if np.linalg.det(Q) < 0:
        Q[:, 0] *= -1
    return Q


def K_from_L(L: np.ndarray) -> np.ndarray:
    I = np.eye(3)
    K = np.linalg.solve(I + L, L)
    return (K + K.T) / 2.0


def is_spd_float(M: np.ndarray) -> bool:
    try:
        return float(np.linalg.eigvalsh((M + M.T) / 2.0)[0]) > 0
    except np.linalg.LinAlgError:
        return False


def max_edge_alpha(diag: Sequence[float], pattern: Sequence[float]) -> float:
    D = np.diag(diag)
    P = sym_from_coords([0, 0, 0, pattern[0], pattern[1], pattern[2]])

    def strict(alpha: float) -> bool:
        K = D + alpha * P
        return is_spd_float(K) and is_spd_float(np.eye(3) - K)

    hi = 1.0
    while strict(hi) and hi < 1e6:
        hi *= 2.0
    lo = 0.0
    for _ in range(80):
        mid = (lo + hi) / 2.0
        if strict(mid):
            lo = mid
        else:
            hi = mid
    return lo


def scan_spectral_corners(rec: Recorder, rng: np.random.Generator) -> None:
    route = "spectral_0_1_corners"
    rotations: List[np.ndarray] = []
    for ax in [0.19, 0.73, 1.21]:
        for ay in [0.37, 0.94]:
            for az in [0.51, 1.38]:
                rotations.append(rotation_from_angles((ax, ay, az)))
    for _ in range(48):
        rotations.append(random_rotation(rng))
    eps_vals = [1e-2, 1e-4, 1e-7, 1e-10, 1e-14]
    profiles: List[Tuple[float, float, float]] = []
    for e in eps_vals:
        profiles += [
            (e, 0.31, 0.73),
            (e, e, 0.51),
            (e, 1 - e, 0.47),
            (1 - e, 1 - math.sqrt(e), 0.62),
            (1 - e, e, 0.38),
        ]
    for Qid, Q in enumerate(rotations):
        for pid, base_lam in enumerate(profiles):
            for perm in [(0, 1, 2), (0, 2, 1), (1, 0, 2), (2, 1, 0)]:
                lam = tuple(base_lam[i] for i in perm)
                rec.try_K(K_from_eigs(Q, lam), route, {"Qid": Qid, "profile": pid, "perm": perm, "lambda": lam})


def scan_rank_one_rates(rec: Recorder) -> None:
    route = "rank_one_unequal_soft_rates"
    u_list = [
        (1, 2, 2),
        (1, -2, 2),
        (1, 1, 5),
        (1, -3, -2),
        (1, 7, -1),
        (1, 0.07, -2.0),
    ]
    phis = [0.0, 0.41, 1.13]
    thetas = [0.08, 0.2, 0.5, 0.88, 0.97]
    epsks = [2, 4, 8, 16, 32]
    rates = [(1, 2), (1, 3), (2, 3), (1, 5), (2, 5), (1, 1)]
    for uid, u in enumerate(u_list):
        for phi in phis:
            Q = orthonormal_from_u(u, phi)
            for theta in thetas:
                for k in epsks:
                    eps = 10.0 ** (-k)
                    for r, s in rates:
                        lam = (eps**r, eps**s, theta)
                        rec.try_K(
                            K_from_eigs(Q, lam),
                            route,
                            {"uid": uid, "u": u, "phi": phi, "theta": theta, "k": k, "rates": [r, s], "complement": False},
                        )
                        lamc = (1 - eps**r, 1 - eps**s, theta)
                        rec.try_K(
                            K_from_eigs(Q, lamc),
                            route,
                            {"uid": uid, "u": u, "phi": phi, "theta": theta, "k": k, "rates": [r, s], "complement": True},
                        )


def scan_L_atom_boundaries(rec: Recorder, rng: np.random.Generator) -> None:
    route = "L_ensemble_exact_atom_boundaries"
    epsks = [2, 4, 6, 8, 10, 12]
    signs = [-1.0, 1.0]

    # Empty and full boundaries via large/small eigenvalues in L.
    for qid in range(12):
        Q = random_rotation(rng)
        for k in epsks:
            eps = 10.0 ** (-k)
            for scale in [0.7, 1.5, 4.0]:
                Lfull = Q @ np.diag([eps, scale, 2.0 + 0.3 * qid]) @ Q.T
                rec.try_K(K_from_L(Lfull), route, {"target_atom": "123", "qid": qid, "k": k, "scale": scale})
                Lempty = Q @ np.diag([1 / eps, scale / eps, (2.0 + 0.3 * qid) / eps]) @ Q.T
                rec.try_K(K_from_L(Lempty), route, {"target_atom": "0", "qid": qid, "k": k, "scale": scale})

    # Singleton boundaries: make L_ii tiny but keep a connected SPD L.
    for i in range(3):
        others = [j for j in range(3) if j != i]
        for k in epsks:
            eps = 10.0 ** (-k)
            for s1 in signs:
                for s2 in signs:
                    L = np.zeros((3, 3), dtype=float)
                    L[i, i] = eps
                    L[others[0], others[0]] = 1.3
                    L[others[1], others[1]] = 0.8
                    L[i, others[0]] = L[others[0], i] = s1 * 0.05 * math.sqrt(eps * 1.3)
                    L[i, others[1]] = L[others[1], i] = s2 * 0.04 * math.sqrt(eps * 0.8)
                    L[others[0], others[1]] = L[others[1], others[0]] = 0.17
                    if is_spd_float(L):
                        rec.try_K(K_from_L(L), route, {"target_atom": str(i + 1), "k": k, "signs": [s1, s2]})

    # Pair boundaries: make a 2x2 principal L minor nearly singular.
    pair_targets = [((0, 1), "12"), ((0, 2), "13"), ((1, 2), "23")]
    for (i, j), name in pair_targets:
        kidx = [m for m in range(3) if m not in (i, j)][0]
        for expk in epsks:
            delta = 10.0 ** (-expk)
            for signij in signs:
                for gik in [-0.06, 0.03, 0.11]:
                    for gjk in [-0.04, 0.08]:
                        L = np.zeros((3, 3), dtype=float)
                        L[i, i] = 1.0
                        L[j, j] = 1.0
                        L[kidx, kidx] = 1.4
                        L[i, j] = L[j, i] = signij * math.sqrt(1.0 - delta)
                        L[i, kidx] = L[kidx, i] = gik
                        L[j, kidx] = L[kidx, j] = gjk
                        if is_spd_float(L):
                            rec.try_K(
                                K_from_L(L),
                                route,
                                {"target_atom": name, "delta_exp": expk, "signij": signij, "gik": gik, "gjk": gjk},
                            )
                            Kc = np.eye(3) - K_from_L(L)
                            rec.try_K(
                                Kc,
                                route,
                                {"target_atom": "complement_of_" + name, "delta_exp": expk, "signij": signij, "gik": gik, "gjk": gjk},
                            )


def scan_edge_boundaries(rec: Recorder) -> None:
    route = "near_disconnected_and_sign_mixed_edges"
    diag_grid = [
        (0.08, 0.31, 0.79),
        (0.12, 0.5, 0.88),
        (0.25, 0.37, 0.62),
        (0.48, 0.51, 0.55),
        (0.91, 0.64, 0.21),
        (0.97, 0.83, 0.41),
    ]
    base_patterns = []
    for s12 in [-1, 1]:
        for s13 in [-1, 1]:
            for s23 in [-1, 1]:
                base_patterns.append((s12, s13, s23))
                base_patterns.append((s12, 0.0, s23))
                base_patterns.append((s12, s13, 0.0))
                base_patterns.append((0.0, s13, s23))
                for tiny in [1e-4, 1e-2]:
                    base_patterns.append((s12, tiny * s13, s23))
                    base_patterns.append((tiny * s12, s13, s23))
                    base_patterns.append((s12, s13, tiny * s23))
    fracs = [1e-5, 1e-3, 0.03, 0.12, 0.37, 0.74, 0.93, 0.985, 0.997]
    seen = set()
    for diag in diag_grid:
        for pat in base_patterns:
            key = (diag, pat)
            if key in seen:
                continue
            seen.add(key)
            alpha_max = max_edge_alpha(diag, pat)
            if alpha_max <= 0:
                continue
            P = sym_from_coords([0, 0, 0, pat[0], pat[1], pat[2]])
            for f in fracs:
                K = np.diag(diag) + (f * alpha_max) * P
                rec.try_K(K, route, {"diag": diag, "pattern": pat, "frac": f, "alpha_max": alpha_max})


def local_hill_from_top(rec: Recorder, rng: np.random.Generator) -> None:
    route = "targeted_local_hill_from_best"
    starts = list(rec.best[:24])
    for sid, r in enumerate(starts):
        K = np.array(r["K"], dtype=float)
        best = r["rho_float"]
        scale = min(0.04, max(2e-5, 0.20 * min(r["eigmin_K"], r["eigmin_IK"])))
        for step in range(700):
            if step in [180, 380, 560]:
                scale *= 0.35
            noise = rng.normal(size=6)
            # Bias some trials toward the currently smallest atom and boundary
            # directions by varying off-diagonal coordinates more heavily.
            noise[3:] *= 1.7
            D = sym_from_coords(noise)
            D /= max(1.0, np.linalg.norm(D, ord="fro"))
            K2 = K + scale * D
            res = rec.try_K(K2, route, {"start_rank": sid, "step": step, "scale": scale})
            if res is not None and res.rho is not None and res.rho > best:
                K = K2
                best = res.rho
                scale *= 1.05


def random_interior_targeted(rec: Recorder, rng: np.random.Generator) -> None:
    route = "biased_interior_random"
    lambdas_pool = [
        (0.02, 0.23, 0.91),
        (0.03, 0.67, 0.98),
        (0.08, 0.5, 0.96),
        (0.14, 0.86, 0.97),
        (0.2, 0.5, 0.8),
    ]
    for idx in range(6000):
        if idx % 5 == 0:
            base = lambdas_pool[(idx // 5) % len(lambdas_pool)]
            lam = tuple(min(0.999999, max(1e-9, b * math.exp(0.12 * rng.normal()))) for b in base)
        else:
            # logit-biased to 0/1 but not exactly there
            raw = rng.normal(0.0, 2.2, size=3)
            lam = tuple(float(1.0 / (1.0 + math.exp(-v))) for v in raw)
        Q = random_rotation(rng)
        rec.try_K(K_from_eigs(Q, lam), route, {"idx": idx, "lambda": lam})


# --------------------------- Decimal recheck ---------------------------


def D(x: Any) -> Decimal:
    return Decimal(str(x))


def dec_zero_matrix(n: int, m: int) -> List[List[Decimal]]:
    return [[Decimal(0) for _ in range(m)] for _ in range(n)]


def dec_eye(n: int) -> List[List[Decimal]]:
    M = dec_zero_matrix(n, n)
    for i in range(n):
        M[i][i] = Decimal(1)
    return M


def dec_matmul(A: List[List[Decimal]], B: List[List[Decimal]]) -> List[List[Decimal]]:
    n, m, p = len(A), len(B), len(B[0])
    C = dec_zero_matrix(n, p)
    for i in range(n):
        for k in range(m):
            aik = A[i][k]
            if aik:
                for j in range(p):
                    C[i][j] += aik * B[k][j]
    return C


def dec_transpose(A: List[List[Decimal]]) -> List[List[Decimal]]:
    return [list(row) for row in zip(*A)]


def dec_trace(A: List[List[Decimal]]) -> Decimal:
    return sum(A[i][i] for i in range(len(A)))


def dec_det3(M: List[List[Decimal]]) -> Decimal:
    return (
        M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
        - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
        + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0])
    )


def dec_inverse(A: List[List[Decimal]]) -> List[List[Decimal]]:
    n = len(A)
    M = [row[:] + eye for row, eye in zip([r[:] for r in A], dec_eye(n))]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        if M[piv][col] == 0:
            raise ZeroDivisionError("singular matrix")
        if piv != col:
            M[col], M[piv] = M[piv], M[col]
        pv = M[col][col]
        for j in range(2 * n):
            M[col][j] /= pv
        for i in range(n):
            if i == col:
                continue
            fac = M[i][col]
            if fac:
                for j in range(2 * n):
                    M[i][j] -= fac * M[col][j]
    return [row[n:] for row in M]


def dec_solve(A: List[List[Decimal]], b: List[Decimal]) -> List[Decimal]:
    n = len(A)
    M = [A[i][:] + [b[i]] for i in range(n)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        if M[piv][col] == 0:
            raise ZeroDivisionError("singular solve")
        if piv != col:
            M[col], M[piv] = M[piv], M[col]
        pv = M[col][col]
        for j in range(col, n + 1):
            M[col][j] /= pv
        for i in range(n):
            if i == col:
                continue
            fac = M[i][col]
            if fac:
                for j in range(col, n + 1):
                    M[i][j] -= fac * M[col][j]
    return [M[i][n] for i in range(n)]


def dec_ldl_pivots3(M: List[List[Decimal]]) -> List[Decimal]:
    # No-pivot LDL pivots for 3x3 symmetric positive definite matrices.
    d0 = M[0][0]
    l10 = M[1][0] / d0
    l20 = M[2][0] / d0
    d1 = M[1][1] - l10 * l10 * d0
    l21 = (M[2][1] - l20 * l10 * d0) / d1
    d2 = M[2][2] - l20 * l20 * d0 - l21 * l21 * d1
    return [d0, d1, d2]


def basis_mats_dec() -> List[List[List[Decimal]]]:
    out = []
    for k in range(6):
        M = dec_zero_matrix(3, 3)
        if k == 0:
            M[0][0] = Decimal(1)
        elif k == 1:
            M[1][1] = Decimal(1)
        elif k == 2:
            M[2][2] = Decimal(1)
        elif k == 3:
            M[0][1] = M[1][0] = Decimal(1)
        elif k == 4:
            M[0][2] = M[2][0] = Decimal(1)
        elif k == 5:
            M[1][2] = M[2][1] = Decimal(1)
        out.append(M)
    return out


BASIS_DEC = basis_mats_dec()


def atoms_and_grads_dec(K: List[List[Decimal]]) -> Tuple[List[Decimal], List[List[Decimal]]]:
    x, y, z = K[0][0], K[1][1], K[2][2]
    a, b, c = K[0][1], K[0][2], K[1][2]
    q12 = x * y - a * a
    q13 = x * z - b * b
    q23 = y * z - c * c
    r = x * y * z + 2 * a * b * c - x * c * c - y * b * b - z * a * a
    gq12 = [y, x, Decimal(0), -2 * a, Decimal(0), Decimal(0)]
    gq13 = [z, Decimal(0), x, Decimal(0), -2 * b, Decimal(0)]
    gq23 = [Decimal(0), z, y, Decimal(0), Decimal(0), -2 * c]
    gr = [
        y * z - c * c,
        x * z - b * b,
        x * y - a * a,
        2 * b * c - 2 * z * a,
        2 * a * c - 2 * y * b,
        2 * a * b - 2 * x * c,
    ]
    vals = [
        1 - x - y - z + q12 + q13 + q23 - r,
        x - q12 - q13 + r,
        y - q12 - q23 + r,
        z - q13 - q23 + r,
        q12 - r,
        q13 - r,
        q23 - r,
        r,
    ]
    g0_base = [Decimal(-1), Decimal(-1), Decimal(-1), Decimal(0), Decimal(0), Decimal(0)]
    g0 = [g0_base[i] + gq12[i] + gq13[i] + gq23[i] - gr[i] for i in range(6)]
    g1 = [(1 if i == 0 else 0) - gq12[i] - gq13[i] + gr[i] for i in range(6)]
    g2 = [(1 if i == 1 else 0) - gq12[i] - gq23[i] + gr[i] for i in range(6)]
    g3 = [(1 if i == 2 else 0) - gq13[i] - gq23[i] + gr[i] for i in range(6)]
    grads = [g0, g1, g2, g3, [gq12[i] - gr[i] for i in range(6)], [gq13[i] - gr[i] for i in range(6)], [gq23[i] - gr[i] for i in range(6)], gr]
    return vals, grads


def rho_decimal(K_values: Sequence[Sequence[Any]], dps: int = 120) -> Dict[str, Any]:
    with localcontext() as ctx:
        ctx.prec = dps
        K = [[D(K_values[i][j]) for j in range(3)] for i in range(3)]
        atoms, grads = atoms_and_grads_dec(K)
        if min(atoms) <= 0:
            return {"ok": False, "status": "nonpositive_atom_decimal"}
        p0, p1, p2, p3, p12, p13, p23, p123 = atoms
        l12 = (p0 * p12 / (p1 * p2)).ln()
        l13 = (p0 * p13 / (p1 * p3)).ln()
        l23 = (p0 * p23 / (p2 * p3)).ln()
        Lambda = (p123 * p1 * p2 * p3 / (p0 * p12 * p13 * p23)).ln()
        N = dec_zero_matrix(3, 3)
        N[0][0] = -l23
        N[1][1] = -l13
        N[2][2] = -l12
        for i in range(3):
            for j in range(3):
                N[i][j] -= Lambda * K[i][j]
        detN = dec_det3(N)
        Ninv = dec_inverse(N)
        F = dec_zero_matrix(6, 6)
        for s in range(8):
            for i in range(6):
                for j in range(6):
                    F[i][j] += grads[s][i] * grads[s][j] / atoms[s]
        G = dec_zero_matrix(6, 6)
        eta = [Decimal(0) for _ in range(6)]
        for i, Ei in enumerate(BASIS_DEC):
            eta[i] = dec_trace(dec_matmul(Ninv, Ei))
            for j, Ej in enumerate(BASIS_DEC):
                G[i][j] = dec_trace(dec_matmul(dec_matmul(dec_matmul(Ninv, Ei), Ninv), Ej))
        A = dec_zero_matrix(6, 6)
        for i in range(6):
            for j in range(6):
                A[i][j] = F[i][j] + detN * G[i][j]
        sol = dec_solve(A, eta)
        quad = sum(eta[i] * sol[i] for i in range(6))
        rho = detN * quad
        # Bad-direction entropy second derivative if rho crosses one.
        Hpp_bad = quad * (rho - Decimal(1))
        IminusK = dec_eye(3)
        for i in range(3):
            for j in range(3):
                IminusK[i][j] -= K[i][j]
        return {
            "ok": True,
            "status": "ok",
            "dps": dps,
            "rho": str(+rho),
            "one_minus_rho": str(+(Decimal(1) - rho)),
            "Hpp_bad_direction": str(+Hpp_bad),
            "Lambda": str(+Lambda),
            "detN": str(+detN),
            "min_atom": str(+min(atoms)),
            "min_atom_name": ATOM_NAMES[min(range(8), key=lambda i: atoms[i])],
            "atoms": {name: str(+atoms[i]) for i, name in enumerate(ATOM_NAMES)},
            "K_ldl_pivots": [str(+v) for v in dec_ldl_pivots3(K)],
            "I_minus_K_ldl_pivots": [str(+v) for v in dec_ldl_pivots3(IminusK)],
            "N_ldl_pivots": [str(+v) for v in dec_ldl_pivots3(N)],
            "bad_direction_coords": {name: str(+sol[i]) for i, name in enumerate(COORD_NAMES)},
        }


def rational_Q_decimal() -> List[List[Decimal]]:
    return [
        [Decimal(1) / 3, Decimal(2) / 3, Decimal(2) / 3],
        [Decimal(2) / 3, Decimal(1) / 3, -Decimal(2) / 3],
        [Decimal(2) / 3, -Decimal(2) / 3, Decimal(1) / 3],
    ]


def decimal_K_from_rational_Q(lam: Sequence[Decimal]) -> List[List[Decimal]]:
    Q = rational_Q_decimal()
    K = dec_zero_matrix(3, 3)
    for m in range(3):
        for i in range(3):
            for j in range(3):
                K[i][j] += lam[m] * Q[i][m] * Q[j][m]
    return K


def decimal_boundary_probes() -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    rates_list = [(1, 1), (1, 2), (1, 3), (2, 3), (1, 5), (2, 5), (1, 8)]
    theta_list = [Decimal(1) / 10, Decimal(1) / 2, Decimal(9) / 10, Decimal(99) / 100]
    k_list = [8, 16, 32, 64, 96]
    for theta in theta_list:
        for k in k_list:
            for rates in rates_list:
                r, s = rates
                dps = max(140, 2 * max(r, s) * k + 100)
                with localcontext() as ctx:
                    ctx.prec = dps
                    eps = Decimal(10) ** Decimal(-k)
                    lam = [eps ** r, eps ** s, theta]
                    K = decimal_K_from_rational_Q(lam)
                    for complement in [False, True]:
                        Kuse = K
                        if complement:
                            I = dec_eye(3)
                            Kuse = [[I[i][j] - K[i][j] for j in range(3)] for i in range(3)]
                        res = rho_decimal(Kuse, dps=dps)
                        res.update(
                            {
                                "route": "decimal_rank_one_rate_extremes",
                                "theta": str(theta),
                                "k": k,
                                "rates": list(rates),
                                "complement": complement,
                            }
                        )
                        out.append(res)
    return out


def decimal_near_disconnected_path_probes() -> List[Dict[str, Any]]:
    """High-precision path/near-disconnected probes with Lambda close to zero.

    K=diag(x,y,z)+eps*(s12*w12 E12+s23*w23 E23), K13=0 is connected for
    eps>0 but approaches a disconnected diagonal/factored kernel.  Float rho is
    particularly unreliable here because N can be extremely small.
    """
    out: List[Dict[str, Any]] = []
    diag_list = [
        (Decimal(12) / 100, Decimal(1) / 2, Decimal(88) / 100),
        (Decimal(8) / 100, Decimal(31) / 100, Decimal(79) / 100),
        (Decimal(1) / 4, Decimal(37) / 100, Decimal(62) / 100),
        (Decimal(91) / 100, Decimal(64) / 100, Decimal(21) / 100),
        (Decimal(48) / 100, Decimal(51) / 100, Decimal(55) / 100),
    ]
    weights = [
        (Decimal(1), Decimal(1)),
        (Decimal(1), -Decimal(1)),
        (Decimal(3) / 10, Decimal(1)),
        (Decimal(1), Decimal(3) / 10),
        (Decimal(1), Decimal(1) / 100),
    ]
    k_list = [2, 4, 8, 16, 32, 48]
    for did, diag in enumerate(diag_list):
        for wid, (w12, w23) in enumerate(weights):
            for k in k_list:
                dps = max(180, 10 * k + 140)
                with localcontext() as ctx:
                    ctx.prec = dps
                    eps = Decimal(10) ** Decimal(-k)
                    K = dec_zero_matrix(3, 3)
                    for i in range(3):
                        K[i][i] = diag[i]
                    K[0][1] = K[1][0] = eps * w12
                    K[1][2] = K[2][1] = eps * w23
                    try:
                        # Decimal LDL screens strict feasibility before logs.
                        IminusK = dec_eye(3)
                        for i in range(3):
                            for j in range(3):
                                IminusK[i][j] -= K[i][j]
                        if min(dec_ldl_pivots3(K)) <= 0 or min(dec_ldl_pivots3(IminusK)) <= 0:
                            out.append(
                                {
                                    "ok": False,
                                    "status": "not_strict_decimal",
                                    "route": "decimal_lambda0_near_disconnected_paths",
                                    "diag_id": did,
                                    "weight_id": wid,
                                    "k": k,
                                }
                            )
                            continue
                        res = rho_decimal(K, dps=dps)
                    except Exception as exc:  # retained in ledger, not hidden
                        res = {"ok": False, "status": type(exc).__name__, "error": str(exc)}
                    res.update(
                        {
                            "route": "decimal_lambda0_near_disconnected_paths",
                            "diag": [str(v) for v in diag],
                            "weights": [str(w12), str(w23)],
                            "diag_id": did,
                            "weight_id": wid,
                            "k": k,
                        }
                    )
                    out.append(res)
    return out


def serialize_top_for_decimal(top: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    rechecked: List[Dict[str, Any]] = []
    seen = set()
    for idx, rec in enumerate(top[:30]):
        Ktuple = tuple(round(float(x), 16) for row in rec["K"] for x in row)
        if Ktuple in seen:
            continue
        seen.add(Ktuple)
        dps = 140
        # Increase precision when atoms or spectral margins are very small.
        floor = min(rec["min_atom"], rec["eigmin_K"], rec["eigmin_IK"], rec["min_eig_N"])
        if floor > 0:
            dps = max(dps, min(500, int(-math.log10(floor)) * 6 + 120))
        res = rho_decimal(rec["K"], dps=dps)
        res.update(
            {
                "source_rank_float": idx,
                "source_route": rec["route"],
                "source_rho_float": rec["rho_float"],
                "source_one_minus_rho_float": rec["one_minus_rho_float"],
                "source_min_atom": rec["min_atom"],
                "source_min_atom_name": rec["min_atom_name"],
                "source_eigmin_K": rec["eigmin_K"],
                "source_eigmin_IK": rec["eigmin_IK"],
                "K": rec["K"],
            }
        )
        rechecked.append(res)
    return rechecked


def compact_route_stats(stats: Dict[str, Dict[str, int]]) -> Dict[str, Dict[str, Any]]:
    out = {}
    for route, counts in stats.items():
        attempted = sum(counts.values())
        ok = counts.get("ok", 0)
        out[route] = {
            "attempted": attempted,
            "accepted": ok,
            "rejected": attempted - ok,
            "reject_breakdown": {k: v for k, v in sorted(counts.items()) if k != "ok"},
        }
    return out


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--skip-decimal-boundary", action="store_true")
    args = parser.parse_args(argv)

    random.seed(args.seed)
    rng = np.random.default_rng(args.seed)
    started = time.time()
    rec = Recorder()

    scan_L_atom_boundaries(rec, rng)
    scan_rank_one_rates(rec)
    scan_edge_boundaries(rec)
    scan_spectral_corners(rec, rng)
    random_interior_targeted(rec, rng)
    local_hill_from_top(rec, rng)

    decimal_rechecks = serialize_top_for_decimal(rec.best)
    dec_boundary = [] if args.skip_decimal_boundary else decimal_boundary_probes()
    dec_lambda0 = [] if args.skip_decimal_boundary else decimal_near_disconnected_path_probes()

    decimal_all = decimal_rechecks + dec_boundary + dec_lambda0
    positives_decimal = []
    near_decimal = []
    for item in decimal_all:
        if not item.get("ok"):
            continue
        rho = Decimal(item["rho"])
        if rho > 1:
            positives_decimal.append(item)
        if rho > Decimal("0.95"):
            near_decimal.append(item)
    near_decimal.sort(key=lambda x: Decimal(x["rho"]), reverse=True)
    positives_decimal.sort(key=lambda x: Decimal(x["rho"]), reverse=True)

    best_float = rec.best[0] if rec.best else None
    elapsed = time.time() - started
    ledger = {
        "status": "SCOUT_NO_RHO_GT_1" if not positives_decimal and (best_float is None or best_float["rho_float"] <= 1.0) else "FLOAT_OR_DECIMAL_POSITIVE_REQUIRES_GATE",
        "seed": args.seed,
        "elapsed_seconds": elapsed,
        "script": str(Path(__file__).name),
        "script_sha256": sha256_file(Path(__file__).resolve()),
        "attempted_float_total": rec.attempted,
        "accepted_float_total": rec.accepted,
        "route_stats": compact_route_stats(rec.stats),
        "small_atom_threshold": 1e-8,
        "small_atom_hit_counts": rec.small_atom_hits,
        "top_float": rec.best[:25],
        "decimal_recheck_count": len(decimal_rechecks),
        "decimal_boundary_probe_count": len(dec_boundary),
        "decimal_lambda0_path_probe_count": len(dec_lambda0),
        "decimal_near_threshold_count": len(near_decimal),
        "decimal_positive_count": len(positives_decimal),
        "decimal_top_float_rechecks": decimal_rechecks,
        "best_decimal_near_threshold": near_decimal[:20],
    }
    candidates = {
        "positive_candidates_rho_gt_1": positives_decimal,
        "near_threshold_candidates": near_decimal[:40],
        "top_float_decimal_rechecks": decimal_rechecks,
        "lambda0_path_decimal_probes": dec_lambda0,
        "top_float_candidates": rec.best[:40],
        "notes": [
            "Finite search only; no theorem or global upper bound is claimed.",
            "No author U8 gate/search module is imported.",
            "Decimal probes are high-precision recomputations of selected float seeds and fixed rational-Q boundary families, not interval certificates unless explicitly marked otherwise.",
        ],
    }

    (BASE / "search_ledger.json").write_text(json.dumps(ledger, indent=2, sort_keys=True), encoding="utf-8")
    (BASE / "near_threshold_candidates.json").write_text(json.dumps(candidates, indent=2, sort_keys=True), encoding="utf-8")
    run_log = [
        "# D10-U10c scalar falsification run log",
        "",
        f"Command: `{Path(sys.executable)} {Path(__file__).name}`",
        f"Seed: `{args.seed}`",
        f"Exit code: `0`",
        f"Elapsed seconds: `{elapsed:.6f}`",
        f"Float attempts: `{rec.attempted}`",
        f"Float accepted strict connected cases: `{rec.accepted}`",
        f"Decimal top rechecks: `{len(decimal_rechecks)}`",
        f"Decimal rank-one-rate boundary probes: `{len(dec_boundary)}`",
        f"Decimal Lambda≈0 path probes: `{len(dec_lambda0)}`",
        f"Decimal rho>1 count: `{len(positives_decimal)}`",
    ]
    if best_float:
        run_log.append(f"Best float rho: `{best_float['rho_float']:.17g}` on route `{best_float['route']}`")
        run_log.append(f"Best float min atom: `{best_float['min_atom']:.17g}` (`{best_float['min_atom_name']}`)")
        run_log.append(f"Best float eig margins K/I-K: `{best_float['eigmin_K']:.17g}`, `{best_float['eigmin_IK']:.17g}`")
    if near_decimal:
        run_log.append(f"Best Decimal rho: `{near_decimal[0]['rho']}`")
        run_log.append(f"Best Decimal one_minus_rho: `{near_decimal[0]['one_minus_rho']}`")
    run_log.append("")
    run_log.append("This is a SCOUT ledger unless a rho>1 item subsequently passes a rational/interval admissibility gate.")
    (BASE / "run_log.md").write_text("\n".join(run_log) + "\n", encoding="utf-8")

    print(json.dumps({"status": ledger["status"], "attempted": rec.attempted, "accepted": rec.accepted, "best_float_rho": None if best_float is None else best_float["rho_float"], "decimal_positive_count": len(positives_decimal), "elapsed_seconds": elapsed}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
