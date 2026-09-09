#!/usr/bin/env python3
"""Independent bounded audit for the frozen locked-odds obstruction.

The frozen object at TARGET_COMMIT disproves a proposed dominance condition
max_k Q_k^lock(D) >= C(D) on one exact Lambda-tangent direction.  It does not
disprove the Fisher lower bound F >= Q_k^lock and does not prove or disprove
the global B0/N3 target.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
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

from verify_round2_definitions import COORDS, SUBSETS, det3, event_first_jacobian
from verify_beta_root_certificate import (
    LAMBDA_SIGNS,
    MASK_TO_SUBSET,
    interval_to_json,
    principal_minors_positive,
    q_to_mpf,
)


TARGET_COMMIT = "c6568dfe1c0c57aaf0b627e84601c35b79b22434"
TARGET_FILES = [
    "research/N3/round2/falsification/locked_obstruction.md",
    "research/N3/round2/falsification/locked_certificate.py",
    "research/N3/round2/falsification/locked_certificate.json",
    "research/N3/round2/falsification/locked_source_manifest.json",
    "research/N3/round2/falsification/locked_probe.py",
    "research/N3/round2/falsification/locked_probe_failed_v1.py",
    "research/N3/round2/falsification/beta_affine_probe.py",
    "research/N3/round2/falsification/beta_root_certificate.py",
    "research/N3/falsification/rank2_projection_check.py",
    "research/N3/falsification/unequal_sparse_probe.py",
]


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


def parse_vector(row: list[str]) -> list[Q]:
    return [Q(x) for x in row]


def matrix_from_direction(d: list[Q]) -> list[list[Q]]:
    return [[d[0], d[3], d[4]], [d[3], d[1], d[5]], [d[4], d[5], d[2]]]


def add_scaled(K: list[list[Q]], D: list[list[Q]], scale: Q) -> list[list[Q]]:
    return [[K[i][j] + scale * D[i][j] for j in range(3)] for i in range(3)]


def cofactor_q(M: list[list[Q]], i: int, j: int) -> Q:
    rows = [k for k in range(3) if k != i]
    cols = [k for k in range(3) if k != j]
    return ((-1) ** (i + j)) * (
        M[rows[0]][cols[0]] * M[rows[1]][cols[1]]
        - M[rows[0]][cols[1]] * M[rows[1]][cols[0]]
    )


def transpose_adjugate(M: list[list[Q]]) -> list[list[Q]]:
    return [[cofactor_q(M, j, i) for j in range(3)] for i in range(3)]


def quad(M: list[list[Q]], d: list[Q]) -> Q:
    return sum(d[i] * M[i][j] * d[j] for i in range(6) for j in range(6))


def exact_event_objects(K: list[list[Q]]) -> tuple[list[Q], list[list[Q]], list[Q], list[list[Q]]]:
    p_by_subset, J_by_subset = event_first_jacobian(K)
    p = [p_by_subset[MASK_TO_SUBSET[mask]] for mask in range(8)]
    J = [J_by_subset[SUBSETS.index(MASK_TO_SUBSET[mask])] for mask in range(8)]
    g = [
        sum(Q((-1) ** (3 - int(mask).bit_count())) * J[mask][j] / p[mask] for mask in range(8))
        for j in range(6)
    ]
    F = [
        [sum(J[mask][i] * J[mask][j] / p[mask] for mask in range(8)) for j in range(6)]
        for i in range(6)
    ]
    return p, J, g, F


def locked_q_matrices(K: list[list[Q]], p: list[Q], J: list[list[Q]]) -> tuple[list[list[list[Q]]], dict[str, Any]]:
    matrices: list[list[list[Q]]] = []
    diagnostics: dict[str, Any] = {"conditioning": []}
    for k in range(3):
        q = [[Q(0) for _ in range(6)] for _ in range(6)]
        q[k][k] = 1 / (K[k][k] * (1 - K[k][k]))
        cond = []
        other = [i for i in range(3) if i != k]
        for state in [0, 1]:
            idx = [(state << k) | ((b & 1) << other[0]) | (((b >> 1) & 1) << other[1]) for b in range(4)]
            a0, b0, c0, d0 = [p[i] for i in idx]
            mass = a0 + b0 + c0 + d0
            delta = a0 * d0 - b0 * c0
            V = a0 * d0 * (a0 + d0) + b0 * c0 * (b0 + c0) - 4 * delta * delta / mass
            Rres = 1 / a0 + 1 / b0 + 1 / c0 + 1 / d0 - mass * mass / V
            L = [
                d0 * J[idx[0]][j]
                + a0 * J[idx[3]][j]
                - c0 * J[idx[1]][j]
                - b0 * J[idx[2]][j]
                - 2 * delta * sum(J[i][j] for i in idx) / mass
                for j in range(6)
            ]
            if not (V > 0 and Rres >= 0):
                raise AssertionError("invalid locked odds slice denominator")
            cond.append((mass, L, V, Rres))
            for i in range(6):
                for j in range(6):
                    q[i][j] += L[i] * L[j] / V
        m0, L0, V0, R0 = cond[0]
        m1, L1, V1, R1 = cond[1]
        if not R0 + R1 > 0:
            raise AssertionError("witness should have positive R0+R1")
        w = [m0 * L0[j] / V0 - m1 * L1[j] / V1 for j in range(6)]
        for i in range(6):
            for j in range(6):
                q[i][j] += w[i] * w[j] / (R0 + R1)
        matrices.append(q)
        diagnostics["conditioning"].append(
            {
                "k": k,
                "V": [str(cond[0][2]), str(cond[1][2])],
                "R": [str(cond[0][3]), str(cond[1][3])],
                "R0_plus_R1": str(R0 + R1),
                "positive_denominators": cond[0][2] > 0 and cond[1][2] > 0 and R0 + R1 > 0,
            }
        )
    return matrices, diagnostics


def exact_odds_derivatives(p: list[Q], J: list[list[Q]], d: list[Q]) -> list[list[str]]:
    odds: list[list[str]] = []
    for k in range(3):
        other = [i for i in range(3) if i != k]
        ev: list[Q] = []
        for state in [0, 1]:
            idx = [(state << k) | ((b & 1) << other[0]) | (((b >> 1) & 1) << other[1]) for b in range(4)]
            dp = [sum(J[i][j] * d[j] for j in range(6)) for i in idx]
            ev.append(sum(sign * dd / p[i] for sign, dd, i in zip([1, -1, -1, 1], dp, idx)))
        odds.append([str(ev[0]), str(ev[1])])
    return odds


def interval_log_comparison(root_mod, K: list[list[Q]], p: list[Q], qvals: list[Q], Fval: Q, dmat: list[list[Q]]) -> dict[str, Any]:
    I = root_mod.I
    adj = transpose_adjugate(dmat)
    ell = [
        root_mod.logi(I(p[0] * p[6] / (p[2] * p[4]))),
        root_mod.logi(I(p[0] * p[5] / (p[1] * p[4]))),
        root_mod.logi(I(p[0] * p[3] / (p[1] * p[2]))),
    ]
    lam = root_mod.logi(I(p[7] * p[1] * p[2] * p[4] / (p[0] * p[3] * p[5] * p[6])))
    trKadj = sum(K[i][j] * adj[j][i] for i in range(3) for j in range(3))
    C = -2 * sum(ell[i] * adj[i][i] for i in range(3)) - 2 * lam * trKadj
    gap = I(max(qvals)) - C
    actual = I(Fval) - C
    log_args = [
        p[0] * p[6] / (p[2] * p[4]),
        p[0] * p[5] / (p[1] * p[4]),
        p[0] * p[3] / (p[1] * p[2]),
        p[7] * p[1] * p[2] * p[4] / (p[0] * p[3] * p[5] * p[6]),
    ]
    log_checks = []
    for arg in log_args:
        bounded = root_mod.logi(I(arg))
        exact = mp.log(q_to_mpf(arg))
        log_checks.append(q_to_mpf(bounded.lo) <= exact <= q_to_mpf(bounded.hi))
    return {
        "C": interval_to_json(C),
        "max_Qlock_minus_C": interval_to_json(gap),
        "actual_B": interval_to_json(actual),
        "gap_hi_lt_0": gap.hi < 0,
        "actual_B_lo_gt_0": actual.lo > 0,
        "log_bounds_contain_high_precision_logs": all(log_checks),
    }


def compare_fields(original: dict[str, Any], rerun: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "status",
        "baseline",
        "locked_source",
        "seed",
        "kernel_calls",
        "direction_calls",
        "rejected",
        "K",
        "D",
        "direction",
        "exact_g",
        "exact_g_dot_D",
        "locked_odds_derivatives",
        "Qlock",
        "F_exact",
        "C",
        "max_Qlock_minus_C",
        "actual_B",
        "feasible_step",
        "endpoints",
        "interval_bits",
        "log_series_terms",
    ]
    mismatches = [key for key in keys if original.get(key) != rerun.get(key)]
    return {"critical_fields_match": not mismatches, "mismatches": mismatches, "keys_checked": keys}


def audit_exact_witness(root_mod, certificate: dict[str, Any]) -> dict[str, Any]:
    K = parse_matrix(certificate["K"])
    D = parse_matrix(certificate["D"])
    dvec = parse_vector(certificate["direction"])
    if matrix_from_direction(dvec) != D:
        raise AssertionError("direction vector and D matrix disagree")
    p, J, g, F = exact_event_objects(K)
    q_mats, q_diag = locked_q_matrices(K, p, J)
    qvals = [quad(q, dvec) for q in q_mats]
    Fval = quad(F, dvec)
    odds = exact_odds_derivatives(p, J, dvec)
    interval = interval_log_comparison(root_mod, K, p, qvals, Fval, D)
    I3 = [[Q(int(i == j)) for j in range(3)] for i in range(3)]
    step = Q(certificate["feasible_step"])
    endpoints = [add_scaled(K, D, -step), add_scaled(K, D, step)]
    endpoint_feasible = []
    for M in endpoints:
        IM = [[I3[i][j] - M[i][j] for j in range(3)] for i in range(3)]
        endpoint_feasible.append(principal_minors_positive(M) and principal_minors_positive(IM))
    return {
        "event_atoms_positive": all(x > 0 for x in p),
        "exact_g_matches_certificate": [str(x) for x in g] == certificate["exact_g"],
        "exact_g_dot_D": str(sum(g[i] * dvec[i] for i in range(6))),
        "lambda_tangent_exact": sum(g[i] * dvec[i] for i in range(6)) == 0,
        "Qlock_matches_certificate": [str(x) for x in qvals] == certificate["Qlock"],
        "F_matches_certificate": str(Fval) == certificate["F_exact"],
        "locked_odds_derivatives_match_certificate": odds == certificate["locked_odds_derivatives"],
        "locked_odds_derivatives_equal_across_slices": all(row[0] == row[1] for row in odds),
        "F_ge_each_Qlock": all(Fval >= q for q in qvals),
        "Qlock_approx": [mp.nstr(q_to_mpf(x), 40) for x in qvals],
        "F_approx": mp.nstr(q_to_mpf(Fval), 40),
        "conditioning_diagnostics": q_diag,
        "interval_log_comparison": interval,
        "feasible_step": str(step),
        "endpoints_feasible": endpoint_feasible,
        "all_endpoints_feasible": all(endpoint_feasible),
        "connected_strict_kernel": K[0][1] != 0 and K[0][2] != 0 and K[1][2] != 0 and all(x > 0 for x in p),
    }


def main() -> int:
    start = time.time()
    mp.mp.dps = 160
    out_dir = review_dir()
    original = json.loads(git_text("research/N3/round2/falsification/locked_certificate.json"))
    manifest = json.loads(git_text("research/N3/round2/falsification/locked_source_manifest.json"))
    stdout_path = out_dir / "locked_certificate_rerun.stdout.txt"
    stderr_path = out_dir / "locked_certificate_rerun.stderr.txt"
    env = os.environ.copy()
    for key in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"]:
        env[key] = "1"

    with tempfile.TemporaryDirectory(prefix="locked_obstruction_audit_", dir=out_dir) as tmp_str:
        tmp = Path(tmp_str)
        extracted = write_frozen_tree(tmp)
        proc = subprocess.run(
            [sys.executable, "research/N3/round2/falsification/locked_certificate.py"],
            cwd=tmp,
            env=env,
            text=True,
            capture_output=True,
            timeout=120,
        )
        stdout_path.write_text(proc.stdout, encoding="utf-8")
        stderr_path.write_text(proc.stderr, encoding="utf-8")
        rerun = json.loads((tmp / "research/N3/round2/falsification/locked_certificate.json").read_text(encoding="utf-8"))
        sys.path.insert(0, str(tmp / "research/N3/round2/falsification"))
        sys.path.insert(0, str(tmp / "research/N3/falsification"))
        root_mod = load_module("locked_audit_beta_root_certificate", tmp / "research/N3/round2/falsification/beta_root_certificate.py")
        exact_audit = audit_exact_witness(root_mod, original)

    source_hash_checks = {
        rel: {
            "manifest_sha256": manifest.get(rel),
            "extracted_sha256": extracted.get(rel),
            "matches_manifest": manifest.get(rel) == extracted.get(rel),
        }
        for rel in manifest
    }
    comparison = compare_fields(original, rerun)
    required = [
        proc.returncode == 0,
        comparison["critical_fields_match"],
        all(item["matches_manifest"] for item in source_hash_checks.values()),
        exact_audit["event_atoms_positive"],
        exact_audit["exact_g_matches_certificate"],
        exact_audit["lambda_tangent_exact"],
        exact_audit["Qlock_matches_certificate"],
        exact_audit["F_matches_certificate"],
        exact_audit["locked_odds_derivatives_match_certificate"],
        exact_audit["locked_odds_derivatives_equal_across_slices"],
        exact_audit["F_ge_each_Qlock"],
        exact_audit["interval_log_comparison"]["gap_hi_lt_0"],
        exact_audit["interval_log_comparison"]["actual_B_lo_gt_0"],
        exact_audit["interval_log_comparison"]["log_bounds_contain_high_precision_logs"],
        exact_audit["all_endpoints_feasible"],
        exact_audit["connected_strict_kernel"],
    ]
    status = "PASS" if all(required) else "FAIL"
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
            "command": [sys.executable, "research/N3/round2/falsification/locked_certificate.py"],
            "exit_status": proc.returncode,
            "recorded_pid": rerun.get("pid"),
            "status": rerun.get("status"),
            "stdout_path": str(stdout_path.relative_to(repo_root())),
            "stderr_path": str(stderr_path.relative_to(repo_root())),
        },
        "source_hash_checks": source_hash_checks,
        "critical_certificate_comparison": comparison,
        "exact_witness_audit": exact_audit,
        "coverage": {
            "fixed_commits": 1,
            "author_script_reruns": 1,
            "kernel_calls_certificate": original.get("kernel_calls"),
            "direction_calls_certificate": original.get("direction_calls"),
            "q_lock_forms": 3,
            "conditional_slices": 6,
            "feasible_endpoints": 2,
            "log_terms": 4,
        },
        "noncoverage": [
            "The float scout in locked_probe.py was read for provenance but was not rerun as proof-bearing evidence.",
            "The audit covers only the exact rational K,D certificate at the frozen commit.",
            "The result disproves max Qlock >= C dominance only; it retains F >= Qlock and does not decide B0/N3.",
        ],
        "elapsed_seconds": time.time() - start,
        "exit_status": 0 if status == "PASS" else 1,
    }
    output = out_dir / "locked_obstruction_audit_results.json"
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": status,
        "target_commit": TARGET_COMMIT,
        "pid": os.getpid(),
        "author_rerun_pid": rerun.get("pid"),
        "author_rerun_exit_status": proc.returncode,
        "max_Qlock_minus_C": exact_audit["interval_log_comparison"]["max_Qlock_minus_C"],
        "actual_B": exact_audit["interval_log_comparison"]["actual_B"],
        "coverage": result["coverage"],
        "output": str(output.relative_to(repo_root())),
    }))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
