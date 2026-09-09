#!/usr/bin/env python3
"""Independent exact review checker for PR43 task D / PR47 issue45.

This script intentionally does not import the candidate verifier or reuse its
linear system.  It recomputes the finite DPP law, the matrices G(T), the
directed flow generator, and the density-adjoint eigen-equations from the
literal task input.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import platform
import subprocess
import sys
import time
from fractions import Fraction
from pathlib import Path
from typing import Any


LOCAL_FROZEN_COMMIT = "f249f897c212e49e66ec62a34fba715c47b9bce5"
PUBLIC_PR47_COMMIT = "d1c64ef49c7055df42a496d736742d4fb9aaa904"
UPSTREAM_PR43_COMMIT = "4e1369ef2a59ccfaba3ca8fce95d85e78857bf78"
TASK_FILE = "CODEX_VERIFICATION_TASKS_v2.md:D"

C_LITERAL = [
    ["1/2", "1/12", "1/15"],
    ["1/12", "2/5", "1/20"],
    ["1/15", "1/20", "3/5"],
]

V_LITERAL = [
    ["1", "0"],
    ["0", "1"],
    ["1", "1"],
]

STATE_ORDER = ["000", "001", "010", "011", "100", "101", "110", "111"]
FEATURES = ["G11", "G12", "G22", "d"]
LAMBDA = {"G11": Fraction(1), "G12": Fraction(1), "G22": Fraction(1), "d": Fraction(2)}


def parse_q(value: object) -> Fraction:
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int):
        return Fraction(value, 1)
    if isinstance(value, str):
        return Fraction(value)
    raise TypeError(f"cannot parse rational value {value!r}")


def qstr(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def qmat(data: list[list[str]]) -> list[list[Fraction]]:
    return [[parse_q(entry) for entry in row] for row in data]


def det(matrix: list[list[Fraction]]) -> Fraction:
    n = len(matrix)
    if n == 0:
        return Fraction(1)
    a = [row[:] for row in matrix]
    sign = 1
    out = Fraction(1)
    for col in range(n):
        pivot = None
        for row in range(col, n):
            if a[row][col] != 0:
                pivot = row
                break
        if pivot is None:
            return Fraction(0)
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            sign *= -1
        pivot_value = a[col][col]
        out *= pivot_value
        for row in range(col + 1, n):
            factor = a[row][col] / pivot_value
            if factor == 0:
                continue
            for k in range(col, n):
                a[row][k] -= factor * a[col][k]
    return out * sign


def inverse(matrix: list[list[Fraction]]) -> list[list[Fraction]]:
    n = len(matrix)
    a = [row[:] + [Fraction(int(i == j), 1) for j in range(n)] for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = None
        for row in range(col, n):
            if a[row][col] != 0:
                pivot = row
                break
        if pivot is None:
            raise ZeroDivisionError("singular matrix")
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
        pivot_value = a[col][col]
        for k in range(2 * n):
            a[col][k] /= pivot_value
        for row in range(n):
            if row == col:
                continue
            factor = a[row][col]
            if factor == 0:
                continue
            for k in range(2 * n):
                a[row][k] -= factor * a[col][k]
    return [row[n:] for row in a]


def transpose(matrix: list[list[Fraction]]) -> list[list[Fraction]]:
    return [list(row) for row in zip(*matrix)]


def matmul(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    rows = len(a)
    cols = len(b[0])
    mid = len(b)
    return [[sum(a[i][k] * b[k][j] for k in range(mid)) for j in range(cols)] for i in range(rows)]


def submatrix(matrix: list[list[Fraction]], subset: tuple[int, ...]) -> list[list[Fraction]]:
    return [[matrix[i][j] for j in subset] for i in subset]


def all_subsets(n: int) -> list[tuple[int, ...]]:
    out: list[tuple[int, ...]] = []
    for mask in range(1 << n):
        out.append(tuple(i for i in range(n) if (mask >> i) & 1))
    return out


def state_to_subset(state: str) -> tuple[int, ...]:
    if len(state) != 3 or any(ch not in "01" for ch in state):
        raise ValueError(f"bad state string {state!r}")
    # State strings are b3 b2 b1; the rightmost bit is coordinate 1.
    coords = []
    if state[2] == "1":
        coords.append(0)
    if state[1] == "1":
        coords.append(1)
    if state[0] == "1":
        coords.append(2)
    return tuple(coords)


def subset_to_state(subset: tuple[int, ...]) -> str:
    bits = ["0", "0", "0"]
    for coord in subset:
        bits[2 - coord] = "1"
    return "".join(bits)


def principal_minors(matrix: list[list[Fraction]]) -> dict[str, str]:
    n = len(matrix)
    out: dict[str, str] = {}
    for subset in all_subsets(n):
        if not subset:
            continue
        key = "{" + ",".join(str(i + 1) for i in subset) + "}"
        out[key] = qstr(det(submatrix(matrix, subset)))
    return out


def compute_mu(c: list[list[Fraction]]) -> tuple[dict[str, Fraction], dict[str, Fraction]]:
    inclusion_dets: dict[tuple[int, ...], Fraction] = {}
    for subset in all_subsets(3):
        inclusion_dets[subset] = det(submatrix(c, subset))

    mu: dict[str, Fraction] = {}
    for subset in all_subsets(3):
        total = Fraction(0)
        set_subset = set(subset)
        for superset, inc_det in inclusion_dets.items():
            if set_subset.issubset(superset):
                sign = -1 if (len(superset) - len(subset)) % 2 else 1
                total += sign * inc_det
        mu[subset_to_state(subset)] = total
    inclusion_by_state = {subset_to_state(subset): value for subset, value in inclusion_dets.items()}
    return mu, inclusion_by_state


def compute_g_features(c: list[list[Fraction]], v: list[list[Fraction]]) -> tuple[dict[str, list[list[Fraction]]], dict[str, Fraction], dict[str, Fraction]]:
    vt = transpose(v)
    g_by_state: dict[str, list[list[Fraction]]] = {}
    matrix_dets: dict[str, Fraction] = {}
    det_g: dict[str, Fraction] = {}
    for state in STATE_ORDER:
        occupied = set(state_to_subset(state))
        m = [row[:] for row in c]
        for i in range(3):
            if i not in occupied:
                m[i][i] -= 1
        matrix_dets[state] = det(m)
        inv_m = inverse(m)
        g = matmul(matmul(vt, inv_m), v)
        g_by_state[state] = g
        det_g[state] = det(g)
    return g_by_state, det_g, matrix_dets


def feature_maps(g_by_state: dict[str, list[list[Fraction]]], det_g: dict[str, Fraction]) -> dict[str, dict[str, Fraction]]:
    return {
        "G11": {state: g_by_state[state][0][0] for state in STATE_ORDER},
        "G12": {state: g_by_state[state][0][1] for state in STATE_ORDER},
        "G22": {state: g_by_state[state][1][1] for state in STATE_ORDER},
        "d": {state: det_g[state] for state in STATE_ORDER},
    }


def expected_flow_keys() -> list[str]:
    return [f"r_{x}_{y}" for x in STATE_ORDER for y in STATE_ORDER if x != y]


def parse_flow(flow_data: dict[str, object]) -> dict[tuple[str, str], Fraction]:
    return {
        (key[2:5], key[6:9]): parse_q(value)
        for key, value in flow_data.items()
    }


def safe_git(repo_root: Path, args: list[str]) -> str | None:
    try:
        proc = subprocess.run(
            ["git", "-C", str(repo_root), *args],
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except Exception:
        return None
    if proc.returncode != 0:
        return None
    return proc.stdout.strip()


def maybe_compare_instance(instance_path: Path | None, mu: dict[str, Fraction], g_by_state: dict[str, list[list[Fraction]]], det_g: dict[str, Fraction], features: dict[str, dict[str, Fraction]]) -> dict[str, Any]:
    if instance_path is None:
        return {"provided": False}
    instance = json.loads(instance_path.read_text(encoding="utf-8"))
    checks: dict[str, bool] = {}
    checks["state_order_matches"] = instance.get("state_order") == STATE_ORDER
    checks["c_matches_task_literal"] = instance.get("C") == C_LITERAL
    checks["v_matches_task_literal"] = instance.get("V") == V_LITERAL
    checks["variables_match_ordered_edges"] = instance.get("variables") == expected_flow_keys()

    instance_mu = {state: parse_q(value) for state, value in instance.get("mu", {}).items()}
    checks["mu_matches_recomputed"] = instance_mu == mu

    instance_det_g = {state: parse_q(value) for state, value in instance.get("detG", {}).items()}
    checks["detG_matches_recomputed"] = instance_det_g == det_g

    g_ok = True
    for state in STATE_ORDER:
        raw = instance.get("G", {}).get(state)
        if raw is None:
            g_ok = False
            break
        parsed = [[parse_q(raw[i][j]) for j in range(2)] for i in range(2)]
        if parsed != g_by_state[state]:
            g_ok = False
            break
    checks["G_matches_recomputed"] = g_ok

    feature_name_map = {"G11": "G11", "G12": "G12", "G22": "G22", "detG": "d"}
    features_ok = True
    for instance_name, local_name in feature_name_map.items():
        raw_map = instance.get("features", {}).get(instance_name)
        if raw_map is None:
            features_ok = False
            break
        parsed_map = {state: parse_q(value) for state, value in raw_map.items()}
        if parsed_map != features[local_name]:
            features_ok = False
            break
    checks["features_match_recomputed"] = features_ok
    return {
        "provided": True,
        "path": str(instance_path),
        "checks": checks,
        "all_checks_pass": all(checks.values()),
    }


def validate(certificate_path: Path, instance_path: Path | None, repo_root: Path | None, output_dir: Path) -> tuple[dict[str, Any], bool]:
    start_monotonic = time.monotonic()
    start_utc = _dt.datetime.now(_dt.timezone.utc)
    output_dir.mkdir(parents=True, exist_ok=True)

    c = qmat(C_LITERAL)
    v = qmat(V_LITERAL)
    i_minus_c = [[Fraction(int(i == j), 1) - c[i][j] for j in range(3)] for i in range(3)]

    cert = json.loads(certificate_path.read_text(encoding="utf-8"))
    cert_flow_raw = cert.get("flow")
    if not isinstance(cert_flow_raw, dict):
        raise ValueError("certificate has no object-valued flow field")

    failures: list[str] = []
    expected_keys = expected_flow_keys()
    supplied_keys = list(cert_flow_raw.keys())
    supplied_key_set = set(supplied_keys)
    missing_keys = [key for key in expected_keys if key not in supplied_key_set]
    extra_keys = [key for key in supplied_keys if key not in set(expected_keys)]
    if missing_keys:
        failures.append(f"missing flow keys: {missing_keys}")
    if extra_keys:
        failures.append(f"extra flow keys: {extra_keys}")
    if supplied_keys != expected_keys:
        failures.append("flow keys are not exactly in canonical ordered-edge order")

    flow = parse_flow(cert_flow_raw)
    nonnegative = all(value >= 0 for value in flow.values())
    if not nonnegative:
        failures.append("at least one directed flow entry is negative")

    cert_nonzero_raw = cert.get("nonzero_flow")
    nonzero_check: dict[str, Any]
    if isinstance(cert_nonzero_raw, dict):
        positive_entries = {key: value for key, value in cert_flow_raw.items() if parse_q(value) > 0}
        nonzero_check = {
            "provided": True,
            "matches_positive_entries": cert_nonzero_raw == positive_entries,
            "positive_entry_count": len(positive_entries),
        }
        if not nonzero_check["matches_positive_entries"]:
            failures.append("nonzero_flow does not equal the positive entries of flow")
    else:
        nonzero_check = {"provided": False}

    c_minors = principal_minors(c)
    ic_minors = principal_minors(i_minus_c)
    strict_c = all(parse_q(value) > 0 for value in c_minors.values())
    strict_i_minus_c = all(parse_q(value) > 0 for value in ic_minors.values())
    if not strict_c:
        failures.append("C is not certified positive definite by principal minors")
    if not strict_i_minus_c:
        failures.append("I-C is not certified positive definite by principal minors")

    mu, inclusion_dets = compute_mu(c)
    mu_sum = sum(mu.values(), Fraction(0))
    mu_positive = all(mu[state] > 0 for state in STATE_ORDER)
    if mu_sum != 1:
        failures.append(f"mu sum is {qstr(mu_sum)}, not 1")
    if not mu_positive:
        failures.append("at least one full-event probability mu(T) is nonpositive")

    g_by_state, det_g, c_minus_e_dets = compute_g_features(c, v)
    features = feature_maps(g_by_state, det_g)

    balances: dict[str, dict[str, Fraction]] = {}
    for state in STATE_ORDER:
        outgoing = sum(flow[(state, y)] for y in STATE_ORDER if y != state)
        incoming = sum(flow[(x, state)] for x in STATE_ORDER if x != state)
        residual = outgoing - incoming
        balances[state] = {"outgoing": outgoing, "incoming": incoming, "residual": residual}
        if residual != 0:
            failures.append(f"balance residual at {state} is {qstr(residual)}")

    q: dict[str, dict[str, Fraction]] = {state: {} for state in STATE_ORDER}
    for x in STATE_ORDER:
        for y in STATE_ORDER:
            if x == y:
                continue
            q[x][y] = flow[(x, y)] / mu[x]
        q[x][x] = -sum(q[x][y] for y in STATE_ORDER if y != x)

    q_offdiag_nonnegative = all(q[x][y] >= 0 for x in STATE_ORDER for y in STATE_ORDER if x != y)
    q_row_sums = {x: sum(q[x][y] for y in STATE_ORDER) for x in STATE_ORDER}
    q_rows_zero = all(value == 0 for value in q_row_sums.values())
    mu_q = {
        y: sum(mu[x] * q[x][y] for x in STATE_ORDER)
        for y in STATE_ORDER
    }
    mu_stationary = all(value == 0 for value in mu_q.values())
    if not q_offdiag_nonnegative:
        failures.append("Q has a negative off-diagonal entry")
    if not q_rows_zero:
        failures.append("Q row sums are not all zero")
    if not mu_stationary:
        failures.append("mu Q is not zero")

    density_adjoint: dict[str, dict[str, Fraction]] = {}
    feature_equations: dict[str, dict[str, dict[str, Fraction]]] = {}
    for feature in FEATURES:
        density_adjoint[feature] = {}
        feature_equations[feature] = {}
        fmap = features[feature]
        lam = LAMBDA[feature]
        for y in STATE_ORDER:
            adjoint_value = sum(q[x][y] * mu[x] * fmap[x] for x in STATE_ORDER) / mu[y]
            flow_lhs = sum(flow[(x, y)] * (fmap[x] - fmap[y]) for x in STATE_ORDER if x != y)
            flow_rhs = -lam * mu[y] * fmap[y]
            residual = flow_lhs - flow_rhs
            eigen_residual = adjoint_value - (-lam * fmap[y])
            density_adjoint[feature][y] = adjoint_value
            feature_equations[feature][y] = {
                "flow_lhs": flow_lhs,
                "flow_rhs": flow_rhs,
                "flow_residual": residual,
                "density_adjoint_value": adjoint_value,
                "target_value": -lam * fmap[y],
                "density_adjoint_residual": eigen_residual,
            }
            if residual != 0:
                failures.append(f"{feature} flow equation residual at {y} is {qstr(residual)}")
            if eigen_residual != 0:
                failures.append(f"{feature} density-adjoint eigen residual at {y} is {qstr(eigen_residual)}")

    asymmetry = None
    for x in STATE_ORDER:
        for y in STATE_ORDER:
            if x >= y:
                continue
            if flow[(x, y)] != flow[(y, x)]:
                asymmetry = {
                    "x": x,
                    "y": y,
                    "r_xy": flow[(x, y)],
                    "r_yx": flow[(y, x)],
                    "difference_r_xy_minus_r_yx": flow[(x, y)] - flow[(y, x)],
                }
                break
        if asymmetry is not None:
            break

    if asymmetry is None:
        failures.append("no asymmetric directed edge pair was found")

    instance_comparison = maybe_compare_instance(instance_path, mu, g_by_state, det_g, features)
    if instance_comparison.get("provided") and not instance_comparison.get("all_checks_pass"):
        failures.append("optional instance.json comparison failed")

    repo_metadata: dict[str, Any] = {}
    if repo_root is not None:
        repo_metadata["head"] = safe_git(repo_root, ["rev-parse", "HEAD"])
        repo_metadata["local_frozen_commit_present"] = safe_git(repo_root, ["cat-file", "-t", LOCAL_FROZEN_COMMIT]) == "commit"
        repo_metadata["public_pr47_commit_present_in_local_checkout"] = safe_git(repo_root, ["cat-file", "-t", PUBLIC_PR47_COMMIT]) == "commit"
        repo_metadata["status_short"] = safe_git(repo_root, ["status", "--short"])

    elapsed_seconds = time.monotonic() - start_monotonic
    constraint_count = 8 + 4 * 8
    all_exact_constraints_zero = (
        all(row["residual"] == 0 for row in balances.values())
        and all(
            feature_equations[feature][state]["flow_residual"] == 0
            and feature_equations[feature][state]["density_adjoint_residual"] == 0
            for feature in FEATURES
            for state in STATE_ORDER
        )
    )
    pass_status = len(failures) == 0

    evidence = {
        "verdict": "CORRECT_WITH_SCOPE" if pass_status else "CRITICAL_GAPS",
        "scope": "Exact verification of the PR43 task D directed stationary flow certificate only; no entropy curvature, concavity, or novelty claim is certified.",
        "bindings": {
            "public_pr47_source_commit_from_handoff": PUBLIC_PR47_COMMIT,
            "local_frozen_candidate_commit_actually_checked": LOCAL_FROZEN_COMMIT,
            "upstream_pr43_task_commit": UPSTREAM_PR43_COMMIT,
            "task": TASK_FILE,
            "certificate_path": str(certificate_path),
            "instance_path": str(instance_path) if instance_path is not None else None,
        },
        "run": {
            "started_at_utc": start_utc.isoformat(),
            "finished_at_utc": _dt.datetime.now(_dt.timezone.utc).isoformat(),
            "elapsed_seconds": elapsed_seconds,
            "pid": os.getpid(),
            "python": sys.version,
            "platform": platform.platform(),
            "thread_limits": {
                "OMP_NUM_THREADS": os.environ.get("OMP_NUM_THREADS"),
                "OPENBLAS_NUM_THREADS": os.environ.get("OPENBLAS_NUM_THREADS"),
                "MKL_NUM_THREADS": os.environ.get("MKL_NUM_THREADS"),
                "NUMEXPR_NUM_THREADS": os.environ.get("NUMEXPR_NUM_THREADS"),
            },
        },
        "repo_metadata": repo_metadata,
        "input": {
            "C": C_LITERAL,
            "V": V_LITERAL,
            "state_order": STATE_ORDER,
            "bit_to_coordinate_convention": {
                "state_string": "b3b2b1",
                "rightmost_bit_b1": "coordinate_1",
                "b2": "coordinate_2",
                "leftmost_bit_b3": "coordinate_3",
                "example": "001 occupies coordinate_1 only",
            },
        },
        "strict_kernel_checks": {
            "C_principal_minors": c_minors,
            "I_minus_C_principal_minors": ic_minors,
            "C_positive_definite": strict_c,
            "I_minus_C_positive_definite": strict_i_minus_c,
        },
        "mobius_full_event_law": {
            "inclusion_determinants": {state: qstr(value) for state, value in inclusion_dets.items()},
            "mu": {state: qstr(mu[state]) for state in STATE_ORDER},
            "sum_mu": qstr(mu_sum),
            "all_mu_positive": mu_positive,
        },
        "computed_G": {
            state: [[qstr(entry) for entry in row] for row in g_by_state[state]]
            for state in STATE_ORDER
        },
        "det_C_minus_E_Tc": {state: qstr(c_minus_e_dets[state]) for state in STATE_ORDER},
        "features": {
            feature: {state: qstr(features[feature][state]) for state in STATE_ORDER}
            for feature in FEATURES
        },
        "flow": {
            f"r_{x}_{y}": qstr(flow[(x, y)])
            for x in STATE_ORDER
            for y in STATE_ORDER
            if x != y
        },
        "flow_key_check": {
            "expected_key_count": len(expected_keys),
            "supplied_key_count": len(supplied_keys),
            "exact_order_match": supplied_keys == expected_keys,
            "missing_keys": missing_keys,
            "extra_keys": extra_keys,
            "all_entries_nonnegative": nonnegative,
            "nonzero_flow_field": nonzero_check,
        },
        "q_generator": {
            x: {y: qstr(q[x][y]) for y in STATE_ORDER}
            for x in STATE_ORDER
        },
        "stationary_generator_checks": {
            "off_diagonal_nonnegative": q_offdiag_nonnegative,
            "row_sums": {state: qstr(q_row_sums[state]) for state in STATE_ORDER},
            "all_row_sums_zero": q_rows_zero,
            "mu_Q": {state: qstr(mu_q[state]) for state in STATE_ORDER},
            "mu_stationary": mu_stationary,
            "finite_generator_semigroup_basis": "Off-diagonal rates are nonnegative and row sums are zero, so Q is a finite continuous-time Markov generator. The exact identity mu Q = 0 makes mu stationary for exp(tQ).",
        },
        "constraints": {
            "total_constraint_count": constraint_count,
            "balance_constraint_count": 8,
            "feature_constraint_count": 32,
            "all_exact_residuals_zero": all_exact_constraints_zero,
            "balance": {
                state: {key: qstr(value) for key, value in balances[state].items()}
                for state in STATE_ORDER
            },
            "feature_equations": {
                feature: {
                    state: {key: qstr(value) for key, value in feature_equations[feature][state].items()}
                    for state in STATE_ORDER
                }
                for feature in FEATURES
            },
        },
        "orientation_check": {
            "method": "Direct density adjoint diag(mu)^-1 Q^T diag(mu), independently of stored A,b.",
            "eigenvalues": {"G11": "-1", "G12": "-1", "G22": "-1", "d": "-2"},
            "density_adjoint_values": {
                feature: {state: qstr(density_adjoint[feature][state]) for state in STATE_ORDER}
                for feature in FEATURES
            },
            "all_density_adjoint_eigen_residuals_zero": all(
                feature_equations[feature][state]["density_adjoint_residual"] == 0
                for feature in FEATURES
                for state in STATE_ORDER
            ),
        },
        "asymmetry_certificate": (
            {key: qstr(value) if isinstance(value, Fraction) else value for key, value in asymmetry.items()}
            if asymmetry is not None
            else None
        ),
        "optional_instance_comparison": instance_comparison,
        "failures": failures,
    }
    return evidence, pass_status


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, required=True)
    parser.add_argument("--instance", type=Path)
    parser.add_argument("--repo-root", type=Path)
    parser.add_argument("--output-dir", type=Path, default=Path("."))
    parser.add_argument("--evidence-name", default="evidence.json")
    parser.add_argument("--metadata-name", default="run_metadata.json")
    args = parser.parse_args()

    evidence, pass_status = validate(args.certificate, args.instance, args.repo_root, args.output_dir)
    evidence_path = args.output_dir / args.evidence_name
    evidence_path.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    metadata = {
        "verdict": evidence["verdict"],
        "pid": os.getpid(),
        "argv": sys.argv,
        "evidence_path": str(evidence_path),
        "exit_code": 0 if pass_status else 1,
        "note": "Single-thread exact rational run; no LP resolve/search performed.",
    }
    metadata_path = args.output_dir / args.metadata_name
    metadata_path.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(evidence["verdict"])
    print(f"evidence={evidence_path}")
    if not pass_status:
        for failure in evidence["failures"]:
            print(f"failure: {failure}", file=sys.stderr)
    return 0 if pass_status else 1


if __name__ == "__main__":
    raise SystemExit(main())
