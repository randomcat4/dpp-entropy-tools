"""Local, reproducible optimization of the acceleration/Fisher ratio.

This is a float64 mechanism scout, not a proof.  Strict feasibility is built in
by writing K as the spectral logistic of a real symmetric matrix Z.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import platform
import time
from pathlib import Path

for _name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_name, "1")

import numpy as np

from dense_hessian import (
    acceleration_fisher_mechanism,
    atoms_and_logs,
    entropy_hessian_components,
    margin,
    matrix_from_coordinates,
)


def spectral_function(matrix: np.ndarray, function) -> np.ndarray:
    values, vectors = np.linalg.eigh((matrix + matrix.T) / 2.0)
    return (vectors * function(values)) @ vectors.T


def kernel_to_logit(kernel: np.ndarray) -> np.ndarray:
    return spectral_function(kernel, lambda x: np.log(x / (1.0 - x)))


def project_logit(logit: np.ndarray, bound: float) -> np.ndarray:
    return spectral_function(logit, lambda x: np.clip(x, -bound, bound))


def logit_to_kernel(logit: np.ndarray) -> np.ndarray:
    return spectral_function(logit, lambda x: 1.0 / (1.0 + np.exp(-x)))


def evaluate(kernel: np.ndarray, chunk: int, atom_floor: float) -> dict[str, object] | None:
    try:
        probabilities, _, _ = atoms_and_logs(kernel)
        if float(probabilities.min()) < atom_floor:
            return None
        total, fisher, acceleration, diagnostic = entropy_hessian_components(kernel, chunk=chunk)
        ratio, coordinates, fisher_value, acceleration_value, mechanism_total = (
            acceleration_fisher_mechanism(fisher, acceleration)
        )
        direction = matrix_from_coordinates(coordinates, kernel.shape[0])
        direction /= np.linalg.norm(direction, 2)
        top_total = float(np.linalg.eigvalsh(total)[-1])
        return {
            "ratio": ratio,
            "mechanism_fisher": fisher_value,
            "mechanism_acceleration": acceleration_value,
            "mechanism_total": mechanism_total,
            "top_total_coordinate": top_total,
            "min_atom": diagnostic["min_atom"],
            "margin": margin(kernel),
            "direction": direction,
        }
    except (ArithmeticError, np.linalg.LinAlgError, FloatingPointError):
        return None


def random_symmetric(n: int, rng: np.random.Generator) -> np.ndarray:
    matrix = rng.normal(size=(n, n))
    matrix = (matrix + matrix.T) / 2.0
    return matrix / max(np.linalg.norm(matrix, 2), 1e-15)


def run(args: argparse.Namespace) -> None:
    source = Path(args.source)
    out = Path(args.out)
    if out.exists():
        raise FileExistsError(f"refusing to overwrite {out}")
    out.mkdir(parents=True)
    with np.load(source) as data:
        kernel = np.array(data["kernel"], dtype=float)
    n = kernel.shape[0]
    logit = kernel_to_logit(kernel)
    initial_eigenvectors = np.linalg.eigh(logit)[1]
    rng = np.random.default_rng(args.seed)
    start = time.time()
    current = evaluate(kernel, args.chunk, args.atom_floor)
    if current is None:
        raise ArithmeticError("source kernel failed the evaluation gates")
    best = current
    best_kernel = kernel.copy()
    best_logit = logit.copy()
    accepted = 0
    evaluated = 1
    rejected_gate = 0
    history = [{"evaluation": 0, "scale": 0.0, **{k: v for k, v in current.items() if k != "direction"}}]

    scales = [float(item) for item in args.scales.split(",")]
    for scale in scales:
        for _ in range(args.trials_per_scale):
            if args.spectral_only:
                values = np.linalg.eigvalsh(best_logit)
                delta = rng.normal(size=n)
                delta /= max(np.linalg.norm(delta), 1e-15)
                proposal_logit = (initial_eigenvectors * (values + scale * delta)) @ initial_eigenvectors.T
            else:
                proposal_logit = best_logit + scale * random_symmetric(n, rng)
            proposal_logit = project_logit(proposal_logit, args.logit_bound)
            proposal_kernel = logit_to_kernel(proposal_logit)
            proposal = evaluate(proposal_kernel, args.chunk, args.atom_floor)
            evaluated += 1
            if proposal is None:
                rejected_gate += 1
                continue
            if float(proposal["ratio"]) > float(best["ratio"]):
                best = proposal
                best_kernel = proposal_kernel
                best_logit = proposal_logit
                accepted += 1
                history.append({
                    "evaluation": evaluated,
                    "scale": scale,
                    **{k: v for k, v in proposal.items() if k != "direction"},
                })
                print(json.dumps(history[-1]), flush=True)

    direction = np.asarray(best["direction"])
    np.savez_compressed(out / "best_case.npz", kernel=best_kernel, direction=direction, logit=best_logit)
    summary = {
        "status": "SCOUT_COMPLETE",
        "source": str(source),
        "seed": args.seed,
        "n": n,
        "spectral_only": args.spectral_only,
        "scales": scales,
        "trials_per_scale": args.trials_per_scale,
        "evaluated": evaluated,
        "accepted": accepted,
        "rejected_gate": rejected_gate,
        "atom_floor": args.atom_floor,
        "logit_bound": args.logit_bound,
        "initial_ratio": current["ratio"],
        "best": {k: v for k, v in best.items() if k != "direction"},
        "elapsed_seconds": time.time() - start,
        "numpy": np.__version__,
        "python": platform.python_version(),
        "threads": 1,
        "warning": "float64 local mechanism optimization; not a theorem or counterexample certificate",
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (out / "history.json").write_text(json.dumps(history, indent=2), encoding="utf-8")
    print(json.dumps(summary), flush=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--seed", type=int, default=2026090813)
    parser.add_argument("--scales", default="1,0.5,0.2,0.1,0.05,0.02")
    parser.add_argument("--trials-per-scale", type=int, default=100)
    parser.add_argument("--chunk", type=int, default=128)
    parser.add_argument("--atom-floor", type=float, default=1e-14)
    parser.add_argument("--logit-bound", type=float, default=9.0)
    parser.add_argument("--spectral-only", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    run(parse_args())
