#!/usr/bin/env python3
"""Exact rational sanity checks for D10-U2.

The script constructs exact DPP event atoms from inclusion probabilities by
Möbius inversion for K(t)=diag(x)+tD.  All arithmetic is Fraction-based and no
author verification code is imported.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations
from math import factorial
import json
from pathlib import Path


def f(num: int, den: int = 1) -> Fraction:
    return Fraction(num, den)


def trim(poly: list[Fraction]) -> list[Fraction]:
    out = list(poly)
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def poly_add(a: list[Fraction], b: list[Fraction]) -> list[Fraction]:
    m = max(len(a), len(b))
    out = [Fraction(0) for _ in range(m)]
    for i, v in enumerate(a):
        out[i] += v
    for i, v in enumerate(b):
        out[i] += v
    return trim(out)


def poly_mul(a: list[Fraction], b: list[Fraction]) -> list[Fraction]:
    out = [Fraction(0) for _ in range(len(a) + len(b) - 1)]
    for i, av in enumerate(a):
        for j, bv in enumerate(b):
            out[i + j] += av * bv
    return trim(out)


def perm_sign(perm: tuple[int, ...]) -> int:
    inv = 0
    for i in range(len(perm)):
        for j in range(i + 1, len(perm)):
            inv += int(perm[i] > perm[j])
    return -1 if inv % 2 else 1


def det_poly_principal(x: list[Fraction], D: list[list[Fraction]], mask: int) -> list[Fraction]:
    idx = [i for i in range(len(x)) if mask & (1 << i)]
    if not idx:
        return [Fraction(1)]
    total = [Fraction(0)]
    for perm in permutations(range(len(idx))):
        term = [Fraction(perm_sign(perm))]
        for row, col_pos in enumerate(perm):
            i = idx[row]
            j = idx[col_pos]
            entry = [x[i], D[i][i]] if i == j else [Fraction(0), D[i][j]]
            term = poly_mul(term, entry)
        total = poly_add(total, term)
    return total


def atom_polynomials(x: list[Fraction], D: list[list[Fraction]]) -> dict[int, list[Fraction]]:
    n = len(x)
    dets = {mask: det_poly_principal(x, D, mask) for mask in range(1 << n)}
    atoms: dict[int, list[Fraction]] = {}
    full = (1 << n) - 1
    for S in range(1 << n):
        rest = full ^ S
        sub = rest
        poly = [Fraction(0)]
        while True:
            A = S | sub
            signed = dets[A] if (A.bit_count() - S.bit_count()) % 2 == 0 else [-c for c in dets[A]]
            poly = poly_add(poly, signed)
            if sub == 0:
                break
            sub = (sub - 1) & rest
        atoms[S] = poly
    return atoms


def coeff(poly: list[Fraction], k: int) -> Fraction:
    return poly[k] if k < len(poly) else Fraction(0)


def deriv(poly: list[Fraction], order: int) -> Fraction:
    return Fraction(factorial(order)) * coeff(poly, order)


def frac_str(q: Fraction) -> str:
    return f"{q.numerator}/{q.denominator}" if q.denominator != 1 else str(q.numerator)


def serialize(obj):
    if isinstance(obj, Fraction):
        return frac_str(obj)
    if isinstance(obj, list):
        return [serialize(v) for v in obj]
    if isinstance(obj, tuple):
        return [serialize(v) for v in obj]
    if isinstance(obj, dict):
        return {str(k): serialize(v) for k, v in obj.items()}
    return obj


def product_atom(x: list[Fraction], mask: int) -> Fraction:
    out = Fraction(1)
    for i, xi in enumerate(x):
        out *= xi if mask & (1 << i) else 1 - xi
    return out


def pair_masks(n: int):
    for i in range(n):
        for j in range(i + 1, n):
            yield i, j


def check_case(name: str, x: list[Fraction], D: list[list[Fraction]]) -> dict:
    n = len(x)
    atoms = atom_polynomials(x, D)
    p = {
        order: {S: deriv(poly, order) for S, poly in atoms.items()}
        for order in range(5)
    }

    p0_errors = {
        S: p[0][S] - product_atom(x, S)
        for S in range(1 << n)
        if p[0][S] != product_atom(x, S)
    }
    p1_nonzero = {S: p[1][S] for S in range(1 << n) if p[1][S] != 0}

    mass_derivatives = {
        order: sum((p[order][S] for S in range(1 << n)), Fraction(0))
        for order in range(1, 5)
    }
    singleton_derivatives = {
        order: [
            sum((p[order][S] for S in range(1 << n) if S & (1 << i)), Fraction(0))
            for i in range(n)
        ]
        for order in range(1, 5)
    }

    pair_second_derivatives = {}
    pair_second_errors = {}
    for i, j in pair_masks(n):
        lhs = sum((p[2][S] for S in range(1 << n) if (S & (1 << i)) and (S & (1 << j))), Fraction(0))
        rhs = -2 * D[i][j] * D[i][j]
        pair_second_derivatives[(i, j)] = lhs
        if lhs != rhs:
            pair_second_errors[(i, j)] = lhs - rhs

    q_over_p_errors = {}
    for S in range(1 << n):
        expected = Fraction(0)
        for i, j in pair_masks(n):
            zeta_i = Fraction(1, x[i]) if S & (1 << i) else -Fraction(1, 1 - x[i])
            zeta_j = Fraction(1, x[j]) if S & (1 << j) else -Fraction(1, 1 - x[j])
            expected += D[i][j] * D[i][j] * zeta_i * zeta_j
        expected *= -2
        if p[2][S] != p[0][S] * expected:
            q_over_p_errors[S] = p[2][S] - p[0][S] * expected

    fisher4_sum = sum((p[2][S] * p[2][S] / p[0][S] for S in range(1 << n)), Fraction(0))
    explicit_fisher4_sum = 4 * sum(
        (
            D[i][j] ** 4
            / (x[i] * (1 - x[i]) * x[j] * (1 - x[j]))
            for i, j in pair_masks(n)
        ),
        Fraction(0),
    )
    H4 = -3 * fisher4_sum
    explicit_H4 = -3 * explicit_fisher4_sum
    t4_coeff = H4 / 24

    frob_square = sum((D[i][j] * D[i][j] for i in range(n) for j in range(n)), Fraction(0))
    a = min(x)
    b = max(x)
    M_candidates = [a * (1 - a), b * (1 - b)]
    if a <= Fraction(1, 2) <= b:
        M_candidates.append(Fraction(1, 4))
    M = max(M_candidates)
    if n >= 2:
        uniform_H4_bound_rhs = -6 * frob_square * frob_square / (n * (n - 1) * M * M)
        uniform_bound_margin = H4 - uniform_H4_bound_rhs
    else:
        uniform_H4_bound_rhs = None
        uniform_bound_margin = None

    nonzero_p2_atoms = [S for S in range(1 << n) if p[2][S] != 0]
    nonzero_D_pairs = [(i, j) for i, j in pair_masks(n) if D[i][j] != 0]

    all_half = all(xi == Fraction(1, 2) for xi in x)
    uniform_relation = None
    if all_half:
        sum_d4 = sum((D[i][j] ** 4 for i, j in pair_masks(n)), Fraction(0))
        uniform_relation = {
            "sum_dij_fourth": sum_d4,
            "expected_H4_old_U1": -192 * sum_d4,
            "expected_t4_coefficient_old_U1": -8 * sum_d4,
            "H4_matches_old_U1": H4 == -192 * sum_d4,
            "t4_matches_old_U1": t4_coeff == -8 * sum_d4,
        }

    ok = True
    ok = ok and not p0_errors
    ok = ok and not p1_nonzero
    ok = ok and all(v == 0 for v in mass_derivatives.values())
    ok = ok and all(all(v == 0 for v in vals) for vals in singleton_derivatives.values())
    ok = ok and not pair_second_errors
    ok = ok and not q_over_p_errors
    ok = ok and bool(nonzero_D_pairs) and bool(nonzero_p2_atoms)
    ok = ok and fisher4_sum == explicit_fisher4_sum and H4 == explicit_H4
    ok = ok and H4 < 0 and t4_coeff < 0
    ok = ok and uniform_bound_margin is not None and uniform_bound_margin <= 0
    if uniform_relation is not None:
        ok = ok and uniform_relation["H4_matches_old_U1"] and uniform_relation["t4_matches_old_U1"]

    return {
        "name": name,
        "n": n,
        "x": x,
        "p0_product_errors": p0_errors,
        "p1_nonzero_atoms": p1_nonzero,
        "mass_derivatives_1_to_4": mass_derivatives,
        "singleton_derivatives_1_to_4": singleton_derivatives,
        "pair_second_derivatives": pair_second_derivatives,
        "pair_second_errors": pair_second_errors,
        "q_over_p_explicit_formula_errors": q_over_p_errors,
        "nonzero_D_pairs": nonzero_D_pairs,
        "nonzero_p2_atom_count": len(nonzero_p2_atoms),
        "sum_p2_squared_over_p0": fisher4_sum,
        "explicit_sum_p2_squared_over_p0": explicit_fisher4_sum,
        "H4": H4,
        "explicit_H4_edge_sum": explicit_H4,
        "t4_coefficient": t4_coeff,
        "frob_square": frob_square,
        "box_M_max_x1mx": M,
        "uniform_H4_bound_rhs": uniform_H4_bound_rhs,
        "H4_minus_bound_rhs": uniform_bound_margin,
        "uniform_relation": uniform_relation,
        "status": "PASS" if ok else "FAIL",
    }


def main() -> int:
    cases = [
        (
            "n2_heterogeneous_zero_diag",
            [f(1, 3), f(3, 5)],
            [
                [f(0), f(1, 7)],
                [f(1, 7), f(0)],
            ],
        ),
        (
            "n3_heterogeneous_zero_diag",
            [f(1, 4), f(2, 5), f(7, 10)],
            [
                [f(0), f(1, 5), -f(1, 7)],
                [f(1, 5), f(0), f(1, 6)],
                [-f(1, 7), f(1, 6), f(0)],
            ],
        ),
        (
            "n4_heterogeneous_zero_diag",
            [f(1, 5), f(2, 5), f(3, 5), f(4, 5)],
            [
                [f(0), f(1, 5), -f(1, 7), f(1, 11)],
                [f(1, 5), f(0), f(1, 6), -f(1, 13)],
                [-f(1, 7), f(1, 6), f(0), f(1, 9)],
                [f(1, 11), -f(1, 13), f(1, 9), f(0)],
            ],
        ),
        (
            "n3_uniform_old_U1_relation",
            [f(1, 2), f(1, 2), f(1, 2)],
            [
                [f(0), f(1, 3), -f(2, 5)],
                [f(1, 3), f(0), f(1, 7)],
                [-f(2, 5), f(1, 7), f(0)],
            ],
        ),
    ]
    results = [check_case(*case) for case in cases]
    status = "PASS" if all(r["status"] == "PASS" for r in results) else "FAIL"
    payload = {
        "status": status,
        "method": "exact-event Mobius atoms from inclusion determinants; standard-library Fraction arithmetic",
        "checks": [
            "p0 is heterogeneous product Bernoulli",
            "all pS'(0) vanish for zero-diagonal D",
            "mass and singleton derivatives of orders 1..4 vanish",
            "pair inclusion second derivative equals -2*dij^2",
            "pS''(0)/pS(0) equals -2*sum_edges dij^2*zeta_i*zeta_j",
            "H''=H'''=0 by logged linear-term cancellation",
            "H''''=-12*sum_edges dij^4/[xi(1-xi)xj(1-xj)]<0",
            "explicit compact-box fourth-order bound is satisfied",
            "uniform x_i=1/2 case reduces to old U1 coefficient",
        ],
        "cases": results,
    }
    out = Path(__file__).with_name("flat_ridge_sanity_results.json")
    out.write_text(json.dumps(serialize(payload), indent=2), encoding="utf-8")
    print(json.dumps(serialize({
        "status": status,
        "json": str(out),
        "case_statuses": {r["name"]: r["status"] for r in results},
    }), indent=2))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
