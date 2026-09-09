#!/usr/bin/env python3
"""Exact polynomial verification of fisher_projection.md.

The script reconstructs all required inclusion determinants by the Leibniz
formula over at most four sites. Polynomial coefficients are Fractions in the
nearest-neighbor kernel entry u=t/16. No floating point or entropy computation
is used.
"""

from __future__ import annotations

import itertools
import json
from fractions import Fraction
from pathlib import Path

Poly = tuple[Fraction, ...]


def trim(p: Poly) -> Poly:
    values = list(p)
    while len(values) > 1 and values[-1] == 0:
        values.pop()
    return tuple(values)


def add(p: Poly, q: Poly) -> Poly:
    out = [Fraction(0)] * max(len(p), len(q))
    for i, value in enumerate(p):
        out[i] += value
    for i, value in enumerate(q):
        out[i] += value
    return trim(tuple(out))


def scale(p: Poly, a: Fraction) -> Poly:
    return trim(tuple(a * value for value in p))


def mul(p: Poly, q: Poly) -> Poly:
    out = [Fraction(0)] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            out[i + j] += x * y
    return trim(tuple(out))


def inversion_sign(permutation: tuple[int, ...]) -> int:
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(len(permutation))
        for j in range(i + 1, len(permutation))
    )
    return -1 if inversions & 1 else 1


def kernel_entry(i: int, j: int) -> Poly:
    distance = abs(i - j)
    if distance == 0:
        return (Fraction(1, 2),)
    if distance == 1:
        return (Fraction(0), Fraction(1))
    if distance == 2:
        return (Fraction(1, 8),)
    return (Fraction(0),)


def determinant(indices: tuple[int, ...]) -> Poly:
    n = len(indices)
    total: Poly = (Fraction(0),)
    for permutation in itertools.permutations(range(n)):
        term: Poly = (Fraction(inversion_sign(permutation)),)
        for row, column_position in enumerate(permutation):
            term = mul(term, kernel_entry(indices[row], indices[column_position]))
        total = add(total, term)
    return trim(total)


def sub(p: Poly, q: Poly) -> Poly:
    return add(p, scale(q, Fraction(-1)))


def square(p: Poly) -> Poly:
    return mul(p, p)


def evaluate(p: Poly, x: Fraction) -> Fraction:
    total = Fraction(0)
    for coefficient in reversed(p):
        total = total * x + coefficient
    return total


def as_strings(p: Poly) -> list[str]:
    return [str(value) for value in p]


def main() -> None:
    mean_pair = determinant((0, 1))
    assert mean_pair == (Fraction(1, 4), Fraction(0), Fraction(-1))

    c0 = sub(mean_pair, square(mean_pair))
    c1 = sub(determinant((0, 1, 2)), square(mean_pair))
    c2 = sub(determinant((0, 1, 2, 3)), square(mean_pair))
    c3 = sub(determinant((0, 1, 3, 4)), square(mean_pair))

    expected_c0 = (
        Fraction(3, 16),
        Fraction(0),
        Fraction(-1, 2),
        Fraction(0),
        Fraction(-1),
    )
    expected_c1 = (
        Fraction(7, 128),
        Fraction(0),
        Fraction(-1, 4),
        Fraction(0),
        Fraction(-1),
    )
    expected_c2 = (
        Fraction(-31, 4096),
        Fraction(0),
        Fraction(-1, 32),
    )
    expected_c3 = (Fraction(-1, 256),)
    assert c0 == expected_c0
    assert c1 == expected_c1
    assert c2 == expected_c2
    assert c3 == expected_c3

    variance_density = add(c0, scale(add(add(c1, c2), c3), Fraction(2)))
    assert variance_density == (
        Fraction(561, 2048),
        Fraction(0),
        Fraction(-17, 16),
        Fraction(0),
        Fraction(-3),
    )

    u_half = Fraction(1, 32)
    u_three_halves = Fraction(3, 32)
    v_half = evaluate(variance_density, u_half)
    v_three_halves = evaluate(variance_density, u_three_halves)
    assert v_half == Fraction(286141, 1048576)
    assert v_three_halves == Fraction(277197, 1048576)
    assert v_three_halves > 0

    fisher_at_half = Fraction(1, 4) / (16384 * v_half)
    assert fisher_at_half == Fraction(16, 286141)

    report = {
        "status": "PASS",
        "scope": "exact inclusion covariance and Fisher projection constants only",
        "variable": "u=t/16",
        "pair_mean_coefficients": as_strings(mean_pair),
        "covariance_coefficients": {
            "lag_0": as_strings(c0),
            "lag_1": as_strings(c1),
            "lag_2": as_strings(c2),
            "lag_3": as_strings(c3),
        },
        "variance_density_coefficients": as_strings(variance_density),
        "V_at_t_half": str(v_half),
        "V_at_t_three_halves": str(v_three_halves),
        "uniform_Fisher_lower_bound": str(fisher_at_half),
        "arithmetic": "Fraction polynomial Leibniz determinants",
    }

    target = Path(__file__).resolve().parents[1] / "output" / "pair_fisher_exact.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
