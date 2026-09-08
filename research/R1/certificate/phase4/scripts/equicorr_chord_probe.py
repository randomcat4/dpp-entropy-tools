#!/usr/bin/env python3
"""Finite midpoint-gap probes through n=3 equicorrelation centers.

This script samples strict centers K0=(a-c)I+c11^T and random symmetric
directions V, scales V to spectral norm one, finds a feasible symmetric
radius by bisection, and tests actual midpoint gaps

    [H(K0-tV)+H(K0+tV)]/2 - H(K0).

It is a finite numerical probe only.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import random
import time
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")
os.environ.setdefault("MKL_NUM_THREADS", "2")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "2")

import numpy as np


MASKS = list(range(8))


def bits(mask: int) -> list[int]:
    return [i for i in range(3) if (mask >> i) & 1]


def det_sub(K: np.ndarray, mask: int) -> float:
    idx = bits(mask)
    if not idx:
        return 1.0
    return float(np.linalg.det(K[np.ix_(idx, idx)]))


def event_values(K: np.ndarray) -> np.ndarray:
    inc = np.array([det_sub(K, m) for m in MASKS], dtype=float)
    p = np.zeros(8, dtype=float)
    for s in MASKS:
        total = 0.0
        for t in MASKS:
            if (t & s) == s:
                total += (-1.0 if ((t.bit_count() - s.bit_count()) & 1) else 1.0) * inc[t]
        p[s] = total
    return p


def entropy(K: np.ndarray) -> float:
    p = event_values(K)
    if np.any(p <= 0.0):
        return float("nan")
    return float(-np.sum(p * np.log(p)))


def center_from_lambdas(lam1: float, lam2: float) -> tuple[float, float, np.ndarray]:
    a = (lam1 + 2.0 * lam2) / 3.0
    c = (lam1 - lam2) / 3.0
    return a, c, (a - c) * np.eye(3) + c * np.ones((3, 3), dtype=float)


def spectral_margin(K: np.ndarray) -> float:
    ev = np.linalg.eigvalsh(K)
    return float(min(np.min(ev), np.min(1.0 - ev)))


def feasible(K: np.ndarray, strict_tol: float = 0.0) -> bool:
    return spectral_margin(K) > strict_tol


def random_center(rng: random.Random, eps: float) -> tuple[float, float, np.ndarray, float, float]:
    def draw_lam() -> float:
        if rng.random() < 0.40:
            z = 10.0 ** rng.uniform(math.log10(eps), math.log10(0.5))
            return z if rng.random() < 0.5 else 1.0 - z
        return eps + (1.0 - 2.0 * eps) * rng.random()
    lam1, lam2 = draw_lam(), draw_lam()
    a, c, K = center_from_lambdas(lam1, lam2)
    return a, c, K, lam1, lam2


def random_direction(rng: random.Random) -> np.ndarray:
    A = np.array([[rng.gauss(0, 1) for _ in range(3)] for _ in range(3)], dtype=float)
    V = 0.5 * (A + A.T)
    norm = float(max(abs(np.linalg.eigvalsh(V))))
    if norm == 0.0:
        return random_direction(rng)
    return V / norm


def feasible_radius(K: np.ndarray, V: np.ndarray) -> float:
    lo = 0.0
    hi = 1.0
    while feasible(K + hi * V) and feasible(K - hi * V) and hi < 16.0:
        lo = hi
        hi *= 2.0
    if lo == 0.0 and not (feasible(K + hi * V) and feasible(K - hi * V)):
        pass
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if feasible(K + mid * V) and feasible(K - mid * V):
            lo = mid
        else:
            hi = mid
    return lo


def choose_fraction(rng: random.Random) -> float:
    r = rng.random()
    if r < 0.50:
        return rng.random()
    if r < 0.85:
        return 1.0 - 10.0 ** rng.uniform(-6.0, -0.2)
    return 10.0 ** rng.uniform(-6.0, -0.2)


def scan(args: argparse.Namespace) -> dict[str, object]:
    rng = random.Random(args.seed)
    start = time.time()
    best: dict[str, object] | None = None
    positives: list[dict[str, object]] = []
    checked = 0
    infeasible_radius = 0

    for _ in range(args.trials):
        a, c, K, lam1, lam2 = random_center(rng, args.eps)
        V = random_direction(rng)
        rmax = feasible_radius(K, V)
        if not (rmax > 0.0):
            infeasible_radius += 1
            continue
        frac = choose_fraction(rng)
        t = frac * rmax
        Km = K - t * V
        Kp = K + t * V
        gap = 0.5 * (entropy(Km) + entropy(Kp)) - entropy(K)
        rec = {
            "trial": checked,
            "lambda1": lam1,
            "lambda2": lam2,
            "a": a,
            "c": c,
            "radius": rmax,
            "fraction": frac,
            "t": t,
            "gap": gap,
            "endpoint_margin": min(spectral_margin(Km), spectral_margin(Kp)),
            "V": V.tolist(),
        }
        checked += 1
        if best is None or (math.isfinite(gap) and gap > best["gap"]):
            best = rec
        if math.isfinite(gap) and gap > args.positive_tol:
            positives.append(rec)
            if args.stop_on_positive:
                break

    return {
        "status": "FINITE_PROBE",
        "note": "Random finite chord scan only; positive candidates need high-precision/rational certification.",
        "seed": args.seed,
        "eps": args.eps,
        "trials_requested": args.trials,
        "trials_checked": checked,
        "infeasible_radius": infeasible_radius,
        "elapsed_seconds": time.time() - start,
        "positive_tol": args.positive_tol,
        "best": best,
        "positive_count": len(positives),
        "positives": positives[: args.keep_positives],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=20260908)
    ap.add_argument("--trials", type=int, default=10000)
    ap.add_argument("--eps", type=float, default=1e-6)
    ap.add_argument("--positive-tol", type=float, default=1e-10)
    ap.add_argument("--keep-positives", type=int, default=20)
    ap.add_argument("--stop-on-positive", action="store_true")
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()
    result = scan(args)
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
