#!/usr/bin/env python3
"""Pure-rational checks for the analytic constants in proof.md.

This program proves no entropy-rate statement by itself. It verifies only the
finite algebra behind legality, the comparison supersolution, the advertised
conditional-tail constant, and the binary-entropy derivative bounds.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path


def main() -> None:
    rho = Fraction(49, 64)
    nearest_complex = Fraction(13, 128)
    next_nearest = Fraction(1, 8)

    residual_0 = (
        Fraction(1, 2)
        - 2 * nearest_complex * rho
        - 2 * next_nearest * rho**2
    )
    residual_1 = (
        Fraction(1, 2) * rho
        - nearest_complex * (1 + rho**2)
        - next_nearest * (rho + rho**3)
    )
    residual_2 = (
        Fraction(1, 2) * rho**2
        - nearest_complex * (rho + rho**3)
        - next_nearest * (1 + rho**4)
    )
    far_coefficient = (
        Fraction(1, 2)
        - nearest_complex * (rho + 1 / rho)
        - next_nearest * (rho**2 + 1 / rho**2)
    )

    assert residual_0 == Fraction(3243, 16384)
    assert residual_1 == Fraction(146619, 2097152)
    assert residual_2 == Fraction(241611, 134217728)
    assert far_coefficient == Fraction(241611, 78675968)
    assert min(residual_0, residual_1, residual_2, far_coefficient) > 0

    inverse_constant = 1 / residual_0
    assert inverse_constant == Fraction(16384, 3243)

    propagation_a = nearest_complex * rho + next_nearest
    propagation_b = propagation_a + next_nearest * rho
    assert propagation_a == Fraction(1661, 8192)
    assert propagation_b == Fraction(2445, 8192)

    raw_tail_constant = (
        inverse_constant**3 * propagation_a**2 * propagation_b**2
    )
    advertised_tail_constant = Fraction(1033420800, 1263214441)
    assert raw_tail_constant < advertised_tail_constant < 1

    # Exact legality at the parameter endpoint |t|=3/2.
    t_endpoint = Fraction(3, 2)
    lower_symbol = Fraction(1, 4) - t_endpoint**2 / 128
    upper_symbol = Fraction(3, 4) + t_endpoint / 8
    assert lower_symbol == Fraction(119, 512)
    assert upper_symbol == Fraction(15, 16)
    assert min(lower_symbol, 1 - upper_symbol) == Fraction(1, 16)

    delta = Fraction(1, 16)
    one_minus_delta = 1 - delta
    m2 = 1 / (delta * one_minus_delta)
    m3 = (1 - 2 * delta) / (delta**2 * one_minus_delta**2)
    m4 = (
        2 / (delta**2 * one_minus_delta**2)
        + 2 * (1 - 2 * delta) ** 2 / (delta**3 * one_minus_delta**3)
    )
    assert m2 == Fraction(256, 15)
    assert m3 == Fraction(57344, 225)
    assert m4 == Fraction(27656192, 3375)

    u1 = Fraction(9, 8)
    u2 = Fraction(37, 8)
    a0 = m2 / 2
    a1 = 8 * m2 + m3 * u1 / 2
    a2 = 192 * m2 + 16 * m3 * u1 + (m4 * u1**2 + m3 * u2) / 2
    assert a0 > 0 and a1 > 0 and a2 > 0

    report = {
        "status": "PASS",
        "scope": "exact analytic constants only; no entropy computation",
        "rho": str(rho),
        "comparison_residuals": {
            "distance_0": str(residual_0),
            "distance_1": str(residual_1),
            "distance_2": str(residual_2),
            "distance_at_least_3_coefficient": str(far_coefficient),
        },
        "inverse_constant": str(inverse_constant),
        "propagation_constants": [str(propagation_a), str(propagation_b)],
        "raw_tail_constant": str(raw_tail_constant),
        "advertised_tail_constant": str(advertised_tail_constant),
        "symbol_range_at_abs_t_3_over_2": [str(lower_symbol), str(upper_symbol)],
        "binary_entropy_derivative_bounds": {
            "M2": str(m2),
            "M3": str(m3),
            "M4": str(m4),
        },
        "conditional_derivative_bounds": {"U1": str(u1), "U2": str(u2)},
        "bregman_constants": {"A0": str(a0), "A1": str(a1), "A2": str(a2)},
    }

    target = Path(__file__).resolve().parents[1] / "output" / "analytic_constants_exact.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
