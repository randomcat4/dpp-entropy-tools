#!/usr/bin/env python3
"""Independent bounded reconstruction of the finite PR116 arithmetic units."""

from decimal import Decimal
from fractions import Fraction as F
from itertools import product
import json

import sympy as sp


def rational(value):
    value = sp.cancel(value)
    return F(int(sp.numer(value)), int(sp.denom(value)))


def matrices(alpha, beta):
    Q = sp.ones(3) / 3
    P = sp.eye(3) - Q
    A = alpha * P + beta * Q
    return A, sp.eye(3) - A


def signed_event(matrix, mask):
    shifted = matrix.copy()
    for i in range(matrix.rows):
        if not (mask & (1 << i)):
            shifted[i, i] -= 1
    return sp.factor((-1) ** (matrix.rows - mask.bit_count()) * shifted.det(method="domain-ge"))


def symbolic_types(alpha_value=sp.Rational(1, 10)):
    """Rebuild all 64 coefficient triples and merge only identical (a,b)."""
    alpha = alpha_value
    beta = sp.symbols("beta")
    A, C = matrices(alpha, beta)
    E = sp.Matrix([[1, 0], [0, 1], [-1, -1]])
    GI = sp.Matrix([[sp.Rational(2, 3), -sp.Rational(1, 3)],
                    [-sp.Rational(1, 3), sp.Rational(2, 3)]])
    left, right = {}, {}
    for mask in range(8):
        SA = A.copy()
        SC = C.copy()
        for i in range(3):
            if not (mask & (1 << i)):
                SA[i, i] -= 1
                SC[i, i] -= 1
        left[mask] = (signed_event(A, mask), sp.simplify(E.T * SA.inv() * E))
        right[mask] = (signed_event(C, mask), sp.simplify(GI * E.T * SC.inv() * E * GI))

    rho2 = alpha * (1 - alpha)
    rows = []
    groups = {}
    for lm, rm in product(range(8), repeat=2):
        mu = sp.factor(left[lm][0] * right[rm][0])
        product_matrix = sp.simplify(left[lm][1] * right[rm][1])
        a = sp.factor(rho2 * sp.trace(product_matrix))
        b = sp.factor(rho2**2 * left[lm][1].det() * right[rm][1].det())
        rows.append((mu, a, b))
        key = (sp.cancel(a), sp.cancel(b))
        old_weight, old_count = groups.get(key, (sp.Integer(0), 0))
        groups[key] = (sp.factor(old_weight + mu), old_count + 1)
    assert len(rows) == 64 and len(groups) == 13
    assert sp.factor(sum(mu for mu, _, _ in rows) - 1) == 0
    assert sp.factor(sum(mu * a for mu, a, _ in rows)) == 0
    assert sp.factor(sum(mu * b for mu, _, b in rows)) == 0
    return beta, rows, groups


def merge_at(groups, beta, value):
    merged = {}
    for (a, b), (weight, count) in groups.items():
        key = (sp.factor(a.subs(beta, value)), sp.factor(b.subs(beta, value)))
        w = sp.factor(weight.subs(beta, value))
        previous = merged.get(key, (sp.Integer(0), 0))
        merged[key] = (sp.factor(previous[0] + w), previous[1] + count)
    return merged


def log_interval(value, terms=60):
    value = F(value)
    exponent = 0
    while value < 1:
        value *= 2
        exponent -= 1
    while value >= 2:
        value /= 2
        exponent += 1

    def unit(x):
        z = (x - 1) / (x + 1)
        partial = 2 * sum((z ** (2 * j + 1) / (2 * j + 1) for j in range(terms)), F(0))
        tail = 2 * z ** (2 * terms + 1) / ((2 * terms + 1) * (1 - z * z))
        return partial, partial + tail

    lo, hi = unit(value)
    l2, u2 = unit(F(2))
    return ((lo + exponent * l2, hi + exponent * u2) if exponent >= 0
            else (lo + exponent * u2, hi + exponent * l2))


def scale_interval(interval, scalar):
    scalar = F(scalar)
    return ((scalar * interval[0], scalar * interval[1]) if scalar >= 0
            else (scalar * interval[1], scalar * interval[0]))


def convolution(left, right):
    answer = {}
    for (i, j), x in left.items():
        for (k, l), y in right.items():
            answer[i + k, j + l] = answer.get((i + k, j + l), F(0)) + x * y
    return answer


def cardinality_formula(alpha, beta, s):
    r = alpha * (1 - alpha)
    delta = 1 - s
    g = {(0, 0): (1 - alpha)**2 + r * s,
         (1, 0): r * delta, (0, 1): r * delta,
         (1, 1): alpha**2 + r * s}
    h = {(0, 0): (1 - beta)**2, (1, 0): beta * (1 - beta),
         (0, 1): beta * (1 - beta), (1, 1): beta**2}
    return convolution(convolution(g, g), h)


def cardinality_point(alpha, beta, t):
    alpha, beta, t = map(F, (alpha, beta, t))
    root_r = F(3, 10) if alpha == F(1, 10) else F(2, 5)
    Qm = [[F(1, 3)] * 3 for _ in range(3)]
    Pm = [[F(i == j) - Qm[i][j] for j in range(3)] for i in range(3)]
    A = [[alpha * Pm[i][j] + beta * Qm[i][j] for j in range(3)] for i in range(3)]
    C = [[F(i == j) - A[i][j] for j in range(3)] for i in range(3)]
    B = [[root_r * Pm[i][j] for j in range(3)] for i in range(3)]
    K = sp.Matrix(A).row_join(t * sp.Matrix(B)).col_join((t * sp.Matrix(B)).T.row_join(sp.Matrix(C)))

    direct = {(k, l): F(0) for k in range(4) for l in range(4)}
    channel = {(k, l): {"equal": [], "unequal": []} for k in (1, 2) for l in (1, 2)}
    for left_mask, y_mask in product(range(8), repeat=2):
        right_mask = 7 ^ y_mask
        probability = rational(signed_event(K, left_mask | (right_mask << 3)))
        k, l = left_mask.bit_count(), y_mask.bit_count()
        direct[k, l] += probability
        if k in (1, 2) and l in (1, 2):
            label_left = ((left_mask & -left_mask).bit_length() - 1 if k == 1
                          else (((7 ^ left_mask) & -(7 ^ left_mask)).bit_length() - 1))
            label_right = ((y_mask & -y_mask).bit_length() - 1 if l == 1
                           else (((7 ^ y_mask) & -(7 ^ y_mask)).bit_length() - 1))
            channel[k, l]["equal" if label_left == label_right else "unequal"].append(probability)

    formula = cardinality_formula(alpha, beta, t * t)
    assert direct == formula
    pi = [(1 - alpha)**2 * (1 - beta),
          (1 - alpha) * (2 * alpha * (1 - beta) + (1 - alpha) * beta),
          alpha * (alpha * (1 - beta) + 2 * (1 - alpha) * beta),
          alpha**2 * beta]
    assert all(sum(direct[k, l] for l in range(4)) == pi[k] for k in range(4))
    L = 2 * alpha + beta - 3 * alpha * beta
    N = alpha + 2 * beta - 3 * alpha * beta
    expected_differences = {(1, 1): 3 * t*t * alpha * (1-alpha) * (1-beta)**2 / ((1-alpha)**2 * L**2),
                            (2, 2): 3 * t*t * alpha * (1-alpha) * beta**2 / (alpha**2 * N**2),
                            (1, 2): -3 * t*t * beta * (1-beta) / (L * N),
                            (2, 1): -3 * t*t * beta * (1-beta) / (L * N)}
    for key, buckets in channel.items():
        assert len(set(buckets["equal"])) == 1 and len(set(buckets["unequal"])) == 1
        q_equal = 9 * buckets["equal"][0] / (pi[key[0]] * pi[key[1]])
        q_unequal = 9 * buckets["unequal"][0] / (pi[key[0]] * pi[key[1]])
        qbar = direct[key] / (pi[key[0]] * pi[key[1]])
        assert qbar == (q_equal + 2 * q_unequal) / 3
        assert q_equal - q_unequal == expected_differences[key]
    return {"alpha": str(alpha), "beta": str(beta), "s": str(t*t), "cells": 16, "channel_formulas": 4}


def endpoint_identities():
    alpha, beta = sp.symbols("alpha beta")
    r, B0, d = alpha * (1 - alpha), beta * (1 - beta), beta - alpha
    L, N = 2 * alpha + beta - 3 * alpha * beta, alpha + 2 * beta - 3 * alpha * beta
    WH = 2 * alpha**2 * (1 - alpha) * beta * L
    WL = 2 * alpha * (1 - alpha)**2 * (1 - beta) * N
    WM = sp.Rational(2, 3) * r * L * N
    WD = 2 * r**2 * B0
    kH, kL, kM = 2 * (1 - beta) / L, 2 * beta / N, 2 * (r + d**2) / (L * N)
    CA = sp.factor(2 * (WH * (5*kH - 4) + WL * (5*kL - 4) + WM * (5*kM - 4)) - 16 * WD)
    x, y = 2 * alpha - 1, 2 * beta - 1
    expected_CA = r * (7 + x**2 - 7*y**2 - 4*x*y + 3*x**2*y**2) / 3
    CF = sp.factor(4 * (WH*kH + WL*kL + WM*kM))
    expected_CF = sp.Rational(16, 3) * r * (3*B0 + r + d**2)
    expected_slice = -sp.Rational(3, 625) * (127*beta**2 - 167*beta + 4)
    assert sp.factor(CA - expected_CA) == 0
    assert sp.factor(CF - expected_CF) == 0
    assert sp.factor(CA.subs(alpha, sp.Rational(1, 10)) - expected_slice) == 0
    return {"C_A_identity": True, "C_F_identity": True, "alpha_1_over_10_slice": True,
            "frozen_checker_structural_equality_defect": sp.factor(CA.subs(alpha, sp.Rational(1, 10))) != expected_slice}


def main():
    beta, rows, groups = symbolic_types()

    exchangeable = merge_at(groups, beta, sp.Rational(1, 3))
    assert len(exchangeable) == 11 and sum(count for _, count in exchangeable.values()) == 64
    assert sp.factor(sum(weight for weight, _ in exchangeable.values()) - 1) == 0
    def weight(a, b):
        return exchangeable[(sp.Rational(a), sp.Rational(b))][0]
    reserve = sp.factor(2 * weight(1, 0) - 16 * weight(2, 1)
                        - 2 * weight(-sp.Rational(14, 13), -sp.Rational(27, 13)) * sp.Rational(1225, 1014)
                        - 2 * weight(sp.Rational(302, 1521), sp.Rational(9, 169)) * sp.Rational(3128, 177957))
    assert reserve == sp.Rational(195191, 1755000) > 0

    # Exact negative rational-kernel point from the independently rebuilt types.
    beta0, s0, u0 = sp.Rational(999, 1000), sp.Rational(999, 1000), sp.Integer(1)
    R = sp.Integer(0)
    fisher = sp.Integer(0)
    acceleration = (F(0), F(0))
    for (a_expr, b_expr), (weight_expr, _) in groups.items():
        a = sp.factor(a_expr.subs(beta, beta0)); b = sp.factor(b_expr.subs(beta, beta0)); weight0 = sp.factor(weight_expr.subs(beta, beta0))
        q = sp.factor(1 - a*s0 + b*s0**2)
        z = sp.factor((a - s0*b) * (a - 6*s0*b))
        v = sp.factor(a - 2*s0*b)
        R += weight0 * z / (1 + u0*(q - 1))
        fisher += 4 * weight0 * v*v/q
        qf = rational(q)
        if q == 1:
            interval = (rational(2 * weight0 * z),) * 2
        else:
            coeff = rational(2 * weight0 * z / (q - 1))
            interval = scale_interval(log_interval(qf), coeff)
        acceleration = acceleration[0] + interval[0], acceleration[1] + interval[1]
    R = sp.factor(R); fisher = sp.factor(fisher)
    expected_R = sp.Rational(-4652511275248641251547259673277396396430560770738995603060156315177013829721844617061387219436351135945723000000,
                             234641869065463647119872803882392585968204540713314205480817507948342686413506474822091990896200409106815549)
    assert R == expected_R < 0
    assert F(Decimal("6.9381648836224339")) < acceleration[0] <= acceleration[1] < F(Decimal("6.9381648836224341"))
    assert fisher > 0 and rational(fisher) + acceleration[0] > 0

    cardinality = [cardinality_point(F(1, 10), F(2, 7), F(1, 2)),
                   cardinality_point(F(1, 5), F(3, 11), F(3, 4))]
    endpoints = endpoint_identities()
    result = {
        "status": "PASS_LIGHT_WITH_FROZEN_ENDPOINT_CHECKER_DEFECT",
        "head": "3f276c09fe4da3aded2ab6cf457adb7fdc4254d8",
        "exchangeable_events": 64,
        "exchangeable_types": len(exchangeable),
        "acceleration_reserve": str(reserve),
        "generic_types": len(groups),
        "negative_point": {"R_exact_negative": True, "R_decimal": float(R),
                           "A_norm_interval_decimal": [float(acceleration[0]), float(acceleration[1])],
                           "F_norm_decimal": float(fisher), "Gamma_positive": True},
        "cardinality_label_points": cardinality,
        "endpoint_phase": endpoints,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
