#!/usr/bin/env python3
"""Independent bounded audit for the C3-M1 n=4 negative rate certificate.

The script deliberately avoids the author's Bareiss determinant routine.  For
the small n=5 event kernels it uses permutation determinants over exact
Fraction complex pairs.  It does not reimplement the interval-log entropy
builder; it verifies the exact rational gate, symbol convention, finite event
kernels, boundary residual records, and tail-row coverage.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
from itertools import permutations
import hashlib
import json
from pathlib import Path
import platform
import sys
import time


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

Z = (F(0), F(0))
O = (F(1), F(0))


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


def scale(a, s):
    return (a[0] * s, a[1] * s)


def norm1(a):
    return abs(a[0]) + abs(a[1])


def parse_pair(x):
    return (F(x[0]), F(x[1]))


def encode(a):
    return [str(a[0]), str(a[1])]


def sha256_file(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sign_perm(p):
    inv = 0
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            inv += p[i] > p[j]
    return -1 if inv % 2 else 1


def det_perm(mat):
    n = len(mat)
    total = Z
    for p in permutations(range(n)):
        term = O
        for i, j in enumerate(p):
            term = mul(term, mat[i][j])
        total = sub(total, term) if sign_perm(p) < 0 else add(total, term)
    return total


def exact_event_masses_row(kernel):
    n = len(kernel)
    out = []
    for event in range(1 << n):
        mat = []
        for i in range(n):
            selected = (event >> i) & 1
            row = []
            for j in range(n):
                if selected:
                    row.append(kernel[i][j])
                else:
                    row.append(sub((F(int(i == j)), F(0)), kernel[i][j]))
            mat.append(row)
        d = det_perm(mat)
        if d[1] != 0:
            raise ArithmeticError(f"non-real atom determinant event={event}")
        if d[0] <= 0:
            raise ArithmeticError(f"non-positive atom event={event} p={d[0]}")
        out.append(d[0])
    if sum(out) != 1:
        raise ArithmeticError("atom probabilities do not sum to one")
    return out


def script_coeffs(candidate, t, complement=False):
    p = F(candidate["p"]) + t * F(candidate["dp"])
    a = [F(x) + t * F(dx) for x, dx in zip(candidate["a"], candidate["da"])]
    b = [F(x) + t * F(dx) for x, dx in zip(candidate["b"], candidate["db"])]
    cs = [(p, F(0))] + [(aa / 2, -bb / 2) for aa, bb in zip(a, b)]
    if complement:
        cs = [(1 - p, F(0))] + [neg(c) for c in cs[1:]]
    return cs


def true_coeffs(true_symbol, t):
    p = F(true_symbol["p"]) + t * F(true_symbol["dp"])
    a = [F(x) + t * F(dx) for x, dx in zip(true_symbol["a"], true_symbol["da"])]
    b = [F(x) + t * F(dx) for x, dx in zip(true_symbol["b"], true_symbol["db"])]
    return [(p, F(0))] + [(aa / 2, bb / 2) for aa, bb in zip(a, b)]


def c_at(cs, k):
    m = len(cs) - 1
    if 0 <= k <= m:
        return cs[k]
    if -m <= k < 0:
        return conj(cs[-k])
    return Z


def kernel_from_coeffs(cs, n):
    return [[c_at(cs, i - j) for j in range(n)] for i in range(n)]


def convention_check(candidate, true_symbol):
    step = F(candidate["step"])
    ts = [-step, F(0), step]
    same = []
    conjugate_law = []
    b_negated = all(F(x) == -F(y) for x, y in zip(candidate["b"], true_symbol["b"]))
    db_negated = all(F(x) == -F(y) for x, y in zip(candidate["db"], true_symbol["db"]))
    for t in ts:
        sc = script_coeffs(candidate, t, False)
        tc = true_coeffs(true_symbol, t)
        same.append(sc == tc)
        k = kernel_from_coeffs(tc, 5)
        kc = [[conj(k[j][i]) for j in range(5)] for i in range(5)]
        conjugate_law.append(exact_event_masses_row(k) == exact_event_masses_row(kc))
    return {
        "script_b_is_negative_true_b": b_negated,
        "script_db_is_negative_true_db": db_negated,
        "script_coefficients_equal_true_coefficients_all_three_t": all(same),
        "whole_conjugate_law_invariance_checked_n5": all(conjugate_law),
        "noncritical_wording_note": "actual script coefficients equal the true symbol after negating b/db; conjugate-law invariance is true but not needed for this artifact",
    }


def margin_check(candidate, true_symbol):
    step = F(candidate["step"])
    tau = F(candidate["tau"])
    eps = F(candidate["uniform_margin"])
    ts = [-step, F(0), step]
    amp_sq_values = []
    for t in ts:
        for a, da, b, db in zip(true_symbol["a"], true_symbol["da"], true_symbol["b"], true_symbol["db"]):
            aa = F(a) + t * F(da)
            bb = F(b) + t * F(db)
            amp_sq_values.append(aa * aa + bb * bb)
    one_harmonic_bound = F(36, 625) * (1 + step * step)
    total_osc_sq_bound = 4 * one_harmonic_bound
    margin_sq = (F(1, 2) - eps) ** 2
    return {
        "tau_equals_step": tau == step,
        "step": str(step),
        "epsilon": str(eps),
        "all_harmonic_amplitudes_within_bound": all(x <= one_harmonic_bound for x in amp_sq_values),
        "one_harmonic_amplitude_square_bound": str(one_harmonic_bound),
        "total_oscillation_square_bound": str(total_osc_sq_bound),
        "margin_square": str(margin_sq),
        "epsilon_margin_certified": eps == F(1, 200) and total_osc_sq_bound < margin_sq,
    }


def recompute_boundary_case(candidate, case):
    t = F(case["t"])
    complement = bool(case["complement_symbol"])
    M = int(case["M"])
    cs = script_coeffs(candidate, t, complement)
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

    tail_zero = True
    checked_tail_rows = []
    for r in range(M + m, M + 6 * m + 1):
        row_zero = True
        for j in range(m):
            value = c_at(cs, -r - j - 1)
            for s in range(max(0, r - m), min(M, r + m + 1)):
                value = sub(value, mul(c_at(cs, s - r), xmat[s][j]))
            row_zero = row_zero and value == Z
        checked_tail_rows.append(r)
        tail_zero = tail_zero and row_zero

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

    return {
        "t": str(t),
        "complement_symbol": complement,
        "M": M,
        "residual_rows_checked": M + m,
        "tail_rows_sampled_after_record": [checked_tail_rows[0], checked_tail_rows[-1]],
        "tail_rows_zero_in_sample": tail_zero,
        "R_norm_bound": str(r_bound),
        "operator_error_upper_rational": str(delta),
        "corner_rational": [[encode(x) for x in row] for row in corner],
    }


def boundary_check(candidate, boundary):
    step = F(candidate["step"])
    expected = {(str(t), c) for t in (-step, F(0), step) for c in (False, True)}
    actual = {(case["t"], bool(case["complement_symbol"])) for case in boundary["cases"]}
    rows = []
    for case in boundary["cases"]:
        rec = recompute_boundary_case(candidate, case)
        rows.append(
            {
                "t": rec["t"],
                "complement_symbol": rec["complement_symbol"],
                "stable_residual_and_corner": rec["R_norm_bound"] == case["R_norm_bound"]
                and rec["operator_error_upper_rational"] == case["operator_error_upper_rational"]
                and rec["corner_rational"] == case["corner_rational"]
                and rec["residual_rows_checked"] == case["residual_rows_checked"],
                "tail_rows_zero_after_record": rec["tail_rows_zero_in_sample"],
                "delta": rec["operator_error_upper_rational"],
                "delta_float": float(F(rec["operator_error_upper_rational"])),
            }
        )
    return {
        "six_independent_cases_present": actual == expected and len(boundary["cases"]) == 6,
        "artifact_actual_cases": boundary.get("actual_cases"),
        "artifact_residual_complex_entries": boundary.get("actual_residual_complex_entries"),
        "expected_residual_complex_entries": 6 * (boundary["cases"][0]["M"] + len(candidate["a"])) * len(candidate["a"]),
        "all_delta_below_epsilon": all(F(case["operator_error_upper_rational"]) < F(candidate["uniform_margin"]) for case in boundary["cases"]),
        "cases": rows,
    }


def find_case(boundary, t, complement):
    for case in boundary["cases"]:
        if F(case["t"]) == t and bool(case["complement_symbol"]) == complement:
            return case
    raise KeyError((str(t), complement))


def conditional_error(candidate, delta):
    eps = F(candidate["uniform_margin"])
    return delta * (1 + ((1 + delta) / (eps - delta)) ** 2)


def apply_corner(kernel, candidate, boundary, t, complement):
    out = [[kernel[i][j] for j in range(len(kernel))] for i in range(len(kernel))]
    case = find_case(boundary, t, complement)
    m = len(candidate["a"])
    for i in range(m):
        for j in range(m):
            value = parse_pair(case["corner_rational"][i][j])
            if complement:
                value = sub((F(int(i == j)), F(0)), value)
            out[i][j] = value
    return out


def rate_case(rate, t):
    for case in rate["cases"]:
        if F(case["t"]) == t:
            return case
    raise KeyError(str(t))


def rate_check(candidate, boundary, rate):
    step = F(candidate["step"])
    n = int(rate["cases"][0]["past_length"])
    per_t = []
    det_count = 0
    for t in (-step, F(0), step):
        kernel = kernel_from_coeffs(script_coeffs(candidate, t, False), n + 1)
        raw = exact_event_masses_row(kernel)
        extreme_one = exact_event_masses_row(apply_corner(kernel, candidate, boundary, t, False))
        extreme_zero = exact_event_masses_row(apply_corner(kernel, candidate, boundary, t, True))
        det_count += 3 * (1 << (n + 1))
        stored = rate_case(rate, t)
        stored_errors = {bool(x["complement_symbol"]): F(x["conditional_error_bound"]) for x in stored["boundary_cases"]}
        errors_ok = True
        for comp in (False, True):
            delta = F(find_case(boundary, t, comp)["operator_error_upper_rational"])
            errors_ok = errors_ok and conditional_error(candidate, delta) == stored_errors[comp]
        min_lo = F(1)
        max_hi = F(0)
        width = F(0)
        for event in range(1 << n):
            idx1 = event + (1 << n)
            weight = raw[event] + raw[idx1]
            q = raw[idx1] / weight
            q1 = extreme_one[idx1] / (extreme_one[event] + extreme_one[idx1])
            q0 = extreme_zero[idx1] / (extreme_zero[event] + extreme_zero[idx1])
            lo = max(F(candidate["uniform_margin"]), q1 - stored_errors[False])
            hi = min(1 - F(candidate["uniform_margin"]), q0 + stored_errors[True])
            if not (lo <= q <= hi):
                raise ArithmeticError(f"conditional interval miss t={t} event={event}")
            min_lo = min(min_lo, lo)
            max_hi = max(max_hi, hi)
            width += weight * (hi - lo)
        per_t.append(
            {
                "t": str(t),
                "three_distributions_positive_normalized": True,
                "independent_event_determinants": 3 * (1 << (n + 1)),
                "conditional_error_formula_matches": errors_ok,
                "conditional_range_matches_artifact": [str(min_lo), str(max_hi)] == stored["conditional_range"],
                "weighted_width_contained": F(stored["weighted_extreme_width"]["lower"]) <= width <= F(stored["weighted_extreme_width"]["upper"]),
            }
        )

    minus = rate_case(rate, -step)
    center = rate_case(rate, F(0))
    plus = rate_case(rate, step)
    gap_lower = (F(minus["lower_bound_interval"]["lower"]) + F(plus["lower_bound_interval"]["lower"])) / 2 - F(center["upper_bound_interval"]["upper"])
    gap_upper = (F(minus["upper_bound_interval"]["upper"]) + F(plus["upper_bound_interval"]["upper"])) / 2 - F(center["lower_bound_interval"]["lower"])
    return {
        "n": n,
        "artifact_actual_determinants": rate["actual_determinants"],
        "independent_event_determinants": det_count,
        "per_t": per_t,
        "gap_lower_recomputed": str(gap_lower),
        "gap_upper_recomputed": str(gap_upper),
        "gap_matches_artifact": rate["gap_enclosure"]["lower"] == str(gap_lower) and rate["gap_enclosure"]["upper"] == str(gap_upper),
        "strict_negative_gate": gap_upper < 0,
        "classification": rate["classification"],
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--rate-dir", required=True)
    p.add_argument("--output", required=True)
    args = p.parse_args()
    started = time.perf_counter()
    rate_dir = Path(args.rate_dir)
    paths = {
        "candidate_true_symbol.json": rate_dir / "candidate_true_symbol.json",
        "candidate.json": rate_dir / "candidate.json",
        "c3_m1_variational_boundary.py": rate_dir / "scripts" / "c3_m1_variational_boundary.py",
        "c3_m1_rate_certificate.py": rate_dir / "scripts" / "c3_m1_rate_certificate.py",
        "c3_m1_audit.py": rate_dir / "scripts" / "c3_m1_audit.py",
        "c3_m1_boundary_M64.json": rate_dir / "artifacts" / "c3_m1_boundary_M64.json",
        "c3_m1_rate_n4.json": rate_dir / "artifacts" / "c3_m1_rate_n4.json",
        "c3_m1_audit_result.json": rate_dir / "artifacts" / "c3_m1_audit_result.json",
    }
    candidate = json.loads(paths["candidate.json"].read_text(encoding="utf-8"))
    true_symbol = json.loads(paths["candidate_true_symbol.json"].read_text(encoding="utf-8"))
    boundary = json.loads(paths["c3_m1_boundary_M64.json"].read_text(encoding="utf-8"))
    rate = json.loads(paths["c3_m1_rate_n4.json"].read_text(encoding="utf-8"))
    self_audit = json.loads(paths["c3_m1_audit_result.json"].read_text(encoding="utf-8"))

    result = {
        "status": "PENDING",
        "audit_kind": "non_author_bounded_independent_checks",
        "python": sys.version.replace("\n", " "),
        "platform": platform.platform(),
        "elapsed_seconds": None,
        "file_hashes": {name: sha256_file(path) for name, path in paths.items()},
        "author_self_audit_status_seen_but_not_used_as_verdict": self_audit.get("status"),
        "convention_check": convention_check(candidate, true_symbol),
        "margin_check": margin_check(candidate, true_symbol),
        "boundary_check": boundary_check(candidate, boundary),
        "rate_check": rate_check(candidate, boundary, rate),
        "coverage_note": "interval-log entropy endpoints are source-inspected and gate-checked from saved rational endpoints; they are not independently regenerated by this script",
    }
    ok = True
    ok = ok and result["convention_check"]["script_coefficients_equal_true_coefficients_all_three_t"]
    ok = ok and result["convention_check"]["whole_conjugate_law_invariance_checked_n5"]
    ok = ok and result["margin_check"]["tau_equals_step"]
    ok = ok and result["margin_check"]["epsilon_margin_certified"]
    ok = ok and result["boundary_check"]["six_independent_cases_present"]
    ok = ok and result["boundary_check"]["artifact_actual_cases"] == 6
    ok = ok and result["boundary_check"]["artifact_residual_complex_entries"] == result["boundary_check"]["expected_residual_complex_entries"] == 792
    ok = ok and result["boundary_check"]["all_delta_below_epsilon"]
    ok = ok and all(c["stable_residual_and_corner"] and c["tail_rows_zero_after_record"] for c in result["boundary_check"]["cases"])
    ok = ok and result["rate_check"]["artifact_actual_determinants"] == result["rate_check"]["independent_event_determinants"] == 288
    ok = ok and all(
        c["three_distributions_positive_normalized"]
        and c["conditional_error_formula_matches"]
        and c["conditional_range_matches_artifact"]
        and c["weighted_width_contained"]
        for c in result["rate_check"]["per_t"]
    )
    ok = ok and result["rate_check"]["gap_matches_artifact"]
    ok = ok and result["rate_check"]["strict_negative_gate"]
    result["status"] = "CORRECT_SCOPED" if ok else "CRITICAL_GAPS"
    result["elapsed_seconds"] = time.perf_counter() - started
    Path(args.output).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "elapsed_seconds": result["elapsed_seconds"]}, sort_keys=True))
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
