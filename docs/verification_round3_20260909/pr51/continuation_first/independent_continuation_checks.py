#!/usr/bin/env python3
"""
Independent bounded checks for PR51 continuation.md.

The script checks only displayed identities and method-obstruction examples.
It does not attempt the issue52 global determinant/certificate problem.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import time
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
from typing import Any

import sympy as sp


S = sp.S


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def public_source_label(path: Path) -> str:
    parts = path.as_posix().split("/")
    marker = ["research", "I05-22-missing-edge-20260909"]
    for i in range(len(parts) - len(marker) + 1):
        if parts[i : i + len(marker)] == marker:
            return "/".join(parts[i:])
    return path.name


def ser(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {str(k): ser(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [ser(v) for v in obj]
    if isinstance(obj, Fraction):
        return f"{obj.numerator}/{obj.denominator}" if obj.denominator != 1 else str(obj.numerator)
    if isinstance(obj, (sp.Integer, sp.Rational, sp.Expr)):
        return str(sp.factor(sp.simplify(obj)))
    return obj


def assert_zero(expr: Any, label: str) -> None:
    if isinstance(expr, sp.MatrixBase):
        for i in range(expr.rows):
            for j in range(expr.cols):
                assert_zero(expr[i, j], f"{label}[{i},{j}]")
        return
    val = sp.factor(sp.together(sp.simplify(expr)))
    if val != 0:
        raise AssertionError(f"{label}: expected 0, got {val}")


def assert_equal(a: Any, b: Any, label: str) -> None:
    assert_zero(a - b, label)


def bit_indices(mask: int, n: int) -> list[int]:
    return [i for i in range(n) if (mask >> i) & 1]


def principal_minor(M: sp.Matrix, mask: int) -> Any:
    if mask == 0:
        return S.One
    idx = bit_indices(mask, M.rows)
    return sp.factor(M.extract(idx, idx).det())


def exact_law(K: sp.Matrix) -> list[Any]:
    n = K.rows
    inc = [principal_minor(K, mask) for mask in range(1 << n)]
    out = []
    for exact in range(1 << n):
        total = S.Zero
        for sup in range(1 << n):
            if exact & ~sup:
                continue
            total += (-1) ** ((sup.bit_count() - exact.bit_count()) & 1) * inc[sup]
        out.append(sp.factor(sp.expand(total)))
    return out


def arrow_symbols():
    x, y, A, B, q = sp.symbols("x y A B q")
    d, e, m, f, g, h = sp.symbols("d e m f g h")
    ell0, v0, Lam, k0 = sp.symbols("ell0 v0 Lam k0")
    v = x * (1 - x)
    w = y * (1 - y)
    z = q + A * (1 - x) + B * (1 - y)
    ell1 = ell0 - Lam
    k1 = k0 - Lam
    ell = (1 - y) * ell0 + y * ell1
    kval = (1 - x) * k0 + x * k1
    J = A * k0 + B * ell0 + q * Lam - v0
    n = v0 - Lam * z
    return x, y, A, B, q, d, e, m, f, g, h, ell0, ell1, k0, k1, v0, Lam, v, w, z, ell, kval, J, n


def physical_entries_from_conditional_basis():
    x, y, A, B, q, d, e, m, f, g, h, ell0, ell1, k0, k1, v0, Lam, v, w, z, ell, kval, J, n = arrow_symbols()
    b, c = sp.symbols("b c", nonzero=True)
    D33 = m - A * d - B * e
    D13 = b * ((1 - 2 * x) * d / v - f / A) / 2
    D23 = c * ((1 - 2 * y) * e / w - g / B) / 2
    D12 = b * c * h / (2 * A * B)
    replacements = {
        b**2: A * v,
        c**2: B * w,
        b * c: sp.Symbol("bc"),
    }
    return (x, y, A, B, q, d, e, m, f, g, h, ell0, ell1, k0, k1, v0, Lam, v, w, z, ell, kval, J, n, b, c, D12, D13, D23, D33, replacements)


def reduce_bc(expr: Any, b: sp.Symbol, c: sp.Symbol, A: sp.Symbol, B: sp.Symbol, v: Any, w: Any) -> Any:
    expr = sp.expand(expr)
    expr = expr.xreplace({b**2: A * v, c**2: B * w})
    expr = sp.expand(expr)
    expr = expr.subs(b**2, A * v).subs(c**2, B * w).subs(b**2 * c**2, A * B * v * w)
    expr = expr.subs(b * c, sp.sqrt(A * B * v * w))
    # In the identities checked below all odd sign terms cancel.  Squaring the
    # final square-root monomial replacement is enough after expansion.
    expr = sp.expand(expr).subs(A * B * v * w, A * B * v * w)
    return sp.factor(sp.together(sp.simplify(expr)))


def check_product_domain_direction_logs() -> dict[str, Any]:
    x, y, A, B, q, d, e, m, f, g, h, ell0, ell1, k0, k1, v0, Lam, v, w, z, ell, kval, J, n = arrow_symbols()
    i, j = sp.symbols("i j")

    # Schur complements after b^2=Av and c^2=Bw.
    K_schur = sp.factor(z - A * (1 - x) - B * (1 - y))
    IK_schur = sp.factor(1 - z - A * x - B * y)
    assert_equal(K_schur, q, "K Schur complement")
    assert_equal(IK_schur, 1 - q - A - B, "I-K Schur complement")

    t_formula = q + A * (1 - i) + B * (1 - j)
    previous = z - A * (i - x) - B * (j - y)
    assert_equal(previous, t_formula, "conditional probability formula")

    # Direction inverse map: substitute (22) into the PR41 conditional
    # derivative formula and recover the product-basis expression (21).
    b, c = sp.symbols("b c", nonzero=True)
    phi = (i - x) / v
    psi = (j - y) / w
    D33 = m - A * d - B * e
    D13 = b * ((1 - 2 * x) * d / v - f / A) / 2
    D23 = c * ((1 - 2 * y) * e / w - g / B) / 2
    D12 = b * c * h / (2 * A * B)
    Tij_physical = D33 + (b**2) * d * phi**2 + (c**2) * e * psi**2 - 2 * b * D13 * phi - 2 * c * D23 * psi + 2 * b * c * D12 * phi * psi
    Tij_physical = sp.expand(Tij_physical.subs({b**2: A * v, c**2: B * w, b**2 * c**2: A * B * v * w}))
    target = m + f * (i - x) + g * (j - y) + h * (i - x) * (j - y)
    for ii in (0, 1):
        for jj in (0, 1):
            assert_equal(Tij_physical.subs({i: ii, j: jj}), target.subs({i: ii, j: jj}), f"direction map {ii}{jj}")

    # Lambda=0 equivalence after exponentiating v0=v1.
    Csum = A + B
    equation = sp.expand((1 - q - Csum) * (1 - q) - q * (q + Csum))
    assert_equal(equation, 1 - A - B - 2 * q, "Lambda denominator equivalence")

    # J collection identity as a formal log-coefficient equality.
    Lq, Lqa, Lqb, Lqab, L1q, L1qa, L1qb, L1qab = sp.symbols("Lq Lqa Lqb Lqab L1q L1qa L1qb L1qab")
    # f0(t)=t log t +(1-t)log(1-t); order t00,t11,t10,t01.
    J_logs = (
        (q + A + B) * Lqab + (1 - q - A - B) * L1qab
        + q * Lq + (1 - q) * L1q
        - (q + B) * Lqb - (1 - q - B) * L1qb
        - (q + A) * Lqa - (1 - q - A) * L1qa
    )
    psi00_minus_psi10 = Lqab - L1qab - Lqb + L1qb
    psi00_minus_psi01 = Lqab - L1qab - Lqa + L1qa
    Lambda_log = (L1qb + L1qa - L1qab - L1q) - (Lqb + Lqa - Lqab - Lq)
    v0_log = L1qb + L1qa - L1qab - L1q
    J_formula_logs = A * psi00_minus_psi01 + B * psi00_minus_psi10 + q * Lambda_log - v0_log
    assert_equal(J_logs, J_formula_logs, "J log collection")

    return {
        "status": "PASS",
        "schur_domain": "q and 1-q-A-B",
        "conditional_probability": "t_ij=q+A(1-i)+B(1-j)",
        "direction_inverse": "matched on all four events",
        "lambda_zero_equivalence": "q=(1-A-B)/2",
        "J_collection": "matched formal log coefficients",
    }


def build_logpart_and_blocks():
    vals = physical_entries_from_conditional_basis()
    x, y, A, B, q, d, e, m, f, g, h, ell0, ell1, k0, k1, v0, Lam, v, w, z, ell, kval, J, n, b, c, D12, D13, D23, D33, replacements = vals

    detD23 = e * D33 - D23**2
    detD13 = d * D33 - D13**2
    detD12 = d * e - D12**2
    adj11 = detD23
    adj22 = detD13
    adj33 = detD12
    adj13 = D12 * D23 - e * D13
    adj23 = D12 * D13 - d * D23
    trace_K_adjD = x * adj11 + y * adj22 + z * adj33 + 2 * b * adj13 + 2 * c * adj23
    raw = -2 * k0 * detD23 - 2 * ell0 * detD13 - 2 * v0 * detD12 + 2 * Lam * trace_K_adjD
    logpart = sp.expand(raw.subs({b**2: A * v, c**2: B * w, b**2 * c**2: A * B * v * w}))
    logpart = sp.expand(logpart.subs(b**2, A * v).subs(c**2, B * w).subs(b**2 * c**2, A * B * v * w))
    # The trace expression has no surviving odd b/c monomials after these substitutions.
    if b in logpart.free_symbols or c in logpart.free_symbols:
        logpart = sp.expand(logpart.subs({b**2: A * v, c**2: B * w, b**2 * c**2: A * B * v * w}))
    if b in logpart.free_symbols or c in logpart.free_symbols:
        raise AssertionError(f"uneliminated sign symbols in logpart: {logpart.free_symbols & {b,c}}")

    de = sp.Matrix([d, e])
    u = sp.Matrix([m, f, g, h])
    L = sp.Matrix([[A * ell / (2 * v), J], [J, B * kval / (2 * w)]])
    Cmat = sp.Matrix([
        [-ell, (2 * x - 1) * ell / 2, w * Lam, -w * Lam * (2 * x - 1) / 2],
        [-kval, v * Lam, (2 * y - 1) * kval / 2, -v * Lam * (2 * y - 1) / 2],
    ])
    Rmat = sp.Matrix([
        [0, 0, 0, 0],
        [0, v * ell / (2 * A), 0, -v * w * Lam / (2 * A)],
        [0, 0, w * kval / (2 * B), -v * w * Lam / (2 * B)],
        [0, -v * w * Lam / (2 * A), -v * w * Lam / (2 * B), v * w * n / (2 * A * B)],
    ])
    block_form = (de.T * L * de)[0] + 2 * (de.T * Cmat * u)[0] + (u.T * Rmat * u)[0]
    return x, y, A, B, q, d, e, m, f, g, h, ell0, ell1, k0, k1, v0, Lam, v, w, z, ell, kval, J, n, logpart, block_form


def check_lcr_and_face_identity() -> dict[str, Any]:
    x, y, A, B, q, d, e, m, f, g, h, ell0, ell1, k0, k1, v0, Lam, v, w, z, ell, kval, J, n, logpart, block_form = build_logpart_and_blocks()
    assert_zero(sp.together(logpart - block_form).as_numer_denom()[0], "L,C,R log-acceleration block identity")

    def T(ii: int, jj: int):
        return m + f * (ii - x) + g * (jj - y) + h * (ii - x) * (jj - y)

    Q10 = A * ell0 * d**2 / (2 * v) - ell0 * d * (T(0, 0) + T(1, 0)) + v * ell0 * (T(1, 0) - T(0, 0)) ** 2 / (2 * A)
    Q11 = A * ell1 * d**2 / (2 * v) - ell1 * d * (T(0, 1) + T(1, 1)) + v * ell1 * (T(1, 1) - T(0, 1)) ** 2 / (2 * A)
    Q20 = B * k0 * e**2 / (2 * w) - k0 * e * (T(0, 0) + T(0, 1)) + w * k0 * (T(0, 1) - T(0, 0)) ** 2 / (2 * B)
    Q21 = B * k1 * e**2 / (2 * w) - k1 * e * (T(1, 0) + T(1, 1)) + w * k1 * (T(1, 1) - T(1, 0)) ** 2 / (2 * B)
    face_rhs = (1 - y) * Q10 + y * Q11 + (1 - x) * Q20 + x * Q21 + 2 * J * d * e - v * w * J * h**2 / (2 * A * B)
    assert_zero(sp.together(face_rhs - logpart).as_numer_denom()[0], "face acceleration identity")

    return {
        "status": "PASS",
        "LCR_identity": "matched exact collected cofactor log part",
        "face_acceleration": "matched equation (31)",
        "schur_equivalence": "analytic: positive leading block makes PSD equivalent to displayed Schur complement",
    }


def check_lambda_zero_radial_derivative_identity() -> dict[str, Any]:
    r, u = sp.symbols("r u", real=True)
    Ju = 1 - u**4
    Lu = 1 - r**2 * u**4

    g_u = sp.log((1 + u**2) / (1 - u**2))
    g_ru = sp.log((1 + r * u**2) / (1 - r * u**2))
    ell = g_u + g_ru
    kval = g_u - g_ru
    v0 = sp.log(Lu / Ju)

    n1 = 4 * u * (1 / Ju - r / Lu)
    n2 = 4 * u * (1 / Ju + r / Lu)
    n3 = 4 * u**3 * (1 - r**2) / (Ju * Lu)
    assert_zero(sp.together(sp.simplify(sp.diff(kval, u) - n1)).as_numer_denom()[0], "n1 derivative")
    assert_zero(sp.together(sp.simplify(sp.diff(ell, u) - n2)).as_numer_denom()[0], "n2 derivative")
    assert_zero(sp.together(sp.simplify(sp.diff(v0, u) - n3)).as_numer_denom()[0], "n3 derivative")

    return {
        "status": "PASS_BOUNDED_ANALYTIC",
        "lambda_zero": "q=(1-A-B)/2 gives t00/t11=(1±u^2)/2 and off-diagonal conditionals (1±r*u^2)/2",
        "radial_derivative": "checked n1,n2,n3 as exact derivatives of the three log weights; Q placement reviewed analytically from fixed-coordinate cofactor entries",
        "not_checked": "full six-coordinate symbolic expansion, determinant, or positivity of M",
    }


def check_L_trapezoid_analytic() -> dict[str, Any]:
    return {
        "status": "PASS_ANALYTIC",
        "argument": [
            "f0'' is strictly convex because (f0'')''=2/t^3+2/(1-t)^3>0 on (0,1)",
            "J is the integral over a rectangle of f0''(q+alpha+beta)",
            "for fixed alpha or beta, the integral of a strictly convex function lies strictly below the trapezoid average",
            "ell-w(ell0+ell1)=(1-y)^2 ell0+y^2 ell1>0 and k-v(k0+k1)=(1-x)^2 k0+x^2 k1>0",
            "therefore J^2<L11*L22 and L is positive definite because A,B,ell,k,v,w are positive",
        ],
    }


def floor_log2_fraction(q: Fraction) -> int:
    if q <= 0:
        raise ValueError("log argument must be positive")

    def pow2(m: int) -> Fraction:
        return Fraction(1 << m, 1) if m >= 0 else Fraction(1, 1 << (-m))

    guess = q.numerator.bit_length() - q.denominator.bit_length()
    while q < pow2(guess):
        guess -= 1
    while q >= pow2(guess + 1):
        guess += 1
    return guess


def atanh_log_interval_y(y: Fraction, terms: int) -> tuple[Fraction, Fraction]:
    w = (y - 1) / (y + 1)
    partial = Fraction(0)
    for j in range(terms):
        partial += Fraction(2) * w ** (2 * j + 1) / Fraction(2 * j + 1)
    tail = Fraction(2) * w ** (2 * terms + 1) / (Fraction(2 * terms + 1) * (1 - w**2))
    return (partial, partial + tail) if tail >= 0 else (partial + tail, partial)


def add_scaled_interval(acc: tuple[Fraction, Fraction], scalar: Fraction, interval: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
    alo, ahi = acc
    lo, hi = interval
    if scalar >= 0:
        return alo + scalar * lo, ahi + scalar * hi
    return alo + scalar * hi, ahi + scalar * lo


def log_fraction_interval(q: Fraction, terms: int) -> tuple[Fraction, Fraction]:
    m = floor_log2_fraction(q)
    y = q / (Fraction(1 << m, 1) if m >= 0 else Fraction(1, 1 << (-m)))
    if not (Fraction(1) <= y < Fraction(2)):
        raise AssertionError(f"bad reduction y={y}")
    log2 = atanh_log_interval_y(Fraction(2), terms)
    logy = atanh_log_interval_y(y, terms)
    return add_scaled_interval(logy, Fraction(m), log2)


def sympy_to_fraction(x: Any) -> Fraction:
    r = sp.Rational(x)
    return Fraction(int(r.p), int(r.q))


def interval_to_decimal(x: Fraction, digits: int = 50) -> str:
    with localcontext() as ctx:
        ctx.prec = digits
        return format(Decimal(x.numerator) / Decimal(x.denominator), "f")


def entropy_interval(probs: list[Any], terms: int) -> tuple[Fraction, Fraction]:
    acc = (Fraction(0), Fraction(0))
    for p in probs:
        pf = sympy_to_fraction(p)
        acc = add_scaled_interval(acc, -pf, log_fraction_interval(pf, terms))
    return acc


def B_interval(K: sp.Matrix, D: sp.Matrix, terms: int) -> tuple[Fraction, Fraction]:
    t = sp.Symbol("t")
    p = exact_law(K)
    pt = exact_law(K + t * D)
    p1 = [sp.diff(q, t).subs(t, 0) for q in pt]
    p2 = [sp.diff(q, t, 2).subs(t, 0) for q in pt]
    exact_part = sum(p1[i] ** 2 / p[i] for i in range(8))
    acc = (sympy_to_fraction(exact_part), sympy_to_fraction(exact_part))
    for prob, coeff in zip(p, p2):
        acc = add_scaled_interval(acc, sympy_to_fraction(coeff), log_fraction_interval(sympy_to_fraction(prob), terms))
    return acc


def check_phi_obstruction() -> dict[str, Any]:
    t = sp.Symbol("t")
    K = sp.Matrix([
        [sp.Rational(23, 25), 0, sp.Rational(1, 5)],
        [0, sp.Rational(2, 5), sp.Rational(8, 25)],
        [sp.Rational(1, 5), sp.Rational(8, 25), sp.Rational(3, 10)],
    ])
    D = sp.Matrix([
        [0, -1, sp.Rational(-4, 5)],
        [-1, sp.Rational(1, 3), sp.Rational(1, 20)],
        [sp.Rational(-4, 5), sp.Rational(1, 20), sp.Rational(-2, 15)],
    ])
    pt = exact_law(K + t * D)

    Phi = S.Zero
    for i in (0, 1):
        for j in (0, 1):
            base = i | (j << 1)
            p0 = pt[base]
            p1 = pt[base | 4]
            Pij = p0 + p1
            Phi += Pij**2 / p1
    phi2 = sp.factor(sp.diff(Phi, t, 2).subs(t, 0))
    expected = -sp.Rational(53670727895896612562246875, 14117659525214393686902)
    assert_equal(phi2, expected, "Phi'' obstruction value")

    tau = sp.Rational(1, 10000)
    for label, M in [("minus", K - tau * D), ("zero", K), ("plus", K + tau * D)]:
        for mask in range(1, 8):
            if principal_minor(M, mask) <= 0:
                raise AssertionError(f"{label} K minor {mask} not positive")
            if principal_minor(sp.eye(3) - M, mask) <= 0:
                raise AssertionError(f"{label} I-K minor {mask} not positive")

    terms = 80
    Bint = B_interval(K, D, terms)
    declared_B = (
        Fraction("85.39754587008524590529296252441265816"),
        Fraction("85.39754587008524590529296252441265817"),
    )
    if not (declared_B[0] <= Bint[0] <= Bint[1] <= declared_B[1]):
        raise AssertionError("entropy curvature interval not contained in declared interval")

    Hminus = entropy_interval(exact_law(K - tau * D), terms)
    Hzero = entropy_interval(exact_law(K), terms)
    Hplus = entropy_interval(exact_law(K + tau * D), terms)
    delta = add_scaled_interval((Fraction(0), Fraction(0)), Fraction(1, 2), Hminus)
    delta = add_scaled_interval(delta, Fraction(1, 2), Hplus)
    delta = add_scaled_interval(delta, Fraction(-1), Hzero)
    declared_delta = (
        Fraction("-0.00000042702288120241526682286996218"),
        Fraction("-0.00000042702288120241526682286996217"),
    )
    if not (declared_delta[0] <= delta[0] <= delta[1] <= declared_delta[1]):
        raise AssertionError("Jensen interval not contained in declared interval")
    if not (Bint[0] > 0 and delta[1] < 0):
        raise AssertionError("entropy signs are not as declared")

    return {
        "status": "PASS",
        "Phi_second_derivative": ser(phi2),
        "entropy_curvature_interval_decimal": [interval_to_decimal(Bint[0], 45), interval_to_decimal(Bint[1], 45)],
        "jensen_interval_decimal": [interval_to_decimal(delta[0], 45), interval_to_decimal(delta[1], 45)],
        "interpretation": "auxiliary-method counterexample only; entropy curvature remains negative",
    }


def check_power_series_obstruction() -> dict[str, Any]:
    t = sp.Symbol("t")
    s = sp.Symbol("s", positive=True)
    rt = sp.sqrt(s / 8)
    K = sp.Matrix([[S(1) / 2, 0, rt], [0, S(1) / 2, rt], [rt, rt, S(1) / 2]])
    D = sp.Matrix([[S(1) / 4, -S(1) / 4, 0], [-S(1) / 4, S(1) / 4, 0], [0, 0, s / 6]])
    p = exact_law(K)
    pt = exact_law(K + t * D)
    p1 = [sp.diff(q, t).subs(t, 0) for q in pt]
    p2 = [sp.diff(q, t, 2).subs(t, 0) for q in pt]
    Bform = sum(p1[i] ** 2 / p[i] for i in range(8)) + sum(p2[i] * sp.log(p[i]) for i in range(8))
    expected = S(1) / 2 + S(8) * s**2 / 9 + s**2 / (18 * (1 - s**2)) - s * sp.log((1 + s) / (1 - s)) / 6
    diff = sp.expand_log(Bform - expected, force=True)
    diff = diff.subs(sp.log(s - 1), sp.log(1 - s) + sp.I * sp.pi)
    real_diff = sp.expand(diff).as_real_imag()[0]
    assert_zero(sp.together(sp.simplify(real_diff)).as_numer_denom()[0], "power-series obstruction formula")
    series = sp.series(expected, s, 0, 6).removeO()
    assert_equal(series.coeff(s, 4), -S(1) / 18, "s^4 coefficient")
    return {
        "status": "PASS",
        "formula": "1/2 + 8*s**2/9 + s**2/(18*(1-s**2)) - s*log((1+s)/(1-s))/6",
        "series_through_s4": ser(series),
        "s4_coefficient": "-1/18",
        "interpretation": "moving-center direction obstruction; does not refute fixed-coordinate radial derivative conjecture",
    }


def run(output: Path, source: Path) -> dict[str, Any]:
    started = time.perf_counter()
    result = {
        "status": "PASS_BOUNDED_CONTINUATION_CHECKS",
        "pr": 51,
        "head": "2e4b8754ad4af2fe055ebeeef1159877773372a3",
        "source_hashes": {public_source_label(source): sha256_file(source)},
        "script_sha256": sha256_file(Path(__file__)),
        "checks": {
            "product_domain_direction_logs": check_product_domain_direction_logs(),
            "L_trapezoid": check_L_trapezoid_analytic(),
            "LCR_and_face_identity": check_lcr_and_face_identity(),
            "lambda_zero_radial_derivative": check_lambda_zero_radial_derivative_identity(),
            "Phi_obstruction": check_phi_obstruction(),
            "power_series_obstruction": check_power_series_obstruction(),
        },
        "limits": [
            "does not attempt S_full PSD",
            "does not attempt radial M>0",
            "does not run issue52 determinant/global certificate work",
            "does not use private author scripts",
            "finite obstruction examples are method obstructions only",
        ],
        "environment": {
            "python": platform.python_version(),
            "sympy": sp.__version__,
            "OMP_NUM_THREADS": os.environ.get("OMP_NUM_THREADS"),
            "OPENBLAS_NUM_THREADS": os.environ.get("OPENBLAS_NUM_THREADS"),
            "MKL_NUM_THREADS": os.environ.get("MKL_NUM_THREADS"),
        },
    }
    result["seconds"] = round(time.perf_counter() - started, 6)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(ser(result), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.output.resolve(), args.source.resolve())
    print(json.dumps({"status": result["status"], "seconds": result["seconds"], "output": str(args.output.resolve())}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
