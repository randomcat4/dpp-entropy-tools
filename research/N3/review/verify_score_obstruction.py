#!/usr/bin/env python3
"""Independent checker for the fixed N3 conditional-score obstruction.

This script does not import the author's N3 modules.  It rebuilds exact event
probabilities, first and second directional event jets, the score projection
identities L1/L2, and the displayed rational shortcut obstruction.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
import time
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path


TARGET_COMMIT = "424b4efcec0052ad8d79ac71c69b334dcfb03bb8"
AUTHOR_CERT = "research/N3/main/score_obstruction_certificate.json"
AUTHOR_PROOF = "research/N3/main/conditional_score_lemma_v1.md"
AUTHOR_SCRIPT = "research/N3/main/certify_score_obstruction.py"
AUTHOR_FROZEN = "research/N3/frozen_theorem_v1.md"

SUBSETS = [(), (0,), (1,), (2,), (0, 1), (0, 2), (1, 2), (0, 1, 2)]
BITMASK_ORDER = [(), (0,), (1,), (0, 1), (2,), (0, 2), (1, 2), (0, 1, 2)]
COORDS = [(0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2)]


def qstr(x: Q) -> str:
    return str(x)


def mat_from_coords(v: list[Q]) -> list[list[Q]]:
    x, y, z, a, b, c = v
    return [[x, a, b], [a, y, c], [b, c, z]]


def coords_from_mat(M: list[list[Q]]) -> list[Q]:
    return [M[0][0], M[1][1], M[2][2], M[0][1], M[0][2], M[1][2]]


def direction_from_coords(d: list[Q]) -> list[list[Q]]:
    return mat_from_coords(d)


def det2(M: list[list[Q]], idx: tuple[int, int]) -> Q:
    i, j = idx
    return M[i][i] * M[j][j] - M[i][j] * M[j][i]


def det3(M: list[list[Q]]) -> Q:
    return (
        M[0][0] * M[1][1] * M[2][2]
        + M[0][1] * M[1][2] * M[2][0]
        + M[0][2] * M[1][0] * M[2][1]
        - M[0][2] * M[1][1] * M[2][0]
        - M[0][1] * M[1][0] * M[2][2]
        - M[0][0] * M[1][2] * M[2][1]
    )


def principal_det(M: list[list[Q]], subset: tuple[int, ...]) -> Q:
    if not subset:
        return Q(1)
    if len(subset) == 1:
        return M[subset[0]][subset[0]]
    if len(subset) == 2:
        return det2(M, subset)
    return det3(M)


def events(M: list[list[Q]]) -> dict[tuple[int, ...], Q]:
    universe = {0, 1, 2}
    out: dict[tuple[int, ...], Q] = {}
    for S in SUBSETS:
        S_set = set(S)
        rest = sorted(universe - S_set)
        total = Q(0)
        for mask in range(1 << len(rest)):
            A = set(S_set)
            parity = 0
            for bit, item in enumerate(rest):
                if (mask >> bit) & 1:
                    A.add(item)
                    parity += 1
            total += ((-1) ** parity) * principal_det(M, tuple(sorted(A)))
        out[S] = total
    return out


def ray(K: list[list[Q]], D: list[list[Q]], t: Q) -> list[list[Q]]:
    return [[K[i][j] + t * D[i][j] for j in range(3)] for i in range(3)]


def event_jets(K: list[list[Q]], D: list[list[Q]]) -> tuple[dict[tuple[int, ...], Q], dict[tuple[int, ...], Q], dict[tuple[int, ...], Q]]:
    p0 = events(K)
    p1 = events(ray(K, D, Q(1)))
    pm1 = events(ray(K, D, Q(-1)))
    p2 = events(ray(K, D, Q(2)))
    pm2 = events(ray(K, D, Q(-2)))
    dp: dict[tuple[int, ...], Q] = {}
    ddp: dict[tuple[int, ...], Q] = {}
    for S in SUBSETS:
        dp[S] = (pm2[S] - 8 * pm1[S] + 8 * p1[S] - p2[S]) / 12
        ddp[S] = p1[S] - 2 * p0[S] + pm1[S]
    return p0, dp, ddp


def leading_minors(M: list[list[Q]]) -> list[Q]:
    return [M[0][0], M[0][0] * M[1][1] - M[0][1] * M[1][0], det3(M)]


def subtract_from_identity(K: list[list[Q]]) -> list[list[Q]]:
    return [[(Q(1) if i == j else Q(0)) - K[i][j] for j in range(3)] for i in range(3)]


def feasible(K: list[list[Q]]) -> bool:
    return all(x > 0 for x in leading_minors(K)) and all(x > 0 for x in leading_minors(subtract_from_identity(K)))


def table_for_k(
    p: dict[tuple[int, ...], Q], dp: dict[tuple[int, ...], Q], k: int, present: bool
) -> tuple[list[Q], list[Q], tuple[int, int]]:
    i, j = [x for x in range(3) if x != k]
    base = (k,) if present else ()
    keys = [
        tuple(sorted(base)),
        tuple(sorted(base + (i,))),
        tuple(sorted(base + (j,))),
        tuple(sorted(base + (i, j))),
    ]
    return [p[x] for x in keys], [dp[x] for x in keys], (i, j)


def table_projection(atoms: list[Q], datoms: list[Q]) -> dict[str, Q]:
    a, b, c, d = atoms
    ap, bp, cp, dp = datoms
    m = a + b + c + d
    mp = ap + bp + cp + dp
    delta = a * d - b * c
    deltap = ap * d + a * dp - bp * c - b * cp
    h = [d, -c, -b, a]
    h0 = [x - 2 * delta / m for x in h]
    V = sum(atoms[r] * h0[r] * h0[r] for r in range(4))
    V_formula = a * d * (a + d) + b * c * (b + c) - 4 * delta * delta / m
    u = deltap - 2 * delta * mp / m
    centered_fisher = sum(atoms[r] * (datoms[r] / atoms[r] - mp / m) ** 2 for r in range(4))
    projection = u * u / V
    gamma = u / V
    residual = sum(atoms[r] * (datoms[r] / atoms[r] - mp / m - gamma * h0[r]) ** 2 for r in range(4))
    assert V == V_formula
    assert sum(atoms[r] * h0[r] for r in range(4)) == 0
    assert centered_fisher == projection + residual
    return {
        "m": m,
        "mp": mp,
        "delta": delta,
        "V": V,
        "u": u,
        "centered_fisher": centered_fisher,
        "projection": projection,
        "residual": residual,
    }


def K_entry(K: list[list[Q]], i: int, j: int) -> Q:
    return K[i][j]


def D_entry(D: list[list[Q]], i: int, j: int) -> Q:
    return D[i][j]


def square_specialization(K: list[list[Q]], D: list[list[Q]], p: dict[tuple[int, ...], Q], dp: dict[tuple[int, ...], Q], k: int) -> list[dict[str, bool]]:
    i, j = [x for x in range(3) if x != k]
    pair = tuple(sorted((i, j)))
    ik = tuple(sorted((i, k)))
    jk = tuple(sorted((j, k)))
    full = (0, 1, 2)

    w0 = (1 - K_entry(K, k, k)) * K_entry(K, i, j) + K_entry(K, i, k) * K_entry(K, j, k)
    w0p = (
        -D_entry(D, k, k) * K_entry(K, i, j)
        + (1 - K_entry(K, k, k)) * D_entry(D, i, j)
        + D_entry(D, i, k) * K_entry(K, j, k)
        + K_entry(K, i, k) * D_entry(D, j, k)
    )
    delta0 = p[()] * p[pair] - p[(i,)] * p[(j,)]
    delta0p = dp[()] * p[pair] + p[()] * dp[pair] - dp[(i,)] * p[(j,)] - p[(i,)] * dp[(j,)]

    w1 = K_entry(K, k, k) * K_entry(K, i, j) - K_entry(K, i, k) * K_entry(K, j, k)
    w1p = (
        D_entry(D, k, k) * K_entry(K, i, j)
        + K_entry(K, k, k) * D_entry(D, i, j)
        - D_entry(D, i, k) * K_entry(K, j, k)
        - K_entry(K, i, k) * D_entry(D, j, k)
    )
    delta1 = p[(k,)] * p[full] - p[ik] * p[jk]
    delta1p = dp[(k,)] * p[full] + p[(k,)] * dp[full] - dp[ik] * p[jk] - p[ik] * dp[jk]

    return [
        {"delta_equals_minus_square": delta0 == -(w0 * w0), "d_delta_equals": delta0p == -2 * w0 * w0p},
        {"delta_equals_minus_square": delta1 == -(w1 * w1), "d_delta_equals": delta1p == -2 * w1 * w1p},
    ]


def fisher(p: dict[tuple[int, ...], Q], dp: dict[tuple[int, ...], Q]) -> Q:
    return sum(dp[S] * dp[S] / p[S] for S in SUBSETS)


def q_values_for_all_k(K: list[list[Q]], D: list[list[Q]]) -> dict[str, object]:
    p, dp, _ = event_jets(K, D)
    total_F = fisher(p, dp)
    q_vals: list[Q] = []
    residuals: list[Q] = []
    square_checks = []
    chain_rule_ok = []
    dpp_mass_ok = []
    for k in range(3):
        atoms0, datoms0, _ = table_for_k(p, dp, k, present=False)
        atoms1, datoms1, _ = table_for_k(p, dp, k, present=True)
        t0 = table_projection(atoms0, datoms0)
        t1 = table_projection(atoms1, datoms1)
        m0, m1 = t0["m"], t1["m"]
        m0p, m1p = t0["mp"], t1["mp"]
        mass_fisher = m1p * m1p / (m0 * m1)
        chain = mass_fisher + t0["centered_fisher"] + t1["centered_fisher"]
        Qk = mass_fisher + t0["projection"] + t1["projection"]
        residual = t0["residual"] + t1["residual"]
        q_vals.append(Qk)
        residuals.append(residual)
        chain_rule_ok.append(chain == total_F)
        dpp_mass_ok.append(m1 == K[k][k] and m1p == D[k][k] and m0 + m1 == 1 and m0p + m1p == 0)
        square_checks.extend(square_specialization(K, D, p, dp, k))
        assert total_F == Qk + residual
    return {
        "F": total_F,
        "Q": q_vals,
        "residuals": residuals,
        "F_minus_Q_equals_residual": [total_F - q_vals[i] == residuals[i] for i in range(3)],
        "chain_rule_ok": chain_rule_ok,
        "dpp_mass_ok": dpp_mass_ok,
        "square_checks": square_checks,
    }


def log_unit_bounds(x: Q, terms: int) -> tuple[Q, Q, Q]:
    assert Q(1) <= x <= Q(2)
    z = (x - 1) / (x + 1)
    lower = Q(0)
    for r in range(terms):
        lower += z ** (2 * r + 1) / Q(2 * r + 1)
    lower *= 2
    remainder = 2 * z ** (2 * terms + 1) / (Q(2 * terms + 1) * (1 - z * z))
    return lower, lower + remainder, abs(z)


def log_bounds(x: Q, terms: int = 70) -> tuple[Q, Q, Q]:
    assert x > 0
    y = x
    power = 0
    while y < 1:
        y *= 2
        power -= 1
    while y > 2:
        y /= 2
        power += 1
    lo, hi, z_abs = log_unit_bounds(y, terms)
    lo2, hi2, _ = log_unit_bounds(Q(2), terms)
    if power >= 0:
        return lo + power * lo2, hi + power * hi2, z_abs
    return lo + power * hi2, hi + power * lo2, z_abs


def floor_int(x: Q) -> int:
    return x.numerator // x.denominator


def ceil_int(x: Q) -> int:
    return -((-x.numerator) // x.denominator)


def compact(lo: Q, hi: Q) -> list[str]:
    scale = 10**12
    return [str(Q(floor_int(lo * scale), scale)), str(Q(ceil_int(hi * scale), scale))]


def cofactor_interval(p: dict[tuple[int, ...], Q], ddp: dict[tuple[int, ...], Q], terms: int = 70) -> tuple[Q, Q, Q]:
    lo_total = Q(0)
    hi_total = Q(0)
    max_z = Q(0)
    for S in SUBSETS:
        lo, hi, z_abs = log_bounds(p[S], terms)
        max_z = max(max_z, z_abs)
        coeff = -ddp[S]
        if coeff >= 0:
            lo_total += coeff * lo
            hi_total += coeff * hi
        else:
            lo_total += coeff * hi
            hi_total += coeff * lo
    return lo_total, hi_total, max_z


def author_object(path: str) -> str:
    return subprocess.check_output(["git", "show", f"{TARGET_COMMIT}:{path}"], text=True)


def author_blob(path: str) -> str:
    return subprocess.check_output(["git", "rev-parse", f"{TARGET_COMMIT}:{path}"], text=True).strip()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def obstruction_recompute() -> dict[str, object]:
    K = [[Q(v, 100) for v in row] for row in [(30, 29, 15), (29, 33, 10), (15, 10, 16)]]
    dcoords = [Q(1), Q(1), Q(1, 3), Q(0), Q(0), Q(0)]
    D = direction_from_coords(dcoords)
    step = Q(1, 100000)
    p, dp, ddp = event_jets(K, D)
    F = fisher(p, dp)
    qdata = q_values_for_all_k(K, D)
    C_lo, C_hi, max_z = cofactor_interval(p, ddp, terms=70)
    q_vals = qdata["Q"]
    max_q = max(q_vals)
    report = {
        "status": "EXACT_SHORTCUT_COUNTEREXAMPLE_NOT_ENTROPY_COUNTEREXAMPLE",
        "K": [[qstr(x) for x in row] for row in K],
        "d": [qstr(x) for x in dcoords],
        "t": qstr(step),
        "exact_feasibility": feasible(K) and feasible(ray(K, D, step)) and feasible(ray(K, D, -step)),
        "leading_minors": {
            "K": [qstr(x) for x in leading_minors(K)],
            "I_minus_K": [qstr(x) for x in leading_minors(subtract_from_identity(K))],
            "K_plus_tD": [qstr(x) for x in leading_minors(ray(K, D, step))],
            "I_minus_K_plus_tD": [qstr(x) for x in leading_minors(subtract_from_identity(ray(K, D, step)))],
            "K_minus_tD": [qstr(x) for x in leading_minors(ray(K, D, -step))],
            "I_minus_K_minus_tD": [qstr(x) for x in leading_minors(subtract_from_identity(ray(K, D, -step)))],
        },
        "p_bitmask_order": [qstr(p[S]) for S in BITMASK_ORDER],
        "fisher_interval": compact(F, F),
        "Q_intervals": [compact(x, x) for x in q_vals],
        "cofactor_interval": compact(C_lo, C_hi),
        "shortcut_gap_interval": compact(max_q - C_hi, max_q - C_lo),
        "true_B_interval": compact(F - C_hi, F - C_lo),
        "log_series_terms": 70,
        "max_scaled_log_z_abs": qstr(max_z),
        "score_projection": {
            "F_minus_Q_equals_residual": qdata["F_minus_Q_equals_residual"],
            "chain_rule_ok": qdata["chain_rule_ok"],
            "dpp_mass_ok": qdata["dpp_mass_ok"],
            "all_square_specializations_ok": all(
                item["delta_equals_minus_square"] and item["d_delta_equals"] for item in qdata["square_checks"]
            ),
            "residuals_nonnegative": [x >= 0 for x in qdata["residuals"]],
        },
    }
    return report


def auxiliary_score_projection_checks() -> dict[str, object]:
    samples = [
        {
            "name": "small_edges_mixed_direction",
            "K": mat_from_coords([Q(2, 5), Q(3, 7), Q(4, 9), Q(1, 30), Q(-1, 40), Q(1, 35)]),
            "D": direction_from_coords([Q(1, 7), Q(-1, 5), Q(1, 6), Q(1, 20), Q(-1, 30), Q(1, 25)]),
        },
        {
            "name": "asymmetric_diagonal_direction",
            "K": mat_from_coords([Q(5, 12), Q(7, 15), Q(3, 8), Q(-1, 25), Q(1, 33), Q(-1, 31)]),
            "D": direction_from_coords([Q(-1, 9), Q(1, 8), Q(1, 10), Q(1, 40), Q(1, 45), Q(-1, 50)]),
        },
    ]
    checked = []
    for sample in samples:
        K = sample["K"]
        D = sample["D"]
        assert feasible(K), sample["name"]
        qdata = q_values_for_all_k(K, D)
        checked.append(
            {
                "name": sample["name"],
                "feasible_strict_K": True,
                "F_minus_Q_equals_residual": qdata["F_minus_Q_equals_residual"],
                "chain_rule_ok": qdata["chain_rule_ok"],
                "dpp_mass_ok": qdata["dpp_mass_ok"],
                "all_square_specializations_ok": all(
                    item["delta_equals_minus_square"] and item["d_delta_equals"] for item in qdata["square_checks"]
                ),
                "residuals_nonnegative": [x >= 0 for x in qdata["residuals"]],
            }
        )
    return {"auxiliary_samples": len(checked), "checks": checked}


def compare_author_certificate(independent: dict[str, object]) -> dict[str, object]:
    author = json.loads(author_object(AUTHOR_CERT))
    key_map = {
        "status": "status",
        "K": "K",
        "d": "d",
        "t": "t",
        "exact_feasibility": "exact_feasibility",
        "p": "p_bitmask_order",
        "fisher_interval": "fisher_interval",
        "Q_intervals": "Q_intervals",
        "cofactor_interval": "cofactor_interval",
        "shortcut_gap_interval": "shortcut_gap_interval",
        "true_B_interval": "true_B_interval",
        "log_series_terms": "log_series_terms",
    }
    mismatches = []
    for author_key, own_key in key_map.items():
        if author.get(author_key) != independent.get(own_key):
            mismatches.append({"field": author_key, "author": author.get(author_key), "independent": independent.get(own_key)})
    return {
        "matches_author_certificate": not mismatches,
        "mismatches": mismatches,
        "author_status": author.get("status"),
        "author_source_sha256": author.get("source_sha256"),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="research/N3/review/score_obstruction_audit_results.json")
    ns = parser.parse_args()

    start = time.time()
    own = obstruction_recompute()
    aux = auxiliary_score_projection_checks()
    comparison = compare_author_certificate(own)
    blobs = {path: author_blob(path) for path in [AUTHOR_FROZEN, AUTHOR_PROOF, AUTHOR_SCRIPT, AUTHOR_CERT]}

    pass_checks = [
        own["exact_feasibility"],
        own["score_projection"]["all_square_specializations_ok"],
        all(own["score_projection"]["F_minus_Q_equals_residual"]),
        all(own["score_projection"]["chain_rule_ok"]),
        all(own["score_projection"]["dpp_mass_ok"]),
        all(own["score_projection"]["residuals_nonnegative"]),
        comparison["matches_author_certificate"],
    ]
    for item in aux["checks"]:
        pass_checks.extend(
            [
                item["feasible_strict_K"],
                item["all_square_specializations_ok"],
                all(item["F_minus_Q_equals_residual"]),
                all(item["chain_rule_ok"]),
                all(item["dpp_mass_ok"]),
                all(item["residuals_nonnegative"]),
            ]
        )

    script_path = Path(__file__).resolve()
    result = {
        "status": "PASS" if all(pass_checks) else "FAIL",
        "purpose": "Non-author audit of fixed conditional-score lower bound and shortcut obstruction; not a global theorem certification.",
        "target_commit": TARGET_COMMIT,
        "target_blobs": blobs,
        "script": str(script_path),
        "script_sha256": sha256_file(script_path),
        "argv": sys.argv,
        "pid": os.getpid(),
        "cwd": os.getcwd(),
        "python": sys.version,
        "executable": sys.executable,
        "platform": platform.platform(),
        "env_threads": {k: os.environ.get(k) for k in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"]},
        "obstruction_recompute": own,
        "author_certificate_comparison": comparison,
        "auxiliary_score_projection_checks": aux,
        "coverage": {
            "fixed_commit_objects_read": 4,
            "exact_score_projection_samples": 3,
            "conditioning_coordinates_per_sample": 3,
            "table_projection_identities_per_sample": 6,
            "dpp_square_and_derivative_specializations_per_sample": 6,
            "exact_obstruction_centers": 1,
            "log_interval_terms": 70,
        },
        "non_coverage": [
            "No proof of global rho(K)<=1 or full n=3 entropy concavity.",
            "No certification of optimizer-direction claims; the displayed obstruction direction is not the trace-constrained minimizer.",
            "No claim that max_k Q_k(D_*) >= C(D_*) holds for the optimizer direction.",
            "No interval certification beyond the single displayed rational obstruction.",
            "No Lean certification.",
        ],
        "elapsed_seconds": time.time() - start,
    }

    output = Path(ns.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(f"STATUS {result['status']}")
    print(f"wrote {output}")
    print(f"pid {result['pid']}")
    print(f"target {TARGET_COMMIT}")
    print(f"certificate_match {comparison['matches_author_certificate']}")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
