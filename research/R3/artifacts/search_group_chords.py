"""Bounded resumable scout for grouped real-symmetric DPP chords.

This is diagnostic search only.  A positive floating gap is a candidate, not a
certificate; it must be exported to an independent rational/interval checker.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import platform
import sys
from pathlib import Path
from typing import Any

import numpy as np

from group_count_entropy import grouped_entropy


def logistic(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-x))


def random_symmetric(rng: np.random.Generator, q: int) -> np.ndarray:
    raw = rng.normal(size=(q, q))
    out = 0.5 * (raw + raw.T)
    norm = np.linalg.norm(out, ord="fro")
    return out / norm if norm else np.eye(q) / math.sqrt(q)


def random_base(rng: np.random.Generator, q: int, logit_radius: float) -> tuple[np.ndarray, np.ndarray]:
    avec = logistic(rng.uniform(-logit_radius, logit_radius, size=q))
    qmat, _ = np.linalg.qr(rng.normal(size=(q, q)))
    eig = logistic(rng.uniform(-logit_radius, logit_radius, size=q))
    cmat = qmat @ np.diag(eig) @ qmat.T
    return avec, 0.5 * (cmat + cmat.T)


def feasible(a: np.ndarray, cmat: np.ndarray, da: np.ndarray, dc: np.ndarray, t: float, margin: float) -> bool:
    for sign in (-1.0, 1.0):
        aa = a + sign * t * da
        cc = cmat + sign * t * dc
        eig = np.linalg.eigvalsh(cc)
        if np.min(aa) <= margin or np.max(aa) >= 1.0 - margin:
            return False
        if eig[0] <= margin or eig[-1] >= 1.0 - margin:
            return False
    return True


def chord_radius(a: np.ndarray, cmat: np.ndarray, da: np.ndarray, dc: np.ndarray, margin: float) -> float:
    lo, hi = 0.0, 1.0
    while feasible(a, cmat, da, dc, hi, margin) and hi < 1e6:
        lo, hi = hi, 2.0 * hi
    for _ in range(70):
        mid = 0.5 * (lo + hi)
        if feasible(a, cmat, da, dc, mid, margin):
            lo = mid
        else:
            hi = mid
    return lo


def one_trial(rng: np.random.Generator, sizes: list[int], config: dict[str, Any]) -> dict[str, Any]:
    q = len(sizes)
    a, cmat = random_base(rng, q, float(config["logit_radius"]))
    da = rng.normal(size=q)
    da /= np.linalg.norm(da)
    dc = random_symmetric(rng, q)
    radius = chord_radius(a, cmat, da, dc, float(config["spectral_margin"]))
    t = float(config["radius_fraction"]) * radius
    hmid, zmid, _ = grouped_entropy(sizes, a, cmat)
    hminus, zminus, _ = grouped_entropy(sizes, a - t * da, cmat - t * dc)
    hplus, zplus, _ = grouped_entropy(sizes, a + t * da, cmat + t * dc)
    gap = 0.5 * (hminus + hplus) - hmid
    eig_minus = np.linalg.eigvalsh(cmat - t * dc)
    eig_plus = np.linalg.eigvalsh(cmat + t * dc)
    margin = min(
        float(np.min(a - t * da)),
        float(np.min(a + t * da)),
        float(eig_minus[0]),
        float(eig_plus[0]),
        float(1.0 - np.max(a - t * da)),
        float(1.0 - np.max(a + t * da)),
        float(1.0 - eig_minus[-1]),
        float(1.0 - eig_plus[-1]),
    )
    return {
        "group_sizes": sizes,
        "a": a.tolist(),
        "C": cmat.tolist(),
        "da": da.tolist(),
        "dC": dc.tolist(),
        "t": t,
        "gap_endpoint_average_minus_midpoint": gap,
        "spectral_margin": margin,
        "normalization_error_max": max(abs(zminus - 1.0), abs(zmid - 1.0), abs(zplus - 1.0)),
        "classification": "FLOAT_CANDIDATE" if gap > float(config["candidate_threshold"]) else "NO_HIT",
    }


def completed_ids(path: Path) -> set[int]:
    if not path.exists():
        return set()
    done: set[int] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            done.add(int(json.loads(line)["trial_id"]))
    return done


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    output = (args.config.parent / config["output_jsonl"]).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    done = completed_ids(output)
    master = np.random.SeedSequence(int(config["seed"]))
    children = master.spawn(int(config["trials"]))
    modes = [list(map(int, sizes)) for sizes in config["group_size_cases"]]
    hits = 0
    best: dict[str, Any] | None = None
    with output.open("a", encoding="utf-8", buffering=1) as handle:
        for trial_id, child in enumerate(children):
            if trial_id in done:
                continue
            rng = np.random.default_rng(child)
            sizes = modes[trial_id % len(modes)]
            record = one_trial(rng, sizes, config)
            record.update({"trial_id": trial_id, "seed_entropy": child.entropy})
            handle.write(json.dumps(record, sort_keys=True) + "\n")
            if record["classification"] == "FLOAT_CANDIDATE":
                hits += 1
            if best is None or record["gap_endpoint_average_minus_midpoint"] > best["gap_endpoint_average_minus_midpoint"]:
                best = record
    summary = {
        "status": "COMPLETED",
        "pid": os.getpid(),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "seed": config["seed"],
        "trials_requested": config["trials"],
        "trials_preexisting": len(done),
        "trials_executed": int(config["trials"]) - len(done),
        "float_candidate_count_new": hits,
        "best_new": best,
        "warning": "Floating search is diagnostic only; a positive gap is not certified.",
    }
    summary_path = output.with_suffix(".summary.json")
    summary_path.write_text(json.dumps(summary, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
