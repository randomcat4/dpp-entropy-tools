#!/usr/bin/env python3
"""
Fresh non-author audit for D10-H16 / round24_interior6.

Deliberately does not import the author's search/gate/recheck modules.  It reads
the frozen CSV/JSON/NPZ artifacts, reconstructs the strongest event law from
principal-minor inclusion probabilities, applies Mobius inversion, and performs
independent high-precision entropy-jet and chord checks.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np


DEC_PREC = 160
getcontext().prec = DEC_PREC

AUDIT_DIR = Path(__file__).resolve().parent
BASE = AUDIT_DIR.parent
COMMUTING_DIR = BASE.parent

EXPECTED = {
    "n": 12,
    "shards": 4,
    "proposal_count_per_shard": 5000,
    "ledger_rows_including_source": 5001,
    "margin_floor": Decimal("0.40"),
    "best_shard": 1,
    "best_index": 4686,
    "best_rho": Decimal("0.03861710868283657"),
    "feasible_step": Fraction(1, 200),
    "strict_margin": Fraction(1, 2000),
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def dstr(x: Decimal, digits: int | None = None) -> str:
    if digits is None:
        return format(x, "f")
    return format(+x, f".{digits}E")


def dec_from_fraction(x: Fraction) -> Decimal:
    return Decimal(x.numerator) / Decimal(x.denominator)


def frac_from_float(x: float) -> Fraction:
    return Fraction.from_float(float(x))


def json_default(obj: Any) -> Any:
    if isinstance(obj, Decimal):
        return str(obj)
    if isinstance(obj, Fraction):
        return {"num": obj.numerator, "den": obj.denominator}
    if isinstance(obj, Path):
        return str(obj)
    if isinstance(obj, np.generic):
        return obj.item()
    raise TypeError(f"not JSON serializable: {type(obj)!r}")


def read_ledger(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def parse_log_summary(path: Path) -> dict[str, Any]:
    parsed = []
    with path.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                parsed.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return {
        "path": path.name,
        "json_lines": len(parsed),
        "last_json": parsed[-1] if parsed else None,
        "sha256": sha256_file(path),
    }


def audit_ledgers() -> dict[str, Any]:
    shard_reports = []
    all_rows_with_shard: list[tuple[int, dict[str, str]]] = []
    total_positive_gap = 0
    total_rho_ge_1 = 0
    total_non_no_hit = 0
    min_proposal_margin: Decimal | None = None
    min_any_margin: Decimal | None = None
    max_row: tuple[Decimal, int, dict[str, str]] | None = None

    for shard in range(EXPECTED["shards"]):
        result_dir = BASE / f"results_{shard}"
        ledger_path = result_dir / "candidate_ledger.csv"
        manifest_path = result_dir / "manifest.json"
        best_json_path = result_dir / "best_case.json"
        best_npz_path = result_dir / "best_case.npz"
        rows = read_ledger(ledger_path)
        manifest = read_json(manifest_path)
        best_json = read_json(best_json_path)

        source_rows = [r for r in rows if r["index"] == "-1"]
        proposal_rows = [r for r in rows if r["index"] != "-1"]
        positive_gap = sum(Decimal(r["chord_gap"]) > 0 for r in rows)
        rho_ge_1 = sum(
            (Decimal(r["rho_psd"]) >= 1) or (Decimal(r["rho_unrestricted"]) >= 1)
            for r in rows
        )
        non_no_hit = sum(r["status"] != "NO_HIT" for r in rows)
        accepted_proposals = sum(
            r["accepted"].strip().lower() == "true" for r in proposal_rows
        )

        for r in rows:
            margin = Decimal(r["spectrum_margin"])
            min_any_margin = margin if min_any_margin is None else min(min_any_margin, margin)
            if r["index"] != "-1":
                min_proposal_margin = (
                    margin
                    if min_proposal_margin is None
                    else min(min_proposal_margin, margin)
                )
            rho = Decimal(r["rho_psd"])
            if max_row is None or rho > max_row[0]:
                max_row = (rho, shard, r)
            all_rows_with_shard.append((shard, r))

        total_positive_gap += positive_gap
        total_rho_ge_1 += rho_ge_1
        total_non_no_hit += non_no_hit

        shard_reports.append(
            {
                "shard": shard,
                "ledger_sha256": sha256_file(ledger_path),
                "manifest_sha256": sha256_file(manifest_path),
                "best_json_sha256": sha256_file(best_json_path),
                "best_npz_sha256": sha256_file(best_npz_path),
                "row_count": len(rows),
                "source_row_count": len(source_rows),
                "proposal_row_count": len(proposal_rows),
                "positive_gap_rows": positive_gap,
                "rho_ge_1_rows": rho_ge_1,
                "non_no_hit_rows": non_no_hit,
                "accepted_proposals_from_ledger": accepted_proposals,
                "manifest": {
                    "seed": manifest.get("seed"),
                    "n": manifest.get("n"),
                    "proposal_count": manifest.get("proposal_count"),
                    "ledger_rows_including_source": manifest.get(
                        "ledger_rows_including_source"
                    ),
                    "margin_floor": manifest.get("margin_floor"),
                    "positive_count": manifest.get("positive_count"),
                    "accepted_count": manifest.get("accepted_count"),
                    "exit_code": manifest.get("exit_code"),
                    "status": manifest.get("status"),
                    "best_rho_psd": manifest.get("best_rho_psd"),
                    "best_index": manifest.get("best_index"),
                    "best_spectrum_margin": manifest.get("best_spectrum_margin"),
                    "source_status": manifest.get("source_status"),
                    "source_rho": manifest.get("source_rho"),
                    "source_gap": manifest.get("source_gap"),
                },
                "best_json": {
                    "index": best_json.get("index"),
                    "label": best_json.get("label"),
                    "rho_psd": best_json.get("rho_psd"),
                    "chord_gap": best_json.get("chord_gap"),
                    "spectrum_margin": best_json.get("spectrum_margin"),
                    "status": best_json.get("status"),
                },
                "source_row": source_rows[0] if source_rows else None,
            }
        )

    assert max_row is not None
    max_rho, max_shard, max_data = max_row
    return {
        "shards": shard_reports,
        "total_rows_including_sources": len(all_rows_with_shard),
        "total_proposals": sum(1 for _, r in all_rows_with_shard if r["index"] != "-1"),
        "total_sources": sum(1 for _, r in all_rows_with_shard if r["index"] == "-1"),
        "total_positive_gap_rows": total_positive_gap,
        "total_rho_ge_1_rows": total_rho_ge_1,
        "total_non_no_hit_rows": total_non_no_hit,
        "min_any_spectrum_margin": min_any_margin,
        "min_proposal_spectrum_margin": min_proposal_margin,
        "max_rho_row": {
            "shard": max_shard,
            "index": int(max_data["index"]),
            "rho_psd": max_rho,
            "label": max_data["label"],
            "chord_gap": max_data["chord_gap"],
            "spectrum_margin": max_data["spectrum_margin"],
            "status": max_data["status"],
        },
    }


def npz_reconstruction() -> dict[str, Any]:
    npz_path = BASE / "results_1" / "best_case.npz"
    data = np.load(npz_path)
    K_raw = np.array(data["kernel"], dtype=float)
    D_raw = np.array(data["direction"], dtype=float)
    Q = np.array(data["eigenvectors"], dtype=float)
    lambdas = np.array(data["spectrum"], dtype=float)
    rates = np.array(data["rates"], dtype=float)
    K = (K_raw + K_raw.T) / 2.0
    D = (D_raw + D_raw.T) / 2.0
    K_from_Q = Q @ np.diag(lambdas) @ Q.T
    D_from_Q = Q @ np.diag(rates) @ Q.T
    comm = K @ D - D @ K
    return {
        "npz_sha256": sha256_file(npz_path),
        "n": int(K.shape[0]),
        "kernel_asym_fro": float(np.linalg.norm(K_raw - K_raw.T)),
        "direction_asym_fro": float(np.linalg.norm(D_raw - D_raw.T)),
        "q_orthogonality_fro": float(np.linalg.norm(Q.T @ Q - np.eye(Q.shape[1]))),
        "kernel_reconstruction_fro": float(np.linalg.norm(K - K_from_Q)),
        "direction_reconstruction_fro": float(np.linalg.norm(D - D_from_Q)),
        "commutator_fro": float(np.linalg.norm(comm)),
        "lambda_min": float(np.min(lambdas)),
        "lambda_max": float(np.max(lambdas)),
        "rate_min": float(np.min(rates)),
        "rate_max": float(np.max(rates)),
        "spectrum_margin_float": float(min(np.min(lambdas), np.min(1 - lambdas))),
    }


def load_fraction_matrices() -> tuple[list[list[Fraction]], list[list[Fraction]]]:
    data = np.load(BASE / "results_1" / "best_case.npz")
    K_raw = np.array(data["kernel"], dtype=float)
    D_raw = np.array(data["direction"], dtype=float)
    K_sym = (K_raw + K_raw.T) / 2.0
    D_sym = (D_raw + D_raw.T) / 2.0
    K = [[frac_from_float(K_sym[i, j]) for j in range(K_sym.shape[1])] for i in range(K_sym.shape[0])]
    D = [[frac_from_float(D_sym[i, j]) for j in range(D_sym.shape[1])] for i in range(D_sym.shape[0])]
    return K, D


def fraction_to_decimal_matrix(A: list[list[Fraction]]) -> list[list[Decimal]]:
    return [[dec_from_fraction(x) for x in row] for row in A]


def det_decimal(A: list[list[Decimal]]) -> Decimal:
    n = len(A)
    if n == 0:
        return Decimal(1)
    M = [row[:] for row in A]
    det = Decimal(1)
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(M[r][col]))
        piv = M[pivot][col]
        if piv.is_zero():
            return Decimal(0)
        if pivot != col:
            M[col], M[pivot] = M[pivot], M[col]
            det = -det
        piv = M[col][col]
        det *= piv
        for r in range(col + 1, n):
            fac = M[r][col] / piv
            if fac.is_zero():
                continue
            for c in range(col + 1, n):
                M[r][c] -= fac * M[col][c]
            M[r][col] = Decimal(0)
    return +det


def det_inv_decimal(A: list[list[Decimal]]) -> tuple[Decimal, list[list[Decimal]]]:
    n = len(A)
    if n == 0:
        return Decimal(1), []
    M = [
        A[i][:] + [Decimal(1) if i == j else Decimal(0) for j in range(n)]
        for i in range(n)
    ]
    det = Decimal(1)
    width = 2 * n
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(M[r][col]))
        piv = M[pivot][col]
        if piv.is_zero():
            raise ArithmeticError("singular principal block in Decimal inversion")
        if pivot != col:
            M[col], M[pivot] = M[pivot], M[col]
            det = -det
        piv = M[col][col]
        det *= piv
        inv_piv = Decimal(1) / piv
        for c in range(width):
            M[col][c] *= inv_piv
        for r in range(n):
            if r == col:
                continue
            fac = M[r][col]
            if fac.is_zero():
                continue
            for c in range(width):
                M[r][c] -= fac * M[col][c]
    inv = [row[n:] for row in M]
    return +det, inv


def subset_indices(n: int) -> list[list[int]]:
    return [[i for i in range(n) if (mask >> i) & 1] for mask in range(1 << n)]


def mobius_from_inclusions(values: list[Decimal], n: int) -> list[Decimal]:
    out = values[:]
    for bit in range(n):
        step = 1 << bit
        for mask in range(1 << n):
            if (mask & step) == 0:
                out[mask] -= out[mask | step]
    return [+x for x in out]


def entropy_from_atoms(p: list[Decimal]) -> Decimal:
    total = Decimal(0)
    for x in p:
        if x <= 0:
            raise ArithmeticError(f"non-positive atom in entropy: {x}")
        total -= x * x.ln()
    return +total


def inclusion_jets_decimal(
    K: list[list[Decimal]], D: list[list[Decimal]]
) -> tuple[list[Decimal], list[Decimal], list[Decimal]]:
    n = len(K)
    idx_by_mask = subset_indices(n)
    q0 = [Decimal(0)] * (1 << n)
    q1 = [Decimal(0)] * (1 << n)
    q2 = [Decimal(0)] * (1 << n)

    for mask, idx in enumerate(idx_by_mask):
        m = len(idx)
        if m == 0:
            q0[mask] = Decimal(1)
            continue
        A = [[K[i][j] for j in idx] for i in idx]
        B = [[D[i][j] for j in idx] for i in idx]
        det, inv = det_inv_decimal(A)

        tr1 = Decimal(0)
        C = [[Decimal(0) for _ in range(m)] for __ in range(m)]
        for i in range(m):
            for j in range(m):
                s = Decimal(0)
                for k in range(m):
                    s += inv[i][k] * B[k][j]
                C[i][j] = s
            tr1 += C[i][i]
        tr2 = Decimal(0)
        for i in range(m):
            for j in range(m):
                tr2 += C[i][j] * C[j][i]

        q0[mask] = det
        q1[mask] = det * tr1
        q2[mask] = det * (tr1 * tr1 - tr2)

    return q0, q1, q2


def atom_probabilities_decimal(K: list[list[Decimal]]) -> list[Decimal]:
    n = len(K)
    idx_by_mask = subset_indices(n)
    q = [Decimal(0)] * (1 << n)
    for mask, idx in enumerate(idx_by_mask):
        if not idx:
            q[mask] = Decimal(1)
        else:
            A = [[K[i][j] for j in idx] for i in idx]
            q[mask] = det_decimal(A)
    return mobius_from_inclusions(q, n)


def exact_event_jet_audit() -> dict[str, Any]:
    K_frac, D_frac = load_fraction_matrices()
    K_dec = fraction_to_decimal_matrix(K_frac)
    D_dec = fraction_to_decimal_matrix(D_frac)
    n = len(K_dec)

    q0, q1, q2 = inclusion_jets_decimal(K_dec, D_dec)
    p0 = mobius_from_inclusions(q0, n)
    p1 = mobius_from_inclusions(q1, n)
    p2 = mobius_from_inclusions(q2, n)

    fisher = Decimal(0)
    acceleration = Decimal(0)
    min_atom = min(p0)
    max_abs_mobius_diff = Decimal(0)
    # Independent direct consistency: inclusion q0(A) equals sum_{S superset A} p0(S).
    for mask in range(1 << n):
        recovered = sum(p0[s] for s in range(1 << n) if (s & mask) == mask)
        max_abs_mobius_diff = max(max_abs_mobius_diff, abs(recovered - q0[mask]))
    for a, b, c in zip(p0, p1, p2):
        fisher += (b * b) / a
        acceleration -= c * a.ln()
    h2 = acceleration - fisher
    rho = acceleration / fisher
    entropy0 = entropy_from_atoms(p0)
    return {
        "decimal_precision": DEC_PREC,
        "event_count": 1 << n,
        "sum_p0_minus_1": sum(p0) - Decimal(1),
        "sum_p1": sum(p1),
        "sum_p2": sum(p2),
        "min_atom": min_atom,
        "max_abs_mobius_recovery_error": max_abs_mobius_diff,
        "entropy": entropy0,
        "directional_fisher": fisher,
        "acceleration_minus_p2logp": acceleration,
        "H_second": h2,
        "rho": rho,
        "rho_less_than_1": rho < 1,
        "H_second_negative": h2 < 0,
    }


def entropy_for_fraction_kernel(K_frac: list[list[Fraction]]) -> Decimal:
    return entropy_from_atoms(atom_probabilities_decimal(fraction_to_decimal_matrix(K_frac)))


def chord_audit() -> list[dict[str, Any]]:
    K, D = load_fraction_matrices()
    H0 = entropy_for_fraction_kernel(K)
    steps = [Fraction(1, 100), Fraction(1, 1000), Fraction(1, 10000)]
    reports = []
    for h in steps:
        Kp = [[K[i][j] + h * D[i][j] for j in range(len(K))] for i in range(len(K))]
        Km = [[K[i][j] - h * D[i][j] for j in range(len(K))] for i in range(len(K))]
        Hp = entropy_for_fraction_kernel(Kp)
        Hm = entropy_for_fraction_kernel(Km)
        gap = (Hp + Hm) / Decimal(2) - H0
        reports.append(
            {
                "step": {"num": h.numerator, "den": h.denominator},
                "midpoint_gap": gap,
                "scaled_gap_over_step2": gap / (dec_from_fraction(h) ** 2),
                "negative": gap < 0,
            }
        )
    return reports


def ldl_pivots_fraction(A: list[list[Fraction]]) -> list[Fraction]:
    n = len(A)
    L = [[Fraction(0) for _ in range(n)] for __ in range(n)]
    pivots: list[Fraction] = []
    for j in range(n):
        diag = A[j][j]
        for k in range(j):
            diag -= L[j][k] * L[j][k] * pivots[k]
        pivots.append(diag)
        if diag == 0:
            continue
        for i in range(j + 1, n):
            val = A[i][j]
            for k in range(j):
                val -= L[i][k] * L[j][k] * pivots[k]
            L[i][j] = val / diag
    return pivots


def min_fraction_float(xs: list[Fraction]) -> float:
    return min(float(x) for x in xs)


def ldl_certificate() -> dict[str, Any]:
    K, D = load_fraction_matrices()
    n = len(K)
    eye = [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]
    margin = EXPECTED["strict_margin"]
    reports: dict[str, Any] = {}
    piv_D = ldl_pivots_fraction(D)
    reports["D_positive"] = all(x > 0 for x in piv_D)
    reports["D_pivot_min_float"] = min_fraction_float(piv_D)
    reports["D_min_pivot"] = min(piv_D)

    for h in [EXPECTED["feasible_step"], -EXPECTED["feasible_step"]]:
        Kt = [[K[i][j] + h * D[i][j] for j in range(n)] for i in range(n)]
        lower = [[Kt[i][j] - margin * eye[i][j] for j in range(n)] for i in range(n)]
        upper = [[eye[i][j] - Kt[i][j] - margin * eye[i][j] for j in range(n)] for i in range(n)]
        piv_lower = ldl_pivots_fraction(lower)
        piv_upper = ldl_pivots_fraction(upper)
        key = f"t_{h.numerator}_over_{h.denominator}"
        reports[key] = {
            "K_minus_marginI_positive": all(x > 0 for x in piv_lower),
            "I_minus_K_minus_marginI_positive": all(x > 0 for x in piv_upper),
            "K_minus_marginI_min_pivot_float": min_fraction_float(piv_lower),
            "I_minus_K_minus_marginI_min_pivot_float": min_fraction_float(piv_upper),
            "K_minus_marginI_min_pivot": min(piv_lower),
            "I_minus_K_minus_marginI_min_pivot": min(piv_upper),
        }
    return reports


def profile_h10_h16() -> list[dict[str, Any]]:
    rounds = [
        ("H10", "results_server_round18_boundary1"),
        ("H11", "results_server_round19_interior1"),
        ("H12", "results_server_round20_interior2"),
        ("H13", "results_server_round21_interior3"),
        ("H14", "results_server_round22_interior4"),
        ("H15", "results_server_round23_interior5"),
        ("H16", "results_server_round24_interior6"),
    ]
    out = []
    for label, dirname in rounds:
        root = COMMUTING_DIR / dirname
        if not root.exists():
            out.append({"label": label, "dirname": dirname, "exists": False})
            continue
        best_seen: tuple[Decimal, int, dict[str, Any], Path] | None = None
        manifests = []
        for manifest_path in sorted(root.glob("results_*/manifest.json")):
            m = read_json(manifest_path)
            manifests.append(m)
        for best_path in sorted(root.glob("results_*/best_case.json")):
            b = read_json(best_path)
            rho_raw = b.get("rho_psd", b.get("rho"))
            if rho_raw is None:
                continue
            rho = Decimal(str(rho_raw))
            shard = int(best_path.parent.name.split("_")[-1])
            if best_seen is None or rho > best_seen[0]:
                best_seen = (rho, shard, b, best_path)
        ledgers_total_rows = 0
        non_no_hit = 0
        positive_gap = 0
        rho_ge_1 = 0
        min_margin = None
        for ledger_path in sorted(root.glob("results_*/candidate_ledger.csv")):
            rows = read_ledger(ledger_path)
            ledgers_total_rows += len(rows)
            for r in rows:
                if r.get("status") != "NO_HIT":
                    non_no_hit += 1
                if Decimal(r.get("chord_gap", "0")) > 0:
                    positive_gap += 1
                if Decimal(r.get("rho_psd", "0")) >= 1:
                    rho_ge_1 += 1
                if r.get("spectrum_margin") not in (None, ""):
                    mm = Decimal(r["spectrum_margin"])
                    min_margin = mm if min_margin is None else min(min_margin, mm)
        out.append(
            {
                "label": label,
                "dirname": dirname,
                "exists": True,
                "manifest_count": len(manifests),
                "margin_floors": sorted({str(m.get("margin_floor")) for m in manifests}),
                "manifest_positive_count_sum": sum(int(m.get("positive_count", 0)) for m in manifests),
                "manifest_proposal_count_sum": sum(int(m.get("proposal_count", 0)) for m in manifests),
                "ledger_rows_including_sources": ledgers_total_rows,
                "ledger_non_no_hit_rows": non_no_hit,
                "ledger_positive_gap_rows": positive_gap,
                "ledger_rho_ge_1_rows": rho_ge_1,
                "min_ledger_spectrum_margin": None if min_margin is None else str(min_margin),
                "best": None
                if best_seen is None
                else {
                    "rho": str(best_seen[0]),
                    "shard": best_seen[1],
                    "index": best_seen[2].get("index"),
                    "label": best_seen[2].get("label"),
                    "chord_gap": best_seen[2].get("chord_gap"),
                    "spectrum_margin": best_seen[2].get("spectrum_margin"),
                    "best_json": str(best_seen[3].relative_to(root)),
                },
            }
        )
    return out


def collect_hashes() -> dict[str, str]:
    patterns = [
        "README.md",
        "recheck_best_interior6.json",
        "prepare_interior_source.py",
        "commuting_spectral_search.py",
        "spectral_basis_refine.py",
        "interior_source_margin042.json",
        "interior_source_margin042.npz",
        "run_*.log",
        "results_*/manifest.json",
        "results_*/candidate_ledger.csv",
        "results_*/best_case.json",
        "results_*/best_case.npz",
    ]
    hashes = {}
    for pat in patterns:
        for path in sorted(BASE.glob(pat)):
            if path.is_file():
                hashes[str(path.relative_to(BASE))] = sha256_file(path)
    return hashes


def main() -> None:
    ledger = audit_ledgers()
    npz = npz_reconstruction()
    jet = exact_event_jet_audit()
    chords = chord_audit()
    ldl = ldl_certificate()
    profile = profile_h10_h16()
    logs = [parse_log_summary(BASE / f"run_{i}.log") for i in range(EXPECTED["shards"])]

    checks = {
        "four_shards_present": len(ledger["shards"]) == EXPECTED["shards"],
        "each_ledger_5001_rows": all(
            s["row_count"] == EXPECTED["ledger_rows_including_source"]
            for s in ledger["shards"]
        ),
        "total_20004_rows": ledger["total_rows_including_sources"] == 20004,
        "total_20000_proposals": ledger["total_proposals"] == 20000,
        "four_sources": ledger["total_sources"] == 4,
        "manifests_5000_proposals_each": all(
            s["manifest"]["proposal_count"] == EXPECTED["proposal_count_per_shard"]
            for s in ledger["shards"]
        ),
        "manifests_5001_rows_each": all(
            s["manifest"]["ledger_rows_including_source"]
            == EXPECTED["ledger_rows_including_source"]
            for s in ledger["shards"]
        ),
        "manifest_margin_floor_0p40": all(
            Decimal(str(s["manifest"]["margin_floor"])) == EXPECTED["margin_floor"]
            for s in ledger["shards"]
        ),
        "manifest_positive_count_zero": all(
            int(s["manifest"]["positive_count"]) == 0 for s in ledger["shards"]
        ),
        "manifest_exit_code_zero": all(
            int(s["manifest"]["exit_code"]) == 0 for s in ledger["shards"]
        ),
        "no_positive_gap_rows": ledger["total_positive_gap_rows"] == 0,
        "no_rho_ge_1_rows": ledger["total_rho_ge_1_rows"] == 0,
        "no_non_no_hit_rows": ledger["total_non_no_hit_rows"] == 0,
        "proposal_margin_at_least_0p40_allow_roundoff": ledger[
            "min_proposal_spectrum_margin"
        ]
        >= Decimal("0.399999999999999"),
        "best_location_matches_prompt": (
            ledger["max_rho_row"]["shard"] == EXPECTED["best_shard"]
            and ledger["max_rho_row"]["index"] == EXPECTED["best_index"]
        ),
        "best_rho_matches_prompt": abs(
            ledger["max_rho_row"]["rho_psd"] - EXPECTED["best_rho"]
        )
        < Decimal("1e-15"),
        "strongest_npz_fixed_Q_reconstruction": (
            npz["q_orthogonality_fro"] < 1e-12
            and npz["kernel_reconstruction_fro"] < 1e-12
            and npz["direction_reconstruction_fro"] < 1e-12
            and npz["commutator_fro"] < 1e-12
            and npz["rate_min"] > 0
        ),
        "decimal_event_law_valid": (
            abs(jet["sum_p0_minus_1"]) < Decimal("1e-120")
            and abs(jet["sum_p1"]) < Decimal("1e-110")
            and abs(jet["sum_p2"]) < Decimal("1e-105")
            and jet["min_atom"] > 0
        ),
        "decimal_H2_negative_and_rho_below_1": (
            jet["H_second_negative"] and jet["rho_less_than_1"]
        ),
        "three_chords_negative": all(c["negative"] for c in chords),
        "fraction_ldl_D_positive": bool(ldl["D_positive"]),
        "fraction_ldl_pm_1_200_strict_margin": all(
            ldl[key]["K_minus_marginI_positive"]
            and ldl[key]["I_minus_K_minus_marginI_positive"]
            for key in ldl
            if key.startswith("t_")
        ),
    }

    result = {
        "audit_kind": "fresh non-author independent audit",
        "scope": "D10-H16 results_server_round24_interior6",
        "limitations": [
            "Finite SCOUT only: no theorem or monotonic/global inference is certified.",
            "The script does not regenerate all seeds or full proposal matrices.",
            "It reads frozen artifacts and independently recomputes the strongest exact-event law and certificates.",
        ],
        "input_hashes_sha256": collect_hashes(),
        "ledger_audit": ledger,
        "run_logs": logs,
        "npz_fixed_Q_reconstruction": npz,
        "decimal_exact_event_mobius_jet": jet,
        "decimal_chords": chords,
        "fraction_ldl_certificates": ldl,
        "profile_H10_H16": profile,
        "checks": checks,
        "overall": "FINITE_SCOUT_CORRECT" if all(checks.values()) else "INCOMPLETE_OR_GAP",
    }
    out_path = AUDIT_DIR / "audit_results.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False, default=json_default)
        f.write("\n")
    print(json.dumps({"overall": result["overall"], "out": str(out_path)}, indent=2))


if __name__ == "__main__":
    main()
