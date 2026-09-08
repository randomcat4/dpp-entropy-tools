"""n=2 fixed-eigenvector PSD spectral-rate probe.

This is an author-side scout/helper.  It uses the explicit exact-event atoms
for a 2x2 DPP and never calls server scans or dense_hessian author evaluators.
"""

from __future__ import annotations

import json
import math
import random
from pathlib import Path


def atoms(l1: float, l2: float, alpha: float) -> list[float]:
    """Return [empty, {1}, {2}, {1,2}] for alpha=cos(2 theta)."""
    p0 = (1.0 - l1) * (1.0 - l2)
    p12 = l1 * l2
    r = l1 * (1.0 - l2)
    q = l2 * (1.0 - l1)
    p1 = 0.5 * ((1.0 + alpha) * r + (1.0 - alpha) * q)
    p2 = 0.5 * ((1.0 - alpha) * r + (1.0 + alpha) * q)
    return [p0, p1, p2, p12]


def derivatives(l1: float, l2: float, alpha: float, v1: float, v2: float) -> tuple[list[float], list[float]]:
    p0_1 = -v1 * (1.0 - l2) - v2 * (1.0 - l1)
    p12_1 = v1 * l2 + v2 * l1
    r_1 = v1 * (1.0 - l2) - l1 * v2
    q_1 = v2 * (1.0 - l1) - l2 * v1
    p1_1 = 0.5 * ((1.0 + alpha) * r_1 + (1.0 - alpha) * q_1)
    p2_1 = 0.5 * ((1.0 - alpha) * r_1 + (1.0 + alpha) * q_1)
    cross = v1 * v2
    return [p0_1, p1_1, p2_1, p12_1], [2.0 * cross, -2.0 * cross, -2.0 * cross, 2.0 * cross]


def entropy_h2(l1: float, l2: float, alpha: float, v1: float, v2: float) -> dict[str, float]:
    p = atoms(l1, l2, alpha)
    p1, p2 = derivatives(l1, l2, alpha, v1, v2)
    fisher = sum(a * a / b for a, b in zip(p1, p))
    acceleration = -sum(b * math.log(a) for a, b in zip(p, p2))
    return {
        "H2": acceleration - fisher,
        "fisher": fisher,
        "acceleration": acceleration,
        "rho": acceleration / fisher if fisher else float("nan"),
        "p_min": min(p),
        "odds_ratio_singletons_over_extremes": (p[1] * p[2]) / (p[0] * p[3]),
    }


def random_probe(seed: int = 20260908, trials: int = 200000) -> dict[str, object]:
    rng = random.Random(seed)
    best = {"H2": -float("inf")}
    best_rho = {"rho": -float("inf")}
    positive = 0
    for _ in range(trials):
        l1 = rng.uniform(1e-5, 1 - 1e-5)
        l2 = rng.uniform(1e-5, 1 - 1e-5)
        alpha = rng.uniform(-1, 1)
        v1 = 10 ** rng.uniform(-3, 3)
        v2 = 10 ** rng.uniform(-3, 3)
        row = entropy_h2(l1, l2, alpha, v1, v2)
        if row["H2"] > 1e-12:
            positive += 1
        if row["H2"] > best["H2"]:
            best = {**row, "l1": l1, "l2": l2, "alpha": alpha, "v1": v1, "v2": v2}
        if row["rho"] > best_rho["rho"]:
            best_rho = {**row, "l1": l1, "l2": l2, "alpha": alpha, "v1": v1, "v2": v2}
    return {
        "status": "SCOUT_ONLY",
        "seed": seed,
        "trials": trials,
        "positive_H2_gt_1e-12": positive,
        "best_H2": best,
        "best_rho": best_rho,
        "warning": "finite random probe only; not a proof",
    }


def main() -> None:
    out = random_probe()
    path = Path(__file__).resolve().with_name("n2_probe_results.json")
    path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
