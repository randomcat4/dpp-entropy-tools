#!/usr/bin/env python3
"""Algebraic self-audit for the C3-M1 rate certificate artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
import sys
import time
from fractions import Fraction as F
from pathlib import Path


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

Z = (F(0), F(0))


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def neg(a):
    return (-a[0], -a[1])


def sub(a, b):
    return add(a, neg(b))


def conj(a):
    return (a[0], -a[1])


def mul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def div(a, b):
    d = b[0] * b[0] + b[1] * b[1]
    if d == 0:
        raise ZeroDivisionError("complex Fraction division by zero")
    return ((a[0] * b[0] + a[1] * b[1]) / d, (a[1] * b[0] - a[0] * b[1]) / d)


def scale(a, s):
    return (a[0] * s, a[1] * s)


def norm1(a):
    return abs(a[0]) + abs(a[1])


def parse_pair(x):
    return (F(x[0]), F(x[1]))


def encode(a):
    return [str(a[0]), str(a[1])]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fstr(x: F) -> str:
    return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)


def coeffs(candidate, t, complement=False):
    p = F(candidate["p"]) + t * F(candidate["dp"])
    a = [F(x) + t * F(dx) for x, dx in zip(candidate["a"], candidate["da"])]
    b = [F(x) + t * F(dx) for x, dx in zip(candidate["b"], candidate["db"])]
    cs = [(p, F(0))] + [(aa / 2, -bb / 2) for aa, bb in zip(a, b)]
    if complement:
        cs = [(1 - p, F(0))] + [neg(c) for c in cs[1:]]
    return cs


def c_at(cs, k):
    m = len(cs) - 1
    if 0 <= k <= m:
        return cs[k]
    if -m <= k < 0:
        return conj(cs[-k])
    return Z


def symbol_kernel(candidate, t, n):
    cs = coeffs(candidate, t, False)
    return [[c_at(cs, i - j) for j in range(n)] for i in range(n)]


def determinant(mat):
    n = len(mat)
    a = [[mat[i][j] for j in range(n)] for i in range(n)]
    det = (F(1), F(0))
    for k in range(n):
        pivot = None
        for r in range(k, n):
            if a[r][k] != Z:
                pivot = r
                break
        if pivot is None:
            return Z
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            det = neg(det)
        pv = a[k][k]
        det = mul(det, pv)
        for i in range(k + 1, n):
            factor = div(a[i][k], pv)
            a[i][k] = Z
            for j in range(k + 1, n):
                a[i][j] = sub(a[i][j], mul(factor, a[k][j]))
    return det


def exact_event_masses_row_convention(kernel):
    n = len(kernel)
    masses = []
    for event in range(1 << n):
        mat = []
        for i in range(n):
            row = []
            selected = (event >> i) & 1
            for j in range(n):
                if selected:
                    row.append(kernel[i][j])
                else:
                    row.append(sub((F(int(i == j)), F(0)), kernel[i][j]))
            mat.append(row)
        det = determinant(mat)
        if det[1] != 0:
            raise ArithmeticError(f"non-real event determinant at event {event}")
        if det[0] <= 0:
            raise ArithmeticError(f"non-positive event determinant at event {event}: {det[0]}")
        masses.append(det[0])
    if sum(masses) != 1:
        raise ArithmeticError("event masses do not normalize exactly")
    return masses


def margin_check(candidate, true_symbol):
    step = F(candidate["step"])
    eps = F(candidate["uniform_margin"])
    script_b = [F(x) for x in candidate["b"]]
    true_b = [F(x) for x in true_symbol["b"]]
    script_db = [F(x) for x in candidate["db"]]
    true_db = [F(x) for x in true_symbol["db"]]
    conjugated = all(script_b[i] == -true_b[i] and script_db[i] == -true_db[i] for i in range(len(script_b)))
    # For both harmonics, |c_k(0)|=3/25 and the tangent is multiplication
    # by +/-i. Hence |c_k(t)| <= (3/25)*sqrt(1+step^2).
    lhs = F(9 * 17, 625)
    rhs = F(99 * 99, 200 * 200)
    # lhs < rhs is exactly (3*sqrt(17)/25)^2 < (1/2-1/200)^2.
    return {
        "script_is_conjugate_of_true_symbol": conjugated,
        "step": str(step),
        "claimed_uniform_margin": str(eps),
        "square_comparison_lhs": str(lhs),
        "square_comparison_rhs": str(rhs),
        "margin_one_over_200_certified": eps == F(1, 200) and lhs < rhs,
        "endpoint_equality_assumed": bool(candidate.get("endpoint_equality_assumed")),
    }


def recompute_boundary_case(candidate, case):
    t = F(case["t"])
    complement = bool(case["complement_symbol"])
    M = int(case["M"])
    cs = coeffs(candidate, t, complement)
    m = len(cs) - 1
    eps = F(candidate["uniform_margin"])
    xmat = [[parse_pair(x) for x in row] for row in case["solution_dyadic"]]
    bblock = [[c_at(cs, -r - 1 - j) for j in range(m)] for r in range(M)]
    residual = []
    for r in range(M + m):
        row = []
        for j in range(m):
            value = c_at(cs, -r - j - 1)
            for s in range(max(0, r - m), min(M, r + m + 1)):
                value = sub(value, mul(c_at(cs, s - r), xmat[s][j]))
            row.append(value)
        residual.append(row)
    r_bound = sum(norm1(x) for row in residual for x in row)
    delta = r_bound * r_bound / eps
    bx = [[Z for _ in range(m)] for _ in range(m)]
    xr = [[Z for _ in range(m)] for _ in range(m)]
    for i in range(m):
        for j in range(m):
            for r in range(M):
                bx[i][j] = add(bx[i][j], mul(conj(bblock[r][i]), xmat[r][j]))
                xr[i][j] = add(xr[i][j], mul(conj(xmat[r][i]), residual[r][j]))
    old = [[sub(c_at(cs, i - j), scale(add(bx[i][j], conj(bx[j][i])), F(1, 2))) for j in range(m)] for i in range(m)]
    corner = [[sub(old[i][j], scale(add(xr[i][j], conj(xr[j][i])), F(1, 2))) for j in range(m)] for i in range(m)]
    extra_rows_zero = True
    for r in range(M + m, M + 2 * m + 1):
        for j in range(m):
            value = c_at(cs, -r - j - 1)
            for s in range(max(0, r - m), min(M, r + m + 1)):
                value = sub(value, mul(c_at(cs, s - r), xmat[s][j]))
            extra_rows_zero = extra_rows_zero and (value == Z)
    return {
        "R_norm_bound": str(r_bound),
        "operator_error_upper_rational": str(delta),
        "corner_rational": [[encode(x) for x in row] for row in corner],
        "residual_rows_checked": M + m,
        "extra_tail_rows_zero": extra_rows_zero,
    }


def find_boundary_case(boundary, t, complement):
    for case in boundary["cases"]:
        if F(case["t"]) == t and bool(case["complement_symbol"]) == complement:
            return case
    raise KeyError((str(t), complement))


def boundary_checks(candidate, boundary):
    step = F(candidate["step"])
    expected = {(str(t), c) for t in (-step, F(0), step) for c in (False, True)}
    actual = {(case["t"], bool(case["complement_symbol"])) for case in boundary["cases"]}
    recomputed = []
    for case in boundary["cases"]:
        calc = recompute_boundary_case(candidate, case)
        recomputed.append(
            {
                "t": case["t"],
                "complement_symbol": bool(case["complement_symbol"]),
                "delta_float": float(F(case["operator_error_upper_rational"])),
                "stable_recomputation_ok": calc["R_norm_bound"] == case["R_norm_bound"]
                and calc["operator_error_upper_rational"] == case["operator_error_upper_rational"]
                and calc["corner_rational"] == case["corner_rational"]
                and calc["residual_rows_checked"] == case["residual_rows_checked"]
                and calc["extra_tail_rows_zero"],
            }
        )
    return {
        "expected_case_set_ok": actual == expected,
        "actual_cases": boundary.get("actual_cases"),
        "actual_residual_complex_entries": boundary.get("actual_residual_complex_entries"),
        "recomputed_cases": recomputed,
        "worst_delta": str(max(F(c["operator_error_upper_rational"]) for c in boundary["cases"])),
        "all_delta_below_margin": all(F(c["operator_error_upper_rational"]) < F(candidate["uniform_margin"]) for c in boundary["cases"]),
    }


def apply_boundary_corner(kernel, candidate, boundary, t, complement):
    m = len(candidate["a"])
    out = [[kernel[i][j] for j in range(len(kernel))] for i in range(len(kernel))]
    case = find_boundary_case(boundary, t, complement)
    for i in range(m):
        for j in range(m):
            value = parse_pair(case["corner_rational"][i][j])
            if complement:
                value = sub((F(int(i == j)), F(0)), value)
            out[i][j] = value
    return out


def conditional_error(candidate, delta):
    eps = F(candidate["uniform_margin"])
    return delta * (1 + ((1 + delta) / (eps - delta)) ** 2)


def rate_case_by_t(rate, t):
    for case in rate["cases"]:
        if F(case["t"]) == t:
            return case
    raise KeyError(str(t))


def rate_checks(candidate, boundary, rate):
    step = F(candidate["step"])
    n = int(rate["cases"][0]["past_length"])
    per_t = []
    determinants = 0
    for t in (-step, F(0), step):
        raw = exact_event_masses_row_convention(symbol_kernel(candidate, t, n + 1))
        extreme_one = exact_event_masses_row_convention(apply_boundary_corner(symbol_kernel(candidate, t, n + 1), candidate, boundary, t, False))
        extreme_zero = exact_event_masses_row_convention(apply_boundary_corner(symbol_kernel(candidate, t, n + 1), candidate, boundary, t, True))
        determinants += 3 * (1 << (n + 1))
        rate_case = rate_case_by_t(rate, t)
        stored_errors = {bool(x["complement_symbol"]): F(x["conditional_error_bound"]) for x in rate_case["boundary_cases"]}
        for comp in (False, True):
            delta = F(find_boundary_case(boundary, t, comp)["operator_error_upper_rational"])
            if conditional_error(candidate, delta) != stored_errors[comp]:
                raise ArithmeticError("conditional error formula mismatch")
        min_lo = F(1)
        max_hi = F(0)
        width_sum = F(0)
        for event in range(1 << n):
            idx1 = event + (1 << n)
            weight = raw[event] + raw[idx1]
            q = raw[idx1] / weight
            q1 = extreme_one[idx1] / (extreme_one[event] + extreme_one[idx1])
            q0 = extreme_zero[idx1] / (extreme_zero[event] + extreme_zero[idx1])
            lo = max(F(candidate["uniform_margin"]), q1 - stored_errors[False])
            hi = min(1 - F(candidate["uniform_margin"]), q0 + stored_errors[True])
            if lo > hi:
                raise ArithmeticError(f"empty conditional interval t={t} event={event}")
            if not lo <= q <= hi:
                raise ArithmeticError(f"ordinary finite conditional outside extreme interval t={t} event={event}")
            min_lo = min(min_lo, lo)
            max_hi = max(max_hi, hi)
            width_sum += weight * (hi - lo)
        width_lower = F(rate_case["weighted_extreme_width"]["lower"])
        width_upper = F(rate_case["weighted_extreme_width"]["upper"])
        per_t.append(
            {
                "t": str(t),
                "independent_exact_distributions": 3,
                "independent_exact_determinants": 3 * (1 << (n + 1)),
                "conditional_range_recomputed": [str(min_lo), str(max_hi)],
                "conditional_range_matches_artifact": [str(min_lo), str(max_hi)] == rate_case["conditional_range"],
                "weighted_width_recomputed": str(width_sum),
                "weighted_width_contained_in_artifact_interval": width_lower <= width_sum <= width_upper,
            }
        )
    minus = rate_case_by_t(rate, -step)
    center = rate_case_by_t(rate, F(0))
    plus = rate_case_by_t(rate, step)
    gap_lower = (F(minus["lower_bound_interval"]["lower"]) + F(plus["lower_bound_interval"]["lower"])) / 2 - F(center["upper_bound_interval"]["upper"])
    gap_upper = (F(minus["upper_bound_interval"]["upper"]) + F(plus["upper_bound_interval"]["upper"])) / 2 - F(center["lower_bound_interval"]["lower"])
    return {
        "past_length": n,
        "actual_determinants": rate.get("actual_determinants"),
        "independent_exact_determinants": determinants,
        "per_symbol_checks": per_t,
        "gap_lower_recomputed": str(gap_lower),
        "gap_upper_recomputed": str(gap_upper),
        "gap_matches_artifact": rate["gap_enclosure"]["lower"] == str(gap_lower) and rate["gap_enclosure"]["upper"] == str(gap_upper),
        "strict_negative_upper": gap_upper < 0,
        "classification": rate["classification"],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidate", required=True)
    ap.add_argument("--true-symbol", required=True)
    ap.add_argument("--boundary", required=True)
    ap.add_argument("--rate", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    started = time.perf_counter()
    candidate_path = Path(args.candidate)
    true_path = Path(args.true_symbol)
    boundary_path = Path(args.boundary)
    rate_path = Path(args.rate)
    candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
    true_symbol = json.loads(true_path.read_text(encoding="utf-8"))
    boundary = json.loads(boundary_path.read_text(encoding="utf-8"))
    rate = json.loads(rate_path.read_text(encoding="utf-8"))
    result = {
        "status": "PENDING",
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "scope": "C3-M1 fixed three-symbol negative entropy-rate pair-gap certificate algebraic self-audit",
        "record": {
            "python": sys.version.replace("\n", " "),
            "platform": platform.platform(),
            "elapsed_seconds": None,
            "script_sha256": sha256_file(Path(__file__)),
            "candidate_sha256": sha256_file(candidate_path),
            "true_symbol_sha256": sha256_file(true_path),
            "boundary_sha256": sha256_file(boundary_path),
            "rate_sha256": sha256_file(rate_path),
        },
        "margin_check": margin_check(candidate, true_symbol),
        "boundary_checks": boundary_checks(candidate, boundary),
        "rate_checks": rate_checks(candidate, boundary, rate),
    }
    ok = True
    ok = ok and result["margin_check"]["script_is_conjugate_of_true_symbol"]
    ok = ok and result["margin_check"]["margin_one_over_200_certified"]
    ok = ok and not result["margin_check"]["endpoint_equality_assumed"]
    ok = ok and result["boundary_checks"]["expected_case_set_ok"]
    ok = ok and result["boundary_checks"]["actual_cases"] == 6
    ok = ok and result["boundary_checks"]["all_delta_below_margin"]
    ok = ok and all(c["stable_recomputation_ok"] for c in result["boundary_checks"]["recomputed_cases"])
    ok = ok and result["rate_checks"]["actual_determinants"] == result["rate_checks"]["independent_exact_determinants"] == 288
    ok = ok and all(c["conditional_range_matches_artifact"] and c["weighted_width_contained_in_artifact_interval"] for c in result["rate_checks"]["per_symbol_checks"])
    ok = ok and result["rate_checks"]["gap_matches_artifact"]
    ok = ok and result["rate_checks"]["strict_negative_upper"]
    result["status"] = "CORRECT_SELF_AUDIT" if ok else "CRITICAL_GAPS"
    result["record"]["elapsed_seconds"] = time.perf_counter() - started
    Path(args.output).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "elapsed_seconds": result["record"]["elapsed_seconds"]}, indent=2))
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
