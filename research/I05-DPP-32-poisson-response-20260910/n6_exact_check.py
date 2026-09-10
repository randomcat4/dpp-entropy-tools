#!/usr/bin/env python3
"""Exact author checker for the DPP32 n=6 conditional-Hessian theorem.

Uses only exact Fraction/SymPy polynomial arithmetic.  No finite differences,
floating interval endpoints, sampled maxima, or spectral-entropy substitutions.
The displayed decimal is cosmetic; acceptance is the exact comparison LB > 29.

Run: python n6_exact_check.py
"""
from fractions import Fraction as F
import itertools
import sympy as sp


def mulI(a, b):
    vv = [a[0]*b[0], a[0]*b[1], a[1]*b[0], a[1]*b[1]]
    return min(vv), max(vv)


def addI(a, b):
    return a[0]+b[0], a[1]+b[1]


def polyI(c, lo, hi):
    r = (F(0), F(0))
    x = (lo, hi)
    for z in reversed(c):
        r = addI(mulI(r, x), (z, z))
    return r


def dc(c):
    return [F(i)*c[i] for i in range(1, len(c))]


def log_bounds(x, N=36):
    """Rigorous rational enclosure of log(x), x>0.

    log x = 2 sum_{k>=0} y^(2k+1)/(2k+1), y=(x-1)/(x+1),
    with the absolute tail bounded by the geometric majorant used below.
    """
    assert x > 0
    y = (x-1)/(x+1)
    yy = y
    y2 = y*y
    z = F(0)
    for k in range(N+1):
        z += yy/F(2*k+1)
        yy *= y2
    z *= 2
    rem = 2*abs(y)**(2*N+3)/(F(2*N+3)*(1-y2))
    return z-rem, z+rem


def main():
    s = sp.symbols("s")
    b = sp.Rational(1, 8)
    C = sp.Matrix([
        [sp.Rational(1, 2), b, 0],
        [b, sp.Rational(1, 2), b],
        [0, b, sp.Rational(1, 2)],
    ])
    # E={0,2,4}, O={1,3,5}; B is the unscaled nearest-neighbor incidence.
    B = sp.Matrix([[1, 0, 0], [1, 1, 0], [0, 1, 1]])

    paths = []
    for e in itertools.product([0, 1], repeat=3):
        Ae = C-sp.diag(*[0 if bit else 1 for bit in e])
        Me = sp.simplify(B.T*Ae.inv()*B)
        Ke = C-s*Me
        ps = []
        for o in itertools.product([0, 1], repeat=3):
            X = Ke-sp.diag(*[0 if bit else 1 for bit in o])
            sign = (-1)**sum(1-bit for bit in o)
            p = sp.Poly(sp.expand(sign*X.det()), s)
            ps.append([F(int(p.nth(i).p), int(p.nth(i).q))
                       for i in range(p.degree()+1)])
        assert sp.simplify(sum(sum(sp.Rational(c.numerator, c.denominator)*s**i
                                  for i, c in enumerate(p)) for p in ps)-1) == 0
        paths.append((e, ps))

    S = F(9, 1024)
    cells = 8
    worst = None
    for e, ps in paths:
        for j in range(cells):
            lo, hi = S*j/cells, S*(j+1)/cells
            # -H'' = sum p'^2/p + sum p'' log p.
            LB = F(0)
            for c in ps:
                p = polyI(c, lo, hi)
                p1 = polyI(dc(c), lo, hi)
                p2 = polyI(dc(dc(c)), lo, hi)
                assert p[0] > 0

                if p1[0] <= 0 <= p1[1]:
                    fisher = F(0)
                else:
                    amin = min(abs(p1[0]), abs(p1[1]))
                    fisher = amin*amin/p[1]

                lp = (log_bounds(p[0])[0], log_bounds(p[1])[1])
                LB += fisher + mulI(p2, lp)[0]

            assert LB > 29
            if worst is None or LB < worst[2]:
                worst = (e, j, LB)

    print("AUTHOR_LOCAL_EXACT_PASS")
    print("conditional_paths", len(paths))
    print("s_cells_per_path", cells)
    print("complete_conditional_events_per_path", 8)
    print("log_atanh_terms", 37)
    print("exact_uniform_lower_bound", "> 29")
    print("worst_path", worst[0], "worst_cell", worst[1])
    print("display_only_worst_lower", float(worst[2]))
    print("independent_review", "PENDING")


if __name__ == "__main__":
    main()
