#!/usr/bin/env python3
"""D10-S3 targeted PSD/NSD mechanism scout.

This script is intentionally self-contained: it does not import the author's
dense Hessian code.  It reads only frozen evidence from the neighbouring
dense_hessian directory and writes a JSON report in this directory.
"""

from __future__ import annotations

import json
import math
import os
import time
from pathlib import Path

for _var in (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
):
    os.environ.setdefault(_var, "1")

import numpy as np


SEED = 2026090833
DEEPENING_ROOT = Path(__file__).resolve().parents[2]
FROZEN_NPZ = (
    DEEPENING_ROOT
    / "dense_hessian"
    / "server_round6_analysis"
    / "independent_frozen.npz"
)
OUT = Path(__file__).resolve().parent / "scout_results.json"


def sym(A: np.ndarray) -> np.ndarray:
    return (A + A.T) / 2.0


def strict_margins(K: np.ndarray) -> dict:
    eig = np.linalg.eigvalsh(sym(K))
    ceig = np.linalg.eigvalsh(sym(np.eye(K.shape[0]) - K))
    return {
        "lambda_min_K": float(eig[0]),
        "lambda_max_K": float(eig[-1]),
        "lambda_min_I_minus_K": float(ceig[0]),
        "margin": float(min(eig[0], ceig[0])),
    }


def symmetric_basis(n: int) -> tuple[np.ndarray, list[tuple[int, int]]]:
    mats: list[np.ndarray] = []
    labels: list[tuple[int, int]] = []
    rt2 = math.sqrt(2.0)
    for i in range(n):
        E = np.zeros((n, n))
        E[i, i] = 1.0
        mats.append(E)
        labels.append((i, i))
    for i in range(n):
        for j in range(i + 1, n):
            E = np.zeros((n, n))
            E[i, j] = E[j, i] = 1.0 / rt2
            mats.append(E)
            labels.append((i, j))
    return np.stack(mats, axis=0), labels


def coords_from_matrix(A: np.ndarray) -> np.ndarray:
    n = A.shape[0]
    x: list[float] = []
    rt2 = math.sqrt(2.0)
    for i in range(n):
        x.append(float(A[i, i]))
    for i in range(n):
        for j in range(i + 1, n):
            x.append(float(rt2 * A[i, j]))
    return np.asarray(x, dtype=float)


def matrix_from_coords(x: np.ndarray, n: int) -> np.ndarray:
    A = np.zeros((n, n), dtype=float)
    rt2 = math.sqrt(2.0)
    k = 0
    for i in range(n):
        A[i, i] = x[k]
        k += 1
    for i in range(n):
        for j in range(i + 1, n):
            A[i, j] = A[j, i] = x[k] / rt2
            k += 1
    return A


def event_matrix(K: np.ndarray, mask: int) -> np.ndarray:
    n = K.shape[0]
    A = np.array(K, copy=True)
    for i in range(n):
        if not (mask >> i) & 1:
            A[i, i] -= 1.0
    return A


def signed_distribution(K: np.ndarray) -> np.ndarray:
    n = K.shape[0]
    probs = np.empty(1 << n, dtype=float)
    for mask in range(1 << n):
        A = event_matrix(K, mask)
        sgn = -1.0 if ((n - mask.bit_count()) & 1) else 1.0
        probs[mask] = sgn * np.linalg.det(A)
    return probs


def mobius_distribution(K: np.ndarray) -> np.ndarray:
    n = K.shape[0]
    vals = np.empty(1 << n, dtype=float)
    for mask in range(1 << n):
        idx = [i for i in range(n) if (mask >> i) & 1]
        if idx:
            vals[mask] = np.linalg.det(K[np.ix_(idx, idx)])
        else:
            vals[mask] = 1.0
    # Superset Möbius: exact atom p[S] = sum_{A superset S} (-1)^{|A|-|S|} det K_A.
    for i in range(n):
        bit = 1 << i
        for mask in range(1 << n):
            if (mask & bit) == 0:
                vals[mask] -= vals[mask | bit]
    return vals


def entropy_from_signed(K: np.ndarray) -> tuple[float, dict]:
    p = signed_distribution(K)
    if float(np.min(p)) <= 0.0:
        raise ValueError(f"nonpositive atom in entropy computation: min={float(np.min(p))}")
    H = float(-np.dot(p, np.log(p)))
    return H, {
        "event_count": int(p.size),
        "sum_minus_one": float(np.sum(p) - 1.0),
        "min_probability": float(np.min(p)),
        "max_probability": float(np.max(p)),
    }


def directional_stats_loop(K: np.ndarray, D: np.ndarray) -> dict:
    n = K.shape[0]
    H = 0.0
    fisher = 0.0
    accel = 0.0
    sum_p = 0.0
    sum_p1 = 0.0
    sum_p2 = 0.0
    min_p = float("inf")
    max_p = 0.0
    for mask in range(1 << n):
        A = event_matrix(K, mask)
        sgn = -1.0 if ((n - mask.bit_count()) & 1) else 1.0
        p = float(sgn * np.linalg.det(A))
        X = np.linalg.solve(A, D)
        v = float(np.trace(X))
        w = float(v * v - np.trace(X @ X))
        H -= p * math.log(p)
        fisher += p * v * v
        accel += -p * w * math.log(p)
        sum_p += p
        sum_p1 += p * v
        sum_p2 += p * w
        min_p = min(min_p, p)
        max_p = max(max_p, p)
    return {
        "H": H,
        "Fisher_positive": fisher,
        "acceleration": accel,
        "H2": accel - fisher,
        "rho": accel / fisher if fisher > 0 else None,
        "sum_p_minus_one": sum_p - 1.0,
        "sum_p1": sum_p1,
        "sum_p2": sum_p2,
        "min_probability": min_p,
        "max_probability": max_p,
        "event_count": 1 << n,
    }


def build_quadratic_matrices(K: np.ndarray) -> tuple[np.ndarray, np.ndarray, dict]:
    n = K.shape[0]
    basis, _labels = symmetric_basis(n)
    d = basis.shape[0]
    fisher = np.zeros((d, d), dtype=float)
    accel = np.zeros((d, d), dtype=float)
    sum_p = 0.0
    min_p = float("inf")
    max_p = 0.0
    min_signed_det = float("inf")
    negative_atoms = 0
    for mask in range(1 << n):
        A = event_matrix(K, mask)
        sgn = -1.0 if ((n - mask.bit_count()) & 1) else 1.0
        p = float(sgn * np.linalg.det(A))
        if p <= 0.0:
            negative_atoms += 1
        B = np.linalg.inv(A)
        scores = coords_from_matrix(B)
        BE = np.einsum("ij,kjl->kil", B, basis, optimize=True)
        trprod = np.einsum("kij,lji->kl", BE, BE, optimize=True)
        wmat = np.outer(scores, scores) - trprod
        fisher += p * np.outer(scores, scores)
        accel += -p * math.log(p) * wmat
        sum_p += p
        min_p = min(min_p, p)
        max_p = max(max_p, p)
        min_signed_det = min(min_signed_det, p)
    fisher = sym(fisher)
    accel = sym(accel)
    return fisher, accel, {
        "basis_dimension": d,
        "event_count": 1 << n,
        "sum_p_minus_one": float(sum_p - 1.0),
        "min_probability": float(min_p),
        "max_probability": float(max_p),
        "nonpositive_atoms": int(negative_atoms),
        "min_signed_atom": float(min_signed_det),
    }


def quadratic_stats(F: np.ndarray, A: np.ndarray, x: np.ndarray) -> dict:
    fisher = float(x @ F @ x)
    accel = float(x @ A @ x)
    return {
        "Fisher_positive": fisher,
        "acceleration": accel,
        "H2": accel - fisher,
        "rho": accel / fisher if fisher > 0 else None,
    }


def generalized_max(F: np.ndarray, A: np.ndarray) -> tuple[float, np.ndarray, dict]:
    F = sym(F)
    A = sym(A)
    evals, U = np.linalg.eigh(F)
    keep = evals > max(1e-12, 1e-12 * float(np.max(evals)))
    W = U[:, keep] / np.sqrt(evals[keep])
    C = sym(W.T @ A @ W)
    vals, vecs = np.linalg.eigh(C)
    j = int(np.argmax(vals))
    x = W @ vecs[:, j]
    x = x / math.sqrt(float(x @ F @ x))
    resid = float(np.linalg.norm(A @ x - vals[j] * F @ x) / max(1.0, np.linalg.norm(A @ x)))
    return float(vals[j]), x, {
        "fisher_rank": int(np.count_nonzero(keep)),
        "fisher_min_kept_eig": float(np.min(evals[keep])),
        "fisher_max_eig": float(np.max(evals)),
        "generalized_residual": resid,
    }


def subspace_max(F: np.ndarray, A: np.ndarray, V: np.ndarray) -> tuple[float, np.ndarray, dict]:
    Fs = sym(V.T @ F @ V)
    As = sym(V.T @ A @ V)
    rho, y, meta = generalized_max(Fs, As)
    x = V @ y
    return rho, x, meta


def psd_meta(D: np.ndarray, tol: float = 1e-9) -> dict:
    eig = np.linalg.eigvalsh(sym(D))
    return {
        "lambda_min": float(eig[0]),
        "lambda_max": float(eig[-1]),
        "rank_tol_1e-9": int(np.count_nonzero(eig > tol)),
        "is_psd_tol_1e-9": bool(eig[0] >= -tol),
        "is_nsd_tol_1e-9": bool(eig[-1] <= tol),
        "condition_if_pd": float(eig[-1] / eig[0]) if eig[0] > tol else None,
    }


def safe_chord(K: np.ndarray, D: np.ndarray) -> dict:
    D = sym(D)
    op = float(max(abs(np.linalg.eigvalsh(D))))
    margin = strict_margins(K)["margin"]
    h = min(1e-4, 0.2 * margin / max(op, 1e-300))
    H0, info0 = entropy_from_signed(K)
    Hp, infop = entropy_from_signed(K + h * D)
    Hm, infom = entropy_from_signed(K - h * D)
    gap = (Hp + Hm) / 2.0 - H0
    return {
        "step": float(h),
        "operator_norm_D": op,
        "center_margin": margin,
        "plus_margin": strict_margins(K + h * D)["margin"],
        "minus_margin": strict_margins(K - h * D)["margin"],
        "H0": H0,
        "H_plus": Hp,
        "H_minus": Hm,
        "midpoint_gap": float(gap),
        "central_second_difference": float(2.0 * gap / (h * h)),
        "center_distribution": info0,
        "plus_distribution": infop,
        "minus_distribution": infom,
    }


def random_orthogonal(rng: np.random.Generator, n: int) -> np.ndarray:
    Q, R = np.linalg.qr(rng.normal(size=(n, n)))
    signs = np.sign(np.diag(R))
    signs[signs == 0] = 1.0
    return Q * signs


def random_strict_kernel(rng: np.random.Generator, n: int, margin: float = 0.03) -> np.ndarray:
    Q = random_orthogonal(rng, n)
    lam = rng.uniform(margin, 1.0 - margin, size=n)
    return sym(Q @ np.diag(lam) @ Q.T)


def random_psd_direction(rng: np.random.Generator, n: int, rank: int | None = None) -> np.ndarray:
    if rank is None:
        rank = int(rng.integers(1, n + 1))
    B = rng.normal(size=(n, rank))
    return sym(B @ B.T)


def evaluate_direction(F: np.ndarray, A: np.ndarray, D: np.ndarray) -> dict:
    x = coords_from_matrix(sym(D))
    out = quadratic_stats(F, A, x)
    out.update(psd_meta(D))
    return out


def fixed_center_search(K: np.ndarray, D_frozen: np.ndarray, rng: np.random.Generator) -> dict:
    n = K.shape[0]
    F, A, event_meta = build_quadratic_matrices(K)
    signed = signed_distribution(K)
    mobius = mobius_distribution(K)
    mobius_abs = float(np.max(np.abs(signed - mobius)))
    mobius_rel = float(
        np.max(np.abs(signed - mobius) / np.maximum(np.abs(signed), 1e-300))
    )

    rho_full, x_full, full_meta = generalized_max(F, A)
    D_full = matrix_from_coords(x_full, n)
    if np.linalg.eigvalsh(sym(D_full))[0] < 0:
        D_full = -D_full
    full_stats_loop = directional_stats_loop(K, D_full)

    eigK, QK = np.linalg.eigh(sym(K))
    commuting_cols = []
    for i in range(n):
        P = np.outer(QK[:, i], QK[:, i])
        commuting_cols.append(coords_from_matrix(P))
    V_comm = np.column_stack(commuting_cols)
    rho_comm, x_comm, comm_meta = subspace_max(F, A, V_comm)
    D_comm = matrix_from_coords(x_comm, n)
    # Both signs represent the same generalized quotient; choose the PSD sign if possible.
    if np.linalg.eigvalsh(sym(D_comm))[0] < -1e-9:
        D_comm = -D_comm
        x_comm = -x_comm
    comm_rates = np.diag(QK.T @ D_comm @ QK)

    diag_cols = []
    for i in range(n):
        E = np.zeros((n, n))
        E[i, i] = 1.0
        diag_cols.append(coords_from_matrix(E))
    V_diag = np.column_stack(diag_cols)
    rho_diag, x_diag, diag_meta = subspace_max(F, A, V_diag)
    D_diag = matrix_from_coords(x_diag, n)
    if np.min(np.diag(D_diag)) < 0:
        D_diag = -D_diag
        x_diag = -x_diag

    I = np.eye(n)

    best = {
        "name": "frozen_dense_direction",
        "D": sym(D_frozen),
        "stats": evaluate_direction(F, A, D_frozen),
    }

    def consider(name: str, D: np.ndarray, batch: str) -> None:
        nonlocal best
        stats = evaluate_direction(F, A, D)
        if stats["Fisher_positive"] <= 1e-14:
            return
        record_rho = stats["rho"] if stats["rho"] is not None else -float("inf")
        best_rho = best["stats"]["rho"] if best["stats"]["rho"] is not None else -float("inf")
        if record_rho > best_rho:
            best = {"name": name, "batch": batch, "D": sym(D), "stats": stats}

    batches: list[dict] = []

    deterministic = [
        ("full_generalized_direction", D_full),
        ("commuting_generalized_direction", D_comm),
        ("physical_diagonal_generalized_direction", D_diag),
        ("identity", I),
    ]
    for a in (0.0, 0.05, 0.1, 0.2, 0.5, 0.8, 1.0):
        deterministic.append((f"mix_frozen_identity_{a:.2f}", (1.0 - a) * sym(D_frozen) + a * I))
    for name, D in deterministic:
        consider(name, D, "deterministic_controls")
    batches.append({"name": "deterministic_controls", "draws": len(deterministic)})

    for batch_name, draws, maker in [
        (
            "commuting_loguniform_positive_rates",
            6000,
            lambda: QK @ np.diag(np.exp(rng.uniform(-5.0, 0.0, size=n))) @ QK.T,
        ),
        (
            "random_rank_psd",
            9000,
            lambda: random_psd_direction(rng, n),
        ),
        (
            "random_spd_log_spectrum",
            5000,
            lambda: (
                (lambda Q, e: Q @ np.diag(e) @ Q.T)(
                    random_orthogonal(rng, n), np.exp(rng.uniform(-7.0, 0.0, size=n))
                )
            ),
        ),
    ]:
        start_best = best["stats"]["rho"]
        for j in range(draws):
            consider(f"{batch_name}_{j}", maker(), batch_name)
        batches.append(
            {
                "name": batch_name,
                "draws": draws,
                "best_rho_after_batch": best["stats"]["rho"],
                "improved_global_best": bool(best["stats"]["rho"] > start_best + 1e-12),
            }
        )

    # Local PSD-factor perturbation around the frozen positive definite direction.
    eigD, QD = np.linalg.eigh(sym(D_frozen))
    floor = max(1e-12, -float(eigD[0]) + 1e-12)
    B0 = QD @ np.diag(np.sqrt(np.maximum(eigD + floor, 1e-12)))
    current = B0 / max(np.linalg.norm(B0), 1e-300)
    current_stats = evaluate_direction(F, A, current @ current.T)
    accepted = 0
    proposals = 2500
    scale = 0.18
    for j in range(proposals):
        proposal = current + scale * rng.normal(size=current.shape)
        proposal /= max(np.linalg.norm(proposal), 1e-300)
        Dp = proposal @ proposal.T
        st = evaluate_direction(F, A, Dp)
        if st["rho"] > current_stats["rho"] or rng.random() < math.exp(
            min(0.0, (st["rho"] - current_stats["rho"]) / max(scale, 1e-6))
        ):
            current = proposal
            current_stats = st
            accepted += 1
        consider(f"local_factor_walk_{j}", current @ current.T, "local_factor_walk")
        scale *= 0.999
    batches.append(
        {
            "name": "local_factor_walk",
            "draws": proposals,
            "accepted": accepted,
            "best_rho_after_batch": best["stats"]["rho"],
        }
    )

    topD = best.pop("D")
    top_stats_loop = directional_stats_loop(K, topD)
    chord = safe_chord(K, topD)

    return {
        "fixed_center_source": str(FROZEN_NPZ.as_posix()),
        "n": n,
        "strict_margins": strict_margins(K),
        "event_meta": event_meta,
        "mobius_vs_signed_det": {
            "max_abs_diff": mobius_abs,
            "max_relative_diff": mobius_rel,
            "signed_sum_minus_one": float(np.sum(signed) - 1.0),
            "mobius_sum_minus_one": float(np.sum(mobius) - 1.0),
        },
        "frozen_direction": {
            "psd": psd_meta(D_frozen),
            "quadratic_stats": evaluate_direction(F, A, D_frozen),
            "loop_stats": directional_stats_loop(K, D_frozen),
        },
        "full_symmetric_generalized_control": {
            "rho_max": rho_full,
            "meta": full_meta,
            "direction_psd": psd_meta(D_full),
            "loop_stats": full_stats_loop,
        },
        "commuting_with_K_subspace": {
            "rho_max": rho_comm,
            "meta": comm_meta,
            "direction_psd": psd_meta(D_comm),
            "rates_min": float(np.min(comm_rates)),
            "rates_max": float(np.max(comm_rates)),
            "rates_are_nonnegative_after_sign_choice": bool(np.min(comm_rates) >= -1e-9),
            "loop_stats": directional_stats_loop(K, D_comm),
        },
        "physical_diagonal_subspace": {
            "rho_max": rho_diag,
            "meta": diag_meta,
            "direction_psd": psd_meta(D_diag),
            "diagonal_min": float(np.min(np.diag(D_diag))),
            "diagonal_max": float(np.max(np.diag(D_diag))),
            "diagonal_entries_nonnegative_after_sign_choice": bool(
                np.min(np.diag(D_diag)) >= -1e-9
            ),
            "loop_stats": directional_stats_loop(K, D_diag),
        },
        "identity_direction": {
            "quadratic_stats": evaluate_direction(F, A, I),
            "loop_stats": directional_stats_loop(K, I),
        },
        "psd_search_batches": batches,
        "best_psd_scout": {
            **best,
            "psd": psd_meta(topD),
            "loop_stats": top_stats_loop,
            "strict_chord_gate": chord,
        },
        "positive_gate": {
            "rho_gt_1_candidates": 0 if best["stats"]["rho"] <= 1.0 + 1e-10 else 1,
            "H2_gt_0_candidates": 0 if best["stats"]["H2"] <= 1e-10 else 1,
            "threshold": "rho>1 and H2>0 after strict feasible chord/high-precision gate",
        },
    }


def small_n_psd_scout(rng: np.random.Generator) -> list[dict]:
    specs = [
        (2, 500, 20),
        (3, 260, 12),
        (4, 120, 8),
        (5, 60, 6),
    ]
    out: list[dict] = []
    for n, centers, dirs_per_center in specs:
        best: dict | None = None
        positives = 0
        built = 0
        for ci in range(centers):
            K = random_strict_kernel(rng, n, margin=0.04)
            F, A, meta = build_quadratic_matrices(K)
            built += 1
            for dj in range(dirs_per_center):
                D = random_psd_direction(rng, n)
                stats = evaluate_direction(F, A, D)
                if stats["H2"] > 1e-10 and stats["rho"] is not None and stats["rho"] > 1.0:
                    positives += 1
                if best is None or (
                    stats["rho"] is not None
                    and stats["rho"] > (best["stats"]["rho"] if best["stats"]["rho"] is not None else -1e300)
                ):
                    best = {
                        "center_index": ci,
                        "direction_index": dj,
                        "stats": stats,
                        "kernel_margin": strict_margins(K)["margin"],
                        "event_meta": meta,
                    }
        assert best is not None
        out.append(
            {
                "n": n,
                "centers": centers,
                "directions_per_center": dirs_per_center,
                "directions": centers * dirs_per_center,
                "event_distributions_built": built,
                "event_denominator": built * (1 << n),
                "rho_gt_1_and_H2_gt_0": positives,
                "best": best,
            }
        )
    return out


def main() -> int:
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    z = np.load(FROZEN_NPZ)
    K = sym(np.asarray(z["kernel"], dtype=float))
    D_frozen = sym(np.asarray(z["direction"], dtype=float))

    result = {
        "status": "SCOUT_NO_PSD_FLIP_FOUND_PLUS_DIAGONAL_SUBCLASS_EXCLUSION",
        "date": "2026-09-08",
        "seed": SEED,
        "thread_limits_requested": {
            "OMP_NUM_THREADS": os.environ.get("OMP_NUM_THREADS"),
            "OPENBLAS_NUM_THREADS": os.environ.get("OPENBLAS_NUM_THREADS"),
            "MKL_NUM_THREADS": os.environ.get("MKL_NUM_THREADS"),
            "NUMEXPR_NUM_THREADS": os.environ.get("NUMEXPR_NUM_THREADS"),
        },
        "numpy_version": np.__version__,
        "fixed_center": fixed_center_search(K, D_frozen, rng),
        "small_n_random_psd_scout": small_n_psd_scout(rng),
        "analytic_subclass_exclusion": {
            "name": "standard-coordinate diagonal product kernels with diagonal PSD/NSD directions",
            "claim": (
                "If K(t)=diag(k_i+t d_i) is strictly between 0 and I on an interval, "
                "then H(K(t))=sum_i h(k_i+t d_i) and H''=-sum_i d_i^2/[x_i(1-x_i)]<=0; "
                "strict unless all d_i=0."
            ),
            "scope_warning": (
                "This is a narrow coordinate-product subclass. It does not cover arbitrary commuting "
                "K,D after rotating the observation basis, because DPP configuration entropy is basis-sensitive."
            ),
        },
    }
    result["elapsed_seconds"] = time.time() - t0
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(
        {
            "status": result["status"],
            "output": str(OUT),
            "fixed_center_best_rho": result["fixed_center"]["best_psd_scout"]["stats"]["rho"],
            "full_control_rho": result["fixed_center"]["full_symmetric_generalized_control"]["rho_max"],
            "positive_gate": result["fixed_center"]["positive_gate"],
            "elapsed_seconds": result["elapsed_seconds"],
        },
        indent=2,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
