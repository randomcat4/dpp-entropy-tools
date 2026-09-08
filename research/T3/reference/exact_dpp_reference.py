"""Independent small-n DPP entropy reference implementation.

This module is intentionally self-contained and conservative.  It enumerates
all subset events, uses exact Fraction arithmetic for determinants and jets,
and uses rational logarithm enclosures for entropy certificates.

Two event-law modes are provided because T3 consumers may use either kernel
convention:

* l_ensemble: event weights are det(L_S), probabilities are det(L_S)/det(I+L).
* marginal: det(K_S) is treated as the inclusion probability; exact event
  probabilities are obtained by inclusion-exclusion over all supersets.

Neither mode uses random sampling or floating tolerances for certificate
decisions.  Floating output is diagnostic only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple


Subset = Tuple[int, ...]
Matrix = List[List[Fraction]]
Interval = Tuple[Fraction, Fraction]

VALID_MODES = {"l_ensemble", "marginal"}

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


class ReferenceInputError(ValueError):
    """Raised when a case cannot define a valid small exact reference object."""


@dataclass(frozen=True)
class ProbabilityJet:
    subset: Subset
    p: Fraction
    p1: Fraction
    p2: Fraction


def parse_fraction(value: Any) -> Fraction:
    """Parse JSON-friendly exact rational values.

    Strings such as "3/7", "-2", and "0.125" are accepted.  JSON numbers are
    accepted for convenience, but floats are parsed through repr() and should
    only be used in diagnostic fixtures.
    """

    if isinstance(value, Fraction):
        return value
    if isinstance(value, bool):
        raise ReferenceInputError("Boolean values are not rational numbers")
    if isinstance(value, int):
        return Fraction(value)
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ReferenceInputError("Non-finite floats are not accepted")
        return Fraction(repr(value))
    if isinstance(value, str):
        try:
            return Fraction(value.strip())
        except ValueError as exc:
            raise ReferenceInputError(f"Cannot parse rational value {value!r}") from exc
    raise ReferenceInputError(f"Unsupported rational value {value!r}")


def parse_matrix(value: Any, name: str) -> Matrix:
    if not isinstance(value, list) or not value:
        raise ReferenceInputError(f"{name} must be a nonempty square matrix")
    matrix: Matrix = []
    for row in value:
        if not isinstance(row, list):
            raise ReferenceInputError(f"{name} must be a list of rows")
        matrix.append([parse_fraction(entry) for entry in row])
    n = len(matrix)
    if any(len(row) != n for row in matrix):
        raise ReferenceInputError(f"{name} must be square")
    return matrix


def validate_pair(k: Matrix, d: Matrix) -> None:
    if len(k) != len(d):
        raise ReferenceInputError("K and D must have the same dimension")
    n = len(k)
    if any(len(row) != n for row in d):
        raise ReferenceInputError("D must be square with the same dimension as K")
    for i in range(n):
        for j in range(i + 1, n):
            if k[i][j] != k[j][i]:
                raise ReferenceInputError(f"K is not symmetric at ({i},{j})")
            if d[i][j] != d[j][i]:
                raise ReferenceInputError(f"D is not symmetric at ({i},{j})")


def subset_key(subset: Subset) -> str:
    return "{}" if not subset else "{" + ",".join(str(i) for i in subset) + "}"


def fraction_str(x: Fraction) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def decimal_str(x: Fraction, digits: int = 40) -> str:
    try:
        from decimal import Decimal, localcontext
    except ImportError:
        return fraction_str(x)
    with localcontext() as ctx:
        ctx.prec = digits + 8
        value = Decimal(x.numerator) / Decimal(x.denominator)
        text = format(+value, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text or "0"


def all_subsets(n: int) -> List[Subset]:
    return [tuple(s) for r in range(n + 1) for s in combinations(range(n), r)]


def principal_submatrix(matrix: Matrix, subset: Subset) -> Matrix:
    return [[matrix[i][j] for j in subset] for i in subset]


def matrix_at(k: Matrix, d: Matrix, t: Fraction) -> Matrix:
    return [[k[i][j] + t * d[i][j] for j in range(len(k))] for i in range(len(k))]


def det_fraction(matrix: Matrix) -> Fraction:
    n = len(matrix)
    if n == 0:
        return Fraction(1)
    a = [row[:] for row in matrix]
    sign = 1
    det = Fraction(1)
    for col in range(n):
        pivot = None
        for row in range(col, n):
            if a[row][col] != 0:
                pivot = row
                break
        if pivot is None:
            return Fraction(0)
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            sign *= -1
        pivot_value = a[col][col]
        det *= pivot_value
        for row in range(col + 1, n):
            factor = a[row][col] / pivot_value
            if factor == 0:
                continue
            for c in range(col, n):
                a[row][c] -= factor * a[col][c]
    return det * sign


def det_principal(k: Matrix, subset: Subset) -> Fraction:
    return det_fraction(principal_submatrix(k, subset))


def poly_add(a: Sequence[Fraction], b: Sequence[Fraction]) -> List[Fraction]:
    size = max(len(a), len(b))
    out = [Fraction(0) for _ in range(size)]
    for i in range(size):
        out[i] = (a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)
    return trim_poly(out)


def poly_scale(a: Sequence[Fraction], scalar: Fraction) -> List[Fraction]:
    return trim_poly([scalar * x for x in a])


def poly_mul(a: Sequence[Fraction], b: Sequence[Fraction]) -> List[Fraction]:
    out = [Fraction(0) for _ in range(len(a) + len(b) - 1)]
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[i + j] += ai * bj
    return trim_poly(out)


def trim_poly(a: Sequence[Fraction]) -> List[Fraction]:
    out = list(a)
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def interpolate_at_zero(values: Sequence[Fraction]) -> List[Fraction]:
    """Return power coefficients for the polynomial with f(i)=values[i]."""

    degree = len(values) - 1
    result = [Fraction(0) for _ in range(degree + 1)]
    for i, yi in enumerate(values):
        basis = [Fraction(1)]
        denom = Fraction(1)
        for j in range(degree + 1):
            if i == j:
                continue
            basis = poly_mul(basis, [Fraction(-j), Fraction(1)])
            denom *= Fraction(i - j)
        scaled = poly_scale(basis, yi / denom)
        result = poly_add(result, scaled + [Fraction(0)] * (degree + 1 - len(scaled)))
    return trim_poly(result)


def determinant_polynomial(a: Matrix, b: Matrix) -> List[Fraction]:
    """Return det(a + x b) as exact power coefficients in x."""

    m = len(a)
    if m == 0:
        return [Fraction(1)]
    values = []
    for x in range(m + 1):
        values.append(det_fraction([[a[i][j] + Fraction(x) * b[i][j] for j in range(m)] for i in range(m)]))
    return interpolate_at_zero(values)


def determinant_jet2(a_at_t: Matrix, direction: Matrix) -> Tuple[Fraction, Fraction, Fraction]:
    coeffs = determinant_polynomial(a_at_t, direction)
    c0 = coeffs[0] if len(coeffs) > 0 else Fraction(0)
    c1 = coeffs[1] if len(coeffs) > 1 else Fraction(0)
    c2 = coeffs[2] if len(coeffs) > 2 else Fraction(0)
    return c0, c1, 2 * c2


def inclusion_jet_map(k: Matrix, d: Matrix, t: Fraction) -> Dict[Subset, Tuple[Fraction, Fraction, Fraction]]:
    n = len(k)
    kt = matrix_at(k, d, t)
    out: Dict[Subset, Tuple[Fraction, Fraction, Fraction]] = {}
    for subset in all_subsets(n):
        out[subset] = determinant_jet2(principal_submatrix(kt, subset), principal_submatrix(d, subset))
    return out


def probability_jets(k: Matrix, d: Matrix, t: Fraction, mode: str) -> List[ProbabilityJet]:
    if mode not in VALID_MODES:
        raise ReferenceInputError(f"Unknown mode {mode!r}")
    n = len(k)
    subsets = all_subsets(n)
    inc = inclusion_jet_map(k, d, t)
    if mode == "marginal":
        jets: List[ProbabilityJet] = []
        for subset in subsets:
            p = p1 = p2 = Fraction(0)
            set_subset = set(subset)
            for superset in subsets:
                if not set_subset.issubset(superset):
                    continue
                sign = -1 if (len(superset) - len(subset)) % 2 else 1
                q, q1, q2 = inc[superset]
                p += sign * q
                p1 += sign * q1
                p2 += sign * q2
            jets.append(ProbabilityJet(subset, p, p1, p2))
        return jets

    z = sum(inc[subset][0] for subset in subsets)
    z1 = sum(inc[subset][1] for subset in subsets)
    z2 = sum(inc[subset][2] for subset in subsets)
    if z <= 0:
        raise ReferenceInputError(f"L-ensemble normalizer is not positive at t={fraction_str(t)}")
    jets = []
    for subset in subsets:
        w, w1, w2 = inc[subset]
        if w < 0:
            raise ReferenceInputError(
                f"L-ensemble determinant weight for {subset_key(subset)} is negative at t={fraction_str(t)}"
            )
        p = w / z
        p1 = (w1 * z - w * z1) / (z * z)
        p2 = (w2 * z * z - 2 * w1 * z1 * z - w * z2 * z + 2 * w * z1 * z1) / (z * z * z)
        jets.append(ProbabilityJet(subset, p, p1, p2))
    return jets


def determinant_weight_polynomials(k: Matrix, d: Matrix) -> Dict[Subset, List[Fraction]]:
    out = {}
    for subset in all_subsets(len(k)):
        out[subset] = determinant_polynomial(principal_submatrix(k, subset), principal_submatrix(d, subset))
    return out


def event_probability_polynomials(k: Matrix, d: Matrix, mode: str) -> Dict[Subset, List[Fraction]]:
    if mode not in VALID_MODES:
        raise ReferenceInputError(f"Unknown mode {mode!r}")
    weights = determinant_weight_polynomials(k, d)
    if mode == "l_ensemble":
        return weights

    subsets = all_subsets(len(k))
    out: Dict[Subset, List[Fraction]] = {}
    for subset in subsets:
        total = [Fraction(0)]
        set_subset = set(subset)
        for superset in subsets:
            if not set_subset.issubset(superset):
                continue
            sign = Fraction(-1 if (len(superset) - len(subset)) % 2 else 1)
            total = poly_add(total, poly_scale(weights[superset], sign))
        out[subset] = total
    return out


def pow2_fraction(k: int) -> Fraction:
    return Fraction(1 << k, 1) if k >= 0 else Fraction(1, 1 << (-k))


def floor_log2_fraction(x: Fraction) -> int:
    if x <= 0:
        raise ValueError("floor_log2_fraction requires a positive rational")
    k = x.numerator.bit_length() - x.denominator.bit_length()
    while x < pow2_fraction(k):
        k -= 1
    while x >= pow2_fraction(k + 1):
        k += 1
    return k


def log_unit_interval(y: Fraction, target_bits: int) -> Interval:
    """Rigorous interval for log(y), for 1 <= y <= 2, using atanh series."""

    if y < 1 or y > 2:
        raise ValueError("log_unit_interval requires 1 <= y <= 2")
    if y == 1:
        return Fraction(0), Fraction(0)
    z = (y - 1) / (y + 1)
    z2 = z * z
    total = Fraction(0)
    power = z
    threshold = Fraction(1, 1 << target_bits)
    i = 0
    while True:
        total += power / Fraction(2 * i + 1)
        next_power = power * z2
        remainder = 2 * next_power / (Fraction(2 * i + 3) * (1 - z2))
        if remainder <= threshold:
            return 2 * total, 2 * total + remainder
        power = next_power
        i += 1


def log_rational_interval(x: Fraction, target_bits: int = 180) -> Interval:
    """Rigorous interval for natural log of a positive rational."""

    if x <= 0:
        raise ValueError("log_rational_interval requires a positive rational")
    if x == 1:
        return Fraction(0), Fraction(0)
    k = floor_log2_fraction(x)
    y = x / pow2_fraction(k)
    if y == 2:
        k += 1
        y = Fraction(1)
    extra_bits = max(16, abs(k).bit_length() + 8)
    unit = log_unit_interval(y, target_bits + extra_bits)
    if k == 0:
        return unit
    log2 = log_unit_interval(Fraction(2), target_bits + extra_bits)
    scaled_log2 = interval_mul_scalar(log2, Fraction(k))
    return interval_add(unit, scaled_log2)


def interval_add(a: Interval, b: Interval) -> Interval:
    return a[0] + b[0], a[1] + b[1]


def interval_sub(a: Interval, b: Interval) -> Interval:
    return a[0] - b[1], a[1] - b[0]


def interval_mul_scalar(a: Interval, scalar: Fraction) -> Interval:
    lo, hi = scalar * a[0], scalar * a[1]
    return (lo, hi) if lo <= hi else (hi, lo)


def curvature_interval(jets: Sequence[ProbabilityJet], target_bits: int = 180) -> Dict[str, Any]:
    total: Interval = (Fraction(0), Fraction(0))
    exact_rational_term = Fraction(0)
    zero_notes = []
    for jet in jets:
        if jet.p < 0:
            raise ReferenceInputError(f"Negative event probability for {subset_key(jet.subset)}")
        if jet.p == 0:
            if jet.p1 != 0 or jet.p2 != 0:
                return {
                    "kind": "not_finite_or_not_certified",
                    "status": "NOT_CERTIFIED",
                    "reason": (
                        f"Probability {subset_key(jet.subset)} is zero but has nonzero first/second jet; "
                        "entropy curvature needs a one-sided limit analysis."
                    ),
                }
            zero_notes.append(
                f"{subset_key(jet.subset)} has p=p'=p''=0 and contributes zero through the reported jet order."
            )
            continue
        exact_rational_term -= (jet.p1 * jet.p1) / jet.p
        if jet.p2 != 0:
            total = interval_add(total, interval_mul_scalar(log_rational_interval(jet.p, target_bits), -jet.p2))
    total = interval_add(total, (exact_rational_term, exact_rational_term))
    return {
        "kind": "rigorous_interval",
        "rounding": "H'' = -sum p'' log(p) - sum (p')^2/p, with exact rational jets and log intervals.",
        "interval": interval_json(total),
        "zero_terms": zero_notes,
        "classification": sign_classification(total),
    }


def entropy_at(k: Matrix, d: Matrix, t: Fraction, mode: str, target_bits: int = 180) -> Dict[str, Any]:
    jets = probability_jets(k, d, t, mode)
    prob_sum = sum(jet.p for jet in jets)
    return {
        "t": fraction_str(t),
        "probability_sum_exact": fraction_str(prob_sum),
        "probabilities": jets_json(jets),
        "entropy": entropy_interval(jets, target_bits),
    }


def chord_gap_interval(
    k: Matrix,
    d: Matrix,
    t0: Fraction,
    t: Fraction,
    t1: Fraction,
    mode: str,
    target_bits: int = 180,
) -> Dict[str, Any]:
    if not (t0 < t1):
        raise ReferenceInputError("Chord endpoints require t0 < t1")
    if not (t0 <= t <= t1):
        raise ReferenceInputError("Chord evaluation point must lie in [t0,t1]")
    h0 = entropy_interval(probability_jets(k, d, t0, mode), target_bits)["interval_raw"]
    hm = entropy_interval(probability_jets(k, d, t, mode), target_bits)["interval_raw"]
    h1 = entropy_interval(probability_jets(k, d, t1, mode), target_bits)["interval_raw"]
    alpha = (t1 - t) / (t1 - t0)
    beta = (t - t0) / (t1 - t0)
    linear: Interval = interval_add(interval_mul_scalar(h0, alpha), interval_mul_scalar(h1, beta))
    gap = interval_sub(hm, linear)
    return {
        "kind": "rigorous_interval",
        "definition": "H(t) - ((t1-t)/(t1-t0))*H(t0) - ((t-t0)/(t1-t0))*H(t1)",
        "t0": fraction_str(t0),
        "t": fraction_str(t),
        "t1": fraction_str(t1),
        "alpha": fraction_str(alpha),
        "beta": fraction_str(beta),
        "interval": interval_json(gap),
        "classification": sign_classification(gap),
    }


def entropy_interval_raw(jets: Sequence[ProbabilityJet], target_bits: int = 180) -> Interval:
    total: Interval = (Fraction(0), Fraction(0))
    for jet in jets:
        if jet.p < 0:
            raise ReferenceInputError(f"Negative event probability for {subset_key(jet.subset)}")
        if jet.p == 0:
            continue
        total = interval_add(total, interval_mul_scalar(log_rational_interval(jet.p, target_bits), -jet.p))
    return total


def interval_json(interval: Interval) -> Dict[str, str]:
    return {
        "lo_exact": fraction_str(interval[0]),
        "hi_exact": fraction_str(interval[1]),
        "lo_decimal": decimal_str(interval[0]),
        "hi_decimal": decimal_str(interval[1]),
        "width_exact": fraction_str(interval[1] - interval[0]),
        "width_decimal": decimal_str(interval[1] - interval[0]),
    }


# The JSON-facing entropy function carries a raw interval internally for
# downstream arithmetic in this module.
def entropy_interval(jets: Sequence[ProbabilityJet], target_bits: int = 180) -> Dict[str, Any]:
    raw = entropy_interval_raw(jets, target_bits)
    zero_terms = [subset_key(jet.subset) for jet in jets if jet.p == 0]
    return {
        "kind": "rigorous_interval",
        "rounding": "Exact rational atanh-series log enclosure; remainder has the sign of omitted positive tail.",
        "zero_probability_rule": "Terms with p=0 contribute lim_{p->0+} -p log(p)=0.",
        "interval": interval_json(raw),
        "interval_raw": raw,
        "zero_terms": zero_terms,
    }


def sign_classification(interval: Interval) -> str:
    lo, hi = interval
    if lo > 0:
        return "CERTIFIED_POSITIVE"
    if lo >= 0:
        return "CERTIFIED_NONNEGATIVE"
    if hi < 0:
        return "CERTIFIED_NEGATIVE"
    if hi <= 0:
        return "CERTIFIED_NONPOSITIVE"
    return "NOT_CERTIFIED"


def jets_json(jets: Sequence[ProbabilityJet]) -> List[Dict[str, str]]:
    return [
        {
            "subset": subset_key(jet.subset),
            "p": fraction_str(jet.p),
            "p_decimal": decimal_str(jet.p),
            "p1": fraction_str(jet.p1),
            "p2": fraction_str(jet.p2),
        }
        for jet in jets
    ]


def poly_eval(coeffs: Sequence[Fraction], x: Fraction) -> Fraction:
    total = Fraction(0)
    for coeff in reversed(coeffs):
        total = total * x + coeff
    return total


def compose_affine(coeffs: Sequence[Fraction], a: Fraction, width: Fraction) -> List[Fraction]:
    """Return coefficients of p(a + width*u)."""

    out = [Fraction(0)]
    for k, coeff in enumerate(coeffs):
        if coeff == 0:
            continue
        term = [Fraction(0) for _ in range(k + 1)]
        for j in range(k + 1):
            term[j] += coeff * Fraction(math.comb(k, j)) * (a ** (k - j)) * (width ** j)
        out = poly_add(out, term)
    return trim_poly(out)


def power_to_bernstein(power_coeffs: Sequence[Fraction], degree: Optional[int] = None) -> List[Fraction]:
    if degree is None:
        degree = len(power_coeffs) - 1
    if degree < 0:
        return []
    padded = list(power_coeffs) + [Fraction(0)] * (degree + 1 - len(power_coeffs))
    out: List[Fraction] = []
    for i in range(degree + 1):
        value = Fraction(0)
        for k in range(i + 1):
            value += padded[k] * Fraction(math.comb(i, k), math.comb(degree, k))
        out.append(value)
    return out


def bernstein_bounds(coeffs: Sequence[Fraction], t0: Fraction, t1: Fraction) -> Dict[str, Any]:
    if not t0 <= t1:
        raise ReferenceInputError("Interval requires t0 <= t1")
    if t0 == t1:
        value = poly_eval(coeffs, t0)
        return {
            "method": "point",
            "coefficients": [fraction_str(value)],
            "bounds": interval_json((value, value)),
            "classification": sign_classification((value, value)),
        }
    transformed = compose_affine(coeffs, t0, t1 - t0)
    degree = len(transformed) - 1
    bernstein = power_to_bernstein(transformed, degree)
    lo = min(bernstein)
    hi = max(bernstein)
    return {
        "method": "bernstein_power_to_basis",
        "degree": degree,
        "bernstein_coefficients": [fraction_str(x) for x in bernstein],
        "bounds": interval_json((lo, hi)),
        "classification": sign_classification((lo, hi)),
    }


def feasibility_report(k: Matrix, d: Matrix, t0: Fraction, t1: Fraction, mode: str) -> Dict[str, Any]:
    polys = event_probability_polynomials(k, d, mode)
    reports = []
    worst = "CERTIFIED_NONNEGATIVE"
    for subset in all_subsets(len(k)):
        bounds = bernstein_bounds(polys[subset], t0, t1)
        classification = bounds["classification"]
        if classification in {"CERTIFIED_NEGATIVE", "CERTIFIED_NONPOSITIVE"}:
            worst = "REJECTED"
        elif classification == "NOT_CERTIFIED" and worst != "REJECTED":
            worst = "NOT_CERTIFIED"
        reports.append(
            {
                "subset": subset_key(subset),
                "polynomial_coefficients": [fraction_str(x) for x in polys[subset]],
                "bounds": bounds,
            }
        )
    note = (
        "L-ensemble interval feasibility checks nonnegative determinant weights; det(I+L) is positive once "
        "all weights are nonnegative because the empty-subset weight is 1."
        if mode == "l_ensemble"
        else "Marginal-kernel interval feasibility checks exact event probabilities from inclusion-exclusion, not inclusion minors."
    )
    return {
        "mode": mode,
        "interval": [fraction_str(t0), fraction_str(t1)],
        "status": worst,
        "rationale": note,
        "events": reports,
    }


def float_entropy_from_jets(jets: Sequence[ProbabilityJet]) -> float:
    total = 0.0
    for jet in jets:
        p = float(jet.p)
        if p > 0.0:
            total -= p * math.log(p)
    return total


def float_chord_gap(k: Matrix, d: Matrix, t0: Fraction, t: Fraction, t1: Fraction, mode: str) -> float:
    h0 = float_entropy_from_jets(probability_jets(k, d, t0, mode))
    hm = float_entropy_from_jets(probability_jets(k, d, t, mode))
    h1 = float_entropy_from_jets(probability_jets(k, d, t1, mode))
    alpha = float((t1 - t) / (t1 - t0))
    beta = float((t - t0) / (t1 - t0))
    return hm - alpha * h0 - beta * h1


def check_candidate(candidate: Mapping[str, Any], analyses: Mapping[str, Any]) -> Dict[str, Any]:
    claim = candidate.get("claim")
    if claim != "chord_gap_lower_bound":
        return {"claim": claim, "status": "UNSUPPORTED_CANDIDATE", "reason": "Only chord_gap_lower_bound is implemented."}
    lower = parse_fraction(candidate["lower_bound"])
    gap = analyses.get("chord_gap")
    if not gap:
        return {"claim": claim, "status": "REJECTED", "reason": "No chord gap analysis is available."}
    lo = parse_fraction(gap["interval"]["lo_exact"])
    if lo >= lower:
        status = "ACCEPTED_BY_REFERENCE"
        reason = "Certified lower endpoint is at least the claimed lower bound."
    else:
        status = "REJECTED"
        reason = "Certified lower endpoint is below the claimed lower bound; float-sized positives are not enough."
    return {
        "claim": claim,
        "claimed_lower_bound": fraction_str(lower),
        "certified_gap_lower": fraction_str(lo),
        "status": status,
        "reason": reason,
    }


def parse_case(case: Mapping[str, Any]) -> Tuple[Matrix, Matrix, str]:
    mode = str(case.get("mode", "l_ensemble"))
    if mode not in VALID_MODES:
        raise ReferenceInputError(f"Unknown mode {mode!r}")
    k = parse_matrix(case.get("K"), "K")
    d = parse_matrix(case.get("D"), "D")
    validate_pair(k, d)
    return k, d, mode


def analyze_case(case: Mapping[str, Any]) -> Dict[str, Any]:
    name = str(case.get("name", "unnamed"))
    try:
        k, d, mode = parse_case(case)
        target_bits = int(case.get("target_bits", 180))
        analyses: Dict[str, Any] = {
            "name": name,
            "mode": mode,
            "status": "CANDIDATE",
            "labels": {
                "determinants_and_jets": "exact",
                "entropy_and_gap": "rigorous_interval",
                "float_diagnostics": "diagnostic_only",
            },
        }
        if "feasibility_interval" in case:
            a, b = [parse_fraction(x) for x in case["feasibility_interval"]]
            analyses["feasibility"] = feasibility_report(k, d, a, b, mode)
            if analyses["feasibility"]["status"] == "REJECTED":
                analyses["status"] = "REJECTED_INPUT"
        if "entropy_points" in case:
            analyses["entropy_points"] = [
                entropy_at(k, d, parse_fraction(t), mode, target_bits) for t in case["entropy_points"]
            ]
        if "curvature_at" in case:
            t = parse_fraction(case["curvature_at"])
            analyses["curvature"] = curvature_interval(probability_jets(k, d, t, mode), target_bits)
        if "chord_gap" in case:
            spec = case["chord_gap"]
            t0 = parse_fraction(spec["t0"])
            t = parse_fraction(spec["t"])
            t1 = parse_fraction(spec["t1"])
            analyses["chord_gap"] = chord_gap_interval(k, d, t0, t, t1, mode, target_bits)
            if spec.get("float_diagnostic"):
                analyses["float_chord_gap"] = {
                    "kind": "diagnostic_only",
                    "value": repr(float_chord_gap(k, d, t0, t, t1, mode)),
                    "warning": "Double precision is not used for certificate decisions.",
                }
        if "candidate" in case:
            analyses["candidate_check"] = check_candidate(case["candidate"], analyses)
        return attach_hash(strip_raw_intervals(analyses))
    except Exception as exc:
        status = "REJECTED_INPUT" if isinstance(exc, ReferenceInputError) else "ERROR"
        result = {
            "name": name,
            "status": status,
            "error_type": type(exc).__name__,
            "error": str(exc),
        }
        return attach_hash(result)


def strip_raw_intervals(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: strip_raw_intervals(v) for k, v in value.items() if k != "interval_raw"}
    if isinstance(value, list):
        return [strip_raw_intervals(v) for v in value]
    if isinstance(value, tuple):
        return [strip_raw_intervals(v) for v in value]
    return value


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def attach_hash(result: Dict[str, Any]) -> Dict[str, Any]:
    body = {k: v for k, v in result.items() if k != "certificate_hash"}
    result["certificate_hash"] = hashlib.sha256(canonical_json(body).encode("utf-8")).hexdigest()
    return result


def atomic_write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def run_cases(cases_path: Path, output_dir: Path, stop_after: Optional[int] = None) -> Dict[str, Any]:
    cases_path = cases_path.resolve()
    data = json.loads(cases_path.read_text(encoding="utf-8"))
    cases = data["cases"] if isinstance(data, dict) else data
    if not isinstance(cases, list):
        raise ReferenceInputError("Case file must contain a list or {'cases': [...]}")

    completed = []
    for index, case in enumerate(cases):
        if stop_after is not None and index >= stop_after:
            break
        result = analyze_case(case)
        out_path = output_dir / f"{result['name']}.json"
        atomic_write_json(out_path, result)
        completed.append({"name": result["name"], "status": result["status"], "hash": result["certificate_hash"]})

    try:
        case_file_label = cases_path.relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        case_file_label = cases_path.name
    manifest = {
        "case_file": case_file_label,
        "python_version": ".".join(str(x) for x in sys.version_info[:3]),
        "implementation": "research/T3/reference/exact_dpp_reference.py",
        "completed_count": len(completed),
        "total_count": len(cases),
        "complete": len(completed) == len(cases),
        "completed": completed,
    }
    atomic_write_json(output_dir / "manifest.json", attach_hash(manifest))
    return manifest


def default_cases_path() -> Path:
    return Path(__file__).with_name("adversarial_cases.json")


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Run independent small-n DPP entropy reference cases.")
    parser.add_argument("--cases", type=Path, default=default_cases_path())
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).with_name("out"))
    parser.add_argument("--stop-after", type=int, default=None, help="Write only the first N cases, to test restart behavior.")
    args = parser.parse_args(argv)

    manifest = run_cases(args.cases, args.output_dir, args.stop_after)
    print(json.dumps(manifest, sort_keys=True, indent=2, ensure_ascii=True))
    return 0 if manifest["complete"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
