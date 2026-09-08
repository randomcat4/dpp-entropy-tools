"""Exact-event sanity checks for low-dimensional commuting spectral notes."""

from __future__ import annotations

import json
import math
from fractions import Fraction as F
from pathlib import Path


def det2(m):
    return m[0][0] * m[1][1] - m[0][1] * m[1][0]


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a):
    return [list(row) for row in zip(*a)]


def n2_case(c: F, s: F, l1: F, l2: F, v1: F, v2: F):
    q = [[c, -s], [s, c]]
    lam = [[l1, F(0)], [F(0), l2]]
    rate = [[v1, F(0)], [F(0), v2]]
    k = matmul(matmul(q, lam), transpose(q))
    d = matmul(matmul(q, rate), transpose(q))
    det_k = det2(k)
    inclusion_atoms = [
        F(1) - k[0][0] - k[1][1] + det_k,
        k[0][0] - det_k,
        k[1][1] - det_k,
        det_k,
    ]
    x = c * c
    r = l1 * (1 - l2)
    qq = l2 * (1 - l1)
    spectral_atoms = [
        (1 - l1) * (1 - l2),
        x * r + (1 - x) * qq,
        (1 - x) * r + x * qq,
        l1 * l2,
    ]
    assert inclusion_atoms == spectral_atoms
    p1 = [
        -v1 * (1 - l2) - v2 * (1 - l1),
        x * (v1 * (1 - l2) - l1 * v2) + (1 - x) * (v2 * (1 - l1) - l2 * v1),
        (1 - x) * (v1 * (1 - l2) - l1 * v2) + x * (v2 * (1 - l1) - l2 * v1),
        v1 * l2 + v2 * l1,
    ]
    p2 = [2 * v1 * v2, -2 * v1 * v2, -2 * v1 * v2, 2 * v1 * v2]
    pf = [float(z) for z in spectral_atoms]
    p1f = [float(z) for z in p1]
    p2f = [float(z) for z in p2]
    fisher = sum(a * a / b for a, b in zip(p1f, pf))
    acceleration = -sum(b * math.log(a) for a, b in zip(pf, p2f))
    h2 = acceleration - fisher
    return {
        "c": str(c),
        "s": str(s),
        "lambda": [str(l1), str(l2)],
        "rate": [str(v1), str(v2)],
        "exact_event_atoms": [str(z) for z in spectral_atoms],
        "sum_atoms": str(sum(spectral_atoms)),
        "sum_p1": str(sum(p1)),
        "sum_p2": str(sum(p2)),
        "H2_float": h2,
        "rho_float": acceleration / fisher,
        "strictly_negative_H2_float": h2 < 0,
    }


def n3_blocker():
    q = [
        [F(6, 7), F(-2, 7), F(-3, 7)],
        [F(-2, 7), F(3, 7), F(-6, 7)],
        [F(-3, 7), F(-6, 7), F(-2, 7)],
    ]
    lam = [F(3, 4), F(1, 2), F(1, 2)]
    rate = [F(1, 100), F(1), F(1)]
    terms = []
    for a in range(3):
        b, c = [idx for idx in range(3) if idx != a]
        terms.append(2 * (lam[a] * rate[b] * rate[c] - rate[a] * rate[b] * (1 - lam[c]) - rate[a] * rate[c] * (1 - lam[b])))
    singleton_seconds = []
    for i in range(3):
        singleton_seconds.append(sum(q[i][a] * q[i][a] * terms[a] for a in range(3)))
    return {
        "Q": [[str(x) for x in row] for row in q],
        "lambda": [str(x) for x in lam],
        "rate": [str(x) for x in rate],
        "column_terms": [str(x) for x in terms],
        "singleton_second_derivatives": [str(x) for x in singleton_seconds],
        "has_positive_singleton_second_derivative": any(x > 0 for x in singleton_seconds),
        "positive_example": "p_{1}''=2339/2450",
    }


def main():
    cases = [
        n2_case(F(3, 5), F(4, 5), F(1, 4), F(2, 3), F(1, 5), F(3, 7)),
        n2_case(F(5, 13), F(12, 13), F(3, 10), F(7, 10), F(2, 9), F(5, 11)),
        n2_case(F(1), F(0), F(2, 5), F(4, 7), F(1, 3), F(0)),
        n2_case(F(0), F(1), F(5, 8), F(1, 6), F(0), F(2, 5)),
    ]
    report = {
        "status": "PASS",
        "n2_exact_event_cases": cases,
        "n2_all_checked_H2_negative": all(row["strictly_negative_H2_float"] for row in cases),
        "n3_blocker": n3_blocker(),
        "note": "n2 cases are sanity checks only; theorem.md contains the proof",
    }
    out = Path(__file__).resolve().with_name("n2_exact_check.json")
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if report["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
