#!/usr/bin/env python3
"""C2 search in intrinsic finite-symbol Toeplitz coordinates for n=5,6."""
from __future__ import annotations

import argparse
import json
import math
import platform
import time
from pathlib import Path

import numpy as np
from scipy.optimize import differential_evolution

from finite_dpp import complete_event_jets, complete_shannon_hessian, lipschitz_symbol_certificate, toeplitz_from_coefficients


def decode(x: np.ndarray, n: int, symmetry: bool, eta: float = 0.02):
    d = n - 1
    cursor = 0
    c0 = float(x[cursor]); cursor += 1
    rho = float(x[cursor]); cursor += 1
    if symmetry:
        raw_c = x[cursor:cursor + d].astype(complex); cursor += d
    else:
        raw_c = x[cursor:cursor + 2 * d:2] + 1j * x[cursor + 1:cursor + 2 * d:2]; cursor += 2 * d
    mass = max(float(np.sum(np.abs(raw_c))), 1e-15)
    amplitude = 0.98 * rho * min(c0 - eta, 1 - eta - c0)
    c = raw_c * amplitude / (2 * mass)

    if symmetry:
        raw_d = 1j * x[cursor:cursor + d]
        d0 = 0.0
    else:
        d0 = float(x[cursor]); cursor += 1
        raw_d = x[cursor:cursor + 2 * d:2] + 1j * x[cursor + 1:cursor + 2 * d:2]
    G0 = toeplitz_from_coefficients(d0, raw_d, n)
    norm = np.linalg.norm(G0)
    if norm < 1e-13:
        raw_d = np.zeros(d, dtype=complex); raw_d[0] = 1j if symmetry else 1.0
        d0 = 0.0
        G0 = toeplitz_from_coefficients(d0, raw_d, n)
        norm = np.linalg.norm(G0)
    dcoeff = raw_d / norm
    d0 /= norm
    K = toeplitz_from_coefficients(c0, c, n)
    G = toeplitz_from_coefficients(d0, dcoeff, n)
    return K, G, c0, c, d0, dcoeff


def bounds(n: int, symmetry: bool, rho_min: float):
    d = n - 1
    b = [(0.08, 0.92), (rho_min, 1.0)]
    b += [(-1.0, 1.0)] * (d if symmetry else 2 * d)
    b += [(-1.0, 1.0)] * (d if symmetry else 1 + 2 * d)
    return b


def objective(x, n, symmetry):
    try:
        K, G, *_ = decode(x, n, symmetry)
        return -complete_shannon_hessian(K, G).hessian
    except (ArithmeticError, np.linalg.LinAlgError, FloatingPointError):
        return 1e6


def serialize_complex(values):
    return [[float(z.real), float(z.imag)] for z in values]


def run_case(n: int, symmetry: bool, seed: int, maxiter: int, popsize: int, rho_min: float):
    tick = time.time()
    result = differential_evolution(
        objective,
        bounds(n, symmetry, rho_min),
        args=(n, symmetry),
        seed=seed,
        maxiter=maxiter,
        popsize=popsize,
        tol=1e-9,
        atol=1e-11,
        polish=True,
        updating="immediate",
        workers=1,
    )
    K, G, c0, c, d0, dcoeff = decode(result.x, n, symmetry)
    h = complete_shannon_hessian(K, G)
    jets, imag = complete_event_jets(K, G)
    base_cert = lipschitz_symbol_certificate(c0, c)
    direction_cert = lipschitz_symbol_certificate(d0, dcoeff)
    sup_g = max(abs(direction_cert["certified_lower"]), abs(direction_cert["certified_upper"]))
    base_slack = min(base_cert["certified_lower"], 1 - base_cert["certified_upper"])
    chord_radius = base_slack / sup_g if sup_g else math.inf
    positive_candidate = h.hessian > 1e-10
    return {
        "n": n,
        "class": "even_f_odd_g" if symmetry else "general_complex_toeplitz",
        "parameter_dimension": len(result.x),
        "seed": seed,
        "maxiter": maxiter,
        "population_multiplier": popsize,
        "base_fourier_amplitude_fraction_lower_bound": rho_min,
        "initial_population_size": popsize * len(result.x),
        "objective_evaluations": int(result.nfev),
        "optimizer_success": bool(result.success),
        "optimizer_message": str(result.message),
        "maximum_hessian": h.hessian,
        "fisher": h.fisher,
        "acceleration": h.acceleration,
        "direction_frobenius_norm": float(np.linalg.norm(G)),
        "max_complete_event_first_jet": max(abs(row[1]) for row in jets),
        "min_event_probability": h.min_probability,
        "max_imaginary_jet_residual": imag,
        "base_symbol": {"c0": c0, "coefficients_re_im": serialize_complex(c)},
        "direction_symbol": {"d0": d0, "coefficients_re_im": serialize_complex(dcoeff)},
        "base_whole_circle_certificate": base_cert,
        "direction_bound_certificate": direction_cert,
        "certified_local_chord_radius_from_bounds": chord_radius,
        "positive_candidate": positive_candidate,
        "high_precision_recomputed": False,
        "directed_interval_certified": False,
        "classification": "CANDIDATE_REQUIRES_HIGH_PRECISION_AND_DIRECTED_INTERVAL" if positive_candidate else "NO_POSITIVE_HIT_IN_RECORDED_SEARCH",
        "elapsed_seconds": time.time() - tick,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--maxiter", type=int, default=45)
    parser.add_argument("--popsize", type=int, default=12)
    parser.add_argument("--rho-min", type=float, default=0.25)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    started = time.time()
    cases = []
    for n in (5, 6):
        for symmetry in (True, False):
            seed = 2026091200 + 10 * n + int(not symmetry)
            case = run_case(n, symmetry, seed, args.maxiter, args.popsize, args.rho_min)
            cases.append(case)
            print(n, case["class"], case["maximum_hessian"], case["objective_evaluations"], flush=True)
    record = {
        "method": "SciPy differential_evolution in intrinsic finite Fourier coordinates; all 2^n event determinant jets retained",
        "legality": "base symbols satisfy a global l1 Fourier-amplitude condition and are independently checked by a 65536-grid Lipschitz remainder; a positive local chord radius is reported",
        "direction_normalization": "Frobenius norm of T_n(g) equals one",
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": __import__("scipy").__version__,
        "cases": cases,
        "total_objective_evaluations": sum(c["objective_evaluations"] for c in cases),
        "positive_hits": sum(c["positive_candidate"] for c in cases),
        "certified_hits": sum(c["directed_interval_certified"] for c in cases),
        "elapsed_seconds": time.time() - started,
        "scope": "finite n=5,6 search only; NO_HIT is not a Toeplitz concavity theorem",
    }
    args.output.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: record[k] for k in ("total_objective_evaluations", "positive_hits", "certified_hits", "elapsed_seconds")}, indent=2))


if __name__ == "__main__":
    main()
