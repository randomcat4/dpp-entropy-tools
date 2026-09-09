#!/usr/bin/env python3
"""Exact checks for the I05-W1 continuation theorems.

All structural identities use SymPy exact arithmetic. The final entropy
curvatures are high-precision diagnostics only; the theorem is analytic and
does not rely on their numerical sign.
"""
from __future__ import annotations

from itertools import product
import sympy as sp

Q = sp.Rational


def event_matrix(K: sp.Matrix, mask: int) -> sp.Matrix:
    X = K.copy()
    for i in range(K.rows):
        if not ((mask >> i) & 1):
            X[i, i] -= 1
    return X


def event_prob(K: sp.Matrix, mask: int) -> sp.Expr:
    n = K.rows
    return sp.factor((-1) ** (n - mask.bit_count()) * event_matrix(K, mask).det())


def event_probs(K: sp.Matrix) -> list[sp.Expr]:
    return [event_prob(K, mask) for mask in range(1 << K.rows)]


def assert_positive_definite(M: sp.Matrix, name: str) -> None:
    assert M == M.T, f"{name} is not symmetric"
    for k in range(1, M.rows + 1):
        minor = sp.factor(M[:k, :k].det())
        assert minor > 0, f"{name} leading minor {k} is not positive: {minor}"


def cycle(i: int, j: int, k: int, eps: int) -> list[sp.Integer]:
    out = [sp.Integer(0)] * 8
    for xi, xj in product((0, 1), repeat=2):
        bits = [0, 0, 0]
        bits[i], bits[j], bits[k] = xi, xj, eps
        mask = sum(bits[r] << r for r in range(3))
        out[mask] = 1 if xi == xj else -1
    return out


def check_three_point_cycle_identity() -> None:
    K = sp.Matrix([
        [Q(2, 5), Q(1, 20), -Q(1, 30)],
        [Q(1, 20), Q(1, 2), Q(1, 25)],
        [-Q(1, 30), Q(1, 25), Q(3, 5)],
    ])
    D = sp.Matrix([[1, 2, -3], [2, -1, -1], [-3, -1, 4]])
    assert_positive_definite(K, "cycle K")
    assert_positive_definite(sp.eye(3) - K, "I-cycle K")
    assert D.rank() == 2 and D.det() == 0
    assert D * sp.ones(3, 1) == sp.zeros(3, 1)
    assert D.adjugate() == -5 * sp.ones(3)

    z = sp.symbols("z", real=True)
    pz = event_probs(K + z * D)
    assert max(sp.Poly(p, z).degree() for p in pz) == 2
    c = [sp.expand(p).coeff(z, 2) for p in pz]
    assert sp.simplify(sum(c)) == 0

    gamma = sp.Integer(-15)  # adj(D)=gamma*n*n^T for n=(1,1,1)/sqrt(3)
    kappa = sp.factor((sp.ones(1, 3) * K * sp.ones(3, 1))[0] / 3)
    reconstructed = [sp.Integer(0)] * 8
    for i, j, k in ((0, 1, 2), (0, 2, 1), (1, 2, 0)):
        delta = sp.factor(D.extract([i, j], [i, j]).det())
        assert delta == gamma / 3
        e0, e1 = cycle(i, j, k, 0), cycle(i, j, k, 1)
        for mask in range(8):
            reconstructed[mask] += delta * ((1 - kappa) * e0[mask] + kappa * e1[mask])
    assert all(sp.simplify(a - b) == 0 for a, b in zip(c, reconstructed))

    p0 = event_probs(K)
    for i, j, k in ((0, 1, 2), (0, 2, 1), (1, 2, 0)):
        for eps in (0, 1):
            def m(xi: int, xj: int) -> int:
                bits = [0, 0, 0]
                bits[i], bits[j], bits[k] = xi, xj, eps
                return sum(bits[r] << r for r in range(3))
            rayleigh = sp.factor(p0[m(0, 0)] * p0[m(1, 1)]
                                 - p0[m(1, 0)] * p0[m(0, 1)])
            assert rayleigh <= 0
    print("three-point cycle identity: exact pass")


def check_structural_fixture() -> tuple[sp.Matrix, sp.Matrix, sp.Matrix, sp.Expr]:
    A = Q(2, 5) * sp.eye(3) + Q(1, 30) * sp.ones(3)
    B = sp.Matrix([[1, 2, 3], [4, 5, 6], [-5, -7, -9]])
    M0 = B.T * B
    C = Q(2, 5) * sp.eye(3) + Q(1, 1000) * M0

    assert B.rank() == 2 and B.det() == 0
    assert sp.ones(1, 3) * B == sp.zeros(1, 3)
    assert B * sp.Matrix([1, -2, 1]) == sp.zeros(3, 1)
    assert all(x != 0 for x in B)
    assert M0 == sp.Matrix([[42, 57, 72], [57, 78, 99], [72, 99, 126]])
    x = sp.symbols("x")
    assert sp.factor(M0.charpoly(x).as_expr()) == x * (x**2 - 246 * x + 162)

    assert_positive_definite(A, "A")
    assert_positive_definite(sp.eye(3) - A, "I-A")
    assert_positive_definite(C, "C")
    assert_positive_definite(sp.eye(3) - C, "I-C")

    for mask in range(8):
        X = event_matrix(A, mask)
        M = sp.simplify(B.T * X.inv() * B)
        size = mask.bit_count()
        if size == 0:
            assert M == -Q(5, 3) * M0
        elif size == 3:
            assert M == Q(5, 2) * M0
        else:
            assert M.rank() == 2 and M.det() == 0
            e2 = sp.factor(sum(M.extract(I, I).det()
                               for I in ((0, 1), (0, 2), (1, 2))))
            assert e2 < 0, f"middle conditional direction not indefinite: {mask}, {e2}"

    lam_max = 123 + 3 * sp.sqrt(1663)
    tau2_a = sp.factor(Q(4, 25) / lam_max + Q(1, 2500))
    tau2_c = sp.factor(Q(9, 25) / lam_max - Q(3, 5000))
    tau2 = Q(4091, 15000) - sp.sqrt(1663) / 150
    assert sp.simplify(tau2_c - tau2) == 0
    assert sp.simplify(tau2_a - tau2) > 0
    assert 4091**2 - 10000 * 1663 == 106281 > 0
    assert tau2 > 0
    print("dense 3+3 fixture and exact legal radius: exact pass")
    return A, B, C, tau2


def check_exterior_likelihood(A: sp.Matrix, B: sp.Matrix, C: sp.Matrix) -> None:
    U = sp.Matrix([[1, 0], [0, 1], [-1, -1]])
    R = sp.Matrix([[1, 2, 3], [4, 5, 6]])
    V = R.T
    assert U * R == B
    s = Q(1, 10000)
    K = A.row_join(sp.sqrt(s) * B).col_join((sp.sqrt(s) * B.T).row_join(C))
    pA, pC, pK = event_probs(A), event_probs(C), event_probs(K)

    EG_A = sp.zeros(2)
    Edet_A = sp.Integer(0)
    for smask in range(8):
        X = event_matrix(A, smask)
        GA = sp.simplify(U.T * X.inv() * U)
        EG_A += pA[smask] * GA
        Edet_A += pA[smask] * GA.det()
        for tmask in range(8):
            Y = event_matrix(C, tmask)
            GC = sp.simplify(V.T * Y.inv() * V)
            ratio = sp.factor(pK[smask | (tmask << 3)] / (pA[smask] * pC[tmask]))
            expected = sp.factor((sp.eye(2) - s * GA * GC).det())
            assert sp.simplify(ratio - expected) == 0
    assert EG_A.applyfunc(sp.simplify) == sp.zeros(2)
    assert sp.simplify(Edet_A) == 0
    print("rank-two exterior likelihood and A-moments: exact pass")


def diagnostic_curvature(A: sp.Matrix, B: sp.Matrix, C: sp.Matrix, t0: sp.Rational) -> sp.Expr:
    t = sp.symbols("t", real=True)
    Kt = A.row_join(t * B).col_join((t * B.T).row_join(C))
    total = sp.Integer(0)
    for mask in range(64):
        poly = sp.Poly(event_prob(Kt, mask), t)
        p = sp.factor(poly.eval(t0))
        p1 = sp.factor(sp.diff(poly.as_expr(), t).subs(t, t0))
        p2 = sp.factor(sp.diff(poly.as_expr(), t, 2).subs(t, t0))
        assert p > 0
        total += -p1**2 / p - p2 * sp.log(p)
    return sp.N(total, 100)


def main() -> None:
    check_three_point_cycle_identity()
    A, B, C, tau2 = check_structural_fixture()
    check_exterior_likelihood(A, B, C)
    for t0 in (Q(1, 100), Q(1, 50)):
        assert t0**2 < tau2
        K = A.row_join(t0 * B).col_join((t0 * B.T).row_join(C))
        assert_positive_definite(K, f"K({t0})")
        assert_positive_definite(sp.eye(6) - K, f"I-K({t0})")
        h2 = diagnostic_curvature(A, B, C, t0)
        print(f"diagnostic H''({t0}) = {h2}")
        assert h2 < 0
    print("ALL CONTINUATION CHECKS PASSED")


if __name__ == "__main__":
    main()
