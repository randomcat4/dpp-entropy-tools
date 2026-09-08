#!/usr/bin/env python3
"""
Fresh non-author audit for D10-U10e general symmetric path and the
boundary_full_atom refinement.

The script is intentionally self-contained: it does not import the author's
search, sanity, or asymptotic probe modules.  It rebuilds n=3 exact-event
probabilities by Mobius inversion from principal-minor inclusion determinants,
then uses those jets to check the reflection/even-block/sigma identities and
independent high-precision boundary samples.
"""

from __future__ import annotations

import itertools
import json
import hashlib
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
from typing import Any


getcontext().prec = 170
D = Decimal

AUDIT_DIR = Path(__file__).resolve().parent
GLOBAL_DIR = AUDIT_DIR.parent
GLOBAL_ROOT = GLOBAL_DIR.parent
SUBFAMILY_DIR = GLOBAL_ROOT / "symmetric_path_subfamily"
BOUNDARY_DIR = GLOBAL_DIR / "boundary_full_atom"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def dec_frac(x: Fraction) -> Decimal:
    return D(x.numerator) / D(x.denominator)


def fmt(x: Decimal, digits: int = 50) -> str:
    return format(+x, f".{digits}E")


def jdefault(obj: Any) -> Any:
    if isinstance(obj, Decimal):
        return str(obj)
    if isinstance(obj, Fraction):
        return {"num": obj.numerator, "den": obj.denominator}
    if isinstance(obj, Path):
        return str(obj)
    raise TypeError(type(obj).__name__)


def poly_add(a: list[Fraction], b: list[Fraction]) -> list[Fraction]:
    return [a[i] + b[i] for i in range(4)]


def poly_mul(a: list[Fraction], b: list[Fraction]) -> list[Fraction]:
    out = [Fraction(0) for _ in range(4)]
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            if i + j < 4:
                out[i + j] += ai * bj
    return out


def perm_sign(p: tuple[int, ...]) -> int:
    inv = 0
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            inv += p[i] > p[j]
    return -1 if inv % 2 else 1


def det_poly_linear(
    K: list[list[Fraction]], E: list[list[Fraction]], idx: list[int]
) -> list[Fraction]:
    """det(K_A + eps E_A) as coefficients up to eps^3."""
    m = len(idx)
    if m == 0:
        return [Fraction(1), Fraction(0), Fraction(0), Fraction(0)]
    ans = [Fraction(0), Fraction(0), Fraction(0), Fraction(0)]
    for p in itertools.permutations(range(m)):
        term = [Fraction(1), Fraction(0), Fraction(0), Fraction(0)]
        for row, col in enumerate(p):
            i, j = idx[row], idx[col]
            term = poly_mul(term, [K[i][j], E[i][j], Fraction(0), Fraction(0)])
        if perm_sign(p) == 1:
            ans = poly_add(ans, term)
        else:
            ans = poly_add(ans, [-z for z in term])
    return ans


def mobius_inclusion_to_exact(values: list[Any]) -> list[Any]:
    out = values[:]
    for bit in range(3):
        step = 1 << bit
        for mask in range(8):
            if (mask & step) == 0:
                out[mask] = out[mask] - out[mask | step]
    return out


def K_frac(x: Fraction, a: Fraction) -> list[list[Fraction]]:
    return [
        [x, a, Fraction(0)],
        [a, x, a],
        [Fraction(0), a, x],
    ]


def mat_zero() -> list[list[Fraction]]:
    return [[Fraction(0) for _ in range(3)] for __ in range(3)]


def mat_add(A: list[list[Fraction]], B: list[list[Fraction]]) -> list[list[Fraction]]:
    return [[A[i][j] + B[i][j] for j in range(3)] for i in range(3)]


def dir_even(name: str) -> list[list[Fraction]]:
    M = mat_zero()
    if name == "d":
        M[0][0] = M[2][2] = Fraction(1)
    elif name == "e":
        M[1][1] = Fraction(1)
    elif name == "h":
        M[0][1] = M[1][0] = M[1][2] = M[2][1] = Fraction(1)
    elif name == "k":
        M[0][2] = M[2][0] = Fraction(1)
    else:
        raise ValueError(name)
    return M


def dir_odd(name: str) -> list[list[Fraction]]:
    M = mat_zero()
    if name == "od":
        M[0][0] = Fraction(1)
        M[2][2] = Fraction(-1)
    elif name == "oh":
        M[0][1] = M[1][0] = Fraction(1)
        M[1][2] = M[2][1] = Fraction(-1)
    else:
        raise ValueError(name)
    return M


EVEN_NAMES = ["d", "e", "h", "k"]
ODD_NAMES = ["od", "oh"]
EVEN_BASIS = [dir_even(name) for name in EVEN_NAMES]
ODD_BASIS = [dir_odd(name) for name in ODD_NAMES]


def event_jets_fraction(
    x: Fraction, a: Fraction, direction: list[list[Fraction]]
) -> tuple[list[Fraction], list[Fraction], list[Fraction]]:
    K = K_frac(x, a)
    q0: list[Fraction] = []
    q1: list[Fraction] = []
    q2: list[Fraction] = []
    for mask in range(8):
        idx = [i for i in range(3) if (mask >> i) & 1]
        coeff = det_poly_linear(K, direction, idx)
        q0.append(coeff[0])
        q1.append(coeff[1])
        q2.append(2 * coeff[2])
    return (
        mobius_inclusion_to_exact(q0),
        mobius_inclusion_to_exact(q1),
        mobius_inclusion_to_exact(q2),
    )


def atoms_formula_fraction(x: Fraction, a: Fraction) -> list[Fraction]:
    t = a * a
    one = Fraction(1)
    E = (one - x) * ((one - x) * (one - x) - 2 * t)
    F = x * (x * x - 2 * t)
    U = x * (one - x) * (one - x) + (one - 2 * x) * t
    W = x * (one - x) * (one - x) + 2 * (one - x) * t
    V = x * x * (one - x) + (2 * x - one) * t
    Z = x * x * (one - x) + 2 * x * t
    return [E, U, W, V, U, Z, V, F]


def B_scalar_exact(
    x: Fraction, a: Fraction, direction: list[list[Fraction]]
) -> Decimal:
    p0, p1, p2 = event_jets_fraction(x, a, direction)
    ans = D(0)
    for u, v, w in zip(p0, p1, p2):
        pu = dec_frac(u)
        ans += dec_frac(v * v) / pu + dec_frac(w) * pu.ln()
    return +ans


def B_matrix_exact(
    x: Fraction, a: Fraction, basis: list[list[list[Fraction]]]
) -> list[list[Decimal]]:
    n = len(basis)
    diag = [B_scalar_exact(x, a, E) for E in basis]
    out = [[D(0) for _ in range(n)] for __ in range(n)]
    for i in range(n):
        out[i][i] = diag[i]
    for i in range(n):
        for j in range(i + 1, n):
            Bij = (B_scalar_exact(x, a, mat_add(basis[i], basis[j])) - diag[i] - diag[j]) / D(2)
            out[i][j] = out[j][i] = +Bij
    return out


def atoms_decimal_xa(x: Decimal, a: Decimal) -> dict[str, Decimal]:
    one = D(1)
    t = a * a
    return {
        "E": (one - x) * ((one - x) * (one - x) - D(2) * t),
        "F": x * (x * x - D(2) * t),
        "U": x * (one - x) * (one - x) + (one - D(2) * x) * t,
        "W": x * (one - x) * (one - x) + D(2) * (one - x) * t,
        "V": x * x * (one - x) + (D(2) * x - one) * t,
        "Z": x * x * (one - x) + D(2) * x * t,
    }


def atoms_decimal_xc(x: Decimal, c: Decimal) -> dict[str, Decimal]:
    a = (x * x * c / D(2)).sqrt()
    return atoms_decimal_xa(x, a)


def logs_nml(
    x: Decimal, a: Decimal, atoms_override: dict[str, Decimal] | None = None
) -> tuple[Decimal, Decimal, Decimal, Decimal]:
    at = atoms_decimal_xa(x, a) if atoms_override is None else atoms_override
    E, U, W, V, Z, F = (at[k] for k in ["E", "U", "W", "V", "Z", "F"])
    ell = (E * V / (U * W)).ln()
    kappa = (E * Z / (U * U)).ln()
    Lam = (F * U * U * W / (E * V * V * Z)).ln()
    n = -ell - x * Lam
    m = -kappa - x * Lam
    q = n * m - D(2) * Lam * Lam * a * a
    return n, m, Lam, q


def B_even_formula(
    x: Decimal,
    a: Decimal,
    omit_full_atom: bool = False,
    atoms_override: dict[str, Decimal] | None = None,
    jF_override: list[Decimal] | None = None,
) -> tuple[list[list[Decimal]], list[Decimal], dict[str, Decimal], tuple[Decimal, Decimal, Decimal, Decimal]]:
    at = atoms_decimal_xa(x, a) if atoms_override is None else atoms_override
    E, U, W, V, Z, F = (at[k] for k in ["E", "U", "W", "V", "Z", "F"])
    t = a * a
    jF = (
        [D(2) * (x * x - t), x * x, -D(4) * x * a, D(2) * t]
        if jF_override is None
        else jF_override
    )
    jQ = [x, x, -D(2) * a, D(0)]

    def add(u: list[Decimal], v: list[Decimal]) -> list[Decimal]:
        return [u[i] + v[i] for i in range(4)]

    def sub(u: list[Decimal], v: list[Decimal]) -> list[Decimal]:
        return [u[i] - v[i] for i in range(4)]

    jE = add([D(4) * x - D(2), D(2) * x - D(1), -D(4) * a, D(0)], [-z for z in jF])
    jU = add([D(1) - D(3) * x, -x, D(2) * a, D(0)], jF)
    jW = add([-D(2) * x, D(1) - D(2) * x, D(4) * a, D(0)], jF)
    jV = sub(jQ, jF)
    jZ = add([D(2) * x, D(0), D(0), D(0)], [-z for z in jF])

    forms = [jE, jU, jW, jV, jZ]
    probs = [E, U, W, V, Z]
    mult = [D(1), D(2), D(1), D(2), D(1)]
    if not omit_full_atom:
        forms.append(jF)
        probs.append(F)
        mult.append(D(1))

    B = [[D(0) for _ in range(4)] for __ in range(4)]
    for form, p, mu in zip(forms, probs, mult):
        for i in range(4):
            for j in range(4):
                B[i][j] += mu * form[i] * form[j] / p
    n, m, Lam, q = logs_nml(x, a, at)
    B[0][1] -= D(2) * n
    B[1][0] -= D(2) * n
    B[2][2] += D(4) * n
    B[0][0] -= D(2) * m
    B[3][3] += D(2) * m
    B[0][2] -= D(4) * Lam * a
    B[2][0] -= D(4) * Lam * a
    B[2][3] += D(4) * Lam * a
    B[3][2] += D(4) * Lam * a
    return B, jF, at, (n, m, Lam, q)


def mat_inv(A: list[list[Decimal]]) -> list[list[Decimal]]:
    n = len(A)
    M = [A[i][:] + [D(1) if i == j else D(0) for j in range(n)] for i in range(n)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        if M[piv][col] == 0:
            raise ZeroDivisionError("singular matrix")
        if piv != col:
            M[col], M[piv] = M[piv], M[col]
        p = M[col][col]
        for j in range(2 * n):
            M[col][j] /= p
        for row in range(n):
            if row == col:
                continue
            f = M[row][col]
            if f == 0:
                continue
            for j in range(2 * n):
                M[row][j] -= f * M[col][j]
    return [row[n:] for row in M]


def mat_det(A: list[list[Decimal]]) -> Decimal:
    n = len(A)
    M = [row[:] for row in A]
    ans = D(1)
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        if M[piv][col] == 0:
            return D(0)
        if piv != col:
            M[col], M[piv] = M[piv], M[col]
            ans = -ans
        p = M[col][col]
        ans *= p
        for row in range(col + 1, n):
            f = M[row][col] / p
            for j in range(col, n):
                M[row][j] -= f * M[col][j]
    return +ans


def ldl_pivots(A: list[list[Decimal]]) -> list[Decimal]:
    n = len(A)
    L = [[D(0) for _ in range(n)] for __ in range(n)]
    piv = [D(0) for _ in range(n)]
    for i in range(n):
        for j in range(i):
            s = sum(L[i][k] * L[j][k] * piv[k] for k in range(j))
            L[i][j] = (A[i][j] - s) / piv[j]
        piv[i] = A[i][i] - sum(L[i][k] * L[i][k] * piv[k] for k in range(i))
        L[i][i] = D(1)
    return [+z for z in piv]


def sigma_from_B(
    x: Decimal,
    a: Decimal,
    B: list[list[Decimal]],
    logs_override: tuple[Decimal, Decimal, Decimal, Decimal] | None = None,
) -> dict[str, Any]:
    n, m, Lam, q = logs_nml(x, a) if logs_override is None else logs_override
    eta = [
        D(2) * (n * m - Lam * Lam * a * a) / (n * q),
        n / q,
        D(4) * Lam * a / q,
        D(2) * Lam * Lam * a * a / (n * q),
    ]
    T0 = [
        [D(1), D(0), D(0)],
        [-eta[0] / eta[1], -eta[2] / eta[1], -eta[3] / eta[1]],
        [D(0), D(1), D(0)],
        [D(0), D(0), D(1)],
    ]
    C0 = [
        [
            sum(T0[i][r] * B[i][j] * T0[j][c] for i in range(4) for j in range(4))
            for c in range(3)
        ]
        for r in range(3)
    ]
    b0 = [sum(T0[i][r] * B[i][1] for i in range(4)) for r in range(3)]
    invC = mat_inv(C0)
    sigma = B[1][1] - sum(b0[i] * invC[i][j] * b0[j] for i in range(3) for j in range(3))
    block = [C0[i][:] + [b0[i]] for i in range(3)] + [b0[:] + [B[1][1]]]
    det_block = mat_det(block)
    detC = mat_det(C0)
    return {
        "sigma": +sigma,
        "eta": eta,
        "C0": C0,
        "C0_pivots": ldl_pivots(C0),
        "detC": detC,
        "det_block": det_block,
        "det_block_minus_detC_sigma": det_block - detC * sigma,
    }


def sigma_xc(x: Decimal, c: Decimal) -> dict[str, Any]:
    a = (x * x * c / D(2)).sqrt()
    B, jF, atoms, logs = B_even_formula(x, a, omit_full_atom=False)
    ans = sigma_from_B(x, a, B)
    ans.update({"x": x, "c": c, "a": a, "B": B, "jF": jF, "atoms": atoms, "logs": logs})
    return ans


def sigma_stable_xs(x: Decimal, s: Decimal) -> dict[str, Any]:
    c = D(1) - s
    one = D(1)
    sqrt_one_minus_s = (one - s).sqrt()
    a = x * sqrt_one_minus_s / D(2).sqrt()
    atoms = {
        "E": (one - x) * (one - D(2) * x + x * x * s),
        "F": x * x * x * s,
        "U": x * ((one - x) * (one - x) + (one - D(2) * x) * x * (one - s) / D(2)),
        "W": x * (one - x) * (one - x * s),
        "V": x * x * (one + (one - D(2) * x) * s) / D(2),
        "Z": x * x * (one - x * s),
    }
    jF_boundary = [
        x * x * (one + s),
        x * x,
        -D(2) * D(2).sqrt() * x * x * sqrt_one_minus_s,
        x * x * (one - s),
    ]
    R, jF, atoms, logs = B_even_formula(
        x,
        a,
        omit_full_atom=True,
        atoms_override=atoms,
        jF_override=jF_boundary,
    )
    sig_R = sigma_from_B(x, a, R, logs_override=logs)
    n, m, Lam, q = logs
    eta = sig_R["eta"]
    T0 = [
        [D(1), D(0), D(0)],
        [-eta[0] / eta[1], -eta[2] / eta[1], -eta[3] / eta[1]],
        [D(0), D(1), D(0)],
        [D(0), D(0), D(1)],
    ]
    C = sig_R["C0"]
    b = [sum(T0[i][r] * R[i][1] for i in range(4)) for r in range(3)]
    invC = mat_inv(C)
    Cinv_b = [sum(invC[i][j] * b[j] for j in range(3)) for i in range(3)]
    base = R[1][1] - sum(b[i] * Cinv_b[i] for i in range(3))
    u = [sum(T0[i][r] * jF[i] for i in range(4)) for r in range(3)]
    v = jF[1]
    Cinv_u = [sum(invC[i][j] * u[j] for j in range(3)) for i in range(3)]
    denom = atoms["F"] + sum(u[i] * Cinv_u[i] for i in range(3))
    residual = v - sum(u[i] * Cinv_b[i] for i in range(3))
    correction = residual * residual / denom
    return {
        "sigma_stable": +(base + correction),
        "base_without_full_atom": +base,
        "rank_one_correction": +correction,
        "rank_one_denom": +denom,
        "residual": +residual,
        "F_atom": atoms["F"],
        "x": x,
        "s": s,
        "c": c,
        "a": a,
        "jF": jF,
        "atoms": atoms,
        "logs": logs,
        "eta": eta,
    }


def max_abs_matrix(A: list[list[Decimal]]) -> Decimal:
    return max(abs(z) for row in A for z in row)


def sub_matrix(A: list[list[Decimal]], B: list[list[Decimal]]) -> list[list[Decimal]]:
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def scan_sigma_strings(obj: Any) -> dict[str, Any]:
    count = 0
    neg = 0
    min_seen: tuple[Decimal, str] | None = None

    def rec(x: Any, path: str) -> None:
        nonlocal count, neg, min_seen
        if isinstance(x, dict):
            if "sigma" in x:
                try:
                    val = D(str(x["sigma"]))
                    count += 1
                    if val <= 0:
                        neg += 1
                    if min_seen is None or val < min_seen[0]:
                        min_seen = (val, path + ".sigma")
                except Exception:
                    pass
            for k, v in x.items():
                rec(v, f"{path}.{k}")
        elif isinstance(x, list):
            for i, v in enumerate(x):
                rec(v, f"{path}[{i}]")

    rec(obj, "$")
    return {
        "sigma_fields_seen": count,
        "nonpositive_sigma_fields": neg,
        "min_sigma_seen": None if min_seen is None else str(min_seen[0]),
        "min_sigma_path": None if min_seen is None else min_seen[1],
    }


def exact_atom_and_hessian_checks() -> dict[str, Any]:
    samples = [
        ("interior_rational", Fraction(1, 3), Fraction(1, 5)),
        ("near_boundary_rational", Fraction(1, 3), Fraction(7, 30)),
        ("centered_rational", Fraction(1, 2), Fraction(1, 4)),
    ]
    rows = []
    for label, x, a in samples:
        zero = mat_zero()
        p0, _, _ = event_jets_fraction(x, a, zero)
        p_formula = atoms_formula_fraction(x, a)
        atom_diff = [p0[i] - p_formula[i] for i in range(8)]
        B_exact_even = B_matrix_exact(x, a, EVEN_BASIS)
        B_formula, jF, atoms, logs = B_even_formula(dec_frac(x), dec_frac(a))
        B_diff = sub_matrix(B_exact_even, B_formula)
        combo_basis = EVEN_BASIS + ODD_BASIS
        B_combo = B_matrix_exact(x, a, combo_basis)
        cross = [[B_combo[i][j] for j in range(4, 6)] for i in range(4)]
        odd = [[B_combo[i][j] for j in range(4, 6)] for i in range(4, 6)]
        sig = sigma_from_B(dec_frac(x), dec_frac(a), B_formula)

        # Full atom derivative checked directly from exact-event jets.
        full_derivatives = []
        for E in EVEN_BASIS:
            _, p1, _ = event_jets_fraction(x, a, E)
            full_derivatives.append(p1[7])
        jf_fraction_formula = [
            2 * (x * x - a * a),
            x * x,
            -4 * x * a,
            2 * a * a,
        ]
        rows.append(
            {
                "label": label,
                "x": str(x),
                "a": str(a),
                "c": str(2 * a * a / (x * x)),
                "strict_domain_x_minus_sqrt2a_positive": float(x) > (2 ** 0.5) * float(a),
                "strict_domain_x_plus_sqrt2a_below_one": float(x) + (2 ** 0.5) * float(a) < 1,
                "atoms_match_exactly": all(z == 0 for z in atom_diff),
                "min_atom": str(min(p0)),
                "sum_atoms_minus_1": str(sum(p0) - 1),
                "B_even_formula_vs_exact_max_abs": fmt(max_abs_matrix(B_diff), 35),
                "reflection_even_odd_cross_max_abs": fmt(max_abs_matrix(cross), 35),
                "odd_block_pivots": [fmt(z, 35) for z in ldl_pivots(odd)],
                "odd_block_positive_sample": all(z > 0 for z in ldl_pivots(odd)),
                "full_atom_jF_derivatives_match_exactly": full_derivatives == jf_fraction_formula,
                "sigma": fmt(sig["sigma"], 45),
                "C0_pivots": [fmt(z, 35) for z in sig["C0_pivots"]],
                "det_block_minus_detC_sigma": fmt(sig["det_block_minus_detC_sigma"], 35),
                "eta_e_positive": sig["eta"][1] > 0,
            }
        )
    return {"samples": rows}


def rectangular_and_c0_checks() -> dict[str, Any]:
    rect_samples = [
        (D("0.10"), D("0.01")),
        (D("0.10"), D("0.99")),
        (D("0.49"), D("0.25")),
        (D("0.5"), D("0.999")),
    ]
    rect = []
    for x, c in rect_samples:
        a = (x * x * c / D(2)).sqrt()
        root_c = c.sqrt()
        atoms = atoms_decimal_xc(x, c)
        rect.append(
            {
                "x": str(x),
                "c": str(c),
                "a": fmt(a, 25),
                "lambda_min_formula_x_1_minus_sqrtc": fmt(x * (D(1) - root_c), 25),
                "lambda_max_formula_x_1_plus_sqrtc": fmt(x * (D(1) + root_c), 25),
                "all_atoms_positive": all(v > 0 for v in atoms.values()),
                "min_atom": fmt(min(atoms.values()), 25),
            }
        )

    c0_rows = []
    for x in [D("0.1"), D("0.25"), D("0.49"), D("0.5")]:
        limit = D(1) / (x * (D(1) - x))
        vals = []
        for c in [D("1e-4"), D("1e-8"), D("1e-12")]:
            s = sigma_xc(x, c)
            vals.append(
                {
                    "c": str(c),
                    "sigma": fmt(s["sigma"], 45),
                    "sigma_minus_limit": fmt(s["sigma"] - limit, 35),
                }
            )
        c0_rows.append({"x": str(x), "limit_1_over_x1mx": fmt(limit, 45), "values": vals})
    return {"rectangular_domain_samples": rect, "c_to_zero_limit_samples": c0_rows}


def boundary_checks() -> dict[str, Any]:
    # Unique full-atom vanishing at fixed x<1/2.
    fixed_x_rows = []
    for x in [D("0.1"), D("0.25"), D("0.49")]:
        s0_atoms = {
            "E": (D(1) - x) * (D(1) - D(2) * x),
            "F": D(0),
            "U": x * (D(1) - D(3) * x / D(2)),
            "W": x * (D(1) - x),
            "V": x * x / D(2),
            "Z": x * x,
        }
        fixed_x_rows.append(
            {
                "x": str(x),
                "F_at_s0": fmt(s0_atoms["F"], 20),
                "E_at_s0": fmt(s0_atoms["E"], 25),
                "U_at_s0": fmt(s0_atoms["U"], 25),
                "W_at_s0": fmt(s0_atoms["W"], 25),
                "V_at_s0": fmt(s0_atoms["V"], 25),
                "Z_at_s0": fmt(s0_atoms["Z"], 25),
                "only_F_zero": s0_atoms["F"] == 0 and min(
                    s0_atoms[k] for k in ["E", "U", "W", "V", "Z"]
                )
                > 0,
            }
        )

    sm_samples = []
    for x, s in [(D("0.1"), D("1e-6")), (D("0.25"), D("1e-10")), (D("0.01"), D("1e-8"))]:
        direct = sigma_xc(x, D(1) - s)
        stable = sigma_stable_xs(x, s)
        sm_samples.append(
            {
                "x": str(x),
                "s": str(s),
                "F_expected_x3s": fmt(x * x * x * s, 35),
                "F_atom": fmt(stable["F_atom"], 35),
                "rank_one_prefactor_x_over_s": fmt(x / s, 25),
                "direct_sigma": fmt(direct["sigma"], 45),
                "stable_sigma": fmt(stable["sigma_stable"], 45),
                "direct_minus_stable": fmt(direct["sigma"] - stable["sigma_stable"], 35),
                "rank_one_denom": fmt(stable["rank_one_denom"], 35),
            }
        )

    power_rows = []
    for p in [D("0.5"), D("1"), D("2"), D("4"), D("8")]:
        vals = []
        for k in [2, 3, 4, 5]:
            x = D(10) ** (-k)
            s = x ** p
            stable = sigma_stable_xs(x, s)
            vals.append(
                {
                    "x": str(x),
                    "s": fmt(s, 20),
                    "x_sigma": fmt(x * stable["sigma_stable"], 35),
                    "sigma": fmt(stable["sigma_stable"], 35),
                }
            )
        power_rows.append({"p": str(p), "values": vals})

    beta_rows = []
    best = None
    x_ref = D("1e-4")
    for beta in [D(j) / D(100) for j in range(20, 101, 5)]:
        s = (-beta / x_ref).exp()
        stable = sigma_stable_xs(x_ref, s)
        row = {
            "beta": str(beta),
            "x": str(x_ref),
            "s": fmt(s, 25),
            "sigma": fmt(stable["sigma_stable"], 45),
            "base": fmt(stable["base_without_full_atom"], 35),
            "rank_one_correction": fmt(stable["rank_one_correction"], 35),
        }
        beta_rows.append(row)
        sig = stable["sigma_stable"]
        if best is None or sig < D(best["sigma_raw"]):
            row["sigma_raw"] = str(sig)
            best = row.copy()

    beta = D("0.58")
    x = D("1e-4")
    s = (-beta / x).exp()
    stable = sigma_stable_xs(x, s)
    n, m, Lam, q = stable["logs"]
    log2 = D(2).ln()
    eta_limit = [
        (beta + 2 * log2) / (log2 * (beta + log2)),
        (beta + log2) / (beta * log2),
        -D(2) * D(2).sqrt() / log2,
        beta / (log2 * (beta + log2)),
    ]
    eta = stable["eta"]
    exp_limit_check = {
        "beta": str(beta),
        "x": str(x),
        "Lambda_plus_beta_over_x": fmt(Lam + beta / x, 35),
        "log4": fmt(D(4).ln(), 35),
        "n_minus_beta_minus_log2": fmt(n - beta - log2, 35),
        "m_minus_beta": fmt(m - beta, 35),
        "q_minus_beta_log2": fmt(q - beta * log2, 35),
        "eta_minus_limit": [fmt(eta[i] - eta_limit[i], 35) for i in range(4)],
        "sigma": fmt(stable["sigma_stable"], 45),
    }

    return {
        "fixed_x_s0_unique_full_atom": fixed_x_rows,
        "sherman_morrison_direct_comparison": sm_samples,
        "power_scale_samples": power_rows,
        "exponential_beta_samples_at_x_1e_minus_4": {
            "count": len(beta_rows),
            "best_in_this_audit_grid": best,
            "values": beta_rows,
        },
        "exponential_limit_eta_check_beta_0p58": exp_limit_check,
    }


def author_json_scans() -> dict[str, Any]:
    out = {}
    for name, path in {
        "profile": GLOBAL_DIR / "profile.json",
        "boundary_asymptotic": BOUNDARY_DIR / "asymptotic_results.json",
    }.items():
        if not path.exists():
            out[name] = {"exists": False}
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        out[name] = {
            "exists": True,
            "sha256": sha256(path),
            "status": data.get("status"),
            "scan_sigma_fields": scan_sigma_strings(data),
        }
        if name == "profile":
            out[name]["grid_denominator"] = data.get("grid_denominator")
            out[name]["float_scout"] = {
                "seed": data.get("float_scout", {}).get("seed"),
                "proposals": data.get("float_scout", {}).get("proposals"),
                "negative_hits": data.get("float_scout", {}).get("negative_hits"),
            }
        if name == "boundary_asymptotic":
            out[name]["beta_refinement_count"] = data.get("beta_refinement_at_x_1e_minus_4", {}).get("count")
            out[name]["beta_refinement_best"] = data.get("beta_refinement_at_x_1e_minus_4", {}).get("best")
    return out


def collect_hashes() -> dict[str, str]:
    files = [
        SUBFAMILY_DIR / "frozen_problem.md",
        SUBFAMILY_DIR / "derivation.md",
        SUBFAMILY_DIR / "proof_or_blocker.md",
        SUBFAMILY_DIR / "verdict.md",
        SUBFAMILY_DIR / "audit_nonauthor" / "verdict.md",
        GLOBAL_DIR / "frozen_problem.md",
        GLOBAL_DIR / "derivation.md",
        GLOBAL_DIR / "verdict.md",
        GLOBAL_DIR / "run_log.md",
        GLOBAL_DIR / "search.py",
        GLOBAL_DIR / "profile.json",
        BOUNDARY_DIR / "analysis.md",
        BOUNDARY_DIR / "verdict.md",
        BOUNDARY_DIR / "run_log.md",
        BOUNDARY_DIR / "asymptotic_probe.py",
        BOUNDARY_DIR / "asymptotic_results.json",
    ]
    return {
        str(path.relative_to(GLOBAL_ROOT)): sha256(path)
        for path in files
        if path.exists()
    }


def main() -> None:
    exact_checks = exact_atom_and_hessian_checks()
    rect_checks = rectangular_and_c0_checks()
    boundary = boundary_checks()
    author_scans = author_json_scans()

    booleans = {
        "exact_atoms_all_samples": all(r["atoms_match_exactly"] for r in exact_checks["samples"]),
        "B_even_formula_matches_exact_event_samples": all(
            D(r["B_even_formula_vs_exact_max_abs"]) < D("1e-140")
            for r in exact_checks["samples"]
        ),
        "reflection_cross_zero_samples": all(
            D(r["reflection_even_odd_cross_max_abs"]) < D("1e-140")
            for r in exact_checks["samples"]
        ),
        "odd_block_positive_samples": all(r["odd_block_positive_sample"] for r in exact_checks["samples"]),
        "jF_full_atom_derivatives_exact": all(
            r["full_atom_jF_derivatives_match_exactly"] for r in exact_checks["samples"]
        ),
        "sigma_schur_det_relation_samples": all(
            abs(D(r["det_block_minus_detC_sigma"])) < D("1e-125")
            for r in exact_checks["samples"]
        ),
        "rectangular_samples_strict_positive": all(
            r["all_atoms_positive"] for r in rect_checks["rectangular_domain_samples"]
        ),
        "fixed_x_s0_only_F_zero": all(
            r["only_F_zero"] for r in boundary["fixed_x_s0_unique_full_atom"]
        ),
        "SM_matches_direct_on_moderate_boundary_samples": all(
            abs(D(r["direct_minus_stable"])) < D("1e-120")
            for r in boundary["sherman_morrison_direct_comparison"]
        ),
        "independent_boundary_samples_positive": (
            all(
                D(v["sigma"]) > 0
                for row in boundary["power_scale_samples"]
                for v in row["values"]
            )
            and all(
                D(v["sigma"]) > 0
                for v in boundary["exponential_beta_samples_at_x_1e_minus_4"]["values"]
            )
        ),
        "author_profile_exposed_sigmas_nonnegative": (
            author_scans.get("profile", {}).get("scan_sigma_fields", {}).get("nonpositive_sigma_fields") == 0
        ),
        "author_boundary_exposed_sigmas_nonnegative": (
            author_scans.get("boundary_asymptotic", {}).get("scan_sigma_fields", {}).get("nonpositive_sigma_fields") == 0
        ),
    }

    result = {
        "status": "INCOMPLETE_GLOBAL_SIGMA_OPEN__AUDITED_IDENTITIES_PASS",
        "precision_decimal_digits": getcontext().prec,
        "input_hashes_sha256": collect_hashes(),
        "author_json_scans": author_scans,
        "exact_event_mobius_and_hessian_checks": exact_checks,
        "rectangular_domain_and_c_to_zero_checks": rect_checks,
        "boundary_full_atom_checks": boundary,
        "classification": {
            "analytic_identities": "PASS on independent exact-event/Mobius rational samples and Decimal Schur checks.",
            "asymptotic_candidates": "Plausible and internally consistent, but fixed-x leading coefficient and exponential phi(beta)>0 remain unproved.",
            "finite_scout": "Author profiles and this audit's independent samples show no negative sigma, but this is not an interval proof.",
            "global_sigma": "OPEN; do not upgrade sigma(x,c)>0 on the full rectangle to a theorem.",
        },
        "checks": booleans,
        "overall": "AUDIT_PASS_WITH_OPEN_GLOBAL_INEQUALITY" if all(booleans.values()) else "AUDIT_GAP_OR_INCOMPLETE",
    }

    out = AUDIT_DIR / "audit_results.json"
    with out.open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False, default=jdefault)
        f.write("\n")
    print(json.dumps({"overall": result["overall"], "out": str(out)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
