#!/usr/bin/env python3
"""C1a: distance of exact finite counterexamples to Toeplitz structures."""
from __future__ import annotations

import argparse
import csv
import json
import math
import time
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

from finite_dpp import (
    assert_toeplitz_projection,
    coefficients_from_toeplitz,
    complete_shannon_hessian,
    hermitian_toeplitz_projection,
    lipschitz_symbol_certificate,
    symbol_values,
    toeplitz_from_coefficients,
)


def examples():
    canonical_k = np.array([
        [2719, -3449, 1009, -818, -2490],
        [-3449, 5840, -2889, -1513, 1322],
        [1009, -2889, 2148, 2505, 1101],
        [-818, -1513, 2505, 4698, 3958],
        [-2490, 1322, 1101, 3958, 4596],
    ], dtype=float) / 10000
    canonical_b = np.array([
        [0, -3, -13, -16, 4], [3, 0, -4, 15, 17],
        [13, 4, 0, 6, -15], [16, -15, -6, 0, 1],
        [-4, -17, 15, -1, 0],
    ], dtype=float) / 50

    large5_k = np.array([
        [281472, -264453, 221468, 107027, -263963],
        [-264453, 313361, -297320, -221468, 70061],
        [221468, -297320, 313361, 264453, 70061],
        [107027, -221468, 264453, 281472, 263963],
        [-263963, 70061, 70061, 263963, 813761],
    ], dtype=float) / 1e6
    large5_b = np.array([
        [0, -185, -98, -372, -73], [185, 0, -175, 98, 299],
        [98, 175, 0, 185, -299], [372, -98, -185, 0, -73],
        [73, -299, 299, 73, 0],
    ], dtype=float) / 1e6

    n = 6
    R = np.array([[2 / 3, -1 / 3, 2 / 3], [-1 / 3, 2 / 3, 2 / 3], [2 / 3, 2 / 3, -1 / 3]])
    P = np.zeros((n, n))
    for i in range(3):
        P[i, i] = P[i + 3, i + 3] = 0.5
        for j in range(3):
            P[i, j + 3] = P[i + 3, j] = R[i, j] / 2
    eps = 1 / 475
    large6_k = eps * np.eye(n) + (1 - 2 * eps) * P
    S = np.array([[0, 1, -1], [-1, 0, 1], [1, -1, 0]], dtype=float)
    large6_b = np.zeros((n, n))
    large6_b[:3, :3] = S
    large6_b[3:, 3:] = -S
    return {
        "canonical_n5": (canonical_k, 1j * canonical_b, "randomcat4/icm-conjecture-results@b2645ba: scripts/verify_exact.py"),
        "larger_gap_n5": (large5_k, 1j * large5_b, "randomcat4/icm-conjecture-results@b2645ba: larger_gap/certify_optimized_five.py"),
        "larger_gap_n6": (large6_k, 1j * large6_b, "randomcat4/icm-conjecture-results@b2645ba: larger_gap/certify_symmetric_six.py"),
    }


def unpack_coefficients(x, n):
    c0 = float(x[0])
    coeffs = np.array([x[1 + 2 * k] + 1j * x[2 + 2 * k] for k in range(n - 1)])
    return c0, coeffs


def explicit_symbol_nearest(K, eta=1e-5, optimization_grid=4096, verify_grid=65536):
    n = len(K)
    T = hermitian_toeplitz_projection(K)
    c0, coeffs = coefficients_from_toeplitz(T)
    x0 = [min(max(c0, 0.1), 0.9)]
    for z in coeffs:
        x0.extend((z.real, z.imag))
    x0 = np.array(x0)
    # Contract the nonconstant coefficients until the Lipschitz certificate is feasible.
    for _ in range(80):
        cc0, cc = unpack_coefficients(x0, n)
        cert = lipschitz_symbol_certificate(cc0, cc, optimization_grid)
        if cert["certified_lower"] >= eta and cert["certified_upper"] <= 1 - eta:
            break
        x0[1:] *= 0.92
        x0[0] = 0.5 + 0.92 * (x0[0] - 0.5)

    grid = np.arange(optimization_grid) / optimization_grid

    def objective(x):
        cc0, cc = unpack_coefficients(x, n)
        D = toeplitz_from_coefficients(cc0, cc, n) - K
        return float(np.vdot(D, D).real)

    def legality(x):
        cc0, cc = unpack_coefficients(x, n)
        values = symbol_values(cc0, cc, grid)
        derivative_bound = 4 * math.pi * sum(k * abs(z) for k, z in enumerate(cc, start=1))
        remainder = derivative_bound / (2 * optimization_grid)
        return np.concatenate((values - eta - remainder, 1 - eta - remainder - values))

    result = minimize(
        objective,
        x0,
        method="SLSQP",
        constraints=[{"type": "ineq", "fun": legality}],
        options={"maxiter": 500, "ftol": 1e-13, "disp": False},
    )
    c0, coeffs = unpack_coefficients(result.x, n)
    cert = lipschitz_symbol_certificate(c0, coeffs, verify_grid)
    if cert["certified_lower"] < 0 or cert["certified_upper"] > 1:
        raise ArithmeticError(f"whole-circle certificate failed: {cert}")
    candidate = toeplitz_from_coefficients(c0, coeffs, n)
    return candidate, c0, coeffs, cert, result


def matrix_json(M):
    return [[[float(z.real), float(z.imag)] for z in row] for row in np.asarray(M)]


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        w = csv.DictWriter(handle, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    started = time.time()
    distances, landscape, payload = [], [], {}
    # Resolve the immediate neighborhood of the exact counterexample as well as
    # the full path.  The n=6 center is only about 2e-3 from the spectral wall.
    grid = np.array([0, 1e-4, 5e-4, 1e-3, 2e-3, 5e-3, 1e-2, 2e-2,
                     5e-2, 0.1, 0.2, 0.4, 0.6, 0.8, 1.0], dtype=float)

    for name, (K, A, source) in examples().items():
        KT = hermitian_toeplitz_projection(K)
        AT = hermitian_toeplitz_projection(A)
        assert_toeplitz_projection(K, KT)
        assert_toeplitz_projection(A, AT)
        eigT = np.linalg.eigvalsh(KT)
        base_h = complete_shannon_hessian(K, A)
        distances.append({
            "example": name, "n": len(K),
            "K_distance_fro": float(np.linalg.norm(K - KT)),
            "K_relative_distance": float(np.linalg.norm(K - KT) / np.linalg.norm(K)),
            "A_distance_fro": float(np.linalg.norm(A - AT)),
            "A_relative_distance": float(np.linalg.norm(A - AT) / np.linalg.norm(A)),
            "K_toeplitz_eig_min": float(eigT[0]), "K_toeplitz_eig_max": float(eigT[-1]),
            "K_toeplitz_positive_contraction": bool(eigT[0] >= -1e-12 and eigT[-1] <= 1 + 1e-12),
            "original_hessian": base_h.hessian,
        })
        for s in grid:
            Ks = (1 - s) * K + s * KT
            eigs = np.linalg.eigvalsh(Ks)
            feasible = eigs[0] > 1e-12 and eigs[-1] < 1 - 1e-12
            for r in grid:
                Ar = (1 - r) * A + r * AT
                row = {"example": name, "s": s, "r": r, "eig_min": float(eigs[0]), "eig_max": float(eigs[-1]), "feasible": feasible}
                if feasible and np.linalg.norm(Ar) > 1e-15:
                    h = complete_shannon_hessian(Ks, Ar)
                    row.update({"hessian": h.hessian, "fisher": h.fisher, "acceleration": h.acceleration, "min_event_probability": h.min_probability})
                else:
                    row.update({"hessian": math.nan, "fisher": math.nan, "acceleration": math.nan, "min_event_probability": math.nan})
                landscape.append(row)

        explicit, c0, coeffs, cert, opt = explicit_symbol_nearest(K)
        explicit_eigs = np.linalg.eigvalsh(explicit)
        h_at = complete_shannon_hessian(explicit, AT) if np.linalg.norm(AT) > 1e-15 else None
        h_orig = complete_shannon_hessian(explicit, A)
        payload[name] = {
            "source": source,
            "K": matrix_json(K), "A": matrix_json(A),
            "K_toeplitz": matrix_json(KT), "A_toeplitz": matrix_json(AT),
            "explicit_symbol_candidate": matrix_json(explicit),
            "explicit_symbol": {"c0": c0, "coefficients_re_im": [[float(z.real), float(z.imag)] for z in coeffs]},
            "whole_circle_lipschitz_certificate": cert,
            "optimizer": {"success": bool(opt.success), "status": int(opt.status), "message": str(opt.message), "iterations": int(opt.nit), "objective_squared_fro": float(opt.fun)},
            "explicit_distance_fro": float(np.linalg.norm(explicit - K)),
            "explicit_relative_distance": float(np.linalg.norm(explicit - K) / np.linalg.norm(K)),
            "explicit_eig_min": float(explicit_eigs[0]), "explicit_eig_max": float(explicit_eigs[-1]),
            "hessian_at_explicit_with_original_direction": h_orig.__dict__,
            "hessian_at_explicit_with_toeplitz_direction": h_at.__dict__ if h_at else None,
        }

    write_csv(args.output_dir / "toeplitz_distance.csv", distances)
    write_csv(args.output_dir / "sr_hessian_landscape.csv", landscape)
    record = {
        "source_repository": "randomcat4/icm-conjecture-results",
        "source_commit": "b2645baeff9fdc3b8c767fc621760bf0d57557eb",
        "scope": "Toeplitz linear projection plus nearest candidates inside the selected finite trigonometric-polynomial class; not exact moment-body distance",
        "examples": payload,
        "elapsed_seconds": time.time() - started,
    }
    (args.output_dir / "c1a_results.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"elapsed_seconds": record["elapsed_seconds"], "distance_rows": distances}, indent=2))


if __name__ == "__main__":
    main()
