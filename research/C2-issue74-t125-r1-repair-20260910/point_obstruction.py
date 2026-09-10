#!/usr/bin/env python3
"""Rigorous point obstruction for the PR91 Hessian-only certificate.

The calculation uses exact rational arithmetic for every algebraic operation.
Only logarithms need transcendental enclosures; those are evaluated with
Python Decimal at 96 decimal digits and enlarged by a dynamically computed
rational pad.  Decimal.ln is correctly rounded in ROUND_HALF_EVEN mode.

This program does not claim a curvature sign.  It tests whether the frozen
PR98 degree-10 trial can possibly satisfy the PR91 residual gate at t=5/4.  A
positive lower obstruction margin at one legal state proves that no choice of
valid global upper residual bounds for that same trial can make the gate
negative at that parameter.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import sys
import time
from dataclasses import dataclass
from decimal import Context, Decimal, ROUND_HALF_EVEN, localcontext
from fractions import Fraction
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple


CERT_BITS = 256
DECIMAL_PREC = 96  # > 256/log2(10) decimal digits
LOG_CONTEXT = Context(prec=DECIMAL_PREC, rounding=ROUND_HALF_EVEN)


def f(value) -> Fraction:
    if isinstance(value, Fraction):
        return value
    if isinstance(value, Decimal):
        return Fraction(value)
    if isinstance(value, int):
        return Fraction(value, 1)
    if isinstance(value, str):
        return Fraction(Decimal(value))
    raise TypeError(f"cannot convert {type(value)!r} to Fraction")


@dataclass(frozen=True)
class Interval:
    lo: Fraction
    hi: Fraction

    def __post_init__(self) -> None:
        if self.lo > self.hi:
            raise ValueError("reversed interval")

    @staticmethod
    def exact(value) -> "Interval":
        q = f(value)
        return Interval(q, q)

    def __add__(self, other) -> "Interval":
        other = as_interval(other)
        return Interval(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self) -> "Interval":
        return Interval(-self.hi, -self.lo)

    def __sub__(self, other) -> "Interval":
        return self + (-as_interval(other))

    def __rsub__(self, other) -> "Interval":
        return as_interval(other) - self

    def __mul__(self, other) -> "Interval":
        other = as_interval(other)
        products = (
            self.lo * other.lo,
            self.lo * other.hi,
            self.hi * other.lo,
            self.hi * other.hi,
        )
        return Interval(min(products), max(products))

    __rmul__ = __mul__

    def reciprocal(self) -> "Interval":
        if self.lo <= 0 <= self.hi:
            raise ZeroDivisionError("interval contains zero")
        return Interval(Fraction(1, 1) / self.hi, Fraction(1, 1) / self.lo)

    def __truediv__(self, other) -> "Interval":
        return self * as_interval(other).reciprocal()

    def __rtruediv__(self, other) -> "Interval":
        return as_interval(other) / self

    def abs_lower(self) -> Fraction:
        if self.lo <= 0 <= self.hi:
            return Fraction(0)
        return min(abs(self.lo), abs(self.hi))

    def abs_upper(self) -> Fraction:
        return max(abs(self.lo), abs(self.hi))


def as_interval(value) -> Interval:
    return value if isinstance(value, Interval) else Interval.exact(value)


def decimal_ln_fraction(q: Fraction) -> Tuple[Fraction, Fraction, dict]:
    if q <= 0:
        raise ValueError("logarithm argument must be positive")
    with localcontext(LOG_CONTEXT) as ctx:
        ln_num = ctx.ln(Decimal(q.numerator))
        ln_den = ctx.ln(Decimal(q.denominator))
        rounded = ctx.subtract(ln_num, ln_den)
        max_adjusted = max(ln_num.adjusted(), ln_den.adjusted(), rounded.adjusted())
        # Each elementary result is correctly rounded.  Three rounding errors
        # are dominated by 10^(max_adjusted-prec+3).
        pad_dec = Decimal(1).scaleb(max_adjusted - DECIMAL_PREC + 3)
    center = Fraction(rounded)
    pad = Fraction(pad_dec)
    return center - pad, center + pad, {
        "decimal_precision": DECIMAL_PREC,
        "rounded": str(rounded),
        "pad": str(pad_dec),
    }


LOG_AUDIT: List[dict] = []


def interval_log(a: Interval) -> Interval:
    if a.lo <= 0:
        raise ValueError("nonpositive logarithm interval")
    lo, _, lo_meta = decimal_ln_fraction(a.lo)
    _, hi, hi_meta = decimal_ln_fraction(a.hi)
    LOG_AUDIT.append({"input_lo": rational_text(a.lo), "input_hi": rational_text(a.hi),
                      "lo_eval": lo_meta, "hi_eval": hi_meta})
    return Interval(lo, hi)


# Normalized multivariate Taylor coefficients.  State total degree is at most
# two; parameter degree is at most two.  Coefficients equal D^alpha/alpha!.
Index = Tuple[int, int, int, int]
INDICES: Tuple[Index, ...] = tuple(sorted(
    ((i, j, k, ell)
     for i in range(3)
     for j in range(3)
     for k in range(3)
     for ell in range(3)
     if i + j + k <= 2),
    key=lambda a: (sum(a), a),
))
INDEX_SET = set(INDICES)
ZERO_INDEX: Index = (0, 0, 0, 0)
UNIT_INDICES: Tuple[Index, ...] = (
    (1, 0, 0, 0),
    (0, 1, 0, 0),
    (0, 0, 1, 0),
    (0, 0, 0, 1),
)


def add_index(a: Index, b: Index) -> Index:
    return tuple(a[i] + b[i] for i in range(4))  # type: ignore[return-value]


def sub_index(a: Index, b: Index) -> Index:
    return tuple(a[i] - b[i] for i in range(4))  # type: ignore[return-value]


PRODUCT_PAIRS: Dict[Index, Tuple[Tuple[Index, Index], ...]] = {}
for alpha in INDICES:
    pairs = []
    for beta in INDICES:
        if all(beta[i] <= alpha[i] for i in range(4)):
            gamma = sub_index(alpha, beta)
            if gamma in INDEX_SET:
                pairs.append((beta, gamma))
    PRODUCT_PAIRS[alpha] = tuple(pairs)


class Jet:
    __slots__ = ("c",)

    def __init__(self, coefficients: Dict[Index, Interval] | None = None):
        self.c = {alpha: Interval.exact(0) for alpha in INDICES}
        if coefficients:
            self.c.update(coefficients)

    @staticmethod
    def constant(value) -> "Jet":
        return Jet({ZERO_INDEX: as_interval(value)})

    @staticmethod
    def variable(value, dimension: int) -> "Jet":
        return Jet({ZERO_INDEX: as_interval(value), UNIT_INDICES[dimension]: Interval.exact(1)})

    def __add__(self, other) -> "Jet":
        other = as_jet(other)
        return Jet({alpha: self.c[alpha] + other.c[alpha] for alpha in INDICES})

    __radd__ = __add__

    def __neg__(self) -> "Jet":
        return Jet({alpha: -self.c[alpha] for alpha in INDICES})

    def __sub__(self, other) -> "Jet":
        return self + (-as_jet(other))

    def __rsub__(self, other) -> "Jet":
        return as_jet(other) - self

    def __mul__(self, other) -> "Jet":
        other = as_jet(other)
        out: Dict[Index, Interval] = {}
        zero = Interval.exact(0)
        for alpha in INDICES:
            total = zero
            for beta, gamma in PRODUCT_PAIRS[alpha]:
                total = total + self.c[beta] * other.c[gamma]
            out[alpha] = total
        return Jet(out)

    __rmul__ = __mul__

    def reciprocal(self) -> "Jet":
        out: Dict[Index, Interval] = {ZERO_INDEX: self.c[ZERO_INDEX].reciprocal()}
        zero = Interval.exact(0)
        for alpha in INDICES[1:]:
            total = zero
            for beta, gamma in PRODUCT_PAIRS[alpha]:
                if beta == ZERO_INDEX:
                    continue
                total = total + self.c[beta] * out[gamma]
            out[alpha] = -out[ZERO_INDEX] * total
        return Jet(out)

    def __truediv__(self, other) -> "Jet":
        return self * as_jet(other).reciprocal()

    def __rtruediv__(self, other) -> "Jet":
        return as_jet(other) / self

    def __pow__(self, exponent: int) -> "Jet":
        if exponent < 0:
            return (self.reciprocal()) ** (-exponent)
        result = Jet.constant(1)
        base = self
        n = exponent
        while n:
            if n & 1:
                result = result * base
            n >>= 1
            if n:
                base = base * base
        return result

    def log(self) -> "Jet":
        inv = self.reciprocal()
        out: Dict[Index, Interval] = {ZERO_INDEX: interval_log(self.c[ZERO_INDEX])}
        zero = Interval.exact(0)
        for alpha in INDICES[1:]:
            dimension = next(i for i, value in enumerate(alpha) if value)
            target = list(alpha)
            target[dimension] -= 1
            target_index = tuple(target)  # type: ignore[assignment]
            total = zero
            for beta, gamma in PRODUCT_PAIRS[target_index]:
                shifted = list(beta)
                shifted[dimension] += 1
                shifted_index = tuple(shifted)  # type: ignore[assignment]
                if shifted_index not in INDEX_SET:
                    continue
                derivative_coefficient = self.c[shifted_index] * shifted[dimension]
                total = total + derivative_coefficient * inv.c[gamma]
            out[alpha] = total / alpha[dimension]
        return Jet(out)


def as_jet(value) -> Jet:
    return value if isinstance(value, Jet) else Jet.constant(value)


def load_json_decimal(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle, parse_float=Decimal, parse_int=int)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def polynomial(coefficients: Sequence, exponents: Sequence[Sequence[int]], coordinates: Sequence[Jet]) -> Jet:
    scaled = [8 * coordinate for coordinate in coordinates]
    powers: List[List[Jet]] = []
    for coordinate in scaled:
        row = [Jet.constant(1)]
        for _ in range(10):
            row.append(row[-1] * coordinate)
        powers.append(row)
    total = Jet.constant(0)
    for coefficient, exponent in zip(coefficients, exponents):
        term = powers[0][exponent[0]] * powers[1][exponent[1]] * powers[2][exponent[2]]
        total = total + f(coefficient) * term
    return total


def branch_data(x: Jet, y: Jet, z: Jet, t: Jet, sign_a: int, sign_b: int):
    q = t / 16
    diagonal = Fraction(1, 8)
    left = Fraction(sign_a, 2) - x
    right = Fraction(sign_b, 2) - y
    off = q - z
    determinant = left * right - off * off
    weight = sign_a * sign_b * determinant
    r00 = right / determinant
    r01 = -off / determinant
    r11 = left / determinant
    tx = diagonal * diagonal * r00
    tz = diagonal * q * r00 + diagonal * diagonal * r01
    ty = q * q * r00 + 2 * q * diagonal * r01 + diagonal * diagonal * r11
    return weight, (tx, ty, tz)


def hessian_intervals(jet: Jet, parameter_order: int) -> Dict[str, Interval]:
    def coefficient(ix: int, iy: int, iz: int) -> Interval:
        # The t derivative order is one for r1 and zero for r0.  The normalized
        # coefficient must be multiplied by the state multi-index factorial.
        alpha = (ix, iy, iz, parameter_order)
        factor = 2 if (ix == 2 or iy == 2 or iz == 2) else 1
        return jet.c[alpha] * factor
    return {
        "xx": coefficient(2, 0, 0),
        "yy": coefficient(0, 2, 0),
        "zz": coefficient(0, 0, 2),
        "xy": coefficient(1, 1, 0),
        "xz": coefficient(1, 0, 1),
        "yz": coefficient(0, 1, 1),
    }


def directional_hessian_lower(hessian: Dict[str, Interval]) -> Tuple[Fraction, str]:
    candidates = {
        "Q11 unit direction": hessian["xx"].abs_lower(),
        "Q22 unit direction": hessian["yy"].abs_lower(),
        "normalized off-diagonal direction": hessian["zz"].abs_lower() / 2,
    }
    label = max(candidates, key=candidates.get)
    return candidates[label], label


def rational_text(q: Fraction) -> str:
    return str(q.numerator) if q.denominator == 1 else f"{q.numerator}/{q.denominator}"


def decimal_text(q: Fraction, digits: int = 40) -> str:
    with localcontext(Context(prec=digits, rounding=ROUND_HALF_EVEN)):
        return str(Decimal(q.numerator) / Decimal(q.denominator))


def interval_record(a: Interval) -> dict:
    return {
        "lo": rational_text(a.lo),
        "hi": rational_text(a.hi),
        "lo_decimal": decimal_text(a.lo),
        "hi_decimal": decimal_text(a.hi),
    }


def evaluate_point(exponents, u_coefficients, v_coefficients, w_coefficients,
                   c2: Fraction, t_value: Fraction) -> dict:
    global LOG_AUDIT
    LOG_AUDIT = []
    x = Jet.variable(Fraction(0), 0)
    y = Jet.variable(Fraction(0), 1)
    z = Jet.variable(Fraction(0), 2)
    t = Jet.variable(t_value, 3)
    q_coordinates = (x, y, z)
    uq = polynomial(u_coefficients, exponents, q_coordinates)
    vq = polynomial(v_coefficients, exponents, q_coordinates)
    wq = polynomial(w_coefficients, exponents, q_coordinates)

    entropy = Jet.constant(0)
    lu = Jet.constant(0)
    lv = Jet.constant(0)
    lw = Jet.constant(0)
    weight_sum = Jet.constant(0)
    weight_values = []
    for sign_a, sign_b in ((-1, -1), (-1, 1), (1, -1), (1, 1)):
        weight, image = branch_data(x, y, z, t, sign_a, sign_b)
        weight_sum = weight_sum + weight
        weight_values.append(weight.c[ZERO_INDEX])
        entropy = entropy - weight * weight.log()
        lu = lu + weight * polynomial(u_coefficients, exponents, image)
        lv = lv + weight * polynomial(v_coefficients, exponents, image)
        lw = lw + weight * polynomial(w_coefficients, exponents, image)

    r0_jet = entropy - (uq - lu)
    first_source = entropy + lu
    # r1 Hessian: D_Q^2 [partial_t(B+Lu) - (I-L)v].  Constants disappear.
    h0 = hessian_intervals(r0_jet, 0)
    h1 = {}
    for name, state_alpha in {
        "xx": (2, 0, 0, 1), "yy": (0, 2, 0, 1), "zz": (0, 0, 2, 1),
        "xy": (1, 1, 0, 1), "xz": (1, 0, 1, 1), "yz": (0, 1, 1, 1),
    }.items():
        state_factor = 2 if 2 in state_alpha[:3] else 1
        fixed_t_alpha = state_alpha[:3] + (0,)
        # r1=partial_t(B+Lu)-c1-v+Lv.  Only the first term is extracted at
        # parameter order one; -v+Lv is evaluated at fixed t (order zero).
        h1[name] = (
            first_source.c[state_alpha]
            - vq.c[fixed_t_alpha]
            + lv.c[fixed_t_alpha]
        ) * state_factor

    h0_lower, h0_direction = directional_hessian_lower(h0)
    h1_lower, h1_direction = directional_hessian_lower(h1)
    # r2=B_tt+L_tt u+2L_t v-c2-(I-L)w.
    r2 = 2 * first_source.c[(0, 0, 0, 2)] + 2 * lv.c[(0, 0, 0, 1)]
    r2 = r2 - c2 - (wq.c[ZERO_INDEX] - lw.c[ZERO_INDEX])
    r2_lower = r2.abs_lower()
    obstruction = c2 / 2 + h0_lower / 2 + Fraction(9, 100) * h1_lower + r2_lower / 2

    return {
        "point": {"Q11": "0", "Q22": "0", "Q12": "0", "t": rational_text(t_value)},
        "domain_membership": "Q=0 satisfies (1/8)I+Q>=0 and (1/8)I-Q>=0 exactly",
        "weights": [interval_record(value) for value in weight_values],
        "weight_sum_value": interval_record(weight_sum.c[ZERO_INDEX]),
        "r0_state_hessian": {name: interval_record(value) for name, value in h0.items()},
        "r1_state_hessian": {name: interval_record(value) for name, value in h1.items()},
        "r2": interval_record(r2),
        "lower_bounds": {
            "e02": rational_text(h0_lower),
            "e02_decimal": decimal_text(h0_lower),
            "e02_witness": h0_direction,
            "e12": rational_text(h1_lower),
            "e12_decimal": decimal_text(h1_lower),
            "e12_witness": h1_direction,
            "e20": rational_text(r2_lower),
            "e20_decimal": decimal_text(r2_lower),
        },
        "c2_over_2": {"exact": rational_text(c2 / 2), "decimal": decimal_text(c2 / 2)},
        "obstruction_margin_lower": {
            "exact": rational_text(obstruction),
            "decimal": decimal_text(obstruction),
        },
        "gate_impossible_for_frozen_trial_at_point": obstruction > 0,
        "log_enclosures": LOG_AUDIT,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--meta", required=True, type=Path)
    parser.add_argument("--u", required=True, type=Path)
    parser.add_argument("--v", required=True, type=Path)
    parser.add_argument("--w", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    started_wall = time.time()
    started_mono = time.monotonic()

    meta = load_json_decimal(args.meta)
    u_data = load_json_decimal(args.u)
    v_data = load_json_decimal(args.v)
    w_data = load_json_decimal(args.w)
    exponents = u_data["exponents"]
    if len(exponents) != 285:
        raise ValueError(f"expected 285 degree-10 monomials, found {len(exponents)}")
    if not (len(u_data["u"]) == len(v_data["v"]) == len(w_data["w"]) == len(exponents)):
        raise ValueError("coefficient lengths do not match exponent ordering")
    c2 = f(w_data["c2"])

    points = [
        evaluate_point(exponents, u_data["u"], v_data["v"], w_data["w"], c2, Fraction(5, 4)),
    ]
    any_obstruction = any(point["gate_impossible_for_frozen_trial_at_point"] for point in points)
    finished_wall = time.time()
    record = {
        "schema": "issue74-pr91-hessian-point-obstruction-v2-r1-fixed",
        "status": "RIGOROUS_TRIAL_SCHEME_OBSTRUCTION" if any_obstruction else "NO_POINT_OBSTRUCTION_FOUND",
        "interpretation": (
            "A legal state at t=5/4 gives a positive lower bound for the PR91 Hessian-only "
            "certificate expression. Therefore the frozen PR98 degree-10 trial cannot certify "
            "the PR91 gate at t=5/4. This is not a curvature sign."
            if any_obstruction else
            "The legal point check does not obstruct the frozen trial; no global certificate is claimed."
        ),
        "frozen_sources": {
            "PR91": "c7a072ec4eea0c5b0f445bca5796873a9e234948",
            "PR98": "55649309437a78d9e5174386d8d260a4ee9c02a1",
            "gate": "c2/2 + e02/2 + (9/100)e12 + e20/2 < 0",
        },
        "input_hashes_sha256": {
            "meta": sha256(args.meta), "u": sha256(args.u),
            "v": sha256(args.v), "w": sha256(args.w),
        },
        "input_meta": meta,
        "arithmetic": {
            "algebraic": "exact fractions",
            "transcendental": "Decimal.ln correctly rounded at 96 decimal digits plus rational outward pad",
            "certificate_bits": CERT_BITS,
            "decimal_precision": DECIMAL_PREC,
            "finite_differences": False,
            "sampling": False,
        },
        "process": {
            "pid": os.getpid(),
            "python": sys.version,
            "platform": platform.platform(),
            "started_unix": started_wall,
            "finished_unix": finished_wall,
            "elapsed_seconds": time.monotonic() - started_mono,
            "cpu_threads_used": 1,
            "gpu_used": False,
        },
        "points": points,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    temporary.write_text(
        json.dumps(record, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, args.output)
    print(json.dumps({
        "status": record["status"],
        "pid": record["process"]["pid"],
        "elapsed_seconds": record["process"]["elapsed_seconds"],
        "margins": [point["obstruction_margin_lower"]["decimal"] for point in points],
        "output": str(args.output.resolve()),
    }, sort_keys=True))
    return 0 if any_obstruction else 2


if __name__ == "__main__":
    raise SystemExit(main())
