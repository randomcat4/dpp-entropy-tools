"""Fresh non-author audit for D10-H10 / round18_boundary1.

This script intentionally does not import the author's recheck wrapper,
round14 gate, spectral search, or refinement modules.  It treats the saved
CSV/JSON/NPZ/log artifacts as data, reconstructs exact-event probabilities
from inclusion determinants by Mobius inversion, and performs a separate
Fraction-LDL feasibility certificate on the symmetrized decimal rational
entries stored in the strongest NPZ.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import time
from collections import Counter
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np


DECIMAL_PRECISION = 120
getcontext().prec = DECIMAL_PRECISION


def repo_round_dir() -> Path:
    return Path(__file__).resolve().parents[1]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def d_from_float(x: float) -> Decimal:
    return Decimal.from_float(float(x))


def f_from_float(x: float) -> Fraction:
    return Fraction(repr(float(x)))


def sym_decimal_matrix(a: np.ndarray) -> list[list[Decimal]]:
    n = a.shape[0]
    return [
        [(d_from_float(a[i, j]) + d_from_float(a[j, i])) / Decimal(2) for j in range(n)]
        for i in range(n)
    ]


def sym_fraction_matrix(a: np.ndarray) -> list[list[Fraction]]:
    n = a.shape[0]
    return [
        [(f_from_float(a[i, j]) + f_from_float(a[j, i])) / 2 for j in range(n)]
        for i in range(n)
    ]


def decimal_matrix_from_shift(
    k_mat: list[list[Decimal]], d_mat: list[list[Decimal]], h: Decimal
) -> list[list[Decimal]]:
    n = len(k_mat)
    return [[k_mat[i][j] + h * d_mat[i][j] for j in range(n)] for i in range(n)]


def subset_matrix(mat: list[list[Any]], idx: list[int]) -> list[list[Any]]:
    return [[mat[i][j] for j in idx] for i in idx]


def det_decimal(a: list[list[Decimal]]) -> Decimal:
    n = len(a)
    if n == 0:
        return Decimal(1)
    m = [[a[i][j] for j in range(n)] for i in range(n)]
    det = Decimal(1)
    sign = 1
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(m[r][col]))
        pv = m[pivot][col]
        if pv == 0:
            return Decimal(0)
        if pivot != col:
            m[col], m[pivot] = m[pivot], m[col]
            sign = -sign
        pv = m[col][col]
        det *= pv
        for r in range(col + 1, n):
            factor = m[r][col] / pv
            if factor:
                m[r][col] = Decimal(0)
                for c in range(col + 1, n):
                    m[r][c] -= factor * m[col][c]
    return det if sign > 0 else -det


def det_inv_decimal(a: list[list[Decimal]]) -> tuple[Decimal, list[list[Decimal]]]:
    n = len(a)
    if n == 0:
        return Decimal(1), []
    width = 2 * n
    m = [
        [a[i][j] for j in range(n)]
        + [Decimal(1) if i == j else Decimal(0) for j in range(n)]
        for i in range(n)
    ]
    det = Decimal(1)
    sign = 1
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(m[r][col]))
        pv = m[pivot][col]
        if pv == 0:
            raise ArithmeticError("singular matrix in Decimal det/inv")
        if pivot != col:
            m[col], m[pivot] = m[pivot], m[col]
            sign = -sign
        pv = m[col][col]
        det *= pv
        inv_pv = Decimal(1) / pv
        for c in range(col, width):
            m[col][c] *= inv_pv
        for r in range(n):
            if r == col:
                continue
            factor = m[r][col]
            if factor:
                m[r][col] = Decimal(0)
                for c in range(col + 1, width):
                    m[r][c] -= factor * m[col][c]
    if sign < 0:
        det = -det
    inv = [[m[i][n + j] for j in range(n)] for i in range(n)]
    return det, inv


def indices_by_mask(n: int) -> list[list[int]]:
    return [[i for i in range(n) if (mask >> i) & 1] for mask in range(1 << n)]


def mobius_from_inclusions(q: list[Decimal], n: int) -> list[Decimal]:
    p = q[:]
    for bit_index in range(n):
        bit = 1 << bit_index
        for mask in range(1 << n):
            if (mask & bit) == 0:
                p[mask] -= p[mask | bit]
    return p


def entropy_from_probs(p: list[Decimal]) -> Decimal:
    total = Decimal(0)
    for x in p:
        if x <= 0:
            raise ArithmeticError(f"non-positive atom probability {x}")
        total -= x * x.ln()
    return total


def inclusion_determinants(
    k_mat: list[list[Decimal]], masks: list[list[int]]
) -> list[Decimal]:
    q: list[Decimal] = []
    for idx in masks:
        q.append(det_decimal(subset_matrix(k_mat, idx)))
    return q


def event_probs_for_kernel(
    k_mat: list[list[Decimal]], masks: list[list[int]], n: int
) -> list[Decimal]:
    return mobius_from_inclusions(inclusion_determinants(k_mat, masks), n)


def entropy_for_kernel(
    k_mat: list[list[Decimal]], masks: list[list[int]], n: int
) -> Decimal:
    return entropy_from_probs(event_probs_for_kernel(k_mat, masks, n))


def exact_event_jets(
    k_mat: list[list[Decimal]], d_mat: list[list[Decimal]], masks: list[list[int]], n: int
) -> dict[str, Any]:
    q0: list[Decimal] = []
    q1: list[Decimal] = []
    q2: list[Decimal] = []
    for idx in masks:
        size = len(idx)
        if size == 0:
            q0.append(Decimal(1))
            q1.append(Decimal(0))
            q2.append(Decimal(0))
            continue
        k_sub = subset_matrix(k_mat, idx)
        d_sub = subset_matrix(d_mat, idx)
        det_k, inv_k = det_inv_decimal(k_sub)
        inv_d = [
            [sum(inv_k[i][ell] * d_sub[ell][j] for ell in range(size)) for j in range(size)]
            for i in range(size)
        ]
        tr = sum(inv_d[i][i] for i in range(size))
        tr2 = sum(inv_d[i][j] * inv_d[j][i] for i in range(size) for j in range(size))
        q0.append(det_k)
        q1.append(det_k * tr)
        q2.append(det_k * (tr * tr - tr2))

    p0 = mobius_from_inclusions(q0, n)
    p1 = mobius_from_inclusions(q1, n)
    p2 = mobius_from_inclusions(q2, n)
    entropy = entropy_from_probs(p0)
    fisher = sum((b * b) / a for a, b in zip(p0, p1))
    acceleration = -sum(c * a.ln() for a, c in zip(p0, p2))
    h2 = acceleration - fisher
    rho = acceleration / fisher
    return {
        "entropy": entropy,
        "fisher": fisher,
        "acceleration": acceleration,
        "H2": h2,
        "rho": rho,
        "sum_p0": sum(p0),
        "sum_p1": sum(p1),
        "sum_p2": sum(p2),
        "min_p0": min(p0),
        "max_abs_p1": max(abs(x) for x in p1),
        "max_abs_p2": max(abs(x) for x in p2),
        "p0": p0,
    }


def ldl_pivots_fraction(a: list[list[Fraction]]) -> dict[str, Any]:
    n = len(a)
    ell = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    pivots: list[Fraction] = []
    for i in range(n):
        ell[i][i] = Fraction(1)
    for j in range(n):
        dj = a[j][j]
        for k in range(j):
            dj -= ell[j][k] * ell[j][k] * pivots[k]
        if dj <= 0:
            return {
                "ok": False,
                "first_bad_index": j,
                "first_bad_pivot": str(dj),
                "positive_pivots": len(pivots),
            }
        pivots.append(dj)
        for i in range(j + 1, n):
            num = a[i][j]
            for k in range(j):
                num -= ell[i][k] * ell[j][k] * pivots[k]
            ell[i][j] = num / dj
    min_index, min_pivot = min(enumerate(pivots), key=lambda item: item[1])
    return {
        "ok": True,
        "pivot_count": len(pivots),
        "min_pivot_index": min_index,
        "min_pivot_float": float(min_pivot),
        "min_pivot_num_digits": len(str(abs(min_pivot.numerator))),
        "min_pivot_den_digits": len(str(abs(min_pivot.denominator))),
    }


def add_fraction_matrices(
    k_mat: list[list[Fraction]],
    d_mat: list[list[Fraction]],
    coef: Fraction,
    diag_shift: Fraction = Fraction(0),
) -> list[list[Fraction]]:
    n = len(k_mat)
    return [
        [k_mat[i][j] + coef * d_mat[i][j] + (diag_shift if i == j else 0) for j in range(n)]
        for i in range(n)
    ]


def identity_minus_shifted_fraction(
    k_mat: list[list[Fraction]],
    d_mat: list[list[Fraction]],
    coef: Fraction,
    diag_shift: Fraction = Fraction(0),
) -> list[list[Fraction]]:
    n = len(k_mat)
    return [
        [
            (Fraction(1) if i == j else Fraction(0))
            - k_mat[i][j]
            - coef * d_mat[i][j]
            + (diag_shift if i == j else 0)
            for j in range(n)
        ]
        for i in range(n)
    ]


def audit_ledgers(root: Path) -> dict[str, Any]:
    manifest_summaries: list[dict[str, Any]] = []
    ledger_summaries: list[dict[str, Any]] = []
    all_rows: list[dict[str, Any]] = []
    strongest: dict[str, Any] | None = None

    for shard in range(4):
        shard_dir = root / f"results_{shard}"
        manifest = json.loads((shard_dir / "manifest.json").read_text(encoding="utf-8"))
        best = json.loads((shard_dir / "best_case.json").read_text(encoding="utf-8"))
        with (shard_dir / "candidate_ledger.csv").open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        status_counts = Counter(row["status"] for row in rows)
        source_rows = [row for row in rows if row["index"] == "-1" and row["label"] == "source_base"]
        proposal_rows = [row for row in rows if row["index"] != "-1"]
        positive_gap_rows = [row for row in rows if Decimal(row["chord_gap"]) > 0]
        non_no_hit_rows = [row for row in rows if row["status"] != "NO_HIT"]
        best_row = max(rows, key=lambda row: Decimal(row["rho_psd"]))
        for row in rows:
            augmented = dict(row)
            augmented["_shard"] = shard
            all_rows.append(augmented)
        if strongest is None or Decimal(best_row["rho_psd"]) > Decimal(strongest["rho_psd"]):
            strongest = dict(best_row)
            strongest["_shard"] = shard

        manifest_summaries.append(
            {
                "shard": shard,
                "manifest": manifest,
                "best_case": best,
                "best_npz_sha256": sha256_file(shard_dir / "best_case.npz"),
                "ledger_row_count": len(rows),
                "proposal_row_count": len(proposal_rows),
                "source_row_count": len(source_rows),
                "status_counts": dict(status_counts),
                "positive_gap_count": len(positive_gap_rows),
                "max_chord_gap": str(max(Decimal(row["chord_gap"]) for row in rows)),
                "best_row_index": best_row["index"],
                "best_row_rho_psd": best_row["rho_psd"],
                "best_json_matches_ledger": (
                    str(best["index"]) == best_row["index"]
                    and abs(float(best["rho_psd"]) - float(best_row["rho_psd"])) <= 1e-15
                    and str(best["status"]) == best_row["status"]
                ),
            }
        )
        ledger_summaries.append(
            {
                "shard": shard,
                "row_count": len(rows),
                "proposal_count": len(proposal_rows),
                "source_count": len(source_rows),
                "non_no_hit_count": len(non_no_hit_rows),
                "positive_gap_count": len(positive_gap_rows),
                "source_margin": source_rows[0]["spectrum_margin"] if source_rows else None,
                "source_rho": source_rows[0]["rho_psd"] if source_rows else None,
            }
        )

    assert strongest is not None
    total_proposals = sum(s["proposal_count"] for s in ledger_summaries)
    total_rows = sum(s["row_count"] for s in ledger_summaries)
    total_source_rows = sum(s["source_count"] for s in ledger_summaries)
    total_non_no_hit = sum(s["non_no_hit_count"] for s in ledger_summaries)
    total_positive_gap = sum(s["positive_gap_count"] for s in ledger_summaries)

    run_log_summaries = []
    for shard in range(4):
        log_path = root / f"run_{shard}.log"
        completed_values = []
        final_json = None
        for raw in log_path.read_text(encoding="utf-8").splitlines():
            raw = raw.strip()
            if not raw.startswith("{"):
                continue
            try:
                obj = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if "completed" in obj:
                completed_values.append(int(obj["completed"]))
            if obj.get("status") == "SCOUT_COMPLETE":
                final_json = obj
        run_log_summaries.append(
            {
                "shard": shard,
                "max_completed": max(completed_values) if completed_values else None,
                "completed_line_count": len(completed_values),
                "has_final_manifest_json": final_json is not None,
                "final_manifest_matches_file": final_json
                == manifest_summaries[shard]["manifest"],
            }
        )

    return {
        "manifest_summaries": manifest_summaries,
        "ledger_summaries": ledger_summaries,
        "run_log_summaries": run_log_summaries,
        "aggregate": {
            "total_rows": total_rows,
            "total_source_rows": total_source_rows,
            "total_proposals": total_proposals,
            "total_non_no_hit": total_non_no_hit,
            "total_positive_gap": total_positive_gap,
            "max_chord_gap": str(max(Decimal(row["chord_gap"]) for row in all_rows)),
            "strongest_shard": strongest["_shard"],
            "strongest_index": int(strongest["index"]),
            "strongest_rho_psd": strongest["rho_psd"],
            "strongest_status": strongest["status"],
            "strongest_spectrum_margin": strongest["spectrum_margin"],
        },
    }


def all_proposal_rows(root: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for shard in range(4):
        shard_dir = root / f"results_{shard}"
        with (shard_dir / "candidate_ledger.csv").open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                if row["index"] == "-1":
                    continue
                augmented = dict(row)
                augmented["_shard"] = shard
                rows.append(augmented)
    return rows


def row_summary(row: dict[str, Any] | None) -> dict[str, Any] | None:
    if row is None:
        return None
    return {
        "shard": int(row["_shard"]),
        "index": int(row["index"]),
        "rho_psd": str(Decimal(row["rho_psd"])),
        "spectrum_margin": str(Decimal(row["spectrum_margin"])),
        "chord_gap": str(Decimal(row["chord_gap"])),
        "status": row["status"],
    }


def profile_best(rows: list[dict[str, Any]]) -> dict[str, Any] | None:
    if not rows:
        return None
    return max(rows, key=lambda row: Decimal(row["rho_psd"]))


def json_best_to_comparable(best: dict[str, Any] | None) -> dict[str, Any] | None:
    if best is None:
        return None
    return {
        "shard": int(best["shard"]),
        "index": int(best["index"]),
        "rho_psd": str(Decimal(repr(float(best["rho_psd"])))),
        "spectrum_margin": str(Decimal(repr(float(best["spectrum_margin"])))),
        "chord_gap": str(Decimal(repr(float(best["chord_gap"])))),
        "status": best["status"],
    }


def same_profile_best(a: dict[str, Any] | None, b: dict[str, Any] | None) -> bool:
    if a is None or b is None:
        return a is None and b is None
    return (
        a["shard"] == b["shard"]
        and a["index"] == b["index"]
        and a["status"] == b["status"]
        and abs(Decimal(a["rho_psd"]) - Decimal(b["rho_psd"])) <= Decimal("1e-15")
        and abs(Decimal(a["spectrum_margin"]) - Decimal(b["spectrum_margin"])) <= Decimal("1e-15")
        and abs(Decimal(a["chord_gap"]) - Decimal(b["chord_gap"])) <= Decimal("1e-15")
    )


def audit_margin_profile(root: Path) -> dict[str, Any]:
    profile_path = root / "margin_profile.json"
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    rows = all_proposal_rows(root)

    threshold_recomputations = []
    for item in profile["threshold_profile"]:
        threshold = Decimal(repr(float(item["minimum_margin"])))
        eligible = [row for row in rows if Decimal(row["spectrum_margin"]) >= threshold]
        recomputed_best = row_summary(profile_best(eligible))
        claimed_best = json_best_to_comparable(item["best"])
        threshold_recomputations.append(
            {
                "minimum_margin": str(threshold),
                "claimed_eligible_rows": int(item["eligible_rows"]),
                "recomputed_eligible_rows": len(eligible),
                "eligible_rows_match": int(item["eligible_rows"]) == len(eligible),
                "claimed_best": claimed_best,
                "recomputed_best": recomputed_best,
                "best_matches": same_profile_best(claimed_best, recomputed_best),
            }
        )

    bin_recomputations = []
    for item in profile["bin_profile"]:
        lower = Decimal(repr(float(item["margin_bin"][0])))
        upper = Decimal(repr(float(item["margin_bin"][1])))
        eligible = [
            row
            for row in rows
            if lower <= Decimal(row["spectrum_margin"]) < upper
        ]
        recomputed_best = row_summary(profile_best(eligible))
        claimed_best = json_best_to_comparable(item["best"])
        bin_recomputations.append(
            {
                "margin_bin": [str(lower), str(upper)],
                "claimed_eligible_rows": int(item["eligible_rows"]),
                "recomputed_eligible_rows": len(eligible),
                "eligible_rows_match": int(item["eligible_rows"]) == len(eligible),
                "claimed_best": claimed_best,
                "recomputed_best": recomputed_best,
                "best_matches": same_profile_best(claimed_best, recomputed_best),
            }
        )

    overall_best = row_summary(profile_best(rows))
    claimed_overall = json_best_to_comparable(profile["overall_best"])
    bin_best_rhos = [
        Decimal(item["recomputed_best"]["rho_psd"])
        for item in bin_recomputations
        if item["recomputed_best"] is not None
    ]
    bin_counts_sum = sum(item["recomputed_eligible_rows"] for item in bin_recomputations)
    readme = (root / "README.md").read_text(encoding="utf-8")
    interpretation = profile.get("interpretation", "")
    finite_language_ok = (
        "finite" in readme.lower()
        and ("not a theorem" in readme.lower() or "replace a theorem" in readme.lower())
        and ("non-monotone" in readme.lower() or "nonmonotone" in readme.lower())
        and "finite" in interpretation.lower()
        and "not a theorem" in interpretation.lower()
        and "monotone" in interpretation.lower()
    )
    return {
        "margin_profile_json_sha256": sha256_file(profile_path),
        "margin_profile_py_sha256": sha256_file(root / "margin_profile.py"),
        "proposal_rows_recomputed": len(rows),
        "claimed_proposal_rows": int(profile["proposal_rows"]),
        "overall_best_claimed": claimed_overall,
        "overall_best_recomputed": overall_best,
        "overall_best_matches": same_profile_best(claimed_overall, overall_best),
        "threshold_profile": threshold_recomputations,
        "bin_profile": bin_recomputations,
        "bin_counts_sum": bin_counts_sum,
        "bin_counts_cover_all_proposals": bin_counts_sum == len(rows),
        "bin_best_rhos": [str(x) for x in bin_best_rhos],
        "bin_best_rhos_non_monotone": not (
            all(bin_best_rhos[i] <= bin_best_rhos[i + 1] for i in range(len(bin_best_rhos) - 1))
            or all(bin_best_rhos[i] >= bin_best_rhos[i + 1] for i in range(len(bin_best_rhos) - 1))
        ),
        "finite_not_theorem_language_ok": finite_language_ok,
        "profile_matches_ledger": (
            len(rows) == int(profile["proposal_rows"]) == 20000
            and same_profile_best(claimed_overall, overall_best)
            and all(item["eligible_rows_match"] and item["best_matches"] for item in threshold_recomputations)
            and all(item["eligible_rows_match"] and item["best_matches"] for item in bin_recomputations)
            and bin_counts_sum == len(rows)
            and finite_language_ok
        ),
    }


def npz_structural_checks(root: Path, shard: int) -> dict[str, Any]:
    path = root / f"results_{shard}" / "best_case.npz"
    data = np.load(path)
    k = np.asarray(data["kernel"], dtype=float)
    d = np.asarray(data["direction"], dtype=float)
    q = np.asarray(data["eigenvectors"], dtype=float)
    spectrum = np.asarray(data["spectrum"], dtype=float)
    rates = np.asarray(data["rates"], dtype=float)
    k_sym = (k + k.T) / 2.0
    d_sym = (d + d.T) / 2.0
    eig_k = np.linalg.eigvalsh(k_sym)
    eig_d = np.linalg.eigvalsh(d_sym)
    return {
        "npz_sha256": sha256_file(path),
        "kernel_asymmetry_max": float(np.max(np.abs(k - k.T))),
        "direction_asymmetry_max": float(np.max(np.abs(d - d.T))),
        "basis_orthogonality_residual_fro": float(np.linalg.norm(q.T @ q - np.eye(q.shape[0]))),
        "kernel_reconstruction_residual_fro": float(np.linalg.norm(k_sym - q @ np.diag(spectrum) @ q.T)),
        "direction_reconstruction_residual_fro": float(np.linalg.norm(d_sym - q @ np.diag(rates) @ q.T)),
        "commutator_residual_fro": float(np.linalg.norm(k_sym @ d_sym - d_sym @ k_sym)),
        "spectrum_min": float(np.min(spectrum)),
        "spectrum_max": float(np.max(spectrum)),
        "computed_spectrum_margin": float(np.min(np.minimum(spectrum, 1.0 - spectrum))),
        "eig_k_min": float(np.min(eig_k)),
        "eig_k_max": float(np.max(eig_k)),
        "rates_min": float(np.min(rates)),
        "rates_max": float(np.max(rates)),
        "eig_d_min": float(np.min(eig_d)),
        "eig_d_max": float(np.max(eig_d)),
    }


def fraction_ldl_certificate(root: Path, shard: int) -> dict[str, Any]:
    data = np.load(root / f"results_{shard}" / "best_case.npz")
    k = sym_fraction_matrix(np.asarray(data["kernel"], dtype=float))
    d = sym_fraction_matrix(np.asarray(data["direction"], dtype=float))
    radius = Fraction(1, 200)
    margin = Fraction(1, 2000)
    certs: dict[str, Any] = {
        "rationalization": "Fraction(repr(float_entry)); matrices are symmetrized entrywise before LDL",
        "D_positive_definite": ldl_pivots_fraction(d),
        "radius": "1/200",
        "margin": "1/2000",
        "endpoint_certificates": {},
    }
    for sign_label, coef in [("plus", radius), ("minus", -radius)]:
        k_margin = add_fraction_matrices(k, d, coef, diag_shift=-margin)
        ik_margin = identity_minus_shifted_fraction(k, d, coef, diag_shift=-margin)
        certs["endpoint_certificates"][sign_label] = {
            "K_sign_radius_D_minus_margin_I": ldl_pivots_fraction(k_margin),
            "I_minus_K_sign_radius_D_minus_margin_I": ldl_pivots_fraction(ik_margin),
        }
    return certs


def decimal_str(x: Decimal, digits: int | None = None) -> str:
    if digits is None:
        return str(+x)
    # Decimal scientific format with a controlled number of significant digits.
    return f"{+x:.{digits}E}"


def high_precision_gate(root: Path, shard: int, chord_steps: list[str]) -> dict[str, Any]:
    data = np.load(root / f"results_{shard}" / "best_case.npz")
    k_dec = sym_decimal_matrix(np.asarray(data["kernel"], dtype=float))
    d_dec = sym_decimal_matrix(np.asarray(data["direction"], dtype=float))
    n = len(k_dec)
    masks = indices_by_mask(n)

    start = time.time()
    jets = exact_event_jets(k_dec, d_dec, masks, n)
    gate_seconds = time.time() - start
    h0 = jets["entropy"]
    chords = []
    for step in chord_steps:
        h = Decimal(step)
        plus = decimal_matrix_from_shift(k_dec, d_dec, h)
        minus = decimal_matrix_from_shift(k_dec, d_dec, -h)
        h_plus = entropy_for_kernel(plus, masks, n)
        h_minus = entropy_for_kernel(minus, masks, n)
        midpoint_gap = (h_plus + h_minus) / Decimal(2) - h0
        chords.append(
            {
                "step": step,
                "H_plus": decimal_str(h_plus, 80),
                "H_minus": decimal_str(h_minus, 80),
                "midpoint_avg_minus_center": decimal_str(midpoint_gap, 80),
                "central_second_difference": decimal_str(
                    Decimal(2) * midpoint_gap / (h * h), 80
                ),
                "negative": midpoint_gap < 0,
            }
        )

    return {
        "decimal_precision": DECIMAL_PRECISION,
        "decimal_input_semantics": "Decimal.from_float on the saved float64 entries, then entrywise symmetrization",
        "event_count": 1 << n,
        "gate_seconds": gate_seconds,
        "entropy": decimal_str(jets["entropy"], 90),
        "fisher": decimal_str(jets["fisher"], 90),
        "acceleration": decimal_str(jets["acceleration"], 90),
        "H2": decimal_str(jets["H2"], 90),
        "rho": decimal_str(jets["rho"], 90),
        "sum_p0_minus_1": decimal_str(jets["sum_p0"] - Decimal(1), 50),
        "sum_p1": decimal_str(jets["sum_p1"], 50),
        "sum_p2": decimal_str(jets["sum_p2"], 50),
        "min_p0": decimal_str(jets["min_p0"], 80),
        "max_abs_p1": decimal_str(jets["max_abs_p1"], 50),
        "max_abs_p2": decimal_str(jets["max_abs_p2"], 50),
        "chords": chords,
    }


def current_script_revision_checks(root: Path) -> dict[str, Any]:
    script = root / "spectral_basis_refine.py"
    text = script.read_text(encoding="utf-8")
    snippets = {
        "source_written_to_ledger": 'writer.writerow(source_row)' in text,
        "source_status_into_positive_count": 'positive_count = int(source_status == "FLOAT_CANDIDATE")' in text,
        "candidate_source_base_npz": "candidate_source_base.npz" in text,
        "proposal_candidate_npz": 'candidate_dir / f"{stem}.npz"' in text,
        "manifest_proposal_count_separate": '"proposal_count": args.centers' in text,
        "manifest_ledger_rows_including_source": '"ledger_rows_including_source": args.centers + 1' in text,
    }
    return {
        "spectral_basis_refine_sha256": sha256_file(script),
        "snippet_checks": snippets,
        "all_required_snippets_present": all(snippets.values()),
    }


def main() -> None:
    root = repo_round_dir()
    ledger = audit_ledgers(root)
    strongest_shard = int(ledger["aggregate"]["strongest_shard"])
    strongest_step = json.loads(
        (root / f"results_{strongest_shard}" / "best_case.json").read_text(encoding="utf-8")
    )["chord_step"]
    chord_steps = [repr(float(strongest_step)), "0.001", "0.0001"]

    print("ledger/log audit complete")
    structural = npz_structural_checks(root, strongest_shard)
    print("NPZ structural checks complete")
    high_precision = high_precision_gate(root, strongest_shard, chord_steps)
    print("Decimal exact-event/Mobius gate complete")
    ldl = fraction_ldl_certificate(root, strongest_shard)
    print("Fraction LDL certificates complete")
    margin_profile = audit_margin_profile(root)
    print("margin-profile audit complete")
    revision = current_script_revision_checks(root)

    source_margins = [
        Decimal(item["source_margin"])
        for item in ledger["ledger_summaries"]
        if item["source_margin"] is not None
    ]
    strongest_margin = Decimal(ledger["aggregate"]["strongest_spectrum_margin"])
    margin_floor_values = [
        Decimal(str(item["manifest"]["margin_floor"])) for item in ledger["manifest_summaries"]
    ]
    source_rhos = [
        Decimal(item["source_rho"])
        for item in ledger["ledger_summaries"]
        if item["source_rho"] is not None
    ]
    strongest_rho = Decimal(ledger["aggregate"]["strongest_rho_psd"])

    conclusions = {
        "ledger_complete": (
            ledger["aggregate"]["total_proposals"] == 20000
            and ledger["aggregate"]["total_rows"] == 20004
            and ledger["aggregate"]["total_source_rows"] == 4
            and ledger["aggregate"]["total_non_no_hit"] == 0
            and ledger["aggregate"]["total_positive_gap"] == 0
            and all(m["best_json_matches_ledger"] for m in ledger["manifest_summaries"])
            and all(l["max_completed"] == 5000 for l in ledger["run_log_summaries"])
            and all(l["has_final_manifest_json"] for l in ledger["run_log_summaries"])
        ),
        "strongest_matches_claim": (
            ledger["aggregate"]["strongest_shard"] == 2
            and ledger["aggregate"]["strongest_index"] == 4877
            and abs(float(ledger["aggregate"]["strongest_rho_psd"]) - 0.5746069386526107) < 5e-16
        ),
        "no_positive_status_or_gap": (
            ledger["aggregate"]["total_non_no_hit"] == 0
            and ledger["aggregate"]["total_positive_gap"] == 0
        ),
        "high_precision_negative_H2": Decimal(high_precision["H2"]) < 0,
        "high_precision_rho_below_one": Decimal(high_precision["rho"]) < 1,
        "all_three_chords_negative": all(chord["negative"] for chord in high_precision["chords"]),
        "fraction_ldl_D_positive": bool(ldl["D_positive_definite"]["ok"]),
        "fraction_ldl_endpoint_margin": all(
            side["K_sign_radius_D_minus_margin_I"]["ok"]
            and side["I_minus_K_sign_radius_D_minus_margin_I"]["ok"]
            for side in ldl["endpoint_certificates"].values()
        ),
        "current_script_candidate_freeze_checks_present": revision["all_required_snippets_present"],
        "margin_profile_matches_ledger_and_limited_claim": margin_profile["profile_matches_ledger"],
        "boundary_comparison_finite_claim_supported": (
            strongest_margin > max(source_margins)
            and strongest_margin > max(margin_floor_values)
            and strongest_rho > max(source_rhos)
        ),
    }
    conclusions["fresh_audit_layer_status"] = (
        "CORRECT_FOR_STORED_DATA_AND_STRONGEST_GATE"
        if all(
            conclusions[key]
            for key in [
                "ledger_complete",
                "strongest_matches_claim",
                "no_positive_status_or_gap",
                "high_precision_negative_H2",
                "high_precision_rho_below_one",
                "all_three_chords_negative",
                "fraction_ldl_D_positive",
                "fraction_ldl_endpoint_margin",
                "margin_profile_matches_ledger_and_limited_claim",
                "boundary_comparison_finite_claim_supported",
            ]
        )
        else "INCORRECT_OR_INCOMPLETE_FOR_CORE_CLAIMS"
    )

    out = {
        "audit": "D10-H10 round18_boundary1 fresh non-author audit",
        "scope": "stored artifacts, strongest-point Decimal exact-event/Mobius gate, Fraction-LDL feasibility, and finite boundary comparison; no full seed regeneration",
        "root": str(root),
        "artifact_hashes": {
            "source_npz": sha256_file(root / "source.npz"),
            "recheck_best_boundary1_json": sha256_file(root / "recheck_best_boundary1.json"),
            "README": sha256_file(root / "README.md"),
        },
        "ledger": ledger,
        "strongest_npz_structural_checks": structural,
        "high_precision_exact_event_mobius": high_precision,
        "fraction_ldl_certificate": ldl,
        "margin_profile_audit": margin_profile,
        "current_script_revision_checks": revision,
        "boundary_comparison": {
            "configured_margin_floor_values": [str(x) for x in margin_floor_values],
            "source_margins": [str(x) for x in source_margins],
            "source_rhos": [str(x) for x in source_rhos],
            "strongest_margin": str(strongest_margin),
            "strongest_rho": str(strongest_rho),
            "margin_minus_source_max": str(strongest_margin - max(source_margins)),
            "margin_over_floor_max_ratio": str(strongest_margin / max(margin_floor_values)),
            "rho_improvement_over_source_max": str(strongest_rho - max(source_rhos)),
            "finite_interpretation": "The strongest stored point improves rho while being farther from the spectral boundary than the repeated source rows and far above the configured floor; this supports only the finite comparison, not a theorem.",
        },
        "conclusions": conclusions,
    }
    out_path = root / "verifications" / "fresh_h10_audit.json"
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
