"""Bounded full-Hessian scout for finite real DPP Shannon entropy.

All numerical results are exploratory float64 values.  A positive signal must
be frozen and replayed with rigorous arithmetic before it becomes evidence.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import platform
import time
from pathlib import Path

for _name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_name, "1")

import numpy as np


def symmetric_basis(n: int) -> tuple[np.ndarray, list[tuple[int, int]]]:
    pairs = [(i, j) for i in range(n) for j in range(i, n)]
    basis = np.zeros((len(pairs), n, n), dtype=float)
    for k, (i, j) in enumerate(pairs):
        basis[k, i, j] = 1.0
        basis[k, j, i] = 1.0
    return basis, pairs


def event_matrices(kernel: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    n = kernel.shape[0]
    masks = np.arange(1 << n, dtype=np.uint64)
    bits = ((masks[:, None] >> np.arange(n, dtype=np.uint64)) & 1).astype(float)
    matrices = np.broadcast_to(kernel, (1 << n, n, n)).copy()
    diagonal = np.arange(n)
    matrices[:, diagonal, diagonal] -= 1.0 - bits
    complement_size = n - bits.sum(axis=1).astype(int)
    expected_sign = np.where(complement_size % 2 == 0, 1.0, -1.0)
    return matrices, expected_sign


def atoms_and_logs(kernel: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    matrices, expected_sign = event_matrices(kernel)
    signs, logs = np.linalg.slogdet(matrices)
    if np.any(signs != expected_sign):
        raise ArithmeticError("event determinant sign mismatch")
    probabilities = np.exp(logs)
    residual = abs(float(probabilities.sum()) - 1.0)
    if residual > 2e-9:
        raise ArithmeticError(f"normalization residual {residual}")
    return probabilities, logs, matrices


def entropy(kernel: np.ndarray) -> tuple[float, float, float]:
    probabilities, logs, _ = atoms_and_logs(kernel)
    return float(-probabilities @ logs), float(probabilities.min()), abs(float(probabilities.sum()) - 1.0)


def entropy_hessian_components(
    kernel: np.ndarray, chunk: int = 256
) -> tuple[np.ndarray, np.ndarray, np.ndarray, dict[str, float]]:
    probabilities, logs, matrices = atoms_and_logs(kernel)
    n = kernel.shape[0]
    basis, _ = symmetric_basis(n)
    m = len(basis)
    fisher = np.zeros((m, m), dtype=float)
    acceleration = np.zeros((m, m), dtype=float)

    for start in range(0, len(probabilities), chunk):
        stop = min(start + chunk, len(probabilities))
        inverse = np.linalg.inv(matrices[start:stop])
        score = np.einsum("qij,pji->qp", inverse, basis, optimize=True)
        products = np.einsum("qij,pjk->qpik", inverse, basis, optimize=True)
        hlog = -np.einsum("qpij,qrji->qpr", products, products, optimize=True)
        p = probabilities[start:stop]
        lp = logs[start:stop]

        fisher -= np.einsum("q,qp,qr->pr", p, score, score, optimize=True)
        acceleration -= np.einsum("q,qp,qr->pr", p * lp, score, score, optimize=True)
        acceleration -= np.einsum("q,qpr->pr", p * lp, hlog, optimize=True)

    # fisher is -sum p*g*g; acceleration is -sum p*log(p)*(g*g+hlog).
    total = (fisher + acceleration)
    total = (total + total.T) / 2.0
    fisher = (fisher + fisher.T) / 2.0
    acceleration = (acceleration + acceleration.T) / 2.0
    diagnostics = {
        "entropy": float(-probabilities @ logs),
        "min_atom": float(probabilities.min()),
        "normalization_residual": abs(float(probabilities.sum()) - 1.0),
        "fisher_max_eigenvalue": float(np.linalg.eigvalsh(fisher)[-1]),
        "acceleration_max_eigenvalue": float(np.linalg.eigvalsh(acceleration)[-1]),
    }
    return total, fisher, acceleration, diagnostics


def entropy_hessian(kernel: np.ndarray, chunk: int = 256) -> tuple[np.ndarray, dict[str, float]]:
    total, _, _, diagnostics = entropy_hessian_components(kernel, chunk=chunk)
    return total, diagnostics


def acceleration_fisher_mechanism(
    fisher: np.ndarray, acceleration: np.ndarray
) -> tuple[float, np.ndarray, float, float, float]:
    """Maximize acceleration/(-fisher) on the numerically supported Fisher range.

    This generalized Rayleigh quotient is invariant under a change of symmetric
    coordinates.  A value above one is exactly a positive-curvature direction,
    provided the discarded numerical null space carries no positive curvature.
    """
    information = (-fisher + (-fisher).T) / 2.0
    values, vectors = np.linalg.eigh(information)
    scale = max(float(values[-1]), 1.0)
    keep = values > 1e-12 * scale
    if not np.any(keep):
        raise ArithmeticError("Fisher matrix has no numerically supported range")
    inverse_sqrt = vectors[:, keep] / np.sqrt(values[keep])[None, :]
    whitened = inverse_sqrt.T @ acceleration @ inverse_sqrt
    whitened = (whitened + whitened.T) / 2.0
    ratios, ratio_vectors = np.linalg.eigh(whitened)
    coordinates = inverse_sqrt @ ratio_vectors[:, -1]
    fisher_value = float(coordinates @ fisher @ coordinates)
    acceleration_value = float(coordinates @ acceleration @ coordinates)
    total_value = fisher_value + acceleration_value
    ratio = acceleration_value / (-fisher_value)
    return ratio, coordinates, fisher_value, acceleration_value, total_value


def matrix_from_coordinates(coordinates: np.ndarray, n: int) -> np.ndarray:
    basis, _ = symmetric_basis(n)
    return np.einsum("p,pij->ij", coordinates, basis)


def margin(kernel: np.ndarray) -> float:
    eigenvalues = np.linalg.eigvalsh(kernel)
    return float(min(eigenvalues[0], 1.0 - eigenvalues[-1]))


def symmetric_step(kernel: np.ndarray, direction: np.ndarray) -> float:
    low, high = 0.0, 1.0
    while high < 1024.0 and min(margin(kernel - high * direction), margin(kernel + high * direction)) > 1e-10:
        low, high = high, 2.0 * high
    for _ in range(64):
        middle = (low + high) / 2.0
        if min(margin(kernel - middle * direction), margin(kernel + middle * direction)) > 1e-10:
            low = middle
        else:
            high = middle
    return 0.2 * low


def random_kernel(n: int, rng: np.random.Generator, mode: int) -> np.ndarray:
    q, _ = np.linalg.qr(rng.normal(size=(n, n)))
    if mode == 0:
        eigenvalues = rng.uniform(0.08, 0.92, size=n)
    elif mode == 1:
        eigenvalues = np.clip(rng.beta(0.35, 0.35, size=n), 1e-4, 1.0 - 1e-4)
    elif mode == 2:
        eigenvalues = np.linspace(0.04, 0.96, n)
        rng.shuffle(eigenvalues)
    else:
        displacement = rng.normal(size=n)
        displacement /= max(np.linalg.norm(displacement), 1e-12)
        eigenvalues = np.clip(0.5 + 0.43 * displacement, 0.02, 0.98)
    return (q * eigenvalues) @ q.T


def direct_mobius(kernel: np.ndarray) -> np.ndarray:
    n = kernel.shape[0]
    inclusion = np.ones(1 << n, dtype=float)
    for mask in range(1, 1 << n):
        indices = [i for i in range(n) if (mask >> i) & 1]
        inclusion[mask] = np.linalg.det(kernel[np.ix_(indices, indices)])
    atoms = inclusion.copy()
    for i in range(n):
        for mask in range(1 << n):
            if not ((mask >> i) & 1):
                atoms[mask] -= atoms[mask | (1 << i)]
    return atoms


def self_test() -> dict[str, float | str]:
    rng = np.random.default_rng(2026090807)
    kernel = random_kernel(4, rng, 0)
    probabilities, _, _ = atoms_and_logs(kernel)
    mobius = direct_mobius(kernel)
    event_error = float(np.max(np.abs(probabilities - mobius)))
    hessian, _ = entropy_hessian(kernel, chunk=16)
    direction_coordinates = rng.normal(size=10)
    direction_coordinates /= np.linalg.norm(direction_coordinates)
    direction = matrix_from_coordinates(direction_coordinates, 4)
    direction /= np.linalg.norm(direction, 2)
    step = min(1e-4, margin(kernel) * 1e-3)
    center_entropy = entropy(kernel)[0]
    finite_difference = (entropy(kernel + step * direction)[0] + entropy(kernel - step * direction)[0] - 2.0 * center_entropy) / (step * step)
    # Convert the normalized direction back to the same symmetric coordinates.
    basis, pairs = symmetric_basis(4)
    normalized_coordinates = np.array([direction[i, j] for i, j in pairs])
    analytic = float(normalized_coordinates @ hessian @ normalized_coordinates)
    error = abs(analytic - finite_difference)
    if event_error > 2e-12 or error > 2e-5:
        raise AssertionError({"event_error": event_error, "hessian_error": error})
    return {
        "status": "PASS",
        "event_error": event_error,
        "hessian_analytic": analytic,
        "hessian_finite_difference": finite_difference,
        "hessian_error": error,
    }


def run(args: argparse.Namespace) -> None:
    out = Path(args.out)
    if out.exists():
        raise FileExistsError(f"refusing to overwrite {out}")
    out.mkdir(parents=True)
    ledger_path = out / "candidate_ledger.csv"
    manifest_path = out / "manifest.json"
    manifest = {
        "status": "RUNNING",
        "seed": args.seed,
        "n_min": args.n_min,
        "n_max": args.n_max,
        "trials_per_n": args.trials_per_n,
        "chunk": args.chunk,
        "numpy": np.__version__,
        "python": platform.python_version(),
        "threads": 1,
        "start_time": time.time(),
    }
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    rng = np.random.default_rng(args.seed)
    fields = [
        "index", "n", "mode", "margin", "entropy", "min_atom", "normalization_residual",
        "lambda_max_coordinate", "lambda_max", "fisher_along_top", "acceleration_along_top",
        "fisher_max_eigenvalue", "acceleration_max_eigenvalue", "mechanism_ratio",
        "mechanism_fisher", "mechanism_acceleration", "mechanism_total", "mechanism_rank",
        "direction_rank",
        "direction_singular_1", "direction_singular_2", "step", "gap", "endpoint_margin", "status",
    ]
    best: dict[str, float | int | str] | None = None
    best_mechanism: dict[str, float | int | str] | None = None
    index = 0
    with ledger_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for n in range(args.n_min, args.n_max + 1):
            basis, pairs = symmetric_basis(n)
            for trial in range(args.trials_per_n):
                kernel = random_kernel(n, rng, trial % 4)
                hessian, fisher_matrix, acceleration_matrix, diagnostic = entropy_hessian_components(
                    kernel, chunk=args.chunk
                )
                eigenvalues, eigenvectors = np.linalg.eigh(hessian)
                coordinates = eigenvectors[:, -1]
                direction = matrix_from_coordinates(coordinates, n)
                direction /= np.linalg.norm(direction, 2)
                normalized_coordinates = np.array([direction[i, j] for i, j in pairs])
                lambda_along = float(normalized_coordinates @ hessian @ normalized_coordinates)

                mechanism_ratio, mechanism_coordinates, mechanism_fisher, mechanism_acceleration, mechanism_total = (
                    acceleration_fisher_mechanism(fisher_matrix, acceleration_matrix)
                )
                mechanism_direction = matrix_from_coordinates(mechanism_coordinates, n)
                mechanism_direction /= np.linalg.norm(mechanism_direction, 2)
                mechanism_singular = np.linalg.svd(mechanism_direction, compute_uv=False)
                mechanism_rank = int(np.sum(mechanism_singular > mechanism_singular[0] * 1e-9))

                probabilities, logs, matrices = atoms_and_logs(kernel)
                fisher_along = 0.0
                acceleration_along = 0.0
                for start in range(0, len(probabilities), args.chunk):
                    stop = min(start + args.chunk, len(probabilities))
                    inverse = np.linalg.inv(matrices[start:stop])
                    score = np.einsum("qij,ji->q", inverse, direction, optimize=True)
                    hlog = -np.einsum("qij,qji->q", inverse @ direction, inverse @ direction, optimize=True)
                    p = probabilities[start:stop]
                    lp = logs[start:stop]
                    fisher_along -= float(np.sum(p * score * score))
                    acceleration_along -= float(np.sum(p * lp * (score * score + hlog)))

                step = symmetric_step(kernel, direction)
                minus_entropy = entropy(kernel - step * direction)[0]
                plus_entropy = entropy(kernel + step * direction)[0]
                gap = (minus_entropy + plus_entropy) / 2.0 - diagnostic["entropy"]
                singular = np.linalg.svd(direction, compute_uv=False)
                direction_rank = int(np.sum(singular > singular[0] * 1e-9))
                row = {
                    "index": index,
                    "n": n,
                    "mode": trial % 4,
                    "margin": margin(kernel),
                    "entropy": diagnostic["entropy"],
                    "min_atom": diagnostic["min_atom"],
                    "normalization_residual": diagnostic["normalization_residual"],
                    "lambda_max_coordinate": float(eigenvalues[-1]),
                    "lambda_max": lambda_along,
                    "fisher_along_top": fisher_along,
                    "acceleration_along_top": acceleration_along,
                    "fisher_max_eigenvalue": diagnostic["fisher_max_eigenvalue"],
                    "acceleration_max_eigenvalue": diagnostic["acceleration_max_eigenvalue"],
                    "mechanism_ratio": mechanism_ratio,
                    "mechanism_fisher": mechanism_fisher,
                    "mechanism_acceleration": mechanism_acceleration,
                    "mechanism_total": mechanism_total,
                    "mechanism_rank": mechanism_rank,
                    "direction_rank": direction_rank,
                    "direction_singular_1": float(singular[0]),
                    "direction_singular_2": float(singular[1]) if n > 1 else 0.0,
                    "step": step,
                    "gap": gap,
                    "endpoint_margin": min(margin(kernel - step * direction), margin(kernel + step * direction)),
                    "status": "FLOAT_CANDIDATE" if (lambda_along > args.curvature_threshold or gap > args.gap_threshold) else "NO_HIT",
                }
                writer.writerow(row)
                handle.flush()
                if best is None or float(row["lambda_max"]) > float(best["lambda_max"]):
                    best = row.copy()
                    np.savez_compressed(out / "best_case.npz", kernel=kernel, direction=direction)
                    (out / "best_case.json").write_text(json.dumps(best, indent=2), encoding="utf-8")
                if best_mechanism is None or float(row["mechanism_ratio"]) > float(best_mechanism["mechanism_ratio"]):
                    best_mechanism = row.copy()
                    np.savez_compressed(
                        out / "best_mechanism_case.npz",
                        kernel=kernel,
                        direction=mechanism_direction,
                    )
                    (out / "best_mechanism_case.json").write_text(
                        json.dumps(best_mechanism, indent=2), encoding="utf-8"
                    )
                index += 1
                if index % 5 == 0:
                    print(json.dumps({"completed": index, "best_lambda": best["lambda_max"] if best else None}), flush=True)

    manifest.update({
        "status": "SCOUT_COMPLETE",
        "completed": index,
        "best_lambda": best["lambda_max"] if best else None,
        "best_gap": best["gap"] if best else None,
        "best_mechanism_ratio": best_mechanism["mechanism_ratio"] if best_mechanism else None,
        "elapsed_seconds": time.time() - manifest["start_time"],
        "exit_code": 0,
        "warning": "float64 scout only; finite non-hit is not a theorem",
    })
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest), flush=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--out")
    parser.add_argument("--seed", type=int, default=2026090808)
    parser.add_argument("--n-min", type=int, default=3)
    parser.add_argument("--n-max", type=int, default=8)
    parser.add_argument("--trials-per-n", type=int, default=4)
    parser.add_argument("--chunk", type=int, default=128)
    parser.add_argument("--curvature-threshold", type=float, default=1e-8)
    parser.add_argument("--gap-threshold", type=float, default=1e-10)
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    if arguments.self_test:
        print(json.dumps(self_test(), indent=2))
    else:
        if not arguments.out:
            raise SystemExit("--out is required unless --self-test is used")
        run(arguments)
