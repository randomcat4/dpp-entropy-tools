"""Checkpointed local Hessian search around a selected ledger record.

Proposals lie on random feasible chords through an elite archive.  Both sides of
each chord are sampled, so near-boundary records are not only pushed inward.
All numerical hits remain exploratory until independently high-precision checked.
"""
import os

for name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[name] = "1"

import argparse
import csv
import json
import math
import sys
import time
from pathlib import Path

import numpy as np

STRUCTURE_DIR = Path(__file__).resolve().parents[1] / "structure"
sys.path.insert(0, str(STRUCTURE_DIR))
from structure_search import Family, random_x


def read_row(path, index):
    with Path(path).open(newline="") as handle:
        for row in csv.DictReader(handle):
            if int(row["index"]) == index:
                return row
    raise KeyError(f"ledger index {index} not found")


def atomic_json(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2), encoding="utf-8")
    temporary.replace(path)


def max_reverse_step(family, parent, chord, floor=1e-10):
    """Largest tested alpha with parent-alpha*chord remaining feasible."""
    low, high = 0.0, 1.0
    while family.margin(parent - high * chord) > floor and high < 1024:
        low, high = high, high * 2
    for _ in range(45):
        middle = (low + high) / 2
        if family.margin(parent - middle * chord) > floor:
            low = middle
        else:
            high = middle
    return low


def symmetric_probe(family, x, entropy, direction):
    low, high = 0.0, 1.0
    while min(family.margin(x - high * direction), family.margin(x + high * direction)) > 1e-9:
        low, high = high, high * 2
        if high > 1024:
            break
    for _ in range(45):
        middle = (low + high) / 2
        if min(family.margin(x - middle * direction), family.margin(x + middle * direction)) > 1e-9:
            low = middle
        else:
            high = middle
    step = 0.2 * low
    if not math.isfinite(step) or step <= 0:
        return 0.0, float("nan"), float("nan")
    hm = family.evaluate(x - step * direction)[0]
    hp = family.evaluate(x + step * direction)[0]
    return step, (hm + hp) / 2 - entropy, min(
        family.margin(x - step * direction), family.margin(x + step * direction)
    )


def serialize_elite(elite):
    return [{"lambda_max": item[0], "x": item[1].tolist()} for item in elite]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", required=True)
    parser.add_argument("--index", type=int, required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--trials", type=int, required=True)
    parser.add_argument("--checkpoint-every", type=int, default=100)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    checkpoint_path = out / "checkpoint.json"
    manifest_path = out / "manifest.json"
    improvements_path = out / "improvements.jsonl"
    candidates_path = out / "candidates.jsonl"
    source = read_row(args.ledger, args.index)
    sizes = json.loads(source["sizes"])
    center = np.asarray(json.loads(source["parameters"]), dtype=float)
    family = Family(sizes)
    rng = np.random.default_rng(args.seed)
    started = time.time()

    immutable = {
        "ledger": str(Path(args.ledger).resolve()),
        "index": args.index,
        "sizes": sizes,
        "seed": args.seed,
        "algorithm": "elite-feasible-chords-v1",
    }
    if args.resume:
        saved = json.loads(checkpoint_path.read_text(encoding="utf-8"))
        if saved["immutable"] != immutable:
            raise ValueError("checkpoint configuration mismatch")
        completed = int(saved["completed"])
        rng.bit_generator.state = saved["rng_state"]
        elite = [(float(item["lambda_max"]), np.asarray(item["x"], dtype=float)) for item in saved["elite"]]
        best_record = saved["best_record"]
    else:
        if checkpoint_path.exists():
            raise FileExistsError("output already has a checkpoint; pass --resume")
        entropy, _, hessian = family.evaluate(center, True)
        eigenvalues, eigenvectors = np.linalg.eigh(hessian)
        direction = eigenvectors[:, -1]
        step, gap, endpoint_margin = symmetric_probe(family, center, entropy, direction)
        best_record = {
            "trial": -1,
            "lambda_max": float(eigenvalues[-1]),
            "entropy": entropy,
            "margin": family.margin(center),
            "step": step,
            "gap": gap,
            "endpoint_margin": endpoint_margin,
            "x": center.tolist(),
            "direction": direction.tolist(),
        }
        elite = [(float(eigenvalues[-1]), center.copy())]
        completed = 0
        improvements_path.write_text(json.dumps(best_record) + "\n", encoding="utf-8")
        candidates_path.write_text("", encoding="utf-8")

    manifest = {
        **immutable,
        "requested_trials": args.trials,
        "completed": completed,
        "status": "RUNNING",
        "pid": os.getpid(),
        "started_unix": started,
        "threads": 1,
    }
    atomic_json(manifest_path, manifest)

    for trial in range(completed, args.trials):
        # Bias toward the best archive members but keep enough diversity to avoid
        # collapsing onto one numerical ridge.
        rank = min(int(rng.exponential(5.0)), len(elite) - 1)
        parent = elite[rank][1]
        guide = random_x(family, rng, int(rng.integers(0, 4)))
        chord = guide - parent
        if rng.random() < 0.65:
            alpha = 10.0 ** rng.uniform(-8.0, -0.15)
            proposal = parent + alpha * chord
        else:
            reverse_limit = max_reverse_step(family, parent, chord)
            alpha = reverse_limit * (10.0 ** rng.uniform(-8.0, -0.02))
            proposal = parent - alpha * chord

        try:
            entropy, _, hessian = family.evaluate(proposal, True)
            eigenvalues, eigenvectors = np.linalg.eigh(hessian)
            lambda_max = float(eigenvalues[-1])
            direction = eigenvectors[:, -1]
        except (ArithmeticError, np.linalg.LinAlgError, ValueError, FloatingPointError):
            completed = trial + 1
            continue

        is_elite = len(elite) < 32 or lambda_max > elite[-1][0]
        if is_elite:
            step, gap, endpoint_margin = symmetric_probe(family, proposal, entropy, direction)
            record = {
                "trial": trial,
                "lambda_max": lambda_max,
                "entropy": entropy,
                "margin": family.margin(proposal),
                "step": step,
                "gap": gap,
                "endpoint_margin": endpoint_margin,
                "x": proposal.tolist(),
                "direction": direction.tolist(),
            }
            elite.append((lambda_max, proposal.copy()))
            elite.sort(key=lambda item: item[0], reverse=True)
            elite = elite[:32]
            with improvements_path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(record) + "\n")
            if lambda_max > best_record["lambda_max"]:
                best_record = record
                print(json.dumps({"event": "NEW_BEST", **record}), flush=True)
            if lambda_max > 1e-9 or gap > 1e-10:
                with candidates_path.open("a", encoding="utf-8") as handle:
                    handle.write(json.dumps(record) + "\n")
                print(json.dumps({"event": "FLOAT_CANDIDATE", **record}), flush=True)

        completed = trial + 1
        if completed % args.checkpoint_every == 0 or completed == args.trials:
            checkpoint = {
                "immutable": immutable,
                "completed": completed,
                "rng_state": rng.bit_generator.state,
                "elite": serialize_elite(elite),
                "best_record": best_record,
                "updated_unix": time.time(),
            }
            atomic_json(checkpoint_path, checkpoint)
        if completed % 1000 == 0:
            print(
                json.dumps(
                    {
                        "event": "PROGRESS",
                        "completed": completed,
                        "requested_trials": args.trials,
                        "best_lambda": best_record["lambda_max"],
                        "best_gap": best_record["gap"],
                        "elapsed_seconds": time.time() - started,
                    }
                ),
                flush=True,
            )

    manifest.update(
        status="COMPLETE",
        completed=completed,
        finished_unix=time.time(),
        elapsed_seconds=time.time() - started,
        best_record=best_record,
    )
    atomic_json(manifest_path, manifest)
    print(json.dumps(manifest), flush=True)


if __name__ == "__main__":
    main()
