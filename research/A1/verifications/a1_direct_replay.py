"""Independent exact replay for the A1 fixed-object review.

The checks here are intentionally narrow: they replay short symbolic identities
and rational log certificates used by the frozen A1 auxiliary claims. They do
not search for examples and do not prove any broader theorem.
"""

import json
import os
import platform
import sys
from fractions import Fraction as F
from pathlib import Path

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")

import sympy as sp


FIXED_A1_COMMIT = "58ee11adcf0afd8d183057d61f0168127093bcad"
FIXED_R1_COMMIT = "603300c06059518961766c724377c3b9d1198fc5"


def sym_minor(matrix, mask):
    ids = [i for i in range(matrix.rows) if (mask >> i) & 1]
    return matrix.extract(ids, ids).det() if ids else sp.Integer(1)


def sym_events(matrix):
    n = matrix.rows
    out = []
    for mask in range(1 << n):
        val = 0
        for sup in range(1 << n):
            if sup & mask == mask:
                val += (-1) ** ((sup ^ mask).bit_count()) * sym_minor(matrix, sup)
        out.append(sp.factor(val))
    return out


def assert_zero(expr, label, checks):
    reduced = sp.cancel(expr)
    if reduced != 0:
        raise AssertionError(f"{label}: {sp.factor(reduced)}")
    checks.append(label)


def radial_symbolic_checks():
    checks = []
    a, d, x, c, s, v1, v2, t, rr = sp.symbols("a d x c s v1 v2 t rr", real=True)
    b00, b01, b11 = sp.symbols("b00 b01 b11", real=True)
    A = sp.Matrix([[a, x], [x, d]])
    z = sp.Matrix([v1, v2])
    W = z * z.T
    K = A.row_join(s * z).col_join(sp.Matrix([[s * v1, s * v2, c]]))
    C1 = A - s * s * W / c
    C0 = A + s * s * W / (1 - c)
    p = sym_events(K)
    q0 = sym_events(C0)
    q1 = sym_events(C1)
    for mask in range(4):
        assert_zero(p[mask] - (1 - c) * q0[mask], f"radial_absent_event_{mask}", checks)
        assert_zero(p[mask + 4] - c * q1[mask], f"radial_present_event_{mask}", checks)
    assert_zero(sum(p) - 1, "radial_complete_event_normalization", checks)
    B = sp.Matrix([[b00, b01], [b01, b11]])
    C1_line = A + t * B - (s + t * rr) ** 2 * W / c
    C0_line = A + t * B + (s + t * rr) ** 2 * W / (1 - c)
    assert_zero((C1_line.diff(t, 2) + 2 * rr * rr * W / c).norm(), "radial_C1_acceleration", checks)
    assert_zero((C0_line.diff(t, 2) - 2 * rr * rr * W / (1 - c)).norm(), "radial_C0_acceleration", checks)
    rank_one_events = sym_events(A + t * W)
    for i, event in enumerate(rank_one_events):
        assert_zero(sp.diff(event, t, 2), f"rank_one_event_affine_{i}", checks)
    return {"checks": len(checks), "labels": checks}


def standard_symbolic_checks():
    checks = []
    d, r, t, u, v = sp.symbols("d r t u v", real=True)
    x = sp.symbols("x0:3")
    y = sp.symbols("y0:3")
    zlog = sp.symbols("z0:4")
    K = sp.Matrix([[d, r, r], [r, d, r], [r, r, d]])
    V = sp.Matrix([[x[0], y[2], y[1]], [y[2], x[1], y[0]], [y[1], y[0], x[2]]])
    P = [
        (1 - d) ** 3 - 3 * (1 - d) * r * r - 2 * r ** 3,
        d * (1 - d) ** 2 + (2 - 3 * d) * r * r + 2 * r ** 3,
        d * d * (1 - d) + (3 * d - 1) * r * r - 2 * r ** 3,
        d ** 3 - 3 * d * r * r + 2 * r ** 3,
    ]
    pt = sym_events(K + t * V)
    pd = [sp.diff(p, t).subs(t, 0).expand() for p in pt]
    pdd = [sp.diff(p, t, 2).subs(t, 0).expand() for p in pt]
    for mask, p in enumerate(pt):
        assert_zero(p.subs(t, 0) - P[mask.bit_count()], f"standard_cardinality_probability_{mask}", checks)
    assert_zero(sum(pt) - 1, "standard_complete_event_normalization", checks)

    amean = sum(x) / 3
    bmean = sum(y) / 3
    xc = [value - amean for value in x]
    yc = [value - bmean for value in y]
    xx = sum(value * value for value in xc)
    yy = sum(value * value for value in yc)
    xy = sum(left * right for left, right in zip(xc, yc))
    tfirst = [
        -3 * ((1 - d) ** 2 - r * r) * u - 6 * r * (1 - d + r) * v,
        ((1 - d) * (1 - 3 * d) - 3 * r * r) * u + (2 * r * (2 - 3 * d) + 6 * r * r) * v,
        (d * (2 - 3 * d) + 3 * r * r) * u + (2 * r * (3 * d - 1) - 6 * r * r) * v,
        3 * (d * d - r * r) * u + 6 * r * (r - d) * v,
    ]
    std_squares = [0, 2 * ((1 - d) * u - 2 * r * v) ** 2, 2 * (d * u + 2 * r * v) ** 2, 0]

    def lift(poly):
        p = sp.Poly(sp.expand(poly), u, v)
        return (
            p.coeff_monomial(u * u) * xx
            + p.coeff_monomial(u * v) * xy
            + p.coeff_monomial(v * v) * yy
        ) / 2

    for card, multiplicity in enumerate([1, 3, 3, 1]):
        actual = sum(pd[mask] ** 2 for mask in range(8) if mask.bit_count() == card)
        expected = multiplicity * tfirst[card].subs({u: amean, v: bmean}) ** 2 + lift(std_squares[card])
        assert_zero(actual - expected, f"standard_fisher_decomposition_card_{card}", checks)

    M = (1 - d) * zlog[0] + (3 * d - 2) * zlog[1] + (1 - 3 * d) * zlog[2] + d * zlog[3]
    Lg = zlog[0] - 3 * zlog[1] + 3 * zlog[2] - zlog[3]
    Tlog = 6 * M * u * u + 12 * r * Lg * u * v + (-6 * M - 12 * r * Lg) * v * v
    Slog = -2 * M * u * u + 8 * r * Lg * u * v + (-4 * M + 4 * r * Lg) * v * v
    actual_log = sum(pdd[mask] * zlog[pt[mask].subs(t, 0).as_poly(d, r).total_degree() * 0 + mask.bit_count()] for mask in range(8))
    assert_zero(actual_log - Tlog.subs({u: amean, v: bmean}) - lift(Slog), "standard_acceleration_decomposition", checks)

    q = sp.symbols("q", positive=True)
    half = [
        (1 + q) ** 2 * (1 - 2 * q) / 8,
        (1 + q) * (1 - q + 2 * q * q) / 8,
        (1 - q) * (1 + q + 2 * q * q) / 8,
        (1 - q) ** 2 * (1 + 2 * q) / 8,
    ]
    for i, expected in enumerate(half):
        assert_zero(P[i].subs({d: sp.Rational(1, 2), r: q / 2}) - expected, f"standard_half_probability_{i}", checks)
    Mq = sp.log((1 - q * q) * (1 - 4 * q * q) / (1 + 3 * q * q + 4 * q ** 4)) / 2
    Lq = sp.log((1 - q) * (1 - 2 * q) * (1 + q + 2 * q * q) ** 3 / ((1 + q) * (1 + 2 * q) * (1 - q + 2 * q * q) ** 3))
    E = (1 - q * q) * (1 - 4 * q * q) * (1 + 3 * q * q + 4 * q ** 4)
    assert_zero(sp.diff(Mq, q) - 8 * q * (2 * q * q - 1) * (2 * q * q + 1) / E, "standard_M_derivative", checks)
    assert_zero(sp.diff(Lq, q) - 48 * q * q * (2 * q * q - 1) / E, "standard_Lg_derivative", checks)
    assert_zero(sp.diff(Lq, q) / sp.diff(Mq, q) - 6 * q / (1 + 2 * q * q), "standard_derivative_ratio", checks)
    assert_zero(sp.diff(6 * q / (1 + 2 * q * q), q) - 6 * (1 - 2 * q * q) / (1 + 2 * q * q) ** 2, "standard_ratio_monotone_derivative", checks)
    m, ell = sp.symbols("m ell")
    assert_zero((2 * m) * (4 * m - 4 * ell) - 16 * ell * ell - 8 * (m - 2 * ell) * (m + ell), "standard_R_determinant_factor", checks)
    return {"checks": len(checks), "labels": checks}


def det2(m):
    return m[0][0] * m[1][1] - m[0][1] * m[1][0]


def det3_from_vec(v):
    a, b, c, x, y, z = v
    return a * b * c + 2 * x * y * z - a * z * z - b * y * y - c * x * x


def principal_minors3(v, complement=False):
    a, b, c, x, y, z = v
    if complement:
        a, b, c, x, y, z = 1 - a, 1 - b, 1 - c, -x, -y, -z
    return [a, b, c, a * b - x * x, a * c - y * y, b * c - z * z, det3_from_vec([a, b, c, x, y, z])]


def events2(u, v, r):
    d = u * v - r * r
    return [1 - u - v + d, u - d, v - d, d]


def events3(v):
    a, b, c, x, y, z = v
    out = []
    for mask in range(8):
        signs = [1 if (mask >> i) & 1 else -1 for i in range(3)]
        diagonals = [value if sign == 1 else 1 - value for value, sign in zip([a, b, c], signs)]
        value = diagonals[0] * diagonals[1] * diagonals[2]
        value -= signs[0] * signs[1] * x * x * diagonals[2]
        value -= signs[0] * signs[2] * y * y * diagonals[1]
        value -= signs[1] * signs[2] * z * z * diagonals[0]
        value += 2 * signs[0] * signs[1] * signs[2] * x * y * z
        out.append(value)
    return out


def add_interval(left, right):
    return (left[0] + right[0], left[1] + right[1])


def scale_interval(q, interval):
    return (q * interval[0], q * interval[1]) if q >= 0 else (q * interval[1], q * interval[0])


def log_interval(q, n_terms=256):
    if q <= 0:
        raise ValueError("log interval requires q>0")
    k = 0
    while q > 2:
        q /= 2
        k += 1
    while q < 1:
        q *= 2
        k -= 1

    def base(x):
        z = (x - 1) / (x + 1)
        partial = 2 * sum((z ** (2 * j + 1) / F(2 * j + 1) for j in range(n_terms)), F(0))
        tail = 2 * z ** (2 * n_terms + 1) / (F(2 * n_terms + 1) * (1 - z * z))
        return partial, partial + tail

    lo, hi = base(q)
    l2, h2 = base(F(2))
    if k >= 0:
        return lo + k * l2, hi + k * h2
    return lo + k * h2, hi + k * l2


def df_e2_interval(kernel):
    u, v, r = kernel
    p00, p10, p01, p11 = events2(u, v, r)
    interval = (F(0), F(0))
    interval = add_interval(interval, scale_interval(1 - u, log_interval(p00 / p01)))
    interval = add_interval(interval, scale_interval(u, log_interval(p10 / p11)))
    return interval, [p00, p10, p01, p11]


def acceleration_certificate_checks():
    checks = []
    K = [F(1, 4), F(3, 4), F(1, 2), F(1, 10), F(1, 10), F(1, 1000)]
    if not all(edge != 0 for edge in K[3:]):
        raise AssertionError("acceleration_connected_edges")
    checks.append("acceleration_connected_edges")
    minors_K = principal_minors3(K)
    minors_IK = principal_minors3(K, complement=True)
    if min(minors_K + minors_IK) <= 0:
        raise AssertionError("acceleration_strict_feasibility")
    checks.append("acceleration_strict_feasibility_all_principal_minors")
    expected_leading = {
        "K": [F(1, 4), F(71, 400), F(325079, 4000000)],
        "I_minus_K": [F(3, 4), F(71, 400), F(344917, 4000000)],
    }
    if [K[0], K[0] * K[1] - K[3] * K[3], det3_from_vec(K)] != expected_leading["K"]:
        raise AssertionError("acceleration_K_leading_minors")
    checks.append("acceleration_K_leading_minors")
    if [1 - K[0], (1 - K[0]) * (1 - K[1]) - K[3] * K[3], principal_minors3(K, True)[-1]] != expected_leading["I_minus_K"]:
        raise AssertionError("acceleration_I_minus_K_leading_minors")
    checks.append("acceleration_I_minus_K_leading_minors")

    a, b, c, x12, x13, x23 = K
    C0 = [a + x13 * x13 / (1 - c), b + x23 * x23 / (1 - c), x12 + x13 * x23 / (1 - c)]
    C1 = [a - x13 * x13 / c, b - x23 * x23 / c, x12 - x13 * x23 / c]
    expected_C0 = [F(27, 100), F(375001, 500000), F(501, 5000)]
    expected_C1 = [F(23, 100), F(374999, 500000), F(499, 5000)]
    if C0 != expected_C0 or C1 != expected_C1:
        raise AssertionError("acceleration_conditional_kernels")
    checks.append("acceleration_conditional_kernels")
    I0, p0 = df_e2_interval(C0)
    I1, p1 = df_e2_interval(C1)
    if p0 != [F(344917, 2000000), F(155079, 2000000), F(1115083, 2000000), F(384921, 2000000)]:
        raise AssertionError("acceleration_C0_events")
    checks.append("acceleration_C0_events")
    if p1 != [F(365083, 2000000), F(134921, 2000000), F(1174917, 2000000), F(325079, 2000000)]:
        raise AssertionError("acceleration_C1_events")
    checks.append("acceleration_C1_events")
    R = scale_interval(F(2), add_interval(I0, scale_interval(F(-1), I1)))
    displayed_R = (F(229172119980517, 500000000000000000), F(91668847992207, 200000000000000000))
    if not (displayed_R[0] <= R[0] <= R[1] <= displayed_R[1] and R[0] > 0):
        raise AssertionError("acceleration_R_positive_displayed_enclosure")
    checks.append("acceleration_R_positive_displayed_enclosure")

    p = events3(K)
    pp = events3(K[:-1] + [K[-1] + 1])
    pm = events3(K[:-1] + [K[-1] - 1])
    dp = [(right - left) / 2 for right, left in zip(pp, pm)]
    ddp = [right + left - 2 * center for right, left, center in zip(pp, pm, p)]
    H2 = (-sum(der * der / prob for der, prob in zip(dp, p)),) * 2
    for accel, prob in zip(ddp, p):
        H2 = add_interval(H2, scale_interval(-accel, log_interval(prob)))
    displayed_H2 = (
        F(-32529701732259701, 500000000000000000),
        F(-65059403464519401, 1000000000000000000),
    )
    if not (displayed_H2[0] <= H2[0] <= H2[1] <= displayed_H2[1] and H2[1] < 0):
        raise AssertionError("acceleration_total_H_second_negative_displayed_enclosure")
    checks.append("acceleration_total_H_second_negative_displayed_enclosure")
    return {
        "checks": len(checks),
        "labels": checks,
        "R_interval": [str(R[0]), str(R[1])],
        "R_displayed_outer_interval_contains_replay": True,
        "total_H_second_interval": [str(H2[0]), str(H2[1])],
        "total_H_second_displayed_outer_interval_contains_replay": True,
        "min_principal_minor": str(min(minors_K + minors_IK)),
        "C0_events": [str(x) for x in p0],
        "C1_events": [str(x) for x in p1],
    }


def main():
    out_path = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    result = {
        "status": "PASS",
        "fixed_A1_commit": FIXED_A1_COMMIT,
        "fixed_R1_commit": FIXED_R1_COMMIT,
        "pid": os.getpid(),
        "python": platform.python_version(),
        "sympy": sp.__version__,
        "threads": {
            key: os.environ.get(key)
            for key in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"]
        },
        "radial": radial_symbolic_checks(),
        "standard": standard_symbolic_checks(),
        "acceleration": acceleration_certificate_checks(),
    }
    text = json.dumps(result, indent=2, sort_keys=True)
    if out_path is not None:
        out_path.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
