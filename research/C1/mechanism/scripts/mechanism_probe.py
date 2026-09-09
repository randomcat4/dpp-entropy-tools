#!/usr/bin/env python3
"""Deterministic mechanism probe for the C1 beta-zero slice.

This script is self-contained: it rebuilds the eight-event 3-point DPP
probabilities, the six-coordinate event Jacobian, F, F_pair, N, M, alpha,
beta, and the true M-optimizer direction from K.  It does not import the
parent checkout.

All rows are scouts unless an interval certificate is explicitly produced.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import sys
import time
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import mpmath as mp


ROUND2_REFERENCE_BASELINE = "e476db1bb056af57e883a47f470ea0f4443c1837"
TASK_SOURCE_BASELINE = "e988aa3003484f6368133b8bc0c668331629e369"
TASK_SOURCE_TREE = "e7c177ca74da59744443dbfcaadafd98724767ec"
BASELINE = ROUND2_REFERENCE_BASELINE
LAMBDA = Q(3, 5)
SUBSETS = [(), (0,), (1,), (2,), (0, 1), (0, 2), (1, 2), (0, 1, 2)]
COORDS = [(0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2)]
COORD_NAMES = ["11", "22", "33", "12", "13", "23"]
LAMBDA_SIGNS = {
    (): -1,
    (0,): 1,
    (1,): 1,
    (2,): 1,
    (0, 1): -1,
    (0, 2): -1,
    (1, 2): -1,
    (0, 1, 2): 1,
}


def q_to_mpf(x: Q) -> mp.mpf:
    return mp.mpf(x.numerator) / x.denominator


def qstr(x: Q) -> str:
    return str(x)


def mpstr(x: Any, digits: int = 50) -> str:
    return mp.nstr(x, digits)


def det3(K: list[list[Any]]) -> Any:
    return (
        K[0][0] * (K[1][1] * K[2][2] - K[1][2] * K[2][1])
        - K[0][1] * (K[1][0] * K[2][2] - K[1][2] * K[2][0])
        + K[0][2] * (K[1][0] * K[2][1] - K[1][1] * K[2][0])
    )


def cofactor(K: list[list[Any]], i: int, j: int) -> Any:
    rows = [r for r in range(3) if r != i]
    cols = [c for c in range(3) if c != j]
    return ((-1) ** (i + j)) * (
        K[rows[0]][cols[0]] * K[rows[1]][cols[1]]
        - K[rows[0]][cols[1]] * K[rows[1]][cols[0]]
    )


def transpose(A: list[list[Any]]) -> list[list[Any]]:
    return [list(row) for row in zip(*A)]


def mmul(A: list[list[mp.mpf]], B: list[list[mp.mpf]]) -> list[list[mp.mpf]]:
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def trace(A: list[list[mp.mpf]]) -> mp.mpf:
    return sum(A[i][i] for i in range(len(A)))


def mp_matrix(A: list[list[mp.mpf]]) -> mp.matrix:
    return mp.matrix(A)


def family_from_raw(name: str, eps: Q, raw_u: list[Q], lam: Q = LAMBDA) -> dict[str, Any]:
    norm2 = sum(x * x for x in raw_u)
    A: list[list[Q]] = []
    for i in range(3):
        row = []
        for j in range(3):
            row.append((eps if i == j else Q(0)) + lam * raw_u[i] * raw_u[j] / norm2)
        A.append(row)
    signs = [Q(-1), Q(1), Q(1)]
    B = [[signs[i] * signs[j] * ((Q(1) if i == j else Q(0)) - A[i][j]) for j in range(3)] for i in range(3)]
    return {"name": name, "epsilon": eps, "raw_u": raw_u, "lambda": lam, "A": A, "B": B}


def midpoint(A: list[list[Q]], B: list[list[Q]], t: Q) -> list[list[Q]]:
    return [[(Q(1) - t) * A[i][j] + t * B[i][j] for j in range(3)] for i in range(3)]


def principal_det(K: list[list[Q]], subset: tuple[int, ...]) -> Q:
    if not subset:
        return Q(1)
    if len(subset) == 1:
        return K[subset[0]][subset[0]]
    if len(subset) == 2:
        i, j = subset
        return K[i][i] * K[j][j] - K[i][j] * K[j][i]
    return det3(K)


def one_minus(K: list[list[Q]]) -> list[list[Q]]:
    return [[(Q(1) if i == j else Q(0)) - K[i][j] for j in range(3)] for i in range(3)]


def strict_by_leading_minors(K: list[list[Q]]) -> bool:
    def leading(M: list[list[Q]]) -> list[Q]:
        return [M[0][0], M[0][0] * M[1][1] - M[0][1] * M[1][0], det3(M)]

    return all(v > 0 for v in leading(K)) and all(v > 0 for v in leading(one_minus(K)))


def connected(K: list[list[Q]]) -> bool:
    edges = [(0, 1), (0, 2), (1, 2)]
    present = {(i, j) for i, j in edges if K[i][j] != 0}
    return len(present) >= 2


def event_data_q(K: list[list[Q]]) -> tuple[list[Q], list[list[Q]]]:
    p: list[Q] = []
    J: list[list[Q]] = []
    for mask in range(8):
        M = [list(row) for row in K]
        for i in range(3):
            if not ((mask >> i) & 1):
                M[i][i] -= 1
        sign = Q((-1) ** (3 - int(mask).bit_count()))
        p.append(sign * det3(M))
        J.append([sign * (cofactor(M, i, j) + (cofactor(M, j, i) if i != j else 0)) for i, j in COORDS])
    return p, J


def evaluate(Kq: list[list[Q]], dps: int) -> dict[str, Any]:
    mp.mp.dps = dps
    p_q, J_q = event_data_q(Kq)
    if min(p_q) <= 0:
        raise ValueError("nonpositive event mass")
    K = [[q_to_mpf(x) for x in row] for row in Kq]
    p = [q_to_mpf(x) for x in p_q]
    J = [[q_to_mpf(x) for x in row] for row in J_q]
    Z = sum(1 / x for x in p)
    signs = [(-1) ** (3 - int(mask).bit_count()) for mask in range(8)]
    g = [sum(mp.mpf(signs[k]) * J[k][j] / p[k] for k in range(8)) for j in range(6)]
    F = [[sum(J[k][i] * J[k][j] / p[k] for k in range(8)) for j in range(6)] for i in range(6)]
    Fpair = [[F[i][j] - g[i] * g[j] / Z for j in range(6)] for i in range(6)]
    ell12 = mp.log(p[0] * p[3] / (p[1] * p[2]))
    ell13 = mp.log(p[0] * p[5] / (p[1] * p[4]))
    ell23 = mp.log(p[0] * p[6] / (p[2] * p[4]))
    Lambda_val = mp.log(p[7] * p[1] * p[2] * p[4] / (p[0] * p[3] * p[5] * p[6]))
    N = [[-Lambda_val * K[i][j] for j in range(3)] for i in range(3)]
    N[0][0] -= ell23
    N[1][1] -= ell13
    N[2][2] -= ell12
    detN = det3(N)
    adjN = [[cofactor(N, j, i) for j in range(3)] for i in range(3)]
    basis = []
    for i, j in COORDS:
        E = [[mp.mpf("0") for _ in range(3)] for _ in range(3)]
        E[i][j] = mp.mpf("1")
        E[j][i] = mp.mpf("1")
        basis.append(E)
    adjE = [mmul(adjN, E) for E in basis]
    a_vec = [trace(adjE[i]) for i in range(6)]
    T = [[trace(mmul(mmul(adjE[i], adjN), basis[j])) for j in range(6)] for i in range(6)]
    Htilde = [[detN * Fpair[i][j] + T[i][j] for j in range(6)] for i in range(6)]
    h = mp.lu_solve(mp_matrix(Htilde), mp.matrix(a_vec))
    h_list = [h[i] for i in range(6)]
    beta_times_sqrtZ = sum(g[i] * h_list[i] for i in range(6))
    dalpha = sum(a_vec[i] * h_list[i] for i in range(6))
    alpha = dalpha / detN
    beta = beta_times_sqrtZ / mp.sqrt(Z)
    D_M = [x / alpha for x in h_list]
    eta_D = sum((a_vec[i] / detN) * D_M[i] for i in range(6))
    lambda_D = sum(g[i] * D_M[i] for i in range(6))
    B_DM = 1 / alpha + (beta / alpha) ** 2 - detN
    max_abs_D = max(abs(x) for x in D_M)
    return {
        "beta_times_sqrtZ": beta_times_sqrtZ,
        "beta": beta,
        "dalpha": dalpha,
        "alpha": alpha,
        "detN": detN,
        "Z": Z,
        "Lambda": Lambda_val,
        "min_probability": min(p),
        "D_M_coords": D_M,
        "D_M_max_abs_coord": max_abs_D,
        "eta_D_M": eta_D,
        "Lambda_prime_D_M": lambda_D,
        "negative_entropy_quadratic_at_D_M": B_DM,
        "p": p,
    }


def refine_sign_change(fam: dict[str, Any], left: Q, right: Q, steps: int, dps: int) -> tuple[Q, Q, list[dict[str, str]]]:
    trace_rows: list[dict[str, str]] = []
    left_val = evaluate(midpoint(fam["A"], fam["B"], left), dps)["beta_times_sqrtZ"]
    right_val = evaluate(midpoint(fam["A"], fam["B"], right), dps)["beta_times_sqrtZ"]
    if left_val == 0:
        return left, left, trace_rows
    if right_val == 0:
        return right, right, trace_rows
    if left_val * right_val > 0:
        raise ValueError("endpoint signs do not bracket a root")
    for _ in range(steps):
        mid = (left + right) / 2
        q = evaluate(midpoint(fam["A"], fam["B"], mid), dps)
        mid_val = q["beta_times_sqrtZ"]
        trace_rows.append({"t": qstr(mid), "beta_times_sqrtZ": mpstr(mid_val, 40), "dalpha": mpstr(q["dalpha"], 40)})
        if left_val * mid_val <= 0:
            right = mid
            right_val = mid_val
        else:
            left = mid
            left_val = mid_val
    return left, right, trace_rows


def scan_for_brackets(fam: dict[str, Any], dps: int) -> tuple[list[tuple[Q, Q]], list[dict[str, Any]]]:
    # Bounded deterministic checkpoints.  The old certificate used [0,1/8];
    # the smaller checkpoints distinguish t=epsilon*s from roots with t/epsilon
    # diverging.
    eps = fam["epsilon"]
    checkpoints = {Q(0), eps / 16, eps / 8, eps / 4, eps / 2, eps, 2 * eps, 4 * eps, 8 * eps, Q(1, 128), Q(1, 64), Q(1, 32), Q(1, 16), Q(1, 8), Q(1, 4), Q(1, 2), Q(1)}
    grid = sorted(t for t in checkpoints if Q(0) <= t <= Q(1))
    rows: list[dict[str, Any]] = []
    prev: tuple[Q, mp.mpf] | None = None
    brackets: list[tuple[Q, Q]] = []
    for t in grid:
        K = midpoint(fam["A"], fam["B"], t)
        if not strict_by_leading_minors(K) or not connected(K):
            rows.append({"t": qstr(t), "status": "REJECTED_FEASIBILITY"})
            prev = None
            continue
        q = evaluate(K, dps)
        val = q["beta_times_sqrtZ"]
        row = {
            "t": qstr(t),
            "t_over_epsilon": mpstr(q_to_mpf(t / eps), 30) if eps else None,
            "beta_times_sqrtZ": mpstr(val, 50),
            "beta": mpstr(q["beta"], 50),
            "dalpha": mpstr(q["dalpha"], 50),
            "detN": mpstr(q["detN"], 35),
            "min_probability": mpstr(q["min_probability"], 25),
            "D_M_max_abs_coord": mpstr(q["D_M_max_abs_coord"], 35),
            "Lambda_prime_D_M": mpstr(q["Lambda_prime_D_M"], 35),
            "status": "SCOUT",
        }
        rows.append(row)
        if prev is not None and prev[1] * val < 0:
            brackets.append((prev[0], t))
        prev = (t, val)
    return brackets, rows


def matrix_json(K: list[list[Q]]) -> list[list[str]]:
    return [[qstr(x) for x in row] for row in K]


def family_specs() -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for exp in [2, 3, 4, 5]:
        eps = Q(1, 10**exp)
        out.append(family_from_raw(f"fixed_u123_eps_1e-{exp}", eps, [Q(1), Q(2), Q(3)]))
    # One joint ratio-degeneration family: the first coordinate of u is tied
    # to epsilon, so edges incident to the flipped coordinate become weak while
    # the 23 edge stays order one.  The raw vector remains rational.
    for exp in [2, 3, 4, 5]:
        eps = Q(1, 10**exp)
        out.append(family_from_raw(f"joint_u1_sqrt_eps_eps_1e-{exp}", eps, [Q(1, 10 ** (exp // 2)) if exp % 2 == 0 else Q(1, 10 ** ((exp + 1) // 2)), Q(2), Q(3)]))
    # A second deterministic joint branch with the third coordinate weak,
    # included as a distinct edge-ratio degeneration for obstacle comparison.
    for exp in [2, 3, 4, 5]:
        eps = Q(1, 10**exp)
        out.append(family_from_raw(f"joint_u3_eps_eps_1e-{exp}", eps, [Q(1), Q(2), eps]))
    return out


def row_for_root(fam: dict[str, Any], left: Q, right: Q, dps: int) -> dict[str, Any]:
    mid = (left + right) / 2
    q = evaluate(midpoint(fam["A"], fam["B"], mid), dps)
    eps = fam["epsilon"]
    return {
        "root_bracket": [qstr(left), qstr(right)],
        "root_mid": qstr(mid),
        "root_mid_t_over_epsilon": mpstr(q_to_mpf(mid / eps), 50),
        "root_width": qstr(right - left),
        "beta_times_sqrtZ_mid": mpstr(q["beta_times_sqrtZ"], 50),
        "beta_mid": mpstr(q["beta"], 50),
        "dalpha_mid": mpstr(q["dalpha"], 50),
        "alpha_mid": mpstr(q["alpha"], 50),
        "detN_mid": mpstr(q["detN"], 50),
        "min_probability_mid": mpstr(q["min_probability"], 30),
        "D_M_coords_mid": [mpstr(x, 50) for x in q["D_M_coords"]],
        "D_M_max_abs_coord_mid": mpstr(q["D_M_max_abs_coord"], 50),
        "eta_D_M_mid": mpstr(q["eta_D_M"], 50),
        "Lambda_prime_D_M_mid": mpstr(q["Lambda_prime_D_M"], 50),
        "negative_entropy_quadratic_D_M_mid": mpstr(q["negative_entropy_quadratic_at_D_M"], 50),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="outputs/mechanism_probe.json")
    parser.add_argument("--dps", type=int, default=180)
    parser.add_argument("--steps", type=int, default=70)
    ns = parser.parse_args()
    started = time.time()
    output = Path(ns.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    families = family_specs()
    result: dict[str, Any] = {
        "status": "SCOUT_NO_INTERVAL_CERTIFICATE",
        "task_source": {"baseline": TASK_SOURCE_BASELINE, "tree": TASK_SOURCE_TREE},
        "round2_reference_baseline": ROUND2_REFERENCE_BASELINE,
        "pid": os.getpid(),
        "python": sys.version,
        "platform": platform.platform(),
        "mpmath": mp.__version__,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "thread_env": {k: os.environ.get(k) for k in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"]},
        "lambda": qstr(LAMBDA),
        "randomness": "none: bounded deterministic epsilon and raw-u table",
        "dps": ns.dps,
        "bisection_steps_per_bracket": ns.steps,
        "families": [],
        "accepted_families": 0,
        "sign_change_count": 0,
        "max_dalpha_root_mid": None,
        "exit_status": 0,
    }
    root_rows: list[dict[str, Any]] = []
    for fam in families:
        exp_digits = len(str(fam["epsilon"].denominator)) - 1
        dps = max(ns.dps, 120 + 20 * exp_digits)
        brackets, scan_rows = scan_for_brackets(fam, dps)
        refined = []
        for left0, right0 in brackets:
            left, right, trace_rows = refine_sign_change(fam, left0, right0, ns.steps, dps)
            root = row_for_root(fam, left, right, dps)
            root["initial_bracket"] = [qstr(left0), qstr(right0)]
            root["bisection_tail"] = trace_rows[-5:]
            refined.append(root)
            root_rows.append({"family": fam["name"], **root})
        result["families"].append(
            {
                "name": fam["name"],
                "epsilon": qstr(fam["epsilon"]),
                "raw_u": [qstr(x) for x in fam["raw_u"]],
                "A": matrix_json(fam["A"]),
                "B": matrix_json(fam["B"]),
                "strict_A": strict_by_leading_minors(fam["A"]),
                "strict_B": strict_by_leading_minors(fam["B"]),
                "connected_A": connected(fam["A"]),
                "connected_B": connected(fam["B"]),
                "dps": dps,
                "scan_rows": scan_rows,
                "sign_change_brackets": [[qstr(a), qstr(b)] for a, b in brackets],
                "refined_roots": refined,
            }
        )
        if strict_by_leading_minors(fam["A"]) and strict_by_leading_minors(fam["B"]):
            result["accepted_families"] += 1
    result["sign_change_count"] = len(root_rows)
    if root_rows:
        result["max_dalpha_root_mid"] = max(root_rows, key=lambda r: mp.mpf(r["dalpha_mid"]))
    result["elapsed_seconds"] = time.time() - started
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "pid": result["pid"],
        "families": len(families),
        "sign_change_count": result["sign_change_count"],
        "max_dalpha_root_mid": result["max_dalpha_root_mid"],
        "output": str(output),
        "elapsed_seconds": result["elapsed_seconds"],
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
