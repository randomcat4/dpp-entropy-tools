#!/usr/bin/env python3
"""Fresh non-author audit for D10-U2 diagonal_flat_ridge.

This script intentionally does not import the author sanity code.  It uses
standard-library Fraction arithmetic to rebuild exact-event atoms from
inclusion determinants and to check the zero-diagonal jet identities in
dimensions 2, 3, and 4.
"""

from __future__ import annotations

from decimal import Decimal, localcontext
from fractions import Fraction
from itertools import permutations
import json
import math
from pathlib import Path


MAX_DEGREE = 4


def F(num: int, den: int = 1) -> Fraction:
    return Fraction(num, den)


def frac_to_str(x: Fraction) -> str:
    if x.denominator == 1:
        return str(x.numerator)
    return f"{x.numerator}/{x.denominator}"


def serialize(obj):
    if isinstance(obj, Fraction):
        return frac_to_str(obj)
    if isinstance(obj, Decimal):
        return str(obj)
    if isinstance(obj, tuple):
        return [serialize(x) for x in obj]
    if isinstance(obj, list):
        return [serialize(x) for x in obj]
    if isinstance(obj, dict):
        return {str(k): serialize(v) for k, v in obj.items()}
    return obj


def poly_zero():
    return [Fraction(0) for _ in range(MAX_DEGREE + 1)]


def poly_const(c: Fraction):
    out = poly_zero()
    out[0] = c
    return out


def poly_linear(c0: Fraction, c1: Fraction):
    out = poly_zero()
    out[0] = c0
    out[1] = c1
    return out


def poly_add(a, b):
    return [a[i] + b[i] for i in range(MAX_DEGREE + 1)]


def poly_neg(a):
    return [-x for x in a]


def poly_mul(a, b):
    out = poly_zero()
    for i, ai in enumerate(a):
        if ai == 0:
            continue
        for j, bj in enumerate(b):
            if bj == 0 or i + j > MAX_DEGREE:
                continue
            out[i + j] += ai * bj
    return out


def permutation_sign(perm):
    inversions = 0
    for i in range(len(perm)):
        for j in range(i + 1, len(perm)):
            if perm[i] > perm[j]:
                inversions += 1
    return -1 if inversions % 2 else 1


def det_poly(matrix):
    n = len(matrix)
    if n == 0:
        return poly_const(F(1))
    total = poly_zero()
    for perm in permutations(range(n)):
        term = poly_const(F(permutation_sign(perm)))
        for i, j in enumerate(perm):
            term = poly_mul(term, matrix[i][j])
        total = poly_add(total, term)
    return total


def principal_poly_matrix(x, D, mask):
    idx = [i for i in range(len(x)) if mask & (1 << i)]
    out = []
    for i in idx:
        row = []
        for j in idx:
            if i == j:
                row.append(poly_linear(x[i], D[i][i]))
            else:
                row.append(poly_linear(F(0), D[i][j]))
        out.append(row)
    return out


def inclusion_polys(x, D):
    n = len(x)
    return [det_poly(principal_poly_matrix(x, D, mask)) for mask in range(1 << n)]


def superset_mobius(values, n):
    out = [v[:] if isinstance(v, list) else v for v in values]
    for bit_index in range(n):
        bit = 1 << bit_index
        for mask in range(1 << n):
            if (mask & bit) == 0:
                out[mask] = poly_add(out[mask], poly_neg(out[mask | bit]))
    return out


def atom_polys(x, D):
    return superset_mobius(inclusion_polys(x, D), len(x))


def derivative(poly, order):
    return math.factorial(order) * poly[order]


def product_atom(x, mask):
    out = F(1)
    for i, xi in enumerate(x):
        out *= xi if mask & (1 << i) else (1 - xi)
    return out


def pairs(n):
    for i in range(n):
        for j in range(i + 1, n):
            yield i, j


def zeta(xi, in_set):
    return F(1, 1) / xi if in_set else -F(1, 1) / (1 - xi)


def static_det(matrix):
    n = len(matrix)
    if n == 0:
        return F(1)
    total = F(0)
    for perm in permutations(range(n)):
        term = F(permutation_sign(perm))
        for i, j in enumerate(perm):
            term *= matrix[i][j]
        total += term
    return total


def principal_static(matrix, mask):
    idx = [i for i in range(len(matrix)) if mask & (1 << i)]
    return [[matrix[i][j] for j in idx] for i in idx]


def static_atoms_from_kernel(K):
    n = len(K)
    inclusions = [static_det(principal_static(K, mask)) for mask in range(1 << n)]
    atoms = inclusions[:]
    for bit_index in range(n):
        bit = 1 << bit_index
        for mask in range(1 << n):
            if (mask & bit) == 0:
                atoms[mask] -= atoms[mask | bit]
    return atoms, inclusions


def ldl_pivots(matrix):
    n = len(matrix)
    lower = [[F(1) if i == j else F(0) for j in range(n)] for i in range(n)]
    diag = [F(0) for _ in range(n)]
    for j in range(n):
        value = matrix[j][j] - sum(lower[j][k] * lower[j][k] * diag[k] for k in range(j))
        diag[j] = value
        if value == 0:
            break
        for i in range(j + 1, n):
            lower[i][j] = (
                matrix[i][j] - sum(lower[i][k] * lower[j][k] * diag[k] for k in range(j))
            ) / value
    return diag


def is_spd(matrix):
    pivots = ldl_pivots(matrix)
    return len(pivots) == len(matrix) and all(p > 0 for p in pivots), pivots


def identity(n):
    return [[F(1) if i == j else F(0) for j in range(n)] for i in range(n)]


def mat_sub(A, B):
    n = len(A)
    return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]


def decimal_entropy(atoms, precision=80):
    with localcontext() as ctx:
        ctx.prec = precision
        entropy = Decimal(0)
        for p in atoms:
            q = Decimal(p.numerator) / Decimal(p.denominator)
            if q <= 0:
                raise ArithmeticError("nonpositive atom")
            entropy -= q * q.ln()
        return +entropy


def check_global_sample(name, x, offdiag):
    n = len(x)
    K = [[F(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        K[i][i] = x[i]
    for (i, j), value in offdiag.items():
        K[i][j] = value
        K[j][i] = value
    atoms, inclusions = static_atoms_from_kernel(K)
    X_atoms = [product_atom(x, mask) for mask in range(1 << n)]
    K_spd, K_pivots = is_spd(K)
    IK_spd, IK_pivots = is_spd(mat_sub(identity(n), K))
    marginals = [
        sum(atoms[mask] for mask in range(1 << n) if mask & (1 << i))
        for i in range(n)
    ]
    pair_errors = {}
    pair_product_gaps = {}
    for i, j in pairs(n):
        pair_prob = sum(
            atoms[mask]
            for mask in range(1 << n)
            if (mask & (1 << i)) and (mask & (1 << j))
        )
        expected_dpp = x[i] * x[j] - K[i][j] * K[i][j]
        pair_errors[(i, j)] = pair_prob - expected_dpp
        pair_product_gaps[(i, j)] = pair_prob - x[i] * x[j]
    H_K = decimal_entropy(atoms)
    H_X = decimal_entropy(X_atoms)
    return {
        "name": name,
        "n": n,
        "strict_K": K_spd,
        "strict_I_minus_K": IK_spd,
        "min_K_ldl_pivot": min(K_pivots),
        "min_I_minus_K_ldl_pivot": min(IK_pivots),
        "atom_sum": sum(atoms),
        "min_atom": min(atoms),
        "marginal_errors": [marginals[i] - x[i] for i in range(n)],
        "pair_inclusion_errors": pair_errors,
        "pair_minus_product": pair_product_gaps,
        "has_nonzero_pair_product_gap": any(v != 0 for v in pair_product_gaps.values()),
        "entropy_K_decimal": H_K,
        "entropy_diagonal_decimal": H_X,
        "entropy_gap_diagonal_minus_K": H_X - H_K,
        "status": "PASS"
        if (
            K_spd
            and IK_spd
            and min(atoms) > 0
            and sum(atoms) == 1
            and all(marginals[i] == x[i] for i in range(n))
            and all(v == 0 for v in pair_errors.values())
            and any(v != 0 for v in pair_product_gaps.values())
            and H_X > H_K
        )
        else "FAIL",
    }


def check_jet_case(name, x, D):
    n = len(x)
    atoms = atom_polys(x, D)
    p = {
        order: [derivative(poly, order) for poly in atoms]
        for order in range(5)
    }
    p0_errors = {
        mask: p[0][mask] - product_atom(x, mask)
        for mask in range(1 << n)
        if p[0][mask] != product_atom(x, mask)
    }
    p1_nonzero = {mask: p[1][mask] for mask in range(1 << n) if p[1][mask] != 0}
    mass_derivatives = {
        order: sum(p[order][mask] for mask in range(1 << n))
        for order in range(1, 5)
    }
    singleton_derivatives = {
        order: [
            sum(p[order][mask] for mask in range(1 << n) if mask & (1 << i))
            for i in range(n)
        ]
        for order in range(1, 5)
    }
    pair_second_errors = {}
    for i, j in pairs(n):
        lhs = sum(
            p[2][mask]
            for mask in range(1 << n)
            if (mask & (1 << i)) and (mask & (1 << j))
        )
        rhs = -2 * D[i][j] * D[i][j]
        if lhs != rhs:
            pair_second_errors[(i, j)] = lhs - rhs

    q_formula_errors = {}
    for mask in range(1 << n):
        score = F(0)
        for i, j in pairs(n):
            zi = zeta(x[i], bool(mask & (1 << i)))
            zj = zeta(x[j], bool(mask & (1 << j)))
            score += D[i][j] * D[i][j] * zi * zj
        score *= -2
        if p[2][mask] != p[0][mask] * score:
            q_formula_errors[mask] = p[2][mask] - p[0][mask] * score

    # Orthogonality of distinct edge characters under the product atom law.
    orthogonality_errors = {}
    pair_list = list(pairs(n))
    for edge_a_index, (i, j) in enumerate(pair_list):
        for k, ell in pair_list[edge_a_index + 1 :]:
            expectation = F(0)
            for mask in range(1 << n):
                value = (
                    zeta(x[i], bool(mask & (1 << i)))
                    * zeta(x[j], bool(mask & (1 << j)))
                    * zeta(x[k], bool(mask & (1 << k)))
                    * zeta(x[ell], bool(mask & (1 << ell)))
                )
                expectation += p[0][mask] * value
            if expectation != 0:
                orthogonality_errors[((i, j), (k, ell))] = expectation

    fisher4 = sum(p[2][mask] * p[2][mask] / p[0][mask] for mask in range(1 << n))
    explicit_fisher4 = 4 * sum(
        D[i][j] ** 4 / (x[i] * (1 - x[i]) * x[j] * (1 - x[j]))
        for i, j in pairs(n)
    )
    H4 = -3 * fisher4
    explicit_H4 = -12 * sum(
        D[i][j] ** 4 / (x[i] * (1 - x[i]) * x[j] * (1 - x[j]))
        for i, j in pairs(n)
    )
    frob2 = sum(D[i][j] * D[i][j] for i in range(n) for j in range(n))
    a = min(x)
    b = max(x)
    M_candidates = [a * (1 - a), b * (1 - b)]
    if a <= F(1, 2) <= b:
        M_candidates.append(F(1, 4))
    M = max(M_candidates)
    bound_rhs = -6 * frob2 * frob2 / (n * (n - 1) * M * M)
    zero_log_linear_terms = all(v == 0 for v in mass_derivatives.values()) and all(
        v == 0 for vals in singleton_derivatives.values() for v in vals
    )
    ok = (
        not p0_errors
        and not p1_nonzero
        and zero_log_linear_terms
        and not pair_second_errors
        and not q_formula_errors
        and not orthogonality_errors
        and fisher4 == explicit_fisher4
        and H4 == explicit_H4
        and H4 < 0
        and H4 <= bound_rhs
    )
    return {
        "name": name,
        "n": n,
        "atom_count": 1 << n,
        "p0_product_errors": p0_errors,
        "p1_nonzero": p1_nonzero,
        "mass_derivatives_1_to_4": mass_derivatives,
        "singleton_derivatives_1_to_4": singleton_derivatives,
        "pair_second_errors": pair_second_errors,
        "q_over_p_errors": q_formula_errors,
        "distinct_edge_orthogonality_errors": orthogonality_errors,
        "sum_q_squared_over_p0": fisher4,
        "explicit_sum_q_squared_over_p0": explicit_fisher4,
        "H4_from_minus3_fisher4": H4,
        "explicit_H4_edge_formula": explicit_H4,
        "frob_norm_squared": frob2,
        "M_box_value": M,
        "uniform_bound_rhs": bound_rhs,
        "H4_minus_bound_rhs": H4 - bound_rhs,
        "formal_entropy_derivative_zero_reason": (
            "p'(0)=0 and the mass/singleton derivative sums annihilate "
            "the affine log p_S(0) coefficients through orders 2,3,4"
        ),
        "status": "PASS" if ok else "FAIL",
    }


def main():
    jet_cases = [
        (
            "n2_fraction_edge",
            [F(2, 7), F(5, 8)],
            [[F(0), F(3, 20)], [F(3, 20), F(0)]],
        ),
        (
            "n3_fraction_mixed_signs",
            [F(2, 9), F(4, 7), F(5, 6)],
            [
                [F(0), F(1, 9), -F(2, 15)],
                [F(1, 9), F(0), F(1, 10)],
                [-F(2, 15), F(1, 10), F(0)],
            ],
        ),
        (
            "n4_fraction_all_edges",
            [F(3, 11), F(5, 13), F(7, 17), F(9, 19)],
            [
                [F(0), F(1, 12), -F(1, 14), F(1, 15)],
                [F(1, 12), F(0), F(2, 21), -F(1, 16)],
                [-F(1, 14), F(2, 21), F(0), F(1, 18)],
                [F(1, 15), -F(1, 16), F(1, 18), F(0)],
            ],
        ),
    ]
    global_samples = [
        (
            "n2_strict_fixed_diagonal",
            [F(2, 7), F(5, 8)],
            {(0, 1): F(1, 30)},
        ),
        (
            "n3_strict_fixed_diagonal",
            [F(2, 9), F(4, 7), F(5, 6)],
            {(0, 1): F(1, 50), (0, 2): -F(1, 60), (1, 2): F(1, 70)},
        ),
        (
            "n4_strict_fixed_diagonal",
            [F(3, 11), F(5, 13), F(7, 17), F(9, 19)],
            {
                (0, 1): F(1, 80),
                (0, 2): -F(1, 90),
                (0, 3): F(1, 100),
                (1, 2): F(1, 110),
                (1, 3): -F(1, 120),
                (2, 3): F(1, 130),
            },
        ),
    ]
    jet_results = [check_jet_case(*case) for case in jet_cases]
    global_results = [check_global_sample(*sample) for sample in global_samples]
    status = "PASS" if all(r["status"] == "PASS" for r in jet_results + global_results) else "FAIL"
    result = {
        "status": status,
        "independence": "does not import author sanity or author gate",
        "global_fiber_checks": global_results,
        "jet_checks": jet_results,
        "layer_status": {
            "fixed_diagonal_global_maximum_semantics": "PASS"
            if all(r["status"] == "PASS" for r in global_results)
            else "FAIL",
            "zero_diagonal_exact_event_jet": "PASS"
            if all(r["status"] == "PASS" for r in jet_results)
            else "FAIL",
            "compact_box_fourth_order_constant": "PASS"
            if all(r["status"] == "PASS" and r["H4_minus_bound_rhs"] <= 0 for r in jet_results)
            else "FAIL",
        },
    }
    out = Path(__file__).with_name("fresh_u2_audit.json")
    out.write_text(json.dumps(serialize(result), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(serialize({
        "status": status,
        "json": str(out),
        "layer_status": result["layer_status"],
        "jet_cases": {r["name"]: r["status"] for r in jet_results},
        "global_cases": {r["name"]: r["status"] for r in global_results},
    }), indent=2, ensure_ascii=False))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
