#!/usr/bin/env python3
"""Fresh non-author checks for D10-M7.

The script reconstructs n=3 exact-event atom polynomials from inclusion
determinants by Mobius inversion, independently checks the spectral-layer
channel formulas, and verifies selected exact rational consequences of the
author's Theorem A/E certificates.  It does not import or execute the author's
sanity.py.
"""

from __future__ import annotations

from decimal import Decimal, localcontext
from fractions import Fraction as F
from itertools import combinations, permutations
import json
from pathlib import Path
import sys


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


N = 3
ZERO = F(0)
ONE = F(1)
DEG = 4


def frac(num: int, den: int = 1) -> F:
    return F(num, den)


def fstr(x: F) -> str:
    return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)


def serialize(obj):
    if isinstance(obj, F):
        return fstr(obj)
    if isinstance(obj, Decimal):
        return str(obj)
    if isinstance(obj, list):
        return [serialize(v) for v in obj]
    if isinstance(obj, tuple):
        return [serialize(v) for v in obj]
    if isinstance(obj, dict):
        return {str(k): serialize(v) for k, v in obj.items()}
    return obj


def dec(x: F) -> Decimal:
    return Decimal(x.numerator) / Decimal(x.denominator)


def padd(a: list[F], b: list[F]) -> list[F]:
    return [a[i] + b[i] for i in range(DEG)]


def psub(a: list[F], b: list[F]) -> list[F]:
    return [a[i] - b[i] for i in range(DEG)]


def pscale(c: F, a: list[F]) -> list[F]:
    return [c * a[i] for i in range(DEG)]


def pmul(a: list[F], b: list[F]) -> list[F]:
    out = [ZERO] * DEG
    for i, av in enumerate(a):
        for j, bv in enumerate(b):
            if i + j < DEG:
                out[i + j] += av * bv
    return out


def peval(a: list[F], t: F) -> F:
    total = ZERO
    power = ONE
    for c in a:
        total += c * power
        power *= t
    return total


def psum(rows: list[list[F]]) -> list[F]:
    total = [ZERO] * DEG
    for row in rows:
        total = padd(total, row)
    return total


def deriv(poly: list[F], order: int) -> F:
    if order >= len(poly):
        return ZERO
    factor = 1
    for k in range(2, order + 1):
        factor *= k
    return F(factor) * poly[order]


def perm_sign(perm: tuple[int, ...]) -> int:
    inv = 0
    for i in range(len(perm)):
        for j in range(i + 1, len(perm)):
            inv += int(perm[i] > perm[j])
    return -1 if inv % 2 else 1


def det_poly(matrix: list[list[list[F]]]) -> list[F]:
    m = len(matrix)
    if m == 0:
        return [ONE, ZERO, ZERO, ZERO]
    total = [ZERO] * DEG
    for perm in permutations(range(m)):
        term = [F(perm_sign(perm)), ZERO, ZERO, ZERO]
        for i, j in enumerate(perm):
            term = pmul(term, matrix[i][j])
        total = padd(total, term)
    return total


def eye() -> list[list[F]]:
    return [[F(int(i == j)) for j in range(N)] for i in range(N)]


def project(v: tuple[int, int, int]) -> list[list[F]]:
    norm = sum(F(x * x) for x in v)
    return [[F(v[i] * v[j], norm) for j in range(N)] for i in range(N)]


def symmetric_frame() -> list[list[list[F]]]:
    U = [[F(1, 3) for _ in range(N)] for _ in range(N)]
    V = project((1, 2, -3))
    I = eye()
    W = [[I[i][j] - U[i][j] - V[i][j] for j in range(N)] for i in range(N)]
    return [U, V, W]


def mat_from_frame(frame: list[list[list[F]]], coeffs: list[F]) -> list[list[F]]:
    return [
        [sum(coeffs[a] * frame[a][i][j] for a in range(N)) for j in range(N)]
        for i in range(N)
    ]


def P_from_frame(frame: list[list[list[F]]]) -> list[list[F]]:
    return [[frame[col][row][row] for col in range(N)] for row in range(N)]


def vec_apply(P: list[list[F]], x: list[F]) -> list[F]:
    return [sum(P[row][col] * x[col] for col in range(N)) for row in range(N)]


def l1(x: list[F]) -> F:
    return sum(abs(v) for v in x)


def spectral_pattern_polys(theta: list[F], rates: list[F]) -> list[list[F]]:
    rows = []
    for mask in range(8):
        term = [ONE, ZERO, ZERO, ZERO]
        for i in range(N):
            factor = [theta[i], rates[i], ZERO, ZERO] if mask & (1 << i) else [1 - theta[i], -rates[i], ZERO, ZERO]
            term = pmul(term, factor)
        rows.append(term)
    return rows


def direct_mobius_events(frame: list[list[list[F]]], theta: list[F], rates: list[F]) -> list[list[F]]:
    K0 = mat_from_frame(frame, theta)
    D = mat_from_frame(frame, rates)
    dets = {}
    for mask in range(8):
        idx = [i for i in range(N) if mask & (1 << i)]
        matrix = [
            [[K0[i][j], D[i][j], ZERO, ZERO] for j in idx]
            for i in idx
        ]
        dets[mask] = det_poly(matrix)
    atoms = []
    full = 7
    for S in range(8):
        total = [ZERO] * DEG
        rest = full ^ S
        sub = rest
        while True:
            A = S | sub
            term = dets[A] if (A.bit_count() - S.bit_count()) % 2 == 0 else pscale(-ONE, dets[A])
            total = padd(total, term)
            if sub == 0:
                break
            sub = (sub - 1) & rest
        atoms.append(total)
    return atoms


def channel_events(frame: list[list[list[F]]], theta: list[F], rates: list[F]) -> list[list[F]]:
    P = P_from_frame(frame)
    raw = spectral_pattern_polys(theta, rates)
    events = [[ZERO] * DEG for _ in range(8)]
    events[0] = raw[0]
    events[7] = raw[7]
    for obs in range(N):
        events[1 << obs] = psum([pscale(P[obs][spec], raw[1 << spec]) for spec in range(N)])
        events[7 ^ (1 << obs)] = psum([pscale(P[obs][spec], raw[7 ^ (1 << spec)]) for spec in range(N)])
    return events


def check_jets(theta: list[F], rates: list[F]) -> dict:
    raw = spectral_pattern_polys(theta, rates)
    errors = []
    for i in range(N):
        j, k = [a for a in range(N) if a != i]
        ai, aj, ak = 1 - theta[i], 1 - theta[j], 1 - theta[k]
        vi, vj, vk = rates[i], rates[j], rates[k]
        r_expected = [
            theta[i] * aj * ak,
            vi * aj * ak - theta[i] * (vj * ak + vk * aj),
            2 * (theta[i] * vj * vk - vi * vj * ak - vi * vk * aj),
            6 * rates[0] * rates[1] * rates[2],
        ]
        s_expected = [
            ai * theta[j] * theta[k],
            -vi * theta[j] * theta[k] + ai * (vj * theta[k] + vk * theta[j]),
            2 * (ai * vj * vk - vi * vj * theta[k] - vi * vk * theta[j]),
            -6 * rates[0] * rates[1] * rates[2],
        ]
        r_got = [deriv(raw[1 << i], m) for m in range(4)]
        s_got = [deriv(raw[7 ^ (1 << i)], m) for m in range(4)]
        if r_expected != r_got:
            errors.append(("r", i, r_expected, r_got))
        if s_expected != s_got:
            errors.append(("s", i, s_expected, s_got))
    comp_raw = spectral_pattern_polys([1 - x for x in theta], rates)
    complement_errors = []
    for i in range(N):
        for m in range(4):
            lhs = deriv(raw[7 ^ (1 << i)], m)
            rhs = ((-1) ** m) * deriv(comp_raw[1 << i], m)
            if lhs != rhs:
                complement_errors.append((i, m, lhs, rhs))
    return {"jet_errors": errors, "complement_errors": complement_errors}


def B_of_rows(rows: list[list[F]]) -> Decimal:
    total = Decimal(0)
    for row in rows:
        p0 = row[0]
        p1 = row[1]
        p2 = 2 * row[2]
        total += dec(p1 * p1 / p0) + dec(p2) * dec(p0).ln()
    return total


def layer_parts(rows: list[list[F]]) -> tuple[list[F], F, Decimal]:
    mass = psum(rows)
    fisher_deficit = sum(row[1] * row[1] / row[0] for row in rows) - mass[1] * mass[1] / mass[0]
    residual = Decimal(0)
    for row in rows:
        residual += dec(2 * row[2]) * dec(3 * row[0] / mass[0]).ln()
    return mass, fisher_deficit, residual


def decomposition_check(events: list[list[F]], rates: list[F]) -> dict:
    singletons = [events[1], events[2], events[4]]
    pairs = [events[6], events[5], events[3]]
    R, Dr, residual_r = layer_parts(singletons)
    T, Ds, residual_s = layer_parts(pairs)
    count_rows = [events[0], R, T, events[7]]
    cross = sum(rates[i] * rates[j] for i, j in combinations(range(N), 2))
    B_direct = B_of_rows(events)
    B_decomp = B_of_rows(count_rows) + dec(Dr + Ds) + 2 * Decimal(3).ln() * dec(cross) + residual_r + residual_s
    return {
        "B_direct": B_direct,
        "B_decomposed": B_decomp,
        "decomposition_abs_error": abs(B_direct - B_decomp),
        "count_barrier": B_of_rows(count_rows),
        "D_r": Dr,
        "D_s": Ds,
        "cross": cross,
        "residual": residual_r + residual_s,
        "uniform_singleton_layer": all(3 * row[0] == R[0] for row in singletons),
        "uniform_pair_layer": all(3 * row[0] == T[0] for row in pairs),
    }


def l1_bound_check(theta: list[F], rates: list[F], P: list[list[F]]) -> dict:
    raw = spectral_pattern_polys(theta, rates)
    r2 = [deriv(raw[1 << i], 2) for i in range(N)]
    s2 = [deriv(raw[7 ^ (1 << i)], 2) for i in range(N)]
    Pr2 = vec_apply(P, r2)
    Ps2 = vec_apply(P, s2)
    cross = sum(rates[i] * rates[j] for i, j in combinations(range(N), 2))
    return {
        "r2": r2,
        "s2": s2,
        "l1_r2_plus_s2": l1(r2) + l1(s2),
        "six_cross": 6 * cross,
        "l1_after_P": l1(Pr2) + l1(Ps2),
        "P_contracts_this_case": l1(Pr2) + l1(Ps2) <= l1(r2) + l1(s2),
        "paired_bound_holds": l1(r2) + l1(s2) <= 6 * cross,
    }


def interval_lower_bound(poly: list[F], h: F) -> F:
    return poly[0] - sum(abs(poly[k]) * h**k for k in range(1, DEG))


def interval_certificate(frame: list[list[list[F]]]) -> dict:
    theta = [F(1, 5), F(7, 10), F(71, 100)]
    rates = [F(1, 5), F(1, 3), F(2, 3)]
    h = F(1, 20)
    events = channel_events(frame, theta, rates)
    direct = direct_mobius_events(frame, theta, rates)
    assert events == direct
    constraints = []
    min_bound = None
    for masks in ([1, 2, 4], [6, 5, 3]):
        mass = psum([events[m] for m in masks])
        for mask in masks:
            lower_poly = psub(pscale(F(4), events[mask]), mass)
            upper_poly = psub(pscale(F(4), mass), pscale(F(9), events[mask]))
            for side, poly in (("lower_4p_minus_mass", lower_poly), ("upper_4mass_minus_9p", upper_poly)):
                bound = interval_lower_bound(poly, h)
                assert bound > 0
                min_bound = bound if min_bound is None else min(min_bound, bound)
                constraints.append({"mask": mask, "side": side, "coefficients": poly, "bound": bound})
    spectral_margin = min(
        min(theta[i] + sign * h * rates[i], 1 - theta[i] - sign * h * rates[i])
        for i in range(N)
        for sign in (-1, 1)
    )
    K = mat_from_frame(frame, theta)
    D = mat_from_frame(frame, rates)
    diag = [K[i][i] for i in range(N)]
    offdiag = [K[i][j] for i, j in combinations(range(N), 2)]
    thinning_ratios = [rates[i] / theta[i] for i in range(N)]
    return {
        "theta": theta,
        "rates": rates,
        "spectral_margin_on_abs_t_le_1_20": spectral_margin,
        "K": K,
        "D": D,
        "K_diagonal": diag,
        "K_offdiagonal": offdiag,
        "distinct_spectrum": len(set(theta)) == 3,
        "heterogeneous_diagonal": len(set(diag)) == 3,
        "fully_connected": all(x != 0 for x in offdiag),
        "rank3_psd_direction": all(x > 0 for x in rates),
        "non_thinning": len(set(thinning_ratios)) > 1,
        "constraints_count": len(constraints),
        "min_constraint_bound": min_bound,
        "constraints": constraints,
        "l1_bound": l1_bound_check(theta, rates, P_from_frame(frame)),
    }


def log_bounds(x: F, terms: int = 70) -> tuple[F, F]:
    assert x > 0
    if x == 1:
        return ZERO, ZERO
    exponent = 0
    y = x
    while y < 1:
        y *= 2
        exponent -= 1
    while y >= 2:
        y /= 2
        exponent += 1

    def atanh_series(z: F) -> tuple[F, F]:
        partial = 2 * sum(z ** (2 * k + 1) / F(2 * k + 1) for k in range(terms))
        tail = 2 * z ** (2 * terms + 1) / (F(2 * terms + 1) * (1 - z * z))
        return partial, partial + tail

    lo, hi = atanh_series((y - 1) / (y + 1))
    lo2, hi2 = atanh_series(F(1, 3))
    if exponent >= 0:
        return lo + exponent * lo2, hi + exponent * hi2
    return lo + exponent * hi2, hi + exponent * lo2


def entropy_interval(probabilities: list[F]) -> tuple[F, F]:
    lo = ZERO
    hi = ZERO
    for p in probabilities:
        llo, lhi = log_bounds(p)
        lo += -p * lhi
        hi += -p * llo
    return lo, hi


def chord_checks(frame: list[list[list[F]]]) -> list[dict]:
    theta = [F(1, 5), F(7, 10), F(7, 10)]
    rates = [F(1, 5), F(1, 3), F(2, 3)]
    events = channel_events(frame, theta, rates)
    assert events == direct_mobius_events(frame, theta, rates)
    center = entropy_interval([row[0] for row in events])
    chords = []
    for h in (F(1, 100), F(1, 1000), F(1, 10000)):
        minus_probs = [peval(row, -h) for row in events]
        plus_probs = [peval(row, h) for row in events]
        assert min(minus_probs + plus_probs) > 0
        Hm = entropy_interval(minus_probs)
        Hp = entropy_interval(plus_probs)
        gap = ((Hm[0] + Hp[0]) / 2 - center[1], (Hm[1] + Hp[1]) / 2 - center[0])
        assert gap[1] < 0
        margin = min(
            min(theta[i] + sign * h * rates[i], 1 - theta[i] - sign * h * rates[i])
            for i in range(N)
            for sign in (-1, 1)
        )
        chords.append({"step": h, "gap_interval": gap, "spectral_margin": margin})
    return chords


def main() -> int:
    frame = symmetric_frame()
    P = P_from_frame(frame)
    test_cases = [
        ("uniform_single_rate", [F(1, 5), F(7, 10), F(7, 10)], [ONE, ZERO, ZERO]),
        ("uniform_rank3_breaks_repeated_rates", [F(1, 5), F(7, 10), F(7, 10)], [F(1, 5), F(1, 3), F(2, 3)]),
        ("general_identity_only", [F(1, 5), F(2, 5), F(4, 5)], [F(1, 7), F(2, 5), F(3, 8)]),
    ]
    case_records = []
    with localcontext() as ctx:
        ctx.prec = 90
        for name, theta, rates in test_cases:
            direct = direct_mobius_events(frame, theta, rates)
            channel = channel_events(frame, theta, rates)
            assert direct == channel
            jets = check_jets(theta, rates)
            assert not jets["jet_errors"] and not jets["complement_errors"]
            decomp = decomposition_check(direct, rates)
            assert decomp["decomposition_abs_error"] < Decimal("1e-75")
            if name.startswith("uniform"):
                assert decomp["uniform_singleton_layer"] and decomp["uniform_pair_layer"]
                if name == "uniform_single_rate":
                    assert decomp["cross"] == 0 and decomp["count_barrier"] > 0
                    assert decomp["B_direct"] > 0
                if name == "uniform_rank3_breaks_repeated_rates":
                    assert decomp["cross"] > 0 and decomp["B_direct"] > 0
            case_records.append({
                "name": name,
                "theta": theta,
                "rates": rates,
                "P": P,
                "K": mat_from_frame(frame, theta),
                "D": mat_from_frame(frame, rates),
                "decomposition": decomp,
                "l1_bound": l1_bound_check(theta, rates, P),
            })
        interval = interval_certificate(frame)
        chords = chord_checks(frame)

    report = {
        "status": "PASS",
        "method": "independent Fraction exact-event Mobius reconstruction plus rigorous rational log intervals for chords",
        "case_count": len(case_records),
        "cases": case_records,
        "interval_certificate": interval,
        "chords_for_symmetric_base_eq12": chords,
        "notes": [
            "The three chord checks are for the symmetric base used in equation (12), not for the asymmetric K_* interval certificate.",
            "The asymmetric K_* certificate is whole-interval via the twelve exact conditional-layer polynomial inequalities.",
        ],
    }
    out = Path(__file__).with_name("fresh_m7_verify.json")
    out.write_text(json.dumps(serialize(report), indent=2), encoding="utf-8")
    print(json.dumps(serialize({
        "status": report["status"],
        "json": str(out),
        "case_count": len(case_records),
        "interval_constraints": interval["constraints_count"],
        "min_interval_bound": interval["min_constraint_bound"],
        "chord_count": len(chords),
        "all_chord_gap_upper_bounds_negative": all(g["gap_interval"][1] < 0 for g in chords),
    }), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
