#!/usr/bin/env python3
"""Independent small checks for D10-M3 analytic_channel.

This script does not import the author implementation.  It checks the exact
spectral-subset channel formulas with Fraction arithmetic and uses Decimal
logs only for entropy diagnostics.
"""

from __future__ import annotations

import json
import math
import os
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path

for _var in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_var, "1")

getcontext().prec = 90
OUT = Path(__file__).with_name("fresh_channel_audit_results.json")


def F(a: int, b: int = 1) -> Fraction:
    return Fraction(a, b)


def masks(n: int):
    return range(1 << n)


def bits(mask: int, n: int) -> list[int]:
    return [i for i in range(n) if (mask >> i) & 1]


def pop(mask: int) -> int:
    return mask.bit_count()


def det(A: list[list[Fraction]]) -> Fraction:
    n = len(A)
    if n == 0:
        return F(1)
    M = [row[:] for row in A]
    ans = F(1)
    for i in range(n):
        pivot = None
        for r in range(i, n):
            if M[r][i] != 0:
                pivot = r
                break
        if pivot is None:
            return F(0)
        if pivot != i:
            M[i], M[pivot] = M[pivot], M[i]
            ans = -ans
        pv = M[i][i]
        ans *= pv
        for r in range(i + 1, n):
            q = M[r][i] / pv
            if q:
                for c in range(i, n):
                    M[r][c] -= q * M[i][c]
    return ans


def sub(A: list[list[Fraction]], rows: list[int], cols: list[int]) -> list[list[Fraction]]:
    return [[A[i][j] for j in cols] for i in rows]


def transpose(A: list[list[Fraction]]) -> list[list[Fraction]]:
    return [list(row) for row in zip(*A)]


def matmul(A: list[list[Fraction]], B: list[list[Fraction]]) -> list[list[Fraction]]:
    n, m, r = len(A), len(B[0]), len(B)
    return [[sum(A[i][k] * B[k][j] for k in range(r)) for j in range(m)] for i in range(n)]


def diag(vals: list[Fraction]) -> list[list[Fraction]]:
    n = len(vals)
    A = [[F(0) for _ in range(n)] for __ in range(n)]
    for i, val in enumerate(vals):
        A[i][i] = val
    return A


def add_scaled(A: list[list[Fraction]], B: list[list[Fraction]], t: Fraction) -> list[list[Fraction]]:
    n = len(A)
    return [[A[i][j] + t * B[i][j] for j in range(n)] for i in range(n)]


def kernel(Q: list[list[Fraction]], vals: list[Fraction]) -> list[list[Fraction]]:
    return matmul(matmul(Q, diag(vals)), transpose(Q))


def event_matrix(K: list[list[Fraction]], S: int) -> list[list[Fraction]]:
    n = len(K)
    A = [row[:] for row in K]
    for i in range(n):
        if not ((S >> i) & 1):
            A[i][i] -= 1
    return A


def signed_atom_at(K0: list[list[Fraction]], D: list[list[Fraction]], S: int, t: Fraction) -> Fraction:
    n = len(K0)
    sign = -1 if ((n - pop(S)) & 1) else 1
    return sign * det(event_matrix(add_scaled(K0, D, t), S))


def interpolate(values: list[tuple[Fraction, Fraction]], degree: int) -> list[Fraction]:
    M = [[x**j for j in range(degree + 1)] + [y] for x, y in values[: degree + 1]]
    n = degree + 1
    for i in range(n):
        pivot = None
        for r in range(i, n):
            if M[r][i] != 0:
                pivot = r
                break
        if pivot is None:
            raise RuntimeError("singular interpolation")
        if pivot != i:
            M[i], M[pivot] = M[pivot], M[i]
        pv = M[i][i]
        M[i] = [z / pv for z in M[i]]
        for r in range(n):
            if r == i:
                continue
            q = M[r][i]
            if q:
                M[r] = [M[r][c] - q * M[i][c] for c in range(n + 1)]
    return [M[i][-1] for i in range(n)]


def signed_poly(K0: list[list[Fraction]], D: list[list[Fraction]], S: int) -> list[Fraction]:
    n = len(K0)
    return interpolate([(F(t), signed_atom_at(K0, D, S, F(t))) for t in range(n + 1)], n)


def channel_weight(Q: list[list[Fraction]], S: int, R: int) -> Fraction:
    n = len(Q)
    if pop(S) != pop(R):
        return F(0)
    rows = bits(S, n)
    cols = bits(R, n)
    return det(sub(Q, rows, cols)) ** 2


def mu_derivatives(lam: list[Fraction], v: list[Fraction], R: int) -> tuple[Fraction, Fraction, Fraction]:
    n = len(lam)
    mu = F(1)
    scores = []
    for i in range(n):
        if (R >> i) & 1:
            mu *= lam[i]
            scores.append(v[i] / lam[i])
        else:
            mu *= 1 - lam[i]
            scores.append(-v[i] / (1 - lam[i]))
    a = sum(scores, F(0))
    b = F(0)
    for i in range(n):
        for j in range(i + 1, n):
            b += 2 * scores[i] * scores[j]
    return mu, mu * a, mu * b


def all_channel_derivatives(Q: list[list[Fraction]], lam: list[Fraction], v: list[Fraction]):
    n = len(lam)
    p0 = [F(0) for _ in masks(n)]
    p1 = [F(0) for _ in masks(n)]
    p2 = [F(0) for _ in masks(n)]
    for S in masks(n):
        for R in masks(n):
            T = channel_weight(Q, S, R)
            if T == 0:
                continue
            m0, m1, m2 = mu_derivatives(lam, v, R)
            p0[S] += T * m0
            p1[S] += T * m1
            p2[S] += T * m2
    return p0, p1, p2


def signed_derivatives(Q: list[list[Fraction]], lam: list[Fraction], v: list[Fraction]):
    n = len(lam)
    K0 = kernel(Q, lam)
    D = kernel(Q, v)
    p0, p1, p2 = [], [], []
    for S in masks(n):
        poly = signed_poly(K0, D, S)
        p0.append(poly[0])
        p1.append(poly[1] if len(poly) > 1 else F(0))
        p2.append(2 * poly[2] if len(poly) > 2 else F(0))
    return p0, p1, p2


def D(x: Fraction) -> Decimal:
    return Decimal(x.numerator) / Decimal(x.denominator)


def dlog(x: Fraction) -> Decimal:
    return D(x).ln()


def entropy(p: list[Fraction]) -> Decimal:
    ans = Decimal(0)
    for x in p:
        if x:
            ans -= D(x) * dlog(x)
    return +ans


def entropy_second(p0: list[Fraction], p1: list[Fraction], p2: list[Fraction]) -> Decimal:
    ans = Decimal(0)
    for a, b, c in zip(p0, p1, p2):
        ans += -(D(b) * D(b) / D(a)) - D(c) * dlog(a)
    return +ans


def by_cardinality(vals: list[Fraction], n: int) -> list[Fraction]:
    out = [F(0) for _ in range(n + 1)]
    for S, val in enumerate(vals):
        out[pop(S)] += val
    return out


def conditional_entropy_by_count(p: list[Fraction], n: int) -> Decimal:
    pi = by_cardinality(p, n)
    ans = Decimal(0)
    for k in range(n + 1):
        if pi[k] == 0:
            continue
        hk = Decimal(0)
        for S, val in enumerate(p):
            if pop(S) == k and val:
                q = val / pi[k]
                hk -= D(q) * dlog(q)
        ans += D(pi[k]) * hk
    return +ans


def entropy_report(Q: list[list[Fraction]], lam: list[Fraction], v: list[Fraction]) -> dict:
    n = len(lam)
    cp0, cp1, cp2 = all_channel_derivatives(Q, lam, v)
    sp0, sp1, sp2 = signed_derivatives(Q, lam, v)
    max_diff = max(
        abs(a - b)
        for left, right in ((cp0, sp0), (cp1, sp1), (cp2, sp2))
        for a, b in zip(left, right)
    )
    pi0 = by_cardinality(cp0, n)
    pi1 = by_cardinality(cp1, n)
    pi2 = by_cardinality(cp2, n)
    HY = entropy(cp0)
    HN = entropy(pi0)
    Hcond_direct = conditional_entropy_by_count(cp0, n)
    HY2 = entropy_second(cp0, cp1, cp2)
    HN2 = entropy_second(pi0, pi1, pi2)
    psi2_by_difference = HY2 - HN2
    psi2_formula = HY2 + sum((D(pi1[k]) * D(pi1[k]) / D(pi0[k])) + D(pi2[k]) * dlog(pi0[k]) for k in range(n + 1))
    return {
        "n": n,
        "max_signed_vs_channel_derivative_diff": str(max_diff),
        "sum_p": str(sum(cp0)),
        "sum_p_prime": str(sum(cp1)),
        "sum_p_second": str(sum(cp2)),
        "min_atom": str(min(cp0)),
        "H_Y": str(HY),
        "H_count": str(HN),
        "H_conditional_direct": str(Hcond_direct),
        "H_split_residual_decimal": str(+(HY - HN - Hcond_direct)),
        "H2_Y": str(HY2),
        "H2_count": str(HN2),
        "Psi2_by_difference": str(+psi2_by_difference),
        "Psi2_formula": str(+psi2_formula),
        "Psi2_residual_decimal": str(+(psi2_by_difference - psi2_formula)),
    }


def poisson_binomial_derivatives(lam: list[Fraction], v: list[Fraction]):
    n = len(lam)
    pi0 = [F(0) for _ in range(n + 1)]
    pi1 = [F(0) for _ in range(n + 1)]
    pi2 = [F(0) for _ in range(n + 1)]
    for R in masks(n):
        m0, m1, m2 = mu_derivatives(lam, v, R)
        k = pop(R)
        pi0[k] += m0
        pi1[k] += m1
        pi2[k] += m2
    return pi0, pi1, pi2


def expected_layer_constant_second(lam: list[Fraction], v: list[Fraction], c: list[Decimal]) -> Decimal:
    _, _, pi2 = poisson_binomial_derivatives(lam, v)
    return +sum(D(pi2[k]) * c[k] for k in range(len(c)))


def cardinality_uniform_sanity() -> dict:
    n = 4
    lam = [F(1, 5), F(2, 7), F(3, 8), F(5, 9)]
    v_pos = [F(1, 31), F(2, 37), F(1, 41), F(3, 43)]
    c = [Decimal(math.log(math.comb(n, k))) for k in range(n + 1)]
    pi0, pi1, pi2 = poisson_binomial_derivatives(lam, v_pos)
    HN2 = entropy_second(pi0, pi1, pi2)
    Ec2 = expected_layer_constant_second(lam, v_pos, c)
    return {
        "n": n,
        "lambda": [str(x) for x in lam],
        "v_same_sign": [str(x) for x in v_pos],
        "H_count_second": str(HN2),
        "E_log_binom_second": str(Ec2),
        "total_second": str(+(HN2 + Ec2)),
        "note": "Finite sanity for the theorem proof: same-sign rates and c_k=log binomial layer constants give nonpositive second derivative in this case.",
    }


def direct_sum_sanity() -> dict:
    Q2 = [[F(3, 5), -F(4, 5)], [F(4, 5), F(3, 5)]]
    Q = [
        [Q2[0][0], Q2[0][1], F(0)],
        [Q2[1][0], Q2[1][1], F(0)],
        [F(0), F(0), F(1)],
    ]
    lam = [F(2, 7), F(5, 11), F(3, 8)]
    v = [F(1, 13), F(2, 17), F(1, 19)]
    full = entropy_report(Q, lam, v)
    block2 = entropy_report(Q2, lam[:2], v[:2])
    Q1 = [[F(1)]]
    block1 = entropy_report(Q1, [lam[2]], [v[2]])
    block_sum_H2 = Decimal(block2["H2_Y"]) + Decimal(block1["H2_Y"])
    return {
        "full_H2": full["H2_Y"],
        "block2_H2": block2["H2_Y"],
        "block1_H2": block1["H2_Y"],
        "block_sum_H2": str(+block_sum_H2),
        "full_minus_block_sum_decimal": str(+(Decimal(full["H2_Y"]) - block_sum_H2)),
        "full_min_atom": full["min_atom"],
        "note": "Block diagonal K gives product exact atoms; Decimal residual is log-rounding only.",
    }


def generic_blocker_sanity() -> dict:
    # Rational Householder orthogonal matrix Q = I - ww^T/7, w=(1,2,3).
    Q = [
        [F(6, 7), F(-2, 7), F(-3, 7)],
        [F(-2, 7), F(3, 7), F(-6, 7)],
        [F(-3, 7), F(-6, 7), F(-2, 7)],
    ]
    lam = [F(3, 4), F(1, 2), F(1, 2)]
    v = [F(1, 100), F(1), F(1)]
    p0, p1, p2 = all_channel_derivatives(Q, lam, v)
    singleton_p2 = {format(1 << i, "03b"): str(p2[1 << i]) for i in range(3)}
    singleton_p2_float = {format(1 << i, "03b"): float(p2[1 << i]) for i in range(3)}
    return {
        "Q": "Householder I - (1/7)(1,2,3)(1,2,3)^T",
        "lambda": [str(x) for x in lam],
        "v": [str(x) for x in v],
        "singleton_atom_second_derivatives": singleton_p2,
        "singleton_atom_second_derivatives_float": singleton_p2_float,
        "sum_singleton_p2": str(sum(p2[1 << i] for i in range(3))),
        "note": "This is not a positive-entropy candidate; it shows generic fixed-Q layer accelerations are sign-indefinite, so doubly stochasticity alone is not a curvature certificate.",
    }


def main() -> int:
    Q_house = [
        [F(6, 7), F(-2, 7), F(-3, 7)],
        [F(-2, 7), F(3, 7), F(-6, 7)],
        [F(-3, 7), F(-6, 7), F(-2, 7)],
    ]
    generic = entropy_report(Q_house, [F(3, 7), F(2, 5), F(5, 8)], [F(1, 11), F(2, 13), F(3, 17)])
    results = {
        "status": "FRESH_CHANNEL_AUDIT_SANITY_PASSED",
        "exact_mixture_derivative_case": generic,
        "cardinality_uniform_sufficient_condition_sanity": cardinality_uniform_sanity(),
        "direct_sum_sanity": direct_sum_sanity(),
        "generic_Q_blocker_sanity": generic_blocker_sanity(),
        "decimal_precision": getcontext().prec,
    }
    OUT.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(results, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
