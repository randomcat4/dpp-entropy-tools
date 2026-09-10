#!/usr/bin/env python3
"""Preflight for the repaired r1 extractor.

The certificate implementation uses normalized interval jets.  This preflight
adds a structurally separate direct-Decimal path with high-order centered
differences.  That path is diagnostic only: it validates extraction and sign
conventions but is never used as certificate evidence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from decimal import Context, Decimal, ROUND_HALF_EVEN, getcontext, localcontext
from fractions import Fraction
from pathlib import Path

import point_obstruction as cert
import symbolic_preflight as symbolic


CTX = Context(prec=120, rounding=ROUND_HALF_EVEN)
getcontext().prec = CTX.prec
getcontext().rounding = CTX.rounding
T0 = Decimal(5) / Decimal(4)
HP = Decimal(1) / Decimal(2**18)
HS = Decimal(1) / Decimal(2**12)
TOL = Decimal("2e-10")
SYMBOLIC_TOL = Decimal("1e-70")
NAMES = ("xx", "yy", "zz", "xy", "xz", "yz")
EXPECTED = {
    "meta": "4c70a5b7dc7961e37afffadc6230865df1c4cf99adeb148b82e4ae5bdf74e679",
    "u": "b313a5e880c2c8a503895ff404b31315ae37c75c3db3ed23f8647c781eca3af6",
    "v": "b4871c0de631720ccaccde2eae69b9134b7611c2cb793eafff64b039fefd2f34",
    "w": "9bfe902331e46d8b6136abb2f254f4f9ffe347708814386b81dbf7f112d8005d",
}


def dec(value) -> Decimal:
    if isinstance(value, Decimal):
        return value
    if isinstance(value, Fraction):
        return Decimal(value.numerator) / Decimal(value.denominator)
    return Decimal(str(value))


def load(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle, parse_float=Decimal, parse_int=int)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def poly(coefficients, exponents, q):
    x, y, z = (Decimal(8) * value for value in q)
    total = Decimal(0)
    for coefficient, (i, j, k) in zip(coefficients, exponents):
        xp = x**i if i else Decimal(1)
        yp = y**j if j else Decimal(1)
        zp = z**k if k else Decimal(1)
        total += dec(coefficient) * xp * yp * zp
    return total


def direct_components(q, t, exponents, uc, vc, wc):
    x, y, z = q
    small_q = t / Decimal(16)
    b0 = Decimal(1) / Decimal(8)
    entropy = Decimal(0)
    lu = Decimal(0)
    lv = Decimal(0)
    lw = Decimal(0)
    weights = []
    for a, b in ((-1, -1), (-1, 1), (1, -1), (1, 1)):
        left = Decimal(a) / Decimal(2) - x
        right = Decimal(b) / Decimal(2) - y
        off = small_q - z
        determinant = left * right - off * off
        weight = Decimal(a * b) * determinant
        r00 = right / determinant
        r01 = -off / determinant
        r11 = left / determinant
        tx = b0 * b0 * r00
        tz = b0 * small_q * r00 + b0 * b0 * r01
        ty = small_q * small_q * r00 + Decimal(2) * small_q * b0 * r01 + b0 * b0 * r11
        image = (tx, ty, tz)
        weights.append(weight)
        entropy -= weight * weight.ln()
        lu += weight * poly(uc, exponents, image)
        lv += weight * poly(vc, exponents, image)
        lw += weight * poly(wc, exponents, image)
    return {
        "B": entropy,
        "Lu": lu,
        "Lv": lv,
        "Lw": lw,
        "u": poly(uc, exponents, q),
        "v": poly(vc, exponents, q),
        "w": poly(wc, exponents, q),
        "weights": weights,
    }


def first_t(function, q, t, h=HP):
    return (
        function(q, t - Decimal(2) * h)
        - Decimal(8) * function(q, t - h)
        + Decimal(8) * function(q, t + h)
        - function(q, t + Decimal(2) * h)
    ) / (Decimal(12) * h)


def second_t(function, q, t, h=HP):
    return (
        -function(q, t + Decimal(2) * h)
        + Decimal(16) * function(q, t + h)
        - Decimal(30) * function(q, t)
        + Decimal(16) * function(q, t - h)
        - function(q, t - Decimal(2) * h)
    ) / (Decimal(12) * h * h)


def direct_residuals(q, t, exponents, uc, vc, wc, c2):
    def source(qv, tv):
        c = direct_components(qv, tv, exponents, uc, vc, wc)
        return c["B"] + c["Lu"]

    def lv_only(qv, tv):
        return direct_components(qv, tv, exponents, uc, vc, wc)["Lv"]

    c = direct_components(q, t, exponents, uc, vc, wc)
    r0 = source(q, t) - c["u"]
    r1 = first_t(source, q, t) - c["v"] + c["Lv"]
    r2 = second_t(source, q, t) + Decimal(2) * first_t(lv_only, q, t) - dec(c2) - c["w"] + c["Lw"]
    return r0, r1, r2


def shift(q, dimension, amount):
    out = list(q)
    out[dimension] += amount
    return tuple(out)


def diagonal_second(function, q, dimension, h):
    return (
        -function(shift(q, dimension, Decimal(2) * h))
        + Decimal(16) * function(shift(q, dimension, h))
        - Decimal(30) * function(q)
        + Decimal(16) * function(shift(q, dimension, -h))
        - function(shift(q, dimension, -Decimal(2) * h))
    ) / (Decimal(12) * h * h)


def mixed_second_basic(function, q, i, j, h):
    values = Decimal(0)
    for si, sj, sign in ((1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)):
        point = list(q)
        point[i] += Decimal(si) * h
        point[j] += Decimal(sj) * h
        values += Decimal(sign) * function(tuple(point))
    return values / (Decimal(4) * h * h)


def hessian_direct(function, q, h):
    out = {
        "xx": diagonal_second(function, q, 0, h),
        "yy": diagonal_second(function, q, 1, h),
        "zz": diagonal_second(function, q, 2, h),
    }
    for name, i, j in (("xy", 0, 1), ("xz", 0, 2), ("yz", 1, 2)):
        coarse = mixed_second_basic(function, q, i, j, h)
        fine = mixed_second_basic(function, q, i, j, h / Decimal(2))
        out[name] = fine + (fine - coarse) / Decimal(3)
    return out


def fraction_from_text(text):
    return Fraction(text)


def interval_mid(record):
    lo = fraction_from_text(record["lo"])
    hi = fraction_from_text(record["hi"])
    return dec((lo + hi) / 2)


def jet_terms(exponents, uc, vc, wc, t_value=Fraction(5, 4)):
    x = cert.Jet.variable(Fraction(0), 0)
    y = cert.Jet.variable(Fraction(0), 1)
    z = cert.Jet.variable(Fraction(0), 2)
    t = cert.Jet.variable(t_value, 3)
    qcoords = (x, y, z)
    vq = cert.polynomial(vc, exponents, qcoords)
    source = cert.Jet.constant(0)
    lv = cert.Jet.constant(0)
    for a, b in ((-1, -1), (-1, 1), (1, -1), (1, 1)):
        weight, image = cert.branch_data(x, y, z, t, a, b)
        source = source - weight * weight.log() + weight * cert.polynomial(uc, exponents, image)
        lv = lv + weight * cert.polynomial(vc, exponents, image)
    records = {}
    for name, alpha0 in {
        "xx": (2, 0, 0, 0), "yy": (0, 2, 0, 0), "zz": (0, 0, 2, 0),
        "xy": (1, 1, 0, 0), "xz": (1, 0, 1, 0), "yz": (0, 1, 1, 0),
    }.items():
        factor = 2 if 2 in alpha0[:3] else 1
        alpha1 = alpha0[:3] + (1,)
        first = source.c[alpha1] * factor
        minus_v = -vq.c[alpha0] * factor
        plus_lv = lv.c[alpha0] * factor
        old_extra = lv.c[alpha1] * factor
        records[name] = {
            "partial_t_source": cert.interval_record(first),
            "minus_v_fixed_t": cert.interval_record(minus_v),
            "plus_Lv_fixed_t": cert.interval_record(plus_lv),
            "withdrawn_partial_t_Lv": cert.interval_record(old_extra),
            "correct": cert.interval_record(first + minus_v + plus_lv),
            "withdrawn": cert.interval_record(first + old_extra),
        }
    return records


def run_fixture():
    exponents = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (2, 0, 0), (0, 1, 1), (0, 0, 2), (1, 0, 1)]
    uc = [Fraction(1, 8), Fraction(-1, 16), Fraction(3, 32), Fraction(1, 64), Fraction(1, 32), Fraction(-1, 64), Fraction(1, 128)]
    vc = [Fraction(-1, 16), Fraction(1, 32), Fraction(1, 8), Fraction(1, 64), Fraction(-1, 64), Fraction(1, 64), Fraction(1, 32)]
    wc = [Fraction(1, 32), Fraction(1, 16), Fraction(-1, 32), Fraction(-1, 128), Fraction(1, 64), Fraction(1, 128), Fraction(-1, 64)]
    c2 = Fraction(-1, 1000)
    q0 = (Decimal(0), Decimal(0), Decimal(0))
    direct0 = lambda q: direct_residuals(q, T0, exponents, uc, vc, wc, c2)[0]
    direct1 = lambda q: direct_residuals(q, T0, exponents, uc, vc, wc, c2)[1]
    h0a = hessian_direct(direct0, q0, HS)
    h0b = hessian_direct(direct0, q0, HS / Decimal(2))
    h1a = hessian_direct(direct1, q0, HS)
    h1b = hessian_direct(direct1, q0, HS / Decimal(2))
    jet = cert.evaluate_point(exponents, uc, vc, wc, c2, Fraction(5, 4))
    symbolic_result = symbolic.fixture_values(exponents, uc, vc, wc, c2, T0)
    checks = []
    comparisons = {}
    for name in NAMES:
        j0 = interval_mid(jet["r0_state_hessian"][name])
        j1 = interval_mid(jet["r1_state_hessian"][name])
        s0 = symbolic_result["r0_hessian"][name]
        s1 = symbolic_result["r1_hessian"][name]
        e0 = abs(h0b[name] - j0)
        e1 = abs(h1b[name] - j1)
        symbolic_e0 = abs(s0 - j0)
        symbolic_e1 = abs(s1 - j1)
        stable0 = abs(h0b[name] - h0a[name])
        stable1 = abs(h1b[name] - h1a[name])
        ok = (
            symbolic_e0 < SYMBOLIC_TOL and symbolic_e1 < SYMBOLIC_TOL
            and e0 < TOL and e1 < TOL and stable0 < TOL and stable1 < TOL
        )
        checks.append(ok)
        comparisons[name] = {
            "r0_symbolic": str(s0), "r0_symbolic_error": str(symbolic_e0),
            "r0_jet": str(j0), "r0_direct": str(h0b[name]), "r0_error": str(e0), "r0_stability": str(stable0),
            "r1_symbolic": str(s1), "r1_symbolic_error": str(symbolic_e1),
            "r1_jet": str(j1), "r1_direct": str(h1b[name]), "r1_error": str(e1), "r1_stability": str(stable1),
            "pass": ok,
        }
    direct_r2 = direct_residuals(q0, T0, exponents, uc, vc, wc, c2)[2]
    jet_r2 = interval_mid(jet["r2"])
    symbolic_r2 = symbolic_result["r2"]
    r2_error = abs(direct_r2 - jet_r2)
    symbolic_r2_error = abs(symbolic_r2 - jet_r2)
    checks.append(r2_error < TOL)
    checks.append(symbolic_r2_error < SYMBOLIC_TOL)
    terms = jet_terms(exponents, uc, vc, wc)
    witness = None
    lv_parameter_witness = None
    for name in NAMES:
        correct = interval_mid(terms[name]["correct"])
        withdrawn = interval_mid(terms[name]["withdrawn"])
        withdrawn_dt_lv = interval_mid(terms[name]["withdrawn_partial_t_Lv"])
        if lv_parameter_witness is None and abs(withdrawn_dt_lv) > Decimal("1e-8"):
            lv_parameter_witness = {
                "component": name,
                "partial_t_Lv_hessian": str(withdrawn_dt_lv),
            }
        if abs(correct - withdrawn) > Decimal("1e-8"):
            witness = {"component": name, "correct": str(correct), "withdrawn": str(withdrawn), "difference": str(correct - withdrawn)}
    checks.append(any(value != 0 for value in uc))
    checks.append(any(value != 0 for value in vc))
    checks.append(lv_parameter_witness is not None)
    checks.append(witness is not None)
    # Because the x^2 coefficient of v is 1/64 and features use (8x)^2,
    # the fixture has v_xx=2 exactly.  This is the fixed-t term the old rule omitted.
    checks.append(vc[3] * 128 == 2)
    return {
        "pass": all(checks),
        "analytic_hand_checks": {
            "v_xx_exact": "2",
            "u_polynomial_nonzero": True,
            "v_polynomial_nonzero": True,
            "parameter_dependent_Lv_witness": lv_parameter_witness,
            "nonzero_correct_vs_withdrawn_witness": witness,
            "component_terms": terms,
        },
        "independent_direct_decimal": {
            "method": "independent expression-DAG symbolic differentiation; finite differences are an additional diagnostic only",
            "tolerance": str(TOL),
            "symbolic_tolerance": str(SYMBOLIC_TOL),
            "comparisons": comparisons,
            "r2_jet": str(jet_r2), "r2_symbolic": str(symbolic_r2),
            "r2_symbolic_error": str(symbolic_r2_error),
            "r2_direct": str(direct_r2), "r2_error": str(r2_error),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--meta", required=True, type=Path)
    parser.add_argument("--u", required=True, type=Path)
    parser.add_argument("--v", required=True, type=Path)
    parser.add_argument("--w", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    start = time.monotonic()
    paths = {"meta": args.meta, "u": args.u, "v": args.v, "w": args.w}
    hashes = {name: digest(path) for name, path in paths.items()}
    udata, vdata, wdata = load(args.u), load(args.v), load(args.w)
    exponents = udata["exponents"]
    fixture = run_fixture()
    actual_terms = jet_terms(exponents, udata["u"], vdata["v"], wdata["w"])
    distinct = any(
        interval_mid(actual_terms[name]["correct"]) != interval_mid(actual_terms[name]["withdrawn"])
        for name in NAMES
    )
    actual = cert.evaluate_point(exponents, udata["u"], vdata["v"], wdata["w"], cert.f(wdata["c2"]), Fraction(5, 4))
    sanity = {
        "hashes": hashes,
        "hashes_match": hashes == EXPECTED,
        "monomial_count": len(exponents),
        "coefficient_counts": {"u": len(udata["u"]), "v": len(vdata["v"]), "w": len(wdata["w"])},
        "all_trials_nonzero": all(any(dec(x) != 0 for x in data) for data in (udata["u"], vdata["v"], wdata["w"])),
        "weights_positive": all(Fraction(item["lo"]) > 0 for item in actual["weights"]),
        "weight_sum_exact_one": actual["weight_sum_value"]["lo"] == "1" and actual["weight_sum_value"]["hi"] == "1",
        "corrected_vs_withdrawn_distinct": distinct,
    }
    passed = fixture["pass"] and sanity["hashes_match"] and sanity["monomial_count"] == 285
    passed = passed and all(value == 285 for value in sanity["coefficient_counts"].values())
    passed = passed and sanity["all_trials_nonzero"] and sanity["weights_positive"]
    passed = passed and sanity["weight_sum_exact_one"] and sanity["corrected_vs_withdrawn_distinct"]
    record = {
        "schema": "issue74-r1-repair-preflight-v1",
        "status": "PASS" if passed else "FAIL",
        "fixture": fixture,
        "frozen_input_sanity": sanity,
        "process": {"pid": os.getpid(), "python": sys.version, "elapsed_seconds": time.monotonic() - start},
        "non_claim": "Finite differences are diagnostic only and are not certificate evidence.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    tmp = args.output.with_suffix(args.output.suffix + ".tmp")
    tmp.write_text(json.dumps(record, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    os.replace(tmp, args.output)
    print(json.dumps({"status": record["status"], "pid": os.getpid(), "elapsed_seconds": record["process"]["elapsed_seconds"], "output": str(args.output.resolve())}))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
