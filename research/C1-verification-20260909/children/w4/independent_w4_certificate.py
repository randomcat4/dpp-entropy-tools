#!/usr/bin/env python3
from __future__ import annotations

from fractions import Fraction as F
from pathlib import Path
import json
import math
import os
import platform
import sys

import mpmath as mp
import numpy as np
import sympy as sp


EVENTS = ["0", "1", "2", "12", "3", "13", "23", "123"]
BITS = {
    "0": (0, 0, 0),
    "1": (1, 0, 0),
    "2": (0, 1, 0),
    "12": (1, 1, 0),
    "3": (0, 0, 1),
    "13": (1, 0, 1),
    "23": (0, 1, 1),
    "123": (1, 1, 1),
}


def frac_brief(q: F):
    return {
        "positive": q > 0,
        "approx": format(float(q), ".17g") if q else "0",
        "numerator_bits": q.numerator.bit_length(),
        "denominator_bits": q.denominator.bit_length(),
    }


def ff(q) -> F:
    q = sp.Rational(q)
    return F(int(q.p), int(q.q))


def iv_add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def iv_sub(a, b):
    return (a[0] - b[1], a[1] - b[0])


def iv_scale(k, a):
    k = F(k)
    if k >= 0:
        return (k * a[0], k * a[1])
    return (k * a[1], k * a[0])


def iv_mul(a, b):
    vals = [a[0] * b[0], a[0] * b[1], a[1] * b[0], a[1] * b[1]]
    return (min(vals), max(vals))


def iv_square(a):
    lo, hi = a
    if lo <= 0 <= hi:
        return (F(0), max(lo * lo, hi * hi))
    vals = [lo * lo, hi * hi]
    return (min(vals), max(vals))


def iv_div_pos(a, b):
    assert b[0] > 0
    return iv_mul(a, (F(1, 1) / b[1], F(1, 1) / b[0]))


def iv_width(a) -> F:
    return a[1] - a[0]


def log_unit_interval(q: F, n: int):
    assert F(1, 1) <= q <= F(2, 1)
    u = (q - 1) / (q + 1)
    total = F(0)
    for j in range(n):
        total += 2 * u ** (2 * j + 1) / (2 * j + 1)
    tail = 2 * u ** (2 * n + 1) / ((2 * n + 1) * (1 - u * u))
    return (total, total + tail)


def log_interval(q: F, n: int):
    if q <= 0:
        raise ValueError("log argument must be positive")
    k = 0
    z = q
    while z >= 2:
        z /= 2
        k += 1
    while z < 1:
        z *= 2
        k -= 1
    out = log_unit_interval(z, n)
    if k:
        out = iv_add(out, iv_scale(k, log_unit_interval(F(2, 1), n)))
    return out


def iv_mid_float(a):
    return float((a[0] + a[1]) / 2)


def interval_ldl_positive(A):
    n = len(A)
    L = [[(F(0), F(0)) for _ in range(n)] for __ in range(n)]
    D = [(F(0), F(0)) for _ in range(n)]
    pivots = []
    for k in range(n):
        accum = (F(0), F(0))
        for j in range(k):
            accum = iv_add(accum, iv_mul(iv_square(L[k][j]), D[j]))
        dk = iv_sub(A[k][k], accum)
        pivots.append(dk)
        if dk[0] <= 0:
            return False, pivots
        D[k] = dk
        L[k][k] = (F(1), F(1))
        for i in range(k + 1, n):
            num = A[i][k]
            for j in range(k):
                num = iv_sub(num, iv_mul(iv_mul(L[i][j], L[k][j]), D[j]))
            L[i][k] = iv_div_pos(num, dk)
    return True, pivots


x, y, z, a, b, c = coords = sp.symbols("x y z a b c", real=True)
d1, d2, d3, h12, h13, h23 = dirs = sp.symbols(
    "d1 d2 d3 h12 h13 h23", real=True
)

q12 = x * y - a * a
q13 = x * z - b * b
q23 = y * z - c * c
r = x * y * z + 2 * a * b * c - x * c * c - y * b * b - z * a * a
ps = sp.Matrix(
    [
        1 - x - y - z + q12 + q13 + q23 - r,
        x - q12 - q13 + r,
        y - q12 - q23 + r,
        q12 - r,
        z - q13 - q23 + r,
        q13 - r,
        q23 - r,
        r,
    ]
)


def directional_derivative(expr):
    return sum(sp.diff(expr, u) * v for u, v in zip(coords, dirs))


p1 = ps.applyfunc(directional_derivative)
p2 = p1.applyfunc(directional_derivative)
J = ps.jacobian(coords)
Hp = [sp.hessian(p, coords) for p in ps]


def product_prob(bits):
    xs = [x, y, z]
    out = sp.Integer(1)
    for bit, xi in zip(bits, xs):
        out *= xi if bit else (1 - xi)
    return out


def event_s(bits):
    xs = [x, y, z]
    return [sp.Integer(bit) - xi for bit, xi in zip(bits, xs)]


def symbolic_identity_checks():
    checks = []
    checks.append(("mass", sp.expand(sum(ps) - 1) == 0))
    checks.append(("mass_prime", sp.expand(sum(p1)) == 0))
    checks.append(("mass_double_prime", sp.expand(sum(p2)) == 0))

    v1, v2, v3 = x * (1 - x), y * (1 - y), z * (1 - z)
    V0 = v1 * v2 * v3
    for idx, label in enumerate(EVENTS):
        s1, s2, s3 = event_s(BITS[label])
        p0 = product_prob(BITS[label])
        R = (
            1
            - a * a * s1 * s2 / (v1 * v2)
            - b * b * s1 * s3 / (v1 * v3)
            - c * c * s2 * s3 / (v2 * v3)
            + 2 * a * b * c * s1 * s2 * s3 / V0
        )
        g = (
            d1 * s1 / v1
            + d2 * s2 / v2
            + d3 * s3 / v3
            - 2 * a * h12 * s1 * s2 / (v1 * v2)
            - 2 * b * h13 * s1 * s3 / (v1 * v3)
            - 2 * c * h23 * s2 * s3 / (v2 * v3)
            + (
                2 * (h12 * b * c + a * h13 * c + a * b * h23)
                - d1 * c * c
                - d2 * b * b
                - d3 * a * a
            )
            * s1
            * s2
            * s3
            / V0
        )
        h = (
            2 * (d1 * d2 - h12 * h12) * s1 * s2 / (v1 * v2)
            + 2 * (d1 * d3 - h13 * h13) * s1 * s3 / (v1 * v3)
            + 2 * (d2 * d3 - h23 * h23) * s2 * s3 / (v2 * v3)
            + 4
            * (
                c * h12 * h13
                + b * h12 * h23
                + a * h13 * h23
                - a * h12 * d3
                - b * h13 * d2
                - c * h23 * d1
            )
            * s1
            * s2
            * s3
            / V0
        )
        checks.append((f"R_{label}", sp.cancel(p0 * R - ps[idx]) == 0))
        checks.append((f"g_{label}", sp.cancel(p0 * g - p1[idx]) == 0))
        checks.append((f"h_{label}", sp.cancel(p0 * h - p2[idx]) == 0))

    e12, e13, e23, s1, s2, s3 = sp.symbols("e12 e13 e23 s1 s2 s3", real=True)
    Rn = (
        1
        - e12 * e12 * s1 * s2
        - e13 * e13 * s1 * s3
        - e23 * e23 * s2 * s3
        + 2 * e12 * e13 * e23 * s1 * s2 * s3
    )
    ray_checks = [
        (
            "ray_12",
            sp.expand(
                sp.diff(Rn, s1) * sp.diff(Rn, s2)
                - Rn * sp.diff(Rn, s1, s2)
                - (e12 - e13 * e23 * s3) ** 2
            )
            == 0,
        ),
        (
            "ray_13",
            sp.expand(
                sp.diff(Rn, s1) * sp.diff(Rn, s3)
                - Rn * sp.diff(Rn, s1, s3)
                - (e13 - e12 * e23 * s2) ** 2
            )
            == 0,
        ),
        (
            "ray_23",
            sp.expand(
                sp.diff(Rn, s2) * sp.diff(Rn, s3)
                - Rn * sp.diff(Rn, s2, s3)
                - (e23 - e12 * e13 * s1) ** 2
            )
            == 0,
        ),
    ]
    checks.extend(ray_checks)

    f0, f1, f2, f12, f3, f13, f23, f123 = fs = sp.symbols(
        "f0 f1 f2 f12 f3 f13 f23 f123", real=True
    )
    f_by_label = dict(zip(EVENTS, fs))
    delta12_0 = f12 - f2 - f1 + f0
    delta12_1 = f123 - f23 - f13 + f3
    delta13_0 = f13 - f3 - f1 + f0
    delta13_1 = f123 - f23 - f12 + f2
    delta23_0 = f23 - f3 - f2 + f0
    delta23_1 = f123 - f13 - f12 + f1
    bar12 = (1 - z) * delta12_0 + z * delta12_1
    bar13 = (1 - y) * delta13_0 + y * delta13_1
    bar23 = (1 - x) * delta23_0 + x * delta23_1
    lam = f123 - f23 - f13 - f12 + f3 + f2 + f1 - f0
    W = (
        c * h12 * h13
        + b * h12 * h23
        + a * h13 * h23
        - a * h12 * d3
        - b * h13 * d2
        - c * h23 * d1
    )
    rhs = (
        2 * bar12 * (d1 * d2 - h12 * h12)
        + 2 * bar13 * (d1 * d3 - h13 * h13)
        + 2 * bar23 * (d2 * d3 - h23 * h23)
        + 4 * lam * W
    )
    lhs = sum(p2[i] * fs[i] for i in range(8))
    checks.append(("acceleration_finite_difference", sp.expand(lhs - rhs) == 0))

    return checks


def constant_checks():
    eps = F(1, 4)
    m = F(1) - 3 * eps * eps - 2 * eps ** 3
    M = F(1) + 3 * eps * eps + 2 * eps ** 3
    cp = (
        2 / m
        + (18 * eps * eps + 12 * eps ** 3) / (m * m)
        + 2 * (24 * eps ** 4 + 24 * eps ** 5 + 8 * eps ** 6) / (m ** 3)
    )
    cq = 2 / (m * m) + 6 * eps * eps / (m ** 3)
    cS = (1 - 3 * eps ** 4 / 16) / M - (
        eps * eps / 2 + eps ** 4 / 8
    ) / (m * m) - (6 * eps ** 3 + 15 * eps ** 4) / 4
    cU = (4 - eps * eps) / M - 21 * eps * eps - (
        6 * eps ** 3 + 15 * eps ** 4
    ) / 4
    cV = 2 / M - 15 * eps * eps
    return {
        "epsilon": str(eps),
        "m": str(m),
        "M": str(M),
        "C_P": str(cp),
        "C_Q": str(cq),
        "C_P_lt_6": cp < 6,
        "C_Q_lt_5": cq < 5,
        "cS": str(cS),
        "cU": str(cU),
        "cV": str(cV),
        "excess_S": str(cS - F(7, 10)),
        "excess_U": str(cU - F(7, 10)),
        "excess_V": str(cV - F(7, 10)),
        "all_excess_positive": min(cS, cU, cV) > F(7, 10),
    }


def x_from_r(r: F):
    return r * r / (1 + r * r), r / (1 + r * r)


def center_from_rs(label, rs, es):
    xs = []
    sqv = []
    for r0 in rs:
        xi, svi = x_from_r(F(r0))
        xs.append(xi)
        sqv.append(svi)
    a0 = F(es[0]) * sqv[0] * sqv[1]
    b0 = F(es[1]) * sqv[0] * sqv[2]
    c0 = F(es[2]) * sqv[1] * sqv[2]
    return {"label": label, "values": xs + [a0, b0, c0], "e": [F(e) for e in es]}


def direct_center(label, values):
    vals = [F(v) for v in values]
    xv = vals[:3]
    sv = [math.sqrt(float(xi * (1 - xi))) for xi in xv]
    ev = [
        float(vals[3] / F.from_float(sv[0]).limit_denominator(10**9) / F.from_float(sv[1]).limit_denominator(10**9)),
        float(vals[4] / F.from_float(sv[0]).limit_denominator(10**9) / F.from_float(sv[2]).limit_denominator(10**9)),
        float(vals[5] / F.from_float(sv[1]).limit_denominator(10**9) / F.from_float(sv[2]).limit_denominator(10**9)),
    ]
    return {"label": label, "values": vals, "e_float": ev}


def graph_connected(vals):
    present = [vals[3] != 0, vals[4] != 0, vals[5] != 0]
    if sum(present) < 2:
        return False
    parent = list(range(3))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(i, j):
        ri, rj = find(i), find(j)
        if ri != rj:
            parent[ri] = rj

    for p, edge in zip(present, [(0, 1), (0, 2), (1, 2)]):
        if p:
            union(*edge)
    return len({find(i) for i in range(3)}) == 1


def present_edges(vals):
    return [vals[3] != 0, vals[4] != 0, vals[5] != 0]


def factorized_log_symbols(vals):
    present = present_edges(vals)
    if sum(present) == 0:
        l10, l11, l20, l21, l30, l31 = sp.symbols("l10 l11 l20 l21 l30 l31")
        out = []
        for label in EVENTS:
            b0, b1, b2 = BITS[label]
            out.append((l11 if b0 else l10) + (l21 if b1 else l20) + (l31 if b2 else l30))
        return out
    if sum(present) == 1:
        edge_idx = present.index(True)
        edge_vertices = [(0, 1), (0, 2), (1, 2)][edge_idx]
        isolated = ({0, 1, 2} - set(edge_vertices)).pop()
        b00, b10, b01, b11, s0, s1 = sp.symbols("b00 b10 b01 b11 s0 s1")
        block = {(0, 0): b00, (1, 0): b10, (0, 1): b01, (1, 1): b11}
        out = []
        for label in EVENTS:
            bits = BITS[label]
            pair_bits = (bits[edge_vertices[0]], bits[edge_vertices[1]])
            out.append(block[pair_bits] + (s1 if bits[isolated] else s0))
        return out
    return None


def symbolic_zero_rows_certified(vals, zero_rows):
    if not zero_rows:
        return True
    logs = factorized_log_symbols(vals)
    if logs is None:
        return False
    sub = dict(zip(coords, [sp.Rational(v.numerator, v.denominator) for v in vals]))
    pvals = [ff(p.subs(sub)) for p in ps]
    jvals = [[ff(J[row, col].subs(sub)) for col in range(6)] for row in range(8)]
    hvals = [
        [[ff(Hp[row][i, j].subs(sub)) for j in range(6)] for i in range(6)]
        for row in range(8)
    ]
    for i in zero_rows:
        for j in range(6):
            expr = sp.Rational(0)
            for row in range(8):
                expr += sp.Rational(jvals[row][i].numerator, jvals[row][i].denominator) * sp.Rational(
                    jvals[row][j].numerator, jvals[row][j].denominator
                ) / sp.Rational(pvals[row].numerator, pvals[row].denominator)
            for row in range(8):
                if hvals[row][i][j] != 0:
                    expr += sp.Rational(hvals[row][i][j].numerator, hvals[row][i][j].denominator) * logs[row]
            if sp.expand(expr) != 0:
                return False
    return True


def leading_minors(vals):
    K = sp.Matrix([[vals[0], vals[3], vals[4]], [vals[3], vals[1], vals[5]], [vals[4], vals[5], vals[2]]])
    I = sp.eye(3)
    return [ff(K[:i, :i].det()) for i in range(1, 4)], [ff((I - K)[:i, :i].det()) for i in range(1, 4)]


def center_matrices(vals, terms=96):
    sub = dict(zip(coords, [sp.Rational(v.numerator, v.denominator) for v in vals]))
    pvals = [ff(p.subs(sub)) for p in ps]
    if any(v <= 0 for v in pvals):
        raise ValueError("nonpositive event probability")
    jvals = [[ff(J[row, col].subs(sub)) for col in range(6)] for row in range(8)]
    hvals = [
        [[ff(Hp[row][i, j].subs(sub)) for j in range(6)] for i in range(6)]
        for row in range(8)
    ]
    logs = [log_interval(p, terms) for p in pvals]
    x0, y0, z0, a0, b0, c0 = vals
    v1 = x0 * (1 - x0)
    v2 = y0 * (1 - y0)
    v3 = z0 * (1 - z0)
    V0 = v1 * v2 * v3
    G = [[F(0) for _ in range(6)] for __ in range(6)]
    G[0][0] = 1 / v1
    G[1][1] = 1 / v2
    G[2][2] = 1 / v3
    G[3][3] = a0 * a0 / (v1 * v2) + b0 * b0 * c0 * c0 / V0
    G[4][4] = b0 * b0 / (v1 * v3) + a0 * a0 * c0 * c0 / V0
    G[5][5] = c0 * c0 / (v2 * v3) + a0 * a0 * b0 * b0 / V0

    A = [[(F(0), F(0)) for _ in range(6)] for __ in range(6)]
    Bmid = np.zeros((6, 6), dtype=float)
    Rmid = np.zeros((6, 6), dtype=float)
    for i in range(6):
        for j in range(6):
            exact = F(0)
            for row in range(8):
                exact += jvals[row][i] * jvals[row][j] / pvals[row]
            entry = (exact, exact)
            for row in range(8):
                if hvals[row][i][j] != 0:
                    entry = iv_add(entry, iv_scale(hvals[row][i][j], logs[row]))
            Bmid[i, j] = iv_mid_float(entry)
            entry = iv_sub(entry, (F(7, 10) * G[i][j], F(7, 10) * G[i][j]))
            Rmid[i, j] = iv_mid_float(entry)
            A[i][j] = entry
    return A, Bmid, Rmid, pvals, G


def certify_center(center):
    vals = center["values"]
    kmins, ikmins = leading_minors(vals)
    connected = graph_connected(vals)
    active = [0, 1, 2]
    zero_rows = []
    if vals[3] != 0:
        active.append(3)
    if vals[4] != 0:
        active.append(4)
    if vals[5] != 0:
        active.append(5)
    if connected:
        active = list(range(6))
    else:
        zero_rows = [idx for idx in [3, 4, 5] if idx not in active]

    last = None
    for terms in [80, 120, 180]:
        A, Bmid, Rmid, pvals, G = center_matrices(vals, terms=terms)
        subA = [[A[i][j] for j in active] for i in active]
        ok, pivots = interval_ldl_positive(subA)
        zero_ok = symbolic_zero_rows_certified(vals, zero_rows)
        last = (terms, ok, zero_ok, pivots, Bmid, Rmid, pvals)
        if ok and zero_ok:
            break

    terms, ok, zero_ok, pivots, Bmid, Rmid, pvals = last
    min_pivot = min(p[0] for p in pivots) if pivots else F(0)
    max_pivot_width = max(iv_width(p) for p in pivots) if pivots else F(0)
    eig_B = np.linalg.eigvalsh(Bmid)
    eig_R_active = np.linalg.eigvalsh(Rmid[np.ix_(active, active)])
    return {
        "label": center["label"],
        "connected": connected,
        "active_coordinates": active,
        "zero_rows": zero_rows,
        "K_leading_minors": [str(v) for v in kmins],
        "I_minus_K_leading_minors": [str(v) for v in ikmins],
        "min_event_probability": str(min(pvals)),
        "ldl_terms": terms,
        "ldl_certified": bool(ok),
        "zero_rows_certified": bool(zero_ok),
        "min_ldl_pivot_lower": frac_brief(min_pivot),
        "max_pivot_interval_width": frac_brief(max_pivot_width),
        "diagnostic_min_eig_B": float(eig_B[0]),
        "diagnostic_min_eig_residual_active": float(eig_R_active[0]),
    }


def center_suite():
    return [
        center_from_rs("balanced_zero_edge", (1, 1, 1), (0, 0, 0)),
        center_from_rs("balanced_all_positive_boundary", (1, 1, 1), (F(1, 4), F(1, 4), F(1, 4))),
        center_from_rs("balanced_mixed_cycle_boundary", (1, 1, 1), (F(1, 4), F(1, 4), F(-1, 4))),
        center_from_rs("balanced_one_edge_12", (1, 1, 1), (F(1, 4), 0, 0)),
        center_from_rs("balanced_two_edge_path_12_13", (1, 1, 1), (F(1, 4), F(1, 4), 0)),
        center_from_rs("balanced_two_edge_mixed_path", (1, 1, 1), (F(1, 4), F(-1, 4), 0)),
        direct_center(
            "author_noncommuting_example",
            [F(1, 4), F(1, 2), F(3, 4), F(1, 32), F(1, 40), F(1, 48)],
        ),
        center_from_rs("rare_opposite_diagonals_boundary", (F(1, 8), 1, 8), (F(1, 4), F(-1, 4), F(1, 4))),
        center_from_rs("rare_two_small_boundary", (F(1, 8), F(1, 7), 1), (F(1, 4), F(-1, 4), F(1, 4))),
        center_from_rs("near_one_two_large_boundary", (8, 7, 1), (F(1, 4), F(1, 4), F(-1, 4))),
        center_from_rs("asymmetric_all_positive", (F(1, 2), F(2, 3), F(3, 2)), (F(1, 4), F(1, 4), F(1, 4))),
        center_from_rs("asymmetric_mixed_cycle", (F(1, 2), F(2, 3), F(3, 2)), (F(1, 4), F(1, 4), F(-1, 4))),
        center_from_rs("single_edge_23_asymmetric", (F(1, 2), 1, 2), (0, 0, F(1, 4))),
        center_from_rs("connected_missing_12", (F(1, 3), F(2, 3), F(3, 4)), (0, F(1, 4), F(1, 4))),
        center_from_rs("connected_missing_13_mixed", (F(1, 3), F(2, 3), F(3, 4)), (F(1, 4), 0, F(-1, 4))),
        center_from_rs("tiny_interactions", (F(1, 3), F(2, 5), F(3, 5)), (F(1, 16), F(-1, 16), F(1, 32))),
    ]


def main():
    mp.mp.dps = 80
    print("Python", sys.version.split()[0])
    print("Platform", platform.platform())
    print("NumPy", np.__version__, "mpmath", mp.__version__, "SymPy", sp.__version__)
    print("Thread env", {k: os.environ.get(k) for k in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"]})

    symbolic = symbolic_identity_checks()
    failed = [name for name, ok in symbolic if not ok]
    if failed:
        raise AssertionError(f"symbolic checks failed: {failed}")
    print("PASS symbolic identities:", len(symbolic))

    constants = constant_checks()
    if not constants["C_P_lt_6"] or not constants["C_Q_lt_5"] or not constants["all_excess_positive"]:
        raise AssertionError("constant check failed")
    print("PASS rational constants", constants)

    centers = []
    for center in center_suite():
        cert = certify_center(center)
        if not cert["ldl_certified"] or not cert["zero_rows_certified"]:
            raise AssertionError(f"center certificate failed: {center['label']} -> {cert}")
        centers.append(cert)
        print("PASS center", cert["label"], "active", cert["active_coordinates"], "min_p", cert["min_event_probability"])

    summary = {
        "status": "PASS",
        "symbolic_check_count": len(symbolic),
        "constants": constants,
        "center_count": len(centers),
        "centers": centers,
    }
    Path("certificate_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("ALL INDEPENDENT W4 CERTIFICATE CHECKS PASSED")


if __name__ == "__main__":
    main()
