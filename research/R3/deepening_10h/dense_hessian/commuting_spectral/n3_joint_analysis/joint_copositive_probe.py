#!/usr/bin/env python3
"""D10-M6 n=3 joint singleton/pair curvature probe.

This is an author-side scout, not a certificate of a theorem.  It uses the
already-derived n=3 fixed-Q spectral-channel formulas

    H(Y) = H(|Y|) + G_P(r) + G_P(s),  P_{ai}=q_{ai}^2,

and, for every sampled strict base point (theta, Q), reconstructs the full
quadratic form v -> H''(theta; v).  It then searches the positive cone by
combining a repaired positive-simplex KKT enumeration with an independent
positive-sphere support-eigenvector sign gate.  This is still a floating scout
over sampled (theta, Q), not a theorem over the continuous base domain.
"""

from __future__ import annotations

import hashlib
import json
import math
import time
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path

import numpy as np


SEED = 2026090836
RANDOM_BASE_POINTS = 60_000
STRUCTURED_BASE_POINTS = 384
STRICT_CLIP = 1.0e-5
POSITIVE_TOL = 1.0e-10
SIMPLEX_KKT_ABS_TOL = 1.0e-9
SIMPLEX_KKT_REL_TOL = 1.0e-10


def random_orthogonal(rng: np.random.Generator) -> np.ndarray:
    """Haar-ish 3x3 orthogonal matrix with deterministic sign convention."""
    a = rng.normal(size=(3, 3))
    q, r = np.linalg.qr(a)
    signs = np.sign(np.diag(r))
    signs[signs == 0.0] = 1.0
    q = q * signs
    if np.linalg.det(q) < 0.0:
        q[:, 0] *= -1.0
    return q


def rotation12(angle: float) -> np.ndarray:
    c = math.cos(angle)
    s = math.sin(angle)
    return np.array([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]])


def rotation13(angle: float) -> np.ndarray:
    c = math.cos(angle)
    s = math.sin(angle)
    return np.array([[c, 0.0, -s], [0.0, 1.0, 0.0], [s, 0.0, c]])


def rotation23(angle: float) -> np.ndarray:
    c = math.cos(angle)
    s = math.sin(angle)
    return np.array([[1.0, 0.0, 0.0], [0.0, c, -s], [0.0, s, c]])


def structured_orthogonals() -> list[np.ndarray]:
    angles = [
        0.0,
        math.asin(1.0 / 3.0),
        math.asin(3.0 / 5.0),
        math.pi / 4.0,
        math.asin(4.0 / 5.0),
        math.pi / 2.0,
    ]
    out: list[np.ndarray] = []
    for a in angles:
        for b in angles:
            for c in angles:
                out.append(rotation12(a) @ rotation13(b) @ rotation23(c))
                out.append(rotation23(c) @ rotation13(b) @ rotation12(a))
    return out


def theta_samples(rng: np.random.Generator):
    """Mixture of interior and near-boundary strict theta samples."""
    modes = rng.integers(0, 4, size=RANDOM_BASE_POINTS)
    for mode in modes:
        if mode == 0:
            theta = rng.uniform(0.03, 0.97, size=3)
        elif mode == 1:
            theta = rng.beta(0.45, 0.45, size=3)
        elif mode == 2:
            theta = rng.beta(1.8, 1.8, size=3)
        else:
            # One coordinate deliberately close to a face, but still strict.
            theta = rng.uniform(0.08, 0.92, size=3)
            j = int(rng.integers(0, 3))
            theta[j] = 10.0 ** rng.uniform(-4.5, -1.0)
            if rng.random() < 0.5:
                theta[j] = 1.0 - theta[j]
        yield np.clip(theta, STRICT_CLIP, 1.0 - STRICT_CLIP)


def monomial_derivatives(theta: np.ndarray, v: np.ndarray, use_theta: tuple[bool, bool, bool]):
    vals = np.array(
        [theta[i] if use_theta[i] else 1.0 - theta[i] for i in range(3)],
        dtype=float,
    )
    ders = np.array(
        [v[i] if use_theta[i] else -v[i] for i in range(3)],
        dtype=float,
    )
    m = float(vals[0] * vals[1] * vals[2])
    mp = float(
        ders[0] * vals[1] * vals[2]
        + vals[0] * ders[1] * vals[2]
        + vals[0] * vals[1] * ders[2]
    )
    mpp = float(
        2.0
        * (
            ders[0] * ders[1] * vals[2]
            + ders[0] * vals[1] * ders[2]
            + vals[0] * ders[1] * ders[2]
        )
    )
    return m, mp, mpp


def layer_derivatives(theta: np.ndarray, v: np.ndarray):
    empty = monomial_derivatives(theta, v, (False, False, False))
    full = monomial_derivatives(theta, v, (True, True, True))

    r = []
    rp = []
    rpp = []
    s = []
    sp = []
    spp = []
    for i in range(3):
        r_mask = tuple(j == i for j in range(3))
        s_mask = tuple(j != i for j in range(3))
        a, b, c = monomial_derivatives(theta, v, r_mask)
        r.append(a)
        rp.append(b)
        rpp.append(c)
        a, b, c = monomial_derivatives(theta, v, s_mask)
        s.append(a)
        sp.append(b)
        spp.append(c)

    return (
        empty,
        np.array(r),
        np.array(rp),
        np.array(rpp),
        np.array(s),
        np.array(sp),
        np.array(spp),
        full,
    )


def entropy_second_from_derivatives(p: np.ndarray, p1: np.ndarray, p2: np.ndarray) -> float:
    if np.min(p) <= 0.0:
        raise ValueError("non-positive atom in strict probe")
    # sum p2 is zero analytically; this formula keeps the finite exact-event
    # Hessian convention H'' = -Σ p'^2/p - Σ p'' log p.
    return float(-np.sum((p1 * p1) / p) - np.sum(p2 * np.log(p)))


def g_second(P: np.ndarray, x: np.ndarray, x1: np.ndarray, x2: np.ndarray) -> float:
    y = P @ x
    y1 = P @ x1
    y2 = P @ x2
    pi = float(np.sum(x))
    pi1 = float(np.sum(x1))
    if np.min(y) <= 0.0 or pi <= 0.0:
        raise ValueError("non-positive conditional layer")
    return float(
        -np.sum((y1 * y1) / y)
        + (pi1 * pi1) / pi
        - np.sum(y2 * np.log(y / pi))
    )


def h2_components(theta: np.ndarray, v: np.ndarray, Q: np.ndarray):
    P = Q * Q
    empty, r, rp, rpp, s, sp, spp, full = layer_derivatives(theta, v)
    e0, e1, e2 = empty
    f0, f1, f2 = full
    y = P @ r
    y1 = P @ rp
    y2 = P @ rpp
    z = P @ s
    z1 = P @ sp
    z2 = P @ spp

    p = np.concatenate(([e0], y, z, [f0]))
    p1 = np.concatenate(([e1], y1, z1, [f1]))
    p2 = np.concatenate(([e2], y2, z2, [f2]))
    total = entropy_second_from_derivatives(p, p1, p2)

    pi = np.array([e0, float(np.sum(r)), float(np.sum(s)), f0])
    pi1 = np.array([e1, float(np.sum(rp)), float(np.sum(sp)), f1])
    pi2 = np.array([e2, float(np.sum(rpp)), float(np.sum(spp)), f2])
    count = entropy_second_from_derivatives(pi, pi1, pi2)
    singleton = g_second(P, r, rp, rpp)
    pair = g_second(P, s, sp, spp)
    return {
        "total": total,
        "count": count,
        "psi": singleton + pair,
        "singleton": singleton,
        "pair": pair,
        "min_atom": float(np.min(p)),
        "sum_p": float(np.sum(p)),
        "sum_p1": float(np.sum(p1)),
        "sum_p2": float(np.sum(p2)),
    }


def theta_hessian(theta: np.ndarray, Q: np.ndarray, key: str = "total") -> np.ndarray:
    basis = [np.eye(3)[i] for i in range(3)]
    diag = [h2_components(theta, b, Q)[key] for b in basis]
    H = np.zeros((3, 3), dtype=float)
    for i in range(3):
        H[i, i] = diag[i]
    for i, j in combinations(range(3), 2):
        hij_sum = h2_components(theta, basis[i] + basis[j], Q)[key]
        H[i, j] = H[j, i] = 0.5 * (hij_sum - H[i, i] - H[j, j])
    return H


def _add_simplex_candidate(candidates: list[np.ndarray], idx: list[int], loc: np.ndarray):
    if np.all(np.isfinite(loc)) and np.all(loc >= -1e-9):
        v = np.zeros(3)
        v[idx] = np.maximum(loc, 0.0)
        total = float(np.sum(v))
        if total > 0.0:
            v = v / total
            if not any(np.linalg.norm(v - old) < 1e-9 for old in candidates):
                candidates.append(v)


def _kkt_residual_ok(kkt: np.ndarray, sol: np.ndarray, rhs: np.ndarray):
    residual = float(np.linalg.norm(kkt @ sol - rhs, ord=np.inf))
    scale = max(
        1.0,
        float(np.linalg.norm(kkt, ord=np.inf)) * max(1.0, float(np.linalg.norm(sol, ord=np.inf))),
        float(np.linalg.norm(rhs, ord=np.inf)),
    )
    ok = residual <= SIMPLEX_KKT_ABS_TOL + SIMPLEX_KKT_REL_TOL * scale
    return ok, residual, scale


def max_quadratic_on_simplex(M: np.ndarray):
    """Return a repaired KKT scout for max v^T M v on the positive simplex.

    The previous version skipped singular full-support KKT systems.  This
    version solves the augmented KKT equations by least squares on every face,
    checks scale-aware residuals, and keeps explicit edge candidates.
    Degenerate affine families are still treated as floating scout data, so
    documentation must not advertise this routine as a formal exact optimizer
    for arbitrary symmetric 3x3 matrices.
    """
    best_val = -float("inf")
    best_v = None
    candidates = []
    for mask in range(1, 1 << 3):
        idx = [i for i in range(3) if (mask >> i) & 1]
        if len(idx) == 1:
            v = np.zeros(3)
            v[idx[0]] = 1.0
            candidates.append(v)
            continue
        A = M[np.ix_(idx, idx)]
        ones = np.ones(len(idx))
        kkt = np.zeros((len(idx) + 1, len(idx) + 1))
        kkt[: len(idx), : len(idx)] = 2.0 * A
        kkt[: len(idx), -1] = -1.0
        kkt[-1, : len(idx)] = 1.0
        rhs = np.zeros(len(idx) + 1)
        rhs[-1] = 1.0
        sol, *_ = np.linalg.lstsq(kkt, rhs, rcond=None)
        ok, _residual, _scale = _kkt_residual_ok(kkt, sol, rhs)
        if ok:
            _add_simplex_candidate(candidates, idx, sol[: len(idx)])

        if len(idx) == 2:
            i, j = idx
            a = M[i, i] - 2.0 * M[i, j] + M[j, j]
            b = 2.0 * (M[i, j] - M[j, j])
            if a < -1e-14:
                t = -b / (2.0 * a)
                if -1e-10 <= t <= 1.0 + 1e-10:
                    t = min(1.0, max(0.0, t))
                    v = np.zeros(3)
                    v[i] = t
                    v[j] = 1.0 - t
                    _add_simplex_candidate(candidates, idx, np.array([t, 1.0 - t]))

    for v in candidates:
        val = float(v @ M @ v)
        if val > best_val:
            best_val = val
            best_v = v.copy()
    return best_val, best_v


def support_sphere_candidates(M: np.ndarray):
    """Same-sign principal-submatrix eigenvectors on the positive sphere."""
    candidates: list[np.ndarray] = []
    for mask in range(1, 1 << 3):
        idx = [i for i in range(3) if (mask >> i) & 1]
        A = M[np.ix_(idx, idx)]
        _vals, vecs = np.linalg.eigh(A)
        for col in range(vecs.shape[1]):
            loc = vecs[:, col]
            if np.all(loc >= -1e-10) or np.all(loc <= 1e-10):
                loc = np.abs(loc)
                norm = float(np.linalg.norm(loc))
                if norm > 0.0:
                    v = np.zeros(3)
                    v[idx] = loc / norm
                    if not any(np.linalg.norm(v - old) < 1e-9 for old in candidates):
                        candidates.append(v)
    return candidates


def max_quadratic_on_positive_sphere(M: np.ndarray):
    best_val = -float("inf")
    best_v = None
    candidates = support_sphere_candidates(M)
    for v in candidates:
        val = float(v @ M @ v)
        if val > best_val:
            best_val = val
            best_v = v.copy()
    return best_val, best_v, len(candidates)


def copositive_margins_for_negative_hessian(M: np.ndarray):
    """Margins for C=-M to be copositive on R_+^3."""
    C = -0.5 * (M + M.T)
    diag = np.diag(C)
    min_diag = float(np.min(diag))
    if min_diag < 0:
        return {
            "min_diag": min_diag,
            "min_bar": None,
            "final_margin": None,
            "criterion_pass": False,
        }
    bars = []
    for i, j in combinations(range(3), 2):
        bars.append(float(C[i, j] + math.sqrt(max(0.0, C[i, i] * C[j, j]))))
    min_bar = float(min(bars))
    if min_bar < 0:
        return {
            "min_diag": min_diag,
            "min_bar": min_bar,
            "final_margin": None,
            "criterion_pass": False,
        }
    b12, b13, b23 = bars
    final = (
        math.sqrt(max(0.0, C[0, 0] * C[1, 1] * C[2, 2]))
        + C[0, 1] * math.sqrt(max(0.0, C[2, 2]))
        + C[0, 2] * math.sqrt(max(0.0, C[1, 1]))
        + C[1, 2] * math.sqrt(max(0.0, C[0, 0]))
        + math.sqrt(max(0.0, 2.0 * b12 * b13 * b23))
    )
    return {
        "min_diag": min_diag,
        "min_bar": min_bar,
        "final_margin": float(final),
        "criterion_pass": bool(final >= -5e-9),
    }


def direct_mobius_atoms(K: np.ndarray) -> np.ndarray:
    """Exact-event atoms ordered as masks 0..7 from inclusion determinants."""
    n = K.shape[0]
    inc = np.zeros(1 << n)
    for mask in range(1 << n):
        idx = [i for i in range(n) if (mask >> i) & 1]
        if not idx:
            inc[mask] = 1.0
        else:
            inc[mask] = float(np.linalg.det(K[np.ix_(idx, idx)]))
    atoms = np.zeros(1 << n)
    for S in range(1 << n):
        total = 0.0
        rest = ((1 << n) - 1) ^ S
        T = rest
        while True:
            A = S | T
            total += ((-1.0) ** (T.bit_count())) * inc[A]
            if T == 0:
                break
            T = (T - 1) & rest
        atoms[S] = total
    return atoms


def channel_atoms(theta: np.ndarray, Q: np.ndarray) -> np.ndarray:
    P = Q * Q
    v0 = np.zeros(3)
    empty, r, _rp, _rpp, s, _sp, _spp, full = layer_derivatives(theta, v0)
    atoms = np.zeros(8)
    atoms[0] = empty[0]
    # singleton mask 1<<a has probability (P r)_a
    y = P @ r
    for a in range(3):
        atoms[1 << a] = y[a]
    z = P @ s
    full_mask = 7
    for a in range(3):
        atoms[full_mask ^ (1 << a)] = z[a]
    atoms[full_mask] = full[0]
    return atoms


def sanity_checks():
    """Independent checks against direct Möbius atoms and finite differences."""
    q = rotation12(math.asin(3.0 / 5.0)) @ rotation13(math.asin(5.0 / 13.0)) @ rotation23(
        math.asin(8.0 / 17.0)
    )
    theta = np.array([0.23, 0.57, 0.81])
    v = np.array([0.04, 0.07, 0.02])
    K = q @ np.diag(theta) @ q.T
    atoms_mobius = direct_mobius_atoms(K)
    atoms_channel = channel_atoms(theta, q)
    atom_err = float(np.max(np.abs(atoms_mobius - atoms_channel)))

    h = 1e-5

    def entropy_at(th):
        return float(-np.sum(channel_atoms(th, q) * np.log(channel_atoms(th, q))))

    second_fd = (entropy_at(theta + h * v) - 2.0 * entropy_at(theta) + entropy_at(theta - h * v)) / (
        h * h
    )
    exact_h2 = h2_components(theta, v, q)["total"]
    fd_err = float(abs(second_fd - exact_h2))
    return {
        "mobius_channel_max_abs_atom_error": atom_err,
        "finite_difference_second": float(second_fd),
        "formula_second": float(exact_h2),
        "finite_difference_abs_error": fd_err,
        "theta": theta.tolist(),
        "v": v.tolist(),
    }


def optimizer_regression_checks():
    singular_zero_matrix = np.array(
        [
            [-2.0, 1.0, 1.0],
            [1.0, -2.0, 1.0],
            [1.0, 1.0, -2.0],
        ]
    )
    scaled_positive_matrix = 1.0e14 * np.array(
        [
            [-10.0, 6.0, 6.0],
            [6.0, -10.0, 6.0],
            [6.0, 6.0, -10.0],
        ]
    )
    simplex_value, simplex_v = max_quadratic_on_simplex(singular_zero_matrix)
    sphere_value, sphere_v, sphere_candidates = max_quadratic_on_positive_sphere(singular_zero_matrix)
    scaled_simplex_value, scaled_simplex_v = max_quadratic_on_simplex(scaled_positive_matrix)
    scaled_sphere_value, scaled_sphere_v, scaled_sphere_candidates = max_quadratic_on_positive_sphere(
        scaled_positive_matrix
    )
    scaled_expected_simplex = 2.0e14 / 3.0
    scaled_expected_sphere = 2.0e14
    return {
        "singular_zero_matrix": {
            "matrix": singular_zero_matrix.tolist(),
            "expected_simplex_maximum": 0.0,
            "expected_sphere_maximum": 0.0,
            "simplex_value": float(simplex_value),
            "simplex_v": simplex_v.tolist(),
            "sphere_value": float(sphere_value),
            "sphere_v": sphere_v.tolist(),
            "sphere_candidates": sphere_candidates,
            "simplex_pass": bool(abs(simplex_value) <= 1e-10),
            "sphere_pass": bool(abs(sphere_value) <= 1e-10),
        },
        "scaled_positive_matrix": {
            "matrix_scale": 1.0e14,
            "expected_simplex_maximum": scaled_expected_simplex,
            "expected_sphere_maximum": scaled_expected_sphere,
            "simplex_value": float(scaled_simplex_value),
            "simplex_v": scaled_simplex_v.tolist(),
            "sphere_value": float(scaled_sphere_value),
            "sphere_v": scaled_sphere_v.tolist(),
            "sphere_candidates": scaled_sphere_candidates,
            "simplex_relative_error": float(
                abs(scaled_simplex_value - scaled_expected_simplex) / scaled_expected_simplex
            ),
            "sphere_relative_error": float(
                abs(scaled_sphere_value - scaled_expected_sphere) / scaled_expected_sphere
            ),
            "simplex_pass": bool(
                abs(scaled_simplex_value - scaled_expected_simplex)
                <= 1.0e-10 * scaled_expected_simplex
            ),
            "sphere_pass": bool(
                abs(scaled_sphere_value - scaled_expected_sphere)
                <= 1.0e-10 * scaled_expected_sphere
            ),
        },
    }


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@dataclass
class BestRecord:
    value: float
    theta: list[float] | None = None
    Q: list[list[float]] | None = None
    v: list[float] | None = None
    components: dict | None = None
    hessian: list[list[float]] | None = None
    copositive_margins: dict | None = None

    def update(self, value: float, theta: np.ndarray, Q: np.ndarray, v: np.ndarray, M: np.ndarray):
        if value > self.value:
            self.value = float(value)
            self.theta = theta.tolist()
            self.Q = Q.tolist()
            self.v = v.tolist()
            self.components = h2_components(theta, v, Q)
            self.hessian = M.tolist()
            self.copositive_margins = copositive_margins_for_negative_hessian(M)


def scan():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    best_total = BestRecord(value=-float("inf"))
    best_psi = BestRecord(value=-float("inf"))
    best_singleton = BestRecord(value=-float("inf"))
    best_pair = BestRecord(value=-float("inf"))
    min_copositive_final = {
        "value": float("inf"),
        "theta": None,
        "Q": None,
        "hessian": None,
        "margins": None,
    }
    positive_total_candidates = []
    copositive_mismatches = []
    sphere_positive_gate_hits = []
    sphere_candidate_vectors = 0

    base_count = 0
    all_Q = structured_orthogonals()
    structured_thetas = [
        np.array(x)
        for x in [
            (0.5, 0.5, 0.5),
            (0.2, 0.2, 0.8),
            (0.2, 0.8, 0.8),
            (0.1, 0.4, 0.9),
            (0.01, 0.2, 0.8),
            (0.001, 0.5, 0.999),
            (0.03, 0.57, 0.91),
            (0.17, 0.41, 0.73),
        ]
    ]

    for Q in all_Q[: STRUCTURED_BASE_POINTS // len(structured_thetas)]:
        for theta in structured_thetas:
            base_count += 1
            M = theta_hessian(theta, Q, "total")
            max_total, v_total = max_quadratic_on_simplex(M)
            max_sphere, v_sphere, n_sphere = max_quadratic_on_positive_sphere(M)
            sphere_candidate_vectors += n_sphere
            best_total.update(max_total, theta, Q, v_total, M)
            margins = copositive_margins_for_negative_hessian(M)
            if margins["final_margin"] is not None and margins["final_margin"] < min_copositive_final["value"]:
                min_copositive_final = {
                    "value": margins["final_margin"],
                    "theta": theta.tolist(),
                    "Q": Q.tolist(),
                    "hessian": M.tolist(),
                    "margins": margins,
                }
            if max_total > POSITIVE_TOL:
                positive_total_candidates.append(
                    {
                        "source": "structured",
                        "max_total": float(max_total),
                        "theta": theta.tolist(),
                        "v": v_total.tolist(),
                        "Q": Q.tolist(),
                        "components": h2_components(theta, v_total, Q),
                        "hessian": M.tolist(),
                    }
                )
                break
            if max_sphere > POSITIVE_TOL:
                sphere_positive_gate_hits.append(
                    {
                        "source": "structured",
                        "max_sphere": float(max_sphere),
                        "theta": theta.tolist(),
                        "v": v_sphere.tolist(),
                        "Q": Q.tolist(),
                        "components": h2_components(theta, v_sphere, Q),
                        "hessian": M.tolist(),
                    }
                )
                break
        if positive_total_candidates or sphere_positive_gate_hits:
            break

    if not positive_total_candidates and not sphere_positive_gate_hits:
        for theta in theta_samples(rng):
            Q = random_orthogonal(rng)
            base_count += 1
            M_total = theta_hessian(theta, Q, "total")
            max_total, v_total = max_quadratic_on_simplex(M_total)
            max_sphere, v_sphere, n_sphere = max_quadratic_on_positive_sphere(M_total)
            sphere_candidate_vectors += n_sphere
            best_total.update(max_total, theta, Q, v_total, M_total)

            M_psi = theta_hessian(theta, Q, "psi")
            max_psi, v_psi = max_quadratic_on_simplex(M_psi)
            best_psi.update(max_psi, theta, Q, v_psi, M_psi)

            M_singleton = theta_hessian(theta, Q, "singleton")
            max_singleton, v_singleton = max_quadratic_on_simplex(M_singleton)
            best_singleton.update(max_singleton, theta, Q, v_singleton, M_singleton)

            M_pair = theta_hessian(theta, Q, "pair")
            max_pair, v_pair = max_quadratic_on_simplex(M_pair)
            best_pair.update(max_pair, theta, Q, v_pair, M_pair)

            margins = copositive_margins_for_negative_hessian(M_total)
            if margins["final_margin"] is not None and margins["final_margin"] < min_copositive_final["value"]:
                min_copositive_final = {
                    "value": margins["final_margin"],
                    "theta": theta.tolist(),
                    "Q": Q.tolist(),
                    "hessian": M_total.tolist(),
                    "margins": margins,
                }
            criterion_says_pass = bool(margins["criterion_pass"])
            simplex_says_pass = bool(max_total <= 5e-8)
            if criterion_says_pass != simplex_says_pass and len(copositive_mismatches) < 10:
                copositive_mismatches.append(
                    {
                        "theta": theta.tolist(),
                        "Q": Q.tolist(),
                        "max_total_simplex": float(max_total),
                        "v": v_total.tolist(),
                        "hessian": M_total.tolist(),
                        "margins": margins,
                    }
                )
            if max_total > POSITIVE_TOL:
                positive_total_candidates.append(
                    {
                        "source": "random",
                        "base_index": base_count,
                        "max_total": float(max_total),
                        "theta": theta.tolist(),
                        "v": v_total.tolist(),
                        "Q": Q.tolist(),
                        "components": h2_components(theta, v_total, Q),
                        "hessian": M_total.tolist(),
                        "copositive_margins": margins,
                    }
                )
                break
            if max_sphere > POSITIVE_TOL:
                sphere_positive_gate_hits.append(
                    {
                        "source": "random",
                        "base_index": base_count,
                        "max_sphere": float(max_sphere),
                        "theta": theta.tolist(),
                        "v": v_sphere.tolist(),
                        "Q": Q.tolist(),
                        "components": h2_components(theta, v_sphere, Q),
                        "hessian": M_total.tolist(),
                        "copositive_margins": margins,
                    }
                )
                break

    return {
        "status": "POSITIVE_FOUND" if (positive_total_candidates or sphere_positive_gate_hits) else "SCOUT_NO_POSITIVE_FOUND",
        "result_version": "v3_relative_kkt_scaled_regression",
        "script_sha256": file_sha256(Path(__file__)),
        "seed": SEED,
        "random_base_points_requested": RANDOM_BASE_POINTS,
        "structured_base_points_requested": STRUCTURED_BASE_POINTS,
        "base_points_checked": base_count,
        "positive_tolerance": POSITIVE_TOL,
        "strict_clip": STRICT_CLIP,
        "events_per_direction": 8,
        "directions_per_total_hessian": 6,
        "simplex_optimizer_note": "repaired singular KKT scout with relative residual checks; not a formal proof optimizer for arbitrary degenerate 3x3 matrices",
        "sphere_positive_gate": "principal-submatrix same-sign eigenvector enumeration on v_i>=0, ||v||_2=1",
        "sphere_candidate_vectors_evaluated": sphere_candidate_vectors,
        "total_direction_cone": "v_i >= 0, normalized by sum_i v_i = 1",
        "sanity_checks": sanity_checks(),
        "optimizer_regression_checks": optimizer_regression_checks(),
        "best_total_simplex": best_total.__dict__,
        "best_psi_simplex": best_psi.__dict__,
        "best_singleton_layer_simplex": best_singleton.__dict__,
        "best_pair_layer_simplex": best_pair.__dict__,
        "min_copositive_final_margin": min_copositive_final,
        "copositive_mismatches": copositive_mismatches,
        "positive_total_candidates": positive_total_candidates[:3],
        "sphere_positive_gate_hits": sphere_positive_gate_hits[:3],
        "runtime_seconds": time.time() - t0,
    }


def main():
    result = scan()
    out = Path(__file__).with_name("joint_probe_results_v3.json")
    out.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] == "POSITIVE_FOUND":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
