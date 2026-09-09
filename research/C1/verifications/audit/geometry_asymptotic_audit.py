#!/usr/bin/env python3
"""Finite independent diagnostics for the geometry collar proof.

This script reuses the audit-owned eight-probability reconstruction. The
output is only a consistency check for the displayed asymptotic signs and
ratios; it is not an interval certificate.
"""

from __future__ import annotations

import json
import math
import os
import platform
import sys

import numpy as np

from formula_rebuild_audit import quantities


def coords_from_K(K):
    return np.array([K[0, 0], K[1, 1], K[2, 2], K[0, 1], K[0, 2], K[1, 2]], dtype=float)


def normalized_u():
    u = np.array([math.sqrt(0.2), math.sqrt(0.3), math.sqrt(0.5)], dtype=float)
    return u / np.linalg.norm(u)


def collar_case(lam, tau):
    u = normalized_u()
    K = lam * np.outer(u, u) + tau * np.eye(3)
    return K, 1.0


def affine_case(lam, tau, ratio):
    u = normalized_u()
    S = np.diag([-1.0, 1.0, 1.0])
    v = S @ u
    eps = (1.0 - ratio) * tau
    t = ratio * tau
    A_eps = eps * np.eye(3) + lam * np.outer(u, u)
    K = (1.0 - t) * A_eps + t * S @ (np.eye(3) - A_eps) @ S
    delta = 1.0 - lam * ratio * (1.0 - float(np.dot(u, v) ** 2))
    return K, delta


def record(label, lam, tau, K, delta):
    q = quantities(coords_from_K(K))
    L = math.log(1.0 / tau)
    raw = q["beta"] * math.sqrt(q["Z"])
    return {
        "label": label,
        "tau": tau,
        "L": L,
        "Delta": delta,
        "min_atom": float(np.min(q["p"])),
        "beta": float(q["beta"]),
        "detN_alpha": float(q["detN"] * q["alpha"]),
        "raw_gMh": float(raw),
        "raw_ratio_to_minus_1_over_lambda_L": float(raw / (-1.0 / (lam * L))),
        "beta_ratio_to_section_1": float(q["beta"] / (-tau * math.sqrt(delta) / (math.sqrt(lam) * L))),
        "gap_ratio_to_1_over_lambda_L": float((1.0 - q["detN"] * q["alpha"]) / (1.0 / (lam * L))),
    }


def main():
    lam = 0.7
    rows = []
    for tau in [1e-4, 1e-6, 1e-8]:
        K, delta = collar_case(lam, tau)
        rows.append(record("plain_C_equals_I", lam, tau, K, delta))
    for ratio in [0.0, 0.25, 0.75, 1.0]:
        tau = 1e-6
        K, delta = affine_case(lam, tau, ratio)
        rows.append(record(f"affine_ratio_{ratio}", lam, tau, K, delta))

    pass_checks = [
        all(row["min_atom"] > 0 for row in rows),
        all(row["beta"] < 0 for row in rows),
        all(row["detN_alpha"] < 1 for row in rows),
        rows[2]["raw_ratio_to_minus_1_over_lambda_L"] > rows[0]["raw_ratio_to_minus_1_over_lambda_L"],
        rows[2]["gap_ratio_to_1_over_lambda_L"] > 0.95,
    ]
    result = {
        "status": "PASS" if all(pass_checks) else "FAIL",
        "pid": os.getpid(),
        "exit_status_if_printed": 0 if all(pass_checks) else 1,
        "python": sys.version,
        "python_executable": sys.executable,
        "platform": platform.platform(),
        "numpy": np.__version__,
        "thread_env": {k: os.environ.get(k) for k in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"]},
        "rows": rows,
        "non_coverage": [
            "Finite floating diagnostics only.",
            "No explicit uniform collar radius.",
            "No proof of B0 on its full beta-zero domain.",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return result["exit_status_if_printed"]


if __name__ == "__main__":
    raise SystemExit(main())
