"""Targeted PSD search with fixed eigenvectors and heterogeneous spectral rates.

This is a float64 scout.  A positive rho or midpoint gap must be frozen and
replayed independently at high precision before it is evidence.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import time
from pathlib import Path

for _key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_key] = "1"

import numpy as np


def event_data(kernel: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    n = len(kernel)
    masks = np.arange(1 << n, dtype=np.int64)
    absent = 1 - ((masks[:, None] >> np.arange(n)) & 1)
    mixed = np.broadcast_to(kernel, (len(masks), n, n)).copy()
    mixed[:, np.arange(n), np.arange(n)] -= absent
    sign, logabs = np.linalg.slogdet(mixed)
    expected = (-1.0) ** absent.sum(axis=1)
    if not np.all(sign * expected > 0):
        raise ArithmeticError("nonpositive exact event atom")
    probabilities = np.exp(logabs)
    if abs(float(probabilities.sum()) - 1.0) > 5e-10:
        raise ArithmeticError("event probabilities do not normalize")
    return probabilities, logabs, mixed


def restricted_components(
    kernel: np.ndarray, projectors: np.ndarray, chunk: int
) -> tuple[np.ndarray, np.ndarray, dict[str, float]]:
    probabilities, logabs, mixed = event_data(kernel)
    dimension = len(projectors)
    fisher = np.zeros((dimension, dimension))
    acceleration = np.zeros((dimension, dimension))
    first_residual = 0.0
    second_residual = 0.0
    for start in range(0, len(probabilities), chunk):
        stop = min(start + chunk, len(probabilities))
        inverse = np.linalg.inv(mixed[start:stop])
        score = np.einsum("qij,aij->qa", inverse, projectors, optimize=True)
        products = np.einsum("qij,ajk->qaik", inverse, projectors, optimize=True)
        hlog = -np.einsum("qaij,qbji->qab", products, products, optimize=True)
        weights = probabilities[start:stop]
        logs = logabs[start:stop]
        fisher += np.einsum("q,qa,qb->ab", weights, score, score, optimize=True)
        acceleration -= np.einsum(
            "q,qab->ab", weights * logs, score[:, :, None] * score[:, None, :] + hlog, optimize=True
        )
        first_residual += float(np.sum(weights[:, None] * score))
        second_residual += float(np.sum(weights[:, None, None] * (score[:, :, None] * score[:, None, :] + hlog)))
    fisher = (fisher + fisher.T) / 2.0
    acceleration = (acceleration + acceleration.T) / 2.0
    return fisher, acceleration, {
        "entropy": -float(probabilities @ logabs),
        "min_atom": float(probabilities.min()),
        "normalization_residual": float(probabilities.sum() - 1.0),
        "aggregate_first_residual": first_residual,
        "aggregate_second_residual": second_residual,
    }


def quotient(vector: np.ndarray, fisher: np.ndarray, acceleration: np.ndarray) -> float:
    denominator = float(vector @ fisher @ vector)
    if denominator <= 0:
        return float("-inf")
    return float(vector @ acceleration @ vector) / denominator


def unrestricted_maximum(
    fisher: np.ndarray, acceleration: np.ndarray
) -> tuple[float, np.ndarray, float]:
    values, vectors = np.linalg.eigh(fisher)
    if values[0] <= 0:
        raise ArithmeticError("singular Fisher matrix")
    whitening = vectors / np.sqrt(values)[None, :]
    rho, directions = np.linalg.eigh(whitening.T @ acceleration @ whitening)
    vector = whitening @ directions[:, -1]
    vector /= np.sqrt(float(vector @ fisher @ vector))
    residual = np.linalg.norm(acceleration @ vector - rho[-1] * fisher @ vector)
    residual /= np.linalg.norm(acceleration @ vector) + np.linalg.norm(fisher @ vector)
    return float(rho[-1]), vector, float(residual)


def positive_maximum(
    fisher: np.ndarray, acceleration: np.ndarray, rng: np.random.Generator
) -> tuple[float, np.ndarray]:
    n = len(fisher)
    top_rho, top_vector, _ = unrestricted_maximum(fisher, acceleration)
    candidates: list[np.ndarray] = [np.ones(n)]
    if np.all(top_vector > 0):
        candidates.append(top_vector)
    if np.all(top_vector < 0):
        candidates.append(-top_vector)
    candidates.extend(np.eye(n))
    candidates.extend(np.exp(rng.normal(0.0, 1.2, size=(8, n))))

    best_rho = float("-inf")
    best_vector = np.ones(n)
    for initial in candidates:
        y = np.log(np.maximum(initial, 1e-12))
        y -= y.mean()
        first_moment = np.zeros(n)
        second_moment = np.zeros(n)
        for iteration in range(160):
            vector = np.exp(np.clip(y, -14.0, 14.0))
            denominator = float(vector @ fisher @ vector)
            rho = float(vector @ acceleration @ vector) / denominator
            gradient_v = 2.0 * (acceleration @ vector - rho * (fisher @ vector)) / denominator
            gradient_y = vector * gradient_v
            gradient_y -= gradient_y.mean()
            first_moment = 0.9 * first_moment + 0.1 * gradient_y
            second_moment = 0.999 * second_moment + 0.001 * gradient_y * gradient_y
            corrected_first = first_moment / (1.0 - 0.9 ** (iteration + 1))
            corrected_second = second_moment / (1.0 - 0.999 ** (iteration + 1))
            y += 0.035 * corrected_first / (np.sqrt(corrected_second) + 1e-10)
            y -= y.mean()
        vector = np.exp(np.clip(y, -14.0, 14.0))
        rho = quotient(vector, fisher, acceleration)
        if rho > best_rho:
            best_rho = rho
            best_vector = vector
    best_vector /= np.sqrt(float(best_vector @ fisher @ best_vector))
    if top_rho > best_rho and (np.all(top_vector > 0) or np.all(top_vector < 0)):
        return top_rho, top_vector if np.all(top_vector > 0) else -top_vector
    return best_rho, best_vector


def entropy(kernel: np.ndarray) -> float:
    probabilities, logabs, _ = event_data(kernel)
    return -float(probabilities @ logabs)


def center_spectrum(
    original: np.ndarray, rng: np.random.Generator, index: int, margin: float
) -> tuple[np.ndarray, str]:
    n = len(original)
    mode = index % 4
    if mode == 0:
        epsilon = (index // 4 % 9) / 1000.0
        spectrum = (1.0 - 2.0 * epsilon) * original + epsilon
        spectrum += rng.normal(0.0, 0.025, n)
        label = "frozen_logit_neighborhood"
    elif mode == 1:
        low = rng.uniform(margin, 0.18, n // 2)
        high = rng.uniform(0.82, 1.0 - margin, n - n // 2)
        spectrum = np.concatenate([low, high])
        rng.shuffle(spectrum)
        label = "two_edge_clusters"
    elif mode == 2:
        logits = rng.uniform(-4.4, 4.4, n)
        spectrum = 1.0 / (1.0 + np.exp(-logits))
        label = "logit_spread"
    else:
        anchors = np.array([0.03, 0.12, 0.5, 0.88, 0.97])
        spectrum = rng.choice(anchors, size=n) + rng.normal(0.0, 0.012, n)
        label = "five_spectral_clusters"
    spectrum = np.clip(spectrum, margin, 1.0 - margin)
    return spectrum, label


def run(args: argparse.Namespace) -> None:
    start = time.time()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    source = np.load(args.source)
    frozen_kernel = (source["kernel"] + source["kernel"].T) / 2.0
    original_spectrum, eigenvectors = np.linalg.eigh(frozen_kernel)
    projectors = np.einsum("ij,kj->jik", eigenvectors, eigenvectors)
    rng = np.random.default_rng(args.seed)
    fields = [
        "index", "mode", "margin", "label", "rho_psd", "rho_unrestricted",
        "unrestricted_same_sign", "total_psd_fisher_normalized", "min_atom",
        "normalization_residual", "generalized_residual", "direction_min_rate",
        "direction_max_rate", "chord_step", "chord_gap", "status",
    ]
    best: dict[str, float | int | str | bool] | None = None
    positive_count = 0
    with (out / "candidate_ledger.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for index in range(args.centers):
            spectrum, label = center_spectrum(original_spectrum, rng, index, args.margin)
            kernel = eigenvectors @ np.diag(spectrum) @ eigenvectors.T
            fisher, acceleration, diagnostics = restricted_components(kernel, projectors, args.chunk)
            rho_free, free_vector, residual = unrestricted_maximum(fisher, acceleration)
            same_sign = bool(np.all(free_vector > 0) or np.all(free_vector < 0))
            rho_psd, rates = positive_maximum(fisher, acceleration, rng)
            rates /= rates.max()
            direction = eigenvectors @ np.diag(rates) @ eigenvectors.T
            max_step = float(np.min(np.minimum(spectrum, 1.0 - spectrum) / rates))
            step = min(args.step_fraction * max_step, 0.02)
            center_entropy = diagnostics["entropy"]
            gap = (entropy(kernel - step * direction) + entropy(kernel + step * direction)) / 2.0 - center_entropy
            row = {
                "index": index,
                "mode": index % 4,
                "margin": float(np.min(np.minimum(spectrum, 1.0 - spectrum))),
                "label": label,
                "rho_psd": rho_psd,
                "rho_unrestricted": rho_free,
                "unrestricted_same_sign": same_sign,
                "total_psd_fisher_normalized": rho_psd - 1.0,
                "min_atom": diagnostics["min_atom"],
                "normalization_residual": diagnostics["normalization_residual"],
                "generalized_residual": residual,
                "direction_min_rate": float(rates.min()),
                "direction_max_rate": float(rates.max()),
                "chord_step": step,
                "chord_gap": gap,
                "status": "FLOAT_CANDIDATE" if rho_psd > 1.0 + args.threshold or gap > args.gap_threshold else "NO_HIT",
            }
            if row["status"] == "FLOAT_CANDIDATE":
                positive_count += 1
            writer.writerow(row)
            handle.flush()
            if best is None or rho_psd > float(best["rho_psd"]):
                best = row.copy()
                np.savez_compressed(out / "best_case.npz", kernel=kernel, direction=direction, spectrum=spectrum, rates=rates, eigenvectors=eigenvectors)
                (out / "best_case.json").write_text(json.dumps(best, indent=2), encoding="utf-8")
            if (index + 1) % 5 == 0:
                print(json.dumps({"completed": index + 1, "best_rho_psd": best["rho_psd"]}), flush=True)
    manifest = {
        "status": "SCOUT_COMPLETE",
        "seed": args.seed,
        "centers": args.centers,
        "n": len(frozen_kernel),
        "margin_floor": args.margin,
        "chunk": args.chunk,
        "threads": 1,
        "best_rho_psd": best["rho_psd"] if best else None,
        "best_gap": best["chord_gap"] if best else None,
        "positive_count": positive_count,
        "elapsed_seconds": time.time() - start,
        "exit_code": 0,
        "warning": "float64 targeted scout only; finite non-hit is not a theorem",
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest), flush=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--seed", type=int, default=2026090816)
    parser.add_argument("--centers", type=int, default=80)
    parser.add_argument("--margin", type=float, default=0.01)
    parser.add_argument("--chunk", type=int, default=32)
    parser.add_argument("--step-fraction", type=float, default=0.1)
    parser.add_argument("--threshold", type=float, default=1e-8)
    parser.add_argument("--gap-threshold", type=float, default=1e-10)
    return parser.parse_args()


if __name__ == "__main__":
    run(parse_args())
