#!/usr/bin/env python3
"""Outward-rational interval supplement for previously computed certificates."""

from __future__ import annotations

import hashlib
import json
import os
import sys
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

import finite_noncommuting_bsc_cert as finite
import n5_projection_q_check as qcheck


def fs(x: F) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def fixed_decimal(x: F, places: int = 18) -> str:
    sign = "-" if x < 0 else ""
    x = abs(x)
    whole = x.numerator // x.denominator
    rem = x.numerator % x.denominator
    frac = (rem * (10 ** places)) // x.denominator
    return f"{sign}{whole}.{frac:0{places}d}"


def outward(lo: F, hi: F, scale: int):
    lower_scaled = (lo.numerator * scale) // lo.denominator
    upper_scaled = -((-hi.numerator * scale) // hi.denominator)
    return F(lower_scaled, scale), F(upper_scaled, scale)


def q_entropy_interval(terms: int):
    a = [F(x) for x in (1, 2, 3, 4, 5)]
    b = [F(x) for x in (2, -1, 3, -2, 1)]
    u = [row[:3] for row in qcheck.mm(qcheck.householder(a), qcheck.householder(b))]
    weights = []
    for rows in combinations(range(5), 3):
        minor = [[u[i][j] for j in range(3)] for i in rows]
        weights.append(qcheck.det(minor) ** 2)
    logs = qcheck.LogBounds(terms)
    lo = F(0)
    hi = F(0)
    for q in weights:
        lq, uq = logs.log(q)
        lo += -q * uq
        hi += -q * lq
    return lo, hi, logs.calls


def finite_intervals(terms: int):
    u, _z, a, v = finite.householder_fixture()
    t = F(1, 20)
    eps = F(1, 100)
    ka = finite.make_k(u, a)
    kv = finite.make_k(u, v)
    polys = {mask: finite.event_poly(ka, kv, mask) for mask in range(16)}
    center = {mask: finite.peval(polys[mask], F(0)) for mask in range(16)}
    minus = {mask: finite.peval(polys[mask], -t) for mask in range(16)}
    plus = {mask: finite.peval(polys[mask], t) for mask in range(16)}
    face_lo, face_hi, face_calls = finite.entropy_delta_interval(minus, center, plus, range(15), terms)

    k_minus = finite.make_k(u, finite.madd(a, finite.mscale(-t, v)))
    k_zero = ka
    k_plus = finite.make_k(u, finite.madd(a, finite.mscale(t, v)))
    lifted = {}
    for label, k in [("minus", k_minus), ("zero", k_zero), ("plus", k_plus)]:
        lifted[label] = finite.madd(finite.mscale(1 - 2 * eps, k), finite.mscale(eps, finite.eye(4)))
    lift_events = {label: {mask: finite.event_prob(k, mask) for mask in range(16)} for label, k in lifted.items()}
    lift_lo, lift_hi, lift_calls = finite.entropy_delta_interval(lift_events["minus"], lift_events["zero"], lift_events["plus"], range(16), terms)
    return (face_lo, face_hi, face_calls), (lift_lo, lift_hi, lift_calls)


def interval_record(lo: F, hi: F, scale: int, sign: str, display_values):
    out_lo, out_hi = outward(lo, hi, scale)
    display_lo, display_hi = outward(lo, hi, 10 ** 15)
    parsed = [F(v) for v in display_values]
    if sign == "positive_gt_3_over_2":
        strict = out_lo > F(3, 2)
    elif sign == "negative":
        strict = out_hi < 0
    else:
        raise ValueError(sign)
    return {
        "outward_scale": str(scale),
        "outward_lower": fs(out_lo),
        "outward_upper": fs(out_hi),
        "outward_lower_decimal": fixed_decimal(out_lo),
        "outward_upper_decimal": fixed_decimal(out_hi),
        "strict_sign_confirmed": strict,
        "display_envelope_scale": str(10 ** 15),
        "display_envelope_lower": fs(display_lo),
        "display_envelope_upper": fs(display_hi),
        "display_envelope_lower_decimal": fixed_decimal(display_lo, 15),
        "display_envelope_upper_decimal": fixed_decimal(display_hi, 15),
        "original_display_values_are_enveloped": all(display_lo <= x <= display_hi for x in parsed),
        "original_display_values_checked": display_values,
    }


def sha256_if_exists(path: Path):
    if not path.exists():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    if len(sys.argv) < 3:
        raise SystemExit("usage: interval_presentation_supplement.py REVIEW_DIR OUT_JSON")
    review_dir = Path(sys.argv[1])
    out = Path(sys.argv[2])
    script = Path(__file__).resolve()
    scale = 10 ** 18
    q_lo, q_hi, q_calls = q_entropy_interval(180)
    (face_lo, face_hi, face_calls), (lift_lo, lift_hi, lift_calls) = finite_intervals(48)
    result = {
        "pid": os.getpid(),
        "argv": sys.argv,
        "python": sys.version,
        "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
        "exit_status": 0,
        "rounding_rule": "lower=floor(exact_lower*scale)/scale, upper=ceil(exact_upper*scale)/scale",
        "exact_log_fraction_endpoints_saved": False,
        "source_output_sha256": {
            "n5_projection_q_certificate.json": sha256_if_exists(review_dir / "n5_projection_q_certificate.json"),
            "finite_noncommuting_bsc_certificate.json": sha256_if_exists(review_dir / "finite_noncommuting_bsc_certificate.json"),
        },
        "q_entropy": {
            **interval_record(q_lo, q_hi, scale, "positive_gt_3_over_2", ["1.9001618764609496", "1.9001618764609497"]),
            "log_terms": 180,
            "log_interval_calls": q_calls,
            "outward_lower_minus_3_over_2_decimal": fixed_decimal(outward(q_lo, q_hi, scale)[0] - F(3, 2)),
        },
        "face_delta": {
            **interval_record(face_lo, face_hi, scale, "negative", ["-8.6555894403771017e-05"]),
            "log_terms": 48,
            "log_interval_calls": face_calls,
        },
        "bsc_lift_delta": {
            **interval_record(lift_lo, lift_hi, scale, "negative", ["-7.9835082773968232e-05"]),
            "log_terms": 48,
            "log_interval_calls": lift_calls,
        },
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
