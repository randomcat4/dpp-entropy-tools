#!/usr/bin/env python3
"""Non-smooth stationary-DPP entropy-increment curvature probe.

This program studies fixed scalar symbols on T=R/Z.  It computes exact
finite-block directional jets (up to floating-point roundoff) of the one-site
Toeplitz entropy increments

    R_n(f) = H(P_f restricted to {0,...,n-1})
             - H(P_f restricted to {0,...,n-2}).

The core recursion conditions the finite DPP one site at a time and propagates
K, dK, d^2K, prefix mass, and its first two derivatives.  No finite-difference
step is used in the main Hessian calculation.

Families included here:
  * two/three/four-interval near-projection chords;
  * reflection-generated endpoint perturbations (even midpoint, odd direction);
  * piecewise-linear trapezoidal boundary layers;
  * fixed-total-measure families with one through eight intervals.

The output is exploratory numerical evidence.  It does not certify the
n->infinity entropy-rate tail for jump symbols.
"""
from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path
from typing import Any, Iterable

import numpy as np
from numba import njit

SEED = 2026090701
DEFAULT_EPSILONS = (0.2, 0.1, 0.05, 0.02, 0.01, 0.005, 0.002)


# ---------------------------------------------------------------------------
# Conditional DPP jet recursion
# ---------------------------------------------------------------------------

@njit
def _dfs_jet(
    K0: np.ndarray,
    K1: np.ndarray,
    K2: np.ndarray,
    depth: int,
    weight: float,
    weight1: float,
    weight2: float,
    R: np.ndarray,
    R1: np.ndarray,
    R2: np.ndarray,
    fisher: np.ndarray,
    transport: np.ndarray,
    stats: np.ndarray,
) -> None:
    """Enumerate all prefix histories and accumulate conditional-entropy jets."""
    m = K0.shape[0]
    p = K0[0, 0].real
    p1 = K1[0, 0].real
    p2 = K2[0, 0].real

    if p < stats[0]:
        stats[0] = p
    if p > stats[1]:
        stats[1] = p
    stats[2] += 1.0
    if p <= 0.0 or p >= 1.0 or not np.isfinite(p):
        stats[3] += 1.0
        return

    h = -p * np.log(p) - (1.0 - p) * np.log(1.0 - p)
    hp = np.log((1.0 - p) / p)
    hpp = -1.0 / (p * (1.0 - p))

    R[depth] += weight * h
    R1[depth] += weight1 * h + weight * hp * p1

    fterm = weight * hpp * p1 * p1
    pterm = weight2 * h + 2.0 * weight1 * hp * p1 + weight * hp * p2
    fisher[depth] += fterm
    transport[depth] += pterm
    R2[depth] += fterm + pterm

    if m == 1:
        return

    A0 = K0[1:, 1:].copy()
    A1 = K1[1:, 1:].copy()
    A2 = K2[1:, 1:].copy()
    v0 = K0[1:, 0].copy()
    v1 = K1[1:, 0].copy()
    v2 = K2[1:, 0].copy()

    B0 = np.outer(v0, np.conj(v0))
    B1 = np.outer(v1, np.conj(v0)) + np.outer(v0, np.conj(v1))
    B2 = (
        np.outer(v2, np.conj(v0))
        + 2.0 * np.outer(v1, np.conj(v1))
        + np.outer(v0, np.conj(v2))
    )

    # Condition current site to be 0.
    den = 1.0 - p
    q = 1.0 / den
    q1 = p1 / (den * den)
    q2 = p2 / (den * den) + 2.0 * p1 * p1 / (den * den * den)
    C0 = A0 + B0 * q
    C1 = A1 + B1 * q + B0 * q1
    C2 = A2 + B2 * q + 2.0 * B1 * q1 + B0 * q2
    wc = weight * den
    wc1 = weight1 * den - weight * p1
    wc2 = weight2 * den - 2.0 * weight1 * p1 - weight * p2
    _dfs_jet(C0, C1, C2, depth + 1, wc, wc1, wc2,
             R, R1, R2, fisher, transport, stats)

    # Condition current site to be 1.
    q = 1.0 / p
    q1 = -p1 / (p * p)
    q2 = 2.0 * p1 * p1 / (p * p * p) - p2 / (p * p)
    C0 = A0 - B0 * q
    C1 = A1 - B1 * q - B0 * q1
    C2 = A2 - B2 * q - 2.0 * B1 * q1 - B0 * q2
    wc = weight * p
    wc1 = weight1 * p + weight * p1
    wc2 = weight2 * p + 2.0 * weight1 * p1 + weight * p2
    _dfs_jet(C0, C1, C2, depth + 1, wc, wc1, wc2,
             R, R1, R2, fisher, transport, stats)


@njit
def conditional_increment_jets(K0: np.ndarray, K1: np.ndarray):
    """Return R_n, R_n', R_n'', Fisher, remainder, and probability stats."""
    n = K0.shape[0]
    K2 = np.zeros_like(K0)
    R = np.zeros(n)
    R1 = np.zeros(n)
    R2 = np.zeros(n)
    fisher = np.zeros(n)
    transport = np.zeros(n)
    # min p, max p, number of nodes, invalid nodes
    stats = np.array([1.0, 0.0, 0.0, 0.0])
    _dfs_jet(K0, K1, K2, 0, 1.0, 0.0, 0.0,
             R, R1, R2, fisher, transport, stats)
    return R, R1, R2, fisher, transport, stats


# ---------------------------------------------------------------------------
# Fourier and Toeplitz helpers
# ---------------------------------------------------------------------------

def toeplitz_from_lags(lags: dict[int, complex], n: int) -> np.ndarray:
    return np.array(
        [[lags[i - j] for j in range(n)] for i in range(n)],
        dtype=np.complex128,
    )


def union_interval_lags(
    centers: Iterable[float], halfwidths: Iterable[float], n: int
) -> dict[int, complex]:
    centers = np.asarray(tuple(centers), dtype=float)
    halfwidths = np.asarray(tuple(halfwidths), dtype=float)
    out: dict[int, complex] = {}
    for k in range(-(n - 1), n):
        if k == 0:
            value = float(np.sum(2.0 * halfwidths))
        else:
            value = np.sum(
                np.exp(-2j * np.pi * k * centers)
                * np.sin(2.0 * np.pi * k * halfwidths)
                / (np.pi * k)
            )
        out[k] = complex(value)
    return out


def trapezoid_hat(
    k: int, center: float, plateau_halfwidth: float, ramp_width: float
) -> complex:
    """Fourier coefficient of a unit-height symmetric trapezoidal band."""
    if k == 0:
        value = 2.0 * plateau_halfwidth + ramp_width
    else:
        a = 2.0 * plateau_halfwidth + ramp_width
        value = (
            np.sin(np.pi * k * a) / (np.pi * k)
            * np.sin(np.pi * k * ramp_width) / (np.pi * k * ramp_width)
        )
    return complex(value * np.exp(-2j * np.pi * k * center))


def trapezoid_lags(
    centers: Iterable[float],
    velocities: Iterable[float],
    plateau_halfwidth: float,
    ramp_width: float,
    epsilon: float,
    n: int,
) -> tuple[dict[int, complex], dict[int, complex]]:
    """Lags for f and g=-sum_j v_j d/dx f_j."""
    centers = tuple(centers)
    velocities = tuple(velocities)
    amplitude = 1.0 - 2.0 * epsilon
    fhat: dict[int, complex] = {}
    ghat: dict[int, complex] = {}
    for k in range(-(n - 1), n):
        bands = tuple(
            trapezoid_hat(k, c, plateau_halfwidth, ramp_width)
            for c in centers
        )
        fhat[k] = complex(
            (epsilon if k == 0 else 0.0) + amplitude * sum(bands)
        )
        ghat[k] = complex(
            -amplitude * (2j * np.pi * k)
            * sum(v * band for v, band in zip(velocities, bands))
        )
    return fhat, ghat


# ---------------------------------------------------------------------------
# Exact finite spectral/coherence decomposition
# ---------------------------------------------------------------------------

def trace_binary_entropy_hessian(K: np.ndarray, E: np.ndarray) -> float:
    """D^2 Tr h_2(K)[E,E] from the Loewner matrix of h_2'."""
    eigenvalues, U = np.linalg.eigh(K)
    if eigenvalues[0] <= 0.0 or eigenvalues[-1] >= 1.0:
        raise ArithmeticError(
            f"spectrum leaves (0,1): {eigenvalues[0]}, {eigenvalues[-1]}"
        )
    Et = U.conj().T @ E @ U
    hp = np.log((1.0 - eigenvalues) / eigenvalues)
    differences = eigenvalues[:, None] - eigenvalues[None, :]
    numerator = hp[:, None] - hp[None, :]
    loewner = np.empty_like(differences)
    separated = np.abs(differences) > 1e-11
    loewner[separated] = numerator[separated] / differences[separated]
    midpoint = (eigenvalues[:, None] + eigenvalues[None, :]) / 2.0
    loewner[~separated] = -1.0 / (
        midpoint[~separated] * (1.0 - midpoint[~separated])
    )
    np.fill_diagonal(
        loewner, -1.0 / (eigenvalues * (1.0 - eigenvalues))
    )
    return float(np.sum(loewner * np.abs(Et) ** 2).real)


def spectral_increment_hessian(K: np.ndarray, E: np.ndarray) -> float:
    current = trace_binary_entropy_hessian(K, E)
    if len(K) == 1:
        return current
    previous = trace_binary_entropy_hessian(K[:-1, :-1], E[:-1, :-1])
    return current - previous


# ---------------------------------------------------------------------------
# Hard multi-interval chords
# ---------------------------------------------------------------------------

def intervals_valid(
    centers: Iterable[float], halfwidths: Iterable[float], gap: float = 0.002
) -> bool:
    pieces = sorted(
        (float(c - w), float(c + w)) for c, w in zip(centers, halfwidths)
    )
    if any(a < 0.0 or b > 1.0 or b - a < 2.0 * gap for a, b in pieces):
        return False
    return all(pieces[j][1] + gap < pieces[j + 1][0]
               for j in range(len(pieces) - 1))


def reflect_intervals(centers, halfwidths):
    return [1.0 - float(c) for c in centers], [float(w) for w in halfwidths]


def symmetric_difference_grid(
    plus_centers,
    plus_halfwidths,
    minus_centers,
    minus_halfwidths,
    grid: int = 65536,
) -> float:
    x = (np.arange(grid) + 0.5) / grid

    def indicator(centers, halfwidths):
        answer = np.zeros(grid, dtype=np.bool_)
        for center, halfwidth in zip(centers, halfwidths):
            answer |= ((x >= center - halfwidth) & (x < center + halfwidth))
        return answer

    return float(np.mean(
        indicator(plus_centers, plus_halfwidths)
        ^ indicator(minus_centers, minus_halfwidths)
    ))


def evaluate_interval_chord(
    plus_centers,
    plus_halfwidths,
    minus_centers,
    minus_halfwidths,
    epsilon: float,
    n: int,
    label: str,
) -> dict[str, Any] | None:
    if not intervals_valid(plus_centers, plus_halfwidths):
        return None
    if not intervals_valid(minus_centers, minus_halfwidths):
        return None

    plus = union_interval_lags(plus_centers, plus_halfwidths, n)
    minus = union_interval_lags(minus_centers, minus_halfwidths, n)
    fhat = {
        k: complex(
            (epsilon if k == 0 else 0.0)
            + (1.0 - 2.0 * epsilon) * (plus[k] + minus[k]) / 2.0
        )
        for k in plus
    }
    ghat = {
        k: complex((1.0 - 2.0 * epsilon) * (plus[k] - minus[k]) / 2.0)
        for k in plus
    }
    K = toeplitz_from_lags(fhat, n)
    E = toeplitz_from_lags(ghat, n)
    if np.linalg.norm(E) < 1e-12:
        return None

    R, R1, R2, fisher, transport, stats = conditional_increment_jets(K, E)
    if stats[3] != 0.0:
        raise ArithmeticError(f"invalid conditional probabilities: {stats}")

    symdiff = symmetric_difference_grid(
        plus_centers, plus_halfwidths, minus_centers, minus_halfwidths
    )
    bulk = -(1.0 - 2.0 * epsilon) ** 2 * symdiff
    spectral = spectral_increment_hessian(K, E)
    return {
        "label": label,
        "m": len(tuple(plus_centers)),
        "epsilon": epsilon,
        "n": n,
        "plus_centers": [float(x) for x in plus_centers],
        "plus_halfwidths": [float(x) for x in plus_halfwidths],
        "minus_centers": [float(x) for x in minus_centers],
        "minus_halfwidths": [float(x) for x in minus_halfwidths],
        "symmetric_difference": symdiff,
        "R2": float(R2[-1]),
        "R1": float(R1[-1]),
        "conditional_fisher": float(fisher[-1]),
        "prediction_vertical": float(transport[-1]),
        "spectral_increment": spectral,
        "coherence_increment": float(R2[-1] - spectral),
        "bulk_limit": bulk,
        "bulk_subtracted": float(R2[-1] - bulk),
        "min_conditional_p": float(stats[0]),
        "max_conditional_p": float(stats[1]),
        "increment_sequence": [float(x) for x in R2],
    }


def random_near_symmetric(rng: np.random.Generator, m: int):
    for _ in range(1000):
        if m == 2:
            a = rng.uniform(0.14, 0.38)
            base_centers = np.array([a, 1.0 - a])
            base_halfwidths = np.repeat(rng.uniform(0.035, 0.09), 2)
        elif m == 3:
            a = rng.uniform(0.12, 0.30)
            base_centers = np.array([a, 0.5, 1.0 - a])
            u = rng.uniform(0.025, 0.07)
            base_halfwidths = np.array([u, rng.uniform(0.025, 0.07), u])
        elif m == 4:
            a = rng.uniform(0.08, 0.20)
            b = rng.uniform(0.28, 0.40)
            base_centers = np.array([a, b, 1.0 - b, 1.0 - a])
            u = rng.uniform(0.02, 0.055)
            v = rng.uniform(0.02, 0.055)
            base_halfwidths = np.array([u, v, v, u])
        else:
            raise ValueError(m)

        plus_centers = base_centers + rng.uniform(-0.018, 0.018, m)
        plus_halfwidths = base_halfwidths + rng.uniform(-0.012, 0.012, m)
        minus_centers, minus_halfwidths = reflect_intervals(
            plus_centers, plus_halfwidths
        )
        if (
            intervals_valid(plus_centers, plus_halfwidths, 0.004)
            and intervals_valid(minus_centers, minus_halfwidths, 0.004)
        ):
            return (
                plus_centers.tolist(), plus_halfwidths.tolist(),
                minus_centers, minus_halfwidths,
            )
    return None


def random_reflection(rng: np.random.Generator, m: int):
    for _ in range(1000):
        centers = np.sort(rng.uniform(0.06, 0.94, m))
        halfwidths = rng.uniform(0.018, 0.075, m)
        if intervals_valid(centers, halfwidths, 0.006):
            reflected_centers, reflected_halfwidths = reflect_intervals(
                centers, halfwidths
            )
            if intervals_valid(reflected_centers, reflected_halfwidths, 0.006):
                return (
                    centers.tolist(), halfwidths.tolist(),
                    reflected_centers, reflected_halfwidths,
                )
    return None


def deterministic_even_width_families():
    answer = []
    for delta in (0.004, 0.008, 0.015, 0.025):
        centers = [0.2, 0.5, 0.8]
        widths = [0.055, 0.07, 0.055]
        plus = [widths[0] - delta / 2.0,
                widths[1] + delta,
                widths[2] - delta / 2.0]
        minus = [widths[0] + delta / 2.0,
                 widths[1] - delta,
                 widths[2] + delta / 2.0]
        answer.append((centers, plus, centers, minus, "even_width_m3"))
    for delta in (0.004, 0.008, 0.015):
        centers = [0.12, 0.35, 0.65, 0.88]
        widths = [0.04, 0.05, 0.05, 0.04]
        plus = [widths[0] + delta, widths[1] - delta,
                widths[2] - delta, widths[3] + delta]
        minus = [widths[0] - delta, widths[1] + delta,
                 widths[2] + delta, widths[3] - delta]
        answer.append((centers, plus, centers, minus, "even_width_m4"))
    return answer


def scan_one_epsilon(epsilon: float, n: int = 14) -> list[dict[str, Any]]:
    rng = np.random.default_rng(SEED)
    # Reproduce the compilation warm-up consumed by the frozen scan.
    warm = random_near_symmetric(rng, 2)
    if warm is not None:
        evaluate_interval_chord(*warm, 0.05, 8, "warmup")

    rows: list[dict[str, Any]] = []
    for m in (2, 3, 4):
        for _ in range(45):
            candidate = random_near_symmetric(rng, m)
            if candidate is not None:
                row = evaluate_interval_chord(
                    *candidate, epsilon, n, f"near_symmetric_m{m}"
                )
                if row is not None:
                    rows.append(row)
        for _ in range(25):
            candidate = random_reflection(rng, m)
            if candidate is not None:
                row = evaluate_interval_chord(
                    *candidate, epsilon, n, f"arbitrary_reflection_m{m}"
                )
                if row is not None:
                    rows.append(row)

    for plus_c, plus_w, minus_c, minus_w, label in deterministic_even_width_families():
        row = evaluate_interval_chord(
            plus_c, plus_w, minus_c, minus_w, epsilon, n, label
        )
        if row is not None:
            rows.append(row)

    rows.sort(key=lambda row: row["R2"], reverse=True)
    return rows


# ---------------------------------------------------------------------------
# Boundary-layer and interval-count comparison families
# ---------------------------------------------------------------------------

def evaluate_ramp(epsilon: float, n: int) -> dict[str, Any]:
    centers = (0.12, 0.35, 0.65, 0.88)
    velocities = (1.0, -1.0, -1.0, 1.0)
    plateau_halfwidth = 0.0225
    ramp_width = 0.015
    fhat, ghat = trapezoid_lags(
        centers, velocities, plateau_halfwidth, ramp_width, epsilon, n
    )
    K = toeplitz_from_lags(fhat, n)
    E = toeplitz_from_lags(ghat, n)
    R, R1, R2, fisher, transport, stats = conditional_increment_jets(K, E)
    spectral = spectral_increment_hessian(K, E)

    log_ratio = math.log((1.0 - epsilon) / epsilon)
    bulk = -4.0 * (1.0 - 2.0 * epsilon) * sum(
        v * v / ramp_width for v in velocities
    ) * log_ratio
    legal_radius = (
        0.5 * epsilon * ramp_width
        / ((1.0 - 2.0 * epsilon) * max(abs(v) for v in velocities))
    )
    return {
        "family": "four_band_piecewise_linear_ramp",
        "epsilon": epsilon,
        "n": n,
        "R2": float(R2[-1]),
        "R1": float(R1[-1]),
        "conditional_fisher": float(fisher[-1]),
        "prediction_vertical": float(transport[-1]),
        "spectral_increment": spectral,
        "coherence_increment": float(R2[-1] - spectral),
        "bulk_limit": bulk,
        "bulk_subtracted": float(R2[-1] - bulk),
        "legal_affine_radius": legal_radius,
        "min_conditional_p": float(stats[0]),
        "max_conditional_p": float(stats[1]),
        "increment_sequence": [float(x) for x in R2],
    }


COUNT_CENTERS = {
    1: [0.5],
    2: [0.22, 0.78],
    3: [0.16, 0.5, 0.84],
    4: [0.11, 0.34, 0.66, 0.89],
    5: [0.08, 0.25, 0.5, 0.75, 0.92],
    6: [0.07, 0.20, 0.37, 0.63, 0.80, 0.93],
    7: [0.055, 0.17, 0.31, 0.5, 0.69, 0.83, 0.945],
    8: [0.05, 0.16, 0.28, 0.41, 0.59, 0.72, 0.84, 0.95],
}


def evaluate_interval_count(m: int, epsilon: float, n: int) -> dict[str, Any]:
    centers = np.array(COUNT_CENTERS[m], dtype=float)
    halfwidth = 0.12 / m
    shift = 0.25 * halfwidth
    velocities = np.zeros(m)
    used = np.zeros(m, dtype=np.bool_)
    pair_index = 0
    for i, center in enumerate(centers):
        if used[i]:
            continue
        j = int(np.argmin(np.abs(centers - (1.0 - center))))
        velocity = 1.0 if pair_index % 2 == 0 else -1.0
        velocities[i] = velocity
        velocities[j] = velocity
        used[i] = True
        used[j] = True
        pair_index += 1

    plus_centers = ((centers + shift * velocities) % 1.0).tolist()
    minus_centers = ((centers - shift * velocities) % 1.0).tolist()
    widths = [halfwidth] * m
    row = evaluate_interval_chord(
        plus_centers, widths, minus_centers, widths,
        epsilon, n, f"fixed_measure_m{m}",
    )
    if row is None:
        raise ArithmeticError("count-family construction unexpectedly invalid")
    row["base_centers"] = centers.tolist()
    row["velocities"] = velocities.tolist()
    row["halfwidth"] = halfwidth
    row["shift"] = shift
    return row


# ---------------------------------------------------------------------------
# CLI and compact summaries
# ---------------------------------------------------------------------------

def summarize_scan(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        raise ValueError("empty scan")
    meaningful = [row for row in rows if row["symmetric_difference"] >= 0.02]
    return {
        "count": len(rows),
        "positive_count": sum(row["R2"] > 0.0 for row in rows),
        "any_positive_increment_count": sum(
            max(row["increment_sequence"]) > 1e-12 for row in rows
        ),
        "least_negative": max(rows, key=lambda row: row["R2"]),
        "most_negative": min(rows, key=lambda row: row["R2"]),
        "least_negative_with_symmetric_difference_ge_0.02": (
            max(meaningful, key=lambda row: row["R2"])
            if meaningful else None
        ),
    }


def write_json(path: str | Path, value: Any) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def command_scan(args) -> None:
    started = time.time()
    rows = scan_one_epsilon(args.epsilon, args.n)
    result = {
        "seed": SEED,
        "epsilon": args.epsilon,
        "n": args.n,
        "elapsed_seconds": time.time() - started,
        "summary": summarize_scan(rows),
        "rows": rows if args.keep_all else None,
    }
    write_json(args.output, result)
    print(json.dumps(result["summary"], indent=2))


def command_full_scan(args) -> None:
    destination = Path(args.output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    summaries = []
    for epsilon in DEFAULT_EPSILONS:
        started = time.time()
        rows = scan_one_epsilon(epsilon, args.n)
        summary = summarize_scan(rows)
        summary["epsilon"] = epsilon
        summary["elapsed_seconds"] = time.time() - started
        summaries.append(summary)
        write_json(destination / f"scan_epsilon_{epsilon:g}.json", {
            "seed": SEED,
            "epsilon": epsilon,
            "n": args.n,
            "summary": summary,
            "rows": rows if args.keep_all else None,
        })
        print(epsilon, summary["count"], summary["positive_count"],
              summary["least_negative"]["R2"], flush=True)
    write_json(destination / "scan_summary.json", summaries)


def command_selected(args) -> None:
    rows: list[dict[str, Any]] = []
    for epsilon in (0.05, 0.01, 0.002):
        for n in (14, 18, 20):
            if n <= args.max_n:
                rows.append(evaluate_ramp(epsilon, n))
    for epsilon in (0.05, 0.01, 0.002):
        for m in range(1, 9):
            rows.append(evaluate_interval_count(m, epsilon, min(14, args.max_n)))
    write_json(args.output, {
        "seed": SEED,
        "rows": rows,
        "positive_count": sum(row["R2"] > 0.0 for row in rows),
    })
    for row in rows:
        print(row["family"] if "family" in row else row["label"],
              row["epsilon"], row["n"], row["R2"])


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(required=True)

    scan = sub.add_parser("scan", help="scan one epsilon")
    scan.add_argument("--epsilon", type=float, required=True)
    scan.add_argument("--n", type=int, default=14)
    scan.add_argument("--output", required=True)
    scan.add_argument("--keep-all", action="store_true")
    scan.set_defaults(func=command_scan)

    full = sub.add_parser("full-scan", help="run the frozen seven-epsilon scan")
    full.add_argument("--n", type=int, default=14)
    full.add_argument("--output-dir", required=True)
    full.add_argument("--keep-all", action="store_true")
    full.set_defaults(func=command_full_scan)

    selected = sub.add_parser("selected", help="run deterministic comparison cases")
    selected.add_argument("--max-n", type=int, default=20)
    selected.add_argument("--output", required=True)
    selected.set_defaults(func=command_selected)
    return p


def main() -> None:
    args = parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
