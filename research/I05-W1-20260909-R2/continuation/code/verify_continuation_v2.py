#!/usr/bin/env python3
"""Exact v2 checks, adding the reversible Markov obstruction."""

from pathlib import Path
import sympy as sp

from verify_continuation import (
    Q,
    active_sector_checks,
    diagonal_refresh_checks,
    event_law,
    generator_instance,
    quasi_free_obstruction_checks,
    assert_strict_contraction,
)


def reversible_markov_obstruction() -> None:
    C = sp.Matrix([[Q(1, 2), Q(1, 10)], [Q(1, 10), Q(1, 2)]])
    V = sp.eye(2)
    assert_strict_contraction(C)
    mu = event_law(C)
    assert mu == [Q(6, 25), Q(13, 50), Q(13, 50), Q(6, 25)]
    moment = sp.Integer(0)
    for mask, p in enumerate(mu):
        E = sp.zeros(2)
        for i in range(2):
            if not ((mask >> i) & 1):
                E[i, i] = 1
        Y = C - E
        G = sp.simplify(V.T * Y.inv() * V)
        d = sp.factor(G.det())
        moment += p * d * G[0, 1]
    assert sp.factor(moment) == -Q(125, 78)
    print("REVERSIBLE EXTERIOR-MARKOV OBSTRUCTION CHECKED")


def main() -> None:
    active_sector_checks()
    diagonal_refresh_checks()
    quasi_free_obstruction_checks()
    reversible_markov_obstruction()
    here = Path(__file__).resolve().parent
    generator_instance(here.parent / "inputs" / "generator_instance.json")
    print("ALL CONTINUATION V2 CHECKS PASSED")


if __name__ == "__main__":
    main()
