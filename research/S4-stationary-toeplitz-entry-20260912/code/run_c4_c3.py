#!/usr/bin/env python3
"""C4 transition-spectrum diagnostics and C3 fixed-family continuation."""
from __future__ import annotations

import argparse
import csv
import json
import math
import os
import platform
import time
from pathlib import Path

import numpy as np

import upstream_nonsmooth_interval_probe as upstream


EPSILONS = (0.2, 0.05, 0.01, 0.002)
DELTAS = (0.01, 0.02, 0.05, 0.1, 0.2)
SPECTRAL_N = (8, 12, 16, 24, 32, 48, 64, 96, 128, 192, 256, 384, 512, 768, 1024, 1536, 2048)


FAMILIES = {
    # Exact frozen rows of the upstream seed-2026090701 scan.  The m=2 row is
    # the global least-negative candidate; m=3 is the least-negative
    # near-symmetric row with symmetric difference >=0.005; m=4 is the
    # upstream "meaningful" row used in its n=22 continuation.
    "near_symmetric_m2_least": (
        [0.1682317687756767, 0.831041044743125],
        [0.07316291546247072, 0.07282492638916131],
        [0.8317682312243233, 0.168958955256875],
        [0.07316291546247072, 0.07282492638916131],
    ),
    "near_symmetric_m3_selected": (
        [0.3050131627700731, 0.4969063133026255, 0.6956911263626705],
        [0.03288216842023798, 0.029175516713043834, 0.03336840566043635],
        [0.6949868372299268, 0.5030936866973745, 0.3043088736373295],
        [0.03288216842023798, 0.029175516713043834, 0.03336840566043635],
    ),
    "near_symmetric_m4_meaningful": (
        [0.14624338786771943, 0.3854847240109157, 0.6165014489392875, 0.8543205169585452],
        [0.028383173537270174, 0.02345136782009442, 0.027071108885513076, 0.031129349243439266],
        [0.8537566121322806, 0.6145152759890843, 0.3834985510607125, 0.14567948304145484],
        [0.028383173537270174, 0.02345136782009442, 0.027071108885513076, 0.031129349243439266],
    ),
}


def matrices(family: str, epsilon: float, n: int):
    pc, pw, mc, mw = FAMILIES[family]
    plus = upstream.union_interval_lags(pc, pw, n)
    minus = upstream.union_interval_lags(mc, mw, n)
    fhat = {
        k: complex((epsilon if k == 0 else 0.0) + (1 - 2 * epsilon) * (plus[k] + minus[k]) / 2)
        for k in plus
    }
    ghat = {k: complex((1 - 2 * epsilon) * (plus[k] - minus[k]) / 2) for k in plus}
    return upstream.toeplitz_from_lags(fhat, n), upstream.toeplitz_from_lags(ghat, n)


def exact_symmetric_difference(pc, pw, mc, mw):
    """Exact-in-double length of the XOR of two disjoint interval unions."""
    events = []
    for centers, widths, bit in ((pc, pw, 1), (mc, mw, 2)):
        for c, w in zip(centers, widths):
            events.append((c - w, bit, 1))
            events.append((c + w, bit, -1))
    events.sort()
    active = [0, 0]
    previous = events[0][0]
    total = 0.0
    for x, bit, change in events:
        if bool(active[0]) != bool(active[1]):
            total += x - previous
        active[bit - 1] += change
        previous = x
    return total


def write_csv(path: Path, rows: list[dict]):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def regression_rows(transition: list[dict]):
    result = []
    safe = [r for r in transition if r["threshold_status"] == "SAFE_DELTA_AWAY_FROM_EPSILON"]
    keys = sorted({(r["family"], r["epsilon"], r["delta"]) for r in safe})
    for family, epsilon, delta in keys:
        rows = [r for r in safe if (r["family"], r["epsilon"], r["delta"]) == (family, epsilon, delta) and r["n"] >= 64]
        x = np.log(np.array([r["n"] for r in rows], dtype=float))
        y = np.array([r["transition_count"] for r in rows], dtype=float)
        slope, intercept = np.polyfit(x, y, 1)
        pred = intercept + slope * x
        ss_res = float(np.sum((y - pred) ** 2))
        ss_tot = float(np.sum((y - np.mean(y)) ** 2))
        nvec = np.array([r["n"] for r in rows], dtype=float)
        design = np.column_stack((nvec, x, np.ones_like(x)))
        linear, logcoef, constant = np.linalg.lstsq(design, y, rcond=None)[0]
        pred_two = design @ np.array([linear, logcoef, constant])
        result.append({
            "family": family,
            "epsilon": epsilon,
            "delta": delta,
            "n_min": min(r["n"] for r in rows),
            "n_max": max(r["n"] for r in rows),
            "points": len(rows),
            "slope_vs_log_n": float(slope),
            "intercept": float(intercept),
            "r_squared_diagnostic": 1.0 - ss_res / ss_tot if ss_tot else 1.0,
            "max_abs_residual": float(np.max(np.abs(y - pred))),
            "linear_plus_log_linear_coefficient": float(linear),
            "linear_plus_log_log_coefficient": float(logcoef),
            "linear_plus_log_constant": float(constant),
            "linear_plus_log_max_abs_residual": float(np.max(np.abs(y - pred_two))),
            "symbol_half_level_measure": float(rows[0]["symmetric_difference"]),
            "semantics": "deterministic least-squares diagnostic; not a confidence interval",
        })
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--max-curvature-n", type=int, default=22)
    parser.add_argument("--skip-curvature", action="store_true")
    args = parser.parse_args()
    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)
    started = time.time()

    transition = []
    eigen_cache: dict[tuple[int, float, int], np.ndarray] = {}
    for family in FAMILIES:
        pc, pw, mc, mw = FAMILIES[family]
        symdiff = exact_symmetric_difference(pc, pw, mc, mw)
        # Eigenvalues for all epsilon are affine transforms of the epsilon=0 spectrum.
        for n in SPECTRAL_N:
            K0, _ = matrices(family, 0.0, n)
            base_eigs = np.linalg.eigvalsh(K0)
            for epsilon in EPSILONS:
                eigs = epsilon + (1 - 2 * epsilon) * base_eigs
                eigen_cache[(family, epsilon, n)] = eigs
                closest = eigs[np.argsort(np.abs(eigs - 0.5))[:6]]
                distance01 = float(np.sum(np.minimum(eigs, 1 - eigs)))
                for delta in DELTAS:
                    threshold_status = (
                        "EXCLUDED_FROM_FITS_DELTA_EQUALS_EPSILON_ROUNDOFF_SENSITIVE"
                        if abs(delta - epsilon) <= 1e-15
                        else "SAFE_DELTA_AWAY_FROM_EPSILON"
                    )
                    count = int(np.sum((eigs >= delta) & (eigs <= 1 - delta)))
                    transition.append({
                        "family": family,
                        "epsilon": epsilon,
                        "n": n,
                        "delta": delta,
                        "threshold_status": threshold_status,
                        "symmetric_difference": symdiff,
                        "transition_count": count,
                        "count_over_log_n": count / math.log(n),
                        "spectral_distance_to_01": distance01,
                        "closest_to_half": ";".join(f"{x:.17g}" for x in closest),
                        "eig_min": float(eigs[0]),
                        "eig_max": float(eigs[-1]),
                    })

    curvature = []
    extended = []
    timings = []
    for family in FAMILIES:
        for epsilon in (() if args.skip_curvature else EPSILONS):
            K, E = matrices(family, epsilon, args.max_curvature_n)
            tick = time.time()
            R, R1, R2, fisher, transport, stats = upstream.conditional_increment_jets(K, E)
            timings.append({"family": family, "epsilon": epsilon, "max_n": args.max_curvature_n, "seconds": time.time() - tick, "nodes": float(stats[2])})
            cumulative = np.cumsum(R2)
            pc, pw, mc, mw = FAMILIES[family]
            symdiff = exact_symmetric_difference(pc, pw, mc, mw)
            bulk = -(1 - 2 * epsilon) ** 2 * symdiff
            for n in range(2, args.max_curvature_n + 1):
                Kn, En = K[:n, :n], E[:n, :n]
                spectral = upstream.spectral_increment_hessian(Kn, En)
                coherence = float(R2[n - 1] - spectral)
                eigs = np.linalg.eigvalsh(Kn)
                base = {
                    "family": family,
                    "epsilon": epsilon,
                    "n": n,
                    "Hn_second": float(cumulative[n - 1]),
                    "increment_second": float(R2[n - 1]),
                    "Hn_second_over_n": float(cumulative[n - 1] / n),
                    "conditional_fisher": float(fisher[n - 1]),
                    "prediction_vertical": float(transport[n - 1]),
                    "spectral_increment": float(spectral),
                    "coherence_increment": coherence,
                    "coherence_over_abs_spectral": coherence / abs(spectral) if spectral else math.nan,
                    "bulk_limit": bulk,
                    "bulk_correction": float(R2[n - 1] - bulk),
                    "min_conditional_p": float(stats[0]),
                    "max_conditional_p": float(stats[1]),
                    "eig_min": float(eigs[0]),
                    "eig_max": float(eigs[-1]),
                }
                extended.append(base)
                for delta in DELTAS:
                    threshold_status = (
                        "EXCLUDED_FROM_FITS_DELTA_EQUALS_EPSILON_ROUNDOFF_SENSITIVE"
                        if abs(delta - epsilon) <= 1e-15
                        else "SAFE_DELTA_AWAY_FROM_EPSILON"
                    )
                    count = int(np.sum((eigs >= delta) & (eigs <= 1 - delta)))
                    curvature.append({
                        **base,
                        "delta": delta,
                        "threshold_status": threshold_status,
                        "transition_count": count,
                        "correction_over_transition_count": coherence / count if count else math.nan,
                    })

    write_csv(out / "transition_spectrum.csv", transition)
    write_csv(out / "transition_fit.csv", regression_rows(transition))
    write_csv(out / "curvature_vs_transition.csv", curvature)
    write_csv(out / "extended_curvature.csv", extended)
    record = {
        "seed": upstream.SEED,
        "source_sha256": "f3f49dd0ed382df7dba1d6eb849fac607023b1de5e21f9679c03f52323fc1b30",
        "source_repository": "randomcat4/icm-conjecture-lab",
        "source_commit": "ee97a7341ac968fc341599aa973d0793497e7db3",
        "source_path": "research/I05_info_geometry_independent/nonsmooth_stationary/artifacts/nonsmooth_interval_probe.py",
        "families": list(FAMILIES),
        "epsilons": EPSILONS,
        "deltas": DELTAS,
        "spectral_n": SPECTRAL_N,
        "max_curvature_n": args.max_curvature_n,
        "skip_curvature": args.skip_curvature,
        "timings": timings,
        "elapsed_seconds": time.time() - started,
        "python": platform.python_version(),
        "numpy": np.__version__,
        "pid": os.getpid(),
        "status": "FINITE_NUMERICAL_EVIDENCE_ONLY",
        "threshold_policy": "Rows with delta=epsilon are retained and explicitly marked roundoff-sensitive; they are excluded from every regression fit.",
    }
    (out / "c4_c3_run.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
