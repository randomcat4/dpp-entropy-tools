#!/usr/bin/env python3
"""Independent exact-event checks for D10-S4.

This script deliberately does not import the author's sanity checker.  It
constructs exact atom polynomials from the inclusion-probability Möbius formula
for K(t)=diag(x)+tD, then checks the diagonal-kernel Hessian identity and the
PSD/NSD Frobenius bound on small heterogeneous rational examples.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations
import json
from pathlib import Path


def f(num: int, den: int = 1) -> Fraction:
    return Fraction(num, den)


def poly_add(a: list[Fraction], b: list[Fraction]) -> list[Fraction]:
    m = max(len(a), len(b))
    out = [Fraction(0) for _ in range(m)]
    for i, v in enumerate(a):
        out[i] += v
    for i, v in enumerate(b):
        out[i] += v
    return trim(out)


def poly_mul(a: list[Fraction], b: list[Fraction]) -> list[Fraction]:
    out = [Fraction(0) for _ in range(len(a) + len(b) - 1)]
    for i, av in enumerate(a):
        for j, bv in enumerate(b):
            out[i + j] += av * bv
    return trim(out)


def trim(p: list[Fraction]) -> list[Fraction]:
    q = list(p)
    while len(q) > 1 and q[-1] == 0:
        q.pop()
    return q


def perm_sign(perm: tuple[int, ...]) -> int:
    inv = 0
    for i in range(len(perm)):
        for j in range(i + 1, len(perm)):
            inv += int(perm[i] > perm[j])
    return -1 if inv % 2 else 1


def det_fraction(mat: list[list[Fraction]]) -> Fraction:
    n = len(mat)
    if n == 0:
        return Fraction(1)
    total = Fraction(0)
    for perm in permutations(range(n)):
        term = Fraction(perm_sign(perm))
        for i, j in enumerate(perm):
            term *= mat[i][j]
        total += term
    return total


def det_poly_principal(x: list[Fraction], D: list[list[Fraction]], mask: int) -> list[Fraction]:
    idx = [i for i in range(len(x)) if mask & (1 << i)]
    m = len(idx)
    if m == 0:
        return [Fraction(1)]
    total = [Fraction(0)]
    for perm in permutations(range(m)):
        term = [Fraction(perm_sign(perm))]
        for row, col_pos in enumerate(perm):
            i = idx[row]
            j = idx[col_pos]
            if i == j:
                entry = [x[i], D[i][i]]
            else:
                entry = [Fraction(0), D[i][j]]
            term = poly_mul(term, entry)
        total = poly_add(total, term)
    return total


def atom_polynomials(x: list[Fraction], D: list[list[Fraction]]) -> dict[int, list[Fraction]]:
    n = len(x)
    dets = {mask: det_poly_principal(x, D, mask) for mask in range(1 << n)}
    atoms: dict[int, list[Fraction]] = {}
    full = (1 << n) - 1
    for S in range(1 << n):
        p = [Fraction(0)]
        rest = full ^ S
        sub = rest
        while True:
            A = S | sub
            parity = (A.bit_count() - S.bit_count()) % 2
            signed = dets[A] if parity == 0 else [-c for c in dets[A]]
            p = poly_add(p, signed)
            if sub == 0:
                break
            sub = (sub - 1) & rest
        atoms[S] = p
    return atoms


def coeff(poly: list[Fraction], k: int) -> Fraction:
    return poly[k] if k < len(poly) else Fraction(0)


def principal_submatrix(D: list[list[Fraction]], mask: int) -> list[list[Fraction]]:
    idx = [i for i in range(len(D)) if mask & (1 << i)]
    return [[D[i][j] for j in idx] for i in idx]


def is_psd_small(D: list[list[Fraction]]) -> bool:
    n = len(D)
    for mask in range(1, 1 << n):
        if det_fraction(principal_submatrix(D, mask)) < 0:
            return False
    return True


def neg_matrix(D: list[list[Fraction]]) -> list[list[Fraction]]:
    return [[-v for v in row] for row in D]


def cone_kind(D: list[list[Fraction]]) -> str:
    psd = is_psd_small(D)
    nsd = is_psd_small(neg_matrix(D))
    if psd and not nsd:
        return "PSD"
    if nsd and not psd:
        return "NSD"
    if psd and nsd:
        return "ZERO"
    return "INDEFINITE"


def max_u_one_minus_u(a: Fraction, b: Fraction) -> Fraction:
    val_a = a * (1 - a)
    val_b = b * (1 - b)
    if a <= Fraction(1, 2) <= b:
        return Fraction(1, 4)
    return max(val_a, val_b)


def frac_str(q: Fraction) -> str:
    return f"{q.numerator}/{q.denominator}" if q.denominator != 1 else str(q.numerator)


def serialize(obj):
    if isinstance(obj, Fraction):
        return frac_str(obj)
    if isinstance(obj, list):
        return [serialize(v) for v in obj]
    if isinstance(obj, dict):
        return {str(k): serialize(v) for k, v in obj.items()}
    return obj


def check_case(name: str, x: list[Fraction], D: list[list[Fraction]]) -> dict:
    n = len(x)
    atoms = atom_polynomials(x, D)
    p0: dict[int, Fraction] = {}
    p1: dict[int, Fraction] = {}
    p2: dict[int, Fraction] = {}
    score: dict[int, Fraction] = {}

    for S, poly in atoms.items():
        p0[S] = coeff(poly, 0)
        p1[S] = coeff(poly, 1)
        p2[S] = 2 * coeff(poly, 2)
        sc = Fraction(0)
        for i in range(n):
            if S & (1 << i):
                sc += D[i][i] / x[i]
            else:
                sc -= D[i][i] / (1 - x[i])
        score[S] = sc

    p0_expected = {}
    for S in range(1 << n):
        prod = Fraction(1)
        for i in range(n):
            prod *= x[i] if S & (1 << i) else (1 - x[i])
        p0_expected[S] = prod

    mass0 = sum(p0.values(), Fraction(0))
    mass1 = sum(p1.values(), Fraction(0))
    mass2 = sum(p2.values(), Fraction(0))
    singleton1 = [sum((p1[S] for S in range(1 << n) if S & (1 << i)), Fraction(0)) for i in range(n)]
    singleton2 = [sum((p2[S] for S in range(1 << n) if S & (1 << i)), Fraction(0)) for i in range(n)]

    score_identity_errors = {
        S: p1[S] - p0[S] * score[S]
        for S in range(1 << n)
        if p1[S] != p0[S] * score[S]
    }
    p0_errors = {
        S: p0[S] - p0_expected[S]
        for S in range(1 << n)
        if p0[S] != p0_expected[S]
    }

    fisher = sum((p1[S] * p1[S] / p0[S] for S in range(1 << n)), Fraction(0))
    formula_positive = sum((D[i][i] * D[i][i] / (x[i] * (1 - x[i])) for i in range(n)), Fraction(0))
    H2 = -fisher
    H2_formula = -formula_positive

    diag_square = sum((D[i][i] * D[i][i] for i in range(n)), Fraction(0))
    frob_square = sum((D[i][j] * D[i][j] for i in range(n) for j in range(n)), Fraction(0))
    kind = cone_kind(D)

    a = min(x)
    b = max(x)
    M = max_u_one_minus_u(a, b)
    cone_bound_checked = kind in ("PSD", "NSD")
    cone_bound_rhs = -frob_square / (n * M) if cone_bound_checked else None
    cone_bound_margin = n * diag_square - frob_square
    hessian_bound_margin = H2_formula - cone_bound_rhs if cone_bound_checked else None

    p2_nonzero_atoms = [S for S in range(1 << n) if p2[S] != 0]

    ok = True
    ok = ok and not p0_errors
    ok = ok and mass0 == 1 and mass1 == 0 and mass2 == 0
    ok = ok and singleton1 == [D[i][i] for i in range(n)]
    ok = ok and singleton2 == [0 for _ in range(n)]
    ok = ok and not score_identity_errors
    ok = ok and fisher == formula_positive and H2 == H2_formula
    if cone_bound_checked:
        ok = ok and cone_bound_margin >= 0 and H2_formula <= cone_bound_rhs

    return {
        "name": name,
        "n": n,
        "x": x,
        "cone_kind": kind,
        "p0_product_law": "PASS" if not p0_errors else "FAIL",
        "mass_derivatives": {"sum_p0": mass0, "sum_p1": mass1, "sum_p2": mass2},
        "singleton_first_derivatives": singleton1,
        "singleton_second_derivatives": singleton2,
        "score_identity_errors": score_identity_errors,
        "fisher": fisher,
        "H2_from_exact_atoms": H2,
        "H2_formula": H2_formula,
        "p2_nonzero_atom_masks": p2_nonzero_atoms,
        "frob_square": frob_square,
        "diag_square": diag_square,
        "box": {"a": a, "b": b, "M": M, "m": Fraction(1, n) / M},
        "cone_bound_checked": cone_bound_checked,
        "cone_trace_frobenius_margin_n_diag2_minus_frob2": cone_bound_margin,
        "cone_bound_rhs": cone_bound_rhs,
        "hessian_minus_bound_rhs": hessian_bound_margin,
        "status": "PASS" if ok else "FAIL",
    }


def main() -> int:
    cases = [
        (
            "n2_heterogeneous_psd",
            [f(1, 3), f(3, 5)],
            [[f(2, 5), f(1, 7)], [f(1, 7), f(1, 4)]],
        ),
        (
            "n2_zero_diagonal_indefinite_offdiag",
            [f(2, 7), f(5, 8)],
            [[f(0), f(4, 9)], [f(4, 9), f(0)]],
        ),
        (
            "n3_heterogeneous_spd",
            [f(1, 4), f(2, 5), f(7, 10)],
            [
                [f(3, 5), f(1, 10), f(1, 12)],
                [f(1, 10), f(1, 2), f(1, 15)],
                [f(1, 12), f(1, 15), f(2, 5)],
            ],
        ),
        (
            "n3_heterogeneous_nsd",
            [f(3, 10), f(1, 2), f(4, 5)],
            [
                [-f(3, 5), -f(1, 10), -f(1, 12)],
                [-f(1, 10), -f(1, 2), -f(1, 15)],
                [-f(1, 12), -f(1, 15), -f(2, 5)],
            ],
        ),
    ]
    results = [check_case(*case) for case in cases]
    status = "PASS" if all(r["status"] == "PASS" for r in results) else "FAIL"
    payload = {
        "status": status,
        "method": "exact-event atoms via Mobius inversion from inclusion determinants; Fraction arithmetic",
        "checks": [
            "p0 equals heterogeneous product Bernoulli law at diagonal K0",
            "p1/p0 equals diagonal score and ignores off-diagonal D",
            "sum_S pS''=0 and sum_{S containing i} pS''=0 exactly",
            "H'' equals -sum_i Dii^2/[xi(1-xi)]",
            "PSD/NSD Frobenius bound checked on cone examples",
            "zero-diagonal indefinite off-diagonal case has nonzero atom accelerations but zero Hessian",
        ],
        "cases": results,
    }
    out = Path(__file__).with_name("fresh_scalar_verify.json")
    out.write_text(json.dumps(serialize(payload), indent=2), encoding="utf-8")
    print(json.dumps(serialize({"status": status, "json": str(out), "case_statuses": {r["name"]: r["status"] for r in results}}), indent=2))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
