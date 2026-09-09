#!/usr/bin/env python3
"""Independent bounded checks for the S1 round-2 mixed Toeplitz baseline.

This script deliberately implements the finite-window event probabilities and
jets from the definition rather than importing the author's round-2 code.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import platform
import subprocess
import sys
import time
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np


BASIS_NAMES = ["p", "a1", "a2", "a3", "b1", "b2", "b3"]


def frac(s: str) -> Fraction:
    return Fraction(s)


def frac_abs(x: Fraction) -> Fraction:
    return abs(x)


def fstr(x: Fraction) -> str:
    return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git_commit(path: Path) -> str | None:
    try:
        out = subprocess.check_output(
            ["git", "-C", str(path), "rev-parse", "HEAD"],
            stderr=subprocess.DEVNULL,
            text=True,
        )
        return out.strip()
    except Exception:
        return None


def load_candidate(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return data


def candidate_to_fractions(data: dict[str, Any]) -> dict[str, Any]:
    return {
        "p": frac(data["p"]),
        "a": [frac(x) for x in data["a"]],
        "b": [frac(x) for x in data["b"]],
        "dp": frac(data["dp"]),
        "da": [frac(x) for x in data["da"]],
        "db": [frac(x) for x in data["db"]],
        "tau": frac(data["tau"]),
        "uniform_margin": frac(data["uniform_margin"]),
    }


def triangle_margin(c: dict[str, Any]) -> dict[str, Any]:
    tau = c["tau"]
    osc = tau * frac_abs(c["dp"])
    for x, dx in zip(c["a"], c["da"]):
        osc += frac_abs(x) + tau * frac_abs(dx)
    for x, dx in zip(c["b"], c["db"]):
        osc += frac_abs(x) + tau * frac_abs(dx)
    lower = c["p"] - osc
    upper = c["p"] + osc
    eps = min(lower, 1 - upper)
    return {
        "oscillation_bound": fstr(osc),
        "lower_bound": fstr(lower),
        "upper_bound": fstr(upper),
        "epsilon_from_triangle": fstr(eps),
        "claimed_margin": fstr(c["uniform_margin"]),
        "claimed_margin_certified": eps >= c["uniform_margin"],
    }


def cplx_pair_mul(x: tuple[Fraction, Fraction], y: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
    xr, xi = x
    yr, yi = y
    return xr * yr - xi * yi, xr * yi + xi * yr


def cplx_pair_conj(x: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
    return x[0], -x[1]


def center_fourier_pairs(c: dict[str, Any]) -> list[tuple[Fraction, Fraction]]:
    pairs = []
    for ak, bk in zip(c["a"], c["b"]):
        pairs.append((ak / 2, -bk / 2))
    return pairs


def gauge_diagnostics(c: dict[str, Any]) -> dict[str, Any]:
    pairs = center_fourier_pairs(c)
    c1, c2, c3 = pairs[:3]
    inv112 = cplx_pair_mul(cplx_pair_mul(c1, c1), cplx_pair_conj(c2))
    inv1113 = cplx_pair_mul(cplx_pair_mul(cplx_pair_mul(c1, c1), c1), cplx_pair_conj(c3))
    t = c["tau"]
    p_minus = c["p"] - t * c["dp"]
    p_plus = c["p"] + t * c["dp"]
    a_minus = [x - t * dx for x, dx in zip(c["a"], c["da"])]
    a_plus = [x + t * dx for x, dx in zip(c["a"], c["da"])]
    b_minus = [x - t * dx for x, dx in zip(c["b"], c["db"])]
    b_plus = [x + t * dx for x, dx in zip(c["b"], c["db"])]
    reflected_equal = (p_minus == p_plus) and (a_minus == a_plus) and (b_minus == [-x for x in b_plus])
    same_coefficients = (p_minus == p_plus) and (a_minus == a_plus) and (b_minus == b_plus)
    return {
        "center_has_sine_terms": any(x != 0 for x in c["b"]),
        "center_cycle_c1_c1_conj_c2": {"real": fstr(inv112[0]), "imag": fstr(inv112[1])},
        "center_cycle_c1_c1_c1_conj_c3": {"real": fstr(inv1113[0]), "imag": fstr(inv1113[1])},
        "translation_to_even_obstructed_by_nonzero_cycle_imag": inv112[1] != 0 or inv1113[1] != 0,
        "endpoint_p_minus": fstr(p_minus),
        "endpoint_p_plus": fstr(p_plus),
        "endpoint_same_coefficients": same_coefficients,
        "endpoint_reflection_conjugate_equal": reflected_equal,
        "endpoint_not_translation_equivalent_by_mean": p_minus != p_plus,
    }


def params_at(c: dict[str, Any], t: float) -> tuple[float, list[float], list[float]]:
    p = float(c["p"]) + t * float(c["dp"])
    a = [float(x) + t * float(dx) for x, dx in zip(c["a"], c["da"])]
    b = [float(x) + t * float(dx) for x, dx in zip(c["b"], c["db"])]
    return p, a, b


def coeffs_from_params(p: float, a: list[float], b: list[float]) -> dict[int, complex]:
    coeffs: dict[int, complex] = {0: complex(p, 0.0)}
    for k, (ak, bk) in enumerate(zip(a, b), start=1):
        coeffs[k] = complex(ak / 2.0, -bk / 2.0)
        coeffs[-k] = complex(ak / 2.0, bk / 2.0)
    return coeffs


def basis_coeffs(m: int = 3) -> list[dict[int, complex]]:
    out: list[dict[int, complex]] = []
    out.append({0: 1.0 + 0.0j})
    for k in range(1, m + 1):
        out.append({k: 0.5 + 0.0j, -k: 0.5 + 0.0j})
    for k in range(1, m + 1):
        out.append({k: -0.5j, -k: 0.5j})
    return out


def toeplitz(n: int, coeffs: dict[int, complex]) -> np.ndarray:
    K = np.zeros((n, n), dtype=np.complex128)
    for i in range(n):
        for j in range(n):
            K[i, j] = coeffs.get(i - j, 0.0 + 0.0j)
    return K


def event_matrix_from(K: np.ndarray, mask: int) -> np.ndarray:
    n = K.shape[0]
    M = np.empty_like(K)
    eye = np.eye(n, dtype=np.complex128)
    for i in range(n):
        if (mask >> i) & 1:
            M[i, :] = K[i, :]
        else:
            M[i, :] = eye[i, :] - K[i, :]
    return M


def event_direction_from(D: np.ndarray, mask: int) -> np.ndarray:
    n = D.shape[0]
    E = np.empty_like(D)
    for i in range(n):
        if (mask >> i) & 1:
            E[i, :] = D[i, :]
        else:
            E[i, :] = -D[i, :]
    return E


def entropy_at(c: dict[str, Any], n: int, t: float) -> dict[str, Any]:
    p, a, b = params_at(c, t)
    K = toeplitz(n, coeffs_from_params(p, a, b))
    probs = []
    max_imag = 0.0
    min_prob = float("inf")
    for mask in range(1 << n):
        det = np.linalg.det(event_matrix_from(K, mask))
        max_imag = max(max_imag, abs(float(np.imag(det))))
        val = float(np.real(det))
        probs.append(val)
        min_prob = min(min_prob, val)
    arr = np.array(probs, dtype=np.float64)
    H = -float(np.sum(arr * np.log(arr)))
    return {
        "entropy": H,
        "sum_prob": float(np.sum(arr)),
        "min_prob": min_prob,
        "max_det_imag_abs": max_imag,
        "max_prob_residual_abs": float(np.max(np.abs(arr))),
    }


def jet_at_center(c: dict[str, Any], n: int) -> dict[str, Any]:
    p0, a0, b0 = params_at(c, 0.0)
    K0 = toeplitz(n, coeffs_from_params(p0, a0, b0))
    Bs = [toeplitz(n, z) for z in basis_coeffs(3)]
    direction = np.array(
        [float(c["dp"])] + [float(x) for x in c["da"]] + [float(x) for x in c["db"]],
        dtype=np.float64,
    )
    dim = len(Bs)
    sum_prob = 0.0
    sum_grad = np.zeros(dim, dtype=np.float64)
    sum_hess_prob = np.zeros((dim, dim), dtype=np.float64)
    fisher = np.zeros((dim, dim), dtype=np.float64)
    acceleration = np.zeros((dim, dim), dtype=np.float64)
    max_det_imag = 0.0
    max_grad_imag = 0.0
    max_hess_imag = 0.0
    max_fixed_pprime_abs = 0.0
    max_basis_pprime_abs = 0.0
    min_prob = float("inf")
    max_cond = 0.0
    for mask in range(1 << n):
        M = event_matrix_from(K0, mask)
        Dms = [event_direction_from(B, mask) for B in Bs]
        det = np.linalg.det(M)
        p = float(np.real(det))
        max_det_imag = max(max_det_imag, abs(float(np.imag(det))))
        min_prob = min(min_prob, p)
        A = np.linalg.inv(M)
        max_cond = max(max_cond, float(np.linalg.cond(M)))
        traces = np.array([np.trace(A @ D) for D in Dms], dtype=np.complex128)
        grad_c = det * traces
        hess_c = np.empty((dim, dim), dtype=np.complex128)
        for r in range(dim):
            AD_r = A @ Dms[r]
            for s in range(dim):
                hess_c[r, s] = det * (traces[r] * traces[s] - np.trace(AD_r @ A @ Dms[s]))
        max_grad_imag = max(max_grad_imag, float(np.max(np.abs(np.imag(grad_c)))))
        max_hess_imag = max(max_hess_imag, float(np.max(np.abs(np.imag(hess_c)))))
        grad = np.real(grad_c).astype(np.float64)
        hess_prob = np.real(hess_c).astype(np.float64)
        sum_prob += p
        sum_grad += grad
        sum_hess_prob += hess_prob
        fixed_pprime = float(direction @ grad)
        max_fixed_pprime_abs = max(max_fixed_pprime_abs, abs(fixed_pprime))
        max_basis_pprime_abs = max(max_basis_pprime_abs, float(np.max(np.abs(grad))))
        fisher += np.outer(grad, grad) / p
        acceleration += -hess_prob * math.log(p)
    entropy_hess = acceleration - fisher
    entropy_hess_sym = 0.5 * (entropy_hess + entropy_hess.T)
    eigvals = np.linalg.eigvalsh(entropy_hess_sym)
    fixed_fisher = float(direction @ fisher @ direction)
    fixed_accel = float(direction @ acceleration @ direction)
    fixed_h2 = float(direction @ entropy_hess_sym @ direction)
    return {
        "event_count": 1 << n,
        "sum_prob": sum_prob,
        "min_prob": min_prob,
        "sum_grad_linf": float(np.max(np.abs(sum_grad))),
        "sum_hess_prob_linf": float(np.max(np.abs(sum_hess_prob))),
        "max_det_imag_abs": max_det_imag,
        "max_grad_imag_abs": max_grad_imag,
        "max_hess_imag_abs": max_hess_imag,
        "max_condition_number": max_cond,
        "max_basis_pprime_abs": max_basis_pprime_abs,
        "max_fixed_direction_pprime_abs": max_fixed_pprime_abs,
        "entropy_hessian_basis": BASIS_NAMES,
        "entropy_hessian_eigenvalues": [float(x) for x in eigvals],
        "entropy_hessian_max_eigenvalue": float(eigvals[-1]),
        "fixed_direction_coefficients": dict(zip(BASIS_NAMES, [float(x) for x in direction])),
        "fixed_direction_h2": fixed_h2,
        "fixed_direction_fisher_positive": fixed_fisher,
        "fixed_direction_acceleration": fixed_accel,
        "fixed_direction_recombines": float(fixed_accel - fixed_fisher),
    }


def finite_gap(c: dict[str, Any], n: int) -> dict[str, Any]:
    tau = float(c["tau"])
    hm = entropy_at(c, n, -tau)
    h0 = entropy_at(c, n, 0.0)
    hp = entropy_at(c, n, tau)
    gap = 0.5 * (hm["entropy"] + hp["entropy"]) - h0["entropy"]
    return {
        "H_minus_tau": hm["entropy"],
        "H_0": h0["entropy"],
        "H_plus_tau": hp["entropy"],
        "midpoint_gap": gap,
        "endpoint_sum_prob_residual_max": max(abs(hm["sum_prob"] - 1), abs(h0["sum_prob"] - 1), abs(hp["sum_prob"] - 1)),
        "endpoint_min_prob": min(hm["min_prob"], h0["min_prob"], hp["min_prob"]),
        "endpoint_max_det_imag_abs": max(hm["max_det_imag_abs"], h0["max_det_imag_abs"], hp["max_det_imag_abs"]),
    }


def make_report(args: argparse.Namespace) -> dict[str, Any]:
    start = time.perf_counter()
    candidate_path = Path(args.candidate)
    output_path = Path(args.output)
    raw = load_candidate(candidate_path)
    c = candidate_to_fractions(raw)
    n_values = [int(x) for x in args.n.split(",") if x.strip()]
    results = {
        "status": "INDEPENDENT_BASELINE_CHECK",
        "candidate_id": raw.get("id"),
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "record": {
            "python": sys.version.replace("\n", " "),
            "executable_name": Path(sys.executable).name,
            "platform": platform.platform(),
            "numpy": np.__version__,
            "pid": os.getpid(),
            "seed": "deterministic-no-random-seed-used",
            "thread_env": {
                "OMP_NUM_THREADS": os.environ.get("OMP_NUM_THREADS"),
                "OPENBLAS_NUM_THREADS": os.environ.get("OPENBLAS_NUM_THREADS"),
                "MKL_NUM_THREADS": os.environ.get("MKL_NUM_THREADS"),
                "NUMEXPR_NUM_THREADS": os.environ.get("NUMEXPR_NUM_THREADS"),
            },
            "command_shape": "python research/S1/round2/review/round2_baseline_review.py --candidate <main-repo>/research/S1/round2/baseline_candidate.json --output research/S1/round2/review/round2_baseline_review_result.json --n "
            + args.n,
            "script_sha256": sha256_file(Path(__file__)),
            "candidate_sha256": sha256_file(candidate_path),
            "main_repo_commit": git_commit(Path(args.main_repo)) if args.main_repo else None,
            "review_repo_commit": git_commit(Path(args.review_repo)) if args.review_repo else None,
        },
        "candidate_shape": {
            "fixed_independent_of_window": bool(raw.get("fixed_independent_of_window")),
            "endpoint_equality_assumed": bool(raw.get("endpoint_equality_assumed")),
            "degree": len(c["a"]),
            "p": fstr(c["p"]),
            "tau": fstr(c["tau"]),
        },
        "uniform_margin": triangle_margin(c),
        "gauge_and_endpoints": gauge_diagnostics(c),
        "n_results": {},
    }
    for n in n_values:
        results["n_results"][str(n)] = {
            "finite_gap": finite_gap(c, n),
            "center_all_event_jet": jet_at_center(c, n),
        }
    results["record"]["elapsed_seconds"] = time.perf_counter() - start
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(results, indent=2, sort_keys=True), encoding="utf-8")
    return results


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidate", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--n", default="6,8")
    ap.add_argument("--main-repo", default="")
    ap.add_argument("--review-repo", default="")
    args = ap.parse_args()
    report = make_report(args)
    print(json.dumps({
        "status": report["status"],
        "candidate_id": report["candidate_id"],
        "n": sorted(report["n_results"].keys(), key=int),
        "pid": report["record"]["pid"],
        "elapsed_seconds": report["record"]["elapsed_seconds"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
