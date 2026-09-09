#!/usr/bin/env python3
"""Independent bounded audit for the frozen beta-zero root certificate.

This script does two things:

1. It reconstructs a temporary copy of the fixed frozen source tree at
   TARGET_COMMIT and reruns beta_root_certificate.py without modifying the
   author's checkout.
2. It independently cross-checks the event probabilities/Jacobian, off-diagonal
   factor two, scaled Htilde identities, log enclosures, root-bracket interval
   signs, Gaussian interval solve diagnostics, strictness, connectedness and the
   "whole bracket" dalpha < 1 assertion.

The checks are deterministic and bounded.  They certify only the fixed frozen
object named below, not the global B0/N3 theorem and not uniqueness of a beta
zero.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import os
import platform
import subprocess
import sys
import tempfile
import time
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import mpmath as mp

from verify_round2_definitions import (
    COORDS,
    SUBSETS,
    det3,
    event_first_jacobian,
    events,
)


TARGET_COMMIT = "ab914ec2f73577907314ab3119c4d9f499b17e10"
TARGET_FILES = [
    "research/N3/round2/falsification/beta_zero_existence.md",
    "research/N3/round2/falsification/beta_affine_probe.py",
    "research/N3/round2/falsification/beta_root_certificate.py",
    "research/N3/round2/falsification/root_certificate.json",
    "research/N3/round2/falsification/source_manifest.json",
    "research/N3/falsification/rank2_projection_check.py",
    "research/N3/falsification/unequal_sparse_probe.py",
]
MASK_TO_SUBSET = {
    0: (),
    1: (0,),
    2: (1,),
    3: (0, 1),
    4: (2,),
    5: (0, 2),
    6: (1, 2),
    7: (0, 1, 2),
}
LAMBDA_SIGNS = {
    (): -1,
    (0,): 1,
    (1,): 1,
    (2,): 1,
    (0, 1): -1,
    (0, 2): -1,
    (1, 2): -1,
    (0, 1, 2): 1,
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def review_dir() -> Path:
    return Path(__file__).resolve().parent


def git_bytes(path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{TARGET_COMMIT}:{path}"], cwd=repo_root())


def git_text(path: str) -> str:
    return git_bytes(path).decode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_frozen_tree(root: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for rel in TARGET_FILES:
        data = git_bytes(rel)
        dst = root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(data)
        hashes[rel] = sha256_bytes(data)
    return hashes


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def parse_matrix(rows: list[list[str]]) -> list[list[Q]]:
    return [[Q(x) for x in row] for row in rows]


def interpolate(A: list[list[Q]], B: list[list[Q]], t: Q) -> list[list[Q]]:
    return [[(1 - t) * A[i][j] + t * B[i][j] for j in range(3)] for i in range(3)]


def q_to_mpf(x: Q) -> mp.mpf:
    return mp.mpf(x.numerator) / x.denominator


def i_to_bounds(x: Any) -> tuple[mp.mpf, mp.mpf]:
    return q_to_mpf(x.lo), q_to_mpf(x.hi)


def interval_to_json(x: Any) -> dict[str, str]:
    return {
        "lower": str(x.lo),
        "upper": str(x.hi),
        "approx_lower": mp.nstr(q_to_mpf(x.lo), 30),
        "approx_upper": mp.nstr(q_to_mpf(x.hi), 30),
    }


def event_matrix_from_det_formula(K: list[list[Q]]) -> tuple[list[Q], list[list[Q]]]:
    """Author-style determinant event formula, implemented independently."""

    def cofactor(M: list[list[Q]], i: int, j: int) -> Q:
        rows = [k for k in range(3) if k != i]
        cols = [k for k in range(3) if k != j]
        return ((-1) ** (i + j)) * (
            M[rows[0]][cols[0]] * M[rows[1]][cols[1]]
            - M[rows[0]][cols[1]] * M[rows[1]][cols[0]]
        )

    p: list[Q] = []
    J: list[list[Q]] = []
    for mask in range(8):
        M = [row[:] for row in K]
        for i in range(3):
            if not ((mask >> i) & 1):
                M[i][i] -= 1
        s = Q((-1) ** (3 - int(mask).bit_count()))
        p.append(s * det3(M))
        row: list[Q] = []
        for i, j in COORDS:
            val = cofactor(M, i, j)
            if i != j:
                val += cofactor(M, j, i)
            row.append(s * val)
        J.append(row)
    return p, J


def audit_events_and_offdiag(A: list[list[Q]], B: list[list[Q]], samples: dict[str, Q]) -> dict[str, Any]:
    max_event_error = Q(0)
    max_jacobian_error = Q(0)
    offdiag_factor2_checks = 0
    positive_atoms = True
    for t in samples.values():
        K = interpolate(A, B, t)
        p_mobius, J_mobius = event_first_jacobian(K)
        p_det, J_det = event_matrix_from_det_formula(K)
        for mask in range(8):
            subset = MASK_TO_SUBSET[mask]
            max_event_error = max(max_event_error, abs(p_det[mask] - p_mobius[subset]))
            row_idx = SUBSETS.index(subset)
            for col in range(6):
                max_jacobian_error = max(max_jacobian_error, abs(J_det[mask][col] - J_mobius[row_idx][col]))
            positive_atoms = positive_atoms and p_det[mask] > 0

        # Directly check that the three symmetric off-diagonal coordinates
        # carry both matrix-entry derivatives.  This catches the missing-factor-2
        # failure mode at nonzero cofactor rows.
        for mask in range(8):
            M = [row[:] for row in K]
            for i in range(3):
                if not ((mask >> i) & 1):
                    M[i][i] -= 1
            s = Q((-1) ** (3 - int(mask).bit_count()))
            for col, (i, j) in enumerate(COORDS[3:], start=3):
                def cof(ii: int, jj: int) -> Q:
                    rows = [k for k in range(3) if k != ii]
                    cols = [k for k in range(3) if k != jj]
                    return ((-1) ** (ii + jj)) * (
                        M[rows[0]][cols[0]] * M[rows[1]][cols[1]]
                        - M[rows[0]][cols[1]] * M[rows[1]][cols[0]]
                    )

                expected = s * (cof(i, j) + cof(j, i))
                symmetric_expected = 2 * s * cof(i, j)
                if expected != symmetric_expected:
                    raise AssertionError("symmetric cofactor equality failed")
                if J_det[mask][col] != symmetric_expected:
                    raise AssertionError("off-diagonal factor-two check failed")
                offdiag_factor2_checks += 1

    return {
        "sample_count": len(samples),
        "samples": {k: str(v) for k, v in samples.items()},
        "max_event_error": str(max_event_error),
        "max_jacobian_error": str(max_jacobian_error),
        "offdiag_factor2_checks": offdiag_factor2_checks,
        "all_sample_atoms_positive": positive_atoms,
    }


def matmul(A: list[list[mp.mpf]], B: list[list[mp.mpf]]) -> list[list[mp.mpf]]:
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def trace(A: list[list[mp.mpf]]) -> mp.mpf:
    return sum(A[i][i] for i in range(len(A)))


def det3_mp(A: list[list[mp.mpf]]) -> mp.mpf:
    return (
        A[0][0] * (A[1][1] * A[2][2] - A[1][2] * A[2][1])
        - A[0][1] * (A[1][0] * A[2][2] - A[1][2] * A[2][0])
        + A[0][2] * (A[1][0] * A[2][1] - A[1][1] * A[2][0])
    )


def cofactor_mp(A: list[list[mp.mpf]], i: int, j: int) -> mp.mpf:
    rows = [k for k in range(3) if k != i]
    cols = [k for k in range(3) if k != j]
    return ((-1) ** (i + j)) * (
        A[rows[0]][cols[0]] * A[rows[1]][cols[1]]
        - A[rows[0]][cols[1]] * A[rows[1]][cols[0]]
    )


def mp_matrix(rows: list[list[mp.mpf]]) -> mp.matrix:
    return mp.matrix(rows)


def independent_scaled_quantities(K: list[list[Q]]) -> dict[str, Any]:
    p, Jq = event_first_jacobian(K)
    pf = {S: q_to_mpf(p[S]) for S in SUBSETS}
    J = [[q_to_mpf(x) for x in row] for row in Jq]
    Z = sum(1 / pf[S] for S in SUBSETS)
    g = [
        sum(mp.mpf(LAMBDA_SIGNS[S]) * J[SUBSETS.index(S)][j] / pf[S] for S in SUBSETS)
        for j in range(6)
    ]
    F = [
        [sum(J[s][i] * J[s][j] / pf[SUBSETS[s]] for s in range(8)) for j in range(6)]
        for i in range(6)
    ]
    Fpair = [[F[i][j] - g[i] * g[j] / Z for j in range(6)] for i in range(6)]
    ell12 = mp.log(pf[()] * pf[(0, 1)] / (pf[(0,)] * pf[(1,)]))
    ell13 = mp.log(pf[()] * pf[(0, 2)] / (pf[(0,)] * pf[(2,)]))
    ell23 = mp.log(pf[()] * pf[(1, 2)] / (pf[(1,)] * pf[(2,)]))
    lam = mp.log(pf[(0, 1, 2)] * pf[(0,)] * pf[(1,)] * pf[(2,)] / (pf[()] * pf[(0, 1)] * pf[(0, 2)] * pf[(1, 2)]))
    Km = [[q_to_mpf(K[i][j]) for j in range(3)] for i in range(3)]
    N = [[-lam * Km[i][j] for j in range(3)] for i in range(3)]
    N[0][0] -= ell23
    N[1][1] -= ell13
    N[2][2] -= ell12
    d = det3_mp(N)
    adj = [[cofactor_mp(N, j, i) for j in range(3)] for i in range(3)]
    E: list[list[list[mp.mpf]]] = []
    for i, j in COORDS:
        e = [[mp.mpf("0") for _ in range(3)] for _ in range(3)]
        e[i][j] = mp.mpf("1")
        e[j][i] = mp.mpf("1")
        E.append(e)
    ae = [trace(matmul(adj, e)) for e in E]
    T = [[trace(matmul(matmul(matmul(adj, E[i]), adj), E[j])) for j in range(6)] for i in range(6)]
    Htilde = [[d * Fpair[i][j] + T[i][j] for j in range(6)] for i in range(6)]
    H = [[Fpair[i][j] + T[i][j] / d for j in range(6)] for i in range(6)]
    h_scaled = mp.lu_solve(mp_matrix(Htilde), mp.matrix(ae))
    c = mp.matrix([ae[i] / d for i in range(6)])
    h_unscaled = mp.lu_solve(mp_matrix(H), c)
    dalpha_scaled = sum(ae[i] * h_scaled[i] for i in range(6))
    alpha = sum(c[i] * h_unscaled[i] for i in range(6))
    beta_times_sqrtZ = sum(g[i] * h_scaled[i] for i in range(6))
    beta = beta_times_sqrtZ / mp.sqrt(Z)
    return {
        "d": d,
        "alpha": alpha,
        "dalpha_scaled": dalpha_scaled,
        "d_alpha_unscaled": d * alpha,
        "scaling_error": abs(dalpha_scaled - d * alpha),
        "beta": beta,
        "beta_times_sqrtZ": beta_times_sqrtZ,
        "Z": Z,
        "min_atom": min(pf.values()),
    }


def audit_h_scaling_and_logs(
    A: list[list[Q]],
    B: list[list[Q]],
    samples: dict[str, Q],
    log_bound,
) -> dict[str, Any]:
    max_scaling_error = mp.mpf("0")
    max_log_miss = mp.mpf("0")
    rows: dict[str, Any] = {}
    for name, t in samples.items():
        K = interpolate(A, B, t)
        q = independent_scaled_quantities(K)
        max_scaling_error = max(max_scaling_error, q["scaling_error"])
        p = events(K)
        args = [
            p[()] * p[(1, 2)] / (p[(1,)] * p[(2,)]),
            p[()] * p[(0, 2)] / (p[(0,)] * p[(2,)]),
            p[()] * p[(0, 1)] / (p[(0,)] * p[(1,)]),
            p[(0, 1, 2)] * p[(0,)] * p[(1,)] * p[(2,)] / (p[()] * p[(0, 1)] * p[(0, 2)] * p[(1, 2)]),
        ]
        log_ok = True
        for arg in args:
            lo, hi = log_bound(arg)
            exact = mp.log(q_to_mpf(arg))
            miss = max(q_to_mpf(lo) - exact, exact - q_to_mpf(hi), mp.mpf("0"))
            max_log_miss = max(max_log_miss, miss)
            log_ok = log_ok and q_to_mpf(lo) <= exact <= q_to_mpf(hi)
        rows[name] = {
            "t": str(t),
            "beta": mp.nstr(q["beta"], 35),
            "beta_times_sqrtZ": mp.nstr(q["beta_times_sqrtZ"], 35),
            "dalpha": mp.nstr(q["dalpha_scaled"], 35),
            "d_alpha_unscaled": mp.nstr(q["d_alpha_unscaled"], 35),
            "scaling_error": mp.nstr(q["scaling_error"], 12),
            "min_atom": mp.nstr(q["min_atom"], 20),
            "log_bounds_contain_high_precision_logs": log_ok,
        }
    return {
        "sample_count": len(samples),
        "max_scaling_error": mp.nstr(max_scaling_error, 20),
        "max_log_miss": mp.nstr(max_log_miss, 20),
        "samples": rows,
    }


def solve_with_pivots(mod, A: list[list[Any]], b: list[Any]) -> tuple[list[Any], list[Any]]:
    work = [list(row) + [b[i]] for i, row in enumerate(A)]
    n = len(b)
    pivots: list[Any] = []
    for k in range(n):
        pivots.append(work[k][k])
        for j in range(k + 1, n):
            q = work[j][k] / work[k][k]
            for col in range(k + 1, n + 1):
                work[j][col] = work[j][col] - q * work[k][col]
            work[j][k] = mod.I(0)
    x = [mod.I(0)] * n
    for k in reversed(range(n)):
        x[k] = (work[k][n] - sum(work[k][j] * x[j] for j in range(k + 1, n))) / work[k][k]
    return x, pivots


def interval_diagnostics(mod, A: list[list[Q]], B: list[list[Q]], left: Q, right: Q) -> dict[str, Any]:
    I = mod.I
    t = I(left, right)
    K = [[I(A[i][j]) + t * (B[i][j] - A[i][j]) for j in range(3)] for i in range(3)]
    p, J, pairs = mod.event_data(K)
    Z = sum(1 / x for x in p)
    signs = [(-1) ** (3 - int(i).bit_count()) for i in range(8)]
    g = [sum(signs[k] * J[k][j] / p[k] for k in range(8)) for j in range(6)]
    Fpair = [[sum(J[k][i] * J[k][j] / p[k] for k in range(8)) - g[i] * g[j] / Z for j in range(6)] for i in range(6)]
    ell = [
        mod.logi(p[0] * p[6] / (p[2] * p[4])),
        mod.logi(p[0] * p[5] / (p[1] * p[4])),
        mod.logi(p[0] * p[3] / (p[1] * p[2])),
    ]
    lam = mod.logi(p[7] * p[1] * p[2] * p[4] / (p[0] * p[3] * p[5] * p[6]))
    N = [[-lam * K[i][j] - (ell[i] if i == j else I(0)) for j in range(3)] for i in range(3)]
    d = mod.det(N)
    adj = [[mod.cof(N, j, i) for j in range(3)] for i in range(3)]
    E = []
    for i, j in pairs:
        e = [[I(0) for _ in range(3)] for _ in range(3)]
        e[i][j] = I(1)
        e[j][i] = I(1)
        E.append(e)
    ae = [mod.tr(mod.prod(adj, e)) for e in E]
    Ht = [
        [
            d * Fpair[i][j] + mod.tr(mod.prod(mod.prod(mod.prod(adj, E[i]), adj), E[j]))
            for j in range(6)
        ]
        for i in range(6)
    ]
    h, pivots = solve_with_pivots(mod, Ht, ae)
    residual = [sum(Ht[i][j] * h[j] for j in range(6)) - ae[i] for i in range(6)]
    b = sum(g[i] * h[i] for i in range(6))
    da = sum(ae[i] * h[i] for i in range(6))
    pivot_abs_lower = min(min(abs(piv.lo), abs(piv.hi)) for piv in pivots if not (piv.lo <= 0 <= piv.hi))
    return {
        "beta_times_sqrtZ": b,
        "dalpha": da,
        "detN": d,
        "min_p": I(min(x.lo for x in p), min(x.hi for x in p)),
        "pivots_exclude_zero": all(not (piv.lo <= 0 <= piv.hi) for piv in pivots),
        "pivot_abs_lower": pivot_abs_lower,
        "residual_contains_zero": all(r.lo <= 0 <= r.hi for r in residual),
        "residuals": residual,
        "h": h,
    }


def high_precision_h(A: list[list[Q]], B: list[list[Q]], t: Q) -> list[mp.mpf]:
    K = interpolate(A, B, t)
    p, Jq = event_first_jacobian(K)
    pf = {S: q_to_mpf(p[S]) for S in SUBSETS}
    J = [[q_to_mpf(x) for x in row] for row in Jq]
    Z = sum(1 / pf[S] for S in SUBSETS)
    g = [
        sum(mp.mpf(LAMBDA_SIGNS[S]) * J[SUBSETS.index(S)][j] / pf[S] for S in SUBSETS)
        for j in range(6)
    ]
    F = [
        [sum(J[s][i] * J[s][j] / pf[SUBSETS[s]] for s in range(8)) for j in range(6)]
        for i in range(6)
    ]
    Fpair = [[F[i][j] - g[i] * g[j] / Z for j in range(6)] for i in range(6)]
    ell12 = mp.log(pf[()] * pf[(0, 1)] / (pf[(0,)] * pf[(1,)]))
    ell13 = mp.log(pf[()] * pf[(0, 2)] / (pf[(0,)] * pf[(2,)]))
    ell23 = mp.log(pf[()] * pf[(1, 2)] / (pf[(1,)] * pf[(2,)]))
    lam = mp.log(pf[(0, 1, 2)] * pf[(0,)] * pf[(1,)] * pf[(2,)] / (pf[()] * pf[(0, 1)] * pf[(0, 2)] * pf[(1, 2)]))
    Km = [[q_to_mpf(K[i][j]) for j in range(3)] for i in range(3)]
    N = [[-lam * Km[i][j] for j in range(3)] for i in range(3)]
    N[0][0] -= ell23
    N[1][1] -= ell13
    N[2][2] -= ell12
    d = det3_mp(N)
    adj = [[cofactor_mp(N, j, i) for j in range(3)] for i in range(3)]
    E = []
    for i, j in COORDS:
        e = [[mp.mpf("0") for _ in range(3)] for _ in range(3)]
        e[i][j] = mp.mpf("1")
        e[j][i] = mp.mpf("1")
        E.append(e)
    ae = [trace(matmul(adj, e)) for e in E]
    T = [[trace(matmul(matmul(matmul(adj, E[i]), adj), E[j])) for j in range(6)] for i in range(6)]
    Htilde = [[d * Fpair[i][j] + T[i][j] for j in range(6)] for i in range(6)]
    h = mp.lu_solve(mp_matrix(Htilde), mp.matrix(ae))
    return [h[i] for i in range(6)]


def audit_interval_solve(mod, A: list[list[Q]], B: list[list[Q]], left: Q, right: Q) -> dict[str, Any]:
    bracket = interval_diagnostics(mod, A, B, left, right)
    endpoint_left = interval_diagnostics(mod, A, B, left, left)
    endpoint_right = interval_diagnostics(mod, A, B, right, right)
    mid = (left + right) / 2
    h_bracket = bracket["h"]
    contain_samples: dict[str, bool] = {}
    for name, t in {"left": left, "mid": mid, "right": right}.items():
        hp = high_precision_h(A, B, t)
        contain_samples[name] = all(i_to_bounds(h_bracket[i])[0] <= hp[i] <= i_to_bounds(h_bracket[i])[1] for i in range(6))
    return {
        "root_left_beta_hi_lt_0": endpoint_left["beta_times_sqrtZ"].hi < 0,
        "root_right_beta_lo_gt_0": endpoint_right["beta_times_sqrtZ"].lo > 0,
        "whole_bracket_dalpha_hi_lt_1": bracket["dalpha"].hi < 1,
        "whole_bracket_min_p_lo_gt_0": bracket["min_p"].lo > 0,
        "whole_bracket_detN_lo_gt_0": bracket["detN"].lo > 0,
        "pivots_exclude_zero": bracket["pivots_exclude_zero"],
        "pivot_abs_lower": str(bracket["pivot_abs_lower"]),
        "residual_contains_zero": bracket["residual_contains_zero"],
        "high_precision_h_samples_inside_bracket_interval_h": contain_samples,
        "root_left_beta_times_sqrtZ": interval_to_json(endpoint_left["beta_times_sqrtZ"]),
        "root_right_beta_times_sqrtZ": interval_to_json(endpoint_right["beta_times_sqrtZ"]),
        "root_entire_bracket_dalpha": interval_to_json(bracket["dalpha"]),
        "root_entire_bracket_min_p": interval_to_json(bracket["min_p"]),
        "root_entire_bracket_detN": interval_to_json(bracket["detN"]),
    }


def principal_minors_positive(M: list[list[Q]]) -> bool:
    return M[0][0] > 0 and M[0][0] * M[1][1] - M[0][1] * M[1][0] > 0 and det3(M) > 0


def audit_strictness(A: list[list[Q]], B: list[list[Q]], left: Q, right: Q) -> dict[str, Any]:
    I = [[Q(int(i == j)) for j in range(3)] for i in range(3)]
    IA = [[I[i][j] - A[i][j] for j in range(3)] for i in range(3)]
    IB = [[I[i][j] - B[i][j] for j in range(3)] for i in range(3)]
    Kleft = interpolate(A, B, left)
    Kright = interpolate(A, B, right)
    fixed_edges = {
        "12": str(Kleft[0][1]),
        "13": str(Kleft[0][2]),
        "23_left": str(Kleft[1][2]),
        "23_right": str(Kright[1][2]),
    }
    return {
        "A_positive_definite": principal_minors_positive(A),
        "B_positive_definite": principal_minors_positive(B),
        "I_minus_A_positive_definite": principal_minors_positive(IA),
        "I_minus_B_positive_definite": principal_minors_positive(IB),
        "bracket_inside_0_1_over_8": Q(0) < left < right < Q(1, 8),
        "connected_on_bracket_by_fixed_edges_12_13": Kleft[0][1] != 0 and Kleft[0][2] != 0,
        "nonexchangeable_by_unequal_fixed_edges": abs(Kleft[0][1]) != abs(Kleft[0][2]),
        "fixed_edges": fixed_edges,
    }


def compare_critical_certificate_fields(original: dict[str, Any], rerun: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "status",
        "baseline",
        "interval_bits",
        "family",
        "A",
        "B",
        "bisection_calls",
        "interval_calls",
        "rejected",
        "root_bracket",
        "certificate",
    ]
    mismatches = [key for key in keys if original.get(key) != rerun.get(key)]
    return {"critical_fields_match": not mismatches, "mismatches": mismatches, "keys_checked": keys}


def main() -> int:
    start = time.time()
    mp.mp.dps = 180
    out_dir = review_dir()
    original_cert = json.loads(git_text("research/N3/round2/falsification/root_certificate.json"))
    source_manifest = json.loads(git_text("research/N3/round2/falsification/source_manifest.json"))
    left, right = [Q(x) for x in original_cert["root_bracket"]]
    A = parse_matrix(original_cert["A"])
    B = parse_matrix(original_cert["B"])
    samples = {
        "root_left": left,
        "root_mid": (left + right) / 2,
        "root_right": right,
        "endpoint_negative": Q(0),
        "endpoint_positive": Q(1, 8),
    }
    stdout_path = out_dir / "beta_root_author_rerun.stdout.txt"
    stderr_path = out_dir / "beta_root_author_rerun.stderr.txt"
    env = os.environ.copy()
    for key in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"]:
        env[key] = "1"

    with tempfile.TemporaryDirectory(prefix="beta_root_audit_", dir=out_dir) as tmp_str:
        tmp = Path(tmp_str)
        extracted_hashes = write_frozen_tree(tmp)
        proc = subprocess.run(
            [sys.executable, "research/N3/round2/falsification/beta_root_certificate.py"],
            cwd=tmp,
            env=env,
            text=True,
            capture_output=True,
            timeout=180,
        )
        stdout_path.write_text(proc.stdout, encoding="utf-8")
        stderr_path.write_text(proc.stderr, encoding="utf-8")
        rerun_cert_path = tmp / "research/N3/round2/falsification/root_certificate.json"
        rerun_cert = json.loads(rerun_cert_path.read_text(encoding="utf-8"))
        sys.path.insert(0, str(tmp / "research/N3/round2/falsification"))
        sys.path.insert(0, str(tmp / "research/N3/falsification"))
        root_mod = load_module("frozen_beta_root_certificate_for_audit", tmp / "research/N3/round2/falsification/beta_root_certificate.py")
        rank2_mod = load_module("frozen_rank2_projection_check_for_audit", tmp / "research/N3/falsification/rank2_projection_check.py")
        interval = audit_interval_solve(root_mod, A, B, left, right)
        logs_and_scaling = audit_h_scaling_and_logs(A, B, samples, rank2_mod.log_bound)

    source_hash_checks = {
        rel: {
            "manifest_sha256": source_manifest.get(rel),
            "extracted_sha256": extracted_hashes.get(rel),
            "matches_manifest": source_manifest.get(rel) == extracted_hashes.get(rel),
        }
        for rel in source_manifest
    }
    event_audit = audit_events_and_offdiag(A, B, samples)
    strictness = audit_strictness(A, B, left, right)
    rerun_compare = compare_critical_certificate_fields(original_cert, rerun_cert)
    required_booleans = [
        proc.returncode == 0,
        rerun_compare["critical_fields_match"],
        all(item["matches_manifest"] for item in source_hash_checks.values()),
        event_audit["max_event_error"] == "0",
        event_audit["max_jacobian_error"] == "0",
        event_audit["all_sample_atoms_positive"],
        interval["root_left_beta_hi_lt_0"],
        interval["root_right_beta_lo_gt_0"],
        interval["whole_bracket_dalpha_hi_lt_1"],
        interval["whole_bracket_min_p_lo_gt_0"],
        interval["whole_bracket_detN_lo_gt_0"],
        interval["pivots_exclude_zero"],
        interval["residual_contains_zero"],
        all(interval["high_precision_h_samples_inside_bracket_interval_h"].values()),
        all(row["log_bounds_contain_high_precision_logs"] for row in logs_and_scaling["samples"].values()),
        all(v for k, v in strictness.items() if isinstance(v, bool)),
    ]
    status = "PASS" if all(required_booleans) else "FAIL"
    result = {
        "status": status,
        "target_commit": TARGET_COMMIT,
        "target_blob_sha1": {
            rel: subprocess.check_output(["git", "rev-parse", f"{TARGET_COMMIT}:{rel}"], cwd=repo_root(), text=True).strip()
            for rel in TARGET_FILES
        },
        "review_script_sha256": sha256_path(Path(__file__)),
        "python": sys.version,
        "platform": platform.platform(),
        "pid": os.getpid(),
        "thread_env": {key: env.get(key) for key in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"]},
        "author_rerun": {
            "command": [sys.executable, "research/N3/round2/falsification/beta_root_certificate.py"],
            "exit_status": proc.returncode,
            "recorded_pid": rerun_cert.get("pid"),
            "status": rerun_cert.get("status"),
            "root_bracket": rerun_cert.get("root_bracket"),
            "source_sha256": rerun_cert.get("source_sha256"),
            "stdout_path": str(stdout_path.relative_to(repo_root())),
            "stderr_path": str(stderr_path.relative_to(repo_root())),
        },
        "source_hash_checks": source_hash_checks,
        "critical_certificate_comparison": rerun_compare,
        "event_probability_and_gradient_audit": event_audit,
        "h_tilde_scaling_and_log_audit": logs_and_scaling,
        "interval_root_bracket_audit": interval,
        "strict_connected_nonexchangeable_audit": strictness,
        "coverage": {
            "fixed_commits": 1,
            "author_script_reruns": 1,
            "bisection_calls_rerun": rerun_cert.get("bisection_calls"),
            "interval_calls_rerun": rerun_cert.get("interval_calls"),
            "event_formula_samples": event_audit["sample_count"],
            "offdiag_factor2_checks": event_audit["offdiag_factor2_checks"],
            "h_scaling_samples": logs_and_scaling["sample_count"],
            "interval_gaussian_brackets": 3,
            "whole_root_bracket_checked": True,
        },
        "noncoverage": [
            "No uniqueness claim for beta zeros was checked or needed.",
            "No global B0/N3 theorem is proved by this certificate.",
            "No search beyond the fixed frozen affine family and root bracket was performed.",
            "No Lean/formalization audit was performed.",
        ],
        "elapsed_seconds": time.time() - start,
        "exit_status": 0 if status == "PASS" else 1,
    }
    output = out_dir / "beta_root_audit_results.json"
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": status,
        "target_commit": TARGET_COMMIT,
        "pid": os.getpid(),
        "author_rerun_pid": rerun_cert.get("pid"),
        "author_rerun_exit_status": proc.returncode,
        "whole_bracket_dalpha": interval["root_entire_bracket_dalpha"],
        "coverage": result["coverage"],
        "output": str(output.relative_to(repo_root())),
    }))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
