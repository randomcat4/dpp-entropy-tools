#!/usr/bin/env python3
"""Low-cost independent review of the n=8 negative rate certificate.

This script does not import the author's certificate code.  It rebuilds the
finite exact-event masses with a direct exact-event matrix, checks the rational
gap and q-error algebra in the JSON artifacts, and recomputes the displayed
entropy bounds numerically with Python Decimal logs.  The Decimal portion is a
sanity check; the rigorous outward log intervals remain the author's artifact.
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
from decimal import Decimal, getcontext
from fractions import Fraction as F
from pathlib import Path

Z = (0, 0)


def z_add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def z_sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def z_mul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def z_conj(a):
    return (a[0], -a[1])


def z_div_exact(a, b):
    d = b[0] * b[0] + b[1] * b[1]
    if d == 0:
        raise ZeroDivisionError("zero Gaussian denominator")
    re = a[0] * b[0] + a[1] * b[1]
    im = a[1] * b[0] - a[0] * b[1]
    if re % d or im % d:
        raise ArithmeticError("non-exact Gaussian Bareiss division")
    return (re // d, im // d)


def f_add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def f_sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def f_conj(a):
    return (a[0], -a[1])


def decode_pair(x):
    return (F(x[0]), F(x[1]))


def coeffs(candidate, t):
    return [(F(candidate["p"]), F(0))] + [
        (F(a) / 2, -t * F(b) / 2) for a, b in zip(candidate["a"], candidate["b"])
    ]


def coeff(cs, lag):
    m = len(cs) - 1
    if 0 <= lag <= m:
        return cs[lag]
    if -m <= lag < 0:
        return f_conj(cs[-lag])
    return (F(0), F(0))


def common_denominator(K):
    d = 1
    for row in K:
        for z in row:
            d = math.lcm(d, z[0].denominator, z[1].denominator)
    return d


def det_bareiss_gaussian(A):
    n = len(A)
    M = [[x for x in row] for row in A]
    previous = (1, 0)
    sign = 1
    for k in range(n - 1):
        if M[k][k] == Z:
            swap = next((r for r in range(k + 1, n) if M[r][k] != Z), None)
            if swap is None:
                return Z
            M[k], M[swap] = M[swap], M[k]
            sign *= -1
        pivot = M[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                M[i][j] = z_div_exact(
                    z_sub(z_mul(M[i][j], pivot), z_mul(M[i][k], M[k][j])),
                    previous,
                )
        previous = pivot
    det = M[-1][-1]
    return (sign * det[0], sign * det[1])


def event_masses_direct(K):
    n = len(K)
    denominator = common_denominator(K)
    scaled = [[(int(z[0] * denominator), int(z[1] * denominator)) for z in row] for row in K]
    masses = []
    for event in range(1 << n):
        M = []
        for i in range(n):
            row = []
            is_one = ((event >> i) & 1) == 1
            for j in range(n):
                value = scaled[i][j]
                if not is_one:
                    value = z_sub((denominator if i == j else 0, 0), value)
                row.append(value)
            M.append(row)
        det = det_bareiss_gaussian(M)
        if det[1] != 0:
            raise ArithmeticError(f"non-real exact event determinant at event {event}")
        prob = F(det[0], denominator**n)
        if prob <= 0:
            raise ArithmeticError(f"non-positive exact event probability at event {event}")
        masses.append(prob)
    if sum(masses) != 1:
        raise ArithmeticError("event masses do not sum exactly to one")
    return masses


def symbol_kernel(candidate, t, n):
    cs = coeffs(candidate, t)
    return [[coeff(cs, i - j) for j in range(n)] for i in range(n)]


def kernel_with_extreme_corner(candidate, boundary, t, n, complement_symbol):
    K = symbol_kernel(candidate, t, n)
    m = len(candidate["a"])
    case = next(
        c
        for c in boundary["cases"]
        if F(c["t"]) == t and bool(c["complement_symbol"]) == complement_symbol
    )
    for i in range(m):
        for j in range(m):
            value = decode_pair(case["corner_rational"][i][j])
            if complement_symbol:
                value = f_sub((F(1) if i == j else F(0), F(0)), value)
            K[i][j] = value
    return K


def d(frac):
    return Decimal(frac.numerator) / Decimal(frac.denominator)


def binary_decimal(frac):
    if frac == 0 or frac == 1:
        return Decimal(0)
    x = d(frac)
    return -x * x.ln() - (Decimal(1) - x) * (Decimal(1) - x).ln()


def recompute_case(candidate, boundary, rate_case):
    n = int(rate_case["past_length"])
    t = F(rate_case["t"])
    eps = F(candidate["uniform_margin"])
    raw = event_masses_direct(symbol_kernel(candidate, t, n + 1))
    one = event_masses_direct(kernel_with_extreme_corner(candidate, boundary, t, n + 1, False))
    zero = event_masses_direct(kernel_with_extreme_corner(candidate, boundary, t, n + 1, True))

    errors = []
    for complement in [False, True]:
        case = next(
            c
            for c in boundary["cases"]
            if F(c["t"]) == t and bool(c["complement_symbol"]) == complement
        )
        delta = F(case["operator_error_upper_rational"])
        errors.append(delta * (1 + ((1 + delta) / (eps - delta)) ** 2))
    if [str(e) for e in errors] != rate_case["conditional_error_bounds"]:
        raise AssertionError("conditional q-error bounds do not match delta formula")

    lower = Decimal(0)
    upper = Decimal(0)
    min_interval = F(1)
    max_interval = F(0)
    order_failures = 0
    for event in range(1 << n):
        idx1 = event + (1 << n)
        weight = raw[event] + raw[idx1]
        q = raw[idx1] / weight
        q1 = one[idx1] / (one[event] + one[idx1])
        q0 = zero[idx1] / (zero[event] + zero[idx1])
        lo = max(eps, q1 - errors[0])
        hi = min(1 - eps, q0 + errors[1])
        if not (lo <= q <= hi):
            order_failures += 1
        min_interval = min(min_interval, lo)
        max_interval = max(max_interval, hi)
        lower += d(weight) * min(binary_decimal(lo), binary_decimal(hi))
        upper += d(weight) * binary_decimal(q)

    return {
        "t": str(t),
        "past_length": n,
        "order_failures": order_failures,
        "normalization": "EXACT_FRACTION_EQUALITY",
        "determinants_recomputed": 3 * (1 << (n + 1)),
        "conditional_range": [str(min_interval), str(max_interval)],
        "lower_decimal": str(+lower),
        "upper_decimal": str(+upper),
    }


def frac_decimal_string(frac_str):
    return str(+d(F(frac_str)))


def sha256_file(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git_head():
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except Exception as exc:
        return f"UNAVAILABLE: {exc}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--boundary", type=Path, required=True)
    parser.add_argument("--rate", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    getcontext().prec = 90
    candidate = json.loads(args.candidate.read_text(encoding="utf-8"))
    boundary = json.loads(args.boundary.read_text(encoding="utf-8"))
    rate = json.loads(args.rate.read_text(encoding="utf-8"))
    cases = [recompute_case(candidate, boundary, c) for c in rate["cases"]]
    center = next(c for c in rate["cases"] if c["t"] == "0")
    endpoint = next(c for c in rate["cases"] if c["t"] != "0")
    gap_lower = F(endpoint["lower_bound_interval"]["lower"]) - F(center["upper_bound_interval"]["upper"])
    gap_upper = F(endpoint["upper_bound_interval"]["upper"]) - F(center["lower_bound_interval"]["lower"])
    if str(gap_lower) != rate["gap_enclosure"]["lower"]:
        raise AssertionError("gap lower does not match case interval subtraction")
    if str(gap_upper) != rate["gap_enclosure"]["upper"]:
        raise AssertionError("gap upper does not match case interval subtraction")
    status = "CORRECT" if gap_lower <= gap_upper < 0 and all(c["order_failures"] == 0 for c in cases) else "CRITICAL_GAPS"
    result = {
        "status": status,
        "exit_status": 0,
        "pid": os.getpid(),
        "command": " ".join([sys.executable, *sys.argv]),
        "python": sys.version,
        "platform": platform.platform(),
        "git_head": git_head(),
        "seed": "deterministic-no-random-seed-used",
        "source_sha256": sha256_file(Path(__file__).resolve()),
        "candidate_sha256": sha256_file(args.candidate),
        "boundary_sha256": sha256_file(args.boundary),
        "rate_sha256": sha256_file(args.rate),
        "cases": cases,
        "gap_enclosure_checked_exactly": {
            "lower": str(gap_lower),
            "upper": str(gap_upper),
            "lower_decimal": frac_decimal_string(str(gap_lower)),
            "upper_decimal": frac_decimal_string(str(gap_upper)),
        },
        "classification": "NEGATIVE_PAIR_GAP" if gap_upper < 0 else "INCONCLUSIVE",
        "coverage": {
            "exact_event_determinants": "3 * 2^(n+1) per t case, with n=8 and two t values",
            "q_error": "all two t cases and both extreme boundary symbols checked from rational delta",
            "gap": "exact rational interval subtraction checked against JSON",
        },
    }
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"status": status, "pid": os.getpid(), "exit": 0, "out": str(args.out)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
