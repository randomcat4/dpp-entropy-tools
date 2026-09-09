#!/usr/bin/env python3
"""Exact symbolic cross-check of proof.md equation (6.9).

This is an author algebra check, not a proof of the DPP theorem.  It uses a
non-i.i.d. two-state normalized g-function whose invariant law depends on the
parameter, so all stationary-response terms in the RPF Hessian are active.
"""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


def hadamard(a: sp.Matrix, b: sp.Matrix) -> sp.Matrix:
    return sp.Matrix([sp.simplify(a[i] * b[i]) for i in range(a.rows)])


def main() -> None:
    t = sp.symbols("t", real=True)

    # q_b(t)=P(X_0=1 | X_1=b); rows are future b, columns are prepended a.
    q0 = sp.Rational(1, 3) + t / 20
    q1 = sp.Rational(2, 3) - t / 30
    q = sp.Matrix([[1 - q0, q0], [1 - q1, q1]])

    pi0 = (2 * t + 20) / (5 * t + 40)
    pi1 = (3 * t + 20) / (5 * t + 40)
    pi = sp.Matrix([[pi0, pi1]])
    assert all(sp.simplify(x) == 0 for x in pi * q - pi)
    assert sp.simplify(pi0 + pi1 - 1) == 0

    # Functions depending on the first two symbols are represented on (a,b).
    pairs = [(a, b) for a in (0, 1) for b in (0, 1)]
    index = {pair: i for i, pair in enumerate(pairs)}
    dimension = len(pairs)

    L = sp.zeros(dimension, dimension)
    for row, (b, c) in enumerate(pairs):
        del c
        for a in (0, 1):
            L[row, index[(a, b)]] = q[b, a]

    nu = sp.zeros(1, dimension)
    for a, b in pairs:
        nu[0, index[(a, b)]] = sp.simplify(pi[0, b] * q[b, a])

    one = sp.ones(dimension, 1)
    identity = sp.eye(dimension)
    assert all(sp.simplify(x) == 0 for x in nu * L - nu)
    assert sp.simplify((nu * one)[0] - 1) == 0

    phi = sp.Matrix([sp.log(q[b, a]) for a, b in pairs])
    psi = phi.diff(t)
    xi = psi.diff(t)

    B = -(L * phi)
    h = sp.simplify((nu * B)[0])

    Pi = identity - one * nu
    R = sp.simplify((identity - L + one * nu).inv() * Pi)
    assert all(sp.simplify(x) == 0 for x in (identity - L) * R - Pi)
    assert all(sp.simplify(x) == 0 for x in nu * R)
    assert all(sp.simplify(x) == 0 for x in R * one)

    B_dot = -(L * hadamard(psi, phi))
    B_ddot = -(L * (hadamard(xi + hadamard(psi, psi), phi) + hadamard(psi, psi)))
    assert all(sp.simplify(x) == 0 for x in B.diff(t) - B_dot)
    assert all(sp.simplify(x) == 0 for x in B.diff(t, 2) - B_ddot)

    u = sp.simplify(R * B)
    rhs = (nu * B_ddot)[0]
    rhs += (nu * hadamard(xi, u))[0]
    rhs += 2 * (nu * hadamard(psi, R * B_dot))[0]
    rhs += 2 * (nu * hadamard(psi, R * hadamard(psi, u)))[0]
    rhs -= (nu * hadamard(hadamard(psi, psi), u))[0]

    direct = sp.diff(h, t, 2)
    global_difference = sp.simplify(rhs - direct)
    assert global_difference == 0

    t0 = sp.Rational(1, 7)
    report = {
        "status": "PASS",
        "scope": "exact symbolic finite-memory RPF Hessian identity only; not a DPP theorem",
        "sympy_version": sp.__version__,
        "conditional_q0": str(q0),
        "conditional_q1": str(q1),
        "stationary_pi0": str(pi0),
        "stationary_pi1": str(pi1),
        "test_parameter": str(t0),
        "global_formula_difference": str(global_difference),
        "difference_at_test_parameter": str(sp.simplify((rhs - direct).subs(t, t0))),
        "checks": [
            "stationarity",
            "normalization",
            "centered_resolvent",
            "B first derivative",
            "B second derivative with Fisher term",
            "full five-term RPF Hessian",
        ],
    }

    target = Path(__file__).resolve().parents[1] / "output" / "rpf_hessian_exact.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
