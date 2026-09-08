#!/usr/bin/env python3
"""Finite probes for the n=3 equicorrelation midpoint Hessian.

This is deliberately a probe, not a proof.  It computes the exact-event
probability Hessian numerically by Mobius inversion of inclusion
determinants, then exploits S3 symmetry diagnostics (trivial and standard
2x2 blocks) at compound-symmetric centers

    K0 = (a-c) I + c 11^T.

Allowed centers are parameterized by eigenvalues

    lambda_1 = a + 2c,   lambda_2 = a - c,

with 0 < lambda_1, lambda_2 < 1.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import random
import sys
import time
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")
os.environ.setdefault("MKL_NUM_THREADS", "2")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "2")

import numpy as np


MASKS = list(range(8))
POLY_TS = np.array([0.0, 1.0, -1.0, 2.0], dtype=float)
VAND = np.vstack([POLY_TS**0, POLY_TS**1, POLY_TS**2, POLY_TS**3]).T
VAND_INV = np.linalg.inv(VAND)


def bits(mask: int) -> list[int]:
    return [i for i in range(3) if (mask >> i) & 1]


def det_sub(K: np.ndarray, mask: int) -> float:
    idx = bits(mask)
    if not idx:
        return 1.0
    return float(np.linalg.det(K[np.ix_(idx, idx)]))


def event_values(K: np.ndarray) -> np.ndarray:
    """Exact event probabilities from inclusion probabilities by Mobius inversion."""
    inc = np.array([det_sub(K, m) for m in MASKS], dtype=float)
    p = np.zeros(8, dtype=float)
    for s in MASKS:
        total = 0.0
        for t in MASKS:
            if (t & s) == s:
                sign = -1.0 if ((t.bit_count() - s.bit_count()) & 1) else 1.0
                total += sign * inc[t]
        p[s] = total
    return p


def entropy_from_events(p: np.ndarray) -> float:
    if np.any(p <= 0.0):
        return float("nan")
    return float(-np.sum(p * np.log(p)))


def entropy(K: np.ndarray) -> float:
    return entropy_from_events(event_values(K))


def event_derivatives(K: np.ndarray, V: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return p(0), p'(0), p''(0) for all exact events.

    Each event probability is a degree <=3 polynomial in the line parameter.
    Coefficients are recovered from four determinant evaluations; feasibility
    away from 0 is not required for this local Hessian calculation.
    """
    pvals = np.zeros((8, 4), dtype=float)
    for j, tt in enumerate(POLY_TS):
        pvals[:, j] = event_values(K + tt * V)
    coeff = pvals @ VAND_INV.T  # columns: constant, linear, quadratic, cubic
    return coeff[:, 0], coeff[:, 1], 2.0 * coeff[:, 2]


def h2(K: np.ndarray, V: np.ndarray) -> float:
    p0, p1, p2 = event_derivatives(K, V)
    if np.any(p0 <= 0.0):
        return float("nan")
    # The '+1' part cancels because sum_S p_S'' = 0.
    return float(-np.sum((p1 * p1) / p0) - np.sum(np.log(p0) * p2))


def basis6() -> list[np.ndarray]:
    out: list[np.ndarray] = []
    for i in range(3):
        M = np.zeros((3, 3), dtype=float)
        M[i, i] = 1.0
        out.append(M)
    for i, j in [(0, 1), (0, 2), (1, 2)]:
        M = np.zeros((3, 3), dtype=float)
        M[i, j] = M[j, i] = 1.0
        out.append(M)
    return out


BASIS6 = basis6()


def quadratic_matrix(K: np.ndarray, basis: list[np.ndarray]) -> np.ndarray:
    n = len(basis)
    Q = np.zeros((n, n), dtype=float)
    diag = [h2(K, B) for B in basis]
    for i in range(n):
        Q[i, i] = diag[i]
    for i in range(n):
        for j in range(i + 1, n):
            hij = 0.5 * (h2(K, basis[i] + basis[j]) - diag[i] - diag[j])
            Q[i, j] = Q[j, i] = hij
    return 0.5 * (Q + Q.T)


def center_from_lambdas(lam1: float, lam2: float) -> tuple[float, float, np.ndarray]:
    a = (lam1 + 2.0 * lam2) / 3.0
    c = (lam1 - lam2) / 3.0
    K = (a - c) * np.eye(3) + c * np.ones((3, 3), dtype=float)
    return a, c, K


def spectral_margin(K: np.ndarray) -> float:
    ev = np.linalg.eigvalsh(K)
    return float(min(np.min(ev), np.min(1.0 - ev)))


def s3_blocks(K: np.ndarray) -> dict[str, object]:
    T_diag = np.eye(3)
    T_off = np.ones((3, 3), dtype=float) - np.eye(3)
    x = np.array([1.0, -1.0, 0.0])
    S_diag = np.diag(x)
    S_off = np.zeros((3, 3), dtype=float)
    # Edge standard copy: edge ij carries x_i + x_j = -x_k on sum-zero x.
    for i, j in [(0, 1), (0, 2), (1, 2)]:
        S_off[i, j] = S_off[j, i] = x[i] + x[j]

    def mat_block(bs: list[np.ndarray]) -> np.ndarray:
        return quadratic_matrix(K, bs)

    Bt = mat_block([T_diag, T_off])
    Bs = mat_block([S_diag, S_off])
    return {
        "trivial_block": Bt.tolist(),
        "standard_probe_block": Bs.tolist(),
        "trivial_eig": np.linalg.eigvalsh(Bt).tolist(),
        "standard_probe_eig": np.linalg.eigvalsh(Bs).tolist(),
        "standard_basis_x": x.tolist(),
    }


def try_chord(K: np.ndarray, eigvec: np.ndarray) -> dict[str, object]:
    V = sum(float(eigvec[i]) * BASIS6[i] for i in range(6))
    norm = float(max(abs(np.linalg.eigvalsh(V))))
    margin = spectral_margin(K)
    if not (norm > 0 and margin > 0):
        return {"ok": False, "reason": "zero norm or nonstrict center"}
    best: dict[str, object] | None = None
    for factor in [1e-1, 5e-2, 2e-2, 1e-2, 5e-3, 2e-3, 1e-3]:
        t = factor * margin / norm
        Km = K - t * V
        Kp = K + t * V
        gap = 0.5 * (entropy(Km) + entropy(Kp)) - entropy(K)
        min_margin = min(spectral_margin(Km), spectral_margin(Kp))
        rec = {
            "ok": bool(min_margin > 0.0 and math.isfinite(gap)),
            "factor": factor,
            "t": t,
            "gap": gap,
            "endpoint_spectral_margin": min_margin,
            "direction_matrix": V.tolist(),
        }
        if best is None or (math.isfinite(gap) and gap > float(best.get("gap", -1e300))):
            best = rec
        if min_margin > 0 and gap > 0:
            rec["ok"] = True
            return rec
    assert best is not None
    best["ok"] = False
    best.setdefault("reason", "no positive finite small chord gap")
    return best


def scan(args: argparse.Namespace) -> dict[str, object]:
    rng = random.Random(args.seed)
    start = time.time()
    best: dict[str, object] | None = None
    positives: list[dict[str, object]] = []
    checked = 0

    centers: list[tuple[float, float, str]] = []
    if args.grid > 1:
        for i in range(args.grid):
            for j in range(args.grid):
                lam1 = args.eps + (1.0 - 2.0 * args.eps) * (i + 0.5) / args.grid
                lam2 = args.eps + (1.0 - 2.0 * args.eps) * (j + 0.5) / args.grid
                centers.append((lam1, lam2, "grid"))
    for _ in range(args.samples):
        # Mixture: uniform interior plus log-near-boundary draws.
        if rng.random() < 0.35:
            def near() -> float:
                z = 10.0 ** rng.uniform(math.log10(args.eps), math.log10(0.5))
                return z if rng.random() < 0.5 else 1.0 - z
            lam1, lam2 = near(), near()
        else:
            lam1 = args.eps + (1.0 - 2.0 * args.eps) * rng.random()
            lam2 = args.eps + (1.0 - 2.0 * args.eps) * rng.random()
        centers.append((lam1, lam2, "random"))

    for lam1, lam2, source in centers:
        checked += 1
        a, c, K = center_from_lambdas(lam1, lam2)
        H = quadratic_matrix(K, BASIS6)
        eigvals, eigvecs = np.linalg.eigh(H)
        max_i = int(np.argmax(eigvals))
        rec = {
            "source": source,
            "lambda1": lam1,
            "lambda2": lam2,
            "a": a,
            "c": c,
            "max_hessian_eig": float(eigvals[max_i]),
            "min_hessian_eig": float(eigvals[0]),
            "eigvals": eigvals.tolist(),
            "max_eigvec_basis6": eigvecs[:, max_i].tolist(),
            "s3_blocks": s3_blocks(K),
        }
        if best is None or rec["max_hessian_eig"] > best["max_hessian_eig"]:
            best = rec
        if rec["max_hessian_eig"] > args.positive_tol:
            rec["local_chord_probe"] = try_chord(K, eigvecs[:, max_i])
            positives.append(rec)
            if args.stop_on_positive and rec["local_chord_probe"].get("gap", 0.0) > 0:
                break
        if checked >= args.max_centers:
            break

    return {
        "status": "FINITE_PROBE",
        "note": "Numerical scan only; not a proof or disproof without a certified strict chord.",
        "seed": args.seed,
        "eps": args.eps,
        "grid": args.grid,
        "samples_requested": args.samples,
        "centers_checked": checked,
        "elapsed_seconds": time.time() - start,
        "positive_tol": args.positive_tol,
        "best": best,
        "positive_count": len(positives),
        "positives": positives[: args.keep_positives],
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=20260908)
    ap.add_argument("--samples", type=int, default=5000)
    ap.add_argument("--grid", type=int, default=31)
    ap.add_argument("--eps", type=float, default=1e-5)
    ap.add_argument("--max-centers", type=int, default=200000)
    ap.add_argument("--positive-tol", type=float, default=1e-8)
    ap.add_argument("--keep-positives", type=int, default=20)
    ap.add_argument("--stop-on-positive", action="store_true")
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args(argv)

    result = scan(args)
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
