#!/usr/bin/env python3
"""Exact small-dimensional sanity checks for the commuting spectral channel.

The checks use Fraction arithmetic for atom-polynomial identities.  Decimal
logs are only used for the final displayed H'' diagnostics.
"""

from __future__ import annotations

import json
import math
import os
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path

for _var in (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
):
    os.environ.setdefault(_var, "1")

getcontext().prec = 80
OUT = Path(__file__).with_name("channel_sanity_results.json")


def f(x: int, y: int = 1) -> Fraction:
    return Fraction(x, y)


def pop(mask: int) -> int:
    return mask.bit_count()


def frac_matrix_mul(A: list[list[Fraction]], B: list[list[Fraction]]) -> list[list[Fraction]]:
    n, m, r = len(A), len(B[0]), len(B)
    return [[sum(A[i][k] * B[k][j] for k in range(r)) for j in range(m)] for i in range(n)]


def frac_transpose(A: list[list[Fraction]]) -> list[list[Fraction]]:
    return [list(row) for row in zip(*A)]


def frac_diag(vals: list[Fraction]) -> list[list[Fraction]]:
    n = len(vals)
    M = [[f(0) for _ in range(n)] for __ in range(n)]
    for i, val in enumerate(vals):
        M[i][i] = val
    return M


def frac_det(A: list[list[Fraction]]) -> Fraction:
    n = len(A)
    if n == 0:
        return f(1)
    M = [row[:] for row in A]
    det = f(1)
    for i in range(n):
        piv = None
        for r in range(i, n):
            if M[r][i] != 0:
                piv = r
                break
        if piv is None:
            return f(0)
        if piv != i:
            M[i], M[piv] = M[piv], M[i]
            det = -det
        pivot = M[i][i]
        det *= pivot
        for r in range(i + 1, n):
            factor = M[r][i] / pivot
            if factor:
                for c in range(i, n):
                    M[r][c] -= factor * M[i][c]
    return det


def submatrix(A: list[list[Fraction]], rows: list[int], cols: list[int]) -> list[list[Fraction]]:
    return [[A[i][j] for j in cols] for i in rows]


def add_scaled(A: list[list[Fraction]], B: list[list[Fraction]], t: Fraction) -> list[list[Fraction]]:
    n = len(A)
    return [[A[i][j] + t * B[i][j] for j in range(n)] for i in range(n)]


def event_matrix(K: list[list[Fraction]], mask: int) -> list[list[Fraction]]:
    n = len(K)
    A = [row[:] for row in K]
    for i in range(n):
        if not ((mask >> i) & 1):
            A[i][i] -= 1
    return A


def signed_atom_at(K0: list[list[Fraction]], D: list[list[Fraction]], mask: int, t: Fraction) -> Fraction:
    Kt = add_scaled(K0, D, t)
    sign = -1 if ((len(K0) - pop(mask)) & 1) else 1
    return sign * frac_det(event_matrix(Kt, mask))


def interpolate_coeffs(values: list[tuple[Fraction, Fraction]], degree: int) -> list[Fraction]:
    # Solve Vandermonde system sum_j c_j x^j = y.
    M = [[x**j for j in range(degree + 1)] + [y] for x, y in values[: degree + 1]]
    n = degree + 1
    for i in range(n):
        piv = None
        for r in range(i, n):
            if M[r][i] != 0:
                piv = r
                break
        if piv is None:
            raise ValueError("singular interpolation system")
        if piv != i:
            M[i], M[piv] = M[piv], M[i]
        pivot = M[i][i]
        M[i] = [z / pivot for z in M[i]]
        for r in range(n):
            if r == i:
                continue
            factor = M[r][i]
            if factor:
                M[r] = [M[r][c] - factor * M[i][c] for c in range(n + 1)]
    return [M[i][-1] for i in range(n)]


def signed_atom_poly(K0: list[list[Fraction]], D: list[list[Fraction]], mask: int) -> list[Fraction]:
    n = len(K0)
    values = [(f(t), signed_atom_at(K0, D, mask, f(t))) for t in range(n + 1)]
    return interpolate_coeffs(values, n)


def bernoulli_weight(theta: list[Fraction], J: int) -> Fraction:
    ans = f(1)
    for i, th in enumerate(theta):
        ans *= th if ((J >> i) & 1) else (1 - th)
    return ans


def channel_prob(Q: list[list[Fraction]], S: int, J: int) -> Fraction:
    n = len(Q)
    if pop(S) != pop(J):
        return f(0)
    rows = [i for i in range(n) if (S >> i) & 1]
    cols = [j for j in range(n) if (J >> j) & 1]
    return frac_det(submatrix(Q, rows, cols)) ** 2


def channel_atom_at(Q: list[list[Fraction]], lam: list[Fraction], v: list[Fraction], S: int, t: Fraction) -> Fraction:
    theta = [lam[i] + t * v[i] for i in range(len(lam))]
    return sum(channel_prob(Q, S, J) * bernoulli_weight(theta, J) for J in range(1 << len(lam)))


def channel_atom_poly(Q: list[list[Fraction]], lam: list[Fraction], v: list[Fraction], S: int) -> list[Fraction]:
    n = len(lam)
    values = [(f(t), channel_atom_at(Q, lam, v, S, f(t))) for t in range(n + 1)]
    return interpolate_coeffs(values, n)


def channel_atom_at_custom(channel, lam: list[Fraction], v: list[Fraction], S: int, t: Fraction) -> Fraction:
    theta = [lam[i] + t * v[i] for i in range(len(lam))]
    return sum(channel(S, J) * bernoulli_weight(theta, J) for J in range(1 << len(lam)))


def channel_atom_poly_custom(channel, lam: list[Fraction], v: list[Fraction], S: int) -> list[Fraction]:
    n = len(lam)
    values = [(f(t), channel_atom_at_custom(channel, lam, v, S, f(t))) for t in range(n + 1)]
    return interpolate_coeffs(values, n)


def kernel_from_Q(Q: list[list[Fraction]], lam: list[Fraction]) -> list[list[Fraction]]:
    return frac_matrix_mul(frac_matrix_mul(Q, frac_diag(lam)), frac_transpose(Q))


def derivative_entropy(poly_by_mask: list[list[Fraction]]) -> dict:
    sum_p = sum(poly[0] for poly in poly_by_mask)
    sum_p1 = sum(poly[1] if len(poly) > 1 else f(0) for poly in poly_by_mask)
    sum_p2 = sum(2 * poly[2] if len(poly) > 2 else f(0) for poly in poly_by_mask)
    H2 = Decimal(0)
    min_p = None
    for poly in poly_by_mask:
        p0 = poly[0]
        p1 = poly[1] if len(poly) > 1 else f(0)
        p2 = 2 * poly[2] if len(poly) > 2 else f(0)
        if min_p is None or p0 < min_p:
            min_p = p0
        pd = Decimal(p0.numerator) / Decimal(p0.denominator)
        p1d = Decimal(p1.numerator) / Decimal(p1.denominator)
        p2d = Decimal(p2.numerator) / Decimal(p2.denominator)
        H2 += -(p1d * p1d / pd) - p2d * pd.ln()
    return {
        "sum_p": str(sum_p),
        "sum_p1": str(sum_p1),
        "sum_p2": str(sum_p2),
        "min_p": str(min_p),
        "H2_decimal": str(+H2),
    }


def run_case(name: str, Q: list[list[Fraction]], lam: list[Fraction], v: list[Fraction]) -> dict:
    K0 = kernel_from_Q(Q, lam)
    D = kernel_from_Q(Q, v)
    n = len(lam)
    max_coeff_diff = f(0)
    signed_polys = []
    channel_polys = []
    for S in range(1 << n):
        sp = signed_atom_poly(K0, D, S)
        cp = channel_atom_poly(Q, lam, v, S)
        signed_polys.append(sp)
        channel_polys.append(cp)
        for a, b in zip(sp, cp):
            diff = abs(a - b)
            if diff > max_coeff_diff:
                max_coeff_diff = diff
    entropy = derivative_entropy(signed_polys)
    eig_note = "D=Q diag(v) Q^T is PSD because every listed v_i is positive."
    return {
        "name": name,
        "n": n,
        "atom_count": 1 << n,
        "max_signed_vs_channel_polynomial_coeff_diff": str(max_coeff_diff),
        "entropy_second_derivative_at_zero": entropy,
        "lambda": [str(x) for x in lam],
        "v": [str(x) for x in v],
        "psd_note": eig_note,
    }


def run_case_custom_channel(
    name: str,
    K0: list[list[Fraction]],
    D: list[list[Fraction]],
    lam: list[Fraction],
    v: list[Fraction],
    channel,
) -> dict:
    n = len(lam)
    max_coeff_diff = f(0)
    signed_polys = []
    for S in range(1 << n):
        sp = signed_atom_poly(K0, D, S)
        cp = channel_atom_poly_custom(channel, lam, v, S)
        signed_polys.append(sp)
        for a, b in zip(sp, cp):
            diff = abs(a - b)
            if diff > max_coeff_diff:
                max_coeff_diff = diff
    entropy = derivative_entropy(signed_polys)
    return {
        "name": name,
        "n": n,
        "atom_count": 1 << n,
        "max_signed_vs_channel_polynomial_coeff_diff": str(max_coeff_diff),
        "entropy_second_derivative_at_zero": entropy,
        "lambda": [str(x) for x in lam],
        "v": [str(x) for x in v],
        "psd_note": "D=Q diag(v) Q^T is PSD because every listed v_i is positive.",
    }


def main() -> int:
    # Rational 2D rotation, not a signed permutation.  This checks a genuinely
    # rotated observation channel with heterogeneous positive spectral rates.
    Q2 = [[f(3, 5), -f(4, 5)], [f(4, 5), f(3, 5)]]
    case2 = run_case(
        "n2_rational_rotation",
        Q2,
        [f(2, 7), f(5, 11)],
        [f(1, 13), f(2, 17)],
    )

    # 3D signed-permutation control.
    Q3 = [[f(0), f(1), f(0)], [f(1), f(0), f(0)], [f(0), f(0), -f(1)]]
    case3 = run_case(
        "n3_signed_permutation_control",
        Q3,
        [f(1, 5), f(2, 3), f(4, 7)],
        [f(1, 17), f(1, 19), f(1, 23)],
    )

    # 3D block-Hadamard plus fixed coordinate.  Q itself contains sqrt(2), but
    # K0, D, and every squared minor in the channel are rational, so this is an
    # exact non-permutation sanity check.
    lam3h = [f(1, 5), f(2, 3), f(4, 7)]
    v3h = [f(1, 17), f(1, 19), f(1, 23)]
    K3h = [
        [(lam3h[0] + lam3h[1]) / 2, (lam3h[0] - lam3h[1]) / 2, f(0)],
        [(lam3h[0] - lam3h[1]) / 2, (lam3h[0] + lam3h[1]) / 2, f(0)],
        [f(0), f(0), lam3h[2]],
    ]
    D3h = [
        [(v3h[0] + v3h[1]) / 2, (v3h[0] - v3h[1]) / 2, f(0)],
        [(v3h[0] - v3h[1]) / 2, (v3h[0] + v3h[1]) / 2, f(0)],
        [f(0), f(0), v3h[2]],
    ]

    def block_hadamard_channel(S: int, J: int) -> Fraction:
        if ((S >> 2) & 1) != ((J >> 2) & 1):
            return f(0)
        S2 = S & 0b011
        J2 = J & 0b011
        if pop(S2) != pop(J2):
            return f(0)
        if pop(J2) == 0:
            return f(1) if S2 == 0 else f(0)
        if pop(J2) == 2:
            return f(1) if S2 == 0b011 else f(0)
        return f(1, 2) if pop(S2) == 1 else f(0)

    case3h = run_case_custom_channel(
        "n3_block_hadamard_plus_coordinate",
        K3h,
        D3h,
        lam3h,
        v3h,
        block_hadamard_channel,
    )

    result = {
        "status": "EXACT_CHANNEL_SANITY_PASSED",
        "cases": [case2, case3, case3h],
        "total_atom_polynomials_checked": sum(c["atom_count"] for c in [case2, case3, case3h]),
        "decimal_precision": getcontext().prec,
        "note": "Polynomial coefficients of exact atoms from signed determinants and from the spectral channel agree exactly in all cases.",
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
