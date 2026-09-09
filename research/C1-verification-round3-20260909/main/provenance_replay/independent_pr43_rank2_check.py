#!/usr/bin/env python3
"""Independent exact checks for PR43 clauses E--H.

The script uses complete-event probabilities
    p_K(S)=(-1)^(n-|S|) det(K-E_{S^c})
as the primitive object.  High-precision curvature values at the end are
diagnostics only; the universal concavity judgment is proof-level.
"""

from __future__ import annotations

import json
import platform
import sys
from collections import defaultdict
from itertools import combinations, product
from pathlib import Path

import mpmath
import numpy
import sympy as sp


def bits(mask: int, n: int) -> list[int]:
    return [(mask >> i) & 1 for i in range(n)]


def event_matrix(K: sp.Matrix, mask: int) -> sp.Matrix:
    X = sp.Matrix(K)
    for i, bit in enumerate(bits(mask, K.rows)):
        if bit == 0:
            X[i, i] -= 1
    return X


def event_prob(K: sp.Matrix, mask: int) -> sp.Expr:
    n = K.rows
    return sp.factor((-1) ** (n - int(mask).bit_count()) * event_matrix(K, mask).det())


def all_principal_minors_positive(M: sp.Matrix, label: str) -> None:
    n = M.rows
    if M != M.T:
        raise AssertionError(f"{label} is not symmetric")
    for size in range(1, n + 1):
        for idx in combinations(range(n), size):
            minor = sp.factor(M.extract(idx, idx).det())
            if not bool(minor > 0):
                raise AssertionError(f"{label} principal minor {idx} is not positive: {minor}")


def cycle_atom(i: int, j: int, k: int, eps: int) -> list[sp.Expr]:
    out = [sp.Integer(0)] * 8
    for xi, xj in product((0, 1), repeat=2):
        b = [0, 0, 0]
        b[i], b[j], b[k] = xi, xj, eps
        mask = sum(b[r] << r for r in range(3))
        out[mask] = sp.Integer(1 if xi == xj else -1)
    return out


def check_symbolic_three_point_cycle() -> None:
    a, b, c = sp.symbols("a b c", nonzero=True)
    x, y, z = sp.symbols("x y z")
    k11, k22, k33, k12, k13, k23 = sp.symbols("k11 k22 k33 k12 k13 k23")
    zz = sp.symbols("zz")

    n = sp.Matrix([a, b, c])
    n2 = (n.T * n)[0]
    D = sp.Matrix(
        [
            [x, y, -(a * x + b * y) / c],
            [y, z, -(a * y + b * z) / c],
            [
                -(a * x + b * y) / c,
                -(a * y + b * z) / c,
                (a * a * x + 2 * a * b * y + b * b * z) / (c * c),
            ],
        ]
    )
    K = sp.Matrix([[k11, k12, k13], [k12, k22, k23], [k13, k23, k33]])

    if any(sp.simplify(v) != 0 for v in D * n):
        raise AssertionError("constructed D does not annihilate n")
    if sp.simplify(D.det()) != 0:
        raise AssertionError("constructed D is not singular")

    adj = D.adjugate()
    lam = sp.factor(sum(adj[i, i] for i in range(3)) / n2)
    for i in range(3):
        for j in range(3):
            if sp.simplify(adj[i, j] - lam * n[i] * n[j]) != 0:
                raise AssertionError("adj(D) is not lambda n n^T")

    kappa = sp.factor((n.T * K * n)[0] / n2)
    coeffs = []
    for mask in range(8):
        poly = sp.Poly(event_prob(K + zz * D, mask), zz)
        coeffs.append(sp.factor(poly.coeff_monomial(zz**2)))

    reconstructed = [sp.Integer(0)] * 8
    for i, j, k in ((0, 1, 2), (0, 2, 1), (1, 2, 0)):
        delta = sp.factor(D.extract([i, j], [i, j]).det())
        if sp.simplify(delta - lam * n[k] ** 2) != 0:
            raise AssertionError("principal pair coefficient disagrees with adj(D)")
        e0 = cycle_atom(i, j, k, 0)
        e1 = cycle_atom(i, j, k, 1)
        for mask in range(8):
            reconstructed[mask] += delta * ((1 - kappa) * e0[mask] + kappa * e1[mask])

    for mask, (lhs, rhs) in enumerate(zip(coeffs, reconstructed)):
        if sp.factor(sp.together(lhs - rhs)) != 0:
            raise AssertionError(f"four-cycle coefficient mismatch at atom {mask}")

    aa, bb, cc = sp.symbols("aa bb cc")
    dd = aa * bb - cc**2
    p00, p10, p01, p11 = 1 - aa - bb + dd, aa - dd, bb - dd, dd
    if sp.expand(p00 * p11 - p10 * p01 + cc**2) != 0:
        raise AssertionError("two-point conditional odds identity failed")

    print("symbolic three-point cycle and two-point odds: exact pass", flush=True)


def parse_expr(text: str) -> sp.Expr:
    return sp.sympify(text, locals={"sqrt": sp.sqrt})


def matrix_from_json(rows: list[list[str]]) -> sp.Matrix:
    return sp.Matrix([[parse_expr(x) for x in row] for row in rows])


def second_elementary_symmetric(M: sp.Matrix) -> sp.Expr:
    return sp.factor(
        sum(M.extract(idx, idx).det() for idx in combinations(range(M.rows), 2))
    )


def load_fixture(path: Path) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix, sp.Matrix, sp.Expr]:
    data = json.loads(path.read_text(encoding="utf-8"))
    A = matrix_from_json(data["A"])
    B = matrix_from_json(data["B"])
    C = matrix_from_json(data["C"])
    M0 = matrix_from_json(data["M0"])
    tau2 = parse_expr(data["tau_squared"])
    return A, B, C, M0, tau2


def check_fixture(path: Path) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix, sp.Expr]:
    A, B, C, M0, tau2 = load_fixture(path)
    one = sp.ones(1, 3)
    right_null = sp.Matrix([1, -2, 1])

    if B.rank() != 2:
        raise AssertionError("B does not have rank two")
    if one * B != sp.zeros(1, 3):
        raise AssertionError("left null vector is wrong")
    if B * right_null != sp.zeros(3, 1):
        raise AssertionError("right null vector is wrong")
    if any(x == 0 for x in list(B)):
        raise AssertionError("B is not dense")
    if B.T * B != M0:
        raise AssertionError("M0 is not B^T B")

    x = sp.symbols("x")
    if sp.factor(M0.charpoly(x).as_expr()) != x * (x**2 - 246 * x + 162):
        raise AssertionError("M0 characteristic polynomial mismatch")

    for M, label in ((A, "A"), (sp.eye(3) - A, "I-A"), (C, "C"), (sp.eye(3) - C, "I-C")):
        all_principal_minors_positive(M, label)

    U = sp.Matrix([[1, 0], [0, 1], [-1, -1]])
    n = sp.Matrix([1, 1, 1])
    for mask in range(8):
        X = event_matrix(A, mask)
        M = sp.simplify(B.T * X.inv() * B)
        size = mask.bit_count()
        if size == 0:
            if M != -sp.Rational(5, 3) * M0:
                raise AssertionError("empty conditional matrix mismatch")
        elif size == 3:
            if M != sp.Rational(5, 2) * M0:
                raise AssertionError("full conditional matrix mismatch")
        else:
            det_g = sp.factor((U.T * X.inv() * U).det())
            ratio = sp.factor(((n.T * X * n)[0]) / X.det())
            if not bool(det_g < 0) or not bool(ratio < 0):
                raise AssertionError(f"Jacobi sign failed for mask {mask}: {det_g}, {ratio}")
            if M.rank() != 2 or sp.factor(M.det()) != 0:
                raise AssertionError(f"middle conditional matrix rank failed for mask {mask}")
            if not bool(second_elementary_symmetric(M) < 0):
                raise AssertionError(f"middle conditional matrix is not indefinite for mask {mask}")

    lam_max = 123 + 3 * sp.sqrt(1663)
    tau2_pos = sp.factor(sp.Rational(4, 25) / lam_max + sp.Rational(1, 2500))
    tau2_comp = sp.factor(sp.Rational(9, 25) / lam_max - sp.Rational(3, 5000))
    if sp.simplify(tau2_comp - tau2) != 0:
        raise AssertionError("tau^2 formula mismatch")
    if not bool(tau2_pos > tau2):
        raise AssertionError("wrong active legal-radius side")
    if 4091**2 - 10000 * 1663 != 106281:
        raise AssertionError("tau positivity integer certificate mismatch")
    if not bool(tau2 > 0):
        raise AssertionError("tau^2 is not positive")

    print("dense 3+3 fixture structure and radius: exact pass", flush=True)
    return A, B, C, tau2


def check_all_events_and_curvature(A: sp.Matrix, B: sp.Matrix, C: sp.Matrix, tau2: sp.Expr) -> None:
    tt = sp.symbols("tt")
    Kt = A.row_join(tt * B).col_join((tt * B.T).row_join(C))
    polynomials = [sp.Poly(event_prob(Kt, mask), tt) for mask in range(64)]

    for t0 in (sp.Rational(1, 100), sp.Rational(1, 50)):
        if not bool(t0**2 < tau2):
            raise AssertionError(f"diagnostic t={t0} is outside legal radius")
        min_prob = None
        hessian = sp.Integer(0)
        for poly in polynomials:
            expr = poly.as_expr()
            p = sp.factor(poly.eval(t0))
            p1 = sp.factor(sp.diff(expr, tt).subs(tt, t0))
            p2 = sp.factor(sp.diff(expr, tt, 2).subs(tt, t0))
            if not bool(p > 0):
                raise AssertionError(f"nonpositive event probability at t={t0}: {p}")
            min_prob = p if min_prob is None or bool(p < min_prob) else min_prob
            hessian += -p1**2 / p - p2 * sp.log(p)
        numeric_hessian = sp.N(hessian, 110)
        print(f"t={t0}: all 64 events positive; min p={sp.N(min_prob, 40)}", flush=True)
        print(f"t={t0}: diagnostic H''={numeric_hessian}", flush=True)
        if not bool(numeric_hessian < 0):
            raise AssertionError(f"diagnostic curvature is not negative at t={t0}")


def canonical_matrix_key(M: sp.Matrix) -> tuple[str, ...]:
    return tuple(str(sp.factor(x)) for x in list(M))


def check_exterior_statistics(A: sp.Matrix, B: sp.Matrix, C: sp.Matrix) -> None:
    U = sp.Matrix([[1, 0], [0, 1], [-1, -1]])
    R = sp.Matrix([[1, 2, 3], [4, 5, 6]])
    V = R.T
    if U * R != B:
        raise AssertionError("chosen rank-two factorization does not equal B")

    s = sp.Rational(1, 2500)
    pA = [event_prob(A, mask) for mask in range(8)]
    pC = [event_prob(C, mask) for mask in range(8)]
    K = A.row_join(sp.sqrt(s) * B).col_join((sp.sqrt(s) * B.T).row_join(C))

    grouped_joint: dict[tuple[tuple[str, ...], tuple[str, ...]], sp.Expr] = defaultdict(lambda: sp.Integer(0))
    grouped_product: dict[tuple[tuple[str, ...], tuple[str, ...]], sp.Expr] = defaultdict(lambda: sp.Integer(0))
    kl_full = sp.Integer(0)
    for smask in range(8):
        GA = sp.simplify(U.T * event_matrix(A, smask).inv() * U)
        for tmask in range(8):
            GC = sp.simplify(V.T * event_matrix(C, tmask).inv() * V)
            ratio_expected = sp.factor((sp.eye(2) - s * GA * GC).det())
            p_joint = event_prob(K, smask | (tmask << 3))
            p_prod = pA[smask] * pC[tmask]
            if sp.simplify(p_joint / p_prod - ratio_expected) != 0:
                raise AssertionError(f"exterior likelihood mismatch at ({smask},{tmask})")
            key = (canonical_matrix_key(GA), canonical_matrix_key(GC))
            grouped_joint[key] += p_joint
            grouped_product[key] += p_prod
            kl_full += p_joint * sp.log(p_joint / p_prod)

    kl_compressed = sp.Integer(0)
    for key, pj in grouped_joint.items():
        pp = grouped_product[key]
        kl_compressed += pj * sp.log(pj / pp)
    if sp.N(abs(kl_full - kl_compressed), 100) != 0:
        raise AssertionError("compressed KL does not equal full KL")

    mean_GA = sp.zeros(2)
    mean_det_GA = sp.Integer(0)
    for smask in range(8):
        GA = sp.simplify(U.T * event_matrix(A, smask).inv() * U)
        mean_GA += pA[smask] * GA
        mean_det_GA += pA[smask] * GA.det()
    if mean_GA.applyfunc(sp.simplify) != sp.zeros(2):
        raise AssertionError("E[G_A] is not zero")
    if sp.simplify(mean_det_GA) != 0:
        raise AssertionError("E[det G_A] is not zero")

    print("rank-two exterior likelihood, KL compression, and A moments: exact pass", flush=True)


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: independent_pr43_rank2_check.py fixture.json")
    print(f"python={sys.version.split()[0]} platform={platform.platform()}", flush=True)
    print(f"sympy={sp.__version__} numpy={numpy.__version__} mpmath={mpmath.__version__}", flush=True)
    fixture = Path(sys.argv[1]).resolve()
    print(f"fixture={fixture}", flush=True)
    check_symbolic_three_point_cycle()
    A, B, C, tau2 = check_fixture(fixture)
    check_exterior_statistics(A, B, C)
    check_all_events_and_curvature(A, B, C, tau2)
    print("ALL INDEPENDENT PR43 RANK-TWO CHECKS PASSED", flush=True)


if __name__ == "__main__":
    main()
