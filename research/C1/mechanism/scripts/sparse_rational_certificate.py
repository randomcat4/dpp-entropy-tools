#!/usr/bin/env python3
"""Rational sparse-edge beta-zero certificate for C1/B0.

Family:

    K(epsilon, q) = epsilon I + (7/10) u(q) u(q)^T,
    u(q) = (3/5, 4/5, q sqrt(epsilon)).

For epsilon=10^-8 and rational q, every entry of K is rational.  This script
uses high-precision bisection only to choose a bracket, then certifies the
bracket by exact rational outward-rounded interval arithmetic.  The certificate
proves an exact beta zero in q and a whole-bracket bound det(N) alpha < 1.
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

from mechanism_probe import (
    BASELINE,
    COORDS,
    TASK_SOURCE_BASELINE,
    TASK_SOURCE_TREE,
    det3,
    evaluate,
    mpstr,
    q_to_mpf,
    qstr,
    strict_by_leading_minors,
)


LAMBDA = Q(7, 10)
SUBSET_SIGNS = [(-1) ** (3 - int(mask).bit_count()) for mask in range(8)]


def sqrt_eps_for_exp(exp: int) -> Q:
    if exp % 2:
        raise ValueError("this rational family expects epsilon=10^-exp with even exp")
    return Q(1, 10 ** (exp // 2))


def rational_sparse_K(exp: int, q: Q) -> list[list[Q]]:
    eps = Q(1, 10**exp)
    se = sqrt_eps_for_exp(exp)
    raw = [Q(3, 5), Q(4, 5), q * se]
    return [[(eps if i == j else Q(0)) + LAMBDA * raw[i] * raw[j] for j in range(3)] for i in range(3)]


def eval_sparse(exp: int, q: Q, dps: int) -> dict[str, Any]:
    return evaluate(rational_sparse_K(exp, q), dps)


def coarse_bracket(exp: int, dps: int) -> tuple[Q, Q, list[dict[str, str]]]:
    grid = [Q(1), Q(5, 4), Q(3, 2), Q(7, 4), Q(2), Q(5, 2), Q(3)]
    rows = []
    prev = None
    for q in grid:
        ev = eval_sparse(exp, q, dps)
        val = ev["beta_times_sqrtZ"]
        rows.append({"q": qstr(q), "kappa": qstr(q * q), "beta_times_sqrtZ": mpstr(val, 40), "dalpha": mpstr(ev["dalpha"], 40)})
        if prev is not None and prev[1] * val < 0:
            return prev[0], q, rows
        prev = (q, val)
    raise RuntimeError(f"no q sign change for epsilon=1e-{exp}")


def refine(exp: int, left: Q, right: Q, steps: int, dps: int) -> tuple[Q, Q, list[dict[str, str]]]:
    left_val = eval_sparse(exp, left, dps)["beta_times_sqrtZ"]
    right_val = eval_sparse(exp, right, dps)["beta_times_sqrtZ"]
    assert left_val * right_val < 0
    trace = []
    for _ in range(steps):
        mid = (left + right) / 2
        ev = eval_sparse(exp, mid, dps)
        val = ev["beta_times_sqrtZ"]
        trace.append({"q": qstr(mid), "kappa": qstr(mid * mid), "beta_times_sqrtZ": mpstr(val, 50), "dalpha": mpstr(ev["dalpha"], 50)})
        if left_val * val <= 0:
            right = mid
            right_val = val
        else:
            left = mid
            left_val = val
    return left, right, trace


def root_row(exp: int, left: Q, right: Q, dps: int) -> dict[str, Any]:
    mid = (left + right) / 2
    ev = eval_sparse(exp, mid, dps)
    eps = Q(1, 10**exp)
    return {
        "epsilon": qstr(eps),
        "q_bracket": [qstr(left), qstr(right)],
        "q_mid": qstr(mid),
        "kappa_mid": qstr(mid * mid),
        "u3_squared_mid": qstr(mid * mid * eps),
        "beta_times_sqrtZ_mid": mpstr(ev["beta_times_sqrtZ"], 55),
        "beta_mid": mpstr(ev["beta"], 55),
        "dalpha_mid": mpstr(ev["dalpha"], 55),
        "alpha_mid": mpstr(ev["alpha"], 55),
        "detN_mid": mpstr(ev["detN"], 55),
        "min_probability_mid": mpstr(ev["min_probability"], 35),
        "D_M_coords_mid": [mpstr(x, 55) for x in ev["D_M_coords"]],
        "D_M_max_abs_coord_mid": mpstr(ev["D_M_max_abs_coord"], 55),
        "eta_D_M_mid": mpstr(ev["eta_D_M"], 55),
        "Lambda_prime_D_M_mid": mpstr(ev["Lambda_prime_D_M"], 55),
        "negative_entropy_quadratic_D_M_mid": mpstr(ev["negative_entropy_quadratic_at_D_M"], 55),
        "strict_K_mid": strict_by_leading_minors(rational_sparse_K(exp, mid)),
    }


def log_unit(x: Q, terms: int = 110) -> tuple[Q, Q]:
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
    DEN = 2**620

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


def logi(x: I) -> I:
    assert x.lo > 0
    lo, _ = log_bound(x.lo)
    _, hi = log_bound(x.hi)
    return I(lo, hi)


def sparse_K_interval(exp: int, qlo: Q, qhi: Q) -> list[list[I]]:
    eps = Q(1, 10**exp)
    se = sqrt_eps_for_exp(exp)
    q = I(qlo, qhi)
    raw = [I(Q(3, 5)), I(Q(4, 5)), q * I(se)]
    return [[I(eps if i == j else Q(0)) + I(LAMBDA) * raw[i] * raw[j] for j in range(3)] for i in range(3)]


def event_data_interval(K: list[list[I]]) -> tuple[list[I], list[list[I]]]:
    p = []
    J = []
    for mask in range(8):
        M = [list(row) for row in K]
        for i in range(3):
            if not ((mask >> i) & 1):
                M[i][i] = M[i][i] - I(1)
        sign = SUBSET_SIGNS[mask]
        p.append(sign * det3(M))
        J.append([sign * (cofactor(M, i, j) + (cofactor(M, j, i) if i != j else I(0))) for i, j in COORDS])
    return p, J


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


def interval_quantities(exp: int, qlo: Q, qhi: Q) -> dict[str, Any]:
    K = sparse_K_interval(exp, qlo, qhi)
    p, J = event_data_interval(K)
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


def family_strict_reason(exp: int, qlo: Q, qhi: Q) -> dict[str, str | bool]:
    eps = Q(1, 10**exp)
    max_norm2 = Q(1) + qhi * qhi * eps
    max_eigen_upper = eps + LAMBDA * max_norm2
    return {
        "epsilon_positive": eps > 0,
        "max_norm2": qstr(max_norm2),
        "max_eigen_upper": qstr(max_eigen_upper),
        "max_eigen_upper_lt_one": max_eigen_upper < 1,
        "connected_for_positive_q": qlo > 0,
    }


def certificate(exp: int, left0: Q, right0: Q, steps: int, dps: int) -> dict[str, Any]:
    left, right, trace_rows = refine(exp, left0, right0, steps, dps)
    left_i = interval_quantities(exp, left, left)
    right_i = interval_quantities(exp, right, right)
    whole_i = interval_quantities(exp, left, right)
    strict = family_strict_reason(exp, left, right)
    return {
        "epsilon": qstr(Q(1, 10**exp)),
        "coarse_q_bracket": [qstr(left0), qstr(right0)],
        "certified_q_bracket": [qstr(left), qstr(right)],
        "certified_kappa_bracket": [qstr(left * left), qstr(right * right)],
        "certified_width": qstr(right - left),
        "strict_reason": strict,
        "endpoint_left_beta_times_sqrtZ": interval_json(left_i["beta_times_sqrtZ"]),
        "endpoint_right_beta_times_sqrtZ": interval_json(right_i["beta_times_sqrtZ"]),
        "whole_bracket_dalpha": interval_json(whole_i["dalpha"]),
        "whole_bracket_min_p": interval_json(whole_i["min_p"]),
        "whole_bracket_detN": interval_json(whole_i["detN"]),
        "whole_bracket_N00": interval_json(whole_i["N00"]),
        "whole_bracket_leading2_N": interval_json(whole_i["leading2_N"]),
        "left_sign_certified_positive": left_i["beta_times_sqrtZ"].lo > 0,
        "right_sign_certified_negative": right_i["beta_times_sqrtZ"].hi < 0,
        "whole_bracket_dalpha_hi_lt_one": whole_i["dalpha"].hi < 1,
        "whole_bracket_min_p_lo_gt_zero": whole_i["min_p"].lo > 0,
        "whole_bracket_detN_lo_gt_zero": whole_i["detN"].lo > 0,
        "whole_bracket_N_leading_minors_positive": whole_i["N00"].lo > 0 and whole_i["leading2_N"].lo > 0 and whole_i["detN"].lo > 0,
        "pivots_exclude_zero": whole_i["pivots_exclude_zero"],
        "pivot_abs_lower": str(whole_i["pivot_abs_lower"]),
        "residual_contains_zero": whole_i["residual_contains_zero"],
        "bisection_tail": trace_rows[-6:],
    }


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="outputs/sparse_rational_certificate.json")
    parser.add_argument("--table-exps", default="6,8,12")
    parser.add_argument("--table-steps", type=int, default=80)
    parser.add_argument("--cert-exp", type=int, default=8)
    parser.add_argument("--cert-steps", type=int, default=24)
    ns = parser.parse_args()
    start = time.time()
    output = Path(ns.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    table = []
    coarse_by_exp = {}
    for exp in [int(x) for x in ns.table_exps.split(",") if x.strip()]:
        dps = max(220, 130 + 20 * exp)
        left0, right0, coarse_rows = coarse_bracket(exp, dps)
        coarse_by_exp[exp] = (left0, right0)
        left, right, trace_rows = refine(exp, left0, right0, ns.table_steps, dps)
        row = root_row(exp, left, right, dps)
        row["coarse_bracket"] = [qstr(left0), qstr(right0)]
        row["coarse_rows_until_bracket"] = coarse_rows
        row["bisection_tail"] = trace_rows[-6:]
        row["dps"] = dps
        table.append(row)
    cert_exp = ns.cert_exp
    if cert_exp not in coarse_by_exp:
        coarse_by_exp[cert_exp] = coarse_bracket(cert_exp, max(260, 150 + 20 * cert_exp))[:2]
    cert = certificate(cert_exp, *coarse_by_exp[cert_exp], ns.cert_steps, max(280, 160 + 20 * cert_exp))
    ok = (
        cert["strict_reason"]["epsilon_positive"]
        and cert["strict_reason"]["max_eigen_upper_lt_one"]
        and cert["strict_reason"]["connected_for_positive_q"]
        and cert["left_sign_certified_positive"]
        and cert["right_sign_certified_negative"]
        and cert["whole_bracket_dalpha_hi_lt_one"]
        and cert["whole_bracket_min_p_lo_gt_zero"]
        and cert["whole_bracket_detN_lo_gt_zero"]
        and cert["whole_bracket_N_leading_minors_positive"]
        and cert["pivots_exclude_zero"]
        and cert["residual_contains_zero"]
    )
    mp.mp.dps = 100
    kappa_star = (mp.mpf(3) / 7) * (mp.e ** (mp.mpf(40) / 21) - 1)
    result = {
        "status": "CERTIFIED_RATIONAL_SPARSE_ROOT_DALPHA_LT_ONE" if ok else "CERTIFICATE_FAILED",
        "task_source": {"baseline": TASK_SOURCE_BASELINE, "tree": TASK_SOURCE_TREE},
        "round2_reference_baseline": BASELINE,
        "pid": os.getpid(),
        "python": sys.version,
        "platform": platform.platform(),
        "mpmath": mp.__version__,
        "source_sha256": sha(Path(__file__)),
        "mechanism_probe_sha256": sha(Path(__file__).resolve().with_name("mechanism_probe.py")),
        "thread_env": {k: os.environ.get(k) for k in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"]},
        "family": "K=epsilon I+(7/10)uu^T, u=(3/5,4/5,q*sqrt(epsilon)); t=0 endpoint variant of the twisted-complement setup",
        "finite_epsilon_variant_note": "This is not the unit-normalized u1^2=2/5,u2^2=3/5,u3^2=kappa*epsilon finite-epsilon family. Here ||u||^2=1+q^2 epsilon and the top eigenvalue is epsilon+(7/10)(1+q^2 epsilon). The leading sparse phase mechanism has the same kappa=q^2 limit, but finite-epsilon certificates apply only to this displayed rational K.",
        "asymptotic_cue_not_used_for_certificate": {
            "kappa_star_formula": "3/7*(exp(40/21)-1)",
            "kappa_star_approx": mpstr(kappa_star, 50),
            "q_star_approx": mpstr(mp.sqrt(kappa_star), 50),
        },
        "randomness": "none: fixed q grid and deterministic bisection",
        "table": table,
        "certificate": cert,
        "interpretation": [
            "The certificate proves at least one exact beta-zero kernel in the displayed q/kappa bracket.",
            "The whole certified bracket satisfies det(N)*alpha < 1, so it is not a B0 counterexample.",
            "The high-precision table gives a near-boundary root tube with det(N)*alpha increasing as epsilon decreases.",
        ],
        "elapsed_seconds": time.time() - start,
        "exit_status": 0 if ok else 1,
    }
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "pid": result["pid"],
        "table_rows": len(table),
        "certified_epsilon": cert["epsilon"],
        "certified_q_bracket": cert["certified_q_bracket"],
        "whole_bracket_dalpha": cert["whole_bracket_dalpha"],
        "output": str(output),
        "elapsed_seconds": result["elapsed_seconds"],
    }))
    return result["exit_status"]


if __name__ == "__main__":
    raise SystemExit(main())
