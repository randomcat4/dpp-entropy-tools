#!/usr/bin/env python3
"""Rigorous true entropy-rate curvature at t=1/2,1,3/2.

The finite object is the depth-r conditional entropy H_{r+1}-H_r, not H_n/n.
All complete-event probability numerators and their first two t-jets are exact
integers. Decimal logarithms are correctly rounded at precision 100, widened
by 1e-90, and all subsequent interval operations are directed.

A parameter-point-specific complex comparison inverse supplies a closed exact
bound on the second derivative of the remaining conditional-mutual-information
tail. The output is therefore a true-rate curvature certificate, not a finite
window extrapolation.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import platform
import sys
from collections import Counter, defaultdict
from decimal import Context, Decimal, ROUND_CEILING, ROUND_FLOOR, ROUND_HALF_EVEN
from fractions import Fraction
from pathlib import Path

PRECISION = 100
LOG_WIDEN = Decimal(1).scaleb(-90)
NEAREST = Context(prec=PRECISION, rounding=ROUND_HALF_EVEN)
LOWER = Context(prec=PRECISION, rounding=ROUND_FLOOR)
UPPER = Context(prec=PRECISION, rounding=ROUND_CEILING)
BANDWIDTH = 2


def load_base_module():
    source = Path(__file__).with_name("certify_midpoint_rate_gap.py")
    spec = importlib.util.spec_from_file_location("dpp21_midpoint_base", source)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load base certificate module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def initial_mask(n: int) -> int:
    mask = 0
    for position, column in enumerate(range(-BANDWIDTH, BANDWIDTH)):
        if column < 0 or column >= n:
            mask |= 1 << position
    return mask


def jet_transition(
    vector: dict[int, tuple[int, int, int]],
    row: int,
    n: int,
    diagonal: int,
    nearest: int,
) -> dict[int, tuple[int, int, int]]:
    """Advance exact determinant value/first/second t-derivative jets."""
    accum: defaultdict[int, list[int]] = defaultdict(lambda: [0, 0, 0])
    entering_column = row + BANDWIDTH

    for mask, (v0, v1, v2) in vector.items():
        extended = mask
        if entering_column < 0 or entering_column >= n:
            extended |= 1 << (2 * BANDWIDTH)

        for position in range(2 * BANDWIDTH + 1):
            if (extended >> position) & 1:
                continue
            column = row - BANDWIDTH + position
            if not 0 <= column < n:
                continue
            offset = column - row
            if offset == 0:
                coefficient, derivative = diagonal, 0
            elif abs(offset) == 1:
                coefficient, derivative = nearest, 2
            elif abs(offset) == 2:
                coefficient, derivative = 4, 0
            else:
                continue

            inversions = (extended >> (position + 1)).bit_count()
            if inversions & 1:
                coefficient = -coefficient
                derivative = -derivative

            selected = extended | (1 << position)
            if not (selected & 1):
                continue
            target = selected >> 1
            out = accum[target]
            out[0] += coefficient * v0
            out[1] += coefficient * v1 + derivative * v0
            out[2] += coefficient * v2 + 2 * derivative * v1

    return {mask: tuple(values) for mask, values in accum.items()}


def event_jet_counts(n: int, nearest: int) -> Counter[tuple[int, int, int]]:
    counts: Counter[tuple[int, int, int]] = Counter()
    start = {initial_mask(n): (1, 0, 0)}

    def recurse(
        row: int,
        vector: dict[int, tuple[int, int, int]],
        zero_count: int,
    ) -> None:
        if row == n:
            value = sum(jet[0] for jet in vector.values())
            first = sum(jet[1] for jet in vector.values())
            second = sum(jet[2] for jet in vector.values())
            if zero_count & 1:
                value, first, second = -value, -first, -second
            if value <= 0:
                raise AssertionError(
                    f"nonpositive complete-event numerator n={n}, nearest={nearest}"
                )
            counts[(value, first, second)] += 1
            return

        recurse(
            row + 1,
            jet_transition(vector, row, n, -16, nearest),
            zero_count + 1,
        )
        recurse(
            row + 1,
            jet_transition(vector, row, n, 16, nearest),
            zero_count,
        )

    recurse(0, start, 0)

    denominator = 32**n
    if sum(count * jet[0] for jet, count in counts.items()) != denominator:
        raise AssertionError("probability numerators do not normalize")
    if sum(count * jet[1] for jet, count in counts.items()) != 0:
        raise AssertionError("first probability jets do not sum to zero")
    if sum(count * jet[2] for jet, count in counts.items()) != 0:
        raise AssertionError("second probability jets do not sum to zero")
    if sum(counts.values()) != 2**n:
        raise AssertionError("not all complete events were enumerated")
    return counts


def ln_bounds(value: int) -> tuple[Decimal, Decimal]:
    nearest = NEAREST.ln(Decimal(value))
    return LOWER.subtract(nearest, LOG_WIDEN), UPPER.add(nearest, LOG_WIDEN)


def rational_decimal_bounds(numerator: int, denominator: int) -> tuple[Decimal, Decimal]:
    return (
        LOWER.divide(Decimal(numerator), Decimal(denominator)),
        UPPER.divide(Decimal(numerator), Decimal(denominator)),
    )


def entropy_curvature_bounds(
    n: int, counts: Counter[tuple[int, int, int]]
) -> tuple[Decimal, Decimal, dict[str, str | int]]:
    """Directed enclosure of the full complete-event H_n''."""
    total_lower = Decimal(0)
    total_upper = Decimal(0)

    for (value, first, second), multiplicity in counts.items():
        fisher_num = multiplicity * first * first
        fisher_lower, fisher_upper = rational_decimal_bounds(fisher_num, value)

        log_lower, log_upper = ln_bounds(value)
        accel_integer = multiplicity * second
        if accel_integer >= 0:
            accel_lower = LOWER.multiply(Decimal(accel_integer), log_lower)
            accel_upper = UPPER.multiply(Decimal(accel_integer), log_upper)
        else:
            accel_lower = LOWER.multiply(Decimal(accel_integer), log_upper)
            accel_upper = UPPER.multiply(Decimal(accel_integer), log_lower)

        total_lower = LOWER.add(total_lower, LOWER.add(fisher_lower, accel_lower))
        total_upper = UPPER.add(total_upper, UPPER.add(fisher_upper, accel_upper))

    denominator = Decimal(32**n)
    curvature_lower = LOWER.divide(LOWER.minus(total_upper), denominator)
    curvature_upper = UPPER.divide(UPPER.minus(total_lower), denominator)
    if curvature_lower > curvature_upper:
        raise AssertionError("curvature interval is reversed")

    return curvature_lower, curvature_upper, {
        "events": 2**n,
        "distinct_jets": len(counts),
        "scaled_denominator": str(32**n),
        "summand_interval": [str(total_lower), str(total_upper)],
    }


def conditional_curvature_bounds(
    depth: int, nearest: int
) -> tuple[Decimal, Decimal, dict[str, object]]:
    counts_n = event_jet_counts(depth, nearest)
    counts_np1 = event_jet_counts(depth + 1, nearest)
    hn = entropy_curvature_bounds(depth, counts_n)
    hnp1 = entropy_curvature_bounds(depth + 1, counts_np1)
    lower = LOWER.subtract(hnp1[0], hn[1])
    upper = UPPER.subtract(hnp1[1], hn[0])
    return lower, upper, {
        "H_n_second": [str(hn[0]), str(hn[1])],
        "H_n_plus_1_second": [str(hnp1[0]), str(hnp1[1])],
        "H_conditional_second": [str(lower), str(upper)],
        "n_details": hn[2],
        "n_plus_1_details": hnp1[2],
    }


def point_tail_data(t: Fraction) -> dict[str, Fraction]:
    """Exact point-specific comparison and curvature-tail constants."""
    if t == Fraction(1, 2):
        disc = Fraction(1, 4)
        rho = Fraction(2, 3)
    elif t == Fraction(1, 1):
        disc = Fraction(1, 8)
        rho = Fraction(2, 3)
    elif t == Fraction(3, 2):
        disc = Fraction(1, 16)
        rho = Fraction(3, 4)
    else:
        raise ValueError("unsupported frozen parameter")

    nearest_complex = (t + disc) / 16
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
    residual_far = (
        Fraction(1, 2)
        - nearest_complex * (rho + 1 / rho)
        - next_nearest * (rho**2 + 1 / rho**2)
    )
    if min(residual_0, residual_1, residual_2, residual_far) <= 0:
        raise AssertionError(f"invalid comparison supersolution at t={t}")

    inverse_constant = 1 / residual_0
    propagation_a = nearest_complex * rho + next_nearest
    propagation_b = propagation_a + next_nearest * rho
    conditional_constant = (
        inverse_constant**3 * propagation_a**2 * propagation_b**2
    )

    delta = Fraction(1, 16)
    m2 = Fraction(256, 15)
    m3 = Fraction(57344, 225)
    m4 = Fraction(27656192, 3375)
    u1 = Fraction(9, 8)
    u2 = Fraction(37, 8)
    kappa1 = 1 / disc
    kappa2 = 2 / disc**2

    a0 = m2 / 2
    a1 = kappa1 * m2 + m3 * u1 / 2
    a2 = (
        m2 * (kappa1**2 + kappa2)
        + 2 * kappa1 * m3 * u1
        + (m4 * u1**2 + m3 * u2) / 2
    )

    return {
        "disc": disc,
        "rho": rho,
        "nearest_complex": nearest_complex,
        "residual_0": residual_0,
        "residual_1": residual_1,
        "residual_2": residual_2,
        "residual_far": residual_far,
        "inverse_constant": inverse_constant,
        "conditional_constant": conditional_constant,
        "A0": a0,
        "A1": a1,
        "A2": a2,
        "delta": delta,
    }


def geometric_tail(depth: int, data: dict[str, Fraction]) -> Fraction:
    rho = data["rho"]
    q = rho**4
    conditional_constant = data["conditional_constant"]
    a0, a1, a2 = data["A0"], data["A1"], data["A2"]

    # B_r = c2*r^2+c1*r+c0 in proof.md equation (8.14).
    c2 = 4 * a0
    c1 = 12 * a0 + 4 * a1
    c0 = 8 * a0 + 4 * a1 + a2

    one_minus_q = 1 - q
    sum0 = q**depth / one_minus_q
    sum1 = q**depth * (
        Fraction(depth, 1) / one_minus_q + q / one_minus_q**2
    )
    sum2 = q**depth * (
        Fraction(depth**2, 1) / one_minus_q
        + 2 * depth * q / one_minus_q**2
        + q * (1 + q) / one_minus_q**3
    )

    prefactor = conditional_constant**2 * rho ** (-12)
    return prefactor * (c2 * sum2 + c1 * sum1 + c0 * sum0)


def fraction_upper(value: Fraction) -> Decimal:
    return UPPER.divide(Decimal(value.numerator), Decimal(value.denominator))


def small_jet_checks(base_module, max_n: int = 6) -> None:
    """Check jet values against exact polynomial interpolation at small size."""
    # A determinant in the nearest scaled entry has degree at most n.  Values
    # at n+1 integer nodes determine it.  Lagrange interpolation is evaluated
    # exactly with Fraction, independently of the jet automaton.
    def interpolate_derivatives(values: list[tuple[int, int]], x0: int) -> tuple[Fraction, Fraction, Fraction]:
        result0 = Fraction(0)
        result1 = Fraction(0)
        result2 = Fraction(0)
        for j, (xj, yj) in enumerate(values):
            others = [x for i, (x, _) in enumerate(values) if i != j]
            denominator = Fraction(1)
            for x in others:
                denominator *= xj - x

            # Build the numerator polynomial prod_{x in others}(X-x).
            poly = [Fraction(1)]
            for x in others:
                new = [Fraction(0)] * (len(poly) + 1)
                for degree, coefficient in enumerate(poly):
                    new[degree] -= coefficient * x
                    new[degree + 1] += coefficient
                poly = new

            value0 = sum(coefficient * x0**degree for degree, coefficient in enumerate(poly))
            value1 = sum(
                degree * coefficient * x0 ** (degree - 1)
                for degree, coefficient in enumerate(poly)
                if degree >= 1
            )
            value2 = sum(
                degree * (degree - 1) * coefficient * x0 ** (degree - 2)
                for degree, coefficient in enumerate(poly)
                if degree >= 2
            )
            scale = Fraction(yj, 1) / denominator
            result0 += scale * value0
            result1 += scale * value1
            result2 += scale * value2
        return result0, result1, result2

    for nearest in (1, 2, 3):
        for n in range(1, max_n + 1):
            automaton = event_jet_counts(n, nearest)
            direct: Counter[tuple[int, int, int]] = Counter()
            nodes = list(range(-n, n + 1))
            for mask in range(1 << n):
                bits = tuple((mask >> i) & 1 for i in range(n))
                samples = [
                    (node, base_module.signed_event_numerator_direct(bits, node))
                    for node in nodes
                ]
                value, da, dda = interpolate_derivatives(samples, nearest)
                if value.denominator != 1 or da.denominator != 1 or dda.denominator != 1:
                    raise AssertionError("interpolated determinant jet is not integral")
                # nearest scaled entry is 2*t.
                direct[(int(value), int(2 * da), int(4 * dda))] += 1
            if automaton != direct:
                raise AssertionError(
                    f"jet automaton mismatch nearest={nearest}, n={n}"
                )


def run(depth: int) -> dict[str, object]:
    if depth < 3:
        raise ValueError("depth must be at least three")
    base_module = load_base_module()
    small_jet_checks(base_module)

    thresholds = {
        Fraction(1, 2): Fraction(-1, 2500),
        Fraction(1, 1): Fraction(-1, 1000),
        Fraction(3, 2): Fraction(-1, 500),
    }
    results: dict[str, object] = {}

    for t, nearest in (
        (Fraction(1, 2), 1),
        (Fraction(1, 1), 2),
        (Fraction(3, 2), 3),
    ):
        finite_lower, finite_upper, details = conditional_curvature_bounds(depth, nearest)
        data = point_tail_data(t)
        tail = geometric_tail(depth, data)
        tail_upper = fraction_upper(tail)
        true_lower = LOWER.subtract(finite_lower, tail_upper)
        true_upper = UPPER.add(finite_upper, tail_upper)
        threshold = thresholds[t]
        threshold_decimal = LOWER.divide(
            Decimal(threshold.numerator), Decimal(threshold.denominator)
        )
        if not true_upper < threshold_decimal:
            raise AssertionError(
                f"true curvature upper {true_upper} does not beat {threshold} at t={t}"
            )

        results[str(t)] = {
            "t": str(t),
            "finite_conditional_curvature": [str(finite_lower), str(finite_upper)],
            "true_curvature": [str(true_lower), str(true_upper)],
            "certified_upper_threshold": str(threshold),
            "tail_bound_exact": str(tail),
            "tail_bound_upper_decimal": str(tail_upper),
            "comparison": {
                key: str(value)
                for key, value in data.items()
                if key
                in {
                    "disc",
                    "rho",
                    "nearest_complex",
                    "residual_0",
                    "residual_1",
                    "residual_2",
                    "residual_far",
                    "inverse_constant",
                    "conditional_constant",
                    "A0",
                    "A1",
                    "A2",
                }
            },
            "finite_details": details,
        }

    return {
        "status": "PASS",
        "scope": "three fixed nonzero true entropy-rate curvature points only",
        "symbol": "1/2+(1/4)cos(4*pi*theta)+(t/8)cos(2*pi*theta)",
        "conditioning_depth": depth,
        "results": results,
        "small_exact_jet_crosscheck_max_length": 6,
        "decimal_precision": PRECISION,
        "per_log_widening": str(LOG_WIDEN),
        "python": sys.version,
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--depth", type=int, default=18)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parents[1]
        / "output"
        / "point_curvature_certificate.full.json",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = run(args.depth)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
