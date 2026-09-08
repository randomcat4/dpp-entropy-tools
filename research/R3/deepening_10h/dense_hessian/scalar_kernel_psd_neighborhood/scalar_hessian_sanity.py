#!/usr/bin/env python3
"""Exact rational sanity checks for the scalar-kernel Hessian formula.

The script works with K(t)=diag(x_i)+t D for n=2,3.  It computes exact-event
atoms by Möbius inversion from inclusion determinants, keeping determinant
polynomials with Fraction coefficients.  It then checks the identities used in
the proof:

  p'_S / p_S = sum_{i in S} d_i/x_i - sum_{i notin S} d_i/(1-x_i),
  sum_S p''_S = 0,
  sum_{S: i in S} p''_S = 0 for every i,
  sum_S (p'_S)^2/p_S = sum_i d_i^2/[x_i(1-x_i)].

The last two identities are what remove every p'' contribution from the entropy
Hessian at xI, including off-diagonal determinant acceleration.
"""

from __future__ import annotations

import itertools
import json
from fractions import Fraction
from pathlib import Path


def f(num: int, den: int = 1) -> Fraction:
    return Fraction(num, den)


def poly_add(a, b):
    n = max(len(a), len(b))
    out = [Fraction(0) for _ in range(n)]
    for i in range(n):
        out[i] = (a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)
    return trim(out)


def poly_scale(a, c):
    return trim([c * x for x in a])


def poly_mul(a, b):
    out = [Fraction(0) for _ in range(len(a) + len(b) - 1)]
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[i + j] += ai * bj
    return trim(out)


def trim(a):
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def permutation_sign(p):
    inv = 0
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            if p[i] > p[j]:
                inv += 1
    return -1 if inv % 2 else 1


def det_poly_for_subset(xs, D, subset_mask: int, n: int):
    idx = [i for i in range(n) if (subset_mask >> i) & 1]
    m = len(idx)
    if m == 0:
        return [Fraction(1)]
    total = [Fraction(0)]
    for perm in itertools.permutations(range(m)):
        term = [Fraction(permutation_sign(perm))]
        for row_local, col_local in enumerate(perm):
            i = idx[row_local]
            j = idx[col_local]
            a0 = xs[i] if i == j else Fraction(0)
            a1 = D[i][j]
            term = poly_mul(term, [a0, a1])
        total = poly_add(total, term)
    return trim(total)


def exact_atom_polys(xs, D):
    n = len(D)
    inc = [det_poly_for_subset(xs, D, mask, n) for mask in range(1 << n)]
    atoms = []
    full = (1 << n) - 1
    for S in range(1 << n):
        comp = full ^ S
        total = [Fraction(0)]
        T = comp
        while True:
            sign = Fraction(-1 if (T.bit_count() % 2) else 1)
            total = poly_add(total, poly_scale(inc[S | T], sign))
            if T == 0:
                break
            T = (T - 1) & comp
        atoms.append(trim(total))
    return atoms


def coeff(poly, degree):
    return poly[degree] if degree < len(poly) else Fraction(0)


def score(mask: int, xs, diag):
    n = len(diag)
    total = Fraction(0)
    for i, d in enumerate(diag):
        if (mask >> i) & 1:
            total += d / xs[i]
        else:
            total -= d / (1 - xs[i])
    return total


def fraction_str(q: Fraction) -> str:
    if q.denominator == 1:
        return str(q.numerator)
    return f"{q.numerator}/{q.denominator}"


def matrix_str(D):
    return [[fraction_str(x) for x in row] for row in D]


def run_case(name: str, xs, D):
    n = len(D)
    if isinstance(xs, Fraction):
        xs = [xs for _ in range(n)]
    atoms = exact_atom_polys(xs, D)
    diag = [D[i][i] for i in range(n)]
    p0 = []
    p1 = []
    p2 = []
    score_errors = []
    for mask, poly in enumerate(atoms):
        base = coeff(poly, 0)
        first = coeff(poly, 1)
        second_deriv = 2 * coeff(poly, 2)
        p0.append(base)
        p1.append(first)
        p2.append(second_deriv)
        score_errors.append(first - base * score(mask, xs, diag))

    fisher = sum((p1[i] * p1[i]) / p0[i] for i in range(1 << n))
    expected_fisher = sum((diag[i] * diag[i]) / (xs[i] * (1 - xs[i])) for i in range(n))
    sum_p2 = sum(p2)
    singleton_p2 = [
        sum(p2[mask] for mask in range(1 << n) if (mask >> i) & 1)
        for i in range(n)
    ]
    formula_h2 = -expected_fisher
    p2_nonzero_masks = [mask for mask, val in enumerate(p2) if val != 0]

    frob2 = sum(D[i][j] * D[i][j] for i in range(n) for j in range(n))
    diag2 = sum(d * d for d in diag)
    cone_bound_margin = n * diag2 - frob2

    return {
        "name": name,
        "n": n,
        "x": [fraction_str(x) for x in xs],
        "D": matrix_str(D),
        "score_identity_ok": all(e == 0 for e in score_errors),
        "score_errors": [fraction_str(e) for e in score_errors if e != 0],
        "sum_p2": fraction_str(sum_p2),
        "singleton_weighted_sum_p2": [fraction_str(z) for z in singleton_p2],
        "fisher": fraction_str(fisher),
        "expected_fisher": fraction_str(expected_fisher),
        "hessian_formula": fraction_str(formula_h2),
        "fisher_identity_ok": fisher == expected_fisher,
        "entropy_p2_term_vanishes": sum_p2 == 0 and all(z == 0 for z in singleton_p2),
        "p2_nonzero_masks": p2_nonzero_masks,
        "sum_diag_squared": fraction_str(diag2),
        "frobenius_squared": fraction_str(frob2),
        "n_sum_diag_squared_minus_frobenius_squared": fraction_str(cone_bound_margin),
    }


def main():
    cases = [
        (
            "n2_zero_diag_offdiag_flat",
            [f(2, 5), f(2, 5)],
            [
                [f(0), f(3, 7)],
                [f(3, 7), f(0)],
            ],
        ),
        (
            "n2_psd_mixed",
            [f(3, 8), f(3, 8)],
            [
                [f(1, 3), f(1, 5)],
                [f(1, 5), f(2, 7)],
            ],
        ),
        (
            "n2_heterogeneous_zero_diag_offdiag_flat",
            [f(2, 7), f(5, 8)],
            [
                [f(0), f(3, 7)],
                [f(3, 7), f(0)],
            ],
        ),
        (
            "n3_general_symmetric",
            [f(3, 7), f(3, 7), f(3, 7)],
            [
                [f(1, 4), f(2, 7), -f(1, 5)],
                [f(2, 7), -f(1, 6), f(1, 8)],
                [-f(1, 5), f(1, 8), f(1, 9)],
            ],
        ),
        (
            "n3_heterogeneous_general_symmetric",
            [f(2, 7), f(3, 5), f(5, 11)],
            [
                [f(1, 4), f(2, 7), -f(1, 5)],
                [f(2, 7), -f(1, 6), f(1, 8)],
                [-f(1, 5), f(1, 8), f(1, 9)],
            ],
        ),
        (
            "n3_psd_rational",
            [f(5, 11), f(5, 11), f(5, 11)],
            [
                [f(5, 13), f(1, 6), f(1, 10)],
                [f(1, 6), f(7, 18), f(1, 12)],
                [f(1, 10), f(1, 12), f(4, 15)],
            ],
        ),
        (
            "n3_heterogeneous_psd_rational",
            [f(1, 4), f(1, 2), f(4, 5)],
            [
                [f(5, 13), f(1, 6), f(1, 10)],
                [f(1, 6), f(7, 18), f(1, 12)],
                [f(1, 10), f(1, 12), f(4, 15)],
            ],
        ),
    ]
    results = [run_case(name, x, D) for name, x, D in cases]
    all_ok = all(
        r["score_identity_ok"]
        and r["fisher_identity_ok"]
        and r["entropy_p2_term_vanishes"]
        for r in results
    )
    payload = {
        "status": "PASS" if all_ok else "FAIL",
        "cases": results,
        "notes": [
            "p2_nonzero_masks in the zero-diagonal case show off-diagonal acceleration exists.",
            "The entropy p'' term vanishes because sum p'' and each singleton-inclusion weighted sum p'' are zero.",
        ],
    }
    out = Path(__file__).with_name("scalar_hessian_sanity_results.json")
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))
    raise SystemExit(0 if all_ok else 2)


if __name__ == "__main__":
    main()
