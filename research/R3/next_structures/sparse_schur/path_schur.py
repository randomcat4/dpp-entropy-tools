"""Sparse Schur prototype for path-sparse L-ensemble DPP entropy.

The structure is not the old block-exchangeable repeated-row family.  The
input is a real symmetric positive definite tridiagonal L matrix on a path.
It defines the strict real marginal kernel K=L(I+L)^(-1), hence 0<K<I.

For a path, det(L_S) factors over the selected contiguous runs of S.  This file
uses that factorization to compute

    H = log Z - (1/Z) sum_S det(L_S) log det(L_S),
    Z = det(I+L),

without enumerating all events.  Direct Mobius comparison is retained for
n<=8 only.
"""

from __future__ import annotations

import argparse
import json
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
from typing import Sequence


Matrix = list[list[Fraction]]


def q(x) -> Fraction:
    return x if isinstance(x, Fraction) else Fraction(x)


def dec(x: Fraction, precision: int) -> Decimal:
    return Decimal(x.numerator) / Decimal(x.denominator)


def eye(n: int) -> Matrix:
    return [[Fraction(i == j) for j in range(n)] for i in range(n)]


def zeros(n: int, m: int) -> Matrix:
    return [[Fraction(0) for _ in range(m)] for _ in range(n)]


def mat_sub(a: Matrix, b: Matrix) -> Matrix:
    return [[x - y for x, y in zip(row_a, row_b)] for row_a, row_b in zip(a, b)]


def mat_mul(a: Matrix, b: Matrix) -> Matrix:
    bt = list(zip(*b))
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def det_bareiss(a: Matrix) -> Fraction:
    n = len(a)
    if n == 0:
        return Fraction(1)
    m = [row[:] for row in a]
    sign = Fraction(1)
    previous = Fraction(1)
    for k in range(n - 1):
        pivot = None
        for i in range(k, n):
            if m[i][k] != 0:
                pivot = i
                break
        if pivot is None:
            return Fraction(0)
        if pivot != k:
            m[k], m[pivot] = m[pivot], m[k]
            sign = -sign
        pivot_value = m[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                m[i][j] = (m[i][j] * pivot_value - m[i][k] * m[k][j]) / previous
        previous = pivot_value
        for i in range(k + 1, n):
            m[i][k] = Fraction(0)
    return sign * m[n - 1][n - 1]


def inverse(a: Matrix) -> Matrix:
    n = len(a)
    m = [row[:] + ident[:] for row, ident in zip(a, eye(n))]
    for k in range(n):
        pivot = None
        for i in range(k, n):
            if m[i][k] != 0:
                pivot = i
                break
        if pivot is None:
            raise ValueError("singular matrix")
        if pivot != k:
            m[k], m[pivot] = m[pivot], m[k]
        scale = m[k][k]
        m[k] = [x / scale for x in m[k]]
        for i in range(n):
            if i == k:
                continue
            factor = m[i][k]
            if factor:
                m[i] = [x - factor * y for x, y in zip(m[i], m[k])]
    return [row[n:] for row in m]


def principal_submatrix(a: Matrix, indices: Sequence[int]) -> Matrix:
    return [[a[i][j] for j in indices] for i in indices]


def indices(mask: int, n: int) -> list[int]:
    return [i for i in range(n) if (mask >> i) & 1]


def build_tridiagonal(diagonal: Sequence[Fraction], edge: Sequence[Fraction]) -> Matrix:
    n = len(diagonal)
    if len(edge) != n - 1:
        raise ValueError("edge length must be n-1")
    out = zeros(n, n)
    for i, value in enumerate(diagonal):
        out[i][i] = q(value)
    for i, value in enumerate(edge):
        out[i][i + 1] = q(value)
        out[i + 1][i] = q(value)
    return out


def leading_continuants(diagonal: Sequence[Fraction], edge: Sequence[Fraction]) -> list[Fraction]:
    if not diagonal:
        return []
    out = [q(diagonal[0])]
    if len(diagonal) == 1:
        return out
    previous2 = Fraction(1)
    previous1 = q(diagonal[0])
    for i in range(1, len(diagonal)):
        current = q(diagonal[i]) * previous1 - q(edge[i - 1]) ** 2 * previous2
        out.append(current)
        previous2, previous1 = previous1, current
    return out


def is_spd_tridiagonal(diagonal: Sequence[Fraction], edge: Sequence[Fraction]) -> tuple[bool, list[Fraction]]:
    minors = leading_continuants(diagonal, edge)
    return all(x > 0 for x in minors), minors


def interval_determinants(diagonal: Sequence[Fraction], edge: Sequence[Fraction]) -> list[list[Fraction]]:
    """kappa[start][end] = det L_{start..end}, for start<=end."""

    n = len(diagonal)
    kappa = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for start in range(n):
        previous2 = Fraction(1)
        previous1 = q(diagonal[start])
        kappa[start][start] = previous1
        for end in range(start + 1, n):
            current = q(diagonal[end]) * previous1 - q(edge[end - 1]) ** 2 * previous2
            kappa[start][end] = current
            previous2, previous1 = previous1, current
    return kappa


def det_i_plus_l(diagonal: Sequence[Fraction], edge: Sequence[Fraction]) -> Fraction:
    shifted = [q(x) + 1 for x in diagonal]
    return leading_continuants(shifted, edge)[-1]


def path_weight(mask: int, kappa: list[list[Fraction]], n: int) -> Fraction:
    weight = Fraction(1)
    i = 0
    while i < n:
        if not ((mask >> i) & 1):
            i += 1
            continue
        start = i
        while i + 1 < n and ((mask >> (i + 1)) & 1):
            i += 1
        weight *= kappa[start][i]
        i += 1
    return weight


def path_entropy_dp(
    diagonal: Sequence[Fraction], edge: Sequence[Fraction], precision: int = 80
) -> dict[str, object]:
    """Compute path L-ensemble entropy by run-Schur dynamic programming."""

    diagonal = [q(x) for x in diagonal]
    edge = [q(x) for x in edge]
    n = len(diagonal)
    ok, minors = is_spd_tridiagonal(diagonal, edge)
    if not ok:
        raise ValueError("L is not certified positive definite by leading minors")
    kappa = interval_determinants(diagonal, edge)
    if any(kappa[i][j] <= 0 for i in range(n) for j in range(i, n)):
        raise ValueError("an interval principal minor is nonpositive")

    z: list[Fraction] = [Fraction(0) for _ in range(n + 1)]
    t_log: list[Decimal] = [Decimal(0) for _ in range(n + 1)]
    z[0] = Fraction(1)

    with localcontext() as ctx:
        ctx.prec = precision
        for length in range(1, n + 1):
            z_value = z[length - 1]
            t_value = t_log[length - 1]
            end = length - 1
            for start in range(0, length):
                prefix_len = 0 if start == 0 else start - 1
                block = kappa[start][end]
                block_dec = dec(block, precision)
                prefix_dec = dec(z[prefix_len], precision)
                z_value += z[prefix_len] * block
                t_value += block_dec * t_log[prefix_len]
                t_value += prefix_dec * block_dec * block_dec.ln()
            z[length] = z_value
            t_log[length] = +t_value

        z_dec = dec(z[n], precision)
        entropy = +(z_dec.ln() - t_log[n] / z_dec)
    return {
        "n": n,
        "state_count": n * (n + 1) // 2,
        "full_events": 2**n,
        "Z": z[n],
        "det_I_plus_L": det_i_plus_l(diagonal, edge),
        "entropy": entropy,
        "leading_minors": minors,
        "min_interval_det": min(kappa[i][j] for i in range(n) for j in range(i, n)),
    }


def event_probabilities_mobius(k: Matrix) -> list[Fraction]:
    n = len(k)
    full = (1 << n) - 1
    inclusion = [
        det_bareiss(principal_submatrix(k, indices(mask, n))) for mask in range(1 << n)
    ]
    atoms: list[Fraction] = []
    for s_mask in range(1 << n):
        comp = full ^ s_mask
        total = Fraction(0)
        t_mask = comp
        while True:
            total += (-1 if t_mask.bit_count() & 1 else 1) * inclusion[s_mask | t_mask]
            if t_mask == 0:
                break
            t_mask = (t_mask - 1) & comp
        atoms.append(total)
    return atoms


def k_from_l(l_matrix: Matrix) -> Matrix:
    n = len(l_matrix)
    return mat_mul(l_matrix, inverse([[Fraction(i == j) + l_matrix[i][j] for j in range(n)] for i in range(n)]))


def direct_validation_case(
    diagonal: Sequence[Fraction], edge: Sequence[Fraction], precision: int = 80
) -> dict[str, object]:
    diagonal = [q(x) for x in diagonal]
    edge = [q(x) for x in edge]
    n = len(diagonal)
    if n > 8:
        raise ValueError("direct Mobius validation is intentionally limited to n<=8")

    l_matrix = build_tridiagonal(diagonal, edge)
    k_matrix = k_from_l(l_matrix)
    z = det_i_plus_l(diagonal, edge)
    kappa = interval_determinants(diagonal, edge)
    l_atoms = [path_weight(mask, kappa, n) / z for mask in range(1 << n)]
    mobius_atoms = event_probabilities_mobius(k_matrix)
    mismatches = [
        (mask, mobius_atoms[mask], l_atoms[mask])
        for mask in range(1 << n)
        if mobius_atoms[mask] != l_atoms[mask]
    ]

    with localcontext() as ctx:
        ctx.prec = precision
        direct_entropy = Decimal(0)
        for p in mobius_atoms:
            if p:
                p_dec = dec(p, precision)
                direct_entropy -= p_dec * p_dec.ln()
        dp_entropy = path_entropy_dp(diagonal, edge, precision=precision)["entropy"]
        entropy_abs_diff = abs(+direct_entropy - dp_entropy)

    return {
        "n": n,
        "events_checked": 2**n,
        "mobius_sum": sum(mobius_atoms, Fraction(0)),
        "l_ensemble_sum": sum(l_atoms, Fraction(0)),
        "mismatch_count": len(mismatches),
        "first_mismatch": None if not mismatches else str(mismatches[0]),
        "min_atom": min(mobius_atoms),
        "entropy_abs_diff": entropy_abs_diff,
        "Z": z,
    }


def fraction_to_json(x):
    if isinstance(x, Fraction):
        return f"{x.numerator}/{x.denominator}"
    if isinstance(x, Decimal):
        return str(x)
    if isinstance(x, list):
        return [fraction_to_json(v) for v in x]
    if isinstance(x, dict):
        return {key: fraction_to_json(value) for key, value in x.items()}
    return x


def self_test(precision: int = 90) -> dict[str, object]:
    cases = [
        {
            "name": "heterogeneous_path_n6",
            "diagonal": [Fraction(3, 2), Fraction(7, 5), Fraction(11, 6), Fraction(13, 7), Fraction(17, 8), Fraction(19, 9)],
            "edge": [Fraction(1, 5), -Fraction(1, 7), Fraction(1, 6), Fraction(1, 8), -Fraction(1, 9)],
        },
        {
            "name": "heterogeneous_path_n8",
            "diagonal": [Fraction(5, 4), Fraction(4, 3), Fraction(3, 2), Fraction(7, 4), Fraction(9, 5), Fraction(11, 6), Fraction(13, 7), Fraction(15, 8)],
            "edge": [Fraction(1, 6), Fraction(1, 8), -Fraction(1, 9), Fraction(1, 10), Fraction(1, 11), -Fraction(1, 12), Fraction(1, 13)],
        },
    ]
    validations = []
    for case in cases:
        result = direct_validation_case(case["diagonal"], case["edge"], precision)
        result["name"] = case["name"]
        validations.append(result)

    smoke_diag = [Fraction(6 + (i % 5), 5) for i in range(12)]
    smoke_edge = [Fraction((-1) ** i, 10 + i) for i in range(11)]
    smoke = path_entropy_dp(smoke_diag, smoke_edge, precision=70)

    return {
        "status": "PASS" if all(v["mismatch_count"] == 0 for v in validations) else "FAIL",
        "direct_validations": validations,
        "n12_smoke": smoke,
        "notes": [
            "Exact atom comparisons are rational equalities.",
            "Entropy differences use Decimal logarithms and are diagnostic.",
            "The n=12 smoke uses DP only and is not a Mobius enumeration.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--out", type=Path)
    parser.add_argument("--precision", type=int, default=90)
    args = parser.parse_args()

    if not args.self_test:
        parser.error("this prototype currently exposes --self-test")
    result = fraction_to_json(self_test(args.precision))
    text = json.dumps(result, indent=2)
    if args.out:
        args.out.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
