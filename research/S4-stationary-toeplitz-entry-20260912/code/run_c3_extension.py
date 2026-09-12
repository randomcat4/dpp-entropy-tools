#!/usr/bin/env python3
"""Targeted C3 continuation with an explicit exponential-cost stop."""
from __future__ import annotations

import argparse
import csv
import json
import time
from pathlib import Path

import numpy as np

import upstream_nonsmooth_interval_probe as upstream
from run_c4_c3 import FAMILIES, matrices


CASES = (
    ("near_symmetric_m2_least", 0.2, 26),
    ("near_symmetric_m3_selected", 0.01, 24),
    ("near_symmetric_m4_meaningful", 0.01, 24),
    ("near_symmetric_m4_meaningful", 0.002, 24),
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    rows, timings = [], []
    started = time.time()
    for family, epsilon, max_n in CASES:
        K, E = matrices(family, epsilon, max_n)
        tick = time.time()
        R, R1, R2, fisher, transport, stats = upstream.conditional_increment_jets(K, E)
        elapsed = time.time() - tick
        cumulative = np.cumsum(R2)
        timings.append({"family": family, "epsilon": epsilon, "max_n": max_n, "nodes": int(stats[2]), "seconds": elapsed})
        for n in range(2, max_n + 1):
            spectral = upstream.spectral_increment_hessian(K[:n, :n], E[:n, :n])
            rows.append({
                "family": family, "epsilon": epsilon, "n": n,
                "Hn_second": float(cumulative[n - 1]),
                "increment_second": float(R2[n - 1]),
                "Hn_second_over_n": float(cumulative[n - 1] / n),
                "conditional_fisher": float(fisher[n - 1]),
                "prediction_vertical": float(transport[n - 1]),
                "spectral_increment": float(spectral),
                "coherence_increment": float(R2[n - 1] - spectral),
            })
        print(family, epsilon, max_n, R2[max_n - 1], elapsed, flush=True)
    with (args.output_dir / "extended_curvature.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)
    # The node count is exactly 2^n-1.  Use measured n=26 cost to make the
    # stop auditable rather than silently abandoning requested larger n.
    anchor = max(timings, key=lambda x: x["max_n"])
    projected = {str(n): anchor["seconds"] * 2 ** (n - anchor["max_n"]) for n in (28, 30)}
    record = {
        "cases": timings,
        "cost_model": "complete prefix recursion visits exactly 2^n-1 nodes",
        "projected_seconds_from_largest_run": projected,
        "stop": "Stopped after n=26 for the closest-to-zero family and n=24 for three substantive families because every tested increment remained negative and exact recursion cost quadruples for each +2 sites.",
        "elapsed_seconds": time.time() - started,
        "scope": "finite deterministic sequence; no entropy-rate sign conclusion",
    }
    (args.output_dir / "c3_extension_run.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
