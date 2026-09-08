#!/usr/bin/env python3
"""Bounded numerical optimization probes for P4-03.

Two objectives are available:

* hessian: maximize the largest Hessian eigenvalue at an equicorrelation
  center over allowed eigenvalues (lambda1, lambda2).
* gap: maximize the finite midpoint gap over center, direction, and feasible
  radius fraction.

This is not a certificate.  It is intended only to find candidate
counterexamples or small residual margins worth proving.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")
os.environ.setdefault("MKL_NUM_THREADS", "2")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "2")

import numpy as np
from scipy.optimize import differential_evolution, minimize

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from equicorr_chord_probe import entropy, feasible_radius, spectral_margin
from equicorr_hessian_probe import BASIS6, center_from_lambdas, quadratic_matrix, s3_blocks


def direction_from_coords(z: np.ndarray) -> np.ndarray | None:
    V = sum(float(z[i]) * BASIS6[i] for i in range(6))
    norm = float(max(abs(np.linalg.eigvalsh(V))))
    if not (norm > 1e-14):
        return None
    return V / norm


def hessian_record(lam1: float, lam2: float) -> dict[str, object]:
    a, c, K = center_from_lambdas(lam1, lam2)
    H = quadratic_matrix(K, BASIS6)
    eigvals, eigvecs = np.linalg.eigh(H)
    i = int(np.argmax(eigvals))
    return {
        "lambda1": float(lam1),
        "lambda2": float(lam2),
        "a": float(a),
        "c": float(c),
        "max_hessian_eig": float(eigvals[i]),
        "min_hessian_eig": float(eigvals[0]),
        "eigvals": eigvals.tolist(),
        "max_eigvec_basis6": eigvecs[:, i].tolist(),
        "s3_blocks": s3_blocks(K),
    }


def gap_record(z: np.ndarray, eps: float) -> dict[str, object]:
    lam1 = float(min(max(z[0], eps), 1.0 - eps))
    lam2 = float(min(max(z[1], eps), 1.0 - eps))
    a, c, K = center_from_lambdas(lam1, lam2)
    V = direction_from_coords(z[2:8])
    if V is None:
        return {"ok": False, "gap": -1e100, "reason": "zero direction"}
    radius = feasible_radius(K, V)
    frac = float(min(max(z[8], 0.0), 1.0 - 1e-12))
    t = frac * radius
    Km = K - t * V
    Kp = K + t * V
    gap = 0.5 * (entropy(Km) + entropy(Kp)) - entropy(K)
    return {
        "ok": bool(math.isfinite(gap) and spectral_margin(Km) > 0 and spectral_margin(Kp) > 0),
        "lambda1": lam1,
        "lambda2": lam2,
        "a": float(a),
        "c": float(c),
        "radius": float(radius),
        "fraction": frac,
        "t": float(t),
        "gap": float(gap),
        "endpoint_margin": float(min(spectral_margin(Km), spectral_margin(Kp))),
        "V": V.tolist(),
    }


def run_hessian(args: argparse.Namespace) -> dict[str, object]:
    start = time.time()
    bounds = [(args.eps, 1.0 - args.eps), (args.eps, 1.0 - args.eps)]

    def objective(z: np.ndarray) -> float:
        return -hessian_record(float(z[0]), float(z[1]))["max_hessian_eig"]

    de = differential_evolution(
        objective,
        bounds,
        maxiter=args.maxiter,
        popsize=args.popsize,
        seed=args.seed,
        workers=1,
        updating="immediate",
        polish=False,
        tol=1e-9,
    )
    loc = minimize(objective, de.x, method="Nelder-Mead", options={"maxiter": args.local_iter})
    z = loc.x if loc.fun < de.fun else de.x
    return {
        "status": "OPTIMIZATION_PROBE",
        "mode": "hessian",
        "note": "Numerical maximization only; nonpositive result is not a proof.",
        "seed": args.seed,
        "eps": args.eps,
        "maxiter": args.maxiter,
        "popsize": args.popsize,
        "elapsed_seconds": time.time() - start,
        "differential_evolution": {"fun": float(de.fun), "x": de.x.tolist(), "success": bool(de.success), "message": str(de.message)},
        "local": {"fun": float(loc.fun), "x": loc.x.tolist(), "success": bool(loc.success), "message": str(loc.message)},
        "best": hessian_record(float(z[0]), float(z[1])),
    }


def run_gap(args: argparse.Namespace) -> dict[str, object]:
    start = time.time()
    bounds = [(args.eps, 1.0 - args.eps), (args.eps, 1.0 - args.eps)] + [(-1.0, 1.0)] * 6 + [(args.min_fraction, 1.0 - 1e-10)]

    def objective(z: np.ndarray) -> float:
        if z[8] < args.min_fraction:
            return 1e50 + (args.min_fraction - float(z[8])) * 1e6
        rec = gap_record(z, args.eps)
        gap = rec["gap"]
        if not rec.get("ok", False) or not math.isfinite(gap):
            return 1e50
        return -float(gap)

    de = differential_evolution(
        objective,
        bounds,
        maxiter=args.maxiter,
        popsize=args.popsize,
        seed=args.seed,
        workers=1,
        updating="immediate",
        polish=False,
        tol=1e-8,
    )
    loc = minimize(objective, de.x, method="Nelder-Mead", options={"maxiter": args.local_iter})
    z = loc.x if loc.fun < de.fun else de.x
    return {
        "status": "OPTIMIZATION_PROBE",
        "mode": "gap",
        "note": "Numerical maximization only; positive result needs high-precision/rational certification.",
        "seed": args.seed,
        "eps": args.eps,
        "maxiter": args.maxiter,
        "popsize": args.popsize,
        "min_fraction": args.min_fraction,
        "elapsed_seconds": time.time() - start,
        "differential_evolution": {"fun": float(de.fun), "x": de.x.tolist(), "success": bool(de.success), "message": str(de.message)},
        "local": {"fun": float(loc.fun), "x": loc.x.tolist(), "success": bool(loc.success), "message": str(loc.message)},
        "best": gap_record(z, args.eps),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["hessian", "gap"], required=True)
    ap.add_argument("--seed", type=int, default=20260908)
    ap.add_argument("--eps", type=float, default=1e-7)
    ap.add_argument("--maxiter", type=int, default=80)
    ap.add_argument("--popsize", type=int, default=10)
    ap.add_argument("--local-iter", type=int, default=500)
    ap.add_argument("--min-fraction", type=float, default=0.0)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()
    result = run_hessian(args) if args.mode == "hessian" else run_gap(args)
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
