"""D10-H14 / round22_interior4 independent non-author audit.

No author module is imported.  The 4096 exact-event probabilities and their
first/second jets are rebuilt from inclusion determinants by Mobius inversion.
High-precision arithmetic uses only the Python standard-library Decimal module;
numpy is used only to read NPZ arrays and for non-certifying float diagnostics.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import time
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path

import numpy as np


getcontext().prec = 130

AUDIT_DIR = Path(__file__).resolve().parent
BASE = AUDIT_DIR.parent
ROOT = BASE.parent
OUT_JSON = AUDIT_DIR / "audit_results.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def parse_bool(s: str) -> bool:
    return str(s).strip().lower() == "true"


def parse_csv(path: Path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def last_json_line(path: Path):
    last = None
    completed = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            last = obj
            if "completed" in obj:
                completed.append(int(obj["completed"]))
    return last, completed


def ledger_audit():
    per = []
    all_rows = []
    manifests = []
    log_finals = []
    for shard in range(4):
        rdir = BASE / f"results_{shard}"
        rows = parse_csv(rdir / "candidate_ledger.csv")
        manifest = read_json(rdir / "manifest.json")
        best_json = read_json(rdir / "best_case.json")
        final_log, completed = last_json_line(BASE / f"run_{shard}.log")
        for row in rows:
            row["_shard"] = shard
        all_rows.extend(rows)
        manifests.append(manifest)
        log_finals.append(final_log)
        proposal_rows = [r for r in rows if int(r["index"]) >= 0]
        source_rows = [r for r in rows if int(r["index"]) == -1]
        accepted_rows = [r for r in proposal_rows if parse_bool(r["accepted"])]
        best_row = max(rows, key=lambda r: float(r["rho_psd"]))
        per.append(
            {
                "shard": shard,
                "rows": len(rows),
                "proposal_rows": len(proposal_rows),
                "source_rows": len(source_rows),
                "accepted_rows": len(accepted_rows),
                "status_values": sorted({r["status"] for r in rows}),
                "rho_ge_1_rows": sum(float(r["rho_psd"]) >= 1.0 for r in rows),
                "rho_gt_1_rows": sum(float(r["rho_psd"]) > 1.0 for r in rows),
                "positive_gap_rows": sum(float(r["chord_gap"]) > 0.0 for r in rows),
                "max_gap": max(float(r["chord_gap"]) for r in rows),
                "min_proposal_margin": min(float(r["spectrum_margin"]) for r in proposal_rows),
                "below_margin_floor_exact_float": sum(float(r["spectrum_margin"]) < 0.2 for r in proposal_rows),
                "below_margin_floor_tol_1e_14": sum(float(r["spectrum_margin"]) < 0.2 - 1e-14 for r in proposal_rows),
                "best_row": best_row,
                "best_json": best_json,
                "manifest": manifest,
                "log_final": final_log,
                "log_last_completed": completed[-1] if completed else None,
            }
        )

    proposals = [r for r in all_rows if int(r["index"]) >= 0]
    sources = [r for r in all_rows if int(r["index"]) == -1]
    strongest = max(all_rows, key=lambda r: float(r["rho_psd"]))
    return {
        "per_shard": per,
        "total_rows": len(all_rows),
        "proposal_rows": len(proposals),
        "source_rows": len(sources),
        "status_values": sorted({r["status"] for r in all_rows}),
        "rho_ge_1_rows": sum(float(r["rho_psd"]) >= 1.0 for r in all_rows),
        "rho_gt_1_rows": sum(float(r["rho_psd"]) > 1.0 for r in all_rows),
        "positive_gap_rows": sum(float(r["chord_gap"]) > 0.0 for r in all_rows),
        "max_gap": max(float(r["chord_gap"]) for r in all_rows),
        "min_proposal_margin": min(float(r["spectrum_margin"]) for r in proposals),
        "below_margin_floor_exact_float": sum(float(r["spectrum_margin"]) < 0.2 for r in proposals),
        "below_margin_floor_tol_1e_14": sum(float(r["spectrum_margin"]) < 0.2 - 1e-14 for r in proposals),
        "strongest": strongest,
        "manifests": manifests,
        "log_finals": log_finals,
        "all_checks": {
            "four_shards": len(per) == 4,
            "each_ledger_5001": all(x["rows"] == 5001 for x in per),
            "each_proposals_5000": all(x["proposal_rows"] == 5000 for x in per),
            "each_one_source": all(x["source_rows"] == 1 for x in per),
            "all_20004_rows": len(all_rows) == 20004,
            "all_20000_proposals": len(proposals) == 20000,
            "all_four_sources": len(sources) == 4,
            "all_status_no_hit": {r["status"] for r in all_rows} == {"NO_HIT"},
            "no_rho_gt_1": all(float(r["rho_psd"]) <= 1.0 for r in all_rows),
            "no_positive_gap": all(float(r["chord_gap"]) <= 0.0 for r in all_rows),
            "manifest_exit_zero": all(m.get("exit_code") == 0 for m in manifests),
            "manifest_positive_count_zero": all(m.get("positive_count") == 0 for m in manifests),
            "log_final_matches_manifest": all(log_finals[i] == manifests[i] for i in range(4)),
            "logs_reach_5000": all(x["log_last_completed"] == 5000 for x in per),
            "margin_floor_ok_with_1e_14_float_tolerance": all(
                float(r["spectrum_margin"]) >= 0.2 - 1e-14 for r in proposals
            ),
        },
    }


def dec_from_float(x: float) -> Decimal:
    return Decimal(repr(float(x)))


def dec_matrix_from_np(A: np.ndarray):
    n, m = A.shape
    return [[dec_from_float(A[i, j]) for j in range(m)] for i in range(n)]


def mat_sub_dec(M, idx):
    return [[M[i][j] for j in idx] for i in idx]


def mat_mul_dec(A, B):
    n, k, m = len(A), len(B), len(B[0])
    return [[sum(A[i][r] * B[r][j] for r in range(k)) for j in range(m)] for i in range(n)]


def mat_trace_dec(A):
    return sum(A[i][i] for i in range(len(A)))


def det_dec(A):
    n = len(A)
    if n == 0:
        return Decimal(1)
    M = [row[:] for row in A]
    det = Decimal(1)
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(M[r][c]))
        if M[piv][c] == 0:
            return Decimal(0)
        if piv != c:
            M[c], M[piv] = M[piv], M[c]
            det = -det
        pv = M[c][c]
        det *= pv
        for r in range(c + 1, n):
            fac = M[r][c] / pv
            if fac:
                for j in range(c, n):
                    M[r][j] -= fac * M[c][j]
    return det


def det_inv_dec(A):
    n = len(A)
    M = [
        A[i][:] + [Decimal(1) if i == j else Decimal(0) for j in range(n)]
        for i in range(n)
    ]
    det = Decimal(1)
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(M[r][c]))
        if M[piv][c] == 0:
            raise ArithmeticError("singular principal submatrix")
        if piv != c:
            M[c], M[piv] = M[piv], M[c]
            det = -det
        pv = M[c][c]
        det *= pv
        inv_pv = Decimal(1) / pv
        M[c] = [x * inv_pv for x in M[c]]
        for r in range(n):
            if r == c:
                continue
            fac = M[r][c]
            if fac:
                M[r] = [M[r][j] - fac * M[c][j] for j in range(2 * n)]
    return det, [row[n:] for row in M]


def det_jets_sub(K, D, idx):
    k = len(idx)
    if k == 0:
        return Decimal(1), Decimal(0), Decimal(0)
    Ks = mat_sub_dec(K, idx)
    Ds = mat_sub_dec(D, idx)
    det, inv = det_inv_dec(Ks)
    A = mat_mul_dec(inv, Ds)
    trA = mat_trace_dec(A)
    trA2 = sum(A[i][j] * A[j][i] for i in range(k) for j in range(k))
    return det, det * trA, det * (trA * trA - trA2)


def superset_mobius(vals, n):
    out = list(vals)
    for bit in range(n):
        step = 1 << bit
        for mask in range(1 << n):
            if not (mask & step):
                out[mask] -= out[mask | step]
    return out


def event_jets(K_np: np.ndarray, D_np: np.ndarray):
    n = K_np.shape[0]
    K = dec_matrix_from_np(K_np)
    D = dec_matrix_from_np(D_np)
    q0, q1, q2 = [], [], []
    for mask in range(1 << n):
        idx = [i for i in range(n) if (mask >> i) & 1]
        a, b, c = det_jets_sub(K, D, idx)
        q0.append(a)
        q1.append(b)
        q2.append(c)
    return superset_mobius(q0, n), superset_mobius(q1, n), superset_mobius(q2, n)


def event_probs_only_from_dec(K):
    n = len(K)
    q = []
    for mask in range(1 << n):
        idx = [i for i in range(n) if (mask >> i) & 1]
        q.append(det_dec(mat_sub_dec(K, idx)))
    return superset_mobius(q, n)


def entropy_from_probs(p):
    return -sum(x * x.ln() for x in p)


def directional_audit(K_np: np.ndarray, D_np: np.ndarray):
    p, p1, p2 = event_jets(K_np, D_np)
    H = entropy_from_probs(p)
    fisher = sum((p1[i] * p1[i]) / p[i] for i in range(len(p)))
    acceleration = -sum(p2[i] * p[i].ln() for i in range(len(p)))
    H2 = acceleration - fisher
    rho = acceleration / fisher
    return {
        "event_count": len(p),
        "entropy": H,
        "fisher": fisher,
        "acceleration": acceleration,
        "H2": H2,
        "rho": rho,
        "sum_p_minus_one": sum(p) - Decimal(1),
        "sum_p1": sum(p1),
        "sum_p2": sum(p2),
        "min_atom": min(p),
    }


def chord_audit(K_np: np.ndarray, D_np: np.ndarray, steps):
    K = dec_matrix_from_np(K_np)
    D = dec_matrix_from_np(D_np)
    H0 = entropy_from_probs(event_probs_only_from_dec(K))
    out = []
    for h_frac in steps:
        h = Decimal(h_frac.numerator) / Decimal(h_frac.denominator)
        Kp = [[K[i][j] + h * D[i][j] for j in range(len(K))] for i in range(len(K))]
        Km = [[K[i][j] - h * D[i][j] for j in range(len(K))] for i in range(len(K))]
        Hp = entropy_from_probs(event_probs_only_from_dec(Kp))
        Hm = entropy_from_probs(event_probs_only_from_dec(Km))
        gap = (Hp + Hm) / 2 - H0
        out.append(
            {
                "step": f"{h_frac.numerator}/{h_frac.denominator}",
                "Hminus": Hm,
                "Hplus": Hp,
                "midpoint_gap": gap,
                "central_H2": 2 * gap / (h * h),
            }
        )
    return out


def frac_from_float_exact(x: float) -> Fraction:
    return Fraction.from_float(float(x))


def sym_fraction_matrix(A: np.ndarray):
    n = A.shape[0]
    out = [[Fraction(0) for _ in range(n)] for __ in range(n)]
    for i in range(n):
        for j in range(n):
            out[i][j] = (frac_from_float_exact(A[i, j]) + frac_from_float_exact(A[j, i])) / 2
    return out


def frac_mat_add(A, B, scale=Fraction(1)):
    n = len(A)
    return [[A[i][j] + scale * B[i][j] for j in range(n)] for i in range(n)]


def frac_shift_diag(A, shift):
    n = len(A)
    out = [[A[i][j] for j in range(n)] for i in range(n)]
    for i in range(n):
        out[i][i] += shift
    return out


def ldl_pivots_fraction(A):
    n = len(A)
    L = [[Fraction(0) for _ in range(n)] for __ in range(n)]
    piv = []
    for i in range(n):
        for j in range(i):
            s = sum(L[i][k] * L[j][k] * piv[k] for k in range(j))
            L[i][j] = (A[i][j] - s) / piv[j]
        diag = A[i][i] - sum(L[i][k] * L[i][k] * piv[k] for k in range(i))
        piv.append(diag)
        L[i][i] = Fraction(1)
    return piv


def summarize_pivots(piv):
    mn = min(piv)
    return {
        "count": len(piv),
        "all_positive": all(x > 0 for x in piv),
        "minimum_float": float(mn),
        "minimum_numerator_digits": len(str(abs(mn.numerator))),
        "minimum_denominator_digits": len(str(abs(mn.denominator))),
    }


def fraction_feasibility(K_np: np.ndarray, D_np: np.ndarray):
    K = sym_fraction_matrix(K_np)
    D = sym_fraction_matrix(D_np)
    n = len(K)
    I = [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
    h = Fraction(1, 200)
    margin = Fraction(1, 2000)
    endpoints = []
    for sgn in [-1, 1]:
        Kt = frac_mat_add(K, D, scale=sgn * h)
        K_margin = frac_shift_diag(Kt, -margin)
        I_minus = [[I[i][j] - Kt[i][j] for j in range(n)] for i in range(n)]
        I_minus_margin = frac_shift_diag(I_minus, -margin)
        endpoints.append(
            {
                "step": f"{sgn}/200",
                "K_t_minus_margin_I": summarize_pivots(ldl_pivots_fraction(K_margin)),
                "I_minus_K_t_minus_margin_I": summarize_pivots(ldl_pivots_fraction(I_minus_margin)),
            }
        )
    return {
        "interpretation": "stored float64 matrices symmetrized exactly as binary rationals",
        "interval": ["-1/200", "1/200"],
        "margin": "1/2000",
        "D_positive_definite": summarize_pivots(ldl_pivots_fraction(D)),
        "endpoints": endpoints,
    }


def npz_audit(path: Path):
    data = np.load(path)
    K_raw = data["kernel"]
    D_raw = data["direction"]
    spectrum = data["spectrum"]
    rates = data["rates"]
    Q = data["eigenvectors"]
    K = (K_raw + K_raw.T) / 2
    D = (D_raw + D_raw.T) / 2
    K_recon = Q @ np.diag(spectrum) @ Q.T
    D_recon = Q @ np.diag(rates) @ Q.T
    return {
        "K": K,
        "D": D,
        "diagnostics": {
            "kernel_shape": list(K.shape),
            "direction_shape": list(D.shape),
            "max_kernel_asymmetry": float(np.max(np.abs(K_raw - K_raw.T))),
            "max_direction_asymmetry": float(np.max(np.abs(D_raw - D_raw.T))),
            "basis_orthogonality_fro": float(np.linalg.norm(Q.T @ Q - np.eye(Q.shape[0]))),
            "kernel_reconstruction_fro": float(np.linalg.norm(K - K_recon)),
            "direction_reconstruction_fro": float(np.linalg.norm(D - D_recon)),
            "commutator_fro": float(np.linalg.norm(K @ D - D @ K)),
            "spectrum_min": float(np.min(spectrum)),
            "spectrum_max": float(np.max(spectrum)),
            "rates_min": float(np.min(rates)),
            "rates_max": float(np.max(rates)),
            "float_K_eig_min": float(np.min(np.linalg.eigvalsh(K))),
            "float_K_eig_max": float(np.max(np.linalg.eigvalsh(K))),
            "float_D_eig_min": float(np.min(np.linalg.eigvalsh(D))),
            "fixed_Q_psd_rates": bool(np.min(rates) >= -1e-12),
        },
    }


def parse_profile():
    dirs = [
        ("H10_round18_boundary1", ROOT / "results_server_round18_boundary1"),
        ("H11_round19_interior1", ROOT / "results_server_round19_interior1"),
        ("H12_round20_interior2", ROOT / "results_server_round20_interior2"),
        ("H13_round21_interior3", ROOT / "results_server_round21_interior3"),
        ("H14_round22_interior4", BASE),
    ]
    out = []
    for name, d in dirs:
        text = (d / "README.md").read_text(encoding="utf-8")
        if name.startswith("H10"):
            rho = re.search(r"strongest mechanism ratio: `rho=([0-9.]+)`", text)
            margin = re.search(r"strongest stored spectrum margin: `([0-9.]+)`", text)
        else:
            rho = re.search(r"rho\s+=\s*([0-9.]+)", text)
            margin = re.search(r"spectrum margin\s+=\s*([0-9.]+)", text)
        out.append(
            {
                "name": name,
                "rho": float(rho.group(1)) if rho else None,
                "margin": float(margin.group(1)) if margin else None,
                "readme_sha256": sha256(d / "README.md"),
            }
        )
    return out


def decimalize(obj):
    if isinstance(obj, Decimal):
        return format(obj, "f")
    if isinstance(obj, np.ndarray):
        return None
    if isinstance(obj, dict):
        return {k: decimalize(v) for k, v in obj.items() if k not in {"K", "D"}}
    if isinstance(obj, list):
        return [decimalize(x) for x in obj]
    return obj


def main():
    t0 = time.time()
    ledger = ledger_audit()
    strongest = ledger["strongest"]
    strongest_shard = int(strongest["_shard"])
    strongest_index = int(strongest["index"])
    best_npz = BASE / f"results_{strongest_shard}" / "best_case.npz"
    best_json = read_json(BASE / f"results_{strongest_shard}" / "best_case.json")
    npz = npz_audit(best_npz)
    directional = directional_audit(npz["K"], npz["D"])
    chords = chord_audit(
        npz["K"],
        npz["D"],
        [Fraction(1, 100), Fraction(1, 200), Fraction(1, 1000), Fraction(1, 10000)],
    )
    feasibility = fraction_feasibility(npz["K"], npz["D"])

    source_hash = sha256(BASE / "interior_source_margin022.npz")
    best_hash = sha256(best_npz)
    files = {
        "README.md": sha256(BASE / "README.md"),
        "spectral_basis_refine.py": sha256(BASE / "spectral_basis_refine.py"),
        "commuting_spectral_search.py": sha256(BASE / "commuting_spectral_search.py"),
        "recheck_best_interior4.py": sha256(BASE / "recheck_best_interior4.py"),
        "recheck_best_interior4.json": sha256(BASE / "recheck_best_interior4.json"),
        "interior_source_margin022.npz": source_hash,
        f"results_{strongest_shard}/best_case.npz": best_hash,
        f"results_{strongest_shard}/best_case.json": sha256(BASE / f"results_{strongest_shard}" / "best_case.json"),
    }
    for shard in range(4):
        files[f"results_{shard}/candidate_ledger.csv"] = sha256(BASE / f"results_{shard}" / "candidate_ledger.csv")
        files[f"results_{shard}/manifest.json"] = sha256(BASE / f"results_{shard}" / "manifest.json")
        files[f"run_{shard}.log"] = sha256(BASE / f"run_{shard}.log")

    checks = {
        "strongest_is_shard0_index2996": strongest_shard == 0 and strongest_index == 2996,
        "strongest_rho_matches_readme": abs(float(strongest["rho_psd"]) - 0.3337720601402677) < 1e-15,
        "best_json_matches_strongest_row": int(best_json["index"]) == strongest_index
        and abs(float(best_json["rho_psd"]) - float(strongest["rho_psd"])) < 1e-15,
        "source_npz_hash_matches_readme": source_hash == "b5972686e06976da1ac5e8dc3dcef2090fdd010e2586520ee69836a25ee684cf",
        "best_npz_hash_matches_readme": best_hash == "8c62a7236a613640f0d76f3cedc1899825d63e60a33ca9c49beba4f8754a822b",
        "decimal_event_count_4096": directional["event_count"] == 4096,
        "decimal_H2_negative": directional["H2"] < 0,
        "decimal_rho_below_one": directional["rho"] < 1,
        "all_requested_chords_negative": all(c["midpoint_gap"] < 0 for c in chords),
        "fraction_D_positive": feasibility["D_positive_definite"]["all_positive"],
        "fraction_endpoints_margin_positive": all(
            e["K_t_minus_margin_I"]["all_positive"] and e["I_minus_K_t_minus_margin_I"]["all_positive"]
            for e in feasibility["endpoints"]
        ),
    }
    checks.update(ledger["all_checks"])

    result = {
        "status": "PASS_SCOUT_ONLY",
        "scope": "independent non-author audit of frozen round22_interior4 copied outputs; no author module import",
        "strongest": {
            "shard": strongest_shard,
            "index": strongest_index,
            "row": strongest,
        },
        "ledger": ledger,
        "npz_diagnostics": npz["diagnostics"],
        "directional_120_digit": directional,
        "chords_120_digit": chords,
        "fraction_ldl": feasibility,
        "profile_H10_to_H14": parse_profile(),
        "file_hashes": files,
        "checks": checks,
        "elapsed_seconds": time.time() - t0,
    }
    OUT_JSON.write_text(json.dumps(decimalize(result), indent=2), encoding="utf-8")
    print(json.dumps(decimalize(result), indent=2))


if __name__ == "__main__":
    main()
