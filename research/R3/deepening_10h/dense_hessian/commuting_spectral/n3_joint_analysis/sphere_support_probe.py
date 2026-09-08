#!/usr/bin/env python3
"""Support-eigenvector probe for D10-M6.

For each sampled (theta, Q), reconstruct the 3x3 Hessian M of
v -> H''(theta; v), then maximize v^T M v over the positive orthant of the
Euclidean unit sphere.  In dimension three this can be done by checking every
non-empty support and every same-sign eigenvector of the corresponding
principal submatrix.  Boundary supports are included.

This is meant as a candidate generator / scout.  The numeric scan is not a
proof over the continuous (theta, Q) domain.
"""

from __future__ import annotations

import json
import time
from itertools import combinations
from pathlib import Path

import numpy as np

from joint_copositive_probe import (
    POSITIVE_TOL,
    SEED,
    STRICT_CLIP,
    h2_components,
    random_orthogonal,
    structured_orthogonals,
    theta_hessian,
)


SPHERE_SEED = SEED + 1
RANDOM_BASE_POINTS = 80_000


def theta_stream(rng: np.random.Generator):
    modes = rng.integers(0, 5, size=RANDOM_BASE_POINTS)
    for mode in modes:
        if mode == 0:
            theta = rng.uniform(0.02, 0.98, size=3)
        elif mode == 1:
            theta = rng.beta(0.35, 0.35, size=3)
        elif mode == 2:
            theta = rng.beta(1.5, 1.5, size=3)
        elif mode == 3:
            theta = rng.uniform(0.1, 0.9, size=3)
            j = int(rng.integers(0, 3))
            theta[j] = 10.0 ** rng.uniform(-5.0, -1.0)
            if rng.random() < 0.5:
                theta[j] = 1.0 - theta[j]
        else:
            theta = np.array([0.5, 0.5, 0.5]) + rng.normal(scale=0.08, size=3)
        yield np.clip(theta, STRICT_CLIP, 1.0 - STRICT_CLIP)


def support_sphere_candidates(M: np.ndarray):
    """Enumerate same-sign eigenvector candidates on all non-empty supports."""
    candidates: list[np.ndarray] = []
    for mask in range(1, 1 << 3):
        idx = [i for i in range(3) if (mask >> i) & 1]
        A = M[np.ix_(idx, idx)]
        vals, vecs = np.linalg.eigh(A)
        for col in range(vecs.shape[1]):
            loc = vecs[:, col]
            if np.all(loc >= -1e-10) or np.all(loc <= 1e-10):
                loc = np.abs(loc)
                norm = float(np.linalg.norm(loc))
                if norm > 0.0:
                    v = np.zeros(3)
                    v[idx] = loc / norm
                    candidates.append(v)
    # Coordinate axes are already present, but keep an explicit de-duplicated
    # list to make the denominator stable.
    unique: list[np.ndarray] = []
    for cand in candidates:
        if not any(np.linalg.norm(cand - old) < 1e-9 for old in unique):
            unique.append(cand)
    return unique


def max_on_positive_sphere(M: np.ndarray):
    best_val = -float("inf")
    best_v = None
    best_support = None
    candidate_count = 0
    for v in support_sphere_candidates(M):
        candidate_count += 1
        val = float(v @ M @ v)
        if val > best_val:
            best_val = val
            best_v = v.copy()
            best_support = [int(i) for i, x in enumerate(v) if x > 1e-9]
    omitted_gradients = None
    if best_v is not None:
        support = set(best_support or [])
        omitted_gradients = {
            str(i): float((M @ best_v)[i])
            for i in range(3)
            if i not in support
        }
    return best_val, best_v, best_support, candidate_count, omitted_gradients


def mechanism_ratio(components: dict):
    barrier = -components["count"]
    if barrier <= 0.0:
        return None
    return float(components["psi"] / barrier)


def maybe_update_best(best: dict, value: float, theta: np.ndarray, Q: np.ndarray, v: np.ndarray, M: np.ndarray, support, omitted):
    if value > best["value"]:
        comps = h2_components(theta, v, Q)
        best.update(
            {
                "value": float(value),
                "theta": theta.tolist(),
                "Q": Q.tolist(),
                "v_unit": v.tolist(),
                "support": support,
                "omitted_gradients_Mv": omitted,
                "components": comps,
                "psi_over_count_barrier": mechanism_ratio(comps),
                "hessian": M.tolist(),
            }
        )


def scan():
    t0 = time.time()
    rng = np.random.default_rng(SPHERE_SEED)
    best_total = {"value": -float("inf")}
    best_ratio = {"value": -float("inf")}
    positives = []
    candidate_vectors = 0
    base_points = 0

    structured_thetas = [
        np.array(x)
        for x in [
            (0.5, 0.5, 0.5),
            (0.2, 0.2, 0.8),
            (0.2, 0.8, 0.8),
            (0.1, 0.4, 0.9),
            (0.01, 0.2, 0.8),
            (0.001, 0.5, 0.999),
            (0.03, 0.57, 0.91),
            (0.17, 0.41, 0.73),
        ]
    ]

    for Q in structured_orthogonals():
        for theta in structured_thetas:
            base_points += 1
            M = theta_hessian(theta, Q, "total")
            value, v, support, n_cand, omitted = max_on_positive_sphere(M)
            candidate_vectors += n_cand
            maybe_update_best(best_total, value, theta, Q, v, M, support, omitted)
            comps = h2_components(theta, v, Q)
            ratio = mechanism_ratio(comps)
            if ratio is not None and ratio > best_ratio["value"]:
                best_ratio = {
                    "value": ratio,
                    "theta": theta.tolist(),
                    "Q": Q.tolist(),
                    "v_unit": v.tolist(),
                    "support": support,
                    "omitted_gradients_Mv": omitted,
                    "components": comps,
                    "hessian": M.tolist(),
                }
            if value > POSITIVE_TOL:
                positives.append(
                    {
                        "source": "structured",
                        "base_index": base_points,
                        "value": float(value),
                        "theta": theta.tolist(),
                        "Q": Q.tolist(),
                        "v_unit": v.tolist(),
                        "support": support,
                        "components": comps,
                        "hessian": M.tolist(),
                    }
                )
                break
        if positives:
            break

    if not positives:
        for theta in theta_stream(rng):
            Q = random_orthogonal(rng)
            base_points += 1
            M = theta_hessian(theta, Q, "total")
            value, v, support, n_cand, omitted = max_on_positive_sphere(M)
            candidate_vectors += n_cand
            maybe_update_best(best_total, value, theta, Q, v, M, support, omitted)
            comps = h2_components(theta, v, Q)
            ratio = mechanism_ratio(comps)
            if ratio is not None and ratio > best_ratio["value"]:
                best_ratio = {
                    "value": ratio,
                    "theta": theta.tolist(),
                    "Q": Q.tolist(),
                    "v_unit": v.tolist(),
                    "support": support,
                    "omitted_gradients_Mv": omitted,
                    "components": comps,
                    "hessian": M.tolist(),
                }
            if value > POSITIVE_TOL:
                positives.append(
                    {
                        "source": "random",
                        "base_index": base_points,
                        "value": float(value),
                        "theta": theta.tolist(),
                        "Q": Q.tolist(),
                        "v_unit": v.tolist(),
                        "support": support,
                        "components": comps,
                        "hessian": M.tolist(),
                    }
                )
                break

    return {
        "status": "POSITIVE_FOUND" if positives else "SCOUT_NO_POSITIVE_FOUND",
        "seed": SPHERE_SEED,
        "random_base_points_requested": RANDOM_BASE_POINTS,
        "structured_base_points_requested": len(structured_orthogonals()) * len(structured_thetas),
        "base_points_checked": base_points,
        "candidate_vectors_evaluated": candidate_vectors,
        "support_sets_per_hessian": 7,
        "events_per_direction": 8,
        "directions_per_total_hessian": 6,
        "sphere_constraint": "v_i >= 0, ||v||_2 = 1",
        "best_total_sphere": best_total,
        "best_psi_over_count_barrier": best_ratio,
        "positive_total_candidates": positives[:3],
        "runtime_seconds": time.time() - t0,
    }


def main():
    result = scan()
    out = Path(__file__).with_name("sphere_probe_results.json")
    out.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] == "POSITIVE_FOUND":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
