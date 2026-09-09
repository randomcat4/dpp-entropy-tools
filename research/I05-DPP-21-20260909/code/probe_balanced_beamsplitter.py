#!/usr/bin/env python3
"""
Bounded diagnostic for the DPP21 balanced-fermionic-beam-splitter bridge.

This program is NOT a proof. It uses ordinary IEEE double precision and a
finite list of fixed Toeplitz kernels. Its purpose is to cross-check:
  (i) complete DPP probabilities by signed event determinants,
 (ii) their equality with the occupation diagonal of the quasifree state,
(iii) the balanced beam-splitter covariance and both output marginals, and
 (iv) the two finite entropy gaps in proof.md (5.5)--(5.9).

No finite result is extrapolated to an entropy rate.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Iterable

import numpy as np


def occupied(mask: int, n: int) -> list[int]:
    return [i for i in range(n) if (mask >> i) & 1]


def entropy(prob: np.ndarray) -> float:
    p = np.real_if_close(prob, tol=1000).real.astype(float)
    if float(np.min(p)) < -2e-11:
        raise ValueError(f"negative probability {float(np.min(p))}")
    p = np.maximum(p, 0.0)
    p /= float(np.sum(p))
    nz = p > 0.0
    return float(-np.sum(p[nz] * np.log(p[nz])))


def complete_dpp_probabilities(K: np.ndarray) -> np.ndarray:
    """Signed determinant formula for every complete event."""
    n = K.shape[0]
    out = np.empty(1 << n, dtype=float)
    eye = np.eye(n, dtype=complex)
    for mask in range(1 << n):
        zeros = [i for i in range(n) if not ((mask >> i) & 1)]
        M = K.astype(complex).copy()
        if zeros:
            M[np.ix_(zeros, zeros)] -= eye[np.ix_(zeros, zeros)]
        sign = -1.0 if len(zeros) % 2 else 1.0
        out[mask] = float(np.real_if_close(sign * np.linalg.det(M)))
    return out


def quasifree_density(K: np.ndarray) -> np.ndarray:
    """Gauge-invariant quasifree density in the occupation basis."""
    n = K.shape[0]
    L = K @ np.linalg.inv(np.eye(n) - K)
    prefactor = np.linalg.det(np.eye(n) - K)
    rho = np.zeros((1 << n, 1 << n), dtype=complex)
    bitsets = [occupied(mask, n) for mask in range(1 << n)]
    for s, S in enumerate(bitsets):
        for t, T in enumerate(bitsets):
            if len(S) != len(T):
                continue
            rho[s, t] = prefactor if not S else prefactor * np.linalg.det(L[np.ix_(S, T)])
    return (rho + rho.conj().T) / 2.0


def second_quantization(W: np.ndarray) -> np.ndarray:
    """Fock representation: matrix elements are exterior-power minors."""
    n = W.shape[0]
    dim = 1 << n
    U = np.zeros((dim, dim), dtype=complex)
    bitsets = [occupied(mask, n) for mask in range(dim)]
    for s, S in enumerate(bitsets):
        for t, T in enumerate(bitsets):
            if len(S) != len(T):
                continue
            U[s, t] = 1.0 if not S else np.linalg.det(W[np.ix_(S, T)])
    return U


def product_density(rho0: np.ndarray, rho1: np.ndarray) -> np.ndarray:
    """Product in mode order (copy 0 modes, then copy 1 modes)."""
    d = rho0.shape[0]
    n = int(round(math.log2(d)))
    out = np.zeros((d * d, d * d), dtype=complex)
    for s0 in range(d):
        for s1 in range(d):
            s = s0 | (s1 << n)
            for t0 in range(d):
                for t1 in range(d):
                    t = t0 | (t1 << n)
                    out[s, t] = rho0[s0, t0] * rho1[s1, t1]
    return out


def marginal_from_joint_prob(q: np.ndarray, n: int, copy: int) -> np.ndarray:
    out = np.zeros(1 << n, dtype=float)
    for mask, value in enumerate(q):
        part = (mask & ((1 << n) - 1)) if copy == 0 else (mask >> n)
        out[part] += float(value)
    return out


def toeplitz_pr39(n: int, t: float) -> np.ndarray:
    """Kernel for c=1/2+cos(4pi theta)/8, g=cos(2pi theta)/1024."""
    coeff = {
        0: 0.5,
        2: 1.0 / 16.0,
        -2: 1.0 / 16.0,
        1: t / 2048.0,
        -1: t / 2048.0,
    }
    return np.array(
        [[coeff.get(i - j, 0.0) for j in range(n)] for i in range(n)],
        dtype=complex,
    )


def run_pair(n: int, t0: float, t1: float) -> dict[str, float | int]:
    K0 = toeplitz_pr39(n, t0)
    K1 = toeplitz_pr39(n, t1)
    M = (K0 + K1) / 2.0

    p0 = complete_dpp_probabilities(K0)
    p1 = complete_dpp_probabilities(K1)
    pm = complete_dpp_probabilities(M)
    rho0 = quasifree_density(K0)
    rho1 = quasifree_density(K1)

    eye = np.eye(n)
    W = np.block([[eye, eye], [-eye, eye]]) / math.sqrt(2.0)
    U = second_quantization(W)
    tau = U @ product_density(rho0, rho1) @ U.conj().T
    q = np.real_if_close(np.diag(tau), tol=1000).real
    q = np.maximum(q, 0.0)
    q /= np.sum(q)

    q0 = marginal_from_joint_prob(q, n, 0)
    q1 = marginal_from_joint_prob(q, n, 1)

    h0, h1, hm, hq = map(entropy, (p0, p1, pm, q))
    input_h = h0 + h1
    midpoint_gap = 2.0 * hm - input_h
    occupation_gain = hq - input_h
    output_mutual_information = 2.0 * hm - hq

    return {
        "n": n,
        "t0": t0,
        "t1": t1,
        "min_eigenvalue_K0": float(np.min(np.linalg.eigvalsh(K0))),
        "max_eigenvalue_K0": float(np.max(np.linalg.eigvalsh(K0))),
        "min_eigenvalue_K1": float(np.min(np.linalg.eigvalsh(K1))),
        "max_eigenvalue_K1": float(np.max(np.linalg.eigvalsh(K1))),
        "probability_sum_error": float(
            max(abs(np.sum(p0) - 1), abs(np.sum(p1) - 1), abs(np.sum(pm) - 1), abs(np.sum(q) - 1))
        ),
        "quasifree_diagonal_error": float(
            max(np.max(abs(np.diag(rho0).real - p0)), np.max(abs(np.diag(rho1).real - p1)))
        ),
        "output_marginal_error": float(max(np.max(abs(q0 - pm)), np.max(abs(q1 - pm)))),
        "unitarity_error": float(np.linalg.norm(U.conj().T @ U - np.eye(U.shape[0]), ord=2)),
        "H_K0": h0,
        "H_K1": h1,
        "H_mid": hm,
        "H_joint_output": hq,
        "midpoint_concavity_gap": midpoint_gap,
        "balanced_occupation_entropy_gain": occupation_gain,
        "output_occupation_mutual_information": output_mutual_information,
        "gap_decomposition_error": float(
            abs(midpoint_gap - (occupation_gain + output_mutual_information))
        ),
    }


def main() -> None:
    cases: Iterable[tuple[int, float, float]] = (
        (4, -1.0, 1.0),
        (4, -100.0, 100.0),
        (4, -384.0, 384.0),
        (4, 0.0, 384.0),
    )
    report = {
        "status": "FINITE_FLOAT_DIAGNOSTIC_ONLY_NOT_A_PROOF",
        "numpy_version": np.__version__,
        "cases": [run_pair(*case) for case in cases],
    }
    path = Path(__file__).resolve().parents[1] / "output" / "balanced_beamsplitter_probe.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
