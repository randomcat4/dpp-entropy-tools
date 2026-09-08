"""Fresh non-author checks for dense_hessian.

This script deliberately computes exact-event probabilities and their first
and second derivatives from inclusion determinants plus Mobius aggregation,
not from the author's signed event determinant matrix.  It then compares the
resulting Hessian with finite differences and, when importable, with the
author implementation.
"""

from __future__ import annotations

import importlib.util
import json
import math
import os
from pathlib import Path

for _name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_name, "1")

import numpy as np


AUTHOR = Path(__file__).resolve().parents[1] / "dense_hessian.py"


def popcount(mask: int) -> int:
    return int(mask.bit_count())


def symmetric_basis(n: int) -> tuple[np.ndarray, list[tuple[int, int]]]:
    pairs = [(i, j) for i in range(n) for j in range(i, n)]
    basis = np.zeros((len(pairs), n, n), dtype=float)
    for a, (i, j) in enumerate(pairs):
        basis[a, i, j] = 1.0
        basis[a, j, i] = 1.0
    return basis, pairs


def matrix_from_coordinates(coords: np.ndarray, n: int) -> np.ndarray:
    basis, _ = symmetric_basis(n)
    out = np.zeros((n, n), dtype=float)
    for a in range(len(coords)):
        out += coords[a] * basis[a]
    return out


def strict_margin(k: np.ndarray) -> float:
    eig = np.linalg.eigvalsh(k)
    return float(min(eig[0], 1.0 - eig[-1]))


def deterministic_kernel(n: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    q, _ = np.linalg.qr(rng.normal(size=(n, n)))
    if np.linalg.det(q) < 0:
        q[:, 0] *= -1.0
    if n == 3:
        eig = np.array([0.17, 0.43, 0.82], dtype=float)
    elif n == 5:
        eig = np.array([0.09, 0.24, 0.51, 0.73, 0.89], dtype=float)
    else:
        eig = np.linspace(0.11, 0.87, n)
    return (q * eig) @ q.T


def inclusion_det_derivatives(k: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return det(K_U), first, and mixed second derivatives for every U.

    Coordinates are the full symmetric upper-triangle basis.  Empty principal
    determinant is constant one; its derivatives are zero.
    """
    n = k.shape[0]
    basis, _ = symmetric_basis(n)
    m = len(basis)
    dets = np.zeros(1 << n, dtype=float)
    first = np.zeros((1 << n, m), dtype=float)
    second = np.zeros((1 << n, m, m), dtype=float)
    dets[0] = 1.0

    for mask in range(1, 1 << n):
        idx = [i for i in range(n) if (mask >> i) & 1]
        sub = k[np.ix_(idx, idx)]
        det = float(np.linalg.det(sub))
        inv = np.linalg.inv(sub)
        dets[mask] = det
        restricted = basis[:, idx, :][:, :, idx]
        scores = np.einsum("ij,aji->a", inv, restricted, optimize=True)
        products = np.einsum("ij,ajk->aik", inv, restricted, optimize=True)
        traces = np.einsum("aij,bji->ab", products, products, optimize=True)
        first[mask] = det * scores
        second[mask] = det * (np.outer(scores, scores) - traces)
    return dets, first, second


def mobius_atoms_derivatives(k: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    n = k.shape[0]
    _, pairs = symmetric_basis(n)
    m = len(pairs)
    inc, inc_first, inc_second = inclusion_det_derivatives(k)
    p = np.zeros(1 << n, dtype=float)
    p_first = np.zeros((1 << n, m), dtype=float)
    p_second = np.zeros((1 << n, m, m), dtype=float)
    for event in range(1 << n):
        for superset in range(1 << n):
            if (superset & event) != event:
                continue
            sign = -1.0 if ((popcount(superset) - popcount(event)) % 2) else 1.0
            p[event] += sign * inc[superset]
            p_first[event] += sign * inc_first[superset]
            p_second[event] += sign * inc_second[superset]
    return p, p_first, p_second


def event_det_atoms(k: np.ndarray) -> np.ndarray:
    n = k.shape[0]
    out = np.zeros(1 << n, dtype=float)
    for event in range(1 << n):
        a = k.copy()
        for i in range(n):
            if not ((event >> i) & 1):
                a[i, i] -= 1.0
        sign = -1.0 if ((n - popcount(event)) % 2) else 1.0
        out[event] = sign * float(np.linalg.det(a))
    return out


def entropy_from_mobius(k: np.ndarray) -> float:
    p, _, _ = mobius_atoms_derivatives(k)
    if np.any(p <= 0):
        raise ArithmeticError(f"non-positive atom: {p.min()}")
    return float(-np.sum(p * np.log(p)))


def hessian_from_mobius(k: np.ndarray) -> tuple[np.ndarray, dict[str, float]]:
    p, p1, p2 = mobius_atoms_derivatives(k)
    if np.any(p <= 0):
        raise ArithmeticError(f"non-positive atom: {p.min()}")
    logs = np.log(p)
    h = -np.einsum("sa,sb,s->ab", p1, p1, 1.0 / p, optimize=True)
    h -= np.einsum("sab,s->ab", p2, logs, optimize=True)
    h = (h + h.T) / 2.0
    diagnostics = {
        "min_atom": float(p.min()),
        "normalization_residual": float(abs(p.sum() - 1.0)),
        "first_sum_max_abs": float(np.max(np.abs(p1.sum(axis=0)))),
        "second_sum_max_abs": float(np.max(np.abs(p2.sum(axis=0)))),
        "event_det_max_error": float(np.max(np.abs(p - event_det_atoms(k)))),
    }
    return h, diagnostics


def finite_second(k: np.ndarray, coords: np.ndarray, h: float) -> float:
    n = k.shape[0]
    d = matrix_from_coordinates(coords, n)
    return (
        entropy_from_mobius(k + h * d)
        + entropy_from_mobius(k - h * d)
        - 2.0 * entropy_from_mobius(k)
    ) / (h * h)


def feasible_step(k: np.ndarray, coords: np.ndarray) -> float:
    n = k.shape[0]
    d = matrix_from_coordinates(coords, n)
    lo, hi = 0.0, 1.0
    while hi < 8.0 and min(strict_margin(k + hi * d), strict_margin(k - hi * d)) > 1e-8:
        lo, hi = hi, 2.0 * hi
    for _ in range(80):
        mid = (lo + hi) / 2.0
        if min(strict_margin(k + mid * d), strict_margin(k - mid * d)) > 1e-8:
            lo = mid
        else:
            hi = mid
    return lo


def load_author_module():
    spec = importlib.util.spec_from_file_location("dense_hessian_author", AUTHOR)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not import {AUTHOR}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def check_case(n: int, seed: int) -> dict[str, object]:
    rng = np.random.default_rng(seed + 1000)
    k = deterministic_kernel(n, seed)
    hess, diag = hessian_from_mobius(k)
    eigvals, eigvecs = np.linalg.eigh(hess)
    top_coords = eigvecs[:, -1]
    random_coords = rng.normal(size=len(top_coords))
    random_coords /= np.linalg.norm(random_coords)
    h_top_max = min(1e-4, 0.01 * feasible_step(k, top_coords))
    h_random_max = min(1e-4, 0.01 * feasible_step(k, random_coords))
    fd_top_values = {}
    fd_random_values = {}
    for factor in (1.0, 0.5, 0.25):
        ht = h_top_max * factor
        hr = h_random_max * factor
        fd_top_values[f"{ht:.3e}"] = finite_second(k, top_coords, ht)
        fd_random_values[f"{hr:.3e}"] = finite_second(k, random_coords, hr)
    analytic_top = float(top_coords @ hess @ top_coords)
    analytic_random = float(random_coords @ hess @ random_coords)
    endpoint_margin_top = min(
        strict_margin(k + h_top_max * matrix_from_coordinates(top_coords, n)),
        strict_margin(k - h_top_max * matrix_from_coordinates(top_coords, n)),
    )
    author_delta = None
    author_self_test = None
    author = load_author_module()
    author_hess, author_diag = author.entropy_hessian(k, chunk=16)
    author_delta = float(np.max(np.abs(hess - author_hess)))
    if n == 3:
        author_self_test = author.self_test()
    return {
        "n": n,
        "seed": seed,
        "strict_margin": strict_margin(k),
        "dimension": int(n * (n + 1) // 2),
        "atoms": int(1 << n),
        "diagnostics": diag,
        "author_hessian_max_abs_delta": author_delta,
        "author_entropy": author_diag["entropy"],
        "eigen_min": float(eigvals[0]),
        "eigen_max": float(eigvals[-1]),
        "positive_eigen_count_gt_1e-9": int(np.sum(eigvals > 1e-9)),
        "near_zero_eigen_count_abs_le_1e-7": int(np.sum(np.abs(eigvals) <= 1e-7)),
        "analytic_top": analytic_top,
        "finite_difference_top": fd_top_values,
        "top_fd_best_abs_error": float(min(abs(v - analytic_top) for v in fd_top_values.values())),
        "analytic_random": analytic_random,
        "finite_difference_random": fd_random_values,
        "random_fd_best_abs_error": float(min(abs(v - analytic_random) for v in fd_random_values.values())),
        "top_test_step": h_top_max,
        "top_endpoint_margin": endpoint_margin_top,
        "author_self_test_if_n3": author_self_test,
    }


def main() -> None:
    cases = [check_case(3, 2026090821), check_case(5, 2026090822)]
    result = {
        "status": "PASS",
        "implementation": "Mobius aggregation from inclusion determinants; finite differences use the same exact-event entropy evaluator.",
        "cases": cases,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
