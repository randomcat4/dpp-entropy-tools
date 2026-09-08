#!/usr/bin/env python3
"""Independent finite-window checks for the S1 Toeplitz DPP review.

The script intentionally rebuilds the exact-event determinant and small-window
entropy calculations from the public definition instead of importing project
helpers.  It uses only the Python standard library plus NumPy for floating
determinants; the first-derivative check is exact rational arithmetic.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import os
import platform
import subprocess
import sys
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Iterable

import numpy as np


@dataclass(frozen=True)
class Family:
    name: str
    p: Fraction
    a: tuple[Fraction, ...]
    b: tuple[Fraction, ...]
    tau: Fraction

    @property
    def m(self) -> int:
        return len(self.a)


BENCHMARK = Family(
    name="main_benchmark",
    p=Fraction(1, 2),
    a=(Fraction(9, 50), Fraction(-3, 25), Fraction(2, 25)),
    b=(Fraction(1, 10), Fraction(2, 25), Fraction(-3, 50)),
    tau=Fraction(1, 4),
)

OWN_CONTROL = Family(
    name="own_rational_three_harmonic_control",
    p=Fraction(1, 2),
    a=(Fraction(1, 7), Fraction(-1, 9), Fraction(1, 11)),
    b=(Fraction(1, 13), Fraction(2, 17), Fraction(-1, 19)),
    tau=Fraction(1, 5),
)

ONE_HARMONIC_CONTROL = Family(
    name="one_harmonic_phase_gauge_control",
    p=Fraction(1, 2),
    a=(Fraction(1, 5),),
    b=(Fraction(1, 7),),
    tau=Fraction(1, 4),
)

TRANSLATION_TANGENT_CONTROL = Family(
    name="translation_tangent_three_harmonic_control",
    p=Fraction(1, 2),
    a=(Fraction(1, 6), Fraction(-1, 10), Fraction(1, 14)),
    b=(Fraction(1, 30), Fraction(-1, 25), Fraction(3, 70)),
    tau=Fraction(1, 6),
)


def frac_to_json(x: Fraction) -> str:
    return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)


def complex_coeff(family: Family, lag: int, t: float) -> complex:
    if lag == 0:
        return complex(float(family.p), 0.0)
    k = abs(lag)
    if k > family.m:
        return 0.0j
    a = float(family.a[k - 1])
    b = float(family.b[k - 1])
    # Fourier convention: fhat(r)=int f(x) exp(-2*pi*i*r*x) dx.
    # sin(2*pi*k*x) has coefficient -i/2 at r=k and +i/2 at r=-k.
    imag = -t * b / 2.0 if lag > 0 else t * b / 2.0
    return complex(a / 2.0, imag)


def center_coeff_fraction(family: Family, lag: int) -> Fraction:
    if lag == 0:
        return family.p
    k = abs(lag)
    if k > family.m:
        return Fraction(0)
    return family.a[k - 1] / 2


def direction_imag_fraction(family: Family, lag: int) -> Fraction:
    """Return R_lag where d/dt fhat(lag) = i R_lag."""
    if lag == 0:
        return Fraction(0)
    k = abs(lag)
    if k > family.m:
        return Fraction(0)
    b = family.b[k - 1]
    return -b / 2 if lag > 0 else b / 2


def toeplitz_matrix(family: Family, n: int, t: float) -> np.ndarray:
    return np.array(
        [[complex_coeff(family, i - j, t) for j in range(n)] for i in range(n)],
        dtype=np.complex128,
    )


def exact_event_matrix(K: np.ndarray, mask: int) -> np.ndarray:
    n = K.shape[0]
    M = np.empty_like(K)
    eye = np.eye(n, dtype=np.complex128)
    for i in range(n):
        if (mask >> i) & 1:
            M[i, :] = K[i, :]
        else:
            M[i, :] = eye[i, :] - K[i, :]
    return M


def exact_event_probability(K: np.ndarray, mask: int) -> complex:
    return np.linalg.det(exact_event_matrix(K, mask))


def block_entropy(family: Family, n: int, t: float) -> dict[str, float]:
    K = toeplitz_matrix(family, n, t)
    entropy = 0.0
    total = 0.0
    max_abs_imag = 0.0
    min_prob = float("inf")
    max_prob = 0.0
    min_raw_real = float("inf")
    negative_count = 0
    for mask in range(1 << n):
        z = exact_event_probability(K, mask)
        max_abs_imag = max(max_abs_imag, abs(float(z.imag)))
        p = float(z.real)
        min_raw_real = min(min_raw_real, p)
        if p < -1e-10:
            negative_count += 1
        p = min(1.0, max(0.0, p))
        total += p
        min_prob = min(min_prob, p)
        max_prob = max(max_prob, p)
        if p > 0.0:
            entropy -= p * math.log(p)
    return {
        "H_n": entropy,
        "H_n_over_n": entropy / n,
        "prob_sum": total,
        "prob_sum_error": total - 1.0,
        "max_abs_imag_prob": max_abs_imag,
        "min_prob_clamped": min_prob,
        "max_prob": max_prob,
        "min_raw_real": min_raw_real,
        "negative_count_below_1e-10": negative_count,
    }


def entropy_curve(family: Family, nmax: int) -> list[dict[str, float]]:
    rows = []
    prev_gap = None
    for n in range(1, nmax + 1):
        minus = block_entropy(family, n, -float(family.tau))
        center = block_entropy(family, n, 0.0)
        plus = block_entropy(family, n, float(family.tau))
        finite_gap = 0.5 * (minus["H_n"] + plus["H_n"]) - center["H_n"]
        row = {
            "n": n,
            "H_minus": minus["H_n"],
            "H_center": center["H_n"],
            "H_plus": plus["H_n"],
            "finite_gap": finite_gap,
            "finite_gap_per_site": finite_gap / n,
            "endpoint_entropy_abs_diff": abs(minus["H_n"] - plus["H_n"]),
            "center_upper_Hn_over_n": center["H_n_over_n"],
            "plus_upper_Hn_over_n": plus["H_n_over_n"],
            "minus_upper_Hn_over_n": minus["H_n_over_n"],
            "max_prob_sum_error_abs": max(
                abs(minus["prob_sum_error"]),
                abs(center["prob_sum_error"]),
                abs(plus["prob_sum_error"]),
            ),
            "max_abs_imag_prob": max(
                minus["max_abs_imag_prob"],
                center["max_abs_imag_prob"],
                plus["max_abs_imag_prob"],
            ),
            "min_raw_real": min(
                minus["min_raw_real"], center["min_raw_real"], plus["min_raw_real"]
            ),
            "negative_count_below_1e-10": int(
                minus["negative_count_below_1e-10"]
                + center["negative_count_below_1e-10"]
                + plus["negative_count_below_1e-10"]
            ),
        }
        if prev_gap is not None:
            row["increment_gap"] = finite_gap - prev_gap
        prev_gap = finite_gap
        rows.append(row)
    return rows


def permutation_sign(perm: tuple[int, ...]) -> int:
    inversions = 0
    for i in range(len(perm)):
        pi = perm[i]
        for j in range(i + 1, len(perm)):
            if pi > perm[j]:
                inversions += 1
    return -1 if inversions % 2 else 1


def exact_first_derivative_imag(family: Family, n: int, mask: int) -> Fraction:
    """Coefficient C where p'_mask(0)=i*C, computed exactly over Q."""
    M0: list[list[Fraction]] = []
    R1: list[list[Fraction]] = []
    for i in range(n):
        row0 = []
        row1 = []
        row_is_one = ((mask >> i) & 1) == 1
        for j in range(n):
            lag = i - j
            k0 = center_coeff_fraction(family, lag)
            r1 = direction_imag_fraction(family, lag)
            if row_is_one:
                row0.append(k0)
                row1.append(r1)
            else:
                row0.append((Fraction(1) if i == j else Fraction(0)) - k0)
                row1.append(-r1)
        M0.append(row0)
        R1.append(row1)
    total = Fraction(0)
    for perm in itertools.permutations(range(n)):
        sign = permutation_sign(perm)
        for chosen_row in range(n):
            term = Fraction(sign) * R1[chosen_row][perm[chosen_row]]
            if term == 0:
                continue
            for row in range(n):
                if row != chosen_row:
                    term *= M0[row][perm[row]]
                    if term == 0:
                        break
            total += term
    return total


def exact_derivative_sweep(family: Family, nmax: int) -> list[dict[str, object]]:
    rows = []
    for n in range(1, nmax + 1):
        nonzero = []
        max_abs = Fraction(0)
        for mask in range(1 << n):
            coeff = exact_first_derivative_imag(family, n, mask)
            if coeff:
                nonzero.append({"mask": mask, "imag_coeff": frac_to_json(coeff)})
                max_abs = max(max_abs, abs(coeff))
        rows.append(
            {
                "n": n,
                "events_checked": 1 << n,
                "nonzero_exact_first_derivative_count": len(nonzero),
                "max_abs_exact_imag_coeff": frac_to_json(max_abs),
                "examples": nonzero[:5],
            }
        )
    return rows


def finite_difference_derivative_sweep(
    family: Family, nmax: int, step: float
) -> list[dict[str, float]]:
    rows = []
    for n in range(1, nmax + 1):
        Kp = toeplitz_matrix(family, n, step)
        Km = toeplitz_matrix(family, n, -step)
        max_abs = 0.0
        max_mask = 0
        for mask in range(1 << n):
            deriv = (exact_event_probability(Kp, mask) - exact_event_probability(Km, mask)) / (
                2.0 * step
            )
            val = abs(float(deriv.real)) + abs(float(deriv.imag))
            if val > max_abs:
                max_abs = val
                max_mask = mask
        rows.append({"n": n, "events_checked": 1 << n, "step": step, "max_abs": max_abs, "mask": max_mask})
    return rows


def triangle_margin(family: Family) -> Fraction:
    osc = sum(abs(x) for x in family.a) + family.tau * sum(abs(x) for x in family.b)
    return min(family.p - osc, Fraction(1) - family.p - osc)


def wrap_to_pi(theta: float) -> float:
    return (theta + math.pi) % (2.0 * math.pi) - math.pi


def distance_to_pi_lattice(theta: float) -> float:
    return abs((theta + math.pi / 2.0) % math.pi - math.pi / 2.0)


def phase_diagnostics(family: Family) -> dict[str, object]:
    tau = float(family.tau)
    coeffs = [complex(float(a), -tau * float(b)) for a, b in zip(family.a, family.b)]
    phases = [math.atan2(z.imag, z.real) for z in coeffs]
    tangent_ratios = []
    for k, (a, b) in enumerate(zip(family.a, family.b), start=1):
        tangent_ratios.append(None if a == 0 else b / (k * a))
    tangent_nonnull = [x for x in tangent_ratios if x is not None]
    tangent_translation = bool(tangent_nonnull) and all(x == tangent_nonnull[0] for x in tangent_nonnull)

    # Search for a torus translation that makes all endpoint coefficients real.
    # The residual is zero for a one-harmonic phase and positive when a cycle phase remains.
    best_theta = 0.0
    best_residual = float("inf")
    grid = 20001
    for q in range(grid):
        theta = 2.0 * math.pi * q / grid
        residual = max(
            abs(math.sin(phases[k - 1] + k * theta))
            for k in range(1, family.m + 1)
            if abs(coeffs[k - 1]) > 0
        )
        if residual < best_residual:
            best_residual = residual
            best_theta = theta
    # Refine by a tiny local grid around the best point.
    step = 2.0 * math.pi / grid
    for q in range(-2000, 2001):
        theta = best_theta + q * step / 2000.0
        residual = max(
            abs(math.sin(phases[k - 1] + k * theta))
            for k in range(1, family.m + 1)
            if abs(coeffs[k - 1]) > 0
        )
        if residual < best_residual:
            best_residual = residual
            best_theta = theta

    cycle_1_2_3 = None
    if family.m >= 3:
        cycle_angle = wrap_to_pi(phases[0] + phases[1] - phases[2])
        cycle_1_2_3 = {
            "phase_angle": cycle_angle,
            "distance_to_pi_lattice": distance_to_pi_lattice(cycle_angle),
        }

    return {
        "tau": frac_to_json(family.tau),
        "triangle_margin": frac_to_json(triangle_margin(family)),
        "endpoint_coeff_phases_radians": phases,
        "tangent_ratios_b_over_k_a": [
            None if x is None else frac_to_json(x) for x in tangent_ratios
        ],
        "is_infinitesimal_translation_of_center": tangent_translation,
        "endpoint_evenization_best_theta": best_theta,
        "endpoint_evenization_max_abs_sin_residual": best_residual,
        "cycle_phase_relation_1_plus_2_minus_3": cycle_1_2_3,
    }


def family_to_json(family: Family) -> dict[str, object]:
    return {
        "name": family.name,
        "p": frac_to_json(family.p),
        "a": [frac_to_json(x) for x in family.a],
        "b": [frac_to_json(x) for x in family.b],
        "tau": frac_to_json(family.tau),
        "m": family.m,
    }


def git_value(args: list[str]) -> str:
    try:
        return subprocess.check_output(["git", *args], text=True, stderr=subprocess.DEVNULL).strip()
    except Exception as exc:
        return f"UNAVAILABLE: {exc}"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--nmax", type=int, default=10)
    parser.add_argument("--exact-deriv-nmax", type=int, default=6)
    parser.add_argument("--fd-deriv-nmax", type=int, default=8)
    parser.add_argument("--fd-step", type=float, default=1e-7)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)

    np.set_printoptions(precision=17)
    families = [BENCHMARK, OWN_CONTROL, ONE_HARMONIC_CONTROL, TRANSLATION_TANGENT_CONTROL]

    result = {
        "metadata": {
            "script": str(Path(__file__).resolve()),
            "script_sha256": sha256_file(Path(__file__).resolve()),
            "pid": os.getpid(),
            "command": " ".join([sys.executable, *sys.argv]),
            "python": sys.version,
            "platform": platform.platform(),
            "numpy": np.__version__,
            "git_head": git_value(["rev-parse", "HEAD"]),
            "git_branch": git_value(["branch", "--show-current"]),
            "seed": "deterministic-no-random-seed-used",
            "thread_env": {
                key: os.environ.get(key)
                for key in [
                    "OMP_NUM_THREADS",
                    "OPENBLAS_NUM_THREADS",
                    "MKL_NUM_THREADS",
                    "BLIS_NUM_THREADS",
                    "NUMEXPR_NUM_THREADS",
                ]
            },
            "coverage": {
                "entropy_exact_events_n": f"all 2^n exact configurations for n=1..{args.nmax}",
                "exact_first_derivative_n": f"all 2^n exact configurations for n=1..{args.exact_deriv_nmax}",
                "finite_difference_first_derivative_n": f"all 2^n exact configurations for n=1..{args.fd_deriv_nmax}",
            },
        },
        "families": {},
    }

    for family in families:
        result["families"][family.name] = {
            "parameters": family_to_json(family),
            "phase_diagnostics": phase_diagnostics(family),
            "entropy_curve": entropy_curve(family, args.nmax),
            "exact_first_derivative_at_zero": exact_derivative_sweep(
                family, args.exact_deriv_nmax
            ),
            "finite_difference_first_derivative_at_zero": finite_difference_derivative_sweep(
                family, args.fd_deriv_nmax, args.fd_step
            ),
        }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"out": str(args.out), "pid": os.getpid(), "exit": 0}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
