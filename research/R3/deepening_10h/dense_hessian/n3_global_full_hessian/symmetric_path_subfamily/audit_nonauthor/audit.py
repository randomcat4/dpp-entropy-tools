#!/usr/bin/env python3
"""Independent audit for D10-U10d symmetric_path_subfamily.

This script deliberately does not import the author's sanity.py or any
research module.  It rebuilds n=3 exact-event probabilities from the
inclusion-probability Möbius formula, differentiates them as polynomials
along arbitrary real-symmetric directions, and checks the algebraic claims
used in the centered symmetric-path proof.
"""

from __future__ import annotations

import hashlib
import json
import os
from decimal import Decimal, getcontext
from fractions import Fraction
from itertools import permutations
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple


getcontext().prec = 150

TARGET = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent

MASKS = list(range(8))
EVENT_ORDER = ["empty", "1", "2", "12", "3", "13", "23", "123"]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def dec(q: Fraction | int) -> Decimal:
    if isinstance(q, int):
        return Decimal(q)
    return Decimal(q.numerator) / Decimal(q.denominator)


def dabs(x: Decimal) -> Decimal:
    return x.copy_abs()


def popcount(mask: int) -> int:
    return int(mask.bit_count())


def indices(mask: int) -> List[int]:
    return [i for i in range(3) if (mask >> i) & 1]


def poly_add(a: Sequence[Fraction], b: Sequence[Fraction]) -> List[Fraction]:
    n = max(len(a), len(b))
    out = [Fraction(0) for _ in range(n)]
    for i, v in enumerate(a):
        out[i] += v
    for i, v in enumerate(b):
        out[i] += v
    return out


def poly_mul(a: Sequence[Fraction], b: Sequence[Fraction], deg: int = 3) -> List[Fraction]:
    out = [Fraction(0) for _ in range(deg + 1)]
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            if i + j <= deg:
                out[i + j] += ai * bj
    return out


def perm_sign(p: Sequence[int]) -> int:
    inv = 0
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            inv += p[i] > p[j]
    return -1 if inv % 2 else 1


def det_poly(k: Sequence[Sequence[Fraction]], d: Sequence[Sequence[Fraction]], mask: int) -> List[Fraction]:
    idx = indices(mask)
    m = len(idx)
    if m == 0:
        return [Fraction(1), Fraction(0), Fraction(0), Fraction(0)]
    out = [Fraction(0), Fraction(0), Fraction(0), Fraction(0)]
    for p in permutations(range(m)):
        term = [Fraction(1)]
        for row_local, col_local in enumerate(p):
            i = idx[row_local]
            j = idx[col_local]
            term = poly_mul(term, [k[i][j], d[i][j]], 3)
        if perm_sign(p) < 0:
            term = [-v for v in term]
        out = poly_add(out, term)
    out += [Fraction(0)] * (4 - len(out))
    return out[:4]


def atom_polys(k: Sequence[Sequence[Fraction]], d: Sequence[Sequence[Fraction]]) -> Dict[int, List[Fraction]]:
    """p_S(t)=sum_{A superset S} (-1)^{|A|-|S|} det(K_A+tD_A)."""
    dets = {mask: det_poly(k, d, mask) for mask in MASKS}
    atoms: Dict[int, List[Fraction]] = {}
    for s in MASKS:
        acc = [Fraction(0), Fraction(0), Fraction(0), Fraction(0)]
        for a in MASKS:
            if (a & s) == s:
                term = dets[a]
                sign = -1 if (popcount(a) - popcount(s)) % 2 else 1
                if sign < 0:
                    term = [-v for v in term]
                acc = poly_add(acc, term)
        atoms[s] = acc[:4]
    return atoms


def atom_jets(k: Sequence[Sequence[Fraction]], d: Sequence[Sequence[Fraction]]) -> Tuple[Dict[int, Fraction], Dict[int, Fraction], Dict[int, Fraction]]:
    polys = atom_polys(k, d)
    p0 = {s: polys[s][0] for s in MASKS}
    p1 = {s: polys[s][1] for s in MASKS}
    p2 = {s: 2 * polys[s][2] for s in MASKS}
    return p0, p1, p2


def k_path(x: Fraction, a: Fraction) -> List[List[Fraction]]:
    return [
        [x, a, Fraction(0)],
        [a, x, a],
        [Fraction(0), a, x],
    ]


def zero3() -> List[List[Fraction]]:
    return [[Fraction(0) for _ in range(3)] for _ in range(3)]


def mat_add(a: Sequence[Sequence[Fraction]], b: Sequence[Sequence[Fraction]]) -> List[List[Fraction]]:
    return [[a[i][j] + b[i][j] for j in range(3)] for i in range(3)]


def mat_scale(c: Fraction, a: Sequence[Sequence[Fraction]]) -> List[List[Fraction]]:
    return [[c * a[i][j] for j in range(3)] for i in range(3)]


def sym_dir(d11=0, d22=0, d33=0, d12=0, d13=0, d23=0) -> List[List[Fraction]]:
    return [
        [Fraction(d11), Fraction(d12), Fraction(d13)],
        [Fraction(d12), Fraction(d22), Fraction(d23)],
        [Fraction(d13), Fraction(d23), Fraction(d33)],
    ]


FULL_BASIS = [
    sym_dir(d11=1),
    sym_dir(d22=1),
    sym_dir(d33=1),
    sym_dir(d12=1),
    sym_dir(d13=1),
    sym_dir(d23=1),
]

EVEN_BASIS = [
    sym_dir(d11=1, d33=1),      # d
    sym_dir(d22=1),             # e
    sym_dir(d12=1, d23=1),      # h
    sym_dir(d13=1),             # k
]

ODD_BASIS = [
    sym_dir(d11=1, d33=-1),     # d
    sym_dir(d12=1, d23=-1),     # h
]

CORE_BASIS = [EVEN_BASIS[0], EVEN_BASIS[1], EVEN_BASIS[3]]


def q_negative_entropy_hessian(k: Sequence[Sequence[Fraction]], d: Sequence[Sequence[Fraction]]) -> Decimal:
    p0, p1, p2 = atom_jets(k, d)
    assert sum(p0.values(), Fraction(0)) == 1
    assert sum(p1.values(), Fraction(0)) == 0
    assert sum(p2.values(), Fraction(0)) == 0
    total = Decimal(0)
    for s in MASKS:
        if p0[s] <= 0:
            raise ValueError(f"nonpositive atom {s}: {p0[s]}")
        total += dec(p1[s] * p1[s] / p0[s])
        total += dec(p2[s]) * dec(p0[s]).ln()
    return total


def bilinear(k: Sequence[Sequence[Fraction]], a: Sequence[Sequence[Fraction]], b: Sequence[Sequence[Fraction]]) -> Decimal:
    return (q_negative_entropy_hessian(k, mat_add(a, b))
            - q_negative_entropy_hessian(k, a)
            - q_negative_entropy_hessian(k, b)) / Decimal(2)


def gram(k: Sequence[Sequence[Fraction]], basis: Sequence[Sequence[Sequence[Fraction]]]) -> List[List[Decimal]]:
    n = len(basis)
    out = [[Decimal(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        out[i][i] = q_negative_entropy_hessian(k, basis[i])
        for j in range(i + 1, n):
            out[i][j] = out[j][i] = bilinear(k, basis[i], basis[j])
    return out


def ldl_pivots_fraction(a: Sequence[Sequence[Fraction]]) -> List[Fraction]:
    n = len(a)
    L = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    D = [Fraction(0) for _ in range(n)]
    for i in range(n):
        for j in range(i):
            s = sum(L[i][k] * L[j][k] * D[k] for k in range(j))
            L[i][j] = (a[i][j] - s) / D[j]
        D[i] = a[i][i] - sum(L[i][k] * L[i][k] * D[k] for k in range(i))
        L[i][i] = 1
    return D


def ldl_pivots_decimal(a: Sequence[Sequence[Decimal]]) -> List[Decimal]:
    n = len(a)
    L = [[Decimal(0) for _ in range(n)] for _ in range(n)]
    D = [Decimal(0) for _ in range(n)]
    for i in range(n):
        for j in range(i):
            s = sum(L[i][k] * L[j][k] * D[k] for k in range(j))
            L[i][j] = (a[i][j] - s) / D[j]
        D[i] = a[i][i] - sum(L[i][k] * L[i][k] * D[k] for k in range(i))
        L[i][i] = Decimal(1)
    return D


def subtract_from_identity(k: Sequence[Sequence[Fraction]]) -> List[List[Fraction]]:
    return [[(Fraction(1) if i == j else Fraction(0)) - k[i][j] for j in range(3)] for i in range(3)]


def claimed_atoms(x: Fraction, a: Fraction) -> List[Fraction]:
    t = a * a
    E = (1 - x) * ((1 - x) * (1 - x) - 2 * t)
    F = x * (x * x - 2 * t)
    U = x * (1 - x) * (1 - x) + (1 - 2 * x) * t
    W = x * (1 - x) * (1 - x) + 2 * (1 - x) * t
    V = x * x * (1 - x) + (2 * x - 1) * t
    Z = x * x * (1 - x) + 2 * x * t
    return [E, U, W, V, U, Z, V, F]


def claimed_even_atom_derivatives(x: Fraction, a: Fraction, d: Fraction, e: Fraction, h: Fraction, kk: Fraction) -> List[Fraction]:
    t = a * a
    jF = 2 * (x * x - t) * d + x * x * e - 4 * x * a * h + 2 * t * kk
    jQ = x * (d + e) - 2 * a * h
    jE = (4 * x - 2) * d + (2 * x - 1) * e - 4 * a * h - jF
    jU = (1 - 3 * x) * d - x * e + 2 * a * h + jF
    jW = -2 * x * d + (1 - 2 * x) * e + 4 * a * h + jF
    jV = jQ - jF
    jZ = 2 * x * d - jF
    return [jE, jU, jW, jV, jU, jZ, jV, jF]


def centered_core_claim_matrix(a: Fraction) -> Tuple[List[List[Decimal]], Dict[str, Decimal]]:
    r = dec(8 * a * a)
    u = r * r
    L = Decimal(1) - u
    v = Decimal(2) - u
    n = ((Decimal(1) + r) / (Decimal(1) - r)).ln()
    m = -(Decimal(1) - u).ln()
    C = [
        [Decimal(4) - 2 * u - u * u - m * L, r * v - n * L, u * u],
        [r * v - n * L, v, r * u],
        [u * u, r * u, u * v + m * L],
    ]
    B = [[(Decimal(2) / L) * C[i][j] for j in range(3)] for i in range(3)]
    z = r * n - m
    det_formula = (m * (Decimal(8) - L * n * n) + Decimal(8) * u * z + Decimal(16) * u - v * z * z) / v
    Tkk = m + Decimal(4) * u / v
    lower = Decimal(4) * m + Decimal(12) * u
    return B, {
        "r": r,
        "u": u,
        "L": L,
        "v": v,
        "n": n,
        "m": m,
        "z": z,
        "L_n2": L * n * n,
        "det_T_formula": det_formula,
        "Tkk": Tkk,
        "det_numerator_lower": lower,
    }


def core_fisher_claim_q(a: Fraction, d: Fraction, e: Fraction, kk: Fraction) -> Decimal:
    r = dec(8 * a * a)
    n = ((Decimal(1) + r) / (Decimal(1) - r)).ln()
    m = -((Decimal(1) - r * r)).ln()
    dd, ee, kv = dec(d), dec(e), dec(kk)
    fisher = (((Decimal(2) - r) * dd + ee + r * kv) ** 2 / (Decimal(1) - r)
              + Decimal(2) * (r * dd + ee - r * kv) ** 2
              + ((Decimal(2) + r) * dd - ee - r * kv) ** 2 / (Decimal(1) + r))
    return fisher - Decimal(4) * n * dd * ee - Decimal(2) * m * dd * dd + Decimal(2) * m * kv * kv


def max_abs_matrix(a: Sequence[Sequence[Decimal]]) -> str:
    if not a:
        return "0"
    return str(max(dabs(x) for row in a for x in row))


def matmul_decimal(A: Sequence[Sequence[Decimal]], B: Sequence[Sequence[Decimal]]) -> List[List[Decimal]]:
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def transpose_decimal(A: Sequence[Sequence[Decimal]]) -> List[List[Decimal]]:
    return [list(row) for row in zip(*A)]


def claimed_even_B_value(x: Fraction, a: Fraction, d: Fraction, e: Fraction, h: Fraction, kk: Fraction) -> Decimal:
    atoms = claimed_atoms(x, a)
    j = claimed_even_atom_derivatives(x, a, d, e, h, kk)
    E, U, W, V, _, Z, _, F = [dec(v) for v in atoms]
    jd = [dec(v) for v in j]
    fisher = (jd[0] ** 2 / E + Decimal(2) * jd[1] ** 2 / U + jd[2] ** 2 / W
              + Decimal(2) * jd[3] ** 2 / V + jd[5] ** 2 / Z + jd[7] ** 2 / F)
    ell = (E * V / (U * W)).ln()
    kappa = (E * Z / (U * U)).ln()
    Lam = (F * U * U * W / (E * V * V * Z)).ln()
    n = -ell - Lam * dec(x)
    m = -kappa - Lam * dec(x)
    return (fisher - Decimal(4) * n * dec(d) * dec(e) + Decimal(4) * n * dec(h) * dec(h)
            - Decimal(2) * m * dec(d) * dec(d) + Decimal(2) * m * dec(kk) * dec(kk)
            - Decimal(8) * Lam * dec(a) * dec(h) * (dec(d) - dec(kk)))


class Poly:
    def __init__(self, terms=None):
        self.terms: Dict[Tuple[int, int, int], Fraction] = {}
        if terms:
            for k, v in terms.items():
                if v:
                    self.terms[k] = Fraction(v)

    @staticmethod
    def c(v: int | Fraction) -> "Poly":
        return Poly({(0, 0, 0): Fraction(v)}) if v else Poly()

    @staticmethod
    def var(i: int) -> "Poly":
        exp = [0, 0, 0]
        exp[i] = 1
        return Poly({tuple(exp): Fraction(1)})

    def __add__(self, other) -> "Poly":
        other = as_poly(other)
        out = dict(self.terms)
        for k, v in other.terms.items():
            out[k] = out.get(k, Fraction(0)) + v
            if out[k] == 0:
                del out[k]
        return Poly(out)

    def __radd__(self, other) -> "Poly":
        return self + other

    def __neg__(self) -> "Poly":
        return Poly({k: -v for k, v in self.terms.items()})

    def __sub__(self, other) -> "Poly":
        return self + (-as_poly(other))

    def __rsub__(self, other) -> "Poly":
        return as_poly(other) + (-self)

    def __mul__(self, other) -> "Poly":
        other = as_poly(other)
        out: Dict[Tuple[int, int, int], Fraction] = {}
        for a, av in self.terms.items():
            for b, bv in other.terms.items():
                k = (a[0] + b[0], a[1] + b[1], a[2] + b[2])
                out[k] = out.get(k, Fraction(0)) + av * bv
        return Poly(out)

    def __rmul__(self, other) -> "Poly":
        return self * other

    def __pow__(self, n: int) -> "Poly":
        out = Poly.c(1)
        for _ in range(n):
            out = out * self
        return out

    def __repr__(self) -> str:
        return repr(self.terms)


def as_poly(v) -> Poly:
    if isinstance(v, Poly):
        return v
    return Poly.c(v)


def symbolic_center_identities() -> Dict[str, object]:
    r = Poly.var(0)
    n = Poly.var(1)
    m = Poly.var(2)
    u = r * r
    L = 1 - u
    v = 2 - u
    z = r * n - m
    Cdd = 4 - 2 * u - u * u - m * L
    Cde = r * v - n * L
    Cdk = u * u
    Cee = v
    Cek = r * u
    Ckk = u * v + m * L
    vSdd = Cdd * v - Cde * Cde
    vSdk = Cdk * v - Cde * Cek
    vSkk = Ckk * v - Cek * Cek
    A = v * (4 + 2 * r * n - m) - L * n * n
    B = r * r * r * n
    C = v * m + 4 * u
    residuals = {
        "Schur_dd_v_times": (vSdd - L * A).terms,
        "Schur_dk_v_times": (vSdk - L * B).terms,
        "Schur_kk_v_times": (vSkk - L * C).terms,
        "detT_numerator": (A * C - B * B - v * (m * (8 - L * n * n) + 8 * u * z + 16 * u - v * z * z)).terms,
    }
    return {
        "all_zero": all(not value for value in residuals.values()),
        "residuals": {k: {str(mon): str(coef) for mon, coef in value.items()} for k, value in residuals.items()},
    }


def run() -> Dict[str, object]:
    input_files = ["frozen_problem.md", "proof_or_blocker.md", "derivation.md", "verdict.md", "run_log.md", "sanity.json"]
    hashes = {name: sha256(TARGET / name) for name in input_files if (TARGET / name).exists()}

    # Exact atom formula check at rational points not copied from the author's
    # 16-row denominator.
    atom_samples = [
        (Fraction(2, 5), Fraction(1, 9)),
        (Fraction(1, 3), Fraction(1, 7)),
        (Fraction(3, 5), Fraction(-1, 8)),
        (Fraction(1, 2), Fraction(3, 20)),
    ]
    atom_checks = []
    for x, a in atom_samples:
        k = k_path(x, a)
        p0, _, _ = atom_jets(k, zero3())
        listed = [p0[m] for m in MASKS]
        claimed = claimed_atoms(x, a)
        atom_checks.append({
            "x": str(x),
            "a": str(a),
            "matches_claimed_formula": listed == claimed,
            "all_atoms_positive": all(v > 0 for v in listed),
            "sum": str(sum(listed, Fraction(0))),
            "p": [str(v) for v in listed],
            "K_ldl": [str(v) for v in ldl_pivots_fraction(k)],
            "I_minus_K_ldl": [str(v) for v in ldl_pivots_fraction(subtract_from_identity(k))],
        })

    # General-x even derivative and B_even formula check.
    even_formula_checks = []
    even_samples = [
        (Fraction(2, 5), Fraction(1, 9), (Fraction(3, 7), Fraction(-2, 5), Fraction(1, 6), Fraction(5, 11))),
        (Fraction(1, 3), Fraction(1, 7), (Fraction(-1, 4), Fraction(5, 8), Fraction(-2, 9), Fraction(1, 3))),
        (Fraction(3, 5), Fraction(-1, 8), (Fraction(2, 9), Fraction(1, 5), Fraction(3, 10), Fraction(-4, 7))),
    ]
    for x, a, coords in even_samples:
        d, e, h, kk = coords
        D = mat_add(mat_add(mat_scale(d, EVEN_BASIS[0]), mat_scale(e, EVEN_BASIS[1])),
                    mat_add(mat_scale(h, EVEN_BASIS[2]), mat_scale(kk, EVEN_BASIS[3])))
        p0, p1, _ = atom_jets(k_path(x, a), D)
        claimed_j = claimed_even_atom_derivatives(x, a, d, e, h, kk)
        exact_B = q_negative_entropy_hessian(k_path(x, a), D)
        formula_B = claimed_even_B_value(x, a, d, e, h, kk)
        even_formula_checks.append({
            "x": str(x),
            "a": str(a),
            "coords_d_e_h_k": [str(v) for v in coords],
            "derivatives_match": [p1[m] for m in MASKS] == claimed_j,
            "B_even_abs_error": str(dabs(exact_B - formula_B)),
        })

    # Reflection splitting, centered h separation, core matrix and Schur checks.
    center_samples = [Fraction(1, 12), Fraction(3, 20), Fraction(5, 16), Fraction(7, 20)]
    center_checks = []
    for a in center_samples:
        k = k_path(Fraction(1, 2), a)
        full_pivots = ldl_pivots_decimal(gram(k, FULL_BASIS))
        even = gram(k, EVEN_BASIS)
        odd = gram(k, ODD_BASIS)
        cross_even_odd = [[bilinear(k, e, o) for o in ODD_BASIS] for e in EVEN_BASIS]
        h_core_cross = [even[2][i] for i in [0, 1, 3]]
        core = gram(k, CORE_BASIS)
        claimed_core, scalars = centered_core_claim_matrix(a)
        core_err = [[core[i][j] - claimed_core[i][j] for j in range(3)] for i in range(3)]
        C_pivots = ldl_pivots_decimal([[claimed_core[i][j] * scalars["L"] / Decimal(2) for j in range(3)] for i in range(3)])
        center_checks.append({
            "a": str(a),
            "r_8a2": str(scalars["r"]),
            "full_B_ldl_pivots": [str(v) for v in full_pivots],
            "even_odd_cross_max_abs": max_abs_matrix(cross_even_odd),
            "center_h_core_cross_max_abs": str(max(dabs(v) for v in h_core_cross)),
            "core_matrix_claim_max_abs_error": max_abs_matrix(core_err),
            "C_ldl_pivots": [str(v) for v in C_pivots],
            "det_T_formula": str(scalars["det_T_formula"]),
            "Tkk": str(scalars["Tkk"]),
            "L_n2_less_4": scalars["L_n2"] < Decimal(4),
            "z_between_0_and_2u": Decimal(0) < scalars["z"] < Decimal(2) * scalars["u"],
            "det_numerator_lower_4m_plus_12u": str(scalars["det_numerator_lower"]),
        })

    # Direct core q-form sanity with arbitrary coordinates, independent of
    # matrix assembly.
    core_q_checks = []
    for a, coords in [
        (Fraction(1, 12), (Fraction(2, 3), Fraction(-1, 5), Fraction(7, 11))),
        (Fraction(5, 16), (Fraction(-3, 8), Fraction(4, 9), Fraction(1, 6))),
        (Fraction(7, 20), (Fraction(5, 13), Fraction(-7, 10), Fraction(2, 7))),
    ]:
        d, e, kk = coords
        D = mat_add(mat_add(mat_scale(d, CORE_BASIS[0]), mat_scale(e, CORE_BASIS[1])), mat_scale(kk, CORE_BASIS[2]))
        exact = q_negative_entropy_hessian(k_path(Fraction(1, 2), a), D)
        formula = core_fisher_claim_q(a, d, e, kk)
        core_q_checks.append({
            "a": str(a),
            "coords_d_e_k": [str(v) for v in coords],
            "abs_error": str(dabs(exact - formula)),
        })

    symbolic = symbolic_center_identities()

    # Eta/sigma linear-algebra reduction: independent exact-event B_even
    # matrix, with the author's eta formula evaluated numerically.  This does
    # not reprove the external U8 weighted-trace-zero theorem; it checks that
    # once C0>0 is granted, only one scalar remains.
    sigma_checks = []
    for x, a in [(Fraction(2, 5), Fraction(1, 9)), (Fraction(1, 3), Fraction(1, 7)), (Fraction(1, 2), Fraction(3, 20))]:
        k = k_path(x, a)
        B = gram(k, EVEN_BASIS)
        E, U, W, V, _, Z, _, F = [dec(v) for v in claimed_atoms(x, a)]
        ell = (E * V / (U * W)).ln()
        kappa = (E * Z / (U * U)).ln()
        Lam = (F * U * U * W / (E * V * V * Z)).ln()
        n = -ell - Lam * dec(x)
        m = -kappa - Lam * dec(x)
        q = n * m - Decimal(2) * Lam * Lam * dec(a * a)
        eta = [
            Decimal(2) * (n * m - Lam * Lam * dec(a * a)) / (n * q),
            n / q,
            Decimal(4) * Lam * dec(a) / q,
            Decimal(2) * Lam * Lam * dec(a * a) / (n * q),
        ]
        # T0 columns t_d,t_h,t_k in coordinates d,e,h,k.
        T0 = [
            [Decimal(1), Decimal(0), Decimal(0)],
            [-eta[0] / eta[1], -eta[2] / eta[1], -eta[3] / eta[1]],
            [Decimal(0), Decimal(1), Decimal(0)],
            [Decimal(0), Decimal(0), Decimal(1)],
        ]
        Bt = matmul_decimal(transpose_decimal(T0), matmul_decimal(B, T0))
        be = [B[i][1] for i in range(4)]
        b0 = [sum(T0[i][j] * be[i] for i in range(4)) for j in range(3)]
        d0 = B[1][1]
        # Solve C0 y=b0 by Decimal Gaussian elimination.
        aug = [Bt[i][:] + [b0[i]] for i in range(3)]
        for col in range(3):
            pivot = aug[col][col]
            for j in range(col, 4):
                aug[col][j] /= pivot
            for row in range(3):
                if row == col:
                    continue
                factor = aug[row][col]
                for j in range(col, 4):
                    aug[row][j] -= factor * aug[col][j]
        y = [aug[i][3] for i in range(3)]
        sigma = d0 - sum(b0[i] * y[i] for i in range(3))
        sigma_checks.append({
            "x": str(x),
            "a": str(a),
            "eta": [str(v) for v in eta],
            "eta_e_positive": eta[1] > 0,
            "C0_ldl_pivots_numeric": [str(v) for v in ldl_pivots_decimal(Bt)],
            "sigma_numeric": str(sigma),
            "linear_algebra_reduction": "B_even positive iff C0 positive and sigma positive (Schur complement in basis [T0,e0]).",
        })

    passed = (
        all(row["matches_claimed_formula"] and row["all_atoms_positive"] and row["sum"] == "1" for row in atom_checks)
        and all(row["derivatives_match"] and Decimal(row["B_even_abs_error"]) < Decimal("1e-120") for row in even_formula_checks)
        and all(Decimal(row["even_odd_cross_max_abs"]) < Decimal("1e-120") for row in center_checks)
        and all(Decimal(row["center_h_core_cross_max_abs"]) < Decimal("1e-120") for row in center_checks)
        and all(Decimal(row["core_matrix_claim_max_abs_error"]) < Decimal("1e-120") for row in center_checks)
        and all(row["L_n2_less_4"] and row["z_between_0_and_2u"] for row in center_checks)
        and all(Decimal(row["abs_error"]) < Decimal("1e-120") for row in core_q_checks)
        and symbolic["all_zero"]
    )

    return {
        "status": "PASS_CENTERED_THEOREM_AND_SCOPE_AUDIT" if passed else "FAIL",
        "precision_decimal_digits": getcontext().prec,
        "input_hashes_sha256": hashes,
        "atom_formula_checks": atom_checks,
        "general_x_even_formula_checks": even_formula_checks,
        "centered_block_and_schur_checks": center_checks,
        "centered_core_qform_checks": core_q_checks,
        "symbolic_polynomial_identities": symbolic,
        "general_x_sigma_reduction_checks": sigma_checks,
        "finite_sanity_role": "Supplementary exact-event reconstruction only; analytic inequalities, not finite samples, certify the centered line.",
    }


if __name__ == "__main__":
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
    os.environ.setdefault("MKL_NUM_THREADS", "1")
    OUT.mkdir(parents=True, exist_ok=True)
    result = run()
    with (OUT / "audit_results.json").open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(json.dumps({"status": result["status"], "output": str(OUT / "audit_results.json")}, ensure_ascii=False))
