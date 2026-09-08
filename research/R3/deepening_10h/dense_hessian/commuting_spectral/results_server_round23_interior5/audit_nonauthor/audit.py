#!/usr/bin/env python3
"""
D10-H15 / round23_interior5 fresh audit.

No author recheck/search/gate module is imported or called.  The script reads
the frozen CSV/JSON/NPZ artifacts, independently audits ledger consistency, and
recomputes the strongest point from exact-event Mobius atoms and determinant
jets using Decimal arithmetic.

The result is finite SCOUT evidence only.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import sys
import time
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

import numpy as np


BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
COMMUTING_ROOT = ROOT.parent
N = 12
MASK_COUNT = 1 << N


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def audit_ledgers() -> Dict[str, Any]:
    per = []
    global_rows = 0
    proposal_rows = 0
    source_rows = 0
    rho_ge_1 = 0
    positive_gap = 0
    non_no_hit = 0
    best: Tuple[float, int, Dict[str, str]] = (-1.0, -1, {})
    for shard in range(4):
        sp = ROOT / f"results_{shard}"
        manifest = read_json(sp / "manifest.json")
        best_json = read_json(sp / "best_case.json")
        rows: List[Dict[str, str]]
        with (sp / "candidate_ledger.csv").open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        this_source = [r for r in rows if r["index"] == "-1"]
        this_prop = [r for r in rows if r["index"] != "-1"]
        indices = sorted(int(r["index"]) for r in this_prop)
        statuses = {}
        for r in rows:
            statuses[r["status"]] = statuses.get(r["status"], 0) + 1
        accepted_prop = sum(r["accepted"] == "True" for r in this_prop)
        rho_ge = sum(float(r["rho_psd"]) >= 1.0 for r in rows)
        pos_gap = sum(float(r["chord_gap"]) > 0.0 for r in rows)
        non_no = sum(r["status"] != "NO_HIT" for r in rows)
        min_margin_prop = min(float(r["spectrum_margin"]) for r in this_prop)
        source_margin = float(this_source[0]["spectrum_margin"]) if this_source else float("nan")
        max_gap = max(float(r["chord_gap"]) for r in rows)
        best_row = max(rows, key=lambda r: float(r["rho_psd"]))
        best_rho = float(best_row["rho_psd"])
        if best_rho > best[0]:
            best = (best_rho, shard, best_row)
        fields_to_match = [
            "index",
            "label",
            "accepted",
            "rho_psd",
            "rho_unrestricted",
            "unrestricted_same_sign",
            "total_psd_fisher_normalized",
            "min_atom",
            "direction_min_rate",
            "direction_max_rate",
            "chord_gap",
            "spectrum_margin",
            "status",
        ]
        best_matches_json = all(str(best_json[k]) == str(best_row[k]) for k in fields_to_match)
        per.append(
            {
                "shard": shard,
                "rows": len(rows),
                "source_rows": len(this_source),
                "proposal_rows": len(this_prop),
                "proposal_indices_are_0_to_4999": indices == list(range(5000)),
                "accepted_proposals_from_csv": accepted_prop,
                "accepted_count_manifest": manifest["accepted_count"],
                "accepted_count_matches_manifest": accepted_prop == manifest["accepted_count"],
                "manifest_status": manifest["status"],
                "manifest_exit_code": manifest["exit_code"],
                "manifest_positive_count": manifest["positive_count"],
                "manifest_proposal_count": manifest["proposal_count"],
                "manifest_margin_floor": manifest["margin_floor"],
                "min_proposal_spectrum_margin": min_margin_prop,
                "source_spectrum_margin": source_margin,
                "rho_ge_1_rows": rho_ge,
                "positive_gap_rows": pos_gap,
                "non_NO_HIT_status_rows": non_no,
                "status_counts": statuses,
                "max_gap": max_gap,
                "best_row_by_csv": best_row,
                "best_json_matches_csv_best": best_matches_json,
                "best_case_json_sha256": sha256_file(sp / "best_case.json"),
                "best_case_npz_sha256": sha256_file(sp / "best_case.npz"),
                "candidate_ledger_sha256": sha256_file(sp / "candidate_ledger.csv"),
                "manifest_sha256": sha256_file(sp / "manifest.json"),
            }
        )
        global_rows += len(rows)
        proposal_rows += len(this_prop)
        source_rows += len(this_source)
        rho_ge_1 += rho_ge
        positive_gap += pos_gap
        non_no_hit += non_no
    return {
        "per_shard": per,
        "global_rows": global_rows,
        "proposal_rows": proposal_rows,
        "source_rows": source_rows,
        "rho_ge_1_rows": rho_ge_1,
        "positive_gap_rows": positive_gap,
        "non_NO_HIT_status_rows": non_no_hit,
        "best_overall_by_csv": {"rho": best[0], "shard": best[1], "row": best[2]},
        "checks": {
            "four_shards": len(per) == 4,
            "rows_20004": global_rows == 20004,
            "proposal_rows_20000": proposal_rows == 20000,
            "source_rows_4": source_rows == 4,
            "each_shard_5001": all(p["rows"] == 5001 for p in per),
            "one_source_each_shard": all(p["source_rows"] == 1 for p in per),
            "all_indices_0_to_4999": all(p["proposal_indices_are_0_to_4999"] for p in per),
            "accepted_counts_match": all(p["accepted_count_matches_manifest"] for p in per),
            "manifest_positive_counts_zero": all(p["manifest_positive_count"] == 0 for p in per),
            "manifest_exit_codes_zero": all(p["manifest_exit_code"] == 0 for p in per),
            "proposal_margin_floor_ge_0_30": all(p["min_proposal_spectrum_margin"] >= 0.3 - 1e-15 for p in per),
            "source_margin_ge_0_32_minus_roundoff": all(p["source_spectrum_margin"] >= 0.32 - 1e-14 for p in per),
            "rho_ge_1_zero": rho_ge_1 == 0,
            "positive_gap_zero": positive_gap == 0,
            "all_status_NO_HIT": non_no_hit == 0,
            "all_best_json_match_csv": all(p["best_json_matches_csv_best"] for p in per),
            "best_is_shard3_index2902": best[1] == 3 and best[2].get("index") == "2902",
        },
    }


def D_from_float(x: float) -> Decimal:
    return Decimal(repr(float(x)))


def decimal_matrix_from_np(A: np.ndarray) -> List[List[Decimal]]:
    S = (A + A.T) / 2.0
    return [[D_from_float(S[i, j]) for j in range(S.shape[1])] for i in range(S.shape[0])]


def submatrix(M: List[List[Decimal]], idx: List[int]) -> List[List[Decimal]]:
    return [[M[i][j] for j in idx] for i in idx]


def det_inv(A: List[List[Decimal]]) -> Tuple[Decimal, List[List[Decimal]]]:
    n = len(A)
    if n == 0:
        return Decimal(1), []
    M = [row[:] + [Decimal(1 if i == j else 0) for j in range(n)] for i, row in enumerate(A)]
    det = Decimal(1)
    sign = 1
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        pv = M[piv][col]
        if pv == 0:
            raise ZeroDivisionError("singular principal minor")
        if piv != col:
            M[col], M[piv] = M[piv], M[col]
            sign *= -1
        pv = M[col][col]
        det *= pv
        for j in range(col, 2 * n):
            M[col][j] /= pv
        for i in range(n):
            if i == col:
                continue
            fac = M[i][col]
            if fac:
                for j in range(col, 2 * n):
                    M[i][j] -= fac * M[col][j]
    if sign < 0:
        det = -det
    return det, [row[n:] for row in M]


def det_only(A: List[List[Decimal]]) -> Decimal:
    n = len(A)
    if n == 0:
        return Decimal(1)
    M = [row[:] for row in A]
    det = Decimal(1)
    sign = 1
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        pv = M[piv][col]
        if pv == 0:
            return Decimal(0)
        if piv != col:
            M[col], M[piv] = M[piv], M[col]
            sign *= -1
        pv = M[col][col]
        det *= pv
        for i in range(col + 1, n):
            fac = M[i][col] / pv
            if fac:
                for j in range(col, n):
                    M[i][j] -= fac * M[col][j]
    return -det if sign < 0 else det


def matmul_small(A: List[List[Decimal]], B: List[List[Decimal]]) -> List[List[Decimal]]:
    n, m, p = len(A), len(B), len(B[0])
    C = [[Decimal(0) for _ in range(p)] for _ in range(n)]
    for i in range(n):
        for k in range(m):
            aik = A[i][k]
            if aik:
                for j in range(p):
                    C[i][j] += aik * B[k][j]
    return C


def trace_small(A: List[List[Decimal]]) -> Decimal:
    return sum(A[i][i] for i in range(len(A)))


def mobius_superset(vals: List[Decimal], n: int) -> List[Decimal]:
    out = vals[:]
    for bit in range(n):
        step = 1 << bit
        for mask in range(1 << n):
            if (mask & step) == 0:
                out[mask] -= out[mask | step]
    return out


def inclusion_jets(K: List[List[Decimal]], V: List[List[Decimal]]) -> Tuple[List[Decimal], List[Decimal], List[Decimal]]:
    q = [Decimal(0)] * MASK_COUNT
    q1 = [Decimal(0)] * MASK_COUNT
    q2 = [Decimal(0)] * MASK_COUNT
    indices_by_mask = [[i for i in range(N) if (mask >> i) & 1] for mask in range(MASK_COUNT)]
    for mask, idx in enumerate(indices_by_mask):
        if not idx:
            q[mask] = Decimal(1)
            continue
        A = submatrix(K, idx)
        B = submatrix(V, idx)
        detA, invA = det_inv(A)
        X = matmul_small(invA, B)
        trX = trace_small(X)
        X2 = matmul_small(X, X)
        trX2 = trace_small(X2)
        q[mask] = detA
        q1[mask] = detA * trX
        q2[mask] = detA * (trX * trX - trX2)
    return q, q1, q2


def atoms_only(K: List[List[Decimal]]) -> List[Decimal]:
    q = [Decimal(0)] * MASK_COUNT
    indices_by_mask = [[i for i in range(N) if (mask >> i) & 1] for mask in range(MASK_COUNT)]
    for mask, idx in enumerate(indices_by_mask):
        q[mask] = det_only(submatrix(K, idx)) if idx else Decimal(1)
    return mobius_superset(q, N)


def entropy_from_atoms(p: List[Decimal]) -> Decimal:
    return -sum(x * x.ln() for x in p)


def directional_decimal(K_np: np.ndarray, D_np: np.ndarray, dps: int = 130) -> Dict[str, Any]:
    with localcontext() as ctx:
        ctx.prec = dps
        K = decimal_matrix_from_np(K_np)
        V = decimal_matrix_from_np(D_np)
        q, q1, q2 = inclusion_jets(K, V)
        p = mobius_superset(q, N)
        p1 = mobius_superset(q1, N)
        p2 = mobius_superset(q2, N)
        logs = [x.ln() for x in p]
        entropy = -sum(p[i] * logs[i] for i in range(MASK_COUNT))
        fisher = sum(p1[i] * p1[i] / p[i] for i in range(MASK_COUNT))
        acceleration = -sum(p2[i] * logs[i] for i in range(MASK_COUNT))
        H2 = acceleration - fisher
        rho = acceleration / fisher
        return {
            "precision": dps,
            "event_count": MASK_COUNT,
            "entropy": str(+entropy),
            "fisher": str(+fisher),
            "acceleration": str(+acceleration),
            "H2": str(+H2),
            "rho": str(+rho),
            "sum_p_minus_one": str(+(sum(p) - Decimal(1))),
            "sum_p1": str(+sum(p1)),
            "sum_p2": str(+sum(p2)),
            "min_atom": str(+min(p)),
            "min_atom_index": int(min(range(MASK_COUNT), key=lambda i: p[i])),
        }


def add_scaled(K: List[List[Decimal]], V: List[List[Decimal]], h: Decimal) -> List[List[Decimal]]:
    return [[K[i][j] + h * V[i][j] for j in range(N)] for i in range(N)]


def chord_checks(K_np: np.ndarray, D_np: np.ndarray, steps: Sequence[str], dps: int = 125) -> List[Dict[str, Any]]:
    out = []
    with localcontext() as ctx:
        ctx.prec = dps
        K = decimal_matrix_from_np(K_np)
        V = decimal_matrix_from_np(D_np)
        H0 = entropy_from_atoms(atoms_only(K))
        for step in steps:
            h = Decimal(step)
            Hp = entropy_from_atoms(atoms_only(add_scaled(K, V, h)))
            Hm = entropy_from_atoms(atoms_only(add_scaled(K, V, -h)))
            gap = (Hp + Hm) / Decimal(2) - H0
            central = (Hp - 2 * H0 + Hm) / (h * h)
            out.append(
                {
                    "step": step,
                    "Hminus": str(+Hm),
                    "Hplus": str(+Hp),
                    "midpoint_gap": str(+gap),
                    "central_H2": str(+central),
                }
            )
    return out


def frac_from_float(x: float) -> Fraction:
    return Fraction(repr(float(x)))


def fraction_sym_matrix(A: np.ndarray) -> List[List[Fraction]]:
    S = [[Fraction(0) for _ in range(A.shape[0])] for _ in range(A.shape[0])]
    for i in range(A.shape[0]):
        for j in range(A.shape[0]):
            S[i][j] = (frac_from_float(A[i, j]) + frac_from_float(A[j, i])) / 2
    return S


def ldl_fraction(M: List[List[Fraction]]) -> List[Fraction]:
    n = len(M)
    L = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    piv = [Fraction(0) for _ in range(n)]
    for i in range(n):
        L[i][i] = Fraction(1)
    for j in range(n):
        val = M[j][j]
        for k in range(j):
            val -= L[j][k] * L[j][k] * piv[k]
        piv[j] = val
        for i in range(j + 1, n):
            val2 = M[i][j]
            for k in range(j):
                val2 -= L[i][k] * L[j][k] * piv[k]
            L[i][j] = val2 / piv[j]
    return piv


def mat_fraction_combo(K: List[List[Fraction]], Dm: List[List[Fraction]], t: Fraction, margin: Fraction, complement: bool) -> List[List[Fraction]]:
    n = len(K)
    M = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            base = (Fraction(1) if i == j else Fraction(0)) - K[i][j] if complement else K[i][j]
            dirpart = -t * Dm[i][j] if complement else t * Dm[i][j]
            M[i][j] = base + dirpart - (margin if i == j else Fraction(0))
    return M


def fraction_ldl_checks(K_np: np.ndarray, D_np: np.ndarray) -> Dict[str, Any]:
    K = fraction_sym_matrix(K_np)
    Dm = fraction_sym_matrix(D_np)
    margin = Fraction(1, 2000)
    checks = {}
    for label, M in [
        ("D_positive_definite", Dm),
        ("K_minus_margin_I", mat_fraction_combo(K, Dm, Fraction(0), margin, False)),
        ("I_minus_K_minus_margin_I", mat_fraction_combo(K, Dm, Fraction(0), margin, True)),
    ]:
        piv = ldl_fraction(M)
        checks[label] = {
            "all_positive": all(x > 0 for x in piv),
            "minimum_float": float(min(piv)),
            "count": len(piv),
            "minimum_numerator_digits": len(str(abs(min(piv).numerator))),
            "minimum_denominator_digits": len(str(abs(min(piv).denominator))),
        }
    endpoints = []
    for t in [Fraction(-1, 200), Fraction(1, 200)]:
        Kp = ldl_fraction(mat_fraction_combo(K, Dm, t, margin, False))
        IKp = ldl_fraction(mat_fraction_combo(K, Dm, t, margin, True))
        endpoints.append(
            {
                "step": f"{t.numerator}/{t.denominator}",
                "K_plus_tD_minus_margin_I": {
                    "all_positive": all(x > 0 for x in Kp),
                    "minimum_float": float(min(Kp)),
                    "count": len(Kp),
                    "minimum_numerator_digits": len(str(abs(min(Kp).numerator))),
                    "minimum_denominator_digits": len(str(abs(min(Kp).denominator))),
                },
                "I_minus_K_minus_tD_minus_margin_I": {
                    "all_positive": all(x > 0 for x in IKp),
                    "minimum_float": float(min(IKp)),
                    "count": len(IKp),
                    "minimum_numerator_digits": len(str(abs(min(IKp).numerator))),
                    "minimum_denominator_digits": len(str(abs(min(IKp).denominator))),
                },
            }
        )
    checks["endpoints"] = endpoints
    checks["uniform_interval"] = ["-1/200", "1/200"]
    checks["strict_spectral_margin"] = "1/2000"
    checks["all_pass"] = (
        checks["D_positive_definite"]["all_positive"]
        and all(e["K_plus_tD_minus_margin_I"]["all_positive"] and e["I_minus_K_minus_tD_minus_margin_I"]["all_positive"] for e in endpoints)
    )
    return checks


def float_npz_diagnostics(npz_path: Path) -> Dict[str, Any]:
    data = np.load(npz_path, allow_pickle=False)
    K = (data["kernel"] + data["kernel"].T) / 2.0
    Dm = (data["direction"] + data["direction"].T) / 2.0
    evK = np.linalg.eigvalsh(K)
    evD = np.linalg.eigvalsh(Dm)
    comm = K @ Dm - Dm @ K
    return {
        "keys": list(data.files),
        "kernel_shape": list(K.shape),
        "direction_shape": list(Dm.shape),
        "K_min": float(evK[0]),
        "K_max": float(evK[-1]),
        "K_spectrum_margin": float(min(evK[0], 1 - evK[-1])),
        "D_min": float(evD[0]),
        "D_max": float(evD[-1]),
        "commutator_frobenius": float(np.linalg.norm(comm, ord="fro")),
        "kernel_max_asymmetry": float(np.max(np.abs(data["kernel"] - data["kernel"].T))),
        "direction_max_asymmetry": float(np.max(np.abs(data["direction"] - data["direction"].T))),
        "basis_orthogonality_residual": float(np.linalg.norm(data["eigenvectors"].T @ data["eigenvectors"] - np.eye(N), ord="fro")),
        "rates_min": float(np.min(data["rates"])),
        "rates_max": float(np.max(data["rates"])),
    }


def profile_H10_to_H15() -> List[Dict[str, Any]]:
    specs = [
        ("H10_round18_boundary1", "results_server_round18_boundary1", "recheck_best_boundary1.json"),
        ("H11_round19_interior1", "results_server_round19_interior1", "recheck_best_interior1.json"),
        ("H12_round20_interior2", "results_server_round20_interior2", "recheck_best_interior2.json"),
        ("H13_round21_interior3", "results_server_round21_interior3", "recheck_best_interior3.json"),
        ("H14_round22_interior4", "results_server_round22_interior4", "recheck_best_interior4.json"),
        ("H15_round23_interior5", "results_server_round23_interior5", "recheck_best_interior5.json"),
    ]
    out = []
    for label, dname, fname in specs:
        p = COMMUTING_ROOT / dname / fname
        if not p.exists():
            out.append({"label": label, "missing": True})
            continue
        data = read_json(p)
        row = data.get("ledger", {}).get("best_row", {})
        out.append(
            {
                "label": label,
                "path": str(p.relative_to(COMMUTING_ROOT)),
                "rho_psd": float(row.get("rho_psd", "nan")),
                "spectrum_margin": float(row.get("spectrum_margin", "nan")),
                "shard": row.get("_shard") or row.get("shard"),
                "index": row.get("index"),
                "max_gap": data.get("ledger", {}).get("maximum_gap"),
                "sha256": sha256_file(p),
            }
        )
    return out


def main() -> int:
    t0 = time.time()
    ledgers = audit_ledgers()
    recheck = read_json(ROOT / "recheck_best_interior5.json")
    best_npz = ROOT / "results_3" / "best_case.npz"
    best_json = read_json(ROOT / "results_3" / "best_case.json")
    npz_data = np.load(best_npz, allow_pickle=False)
    K_np = npz_data["kernel"]
    D_np = npz_data["direction"]
    directional = directional_decimal(K_np, D_np, dps=130)
    chords = chord_checks(K_np, D_np, ["0.01", "0.001", "0.0001"], dps=125)
    frac = fraction_ldl_checks(K_np, D_np)
    diag = float_npz_diagnostics(best_npz)
    profile = profile_H10_to_H15()
    input_files = [
        ROOT / "README.md",
        ROOT / "recheck_best_interior5.json",
        ROOT / "interior_source_margin032.json",
        ROOT / "interior_source_margin032.npz",
        ROOT / "commuting_spectral_search.py",
        ROOT / "spectral_basis_refine.py",
        ROOT / "prepare_interior_source.py",
        ROOT / "recheck_best_interior5.py",
    ]
    for s in range(4):
        input_files += [
            ROOT / f"results_{s}" / "candidate_ledger.csv",
            ROOT / f"results_{s}" / "manifest.json",
            ROOT / f"results_{s}" / "best_case.json",
            ROOT / f"results_{s}" / "best_case.npz",
            ROOT / f"run_{s}.log",
        ]
    hashes = {p.relative_to(ROOT).as_posix(): sha256_file(p) for p in input_files if p.exists()}
    checks = {
        "ledger_checks_pass": all(ledgers["checks"].values()),
        "best_npz_hash_matches_recheck": hashes["results_3/best_case.npz"] == recheck["hashes"]["best_case_npz"],
        "source_npz_hash_matches_recheck": hashes["interior_source_margin032.npz"] == recheck["hashes"]["source_npz"],
        "best_json_index_matches": str(best_json["index"]) == "2902",
        "best_json_rho_matches_readme_target": abs(float(best_json["rho_psd"]) - 0.15219460446316677) < 1e-16,
        "decimal_rho_below_one": Decimal(directional["rho"]) < 1,
        "decimal_H2_negative": Decimal(directional["H2"]) < 0,
        "decimal_fisher_positive": Decimal(directional["fisher"]) > 0,
        "three_chords_negative": all(Decimal(c["midpoint_gap"]) < 0 for c in chords),
        "fraction_ldl_feasible": frac["all_pass"],
        "margin_floor_npz": diag["K_spectrum_margin"] >= 0.3 - 1e-14,
        "D_positive_float": diag["D_min"] > 0,
        "rho_close_to_author_decimal": abs(float(Decimal(directional["rho"])) - float(recheck["decimal_directional"][-1]["rho"])) < 1e-12,
        "H2_close_to_author_decimal": abs(float(Decimal(directional["H2"])) - float(recheck["decimal_directional"][-1]["H2"])) < 1e-10,
    }
    status = "SCOUT_CORRECT" if all(checks.values()) else "SCOUT_CRITICAL_GAPS"
    results = {
        "status": status,
        "scope": "finite SCOUT only; no theorem/global bound certified",
        "input_hashes": hashes,
        "ledger": ledgers,
        "strongest": {
            "expected_shard": 3,
            "expected_index": 2902,
            "best_case_json": best_json,
            "npz_sha256": hashes["results_3/best_case.npz"],
            "npz_diagnostics": diag,
        },
        "directional_130_digit": directional,
        "chords_125_digit": chords,
        "fraction_ldl": frac,
        "profile_H10_to_H15": profile,
        "checks": checks,
        "author_reference_values": {
            "recheck_status": recheck.get("status"),
            "author_decimal_last": recheck.get("decimal_directional", [])[-1],
            "author_chords": recheck.get("decimal_chords"),
            "author_fraction_feasibility": recheck.get("exact_fraction_feasibility"),
        },
        "elapsed_seconds": time.time() - t0,
    }
    (BASE / "results.json").write_text(json.dumps(results, indent=2, sort_keys=True), encoding="utf-8")
    run_log = [
        "# D10-H15 round23_interior5 non-author audit run log",
        "",
        f"Command: `{Path(sys.executable)} {Path(__file__).name}`",
        "Exit code: `0`",
        f"Elapsed seconds: `{results['elapsed_seconds']:.6f}`",
        "No author recheck/search/gate module was imported or called.",
        "",
        f"Status: `{status}`",
        f"CSV rows: `{ledgers['global_rows']}`; proposals `{ledgers['proposal_rows']}`; sources `{ledgers['source_rows']}`",
        f"Best row: shard `{ledgers['best_overall_by_csv']['shard']}`, index `{ledgers['best_overall_by_csv']['row'].get('index')}`, rho `{ledgers['best_overall_by_csv']['rho']}`",
        f"130-digit rho: `{directional['rho']}`",
        f"130-digit H2: `{directional['H2']}`",
        f"Fraction LDL feasible on |t|<=1/200 with 1/2000 margin: `{frac['all_pass']}`",
    ]
    (BASE / "run_log.md").write_text("\n".join(run_log) + "\n", encoding="utf-8")
    print(json.dumps({"status": status, "rows": ledgers["global_rows"], "rho": directional["rho"], "H2": directional["H2"], "frac": frac["all_pass"], "elapsed": results["elapsed_seconds"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
