"""Strict rational verifier for real-symmetric DPP entropy chords.

Input is a JSON file with rational K, V, and t. The verifier checks
0 < K +- tV < I by Sylvester's criterion, rebuilds all exact DPP event
probabilities by Mobius inversion, and bounds the entropy midpoint gap with
rational logarithm intervals.
"""

from __future__ import annotations

import argparse
import json
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
from typing import Iterable


F = Fraction


def parse_fraction(x) -> Fraction:
    if isinstance(x, int):
        return F(x, 1)
    if isinstance(x, str):
        return F(x)
    if isinstance(x, list) and len(x) == 2:
        return F(int(x[0]), int(x[1]))
    if isinstance(x, float):
        raise TypeError("floats are not accepted; use strings or numerator/denominator pairs")
    raise TypeError(f"cannot parse rational value {x!r}")


def read_matrix(data: dict, key: str) -> list[list[Fraction]]:
    denom_key = f"{key}_denominator"
    numer_key = f"{key}_numerators"
    if denom_key in data and numer_key in data:
        denom = int(data[denom_key])
        return [[F(int(x), denom) for x in row] for row in data[numer_key]]
    if key in data:
        return [[parse_fraction(x) for x in row] for row in data[key]]
    raise KeyError(f"missing matrix {key}")


def check_square_symmetric(m: list[list[Fraction]], name: str) -> None:
    n = len(m)
    if n == 0 or any(len(row) != n for row in m):
        raise ValueError(f"{name} is not a nonempty square matrix")
    for i in range(n):
        for j in range(i + 1, n):
            if m[i][j] != m[j][i]:
                raise ValueError(f"{name} is not symmetric at {(i, j)}")


def mat_add(a, b, scale_b=F(1)):
    n = len(a)
    return [[a[i][j] + scale_b * b[i][j] for j in range(n)] for i in range(n)]


def identity_minus(a):
    n = len(a)
    return [[(F(1) if i == j else F(0)) - a[i][j] for j in range(n)] for i in range(n)]


def event_matrix(k, mask: int):
    n = len(k)
    out = [row[:] for row in k]
    for i in range(n):
        if not ((mask >> i) & 1):
            out[i][i] -= 1
    return out


def det_bareiss(a: list[list[Fraction]]) -> Fraction:
    n = len(a)
    if n == 0:
        return F(1)
    m = [row[:] for row in a]
    prev = F(1)
    sign = F(1)
    for k in range(n - 1):
        pivot = None
        for r in range(k, n):
            if m[r][k]:
                pivot = r
                break
        if pivot is None:
            return F(0)
        if pivot != k:
            m[k], m[pivot] = m[pivot], m[k]
            sign = -sign
        pivot_val = m[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                m[i][j] = (m[i][j] * pivot_val - m[i][k] * m[k][j]) / prev
        prev = pivot_val
        for i in range(k + 1, n):
            m[i][k] = F(0)
        for j in range(k + 1, n):
            m[k][j] = F(0)
    return sign * m[-1][-1]


def leading_principal_minors(a) -> list[Fraction]:
    return [det_bareiss([row[:r] for row in a[:r]]) for r in range(1, len(a) + 1)]


def event_probabilities(k) -> list[Fraction]:
    n = len(k)
    out = []
    for mask in range(1 << n):
        sign = -1 if (n - mask.bit_count()) % 2 else 1
        out.append(sign * det_bareiss(event_matrix(k, mask)))
    return out


def log2_interval(terms: int) -> tuple[Fraction, Fraction]:
    z = F(1, 3)
    z2 = z * z
    power = z
    total = F(0)
    for j in range(terms):
        total += F(2) * power / (2 * j + 1)
        power *= z2
    rem = F(2) * power / ((2 * terms + 1) * (1 - z2))
    return total, total + rem


def normalize_power_two(x: Fraction) -> tuple[int, Fraction]:
    if x <= 0:
        raise ValueError("log input must be positive")
    k = 0
    y = x
    while y >= 2:
        y /= 2
        k += 1
    while y < 1:
        y *= 2
        k -= 1
    return k, y


def log_interval(x: Fraction, terms: int, log2_cache: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
    k, y = normalize_power_two(x)
    z = (y - 1) / (y + 1)
    z2 = z * z
    power = z
    total = F(0)
    for j in range(terms):
        total += F(2) * power / (2 * j + 1)
        power *= z2
    rem = F(0) if z == 0 else F(2) * power / ((2 * terms + 1) * (1 - z2))
    lo_y, hi_y = total, total + rem
    lo2, hi2 = log2_cache
    if k >= 0:
        return k * lo2 + lo_y, k * hi2 + hi_y
    return k * hi2 + lo_y, k * lo2 + hi_y


def entropy_interval(probabilities: Iterable[Fraction], terms: int) -> tuple[Fraction, Fraction]:
    log2_cache = log2_interval(terms)
    lo = F(0)
    hi = F(0)
    for p in probabilities:
        if p <= 0:
            raise ValueError(f"nonpositive event probability {p}")
        llo, lhi = log_interval(p, terms, log2_cache)
        coeff = -p
        if coeff >= 0:
            lo += coeff * llo
            hi += coeff * lhi
        else:
            lo += coeff * lhi
            hi += coeff * llo
    return lo, hi


def frac(x: Fraction) -> str:
    return f"{x.numerator}/{x.denominator}"


def dec(x: Fraction, precision: int = 60) -> str:
    getcontext().prec = precision
    return str(Decimal(x.numerator) / Decimal(x.denominator))


def classify(feasible: bool, events_ok: bool, gap_lo: Fraction, gap_hi: Fraction) -> str:
    if not feasible:
        return "NOT_FEASIBLE"
    if not events_ok:
        return "EVENT_PROBABILITY_FAILURE"
    if gap_lo > 0:
        return "CERTIFIED_POSITIVE_GAP"
    if gap_hi < 0:
        return "CERTIFIED_NEGATIVE_GAP"
    return "GAP_UNCERTAIN"


def certify(data: dict, terms: int) -> dict:
    k0 = read_matrix(data, "K")
    v = read_matrix(data, "V")
    check_square_symmetric(k0, "K")
    check_square_symmetric(v, "V")
    if len(k0) != len(v):
        raise ValueError("K and V dimensions differ")
    t = parse_fraction(data.get("t", data.get("h")))
    if t <= 0:
        raise ValueError("t must be positive")

    km = mat_add(k0, v, -t)
    kp = mat_add(k0, v, t)
    matrices = {
        "K_minus": km,
        "I_minus_K_minus": identity_minus(km),
        "K0": k0,
        "I_minus_K0": identity_minus(k0),
        "K_plus": kp,
        "I_minus_K_plus": identity_minus(kp),
    }
    feasibility = {}
    for name, matrix in matrices.items():
        minors = leading_principal_minors(matrix)
        feasibility[name] = {
            "leading_principal_minors": [frac(x) for x in minors],
            "positive_definite": all(x > 0 for x in minors),
        }
    feasible = all(row["positive_definite"] for row in feasibility.values())

    p_minus = event_probabilities(km)
    p0 = event_probabilities(k0)
    p_plus = event_probabilities(kp)
    sums = {"minus": sum(p_minus), "center": sum(p0), "plus": sum(p_plus)}
    mins = {"minus": min(p_minus), "center": min(p0), "plus": min(p_plus)}
    events_ok = all(p > 0 for p in p_minus + p0 + p_plus) and all(x == 1 for x in sums.values())

    if not feasible or not events_ok:
        return {
            "status": classify(feasible, events_ok, F(0), F(0)),
            "n": len(k0),
            "terms": terms,
            "t": frac(t),
            "feasible": feasible,
            "events_positive_and_normalized": events_ok,
            "feasibility": feasibility,
            "probability_sums": {key: frac(value) for key, value in sums.items()},
            "minimum_probabilities": {key: frac(value) for key, value in mins.items()},
            "gap_interval": null_gap(),
            "gap_decimal_interval": null_gap(),
            "strict_positive_gap": False,
            "strict_negative_gap": False,
        }

    h_minus = entropy_interval(p_minus, terms)
    h0 = entropy_interval(p0, terms)
    h_plus = entropy_interval(p_plus, terms)
    gap_lo = (h_minus[0] + h_plus[0]) / 2 - h0[1]
    gap_hi = (h_minus[1] + h_plus[1]) / 2 - h0[0]

    return {
        "status": classify(feasible, events_ok, gap_lo, gap_hi),
        "n": len(k0),
        "terms": terms,
        "t": frac(t),
        "feasible": feasible,
        "events_positive_and_normalized": events_ok,
        "feasibility": feasibility,
        "probability_sums": {key: frac(value) for key, value in sums.items()},
        "minimum_probabilities": {key: frac(value) for key, value in mins.items()},
        "gap_interval": [frac(gap_lo), frac(gap_hi)],
        "gap_decimal_interval": [dec(gap_lo), dec(gap_hi)],
        "strict_positive_gap": gap_lo > 0,
        "strict_negative_gap": gap_hi < 0,
    }


def null_gap() -> list[None]:
    return [None, None]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--terms", type=int, default=120)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    data = json.loads(args.candidate.read_text(encoding="utf-8"))
    result = certify(data, args.terms)
    text = json.dumps(result, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text + "\n", encoding="utf-8", newline="\n")
    print(text)
    return 0 if result["status"].startswith("CERTIFIED_") or result["status"] == "GAP_UNCERTAIN" else 2


if __name__ == "__main__":
    raise SystemExit(main())
