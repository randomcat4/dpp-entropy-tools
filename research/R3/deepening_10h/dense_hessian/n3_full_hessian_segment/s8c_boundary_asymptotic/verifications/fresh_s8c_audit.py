"""Fresh non-author audit for D10-S8c boundary-asymptotic certificate.

The script deliberately does not import boundary_probe.py or any S8/S8b gate.
It reconstructs the n=3 exact-event atoms and their first/second derivatives
from inclusion determinants, then independently checks the saved rational
tail and bridge certificates in boundary_probe_results.json.
"""

from __future__ import annotations

import itertools
import json
import math
import sys
from collections.abc import Iterable
from decimal import Decimal, getcontext
from fractions import Fraction as F
from pathlib import Path
from typing import Any

sys.set_int_max_str_digits(0)

DEG = 3
NLOG = 24
getcontext().prec = 60


def root_dir() -> Path:
    return Path(__file__).resolve().parents[1]


def f(x: Any) -> F:
    return x if isinstance(x, F) else F(x)


def ser(obj: Any) -> Any:
    if isinstance(obj, F):
        return str(obj)
    if isinstance(obj, tuple):
        return [ser(x) for x in obj]
    if isinstance(obj, list):
        return [ser(x) for x in obj]
    if isinstance(obj, dict):
        return {k: ser(v) for k, v in obj.items()}
    return obj


def frac_float(x: F) -> float:
    return float(Decimal(x.numerator) / Decimal(x.denominator))


def poly_zero() -> list[F]:
    return [F(0) for _ in range(DEG + 1)]


def poly_const(c: F) -> list[F]:
    p = poly_zero()
    p[0] = f(c)
    return p


def poly_t() -> list[F]:
    p = poly_zero()
    p[1] = F(1)
    return p


def poly_add(a: list[F], b: list[F]) -> list[F]:
    return [a[i] + b[i] for i in range(DEG + 1)]


def poly_sub(a: list[F], b: list[F]) -> list[F]:
    return [a[i] - b[i] for i in range(DEG + 1)]


def poly_scale(c: F, a: list[F]) -> list[F]:
    return [f(c) * x for x in a]


def poly_mul(a: list[F], b: list[F]) -> list[F]:
    out = poly_zero()
    for i, ai in enumerate(a):
        if ai == 0:
            continue
        for j, bj in enumerate(b):
            if bj == 0 or i + j > DEG:
                continue
            out[i + j] += ai * bj
    return out


def poly_eval(a: list[F], x: F) -> F:
    acc = F(0)
    for c in reversed(a):
        acc = acc * x + c
    return acc


def poly_compose_endpoint_minus_s(a: list[F], endpoint: F) -> list[F]:
    # Return coefficients of a(endpoint - s).
    out = poly_zero()
    for k, ak in enumerate(a):
        if ak == 0:
            continue
        for j in range(k + 1):
            out[j] += ak * F(math.comb(k, j)) * (endpoint ** (k - j)) * ((-1) ** j)
    return out


def interval_add(x: tuple[F, F], y: tuple[F, F]) -> tuple[F, F]:
    return (x[0] + y[0], x[1] + y[1])


def interval_sub(x: tuple[F, F], y: tuple[F, F]) -> tuple[F, F]:
    return (x[0] - y[1], x[1] - y[0])


def interval_mul(x: tuple[F, F], y: tuple[F, F]) -> tuple[F, F]:
    vals = (x[0] * y[0], x[0] * y[1], x[1] * y[0], x[1] * y[1])
    return (min(vals), max(vals))


def interval_scale(c: F, x: tuple[F, F]) -> tuple[F, F]:
    return (c * x[0], c * x[1]) if c >= 0 else (c * x[1], c * x[0])


def interval_div_pos(x: tuple[F, F], y: tuple[F, F]) -> tuple[F, F]:
    if y[0] <= 0:
        raise ArithmeticError(f"positive denominator interval required, got {y}")
    return interval_mul(x, (F(1, y[1]), F(1, y[0])))


def interval_abs_max(x: tuple[F, F]) -> F:
    return max(abs(x[0]), abs(x[1]))


def poly_interval_eval(a: list[F], interval: tuple[F, F]) -> tuple[F, F]:
    acc = (F(0), F(0))
    for c in reversed(a):
        acc = interval_add(interval_mul(acc, interval), (c, c))
    return acc


def log_bounds_point(x: F, terms: int = NLOG) -> tuple[F, F]:
    if x <= 0:
        raise ArithmeticError("log on non-positive rational")
    y = x
    exponent = 0
    while y < 1:
        y *= 2
        exponent -= 1
    while y > 2:
        y /= 2
        exponent += 1

    z = (y - 1) / (y + 1)
    partial = F(0)
    zpow = z
    for k in range(terms):
        partial += zpow / (2 * k + 1)
        zpow *= z * z
    lo_y = 2 * partial
    rem = 2 * zpow / ((2 * terms + 1) * (1 - z * z))
    hi_y = lo_y + rem

    lo_2, hi_2 = _LOG2_BOUNDS
    if exponent >= 0:
        return (exponent * lo_2 + lo_y, exponent * hi_2 + hi_y)
    return (exponent * hi_2 + lo_y, exponent * lo_2 + hi_y)


def log_interval(x: tuple[F, F], terms: int = NLOG) -> tuple[F, F]:
    if x[0] <= 0:
        raise ArithmeticError(f"log interval lower bound is not positive: {x[0]}")
    lo, _ = log_bounds_point(x[0], terms)
    _, hi = log_bounds_point(x[1], terms)
    return (lo, hi)


def _init_log2_bounds(terms: int = NLOG) -> tuple[F, F]:
    z = F(1, 3)
    partial = F(0)
    zpow = z
    for k in range(terms):
        partial += zpow / (2 * k + 1)
        zpow *= z * z
    lo = 2 * partial
    hi = lo + 2 * zpow / ((2 * terms + 1) * (1 - z * z))
    return (lo, hi)


_LOG2_BOUNDS = _init_log2_bounds()


def bpoly_entry(base: list[F], dx: F, dy: F) -> dict[tuple[int, int], list[F]]:
    out: dict[tuple[int, int], list[F]] = {(0, 0): base}
    if dx:
        out[(1, 0)] = poly_const(dx)
    if dy:
        out[(0, 1)] = poly_const(dy)
    return out


def bpoly_add(
    a: dict[tuple[int, int], list[F]], b: dict[tuple[int, int], list[F]]
) -> dict[tuple[int, int], list[F]]:
    out = dict(a)
    for key, val in b.items():
        out[key] = poly_add(out.get(key, poly_zero()), val)
    return {key: val for key, val in out.items() if any(val)}


def bpoly_mul(
    a: dict[tuple[int, int], list[F]], b: dict[tuple[int, int], list[F]]
) -> dict[tuple[int, int], list[F]]:
    out: dict[tuple[int, int], list[F]] = {}
    for (ax, ay), ap in a.items():
        for (bx, by), bp in b.items():
            key = (ax + bx, ay + by)
            if key[0] > 1 or key[1] > 1:
                continue
            out[key] = poly_add(out.get(key, poly_zero()), poly_mul(ap, bp))
    return {key: val for key, val in out.items() if any(val)}


def perm_sign(perm: tuple[int, ...]) -> int:
    inv = 0
    for i in range(len(perm)):
        for j in range(i + 1, len(perm)):
            inv += int(perm[i] > perm[j])
    return -1 if inv % 2 else 1


def det_poly_matrix(mat: list[list[list[F]]]) -> list[F]:
    n = len(mat)
    if n == 0:
        return poly_const(F(1))
    acc = poly_zero()
    for perm in itertools.permutations(range(n)):
        term = poly_const(F(1))
        for i, j in enumerate(perm):
            term = poly_mul(term, mat[i][j])
        acc = poly_add(acc, poly_scale(F(perm_sign(perm)), term))
    return acc


def det_bpoly_matrix(mat: list[list[dict[tuple[int, int], list[F]]]]) -> dict[tuple[int, int], list[F]]:
    n = len(mat)
    if n == 0:
        return {(0, 0): poly_const(F(1))}
    acc: dict[tuple[int, int], list[F]] = {}
    for perm in itertools.permutations(range(n)):
        term: dict[tuple[int, int], list[F]] = {(0, 0): poly_const(F(1))}
        for i, j in enumerate(perm):
            term = bpoly_mul(term, mat[i][j])
        if perm_sign(perm) < 0:
            term = {key: poly_scale(F(-1), val) for key, val in term.items()}
        acc = bpoly_add(acc, term)
    return acc


def outer(vec: tuple[int, int, int], den: int) -> list[list[F]]:
    return [[F(vec[i] * vec[j], den) for j in range(3)] for i in range(3)]


def symcross(a: tuple[int, int, int], b: tuple[int, int, int], den: int) -> list[list[F]]:
    return [[F(a[i] * b[j] + b[i] * a[j], den) for j in range(3)] for i in range(3)]


def mat_add(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [[a[i][j] + b[i][j] for j in range(3)] for i in range(3)]


def mat_scale(c: F, a: list[list[F]]) -> list[list[F]]:
    return [[c * a[i][j] for j in range(3)] for i in range(3)]


def build_basis() -> list[list[list[F]]]:
    u = (1, 1, 1)
    v = (1, 2, -3)
    w = (5, -4, -1)
    U = outer(u, 3)
    V = outer(v, 14)
    W = outer(w, 42)
    return [W, symcross(u, w, 11), symcross(v, w, 24), U, V, symcross(u, v, 7)]


def basis_gram(basis: list[list[list[F]]]) -> list[list[F]]:
    return [
        [sum(a[i][j] * b[i][j] for i in range(3) for j in range(3)) for b in basis]
        for a in basis
    ]


def k_line_polys() -> list[list[list[F]]]:
    u = (1, 1, 1)
    v = (1, 2, -3)
    w = (5, -4, -1)
    U = outer(u, 3)
    V = outer(v, 14)
    W = outer(w, 42)
    lam_u = [F(1, 5), F(1, 5), F(0), F(0)]
    lam_v = [F(1, 2), F(1, 3), F(0), F(0)]
    lam_w = [F(4, 5), F(2, 3), F(0), F(0)]
    mat = [[poly_zero() for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            mat[i][j] = poly_add(
                poly_add(poly_scale(U[i][j], lam_u), poly_scale(V[i][j], lam_v)),
                poly_scale(W[i][j], lam_w),
            )
    return mat


def mobius_polys(q: list[list[F]]) -> list[list[F]]:
    p = [item[:] for item in q]
    for bit in (1, 2, 4):
        for mask in range(8):
            if (mask & bit) == 0:
                p[mask] = poly_sub(p[mask], p[mask | bit])
    return p


def build_event_jets() -> dict[str, Any]:
    basis = build_basis()
    kpolys = k_line_polys()
    q0: list[list[F]] = []
    q1 = [[poly_zero() for _ in range(8)] for _ in range(6)]
    qij = [[[poly_zero() for _ in range(8)] for _ in range(6)] for _ in range(6)]
    for mask in range(8):
        idx = [i for i in range(3) if (mask >> i) & 1]
        mat = [[kpolys[i][j] for j in idx] for i in idx]
        q0[mask:mask] = [det_poly_matrix(mat)]
        for a in range(6):
            for b in range(6):
                bmat = [
                    [
                        bpoly_entry(kpolys[i][j], basis[a][i][j], basis[b][i][j])
                        for j in idx
                    ]
                    for i in idx
                ]
                det = det_bpoly_matrix(bmat)
                if b == 0:
                    q1[a][mask] = det.get((1, 0), poly_zero())
                qij[a][b][mask] = det.get((1, 1), poly_zero())
    return {
        "basis": basis,
        "basis_gram": basis_gram(basis),
        "p0": mobius_polys(q0),
        "p1": [mobius_polys(q1[a]) for a in range(6)],
        "pij": [[mobius_polys(qij[a][b]) for b in range(6)] for a in range(6)],
    }


def B_interval(jets: dict[str, Any], interval: tuple[F, F], events: Iterable[int]) -> tuple[list[list[tuple[F, F]]], list[tuple[F, F]]]:
    p = [poly_interval_eval(poly, interval) for poly in jets["p0"]]
    events = list(events)
    for ev in events:
        if p[ev][0] <= 0:
            raise ArithmeticError(f"non-positive atom lower bound for event {ev}: {p[ev][0]}")
    logs = {ev: log_interval(p[ev], NLOG) for ev in events}
    out: list[list[tuple[F, F]]] = []
    for i in range(6):
        row = []
        for j in range(6):
            acc = (F(0), F(0))
            for ev in events:
                pi = poly_interval_eval(jets["p1"][i][ev], interval)
                pj = poly_interval_eval(jets["p1"][j][ev], interval)
                pij = poly_interval_eval(jets["pij"][i][j][ev], interval)
                acc = interval_add(acc, interval_div_pos(interval_mul(pi, pj), p[ev]))
                acc = interval_add(acc, interval_mul(pij, logs[ev]))
            row.append(acc)
        out.append(row)
    return out, p


def congruence(B: list[list[tuple[F, F]]], P: list[list[F]]) -> list[list[tuple[F, F]]]:
    n = len(P)
    out: list[list[tuple[F, F]]] = []
    for a in range(n):
        row = []
        for b in range(n):
            acc = (F(0), F(0))
            for i in range(n):
                for j in range(n):
                    c = P[i][a] * P[j][b]
                    acc = interval_add(acc, interval_scale(c, B[i][j]))
            row.append(acc)
        out.append(row)
    return out


def gersh_margins(T: list[list[tuple[F, F]]]) -> list[F]:
    return [
        T[i][i][0] - sum(interval_abs_max(T[i][j]) for j in range(len(T)) if i != j)
        for i in range(len(T))
    ]


def parse_frac_matrix(raw: list[list[str]]) -> list[list[F]]:
    return [[F(x) for x in row] for row in raw]


def min_margin_summary(margins: list[F]) -> dict[str, Any]:
    m = min(margins)
    return {"fraction": str(m), "float": frac_float(m), "positive": m > 0}


def tail_model_check(jets: dict[str, Any], raw_attempt: dict[str, Any]) -> dict[str, Any]:
    endpoint = F(3, 10)
    h = F(raw_attempt["h"])
    reg, pints = B_interval(jets, (endpoint - h, endpoint), range(1, 8))
    a0, b0, kappa = F(37, 50), F(2, 5), F(2, 3)
    amax, bmax = a0 + h / 5, b0 + h / 3
    c0 = a0 * b0 * kappa
    k0 = a0 * b0 / kappa
    w0 = -log_bounds_point(c0 * h, NLOG)[0]
    log_min = -log_bounds_point(amax * bmax * kappa * h, NLOG)[1]
    vcoef = [F(0), F(0), bmax, amax, F(0)]
    ucoef = [interval_abs_max(reg[0][i + 1]) + vcoef[i] for i in range(5)]
    correction = [
        [
            h / k0 * (ucoef[i] + vcoef[i] * w0) * (ucoef[j] + vcoef[j] * w0)
            for j in range(5)
        ]
        for i in range(5)
    ]
    lowdiag = [
        2 * b0 * F(126, 121) * log_min,
        2 * a0 * F(49, 48) * log_min,
        F(0),
        F(0),
        F(0),
    ]
    tangent_off = kappa * h * (1 + w0)
    M: list[list[tuple[F, F]]] = []
    for i in range(5):
        row = []
        for j in range(5):
            lo, hi = reg[i + 1][j + 1]
            if i == j:
                row.append((lo + lowdiag[i] - correction[i][i], hi + lowdiag[i]))
            else:
                extra = correction[i][j] + (tangent_off if {i, j} == {2, 3} else F(0))
                row.append((lo - extra, hi + extra))
        M.append(row)
    P = parse_frac_matrix(raw_attempt["P"]) if raw_attempt.get("P") else None
    transformed_margins = None
    if P is not None:
        transformed_margins = gersh_margins(congruence(M, P))
    plain_margins = gersh_margins(M)
    return {
        "h": str(h),
        "nonempty_atom_floor": str(min(x[0] for x in pints[1:])),
        "w0_upper_for_w_at_h": str(w0),
        "log_min": str(log_min),
        "log_min_gt_2": log_min > 2,
        "plain_margin": min_margin_summary(plain_margins),
        "transformed_margin": min_margin_summary(transformed_margins) if transformed_margins else None,
        "matches_claimed_passed": (min(plain_margins) > 0 or (transformed_margins is not None and min(transformed_margins) > 0))
        == bool(raw_attempt["passed"]),
    }


def bridge_checks(jets: dict[str, Any], raw_bridge: dict[str, Any]) -> dict[str, Any]:
    leaves = raw_bridge["passed"]
    leaf_checks = []
    endpoints_match = True
    for i, leaf in enumerate(leaves):
        lo, hi = (F(leaf["interval"][0]), F(leaf["interval"][1]))
        if i == 0 and lo != F(29, 100):
            endpoints_match = False
        if i + 1 < len(leaves) and hi != F(leaves[i + 1]["interval"][0]):
            endpoints_match = False
        if i + 1 == len(leaves) and hi != F(299, 1000):
            endpoints_match = False
        B, pints = B_interval(jets, (lo, hi), range(8))
        P = parse_frac_matrix(leaf["P"])
        margins = gersh_margins(congruence(B, P))
        claimed_margins = [F(x) for x in leaf["row_margins"]]
        leaf_checks.append(
            {
                "interval": [str(lo), str(hi)],
                "min_atom_lower_recomputed": str(min(x[0] for x in pints)),
                "min_atom_lower_claimed": leaf["min_atom_lower"],
                "min_atom_lower_matches": min(x[0] for x in pints) == F(leaf["min_atom_lower"]),
                "min_margin": min_margin_summary(margins),
                "margins_match_json": margins == claimed_margins,
                "P_upper_triangular_positive_diagonal": all(
                    (P[i][j] == 0 if i > j else True) for i in range(6) for j in range(6)
                )
                and all(P[i][i] > 0 for i in range(6)),
                "P_denominator_max": max(x.denominator for row in P for x in row),
            }
        )
    return {
        "passed_leaf_count": len(leaves),
        "failed_leaf_count": len(raw_bridge["failed"]),
        "rejected_internal_nodes": len(raw_bridge["rejected_internal_nodes"]),
        "processed": raw_bridge["processed"],
        "success_flag": raw_bridge["success"],
        "endpoints_cover_bridge": endpoints_match,
        "all_leaf_margins_positive": all(item["min_margin"]["positive"] for item in leaf_checks),
        "all_leaf_margins_match_json": all(item["margins_match_json"] for item in leaf_checks),
        "all_min_atom_lowers_match": all(item["min_atom_lower_matches"] for item in leaf_checks),
        "all_P_valid": all(
            item["P_upper_triangular_positive_diagonal"] and item["P_denominator_max"] <= 4096
            for item in leaf_checks
        ),
        "leaf_checks": leaf_checks,
        "minimum_leaf_margin_float": min(item["min_margin"]["float"] for item in leaf_checks),
    }


def main() -> None:
    here = root_dir()
    raw = json.loads((here / "boundary_probe_results.json").read_text(encoding="utf-8"))
    jets = build_event_jets()
    endpoint = F(3, 10)
    basis = build_basis()
    expected_basis = [[[F(x) for x in row] for row in mat] for mat in raw["basis"]]
    expected_gram = [[F(x) for x in row] for row in raw["basis_gram"]]
    pstar = [poly_eval(poly, endpoint) for poly in jets["p0"]]
    empty_s_poly = poly_compose_endpoint_minus_s(jets["p0"][0], endpoint)

    a = [F(4, 5), -F(1, 5), F(0), F(0)]
    b = [F(1, 2), -F(1, 3), F(0), F(0)]
    c = [F(1, 5), -F(2, 3), F(0), F(0)]
    expected_grad = [
        poly_scale(-1, poly_mul(a, b)),
        poly_zero(),
        poly_zero(),
        poly_scale(-1, poly_mul(b, c)),
        poly_scale(-1, poly_mul(a, c)),
        poly_zero(),
    ]
    expected_hess = [[poly_zero() for _ in range(6)] for _ in range(6)]
    for i, j, poly in ((0, 3, b), (0, 4, a), (3, 4, c)):
        expected_hess[i][j] = expected_hess[j][i] = poly
    for i, poly, ratio in ((1, b, F(126, 121)), (2, a, F(49, 48)), (5, c, F(6, 7))):
        expected_hess[i][i] = poly_scale(-2 * ratio, poly)

    tail_1000 = tail_model_check(jets, next(item for item in raw["attempts"] if item["h"] == "1/1000"))
    tail_100 = tail_model_check(jets, next(item for item in raw["attempts"] if item["h"] == "1/100"))
    tail_10000 = tail_model_check(jets, next(item for item in raw["attempts"] if item["h"] == "1/10000"))
    finite_B, _ = B_interval(jets, (endpoint, endpoint), range(1, 8))
    finite_block = [[finite_B[i][j] for j in (3, 4, 5)] for i in (3, 4, 5)]
    finite_margins = gersh_margins(finite_block)
    bridge = bridge_checks(jets, raw["bridge"])

    conclusions = {
        "basis_entries_match": basis == expected_basis,
        "basis_gram_matches": basis_gram(basis) == expected_gram,
        "endpoint_atoms_match": pstar == [F(x) for x in raw["endpoint_atoms"]],
        "only_empty_atom_vanishes": pstar[0] == 0 and all(x > 0 for x in pstar[1:]),
        "empty_s_polynomial_matches": empty_s_poly == [F(x) for x in raw["empty_atom_s_polynomial"]],
        "empty_gradient_matches": [jets["p1"][i][0] for i in range(6)] == expected_grad,
        "empty_hessian_matches": [[jets["pij"][i][j][0] for j in range(6)] for i in range(6)] == expected_hess,
        "all_event_p00_zero": all(jets["pij"][0][0][ev] == poly_zero() for ev in range(8)),
        "singular_pole_coefficient_matches": F(raw["singular_pole_coefficient"]) == F(111, 250),
        "log_coefficients_match": [F(x) for x in raw["log_coefficients"]]
        == [F(504, 605), F(1813, 1200)],
        "finite_C0_block_margins_positive": min(finite_margins) > 0,
        "tail_h_1_over_1000_passes": bool(tail_1000["transformed_margin"]["positive"]),
        "tail_h_1_over_100_failure_recorded_and_not_used": (not raw["attempts"][0]["passed"])
        and F(raw["attempts"][0]["h"]) == F(1, 100)
        and "not a counterexample" in " ".join(raw["frozen_failures"]),
        "tail_h_1_over_10000_passes_but_not_needed": bool(tail_10000["transformed_margin"]["positive"]),
        "bridge_success_and_coverage": bridge["success_flag"]
        and bridge["passed_leaf_count"] == 6
        and bridge["failed_leaf_count"] == 0
        and bridge["endpoints_cover_bridge"],
        "bridge_all_leaf_certificates_positive": bridge["all_leaf_margins_positive"]
        and bridge["all_leaf_margins_match_json"]
        and bridge["all_min_atom_lowers_match"]
        and bridge["all_P_valid"],
        "right_endpoint_excluded": raw["right_endpoint_included"] is False,
    }
    conclusions["overall"] = "CORRECT" if all(conclusions.values()) else "CRITICAL_GAPS"

    out = {
        "status": conclusions["overall"],
        "scope": "fresh non-author reconstruction of n=3 event jets, tail h=1/1000 majorant, h=1/100 failure record, and six bridge leaves; no import of boundary_probe.py",
        "endpoint_atoms": [str(x) for x in pstar],
        "empty_atom_s_polynomial": [str(x) for x in empty_s_poly],
        "basis_gram": ser(basis_gram(basis)),
        "finite_C0_margins": ser(finite_margins),
        "finite_C0_min_margin_float": frac_float(min(finite_margins)),
        "tail_checks": {
            "h_1_over_100": tail_100,
            "h_1_over_1000": tail_1000,
            "h_1_over_10000": tail_10000,
        },
        "bridge_checks": bridge,
        "conclusions": conclusions,
    }
    (here / "verifications" / "fresh_s8c_audit.json").write_text(
        json.dumps(ser(out), indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(json.dumps({"status": conclusions["overall"], "tail_1000_margin": tail_1000["transformed_margin"]["float"], "bridge_min_margin": bridge["minimum_leaf_margin_float"]}, indent=2))


if __name__ == "__main__":
    main()
