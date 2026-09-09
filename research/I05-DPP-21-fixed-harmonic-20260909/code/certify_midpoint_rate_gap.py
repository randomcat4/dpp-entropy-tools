#!/usr/bin/env python3
"""Rigorous fixed-three-symbol entropy-rate Jensen certificate.

Object:
    f_t(theta)=1/2+(1/4)cos(4*pi*theta)+(t/8)cos(2*pi*theta)
    t in {1/2,1,3/2}.

All finite probabilities are complete DPP events.  At these three rational
parameters, 32*(K-I_Z) is an integer symmetric matrix with bandwidth two.
The main computation enumerates its signed determinants by a fraction-free
band automaton.  A separate small-size path reconstructs inclusion minors and
performs Mobius inversion.

The only transcendental operation is Decimal.ln at precision 100.  Python's
decimal/libmpdec contract gives a correctly rounded nearest result; every log
is widened by 1e-90, and all subsequent interval operations use directed
ROUND_FLOOR / ROUND_CEILING contexts.

The true-rate passage is analytic, not an extrapolation: the script subtracts
the exact conditional-mutual-information tail bound proved in proof.md.
"""

from __future__ import annotations

import argparse
import json
import platform
import sys
from collections import Counter, defaultdict
from decimal import (
    Context,
    Decimal,
    ROUND_CEILING,
    ROUND_FLOOR,
    ROUND_HALF_EVEN,
)
from fractions import Fraction
from pathlib import Path
from typing import Iterable

BANDWIDTH = 2
PRECISION = 100
LOG_WIDEN = Decimal(1).scaleb(-90)
NEAREST = Context(prec=PRECISION, rounding=ROUND_HALF_EVEN)
LOWER = Context(prec=PRECISION, rounding=ROUND_FLOOR)
UPPER = Context(prec=PRECISION, rounding=ROUND_CEILING)


def bareiss_det(matrix: list[list[int]]) -> int:
    """Exact fraction-free determinant for a small integer matrix."""
    n = len(matrix)
    if n == 0:
        return 1
    a = [row[:] for row in matrix]
    sign = 1
    previous = 1
    for k in range(n - 1):
        if a[k][k] == 0:
            pivot = next((i for i in range(k + 1, n) if a[i][k] != 0), None)
            if pivot is None:
                return 0
            a[k], a[pivot] = a[pivot], a[k]
            sign = -sign
        pivot_value = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = a[i][j] * pivot_value - a[i][k] * a[k][j]
                if numerator % previous != 0:
                    raise ArithmeticError("Bareiss division was not exact")
                a[i][j] = numerator // previous
        previous = pivot_value
        for i in range(k + 1, n):
            a[i][k] = 0
        for j in range(k + 1, n):
            a[k][j] = 0
    return sign * a[-1][-1]


def scaled_kernel(n: int, nearest: int) -> list[list[int]]:
    """Return 32*K_t, where nearest=2*t is one of 1,2,3."""
    out = [[0] * n for _ in range(n)]
    for i in range(n):
        out[i][i] = 16
        if i + 1 < n:
            out[i][i + 1] = out[i + 1][i] = nearest
        if i + 2 < n:
            out[i][i + 2] = out[i + 2][i] = 4
    return out


def principal_det(matrix: list[list[int]], subset: tuple[int, ...]) -> int:
    return bareiss_det([[matrix[i][j] for j in subset] for i in subset])


def signed_event_numerator_direct(bits: tuple[int, ...], nearest: int) -> int:
    """Numerator of P(X=bits) over denominator 32**n."""
    n = len(bits)
    matrix = scaled_kernel(n, nearest)
    zero_count = 0
    for i, bit in enumerate(bits):
        if bit == 0:
            matrix[i][i] -= 32
            zero_count += 1
    det = bareiss_det(matrix)
    return -det if zero_count & 1 else det


def mobius_event_numerators(n: int, nearest: int) -> list[int]:
    """Independent inclusion-minor/Mobius reconstruction, scaled by 32**n."""
    kernel = scaled_kernel(n, nearest)
    inclusion: dict[int, int] = {}
    for mask in range(1 << n):
        subset = tuple(i for i in range(n) if (mask >> i) & 1)
        inclusion[mask] = principal_det(kernel, subset) * 32 ** (n - len(subset))

    events = [0] * (1 << n)
    full_mask = (1 << n) - 1
    for s_mask in range(1 << n):
        total = 0
        remaining = full_mask ^ s_mask
        sub = remaining
        while True:
            t_mask = s_mask | sub
            parity = (t_mask.bit_count() - s_mask.bit_count()) & 1
            total += -inclusion[t_mask] if parity else inclusion[t_mask]
            if sub == 0:
                break
            sub = (sub - 1) & remaining
        events[s_mask] = total
    return events


def independent_small_crosscheck(max_n: int = 6) -> None:
    """Check signed determinants against Mobius inversion for every small word."""
    for nearest in (1, 2, 3):
        for n in range(1, max_n + 1):
            mobius = mobius_event_numerators(n, nearest)
            for mask, expected in enumerate(mobius):
                bits = tuple((mask >> i) & 1 for i in range(n))
                direct = signed_event_numerator_direct(bits, nearest)
                if direct != expected:
                    raise AssertionError(
                        f"Mobius mismatch nearest={nearest}, n={n}, mask={mask}: "
                        f"{direct} != {expected}"
                    )


def initial_mask(n: int) -> int:
    """Used-column mask for the band determinant automaton at row zero."""
    mask = 0
    for position, column in enumerate(range(-BANDWIDTH, BANDWIDTH)):
        if column < 0 or column >= n:
            mask |= 1 << position
    return mask


def transition(
    vector: dict[int, int],
    row: int,
    n: int,
    diagonal: int,
    nearest: int,
    next_nearest: int = 4,
) -> dict[int, int]:
    """Advance one row in the exact Leibniz expansion of a width-two matrix."""
    out: defaultdict[int, int] = defaultdict(int)
    entering_column = row + BANDWIDTH

    for mask, value in vector.items():
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
                entry = diagonal
            elif abs(offset) == 1:
                entry = nearest
            elif abs(offset) == 2:
                entry = next_nearest
            else:
                entry = 0
            if entry == 0:
                continue

            # Earlier rows have already chosen the marked columns.  Every
            # marked column to the right of the new choice creates one inversion.
            inversions = (extended >> (position + 1)).bit_count()
            coefficient = -entry if inversions & 1 else entry
            selected = extended | (1 << position)

            # The leftmost column leaves the active band after this row and
            # therefore must already have been selected.
            if not (selected & 1):
                continue
            out[selected >> 1] += value * coefficient

    return dict(out)


def determinant_counts(n: int, nearest: int) -> Counter[int]:
    """Count all positive signed event numerators exactly."""
    counts: Counter[int] = Counter()
    start = {initial_mask(n): 1}

    def recurse(row: int, vector: dict[int, int], zero_count: int) -> None:
        if row == n:
            determinant = sum(vector.values())
            numerator = -determinant if zero_count & 1 else determinant
            if numerator <= 0:
                raise AssertionError(
                    f"nonpositive event numerator n={n}, nearest={nearest}: {numerator}"
                )
            counts[numerator] += 1
            return

        recurse(
            row + 1,
            transition(vector, row, n, -16, nearest),
            zero_count + 1,
        )
        recurse(
            row + 1,
            transition(vector, row, n, 16, nearest),
            zero_count,
        )

    recurse(0, start, 0)

    denominator = 32**n
    if sum(numerator * count for numerator, count in counts.items()) != denominator:
        raise AssertionError("complete-event probabilities do not normalize exactly")
    if sum(counts.values()) != 2**n:
        raise AssertionError("not all complete events were enumerated")
    return counts


def ln_integer_bounds(value: int) -> tuple[Decimal, Decimal]:
    nearest = NEAREST.ln(Decimal(value))
    return LOWER.subtract(nearest, LOG_WIDEN), UPPER.add(nearest, LOG_WIDEN)


def entropy_bounds(n: int, counts: Counter[int]) -> tuple[Decimal, Decimal]:
    """Directed enclosure of H_n from exact integer event numerators."""
    denominator_int = 32**n
    denominator = Decimal(denominator_int)
    log32_lower, log32_upper = ln_integer_bounds(32)

    weighted_log_lower = Decimal(0)
    weighted_log_upper = Decimal(0)
    for numerator, count in counts.items():
        log_lower, log_upper = ln_integer_bounds(numerator)
        exact_weight_numerator = Decimal(count * numerator)
        weight_lower = LOWER.divide(exact_weight_numerator, denominator)
        weight_upper = UPPER.divide(exact_weight_numerator, denominator)
        weighted_log_lower = LOWER.add(
            weighted_log_lower,
            LOWER.multiply(weight_lower, log_lower),
        )
        weighted_log_upper = UPPER.add(
            weighted_log_upper,
            UPPER.multiply(weight_upper, log_upper),
        )

    entropy_lower = LOWER.subtract(
        LOWER.multiply(Decimal(n), log32_lower),
        weighted_log_upper,
    )
    entropy_upper = UPPER.subtract(
        UPPER.multiply(Decimal(n), log32_upper),
        weighted_log_lower,
    )
    if entropy_lower > entropy_upper:
        raise AssertionError("directed entropy interval is reversed")
    return entropy_lower, entropy_upper


def fraction_to_decimal_upper(value: Fraction) -> Decimal:
    return UPPER.divide(Decimal(value.numerator), Decimal(value.denominator))


def conditional_entropy_bounds(depth: int, nearest: int) -> tuple[Decimal, Decimal, dict]:
    lower_counts = determinant_counts(depth, nearest)
    upper_counts = determinant_counts(depth + 1, nearest)
    h_n = entropy_bounds(depth, lower_counts)
    h_np1 = entropy_bounds(depth + 1, upper_counts)
    conditional_lower = LOWER.subtract(h_np1[0], h_n[1])
    conditional_upper = UPPER.subtract(h_np1[1], h_n[0])
    return conditional_lower, conditional_upper, {
        "H_n": [str(h_n[0]), str(h_n[1])],
        "H_n_plus_1": [str(h_np1[0]), str(h_np1[1])],
        "unique_numerators_n": len(lower_counts),
        "unique_numerators_n_plus_1": len(upper_counts),
    }


def analytic_tail(depth: int) -> Fraction:
    rho = Fraction(49, 64)
    c0 = Fraction(1033420800, 1263214441)
    conditional_error = c0 * rho ** (2 * depth - 6)
    return Fraction(256, 15) * conditional_error**2


def run(depth: int) -> dict:
    if depth < 3:
        raise ValueError("depth must be at least three")

    independent_small_crosscheck()

    conditionals: dict[int, tuple[Decimal, Decimal]] = {}
    finite_details: dict[str, dict] = {}
    for nearest in (1, 2, 3):
        lower, upper, details = conditional_entropy_bounds(depth, nearest)
        conditionals[nearest] = (lower, upper)
        finite_details[str(nearest)] = {
            "t": {1: "1/2", 2: "1", 3: "3/2"}[nearest],
            "conditional_entropy": [str(lower), str(upper)],
            **details,
        }

    tail_fraction = analytic_tail(depth)
    tail_upper = fraction_to_decimal_upper(tail_fraction)

    endpoint_average_upper = UPPER.divide(
        UPPER.add(conditionals[1][1], conditionals[3][1]), Decimal(2)
    )
    true_gap_lower = LOWER.subtract(conditionals[2][0], tail_upper)
    true_gap_lower = LOWER.subtract(true_gap_lower, endpoint_average_upper)

    finite_gap_upper = UPPER.subtract(
        conditionals[2][1],
        LOWER.divide(LOWER.add(conditionals[1][0], conditionals[3][0]), Decimal(2)),
    )

    threshold = Decimal(1) / Decimal(10000)
    if not true_gap_lower > threshold:
        raise AssertionError(
            f"certificate margin {true_gap_lower} does not exceed {threshold}"
        )

    comparison_constant = (
        Fraction(16384, 3243) ** 3
        * Fraction(1661, 8192) ** 2
        * Fraction(2445, 8192) ** 2
    )
    advertised_c0 = Fraction(1033420800, 1263214441)
    if not comparison_constant < advertised_c0:
        raise AssertionError("advertised conditional-tail constant is too small")

    return {
        "status": "PASS",
        "scope": "fixed three true entropy rates; no whole-interval curvature claim",
        "symbol": "1/2+(1/4)cos(4*pi*theta)+(t/8)cos(2*pi*theta)",
        "parameters": ["1/2", "1", "3/2"],
        "conditioning_depth": depth,
        "finite_details": finite_details,
        "tail_bound_exact": str(tail_fraction),
        "tail_bound_upper_decimal": str(tail_upper),
        "true_midpoint_gap_lower": str(true_gap_lower),
        "finite_midpoint_gap_upper": str(finite_gap_upper),
        "certified_threshold": "1/10000",
        "comparison_constant_exact": str(comparison_constant),
        "advertised_C0": str(advertised_c0),
        "rho": "49/64",
        "decimal_precision": PRECISION,
        "per_log_widening": str(LOG_WIDEN),
        "small_mobius_crosscheck_max_length": 6,
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
        / "midpoint_rate_certificate.full.json",
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
