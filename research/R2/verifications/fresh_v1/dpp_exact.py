from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, getcontext
from fractions import Fraction
from itertools import combinations
import json
import math
from typing import Iterable, List, Sequence, Tuple


Matrix = List[List[Fraction]]


def frac(x) -> Fraction:
    if isinstance(x, Fraction):
        return x
    if isinstance(x, int):
        return Fraction(x, 1)
    if isinstance(x, str):
        return Fraction(x)
    return Fraction(x)


def eye(n: int) -> Matrix:
    return [[Fraction(int(i == j), 1) for j in range(n)] for i in range(n)]


def mat_add(a: Matrix, b: Matrix) -> Matrix:
    return [[a[i][j] + b[i][j] for j in range(len(a))] for i in range(len(a))]


def mat_scale(c: Fraction, a: Matrix) -> Matrix:
    return [[c * a[i][j] for j in range(len(a))] for i in range(len(a))]


def mat_mul(a: Matrix, b: Matrix) -> Matrix:
    n = len(a)
    m = len(b[0])
    k = len(b)
    return [[sum(a[i][r] * b[r][j] for r in range(k)) for j in range(m)] for i in range(n)]


def transpose(a: Matrix) -> Matrix:
    return [list(row) for row in zip(*a)]


def submatrix(a: Matrix, rows: Sequence[int], cols: Sequence[int] | None = None) -> Matrix:
    if cols is None:
        cols = rows
    return [[a[i][j] for j in cols] for i in rows]


def det_fraction(a: Matrix) -> Fraction:
    n = len(a)
    if n == 0:
        return Fraction(1, 1)
    m = [row[:] for row in a]
    det = Fraction(1, 1)
    for i in range(n):
        pivot = None
        for r in range(i, n):
            if m[r][i] != 0:
                pivot = r
                break
        if pivot is None:
            return Fraction(0, 1)
        if pivot != i:
            m[i], m[pivot] = m[pivot], m[i]
            det = -det
        pv = m[i][i]
        det *= pv
        for r in range(i + 1, n):
            if m[r][i] == 0:
                continue
            factor = m[r][i] / pv
            for c in range(i, n):
                m[r][c] -= factor * m[i][c]
    return det


def inverse_fraction(a: Matrix) -> Matrix:
    n = len(a)
    aug = [a[i][:] + [Fraction(int(i == j), 1) for j in range(n)] for i in range(n)]
    for i in range(n):
        pivot = None
        for r in range(i, n):
            if aug[r][i] != 0:
                pivot = r
                break
        if pivot is None:
            raise ValueError("singular matrix")
        if pivot != i:
            aug[i], aug[pivot] = aug[pivot], aug[i]
        pv = aug[i][i]
        for c in range(2 * n):
            aug[i][c] /= pv
        for r in range(n):
            if r == i or aug[r][i] == 0:
                continue
            factor = aug[r][i]
            for c in range(2 * n):
                aug[r][c] -= factor * aug[i][c]
    return [row[n:] for row in aug]


def projection_from_integer_columns(cols: Sequence[Sequence[int]]) -> Matrix:
    b = [[Fraction(x, 1) for x in row] for row in cols]
    bt = transpose(b)
    gram = mat_mul(bt, b)
    if det_fraction(gram) == 0:
        raise ValueError("columns are rank deficient")
    return mat_mul(mat_mul(b, inverse_fraction(gram)), bt)


def affine_projection_kernel(p: Matrix, alpha: Fraction, beta: Fraction) -> Matrix:
    n = len(p)
    return mat_add(mat_scale(beta, eye(n)), mat_scale(alpha - beta, p))


def principal_inclusion_probabilities(k: Matrix) -> List[Fraction]:
    n = len(k)
    out = [Fraction(0, 1)] * (1 << n)
    out[0] = Fraction(1, 1)
    for mask in range(1, 1 << n):
        idx = [i for i in range(n) if (mask >> i) & 1]
        out[mask] = det_fraction(submatrix(k, idx))
    return out


def exact_event_probabilities(k: Matrix) -> List[Fraction]:
    n = len(k)
    inc = principal_inclusion_probabilities(k)
    probs = [Fraction(0, 1)] * (1 << n)
    full = (1 << n) - 1
    for s in range(1 << n):
        comp = full ^ s
        sub = comp
        total = Fraction(0, 1)
        while True:
            sign = -1 if (sub.bit_count() & 1) else 1
            total += sign * inc[s | sub]
            if sub == 0:
                break
            sub = (sub - 1) & comp
        probs[s] = total
    return probs


def min_fraction(xs: Iterable[Fraction]) -> Fraction:
    return min(xs, default=Fraction(0, 1))


def max_abs_denominator(xs: Iterable[Fraction]) -> int:
    return max((x.denominator for x in xs), default=1)


@dataclass(frozen=True)
class LogIntervalConfig:
    terms: int = 140
    decimal_digits: int = 80


def _ln_y_interval_1_to_2(y: Fraction, terms: int) -> Tuple[Fraction, Fraction]:
    if y == 1:
        return Fraction(0, 1), Fraction(0, 1)
    if not (Fraction(1, 1) < y <= Fraction(2, 1)):
        raise ValueError(f"expected 1 < y <= 2, got {y}")
    q = (y - 1) / (y + 1)
    q2 = q * q
    power = q
    partial = Fraction(0, 1)
    for j in range(terms):
        partial += power / (2 * j + 1)
        power *= q2
    lower = 2 * partial
    # Tail is 2 * sum_{j >= terms} q^(2j+1)/(2j+1).
    # Since 1/(2j+1) <= 1/(2*terms+1), this is bounded by
    # 2*q^(2*terms+1)/((2*terms+1)*(1-q^2)).
    tail = 2 * power / ((2 * terms + 1) * (1 - q2))
    return lower, lower + tail


def ln_fraction_interval(x: Fraction, cfg: LogIntervalConfig) -> Tuple[Fraction, Fraction]:
    if x <= 0:
        raise ValueError("log only defined for positive rationals")
    if x == 1:
        return Fraction(0, 1), Fraction(0, 1)
    ln2_lo, ln2_hi = _ln_y_interval_1_to_2(Fraction(2, 1), cfg.terms)
    y = x
    shift = 0
    while y < 1:
        y *= 2
        shift += 1
    while y >= 2:
        y /= 2
        shift -= 1
    y_lo, y_hi = _ln_y_interval_1_to_2(y, cfg.terms) if y != 1 else (Fraction(0, 1), Fraction(0, 1))
    if shift >= 0:
        return y_lo - shift * ln2_hi, y_hi - shift * ln2_lo
    return y_lo + (-shift) * ln2_lo, y_hi + (-shift) * ln2_hi


def entropy_interval(probs: Sequence[Fraction], cfg: LogIntervalConfig) -> Tuple[Fraction, Fraction]:
    lower = Fraction(0, 1)
    upper = Fraction(0, 1)
    for p in probs:
        if p < 0:
            raise ValueError(f"negative event probability {p}")
        if p == 0:
            continue
        lo, hi = ln_fraction_interval(p, cfg)
        lower += -p * hi
        upper += -p * lo
    return lower, upper


def chord_gap_interval(k_minus: Matrix, k_plus: Matrix, cfg: LogIntervalConfig) -> dict:
    n = len(k_minus)
    mid = mat_scale(Fraction(1, 2), mat_add(k_minus, k_plus))
    probs_minus = exact_event_probabilities(k_minus)
    probs_plus = exact_event_probabilities(k_plus)
    probs_mid = exact_event_probabilities(mid)
    hm = entropy_interval(probs_minus, cfg)
    hp = entropy_interval(probs_plus, cfg)
    h0 = entropy_interval(probs_mid, cfg)
    gap_lo = (hm[0] + hp[0]) / 2 - h0[1]
    gap_hi = (hm[1] + hp[1]) / 2 - h0[0]
    return {
        "n": n,
        "event_probabilities": {
            "minus": probs_minus,
            "plus": probs_plus,
            "mid": probs_mid,
        },
        "checks": {
            "sum_minus": sum(probs_minus),
            "sum_plus": sum(probs_plus),
            "sum_mid": sum(probs_mid),
            "min_minus": min_fraction(probs_minus),
            "min_plus": min_fraction(probs_plus),
            "min_mid": min_fraction(probs_mid),
            "zero_minus": sum(1 for p in probs_minus if p == 0),
            "zero_plus": sum(1 for p in probs_plus if p == 0),
            "zero_mid": sum(1 for p in probs_mid if p == 0),
            "max_probability_denominator": max_abs_denominator(probs_minus + probs_plus + probs_mid),
        },
        "entropy_interval": {
            "minus": hm,
            "plus": hp,
            "mid": h0,
        },
        "gap_interval": (gap_lo, gap_hi),
        "strict_positive": gap_lo > 0,
        "strict_negative": gap_hi < 0,
    }


def fraction_to_decimal(x: Fraction, digits: int = 50) -> str:
    getcontext().prec = digits
    return str(Decimal(x.numerator) / Decimal(x.denominator))


def fraction_to_json(x: Fraction) -> dict:
    return {"num": x.numerator, "den": x.denominator}


def matrix_to_json(m: Matrix) -> list:
    return [[fraction_to_json(x) for x in row] for row in m]


def interval_to_json(interval: Tuple[Fraction, Fraction], digits: int = 50) -> dict:
    lo, hi = interval
    return {
        "lower": fraction_to_json(lo),
        "upper": fraction_to_json(hi),
        "lower_decimal": fraction_to_decimal(lo, digits),
        "upper_decimal": fraction_to_decimal(hi, digits),
    }


def probabilities_to_json(probs: Sequence[Fraction], digits: int = 40) -> list:
    return [
        {
            "mask": mask,
            "probability": fraction_to_json(p),
            "decimal": fraction_to_decimal(p, digits),
        }
        for mask, p in enumerate(probs)
    ]


def float_entropy_from_probs(probs: Sequence[Fraction]) -> float:
    vals = [float(p) for p in probs]
    return -sum(p * math.log(p) for p in vals if p > 0.0)


def summarize_certificate(k_minus: Matrix, k_plus: Matrix, cfg: LogIntervalConfig) -> dict:
    cert = chord_gap_interval(k_minus, k_plus, cfg)
    probs = cert["event_probabilities"]
    return {
        "n": cert["n"],
        "K_minus": matrix_to_json(k_minus),
        "K_plus": matrix_to_json(k_plus),
        "K_mid": matrix_to_json(mat_scale(Fraction(1, 2), mat_add(k_minus, k_plus))),
        "checks": {k: fraction_to_json(v) if isinstance(v, Fraction) else v for k, v in cert["checks"].items()},
        "entropy_interval": {
            key: interval_to_json(value, cfg.decimal_digits)
            for key, value in cert["entropy_interval"].items()
        },
        "gap_interval": interval_to_json(cert["gap_interval"], cfg.decimal_digits),
        "strict_positive": cert["strict_positive"],
        "strict_negative": cert["strict_negative"],
        "event_probabilities": {
            key: probabilities_to_json(value, 40)
            for key, value in probs.items()
        },
        "log_interval_terms": cfg.terms,
    }

