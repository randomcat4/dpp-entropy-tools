"""Independent DPP entropy probability and directional derivative checks.

This module is intentionally small and explicit. Event probabilities are
computed from inclusion probabilities by inclusion-exclusion:

    P(X = S) = sum_{B subset S^c} (-1)^|B| det K_{S union B}.

For a strictly interior real symmetric positive contraction K and real
symmetric direction V, the determinant derivative for a principal minor A is

    d det(K_A+tV_A)     = det(K_A) tr(K_A^{-1} V_A),
    d2 det(K_A+tV_A)    = det(K_A) (tr(M)^2 - tr(M^2)),
    M                  = K_A^{-1} V_A.

Those minor derivatives are then linearly combined by the same
inclusion-exclusion coefficients to obtain p'_S and p''_S.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import json
import math
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import numpy as np


Array = np.ndarray


def all_masks(n: int) -> range:
    return range(1 << n)


def mask_size(mask: int) -> int:
    return int(mask.bit_count())


def mask_indices(mask: int, n: int) -> List[int]:
    return [i for i in range(n) if (mask >> i) & 1]


def det_principal(K: Array, mask: int) -> float:
    if mask == 0:
        return 1.0
    idx = mask_indices(mask, K.shape[0])
    return float(np.linalg.det(K[np.ix_(idx, idx)]))


def inclusion_minors(K: Array) -> Array:
    n = K.shape[0]
    return np.array([det_principal(K, mask) for mask in all_masks(n)], dtype=float)


def event_probs_from_inclusion_minors(minors: Sequence[float], n: int) -> Array:
    probs = np.zeros(1 << n, dtype=float)
    full = (1 << n) - 1
    for s in all_masks(n):
        comp = full ^ s
        b = comp
        total = 0.0
        while True:
            a = s | b
            sign = -1.0 if (mask_size(b) & 1) else 1.0
            total += sign * float(minors[a])
            if b == 0:
                break
            b = (b - 1) & comp
        probs[s] = total
    return probs


def event_probs(K: Array) -> Array:
    return event_probs_from_inclusion_minors(inclusion_minors(K), K.shape[0])


def entropy_from_probs(probs: Sequence[float]) -> float:
    total = 0.0
    for p in probs:
        if p < -1e-10:
            raise ValueError(f"negative event probability {p}")
        if p > 0.0:
            total -= float(p) * math.log(float(p))
    return total


def dpp_entropy(K: Array) -> float:
    return entropy_from_probs(event_probs(K))


@dataclass(frozen=True)
class DirectionalEntropy:
    probs: Array
    prob_d1: Array
    prob_d2: Array
    entropy: float
    entropy_d1: float
    entropy_d2: float
    sum_prob: float
    sum_prob_d1: float
    sum_prob_d2: float


def minor_derivatives(K: Array, V: Array) -> Tuple[Array, Array, Array]:
    n = K.shape[0]
    minors = np.zeros(1 << n, dtype=float)
    d1 = np.zeros(1 << n, dtype=float)
    d2 = np.zeros(1 << n, dtype=float)
    minors[0] = 1.0
    for mask in all_masks(n):
        if mask == 0:
            continue
        idx = mask_indices(mask, n)
        KA = K[np.ix_(idx, idx)]
        VA = V[np.ix_(idx, idx)]
        det = float(np.linalg.det(KA))
        M = np.linalg.solve(KA, VA)
        tr = float(np.trace(M))
        tr2 = float(np.trace(M @ M))
        minors[mask] = det
        d1[mask] = det * tr
        d2[mask] = det * (tr * tr - tr2)
    return minors, d1, d2


def event_prob_derivatives(K: Array, V: Array) -> Tuple[Array, Array, Array]:
    n = K.shape[0]
    minors, minor_d1, minor_d2 = minor_derivatives(K, V)
    return (
        event_probs_from_inclusion_minors(minors, n),
        event_probs_from_inclusion_minors(minor_d1, n),
        event_probs_from_inclusion_minors(minor_d2, n),
    )


def entropy_directional(K: Array, V: Array) -> DirectionalEntropy:
    probs, p1, p2 = event_prob_derivatives(K, V)
    if np.min(probs) <= 0.0:
        raise ValueError("K is not strict enough: a DPP event probability is nonpositive")
    entropy = entropy_from_probs(probs)
    logs_plus_one = np.log(probs) + 1.0
    entropy_d1 = -float(np.dot(p1, logs_plus_one))
    entropy_d2 = -float(np.dot(p2, logs_plus_one)) - float(np.dot(p1 * p1, 1.0 / probs))
    return DirectionalEntropy(
        probs=probs,
        prob_d1=p1,
        prob_d2=p2,
        entropy=entropy,
        entropy_d1=entropy_d1,
        entropy_d2=entropy_d2,
        sum_prob=float(np.sum(probs)),
        sum_prob_d1=float(np.sum(p1)),
        sum_prob_d2=float(np.sum(p2)),
    )


def random_orthogonal(rng: np.random.Generator, n: int) -> Array:
    Q, R = np.linalg.qr(rng.normal(size=(n, n)))
    signs = np.sign(np.diag(R))
    signs[signs == 0.0] = 1.0
    return Q * signs


def random_strict_kernel(rng: np.random.Generator, n: int) -> Array:
    Q = random_orthogonal(rng, n)
    eigs = rng.uniform(0.18, 0.82, size=n)
    K = Q @ np.diag(eigs) @ Q.T
    return 0.5 * (K + K.T)


def random_symmetric_direction(rng: np.random.Generator, n: int) -> Array:
    A = rng.normal(size=(n, n))
    V = 0.5 * (A + A.T)
    norm = float(np.linalg.norm(V, "fro"))
    if norm == 0.0:
        raise ValueError("zero random direction")
    return V / norm


def min_spectral_margin(K: Array) -> float:
    eig_k = np.linalg.eigvalsh(K)
    eig_i_minus_k = np.linalg.eigvalsh(np.eye(K.shape[0]) - K)
    return float(min(np.min(eig_k), np.min(eig_i_minus_k)))


def finite_difference_row(K: Array, V: Array, h: float) -> Dict[str, float]:
    analytic = entropy_directional(K, V)
    Hp = dpp_entropy(K + h * V)
    Hm = dpp_entropy(K - h * V)
    fd1 = (Hp - Hm) / (2.0 * h)
    fd2 = (Hp - 2.0 * analytic.entropy + Hm) / (h * h)

    pp = event_probs(K + h * V)
    pm = event_probs(K - h * V)
    p_fd1 = (pp - pm) / (2.0 * h)
    p_fd2 = (pp - 2.0 * analytic.probs + pm) / (h * h)

    return {
        "h": h,
        "fd_entropy_d1": fd1,
        "fd_entropy_d2": fd2,
        "abs_err_entropy_d1": abs(fd1 - analytic.entropy_d1),
        "abs_err_entropy_d2": abs(fd2 - analytic.entropy_d2),
        "max_abs_err_prob_d1": float(np.max(np.abs(p_fd1 - analytic.prob_d1))),
        "max_abs_err_prob_d2": float(np.max(np.abs(p_fd2 - analytic.prob_d2))),
        "min_prob_plus": float(np.min(pp)),
        "min_prob_minus": float(np.min(pm)),
        "sum_prob_plus": float(np.sum(pp)),
        "sum_prob_minus": float(np.sum(pm)),
    }


def finite_difference_case(n: int, seed: int, steps: Sequence[float]) -> Dict[str, object]:
    rng = np.random.default_rng(seed)
    K = random_strict_kernel(rng, n)
    V = random_symmetric_direction(rng, n)
    margin = min_spectral_margin(K)
    rows = [finite_difference_row(K, V, h) for h in steps]
    analytic = entropy_directional(K, V)
    c = -1.7
    scaled = entropy_directional(K, c * V)
    return {
        "n": n,
        "seed": seed,
        "spectral_margin_K": margin,
        "direction_fro_norm": float(np.linalg.norm(V, "fro")),
        "entropy": analytic.entropy,
        "entropy_d1": analytic.entropy_d1,
        "entropy_d2": analytic.entropy_d2,
        "sum_prob": analytic.sum_prob,
        "min_prob": float(np.min(analytic.probs)),
        "sum_prob_d1": analytic.sum_prob_d1,
        "sum_prob_d2": analytic.sum_prob_d2,
        "finite_difference": rows,
        "direction_scaling": {
            "scale": c,
            "d1_abs_err": abs(scaled.entropy_d1 - c * analytic.entropy_d1),
            "d2_abs_err": abs(scaled.entropy_d2 - c * c * analytic.entropy_d2),
        },
    }


FractionMatrix = List[List[Fraction]]


def rational_test_kernel() -> FractionMatrix:
    return [
        [Fraction(1, 3), Fraction(1, 20), Fraction(1, 30)],
        [Fraction(1, 20), Fraction(2, 5), Fraction(1, 25)],
        [Fraction(1, 30), Fraction(1, 25), Fraction(1, 4)],
    ]


def mat_identity(n: int) -> FractionMatrix:
    return [[Fraction(int(i == j), 1) for j in range(n)] for i in range(n)]


def mat_subtract(A: FractionMatrix, B: FractionMatrix) -> FractionMatrix:
    n = len(A)
    return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]


def mat_add(A: FractionMatrix, B: FractionMatrix) -> FractionMatrix:
    n = len(A)
    return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]


def matmul(A: FractionMatrix, B: FractionMatrix) -> FractionMatrix:
    n = len(A)
    m = len(B[0])
    mid = len(B)
    return [[sum(A[i][k] * B[k][j] for k in range(mid)) for j in range(m)] for i in range(n)]


def submatrix_fraction(A: FractionMatrix, mask: int) -> FractionMatrix:
    n = len(A)
    idx = mask_indices(mask, n)
    return [[A[i][j] for j in idx] for i in idx]


def det_fraction(A: FractionMatrix) -> Fraction:
    n = len(A)
    if n == 0:
        return Fraction(1, 1)
    M = [row[:] for row in A]
    det = Fraction(1, 1)
    sign = 1
    for col in range(n):
        pivot = None
        for row in range(col, n):
            if M[row][col] != 0:
                pivot = row
                break
        if pivot is None:
            return Fraction(0, 1)
        if pivot != col:
            M[col], M[pivot] = M[pivot], M[col]
            sign *= -1
        pivot_value = M[col][col]
        det *= pivot_value
        for row in range(col + 1, n):
            factor = M[row][col] / pivot_value
            if factor == 0:
                continue
            for j in range(col, n):
                M[row][j] -= factor * M[col][j]
    return det if sign > 0 else -det


def inverse_fraction(A: FractionMatrix) -> FractionMatrix:
    n = len(A)
    M = [A[i][:] + mat_identity(n)[i][:] for i in range(n)]
    for col in range(n):
        pivot = None
        for row in range(col, n):
            if M[row][col] != 0:
                pivot = row
                break
        if pivot is None:
            raise ValueError("singular matrix")
        if pivot != col:
            M[col], M[pivot] = M[pivot], M[col]
        scale = M[col][col]
        for j in range(2 * n):
            M[col][j] /= scale
        for row in range(n):
            if row == col:
                continue
            factor = M[row][col]
            if factor == 0:
                continue
            for j in range(2 * n):
                M[row][j] -= factor * M[col][j]
    return [row[n:] for row in M]


def event_probs_fraction_ie(K: FractionMatrix) -> List[Fraction]:
    n = len(K)
    minors = [det_fraction(submatrix_fraction(K, mask)) for mask in all_masks(n)]
    probs: List[Fraction] = []
    full = (1 << n) - 1
    for s in all_masks(n):
        comp = full ^ s
        b = comp
        total = Fraction(0, 1)
        while True:
            sign = -1 if (mask_size(b) & 1) else 1
            total += sign * minors[s | b]
            if b == 0:
                break
            b = (b - 1) & comp
        probs.append(total)
    return probs


def event_probs_fraction_l_ensemble(K: FractionMatrix) -> List[Fraction]:
    n = len(K)
    I = mat_identity(n)
    L = matmul(K, inverse_fraction(mat_subtract(I, K)))
    denom = det_fraction(mat_add(I, L))
    probs = []
    for s in all_masks(n):
        probs.append(det_fraction(submatrix_fraction(L, s)) / denom)
    return probs


def exact_probability_check() -> Dict[str, object]:
    K = rational_test_kernel()
    n = len(K)
    I = mat_identity(n)
    probs_ie = event_probs_fraction_ie(K)
    probs_l = event_probs_fraction_l_ensemble(K)
    principal_k = [det_fraction(submatrix_fraction(K, mask)) for mask in all_masks(n)]
    principal_i_minus_k = [
        det_fraction(submatrix_fraction(mat_subtract(I, K), mask)) for mask in all_masks(n)
    ]
    if probs_ie != probs_l:
        raise AssertionError("exact IE probabilities differ from exact L-ensemble probabilities")
    return {
        "n": n,
        "kernel": [[str(x) for x in row] for row in K],
        "probabilities": [
            {
                "mask": mask,
                "set": mask_indices(mask, n),
                "fraction": str(p),
                "decimal": float(p),
            }
            for mask, p in enumerate(probs_ie)
        ],
        "sum_prob_fraction": str(sum(probs_ie, Fraction(0, 1))),
        "min_prob_fraction": str(min(probs_ie)),
        "max_denominator": max(p.denominator for p in probs_ie),
        "min_principal_minor_K": str(min(principal_k[1:])),
        "min_principal_minor_I_minus_K": str(min(principal_i_minus_k[1:])),
        "l_ensemble_cross_check": "exact_match",
    }


def compact_fd_summary(case: Dict[str, object]) -> Dict[str, float]:
    rows = case["finite_difference"]
    best_h1 = min(rows, key=lambda r: r["abs_err_entropy_d1"])
    best_h2 = min(rows, key=lambda r: r["abs_err_entropy_d2"])
    return {
        "best_h_for_d1": best_h1["h"],
        "best_abs_err_entropy_d1": best_h1["abs_err_entropy_d1"],
        "best_h_for_d2": best_h2["h"],
        "best_abs_err_entropy_d2": best_h2["abs_err_entropy_d2"],
        "worst_sum_prob_deviation": max(
            abs(r["sum_prob_plus"] - 1.0) + abs(r["sum_prob_minus"] - 1.0) for r in rows
        ),
        "smallest_fd_event_probability": min(
            min(r["min_prob_plus"], r["min_prob_minus"]) for r in rows
        ),
    }


def run_all_checks() -> Dict[str, object]:
    steps = [1e-2, 3e-3, 1e-3, 3e-4, 1e-4]
    cases = [finite_difference_case(n, 90210 + n, steps) for n in range(2, 6)]
    return {
        "description": "Independent inclusion-exclusion DPP entropy derivative checks",
        "numpy_version": np.__version__,
        "steps": steps,
        "exact_probability_check": exact_probability_check(),
        "finite_difference_cases": cases,
        "finite_difference_summary": [compact_fd_summary(case) for case in cases],
        "limits": {
            "n_values": "2..5",
            "seeds": [90210 + n for n in range(2, 6)],
            "threads_requested": "local only; no remote compute used after load inspection",
            "gpu": "not used",
        },
    }


def to_jsonable(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, np.floating):
        return float(obj)
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, Path):
        return str(obj)
    raise TypeError(f"cannot serialize {type(obj)!r}")


def main() -> None:
    out_dir = Path(__file__).resolve().parent
    log_dir = out_dir / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    results = run_all_checks()
    log_path = log_dir / "checks.json"
    log_path.write_text(json.dumps(results, indent=2, default=to_jsonable), encoding="utf-8")

    print("DPP entropy derivative checks")
    print(f"log={log_path}")
    exact = results["exact_probability_check"]
    print(
        "exact rational n={n}: sum={sum_prob_fraction}, min={min_prob_fraction}, "
        "max_den={max_denominator}, L-check={l_ensemble_cross_check}".format(**exact)
    )
    for case, summary in zip(
        results["finite_difference_cases"], results["finite_difference_summary"]
    ):
        scaling = case["direction_scaling"]
        print(
            "n={n} seed={seed} margin={margin:.3e} min_p={min_p:.3e} "
            "sum_p-1={sum_err:.3e} sum_p1={sum_p1:.3e} sum_p2={sum_p2:.3e} "
            "best_d1_err={d1:.3e}@h={h1:g} best_d2_err={d2:.3e}@h={h2:g} "
            "scale_d1_err={sd1:.3e} scale_d2_err={sd2:.3e}".format(
                n=case["n"],
                seed=case["seed"],
                margin=case["spectral_margin_K"],
                min_p=case["min_prob"],
                sum_err=abs(case["sum_prob"] - 1.0),
                sum_p1=case["sum_prob_d1"],
                sum_p2=case["sum_prob_d2"],
                d1=summary["best_abs_err_entropy_d1"],
                h1=summary["best_h_for_d1"],
                d2=summary["best_abs_err_entropy_d2"],
                h2=summary["best_h_for_d2"],
                sd1=scaling["d1_abs_err"],
                sd2=scaling["d2_abs_err"],
            )
        )


if __name__ == "__main__":
    main()
