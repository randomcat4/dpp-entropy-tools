"""Fresh non-author audit for D10-H2 round6 analysis.

This script intentionally does not import the author's recheck modules.  It
loads only the frozen round6 NPZ/CSV inputs and writes only inside this
verifications directory.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import time
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(key, "1")
os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")

import numpy as np


HERE = Path(__file__).resolve().parent
ANALYSIS = HERE.parent
DENSE = ANALYSIS.parent
SOURCE = DENSE / "results_server_round6"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def symmetrized_frozen() -> tuple[np.ndarray, np.ndarray, dict[str, float]]:
    data = np.load(SOURCE / "best_mechanism_case.npz")
    raw_k = np.asarray(data["kernel"], dtype=float)
    raw_d = np.asarray(data["direction"], dtype=float)
    k = (raw_k + raw_k.T) / 2.0
    d = (raw_d + raw_d.T) / 2.0
    meta = {
        "raw_kernel_asymmetry_max": float(np.max(np.abs(raw_k - raw_k.T))),
        "raw_direction_asymmetry_max": float(np.max(np.abs(raw_d - raw_d.T))),
        "symmetrization_kernel_max_change": float(np.max(np.abs(k - raw_k))),
        "symmetrization_direction_max_change": float(np.max(np.abs(d - raw_d))),
    }
    return k, d, meta


def principal_det_float(k: np.ndarray, mask: int) -> float:
    idx = [i for i in range(len(k)) if (mask >> i) & 1]
    if not idx:
        return 1.0
    return float(np.linalg.det(k[np.ix_(idx, idx)]))


def mobius_atoms_float(k: np.ndarray) -> np.ndarray:
    n = len(k)
    vals = np.array([principal_det_float(k, mask) for mask in range(1 << n)], dtype=float)
    for i in range(n):
        bit = 1 << i
        for mask in range(1 << n):
            if not (mask & bit):
                vals[mask] -= vals[mask | bit]
    return vals


def mixed_atoms_float(k: np.ndarray) -> tuple[np.ndarray, np.ndarray, list[np.ndarray]]:
    n = len(k)
    probs = np.empty(1 << n, dtype=float)
    logs = np.empty(1 << n, dtype=float)
    matrices: list[np.ndarray] = []
    for mask in range(1 << n):
        absent_count = n - mask.bit_count()
        b = k.copy()
        for i in range(n):
            if not ((mask >> i) & 1):
                b[i, i] -= 1.0
        det = float(np.linalg.det(b))
        p = det * ((-1.0) ** absent_count)
        probs[mask] = p
        logs[mask] = math.log(p)
        matrices.append(b)
    return probs, logs, matrices


def l_ensemble_atoms_float(k: np.ndarray) -> np.ndarray:
    n = len(k)
    eye = np.eye(n)
    lmat = np.linalg.solve(eye - k, k)
    sign_base, log_base = np.linalg.slogdet(eye - k)
    if sign_base <= 0:
        raise AssertionError("I-K is not positive definite in float L-ensemble check")
    out = np.empty(1 << n, dtype=float)
    for mask in range(1 << n):
        idx = [i for i in range(n) if (mask >> i) & 1]
        if not idx:
            log_det = 0.0
        else:
            sign, log_det = np.linalg.slogdet(lmat[np.ix_(idx, idx)])
            if sign <= 0:
                raise AssertionError("nonpositive L principal minor in float check")
        out[mask] = math.exp(log_base + log_det)
    return out


def directional_float(k: np.ndarray, d: np.ndarray) -> dict[str, float]:
    p, lp, matrices = mixed_atoms_float(k)
    fisher = 0.0
    accel = 0.0
    sum_p1 = 0.0
    sum_p2 = 0.0
    for prob, logp, b in zip(p, lp, matrices):
        x = np.linalg.solve(b, d)
        score = float(np.trace(x))
        second = float(score * score - np.trace(x @ x))
        fisher += prob * score * score
        accel -= prob * logp * second
        sum_p1 += prob * score
        sum_p2 += prob * second
    return {
        "H": float(-np.dot(p, lp)),
        "Fisher_positive": float(fisher),
        "acceleration": float(accel),
        "H2": float(accel - fisher),
        "rho": float(accel / fisher),
        "normalization_error": float(np.sum(p) - 1.0),
        "sum_p1": float(sum_p1),
        "sum_p2": float(sum_p2),
        "min_probability": float(np.min(p)),
    }


def commuting_subspace_float(k: np.ndarray) -> dict[str, object]:
    p, lp, matrices = mixed_atoms_float(k)
    eigvals, q = np.linalg.eigh(k)
    basis = np.einsum("ia,ja->aij", q, q)
    m = len(basis)
    fisher = np.zeros((m, m), dtype=float)
    accel = np.zeros((m, m), dtype=float)
    for prob, logp, b in zip(p, lp, matrices):
        inv_b = np.linalg.inv(b)
        score = np.einsum("ij,aji->a", inv_b, basis)
        y = np.einsum("ij,ajk->aik", inv_b, basis, optimize=True)
        tr_y = np.einsum("aij,bji->ab", y, y, optimize=True)
        outer = np.outer(score, score)
        fisher += prob * outer
        accel += -prob * logp * (outer - tr_y)
    fisher = (fisher + fisher.T) / 2.0
    accel = (accel + accel.T) / 2.0
    feig, fu = np.linalg.eigh(fisher)
    if feig[0] <= 0:
        raise AssertionError("commuting Fisher matrix is not positive definite")
    whitener = fu / np.sqrt(feig)[None, :]
    rho_vals, rho_vecs = np.linalg.eigh(whitener.T @ accel @ whitener)
    coeff = whitener @ rho_vecs[:, -1]
    direction = np.einsum("a,aij->ij", coeff, basis)
    direction = (direction + direction.T) / 2.0
    direction /= np.linalg.norm(direction, 2)
    if np.trace(direction) < 0:
        direction = -direction
    check = directional_float(k, direction)
    return {
        "kernel_eigenvalues": eigvals.tolist(),
        "dimension": m,
        "rho_max": float(rho_vals[-1]),
        "fisher_min_eigenvalue": float(feig[0]),
        "fisher_max_eigenvalue": float(feig[-1]),
        "directional_recheck": check,
        "commutator_frobenius": float(np.linalg.norm(k @ direction - direction @ k)),
        "direction_min_eigenvalue": float(np.linalg.eigvalsh(direction)[0]),
        "direction_max_eigenvalue": float(np.linalg.eigvalsh(direction)[-1]),
    }


def decimal_matrix_from_float(a: np.ndarray) -> list[list[Decimal]]:
    return [[Decimal(repr(float(x))) for x in row] for row in a]


def decimal_det_and_solve(a_in: list[list[Decimal]], rhs_in: list[list[Decimal]] | None = None):
    n = len(a_in)
    a = [row[:] for row in a_in]
    rhs = None if rhs_in is None else [row[:] for row in rhs_in]
    det = Decimal(1)
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(a[r][col]))
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            if rhs is not None:
                rhs[col], rhs[pivot] = rhs[pivot], rhs[col]
            det = -det
        pv = a[col][col]
        if pv == 0:
            raise AssertionError("singular mixed matrix")
        det *= pv
        for row in range(col + 1, n):
            factor = a[row][col] / pv
            a[row][col] = Decimal(0)
            for j in range(col + 1, n):
                a[row][j] -= factor * a[col][j]
            if rhs is not None:
                for j in range(n):
                    rhs[row][j] -= factor * rhs[col][j]
    if rhs is None:
        return det, None
    x = [[Decimal(0) for _ in range(n)] for _ in range(n)]
    for row in range(n - 1, -1, -1):
        for j in range(n):
            tail = sum(a[row][c] * x[c][j] for c in range(row + 1, n))
            x[row][j] = (rhs[row][j] - tail) / a[row][row]
    return det, x


def decimal_directional(k_np: np.ndarray, d_np: np.ndarray, precision: int = 70) -> dict[str, str]:
    with localcontext() as ctx:
        ctx.prec = precision
        k = decimal_matrix_from_float(k_np)
        d = decimal_matrix_from_float(d_np)
        n = len(k)
        norm = Decimal(0)
        entropy = Decimal(0)
        fisher = Decimal(0)
        accel = Decimal(0)
        sum_p1 = Decimal(0)
        sum_p2 = Decimal(0)
        min_prob = Decimal(1)
        for mask in range(1 << n):
            b = [row[:] for row in k]
            absent = n - mask.bit_count()
            for i in range(n):
                if not ((mask >> i) & 1):
                    b[i][i] -= Decimal(1)
            det, x = decimal_det_and_solve(b, d)
            prob = det * (Decimal(-1) if absent % 2 else Decimal(1))
            if prob <= 0:
                raise AssertionError("nonpositive exact atom in Decimal mixed determinant")
            logp = prob.ln()
            score = sum(x[i][i] for i in range(n))
            tr_x2 = sum(x[i][j] * x[j][i] for i in range(n) for j in range(n))
            second = score * score - tr_x2
            norm += prob
            entropy -= prob * logp
            fisher += prob * score * score
            accel -= prob * logp * second
            sum_p1 += prob * score
            sum_p2 += prob * second
            if prob < min_prob:
                min_prob = prob
        h2 = accel - fisher
        return {
            "precision": str(precision),
            "H": str(+entropy),
            "Fisher_positive": str(+fisher),
            "acceleration": str(+accel),
            "H2": str(+h2),
            "rho": str(+(accel / fisher)),
            "sum_p": str(+norm),
            "sum_p1": str(+sum_p1),
            "sum_p2": str(+sum_p2),
            "min_probability": str(+min_prob),
        }


def decimal_entropy_only(k_np: np.ndarray, precision: int = 70) -> Decimal:
    with localcontext() as ctx:
        ctx.prec = precision
        k = decimal_matrix_from_float(k_np)
        return decimal_entropy_matrix(k)


def decimal_entropy_matrix(k: list[list[Decimal]]) -> Decimal:
        n = len(k)
        entropy = Decimal(0)
        norm = Decimal(0)
        for mask in range(1 << n):
            b = [row[:] for row in k]
            absent = n - mask.bit_count()
            for i in range(n):
                if not ((mask >> i) & 1):
                    b[i][i] -= Decimal(1)
            det, _ = decimal_det_and_solve(b, None)
            prob = det * (Decimal(-1) if absent % 2 else Decimal(1))
            if prob <= 0:
                raise AssertionError("nonpositive exact atom in Decimal entropy-only check")
            norm += prob
            entropy -= prob * prob.ln()
        if abs(norm - Decimal(1)) > Decimal("1e-55"):
            raise AssertionError("Decimal probabilities do not normalize")
        return +entropy


def fraction_matrix_from_float(a: np.ndarray) -> list[list[Fraction]]:
    return [[Fraction(repr(float(x))) for x in row] for row in a]


def ldl_fraction(a: list[list[Fraction]]) -> list[Fraction]:
    n = len(a)
    l = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    pivots: list[Fraction] = []
    for j in range(n):
        val = a[j][j] - sum(l[j][k] * l[j][k] * pivots[k] for k in range(j))
        if val <= 0:
            raise AssertionError(f"nonpositive LDL pivot at {j}")
        pivots.append(val)
        for i in range(j + 1, n):
            l[i][j] = (a[i][j] - sum(l[i][k] * l[j][k] * pivots[k] for k in range(j))) / val
    return pivots


def mat_add_scaled(k, d, h: Fraction):
    n = len(k)
    return [[k[i][j] + h * d[i][j] for j in range(n)] for i in range(n)]


def mat_shift(a, shift: Fraction):
    n = len(a)
    return [[a[i][j] - shift * Fraction(int(i == j)) for j in range(n)] for i in range(n)]


def eye_minus_shifted(a, eps: Fraction):
    n = len(a)
    return [[(Fraction(1) - eps) * Fraction(int(i == j)) - a[i][j] for j in range(n)] for i in range(n)]


def compact_pivots(pivots: list[Fraction]) -> dict[str, object]:
    m = min(pivots)
    return {
        "count": len(pivots),
        "all_positive": all(x > 0 for x in pivots),
        "min_pivot_float": float(m),
        "min_pivot_numerator_digits": len(str(abs(m.numerator))),
        "min_pivot_denominator_digits": len(str(m.denominator)),
    }


def exact_fraction_certificates(k_np: np.ndarray, d_np: np.ndarray) -> dict[str, object]:
    k = fraction_matrix_from_float(k_np)
    d = fraction_matrix_from_float(d_np)
    n = len(k)
    eps = Fraction(1, 20000)
    records = []
    for h in (Fraction(-1, 10000), Fraction(0), Fraction(1, 10000)):
        kh = mat_add_scaled(k, d, h)
        records.append(
            {
                "t": str(h),
                "K_t_minus_epsI": compact_pivots(ldl_fraction(mat_shift(kh, eps))),
                "I_minus_K_t_minus_epsI": compact_pivots(ldl_fraction(eye_minus_shifted(kh, eps))),
            }
        )
    d_pivots = ldl_fraction(d)
    return {
        "input_interpretation": "symmetrized float64 entries interpreted as exact decimal rationals via repr(float)",
        "uniform_interval": ["-1/10000", "1/10000"],
        "strict_margin_eps": "1/20000",
        "endpoint_certificates": records,
        "D_positive_definite": True,
        "D_rank": n,
        "D_LDL": compact_pivots(d_pivots),
    }


def source_ledger_summary() -> dict[str, object]:
    rows = list(csv.DictReader((SOURCE / "candidate_ledger.csv").open(encoding="utf-8")))
    groups = []
    for n in sorted({int(r["n"]) for r in rows}):
        for mode in sorted({int(r["mode"]) for r in rows if int(r["n"]) == n}):
            sub = [r for r in rows if int(r["n"]) == n and int(r["mode"]) == mode]
            groups.append(
                {
                    "n": n,
                    "mode": mode,
                    "count": len(sub),
                    "max_mechanism_ratio": max(float(r["mechanism_ratio"]) for r in sub),
                    "positive_lambda_max_count": sum(float(r["lambda_max"]) > 0.0 for r in sub),
                }
            )
    return {
        "row_count": len(rows),
        "scope_note": "source 160 rows are used only as a statistical ledger, not fully revalidated here",
        "groups": groups,
    }


def run() -> dict[str, object]:
    started = time.time()
    k, d, sym_meta = symmetrized_frozen()
    p_mixed, _, _ = mixed_atoms_float(k)
    p_mobius = mobius_atoms_float(k)
    p_lens = l_ensemble_atoms_float(k)
    base = directional_float(k, d)
    fisher_scale = 1.0 / math.sqrt(base["Fisher_positive"])
    scale_rows = []
    for scale in (fisher_scale, 0.5, -2.0, 3.0):
        row = directional_float(k, scale * d)
        scale_rows.append(
            {
                "scale": scale,
                "Fisher_positive": row["Fisher_positive"],
                "acceleration": row["acceleration"],
                "H2": row["H2"],
                "rho": row["rho"],
                "rho_difference_from_base": row["rho"] - base["rho"],
                "H2_over_scale_squared_base_H2": row["H2"] / (scale * scale * base["H2"]),
            }
        )
    dec = decimal_directional(k, d, precision=70)
    with localcontext() as ctx:
        ctx.prec = 70
        h = Decimal("0.00001")
        center = Decimal(dec["H"])
        k_dec = decimal_matrix_from_float(k)
        d_dec = decimal_matrix_from_float(d)
        minus = [[x - h * y for x, y in zip(row_k, row_d)] for row_k, row_d in zip(k_dec, d_dec)]
        plus = [[x + h * y for x, y in zip(row_k, row_d)] for row_k, row_d in zip(k_dec, d_dec)]
        hminus = decimal_entropy_matrix(minus)
        hplus = decimal_entropy_matrix(plus)
        chord_h2 = (hminus + hplus - Decimal(2) * center) / (h * h)
        chord_gap = (hminus + hplus) / Decimal(2) - center
    cert = exact_fraction_certificates(k, d)
    commuting = commuting_subspace_float(k)
    report = {
        "status": "PASS_INDEPENDENT_H2_VERIFICATION",
        "npz_sha256": sha256(SOURCE / "best_mechanism_case.npz"),
        "source_ledger": source_ledger_summary(),
        "symmetrization": sym_meta,
        "spectra": {
            "K_min_eigenvalue_float": float(np.linalg.eigvalsh(k)[0]),
            "K_max_eigenvalue_float": float(np.linalg.eigvalsh(k)[-1]),
            "D_min_eigenvalue_float": float(np.linalg.eigvalsh(d)[0]),
            "D_max_eigenvalue_float": float(np.linalg.eigvalsh(d)[-1]),
        },
        "event_semantics_float": {
            "mixed_formula": "p_S=(-1)^(n-|S|) det(K-diag(1_{i notin S}))",
            "mobius_formula": "p_S=sum_{T superset S} (-1)^(|T|-|S|) det(K_T)",
            "event_count": int(len(p_mixed)),
            "sum_mixed_minus_1": float(np.sum(p_mixed) - 1.0),
            "min_mixed_probability": float(np.min(p_mixed)),
            "mobius_negative_atoms": int(np.sum(p_mobius < 0.0)),
            "mobius_max_abs_difference": float(np.max(np.abs(p_mobius - p_mixed))),
            "mobius_max_relative_difference": float(np.max(np.abs(p_mobius - p_mixed) / p_mixed)),
            "L_ensemble_max_relative_difference": float(np.max(np.abs(p_lens - p_mixed) / p_mixed)),
        },
        "directional_float_operator_norm_D": base,
        "rho_scale_invariance": scale_rows,
        "decimal_directional": dec,
        "decimal_chord_check": {
            "h": "0.00001",
            "Hminus": str(+hminus),
            "Hplus": str(+hplus),
            "central_H2": str(+chord_h2),
            "midpoint_gap": str(+chord_gap),
            "analytic_H2": dec["H2"],
        },
        "exact_fraction_certificates": cert,
        "commuting_subspace": commuting,
        "conclusions_checked": {
            "decimal_total_curvature_negative": Decimal(dec["H2"]) < 0,
            "rho_less_than_counterexample_threshold_one": Decimal(dec["rho"]) < 1,
            "fisher_normalized_rho_matches_author_scale": abs(scale_rows[0]["Fisher_positive"] - 1.0) < 1e-10
            and abs(scale_rows[0]["acceleration"] - base["rho"]) < 1e-10,
            "strict_chord_gap_negative_at_h_1e_minus_5": chord_gap < 0,
            "D_is_strict_PSD_by_exact_LDL": cert["D_positive_definite"],
            "commuting_subspace_rho_exceeds_half_but_not_one": commuting["rho_max"] > 0.5
            and commuting["rho_max"] < 1.0,
            "commuting_direction_is_effectively_commuting": commuting["commutator_frobenius"] < 1e-12,
            "source_160_not_upgraded_to_theorem": True,
        },
        "exit_code": 0,
        "elapsed_seconds": time.time() - started,
    }
    checks = report["conclusions_checked"]
    if not all(bool(v) for v in checks.values()):
        report["status"] = "FAIL_INDEPENDENT_H2_VERIFICATION"
    return report


def main() -> None:
    report = run()
    out = HERE / "fresh_h2_audit.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if not report["status"].startswith("PASS"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
