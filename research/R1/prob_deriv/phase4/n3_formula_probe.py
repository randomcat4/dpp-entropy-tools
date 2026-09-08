"""P4-02 n=3 full-event Hessian formula and bounded falsification probe."""

from __future__ import annotations

from fractions import Fraction
import json
import math
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import numpy as np


def masks(n: int) -> range:
    return range(1 << n)


def idx(mask: int, n: int) -> List[int]:
    return [i for i in range(n) if (mask >> i) & 1]


def event_probs(K: np.ndarray) -> np.ndarray:
    n = len(K)
    q = np.ones(1 << n)
    for mask in masks(n):
        if mask:
            ii = idx(mask, n)
            q[mask] = np.linalg.det(K[np.ix_(ii, ii)])
    p = q.copy()
    for bit in range(n):
        width = 1 << bit
        view = p.reshape((-1, 2, width))
        view[:, 0] -= view[:, 1]
    return p


def entropy_from_probs(p: np.ndarray) -> float:
    if np.any(p <= 0):
        raise FloatingPointError("nonpositive event probability")
    return -float(p @ np.log(p))


def entropy(K: np.ndarray) -> float:
    return entropy_from_probs(event_probs(K))


def minor_derivatives(K: np.ndarray, V: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    n = len(K)
    q = np.ones(1 << n)
    q1 = np.zeros(1 << n)
    q2 = np.zeros(1 << n)
    for mask in masks(n):
        if not mask:
            continue
        ii = idx(mask, n)
        KA = K[np.ix_(ii, ii)]
        VA = V[np.ix_(ii, ii)]
        det = float(np.linalg.det(KA))
        M = np.linalg.solve(KA, VA)
        tr = float(np.trace(M))
        tr2 = float(np.trace(M @ M))
        q[mask] = det
        q1[mask] = det * tr
        q2[mask] = det * (tr * tr - tr2)
    return q, q1, q2


def mobius(v: np.ndarray, n: int) -> np.ndarray:
    out = v.copy()
    for bit in range(n):
        width = 1 << bit
        view = out.reshape((-1, 2, width) + out.shape[1:])
        view[:, 0] -= view[:, 1]
    return out


def directional_second(K: np.ndarray, V: np.ndarray) -> Dict[str, object]:
    n = len(K)
    q, q1, q2 = minor_derivatives(K, V)
    p, p1, p2 = (mobius(a, n) for a in (q, q1, q2))
    if np.any(p <= 0):
        raise FloatingPointError("nonpositive event probability")
    fisher = -float(np.sum(p1 * p1 / p))
    accel = -float(np.sum(p2 * np.log(p)))
    value = fisher + accel
    return {
        "value": value,
        "fisher": fisher,
        "acceleration": accel,
        "mass": float(p.sum()),
        "first_mass": float(p1.sum()),
        "second_mass": float(p2.sum()),
        "min_event": float(p.min()),
    }


def basis() -> List[np.ndarray]:
    out = []
    for i in range(3):
        E = np.zeros((3, 3))
        E[i, i] = 1.0
        out.append(E)
    for i, j in ((0, 1), (0, 2), (1, 2)):
        E = np.zeros((3, 3))
        E[i, j] = E[j, i] = 1.0
        out.append(E)
    return out


def hessian_matrix(K: np.ndarray) -> Tuple[np.ndarray, List[Dict[str, object]]]:
    bs = basis()
    diag = [directional_second(K, E) for E in bs]
    h = np.zeros((6, 6))
    for i in range(6):
        h[i, i] = diag[i]["value"]
    for i in range(6):
        for j in range(i + 1, 6):
            value = directional_second(K, bs[i] + bs[j])["value"]
            h[i, j] = h[j, i] = 0.5 * (value - h[i, i] - h[j, j])
    return 0.5 * (h + h.T), diag


def random_kernel(rng: np.random.Generator) -> np.ndarray:
    q, _ = np.linalg.qr(rng.normal(size=(3, 3)))
    eigs = rng.uniform(0.001, 0.999, size=3)
    K = q @ np.diag(eigs) @ q.T
    return 0.5 * (K + K.T)


def strict_margin(K: np.ndarray) -> float:
    e = np.linalg.eigvalsh(K)
    return float(min(e[0], 1.0 - e[-1]))


def feasible_step(K: np.ndarray, V: np.ndarray) -> float:
    norm = float(np.linalg.norm(V, 2))
    if norm == 0:
        return 0.0
    return 0.1 * strict_margin(K) / norm


def random_scan(samples: int = 20000, seed: int = 2026090842) -> Dict[str, object]:
    rng = np.random.default_rng(seed)
    best = None
    positive_over_1e_8 = 0
    positive_over_1e_10 = 0
    failures = 0
    for call in range(1, samples + 1):
        try:
            K = random_kernel(rng)
            H, _ = hessian_matrix(K)
            w, U = np.linalg.eigh(H)
            value = float(w[-1])
            if value > 1e-8:
                positive_over_1e_8 += 1
            if value > 1e-10:
                positive_over_1e_10 += 1
            if best is None or value > best["max_hessian"]:
                coeff = U[:, -1]
                V = sum(c * E for c, E in zip(coeff, basis()))
                step = feasible_step(K, V)
                chord_gap = None
                if step > 0:
                    chord_gap = 0.5 * (entropy(K - step * V) + entropy(K + step * V)) - entropy(K)
                best = {
                    "call": call,
                    "max_hessian": value,
                    "spectral_margin": strict_margin(K),
                    "min_event": float(event_probs(K).min()),
                    "eigen_residual": float(np.linalg.norm(H @ coeff - value * coeff)),
                    "coefficients_raw_basis": coeff.tolist(),
                    "small_chord_step": step,
                    "small_chord_gap": chord_gap,
                    "K": K.tolist(),
                }
        except (FloatingPointError, np.linalg.LinAlgError, ValueError):
            failures += 1
    return {
        "samples": samples,
        "seed": seed,
        "failures": failures,
        "positive_over_1e-8": positive_over_1e_8,
        "positive_over_1e-10": positive_over_1e_10,
        "best": best,
    }


FMatrix = List[List[Fraction]]


def fdet(A: FMatrix) -> Fraction:
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
        pv = M[col][col]
        det *= pv
        for row in range(col + 1, n):
            factor = M[row][col] / pv
            for j in range(col, n):
                M[row][j] -= factor * M[col][j]
    return det if sign > 0 else -det


def fsub(K: FMatrix, mask: int) -> FMatrix:
    ii = idx(mask, len(K))
    return [[K[i][j] for j in ii] for i in ii]


def fevents(K: FMatrix) -> List[Fraction]:
    n = len(K)
    q = [fdet(fsub(K, mask)) for mask in masks(n)]
    p = []
    full = (1 << n) - 1
    for s in masks(n):
        b = full ^ s
        total = Fraction(0, 1)
        while True:
            total += (-1 if b.bit_count() & 1 else 1) * q[s | b]
            if b == 0:
                break
            b = (b - 1) & (full ^ s)
        p.append(total)
    return p


def fent(p: Sequence[Fraction]) -> float:
    return -sum(float(x) * math.log(float(x)) for x in p)


def fadd(K: FMatrix, V: FMatrix, scale: Fraction) -> FMatrix:
    n = len(K)
    return [[K[i][j] + scale * V[i][j] for j in range(n)] for i in range(n)]


def exact_rational_sanity() -> Dict[str, object]:
    K = [
        [Fraction(1, 3), Fraction(1, 20), Fraction(1, 30)],
        [Fraction(1, 20), Fraction(2, 5), Fraction(1, 25)],
        [Fraction(1, 30), Fraction(1, 25), Fraction(1, 4)],
    ]
    V = [
        [Fraction(1, 200), Fraction(-1, 180), Fraction(1, 210)],
        [Fraction(-1, 180), Fraction(-1, 220), Fraction(1, 240)],
        [Fraction(1, 210), Fraction(1, 240), Fraction(1, 260)],
    ]
    t = Fraction(1, 1)
    pm = fevents(fadd(K, V, -t))
    p0 = fevents(K)
    pp = fevents(fadd(K, V, t))
    gap = 0.5 * (fent(pm) + fent(pp)) - fent(p0)
    return {
        "probability_sums": {
            "minus": str(sum(pm, Fraction(0, 1))),
            "center": str(sum(p0, Fraction(0, 1))),
            "plus": str(sum(pp, Fraction(0, 1))),
        },
        "minimum_probabilities": {
            "minus": str(min(pm)),
            "center": str(min(p0)),
            "plus": str(min(pp)),
        },
        "midpoint_gap": gap,
        "t": str(t),
    }


def main() -> None:
    data = {
        "explicit_formula": "H'' = -sum_s u_s^2/p_s - sum_s w_s log(p_s), where p is Mobius(det K_A), u=p', w=p''.",
        "exact_rational_sanity": exact_rational_sanity(),
        "random_hessian_scan": random_scan(),
    }
    path = Path(__file__).resolve().parent / "n3_probe_summary.json"
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    best = data["random_hessian_scan"]["best"]
    print(f"wrote {path.name}")
    print(
        "scan samples={samples} failures={failures} positives>1e-8={p8} positives>1e-10={p10}".format(
            samples=data["random_hessian_scan"]["samples"],
            failures=data["random_hessian_scan"]["failures"],
            p8=data["random_hessian_scan"]["positive_over_1e-8"],
            p10=data["random_hessian_scan"]["positive_over_1e-10"],
        )
    )
    print(
        "best call={call} max_hessian={value:.12g} residual={res:.3g} chord_gap={gap}".format(
            call=best["call"],
            value=best["max_hessian"],
            res=best["eigen_residual"],
            gap=best["small_chord_gap"],
        )
    )
    print(
        "exact rational gap={gap:.12g}, min_probs={mins}".format(
            gap=data["exact_rational_sanity"]["midpoint_gap"],
            mins=data["exact_rational_sanity"]["minimum_probabilities"],
        )
    )


if __name__ == "__main__":
    main()
