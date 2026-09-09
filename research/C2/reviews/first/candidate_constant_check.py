#!/usr/bin/env python3
"""Independent exact checks for the frozen C2 candidate constants.

This script does not import or read the author-side checker. It rebuilds
the fixed five-point frame and verifies the rational constants that carry
the upper-face compensation proof.
"""

from __future__ import annotations

import itertools
import json
import platform
from fractions import Fraction
from pathlib import Path

import sympy as sp


OUT = Path(__file__).resolve().parent / "candidate_constant_check.json"
Q = sp.Rational


def mat_to_str(M):
    return [[str(M[i, j]) for j in range(M.cols)] for i in range(M.rows)]


def main():
    U = Q(1, 1045) * sp.Matrix(
        [
            [615, 120, -702],
            [240, 735, 246],
            [-630, 30, -71],
            [480, -620, 492],
            [-170, -390, -540],
        ]
    )
    assert U.T * U == sp.eye(3)

    rows = [U[i, :].T for i in range(5)]
    triples = list(itertools.combinations(range(5), 3))
    pairs = list(itertools.combinations(range(5), 2))
    q = {S: sp.factor(U.extract(S, range(3)).det() ** 2) for S in triples}
    assert all(v > 0 for v in q.values())
    assert sum(q.values()) == 1

    ell = {i: sp.factor((rows[i].T * rows[i])[0]) for i in range(5)}
    w = {S: rows[S[0]].cross(rows[S[1]]) for S in pairs}
    z = {S: sp.factor((w[S].T * w[S])[0]) for S in pairs}
    assert all(v > 0 for v in ell.values())
    assert all(v > 0 for v in z.values())
    assert sum((rows[i] * rows[i].T for i in range(5)), sp.zeros(3)) == sp.eye(3)
    assert sum((w[S] * w[S].T for S in pairs), sp.zeros(3)) == sp.eye(3)

    G = sp.zeros(6)
    for S in pairs:
        x = w[S]
        a = sp.Matrix([x[0] ** 2, x[1] ** 2, x[2] ** 2, 2 * x[0] * x[1], 2 * x[0] * x[2], 2 * x[1] * x[2]])
        G += a * a.T / z[S]
    D = sp.diag(1, 1, 1, 2, 2, 2)
    kappa = Q(1, 22)
    M = G - kappa * D
    minors = [sp.factor(M[:i, :i].det()) for i in range(1, 7)]
    assert all(v > 0 for v in minors)
    trace_inverse_bound = sp.factor(1 / sp.trace(D * G.inv()))
    assert trace_inverse_bound > kappa

    normalized_masses = []
    normalized_masses.extend([(f"ell_{i+1}", ell[i] / 4) for i in range(5)])
    normalized_masses.extend([(f"z_{i+1}{j+1}", z[(i, j)] / 16) for i, j in pairs])
    normalized_masses.extend([(f"q_{''.join(str(i+1) for i in S)}", q[S] / 64) for S in triples])
    min_label, min_mass = min(normalized_masses, key=lambda item: item[1])
    assert min_mass == Q(441, 1092025)
    assert min_mass > Q(1, 2**14)
    assert Q(8, 3) ** 10 > 2**14

    e_radius = Q(1, 1971200)
    assert Q(1, 176) / e_radius - 5600 == Q(1, 352) / e_radius
    assert 5600 == Q(1, 352) / e_radius

    # Supplement threshold arithmetic for the fixed five-point application:
    # delta=e*lambda_max(B), B in [I,2I] gives delta<=2e and the main proof
    # uses |log g|<10, total p'' count 560, and kappa=1/22.
    assert Q(1, 1971200) == Q(1, 352 * 5600)
    assert Q(1, 176) / e_radius - 5600 == Q(1, 352) / e_radius

    out = {
        "status": "PASS",
        "python": platform.python_version(),
        "sympy": sp.__version__,
        "U_transpose_U_is_identity": True,
        "all_three_row_determinants_nonzero": True,
        "sum_q": str(sum(q.values())),
        "sum_rrT_identity": True,
        "sum_wwT_identity": True,
        "kappa_certificate": str(kappa),
        "sylvester_minors_positive": [str(v) for v in minors],
        "trace_inverse_bound": str(trace_inverse_bound),
        "min_normalized_mass_label": min_label,
        "min_normalized_mass": str(min_mass),
        "min_normalized_mass_gt_2^-14": True,
        "exp10_integer_proxy": "(8/3)^10 > 2^14",
        "e_radius": str(e_radius),
        "cone_arithmetic": "1/(176e)-5600 = 1/(352e) at e=1/1971200",
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
