"""Joint local refinement of spectrum and fixed eigenbasis for PSD rates.

Each evaluated center still defines a fixed-Q affine spectral-rate path.  The
outer loop is a float64 scout over centers; any positive signal must be frozen
and independently replayed at high precision.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import time
from pathlib import Path

for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[key] = "1"

import numpy as np

from commuting_spectral_search import (
    entropy,
    positive_maximum,
    restricted_components,
    unrestricted_maximum,
)


def logits(spectrum: np.ndarray) -> np.ndarray:
    return np.log(spectrum) - np.log1p(-spectrum)


def logistic(values: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-values))


def givens_perturb(
    basis: np.ndarray, rng: np.random.Generator, scale: float, rotations: int
) -> np.ndarray:
    out = basis.copy()
    n = out.shape[1]
    for _ in range(rotations):
        a, b = rng.choice(n, size=2, replace=False)
        angle = float(rng.normal(0.0, scale))
        cosine = math.cos(angle)
        sine = math.sin(angle)
        first = out[:, a].copy()
        second = out[:, b].copy()
        out[:, a] = cosine * first + sine * second
        out[:, b] = -sine * first + cosine * second
    return out


def evaluate(
    basis: np.ndarray,
    spectrum: np.ndarray,
    rng: np.random.Generator,
    chunk: int,
    step_fraction: float,
) -> tuple[dict[str, float | bool], np.ndarray, np.ndarray, np.ndarray]:
    kernel = basis @ np.diag(spectrum) @ basis.T
    projectors = np.einsum("ij,kj->jik", basis, basis)
    fisher, acceleration, diagnostics = restricted_components(kernel, projectors, chunk)
    rho_free, free_vector, residual = unrestricted_maximum(fisher, acceleration)
    rho_psd, rates = positive_maximum(fisher, acceleration, rng)
    rates = rates / rates.max()
    direction = basis @ np.diag(rates) @ basis.T
    max_step = float(np.min(np.minimum(spectrum, 1.0 - spectrum) / rates))
    step = min(step_fraction * max_step, 0.01)
    gap = (entropy(kernel - step * direction) + entropy(kernel + step * direction)) / 2.0
    gap -= diagnostics["entropy"]
    return (
        {
            "rho_psd": rho_psd,
            "rho_unrestricted": rho_free,
            "unrestricted_same_sign": bool(np.all(free_vector > 0) or np.all(free_vector < 0)),
            "total_psd_fisher_normalized": rho_psd - 1.0,
            "min_atom": diagnostics["min_atom"],
            "normalization_residual": diagnostics["normalization_residual"],
            "generalized_residual": residual,
            "direction_min_rate": float(rates.min()),
            "direction_max_rate": float(rates.max()),
            "chord_step": step,
            "chord_gap": gap,
            "spectrum_margin": float(np.min(np.minimum(spectrum, 1.0 - spectrum))),
            "basis_orthogonality_residual": float(np.linalg.norm(basis.T @ basis - np.eye(len(basis)))),
        },
        kernel,
        direction,
        rates,
    )


def proposal(
    base_basis: np.ndarray,
    base_spectrum: np.ndarray,
    source_basis: np.ndarray,
    source_spectrum: np.ndarray,
    rng: np.random.Generator,
    index: int,
    margin: float,
) -> tuple[np.ndarray, np.ndarray, str, float, float]:
    mode = index % 4
    phase = (index // 400) % 5
    spectral_scales = (0.35, 0.18, 0.09, 0.045, 0.02)
    basis_scales = (0.12, 0.06, 0.03, 0.015, 0.007)
    spectral_scale = spectral_scales[phase]
    basis_scale = basis_scales[phase]
    if mode == 0:
        basis = base_basis
        center_logits = logits(base_spectrum)
        label = "spectrum_local"
    elif mode == 1:
        basis = givens_perturb(base_basis, rng, basis_scale, 1)
        center_logits = logits(base_spectrum)
        label = "one_basis_rotation"
    elif mode == 2:
        basis = givens_perturb(base_basis, rng, basis_scale, 3)
        center_logits = logits(base_spectrum)
        label = "three_basis_rotations"
    else:
        basis = givens_perturb(source_basis, rng, 2.0 * basis_scale, 4)
        center_logits = logits(source_spectrum)
        spectral_scale *= 1.5
        label = "source_restart"
    spectrum = logistic(center_logits + rng.normal(0.0, spectral_scale, len(center_logits)))
    spectrum = np.clip(spectrum, margin, 1.0 - margin)
    return basis.copy(), spectrum, label, spectral_scale, basis_scale


def run(args: argparse.Namespace) -> None:
    started = time.time()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    source = np.load(args.source)
    source_basis = np.asarray(source["eigenvectors"], dtype=float)
    source_spectrum = np.asarray(source["spectrum"], dtype=float)
    rng = np.random.default_rng(args.seed)
    base_basis = source_basis.copy()
    base_spectrum = source_spectrum.copy()
    base_metrics, base_kernel, base_direction, base_rates = evaluate(
        base_basis, base_spectrum, rng, args.chunk, args.step_fraction
    )
    best_metrics = base_metrics.copy()
    best_basis = base_basis.copy()
    best_spectrum = base_spectrum.copy()
    np.savez_compressed(
        out / "best_case.npz",
        kernel=base_kernel,
        direction=base_direction,
        spectrum=base_spectrum,
        rates=base_rates,
        eigenvectors=base_basis,
    )
    fields = [
        "index", "label", "spectral_scale", "basis_scale", "accepted",
        "rho_psd", "rho_unrestricted", "unrestricted_same_sign",
        "total_psd_fisher_normalized", "min_atom", "normalization_residual",
        "generalized_residual", "direction_min_rate", "direction_max_rate",
        "chord_step", "chord_gap", "spectrum_margin",
        "basis_orthogonality_residual", "status",
    ]
    positive_count = 0
    accepted_count = 0
    with (out / "candidate_ledger.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for index in range(args.centers):
            basis, spectrum, label, spectral_scale, basis_scale = proposal(
                base_basis, base_spectrum, source_basis, source_spectrum,
                rng, index, args.margin
            )
            metrics, kernel, direction, rates = evaluate(
                basis, spectrum, rng, args.chunk, args.step_fraction
            )
            temperature = max(0.0002, 0.004 * (1.0 - index / max(1, args.centers)))
            improvement = float(metrics["rho_psd"]) - float(base_metrics["rho_psd"])
            accepted = improvement >= 0.0 or rng.random() < math.exp(improvement / temperature)
            if accepted:
                accepted_count += 1
                base_basis = basis
                base_spectrum = spectrum
                base_metrics = metrics
            status = (
                "FLOAT_CANDIDATE"
                if float(metrics["rho_psd"]) > 1.0 + args.threshold
                or float(metrics["chord_gap"]) > args.gap_threshold
                else "NO_HIT"
            )
            if status == "FLOAT_CANDIDATE":
                positive_count += 1
            row = {
                "index": index,
                "label": label,
                "spectral_scale": spectral_scale,
                "basis_scale": basis_scale,
                "accepted": accepted,
                **metrics,
                "status": status,
            }
            writer.writerow(row)
            handle.flush()
            if float(metrics["rho_psd"]) > float(best_metrics["rho_psd"]):
                best_metrics = metrics.copy()
                best_basis = basis.copy()
                best_spectrum = spectrum.copy()
                np.savez_compressed(
                    out / "best_case.npz",
                    kernel=kernel,
                    direction=direction,
                    spectrum=spectrum,
                    rates=rates,
                    eigenvectors=basis,
                )
                (out / "best_case.json").write_text(
                    json.dumps(row, indent=2), encoding="utf-8"
                )
            if (index + 1) % 5 == 0:
                print(
                    json.dumps(
                        {
                            "completed": index + 1,
                            "best_rho_psd": best_metrics["rho_psd"],
                            "current_rho_psd": base_metrics["rho_psd"],
                        }
                    ),
                    flush=True,
                )
    manifest = {
        "status": "SCOUT_COMPLETE",
        "seed": args.seed,
        "centers": args.centers,
        "n": len(source_spectrum),
        "margin_floor": args.margin,
        "chunk": args.chunk,
        "threads": 1,
        "source_rho_recomputed": float(base_metrics["rho_psd"]) if args.centers == 0 else float(evaluate(source_basis, source_spectrum, np.random.default_rng(args.seed), args.chunk, args.step_fraction)[0]["rho_psd"]),
        "best_rho_psd": best_metrics["rho_psd"],
        "best_spectrum_margin": float(np.min(np.minimum(best_spectrum, 1.0 - best_spectrum))),
        "best_basis_orthogonality_residual": float(np.linalg.norm(best_basis.T @ best_basis - np.eye(len(best_basis)))),
        "positive_count": positive_count,
        "accepted_count": accepted_count,
        "elapsed_seconds": time.time() - started,
        "exit_code": 0,
        "warning": "float64 joint basis/spectrum scout only; freeze and replay any signal",
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest), flush=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--seed", type=int, default=2026090840)
    parser.add_argument("--centers", type=int, default=80)
    parser.add_argument("--margin", type=float, default=0.01)
    parser.add_argument("--chunk", type=int, default=32)
    parser.add_argument("--step-fraction", type=float, default=0.1)
    parser.add_argument("--threshold", type=float, default=1e-8)
    parser.add_argument("--gap-threshold", type=float, default=1e-10)
    return parser.parse_args()


if __name__ == "__main__":
    run(parse_args())
