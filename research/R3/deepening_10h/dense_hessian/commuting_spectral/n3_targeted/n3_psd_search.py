#!/usr/bin/env python3
"""D10-M5: targeted n=3 fixed-eigenvector PSD spectral-rate search.

The implementation uses the n=3 spectral-channel formula directly:

  p0 = prod_i (1-theta_i)
  singleton layer = P r,  r_i = theta_i prod_{j!=i}(1-theta_j)
  pair layer      = P s,  s_i = (1-theta_i) prod_{j!=i} theta_j
  p3 = prod_i theta_i

where P[a,i] = q_{a,i}^2.  This avoids any use of neighbouring dense-Hessian
code and keeps the singleton/pair conditional curvature visible.
"""

from __future__ import annotations

import json
import math
import os
import time
from pathlib import Path

for _var in (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
):
    os.environ.setdefault(_var, "1")

import numpy as np


SEED = 2026090835
OUT = Path(__file__).with_name("n3_search_results.json")


def eta_h2(p: np.ndarray, p1: np.ndarray, p2: np.ndarray) -> float:
    return float(np.sum(-(p1 * p1) / p - p2 * np.log(p)))


def monomial(theta: np.ndarray, v: np.ndarray, included: tuple[int, ...]) -> tuple[float, float, float]:
    inc = set(included)
    p = 1.0
    scores = []
    for i in range(3):
        if i in inc:
            p *= theta[i]
            scores.append(v[i] / theta[i])
        else:
            p *= 1.0 - theta[i]
            scores.append(-v[i] / (1.0 - theta[i]))
    s1 = sum(scores)
    s2 = s1 * s1 - sum(x * x for x in scores)
    return p, p * s1, p * s2


def distribution_derivatives(theta: np.ndarray, v: np.ndarray, Q: np.ndarray) -> dict:
    P = Q * Q

    p0, p0_1, p0_2 = monomial(theta, v, ())
    p3, p3_1, p3_2 = monomial(theta, v, (0, 1, 2))

    r = np.zeros(3)
    r1 = np.zeros(3)
    r2 = np.zeros(3)
    s = np.zeros(3)
    s1 = np.zeros(3)
    s2 = np.zeros(3)
    for i in range(3):
        r[i], r1[i], r2[i] = monomial(theta, v, (i,))
        s[i], s1[i], s2[i] = monomial(theta, v, tuple(j for j in range(3) if j != i))

    u = P @ r
    u1 = P @ r1
    u2 = P @ r2
    w = P @ s
    w1 = P @ s1
    w2 = P @ s2

    p = np.concatenate(([p0], u, w, [p3]))
    p1 = np.concatenate(([p0_1], u1, w1, [p3_1]))
    p2 = np.concatenate(([p0_2], u2, w2, [p3_2]))

    count_p = np.array([p0, np.sum(r), np.sum(s), p3], dtype=float)
    count_p1 = np.array([p0_1, np.sum(r1), np.sum(s1), p3_1], dtype=float)
    count_p2 = np.array([p0_2, np.sum(r2), np.sum(s2), p3_2], dtype=float)

    H2 = eta_h2(p, p1, p2)
    HN2 = eta_h2(count_p, count_p1, count_p2)
    singleton_cond_h2 = eta_h2(u, u1, u2) - eta_h2(np.array([np.sum(r)]), np.array([np.sum(r1)]), np.array([np.sum(r2)]))
    pair_cond_h2 = eta_h2(w, w1, w2) - eta_h2(np.array([np.sum(s)]), np.array([np.sum(s1)]), np.array([np.sum(s2)]))
    psi2 = H2 - HN2

    fisher = float(np.sum((p1 * p1) / p))
    accel = float(np.sum(-p2 * np.log(p)))
    return {
        "p": p,
        "p1": p1,
        "p2": p2,
        "count_p": count_p,
        "count_p1": count_p1,
        "count_p2": count_p2,
        "P": P,
        "r": r,
        "r1": r1,
        "r2": r2,
        "s": s,
        "s1": s1,
        "s2": s2,
        "H2": H2,
        "count_H2": HN2,
        "psi_H2": psi2,
        "singleton_cond_H2": singleton_cond_h2,
        "pair_cond_H2": pair_cond_h2,
        "fisher_positive": fisher,
        "acceleration": accel,
        "rho": accel / fisher if fisher > 0 else None,
        "min_atom": float(np.min(p)),
        "sum_p_minus_one": float(np.sum(p) - 1.0),
        "sum_p1": float(np.sum(p1)),
        "sum_p2": float(np.sum(p2)),
    }


def entropy_from_theta(theta: np.ndarray, Q: np.ndarray) -> float:
    zero_v = np.zeros(3)
    d = distribution_derivatives(theta, zero_v, Q)
    p = d["p"]
    return float(-np.dot(p, np.log(p)))


def random_orthogonal(rng: np.random.Generator) -> np.ndarray:
    Q, R = np.linalg.qr(rng.normal(size=(3, 3)))
    signs = np.sign(np.diag(R))
    signs[signs == 0.0] = 1.0
    return Q * signs


def rotation_from_vector(a: np.ndarray) -> np.ndarray:
    angle = float(np.linalg.norm(a))
    if angle < 1e-15:
        return np.eye(3)
    x, y, z = a / angle
    A = np.array([[0.0, -z, y], [z, 0.0, -x], [-y, x, 0.0]])
    return np.eye(3) + math.sin(angle) * A + (1.0 - math.cos(angle)) * (A @ A)


def sample_theta(rng: np.random.Generator, mode: int) -> np.ndarray:
    if mode == 0:
        return rng.uniform(0.02, 0.98, size=3)
    if mode == 1:
        return np.clip(rng.beta(0.25, 0.25, size=3), 1e-4, 1.0 - 1e-4)
    if mode == 2:
        x = np.array([rng.uniform(1e-4, 0.05), rng.uniform(0.15, 0.85), rng.uniform(0.95, 0.9999)])
        rng.shuffle(x)
        return x
    return np.clip(rng.beta(0.6, 0.6, size=3), 1e-3, 1.0 - 1e-3)


def sample_v(rng: np.random.Generator, mode: int) -> np.ndarray:
    if mode == 0:
        v = rng.exponential(scale=1.0, size=3)
    elif mode == 1:
        v = np.exp(rng.uniform(-6.0, 0.0, size=3))
    elif mode == 2:
        v = np.zeros(3)
        active = rng.choice(3, size=int(rng.integers(1, 4)), replace=False)
        v[active] = rng.exponential(scale=1.0, size=len(active))
    else:
        v = rng.uniform(0.05, 1.0, size=3)
    return v / max(float(np.linalg.norm(v)), 1e-300)


def compact_record(theta: np.ndarray, v: np.ndarray, Q: np.ndarray, d: dict, label: str) -> dict:
    K = Q @ np.diag(theta) @ Q.T
    D = Q @ np.diag(v) @ Q.T
    eigK = np.linalg.eigvalsh((K + K.T) / 2.0)
    eigD = np.linalg.eigvalsh((D + D.T) / 2.0)
    return {
        "label": label,
        "theta": theta.tolist(),
        "v": v.tolist(),
        "Q": Q.tolist(),
        "P_squared_channel": d["P"].tolist(),
        "H2": d["H2"],
        "rho": d["rho"],
        "fisher_positive": d["fisher_positive"],
        "acceleration": d["acceleration"],
        "count_H2": d["count_H2"],
        "psi_H2": d["psi_H2"],
        "singleton_cond_H2": d["singleton_cond_H2"],
        "pair_cond_H2": d["pair_cond_H2"],
        "min_atom": d["min_atom"],
        "sum_p_minus_one": d["sum_p_minus_one"],
        "sum_p1": d["sum_p1"],
        "sum_p2": d["sum_p2"],
        "p": d["p"].tolist(),
        "p1": d["p1"].tolist(),
        "p2": d["p2"].tolist(),
        "singleton_raw_r2": d["r2"].tolist(),
        "pair_raw_s2": d["s2"].tolist(),
        "kernel_eigen_min": float(eigK[0]),
        "kernel_eigen_max": float(eigK[-1]),
        "I_minus_kernel_eigen_min": float(1.0 - eigK[-1]),
        "direction_eigen_min": float(eigD[0]),
        "direction_eigen_max": float(eigD[-1]),
    }


def chord_gate(theta: np.ndarray, v: np.ndarray, Q: np.ndarray) -> dict:
    positive = v > 1e-15
    if np.any(positive):
        max_step = float(np.min(np.minimum(theta[positive] / v[positive], (1.0 - theta[positive]) / v[positive])))
    else:
        max_step = 1.0
    h = min(1e-4, 0.2 * max_step)
    H0 = entropy_from_theta(theta, Q)
    Hp = entropy_from_theta(theta + h * v, Q)
    Hm = entropy_from_theta(theta - h * v, Q)
    return {
        "h": h,
        "max_symmetric_spectral_step": max_step,
        "theta_plus_min": float(np.min(theta + h * v)),
        "one_minus_theta_plus_min": float(np.min(1.0 - theta - h * v)),
        "theta_minus_min": float(np.min(theta - h * v)),
        "one_minus_theta_minus_min": float(np.min(1.0 - theta + h * v)),
        "H0": H0,
        "H_plus": Hp,
        "H_minus": Hm,
        "midpoint_gap": float((Hp + Hm) / 2.0 - H0),
        "central_second_difference": float((Hp + Hm - 2.0 * H0) / (h * h)),
    }


def singleton_positive_blocker_example() -> dict:
    theta = np.array([3 / 5, 1 / 5, 1 / 5], dtype=float)
    v = np.array([1 / 100, 1 / 10, 1 / 10], dtype=float)
    Q = np.eye(3)
    d = distribution_derivatives(theta, v, Q)
    return {
        "theta": theta.tolist(),
        "v": v.tolist(),
        "r2_singleton_raw": d["r2"].tolist(),
        "positive_indices": [int(i) for i, x in enumerate(d["r2"]) if x > 0],
        "note": "raw singleton-layer weights r_i can have positive second derivative even when all v_i>=0",
    }


def main() -> int:
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    best = None
    best_psi = None
    best_singleton_cond = None
    best_pair_cond = None
    positives = []
    random_draws = 180_000
    random_completed = 0

    def update_extrema(theta: np.ndarray, v: np.ndarray, Q: np.ndarray, d: dict, label: str) -> None:
        nonlocal best, best_psi, best_singleton_cond, best_pair_cond
        if best is None or d["H2"] > best["H2"]:
            best = compact_record(theta, v, Q, d, label)
        if best_psi is None or d["psi_H2"] > best_psi["psi_H2"]:
            best_psi = compact_record(theta, v, Q, d, label)
        if best_singleton_cond is None or d["singleton_cond_H2"] > best_singleton_cond["singleton_cond_H2"]:
            best_singleton_cond = compact_record(theta, v, Q, d, label)
        if best_pair_cond is None or d["pair_cond_H2"] > best_pair_cond["pair_cond_H2"]:
            best_pair_cond = compact_record(theta, v, Q, d, label)

    for j in range(random_draws):
        random_completed = j + 1
        theta = sample_theta(rng, j % 4)
        v = sample_v(rng, (j // 4) % 4)
        Q = random_orthogonal(rng)
        d = distribution_derivatives(theta, v, Q)
        update_extrema(theta, v, Q, d, f"random_{j}")
        if d["H2"] > 1e-10:
            positives.append(compact_record(theta, v, Q, d, f"random_positive_{j}"))
            break

    assert best is not None and best_psi is not None and best_singleton_cond is not None and best_pair_cond is not None

    # Local maximization around the best random draw.  This is a scout only.
    theta = np.array(best["theta"], dtype=float)
    v = np.array(best["v"], dtype=float)
    Q = np.array(best["Q"], dtype=float)
    current = best
    accepted = 0
    local_steps = 22_000
    local_completed = 0
    temp = 0.01
    step_theta = 0.18
    step_v = 0.20
    step_rot = 0.18
    logit = lambda x: np.log(x / (1.0 - x))
    sigmoid = lambda x: 1.0 / (1.0 + np.exp(-x))
    theta_logits = logit(theta)
    v_logs = np.log(np.maximum(v, 1e-12))
    for j in range(local_steps):
        local_completed = j + 1
        cand_logits = theta_logits + step_theta * rng.normal(size=3)
        cand_theta = np.clip(sigmoid(cand_logits), 1e-6, 1.0 - 1e-6)
        cand_v_logs = v_logs + step_v * rng.normal(size=3)
        cand_v = np.exp(cand_v_logs)
        cand_v /= max(float(np.linalg.norm(cand_v)), 1e-300)
        cand_Q = rotation_from_vector(step_rot * rng.normal(size=3)) @ Q
        d = distribution_derivatives(cand_theta, cand_v, cand_Q)
        update_extrema(cand_theta, cand_v, cand_Q, d, f"local_probe_{j}")
        if d["H2"] > current["H2"] or rng.random() < math.exp(min(0.0, (d["H2"] - current["H2"]) / temp)):
            theta_logits = cand_logits
            v_logs = cand_v_logs
            Q = cand_Q
            current = compact_record(cand_theta, cand_v, cand_Q, d, f"local_{j}")
            accepted += 1
            if current["H2"] > best["H2"]:
                best = current
        if d["H2"] > 1e-10:
            positives.append(compact_record(cand_theta, cand_v, cand_Q, d, f"local_positive_{j}"))
            break
        step_theta *= 0.99992
        step_v *= 0.99992
        step_rot *= 0.99992
        temp *= 0.9999

    best["strict_spectral_chord_gate"] = chord_gate(np.array(best["theta"]), np.array(best["v"]), np.array(best["Q"]))
    best_psi["strict_spectral_chord_gate"] = chord_gate(np.array(best_psi["theta"]), np.array(best_psi["v"]), np.array(best_psi["Q"]))

    result = {
        "status": "POSITIVE_CANDIDATE_FOUND" if positives else "SCOUT_NO_POSITIVE_FOUND",
        "seed": SEED,
        "random_draws_requested": random_draws,
        "random_draws_completed": random_completed,
        "local_steps_requested": local_steps,
        "local_steps_completed": local_completed,
        "local_accepted": accepted,
        "best": best,
        "best_psi_H2": best_psi,
        "best_singleton_cond_H2": best_singleton_cond,
        "best_pair_cond_H2": best_pair_cond,
        "positive_candidates": positives[:3],
        "singleton_positive_blocker_example": singleton_positive_blocker_example(),
        "elapsed_seconds": time.time() - t0,
        "notes": [
            "All searched directions have v_i>=0 and ||v||_2=1, so D=Q diag(v) Q^T is PSD.",
            "Finite nonhits are scouts only.  A positive candidate would require a separate high-precision chord certificate.",
        ],
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "best_H2": best["H2"],
        "best_rho": best["rho"],
        "best_count_H2": best["count_H2"],
        "best_psi_H2": best["psi_H2"],
        "max_seen_psi_H2": best_psi["psi_H2"],
        "max_seen_singleton_cond_H2": best_singleton_cond["singleton_cond_H2"],
        "max_seen_pair_cond_H2": best_pair_cond["pair_cond_H2"],
        "positives": len(positives),
        "output": str(OUT),
        "elapsed_seconds": result["elapsed_seconds"],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
