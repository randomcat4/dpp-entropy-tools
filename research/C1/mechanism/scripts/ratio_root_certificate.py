#!/usr/bin/env python3
"""Ratio-degeneration beta-zero tube probe and one interval certificate.

Family:

    K = A(epsilon, r) = epsilon I + (3/5) u u^T,
    u proportional to (r, 2, 3), r > 0.

This is the t=0 endpoint of the assigned twisted-complement family.  It is
strict for epsilon < 2/5 and connected for r > 0.  The script first builds a
bounded deterministic high-precision table, then certifies one root bracket
using exact rational interval arithmetic.  The certificate proves existence of
at least one beta-zero kernel in the bracket and an entire-bracket upper bound
det(N) alpha < 1.  It does not prove uniqueness or the global B0 implication.
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

from mechanism_probe import (
    BASELINE,
    COORDS,
    LAMBDA,
    det3,
    evaluate,
    family_from_raw,
    mpstr,
    q_to_mpf,
    qstr,
    strict_by_leading_minors,
)


SUBSET_SIGNS = [(-1) ** (3 - int(mask).bit_count()) for mask in range(8)]


def log_unit(x: Q, terms: int = 90) -> tuple[Q, Q]:
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
    DEN = 2**360

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
        assert not other.lo <= 0 <= other.hi, "division by an interval containing zero"
        return self * I(1 / other.hi, 1 / other.lo)

    def __rtruediv__(self, other: Any) -> "I":
        return I(other) / self

    def __repr__(self) -> str:
        return f"I({self.lo},{self.hi})"


def interval_json(x: I, digits: int = 30) -> dict[str, str]:
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


def prod(A: list[list[I]], B: list[list[I]]) -> list[list[I]]:
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def tr(A: list[list[I]]) -> I:
    return sum(A[i][i] for i in range(len(A)))


def cof(A: list[list[I]], i: int, j: int) -> I:
    rows = [r for r in range(3) if r != i]
    cols = [c for c in range(3) if c != j]
    return ((-1) ** (i + j)) * (
        A[rows[0]][cols[0]] * A[rows[1]][cols[1]]
        - A[rows[0]][cols[1]] * A[rows[1]][cols[0]]
    )


def logi(x: I) -> I:
    assert x.lo > 0
    lo, _ = log_bound(x.lo)
    _, hi = log_bound(x.hi)
    return I(lo, hi)


def ratio_kernel_interval(eps: Q, rlo: Q, rhi: Q) -> list[list[I]]:
    r = I(rlo, rhi)
    two = I(2)
    three = I(3)
    raw = [r, two, three]
    norm = r * r + I(13)
    K: list[list[I]] = []
    for i in range(3):
        row: list[I] = []
        for j in range(3):
            entry = I(LAMBDA) * raw[i] * raw[j] / norm
            if i == j:
                entry = entry + I(eps)
            row.append(entry)
        K.append(row)
    return K


def event_data_interval(K: list[list[I]]) -> tuple[list[I], list[list[I]]]:
    p: list[I] = []
    J: list[list[I]] = []
    for mask in range(8):
        M = [list(row) for row in K]
        for i in range(3):
            if not ((mask >> i) & 1):
                M[i][i] = M[i][i] - I(1)
        sign = SUBSET_SIGNS[mask]
        p.append(sign * det3(M))
        J.append([sign * (cof(M, i, j) + (cof(M, j, i) if i != j else I(0))) for i, j in COORDS])
    return p, J


def solve_interval(A: list[list[I]], b: list[I]) -> tuple[list[I], list[I]]:
    work = [list(row) + [b[i]] for i, row in enumerate(A)]
    n = len(b)
    pivots: list[I] = []
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


def interval_quantities(eps: Q, rlo: Q, rhi: Q) -> dict[str, Any]:
    K = ratio_kernel_interval(eps, rlo, rhi)
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
    assert detN.lo > 0
    leading2_N = N[0][0] * N[1][1] - N[0][1] * N[1][0]
    adj = [[cof(N, j, i) for j in range(3)] for i in range(3)]
    E = []
    for i, j in COORDS:
        e = [[I(0) for _ in range(3)] for _ in range(3)]
        e[i][j] = I(1)
        e[j][i] = I(1)
        E.append(e)
    a_vec = [tr(prod(adj, e)) for e in E]
    Htilde = [
        [detN * Fpair[i][j] + tr(prod(prod(prod(adj, E[i]), adj), E[j])) for j in range(6)]
        for i in range(6)
    ]
    h, pivots = solve_interval(Htilde, a_vec)
    residual = [sum(Htilde[i][j] * h[j] for j in range(6)) - a_vec[i] for i in range(6)]
    beta_times_sqrtZ = sum(g[i] * h[i] for i in range(6))
    dalpha = sum(a_vec[i] * h[i] for i in range(6))
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


def coarse_grid() -> list[Q]:
    vals = []
    for exp in range(8, -1, -1):
        scale = Q(1, 10**exp)
        vals.extend([scale, 2 * scale, 5 * scale])
    vals.extend([Q(1), Q(2), Q(5)])
    return sorted(set(v for v in vals if v > 0))


def find_coarse_bracket(eps: Q, dps: int) -> tuple[Q, Q, list[dict[str, str]]]:
    rows: list[dict[str, str]] = []
    prev: tuple[Q, mp.mpf] | None = None
    for r in coarse_grid():
        fam = family_from_raw("ratio", eps, [r, Q(2), Q(3)])
        q = evaluate(fam["A"], dps)
        val = q["beta_times_sqrtZ"]
        rows.append({"r": qstr(r), "beta_times_sqrtZ": mpstr(val, 35), "dalpha": mpstr(q["dalpha"], 35)})
        if prev is not None and prev[1] * val < 0:
            return prev[0], r, rows
        prev = (r, val)
    raise RuntimeError(f"no sign bracket found for eps={eps}")


def refine_r_bracket(eps: Q, left: Q, right: Q, steps: int, dps: int) -> tuple[Q, Q, list[dict[str, str]]]:
    left_val = evaluate(family_from_raw("ratio", eps, [left, Q(2), Q(3)])["A"], dps)["beta_times_sqrtZ"]
    right_val = evaluate(family_from_raw("ratio", eps, [right, Q(2), Q(3)])["A"], dps)["beta_times_sqrtZ"]
    assert left_val * right_val < 0
    trace_rows: list[dict[str, str]] = []
    for _ in range(steps):
        mid = (left + right) / 2
        q = evaluate(family_from_raw("ratio", eps, [mid, Q(2), Q(3)])["A"], dps)
        val = q["beta_times_sqrtZ"]
        trace_rows.append({"r": qstr(mid), "beta_times_sqrtZ": mpstr(val, 45), "dalpha": mpstr(q["dalpha"], 45)})
        if left_val * val <= 0:
            right = mid
            right_val = val
        else:
            left = mid
            left_val = val
    return left, right, trace_rows


def high_precision_root_row(eps: Q, left: Q, right: Q, dps: int) -> dict[str, Any]:
    mid = (left + right) / 2
    fam = family_from_raw("ratio", eps, [mid, Q(2), Q(3)])
    q = evaluate(fam["A"], dps)
    sqrt_eps = mp.sqrt(q_to_mpf(eps))
    cbrt_eps = q_to_mpf(eps) ** (mp.mpf(1) / 3)
    return {
        "epsilon": qstr(eps),
        "r_bracket": [qstr(left), qstr(right)],
        "r_mid": qstr(mid),
        "r_over_sqrt_epsilon": mpstr(q_to_mpf(mid) / sqrt_eps, 40),
        "r_over_cuberoot_epsilon": mpstr(q_to_mpf(mid) / cbrt_eps, 40),
        "edge_ratio_A12_over_A23": mpstr(q_to_mpf(mid) / 3, 40),
        "edge_ratio_A13_over_A23": mpstr(q_to_mpf(mid) / 2, 40),
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
        "strict_A_mid": strict_by_leading_minors(fam["A"]),
    }


def certificate_for(eps: Q, coarse_left: Q, coarse_right: Q, cert_steps: int, dps: int) -> dict[str, Any]:
    left, right, trace_rows = refine_r_bracket(eps, coarse_left, coarse_right, cert_steps, dps)
    left_i = interval_quantities(eps, left, left)
    right_i = interval_quantities(eps, right, right)
    whole_i = interval_quantities(eps, left, right)
    return {
        "epsilon": qstr(eps),
        "coarse_bracket": [qstr(coarse_left), qstr(coarse_right)],
        "certified_r_bracket": [qstr(left), qstr(right)],
        "certified_width": qstr(right - left),
        "certification_bisection_steps": cert_steps,
        "endpoint_left_beta_times_sqrtZ": interval_json(left_i["beta_times_sqrtZ"], 35),
        "endpoint_right_beta_times_sqrtZ": interval_json(right_i["beta_times_sqrtZ"], 35),
        "whole_bracket_dalpha": interval_json(whole_i["dalpha"], 35),
        "whole_bracket_min_p": interval_json(whole_i["min_p"], 35),
        "whole_bracket_detN": interval_json(whole_i["detN"], 35),
        "whole_bracket_N00": interval_json(whole_i["N00"], 35),
        "whole_bracket_leading2_N": interval_json(whole_i["leading2_N"], 35),
        "pivots_exclude_zero": whole_i["pivots_exclude_zero"],
        "pivot_abs_lower": str(whole_i["pivot_abs_lower"]),
        "residual_contains_zero": whole_i["residual_contains_zero"],
        "left_sign_certified_positive": left_i["beta_times_sqrtZ"].lo > 0,
        "right_sign_certified_negative": right_i["beta_times_sqrtZ"].hi < 0,
        "whole_bracket_dalpha_hi_lt_one": whole_i["dalpha"].hi < 1,
        "whole_bracket_min_p_lo_gt_zero": whole_i["min_p"].lo > 0,
        "whole_bracket_detN_lo_gt_zero": whole_i["detN"].lo > 0,
        "whole_bracket_N_leading_minors_positive": whole_i["N00"].lo > 0 and whole_i["leading2_N"].lo > 0 and whole_i["detN"].lo > 0,
        "bisection_tail": trace_rows[-6:],
    }


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="outputs/ratio_root_certificate.json")
    parser.add_argument("--max-exp", type=int, default=8)
    parser.add_argument("--table-steps", type=int, default=80)
    parser.add_argument("--cert-exp", type=int, default=8)
    parser.add_argument("--cert-steps", type=int, default=20)
    ns = parser.parse_args()
    start = time.time()
    output = Path(ns.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    result: dict[str, Any] = {
        "status": "RUNNING",
        "baseline": BASELINE,
        "pid": os.getpid(),
        "python": sys.version,
        "platform": platform.platform(),
        "mpmath": mp.__version__,
        "source_sha256": sha(Path(__file__)),
        "mechanism_probe_sha256": sha(Path(__file__).resolve().with_name("mechanism_probe.py")),
        "thread_env": {k: os.environ.get(k) for k in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"]},
        "family": "A(epsilon,r)=epsilon I+(3/5)uu^T, u proportional to (r,2,3), t=0 endpoint",
        "randomness": "none: deterministic 1/2/5-per-decade r grid and bisection",
        "table": [],
        "certificate": None,
        "exit_status": 0,
    }
    bracket_by_exp: dict[int, tuple[Q, Q]] = {}
    for exp in range(2, ns.max_exp + 1):
        eps = Q(1, 10**exp)
        dps = max(220, 140 + 25 * exp)
        coarse_left, coarse_right, coarse_rows = find_coarse_bracket(eps, dps)
        left, right, trace_rows = refine_r_bracket(eps, coarse_left, coarse_right, ns.table_steps, dps)
        bracket_by_exp[exp] = (coarse_left, coarse_right)
        row = high_precision_root_row(eps, left, right, dps)
        row["coarse_bracket"] = [qstr(coarse_left), qstr(coarse_right)]
        row["coarse_rows_until_bracket"] = coarse_rows
        row["bisection_tail"] = trace_rows[-6:]
        row["dps"] = dps
        result["table"].append(row)
    cert_eps = Q(1, 10**ns.cert_exp)
    result["certificate"] = certificate_for(cert_eps, *bracket_by_exp[ns.cert_exp], ns.cert_steps, max(260, 160 + 30 * ns.cert_exp))
    checks = result["certificate"]
    ok = (
        checks["left_sign_certified_positive"]
        and checks["right_sign_certified_negative"]
        and checks["whole_bracket_dalpha_hi_lt_one"]
        and checks["whole_bracket_min_p_lo_gt_zero"]
        and checks["whole_bracket_detN_lo_gt_zero"]
        and checks["whole_bracket_N_leading_minors_positive"]
        and checks["pivots_exclude_zero"]
        and checks["residual_contains_zero"]
    )
    result["status"] = "CERTIFIED_RATIO_ROOT_DALPHA_LT_ONE" if ok else "CERTIFICATE_FAILED"
    result["elapsed_seconds"] = time.time() - start
    result["exit_status"] = 0 if ok else 1
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "pid": result["pid"],
        "table_rows": len(result["table"]),
        "certified_epsilon": checks["epsilon"],
        "certified_r_bracket": checks["certified_r_bracket"],
        "whole_bracket_dalpha": checks["whole_bracket_dalpha"],
        "output": str(output),
        "elapsed_seconds": result["elapsed_seconds"],
    }))
    return result["exit_status"]


if __name__ == "__main__":
    raise SystemExit(main())
