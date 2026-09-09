#!/usr/bin/env python3
"""Exact arithmetic check for Section 8 of finite_range_local_theorem.md.

This script proves no entropy statement.  It checks only the integer
Rudin--Shapiro identity and the displayed rational Fourier constants.
There is no floating-point tolerance.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path


def add_shift(a: list[int], b: list[int], shift: int, sign: int) -> list[int]:
    out = [0] * max(len(a), shift + len(b))
    for i, value in enumerate(a):
        out[i] += value
    for i, value in enumerate(b):
        out[shift + i] += sign * value
    return out


def autocorrelation(a: list[int], lag: int) -> int:
    return sum(a[j] * a[j + lag] for j in range(len(a) - lag))


def main() -> None:
    p = [1]
    q = [1]
    for r in range(4):
        shift = 2**r
        p, q = add_shift(p, q, shift, 1), add_shift(p, q, shift, -1)

    expected_p = [1, 1, 1, -1, 1, 1, -1, 1, 1, 1, 1, -1, -1, -1, 1, -1]
    assert p == expected_p

    combined_correlation = {
        lag: autocorrelation(p, lag) + autocorrelation(q, lag)
        for lag in range(len(p))
    }
    assert combined_correlation[0] == 32
    assert all(combined_correlation[lag] == 0 for lag in range(1, len(p)))

    wiener = Fraction(15, 16)
    twice_wiener = 2 * wiener
    assert twice_wiener == Fraction(15, 8) > 1

    # (7-4 sqrt(2))/16 > 0 is equivalent to 49 > 32.
    assert 49 > 32

    g_hat_1 = Fraction(1, 128)
    gamma = g_hat_1**2
    alpha = gamma**2 / (8 * Fraction(1, 2) ** 2 * (1 - Fraction(1, 2) ** 2))
    assert gamma == Fraction(1, 16384)
    assert alpha == Fraction(1, 3 * 2**27)

    output = {
        "status": "PASS",
        "scope": "exact example constants only; no entropy or rate computation",
        "P4_coefficients": p,
        "Q4_coefficients": q,
        "combined_autocorrelation": combined_correlation,
        "wiener_norm_c_minus_half": str(wiener),
        "twice_wiener_norm": str(twice_wiener),
        "strict_margin_test": "49 > 32",
        "g_hat_1": str(g_hat_1),
        "gamma": str(gamma),
        "quartic_correction_alpha": str(alpha),
    }

    target = Path(__file__).resolve().parents[1] / "output" / "rudin_shapiro_exact.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
