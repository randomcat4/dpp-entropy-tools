#!/usr/bin/env python3
"""Fresh non-author audit for D10-H8 round16_refine4.

This verifier does not import the author recheck, round14 gate, or search
modules.  It independently checks copied ledgers/manifests/logs/JSON/NPZ and
recomputes the strongest stored point with Decimal exact-event Möbius atoms and
Fraction LDL feasibility certificates.
"""

from __future__ import annotations

import csv
import hashlib
import json
import time
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
BASE = HERE.parent
EXPECTED = {
    "source_npz": "21bcb4d8867b2f7d32ee398432dfaa6f2d91976a4a959191d2da4d112153eb71",
    "strongest_npz": "b078c507558faa74b2a583581bfc5b51859009dafd12e6c2b95e6e25cad0b5a2",
    "producing_script": "28ae523c10184dc1effe2f857adbdad4156683292f2ad7da2d281e2af6ad7268",
    "strongest_shard": 2,
    "strongest_index": 4889,
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def parse_bool(value: str) -> bool:
    return value.strip().lower() == "true"


def close_float(a, b, tol=1e-14) -> bool:
    return abs(float(a) - float(b)) <= tol


def best_json_matches_row(best_json, row):
    mismatches = []
    for key, value in best_json.items():
        if key not in row:
            continue
        if isinstance(value, bool):
            ok = parse_bool(row[key]) == value
        elif isinstance(value, int):
            ok = int(row[key]) == value
        elif isinstance(value, float):
            ok = close_float(row[key], value)
        else:
            ok = str(row[key]) == str(value)
        if not ok:
            mismatches.append({"field": key, "ledger": row[key], "json": value})
    return not mismatches, mismatches


def ledger_audit():
    per_shard = []
    all_rows = []
    for shard in range(4):
        shard_dir = BASE / f"results_{shard}"
        ledger_path = shard_dir / "candidate_ledger.csv"
        physical_lines = ledger_path.read_text(encoding="utf-8").splitlines()
        with ledger_path.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        manifest = read_json(shard_dir / "manifest.json")
        best_json = read_json(shard_dir / "best_case.json")
        source_rows = [row for row in rows if int(row["index"]) == -1]
        proposal_rows = [row for row in rows if int(row["index"]) >= 0]
        proposal_indices = [int(row["index"]) for row in proposal_rows]
        accepted_rows = [row for row in proposal_rows if parse_bool(row["accepted"])]
        non_no_hit_rows = [row for row in rows if row["status"] != "NO_HIT"]
        positive_gap_rows = [row for row in rows if float(row["chord_gap"]) > 0.0]
        best_row = max(rows, key=lambda row: float(row["rho_psd"]))
        best_ok, best_mismatches = best_json_matches_row(best_json, best_row)
        run_log = (BASE / f"run_{shard}.log").read_text(encoding="utf-8", errors="replace")
        for row in rows:
            tagged = dict(row)
            tagged["_shard"] = str(shard)
            all_rows.append(tagged)
        per_shard.append(
            {
                "shard": shard,
                "physical_lines_including_header": len(physical_lines),
                "data_rows": len(rows),
                "source_rows": len(source_rows),
                "proposal_rows": len(proposal_rows),
                "proposal_indices_unique_0_to_4999": sorted(proposal_indices) == list(range(5000)),
                "source_index_is_minus_one": len(source_rows) == 1 and source_rows[0]["index"] == "-1",
                "source_label": source_rows[0]["label"] if source_rows else None,
                "manifest_status": manifest.get("status"),
                "manifest_seed": manifest.get("seed"),
                "manifest_proposal_count": manifest.get("proposal_count"),
                "manifest_rows": manifest.get("ledger_rows_including_source"),
                "manifest_positive_count": manifest.get("positive_count"),
                "manifest_accepted_count": manifest.get("accepted_count"),
                "accepted_rows": len(accepted_rows),
                "accepted_count_matches_manifest": len(accepted_rows) == int(manifest["accepted_count"]),
                "manifest_exit_code": manifest.get("exit_code"),
                "manifest_threads": manifest.get("threads"),
                "non_no_hit_rows": len(non_no_hit_rows),
                "positive_gap_rows": len(positive_gap_rows),
                "maximum_gap": max(float(row["chord_gap"]) for row in rows),
                "maximum_gap_proposals": max(float(row["chord_gap"]) for row in proposal_rows),
                "best_row_index": int(best_row["index"]),
                "best_row_label": best_row["label"],
                "best_row_rho_psd": float(best_row["rho_psd"]),
                "best_row_gap": float(best_row["chord_gap"]),
                "best_matches_manifest_rho": close_float(best_row["rho_psd"], manifest["best_rho_psd"]),
                "best_matches_json": best_ok,
                "best_json_mismatches": best_mismatches,
                "best_json_sha256": sha256(shard_dir / "best_case.json"),
                "best_npz_sha256": sha256(shard_dir / "best_case.npz"),
                "run_log_lines": len(run_log.splitlines()),
                "run_log_mentions_seed": str(manifest.get("seed")) in run_log,
            }
        )
    best_by_rho = max(all_rows, key=lambda row: float(row["rho_psd"]))
    return {
        "per_shard": per_shard,
        "aggregate": {
            "data_rows": len(all_rows),
            "source_rows": sum(1 for row in all_rows if int(row["index"]) == -1),
            "proposal_rows": sum(1 for row in all_rows if int(row["index"]) >= 0),
            "non_no_hit_rows": sum(1 for row in all_rows if row["status"] != "NO_HIT"),
            "positive_gap_rows": sum(1 for row in all_rows if float(row["chord_gap"]) > 0.0),
            "maximum_gap_all_rows": max(float(row["chord_gap"]) for row in all_rows),
            "maximum_gap_proposals": max(
                float(row["chord_gap"]) for row in all_rows if int(row["index"]) >= 0
            ),
            "best_shard": int(best_by_rho["_shard"]),
            "best_index": int(best_by_rho["index"]),
            "best_label": best_by_rho["label"],
            "best_rho_psd": float(best_by_rho["rho_psd"]),
            "best_gap": float(best_by_rho["chord_gap"]),
        },
    }


def dec_matrix(matrix: np.ndarray):
    return [[Decimal(repr(float(value))) for value in row] for row in matrix]


def principal(matrix, idx):
    return [[matrix[i][j] for j in idx] for i in idx]


def matmul(A, B):
    n = len(A)
    m = len(B[0])
    kdim = len(B)
    return [[sum(A[i][k] * B[k][j] for k in range(kdim)) for j in range(m)] for i in range(n)]


def dec_det_inverse(matrix_input):
    n = len(matrix_input)
    matrix = [row[:] for row in matrix_input]
    rhs = [[Decimal(int(i == j)) for j in range(n)] for i in range(n)]
    determinant = Decimal(1)
    for column in range(n):
        pivot = max(range(column, n), key=lambda row: abs(matrix[row][column]))
        if matrix[pivot][column] == 0:
            raise ArithmeticError("singular Decimal matrix")
        if pivot != column:
            matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
            rhs[column], rhs[pivot] = rhs[pivot], rhs[column]
            determinant = -determinant
        value = matrix[column][column]
        determinant *= value
        for row in range(column + 1, n):
            factor = matrix[row][column] / value
            matrix[row][column] = Decimal(0)
            for j in range(column + 1, n):
                matrix[row][j] -= factor * matrix[column][j]
            for j in range(n):
                rhs[row][j] -= factor * rhs[column][j]
    inverse = [[Decimal(0) for _ in range(n)] for _ in range(n)]
    for row in range(n - 1, -1, -1):
        for j in range(n):
            tail = sum(matrix[row][k] * inverse[k][j] for k in range(row + 1, n))
            inverse[row][j] = (rhs[row][j] - tail) / matrix[row][row]
    return determinant, inverse


def dec_det(matrix_input):
    n = len(matrix_input)
    if n == 0:
        return Decimal(1)
    matrix = [row[:] for row in matrix_input]
    determinant = Decimal(1)
    for column in range(n):
        pivot = max(range(column, n), key=lambda row: abs(matrix[row][column]))
        if matrix[pivot][column] == 0:
            return Decimal(0)
        if pivot != column:
            matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
            determinant = -determinant
        value = matrix[column][column]
        determinant *= value
        for row in range(column + 1, n):
            factor = matrix[row][column] / value
            matrix[row][column] = Decimal(0)
            for j in range(column + 1, n):
                matrix[row][j] -= factor * matrix[column][j]
    return determinant


def superset_mobius(values, n):
    out = values[:]
    for bit_index in range(n):
        bit = 1 << bit_index
        for mask in range(1 << n):
            if (mask & bit) == 0:
                out[mask] -= out[mask | bit]
    return out


def inclusion_derivatives(K, D):
    n = len(K)
    inc = [Decimal(0) for _ in range(1 << n)]
    inc1 = [Decimal(0) for _ in range(1 << n)]
    inc2 = [Decimal(0) for _ in range(1 << n)]
    inc[0] = Decimal(1)
    for mask in range(1, 1 << n):
        idx = [i for i in range(n) if mask & (1 << i)]
        K_sub = principal(K, idx)
        D_sub = principal(D, idx)
        det, inv = dec_det_inverse(K_sub)
        B = matmul(inv, D_sub)
        tr = sum(B[i][i] for i in range(len(idx)))
        tr2 = sum(B[i][j] * B[j][i] for i in range(len(idx)) for j in range(len(idx)))
        inc[mask] = det
        inc1[mask] = det * tr
        inc2[mask] = det * (tr * tr - tr2)
    return inc, inc1, inc2


def atoms_only(K):
    n = len(K)
    inc = [Decimal(0) for _ in range(1 << n)]
    inc[0] = Decimal(1)
    for mask in range(1, 1 << n):
        idx = [i for i in range(n) if mask & (1 << i)]
        inc[mask] = dec_det(principal(K, idx))
    return superset_mobius(inc, n)


def entropy_from_dec_matrix(K):
    atoms = atoms_only(K)
    if min(atoms) <= 0:
        raise ArithmeticError("nonpositive exact atom")
    entropy = -sum(p * p.ln() for p in atoms)
    return +entropy, +sum(atoms), +min(atoms)


def directional_dec(K_np, D_np, precision):
    with localcontext() as context:
        context.prec = precision
        K = dec_matrix(K_np)
        D = dec_matrix(D_np)
        inc, inc1, inc2 = inclusion_derivatives(K, D)
        p = superset_mobius(inc, len(K))
        p1 = superset_mobius(inc1, len(K))
        p2 = superset_mobius(inc2, len(K))
        if min(p) <= 0:
            raise ArithmeticError("nonpositive exact atom")
        entropy = Decimal(0)
        fisher = Decimal(0)
        acceleration = Decimal(0)
        for prob, first, second in zip(p, p1, p2):
            logp = prob.ln()
            entropy -= prob * logp
            fisher += first * first / prob
            acceleration -= second * logp
        H2 = acceleration - fisher
        return {
            "precision": precision,
            "event_count": len(p),
            "entropy": str(+entropy),
            "fisher": str(+fisher),
            "acceleration": str(+acceleration),
            "H2": str(+H2),
            "rho": str(+(acceleration / fisher)),
            "sum_p": str(+sum(p)),
            "sum_p1": str(+sum(p1)),
            "sum_p2": str(+sum(p2)),
            "min_atom": str(+min(p)),
        }


def chords_dec(K_np, D_np, steps, precision):
    with localcontext() as context:
        context.prec = precision
        K = dec_matrix(K_np)
        D = dec_matrix(D_np)
        center, center_sum, center_min = entropy_from_dec_matrix(K)
        rows = []
        for step_string in steps:
            step = Decimal(step_string)
            K_minus = [[K[i][j] - step * D[i][j] for j in range(len(K))] for i in range(len(K))]
            K_plus = [[K[i][j] + step * D[i][j] for j in range(len(K))] for i in range(len(K))]
            h_minus, sum_minus, min_minus = entropy_from_dec_matrix(K_minus)
            h_plus, sum_plus, min_plus = entropy_from_dec_matrix(K_plus)
            gap = (h_minus + h_plus) / Decimal(2) - center
            rows.append(
                {
                    "step": step_string,
                    "Hminus": str(+h_minus),
                    "Hplus": str(+h_plus),
                    "midpoint_gap": str(+gap),
                    "central_H2": str(+((h_minus + h_plus - Decimal(2) * center) / (step * step))),
                    "sum_minus": str(+sum_minus),
                    "sum_plus": str(+sum_plus),
                    "min_minus": str(+min_minus),
                    "min_plus": str(+min_plus),
                }
            )
        return {
            "precision": precision,
            "center_entropy": str(+center),
            "center_sum": str(+center_sum),
            "center_min": str(+center_min),
            "rows": rows,
        }


def frac_matrix(matrix: np.ndarray):
    return [[Fraction(repr(float(value))) for value in row] for row in matrix]


def ldl_pivots(matrix):
    n = len(matrix)
    lower = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    diag = [Fraction(0) for _ in range(n)]
    for j in range(n):
        value = matrix[j][j] - sum(lower[j][k] * lower[j][k] * diag[k] for k in range(j))
        diag[j] = value
        if value == 0:
            break
        for i in range(j + 1, n):
            lower[i][j] = (
                matrix[i][j] - sum(lower[i][k] * lower[j][k] * diag[k] for k in range(j))
            ) / value
    return diag


def ldl_report(matrix):
    pivots = ldl_pivots(matrix)
    minimum = min(pivots)
    return {
        "count": len(pivots),
        "all_positive": all(p > 0 for p in pivots),
        "minimum_float": float(minimum),
        "minimum_numerator_digits": len(str(abs(minimum.numerator))),
        "minimum_denominator_digits": len(str(minimum.denominator)),
    }


def add_scaled(A, B, scale):
    n = len(A)
    return [[A[i][j] + scale * B[i][j] for j in range(n)] for i in range(n)]


def fraction_feasible(K_np, D_np):
    K = frac_matrix(K_np)
    D = frac_matrix(D_np)
    n = len(K)
    eye = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    radius = Fraction(1, 200)
    margin = Fraction(1, 2000)
    endpoints = []
    for step in (-radius, radius):
        Kt = add_scaled(K, D, step)
        K_margin = add_scaled(Kt, eye, -margin)
        I_minus_K_margin = add_scaled(add_scaled(eye, Kt, Fraction(-1)), eye, -margin)
        endpoints.append(
            {
                "step": str(step),
                "K_minus_margin_I": ldl_report(K_margin),
                "I_minus_K_minus_margin_I": ldl_report(I_minus_K_margin),
            }
        )
    return {
        "interpretation": "symmetrized float entries interpreted as exact repr(float) rationals",
        "uniform_interval": [str(-radius), str(radius)],
        "strict_spectral_margin": str(margin),
        "D_positive_definite": ldl_report(D),
        "endpoint_LDL": endpoints,
    }


def strongest_arrays(shard):
    data = np.load(BASE / f"results_{shard}" / "best_case.npz")
    raw_K = np.asarray(data["kernel"], dtype=float)
    raw_D = np.asarray(data["direction"], dtype=float)
    K = (raw_K + raw_K.T) / 2.0
    D = (raw_D + raw_D.T) / 2.0
    return raw_K, raw_D, K, D


def audit():
    started = time.time()
    ledger = ledger_audit()
    author = read_json(BASE / "recheck_best_refine4.json")
    strongest_shard = EXPECTED["strongest_shard"]
    best_json = read_json(BASE / f"results_{strongest_shard}" / "best_case.json")
    raw_K, raw_D, K, D = strongest_arrays(strongest_shard)
    steps = [str(best_json["chord_step"]), "0.001", "0.0001"]
    decimal_90 = directional_dec(K, D, 90)
    chords_90 = chords_dec(K, D, steps, 90)
    feasibility = fraction_feasible(K, D)
    hashes = {
        "source_npz": sha256(BASE / "source.npz"),
        "strongest_npz": sha256(BASE / f"results_{strongest_shard}" / "best_case.npz"),
        "producing_script_spectral_basis_refine": sha256(BASE / "spectral_basis_refine.py"),
        "commuting_spectral_search": sha256(BASE / "commuting_spectral_search.py"),
        "recheck_best_refine4_py": sha256(BASE / "recheck_best_refine4.py"),
        "recheck_best_refine4_json": sha256(BASE / "recheck_best_refine4.json"),
    }
    checks = {
        "expected_source_hash": hashes["source_npz"] == EXPECTED["source_npz"],
        "expected_strongest_hash": hashes["strongest_npz"] == EXPECTED["strongest_npz"],
        "expected_producing_script_hash": hashes["producing_script_spectral_basis_refine"]
        == EXPECTED["producing_script"],
        "four_shards": len(ledger["per_shard"]) == 4,
        "each_csv_has_header_plus_5001_rows": all(
            row["physical_lines_including_header"] == 5002 for row in ledger["per_shard"]
        ),
        "each_csv_has_5001_data_rows": all(row["data_rows"] == 5001 for row in ledger["per_shard"]),
        "one_source_row_per_shard": all(row["source_rows"] == 1 for row in ledger["per_shard"]),
        "proposal_indices_complete_each_shard": all(
            row["proposal_indices_unique_0_to_4999"] for row in ledger["per_shard"]
        ),
        "source_rows_have_index_minus_one": all(row["source_index_is_minus_one"] for row in ledger["per_shard"]),
        "manifest_status_complete": all(row["manifest_status"] == "SCOUT_COMPLETE" for row in ledger["per_shard"]),
        "manifest_exit_codes_zero": all(row["manifest_exit_code"] == 0 for row in ledger["per_shard"]),
        "manifest_threads_one": all(row["manifest_threads"] == 1 for row in ledger["per_shard"]),
        "manifest_positive_counts_zero": all(int(row["manifest_positive_count"]) == 0 for row in ledger["per_shard"]),
        "accepted_counts_match_manifest": all(row["accepted_count_matches_manifest"] for row in ledger["per_shard"]),
        "all_status_no_hit": ledger["aggregate"]["non_no_hit_rows"] == 0,
        "no_positive_gaps": ledger["aggregate"]["positive_gap_rows"] == 0,
        "aggregate_rows_20004": ledger["aggregate"]["data_rows"] == 20004,
        "aggregate_proposals_20000": ledger["aggregate"]["proposal_rows"] == 20000,
        "aggregate_sources_4": ledger["aggregate"]["source_rows"] == 4,
        "strongest_location_matches": ledger["aggregate"]["best_shard"] == EXPECTED["strongest_shard"]
        and ledger["aggregate"]["best_index"] == EXPECTED["strongest_index"],
        "strongest_label_one_basis": ledger["aggregate"]["best_label"] == "one_basis_rotation",
        "strongest_json_matches_ledger": all(row["best_matches_json"] for row in ledger["per_shard"]),
        "author_summary_status_matches": author["status"] == "HIGH_PRECISION_STABLE_NEGATIVE",
        "author_summary_best_location_matches": author["strongest_shard"] == EXPECTED["strongest_shard"]
        and author["strongest_index"] == EXPECTED["strongest_index"],
        "author_hashes_match_expected": author["hashes"]["source_npz"] == EXPECTED["source_npz"]
        and author["hashes"]["best_case_npz"] == EXPECTED["strongest_npz"]
        and author["hashes"]["producing_script"] == EXPECTED["producing_script"],
        "decimal_H2_negative": Decimal(decimal_90["H2"]) < 0,
        "decimal_rho_below_one": Decimal(decimal_90["rho"]) < 1,
        "all_chord_gaps_negative": all(Decimal(row["midpoint_gap"]) < 0 for row in chords_90["rows"]),
        "fraction_D_pd": feasibility["D_positive_definite"]["all_positive"],
        "fraction_endpoints_strict": all(
            endpoint["K_minus_margin_I"]["all_positive"]
            and endpoint["I_minus_K_minus_margin_I"]["all_positive"]
            for endpoint in feasibility["endpoint_LDL"]
        ),
    }
    return {
        "status": "CORRECT_FOR_STATED_SCOUT_AND_STRONGEST_GATE" if all(checks.values()) else "CRITICAL_GAPS",
        "elapsed_seconds": time.time() - started,
        "hashes": hashes,
        "ledger_audit": ledger,
        "strongest": {
            "shard": strongest_shard,
            "index": EXPECTED["strongest_index"],
            "raw_kernel_max_asymmetry": float(np.max(np.abs(raw_K - raw_K.T))),
            "raw_direction_max_asymmetry": float(np.max(np.abs(raw_D - raw_D.T))),
            "K_min_eig_float": float(np.linalg.eigvalsh(K)[0]),
            "K_max_eig_float": float(np.linalg.eigvalsh(K)[-1]),
            "D_min_eig_float": float(np.linalg.eigvalsh(D)[0]),
            "D_max_eig_float": float(np.linalg.eigvalsh(D)[-1]),
            "commutator_frobenius_float": float(np.linalg.norm(K @ D - D @ K)),
            "decimal_90_mobius": decimal_90,
            "chords_90_mobius": chords_90,
            "fraction_ldl": feasibility,
        },
        "checks": checks,
        "scope_classification": {
            "ledger_and_manifest": "CORRECT" if all(
                checks[k]
                for k in [
                    "four_shards",
                    "each_csv_has_header_plus_5001_rows",
                    "each_csv_has_5001_data_rows",
                    "one_source_row_per_shard",
                    "proposal_indices_complete_each_shard",
                    "source_rows_have_index_minus_one",
                    "manifest_status_complete",
                    "manifest_exit_codes_zero",
                    "manifest_threads_one",
                    "manifest_positive_counts_zero",
                    "accepted_counts_match_manifest",
                    "all_status_no_hit",
                    "no_positive_gaps",
                    "aggregate_rows_20004",
                    "aggregate_proposals_20000",
                    "aggregate_sources_4",
                    "strongest_location_matches",
                    "strongest_label_one_basis",
                    "strongest_json_matches_ledger",
                ]
            ) else "CRITICAL_GAPS",
            "strongest_high_precision_gate": "CORRECT" if all(
                checks[k]
                for k in [
                    "expected_source_hash",
                    "expected_strongest_hash",
                    "expected_producing_script_hash",
                    "author_hashes_match_expected",
                    "decimal_H2_negative",
                    "decimal_rho_below_one",
                    "all_chord_gaps_negative",
                    "fraction_D_pd",
                    "fraction_endpoints_strict",
                ]
            ) else "CRITICAL_GAPS",
            "proposal_generation_replay": "INCOMPLETE_FULL_REPLAY_NOT_RUN",
            "mathematical_scope": "SCOUT_FIXED_Q_PER_CENTER_OUTER_JOINT_BASIS_SPECTRUM_FINITE_SEARCH",
        },
    }


def main():
    report = audit()
    out = HERE / "fresh_round16_refine4_audit.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if report["status"] == "CRITICAL_GAPS":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
