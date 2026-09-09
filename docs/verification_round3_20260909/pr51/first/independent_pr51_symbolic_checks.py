#!/usr/bin/env python3
"""
Independent exact checks for PR51's public proof.

This script uses only the public proof statements.  It does not import author
code, PR41 code, PR43 code, or private Drive material.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import platform
import time
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
    if isinstance(obj, (sp.Integer, sp.Rational, sp.Expr)):
        return str(sp.factor(sp.simplify(obj)))
    if isinstance(obj, Fraction):
        return f"{obj.numerator}/{obj.denominator}" if obj.denominator != 1 else str(obj.numerator)
    return obj


def assert_zero(expr: Any, label: str) -> None:
    if isinstance(expr, sp.MatrixBase):
        for i in range(expr.rows):
            for j in range(expr.cols):
                assert_zero(expr[i, j], f"{label}[{i},{j}]")
        return
    z = sp.factor(sp.together(sp.simplify(expr)))
    if z != 0:
        raise AssertionError(f"{label}: expected 0, got {z}")


def assert_equal(a: Any, b: Any, label: str) -> None:
    assert_zero(a - b, label)


def bits(mask: int, n: int) -> list[int]:
    return [i for i in range(n) if (mask >> i) & 1]


def principal_minor(M: sp.Matrix, mask: int) -> Any:
    if mask == 0:
        return S.One
    idx = bits(mask, M.rows)
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


def coefficient(expr: Any, var: sp.Symbol, degree: int) -> Any:
    return sp.factor(sp.expand(expr).coeff(var, degree))


def check_general_events_and_cofactor() -> dict[str, Any]:
    t = sp.Symbol("t")
    x, y, z, a, b, c = sp.symbols("x y z a b c")
    d1, d2, d3, h12, h13, h23 = sp.symbols("d1 d2 d3 h12 h13 h23")
    K = sp.Matrix([[x, a, b], [a, y, c], [b, c, z]])
    D = sp.Matrix([[d1, h12, h13], [h12, d2, h23], [h13, h23, d3]])

    q12 = x * y - a**2
    q13 = x * z - b**2
    q23 = y * z - c**2
    q123 = K.det()
    displayed = [
        1 - x - y - z + q12 + q13 + q23 - q123,
        x - q12 - q13 + q123,
        y - q12 - q23 + q123,
        q12 - q123,
        z - q13 - q23 + q123,
        q13 - q123,
        q23 - q123,
        q123,
    ]
    mobius = exact_law(K)
    for i, (m, p) in enumerate(zip(mobius, displayed)):
        assert_equal(m, p, f"general event formula atom {i}")

    Kt = K + t * D
    pt = exact_law(Kt)
    p2 = [sp.diff(p, t, 2).subs(t, 0) for p in pt]

    L0, L1, L2, L12, L3, L13, L23, L123 = sp.symbols("L0 L1 L2 L12 L3 L13 L23 L123")
    logs = [L0, L1, L2, L12, L3, L13, L23, L123]
    A_from_events = sum(p2[i] * logs[i] for i in range(8))
    l12 = L0 + L12 - L1 - L2
    l13 = L0 + L13 - L1 - L3
    l23 = L0 + L23 - L2 - L3
    Lambda = L123 + L1 + L2 + L3 - L0 - L12 - L13 - L23
    detD12 = d1 * d2 - h12**2
    detD13 = d1 * d3 - h13**2
    detD23 = d2 * d3 - h23**2
    cofactor = sp.trace(K * D.adjugate())
    A_formula = 2 * (l12 * detD12 + l13 * detD13 + l23 * detD23) + 2 * Lambda * cofactor
    assert_equal(A_from_events, A_formula, "general cofactor acceleration identity")

    return {"status": "PASS", "atoms": 8, "identity": "B=F+2 sum l_ij det(D_ij)+2 Lambda tr(K adj D)"}


def half_law_and_derivatives():
    t = sp.Symbol("t")
    b, c = sp.symbols("b c", nonzero=True)
    d1, d2, d3, h12, h13, h23 = sp.symbols("d1 d2 d3 h12 h13 h23")
    K = sp.Matrix([[S(1) / 2, 0, b], [0, S(1) / 2, c], [b, c, S(1) / 2]])
    D = sp.Matrix([[d1, h12, h13], [h12, d2, h23], [h13, h23, d3]])
    p = exact_law(K)
    pt = exact_law(K + t * D)
    p1 = [sp.diff(q, t).subs(t, 0) for q in pt]
    p2 = [sp.diff(q, t, 2).subs(t, 0) for q in pt]
    return b, c, d1, d2, d3, h12, h13, h23, p, p1, p2


def check_half_filled_decomposition() -> dict[str, Any]:
    b, c, d1, d2, d3, h12, h13, h23, p, p1, p2 = half_law_and_derivatives()
    s_expr = 4 * (b**2 + c**2)
    d_expr = 4 * (b**2 - c**2)
    k_expr = 8 * b * c
    displayed_atoms = [
        (1 - s_expr) / 8,
        (1 + d_expr) / 8,
        (1 - d_expr) / 8,
        (1 + s_expr) / 8,
        (1 + s_expr) / 8,
        (1 - d_expr) / 8,
        (1 + d_expr) / 8,
        (1 - s_expr) / 8,
    ]
    for i, (actual, expected) in enumerate(zip(p, displayed_atoms)):
        assert_equal(actual, expected, f"half-filled atom {i}")

    # Full six-variable cross-sector orthogonality check, with log atom groups
    # represented by independent symbols for the four complementary pairs.
    Lm, Ldp, Ldm, Lp = sp.symbols("Lm Ldp Ldm Lp")
    log_groups = [Lm, Ldp, Ldm, Lp, Lp, Ldm, Ldp, Lm]
    F_full = sum(p1[i] ** 2 / p[i] for i in range(8))
    A_full = sum(p2[i] * log_groups[i] for i in range(8))
    B_full = sp.expand(F_full + A_full)
    plus = [h13, h23]
    minus = [d1, d2, d3, h12]
    for u in plus:
        for v in minus:
            assert_equal(sp.diff(B_full, u, v), 0, f"2+4 cross Hessian {u},{v}")

    # Two-dimensional sector positivity formula, checked as an exact identity
    # after replacing log combinations by g(s), g(d) symbols.
    gs, gd = sp.symbols("gs gd")
    sector2 = sp.expand(B_full.subs({d1: 0, d2: 0, d3: 0, h12: 0}))
    sector2_rewritten = sector2.subs({
        Lm: S.Zero,
        Lp: gs,
        Ldp: (gs + gd) / 2,
        Ldm: (gs - gd) / 2,
    })
    F_2 = sp.expand(F_full.subs({d1: 0, d2: 0, d3: 0, h12: 0}))
    expected_2 = F_2 + 2 * (gs + gd) * h13**2 + 2 * (gs - gd) * h23**2
    assert_equal(sector2_rewritten, expected_2, "two-dimensional sector formula")

    P, E, Z, R = sp.symbols("P E Z R")
    subs4 = {d1: (P + E) / 2, d2: (P - E) / 2, d3: Z, h12: R, h13: 0, h23: 0}
    p1_4 = [sp.factor(q.subs(subs4)) for q in p1]
    score_expected = {
        7: P + Z - s_expr * P / 2 + d_expr * E / 2 + k_expr * R,
        4: -P + Z - s_expr * P / 2 + d_expr * E / 2 + k_expr * R,
        1: E - Z - s_expr * P / 2 + d_expr * E / 2 + k_expr * R,
        2: -E - Z - s_expr * P / 2 + d_expr * E / 2 + k_expr * R,
    }
    for idx, expected in score_expected.items():
        assert_equal(4 * p1_4[idx], expected, f"four-sector score atom {idx}")
    complement_pairs = [(0, 7), (3, 4), (6, 1), (5, 2)]
    for i, j in complement_pairs:
        assert_equal(p1_4[i] + p1_4[j], 0, f"complementary score pair {i},{j}")

    F4 = sp.factor(sp.together(sum((p1_4[i] ** 2) / p[i] for i in range(8))))
    V = Z + (s_expr * P + d_expr * E) / 2
    F4_expected = 2 * P**2 + 2 * E**2 + 2 * (V + k_expr * R) ** 2 / (1 - s_expr**2) + 2 * (V - k_expr * R) ** 2 / (1 - d_expr**2)
    assert_equal(F4, F4_expected, "four-dimensional Fisher formula")

    A4 = sp.expand(sum(p2[i].subs(subs4) * log_groups[i] for i in range(8)))
    W = sp.Symbol("W")
    A4_rewritten = A4.subs({
        Lm: S.Zero,
        Lp: gs,
        Ldp: (W + gs + gd) / 2,
        Ldm: (W + gs - gd) / 2,
    })
    A4_expected = -W * (P**2 - E**2) / 2 - 2 * Z * (gs * P + gd * E) + 2 * W * R**2
    assert_equal(A4_rewritten, A4_expected, "four-dimensional acceleration formula")

    return {
        "status": "PASS",
        "atoms": "matched formula (4)",
        "cross_block_terms": "zero",
        "two_sector": "matched formula (7)",
        "four_sector_scores": "matched formula (8)",
        "fisher": "matched formula (9)",
        "acceleration": "matched formula (10)",
    }


def check_shape_continuation_certificate() -> dict[str, Any]:
    s, r = sp.symbols("s r")
    As = 1 - s**2
    Bs = 1 - r**2 * s**2
    e1 = sp.Matrix([1, 0, 0, 0])
    e2 = sp.Matrix([0, 1, 0, 0])
    e3 = sp.Matrix([0, 0, 1, 0])
    e4 = sp.Matrix([0, 0, 0, 1])

    def Jij(i: int, j: int) -> sp.Matrix:
        basis = [e1, e2, e3, e4]
        return basis[i] * basis[j].T + basis[j] * basis[i].T

    avec = sp.Matrix([s / 2, r * s / 2, 1, s])
    bvec = sp.Matrix([s / 2, r * s / 2, 1, -s])
    ap = sp.Matrix([S(1) / 2, r / 2, 0, 1])
    bp = sp.Matrix([S(1) / 2, r / 2, 0, -1])
    Wp = 2 * s * (1 - r**2) / (As * Bs)
    dotG = (
        sp.diag(-Wp / 2, Wp / 2, 0, 2 * Wp / (1 - r**2))
        + 2 * (ap * avec.T + avec * ap.T) / As
        + 4 * s * (avec * avec.T) / As**2
        + 2 * (bp * bvec.T + bvec * bp.T) / Bs
        + 4 * r**2 * s * (bvec * bvec.T) / Bs**2
        - 2 * Jij(0, 2) / As
        - 2 * r * Jij(1, 2) / Bs
    )

    det_expected = 48 * s**4 * (1 - r**2) ** 2 * (1 + r**2 - 2 * r**2 * s**2) / ((1 - s**2) ** 4 * (1 - r**2 * s**2) ** 4)
    assert_zero(sp.together(dotG.det() - det_expected).as_numer_denom()[0], "dotG determinant identity")

    dotG0 = dotG.subs(r, 0)
    seed_expected = [
        s * (s**4 - s**2 + 1) / (1 - s**2) ** 2,
        s**2 * (s**4 - s**2 + 1) / (1 - s**2) ** 3,
        s**3 * (s**4 - s**2 + 4) / (1 - s**2) ** 4,
        48 * s**4 / (1 - s**2) ** 4,
    ]
    seed_actual = [dotG0[:i, :i].det() for i in range(1, 5)]
    for i, (a, e) in enumerate(zip(seed_actual, seed_expected), 1):
        assert_zero(sp.together(a - e).as_numer_denom()[0], f"r=0 seed leading minor {i}")

    # G_0 from the quadratic form (11) has the singular seed diag(2,2,4,0).
    P, E, Z, T = sp.symbols("P E Z T")
    v = sp.Matrix([P, E, Z, T])
    V = Z + s * (P + r * E) / 2
    Wseries = sp.log((1 - r**2 * s**2) / (1 - s**2))
    g_s = sp.log((1 + s) / (1 - s))
    g_rs = sp.log((1 + r * s) / (1 - r * s))
    q = (
        2 * P**2 + 2 * E**2 - Wseries * (P**2 - E**2) / 2
        - 2 * Z * (g_s * P + g_rs * E)
        + 2 * (V + s * T) ** 2 / (1 - s**2)
        + 2 * (V - s * T) ** 2 / (1 - r**2 * s**2)
        + 2 * Wseries * T**2 / (1 - r**2)
    )
    G0_entries = []
    for i, vi in enumerate(v):
        row = []
        for j, vj in enumerate(v):
            row.append(sp.limit(sp.diff(q, vi, vj) / (2 if i == j else 1), s, 0))
        G0_entries.append(row)
    G0 = sp.Matrix(G0_entries)
    assert_equal(G0, sp.diag(2, 2, 4, 0), "G0 seed matrix")

    return {
        "status": "PASS",
        "dotG_det": ser(det_expected),
        "seed_minors_r0": ser(seed_expected),
        "G0": "diag(2,2,4,0)",
        "analytic_positivity_conditions": "0<s<1 and |r|<1 make displayed denominators and final numerator factor positive",
    }


def floor_log2_fraction(q: Fraction) -> int:
    if q <= 0:
        raise ValueError("log argument must be positive")
    approx = q.numerator.bit_length() - q.denominator.bit_length()
    def pow2(m: int) -> Fraction:
        if m >= 0:
            return Fraction(1 << m, 1)
        return Fraction(1, 1 << (-m))
    while q < pow2(approx):
        approx -= 1
    while q >= pow2(approx + 1):
        approx += 1
    return approx


def atanh_log_interval_y(y: Fraction, terms: int) -> tuple[Fraction, Fraction]:
    if y <= 0:
        raise ValueError("log argument must be positive")
    w = (y - 1) / (y + 1)
    partial = Fraction(0)
    for j in range(terms):
        partial += Fraction(2) * (w ** (2 * j + 1)) / Fraction(2 * j + 1)
    tail = Fraction(2) * (w ** (2 * terms + 1)) / (Fraction(2 * terms + 1) * (1 - w**2))
    if tail < 0:
        # This branch is not used after reduction to y>=1, but keeps the helper honest.
        return partial + tail, partial
    return partial, partial + tail


def add_scaled_interval(acc: tuple[Fraction, Fraction], scalar: Fraction, interval: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
    lo, hi = interval
    alo, ahi = acc
    if scalar >= 0:
        return alo + scalar * lo, ahi + scalar * hi
    return alo + scalar * hi, ahi + scalar * lo


def log_fraction_interval(q: Fraction, terms: int) -> tuple[Fraction, Fraction]:
    m = floor_log2_fraction(q)
    if m >= 0:
        y = q / Fraction(1 << m, 1)
    else:
        y = q * Fraction(1 << (-m), 1)
    if not (Fraction(1) <= y < Fraction(2)):
        raise AssertionError(f"bad power-of-two reduction y={y}")
    log2 = atanh_log_interval_y(Fraction(2), terms)
    logy = atanh_log_interval_y(y, terms)
    return add_scaled_interval(logy, Fraction(m), log2)


def sympy_rational_to_fraction(x: Any) -> Fraction:
    x = sp.Rational(x)
    return Fraction(int(x.p), int(x.q))


def entropy_interval(probabilities: list[Any], terms: int) -> tuple[Fraction, Fraction]:
    acc = (Fraction(0), Fraction(0))
    for p in probabilities:
        pf = sympy_rational_to_fraction(p)
        acc = add_scaled_interval(acc, -pf, log_fraction_interval(pf, terms))
    return acc


def frac_to_decimal_string(x: Fraction, digits: int = 50) -> str:
    from decimal import Decimal, localcontext

    with localcontext() as ctx:
        ctx.prec = digits
        return format(Decimal(x.numerator) / Decimal(x.denominator), "f")


def check_jensen_illustration() -> dict[str, Any]:
    tau = sp.Rational(1, 144)
    K0 = sp.Matrix([[sp.Rational(1, 2), 0, sp.Rational(1, 3)], [0, sp.Rational(1, 2), sp.Rational(1, 4)], [sp.Rational(1, 3), sp.Rational(1, 4), sp.Rational(1, 2)]])
    D0 = sp.Matrix([[2, -1, 3], [-1, 1, -2], [3, -2, -1]])
    atoms0 = exact_law(K0)
    expected_atoms0 = [sp.Rational(v, 288) for v in (11, 43, 29, 61, 61, 29, 43, 11)]
    for i, (a, e) in enumerate(zip(atoms0, expected_atoms0)):
        assert_equal(a, e, f"illustration atom {i}")

    for label, K in [("minus", K0 - tau * D0), ("zero", K0), ("plus", K0 + tau * D0)]:
        for mask in range(1, 8):
            if principal_minor(K, mask) <= 0:
                raise AssertionError(f"{label} K principal minor {mask} not positive")
            if principal_minor(sp.eye(3) - K, mask) <= 0:
                raise AssertionError(f"{label} I-K principal minor {mask} not positive")

    terms = 60
    Hminus = entropy_interval(exact_law(K0 - tau * D0), terms)
    Hzero = entropy_interval(atoms0, terms)
    Hplus = entropy_interval(exact_law(K0 + tau * D0), terms)
    delta = add_scaled_interval((Fraction(0), Fraction(0)), Fraction(1, 2), Hminus)
    delta = add_scaled_interval(delta, Fraction(1, 2), Hplus)
    delta = add_scaled_interval(delta, Fraction(-1), Hzero)

    declared = (
        Fraction("-0.00413603603307918499086949813852939"),
        Fraction("-0.00413603603307918499086949813852938"),
    )
    if not (declared[0] <= delta[0] <= delta[1] <= declared[1]):
        raise AssertionError(
            "Jensen interval not enclosed by declared decimals: "
            f"computed [{frac_to_decimal_string(delta[0])}, {frac_to_decimal_string(delta[1])}]"
        )
    if not (delta[1] < 0):
        raise AssertionError("Jensen illustration interval is not strictly negative")

    return {
        "status": "PASS",
        "terms": terms,
        "computed_delta_interval_decimal": [frac_to_decimal_string(delta[0], 45), frac_to_decimal_string(delta[1], 45)],
        "declared_interval_contains_computed": True,
        "interpretation": "strictly negative illustration only; not theorem evidence and not a counterexample",
    }


def run(output: Path, sources: list[Path]) -> dict[str, Any]:
    started = time.perf_counter()
    result = {
        "status": "PASS_EXACT_PUBLIC_IDENTITY_CHECKS",
        "pr": 51,
        "head": "4baebc317896278dcb8f0947d308fdce037c87cf",
        "source_hashes": {public_source_label(path): sha256_file(path) for path in sources if path.exists()},
        "script_sha256": sha256_file(Path(__file__)),
        "checks": {
            "general_events_and_cofactor": check_general_events_and_cofactor(),
            "half_filled_decomposition": check_half_filled_decomposition(),
            "shape_continuation_certificate": check_shape_continuation_certificate(),
            "jensen_illustration": check_jensen_illustration(),
        },
        "limits": [
            "checks public displayed identities only",
            "does not use private Drive verifier",
            "does not use PR41 or PR43 as theorem black boxes",
            "does not search outside the frozen family",
            "finite Jensen check is illustration-only",
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
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source", type=Path, action="append", default=[])
    args = parser.parse_args()
    result = run(args.output.resolve(), [p.resolve() for p in args.source])
    print(json.dumps({"status": result["status"], "seconds": result["seconds"], "output": str(args.output.resolve())}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
