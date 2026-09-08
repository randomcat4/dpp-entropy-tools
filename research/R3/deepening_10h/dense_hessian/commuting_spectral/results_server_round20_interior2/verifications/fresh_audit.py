"""Fresh non-author audit for D10-H12 / round20_interior2.

No author search/gate module is imported.  The script reads frozen CSV/JSON/NPZ
outputs, performs independent ledger accounting, rebuilds exact-event atoms by
Mobius inversion from inclusion determinants, computes the directional entropy
Hessian with Decimal precision, checks three symmetric chords, and verifies the
stored PSD/strict-feasible line using Fraction LDL.
"""

from __future__ import annotations

import csv
from decimal import Decimal, getcontext
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import time

import numpy as np


getcontext().prec = 150

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
COMMUTING = ROOT.parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def dstr(x: Decimal, places: int | None = None) -> str:
    if places is None:
        return str(+x)
    return format(+x, f".{places}E")


def dec_from_float(x: float) -> Decimal:
    return Decimal(format(float(x), ".17g"))


def frac_from_float(x: float) -> Fraction:
    return Fraction(format(float(x), ".17g"))


def sym_decimal(arr) -> list[list[Decimal]]:
    n = arr.shape[0]
    return [[(dec_from_float(arr[i, j]) + dec_from_float(arr[j, i])) / 2 for j in range(n)] for i in range(n)]


def sym_fraction(arr) -> list[list[Fraction]]:
    n = arr.shape[0]
    return [[(frac_from_float(arr[i, j]) + frac_from_float(arr[j, i])) / 2 for j in range(n)] for i in range(n)]


def mat_sub(M, inds):
    return [[M[i][j] for j in inds] for i in inds]


def ldl_decimal(A):
    n = len(A)
    L = [[Decimal(0) for _ in range(n)] for _ in range(n)]
    D = [Decimal(0) for _ in range(n)]
    for i in range(n):
        L[i][i] = Decimal(1)
        for j in range(i):
            s = A[i][j]
            for k in range(j):
                s -= L[i][k] * L[j][k] * D[k]
            L[i][j] = s / D[j]
        diag = A[i][i]
        for k in range(i):
            diag -= L[i][k] * L[i][k] * D[k]
        D[i] = +diag
        if D[i] <= 0:
            raise ArithmeticError(f"nonpositive Decimal LDL pivot {i}: {D[i]}")
    return L, D


def solve_ldl(L, Ddiag, B):
    n = len(L)
    if n == 0:
        return []
    m = len(B[0])
    Y = [[Decimal(0) for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for c in range(m):
            s = B[i][c]
            for k in range(i):
                s -= L[i][k] * Y[k][c]
            Y[i][c] = +s
    Z = [[Y[i][c] / Ddiag[i] for c in range(m)] for i in range(n)]
    X = [[Decimal(0) for _ in range(m)] for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for c in range(m):
            s = Z[i][c]
            for k in range(i + 1, n):
                s -= L[k][i] * X[k][c]
            X[i][c] = +s
    return X


def inclusion_det_decimal(K, inds):
    if not inds:
        return Decimal(1)
    _, Ddiag = ldl_decimal(mat_sub(K, inds))
    out = Decimal(1)
    for v in Ddiag:
        out *= v
    return +out


def inclusion_derivatives_decimal(K, Dmat, inds):
    if not inds:
        return Decimal(1), Decimal(0), Decimal(0)
    A = mat_sub(K, inds)
    B = mat_sub(Dmat, inds)
    L, Ddiag = ldl_decimal(A)
    detA = Decimal(1)
    for v in Ddiag:
        detA *= v
    C = solve_ldl(L, Ddiag, B)
    tr = sum(C[i][i] for i in range(len(inds)))
    tr2 = Decimal(0)
    m = len(inds)
    for i in range(m):
        for j in range(m):
            tr2 += C[i][j] * C[j][i]
    p1 = detA * tr
    p2 = detA * (tr * tr - tr2)
    return +detA, +p1, +p2


def mobius_superset(vals, n):
    out = vals[:]
    for i in range(n):
        bit = 1 << i
        for mask in range(1 << n):
            if not (mask & bit):
                out[mask] -= out[mask | bit]
    return [+x for x in out]


def all_indices(n):
    return [[i for i in range(n) if mask >> i & 1] for mask in range(1 << n)]


def exact_events_with_derivatives(K, Dmat):
    n = len(K)
    inds_by_mask = all_indices(n)
    q = [Decimal(0)] * (1 << n)
    q1 = [Decimal(0)] * (1 << n)
    q2 = [Decimal(0)] * (1 << n)
    for mask, inds in enumerate(inds_by_mask):
        q[mask], q1[mask], q2[mask] = inclusion_derivatives_decimal(K, Dmat, inds)
    return mobius_superset(q, n), mobius_superset(q1, n), mobius_superset(q2, n)


def exact_event_entropy(K):
    n = len(K)
    inds_by_mask = all_indices(n)
    q = [inclusion_det_decimal(K, inds) for inds in inds_by_mask]
    p = mobius_superset(q, n)
    H = Decimal(0)
    minp = min(p)
    for prob in p:
        H -= prob * prob.ln()
    return +H, +sum(p), +minp


def directional_metrics(K, Dmat):
    p, p1, p2 = exact_events_with_derivatives(K, Dmat)
    H = Decimal(0)
    fisher = Decimal(0)
    acceleration = Decimal(0)
    for prob, dp, ddp in zip(p, p1, p2):
        logp = prob.ln()
        H -= prob * logp
        fisher += dp * dp / prob
        acceleration -= ddp * logp
    H2 = acceleration - fisher
    rho = acceleration / fisher
    return {
        "entropy": +H,
        "fisher": +fisher,
        "acceleration": +acceleration,
        "H2": +H2,
        "rho": +rho,
        "sum_p": +sum(p),
        "sum_p1": +sum(p1),
        "sum_p2": +sum(p2),
        "min_atom": +min(p),
        "event_count": len(p),
    }


def add_decimal_mats(A, B, scale=Decimal(1)):
    n = len(A)
    return [[A[i][j] + scale * B[i][j] for j in range(n)] for i in range(n)]


def chord_metrics(K, Dmat, H0, steps):
    out = []
    for h in steps:
        Hminus, sum_minus, min_minus = exact_event_entropy(add_decimal_mats(K, Dmat, -h))
        Hplus, sum_plus, min_plus = exact_event_entropy(add_decimal_mats(K, Dmat, h))
        gap = (Hminus + Hplus) / 2 - H0
        central = 2 * gap / (h * h)
        out.append(
            {
                "step": str(h),
                "Hminus": dstr(Hminus),
                "Hplus": dstr(Hplus),
                "midpoint_gap": dstr(gap),
                "central_H2": dstr(central),
                "sum_minus": dstr(sum_minus),
                "sum_plus": dstr(sum_plus),
                "min_minus": dstr(min_minus),
                "min_plus": dstr(min_plus),
            }
        )
    return out


def ldl_fraction(A):
    n = len(A)
    L = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    Ddiag = [Fraction(0) for _ in range(n)]
    for i in range(n):
        L[i][i] = Fraction(1)
        for j in range(i):
            s = A[i][j]
            for k in range(j):
                s -= L[i][k] * L[j][k] * Ddiag[k]
            L[i][j] = s / Ddiag[j]
        diag = A[i][i]
        for k in range(i):
            diag -= L[i][k] * L[i][k] * Ddiag[k]
        Ddiag[i] = diag
    return Ddiag


def mat_fraction_combo(K, Dmat, t=Fraction(0), identity=Fraction(0)):
    n = len(K)
    return [[K[i][j] + t * Dmat[i][j] + (identity if i == j else 0) for j in range(n)] for i in range(n)]


def fraction_feasibility(Kf, Df):
    margin = Fraction(1, 2000)
    out = {
        "interpretation": "symmetrized float entries converted via 17-digit decimal strings to exact Fractions",
        "uniform_interval": ["-1/200", "1/200"],
        "strict_margin": "1/2000",
    }

    def piv_summary(A):
        piv = ldl_fraction(A)
        return {
            "count": len(piv),
            "all_positive": all(v > 0 for v in piv),
            "minimum_float": float(min(piv)),
            "minimum": str(min(piv)),
            "minimum_numerator_digits": len(str(abs(min(piv).numerator))),
            "minimum_denominator_digits": len(str(abs(min(piv).denominator))),
        }

    out["D_positive_definite"] = piv_summary(Df)
    endpoints = []
    n = len(Kf)
    IminusK_base = [[(Fraction(1) if i == j else Fraction(0)) - Kf[i][j] for j in range(n)] for i in range(n)]
    for t in [Fraction(-1, 200), Fraction(1, 200)]:
        Kt_margin = mat_fraction_combo(Kf, Df, t=t, identity=-margin)
        It_margin = mat_fraction_combo(IminusK_base, Df, t=-t, identity=-margin)
        endpoints.append(
            {
                "step": str(t),
                "K_t_minus_margin_I": piv_summary(Kt_margin),
                "I_minus_K_t_minus_margin_I": piv_summary(It_margin),
            }
        )
    out["endpoint_LDL"] = endpoints
    return out


def frob_norm_float(M):
    return float(np.sqrt(np.sum(np.asarray(M, dtype=float) ** 2)))


def matrix_float_checks(npz_path: Path):
    data = np.load(npz_path)
    K = (data["kernel"] + data["kernel"].T) / 2
    D = (data["direction"] + data["direction"].T) / 2
    Q = data["eigenvectors"]
    spectrum = data["spectrum"]
    rates = data["rates"]
    K_recon = Q @ np.diag(spectrum) @ Q.T
    D_recon = Q @ np.diag(rates) @ Q.T
    return {
        "npz_fields": list(data.files),
        "n": int(K.shape[0]),
        "kernel_symmetry_max": float(np.max(np.abs(data["kernel"] - data["kernel"].T))),
        "direction_symmetry_max": float(np.max(np.abs(data["direction"] - data["direction"].T))),
        "Q_orthogonality_frobenius": frob_norm_float(Q.T @ Q - np.eye(K.shape[0])),
        "kernel_reconstruction_frobenius": frob_norm_float(K - K_recon),
        "direction_reconstruction_frobenius": frob_norm_float(D - D_recon),
        "commutator_frobenius": frob_norm_float(K @ D - D @ K),
        "spectrum_min": float(np.min(spectrum)),
        "spectrum_max": float(np.max(spectrum)),
        "spectrum_margin": float(min(np.min(spectrum), np.min(1 - spectrum))),
        "rates_min": float(np.min(rates)),
        "rates_max": float(np.max(rates)),
    }


def parse_float(row, key):
    return float(row[key])


def ledger_and_manifest_audit():
    per = []
    all_rows = []
    for shard in range(4):
        rdir = ROOT / f"results_{shard}"
        ledger_path = rdir / "candidate_ledger.csv"
        rows = list(csv.DictReader(ledger_path.open(newline="", encoding="utf-8")))
        for row in rows:
            row["_shard"] = str(shard)
        manifest = json.loads((rdir / "manifest.json").read_text(encoding="utf-8"))
        best_json = json.loads((rdir / "best_case.json").read_text(encoding="utf-8"))
        log_lines = [json.loads(line) for line in (ROOT / f"run_{shard}.log").read_text(encoding="utf-8").splitlines() if line.strip()]
        source = [r for r in rows if r["index"] == "-1"]
        props = [r for r in rows if r["index"] != "-1"]
        non_no_hit = [r for r in rows if r["status"] != "NO_HIT"]
        pos_gap = [r for r in rows if parse_float(r, "chord_gap") > 0]
        rho_ge_one = [r for r in rows if parse_float(r, "rho_psd") >= 1.0]
        best_row = max(rows, key=lambda r: parse_float(r, "rho_psd"))
        best_match = (
            best_row["index"] == str(best_json["index"])
            and best_row["label"] == best_json["label"]
            and abs(parse_float(best_row, "rho_psd") - float(best_json["rho_psd"])) <= 1e-15
            and best_row["status"] == best_json["status"]
        )
        final_status = log_lines[-1]
        completed_values = [item.get("completed") for item in log_lines if "completed" in item]
        per.append(
            {
                "shard": shard,
                "ledger_rows": len(rows),
                "source_rows": len(source),
                "proposal_rows": len(props),
                "non_no_hit_rows": len(non_no_hit),
                "positive_gap_rows": len(pos_gap),
                "rho_ge_one_rows": len(rho_ge_one),
                "source_margin": min(parse_float(r, "spectrum_margin") for r in source),
                "proposal_min_margin": min(parse_float(r, "spectrum_margin") for r in props),
                "max_gap": max(parse_float(r, "chord_gap") for r in rows),
                "best_row": dict(best_row),
                "best_json": best_json,
                "best_row_matches_json": best_match,
                "manifest": manifest,
                "manifest_matches_counts": manifest["proposal_count"] == len(props)
                and manifest["ledger_rows_including_source"] == len(rows)
                and manifest["positive_count"] == 0
                and manifest["exit_code"] == 0,
                "log_line_count": len(log_lines),
                "log_max_completed": max(completed_values) if completed_values else None,
                "log_final_matches_manifest": final_status == manifest,
            }
        )
        all_rows.extend(rows)
    best_all = max(all_rows, key=lambda r: parse_float(r, "rho_psd"))
    return {
        "per_shard": per,
        "total_rows": len(all_rows),
        "proposal_rows": sum(1 for r in all_rows if r["index"] != "-1"),
        "source_rows": sum(1 for r in all_rows if r["index"] == "-1"),
        "non_no_hit_rows": sum(1 for r in all_rows if r["status"] != "NO_HIT"),
        "positive_gap_rows": sum(1 for r in all_rows if parse_float(r, "chord_gap") > 0),
        "rho_ge_one_rows": sum(1 for r in all_rows if parse_float(r, "rho_psd") >= 1.0),
        "proposal_min_margin": min(parse_float(r, "spectrum_margin") for r in all_rows if r["index"] != "-1"),
        "source_min_margin": min(parse_float(r, "spectrum_margin") for r in all_rows if r["index"] == "-1"),
        "max_gap": max(parse_float(r, "chord_gap") for r in all_rows),
        "best_row": dict(best_all),
    }


def collect_hashes():
    files = [
        "README.md",
        "commuting_spectral_search.py",
        "spectral_basis_refine.py",
        "prepare_interior_source.py",
        "interior_source_margin006.json",
        "interior_source_margin006.npz",
        "recheck_best_interior2.py",
        "recheck_best_interior2.json",
        "run_0.log",
        "run_1.log",
        "run_2.log",
        "run_3.log",
    ]
    out = {}
    for rel in files:
        p = ROOT / rel
        out[rel] = {"sha256": sha256(p), "bytes": p.stat().st_size}
    for shard in range(4):
        for rel in ["candidate_ledger.csv", "manifest.json", "best_case.json", "best_case.npz"]:
            p = ROOT / f"results_{shard}" / rel
            out[f"results_{shard}/{rel}"] = {"sha256": sha256(p), "bytes": p.stat().st_size}
    return out


def round_best_summary():
    names = [
        ("H10_round18_boundary1", COMMUTING / "results_server_round18_boundary1"),
        ("H11_round19_interior1", COMMUTING / "results_server_round19_interior1"),
        ("H12_round20_interior2", ROOT),
    ]
    out = []
    for name, path in names:
        best = None
        for p in sorted(path.glob("results_*/best_case.json")):
            row = json.loads(p.read_text(encoding="utf-8"))
            shard = int(p.parent.name.split("_")[-1])
            item = {
                "round": name,
                "shard": shard,
                "index": row["index"],
                "rho_psd": float(row["rho_psd"]),
                "spectrum_margin": float(row["spectrum_margin"]),
                "chord_gap": float(row["chord_gap"]),
                "status": row["status"],
                "label": row["label"],
            }
            if best is None or item["rho_psd"] > best["rho_psd"]:
                best = item
        out.append(best)
    if len(out) == 3:
        out[2]["drop_from_H10"] = out[0]["rho_psd"] - out[2]["rho_psd"]
        out[2]["drop_from_H11"] = out[1]["rho_psd"] - out[2]["rho_psd"]
        out[2]["retained_fraction_of_H10"] = out[2]["rho_psd"] / out[0]["rho_psd"]
    return out


def main():
    start = time.time()
    ledger = ledger_and_manifest_audit()
    strongest_shard = int(ledger["best_row"]["_shard"])
    strongest_index = int(ledger["best_row"]["index"])
    strongest_npz = ROOT / f"results_{strongest_shard}" / "best_case.npz"
    data = np.load(str(strongest_npz))
    Kd = sym_decimal(data["kernel"])
    Dd = sym_decimal(data["direction"])
    Kf = sym_fraction(data["kernel"])
    Df = sym_fraction(data["direction"])
    directional = directional_metrics(Kd, Dd)
    best_json = json.loads((ROOT / f"results_{strongest_shard}" / "best_case.json").read_text(encoding="utf-8"))
    steps = [Decimal(str(best_json["chord_step"])), Decimal("0.001"), Decimal("0.0001")]
    chords = chord_metrics(Kd, Dd, directional["entropy"], steps)
    feasibility = fraction_feasibility(Kf, Df)
    matrix_checks = matrix_float_checks(strongest_npz)

    checks = {
        "four_shards": len(ledger["per_shard"]) == 4,
        "total_rows_20004": ledger["total_rows"] == 20004,
        "proposal_rows_20000": ledger["proposal_rows"] == 20000,
        "source_rows_4": ledger["source_rows"] == 4,
        "all_status_no_hit": ledger["non_no_hit_rows"] == 0,
        "no_positive_gaps": ledger["positive_gap_rows"] == 0,
        "no_rho_ge_one": ledger["rho_ge_one_rows"] == 0,
        "source_margin_at_least_006": ledger["source_min_margin"] >= 0.059999999,
        "proposal_margin_at_least_005": ledger["proposal_min_margin"] >= 0.049999999,
        "best_is_shard1_index2701": strongest_shard == 1 and strongest_index == 2701,
        "best_rho_matches_expected": abs(float(ledger["best_row"]["rho_psd"]) - 0.5729410207438331) <= 1e-15,
        "all_manifests_counts_ok": all(x["manifest_matches_counts"] for x in ledger["per_shard"]),
        "all_best_json_match_ledger": all(x["best_row_matches_json"] for x in ledger["per_shard"]),
        "all_logs_end_with_manifest": all(x["log_final_matches_manifest"] for x in ledger["per_shard"]),
        "decimal_H2_negative": directional["H2"] < 0,
        "decimal_rho_below_one": directional["rho"] < 1,
        "all_chords_negative": all(Decimal(c["midpoint_gap"]) < 0 for c in chords),
        "fraction_D_positive": feasibility["D_positive_definite"]["all_positive"],
        "fraction_endpoint_margins_positive": all(
            e["K_t_minus_margin_I"]["all_positive"] and e["I_minus_K_t_minus_margin_I"]["all_positive"]
            for e in feasibility["endpoint_LDL"]
        ),
    }
    status = "PASS" if all(checks.values()) else "FAIL"
    result = {
        "status": status,
        "scope": "stored-data accounting plus strongest-point independent Decimal/Fraction gate; no seed regeneration",
        "author_input_hashes": collect_hashes(),
        "ledger": ledger,
        "strongest_shard": strongest_shard,
        "strongest_index": strongest_index,
        "strongest_npz_sha256": sha256(strongest_npz),
        "matrix_float_checks": matrix_checks,
        "decimal_precision": getcontext().prec,
        "decimal_directional": {k: (dstr(v) if isinstance(v, Decimal) else v) for k, v in directional.items()},
        "decimal_chords": chords,
        "fraction_feasibility": feasibility,
        "round_comparison": round_best_summary(),
        "checks": checks,
        "elapsed_seconds": time.time() - start,
    }
    out = HERE / "fresh_audit.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    if status != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
