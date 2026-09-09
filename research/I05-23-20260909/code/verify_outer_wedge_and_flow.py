#!/usr/bin/env python3
"""Exact symbolic/rational checks for ADDENDUM_OUTER_WEDGE_FLOW_RATE.md.

No floating-point assertion is theorem-facing.
"""
from __future__ import annotations

import json
import platform
from itertools import product

import sympy as sp

R = sp.Rational


def s(x):
    return str(sp.factor(x))


def mat(M):
    return [[s(M[i, j]) for j in range(M.cols)] for i in range(M.rows)]


def main() -> int:
    # A. Symbolic curvature decomposition.
    u, y = sp.symbols("u y", real=True)
    q = 1 + u
    raw = 4 * (u + y) ** 2 / q + (2 * u + 10 * y) * sp.log(q)
    Phi = 4 * u**2 / q + 2 * u * sp.log(q)
    psi = 8 * u / q + 10 * sp.log(q)
    diff = sp.simplify(raw - (Phi + 4 * y**2 / q + y * psi))
    assert diff == 0
    psi_prime = sp.simplify(sp.diff(psi, u))
    assert sp.simplify(psi_prime - (8 / q**2 + 10 / q)) == 0

    # C. Symbolic 2x2 adjugate linearity.
    g11, g12, g22 = sp.symbols("g11 g12 g22")
    v11, v12, v21, v22 = sp.symbols("v11 v12 v21 v22")
    G = sp.Matrix([[g11, g12], [g12, g22]])
    V = sp.Matrix([[v11, v12], [v21, v22]])
    numerator = sp.expand((V * G.adjugate() * V.T)[0, 1])
    formula = (
        v12 * v22 * g11
        - (v11 * v22 + v12 * v21) * g12
        + v11 * v21 * g22
    )
    assert sp.expand(numerator - formula) == 0

    # Exact correlated 2-point fixture and Farkas witness.
    C = sp.Matrix([[R(1, 2), R(1, 10)], [R(1, 10), R(1, 2)]])
    rows = []
    state11 = None
    for bits in product([0, 1], repeat=2):
        E = sp.diag(*[0 if bit else 1 for bit in bits])
        Y = C - E
        p = sp.factor((-1) ** (2 - sum(bits)) * Y.det())
        assert p > 0
        Gt = sp.simplify(Y.inv())
        d = sp.factor(Gt.det())
        assert sp.factor(d + 10 * Gt[0, 1]) == 0
        row = {
            "state": "".join(map(str, bits)),
            "p": s(p),
            "G12": s(Gt[0, 1]),
            "d": s(d),
            "d_plus_10_G12": s(d + 10 * Gt[0, 1]),
        }
        rows.append(row)
        if bits == (1, 1):
            state11 = (p, Gt[0, 1], d)

    assert state11 is not None
    mu, g12_11, d_11 = state11
    farkas_rhs = sp.factor(-mu * 10 * g12_11 - 2 * mu * d_11)
    assert farkas_rhs == -1

    output = {
        "status": "PASS",
        "arithmetic": "symbolic/rational assertions only",
        "versions": {"python": platform.python_version(), "sympy": sp.__version__},
        "curvature_identity": {
            "difference": s(diff),
            "Phi": str(Phi),
            "psi": str(psi),
            "psi_prime": str(psi_prime),
        },
        "adjugate_linearity": {
            "difference": s(sp.expand(numerator - formula)),
            "numerator": str(numerator),
        },
        "two_point_fixture": {
            "C": mat(C),
            "pointwise_relation": "det(G) = -10*G12",
            "events": rows,
            "farkas_rhs": s(farkas_rhs),
        },
    }
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
