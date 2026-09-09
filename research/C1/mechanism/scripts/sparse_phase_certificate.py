#!/usr/bin/env python3
"""Sparse phase-transition beta-zero certificate for C1/B0.

Family:

    K(epsilon, kappa) = epsilon I + lambda u u^T,
    lambda = 7/10,
    u_1^2 = 2/5, u_2^2 = 3/5, u_3^2 = kappa epsilon.

This is a near-rank-one, connected but sparse-edge endpoint of the assigned
twisted-complement mechanism.  The computation below reconstructs all B0
quantities from the eight event atoms.  The interval certificate is for one
bounded kappa bracket at epsilon=10^-12.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import platform
import sys
import time
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import mpmath as mp


BASELINE = "e476db1bb056af57e883a47f470ea0f4443c1837"
TASK_SOURCE_BASELINE = "e988aa3003484f6368133b8bc0c668331629e369"
TASK_SOURCE_TREE = "e7c177ca74da59744443dbfcaadafd98724767ec"
LAMBDA = Q(7, 10)
COORDS = [(0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2)]
COORD_NAMES = ["11", "22", "33", "12", "13", "23"]
SUBSET_SIGNS = [(-1) ** (3 - int(mask).bit_count()) for mask in range(8)]


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


def mmul(A: list[list[Any]], B: list[list[Any]]) -> list[list[Any]]:
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def trace(A: list[list[Any]]) -> Any:
    return sum(A[i][i] for i in range(len(A)))


def event_data(K: list[list[Any]], zero: Any, one: Any) -> tuple[list[Any], list[list[Any]]]:
    p = []
    J = []
    for mask in range(8):
        M = [list(row) for row in K]
        for i in range(3):
            if not ((mask >> i) & 1):
                M[i][i] = M[i][i] - one
        sign = SUBSET_SIGNS[mask]
        p.append(sign * det3(M))
        J.append([sign * (cofactor(M, i, j) + (cofactor(M, j, i) if i != j else zero)) for i, j in COORDS])
    return p, J


def evaluate_from_K(K: list[list[mp.mpf]]) -> dict[str, Any]:
    p, J = event_data(K, mp.mpf("0"), mp.mpf("1"))
    if min(p) <= 0:
        raise ValueError("nonpositive event mass")
    Z = sum(1 / x for x in p)
    g = [sum(SUBSET_SIGNS[k] * J[k][j] / p[k] for k in range(8)) for j in range(6)]
    F = [[sum(J[k][i] * J[k][j] / p[k] for k in range(8)) for j in range(6)] for i in range(6)]
    Fpair = [[F[i][j] - g[i] * g[j] / Z for j in range(6)] for i in range(6)]
    ell = [
        mp.log(p[0] * p[6] / (p[2] * p[4])),
        mp.log(p[0] * p[5] / (p[1] * p[4])),
        mp.log(p[0] * p[3] / (p[1] * p[2])),
    ]
    lam = mp.log(p[7] * p[1] * p[2] * p[4] / (p[0] * p[3] * p[5] * p[6]))
    N = [[-lam * K[i][j] - (ell[i] if i == j else mp.mpf("0")) for j in range(3)] for i in range(3)]
    detN = det3(N)
    adj = [[cofactor(N, j, i) for j in range(3)] for i in range(3)]
    E = []
    for i, j in COORDS:
        e = [[mp.mpf("0") for _ in range(3)] for _ in range(3)]
        e[i][j] = mp.mpf("1")
        e[j][i] = mp.mpf("1")
        E.append(e)
    avec = [trace(mmul(adj, e)) for e in E]
    Htilde = [
        [detN * Fpair[i][j] + trace(mmul(mmul(mmul(adj, E[i]), adj), E[j])) for j in range(6)]
        for i in range(6)
    ]
    h = mp.lu_solve(mp.matrix(Htilde), mp.matrix(avec))
    h_list = [h[i] for i in range(6)]
    beta_times_sqrtZ = sum(g[i] * h_list[i] for i in range(6))
    dalpha = sum(avec[i] * h_list[i] for i in range(6))
    alpha = dalpha / detN
    beta = beta_times_sqrtZ / mp.sqrt(Z)
    D_M = [x / alpha for x in h_list]
    eta_D = sum((avec[i] / detN) * D_M[i] for i in range(6))
    lambda_D = sum(g[i] * D_M[i] for i in range(6))
    B_DM = 1 / alpha + (beta / alpha) ** 2 - detN
    return {
        "beta_times_sqrtZ": beta_times_sqrtZ,
        "beta": beta,
        "dalpha": dalpha,
        "alpha": alpha,
        "detN": detN,
        "Z": Z,
        "min_probability": min(p),
        "D_M_coords": D_M,
        "D_M_max_abs_coord": max(abs(x) for x in D_M),
        "eta_D_M": eta_D,
        "Lambda_prime_D_M": lambda_D,
        "negative_entropy_quadratic_D_M": B_DM,
        "N_leading_minors": [N[0][0], N[0][0] * N[1][1] - N[0][1] * N[1][0], detN],
    }


def sparse_K_mp(eps: mp.mpf, kappa: mp.mpf) -> list[list[mp.mpf]]:
    lam = mp.mpf(7) / 10
    raw = [mp.sqrt(mp.mpf(2) / 5), mp.sqrt(mp.mpf(3) / 5), mp.sqrt(kappa * eps)]
    return [[(eps if i == j else mp.mpf("0")) + lam * raw[i] * raw[j] for j in range(3)] for i in range(3)]


def eval_sparse(eps: Q, kappa: Q, dps: int) -> dict[str, Any]:
    mp.mp.dps = dps
    return evaluate_from_K(sparse_K_mp(q_to_mpf(eps), q_to_mpf(kappa)))


def refine_kappa(eps: Q, left: Q, right: Q, steps: int, dps: int) -> tuple[Q, Q, list[dict[str, str]]]:
    left_val = eval_sparse(eps, left, dps)["beta_times_sqrtZ"]
    right_val = eval_sparse(eps, right, dps)["beta_times_sqrtZ"]
    assert left_val * right_val < 0
    trace_rows = []
    for _ in range(steps):
        mid = (left + right) / 2
        q = eval_sparse(eps, mid, dps)
        val = q["beta_times_sqrtZ"]
        trace_rows.append({"kappa": qstr(mid), "beta_times_sqrtZ": mpstr(val, 45), "dalpha": mpstr(q["dalpha"], 45)})
        if left_val * val <= 0:
            right = mid
            right_val = val
        else:
            left = mid
            left_val = val
    return left, right, trace_rows


def coarse_bracket(eps: Q, dps: int) -> tuple[Q, Q, list[dict[str, str]]]:
    grid = [Q(1), Q(3, 2), Q(2), Q(5, 2), Q(3), Q(7, 2), Q(4), Q(5), Q(7), Q(10)]
    rows = []
    prev = None
    for kappa in grid:
        q = eval_sparse(eps, kappa, dps)
        val = q["beta_times_sqrtZ"]
        rows.append({"kappa": qstr(kappa), "beta_times_sqrtZ": mpstr(val, 35), "dalpha": mpstr(q["dalpha"], 35)})
        if prev is not None and prev[1] * val < 0:
            return prev[0], kappa, rows
        prev = (kappa, val)
    raise RuntimeError(f"no kappa sign change on the fixed grid for eps={eps}")


def root_row(eps: Q, left: Q, right: Q, dps: int) -> dict[str, Any]:
    mid = (left + right) / 2
    q = eval_sparse(eps, mid, dps)
    return {
        "epsilon": qstr(eps),
        "kappa_bracket": [qstr(left), qstr(right)],
        "kappa_mid": qstr(mid),
        "u3_squared_mid": qstr(mid * eps),
        "u3_over_sqrt_epsilon_mid": mpstr(mp.sqrt(q_to_mpf(mid)), 40),
        "beta_times_sqrtZ_mid": mpstr(q["beta_times_sqrtZ"], 55),
        "beta_mid": mpstr(q["beta"], 55),
        "dalpha_mid": mpstr(q["dalpha"], 55),
        "alpha_mid": mpstr(q["alpha"], 55),
        "detN_mid": mpstr(q["detN"], 55),
        "min_probability_mid": mpstr(q["min_probability"], 35),
        "D_M_coords_mid": [mpstr(x, 55) for x in q["D_M_coords"]],
        "D_M_max_abs_coord_mid": mpstr(q["D_M_max_abs_coord"], 55),
        "eta_D_M_mid": mpstr(q["eta_D_M"], 55),
        "Lambda_prime_D_M_mid": mpstr(q["Lambda_prime_D_M"], 55),
        "negative_entropy_quadratic_D_M_mid": mpstr(q["negative_entropy_quadratic_D_M"], 55),
        "N_leading_minors_mid": [mpstr(x, 45) for x in q["N_leading_minors"]],
    }


def log_unit(x: Q, terms: int = 120) -> tuple[Q, Q]:
    assert Q(1) <= x <= Q(2)
    z = (x - 1) / (x + 1)
    partial = 2 * sum((z ** (2 * j + 1) / Q(2 * j + 1) for j in range(terms)), Q(0))
    tail = 2 * z ** (2 * terms + 1) / (Q(2 * terms + 1) * (1 - z * z))
    return partial, partial + tail


def log_bound(x: Q) -> tuple[Q, Q]:
    assert x > 0
    power = 0
    while x >= 2:
        x /= 2
        power += 1
    while x < 1:
        x *= 2
        power -= 1
    lo, hi = log_unit(x)
    l2, u2 = log_unit(Q(2))
    if power >= 0:
        return lo + power * l2, hi + power * u2
    return lo + power * u2, hi + power * l2


class I:
    DEN = 2**840

    def __init__(self, lo: Any, hi: Any | None = None):
        if isinstance(lo, I):
            self.lo = lo.lo
            self.hi = lo.hi
            return
        a = Q(lo)
        b = a if hi is None else Q(hi)
        assert a <= b
        self.lo = Q((a * self.DEN).__floor__(), self.DEN)
        self.hi = Q((b * self.DEN).__ceil__(), self.DEN)

    def __add__(self, other: Any) -> "I":
        other = I(other)
        return I(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self) -> "I":
        return I(-self.hi, -self.lo)

    def __sub__(self, other: Any) -> "I":
        return self + (-I(other))

    def __rsub__(self, other: Any) -> "I":
        return I(other) - self

    def __mul__(self, other: Any) -> "I":
        other = I(other)
        vals = [a * b for a in [self.lo, self.hi] for b in [other.lo, other.hi]]
        return I(min(vals), max(vals))

    __rmul__ = __mul__

    def __truediv__(self, other: Any) -> "I":
        other = I(other)
        assert not other.lo <= 0 <= other.hi, "division by zero-containing interval"
        return self * I(1 / other.hi, 1 / other.lo)

    def __rtruediv__(self, other: Any) -> "I":
        return I(other) / self

    def __repr__(self) -> str:
        return f"I({self.lo},{self.hi})"


def sqrt_q_bounds(x: Q) -> tuple[Q, Q]:
    assert x >= 0
    den = I.DEN
    scaled_num = x.numerator * den * den
    lower = math.isqrt(scaled_num // x.denominator)
    upper = math.isqrt((scaled_num + x.denominator - 1) // x.denominator)
    while upper * upper * x.denominator < scaled_num:
        upper += 1
    return Q(lower, den), Q(upper, den)


def sqrt_i(x: I) -> I:
    lo, _ = sqrt_q_bounds(x.lo)
    _, hi = sqrt_q_bounds(x.hi)
    return I(lo, hi)


def logi(x: I) -> I:
    assert x.lo > 0
    lo, _ = log_bound(x.lo)
    _, hi = log_bound(x.hi)
    return I(lo, hi)


def interval_json(x: I, digits: int = 36) -> dict[str, str]:
    scale = 10**digits
    lo_i = (x.lo * scale).__floor__()
    hi_i = (x.hi * scale).__ceil__()

    def dec(v: int) -> str:
        sign = "-" if v < 0 else ""
        v = abs(v)
        return f"{sign}{v // scale}.{str(v % scale).zfill(digits)}"

    return {
        "lower": str(x.lo),
        "upper": str(x.hi),
        "approx_lower": dec(lo_i),
        "approx_upper": dec(hi_i),
    }


def sparse_K_interval(eps: Q, klo: Q, khi: Q) -> list[list[I]]:
    kappa = I(klo, khi)
    eps_i = I(eps)
    lam = I(LAMBDA)
    raw = [sqrt_i(I(Q(2, 5))), sqrt_i(I(Q(3, 5))), sqrt_i(kappa * eps_i)]
    K = []
    for i in range(3):
        row = []
        for j in range(3):
            entry = lam * raw[i] * raw[j]
            if i == j:
                entry = entry + eps_i
            row.append(entry)
        K.append(row)
    return K


def solve_interval(A: list[list[I]], b: list[I]) -> tuple[list[I], list[I]]:
    work = [list(row) + [b[i]] for i, row in enumerate(A)]
    n = len(b)
    pivots = []
    for k in range(n):
        pivots.append(work[k][k])
        for row in range(k + 1, n):
            q = work[row][k] / work[k][k]
            for col in range(k + 1, n + 1):
                work[row][col] = work[row][col] - q * work[k][col]
            work[row][k] = I(0)
    x = [I(0)] * n
    for k in reversed(range(n)):
        x[k] = (work[k][n] - sum(work[k][j] * x[j] for j in range(k + 1, n))) / work[k][k]
    return x, pivots


def interval_quantities(eps: Q, klo: Q, khi: Q) -> dict[str, Any]:
    K = sparse_K_interval(eps, klo, khi)
    p, J = event_data(K, I(0), I(1))
    assert min(x.lo for x in p) > 0
    Z = sum(1 / x for x in p)
    g = [sum(SUBSET_SIGNS[k] * J[k][j] / p[k] for k in range(8)) for j in range(6)]
    Fpair = [
        [sum(J[k][i] * J[k][j] / p[k] for k in range(8)) - g[i] * g[j] / Z for j in range(6)]
        for i in range(6)
    ]
    ell = [
        logi(p[0] * p[6] / (p[2] * p[4])),
        logi(p[0] * p[5] / (p[1] * p[4])),
        logi(p[0] * p[3] / (p[1] * p[2])),
    ]
    lam = logi(p[7] * p[1] * p[2] * p[4] / (p[0] * p[3] * p[5] * p[6]))
    N = [[-lam * K[i][j] - (ell[i] if i == j else I(0)) for j in range(3)] for i in range(3)]
    detN = det3(N)
    leading2_N = N[0][0] * N[1][1] - N[0][1] * N[1][0]
    assert detN.lo > 0
    adj = [[cofactor(N, j, i) for j in range(3)] for i in range(3)]
    E = []
    for i, j in COORDS:
        e = [[I(0) for _ in range(3)] for _ in range(3)]
        e[i][j] = I(1)
        e[j][i] = I(1)
        E.append(e)
    avec = [trace(mmul(adj, e)) for e in E]
    Htilde = [
        [detN * Fpair[i][j] + trace(mmul(mmul(mmul(adj, E[i]), adj), E[j])) for j in range(6)]
        for i in range(6)
    ]
    h, pivots = solve_interval(Htilde, avec)
    residual = [sum(Htilde[i][j] * h[j] for j in range(6)) - avec[i] for i in range(6)]
    beta_times_sqrtZ = sum(g[i] * h[i] for i in range(6))
    dalpha = sum(avec[i] * h[i] for i in range(6))
    return {
        "beta_times_sqrtZ": beta_times_sqrtZ,
        "dalpha": dalpha,
        "detN": detN,
        "N00": N[0][0],
        "leading2_N": leading2_N,
        "min_p": I(min(x.lo for x in p), min(x.hi for x in p)),
        "pivots_exclude_zero": all(not (piv.lo <= 0 <= piv.hi) for piv in pivots),
        "pivot_abs_lower": min(min(abs(piv.lo), abs(piv.hi)) for piv in pivots if not (piv.lo <= 0 <= piv.hi)),
        "residual_contains_zero": all(r.lo <= 0 <= r.hi for r in residual),
    }


def interval_certificate(eps: Q, left0: Q, right0: Q, steps: int, dps: int) -> dict[str, Any]:
    left, right, trace_rows = refine_kappa(eps, left0, right0, steps, dps)
    left_q = interval_quantities(eps, left, left)
    right_q = interval_quantities(eps, right, right)
    whole_q = interval_quantities(eps, left, right)
    return {
        "epsilon": qstr(eps),
        "coarse_kappa_bracket": [qstr(left0), qstr(right0)],
        "certified_kappa_bracket": [qstr(left), qstr(right)],
        "certified_width": qstr(right - left),
        "endpoint_left_beta_times_sqrtZ": interval_json(left_q["beta_times_sqrtZ"]),
        "endpoint_right_beta_times_sqrtZ": interval_json(right_q["beta_times_sqrtZ"]),
        "whole_bracket_dalpha": interval_json(whole_q["dalpha"]),
        "whole_bracket_min_p": interval_json(whole_q["min_p"]),
        "whole_bracket_detN": interval_json(whole_q["detN"]),
        "whole_bracket_N00": interval_json(whole_q["N00"]),
        "whole_bracket_leading2_N": interval_json(whole_q["leading2_N"]),
        "left_sign_certified_positive": left_q["beta_times_sqrtZ"].lo > 0,
        "right_sign_certified_negative": right_q["beta_times_sqrtZ"].hi < 0,
        "whole_bracket_dalpha_hi_lt_one": whole_q["dalpha"].hi < 1,
        "whole_bracket_min_p_lo_gt_zero": whole_q["min_p"].lo > 0,
        "whole_bracket_detN_lo_gt_zero": whole_q["detN"].lo > 0,
        "whole_bracket_N_leading_minors_positive": whole_q["N00"].lo > 0 and whole_q["leading2_N"].lo > 0 and whole_q["detN"].lo > 0,
        "pivots_exclude_zero": whole_q["pivots_exclude_zero"],
        "pivot_abs_lower": str(whole_q["pivot_abs_lower"]),
        "residual_contains_zero": whole_q["residual_contains_zero"],
        "bisection_tail": trace_rows[-6:],
    }


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="outputs/sparse_phase_certificate.json")
    parser.add_argument("--table-exps", default="4,8,12,16,20,24")
    parser.add_argument("--table-steps", type=int, default=80)
    parser.add_argument("--cert-exp", type=int, default=12)
    parser.add_argument("--cert-steps", type=int, default=22)
    ns = parser.parse_args()
    start = time.time()
    output = Path(ns.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    table = []
    coarse_by_exp = {}
    for exp in [int(x) for x in ns.table_exps.split(",") if x.strip()]:
        eps = Q(1, 10**exp)
        dps = max(220, 100 + 12 * exp)
        left0, right0, coarse_rows = coarse_bracket(eps, dps)
        coarse_by_exp[exp] = (left0, right0)
        left, right, trace_rows = refine_kappa(eps, left0, right0, ns.table_steps, dps)
        row = root_row(eps, left, right, dps)
        row["coarse_bracket"] = [qstr(left0), qstr(right0)]
        row["coarse_rows_until_bracket"] = coarse_rows
        row["bisection_tail"] = trace_rows[-6:]
        row["dps"] = dps
        table.append(row)
    cert_exp = ns.cert_exp
    cert_eps = Q(1, 10**cert_exp)
    if cert_exp not in coarse_by_exp:
        dps = max(260, 120 + 14 * cert_exp)
        coarse_by_exp[cert_exp] = coarse_bracket(cert_eps, dps)[:2]
    certificate = interval_certificate(cert_eps, *coarse_by_exp[cert_exp], ns.cert_steps, max(320, 140 + 14 * cert_exp))
    ok = (
        certificate["left_sign_certified_positive"]
        and certificate["right_sign_certified_negative"]
        and certificate["whole_bracket_dalpha_hi_lt_one"]
        and certificate["whole_bracket_min_p_lo_gt_zero"]
        and certificate["whole_bracket_detN_lo_gt_zero"]
        and certificate["whole_bracket_N_leading_minors_positive"]
        and certificate["pivots_exclude_zero"]
        and certificate["residual_contains_zero"]
    )
    result = {
        "status": "CERTIFIED_SPARSE_PHASE_ROOT_DALPHA_LT_ONE" if ok else "CERTIFICATE_FAILED",
        "task_source": {"baseline": TASK_SOURCE_BASELINE, "tree": TASK_SOURCE_TREE},
        "round2_reference_baseline": BASELINE,
        "pid": os.getpid(),
        "python": sys.version,
        "platform": platform.platform(),
        "mpmath": mp.__version__,
        "source_sha256": sha(Path(__file__)),
        "thread_env": {k: os.environ.get(k) for k in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"]},
        "family": "K=epsilon I+(7/10)uu^T with u1^2=2/5,u2^2=3/5,u3^2=kappa*epsilon; t=0 endpoint",
        "randomness": "none: fixed kappa grid and deterministic bisection",
        "table": table,
        "certificate": certificate,
        "interpretation": [
            "The certificate proves existence of at least one exact beta-zero kernel in the displayed kappa bracket.",
            "The whole certified bracket satisfies det(N)*alpha < 1, so it is not a B0 counterexample.",
            "The table is evidence for a sparse-edge phase-transition root tube with det(N)*alpha increasing toward 1 as epsilon decreases.",
        ],
        "elapsed_seconds": time.time() - start,
        "exit_status": 0 if ok else 1,
    }
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "pid": result["pid"],
        "table_rows": len(table),
        "certified_epsilon": certificate["epsilon"],
        "certified_kappa_bracket": certificate["certified_kappa_bracket"],
        "whole_bracket_dalpha": certificate["whole_bracket_dalpha"],
        "output": str(output),
        "elapsed_seconds": result["elapsed_seconds"],
    }))
    return result["exit_status"]


if __name__ == "__main__":
    raise SystemExit(main())
