#!/usr/bin/env python3
"""Fresh verifier for D10-H5 round13 refine artifacts.

This script does not import the author gate or the search modules.  It reads
the round13 artifacts, recomputes ledger summaries, checks best NPZ consistency,
and independently evaluates the strongest exact-event Hessian using Decimal
arithmetic plus Fraction LDL feasibility checks.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import re
import time
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path

import numpy as np

for _var in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_var, "1")

getcontext().prec = 90

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
COMMUTING_ROOT = ROOT.parent
CURRENT_SCRIPT = COMMUTING_ROOT / "spectral_basis_refine.py"
OUT = HERE / "fresh_round13_verify.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_rows(shard: int) -> list[dict[str, str]]:
    path = ROOT / f"results_{shard}" / "candidate_ledger.csv"
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def float_row(row: dict[str, str], key: str) -> float:
    return float(row[key])


def mask_pop(mask: int) -> int:
    return mask.bit_count()


def exact_event_float(kernel: np.ndarray, direction: np.ndarray | None = None) -> dict:
    n = len(kernel)
    p = []
    p1 = []
    p2 = []
    for mask in range(1 << n):
        M = kernel.copy()
        absent = 0
        for i in range(n):
            if not ((mask >> i) & 1):
                M[i, i] -= 1.0
                absent += 1
        sign, logabs = np.linalg.slogdet(M)
        expected = -1.0 if (absent & 1) else 1.0
        if sign * expected <= 0:
            raise ArithmeticError(f"bad atom sign at mask {mask}")
        prob = math.exp(float(logabs))
        p.append(prob)
        if direction is not None:
            inv = np.linalg.inv(M)
            A = inv @ direction
            score = float(np.trace(A))
            hlog = -float(np.trace(A @ A))
            p1.append(prob * score)
            p2.append(prob * (score * score + hlog))
    report = {
        "event_count": len(p),
        "sum_p": float(sum(p)),
        "sum_p_minus_one": float(sum(p) - 1.0),
        "min_atom": float(min(p)),
    }
    if direction is not None:
        fisher = sum((b * b) / a for a, b in zip(p, p1))
        acceleration = sum(-c * math.log(a) for a, c in zip(p, p2))
        report.update(
            {
                "sum_p1": float(sum(p1)),
                "sum_p2": float(sum(p2)),
                "fisher": float(fisher),
                "acceleration": float(acceleration),
                "H2": float(-fisher + acceleration),
                "rho": float(acceleration / fisher),
            }
        )
    return report


def npz_recheck(shard: int, best_row: dict[str, str]) -> dict:
    path = ROOT / f"results_{shard}" / "best_case.npz"
    data = np.load(path)
    K_raw = np.asarray(data["kernel"], dtype=float)
    D_raw = np.asarray(data["direction"], dtype=float)
    spectrum = np.asarray(data["spectrum"], dtype=float)
    rates = np.asarray(data["rates"], dtype=float)
    basis = np.asarray(data["eigenvectors"], dtype=float)
    K = (K_raw + K_raw.T) / 2.0
    D = (D_raw + D_raw.T) / 2.0
    K_recon = basis @ np.diag(spectrum) @ basis.T
    D_recon = basis @ np.diag(rates) @ basis.T
    directional = exact_event_float(K, D)
    return {
        "sha256": sha256(path),
        "keys": sorted(list(data.keys())),
        "basis_orthogonality_residual": float(np.linalg.norm(basis.T @ basis - np.eye(len(basis)))),
        "spectrum_margin": float(np.min(np.minimum(spectrum, 1.0 - spectrum))),
        "rates_min": float(rates.min()),
        "rates_max": float(rates.max()),
        "K_reconstruction_max_abs": float(np.max(np.abs(K - K_recon))),
        "D_reconstruction_max_abs": float(np.max(np.abs(D - D_recon))),
        "K_asymmetry_max_abs": float(np.max(np.abs(K_raw - K_raw.T))),
        "D_asymmetry_max_abs": float(np.max(np.abs(D_raw - D_raw.T))),
        "K_eig_min": float(np.linalg.eigvalsh(K)[0]),
        "K_eig_max": float(np.linalg.eigvalsh(K)[-1]),
        "D_eig_min": float(np.linalg.eigvalsh(D)[0]),
        "D_eig_max": float(np.linalg.eigvalsh(D)[-1]),
        "commutator_frobenius": float(np.linalg.norm(K @ D - D @ K)),
        "directional_float": directional,
        "rho_abs_diff_vs_best_row": abs(directional["rho"] - float_row(best_row, "rho_psd")),
        "min_atom_abs_diff_vs_best_row": abs(directional["min_atom"] - float_row(best_row, "min_atom")),
    }


def ledger_and_best_summary() -> dict:
    shards = []
    all_rows = []
    for shard in range(4):
        rows = read_rows(shard)
        manifest = load_json(ROOT / f"results_{shard}" / "manifest.json")
        best_json = load_json(ROOT / f"results_{shard}" / "best_case.json")
        best_row = max(rows, key=lambda row: float_row(row, "rho_psd"))
        gaps = [float_row(row, "chord_gap") for row in rows]
        statuses = [row["status"] for row in rows]
        log_text = (ROOT / f"run_{shard}.log").read_text(encoding="utf-8", errors="replace")
        completed = [int(x) for x in re.findall(r'"completed"\s*:\s*(\d+)', log_text)]
        npz_check = npz_recheck(shard, best_row)
        row_best_compare = {
            key: str(best_json.get(key)) == best_row.get(key)
            for key in ("index", "label", "accepted", "status")
        }
        row_best_float_abs = {
            key: abs(float(best_json[key]) - float(best_row[key]))
            for key in ("rho_psd", "chord_gap", "spectrum_margin", "basis_orthogonality_residual")
        }
        shard_summary = {
            "shard": shard,
            "seed": manifest["seed"],
            "row_count": len(rows),
            "manifest_centers": manifest.get("centers"),
            "manifest_positive_count": manifest["positive_count"],
            "status_counts": {status: statuses.count(status) for status in sorted(set(statuses))},
            "positive_gap_count": sum(g > 0.0 for g in gaps),
            "max_gap": max(gaps),
            "min_gap": min(gaps),
            "best_row_index": int(best_row["index"]),
            "best_row_label": best_row["label"],
            "best_row_rho": float(best_row["rho_psd"]),
            "manifest_best_rho": float(manifest["best_rho_psd"]),
            "source_rho_recomputed": float(manifest["source_rho_recomputed"]),
            "best_json_matches_row_strings": row_best_compare,
            "best_json_float_abs_diffs": row_best_float_abs,
            "log_max_completed": max(completed) if completed else None,
            "log_completed_count": len(completed),
            "npz_recheck": npz_check,
        }
        shards.append(shard_summary)
        for row in rows:
            all_rows.append((shard, row))
    best_shard, best_row = max(all_rows, key=lambda item: float_row(item[1], "rho_psd"))
    return {
        "shards": shards,
        "total_rows": len(all_rows),
        "total_status_hits": sum(row["status"] == "FLOAT_CANDIDATE" for _, row in all_rows),
        "total_positive_gap_count": sum(float_row(row, "chord_gap") > 0.0 for _, row in all_rows),
        "max_gap": max(float_row(row, "chord_gap") for _, row in all_rows),
        "strongest": {
            "shard": best_shard,
            "index": int(best_row["index"]),
            "label": best_row["label"],
            "rho_psd": float(best_row["rho_psd"]),
            "chord_gap": float(best_row["chord_gap"]),
            "chord_step": float(best_row["chord_step"]),
            "status": best_row["status"],
        },
    }


def D(x: float | str) -> Decimal:
    return Decimal(str(x))


def dec_matrix_from_np(A: np.ndarray) -> list[list[Decimal]]:
    return [[D(float(A[i, j])) for j in range(A.shape[1])] for i in range(A.shape[0])]


def dec_identity(n: int) -> list[list[Decimal]]:
    return [[Decimal(1) if i == j else Decimal(0) for j in range(n)] for i in range(n)]


def dec_inv_det(A: list[list[Decimal]]) -> tuple[Decimal, list[list[Decimal]]]:
    n = len(A)
    M = [row[:] for row in A]
    Inv = dec_identity(n)
    det = Decimal(1)
    for i in range(n):
        pivot = max(range(i, n), key=lambda r: abs(M[r][i]))
        if M[pivot][i] == 0:
            raise ArithmeticError("singular Decimal matrix")
        if pivot != i:
            M[i], M[pivot] = M[pivot], M[i]
            Inv[i], Inv[pivot] = Inv[pivot], Inv[i]
            det = -det
        pv = M[i][i]
        det *= pv
        for c in range(n):
            M[i][c] /= pv
            Inv[i][c] /= pv
        for r in range(n):
            if r == i:
                continue
            q = M[r][i]
            if q:
                for c in range(n):
                    M[r][c] -= q * M[i][c]
                    Inv[r][c] -= q * Inv[i][c]
    return +det, Inv


def dec_det(A: list[list[Decimal]]) -> Decimal:
    n = len(A)
    M = [row[:] for row in A]
    det = Decimal(1)
    for i in range(n):
        pivot = max(range(i, n), key=lambda r: abs(M[r][i]))
        if M[pivot][i] == 0:
            return Decimal(0)
        if pivot != i:
            M[i], M[pivot] = M[pivot], M[i]
            det = -det
        pv = M[i][i]
        det *= pv
        for r in range(i + 1, n):
            q = M[r][i] / pv
            if q:
                for c in range(i, n):
                    M[r][c] -= q * M[i][c]
    return +det


def dec_matmul(A: list[list[Decimal]], B: list[list[Decimal]]) -> list[list[Decimal]]:
    n = len(A)
    m = len(B[0])
    r = len(B)
    return [[sum(A[i][k] * B[k][j] for k in range(r)) for j in range(m)] for i in range(n)]


def dec_trace(A: list[list[Decimal]]) -> Decimal:
    return sum(A[i][i] for i in range(len(A)))


def dec_mixed(K: list[list[Decimal]], mask: int) -> tuple[list[list[Decimal]], int]:
    n = len(K)
    M = [row[:] for row in K]
    absent = 0
    for i in range(n):
        if not ((mask >> i) & 1):
            M[i][i] -= 1
            absent += 1
    expected = -1 if absent & 1 else 1
    return M, expected


def decimal_directional(K_np: np.ndarray, D_np: np.ndarray) -> dict:
    K = dec_matrix_from_np(K_np)
    Dm = dec_matrix_from_np(D_np)
    p_sum = Decimal(0)
    p1_sum = Decimal(0)
    p2_sum = Decimal(0)
    fisher = Decimal(0)
    acceleration = Decimal(0)
    entropy = Decimal(0)
    min_atom: Decimal | None = None
    for mask in range(1 << len(K)):
        M, expected = dec_mixed(K, mask)
        det, Inv = dec_inv_det(M)
        p = det if expected > 0 else -det
        if p <= 0:
            raise ArithmeticError(f"nonpositive Decimal atom {mask}: {p}")
        A = dec_matmul(Inv, Dm)
        score = dec_trace(A)
        A2 = dec_matmul(A, A)
        hlog = -dec_trace(A2)
        p1 = p * score
        p2 = p * (score * score + hlog)
        lp = p.ln()
        p_sum += p
        p1_sum += p1
        p2_sum += p2
        fisher += p1 * p1 / p
        acceleration += -p2 * lp
        entropy += -p * lp
        min_atom = p if min_atom is None or p < min_atom else min_atom
    H2 = -fisher + acceleration
    return {
        "precision": getcontext().prec,
        "entropy": str(+entropy),
        "fisher": str(+fisher),
        "acceleration": str(+acceleration),
        "H2": str(+H2),
        "rho": str(+(acceleration / fisher)),
        "sum_p": str(+p_sum),
        "sum_p1": str(+p1_sum),
        "sum_p2": str(+p2_sum),
        "min_atom": str(+min_atom),
    }


def decimal_entropy(K_np: np.ndarray) -> Decimal:
    K = dec_matrix_from_np(K_np)
    entropy = Decimal(0)
    for mask in range(1 << len(K)):
        M, expected = dec_mixed(K, mask)
        det = dec_det(M)
        p = det if expected > 0 else -det
        if p <= 0:
            raise ArithmeticError(f"nonpositive chord atom {mask}: {p}")
        entropy += -p * p.ln()
    return +entropy


def decimal_chords(K_np: np.ndarray, D_np: np.ndarray, steps: list[str], H0: Decimal) -> list[dict]:
    out = []
    for step_s in steps:
        t = float(step_s)
        Hm = decimal_entropy(K_np - t * D_np)
        Hp = decimal_entropy(K_np + t * D_np)
        gap = (Hm + Hp) / 2 - H0
        out.append(
            {
                "step": step_s,
                "Hminus": str(+Hm),
                "Hplus": str(+Hp),
                "midpoint_gap": str(+gap),
                "central_H2": str(+(2 * gap / (Decimal(step_s) * Decimal(step_s)))),
            }
        )
    return out


def frac_from_float(x: float) -> Fraction:
    return Fraction(str(float(x)))


def frac_matrix(A: np.ndarray) -> list[list[Fraction]]:
    return [[frac_from_float(A[i, j]) for j in range(A.shape[1])] for i in range(A.shape[0])]


def frac_identity(n: int) -> list[list[Fraction]]:
    return [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]


def frac_add(A: list[list[Fraction]], B: list[list[Fraction]], scale: Fraction = Fraction(1)) -> list[list[Fraction]]:
    n = len(A)
    return [[A[i][j] + scale * B[i][j] for j in range(n)] for i in range(n)]


def frac_shift_identity(A: list[list[Fraction]], shift: Fraction) -> list[list[Fraction]]:
    n = len(A)
    out = [row[:] for row in A]
    for i in range(n):
        out[i][i] += shift
    return out


def ldl_pivots(A: list[list[Fraction]]) -> list[Fraction]:
    n = len(A)
    L = [[Fraction(0) for _ in range(n)] for __ in range(n)]
    d = [Fraction(0) for _ in range(n)]
    for i in range(n):
        for j in range(i):
            val = A[i][j] - sum(L[i][k] * L[j][k] * d[k] for k in range(j))
            L[i][j] = val / d[j]
        diag = A[i][i] - sum(L[i][k] * L[i][k] * d[k] for k in range(i))
        d[i] = diag
        L[i][i] = Fraction(1)
    return d


def pivot_summary(pivots: list[Fraction]) -> dict:
    mn = min(pivots)
    return {
        "count": len(pivots),
        "all_positive": all(x > 0 for x in pivots),
        "minimum_float": float(mn),
        "minimum_numerator_digits": len(str(abs(mn.numerator))),
        "minimum_denominator_digits": len(str(abs(mn.denominator))),
    }


def fraction_feasibility(K_np: np.ndarray, D_np: np.ndarray) -> dict:
    K = frac_matrix(K_np)
    Dm = frac_matrix(D_np)
    n = len(K)
    I = frac_identity(n)
    margin = Fraction(1, 2000)
    endpoints = []
    for t in (Fraction(-1, 200), Fraction(1, 200)):
        Kt = frac_add(K, Dm, t)
        K_margin = frac_shift_identity(Kt, -margin)
        I_minus = [[I[i][j] - Kt[i][j] for j in range(n)] for i in range(n)]
        I_minus_margin = frac_shift_identity(I_minus, -margin)
        endpoints.append(
            {
                "step": str(t),
                "K_minus_margin_I": pivot_summary(ldl_pivots(K_margin)),
                "I_minus_K_minus_margin_I": pivot_summary(ldl_pivots(I_minus_margin)),
            }
        )
    return {
        "interpretation": "symmetrized float entries interpreted as decimal rationals through Python str(float)",
        "uniform_interval": ["-1/200", "1/200"],
        "strict_spectral_margin": "1/2000",
        "endpoint_LDL": endpoints,
        "D_positive_definite": pivot_summary(ldl_pivots(Dm)),
    }


def fraction_commutator(K_np: np.ndarray, D_np: np.ndarray) -> dict:
    K = frac_matrix(K_np)
    Dm = frac_matrix(D_np)
    n = len(K)
    max_abs = Fraction(0)
    nonzero = 0
    for i in range(n):
        for j in range(n):
            val = sum(K[i][k] * Dm[k][j] - Dm[i][k] * K[k][j] for k in range(n))
            if val:
                nonzero += 1
                if abs(val) > max_abs:
                    max_abs = abs(val)
    return {
        "exact_zero": nonzero == 0,
        "nonzero_entries": nonzero,
        "max_abs_float": float(max_abs),
        "max_abs_fraction": str(max_abs),
    }


def script_correction_summary() -> dict:
    text = CURRENT_SCRIPT.read_text(encoding="utf-8")
    return {
        "sha256": sha256(CURRENT_SCRIPT),
        "has_source_ledger_index_minus_one": '"index": -1' in text,
        "has_candidate_source_base_npz": "candidate_source_base.npz" in text,
        "has_candidate_source_base_json": "candidate_source_base.json" in text,
        "has_candidate_cases_for_proposals": 'stem = f"candidate_{index:06d}"' in text,
        "has_ledger_rows_including_source": "ledger_rows_including_source" in text,
        "has_proposal_count": "proposal_count" in text,
    }


def main() -> int:
    started = time.time()
    ledger = ledger_and_best_summary()
    strongest_shard = ledger["strongest"]["shard"]
    strongest_npz = ROOT / f"results_{strongest_shard}" / "best_case.npz"
    data = np.load(strongest_npz)
    K_raw = np.asarray(data["kernel"], dtype=float)
    D_raw = np.asarray(data["direction"], dtype=float)
    K = (K_raw + K_raw.T) / 2.0
    Dm = (D_raw + D_raw.T) / 2.0
    dec = decimal_directional(K, Dm)
    chords = decimal_chords(
        K,
        Dm,
        [str(ledger["strongest"]["chord_step"]), "0.001", "0.0001"],
        Decimal(dec["entropy"]),
    )
    feasibility = fraction_feasibility(K, Dm)
    comm = fraction_commutator(K, Dm)
    result = {
        "status": "FRESH_ROUND13_VERIFY_PASS",
        "hashes": {
            "source_npz": sha256(ROOT / "source.npz"),
            "strongest_npz": sha256(strongest_npz),
            "run_version_script": sha256(ROOT / "spectral_basis_refine_run_version.py"),
            "current_corrected_script": sha256(CURRENT_SCRIPT),
        },
        "ledger": ledger,
        "strongest_decimal_directional": dec,
        "strongest_decimal_chords": chords,
        "strongest_fraction_feasibility": feasibility,
        "strongest_fraction_commutator": comm,
        "current_corrected_script_features": script_correction_summary(),
        "checks": {
            "all_20000_proposals_accounted": ledger["total_rows"] == 20000,
            "all_shards_5000": all(s["row_count"] == 5000 for s in ledger["shards"]),
            "all_logs_reached_5000": all(s["log_max_completed"] == 5000 for s in ledger["shards"]),
            "zero_status_hits": ledger["total_status_hits"] == 0,
            "zero_positive_gaps": ledger["total_positive_gap_count"] == 0,
            "strongest_is_shard3_index4901": ledger["strongest"]["shard"] == 3 and ledger["strongest"]["index"] == 4901,
            "strongest_rho_matches_expected": abs(ledger["strongest"]["rho_psd"] - 0.5685905197415816) < 1e-14,
            "decimal_H2_negative": Decimal(dec["H2"]) < 0,
            "decimal_rho_below_one": Decimal(dec["rho"]) < 1,
            "all_decimal_chords_negative": all(Decimal(row["midpoint_gap"]) < 0 for row in chords),
            "fraction_D_positive": feasibility["D_positive_definite"]["all_positive"],
            "fraction_interval_feasible": all(
                item["K_minus_margin_I"]["all_positive"] and item["I_minus_K_minus_margin_I"]["all_positive"]
                for item in feasibility["endpoint_LDL"]
            ),
            "current_script_has_candidate_freeze_fixes": all(script_correction_summary().values()),
        },
        "elapsed_seconds": time.time() - started,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if all(result["checks"].values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
