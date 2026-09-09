#!/usr/bin/env python3
"""Exact arithmetic checks for proof.md Section 5.

This program proves no entropy or entropy-rate statement. It checks only the
rational Fourier constants and elementary pointwise margins of the displayed
trigonometric family. There is no floating-point arithmetic or tolerance.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path


def main() -> None:
    mu = Fraction(1, 3)
    g_amplitude = Fraction(1, 8)
    g_hat_1 = g_amplitude / 2
    lambda_1 = g_hat_1**4
    tube_correction = Fraction(2, 3) * lambda_1
    radial_correction = Fraction(4, 3) * lambda_1
    T = Fraction(2, 1)

    radial_lower = mu - T * g_amplitude
    radial_upper = mu + T * g_amplitude
    assert radial_lower == Fraction(1, 12)
    assert radial_upper == Fraction(7, 12)

    epsilon_bound = Fraction(1, 24)
    full_lower = radial_lower - epsilon_bound
    full_upper = radial_upper + epsilon_bound
    assert full_lower == Fraction(1, 24) > 0
    assert full_upper == Fraction(5, 8) < 1

    assert g_hat_1 == Fraction(1, 16)
    assert lambda_1 == Fraction(1, 65536)
    assert tube_correction == Fraction(1, 98304)
    assert radial_correction == Fraction(1, 49152)

    report = {
        "status": "PASS",
        "scope": "exact displayed constants only; no entropy or rate computation",
        "mu": str(mu),
        "g_amplitude": str(g_amplitude),
        "g_hat_1": str(g_hat_1),
        "lambda_1_abs_g_hat_fourth": str(lambda_1),
        "accepted_radial_quartic_coefficient": str(radial_correction),
        "new_tube_quartic_coefficient": str(tube_correction),
        "T": str(T),
        "constant_center_radial_range": [str(radial_lower), str(radial_upper)],
        "epsilon_pointwise_bound": str(epsilon_bound),
        "full_family_range_at_epsilon_bound": [str(full_lower), str(full_upper)],
        "weighted_center_distance": "|epsilon|*exp(2*beta)",
    }

    target = Path(__file__).resolve().parents[1] / "output" / "explicit_family_exact.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
