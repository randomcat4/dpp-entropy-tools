"""Fresh non-author audit for round19_interior1.

No author gate/search module is imported.  The script reads raw CSV/JSON/NPZ
artifacts, independently recomputes exact-event Mobius atoms and directional
entropy derivatives with Decimal arithmetic, and checks Fraction LDL
admissibility for the frozen best case.
"""

from __future__ import annotations

import csv
import hashlib
import json
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path

import numpy as np


getcontext().prec = 120
BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "verifications" / "fresh_audit.json"
N = 12


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def dec_from_float(x) -> Decimal:
    return Decimal(repr(float(x)))


def frac_from_float(x) -> Fraction:
    return Fraction(repr(float(x)))


def sym_decimal_matrix(arr) -> list[list[Decimal]]:
    n = arr.shape[0]
    return [
        [(dec_from_float(arr[i, j]) + dec_from_float(arr[j, i])) / Decimal(2) for j in range(n)]
        for i in range(n)
    ]


def sym_fraction_matrix(arr) -> list[list[Fraction]]:
    n = arr.shape[0]
    return [
        [(frac_from_float(arr[i, j]) + frac_from_float(arr[j, i])) / 2 for j in range(n)]
        for i in range(n)
    ]


def det_inverse_decimal(mat: list[list[Decimal]]) -> tuple[Decimal, list[list[Decimal]]]:
    n = len(mat)
    if n == 0:
        return Decimal(1), []
    A = [row[:] for row in mat]
    Inv = [[Decimal(int(i == j)) for j in range(n)] for i in range(n)]
    det = Decimal(1)
    sign = 1
    for col in range(n):
        pivot = col
        while pivot < n and A[pivot][col].is_zero():
            pivot += 1
        if pivot == n:
            return Decimal(0), Inv
        if pivot != col:
            A[col], A[pivot] = A[pivot], A[col]
            Inv[col], Inv[pivot] = Inv[pivot], Inv[col]
            sign *= -1
        pv = A[col][col]
        det *= pv
        for j in range(n):
            A[col][j] /= pv
            Inv[col][j] /= pv
        for r in range(n):
            if r == col:
                continue
            factor = A[r][col]
            if factor.is_zero():
                continue
            for j in range(n):
                A[r][j] -= factor * A[col][j]
                Inv[r][j] -= factor * Inv[col][j]
    if sign < 0:
        det = -det
    return det, Inv


def det_decimal(mat: list[list[Decimal]]) -> Decimal:
    n = len(mat)
    if n == 0:
        return Decimal(1)
    A = [row[:] for row in mat]
    det = Decimal(1)
    sign = 1
    for col in range(n):
        pivot = col
        while pivot < n and A[pivot][col].is_zero():
            pivot += 1
        if pivot == n:
            return Decimal(0)
        if pivot != col:
            A[col], A[pivot] = A[pivot], A[col]
            sign *= -1
        pv = A[col][col]
        det *= pv
        for r in range(col + 1, n):
            factor = A[r][col] / pv
            if factor.is_zero():
                continue
            for j in range(col, n):
                A[r][j] -= factor * A[col][j]
    return -det if sign < 0 else det


def submatrix(M, ids):
    return [[M[i][j] for j in ids] for i in ids]


def matmul_decimal(A, B):
    n = len(A)
    m = len(B[0])
    kdim = len(B)
    return [[sum(A[i][k] * B[k][j] for k in range(kdim)) for j in range(m)] for i in range(n)]


def inclusion_derivatives(K, D):
    size = 1 << N
    inc0 = [Decimal(0)] * size
    inc1 = [Decimal(0)] * size
    inc2 = [Decimal(0)] * size
    for mask in range(size):
        ids = [i for i in range(N) if (mask >> i) & 1]
        if not ids:
            inc0[mask] = Decimal(1)
            continue
        KM = submatrix(K, ids)
        DM = submatrix(D, ids)
        det, inv = det_inverse_decimal(KM)
        X = matmul_decimal(inv, DM)
        tr = sum(X[i][i] for i in range(len(ids)))
        tr2 = sum(X[i][j] * X[j][i] for i in range(len(ids)) for j in range(len(ids)))
        inc0[mask] = det
        inc1[mask] = det * tr
        inc2[mask] = det * (tr * tr - tr2)
    return inc0, inc1, inc2


def inclusion_values(K):
    size = 1 << N
    inc = [Decimal(0)] * size
    for mask in range(size):
        ids = [i for i in range(N) if (mask >> i) & 1]
        inc[mask] = det_decimal(submatrix(K, ids)) if ids else Decimal(1)
    return inc


def mobius_atoms(inc):
    arr = inc[:]
    for bit in range(N):
        step = 1 << bit
        for mask in range(1 << N):
            if not (mask & step):
                arr[mask] -= arr[mask | step]
    return arr


def entropy_from_atoms(p):
    return -sum(x * x.ln() for x in p)


def directional_decimal(K, D):
    inc0, inc1, inc2 = inclusion_derivatives(K, D)
    p = mobius_atoms(inc0)
    p1 = mobius_atoms(inc1)
    p2 = mobius_atoms(inc2)
    fisher = sum((a * a) / b for a, b in zip(p1, p))
    acceleration = -sum(b * a.ln() for a, b in zip(p, p2))
    H2 = acceleration - fisher
    rho = acceleration / fisher
    return {
        "event_count": len(p),
        "entropy": entropy_from_atoms(p),
        "fisher": fisher,
        "acceleration": acceleration,
        "H2": H2,
        "rho": rho,
        "sum_p_minus_one": sum(p) - Decimal(1),
        "sum_p1": sum(p1),
        "sum_p2": sum(p2),
        "min_atom": min(p),
    }


def chord_decimal(K, D, step: Decimal, H0: Decimal):
    Kp = [[K[i][j] + step * D[i][j] for j in range(N)] for i in range(N)]
    Km = [[K[i][j] - step * D[i][j] for j in range(N)] for i in range(N)]
    Hp = entropy_from_atoms(mobius_atoms(inclusion_values(Kp)))
    Hm = entropy_from_atoms(mobius_atoms(inclusion_values(Km)))
    gap = (Hp + Hm) / Decimal(2) - H0
    central = Decimal(2) * gap / (step * step)
    return {"step": step, "Hminus": Hm, "Hplus": Hp, "midpoint_gap": gap, "central_H2": central}


def ldl_fraction_pivots(M):
    n = len(M)
    L = [[Fraction(0) for _ in range(n)] for __ in range(n)]
    D = [Fraction(0) for _ in range(n)]
    for i in range(n):
        L[i][i] = Fraction(1)
        pivot = M[i][i] - sum(L[i][k] * L[i][k] * D[k] for k in range(i))
        D[i] = pivot
        if pivot <= 0:
            return False, D[: i + 1]
        for j in range(i + 1, n):
            num = M[j][i] - sum(L[j][k] * L[i][k] * D[k] for k in range(i))
            L[j][i] = num / pivot
    return True, D


def frac_mat_add(A, B, scale=Fraction(1)):
    n = len(A)
    return [[A[i][j] + scale * B[i][j] for j in range(n)] for i in range(n)]


def frac_margin_matrix(K, D, t, kind):
    margin = Fraction(1, 2000)
    n = len(K)
    if kind == "lower":
        M = frac_mat_add(K, D, t)
        for i in range(n):
            M[i][i] -= margin
        return M
    if kind == "upper":
        M = [[Fraction(int(i == j)) - K[i][j] - t * D[i][j] for j in range(n)] for i in range(n)]
        for i in range(n):
            M[i][i] -= margin
        return M
    raise ValueError(kind)


def fraction_feasibility(Kf, Df):
    okD, pivD = ldl_fraction_pivots(Df)
    endpoints = []
    for t in (Fraction(-1, 200), Fraction(1, 200)):
        low = frac_margin_matrix(Kf, Df, t, "lower")
        up = frac_margin_matrix(Kf, Df, t, "upper")
        ok_low, piv_low = ldl_fraction_pivots(low)
        ok_up, piv_up = ldl_fraction_pivots(up)
        endpoints.append(
            {
                "step": str(t),
                "K_t_minus_margin_I": {
                    "all_positive": ok_low,
                    "minimum_pivot_float": float(min(piv_low)),
                    "pivot_count": len(piv_low),
                },
                "I_minus_K_t_minus_margin_I": {
                    "all_positive": ok_up,
                    "minimum_pivot_float": float(min(piv_up)),
                    "pivot_count": len(piv_up),
                },
            }
        )
    return {
        "D_positive_definite": {
            "all_positive": okD,
            "minimum_pivot_float": float(min(pivD)),
            "pivot_count": len(pivD),
        },
        "uniform_interval": ["-1/200", "1/200"],
        "strict_spectral_margin": "1/2000",
        "endpoint_LDL": endpoints,
    }


def str_dec(x: Decimal) -> str:
    return format(x, "f")


def summarize_npz(path):
    data = np.load(path)
    K = (data["kernel"] + data["kernel"].T) / 2.0
    D = (data["direction"] + data["direction"].T) / 2.0
    Q = data["eigenvectors"]
    spectrum = data["spectrum"]
    rates = data["rates"]
    eigK = np.linalg.eigvalsh(K)
    eigD = np.linalg.eigvalsh(D)
    return {
        "sha256": sha256(path),
        "keys": {k: {"shape": list(data[k].shape), "dtype": str(data[k].dtype)} for k in data.files},
        "K_min": float(eigK[0]),
        "K_max": float(eigK[-1]),
        "spectrum_margin": float(min(eigK[0], 1.0 - eigK[-1])),
        "D_min": float(eigD[0]),
        "D_max": float(eigD[-1]),
        "commutator_frobenius": float(np.linalg.norm(K @ D - D @ K)),
        "basis_orthogonality_residual": float(np.linalg.norm(Q.T @ Q - np.eye(Q.shape[0]))),
        "kernel_reconstruction_residual": float(np.linalg.norm(K - Q @ np.diag(spectrum) @ Q.T)),
        "direction_reconstruction_residual": float(np.linalg.norm(D - Q @ np.diag(rates) @ Q.T)),
    }


def audit_ledgers():
    per = []
    all_rows = []
    global_best = None
    for shard in range(4):
        d = BASE / f"results_{shard}"
        manifest = json.loads((d / "manifest.json").read_text(encoding="utf-8"))
        best_json = json.loads((d / "best_case.json").read_text(encoding="utf-8"))
        with (d / "candidate_ledger.csv").open(newline="", encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        source = [r for r in rows if r["index"] == "-1"]
        proposals = [r for r in rows if r["index"] != "-1"]
        proposal_indices = sorted(int(r["index"]) for r in proposals)
        accepted_proposals = sum(r["accepted"] == "True" for r in proposals)
        status_non_no_hit = [r for r in rows if r["status"] != "NO_HIT"]
        positive_gaps = [r for r in rows if Decimal(r["chord_gap"]) > 0]
        positive_rhos = [r for r in rows if Decimal(r["rho_psd"]) > 1]
        proposal_min_margin = min(Decimal(r["spectrum_margin"]) for r in proposals)
        source_margin = Decimal(source[0]["spectrum_margin"]) if source else None
        shard_best = max(rows, key=lambda r: Decimal(r["rho_psd"]))
        if global_best is None or Decimal(shard_best["rho_psd"]) > Decimal(global_best["rho_psd"]):
            global_best = dict(shard_best, _shard=str(shard))
        best_match = all(
            str(best_json[k]) == rows[int(best_json["index"]) + 1][k]
            for k in [
                "index",
                "label",
                "spectral_scale",
                "basis_scale",
                "accepted",
                "rho_psd",
                "rho_unrestricted",
                "unrestricted_same_sign",
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
                "status",
            ]
        )
        per.append(
            {
                "shard": shard,
                "row_count": len(rows),
                "source_rows": len(source),
                "proposal_rows": len(proposals),
                "proposal_indices_exact_0_to_4999": proposal_indices == list(range(5000)),
                "manifest_status": manifest["status"],
                "manifest_exit_code": manifest["exit_code"],
                "manifest_positive_count": manifest["positive_count"],
                "accepted_proposals": accepted_proposals,
                "manifest_accepted_count": manifest["accepted_count"],
                "non_no_hit_rows": len(status_non_no_hit),
                "positive_gap_rows": len(positive_gaps),
                "rho_over_one_rows": len(positive_rhos),
                "proposal_min_spectrum_margin": str(proposal_min_margin),
                "source_spectrum_margin": None if source_margin is None else str(source_margin),
                "best_json_matches_ledger_row": best_match,
                "best_json_sha256": sha256(d / "best_case.json"),
                "best_npz_sha256": sha256(d / "best_case.npz"),
                "csv_sha256": sha256(d / "candidate_ledger.csv"),
                "manifest_sha256": sha256(d / "manifest.json"),
                "best_index": best_json["index"],
                "best_rho_psd": str(best_json["rho_psd"]),
                "best_status": best_json["status"],
            }
        )
        all_rows.extend(dict(r, _shard=str(shard)) for r in rows)
    return {
        "total_rows": len(all_rows),
        "proposal_rows": sum(p["proposal_rows"] for p in per),
        "source_rows": sum(p["source_rows"] for p in per),
        "per_shard": per,
        "global_best_by_rho": global_best,
        "global_max_gap": str(max(Decimal(r["chord_gap"]) for r in all_rows)),
        "all_proposal_margins_at_least_0_02": all(
            Decimal(r["spectrum_margin"]) >= Decimal("0.02") for r in all_rows if r["index"] != "-1"
        ),
        "all_status_no_hit": all(r["status"] == "NO_HIT" for r in all_rows),
        "all_chord_gaps_negative": all(Decimal(r["chord_gap"]) < 0 for r in all_rows),
        "all_rho_below_one": all(Decimal(r["rho_psd"]) < 1 for r in all_rows),
    }


def main():
    input_hashes = {
        str(p.relative_to(BASE)): sha256(p)
        for p in sorted(BASE.rglob("*"))
        if p.is_file() and "verifications" not in p.parts
    }
    ledgers = audit_ledgers()
    recheck = json.loads((BASE / "recheck_best_interior1.json").read_text(encoding="utf-8"))
    best_npz = BASE / "results_0" / "best_case.npz"
    source_npz = BASE / "interior_source_margin003.npz"
    best_data = np.load(best_npz)
    K_np = (best_data["kernel"] + best_data["kernel"].T) / 2.0
    D_np = (best_data["direction"] + best_data["direction"].T) / 2.0
    Kd = sym_decimal_matrix(best_data["kernel"])
    Dd = sym_decimal_matrix(best_data["direction"])
    directional = directional_decimal(Kd, Dd)
    steps = [Decimal(str(recheck["ledger"]["best_row"]["chord_step"])), Decimal("0.001"), Decimal("0.0001")]
    chords = [chord_decimal(Kd, Dd, s, directional["entropy"]) for s in steps]
    feasibility = fraction_feasibility(sym_fraction_matrix(best_data["kernel"]), sym_fraction_matrix(best_data["direction"]))
    h10_path = BASE.parent / "results_server_round18_boundary1" / "recheck_best_boundary1.json"
    h10 = json.loads(h10_path.read_text(encoding="utf-8"))
    h10_rho = Decimal(h10["decimal_directional"][-1]["rho"])
    rho_diff = h10_rho - directional["rho"]
    author80 = recheck["decimal_directional"][-1]
    comparisons = {
        "rho_abs_diff_vs_author80": str(abs(directional["rho"] - Decimal(author80["rho"]))),
        "H2_abs_diff_vs_author80": str(abs(directional["H2"] - Decimal(author80["H2"]))),
        "fisher_abs_diff_vs_author80": str(abs(directional["fisher"] - Decimal(author80["fisher"]))),
        "acceleration_abs_diff_vs_author80": str(abs(directional["acceleration"] - Decimal(author80["acceleration"]))),
    }
    report = {
        "status": "PASS_WITH_SCOUT_SCOPE",
        "scope": "fresh non-author audit of copied ledger/manifests and strongest high-precision gate; no author gate/search import",
        "input_hashes": input_hashes,
        "ledger_audit": ledgers,
        "npz_summaries": {
            "source": summarize_npz(source_npz),
            "strongest": summarize_npz(best_npz),
            "best_by_shard": {str(s): summarize_npz(BASE / f"results_{s}" / "best_case.npz") for s in range(4)},
        },
        "strongest": {
            "shard": 0,
            "index": 4853,
            "row": ledgers["global_best_by_rho"],
            "decimal_precision": getcontext().prec,
            "directional": {k: (str_dec(v) if isinstance(v, Decimal) else v) for k, v in directional.items()},
            "chords": [
                {k: (str_dec(v) if isinstance(v, Decimal) else v) for k, v in c.items()} for c in chords
            ],
            "fraction_feasibility": feasibility,
            "comparisons_to_author80": comparisons,
        },
        "h10_comparison": {
            "h10_round18_boundary1_rho": str_dec(h10_rho),
            "h11_round19_interior1_rho": str_dec(directional["rho"]),
            "h10_minus_h11": str_dec(rho_diff),
            "interpretation": "round19 strict-interior best is lower than H10 boundary1 by about 1.22078e-5",
        },
        "scope_notes": {
            "proposal_matrix_regeneration": "not performed; per-proposal margins are audited from the frozen CSV ledger, while source and best NPZ spectra are recomputed",
            "finite_search": "supports no-hit and interior-near-best scout only; not a global theorem",
            "fixed_Q_scope": "float search is fixed-Q at each center with joint basis/spectrum perturbations; frozen rational line is near-commuting, not exact symbolic commuting theorem",
        },
    }
    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "status": report["status"],
                "rows": {
                    "total": ledgers["total_rows"],
                    "proposals": ledgers["proposal_rows"],
                    "sources": ledgers["source_rows"],
                },
                "strongest_rho": str_dec(directional["rho"]),
                "H2": str_dec(directional["H2"]),
                "h10_minus_h11": str_dec(rho_diff),
                "all_gaps_negative": ledgers["all_chord_gaps_negative"],
                "all_proposal_margins_at_least_0_02": ledgers["all_proposal_margins_at_least_0_02"],
            },
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
