#!/usr/bin/env python3
"""Bounded audit for the sign-shortcut obstruction and locked-odds degeneracy note."""

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

from verify_round2_definitions import COORDS, SUBSETS, det3, event_first_jacobian, events, ray
from verify_beta_root_certificate import LAMBDA_SIGNS, principal_minors_positive, q_to_mpf


SIGN_COMMIT = "2af6538"
LOCKED_LEMMA_COMMIT = "99205d9ac552355c148f011bb053731a8b1349f0"
DEGENERACY_COMMIT = "0b6c89ef15db01385a37302e78509e0203838a74"
SIGN_DOC = "research/N3/round2/main/lambda_tangent_sign_obstruction_v1.md"
SIGN_SCRIPT = "research/N3/round2/main/lambda_tangent_certificate.py"
SIGN_JSON = "research/N3/round2/main/lambda_tangent_certificate.json"
LOCKED_LEMMA_DOC = "research/N3/round2/inequality/lambda_tangent_locked_odds_lemma.md"
DEGENERACY_DOC = "research/N3/round2/inequality/locked_odds_degeneracy_addendum.md"


def repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def review_dir() -> Path:
    return Path(__file__).resolve().parent


def git_bytes(commit: str, path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=repo_root())


def git_text(commit: str, path: str) -> str:
    return git_bytes(commit, path).decode("utf-8")


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def list_tree(commit: str, prefix: str) -> list[str]:
    out = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", commit, "--", prefix], cwd=repo_root(), text=True)
    return [line for line in out.splitlines() if line.strip()]


def write_sign_tree(root: Path) -> dict[str, str]:
    paths = sorted(
        set(
            list_tree(SIGN_COMMIT, "research/N3/main")
            + list_tree(SIGN_COMMIT, "research/N3/round2/main")
            + [
                "research/R3/deepening_10h/dense_hessian/n3_global_full_hessian/rank_one_recheck.py",
                "research/R3/deepening_10h/dense_hessian/n3_global_full_hessian/global_probe.py",
            ]
        )
    )
    hashes: dict[str, str] = {}
    for rel in paths:
        data = git_bytes(SIGN_COMMIT, rel)
        dst = root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(data)
        hashes[rel] = hashlib.sha256(data).hexdigest()
    return hashes


def parse_matrix(rows: list[list[str]]) -> list[list[Q]]:
    return [[Q(x) for x in row] for row in rows]


def parse_vector(row: list[str]) -> list[Q]:
    return [Q(x) for x in row]


def coeffs_from_values(vals: dict[int, Q]) -> list[Q]:
    """Cubic coefficients from values at 0,1,-1,2."""
    c0 = vals[0]
    y1 = vals[1] - c0
    ym1 = vals[-1] - c0
    y2 = vals[2] - c0
    c2 = (y1 + ym1) / 2
    c1_plus_c3 = (y1 - ym1) / 2
    c3 = (y2 - 2 * c1_plus_c3 - 4 * c2) / 6
    c1 = c1_plus_c3 - c3
    return [c0, c1, c2, c3]


def event_second_derivative_along(K: list[list[Q]], D: list[list[Q]]) -> list[Q]:
    rows: list[Q] = []
    for subset in SUBSETS:
        vals = {t: events(ray(K, D, Q(t)))[subset] for t in [0, 1, -1, 2]}
        coeff = coeffs_from_values(vals)
        rows.append(2 * coeff[2])
    return rows


def cofactor_interval_with_log_bounds(log_bounds, K: list[list[Q]], dvec: list[Q]) -> tuple[Q, Q]:
    D = [[dvec[0], dvec[3], dvec[4]], [dvec[3], dvec[1], dvec[5]], [dvec[4], dvec[5], dvec[2]]]
    p = events(K)
    ddp = event_second_derivative_along(K, D)
    lo = Q(0)
    hi = Q(0)
    for prob, acc in zip([p[S] for S in SUBSETS], ddp):
        l, h = log_bounds(prob)
        coef = -acc
        lo += coef * (l if coef >= 0 else h)
        hi += coef * (h if coef >= 0 else l)
    return lo, hi


def sign_independent_audit(cert_mod, original: dict[str, Any]) -> dict[str, Any]:
    K = parse_matrix(original["K"])
    dvec = parse_vector(original["direction"])
    D = [[dvec[0], dvec[3], dvec[4]], [dvec[3], dvec[1], dvec[5]], [dvec[4], dvec[5], dvec[2]]]
    p, J = event_first_jacobian(K)
    grad = [
        sum(Q(LAMBDA_SIGNS[S]) * J[SUBSETS.index(S)][j] / p[S] for S in SUBSETS)
        for j in range(6)
    ]
    dp = [sum(J[SUBSETS.index(S)][j] * dvec[j] for j in range(6)) for S in SUBSETS]
    fisher = sum(dp[i] * dp[i] / p[S] for i, S in enumerate(SUBSETS))
    clo, chi = cofactor_interval_with_log_bounds(cert_mod.log_bounds, K, dvec)
    true_B_lo = fisher - chi
    true_B_hi = fisher - clo

    def poly_mul(a: list[Q], b: list[Q]) -> list[Q]:
        out = [Q(0)] * (len(a) + len(b) - 1)
        for i, u in enumerate(a):
            for j, v in enumerate(b):
                out[i + j] += u * v
        return out

    def poly_add(a: list[Q], b: list[Q]) -> list[Q]:
        out = [Q(0)] * max(len(a), len(b))
        for i, v in enumerate(a):
            out[i] += v
        for i, v in enumerate(b):
            out[i] += v
        return out

    square_rows = []
    for i, j in COORDS[3:]:
        k = 3 - i - j
        a = [K[i][j], dvec[COORDS.index((min(i, j), max(i, j)))]]
        b = [K[i][k], dvec[COORDS.index((min(i, k), max(i, k)))]]
        c = [K[j][k], dvec[COORDS.index((min(j, k), max(j, k)))]]
        diag = [K[k][k], dvec[k]]
        intercept = poly_add(poly_mul(a, diag), [-v for v in poly_mul(b, c)])
        square_rows.append(
            {
                "pair": [i, j],
                "root_z_coefficient": [str(x) for x in a],
                "root_constant": [str(x) for x in intercept],
                "z2_coeff": [str(x) for x in poly_mul(a, a)],
                "z1_coeff": [str(2 * x) for x in poly_mul(a, intercept)],
                "z0_coeff": [str(x) for x in poly_mul(intercept, intercept)],
            }
        )

    I3 = [[Q(int(i == j)) for j in range(3)] for i in range(3)]
    IK = [[I3[i][j] - K[i][j] for j in range(3)] for i in range(3)]
    log_checks = []
    for prob in p.values():
        l, h = cert_mod.log_bounds(prob)
        exact = mp.log(q_to_mpf(prob))
        log_checks.append(q_to_mpf(l) <= exact <= q_to_mpf(h))
    return {
        "strict_K_and_I_minus_K": principal_minors_positive(K) and principal_minors_positive(IK),
        "all_edges_nonzero": K[0][1] != 0 and K[0][2] != 0 and K[1][2] != 0,
        "lambda_derivative": str(sum(grad[i] * dvec[i] for i in range(6))),
        "lambda_tangent_exact": sum(grad[i] * dvec[i] for i in range(6)) == 0,
        "fisher_matches_certificate": str(fisher) == original["Fisher"],
        "cofactor_interval": [str(clo), str(chi)],
        "cofactor_positive": clo > 0,
        "true_B_interval": [str(true_B_lo), str(true_B_hi)],
        "true_B_positive": true_B_lo > 0,
        "rayleigh_square_coefficients_match_certificate": square_rows == original["rayleigh_squares"],
        "log_bounds_contain_high_precision_logs": all(log_checks),
    }


def compare_sign_fields(original: dict[str, Any], rerun: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "status",
        "K",
        "direction",
        "Lambda_direction_derivative",
        "Fisher",
        "cofactor_interval",
        "true_B_interval",
        "rayleigh_squares",
    ]
    mismatches = [key for key in keys if original.get(key) != rerun.get(key)]
    return {"critical_fields_match": not mismatches, "mismatches": mismatches, "keys_checked": keys}


def degeneracy_audit() -> dict[str, Any]:
    a = Q(3)
    b = Q(1)
    c = Q(1)
    d = Q(3)
    x = [a, b, c, d]
    m = sum(x)
    delta = a * d - b * c
    g = [d - 2 * delta / m, -c - 2 * delta / m, -b - 2 * delta / m, a - 2 * delta / m]
    psi = [1 / a, -1 / b, -1 / c, 1 / d]
    V = sum(x[i] * g[i] * g[i] for i in range(4))
    W = sum(x[i] * psi[i] * psi[i] for i in range(4))
    R = W - m * m / V
    scalar = m / V
    psi_projection = [scalar * g[i] for i in range(4)]
    # A concrete centered probability tangent.
    dotx = [Q(1), Q(-2), Q(1), Q(0)]
    dotm = sum(dotx)
    centered_probability = [dotx[i] - x[i] * dotm / m for i in range(4)]
    score = [dotx[i] / x[i] - dotm / m for i in range(4)]
    ordinary_L = sum(g[i] * centered_probability[i] for i in range(4))
    fisher_L = sum(x[i] * g[i] * score[i] for i in range(4))
    ordinary_E = sum(psi[i] * centered_probability[i] for i in range(4))
    fisher_E = sum(x[i] * psi[i] * score[i] for i in range(4))
    return {
        "example": "a=d=3,b=c=1",
        "delta": str(delta),
        "R": str(R),
        "R_zero_with_nonzero_delta": R == 0 and delta != 0,
        "psi_equals_m_over_V_times_g": psi == psi_projection,
        "E_equals_mL_over_V": ordinary_E == scalar * ordinary_L,
        "ordinary_pairing_L": str(ordinary_L),
        "fisher_pairing_same_value_after_score_conversion": str(fisher_L),
        "ordinary_pairing_E": str(ordinary_E),
        "fisher_pairing_E_after_score_conversion": str(fisher_E),
        "pairing_note": "L=<g,dot x-x dot m/m> is an ordinary pairing on probability tangents; Fisher inner products use score s=dot x/x-dot m/m and x-weights.",
        "two_slice_zero_over_zero_convention": "If R0+R1=0 and Lambda lock holds, addendum forces A0=A1 and defines the extra locked term as 0; it does not claim a path-independent limiting value.",
    }


def main() -> int:
    start = time.time()
    mp.mp.dps = 120
    out_dir = review_dir()
    original = json.loads(git_text(SIGN_COMMIT, SIGN_JSON))
    stdout_path = out_dir / "signshortcut_certificate_rerun.stdout.txt"
    stderr_path = out_dir / "signshortcut_certificate_rerun.stderr.txt"
    env = os.environ.copy()
    for key in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"]:
        env[key] = "1"

    with tempfile.TemporaryDirectory(prefix="signshortcut_audit_", dir=out_dir) as tmp_str:
        tmp = Path(tmp_str)
        extracted_hashes = write_sign_tree(tmp)
        proc = subprocess.run(
            [sys.executable, SIGN_SCRIPT],
            cwd=tmp,
            env=env,
            text=True,
            capture_output=True,
            timeout=120,
        )
        stdout_path.write_text(proc.stdout, encoding="utf-8")
        stderr_path.write_text(proc.stderr, encoding="utf-8")
        rerun = json.loads((tmp / SIGN_JSON).read_text(encoding="utf-8"))
        sys.path.insert(0, str(tmp / "research/N3/round2/main"))
        sys.path.insert(0, str(tmp / "research/N3/main"))
        cert_mod = load_module("signshortcut_certify_score_obstruction", tmp / "research/N3/main/certify_score_obstruction.py")
        sign_audit = sign_independent_audit(cert_mod, original)

    comparison = compare_sign_fields(original, rerun)
    degeneracy = degeneracy_audit()
    lemma_text = git_text(LOCKED_LEMMA_COMMIT, LOCKED_LEMMA_DOC)
    addendum_text = git_text(DEGENERACY_COMMIT, DEGENERACY_DOC)
    doc_audit = {
        "locked_lemma_commit": LOCKED_LEMMA_COMMIT,
        "degeneracy_addendum_commit": DEGENERACY_COMMIT,
        "original_lemma_contains_superseded_covariance_root_sentence": "if the covariance root is zero" in lemma_text,
        "addendum_states_R_zero_not_covariance_root_zero": "If `R=0`, it does not follow that the covariance root is zero" in addendum_text,
        "addendum_states_zero_term_not_path_independent_limit": "No claim is made that arbitrary approaches to the degenerate point have a" in addendum_text,
        "addendum_preserves_F_ge_Qlock": "preserves the proven lower bound `F>=Q_k^lock`" in addendum_text,
    }
    required = [
        proc.returncode == 0,
        comparison["critical_fields_match"],
        sign_audit["strict_K_and_I_minus_K"],
        sign_audit["all_edges_nonzero"],
        sign_audit["lambda_tangent_exact"],
        sign_audit["fisher_matches_certificate"],
        sign_audit["cofactor_positive"],
        sign_audit["true_B_positive"],
        sign_audit["rayleigh_square_coefficients_match_certificate"],
        sign_audit["log_bounds_contain_high_precision_logs"],
        degeneracy["R_zero_with_nonzero_delta"],
        degeneracy["psi_equals_m_over_V_times_g"],
        degeneracy["E_equals_mL_over_V"],
        doc_audit["addendum_states_R_zero_not_covariance_root_zero"],
        doc_audit["addendum_states_zero_term_not_path_independent_limit"],
        doc_audit["addendum_preserves_F_ge_Qlock"],
    ]
    status = "PASS" if all(required) else "FAIL"
    result = {
        "status": status,
        "sign_commit": SIGN_COMMIT,
        "locked_lemma_commit": LOCKED_LEMMA_COMMIT,
        "degeneracy_addendum_commit": DEGENERACY_COMMIT,
        "target_blob_sha1": {
            SIGN_DOC: subprocess.check_output(["git", "rev-parse", f"{SIGN_COMMIT}:{SIGN_DOC}"], cwd=repo_root(), text=True).strip(),
            SIGN_SCRIPT: subprocess.check_output(["git", "rev-parse", f"{SIGN_COMMIT}:{SIGN_SCRIPT}"], cwd=repo_root(), text=True).strip(),
            SIGN_JSON: subprocess.check_output(["git", "rev-parse", f"{SIGN_COMMIT}:{SIGN_JSON}"], cwd=repo_root(), text=True).strip(),
            LOCKED_LEMMA_DOC: subprocess.check_output(["git", "rev-parse", f"{LOCKED_LEMMA_COMMIT}:{LOCKED_LEMMA_DOC}"], cwd=repo_root(), text=True).strip(),
            DEGENERACY_DOC: subprocess.check_output(["git", "rev-parse", f"{DEGENERACY_COMMIT}:{DEGENERACY_DOC}"], cwd=repo_root(), text=True).strip(),
        },
        "review_script_sha256": sha256_path(Path(__file__)),
        "python": sys.version,
        "platform": platform.platform(),
        "pid": os.getpid(),
        "thread_env": {key: env.get(key) for key in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"]},
        "sign_author_rerun": {
            "command": [sys.executable, SIGN_SCRIPT],
            "exit_status": proc.returncode,
            "recorded_pid": rerun.get("pid"),
            "status": rerun.get("status"),
            "stdout_path": str(stdout_path.relative_to(repo_root())),
            "stderr_path": str(stderr_path.relative_to(repo_root())),
        },
        "sign_source_hashes": {
            SIGN_SCRIPT: extracted_hashes.get(SIGN_SCRIPT),
            "research/N3/round2/main/beta_probe.py": extracted_hashes.get("research/N3/round2/main/beta_probe.py"),
            "research/N3/main/certify_score_obstruction.py": extracted_hashes.get("research/N3/main/certify_score_obstruction.py"),
        },
        "sign_critical_certificate_comparison": comparison,
        "sign_independent_audit": sign_audit,
        "degeneracy_doc_audit": doc_audit,
        "degeneracy_exact_example": degeneracy,
        "coverage": {
            "sign_fixed_commits": 1,
            "sign_author_script_reruns": 1,
            "sign_event_center_count": 1,
            "sign_rayleigh_pairs": 3,
            "degeneracy_addenda_read": 1,
            "degeneracy_exact_examples": 1,
        },
        "noncoverage": [
            "The signshortcut witness is only an auxiliary shortcut obstruction, not a beta-zero or B0 certificate.",
            "The degeneracy audit checks the stated correction and one exact R=0 example; it is not a full rewrite of the locked-odds lemma.",
        ],
        "elapsed_seconds": time.time() - start,
        "exit_status": 0 if status == "PASS" else 1,
    }
    output = out_dir / "signshortcut_degeneracy_audit_results.json"
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": status,
        "pid": os.getpid(),
        "sign_author_rerun_pid": rerun.get("pid"),
        "sign_author_rerun_exit_status": proc.returncode,
        "sign_true_B_interval": sign_audit["true_B_interval"],
        "degeneracy_R": degeneracy["R"],
        "coverage": result["coverage"],
        "output": str(output.relative_to(repo_root())),
    }))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
