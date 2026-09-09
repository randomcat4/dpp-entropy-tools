#!/usr/bin/env python3
"""Independent bounded checks for the N3 round-2 beta-zero slice.

This review-owned script rebuilds the exact 3x3 real DPP event map, full
Fisher matrix, pair-statistic projected Fisher matrix, H, v_score, and the
Sherman-Morrison scalars alpha, beta, gamma.  It also checks the real principal
minor constraint T^2=4uvw, affine first/second derivative identities, and the
full Rayleigh square polynomials including a zero-edge case.

Finite samples here are deterministic checks only.  They are not a proof of
the beta-zero implication or the full N3 theorem.
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
from fractions import Fraction as Q
from pathlib import Path

import numpy as np


SUBSETS = [(), (0,), (1,), (2,), (0, 1), (0, 2), (1, 2), (0, 1, 2)]
SUBSET_NAMES = ["empty", "1", "2", "3", "12", "13", "23", "123"]
COORDS = [(0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2)]
COORD_NAMES = ["11", "22", "33", "12", "13", "23"]


def mat_from_coords(v: list[Q]) -> list[list[Q]]:
    x, y, z, a, b, c = v
    return [[x, a, b], [a, y, c], [b, c, z]]


def coords_from_mat(K: list[list[Q]]) -> list[Q]:
    return [K[0][0], K[1][1], K[2][2], K[0][1], K[0][2], K[1][2]]


def direction_from_coords(v: list[Q]) -> list[list[Q]]:
    return mat_from_coords(v)


def ray(K: list[list[Q]], D: list[list[Q]], t: Q) -> list[list[Q]]:
    return [[K[i][j] + t * D[i][j] for j in range(3)] for i in range(3)]


def det3(K: list[list[Q]]) -> Q:
    return (
        K[0][0] * K[1][1] * K[2][2]
        + K[0][1] * K[1][2] * K[2][0]
        + K[0][2] * K[1][0] * K[2][1]
        - K[0][2] * K[1][1] * K[2][0]
        - K[0][1] * K[1][0] * K[2][2]
        - K[0][0] * K[1][2] * K[2][1]
    )


def principal_det(K: list[list[Q]], subset: tuple[int, ...]) -> Q:
    if not subset:
        return Q(1)
    if len(subset) == 1:
        return K[subset[0]][subset[0]]
    if len(subset) == 2:
        i, j = subset
        return K[i][i] * K[j][j] - K[i][j] * K[j][i]
    return det3(K)


def events(K: list[list[Q]]) -> dict[tuple[int, ...], Q]:
    out: dict[tuple[int, ...], Q] = {}
    universe = {0, 1, 2}
    for S in SUBSETS:
        rest = sorted(universe - set(S))
        total = Q(0)
        for mask in range(1 << len(rest)):
            A = set(S)
            parity = 0
            for bit, item in enumerate(rest):
                if (mask >> bit) & 1:
                    A.add(item)
                    parity += 1
            total += ((-1) ** parity) * principal_det(K, tuple(sorted(A)))
        out[S] = total
    return out


def poly_coeffs_at_zero(values: dict[int, Q]) -> tuple[Q, Q, Q, Q]:
    """Return coefficients c0,c1,c2,c3 from f(0),f(1),f(-1),f(2)."""

    c0 = values[0]
    y1 = values[1] - c0
    ym1 = values[-1] - c0
    y2 = values[2] - c0
    c2 = (y1 + ym1) / 2
    c1_plus_c3 = (y1 - ym1) / 2
    c3 = (y2 - 2 * c1_plus_c3 - 4 * c2) / 6
    c1 = c1_plus_c3 - c3
    return c0, c1, c2, c3


def event_first_jacobian(K: list[list[Q]]) -> tuple[dict[tuple[int, ...], Q], list[list[Q]]]:
    p = events(K)
    columns: list[list[Q]] = []
    for j in range(6):
        d = [Q(0) for _ in range(6)]
        d[j] = Q(1)
        D = direction_from_coords(d)
        column = []
        for S in SUBSETS:
            vals = {t: events(ray(K, D, Q(t)))[S] for t in [0, 1, -1, 2]}
            _, c1, _, _ = poly_coeffs_at_zero(vals)
            column.append(c1)
        columns.append(column)
    J = [[columns[j][s] for j in range(6)] for s in range(8)]
    return p, J


def q_values(K: list[list[Q]]) -> list[Q]:
    return [
        K[0][0],
        K[1][1],
        K[2][2],
        principal_det(K, (0, 1)),
        principal_det(K, (0, 2)),
        principal_det(K, (1, 2)),
    ]


def stats_jacobian(K: list[list[Q]]) -> list[list[Q]]:
    columns: list[list[Q]] = []
    for j in range(6):
        d = [Q(0) for _ in range(6)]
        d[j] = Q(1)
        D = direction_from_coords(d)
        col = []
        for row in range(6):
            vals = {t: q_values(ray(K, D, Q(t)))[row] for t in [0, 1, -1, 2]}
            _, c1, _, _ = poly_coeffs_at_zero(vals)
            col.append(c1)
        columns.append(col)
    return [[columns[j][i] for j in range(6)] for i in range(6)]


def to_float_matrix(M: list[list[Q]]) -> np.ndarray:
    return np.array([[float(x) for x in row] for row in M], dtype=float)


def to_float_vector(v: list[Q]) -> np.ndarray:
    return np.array([float(x) for x in v], dtype=float)


def fisher_matrix(K: list[list[Q]]) -> tuple[dict[tuple[int, ...], Q], np.ndarray]:
    p, J = event_first_jacobian(K)
    Jf = to_float_matrix(J)
    pf = np.array([float(p[S]) for S in SUBSETS], dtype=float)
    F = Jf.T @ np.diag(1.0 / pf) @ Jf
    return p, F


def covariance_pair_projection(K: list[list[Q]]) -> np.ndarray:
    p = events(K)
    weights = np.array([float(p[S]) for S in SUBSETS], dtype=float)
    features = []
    for S in SUBSETS:
        row = []
        Sset = set(S)
        row.extend([1.0 if i in Sset else 0.0 for i in range(3)])
        row.extend([1.0 if i in Sset and j in Sset else 0.0 for i, j in [(0, 1), (0, 2), (1, 2)]])
        features.append(row)
    X = np.array(features, dtype=float)
    mean = weights @ X
    centered = X - mean
    Sigma = centered.T @ np.diag(weights) @ centered
    Jstats = to_float_matrix(stats_jacobian(K))
    return Jstats.T @ np.linalg.solve(Sigma, Jstats)


def lambda_gradient(K: list[list[Q]]) -> tuple[np.ndarray, Q, np.ndarray]:
    p, J = event_first_jacobian(K)
    signs = {(): -1.0, (0,): 1.0, (1,): 1.0, (2,): 1.0, (0, 1): -1.0, (0, 2): -1.0, (1, 2): -1.0, (0, 1, 2): 1.0}
    grad = np.zeros(6, dtype=float)
    for s, S in enumerate(SUBSETS):
        grad += signs[S] * np.array([float(x) for x in J[s]], dtype=float) / float(p[S])
    Z_exact = sum(Q(1, 1) / p[S] for S in SUBSETS)
    v_score = grad / math.sqrt(float(Z_exact))
    return grad, Z_exact, v_score


def logs_and_N(K: list[list[Q]]) -> tuple[dict[str, float], np.ndarray]:
    p = events(K)
    pf = {S: float(p[S]) for S in SUBSETS}
    ell12 = math.log(pf[()] * pf[(0, 1)] / (pf[(0,)] * pf[(1,)]))
    ell13 = math.log(pf[()] * pf[(0, 2)] / (pf[(0,)] * pf[(2,)]))
    ell23 = math.log(pf[()] * pf[(1, 2)] / (pf[(1,)] * pf[(2,)]))
    Lambda = math.log(pf[(0, 1, 2)] * pf[(0,)] * pf[(1,)] * pf[(2,)] / (pf[()] * pf[(0, 1)] * pf[(0, 2)] * pf[(1, 2)]))
    Kf = to_float_matrix(K)
    N = -Lambda * Kf
    N[0, 0] += -ell23
    N[1, 1] += -ell13
    N[2, 2] += -ell12
    return {"ell12": ell12, "ell13": ell13, "ell23": ell23, "Lambda": Lambda}, N


def basis_matrices_float() -> list[np.ndarray]:
    out = []
    for i, j in COORDS:
        E = np.zeros((3, 3), dtype=float)
        E[i, j] = 1.0
        E[j, i] = 1.0
        out.append(E)
    return out


def round2_quantities(K: list[list[Q]]) -> dict[str, object]:
    p, F = fisher_matrix(K)
    F_pair_score = None
    lam_grad, Z_exact, v_score = lambda_gradient(K)
    F_pair = F - np.outer(v_score, v_score)
    F_pair_cov = covariance_pair_projection(K)
    _, N = logs_and_N(K)
    N_inv = np.linalg.inv(N)
    det_N = float(np.linalg.det(N))
    basis = basis_matrices_float()
    eta = np.array([float(np.trace(N_inv @ E)) for E in basis], dtype=float)
    G = np.array([[float(np.trace(N_inv @ Ei @ N_inv @ Ej)) for Ej in basis] for Ei in basis], dtype=float)
    H = F_pair + det_N * G
    H_inv_c = np.linalg.solve(H, eta)
    H_inv_v = np.linalg.solve(H, v_score)
    alpha = float(eta @ H_inv_c)
    beta = float(v_score @ H_inv_c)
    beta_raw = float(lam_grad @ H_inv_c)
    gamma = float(v_score @ H_inv_v)
    beta_from_raw = beta_raw / math.sqrt(float(Z_exact))
    return {
        "min_atom": float(min(p.values())),
        "Z": float(Z_exact),
        "det_N": det_N,
        "min_eig_N": float(np.min(np.linalg.eigvalsh(N))),
        "min_eig_F": float(np.min(np.linalg.eigvalsh(F))),
        "min_eig_F_pair": float(np.min(np.linalg.eigvalsh(F_pair))),
        "min_eig_H": float(np.min(np.linalg.eigvalsh(H))),
        "F_pair_score_vs_cov_max_abs": float(np.max(np.abs(F_pair - F_pair_cov))),
        "alpha": alpha,
        "beta": beta,
        "beta_raw_lambda_grad_Hinv_c": beta_raw,
        "beta_from_raw": beta_from_raw,
        "beta_raw_equivalence_error": abs(beta - beta_from_raw),
        "gamma": gamma,
        "detN_alpha": det_N * alpha,
        "rho_if_beta_zero_formula": det_N * alpha,
        "beta_zero_exact_meaning": "beta=0 iff lambda_grad^T H^-1 c=0 because Z=sum 1/p is strictly positive.",
        "full_F_trace": float(np.trace(F)),
        "F_pair_trace": float(np.trace(F_pair)),
        "H_trace": float(np.trace(H)),
    }


def principal_variables(K: list[list[Q]]) -> dict[str, Q]:
    x, y, z, a, b, c = coords_from_mat(K)
    q12 = x * y - a * a
    q13 = x * z - b * b
    q23 = y * z - c * c
    r = det3(K)
    u = x * y - q12
    v = x * z - q13
    w = y * z - q23
    T = r - x * y * z + x * w + y * v + z * u
    return {"x": x, "y": y, "z": z, "a": a, "b": b, "c": c, "q12": q12, "q13": q13, "q23": q23, "r": r, "u": u, "v": v, "w": w, "T": T}


def derivative_formulas(K: list[list[Q]], D: list[list[Q]]) -> dict[str, Q]:
    x, y, z, a, b, c = coords_from_mat(K)
    dx, dy, dz, da, db, dc = coords_from_mat(D)
    q12_dot = dx * y + x * dy - 2 * a * da
    q13_dot = dx * z + x * dz - 2 * b * db
    q23_dot = dy * z + y * dz - 2 * c * dc
    q12_ddot = 2 * (dx * dy - da * da)
    q13_ddot = 2 * (dx * dz - db * db)
    q23_ddot = 2 * (dy * dz - dc * dc)
    r_dot = (
        dx * y * z
        + x * dy * z
        + x * y * dz
        + 2 * (da * b * c + a * db * c + a * b * dc)
        - dx * c * c
        - 2 * x * c * dc
        - dy * b * b
        - 2 * y * b * db
        - dz * a * a
        - 2 * z * a * da
    )
    r_ddot = (
        2 * (dx * dy * z + dx * y * dz + x * dy * dz)
        + 4 * (da * db * c + da * b * dc + a * db * dc)
        - 2 * x * dc * dc
        - 4 * dx * c * dc
        - 2 * y * db * db
        - 4 * dy * b * db
        - 2 * z * da * da
        - 4 * dz * a * da
    )
    u_dot, v_dot, w_dot = 2 * a * da, 2 * b * db, 2 * c * dc
    u_ddot, v_ddot, w_ddot = 2 * da * da, 2 * db * db, 2 * dc * dc
    T_dot = 2 * (da * b * c + a * db * c + a * b * dc)
    T_ddot = 4 * (da * db * c + da * b * dc + a * db * dc)
    return {
        "q12_dot": q12_dot,
        "q13_dot": q13_dot,
        "q23_dot": q23_dot,
        "q12_ddot": q12_ddot,
        "q13_ddot": q13_ddot,
        "q23_ddot": q23_ddot,
        "r_dot": r_dot,
        "r_ddot": r_ddot,
        "u_dot": u_dot,
        "v_dot": v_dot,
        "w_dot": w_dot,
        "u_ddot": u_ddot,
        "v_ddot": v_ddot,
        "w_ddot": w_ddot,
        "T_dot": T_dot,
        "T_ddot": T_ddot,
    }


def coeffs_for_scalar(func, K: list[list[Q]], D: list[list[Q]]) -> tuple[Q, Q, Q, Q]:
    vals = {t: func(ray(K, D, Q(t))) for t in [0, 1, -1, 2]}
    return poly_coeffs_at_zero(vals)


def affine_derivative_checks(K: list[list[Q]], D: list[list[Q]]) -> dict[str, object]:
    formulas = derivative_formulas(K, D)
    funcs = {
        "q12": lambda M: principal_variables(M)["q12"],
        "q13": lambda M: principal_variables(M)["q13"],
        "q23": lambda M: principal_variables(M)["q23"],
        "r": lambda M: principal_variables(M)["r"],
        "u": lambda M: principal_variables(M)["u"],
        "v": lambda M: principal_variables(M)["v"],
        "w": lambda M: principal_variables(M)["w"],
        "T": lambda M: principal_variables(M)["T"],
    }
    checks = {}
    for name, func in funcs.items():
        _, c1, c2, _ = coeffs_for_scalar(func, K, D)
        checks[f"{name}_first"] = c1 == formulas[f"{name}_dot"]
        checks[f"{name}_second"] = 2 * c2 == formulas[f"{name}_ddot"]

    vars0 = principal_variables(K)
    fd = formulas
    first_constraint = 2 * vars0["T"] * fd["T_dot"] - 4 * (
        fd["u_dot"] * vars0["v"] * vars0["w"]
        + vars0["u"] * fd["v_dot"] * vars0["w"]
        + vars0["u"] * vars0["v"] * fd["w_dot"]
    )
    second_constraint = 2 * (fd["T_dot"] * fd["T_dot"] + vars0["T"] * fd["T_ddot"]) - 4 * (
        fd["u_ddot"] * vars0["v"] * vars0["w"]
        + vars0["u"] * fd["v_ddot"] * vars0["w"]
        + vars0["u"] * vars0["v"] * fd["w_ddot"]
        + 2 * fd["u_dot"] * fd["v_dot"] * vars0["w"]
        + 2 * fd["u_dot"] * vars0["v"] * fd["w_dot"]
        + 2 * vars0["u"] * fd["v_dot"] * fd["w_dot"]
    )
    checks["T2_4uvw_first_derivative"] = first_constraint == 0
    checks["T2_4uvw_second_derivative"] = second_constraint == 0
    checks["T2_equals_4uvw_at_base"] = vars0["T"] * vars0["T"] == 4 * vars0["u"] * vars0["v"] * vars0["w"]

    all_nonzero = vars0["u"] != 0 and vars0["v"] != 0 and vars0["w"] != 0 and vars0["T"] != 0
    if all_nonzero:
        ratio_left = fd["T_dot"] / vars0["T"]
        ratio_right = (fd["u_dot"] / vars0["u"] + fd["v_dot"] / vars0["v"] + fd["w_dot"] / vars0["w"]) / 2
        checks["nonzero_log_derivative_branch"] = ratio_left == ratio_right
    else:
        checks["zero_edge_polynomial_branch_without_division"] = checks["T2_equals_4uvw_at_base"] and checks["T2_4uvw_first_derivative"] and checks["T2_4uvw_second_derivative"]

    return {
        "checks": checks,
        "all_checks_passed": all(checks.values()),
        "base_variables": {k: str(v) for k, v in vars0.items()},
        "formulas": {k: str(v) for k, v in formulas.items()},
    }


def rayleigh_coefficients_from_principal(K: list[list[Q]], pair: tuple[int, int]) -> tuple[Q, Q, Q]:
    i, j = pair
    k = next(m for m in range(3) if m not in pair)
    q = {S: principal_det(K, S) for S in SUBSETS}
    leading = q[(i,)] * q[(j,)] - q[()] * q[tuple(sorted(pair))]
    constant = q[tuple(sorted((i, k)))] * q[tuple(sorted((j, k)))] - q[(k,)] * q[(0, 1, 2)]
    # Evaluate the middle coefficient by expanding the Rayleigh difference
    # for f(t_1,t_2,t_3)=sum_S q_S prod_{m notin S} t_m.
    # For pair (i,j), the remaining variable is tau.
    # Delta(tau) = leading*tau^2 + middle*tau + constant.
    def f_value(tau: Q, ti: Q, tj: Q) -> Q:
        vals = [Q(0), Q(0), Q(0)]
        vals[i] = ti
        vals[j] = tj
        vals[k] = tau
        total = Q(0)
        for S in SUBSETS:
            prod = Q(1)
            for m in range(3):
                if m not in S:
                    prod *= vals[m]
            total += q[S] * prod
        return total

    def partial_i(tau: Q, tj: Q) -> Q:
        return f_value(tau, Q(1), tj) - f_value(tau, Q(0), tj)

    def partial_j(tau: Q, ti: Q) -> Q:
        return f_value(tau, ti, Q(1)) - f_value(tau, ti, Q(0))

    def partial_ij(tau: Q) -> Q:
        return f_value(tau, Q(1), Q(1)) - f_value(tau, Q(1), Q(0)) - f_value(tau, Q(0), Q(1)) + f_value(tau, Q(0), Q(0))

    def delta(tau: Q) -> Q:
        return partial_i(tau, Q(0)) * partial_j(tau, Q(0)) - f_value(tau, Q(0), Q(0)) * partial_ij(tau)

    vals = {t: delta(Q(t)) for t in [0, 1, -1, 2]}
    _, middle, _, _ = poly_coeffs_at_zero(vals)
    return leading, middle, constant


def rayleigh_square_checks(K: list[list[Q]]) -> dict[str, object]:
    checks = []
    vars0 = principal_variables(K)
    entries = coords_from_mat(K)
    for pair in [(0, 1), (0, 2), (1, 2)]:
        i, j = pair
        k = next(m for m in range(3) if m not in pair)
        Kij = K[i][j]
        Kik = K[i][k]
        Kjk = K[j][k]
        Kkk = K[k][k]
        leading, middle, constant = rayleigh_coefficients_from_principal(K, pair)
        branch_constant = Kij * Kkk - Kik * Kjk
        square_coeffs = (Kij * Kij, 2 * Kij * branch_constant, branch_constant * branch_constant)
        checks.append(
            {
                "pair": f"{i+1}{j+1}",
                "complement": k + 1,
                "coefficients": [str(leading), str(middle), str(constant)],
                "square_branch": f"({Kij})*tau + ({branch_constant})",
                "matches_full_square": (leading, middle, constant) == square_coeffs,
                "nonnegative_square_discriminant_zero": middle * middle == 4 * leading * constant,
                "leading_zero_edge": leading == 0,
                "constant_nonnegative": constant >= 0,
                "leading_nonnegative": leading >= 0,
            }
        )
    return {
        "T2_equals_4uvw": vars0["T"] * vars0["T"] == 4 * vars0["u"] * vars0["v"] * vars0["w"],
        "T": str(vars0["T"]),
        "u_v_w": [str(vars0["u"]), str(vars0["v"]), str(vars0["w"])],
        "edge_entries": [str(entries[3]), str(entries[4]), str(entries[5])],
        "pair_checks": checks,
        "all_pair_squares_passed": all(
            c["matches_full_square"]
            and c["nonnegative_square_discriminant_zero"]
            and c["leading_nonnegative"]
            and c["constant_nonnegative"]
            for c in checks
        ),
        "has_zero_edge": any(c["leading_zero_edge"] for c in checks),
    }


def leading_minors(K: list[list[Q]]) -> list[Q]:
    return [K[0][0], principal_det(K, (0, 1)), det3(K)]


def one_minus(K: list[list[Q]]) -> list[list[Q]]:
    return [[(Q(1) if i == j else Q(0)) - K[i][j] for j in range(3)] for i in range(3)]


def strict_by_leading_minors(K: list[list[Q]]) -> bool:
    return all(x > 0 for x in leading_minors(K)) and all(x > 0 for x in leading_minors(one_minus(K)))


def sample_suite() -> list[dict[str, object]]:
    return [
        {
            "name": "generic_connected_positive_T",
            "K": mat_from_coords([Q(2, 5), Q(3, 7), Q(4, 9), Q(1, 30), Q(1, 35), Q(1, 28)]),
            "D": direction_from_coords([Q(1, 11), Q(-1, 13), Q(1, 17), Q(1, 50), Q(-1, 45), Q(1, 42)]),
        },
        {
            "name": "generic_connected_negative_T",
            "K": mat_from_coords([Q(5, 12), Q(7, 15), Q(3, 8), Q(-1, 25), Q(1, 33), Q(1, 31)]),
            "D": direction_from_coords([Q(-1, 9), Q(1, 8), Q(1, 10), Q(1, 40), Q(1, 45), Q(-1, 50)]),
        },
        {
            "name": "zero_edge_connected_path",
            "K": mat_from_coords([Q(2, 5), Q(9, 20), Q(1, 2), Q(0), Q(1, 18), Q(-1, 20)]),
            "D": direction_from_coords([Q(1, 30), Q(-1, 35), Q(1, 40), Q(1, 50), Q(1, 60), Q(-1, 70)]),
        },
    ]


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
    parser.add_argument("--output", default="research/N3/round2/review/round2_definition_audit_results.json")
    ns = parser.parse_args()

    samples = []
    for item in sample_suite():
        K = item["K"]
        D = item["D"]
        round2 = round2_quantities(K)
        derivative = affine_derivative_checks(K, D)
        rayleigh = rayleigh_square_checks(K)
        samples.append(
            {
                "name": item["name"],
                "strict_by_leading_minors_K_and_I_minus_K": strict_by_leading_minors(K),
                "round2_quantities": round2,
                "affine_derivative_checks": derivative,
                "rayleigh_square_checks": rayleigh,
            }
        )

    pass_checks = []
    for sample in samples:
        pass_checks.extend(
            [
                sample["strict_by_leading_minors_K_and_I_minus_K"],
                sample["round2_quantities"]["min_atom"] > 0,
                sample["round2_quantities"]["min_eig_H"] > 0,
                sample["round2_quantities"]["F_pair_score_vs_cov_max_abs"] < 1e-10,
                sample["round2_quantities"]["beta_raw_equivalence_error"] < 1e-12,
                sample["affine_derivative_checks"]["all_checks_passed"],
                sample["rayleigh_square_checks"]["T2_equals_4uvw"],
                sample["rayleigh_square_checks"]["all_pair_squares_passed"],
            ]
        )
    pass_checks.append(any(sample["rayleigh_square_checks"]["has_zero_edge"] for sample in samples))

    script_path = Path(__file__).resolve()
    result = {
        "status": "PASS" if all(pass_checks) else "FAIL",
        "purpose": "Round-2 N3 beta-zero definition audit and bounded deterministic checks; not a proof of beta=0=>det(N)alpha<=1.",
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
        "frozen_source": {
            "path_read": r"C:\game\gameproject\showa100\math\i05-successors-20260909\N3\repo\research\N3\round2\frozen_theorem_v1.md",
            "baseline_in_frozen": "e476db1bb056af57e883a47f470ea0f4443c1837",
        },
        "samples": samples,
        "coverage": {
            "deterministic_strict_kernels": len(samples),
            "zero_edge_connected_samples": sum(1 for s in samples if s["rayleigh_square_checks"]["has_zero_edge"]),
            "round2_quantity_rebuilds": len(samples),
            "affine_derivative_identity_groups": len(samples),
            "rayleigh_polynomial_pairs": 3 * len(samples),
            "pair_projection_cross_checks": len(samples),
        },
        "non_coverage": [
            "No exact beta-zero point is certified.",
            "No proof or disproof of beta(K)=0 => det(N)*alpha(K)<=1.",
            "No proof of the full N3 entropy Hessian theorem or global rho<=1.",
            "No interval global certification and no Lean proof.",
            "No random scan or candidate construction; this is a bounded definition audit only.",
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
