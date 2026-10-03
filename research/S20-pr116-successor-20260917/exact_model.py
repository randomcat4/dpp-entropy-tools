#!/usr/bin/env python3
"""Exact complete-event model for the PR116 natural 3+3 family.

Python standard library only. Finite-point checks are NOT a continuum proof.
The complete law is reconstructed from 64 signed 6-by-6 determinants, rather
than imported from any table. A diagonal similarity removes
sqrt(alpha(1-alpha)) without changing any complete-event determinant.
"""
from __future__ import annotations

import argparse
import json
from fractions import Fraction as F
from pathlib import Path
from typing import Sequence

Triple = tuple[F, F, F]


def determinant(matrix: Sequence[Sequence[F]]) -> F:
    """Gaussian elimination over the rationals, including row pivoting."""
    a = [[F(x) for x in row] for row in matrix]
    n = len(a)
    if any(len(row) != n for row in a):
        raise ValueError("A square matrix is required")
    result = F(1)
    for k in range(n):
        pivot = next((i for i in range(k, n) if a[i][k]), None)
        if pivot is None:
            return F(0)
        if pivot != k:
            a[pivot], a[k] = a[k], a[pivot]
            result = -result
        value = a[k][k]
        result *= value
        for i in range(k + 1, n):
            factor = a[i][k] / value
            if factor:
                for j in range(k + 1, n):
                    a[i][j] -= factor * a[k][j]
            a[i][k] = F(0)
    return result


def similar_kernel(alpha: F, beta: F, t: F) -> list[list[F]]:
    alpha, beta, t = F(alpha), F(beta), F(t)
    if not (0 < alpha < 1 and 0 < beta < 1):
        raise ValueError("Require 0 < alpha,beta < 1")
    r = alpha * (1 - alpha)
    p = [[F(i == j) - F(1, 3) for j in range(3)] for i in range(3)]
    a = [[alpha * p[i][j] + beta / 3 for j in range(3)] for i in range(3)]
    # D^{-1} K D, with D=diag(I_3,sqrt(r) I_3).
    k = [[F(0) for _ in range(6)] for _ in range(6)]
    for i in range(3):
        for j in range(3):
            k[i][j] = a[i][j]
            k[i][j + 3] = t * r * p[i][j]
            k[i + 3][j] = t * p[i][j]
            k[i + 3][j + 3] = F(i == j) - a[i][j]
    return k


def complete_law(alpha: F, beta: F, t: F) -> list[F]:
    k = similar_kernel(alpha, beta, t)
    values: list[F] = []
    for event in range(64):
        # Occupied rows come from K; unoccupied rows come from I-K.
        matrix = [
            [k[i][j] if event & (1 << i) else F(i == j) - k[i][j]
             for j in range(6)]
            for i in range(6)
        ]
        values.append(determinant(matrix))
    return values


def coefficients(alpha: F, beta: F) -> list[Triple]:
    """Recover p_E(s)=c0+c1*s+c2*s^2 from s=0,1,4 exactly.

    The evaluation at t=2 is polynomial interpolation only, not a physical law.
    The rank-two off-diagonal block bounds the degree in s by two.
    """
    p0, p1, p4 = (complete_law(alpha, beta, F(t)) for t in (0, 1, 2))
    out: list[Triple] = []
    for m, x, y in zip(p0, p1, p4):
        c2 = (y - 4 * x + 3 * m) / 12
        c1 = x - m - c2
        out.append((m, c1, c2))
    assert all(row[0] > 0 for row in out), "Nonpositive decoupled atom"
    assert tuple(sum(row[i] for row in out) for i in range(3)) == (1, 0, 0)
    left: list[Triple] = []
    right: list[Triple] = []
    for mask in range(8):
        left.append(tuple(sum(out[mask + 8 * other][i] for other in range(8))
                          for i in range(3)))
        right.append(tuple(sum(out[other + 8 * mask][i] for other in range(8))
                           for i in range(3)))
    assert all(c1 == 0 and c2 == 0 for _, c1, c2 in left + right)
    assert all(out[l + 8 * rr][0] == left[l][0] * right[rr][0]
               for l in range(8) for rr in range(8))
    # An extra rational t binds interpolation to the determinant source.
    direct = complete_law(alpha, beta, F(1, 2))
    assert direct == [m + c1 / 4 + c2 / 16 for m, c1, c2 in out]
    return out


def joint_kernel(rows: Sequence[Triple], s: F, u: F) -> F:
    s, u = F(s), F(u)
    if not (0 <= s < 1 and 0 <= u <= 1):
        raise ValueError("Require 0 <= s < 1 and 0 <= u <= 1")
    result = F(0)
    for m, c1, c2 in rows:
        a, b = -c1 / m, c2 / m
        q = 1 - a * s + b * s * s
        d = 1 - u + u * q
        if q <= 0 or d <= 0:
            raise ArithmeticError("A strict physical denominator is not positive")
        v = a - 2 * s * b
        z = (a - s * b) * (a - 6 * s * b)
        result += m * (4 * v * v / (d * d) + 2 * z / d)
    return result


def run_checks() -> dict:
    parameters = [(F(1, 10), F(1, 3)), (F(1, 2), F(1, 2)),
                  (F(1, 10), F(1, 10)), (F(1, 10), F(9, 10)),
                  (F(1, 3), F(2, 3))]
    samples = []
    for alpha, beta in parameters:
        rows = coefficients(alpha, beta)
        reserve = 64 * (alpha * (1 - alpha)) ** 2
        for s in (F(0), F(1, 4), F(3, 4), F(99, 100)):
            for u in (F(0), F(1, 2), F(1)):
                value = joint_kernel(rows, s, u)
                samples.append({"alpha": str(alpha), "beta": str(beta),
                                "s": str(s), "u": str(u), "J": str(value),
                                "J_minus_64r2": str(value - reserve)})
    center = coefficients(F(1, 2), F(1, 2))
    center_value = joint_kernel(center, F(0), F(0))
    assert center_value == 4, "The claimed sharpness value did not reproduce"
    negative = [r for r in samples if F(r["J_minus_64r2"]) < 0]
    return {
        "status": "FINITE_EXACT_CHECKS_ONLY_NOT_CONTINUUM_CERTIFICATE",
        "complete_events_per_parameter": 64,
        "parameter_pairs": len(parameters),
        "sample_points": len(samples),
        "normalization_fixed_marginals_product_law_and_interpolation": "PASS",
        "center_Gamma_at_s0": str(center_value),
        "center_Gamma_divided_by_r2": str(center_value / F(1, 16)),
        "negative_sample_reserves": len(negative),
        "samples": samples,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Optional exact JSON report")
    args = parser.parse_args()
    report = run_checks()
    text = json.dumps(report, indent=2) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "samples"}, indent=2))
    return 0 if report["negative_sample_reserves"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
