"""Finite scout search inside the general fixed-beta tau family.

The theorem in this directory is exact.  This script is not a proof of
concavity or nonconcavity.  It uses the path-sparse L dynamic program from the
NS-1 route as a scalable entropy evaluator and records deterministic finite
evidence for n=5..30.

No third-party packages are used.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import os
import random
import sys
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Sequence


sys.dont_write_bytecode = True
os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")


def l_parts_float(beta: Sequence[float], tau: Sequence[float]) -> tuple[list[float], list[float]]:
    n = len(tau)
    inv = [1.0 / t for t in tau]
    diag = [0.0] * n
    edge = [0.0] * (n - 1)
    for i in range(n - 1):
        diag[i] = inv[i] + beta[i] * beta[i] * inv[i + 1] - 1.0
        edge[i] = -beta[i] * inv[i + 1]
    diag[-1] = inv[-1] - 1.0
    return diag, edge


def l_parts_fraction(beta: Sequence[Fraction], tau: Sequence[Fraction]) -> tuple[list[Fraction], list[Fraction]]:
    n = len(tau)
    inv = [1 / t for t in tau]
    diag: list[Fraction] = [Fraction(0)] * n
    edge: list[Fraction] = [Fraction(0)] * (n - 1)
    for i in range(n - 1):
        diag[i] = inv[i] + beta[i] * beta[i] * inv[i + 1] - 1
        edge[i] = -beta[i] * inv[i + 1]
    diag[-1] = inv[-1] - 1
    return diag, edge


def min_ldl_pivot(diag: Sequence[float], edge: Sequence[float]) -> float:
    if not diag:
        return math.inf
    pivot = diag[0]
    best = pivot
    for i in range(1, len(diag)):
        if pivot <= 0.0 or not math.isfinite(pivot):
            return pivot
        pivot = diag[i] - edge[i - 1] * edge[i - 1] / pivot
        best = min(best, pivot)
    return best


def admissible(beta: Sequence[float], tau: Sequence[float], margin: float = 1e-10) -> bool:
    if any(t <= 0.0 or not math.isfinite(t) for t in tau):
        return False
    diag, edge = l_parts_float(beta, tau)
    return min_ldl_pivot(diag, edge) > margin


def path_entropy_float(diag: Sequence[float], edge: Sequence[float]) -> float:
    """Path L-ensemble entropy via the NS-1 selected-run recurrence."""

    n = len(diag)
    if n == 0:
        return 0.0
    if min_ldl_pivot(diag, edge) <= 0.0:
        raise ValueError("L is not SPD by float LDL check")

    kappa = [[0.0] * n for _ in range(n)]
    for start in range(n):
        prev2 = 1.0
        prev1 = diag[start]
        if prev1 <= 0.0:
            raise ValueError("nonpositive interval determinant")
        kappa[start][start] = prev1
        for end in range(start + 1, n):
            current = diag[end] * prev1 - edge[end - 1] * edge[end - 1] * prev2
            if current <= 0.0 or not math.isfinite(current):
                raise ValueError("nonpositive/nonfinite interval determinant")
            kappa[start][end] = current
            prev2, prev1 = prev1, current

    z = [0.0] * (n + 1)
    t_log = [0.0] * (n + 1)
    z[0] = 1.0

    for length in range(1, n + 1):
        end = length - 1
        z_terms = [z[length - 1]]
        t_terms = [t_log[length - 1]]
        for start in range(length):
            prefix_len = 0 if start == 0 else start - 1
            block = kappa[start][end]
            z_prefix = z[prefix_len]
            z_terms.append(z_prefix * block)
            t_terms.append(block * t_log[prefix_len] + z_prefix * block * math.log(block))
        z[length] = math.fsum(z_terms)
        t_log[length] = math.fsum(t_terms)

    if z[-1] <= 0.0 or not math.isfinite(z[-1]) or not math.isfinite(t_log[-1]):
        raise ValueError("nonfinite entropy accumulator")
    return math.log(z[-1]) - t_log[-1] / z[-1]


def entropy_tau(beta: Sequence[float], tau: Sequence[float]) -> float:
    diag, edge = l_parts_float(beta, tau)
    return path_entropy_float(diag, edge)


def max_scale_for_profile(beta: Sequence[float], profile: Sequence[float]) -> float:
    """Find a float upper scale for tau=s*profile with L(tau)>0."""

    lo = 0.0
    hi = 1.0
    while admissible(beta, [hi * x for x in profile]) and hi < 1e6:
        hi *= 2.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if admissible(beta, [mid * x for x in profile]):
            lo = mid
        else:
            hi = mid
    return lo


def random_beta(n: int, rng: random.Random) -> list[float]:
    out = []
    for i in range(n - 1):
        sign = -1.0 if (i + rng.randrange(2)) % 2 else 1.0
        magnitude = rng.uniform(0.12, 0.72)
        out.append(sign * magnitude)
    return out


def structured_beta(n: int) -> list[float]:
    return [((-1.0) ** i) * (0.22 + 0.33 * ((3 * i + 1) % 7) / 6.0) for i in range(n - 1)]


def random_center(beta: Sequence[float], rng: random.Random) -> list[float] | None:
    n = len(beta) + 1
    profile = [math.exp(rng.uniform(math.log(0.55), math.log(1.65))) for _ in range(n)]
    smax = max_scale_for_profile(beta, profile)
    if not math.isfinite(smax) or smax <= 0.0:
        return None
    scale = rng.uniform(0.20, 0.92) * smax
    tau = [scale * x for x in profile]
    return tau if admissible(beta, tau) else None


def random_displacement(tau: Sequence[float], support_size: int, rng: random.Random) -> tuple[list[float], float]:
    n = len(tau)
    if support_size >= n:
        support = list(range(n))
    else:
        support = rng.sample(range(n), support_size)
    raw = [0.0] * n
    for i in support:
        raw[i] = rng.gauss(0.0, 1.0)
    norm = max(abs(raw[i]) for i in support)
    if norm == 0.0:
        raw[support[0]] = 1.0
        norm = 1.0
    rho = rng.uniform(0.03, 0.88)
    disp = [0.0] * n
    for i in support:
        disp[i] = rho * tau[i] * raw[i] / norm
    rel_norm = math.sqrt(sum((disp[i] / tau[i]) ** 2 for i in range(n)))
    return disp, rel_norm


def shrink_to_feasible(beta: Sequence[float], tau: Sequence[float], disp: Sequence[float]) -> tuple[list[float], float] | None:
    factor = 1.0
    for _ in range(30):
        trial = [factor * x for x in disp]
        minus = [t - d for t, d in zip(tau, trial)]
        plus = [t + d for t, d in zip(tau, trial)]
        if admissible(beta, minus) and admissible(beta, plus):
            rel_norm = math.sqrt(sum((trial[i] / tau[i]) ** 2 for i in range(len(tau))))
            return trial, rel_norm
        factor *= 0.5
    return None


def chord_delta(beta: Sequence[float], tau: Sequence[float], disp: Sequence[float]) -> tuple[float, float, float, float]:
    minus = [t - d for t, d in zip(tau, disp)]
    plus = [t + d for t, d in zip(tau, disp)]
    h_minus = entropy_tau(beta, minus)
    h_zero = entropy_tau(beta, tau)
    h_plus = entropy_tau(beta, plus)
    delta = 0.5 * (h_minus + h_plus) - h_zero
    return delta, h_minus, h_zero, h_plus


def rounded_list(values: Sequence[float], digits: int = 12) -> list[float]:
    return [round(float(x), digits) for x in values]


def candidate_record(
    beta: Sequence[float],
    tau: Sequence[float],
    disp: Sequence[float],
    rel_norm: float,
    delta: float,
    entropies: tuple[float, float, float],
    support_rank: int,
) -> dict[str, object]:
    curvature = 2.0 * delta / (rel_norm * rel_norm) if rel_norm > 0 else math.nan
    return {
        "delta_endpoint_average_minus_midpoint": delta,
        "second_difference_over_relative_norm_squared": curvature,
        "support_rank_equals_rank_K_perturbation": support_rank,
        "relative_step_norm": rel_norm,
        "H_minus": entropies[0],
        "H_zero": entropies[1],
        "H_plus": entropies[2],
        "beta": rounded_list(beta),
        "tau_zero": rounded_list(tau),
        "tau_displacement": rounded_list(disp),
    }


def search_one_n(n: int, trials: int, rng: random.Random) -> dict[str, object]:
    buckets = {
        "rank1": {"support_size": 1, "feasible": 0, "positive_gt_1e-10": 0, "best": None},
        "rank2": {"support_size": 2, "feasible": 0, "positive_gt_1e-10": 0, "best": None},
        "full_rank": {"support_size": n, "feasible": 0, "positive_gt_1e-10": 0, "best": None},
    }
    center_failures = 0
    chord_failures = 0

    for trial in range(trials):
        beta = structured_beta(n) if trial % 5 == 0 else random_beta(n, rng)
        tau = random_center(beta, rng)
        if tau is None:
            center_failures += 1
            continue
        for name, bucket in buckets.items():
            support_size = int(bucket["support_size"])
            disp0, _ = random_displacement(tau, support_size, rng)
            shrunk = shrink_to_feasible(beta, tau, disp0)
            if shrunk is None:
                chord_failures += 1
                continue
            disp, rel_norm = shrunk
            try:
                delta, hm, h0, hp = chord_delta(beta, tau, disp)
            except (ValueError, OverflowError):
                chord_failures += 1
                continue
            if not math.isfinite(delta):
                chord_failures += 1
                continue
            bucket["feasible"] += 1
            if delta > 1e-10:
                bucket["positive_gt_1e-10"] += 1
            support_rank = sum(1 for x in disp if abs(x) > 0.0)
            record = candidate_record(beta, tau, disp, rel_norm, delta, (hm, h0, hp), support_rank)
            best = bucket["best"]
            if best is None or delta > best["delta_endpoint_average_minus_midpoint"]:
                bucket["best"] = record

    return {
        "n": n,
        "trials": trials,
        "center_failures": center_failures,
        "chord_failures": chord_failures,
        "buckets": buckets,
    }


def load_path_schur():
    here = Path(__file__).resolve()
    module_path = here.parents[3] / "next_structures" / "sparse_schur" / "path_schur.py"
    spec = importlib.util.spec_from_file_location("readonly_path_schur_for_d10b2", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, module_path


def exact_dp_reuse_smoke() -> dict[str, object]:
    path_schur, module_path = load_path_schur()
    beta = [Fraction(1, 3), -Fraction(2, 5), Fraction(1, 4), -Fraction(1, 6)]
    tau = [Fraction(1, 32), Fraction(1, 37), Fraction(1, 41), Fraction(1, 43), Fraction(1, 47)]
    diag_q, edge_q = l_parts_fraction(beta, tau)
    exact = path_schur.path_entropy_dp(diag_q, edge_q, precision=80)
    diag_f = [float(x) for x in diag_q]
    edge_f = [float(x) for x in edge_q]
    h_float = path_entropy_float(diag_f, edge_f)
    h_exact = float(Decimal(str(exact["entropy"])))
    validation = path_schur.direct_validation_case(diag_q, edge_q, precision=80)
    return {
        "module_path": str(module_path),
        "n": 5,
        "direct_mobius_events": validation["events_checked"],
        "direct_mobius_mismatch_count": validation["mismatch_count"],
        "exact_entropy_decimal": str(exact["entropy"]),
        "float_entropy": h_float,
        "absolute_float_vs_exact_entropy": abs(h_float - h_exact),
    }


def run_search(n_min: int, n_max: int, trials: int, seed: int) -> dict[str, object]:
    rng = random.Random(seed)
    results = [search_one_n(n, trials, rng) for n in range(n_min, n_max + 1)]
    positives = []
    best_overall = None
    for item in results:
        for name, bucket in item["buckets"].items():
            best = bucket["best"]
            if best is None:
                continue
            if bucket["positive_gt_1e-10"]:
                positives.append({"n": item["n"], "bucket": name, "count": bucket["positive_gt_1e-10"], "best": best})
            if best_overall is None or best["delta_endpoint_average_minus_midpoint"] > best_overall["best"]["delta_endpoint_average_minus_midpoint"]:
                best_overall = {"n": item["n"], "bucket": name, "best": best}
    return {
        "status": "SCOUT_COMPLETE",
        "seed": seed,
        "n_min": n_min,
        "n_max": n_max,
        "trials_per_n": trials,
        "gap_sign_convention": "Delta=(H_minus+H_plus)/2-H_zero; positive would violate concavity",
        "finite_search_only": True,
        "exact_dp_reuse_smoke": exact_dp_reuse_smoke(),
        "positive_scouts_gt_1e-10": positives,
        "best_overall": best_overall,
        "per_n": results,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-min", type=int, default=5)
    parser.add_argument("--n-max", type=int, default=30)
    parser.add_argument("--trials", type=int, default=160)
    parser.add_argument("--seed", type=int, default=20260908)
    parser.add_argument("--out", type=Path, default=Path(__file__).with_name("search_results.json"))
    args = parser.parse_args()

    result = run_search(args.n_min, args.n_max, args.trials, args.seed)
    text = json.dumps(result, indent=2, ensure_ascii=False)
    args.out.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
