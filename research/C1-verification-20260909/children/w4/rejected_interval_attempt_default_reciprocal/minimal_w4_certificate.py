#!/usr/bin/env python3
from __future__ import annotations

from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR, localcontext
from fractions import Fraction as F
from pathlib import Path
import json
import os
import platform
import sys

import numpy as np
import sympy as sp


PREC = 90
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


def ff(q) -> F:
    q = sp.Rational(q)
    return F(int(q.p), int(q.q))


def write_stage(name, payload):
    Path(f"minimal_stage_{name}.json").write_text(
        json.dumps(payload, indent=2), encoding="utf-8"
    )
    print(f"STAGE {name}: {payload.get('status', 'written')}", flush=True)


def f_iv_add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def f_iv_sub(a, b):
    return (a[0] - b[1], a[1] - b[0])


def f_iv_scale(k, a):
    k = F(k)
    return (k * a[0], k * a[1]) if k >= 0 else (k * a[1], k * a[0])


def log_unit_interval(q: F, n: int):
    assert F(1, 1) <= q <= F(2, 1)
    u = (q - 1) / (q + 1)
    total = F(0)
    for j in range(n):
        total += 2 * u ** (2 * j + 1) / (2 * j + 1)
    tail = 2 * u ** (2 * n + 1) / ((2 * n + 1) * (1 - u * u))
    return (total, total + tail)


def log_interval(q: F, n: int = 48):
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
        out = f_iv_add(out, f_iv_scale(k, log_unit_interval(F(2, 1), n)))
    return out


def dec_from_fraction(q: F, rounding):
    with localcontext() as ctx:
        ctx.prec = PREC
        ctx.rounding = rounding
        return Decimal(q.numerator) / Decimal(q.denominator)


def dec_iv_from_fraction(iv):
    return (dec_from_fraction(iv[0], ROUND_FLOOR), dec_from_fraction(iv[1], ROUND_CEILING))


def d_add(a, b):
    with localcontext() as ctx:
        ctx.prec = PREC
        ctx.rounding = ROUND_FLOOR
        lo = a[0] + b[0]
    with localcontext() as ctx:
        ctx.prec = PREC
        ctx.rounding = ROUND_CEILING
        hi = a[1] + b[1]
    return (lo, hi)


def d_sub(a, b):
    with localcontext() as ctx:
        ctx.prec = PREC
        ctx.rounding = ROUND_FLOOR
        lo = a[0] - b[1]
    with localcontext() as ctx:
        ctx.prec = PREC
        ctx.rounding = ROUND_CEILING
        hi = a[1] - b[0]
    return (lo, hi)


def d_mul_pair(x, y, rounding):
    with localcontext() as ctx:
        ctx.prec = PREC
        ctx.rounding = rounding
        return x * y


def d_mul(a, b):
    lows = [d_mul_pair(u, v, ROUND_FLOOR) for u in a for v in b]
    highs = [d_mul_pair(u, v, ROUND_CEILING) for u in a for v in b]
    return (min(lows), max(highs))


def d_square(a):
    lo, hi = a
    if lo <= 0 <= hi:
        hi2 = max(d_mul_pair(lo, lo, ROUND_CEILING), d_mul_pair(hi, hi, ROUND_CEILING))
        return (Decimal(0), hi2)
    vals_lo = [d_mul_pair(lo, lo, ROUND_FLOOR), d_mul_pair(hi, hi, ROUND_FLOOR)]
    vals_hi = [d_mul_pair(lo, lo, ROUND_CEILING), d_mul_pair(hi, hi, ROUND_CEILING)]
    return (min(vals_lo), max(vals_hi))


def d_div_pos(a, b):
    assert b[0] > 0
    recip = (Decimal(1) / b[1], Decimal(1) / b[0])
    return d_mul(a, recip)


def decimal_ldl_positive(A):
    n = len(A)
    zero = (Decimal(0), Decimal(0))
    one = (Decimal(1), Decimal(1))
    L = [[zero for _ in range(n)] for __ in range(n)]
    D = [zero for _ in range(n)]
    pivots = []
    for k in range(n):
        accum = zero
        for j in range(k):
            accum = d_add(accum, d_mul(d_square(L[k][j]), D[j]))
        dk = d_sub(A[k][k], accum)
        pivots.append(dk)
        if dk[0] <= 0:
            return False, pivots
        D[k] = dk
        L[k][k] = one
        for i in range(k + 1, n):
            num = A[i][k]
            for j in range(k):
                num = d_sub(num, d_mul(d_mul(L[i][j], L[k][j]), D[j]))
            L[i][k] = d_div_pos(num, dk)
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
J = ps.jacobian(coords)
Hp = [sp.hessian(p, coords) for p in ps]


def constants():
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
        "status": "PASS" if cp < 6 and cq < 5 and min(cS, cU, cV) > F(7, 10) else "FAIL",
        "m": str(m),
        "M": str(M),
        "C_P": str(cp),
        "C_Q": str(cq),
        "cS": str(cS),
        "cU": str(cU),
        "cV": str(cV),
        "excess_S": str(cS - F(7, 10)),
        "excess_U": str(cU - F(7, 10)),
        "excess_V": str(cV - F(7, 10)),
    }


def x_from_r(r0: F):
    r0 = F(r0)
    return r0 * r0 / (1 + r0 * r0), r0 / (1 + r0 * r0)


def center_from_rs(label, rs, es):
    xs = []
    sqv = []
    for rr in rs:
        xi, sv = x_from_r(F(rr))
        xs.append(xi)
        sqv.append(sv)
    vals = xs + [F(es[0]) * sqv[0] * sqv[1], F(es[1]) * sqv[0] * sqv[2], F(es[2]) * sqv[1] * sqv[2]]
    return {"label": label, "values": vals}


def direct_center(label, values):
    return {"label": label, "values": [F(v) for v in values]}


def present_edges(vals):
    return [vals[3] != 0, vals[4] != 0, vals[5] != 0]


def graph_connected(vals):
    present = present_edges(vals)
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

    for is_present, edge in zip(present, [(0, 1), (0, 2), (1, 2)]):
        if is_present:
            union(*edge)
    return len({find(i) for i in range(3)}) == 1


def factorized_logs(vals):
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
            out.append(block[(bits[edge_vertices[0]], bits[edge_vertices[1]])] + (s1 if bits[isolated] else s0))
        return out
    return None


def leading_minors(vals):
    K = sp.Matrix([[vals[0], vals[3], vals[4]], [vals[3], vals[1], vals[5]], [vals[4], vals[5], vals[2]]])
    I = sp.eye(3)
    return [ff(K[:i, :i].det()) for i in range(1, 4)], [ff((I - K)[:i, :i].det()) for i in range(1, 4)]


def residual_interval_matrix(vals, terms=48):
    sub = dict(zip(coords, [sp.Rational(v.numerator, v.denominator) for v in vals]))
    pvals = [ff(p.subs(sub)) for p in ps]
    jvals = [[ff(J[row, col].subs(sub)) for col in range(6)] for row in range(8)]
    hvals = [
        [[ff(Hp[row][i, j].subs(sub)) for j in range(6)] for i in range(6)]
        for row in range(8)
    ]
    logs = [log_interval(p, terms) for p in pvals]
    x0, y0, z0, a0, b0, c0 = vals
    v1, v2, v3 = x0 * (1 - x0), y0 * (1 - y0), z0 * (1 - z0)
    V0 = v1 * v2 * v3
    G = [F(0)] * 6
    G[0] = 1 / v1
    G[1] = 1 / v2
    G[2] = 1 / v3
    G[3] = a0 * a0 / (v1 * v2) + b0 * b0 * c0 * c0 / V0
    G[4] = b0 * b0 / (v1 * v3) + a0 * a0 * c0 * c0 / V0
    G[5] = c0 * c0 / (v2 * v3) + a0 * a0 * b0 * b0 / V0
    R = [[None for _ in range(6)] for __ in range(6)]
    Rmid = np.zeros((6, 6), dtype=float)
    for i in range(6):
        for j in range(6):
            entry = (F(0), F(0))
            exact = F(0)
            for row in range(8):
                exact += jvals[row][i] * jvals[row][j] / pvals[row]
            entry = f_iv_add(entry, (exact, exact))
            for row in range(8):
                if hvals[row][i][j] != 0:
                    entry = f_iv_add(entry, f_iv_scale(hvals[row][i][j], logs[row]))
            if i == j:
                entry = f_iv_sub(entry, (F(7, 10) * G[i], F(7, 10) * G[i]))
            R[i][j] = dec_iv_from_fraction(entry)
            Rmid[i, j] = float((R[i][j][0] + R[i][j][1]) / 2)
    return R, Rmid, pvals, jvals, hvals


def zero_rows_symbolic(vals, zero_rows, jvals, hvals, pvals):
    if not zero_rows:
        return True
    logs = factorized_logs(vals)
    if logs is None:
        return False
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


def certify_center(center):
    vals = center["values"]
    kmins, ikmins = leading_minors(vals)
    R, Rmid, pvals, jvals, hvals = residual_interval_matrix(vals, terms=48)
    connected = graph_connected(vals)
    active = [0, 1, 2]
    for idx, present in zip([3, 4, 5], present_edges(vals)):
        if present:
            active.append(idx)
    if connected:
        active = list(range(6))
    zero_rows = [idx for idx in [3, 4, 5] if idx not in active]
    sub = [[R[i][j] for j in active] for i in active]
    ok, pivots = decimal_ldl_positive(sub)
    zero_ok = zero_rows_symbolic(vals, zero_rows, jvals, hvals, pvals)
    eig = np.linalg.eigvalsh(Rmid[np.ix_(active, active)])
    return {
        "label": center["label"],
        "status": "PASS" if ok and zero_ok else "FAIL",
        "connected": connected,
        "active": active,
        "zero_rows": zero_rows,
        "zero_rows_symbolic": zero_ok,
        "K_leading_minors": [str(v) for v in kmins],
        "I_minus_K_leading_minors": [str(v) for v in ikmins],
        "min_event_probability": str(min(pvals)),
        "min_decimal_ldl_pivot_lower": f"{min(p[0] for p in pivots):.18E}",
        "max_decimal_pivot_width": f"{max(p[1] - p[0] for p in pivots):.3E}",
        "diagnostic_min_residual_eig_active": float(eig[0]),
    }


def centers():
    return [
        center_from_rs("balanced_zero_edge", (1, 1, 1), (0, 0, 0)),
        center_from_rs("balanced_all_positive_boundary", (1, 1, 1), (F(1, 4), F(1, 4), F(1, 4))),
        center_from_rs("balanced_mixed_cycle_boundary", (1, 1, 1), (F(1, 4), F(1, 4), F(-1, 4))),
        center_from_rs("balanced_one_edge_12", (1, 1, 1), (F(1, 4), 0, 0)),
        center_from_rs("balanced_two_edge_path_12_13", (1, 1, 1), (F(1, 4), F(1, 4), 0)),
        center_from_rs("rare_opposite_diagonals_boundary", (F(1, 8), 1, 8), (F(1, 4), F(-1, 4), F(1, 4))),
        direct_center("author_noncommuting_example", [F(1, 4), F(1, 2), F(3, 4), F(1, 32), F(1, 40), F(1, 48)]),
    ]


def main():
    write_stage(
        "environment",
        {
            "status": "PASS",
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "numpy": np.__version__,
            "sympy": sp.__version__,
            "thread_env": {k: os.environ.get(k) for k in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"]},
        },
    )
    c = constants()
    write_stage("constants", c)
    if c["status"] != "PASS":
        raise AssertionError("constant stage failed")
    results = []
    for center in centers():
        result = certify_center(center)
        write_stage("center_" + center["label"], result)
        if result["status"] != "PASS":
            raise AssertionError(f"center failed: {result}")
        results.append(result)
    summary = {"status": "PASS", "center_count": len(results), "centers": results}
    Path("minimal_certificate_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("MINIMAL W4 CERTIFICATE PASS", flush=True)


if __name__ == "__main__":
    main()
