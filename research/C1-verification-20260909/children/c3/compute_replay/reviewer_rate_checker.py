#!/usr/bin/env python3
"""Reviewer-side fixed C3-M1 replay checker.

This script is deliberately narrow: it compares substantive replay fields to
the frozen public artifacts and independently recomputes the small exact event
probabilities by a permutation determinant routine.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
from fractions import Fraction as F
from pathlib import Path


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

Z = (F(0), F(0))


def pair(x):
    return (F(x[0]), F(x[1]))


def enc(z):
    return [str(z[0]), str(z[1])]


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def neg(a):
    return (-a[0], -a[1])


def sub(a, b):
    return add(a, neg(b))


def mul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def conj(a):
    return (a[0], -a[1])


def sign_perm(p):
    inv = 0
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            inv += p[i] > p[j]
    return -1 if inv % 2 else 1


def det_perm(mat):
    n = len(mat)
    total = Z
    for p in itertools.permutations(range(n)):
        term = (F(sign_perm(p)), F(0))
        for i, j in enumerate(p):
            term = mul(term, mat[i][j])
            if term == Z:
                break
        total = add(total, term)
    return total


def exact_event_masses(kernel):
    n = len(kernel)
    masses = []
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
            raise ArithmeticError(f"non-real determinant for event {event}")
        if d[0] <= 0:
            raise ArithmeticError(f"non-positive event mass for event {event}: {d[0]}")
        masses.append(d[0])
    if sum(masses) != 1:
        raise ArithmeticError("event masses do not normalize")
    return masses


def coeffs_script(candidate, t, complement=False):
    p = F(candidate["p"]) + t * F(candidate["dp"])
    a = [F(x) + t * F(dx) for x, dx in zip(candidate["a"], candidate["da"])]
    b = [F(x) + t * F(dx) for x, dx in zip(candidate["b"], candidate["db"])]
    cs = [(p, F(0))] + [(aa / 2, -bb / 2) for aa, bb in zip(a, b)]
    if complement:
        cs = [(1 - p, F(0))] + [neg(c) for c in cs[1:]]
    return cs


def coeffs_true(true_symbol, t):
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


def symbol_kernel(candidate, t, n):
    cs = coeffs_script(candidate, t, False)
    return [[c_at(cs, i - j) for j in range(n)] for i in range(n)]


def apply_boundary_corner(kernel, candidate, boundary, t, complement):
    case = find_boundary_case(boundary, t, complement)
    m = len(candidate["a"])
    out = [[kernel[i][j] for j in range(len(kernel))] for i in range(len(kernel))]
    for i in range(m):
        for j in range(m):
            value = pair(case["corner_rational"][i][j])
            if complement:
                value = sub((F(int(i == j)), F(0)), value)
            out[i][j] = value
    return out


def find_boundary_case(boundary, t, complement):
    for case in boundary["cases"]:
        if F(case["t"]) == t and bool(case["complement_symbol"]) == complement:
            return case
    raise KeyError((str(t), complement))


def rate_case(rate, t):
    for case in rate["cases"]:
        if F(case["t"]) == t:
            return case
    raise KeyError(str(t))


def stable_boundary(case):
    keys = [
        "t",
        "complement_symbol",
        "M",
        "dyadic_bits",
        "epsilon",
        "R_norm_bound",
        "operator_error_upper_rational",
        "enclosure_method",
        "corner_rational",
        "solution_dyadic",
        "residual_rows_checked",
    ]
    return {k: case[k] for k in keys}


def stable_rate_case(case):
    keys = [
        "t",
        "past_length",
        "lower_bound_interval",
        "upper_bound_interval",
        "weighted_extreme_width",
        "boundary_cases",
        "exact_determinants",
        "normalization",
        "conditional_range",
    ]
    return {k: case[k] for k in keys}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--original-rate-dir", required=True)
    ap.add_argument("--replay-rate-dir", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    orig = Path(args.original_rate_dir)
    replay = Path(args.replay_rate_dir)
    candidate = load(replay / "candidate.json")
    true_symbol = load(replay / "candidate_true_symbol.json")
    boundary0 = load(orig / "artifacts" / "c3_m1_boundary_M64.json")
    rate0 = load(orig / "artifacts" / "c3_m1_rate_n4.json")
    audit0 = load(orig / "artifacts" / "c3_m1_audit_result.json")
    boundary1 = load(replay / "artifacts" / "c3_m1_boundary_M64.replay.json")
    rate1 = load(replay / "artifacts" / "c3_m1_rate_n4.replay.json")
    audit1 = load(replay / "artifacts" / "c3_m1_audit_result.replay.json")

    step = F(candidate["step"])
    eps = F(candidate["uniform_margin"])
    ts = [-step, F(0), step]
    coeff_equal = {
        str(t): [enc(z) for z in coeffs_script(candidate, t, False)]
        == [enc(z) for z in coeffs_true(true_symbol, t)]
        for t in ts
    }
    note_mentions_conjugate = "conjugate" in candidate.get("conjugation_note", "").lower()

    expected_boundary = {(str(t), c) for t in ts for c in (False, True)}
    actual_boundary = {(case["t"], bool(case["complement_symbol"])) for case in boundary1["cases"]}
    boundary_stable = sorted((stable_boundary(c) for c in boundary0["cases"]), key=lambda x: (x["t"], x["complement_symbol"])) == sorted(
        (stable_boundary(c) for c in boundary1["cases"]), key=lambda x: (x["t"], x["complement_symbol"])
    )

    rate_stable = sorted((stable_rate_case(c) for c in rate0["cases"]), key=lambda x: x["t"]) == sorted(
        (stable_rate_case(c) for c in rate1["cases"]), key=lambda x: x["t"]
    )
    gap_stable = rate0["gap_enclosure"] == rate1["gap_enclosure"] and rate0["classification"] == rate1["classification"]

    per_symbol = []
    determinant_count = 0
    for t in ts:
        n = int(rate_case(rate1, t)["past_length"])
        raw = exact_event_masses(symbol_kernel(candidate, t, n + 1))
        one = exact_event_masses(apply_boundary_corner(symbol_kernel(candidate, t, n + 1), candidate, boundary1, t, False))
        zero = exact_event_masses(apply_boundary_corner(symbol_kernel(candidate, t, n + 1), candidate, boundary1, t, True))
        determinant_count += 3 * (1 << (n + 1))
        rc = rate_case(rate1, t)
        errors = {bool(x["complement_symbol"]): F(x["conditional_error_bound"]) for x in rc["boundary_cases"]}
        min_lo = F(1)
        max_hi = F(0)
        width = F(0)
        for event in range(1 << n):
            idx1 = event + (1 << n)
            weight = raw[event] + raw[idx1]
            q = raw[idx1] / weight
            q1 = one[idx1] / (one[event] + one[idx1])
            q0 = zero[idx1] / (zero[event] + zero[idx1])
            lo = max(eps, q1 - errors[False])
            hi = min(1 - eps, q0 + errors[True])
            if lo > hi:
                raise ArithmeticError(f"empty conditional interval t={t} event={event}")
            if not lo <= q <= hi:
                raise ArithmeticError(f"finite conditional outside interval t={t} event={event}")
            min_lo = min(min_lo, lo)
            max_hi = max(max_hi, hi)
            width += weight * (hi - lo)
        wlo = F(rc["weighted_extreme_width"]["lower"])
        whi = F(rc["weighted_extreme_width"]["upper"])
        per_symbol.append(
            {
                "t": str(t),
                "past_length": n,
                "permutation_event_distributions": 3,
                "permutation_event_determinants": 3 * (1 << (n + 1)),
                "conditional_range_recomputed": [str(min_lo), str(max_hi)],
                "conditional_range_matches": [str(min_lo), str(max_hi)] == rc["conditional_range"],
                "weighted_width_recomputed": str(width),
                "weighted_width_inside_artifact_interval": wlo <= width <= whi,
            }
        )

    minus = rate_case(rate1, -step)
    center = rate_case(rate1, F(0))
    plus = rate_case(rate1, step)
    gap_lower = (F(minus["lower_bound_interval"]["lower"]) + F(plus["lower_bound_interval"]["lower"])) / 2 - F(center["upper_bound_interval"]["upper"])
    gap_upper = (F(minus["upper_bound_interval"]["upper"]) + F(plus["upper_bound_interval"]["upper"])) / 2 - F(center["lower_bound_interval"]["lower"])

    result = {
        "status": "REVIEWER_CHECK_PASS",
        "input_hashes": {
            "candidate": sha(replay / "candidate.json"),
            "candidate_true_symbol": sha(replay / "candidate_true_symbol.json"),
            "original_boundary": sha(orig / "artifacts" / "c3_m1_boundary_M64.json"),
            "original_rate": sha(orig / "artifacts" / "c3_m1_rate_n4.json"),
            "original_audit": sha(orig / "artifacts" / "c3_m1_audit_result.json"),
            "replay_boundary": sha(replay / "artifacts" / "c3_m1_boundary_M64.replay.json"),
            "replay_rate": sha(replay / "artifacts" / "c3_m1_rate_n4.replay.json"),
            "replay_audit": sha(replay / "artifacts" / "c3_m1_audit_result.replay.json"),
        },
        "convention_check": {
            "script_coefficients_equal_true_coefficients": coeff_equal,
            "candidate_note_mentions_conjugate": note_mentions_conjugate,
            "candidate_note_is_mathematically_imprecise": note_mentions_conjugate and all(coeff_equal.values()),
        },
        "boundary_check": {
            "expected_six_cases": actual_boundary == expected_boundary and boundary1.get("actual_cases") == 6,
            "stable_boundary_fields_match_original": boundary_stable,
            "all_delta_below_margin": all(F(c["operator_error_upper_rational"]) < eps for c in boundary1["cases"]),
            "residual_rows": sorted({c["residual_rows_checked"] for c in boundary1["cases"]}),
            "worst_delta": str(max(F(c["operator_error_upper_rational"]) for c in boundary1["cases"])),
        },
        "rate_check": {
            "stable_rate_fields_match_original": rate_stable,
            "gap_stable": gap_stable,
            "classification": rate1["classification"],
            "permutation_determinants": determinant_count,
            "artifact_determinants": rate1["actual_determinants"],
            "per_symbol": per_symbol,
            "gap_lower_recomputed": str(gap_lower),
            "gap_upper_recomputed": str(gap_upper),
            "strict_negative_upper": gap_upper < 0,
        },
        "audit_replay_check": {
            "original_status": audit0["status"],
            "replay_status": audit1["status"],
            "stable_margin": audit0["margin_check"] == audit1["margin_check"],
            "stable_boundary_summary": audit0["boundary_checks"] == audit1["boundary_checks"],
            "stable_rate_summary": audit0["rate_checks"] == audit1["rate_checks"],
        },
    }

    ok = True
    ok = ok and all(coeff_equal.values())
    ok = ok and result["boundary_check"]["expected_six_cases"]
    ok = ok and result["boundary_check"]["stable_boundary_fields_match_original"]
    ok = ok and result["boundary_check"]["all_delta_below_margin"]
    ok = ok and result["rate_check"]["stable_rate_fields_match_original"]
    ok = ok and result["rate_check"]["gap_stable"]
    ok = ok and result["rate_check"]["classification"] == "NEGATIVE_PAIR_GAP"
    ok = ok and result["rate_check"]["permutation_determinants"] == result["rate_check"]["artifact_determinants"] == 288
    ok = ok and all(x["conditional_range_matches"] and x["weighted_width_inside_artifact_interval"] for x in per_symbol)
    ok = ok and result["rate_check"]["strict_negative_upper"]
    ok = ok and result["audit_replay_check"]["replay_status"] == "CORRECT_SELF_AUDIT"
    ok = ok and result["audit_replay_check"]["stable_margin"]
    ok = ok and result["audit_replay_check"]["stable_boundary_summary"]
    ok = ok and result["audit_replay_check"]["stable_rate_summary"]
    result["status"] = "REVIEWER_CHECK_PASS" if ok else "REVIEWER_CHECK_FAIL"
    Path(args.output).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "strict_negative_upper": result["rate_check"]["strict_negative_upper"]}, indent=2))
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
