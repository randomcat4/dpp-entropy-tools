"""Independent exact n=3 symbolic checks for uniform_flat_ridge.

This script intentionally avoids sympy.  It expands

    p_S(t) = 2^{-n} det(I + 2 t Z_S D)

as a polynomial with Fraction coefficients and checks:

* normalization of event polynomials,
* complement parity p_S(t)=p_{S^c}(-t),
* Hessian coefficient for a general symmetric direction,
* quartic coefficient for a different zero-diagonal direction.
"""

from __future__ import annotations

import itertools
import json
from fractions import Fraction as F
from pathlib import Path


Poly = list[F]


def trim(p: Poly) -> Poly:
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def add(a: Poly, b: Poly) -> Poly:
    n = max(len(a), len(b))
    return trim([(a[i] if i < len(a) else F(0)) + (b[i] if i < len(b) else F(0)) for i in range(n)])


def mul(a: Poly, b: Poly) -> Poly:
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return trim(out)


def scale(a: Poly, c: F) -> Poly:
    return trim([c * x for x in a])


def neg_t(a: Poly) -> Poly:
    return [(-x if i % 2 else x) for i, x in enumerate(a)]


def sign_perm(perm: tuple[int, ...]) -> int:
    inv = 0
    for i in range(len(perm)):
        for j in range(i + 1, len(perm)):
            inv += perm[i] > perm[j]
    return -1 if inv % 2 else 1


def det_poly(matrix: list[list[Poly]]) -> Poly:
    n = len(matrix)
    total = [F(0)]
    for perm in itertools.permutations(range(n)):
        term = [F(sign_perm(perm))]
        for i, j in enumerate(perm):
            term = mul(term, matrix[i][j])
        total = add(total, term)
    return total


def event_relative_polys(direction: list[list[F]]) -> list[Poly]:
    n = len(direction)
    out = []
    for mask in range(1 << n):
        z = [F(1) if (mask >> i) & 1 else F(-1) for i in range(n)]
        mat: list[list[Poly]] = []
        for i in range(n):
            row = []
            for j in range(n):
                if i == j:
                    row.append([F(1), 2 * z[i] * direction[i][j]])
                else:
                    row.append([F(0), 2 * z[i] * direction[i][j]])
            mat.append(row)
        out.append(det_poly(mat))
    return out


def coeff(p: Poly, k: int) -> F:
    return p[k] if k < len(p) else F(0)


def average(values: list[F]) -> F:
    return sum(values, F(0)) / len(values)


def fstr(x: F) -> str:
    return f"{x.numerator}/{x.denominator}"


def main() -> None:
    general = [
        [F(1, 5), F(1, 3), -F(2, 7)],
        [F(1, 3), -F(1, 4), F(1, 9)],
        [-F(2, 7), F(1, 9), F(1, 6)],
    ]
    zero_diag = [
        [F(0), F(1, 3), -F(2, 5)],
        [F(1, 3), F(0), F(1, 7)],
        [-F(2, 5), F(1, 7), F(0)],
    ]

    n = 3
    u = F(1, 1 << n)

    rel_general = event_relative_polys(general)
    sum_prob_general = [u * sum(coeff(p, k) for p in rel_general) for k in range(n + 1)]
    c1 = [coeff(p, 1) for p in rel_general]
    h_t2 = -F(1, 2) * average([x * x for x in c1])
    expected_h_t2 = -2 * sum(general[i][i] ** 2 for i in range(n))
    expected_hessian = -4 * sum(general[i][i] ** 2 for i in range(n))

    rel_zero = event_relative_polys(zero_diag)
    sum_prob_zero = [u * sum(coeff(p, k) for p in rel_zero) for k in range(n + 1)]
    c2 = [coeff(p, 2) for p in rel_zero]
    h_t4 = -F(1, 2) * average([x * x for x in c2])
    off4 = sum(zero_diag[i][j] ** 4 for i in range(n) for j in range(i + 1, n))
    expected_h_t4 = -8 * off4
    expected_radial_second_t2 = -96 * off4

    complement_ok = True
    for mask, p in enumerate(rel_zero):
        comp = ((1 << n) - 1) ^ mask
        if trim(p[:]) != trim(neg_t(rel_zero[comp])[:]):
            complement_ok = False
            break

    checks = {
        "status": "PASS",
        "n": n,
        "normalization_general": [fstr(x) for x in sum_prob_general],
        "normalization_zero_diag": [fstr(x) for x in sum_prob_zero],
        "general_direction_H_t2": fstr(h_t2),
        "expected_general_H_t2": fstr(expected_h_t2),
        "general_hessian": fstr(2 * h_t2),
        "expected_general_hessian": fstr(expected_hessian),
        "zero_diag_H_t4": fstr(h_t4),
        "expected_zero_diag_H_t4": fstr(expected_h_t4),
        "zero_diag_radial_second_t2": fstr(12 * h_t4),
        "expected_zero_diag_radial_second_t2": fstr(expected_radial_second_t2),
        "complement_parity_zero_diag": complement_ok,
    }
    assert sum_prob_general == [F(1), F(0), F(0), F(0)]
    assert sum_prob_zero == [F(1), F(0), F(0), F(0)]
    assert h_t2 == expected_h_t2
    assert 2 * h_t2 == expected_hessian
    assert h_t4 == expected_h_t4
    assert 12 * h_t4 == expected_radial_second_t2
    assert complement_ok

    out = Path(__file__).with_name("fresh_symbolic_check.json")
    out.write_text(json.dumps(checks, indent=2), encoding="utf-8")
    print(json.dumps(checks, indent=2))


if __name__ == "__main__":
    main()
