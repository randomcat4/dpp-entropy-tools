#!/usr/bin/env python3
"""Independent n=3 formula checks for the N3 review lane.

The script intentionally rebuilds the event probabilities and their six
coordinate jets from the exact Mobius event definition.  The six coordinates
are (11, 22, 33, 12, 13, 23), where an off-diagonal coordinate means the
real-symmetric direction E_ij + E_ji.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import platform
import subprocess
import sys
from fractions import Fraction
from itertools import combinations
from pathlib import Path

import numpy as np


ORDER = [(), (0,), (1,), (2,), (0, 1), (0, 2), (1, 2), (0, 1, 2)]
ORDER_NAMES = ["empty", "1", "2", "3", "12", "13", "23", "123"]
COORD_NAMES = ["11", "22", "33", "12", "13", "23"]


def basis_matrices() -> list[np.ndarray]:
    mats: list[np.ndarray] = []
    for i in range(3):
        M = np.zeros((3, 3), dtype=float)
        M[i, i] = 1.0
        mats.append(M)
    for i, j in [(0, 1), (0, 2), (1, 2)]:
        M = np.zeros((3, 3), dtype=float)
        M[i, j] = 1.0
        M[j, i] = 1.0
        mats.append(M)
    return mats


BASIS = basis_matrices()


def matrix_from_coords(v: np.ndarray | list[float] | tuple[float, ...]) -> np.ndarray:
    x, y, z, a, b, c = [float(t) for t in v]
    return np.array([[x, a, b], [a, y, c], [b, c, z]], dtype=float)


def coords_from_matrix(K: np.ndarray) -> np.ndarray:
    return np.array([K[0, 0], K[1, 1], K[2, 2], K[0, 1], K[0, 2], K[1, 2]], dtype=float)


def principal_det(K: np.ndarray, subset: tuple[int, ...]) -> float:
    if not subset:
        return 1.0
    sub = K[np.ix_(subset, subset)]
    return float(np.linalg.det(sub))


def event_probs_mobius(K: np.ndarray) -> np.ndarray:
    out = []
    universe = {0, 1, 2}
    for S in ORDER:
        S_set = set(S)
        rest = sorted(universe - S_set)
        total = 0.0
        for mask in range(1 << len(rest)):
            A = set(S_set)
            parity = 0
            for bit, item in enumerate(rest):
                if (mask >> bit) & 1:
                    A.add(item)
                    parity += 1
            total += ((-1.0) ** parity) * principal_det(K, tuple(sorted(A)))
        out.append(total)
    return np.array(out, dtype=float)


def event_probs_formula(v: np.ndarray | list[float] | tuple[float, ...]) -> np.ndarray:
    x, y, z, a, b, c = [float(t) for t in v]
    q12 = x * y - a * a
    q13 = x * z - b * b
    q23 = y * z - c * c
    r = x * y * z + 2.0 * a * b * c - x * c * c - y * b * b - z * a * a
    return np.array(
        [
            1.0 - x - y - z + q12 + q13 + q23 - r,
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


def add_sym(H: np.ndarray, i: int, j: int, value: float) -> None:
    H[i, j] += value
    if i != j:
        H[j, i] += value


def q_and_r_jets(v: np.ndarray) -> tuple[list[np.ndarray], list[np.ndarray]]:
    x, y, z, a, b, c = [float(t) for t in v]
    grads = []
    hessians = []

    g = np.array([y, x, 0.0, -2.0 * a, 0.0, 0.0])
    H = np.zeros((6, 6), dtype=float)
    add_sym(H, 0, 1, 1.0)
    H[3, 3] = -2.0
    grads.append(g)
    hessians.append(H)

    g = np.array([z, 0.0, x, 0.0, -2.0 * b, 0.0])
    H = np.zeros((6, 6), dtype=float)
    add_sym(H, 0, 2, 1.0)
    H[4, 4] = -2.0
    grads.append(g)
    hessians.append(H)

    g = np.array([0.0, z, y, 0.0, 0.0, -2.0 * c])
    H = np.zeros((6, 6), dtype=float)
    add_sym(H, 1, 2, 1.0)
    H[5, 5] = -2.0
    grads.append(g)
    hessians.append(H)

    g = np.array(
        [
            y * z - c * c,
            x * z - b * b,
            x * y - a * a,
            2.0 * b * c - 2.0 * z * a,
            2.0 * a * c - 2.0 * y * b,
            2.0 * a * b - 2.0 * x * c,
        ]
    )
    H = np.zeros((6, 6), dtype=float)
    add_sym(H, 0, 1, z)
    add_sym(H, 0, 2, y)
    add_sym(H, 1, 2, x)
    add_sym(H, 0, 5, -2.0 * c)
    add_sym(H, 1, 4, -2.0 * b)
    add_sym(H, 2, 3, -2.0 * a)
    H[3, 3] = -2.0 * z
    H[4, 4] = -2.0 * y
    H[5, 5] = -2.0 * x
    add_sym(H, 3, 4, 2.0 * c)
    add_sym(H, 3, 5, 2.0 * b)
    add_sym(H, 4, 5, 2.0 * a)
    grads.append(g)
    hessians.append(H)

    return grads, hessians


def event_jets(v: np.ndarray | list[float] | tuple[float, ...]) -> tuple[np.ndarray, np.ndarray]:
    v = np.array(v, dtype=float)
    q12_g, q13_g, q23_g, r_g = q_and_r_jets(v)[0]
    q12_H, q13_H, q23_H, r_H = q_and_r_jets(v)[1]
    linear = np.eye(6, dtype=float)

    G = np.zeros((8, 6), dtype=float)
    H = np.zeros((8, 6, 6), dtype=float)

    G[7] = r_g
    H[7] = r_H
    G[4] = q12_g - r_g
    H[4] = q12_H - r_H
    G[5] = q13_g - r_g
    H[5] = q13_H - r_H
    G[6] = q23_g - r_g
    H[6] = q23_H - r_H
    G[1] = linear[0] - q12_g - q13_g + r_g
    H[1] = -q12_H - q13_H + r_H
    G[2] = linear[1] - q12_g - q23_g + r_g
    H[2] = -q12_H - q23_H + r_H
    G[3] = linear[2] - q13_g - q23_g + r_g
    H[3] = -q13_H - q23_H + r_H
    G[0] = -linear[0] - linear[1] - linear[2] + q12_g + q13_g + q23_g - r_g
    H[0] = q12_H + q13_H + q23_H - r_H

    return G, H


def fisher_matrix(v: np.ndarray) -> np.ndarray:
    p = event_probs_formula(v)
    G, _ = event_jets(v)
    return G.T @ np.diag(1.0 / p) @ G


def logs_and_N(v: np.ndarray) -> tuple[dict[str, float], np.ndarray]:
    p = event_probs_formula(v)
    l12 = math.log((p[0] * p[4]) / (p[1] * p[2]))
    l13 = math.log((p[0] * p[5]) / (p[1] * p[3]))
    l23 = math.log((p[0] * p[6]) / (p[2] * p[3]))
    Lambda = math.log((p[7] * p[1] * p[2] * p[3]) / (p[0] * p[4] * p[5] * p[6]))
    K = matrix_from_coords(v)
    N = -Lambda * K
    N[0, 0] += -l23
    N[1, 1] += -l13
    N[2, 2] += -l12
    return {"l12": l12, "l13": l13, "l23": l23, "Lambda": Lambda}, N


def adjugate_3(M: np.ndarray) -> np.ndarray:
    a, b, c = M[0, 0], M[0, 1], M[0, 2]
    d, e, f = M[1, 0], M[1, 1], M[1, 2]
    g, h, i = M[2, 0], M[2, 1], M[2, 2]
    return np.array(
        [
            [e * i - f * h, c * h - b * i, b * f - c * e],
            [f * g - d * i, a * i - c * g, c * d - a * f],
            [d * h - e * g, b * g - a * h, a * e - b * d],
        ],
        dtype=float,
    )


def trace_N_adj(N: np.ndarray, D: np.ndarray) -> float:
    return float(np.trace(N @ adjugate_3(D)))


def adj_polar_matrix(N: np.ndarray) -> np.ndarray:
    q = np.array([trace_N_adj(N, E) for E in BASIS], dtype=float)
    C = np.zeros((6, 6), dtype=float)
    for i, Ei in enumerate(BASIS):
        for j, Ej in enumerate(BASIS):
            C[i, j] = 0.5 * (trace_N_adj(N, Ei + Ej) - q[i] - q[j])
    return C


def B_direct(v: np.ndarray) -> np.ndarray:
    p = event_probs_formula(v)
    F = fisher_matrix(v)
    _, H = event_jets(v)
    return F + np.einsum("s,sij->ij", np.log(p), H)


def B_from_adj(v: np.ndarray) -> np.ndarray:
    F = fisher_matrix(v)
    _, N = logs_and_N(v)
    return F - 2.0 * adj_polar_matrix(N)


def schur_objects(v: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, float, float]:
    F = fisher_matrix(v)
    _, N = logs_and_N(v)
    N_inv = np.linalg.inv(N)
    delta = float(np.linalg.det(N))
    eta = np.array([float(np.trace(N_inv @ E)) for E in BASIS], dtype=float)
    G = np.zeros((6, 6), dtype=float)
    for i, Ei in enumerate(BASIS):
        for j, Ej in enumerate(BASIS):
            G[i, j] = float(np.trace(N_inv @ Ei @ N_inv @ Ej))
    A = F + delta * G
    B = A - delta * np.outer(eta, eta)
    rho = float(delta * eta @ np.linalg.solve(A, eta))
    return A, B, eta, delta, rho


def max_abs(M: np.ndarray) -> float:
    return float(np.max(np.abs(M)))


def finite_difference_jet_errors(v: np.ndarray, directions: list[np.ndarray]) -> dict[str, float]:
    G, H = event_jets(v)
    h = 1.0e-5
    max_first = 0.0
    max_second = 0.0
    for d in directions:
        p0 = event_probs_formula(v)
        p_p = event_probs_formula(v + h * d)
        p_m = event_probs_formula(v - h * d)
        p_pp = event_probs_formula(v + 2.0 * h * d)
        p_mm = event_probs_formula(v - 2.0 * h * d)
        fd_first = (p_mm - 8.0 * p_m + 8.0 * p_p - p_pp) / (12.0 * h)
        fd_second = (p_p - 2.0 * p0 + p_m) / (h * h)
        analytic_first = G @ d
        analytic_second = np.einsum("i,sij,j->s", d, H, d)
        max_first = max(max_first, max_abs(fd_first - analytic_first))
        max_second = max(max_second, max_abs(fd_second - analytic_second))
    return {"max_first_derivative_error": max_first, "max_second_derivative_error": max_second}


def pair_value(K: np.ndarray, i: int, j: int) -> float:
    return float(K[i, j])


def conditional_square_errors(v: np.ndarray) -> dict[str, float]:
    p = event_probs_formula(v)
    K = matrix_from_coords(v)
    single_idx = {0: 1, 1: 2, 2: 3}
    pair_idx = {(0, 1): 4, (0, 2): 5, (1, 2): 6}
    max_absent = 0.0
    max_present = 0.0
    for i, j in combinations(range(3), 2):
        k = next(t for t in range(3) if t not in (i, j))
        pair = tuple(sorted((i, j)))
        ik = tuple(sorted((i, k)))
        jk = tuple(sorted((j, k)))
        lhs_absent = p[0] * p[pair_idx[pair]] - p[single_idx[i]] * p[single_idx[j]]
        rhs_absent = -((1.0 - K[k, k]) * K[i, j] + K[i, k] * K[j, k]) ** 2
        lhs_present = p[single_idx[k]] * p[7] - p[pair_idx[ik]] * p[pair_idx[jk]]
        rhs_present = -(K[k, k] * K[i, j] - K[i, k] * K[j, k]) ** 2
        max_absent = max(max_absent, abs(lhs_absent - rhs_absent))
        max_present = max(max_present, abs(lhs_present - rhs_present))
    return {"max_absent_square_error": max_absent, "max_present_square_error": max_present}


def fraction_probs(vals: tuple[Fraction, ...]) -> dict[tuple[int, ...], Fraction]:
    x, y, z, a, b, c = vals
    q12 = x * y - a * a
    q13 = x * z - b * b
    q23 = y * z - c * c
    r = x * y * z + 2 * a * b * c - x * c * c - y * b * b - z * a * a
    values = {
        (): 1 - x - y - z + q12 + q13 + q23 - r,
        (0,): x - q12 - q13 + r,
        (1,): y - q12 - q23 + r,
        (2,): z - q13 - q23 + r,
        (0, 1): q12 - r,
        (0, 2): q13 - r,
        (1, 2): q23 - r,
        (0, 1, 2): r,
    }
    return values


def fraction_entry(vals: tuple[Fraction, ...], i: int, j: int) -> Fraction:
    x, y, z, a, b, c = vals
    if i == j:
        return [x, y, z][i]
    return {(0, 1): a, (0, 2): b, (1, 2): c}[tuple(sorted((i, j)))]


def exact_fraction_square_checks() -> dict[str, object]:
    samples = [
        (
            Fraction(2, 5),
            Fraction(3, 7),
            Fraction(4, 9),
            Fraction(1, 30),
            Fraction(-1, 35),
            Fraction(1, 28),
        ),
        (
            Fraction(5, 12),
            Fraction(7, 15),
            Fraction(3, 8),
            Fraction(-1, 25),
            Fraction(1, 33),
            Fraction(-1, 31),
        ),
    ]
    checked = 0
    for vals in samples:
        p = fraction_probs(vals)
        for i, j in combinations(range(3), 2):
            k = next(t for t in range(3) if t not in (i, j))
            pair = tuple(sorted((i, j)))
            ik = tuple(sorted((i, k)))
            jk = tuple(sorted((j, k)))
            Kij = fraction_entry(vals, i, j)
            Kik = fraction_entry(vals, i, k)
            Kjk = fraction_entry(vals, j, k)
            Kkk = fraction_entry(vals, k, k)
            lhs_absent = p[()] * p[pair] - p[(i,)] * p[(j,)]
            rhs_absent = -((1 - Kkk) * Kij + Kik * Kjk) ** 2
            if lhs_absent != rhs_absent:
                raise AssertionError((vals, i, j, "absent", lhs_absent, rhs_absent))
            lhs_present = p[(k,)] * p[(0, 1, 2)] - p[ik] * p[jk]
            rhs_present = -(Kkk * Kij - Kik * Kjk) ** 2
            if lhs_present != rhs_present:
                raise AssertionError((vals, i, j, "present", lhs_present, rhs_present))
            checked += 2
    return {"fraction_samples": len(samples), "exact_square_identities_checked": checked}


def sample_suite() -> list[dict[str, object]]:
    return [
        {
            "name": "interior_mixed_sign",
            "coords": np.array([0.42, 0.37, 0.53, 0.08, -0.05, 0.06], dtype=float),
        },
        {
            "name": "interior_asymmetric",
            "coords": np.array([0.61, 0.29, 0.47, -0.07, 0.045, -0.035], dtype=float),
        },
        {
            "name": "connected_small_edges",
            "coords": np.array([0.31, 0.44, 0.52, 0.012, -0.018, 0.015], dtype=float),
        },
        {
            "name": "diagonal_disconnected",
            "coords": np.array([1.0 / 3.0, 2.0 / 5.0, 3.0 / 7.0, 0.0, 0.0, 0.0], dtype=float),
        },
    ]


def deterministic_directions() -> list[np.ndarray]:
    dirs = [np.eye(6)[i] for i in range(6)]
    dirs.append(np.array([0.3, -0.2, 0.17, 0.11, -0.07, 0.05], dtype=float))
    dirs.append(np.array([-0.13, 0.19, -0.23, 0.04, 0.09, -0.08], dtype=float))
    return dirs


def analyze_sample(name: str, v: np.ndarray) -> dict[str, object]:
    K = matrix_from_coords(v)
    p_formula = event_probs_formula(v)
    p_mobius = event_probs_mobius(K)
    G, H = event_jets(v)
    F = fisher_matrix(v)
    logs, N = logs_and_N(v)
    B0 = B_direct(v)
    B1 = B_from_adj(v)

    eig_K = np.linalg.eigvalsh(K)
    eig_I_minus_K = np.linalg.eigvalsh(np.eye(3) - K)
    eig_N = np.linalg.eigvalsh(N)
    connected = bool(abs(v[3]) > 0.0 and abs(v[4]) > 0.0 and abs(v[5]) > 0.0)
    strict = bool(np.min(eig_K) > 0.0 and np.min(eig_I_minus_K) > 0.0 and np.min(p_formula) > 0.0)

    out: dict[str, object] = {
        "name": name,
        "strict_kernel": strict,
        "complete_offdiagonal_support": connected,
        "min_eig_K": float(np.min(eig_K)),
        "min_eig_I_minus_K": float(np.min(eig_I_minus_K)),
        "min_atom": float(np.min(p_formula)),
        "logs": logs,
        "min_eig_N": float(np.min(eig_N)),
        "max_event_formula_minus_mobius": max_abs(p_formula - p_mobius),
        "max_total_gradient": max_abs(np.sum(G, axis=0)),
        "max_total_hessian": max_abs(np.sum(H, axis=0)),
        "finite_difference_jets": finite_difference_jet_errors(v, deterministic_directions()),
        "conditional_squares": conditional_square_errors(v),
        "max_B_direct_minus_adj": max_abs(B0 - B1),
    }

    offdiag_B_expected = np.array(
        [
            F[3, 3] + 2.0 * N[2, 2],
            F[4, 4] + 2.0 * N[1, 1],
            F[5, 5] + 2.0 * N[0, 0],
        ],
        dtype=float,
    )
    offdiag_B_actual = np.array([B0[3, 3], B0[4, 4], B0[5, 5]], dtype=float)
    out["max_offdiag_coordinate_B_error"] = max_abs(offdiag_B_actual - offdiag_B_expected)

    if np.min(eig_N) > 1.0e-10:
        A, B2, eta, delta, rho = schur_objects(v)
        N_inv = np.linalg.inv(N)
        eta_expected = np.array(
            [N_inv[0, 0], N_inv[1, 1], N_inv[2, 2], 2.0 * N_inv[0, 1], 2.0 * N_inv[0, 2], 2.0 * N_inv[1, 2]],
            dtype=float,
        )
        out.update(
            {
                "det_N": delta,
                "rho": rho,
                "min_eig_A": float(np.min(np.linalg.eigvalsh(A))),
                "min_eig_B": float(np.min(np.linalg.eigvalsh(B0))),
                "max_B_direct_minus_schur": max_abs(B0 - B2),
                "max_eta_offdiag_factor_error": max_abs(eta - eta_expected),
            }
        )
    else:
        out.update(
            {
                "schur_checked": False,
                "schur_skip_reason": "N is singular or numerically too close to singular; inverse-N representation intentionally not applied.",
            }
        )

    return out


def boundary_family(theta: float, eps: float, u: np.ndarray) -> np.ndarray:
    P = np.outer(u, u)
    K = eps * np.eye(3) + (theta - eps) * P
    return coords_from_matrix(K)


def boundary_probes() -> list[dict[str, object]]:
    u = np.array([1.0, 2.0, 2.0], dtype=float) / 3.0
    probes = []
    for theta in [0.5, 0.9]:
        for eps in [1.0e-4, 1.0e-6, 1.0e-8]:
            v = boundary_family(theta, eps, u)
            A, B2, eta, delta, rho = schur_objects(v)
            L = math.log(1.0 / eps)
            probes.append(
                {
                    "theta": theta,
                    "epsilon": eps,
                    "rho": rho,
                    "rho_below_one": bool(rho < 1.0),
                    "theta_L_one_minus_rho": theta * L * (1.0 - rho),
                    "min_eig_A": float(np.min(np.linalg.eigvalsh(A))),
                    "min_eig_B": float(np.min(np.linalg.eigvalsh(B2))),
                }
            )
    return probes


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git_value(args: list[str]) -> str | None:
    try:
        return subprocess.check_output(["git", *args], text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="research/N3/review/formula_audit_results.json")
    ns = parser.parse_args()

    script_path = Path(__file__).resolve()
    samples = [analyze_sample(item["name"], item["coords"]) for item in sample_suite()]
    exact_fraction = exact_fraction_square_checks()
    boundary = boundary_probes()

    checks = []
    for sample in samples:
        checks.extend(
            [
                sample["max_event_formula_minus_mobius"] < 5.0e-14,
                sample["max_total_gradient"] < 5.0e-14,
                sample["max_total_hessian"] < 5.0e-14,
                sample["finite_difference_jets"]["max_first_derivative_error"] < 1.0e-10,
                sample["finite_difference_jets"]["max_second_derivative_error"] < 2.0e-5,
                sample["conditional_squares"]["max_absent_square_error"] < 5.0e-14,
                sample["conditional_squares"]["max_present_square_error"] < 5.0e-14,
                sample["max_B_direct_minus_adj"] < 5.0e-12,
                sample["max_offdiag_coordinate_B_error"] < 5.0e-12,
            ]
        )
        if sample.get("max_B_direct_minus_schur") is not None:
            checks.extend(
                [
                    sample["max_B_direct_minus_schur"] < 5.0e-11,
                    sample["max_eta_offdiag_factor_error"] < 5.0e-12,
                ]
            )
    checks.extend([probe["rho_below_one"] for probe in boundary])

    result = {
        "status": "PASS" if all(checks) else "FAIL",
        "purpose": "N3 independent formula audit; finite deterministic checks only, not a proof of global rho<=1.",
        "script": str(script_path),
        "script_sha256": sha256_file(script_path),
        "argv": sys.argv,
        "pid": os.getpid(),
        "cwd": os.getcwd(),
        "python": sys.version,
        "executable": sys.executable,
        "platform": platform.platform(),
        "numpy": np.__version__,
        "env_threads": {k: os.environ.get(k) for k in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"]},
        "git_head": git_value(["rev-parse", "HEAD"]),
        "git_branch": git_value(["branch", "--show-current"]),
        "samples": samples,
        "exact_fraction_square_checks": exact_fraction,
        "boundary_probes": boundary,
        "coverage": {
            "event_probability_formula_vs_mobius": len(samples),
            "six_coordinate_first_second_jets": len(samples) * len(deterministic_directions()),
            "conditional_covariance_square_float_identities": len(samples) * 6,
            "conditional_covariance_square_exact_fraction_identities": exact_fraction["exact_square_identities_checked"],
            "B_direct_vs_F_minus_2_tr_N_adj": len(samples),
            "B_direct_vs_schur_rank_one": sum(1 for s in samples if s.get("max_B_direct_minus_schur") is not None),
            "boundary_equal_softening_float_probes": len(boundary),
        },
        "non_coverage": [
            "No proof of the global scalar inequality rho(K)<=1.",
            "No interval or Lean certification.",
            "No review of any new author proof candidate beyond the frozen definitions and specified old sources.",
            "Boundary probes cover only fixed theta and all-nonzero u with equal soft eigenvalues; they do not cover unequal rates, theta endpoints, vanishing coordinates, or general interior kernels.",
            "Disconnected samples are used only to check that inverse-N formulas are not applied when N is singular.",
        ],
    }

    output = Path(ns.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(f"STATUS {result['status']}")
    print(f"wrote {output}")
    print(f"pid {result['pid']}")
    print(f"coverage {json.dumps(result['coverage'], sort_keys=True)}")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
