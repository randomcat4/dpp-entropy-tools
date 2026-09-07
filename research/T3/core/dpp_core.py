"""Small exact-arithmetic DPP entropy certificate core.

This module is intentionally conservative.  It enumerates every subset,
builds exact determinant polynomials for inclusion probabilities
det((K+tD)_S), Mobius-inverts them to exact outcome-mass polynomials, and
only signs entropy gaps/curvature when the rational and log-interval
evidence is sufficient.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from dataclasses import dataclass
from decimal import Decimal, localcontext
from fractions import Fraction
from math import comb
from pathlib import Path
from typing import Any, Iterable, Sequence

Polynomial = list[Fraction]
Interval = tuple[Fraction, Fraction]


DEFAULT_MAX_N = 6
DEFAULT_BERNSTEIN_DEPTH = 8
DEFAULT_LOG_BITS = 120


def parse_fraction(value: Any) -> Fraction:
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int):
        return Fraction(value, 1)
    if isinstance(value, str):
        text = value.strip()
        if not text:
            raise ValueError("empty rational literal")
        return Fraction(text)
    raise TypeError(f"unsupported rational literal {value!r}")


def fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def decimal_text(value: Fraction, digits: int = 28) -> str:
    with localcontext() as ctx:
        ctx.prec = digits + 8
        dec = Decimal(value.numerator) / Decimal(value.denominator)
    return format(+dec, "g")


def trim(poly: Polynomial) -> Polynomial:
    out = list(poly)
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out or [Fraction(0)]


def poly_zero() -> Polynomial:
    return [Fraction(0)]


def poly_one() -> Polynomial:
    return [Fraction(1)]


def poly_add(a: Polynomial, b: Polynomial) -> Polynomial:
    n = max(len(a), len(b))
    out = [Fraction(0) for _ in range(n)]
    for i in range(n):
        out[i] = (a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)
    return trim(out)


def poly_sub(a: Polynomial, b: Polynomial) -> Polynomial:
    n = max(len(a), len(b))
    out = [Fraction(0) for _ in range(n)]
    for i in range(n):
        out[i] = (a[i] if i < len(a) else 0) - (b[i] if i < len(b) else 0)
    return trim(out)


def poly_mul(a: Polynomial, b: Polynomial) -> Polynomial:
    out = [Fraction(0) for _ in range(len(a) + len(b) - 1)]
    for i, av in enumerate(a):
        for j, bv in enumerate(b):
            out[i + j] += av * bv
    return trim(out)


def poly_scale(poly: Polynomial, scalar: Fraction) -> Polynomial:
    return trim([scalar * coeff for coeff in poly])


def poly_derivative(poly: Polynomial, order: int = 1) -> Polynomial:
    out = list(poly)
    for _ in range(order):
        if len(out) <= 1:
            return [Fraction(0)]
        out = [Fraction(i) * out[i] for i in range(1, len(out))]
    return trim(out)


def poly_eval(poly: Polynomial, t: Fraction) -> Fraction:
    acc = Fraction(0)
    for coeff in reversed(poly):
        acc = acc * t + coeff
    return acc


def poly_is_zero(poly: Polynomial) -> bool:
    return all(coeff == 0 for coeff in poly)


def poly_to_json(poly: Polynomial) -> list[str]:
    return [fraction_text(c) for c in trim(poly)]


def affine_entry(k: Fraction, d: Fraction) -> Polynomial:
    return trim([k, d])


def permutation_sign(perm: Sequence[int]) -> int:
    inversions = 0
    for i in range(len(perm)):
        for j in range(i + 1, len(perm)):
            if perm[i] > perm[j]:
                inversions += 1
    return -1 if inversions % 2 else 1


def det_poly(matrix: Sequence[Sequence[Polynomial]]) -> Polynomial:
    n = len(matrix)
    if n == 0:
        return poly_one()
    total = poly_zero()
    for perm in itertools.permutations(range(n)):
        term = poly_one()
        for row, col in enumerate(perm):
            term = poly_mul(term, matrix[row][col])
        if permutation_sign(perm) < 0:
            term = poly_scale(term, Fraction(-1))
        total = poly_add(total, term)
    return trim(total)


def principal_minor_poly(
    k_matrix: Sequence[Sequence[Fraction]],
    d_matrix: Sequence[Sequence[Fraction]],
    subset: Sequence[int],
) -> Polynomial:
    submatrix = [
        [affine_entry(k_matrix[i][j], d_matrix[i][j]) for j in subset]
        for i in subset
    ]
    return det_poly(submatrix)


def all_subsets(n: int) -> list[tuple[int, ...]]:
    subsets: list[tuple[int, ...]] = []
    for mask in range(1 << n):
        subsets.append(tuple(i for i in range(n) if mask & (1 << i)))
    return subsets


def subset_mask(subset: Sequence[int]) -> int:
    mask = 0
    for i in subset:
        mask |= 1 << i
    return mask


def shift_scale_power_poly(poly: Polynomial, a: Fraction, b: Fraction) -> Polynomial:
    """Return q(u) = p(a + (b-a)u) in the power basis."""
    width = b - a
    degree = len(poly) - 1
    out = [Fraction(0) for _ in range(degree + 1)]
    for k, coeff in enumerate(poly):
        for j in range(k + 1):
            out[j] += coeff * comb(k, j) * (a ** (k - j)) * (width ** j)
    return trim(out)


def power_to_bernstein(power_poly: Polynomial, degree: int | None = None) -> list[Fraction]:
    if degree is None:
        degree = len(power_poly) - 1
    padded = list(power_poly) + [Fraction(0) for _ in range(degree + 1 - len(power_poly))]
    bernstein: list[Fraction] = []
    for i in range(degree + 1):
        coeff = Fraction(0)
        for k in range(i + 1):
            coeff += Fraction(comb(i, k), comb(degree, k)) * padded[k]
        bernstein.append(coeff)
    return bernstein


@dataclass
class BernsteinResult:
    status: str
    lower_bound: Fraction | None
    witness_t: Fraction | None
    reason: str
    leaves: int
    max_depth_used: int

    def to_json(self) -> dict[str, Any]:
        out: dict[str, Any] = {
            "status": self.status,
            "reason": self.reason,
            "leaves": self.leaves,
            "max_depth_used": self.max_depth_used,
        }
        if self.lower_bound is not None:
            out["bernstein_lower_bound"] = fraction_text(self.lower_bound)
            out["bernstein_lower_bound_decimal"] = decimal_text(self.lower_bound)
        if self.witness_t is not None:
            out["witness_t"] = fraction_text(self.witness_t)
        return out


def certify_nonnegative_bernstein(
    poly: Polynomial,
    a: Fraction,
    b: Fraction,
    max_depth: int,
) -> BernsteinResult:
    best_lower: Fraction | None = None
    leaves = 0
    max_used = 0

    def visit(left: Fraction, right: Fraction, depth: int) -> BernsteinResult:
        nonlocal best_lower, leaves, max_used
        leaves += 1
        max_used = max(max_used, max_depth - depth)
        left_val = poly_eval(poly, left)
        right_val = poly_eval(poly, right)
        if left_val < 0:
            return BernsteinResult("refuted", None, left, "negative endpoint", leaves, max_used)
        if right_val < 0:
            return BernsteinResult("refuted", None, right, "negative endpoint", leaves, max_used)

        q = shift_scale_power_poly(poly, left, right)
        degree = len(q) - 1
        bernstein = power_to_bernstein(q, degree)
        local_lower = min(bernstein)
        if best_lower is None or local_lower < best_lower:
            best_lower = local_lower
        if local_lower >= 0:
            return BernsteinResult(
                "certified", best_lower, None, "all Bernstein coefficients nonnegative", leaves, max_used
            )
        if depth == 0:
            return BernsteinResult(
                "inconclusive",
                best_lower,
                None,
                "negative Bernstein coefficient remains after subdivision budget",
                leaves,
                max_used,
            )
        mid = (left + right) / 2
        first = visit(left, mid, depth - 1)
        if first.status != "certified":
            return first
        second = visit(mid, right, depth - 1)
        if second.status != "certified":
            return second
        return BernsteinResult(
            "certified",
            best_lower,
            None,
            "subdivided Bernstein coefficients nonnegative",
            leaves,
            max_used,
        )

    return visit(a, b, max_depth)


def normalize_power_two(x: Fraction) -> tuple[Fraction, int]:
    if x <= 0:
        raise ValueError("log input must be positive")
    n_bits = x.numerator.bit_length()
    d_bits = x.denominator.bit_length()
    exponent = n_bits - d_bits
    if exponent >= 0:
        y = x / (1 << exponent)
    else:
        y = x * (1 << (-exponent))
    while y < 1:
        y *= 2
        exponent -= 1
    while y >= 2:
        y /= 2
        exponent += 1
    return y, exponent


def log_series_interval_unit(x: Fraction, target_bits: int, max_terms: int = 10000) -> Interval:
    """Rigorous interval for ln(x), with x in [1, 2].

    Uses ln(x) = 2 atanh((x-1)/(x+1)).  In this range the series has
    nonnegative terms and an exact rational geometric tail bound.
    """
    if x == 1:
        return (Fraction(0), Fraction(0))
    if x < 1 or x > 2:
        raise ValueError("unit log series expects x in [1, 2]")
    z = (x - 1) / (x + 1)
    z2 = z * z
    partial = Fraction(0)
    power = z
    target = Fraction(1, 1 << target_bits)
    for k in range(max_terms):
        partial += 2 * power / Fraction(2 * k + 1)
        next_power = power * z2
        if z2 == 1:
            raise ValueError("invalid log series state")
        remainder = 2 * next_power / (Fraction(2 * k + 3) * (1 - z2))
        if remainder <= target:
            return (partial, partial + remainder)
        power = next_power
    raise ValueError("log series did not reach requested width")


def interval_add(a: Interval, b: Interval) -> Interval:
    return (a[0] + b[0], a[1] + b[1])


def interval_sub(a: Interval, b: Interval) -> Interval:
    return (a[0] - b[1], a[1] - b[0])


def interval_mul_scalar(interval: Interval, scalar: Fraction) -> Interval:
    lo, hi = interval
    if scalar >= 0:
        return (scalar * lo, scalar * hi)
    return (scalar * hi, scalar * lo)


def ln_fraction_interval(x: Fraction, target_bits: int) -> Interval:
    y, exponent = normalize_power_two(x)
    extra_bits = target_bits + 8 + abs(exponent).bit_length()
    ln_y = log_series_interval_unit(y, extra_bits)
    if exponent == 0:
        return ln_y
    ln_2 = log_series_interval_unit(Fraction(2), extra_bits)
    return interval_add(ln_y, interval_mul_scalar(ln_2, Fraction(exponent)))


def entropy_term_interval(p: Fraction, log_bits: int) -> Interval:
    if p < 0:
        raise ValueError("entropy term received a negative probability")
    if p == 0 or p == 1:
        return (Fraction(0), Fraction(0))
    log_interval = ln_fraction_interval(p, log_bits)
    return interval_mul_scalar(log_interval, -p)


def entropy_interval(probabilities: Iterable[Fraction], log_bits: int) -> Interval:
    total: Interval = (Fraction(0), Fraction(0))
    for p in probabilities:
        total = interval_add(total, entropy_term_interval(p, log_bits))
    return total


def interval_to_json(interval: Interval, digits: int = 28) -> dict[str, str]:
    lo, hi = interval
    return {
        "lower": fraction_text(lo),
        "upper": fraction_text(hi),
        "lower_decimal": decimal_text(lo, digits),
        "upper_decimal": decimal_text(hi, digits),
        "width": fraction_text(hi - lo),
    }


def parse_matrix(raw: Any, name: str) -> list[list[Fraction]]:
    if not isinstance(raw, list) or not raw:
        raise ValueError(f"{name} must be a nonempty square matrix")
    matrix = [[parse_fraction(cell) for cell in row] for row in raw]
    n = len(matrix)
    if any(len(row) != n for row in matrix):
        raise ValueError(f"{name} must be square")
    return matrix


def canonical_matrix(matrix: Sequence[Sequence[Fraction]]) -> list[list[str]]:
    return [[fraction_text(cell) for cell in row] for row in matrix]


def normalize_payload(raw_payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(raw_payload, dict):
        raise TypeError("payload must be a JSON object")
    if (
        "payload" in raw_payload
        and isinstance(raw_payload["payload"], dict)
        and "K" not in raw_payload
        and "K0" not in raw_payload
    ):
        payload = dict(raw_payload["payload"])
    else:
        payload = dict(raw_payload)
    if "K" not in payload and "K0" in payload:
        payload["K"] = payload["K0"]
    chord = payload.get("chord")
    if isinstance(chord, dict):
        if "interval" not in payload and {"t0", "t1"} <= set(chord):
            payload["interval"] = [chord["t0"], chord["t1"]]
        if "t" not in chord and "tm" in chord:
            payload["chord"] = {"t": chord["tm"]}
    if "interval" not in payload and {"a", "b"} <= set(payload):
        payload["interval"] = [payload["a"], payload["b"]]
    if "chord" not in payload:
        if "t" in payload:
            payload["chord"] = {"t": payload["t"]}
        elif "chord_t" in payload:
            payload["chord"] = {"t": payload["chord_t"]}
    return payload


def canonical_payload(payload: dict[str, Any]) -> dict[str, Any]:
    k_matrix = parse_matrix(payload["K"], "K")
    d_matrix = parse_matrix(payload["D"], "D")
    interval = [fraction_text(parse_fraction(x)) for x in payload.get("interval", ["0", "1"])]
    out: dict[str, Any] = {
        "K": canonical_matrix(k_matrix),
        "D": canonical_matrix(d_matrix),
        "interval": interval,
        "event_family": payload.get("event_family", "all"),
        "require_event_mass_one": bool(payload.get("require_event_mass_one", True)),
        "bernstein_depth": int(payload.get("bernstein_depth", DEFAULT_BERNSTEIN_DEPTH)),
        "log_bits": int(payload.get("log_bits", DEFAULT_LOG_BITS)),
        "max_n": int(payload.get("max_n", DEFAULT_MAX_N)),
    }
    if "events" in payload:
        out["events"] = payload["events"]
    if "chord" in payload:
        out["chord"] = {"t": fraction_text(parse_fraction(payload["chord"]["t"]))}
    if "curvature" in payload:
        out["curvature"] = {"t": fraction_text(parse_fraction(payload["curvature"]["t"]))}
    return out


def input_hash(canonical: dict[str, Any]) -> str:
    encoded = json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def event_subsets(n: int, payload: dict[str, Any]) -> list[tuple[int, ...]]:
    family = payload.get("event_family", "all")
    if family == "all":
        return all_subsets(n)
    if family == "nonempty":
        return [s for s in all_subsets(n) if s]
    if family == "listed":
        events = []
        for raw_subset in payload.get("events", []):
            subset = tuple(sorted(int(i) for i in raw_subset))
            if any(i < 0 or i >= n for i in subset):
                raise ValueError(f"event subset out of range: {raw_subset!r}")
            if len(set(subset)) != len(subset):
                raise ValueError(f"event subset repeats an index: {raw_subset!r}")
            events.append(subset)
        return events
    raise ValueError(f"unknown event_family {family!r}")


def matrix_is_symmetric(matrix: Sequence[Sequence[Fraction]]) -> bool:
    n = len(matrix)
    return all(matrix[i][j] == matrix[j][i] for i in range(n) for j in range(i + 1, n))


def affine_interval(entry: Polynomial, a: Fraction, b: Fraction) -> Interval:
    values = [poly_eval(entry, a), poly_eval(entry, b)]
    return (min(values), max(values))


def abs_affine_max(entry: Polynomial, a: Fraction, b: Fraction) -> Fraction:
    lo, hi = affine_interval(entry, a, b)
    return max(abs(lo), abs(hi))


def gershgorin_psd_fallback(
    k_matrix: Sequence[Sequence[Fraction]],
    d_matrix: Sequence[Sequence[Fraction]],
    a: Fraction,
    b: Fraction,
) -> dict[str, Any]:
    if not matrix_is_symmetric(k_matrix) or not matrix_is_symmetric(d_matrix):
        return {"attempted": False, "reason": "K and D are not both symmetric"}
    n = len(k_matrix)
    rows = []
    certified = True
    for i in range(n):
        diag_poly = affine_entry(k_matrix[i][i], d_matrix[i][i])
        diag_lo = affine_interval(diag_poly, a, b)[0]
        radius = Fraction(0)
        for j in range(n):
            if i == j:
                continue
            radius += abs_affine_max(affine_entry(k_matrix[i][j], d_matrix[i][j]), a, b)
        lower = diag_lo - radius
        if lower < 0:
            certified = False
        rows.append(
            {
                "row": i,
                "diag_lower": fraction_text(diag_lo),
                "radius_upper": fraction_text(radius),
                "eigenvalue_lower_contribution": fraction_text(lower),
            }
        )
    return {
        "attempted": True,
        "certified_psd": certified,
        "method": "interval Gershgorin lower bound for symmetric affine matrices",
        "rows": rows,
    }


def subset_key(subset: Sequence[int]) -> str:
    return ",".join(str(i) for i in subset)


def exact_event_mass_polys(
    principal_polys_by_subset: dict[tuple[int, ...], Polynomial],
    n: int,
) -> dict[tuple[int, ...], Polynomial]:
    """Mobius invert inclusion minors to exact DPP outcome masses.

    For a marginal-kernel finite DPP, det(K_T) is P(T is included).  The
    exact mass of outcome S is
      q(S) = sum_{T superset S} (-1)^(|T|-|S|) det(K_T).
    """
    subsets = all_subsets(n)
    masks = {subset: subset_mask(subset) for subset in subsets}
    masses: dict[tuple[int, ...], Polynomial] = {}
    for subset in subsets:
        subset_mask_value = masks[subset]
        total = poly_zero()
        for superset in subsets:
            superset_mask_value = masks[superset]
            if (superset_mask_value & subset_mask_value) != subset_mask_value:
                continue
            sign = -1 if (len(superset) - len(subset)) % 2 else 1
            total = poly_add(total, poly_scale(principal_polys_by_subset[superset], Fraction(sign)))
        masses[subset] = trim(total)
    return masses


def values_for_subsets(
    polys_by_subset: dict[tuple[int, ...], Polynomial],
    subsets: Sequence[tuple[int, ...]],
    t: Fraction,
) -> list[Fraction]:
    return [poly_eval(polys_by_subset[subset], t) for subset in subsets]


def jets_for_subsets(
    polys_by_subset: dict[tuple[int, ...], Polynomial],
    subsets: Sequence[tuple[int, ...]],
    t: Fraction,
) -> list[dict[str, Any]]:
    jets = []
    for subset in subsets:
        poly = polys_by_subset[subset]
        jets.append(
            {
                "subset": list(subset),
                "p": fraction_text(poly_eval(poly, t)),
                "p_prime": fraction_text(poly_eval(poly_derivative(poly), t)),
                "p_second": fraction_text(poly_eval(poly_derivative(poly, 2), t)),
            }
        )
    return jets


def entropy_chord_certificate(
    polys_by_subset: dict[tuple[int, ...], Polynomial],
    events: Sequence[tuple[int, ...]],
    a: Fraction,
    b: Fraction,
    t: Fraction,
    log_bits: int,
) -> dict[str, Any]:
    if not (a <= t <= b):
        return {"certified": False, "reason": "chord point is outside interval"}
    if a == b:
        return {"certified": False, "reason": "chord interval has zero length"}
    weight_a = (b - t) / (b - a)
    weight_b = (t - a) / (b - a)
    probs_a = values_for_subsets(polys_by_subset, events, a)
    probs_b = values_for_subsets(polys_by_subset, events, b)
    probs_t = values_for_subsets(polys_by_subset, events, t)
    if any(p < 0 for p in itertools.chain(probs_a, probs_b, probs_t)):
        return {"certified": False, "reason": "negative event probability at chord sample"}
    h_a = entropy_interval(probs_a, log_bits)
    h_b = entropy_interval(probs_b, log_bits)
    h_t = entropy_interval(probs_t, log_bits)
    chord = interval_add(interval_mul_scalar(h_a, weight_a), interval_mul_scalar(h_b, weight_b))
    gap = interval_sub(h_t, chord)
    if gap[0] > 0:
        sign = "positive"
        certified = True
    elif gap[1] < 0:
        sign = "negative"
        certified = True
    else:
        sign = "undetermined"
        certified = False
    return {
        "certified": certified,
        "sign": sign,
        "t": fraction_text(t),
        "endpoint_weights": [fraction_text(weight_a), fraction_text(weight_b)],
        "gap_nats": interval_to_json(gap),
        "H_left_nats": interval_to_json(h_a),
        "H_t_nats": interval_to_json(h_t),
        "H_right_nats": interval_to_json(h_b),
        "rounding_rationale": (
            "Each log is bounded by an exact rational atanh-series tail after power-of-two "
            "range reduction; interval arithmetic uses outward rational endpoints."
        ),
    }


def entropy_curvature_certificate(
    polys_by_subset: dict[tuple[int, ...], Polynomial],
    events: Sequence[tuple[int, ...]],
    t: Fraction,
    log_bits: int,
) -> dict[str, Any]:
    total: Interval = (Fraction(0), Fraction(0))
    terms = []
    refused_zero_terms = []
    for subset in events:
        poly = polys_by_subset[subset]
        p = poly_eval(poly, t)
        dp = poly_eval(poly_derivative(poly), t)
        ddp = poly_eval(poly_derivative(poly, 2), t)
        if p < 0:
            return {
                "certified": False,
                "reason": "negative event probability at curvature point",
                "subset": list(subset),
            }
        if p == 0:
            if poly_is_zero(poly):
                terms.append({"subset": list(subset), "term": interval_to_json((0, 0)), "zero": "identically zero"})
                continue
            refused_zero_terms.append(list(subset))
            continue
        log_p = ln_fraction_interval(p, log_bits)
        log_plus_one = (log_p[0] + 1, log_p[1] + 1)
        term = interval_mul_scalar(log_plus_one, -ddp)
        term = interval_add(term, (-dp * dp / p, -dp * dp / p))
        total = interval_add(total, term)
        terms.append({"subset": list(subset), "term": interval_to_json(term)})
    if refused_zero_terms:
        return {
            "certified": False,
            "reason": (
                "non-identically-zero event has p(t)=0; finite second-derivative "
                "limit is singular or requires a separate local zero-order proof"
            ),
            "zero_subsets": refused_zero_terms,
        }
    if total[0] > 0:
        sign = "positive"
        certified = True
    elif total[1] < 0:
        sign = "negative"
        certified = True
    else:
        sign = "undetermined"
        certified = False
    return {
        "certified": certified,
        "sign": sign,
        "t": fraction_text(t),
        "H_second_nats": interval_to_json(total),
        "terms": terms,
        "rounding_rationale": (
            "The formula H'' = -sum[p''(log p + 1) + (p')^2/p] is evaluated only "
            "for positive p, with exact rational derivatives and rigorous log intervals."
        ),
    }


def tiny_example_payload() -> dict[str, Any]:
    """Public seed 2x2 rational path with exact outcome masses.

    Exact outcome masses are:
      q({}) = 107/225 - 19t/225 - 73t^2/900,
      q({0}) = 28/225 + 64t/225 + 73t^2/900,
      q({1}) = 73/225 - 71t/225 + 73t^2/900,
      q({0,1}) = 17/225 + 26t/225 - 73t^2/900.
    """
    return {
        "K": [["1/5", "1/15"], ["1/15", "2/5"]],
        "D": [["2/5", "1/30"], ["1/30", "-1/5"]],
        "interval": ["0", "1"],
        "event_family": "all",
        "require_event_mass_one": True,
        "chord": {"t": "1/2"},
        "curvature": {"t": "1/2"},
        "bernstein_depth": 4,
        "log_bits": 120,
        "max_n": 6,
    }


def build_certificate(payload: dict[str, Any]) -> dict[str, Any]:
    payload = normalize_payload(payload)
    failures: list[str] = []
    canonical = canonical_payload(payload)
    k_matrix = parse_matrix(payload["K"], "K")
    d_matrix = parse_matrix(payload["D"], "D")
    if len(k_matrix) != len(d_matrix):
        raise ValueError("K and D dimensions differ")
    n = len(k_matrix)
    if any(len(row) != n for row in d_matrix):
        raise ValueError("D must have the same square shape as K")
    k_symmetric = matrix_is_symmetric(k_matrix)
    d_symmetric = matrix_is_symmetric(d_matrix)
    if not k_symmetric or not d_symmetric:
        failures.append("K and D must be symmetric rational matrices for the frozen marginal-kernel certificate")
    max_n = int(payload.get("max_n", DEFAULT_MAX_N))
    if n > max_n:
        failures.append(f"n={n} exceeds max_n={max_n}")
    a, b = (parse_fraction(x) for x in payload.get("interval", ["0", "1"]))
    if a >= b:
        failures.append("interval must satisfy left < right")
    bernstein_depth = int(payload.get("bernstein_depth", DEFAULT_BERNSTEIN_DEPTH))
    log_bits = int(payload.get("log_bits", DEFAULT_LOG_BITS))
    subsets = all_subsets(n)
    principal_polys_by_subset = {
        subset: principal_minor_poly(k_matrix, d_matrix, subset) for subset in subsets
    }
    event_mass_polys_by_subset = exact_event_mass_polys(principal_polys_by_subset, n)

    principal_minor_checks = []
    event_mass_checks = []
    feasibility_certified = not failures
    unresolved_feasibility = False
    for subset in subsets:
        result = certify_nonnegative_bernstein(principal_polys_by_subset[subset], a, b, bernstein_depth)
        check = {
            "subset": list(subset),
            "det_poly": poly_to_json(principal_polys_by_subset[subset]),
            "nonnegative": result.to_json(),
        }
        principal_minor_checks.append(check)
        if result.status == "refuted":
            feasibility_certified = False
            failures.append(f"principal minor {list(subset)} is negative at {fraction_text(result.witness_t or a)}")
        elif result.status != "certified":
            unresolved_feasibility = True

    event_mass_certified = not failures
    for subset in subsets:
        result = certify_nonnegative_bernstein(event_mass_polys_by_subset[subset], a, b, bernstein_depth)
        check = {
            "subset": list(subset),
            "q_poly": poly_to_json(event_mass_polys_by_subset[subset]),
            "nonnegative": result.to_json(),
        }
        event_mass_checks.append(check)
        if result.status == "refuted":
            event_mass_certified = False
            feasibility_certified = False
            failures.append(f"exact event mass {list(subset)} is negative at {fraction_text(result.witness_t or a)}")
        elif result.status != "certified":
            event_mass_certified = False
            feasibility_certified = False
            failures.append(f"exact event mass {list(subset)} nonnegativity is inconclusive")

    fallback = None
    if event_mass_certified and unresolved_feasibility:
        fallback = {
            "attempted": False,
            "reason": (
                "principal-minor Bernstein audit was inconclusive, but each inclusion "
                "minor is the exact sum of certified nonnegative outcome masses over "
                "supersets"
            ),
        }
    elif unresolved_feasibility:
        fallback = gershgorin_psd_fallback(k_matrix, d_matrix, a, b)
        if fallback.get("attempted"):
            fallback["note"] = (
                "This fallback is recorded only as an inclusion-minor audit; it does "
                "not replace the required exact outcome-mass nonnegativity checks."
            )

    events = event_subsets(n, payload)
    selected_event_mass = poly_zero()
    for subset in events:
        selected_event_mass = poly_add(selected_event_mass, event_mass_polys_by_subset[subset])
    mass_one_exact = trim(selected_event_mass) == [Fraction(1)]
    require_mass_one = bool(payload.get("require_event_mass_one", True))
    if require_mass_one and not mass_one_exact:
        failures.append("selected event family does not have exact total mass polynomial 1")

    entropy: dict[str, Any] = {}
    entropy_allowed = feasibility_certified and (mass_one_exact or not require_mass_one)
    if entropy_allowed and "chord" in payload:
        chord_t = parse_fraction(payload["chord"]["t"])
        chord = entropy_chord_certificate(event_mass_polys_by_subset, events, a, b, chord_t, log_bits)
        entropy["chord_gap"] = chord
        if not chord.get("certified"):
            failures.append(f"chord gap not certified: {chord.get('reason', chord.get('sign'))}")
    elif "chord" in payload:
        entropy["chord_gap"] = {"certified": False, "reason": "preconditions failed"}

    if entropy_allowed and "curvature" in payload:
        curvature_t = parse_fraction(payload["curvature"]["t"])
        curvature = entropy_curvature_certificate(event_mass_polys_by_subset, events, curvature_t, log_bits)
        entropy["curvature"] = curvature
        if not curvature.get("certified"):
            failures.append(f"curvature not certified: {curvature.get('reason', curvature.get('sign'))}")
    elif "curvature" in payload:
        entropy["curvature"] = {"certified": False, "reason": "preconditions failed"}

    jet_t = None
    if "curvature" in payload:
        jet_t = parse_fraction(payload["curvature"]["t"])
    elif "chord" in payload:
        jet_t = parse_fraction(payload["chord"]["t"])

    cert_status = "CERTIFIED" if not failures else "REFUSED"
    certificate: dict[str, Any] = {
        "certificate_status": cert_status,
        "input_hash_sha256": input_hash(canonical),
        "canonical_input": canonical,
        "assumptions": [
            "All principal-minor polynomials det((K+tD)_S) are computed exactly over rational arithmetic.",
            "Principal minors are inclusion probabilities only, not exact outcome probabilities.",
            "Exact outcome masses are computed by Mobius inversion q(S)=sum_{T superset S} (-1)^(|T|-|S|) det((K+tD)_T).",
            "Entropy uses selected exact outcome masses q(S), with all subsets selected by default.",
            "The frozen v1 marginal-kernel path requires symmetric rational K and D; nonsymmetric inputs are refused.",
            "Entropy certification requires exact event mass one unless require_event_mass_one is false.",
            "The empty determinant is 1 by convention; p log p at p=0 is evaluated as the mathematical limit 0.",
            "This is a finite certificate for the supplied rational path only, not a general theorem proof.",
        ],
        "limits": {
            "max_n": max_n,
            "bernstein_depth": bernstein_depth,
            "log_bits": log_bits,
            "system_dependencies": "Python standard library only",
        },
        "subset_polynomials": [
            {
                "subset": list(subset),
                "mask": subset_mask(subset),
                "det_poly_t_power_basis": poly_to_json(principal_polys_by_subset[subset]),
            }
            for subset in subsets
        ],
        "exact_event_mass_polynomials": [
            {
                "subset": list(subset),
                "mask": subset_mask(subset),
                "q_poly_t_power_basis": poly_to_json(event_mass_polys_by_subset[subset]),
            }
            for subset in subsets
        ],
        "feasibility": {
            "interval": [fraction_text(a), fraction_text(b)],
            "certified": feasibility_certified,
            "matrix_checks": {
                "K_symmetric": k_symmetric,
                "D_symmetric": d_symmetric,
                "path_symmetric": k_symmetric and d_symmetric,
                "rationale": "K+tD is symmetric for every rational t when both K and D are symmetric.",
            },
            "method": (
                "exact principal-minor determinant polynomials, Mobius-inverted exact "
                "outcome masses, and Bernstein nonnegativity certificates"
            ),
            "principal_minor_checks": principal_minor_checks,
            "exact_event_mass_checks": event_mass_checks,
            "fallback": fallback,
        },
        "events": {
            "family": payload.get("event_family", "all"),
            "subsets": [list(subset) for subset in events],
            "selected_mass_poly_t_power_basis": poly_to_json(selected_event_mass),
            "mass_one_exact": mass_one_exact,
        },
        "entropy": entropy,
        "failure_reasons": failures,
    }
    if jet_t is not None:
        certificate["events"]["jets_at_t"] = {
            "t": fraction_text(jet_t),
            "jets": jets_for_subsets(event_mass_polys_by_subset, events, jet_t),
        }
    return certificate


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build a small exact DPP entropy certificate.")
    parser.add_argument("--input", type=Path, help="JSON payload with rational K, D, interval, and certificate requests")
    parser.add_argument("--example", action="store_true", help="run the built-in worked rational example")
    args = parser.parse_args(argv)
    if args.example == bool(args.input):
        parser.error("choose exactly one of --example or --input")
    if args.example:
        payload = tiny_example_payload()
    else:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
    certificate = build_certificate(payload)
    print(json.dumps(certificate, indent=2, sort_keys=True))
    return 0 if certificate["certificate_status"] == "CERTIFIED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
