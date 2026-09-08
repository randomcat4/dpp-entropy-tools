from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import sys
import time
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")

import numpy as np


HERE = Path(__file__).resolve().parent
BASE = HERE.parent
OUT = HERE / "fresh_round17_refine5_audit.json"

EXPECTED = {
    "source_npz": "b078c507558faa74b2a583581bfc5b51859009dafd12e6c2b95e6e25cad0b5a2",
    "strongest_npz": "6a4fb8bd1790fbe17dbb58fac96a5ee3585bf7aac9c8f395608478b58750a978",
    "producing_script": "28ae523c10184dc1effe2f857adbdad4156683292f2ad7da2d281e2af6ad7268",
    "strongest_shard": 1,
    "strongest_index": 4910,
    "proposal_count_per_shard": 5000,
    "data_rows_per_shard": 5001,
    "n": 12,
    "margin_floor": 0.01,
}

FLOAT_KEYS = [
    "spectral_scale",
    "basis_scale",
    "rho_psd",
    "rho_unrestricted",
    "total_psd_fisher_normalized",
    "min_atom",
    "normalization_residual",
    "generalized_residual",
    "direction_min_rate",
    "direction_max_rate",
    "chord_step",
    "chord_gap",
    "spectrum_margin",
    "basis_orthogonality_residual",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def bool_text(x: str) -> bool:
    return x.strip().lower() == "true"


def nearly_equal(a: float, b: float, *, atol: float = 1e-12, rtol: float = 1e-12) -> bool:
    return math.isclose(a, b, abs_tol=atol, rel_tol=rtol)


def row_float(row: dict[str, str], key: str) -> float:
    return float(row[key])


def compare_row_to_json(row: dict[str, str], obj: dict) -> dict[str, bool]:
    checks: dict[str, bool] = {
        "index": int(row["index"]) == int(obj["index"]),
        "label": row["label"] == obj["label"],
        "accepted": bool_text(row["accepted"]) == bool(obj["accepted"]),
        "status": row["status"] == obj["status"],
    }
    for key in FLOAT_KEYS:
        checks[key] = nearly_equal(float(row[key]), float(obj[key]), atol=3e-15, rtol=3e-15)
    checks["unrestricted_same_sign"] = bool_text(row["unrestricted_same_sign"]) == bool(
        obj["unrestricted_same_sign"]
    )
    return checks


def parse_log_manifest(path: Path):
    last_obj = None
    completed = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if not s or not s.startswith("{"):
                continue
            obj = json.loads(s)
            if "completed" in obj:
                completed.append(obj)
            if obj.get("status") == "SCOUT_COMPLETE":
                last_obj = obj
    return last_obj, completed


def load_ledgers_and_check() -> dict:
    recheck = read_json(BASE / "recheck_best_refine5.json")
    ledger_report = {
        "per_shard": [],
        "aggregate": {},
        "checks": {},
    }
    all_rows = []
    all_best_candidates = []
    for shard in range(4):
        result_dir = BASE / f"results_{shard}"
        manifest = read_json(result_dir / "manifest.json")
        best_json = read_json(result_dir / "best_case.json")
        with (result_dir / "candidate_ledger.csv").open("r", encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
        log_manifest, progress = parse_log_manifest(BASE / f"run_{shard}.log")
        data_line_count = len(rows)
        source_rows = [r for r in rows if int(r["index"]) == -1]
        proposal_rows = [r for r in rows if int(r["index"]) >= 0]
        proposal_indices = sorted(int(r["index"]) for r in proposal_rows)
        statuses = {}
        for r in rows:
            statuses[r["status"]] = statuses.get(r["status"], 0) + 1
        positive_gap_rows = [r for r in proposal_rows if row_float(r, "chord_gap") > 0.0]
        non_no_hit_rows = [r for r in rows if r["status"] != "NO_HIT"]
        accepted_proposal_rows = [r for r in proposal_rows if bool_text(r["accepted"])]
        best_row = max(rows, key=lambda r: row_float(r, "rho_psd"))
        max_gap = max(row_float(r, "chord_gap") for r in proposal_rows)
        best_checks = compare_row_to_json(best_row, best_json)
        source = source_rows[0] if source_rows else None
        shard_report = {
            "shard": shard,
            "manifest": manifest,
            "data_rows": data_line_count,
            "source_rows": len(source_rows),
            "proposal_rows": len(proposal_rows),
            "proposal_index_min": min(proposal_indices) if proposal_indices else None,
            "proposal_index_max": max(proposal_indices) if proposal_indices else None,
            "proposal_indices_complete": proposal_indices == list(range(EXPECTED["proposal_count_per_shard"])),
            "statuses": statuses,
            "non_no_hit_rows": len(non_no_hit_rows),
            "positive_gap_rows": len(positive_gap_rows),
            "max_proposal_gap": max_gap,
            "accepted_proposal_rows": len(accepted_proposal_rows),
            "source_status": source["status"] if source else None,
            "source_rho": row_float(source, "rho_psd") if source else None,
            "source_gap": row_float(source, "chord_gap") if source else None,
            "best_row_index": int(best_row["index"]),
            "best_row_rho": row_float(best_row, "rho_psd"),
            "best_row_status": best_row["status"],
            "best_json": best_json,
            "best_row_matches_best_json": all(best_checks.values()),
            "best_row_compare_details": best_checks,
            "best_npz_sha256": sha256_file(result_dir / "best_case.npz"),
            "log_final_manifest_matches_file": log_manifest == manifest,
            "log_progress_records": len(progress),
            "checks": {
                "manifest_status_complete": manifest.get("status") == "SCOUT_COMPLETE",
                "manifest_exit_code_zero": manifest.get("exit_code") == 0,
                "manifest_seed_expected": manifest.get("seed") == 2026090856 + shard,
                "manifest_n_expected": manifest.get("n") == EXPECTED["n"],
                "manifest_margin_floor_expected": nearly_equal(
                    float(manifest.get("margin_floor")), EXPECTED["margin_floor"]
                ),
                "manifest_proposal_count_5000": manifest.get("proposal_count") == EXPECTED[
                    "proposal_count_per_shard"
                ],
                "manifest_ledger_rows_5001": manifest.get("ledger_rows_including_source")
                == EXPECTED["data_rows_per_shard"],
                "csv_data_rows_5001": data_line_count == EXPECTED["data_rows_per_shard"],
                "one_source_row": len(source_rows) == 1,
                "proposal_rows_5000": len(proposal_rows) == EXPECTED["proposal_count_per_shard"],
                "proposal_indices_complete": proposal_indices
                == list(range(EXPECTED["proposal_count_per_shard"])),
                "all_status_no_hit": len(non_no_hit_rows) == 0,
                "no_positive_gap_rows": len(positive_gap_rows) == 0,
                "manifest_positive_count_zero": manifest.get("positive_count") == 0,
                "manifest_accepted_count_matches_proposals": len(accepted_proposal_rows)
                == manifest.get("accepted_count"),
                "source_row_matches_manifest": source is not None
                and source["status"] == manifest.get("source_status")
                and nearly_equal(row_float(source, "rho_psd"), float(manifest.get("source_rho")))
                and nearly_equal(row_float(source, "chord_gap"), float(manifest.get("source_gap"))),
                "best_row_matches_best_json": all(best_checks.values()),
                "best_rho_matches_manifest": nearly_equal(
                    row_float(best_row, "rho_psd"), float(manifest.get("best_rho_psd"))
                ),
                "best_spectrum_margin_matches_manifest": nearly_equal(
                    row_float(best_row, "spectrum_margin"),
                    float(manifest.get("best_spectrum_margin")),
                ),
                "log_final_manifest_matches_file": log_manifest == manifest,
            },
        }
        ledger_report["per_shard"].append(shard_report)
        all_rows.extend((shard, r) for r in rows)
        all_best_candidates.append((shard, best_row))

    global_best_shard, global_best_row = max(all_best_candidates, key=lambda sr: row_float(sr[1], "rho_psd"))
    proposal_rows_all = [(s, r) for s, r in all_rows if int(r["index"]) >= 0]
    source_rows_all = [(s, r) for s, r in all_rows if int(r["index"]) == -1]
    aggregate = {
        "data_rows": len(all_rows),
        "proposal_rows": len(proposal_rows_all),
        "source_rows": len(source_rows_all),
        "non_no_hit_rows": sum(1 for _, r in all_rows if r["status"] != "NO_HIT"),
        "positive_gap_rows": sum(1 for _, r in proposal_rows_all if row_float(r, "chord_gap") > 0.0),
        "max_proposal_gap": max(row_float(r, "chord_gap") for _, r in proposal_rows_all),
        "global_best_shard": global_best_shard,
        "global_best_index": int(global_best_row["index"]),
        "global_best_rho": row_float(global_best_row, "rho_psd"),
        "recheck_best_shard": int(recheck["strongest_shard"]),
        "recheck_best_index": int(recheck["strongest_index"]),
    }
    ledger_report["aggregate"] = aggregate
    ledger_report["recheck_ledger_summary"] = recheck["ledger"]
    ledger_report["checks"] = {
        "four_shards": len(ledger_report["per_shard"]) == 4,
        "all_shard_checks_true": all(
            all(shard_report["checks"].values()) for shard_report in ledger_report["per_shard"]
        ),
        "aggregate_data_rows_20004": aggregate["data_rows"] == 20004,
        "aggregate_proposals_20000": aggregate["proposal_rows"] == 20000,
        "aggregate_sources_4": aggregate["source_rows"] == 4,
        "aggregate_non_no_hit_zero": aggregate["non_no_hit_rows"] == 0,
        "aggregate_positive_gap_zero": aggregate["positive_gap_rows"] == 0,
        "aggregate_max_gap_matches_recheck": nearly_equal(
            aggregate["max_proposal_gap"], float(recheck["ledger"]["maximum_gap"])
        ),
        "global_best_matches_recheck": aggregate["global_best_shard"] == int(recheck["strongest_shard"])
        and aggregate["global_best_index"] == int(recheck["strongest_index"]),
    }
    return ledger_report


def dec_from_float(x: float) -> Decimal:
    return Decimal(str(float(x)))


def to_decimal_matrix(arr: np.ndarray) -> list[list[Decimal]]:
    return [[dec_from_float(arr[i, j]) for j in range(arr.shape[1])] for i in range(arr.shape[0])]


def det_and_inverse_decimal(a: list[list[Decimal]]) -> tuple[Decimal, list[list[Decimal]]]:
    n = len(a)
    if n == 0:
        return Decimal(1), []
    m = [row[:] + [Decimal(1) if i == j else Decimal(0) for j in range(n)] for i, row in enumerate(a)]
    det = Decimal(1)
    sign = Decimal(1)
    for col in range(n):
        pivot_row = max(range(col, n), key=lambda r: abs(m[r][col]))
        pivot = m[pivot_row][col]
        if pivot == 0:
            raise ArithmeticError("singular pivot in Decimal elimination")
        if pivot_row != col:
            m[col], m[pivot_row] = m[pivot_row], m[col]
            sign = -sign
        pivot = m[col][col]
        det *= pivot
        inv_pivot = Decimal(1) / pivot
        for j in range(2 * n):
            m[col][j] *= inv_pivot
        for r in range(n):
            if r == col:
                continue
            factor = m[r][col]
            if factor == 0:
                continue
            for j in range(2 * n):
                m[r][j] -= factor * m[col][j]
    inv = [row[n:] for row in m]
    return sign * det, inv


def det_decimal(a: list[list[Decimal]]) -> Decimal:
    n = len(a)
    if n == 0:
        return Decimal(1)
    m = [row[:] for row in a]
    det = Decimal(1)
    sign = Decimal(1)
    for col in range(n):
        pivot_row = max(range(col, n), key=lambda r: abs(m[r][col]))
        pivot = m[pivot_row][col]
        if pivot == 0:
            return Decimal(0)
        if pivot_row != col:
            m[col], m[pivot_row] = m[pivot_row], m[col]
            sign = -sign
        pivot = m[col][col]
        det *= pivot
        for r in range(col + 1, n):
            factor = m[r][col] / pivot
            if factor == 0:
                continue
            for c in range(col, n):
                m[r][c] -= factor * m[col][c]
    return sign * det


def subset_indices(mask: int, n: int) -> list[int]:
    return [i for i in range(n) if (mask >> i) & 1]


def principal(mat: list[list[Decimal]], idx: list[int]) -> list[list[Decimal]]:
    return [[mat[i][j] for j in idx] for i in idx]


def inclusion_jets_decimal(kmat: list[list[Decimal]], dmat: list[list[Decimal]], n: int):
    size = 1 << n
    q0 = [Decimal(0)] * size
    q1 = [Decimal(0)] * size
    q2 = [Decimal(0)] * size
    q0[0] = Decimal(1)
    for mask in range(1, size):
        idx = subset_indices(mask, n)
        a = principal(kmat, idx)
        e = principal(dmat, idx)
        det_a, inv_a = det_and_inverse_decimal(a)
        m = len(idx)
        g = [[sum(inv_a[i][r] * e[r][j] for r in range(m)) for j in range(m)] for i in range(m)]
        tr_g = sum(g[i][i] for i in range(m))
        tr_g2 = sum(g[i][j] * g[j][i] for i in range(m) for j in range(m))
        q0[mask] = det_a
        q1[mask] = det_a * tr_g
        q2[mask] = det_a * (tr_g * tr_g - tr_g2)
    return q0, q1, q2


def inclusion_probs_decimal(kmat: list[list[Decimal]], n: int):
    size = 1 << n
    q0 = [Decimal(0)] * size
    q0[0] = Decimal(1)
    for mask in range(1, size):
        idx = subset_indices(mask, n)
        q0[mask] = det_decimal(principal(kmat, idx))
    return q0


def mobius_from_inclusion(q: list[Decimal], n: int) -> list[Decimal]:
    p = q[:]
    for bit in range(n):
        step = 1 << bit
        for mask in range(1 << n):
            if (mask & step) == 0:
                p[mask] -= p[mask | step]
    return p


def entropy_from_atoms_decimal(p: list[Decimal]) -> Decimal:
    return -sum(x * x.ln() for x in p)


def decimal_directional_gate(k: np.ndarray, d: np.ndarray, *, precision: int = 95) -> dict:
    getcontext().prec = precision
    n = k.shape[0]
    kmat = to_decimal_matrix(k)
    dmat = to_decimal_matrix(d)
    q0, q1, q2 = inclusion_jets_decimal(kmat, dmat, n)
    p0 = mobius_from_inclusion(q0, n)
    p1 = mobius_from_inclusion(q1, n)
    p2 = mobius_from_inclusion(q2, n)
    if any(x <= 0 for x in p0):
        raise ArithmeticError("non-positive exact atom encountered")
    fisher = sum((b * b) / a for a, b in zip(p0, p1))
    acceleration = -sum(c * a.ln() for a, c in zip(p0, p2))
    h2 = acceleration - fisher
    entropy = entropy_from_atoms_decimal(p0)
    direct_inclusion = q0[:]
    remobius_inclusion = [Decimal(0)] * (1 << n)
    for a_mask in range(1 << n):
        remobius_inclusion[a_mask] = sum(
            p0[y_mask] for y_mask in range(1 << n) if (y_mask & a_mask) == a_mask
        )
    mobius_max_abs_difference = max(
        abs(direct_inclusion[i] - remobius_inclusion[i]) for i in range(1 << n)
    )
    return {
        "precision": precision,
        "event_count": 1 << n,
        "entropy": str(entropy),
        "fisher": str(fisher),
        "acceleration": str(acceleration),
        "H2": str(h2),
        "rho": str(acceleration / fisher),
        "sum_p": str(sum(p0)),
        "sum_p1": str(sum(p1)),
        "sum_p2": str(sum(p2)),
        "min_atom": str(min(p0)),
        "mobius_max_abs_difference": str(mobius_max_abs_difference),
        "checks": {
            "all_atoms_positive": all(x > 0 for x in p0),
            "sum_p_close_to_one": abs(sum(p0) - Decimal(1)) < Decimal("1e-80"),
            "sum_p1_close_to_zero": abs(sum(p1)) < Decimal("1e-80"),
            "sum_p2_close_to_zero": abs(sum(p2)) < Decimal("1e-80"),
            "H2_negative": h2 < 0,
            "rho_below_one": acceleration / fisher < 1,
        },
    }


def decimal_entropy_at(k: np.ndarray, d: np.ndarray, t: str, *, precision: int = 80) -> Decimal:
    getcontext().prec = precision
    td = Decimal(t)
    n = k.shape[0]
    kmat = to_decimal_matrix(k)
    dmat = to_decimal_matrix(d)
    kt = [[kmat[i][j] + td * dmat[i][j] for j in range(n)] for i in range(n)]
    p = mobius_from_inclusion(inclusion_probs_decimal(kt, n), n)
    if any(x <= 0 for x in p):
        raise ArithmeticError(f"non-positive atom at t={t}")
    return entropy_from_atoms_decimal(p)


def decimal_chord_gates(k: np.ndarray, d: np.ndarray, steps: list[str], h0: Decimal) -> list[dict]:
    out = []
    for step in steps:
        hp = decimal_entropy_at(k, d, step, precision=80)
        hm = decimal_entropy_at(k, d, "-" + step if not step.startswith("-") else step[1:], precision=80)
        t = Decimal(step)
        gap = (hp + hm) / Decimal(2) - h0
        out.append(
            {
                "step": step,
                "Hminus": str(hm),
                "Hplus": str(hp),
                "midpoint_gap": str(gap),
                "central_H2": str(Decimal(2) * gap / (t * t)),
                "gap_negative": gap < 0,
            }
        )
    return out


def fraction_from_float(x: float) -> Fraction:
    return Fraction(str(float(x)))


def to_fraction_matrix(arr: np.ndarray) -> list[list[Fraction]]:
    return [[fraction_from_float(arr[i, j]) for j in range(arr.shape[1])] for i in range(arr.shape[0])]


def frac_eye(n: int) -> list[list[Fraction]]:
    return [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]


def frac_add(a, b, scale_b=Fraction(1)):
    n = len(a)
    return [[a[i][j] + scale_b * b[i][j] for j in range(n)] for i in range(n)]


def frac_sub(a, b):
    n = len(a)
    return [[a[i][j] - b[i][j] for j in range(n)] for i in range(n)]


def frac_ldl_pivots(a: list[list[Fraction]]) -> list[Fraction]:
    n = len(a)
    L = [[Fraction(0) for _ in range(n)] for __ in range(n)]
    pivots = [Fraction(0) for _ in range(n)]
    for i in range(n):
        L[i][i] = Fraction(1)
    for j in range(n):
        pivot = a[j][j] - sum(L[j][k] * L[j][k] * pivots[k] for k in range(j))
        pivots[j] = pivot
        if pivot == 0:
            continue
        for i in range(j + 1, n):
            L[i][j] = (
                a[i][j] - sum(L[i][k] * L[j][k] * pivots[k] for k in range(j))
            ) / pivot
    return pivots


def ldl_summary(a: list[list[Fraction]]) -> dict:
    pivots = frac_ldl_pivots(a)
    min_pivot = min(pivots)
    return {
        "count": len(pivots),
        "all_positive": all(x > 0 for x in pivots),
        "minimum_float": float(min_pivot),
        "minimum_numerator_digits": len(str(abs(min_pivot.numerator))),
        "minimum_denominator_digits": len(str(abs(min_pivot.denominator))),
    }


def fraction_feasibility(k: np.ndarray, d: np.ndarray) -> dict:
    n = k.shape[0]
    kf = to_fraction_matrix(k)
    df = to_fraction_matrix(d)
    eye = frac_eye(n)
    margin = Fraction(1, 2000)
    out = {
        "interpretation": "symmetrized float entries converted with Fraction(str(float(entry)))",
        "uniform_interval": ["-1/200", "1/200"],
        "strict_spectral_margin": "1/2000",
        "endpoint_LDL": [],
        "D_positive_definite": ldl_summary(df),
    }
    for t in [Fraction(-1, 200), Fraction(1, 200)]:
        kt = frac_add(kf, df, t)
        kt_minus_margin = frac_sub(kt, [[margin if i == j else Fraction(0) for j in range(n)] for i in range(n)])
        i_minus_kt_minus_margin = frac_sub(
            frac_sub(eye, kt),
            [[margin if i == j else Fraction(0) for j in range(n)] for i in range(n)],
        )
        out["endpoint_LDL"].append(
            {
                "step": f"{t.numerator}/{t.denominator}",
                "K_t_minus_margin_I": ldl_summary(kt_minus_margin),
                "I_minus_K_t_minus_margin_I": ldl_summary(i_minus_kt_minus_margin),
            }
        )
    out["checks"] = {
        "D_positive_definite": out["D_positive_definite"]["all_positive"],
        "endpoints_K_margin_positive": all(
            e["K_t_minus_margin_I"]["all_positive"] for e in out["endpoint_LDL"]
        ),
        "endpoints_I_minus_K_margin_positive": all(
            e["I_minus_K_t_minus_margin_I"]["all_positive"] for e in out["endpoint_LDL"]
        ),
    }
    return out


def float_spectral_checks(k: np.ndarray, d: np.ndarray, spectrum: np.ndarray, rates: np.ndarray, q: np.ndarray) -> dict:
    k_eigs = np.linalg.eigvalsh(k)
    d_eigs = np.linalg.eigvalsh(d)
    return {
        "K_min_eig_float": float(k_eigs[0]),
        "K_max_eig_float": float(k_eigs[-1]),
        "I_minus_K_min_eig_float": float(1.0 - k_eigs[-1]),
        "actual_spectrum_margin_float": float(min(k_eigs[0], 1.0 - k_eigs[-1])),
        "npz_spectrum_min": float(np.min(spectrum)),
        "npz_spectrum_max": float(np.max(spectrum)),
        "npz_spectrum_margin": float(min(np.min(spectrum), 1.0 - np.max(spectrum))),
        "D_min_eig_float": float(d_eigs[0]),
        "D_max_eig_float": float(d_eigs[-1]),
        "rates_min": float(np.min(rates)),
        "rates_max": float(np.max(rates)),
        "basis_orthogonality_residual": float(np.linalg.norm(q.T @ q - np.eye(q.shape[0]))),
        "commutator_frobenius": float(np.linalg.norm(k @ d - d @ k)),
        "K_max_asymmetry": float(np.max(np.abs(k - k.T))),
        "D_max_asymmetry": float(np.max(np.abs(d - d.T))),
    }


def main() -> int:
    t0 = time.time()
    ledger = load_ledgers_and_check()
    recheck = read_json(BASE / "recheck_best_refine5.json")
    strongest_dir = BASE / f"results_{EXPECTED['strongest_shard']}"
    strongest_json = read_json(strongest_dir / "best_case.json")
    z = np.load(strongest_dir / "best_case.npz")
    k = np.array(z["kernel"], dtype=float)
    d = np.array(z["direction"], dtype=float)
    q = np.array(z["eigenvectors"], dtype=float)
    spectrum = np.array(z["spectrum"], dtype=float)
    rates = np.array(z["rates"], dtype=float)
    k = (k + k.T) / 2.0
    d = (d + d.T) / 2.0

    hashes = {
        "source_npz": sha256_file(BASE / "source.npz"),
        "strongest_npz": sha256_file(strongest_dir / "best_case.npz"),
        "spectral_basis_refine_py": sha256_file(BASE / "spectral_basis_refine.py"),
        "commuting_spectral_search_py": sha256_file(BASE / "commuting_spectral_search.py"),
        "recheck_best_refine5_py": sha256_file(BASE / "recheck_best_refine5.py"),
    }
    hash_checks = {
        "source_npz_matches_expected": hashes["source_npz"] == EXPECTED["source_npz"],
        "strongest_npz_matches_expected": hashes["strongest_npz"] == EXPECTED["strongest_npz"],
        "producing_script_matches_expected": hashes["spectral_basis_refine_py"]
        == EXPECTED["producing_script"],
    }

    spectral = float_spectral_checks(k, d, spectrum, rates, q)
    spectrum_margin_reported = float(strongest_json["spectrum_margin"])
    spectral_checks = {
        "reported_margin_matches_npz_spectrum": nearly_equal(
            spectrum_margin_reported, spectral["npz_spectrum_margin"], atol=2e-14, rtol=2e-14
        ),
        "reported_margin_matches_eigvalsh": nearly_equal(
            spectrum_margin_reported,
            spectral["actual_spectrum_margin_float"],
            atol=3e-13,
            rtol=3e-13,
        ),
        "reported_margin_at_floor": abs(spectrum_margin_reported - EXPECTED["margin_floor"]) < 1e-12,
        "K_strict_float": spectral["K_min_eig_float"] > 0 and spectral["K_max_eig_float"] < 1,
        "D_psd_float": spectral["D_min_eig_float"] > 0,
        "near_commuting_float": spectral["commutator_frobenius"] < 1e-12,
    }

    decimal_gate = decimal_directional_gate(k, d, precision=95)
    chords = decimal_chord_gates(
        k,
        d,
        [
            str(strongest_json["chord_step"]),
            "0.001",
            "0.0001",
        ],
        Decimal(decimal_gate["entropy"]),
    )
    frac = fraction_feasibility(k, d)

    directional_against_author = {
        "H2_matches_recheck_decimal_80": abs(
            Decimal(decimal_gate["H2"]) - Decimal(recheck["decimal_directional"][-1]["H2"])
        )
        < Decimal("1e-70"),
        "rho_matches_recheck_decimal_80": abs(
            Decimal(decimal_gate["rho"]) - Decimal(recheck["decimal_directional"][-1]["rho"])
        )
        < Decimal("1e-70"),
        "fisher_matches_recheck_decimal_80": abs(
            Decimal(decimal_gate["fisher"]) - Decimal(recheck["decimal_directional"][-1]["fisher"])
        )
        < Decimal("1e-70"),
        "acceleration_matches_recheck_decimal_80": abs(
            Decimal(decimal_gate["acceleration"]) - Decimal(recheck["decimal_directional"][-1]["acceleration"])
        )
        < Decimal("1e-70"),
    }
    chord_against_author = []
    for own, author in zip(chords, recheck["decimal_chords"]):
        chord_against_author.append(
            {
                "step": own["step"],
                "gap_matches_author": abs(Decimal(own["midpoint_gap"]) - Decimal(author["midpoint_gap"]))
                < Decimal("1e-60"),
                "central_H2_matches_author": abs(Decimal(own["central_H2"]) - Decimal(author["central_H2"]))
                < Decimal("1e-55"),
            }
        )

    checks = {
        "ledger_checks": all(ledger["checks"].values()),
        "hash_checks": all(hash_checks.values()),
        "strongest_json_index_expected": int(strongest_json["index"]) == EXPECTED["strongest_index"],
        "recheck_strongest_expected": int(recheck["strongest_shard"]) == EXPECTED["strongest_shard"]
        and int(recheck["strongest_index"]) == EXPECTED["strongest_index"],
        "spectral_checks": all(spectral_checks.values()),
        "decimal_gate_checks": all(decimal_gate["checks"].values()),
        "directional_matches_author": all(directional_against_author.values()),
        "all_decimal_chords_negative": all(c["gap_negative"] for c in chords),
        "chords_match_author": all(x["gap_matches_author"] and x["central_H2_matches_author"] for x in chord_against_author),
        "fraction_feasibility": all(frac["checks"].values()),
    }
    result = {
        "audit": "D10-H9 round17_refine5 fresh nonauthor audit",
        "base": str(BASE),
        "denominators": {
            "shards": 4,
            "proposal_rows": 20000,
            "source_rows": 4,
            "ledger_data_rows": 20004,
            "exact_atoms": 4096,
            "decimal_chords": 3,
            "fraction_ldl_matrices": 5,
        },
        "hashes": hashes,
        "hash_checks": hash_checks,
        "ledger": ledger,
        "strongest": {
            "shard": EXPECTED["strongest_shard"],
            "index": EXPECTED["strongest_index"],
            "json": strongest_json,
            "spectral": spectral,
            "spectrum_floor_interpretation": (
                "reported margin is at the configured 0.01 search floor; independent eigvalsh and "
                "Fraction endpoint LDL checks still show strict feasibility, so this is not treated as singular"
            ),
            "spectral_checks": spectral_checks,
            "decimal_directional_precision95": decimal_gate,
            "directional_against_author": directional_against_author,
            "decimal_chords": chords,
            "chord_against_author": chord_against_author,
            "fraction_feasibility": frac,
        },
        "scope": {
            "full_seed_regeneration": "INCOMPLETE: not replayed from random seeds",
            "float_scout": "fixed-Q at each accepted center; outer search perturbs joint basis/spectrum",
            "rational_line": "Fraction certificate applies to decimal-rationalized near-commuting line, not an exact commuting theorem",
        },
        "checks": checks,
        "status_layers": {
            "copied_data_accounting_and_hashes": "CORRECT" if all(ledger["checks"].values()) and all(hash_checks.values()) else "CRITICAL_GAPS",
            "strongest_high_precision_gate": "CORRECT"
            if checks["decimal_gate_checks"]
            and checks["directional_matches_author"]
            and checks["all_decimal_chords_negative"]
            and checks["chords_match_author"]
            and checks["fraction_feasibility"]
            and checks["spectral_checks"]
            else "CRITICAL_GAPS",
            "full_seed_regeneration": "INCOMPLETE",
            "mathematical_generalization": "SCOUT",
        },
        "exit_code": 0 if all(checks.values()) else 1,
        "elapsed_seconds": time.time() - t0,
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"exit_code": result["exit_code"], "out": str(OUT), "elapsed_seconds": result["elapsed_seconds"]}, indent=2))
    return int(result["exit_code"])


if __name__ == "__main__":
    sys.exit(main())
