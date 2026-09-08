#!/usr/bin/env python3
"""Fresh non-author audit for D10-M8 n3_complement_barrier_refine.

The verifier does not import or execute the author sanity script.  It reads the
frozen result JSON as data, rebuilds exact-event Mobius atom polynomials from
the listed rational K,D matrices, and independently checks the complementary
barrier identities and interval certificates.
"""

from __future__ import annotations

from decimal import Decimal, localcontext
from fractions import Fraction
from itertools import permutations
from math import factorial
from pathlib import Path
import json
import math


HERE = Path(__file__).resolve().parent
BASE = HERE.parent
FULL = 0b111
DEG = 6


def F(text) -> Fraction:
    return Fraction(text)


def fstr(x: Fraction) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def serialize(obj):
    if isinstance(obj, Fraction):
        return fstr(obj)
    if isinstance(obj, Decimal):
        return str(obj)
    if isinstance(obj, tuple):
        return [serialize(x) for x in obj]
    if isinstance(obj, list):
        return [serialize(x) for x in obj]
    if isinstance(obj, dict):
        return {str(k): serialize(v) for k, v in obj.items()}
    return obj


def poly0():
    return [Fraction(0) for _ in range(DEG + 1)]


def poly_const(c):
    out = poly0()
    out[0] = c
    return out


def poly_linear(c0, c1):
    out = poly0()
    out[0] = c0
    out[1] = c1
    return out


def poly_add(a, b):
    return [a[i] + b[i] for i in range(DEG + 1)]


def poly_sub(a, b):
    return [a[i] - b[i] for i in range(DEG + 1)]


def poly_scale(a, c):
    return [c * x for x in a]


def poly_mul(a, b):
    out = poly0()
    for i, ai in enumerate(a):
        if ai == 0:
            continue
        for j, bj in enumerate(b):
            if bj == 0 or i + j > DEG:
                continue
            out[i + j] += ai * bj
    return out


def sign_perm(perm):
    inv = 0
    for i in range(len(perm)):
        for j in range(i + 1, len(perm)):
            inv += int(perm[i] > perm[j])
    return -1 if inv % 2 else 1


def det_poly(matrix):
    n = len(matrix)
    if n == 0:
        return poly_const(Fraction(1))
    total = poly0()
    for perm in permutations(range(n)):
        term = poly_const(Fraction(sign_perm(perm)))
        for i, j in enumerate(perm):
            term = poly_mul(term, matrix[i][j])
        total = poly_add(total, term)
    return total


def principal_poly_matrix(K, D, mask):
    idx = [i for i in range(3) if mask & (1 << i)]
    return [
        [poly_linear(K[i][j], D[i][j]) for j in idx]
        for i in idx
    ]


def atom_polys_from_KD(K, D):
    inclusions = [det_poly(principal_poly_matrix(K, D, mask)) for mask in range(8)]
    atoms = [p[:] for p in inclusions]
    for bit in (1, 2, 4):
        for mask in range(8):
            if (mask & bit) == 0:
                atoms[mask] = poly_sub(atoms[mask], atoms[mask | bit])
    return atoms, inclusions


def coeff(poly, k):
    return poly[k] if k < len(poly) else Fraction(0)


def deriv(poly, order):
    return factorial(order) * coeff(poly, order)


def poly_eval_abs_lower(poly, h):
    return poly[0] - sum(abs(poly[k]) * (h ** k) for k in range(1, len(poly)))


def mat_vec(P, x):
    return [sum(P[a][i] * x[i] for i in range(3)) for a in range(3)]


def dot_dec(weights, logs):
    return sum(dec_frac(w) * l for w, l in zip(weights, logs))


def dec_frac(x: Fraction) -> Decimal:
    return Decimal(x.numerator) / Decimal(x.denominator)


def dec_ln_frac(x: Fraction) -> Decimal:
    return dec_frac(x).ln()


def parse_matrix(rows):
    return [[F(x) for x in row] for row in rows]


def parse_vector(row):
    return [F(x) for x in row]


def theta_rs(theta):
    r = []
    s = []
    for i in range(3):
        ri = theta[i]
        si = 1 - theta[i]
        for j in range(3):
            if j == i:
                continue
            ri *= 1 - theta[j]
            si *= theta[j]
        r.append(ri)
        s.append(si)
    return r, s, sum(r), sum(s)


def count_polys(theta, rates):
    # Distribution of sum of three independent Bernoullis theta_i+t rates_i.
    polys = [poly_const(Fraction(1)), poly0(), poly0(), poly0()]
    for th, rate in zip(theta, rates):
        fail = poly_linear(1 - th, -rate)
        succ = poly_linear(th, rate)
        nxt = [poly0(), poly0(), poly0(), poly0()]
        for k in range(3):
            nxt[k] = poly_add(nxt[k], poly_mul(polys[k], fail))
            nxt[k + 1] = poly_add(nxt[k + 1], poly_mul(polys[k], succ))
        polys = nxt
    return polys


def entropy_second_negative(prob_polys):
    # B=-H'' at zero for a positive finite distribution p(t).
    with localcontext() as ctx:
        ctx.prec = 90
        out = Decimal(0)
        for poly in prob_polys:
            p0 = coeff(poly, 0)
            p1 = deriv(poly, 1)
            p2 = deriv(poly, 2)
            out += dec_frac(p1 * p1 / p0) + dec_frac(p2) * dec_ln_frac(p0)
        return +out


def product(poly_list):
    out = poly_const(Fraction(1))
    for p in poly_list:
        out = poly_mul(out, p)
    return out


def check_power_ratio(alpha, beta, P, theta, case_signs):
    ratios = []
    prod_alpha = math.prod(alpha, start=Fraction(1))
    prod_beta = math.prod(beta, start=Fraction(1))
    for i, saved in enumerate(case_signs):
        d = int(saved["clearing_denominator"])
        numerator = Fraction(1)
        denominator = Fraction(1)
        for a in range(3):
            e = d * P[a][i]
            if e.denominator != 1:
                raise ArithmeticError("uncleared P exponent")
            numerator *= (alpha[a] * beta[a]) ** e.numerator
        e_alpha = d * (1 - theta[i])
        e_beta = d * theta[i]
        if e_alpha.denominator != 1 or e_beta.denominator != 1:
            raise ArithmeticError("uncleared theta exponent")
        denominator *= prod_alpha ** e_alpha.numerator
        denominator *= prod_beta ** e_beta.numerator
        ratio = numerator / denominator
        ratios.append(
            {
                "i": i,
                "clearing_denominator": d,
                "ratio_matches_saved": fstr(ratio) == saved["power_ratio"],
                "sign_positive": ratio > 1,
                "saved_sign": saved["sign"],
            }
        )
    return ratios


def check_single_rate_count_boundary(theta):
    results = []
    for j in range(3):
        rates = [Fraction(0), Fraction(0), Fraction(0)]
        rates[j] = Fraction(1)
        pi = count_polys(theta, rates)
        fisher = sum(deriv(poly, 1) ** 2 / coeff(poly, 0) for poly in pi)
        mean_derivative = sum(k * deriv(poly, 1) for k, poly in enumerate(pi))
        results.append({"rate_index": j, "count_fisher": fisher, "mean_derivative": mean_derivative})
    return results


def check_case(case):
    theta = parse_vector(case["theta"])
    rates = parse_vector(case["rates"])
    K = parse_matrix(case["K"])
    D = parse_matrix(case["D"])
    P = parse_matrix(case["P"])
    stored_events = [[F(x) for x in poly] for poly in case["events"]]
    atoms, _inclusions = atom_polys_from_KD(K, D)
    atom_errors = {}
    for mask in range(8):
        for k in range(4):
            if coeff(atoms[mask], k) != stored_events[mask][k]:
                atom_errors[(mask, k)] = coeff(atoms[mask], k) - stored_events[mask][k]
        for k in range(4, DEG + 1):
            if coeff(atoms[mask], k) != 0:
                atom_errors[(mask, k)] = coeff(atoms[mask], k)

    r, s, R, T = theta_rs(theta)
    y = mat_vec(P, r)
    z = mat_vec(P, s)
    singleton_errors = [coeff(atoms[1 << a], 0) - y[a] for a in range(3)]
    pair_missing_errors = [coeff(atoms[FULL ^ (1 << a)], 0) - z[a] for a in range(3)]
    alpha = [ya / R for ya in y]
    beta = [za / T for za in z]
    saved_alpha = parse_vector(case["alpha"])
    saved_beta = parse_vector(case["beta"])
    alpha_errors = [alpha[a] - saved_alpha[a] for a in range(3)]
    beta_errors = [beta[a] - saved_beta[a] for a in range(3)]
    row_sums = [sum(P[a][i] for i in range(3)) for a in range(3)]
    col_sums = [sum(P[a][i] for a in range(3)) for i in range(3)]
    min_product = min(alpha[a] * beta[a] for a in range(3))

    with localcontext() as ctx:
        ctx.prec = 90
        logs_alpha = [dec_ln_frac(a) for a in alpha]
        logs_beta = [dec_ln_frac(b) for b in beta]
        logs_prod_alpha = sum(logs_alpha)
        logs_prod_beta = sum(logs_beta)
        C = []
        C_direct = []
        for i in range(3):
            c = sum(
                dec_frac(P[a][i]) * (logs_alpha[a] + logs_beta[a])
                for a in range(3)
            )
            c -= dec_frac(1 - theta[i]) * logs_prod_alpha
            c -= dec_frac(theta[i]) * logs_prod_beta
            C.append(+c)
            others = [j for j in range(3) if j != i]
            r_cross = [Fraction(0), Fraction(0), Fraction(0)]
            s_cross = [Fraction(0), Fraction(0), Fraction(0)]
            r_cross[i] = theta[i]
            s_cross[i] = 1 - theta[i]
            for j in others:
                r_cross[j] = -(1 - theta[i])
                s_cross[j] = -theta[i]
            C_direct.append(+(dot_dec(mat_vec(P, r_cross), logs_alpha) + dot_dec(mat_vec(P, s_cross), logs_beta)))
        A_pair = Decimal(0)
        for i in range(3):
            j, k = [u for u in range(3) if u != i]
            A_pair += Decimal(2) * dec_frac(rates[j] * rates[k]) * C[i]
        # Direct A from exact atom second derivatives on singleton/pair layers.
        y_second = [deriv(atoms[1 << a], 2) for a in range(3)]
        z_second = [deriv(atoms[FULL ^ (1 << a)], 2) for a in range(3)]
        A_direct = +(dot_dec(y_second, logs_alpha) + dot_dec(z_second, logs_beta))
        B_direct = entropy_second_negative(atoms)
        B_count = entropy_second_negative(count_polys(theta, rates))
        y_first = [deriv(atoms[1 << a], 1) for a in range(3)]
        z_first = [deriv(atoms[FULL ^ (1 << a)], 1) for a in range(3)]
        R_first = sum(y_first)
        T_first = sum(z_first)
        D_y = sum(dec_frac(y_first[a] * y_first[a] / y[a]) for a in range(3)) - dec_frac(R_first * R_first / R)
        D_z = sum(dec_frac(z_first[a] * z_first[a] / z[a]) for a in range(3)) - dec_frac(T_first * T_first / T)
        B_decomp = +(B_count + D_y + D_z + A_direct)
        lower_log = +(Decimal(27) * dec_frac(min_product)).ln()
        C_minus_lower = [+(c - lower_log) for c in C]

    interval_reports = []
    for attempt in case["interval_attempts"]:
        h = F(attempt["step"])
        spectral_margin = min(
            min(theta[i] - h * abs(rates[i]), 1 - theta[i] - h * abs(rates[i]))
            for i in range(3)
        )
        y_polys = [atoms[1 << a] for a in range(3)]
        z_polys = [atoms[FULL ^ (1 << a)] for a in range(3)]
        R_poly = poly0()
        T_poly = poly0()
        for p in y_polys:
            R_poly = poly_add(R_poly, p)
        for p in z_polys:
            T_poly = poly_add(T_poly, p)
        constraints = []
        passed = True
        for a in range(3):
            g = poly_sub(poly_scale(poly_mul(y_polys[a], z_polys[a]), Fraction(27)), poly_mul(R_poly, T_poly))
            stored_coeffs = [F(x) for x in attempt["constraints"][a]["coefficients"]]
            stored_lower = F(attempt["constraints"][a]["lower_bound"])
            computed_lower = poly_eval_abs_lower(g, h)
            coeff_match = all(coeff(g, k) == stored_coeffs[k] for k in range(7))
            lower_match = computed_lower == stored_lower
            constraints.append(
                {
                    "a": a,
                    "coefficients_match": coeff_match,
                    "lower_bound_matches": lower_match,
                    "lower_bound": computed_lower,
                    "lower_bound_positive": computed_lower > 0,
                }
            )
            passed = passed and computed_lower > 0
        interval_reports.append(
            {
                "step": attempt["step"],
                "saved_passed": attempt["passed"],
                "computed_passed": passed,
                "pass_flag_matches": passed == attempt["passed"],
                "spectral_margin": spectral_margin,
                "spectral_margin_matches": spectral_margin == F(attempt["spectral_margin"]),
                "spectral_margin_positive": spectral_margin > 0,
                "constraints": constraints,
            }
        )

    power_ratios = check_power_ratio(alpha, beta, P, theta, case["C_rational_signs"])
    single_rate = check_single_rate_count_boundary(theta)
    one_fifth = all(a >= Fraction(1, 5) for a in alpha + beta)
    one_fifth_implies_max_le_3_5 = (not one_fifth) or all(a <= Fraction(3, 5) for a in alpha + beta)
    C_saved = [Decimal(x) for x in case["C"]]
    B_lo, B_hi = [F(x) for x in case["B_interval"]]
    B_in_interval = dec_frac(B_lo) <= B_direct <= dec_frac(B_hi)
    ok = (
        not atom_errors
        and all(e == 0 for e in singleton_errors + pair_missing_errors + alpha_errors + beta_errors)
        and all(s == 1 for s in row_sums)
        and all(s == 1 for s in col_sums)
        and min_product == F(case["min_product"])
        and (min_product > Fraction(1, 27)) == bool(case["product_condition"])
        and one_fifth == bool(case["new_one_fifth"])
        and one_fifth_implies_max_le_3_5
        and all(abs(C[i] - C_saved[i]) < Decimal("1e-70") for i in range(3))
        and all(abs(C[i] - C_direct[i]) < Decimal("1e-80") for i in range(3))
        and abs(A_pair - A_direct) < Decimal("1e-80")
        and abs(B_direct - B_decomp) < Decimal("1e-80")
        and all(r["ratio_matches_saved"] and r["sign_positive"] and r["saved_sign"] == 1 for r in power_ratios)
        and all(item["mean_derivative"] == 1 and item["count_fisher"] > 0 for item in single_rate)
        and B_in_interval
        and all(report["pass_flag_matches"] for report in interval_reports)
        and all(report["spectral_margin_matches"] and report["spectral_margin_positive"] for report in interval_reports)
        and all(c["coefficients_match"] and c["lower_bound_matches"] for report in interval_reports for c in report["constraints"])
    )
    return {
        "index": case["index"],
        "atom_polynomial_errors": atom_errors,
        "singleton_y_errors": singleton_errors,
        "pair_missing_z_errors": pair_missing_errors,
        "alpha_errors": alpha_errors,
        "beta_errors": beta_errors,
        "P_row_sums": row_sums,
        "P_column_sums": col_sums,
        "min_product": min_product,
        "product_condition": min_product > Fraction(1, 27),
        "new_one_fifth": one_fifth,
        "one_fifth_implies_all_entries_at_most_3_5": one_fifth_implies_max_le_3_5,
        "C_decimal": C,
        "C_direct_complement_decimal": C_direct,
        "log_27m_lower_bound": lower_log,
        "C_minus_log_27m": C_minus_lower,
        "A_pair_formula_decimal": +A_pair,
        "A_direct_decimal": +A_direct,
        "B_direct_decimal": +B_direct,
        "B_decomposition_decimal": +B_decomp,
        "B_interval_contains_direct": B_in_interval,
        "power_ratio_checks": power_ratios,
        "single_rate_count_boundary": single_rate,
        "interval_reports": interval_reports,
        "status": "PASS" if ok else "FAIL",
    }


def main():
    source = json.loads((BASE / "sanity_results.json").read_text(encoding="utf-8"))
    reports = [check_case(case) for case in source["cases"]]
    interval_attempts = [attempt for report in reports for attempt in report["interval_reports"]]
    constraints = [c for attempt in interval_attempts for c in attempt["constraints"]]
    failed_attempts = [attempt for attempt in interval_attempts if not attempt["computed_passed"]]
    failed_constraints = [c for c in constraints if not c["lower_bound_positive"]]
    counts = {
        "centers": len(reports),
        "exact_event_polynomials": 8 * len(reports),
        "scalar_coefficients_compared": 8 * 4 * len(reports),
        "interval_attempts": len(interval_attempts),
        "interval_constraints": len(constraints),
        "passed_interval_attempts": sum(1 for attempt in interval_attempts if attempt["computed_passed"]),
        "failed_interval_attempts": len(failed_attempts),
        "failed_interval_constraints": len(failed_constraints),
        "product_pass": sum(1 for report in reports if report["product_condition"]),
        "one_fifth_pass": sum(1 for report in reports if report["new_one_fifth"]),
        "coefficient_pass": sum(
            1 for report in reports if all(item["sign_positive"] for item in report["power_ratio_checks"])
        ),
    }
    status = "PASS" if all(report["status"] == "PASS" for report in reports) else "FAIL"
    payload = {
        "status": status,
        "independence": "author sanity.py was not imported or executed",
        "counts": counts,
        "case_reports": reports,
        "layer_status": {
            "A_coefficient_identity_and_indices": "PASS" if all(r["status"] == "PASS" for r in reports) else "FAIL",
            "product_barrier_and_single_rate_boundary": "PASS"
            if counts["product_pass"] == source["counts"]["product_pass"]
            and all(all(item["count_fisher"] > 0 for item in r["single_rate_count_boundary"]) for r in reports)
            else "FAIL",
            "exact_event_and_segment_certificates": "PASS"
            if counts["interval_attempts"] == 12 and counts["failed_interval_attempts"] == 2
            else "FAIL",
        },
    }
    out = HERE / "fresh_m8_audit.json"
    out.write_text(json.dumps(serialize(payload), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(serialize({
        "status": status,
        "json": str(out),
        "counts": counts,
        "case_statuses": {str(r["index"]): r["status"] for r in reports},
        "layer_status": payload["layer_status"],
    }), indent=2, ensure_ascii=False))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
