#!/usr/bin/env python3
"""Exact symbolic checks for the I05-35 small-edge continuation.

This is a new short algebra check. It does not execute or import the existing
PR124 event checker. The analytic positivity arguments are in the companion
markdown; finite output here is not substituted for those arguments.
"""
from __future__ import annotations

import sympy as s


def check_equal_strength_core() -> None:
    a, u, v = s.symbols("a u v", positive=True)
    mminus = s.Matrix(
        [
            [2 * (a + 1) * (2 * u - v), (2 * u - v) / 2],
            [(2 * u - v) / 2, (a * v + 4 * a + v) / (8 * a * (a + 1))],
        ]
    )
    expected = (2 * u - v) * (4 * a + v + 2 * a * (v - u)) / (4 * a)
    assert s.factor(mminus.det() - expected) == 0

    r, vv, ww = s.symbols("r vv ww", positive=True)
    aa = r / (1 - r)
    uu = (vv + ww) / 2
    chain = s.Rational(1, 4) * s.Matrix(
        [
            [1 / (1 + 2 * aa), -(vv - uu) / aa, 0],
            [-(vv - uu) / aa, 2 / (1 + aa), -uu / aa],
            [0, -uu / aa, 1],
        ]
    )
    cell = s.Matrix([1, -2, 1])
    kappa = s.cancel(1 / (cell.dot(chain.inv() * cell)))
    jj = (1 + 2 * aa) * vv - 2 * (1 + aa) * uu
    gap = s.factor(s.cancel(kappa - jj / (32 * aa**2)))
    den = r**2 * ww**2 + 4 * r**2 * ww + 8 * r**2 - 4 * r * vv - ww**2
    num = (
        16 * r**4
        - r**3 * vv * ww**2
        + 4 * r**3 * vv * ww
        - 8 * r**3 * vv
        + r**2 * ww**3
        + 8 * r**2 * ww
        + r * vv * ww**2
        - 4 * r * vv * ww
        - ww**3
    )
    assert s.cancel(gap - (1 - r) * num / (32 * r**2 * den)) == 0


def check_small_edge_core() -> None:
    a, u = s.symbols("a u", positive=True)
    c = a + 1

    y_a = s.Matrix(
        [
            [(a + 2) / (2 * c), a / (4 * c)],
            [a / (4 * c), u / (8 * a) + (a + 2) / (8 * c)],
        ]
    )
    y_b = s.Rational(3, 64) / c * s.Matrix(
        [[4 * (a + 2), 2 * a], [2 * a, a + 2]]
    )
    assert s.factor(y_a.det() - ((a + 2) * u + 4 * a) / (16 * a * c)) == 0
    assert s.factor(y_b.det() - s.Rational(9, 256) / c) == 0

    e_a_direct = s.cancel(2 * a * u - u**2 * y_a.inv()[0, 0])
    e_a_formula = 2 * u * (4 * a**2 - c * u**2) / ((a + 2) * u + 4 * a)
    assert s.factor(e_a_direct - e_a_formula) == 0

    y00 = (a + 2) / (2 * c)
    y01 = a / (4 * c)
    weak_c1 = s.Matrix([[-y00, -y01]])
    assert s.factor((weak_c1 * y_a.inv() * weak_c1.T)[0] - y00) == 0
    assert s.factor(2 * y00 - (weak_c1 * y_a.inv() * weak_c1.T)[0] - y00) == 0
    strong_c0 = s.Matrix([[-u, 0]])
    assert s.factor(u - (strong_c0 * y_a.inv() * weak_c1.T)[0]) == 0


def check_residual_only_obstruction() -> None:
    a, u = s.symbols("a u", positive=True)
    rmat = s.zeros(4)

    def add_edge(i: int, j: int, di, dj, off) -> None:
        rmat[i, i] += di
        rmat[j, j] += dj
        rmat[i, j] += off
        rmat[j, i] += off

    add_edge(0, 1, 1 / (8 * (1 + a)), s.Rational(1, 8), -u / (8 * a))
    add_edge(2, 3, 1 / (8 * (1 + a)), s.Rational(1, 8), -u / (8 * a))
    add_edge(
        0,
        2,
        1 / (8 * (1 + a)),
        1 / (8 * (1 + a)),
        -1 / (8 * (1 + a)),
    )
    add_edge(1, 3, s.Rational(1, 8), s.Rational(1, 8), -s.Rational(1, 8))
    cell = s.Matrix([1, -1, -1, 1])
    kappa = s.factor(1 / (cell.dot(rmat.inv() * cell)))
    expected = (9 * a**2 - (a + 1) * u**2) / (
        16 * a * (3 * a**2 + 6 * a - 2 * (a + 1) * u)
    )
    assert s.factor(kappa - expected) == 0
    gap = s.factor(kappa - u / (32 * a))
    expected_gap = -3 * ((a + 2) * u - 6 * a) / (
        32 * (3 * a**2 + 6 * a - 2 * (a + 1) * u)
    )
    assert s.factor(gap - expected_gap) == 0


def main() -> None:
    check_equal_strength_core()
    print("PASS: equal-strength antisymmetric determinant and exact chain gap")
    check_small_edge_core()
    print("PASS: removable b=0 pivot and small-edge Schur asymptotics")
    check_residual_only_obstruction()
    print("PASS: residual-only network limit and exact negative-gap criterion")
    print("ALL I05-35 SMALL-EDGE ALGEBRA CHECKS PASSED")


if __name__ == "__main__":
    main()
