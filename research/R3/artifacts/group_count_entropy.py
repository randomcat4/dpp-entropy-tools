"""Exact-event entropy for a grouped real-symmetric DPP family.

The fast path aggregates events by group counts.  The direct path obtains
exact-event probabilities from inclusion minors by Boolean-lattice Mobius
inversion and is used only as a small-n oracle.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, Sequence

import numpy as np


@dataclass(frozen=True)
class CountRow:
    counts: tuple[int, ...]
    multiplicity: int
    log_event_probability: float
    event_probability: float


def _as_arrays(
    group_sizes: Sequence[int], a: Sequence[float], c_matrix: Sequence[Sequence[float]]
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    sizes = np.asarray(group_sizes, dtype=int)
    avec = np.asarray(a, dtype=float)
    cmat = np.asarray(c_matrix, dtype=float)
    q = len(sizes)
    if sizes.ndim != 1 or np.any(sizes < 1):
        raise ValueError("group_sizes must be positive integers")
    if avec.shape != (q,) or cmat.shape != (q, q):
        raise ValueError("a and C have incompatible shapes")
    if not np.allclose(cmat, cmat.T, atol=1e-13, rtol=1e-13):
        raise ValueError("C must be symmetric")
    if not (np.all(avec > 0.0) and np.all(avec < 1.0)):
        raise ValueError("all a_g must lie strictly in (0,1)")
    eig = np.linalg.eigvalsh(cmat)
    if not (eig[0] > 0.0 and eig[-1] < 1.0):
        raise ValueError("C must be a strict positive contraction")
    return sizes, avec, cmat


def grouped_kernel(
    group_sizes: Sequence[int], a: Sequence[float], c_matrix: Sequence[Sequence[float]]
) -> np.ndarray:
    """Construct K=A+U(C-diag(a))U^T."""

    sizes, avec, cmat = _as_arrays(group_sizes, a, c_matrix)
    n, q = int(sizes.sum()), len(sizes)
    u = np.zeros((n, q), dtype=float)
    diag = np.empty(n, dtype=float)
    start = 0
    for g, (m, ag) in enumerate(zip(sizes, avec)):
        stop = start + int(m)
        u[start:stop, g] = 1.0 / math.sqrt(int(m))
        diag[start:stop] = ag
        start = stop
    return np.diag(diag) + u @ (cmat - np.diag(avec)) @ u.T


def mobius_event_probabilities(k: np.ndarray) -> np.ndarray:
    """Return p[mask] by Mobius inversion of det K_A inclusion minors."""

    k = np.asarray(k, dtype=float)
    if k.ndim != 2 or k.shape[0] != k.shape[1]:
        raise ValueError("K must be square")
    if not np.allclose(k, k.T, atol=1e-13, rtol=1e-13):
        raise ValueError("K must be symmetric")
    n = k.shape[0]
    if n > 20:
        raise ValueError("direct Mobius oracle is intentionally limited to n<=20")
    probs = np.empty(1 << n, dtype=float)
    probs[0] = 1.0
    for mask in range(1, 1 << n):
        idx = [i for i in range(n) if mask & (1 << i)]
        probs[mask] = float(np.linalg.det(k[np.ix_(idx, idx)]))
    for bit in range(n):
        step = 1 << bit
        for mask in range(1 << n):
            if not mask & step:
                probs[mask] -= probs[mask | step]
    return probs


def _count_vectors(sizes: np.ndarray) -> Iterator[tuple[int, ...]]:
    yield from itertools.product(*(range(int(m) + 1) for m in sizes))


def group_count_table(
    group_sizes: Sequence[int], a: Sequence[float], c_matrix: Sequence[Sequence[float]]
) -> list[CountRow]:
    """Compute one exact-event probability for every group-count vector."""

    sizes, avec, cmat = _as_arrays(group_sizes, a, c_matrix)
    ell = avec / (1.0 - avec)
    ident = np.eye(len(sizes))
    rmat = np.linalg.solve(ident - cmat, cmat)
    bmat = 0.5 * (rmat + rmat.T) - np.diag(ell)
    sign_c, logdet_c = np.linalg.slogdet(ident - cmat)
    if sign_c <= 0:
        raise ArithmeticError("det(I-C) is not positive")
    logdet_i_minus_k = float(logdet_c + np.dot(sizes - 1, np.log1p(-avec)))
    rows: list[CountRow] = []
    for counts in _count_vectors(sizes):
        count = np.asarray(counts, dtype=float)
        d = count / (sizes * ell)
        sqrt_d = np.sqrt(d)
        small = ident + (sqrt_d[:, None] * bmat) * sqrt_d[None, :]
        small = 0.5 * (small + small.T)
        sign_s, logdet_s = np.linalg.slogdet(small)
        if sign_s <= 0:
            raise ArithmeticError(
                f"count determinant lost positivity at counts={counts}: sign={sign_s}"
            )
        logp = float(logdet_i_minus_k + np.dot(count, np.log(ell)) + logdet_s)
        p = float(math.exp(logp)) if logp > -745.0 else 0.0
        multiplicity = math.prod(
            math.comb(int(m), int(c)) for m, c in zip(sizes, counts)
        )
        rows.append(CountRow(tuple(int(x) for x in counts), multiplicity, logp, p))
    return rows


def grouped_entropy(
    group_sizes: Sequence[int], a: Sequence[float], c_matrix: Sequence[Sequence[float]]
) -> tuple[float, float, list[CountRow]]:
    """Return Shannon entropy, probability sum, and the count table."""

    rows = group_count_table(group_sizes, a, c_matrix)
    mass_sum = math.fsum(row.multiplicity * row.event_probability for row in rows)
    entropy = math.fsum(
        -row.multiplicity * row.event_probability * row.log_event_probability
        for row in rows
        if row.event_probability > 0.0
    )
    return entropy, mass_sum, rows


def event_probability_from_counts(rows: Iterable[CountRow]) -> dict[tuple[int, ...], float]:
    return {row.counts: row.event_probability for row in rows}


def mask_counts(mask: int, group_sizes: Sequence[int]) -> tuple[int, ...]:
    counts = []
    start = 0
    for m in group_sizes:
        counts.append(sum(bool(mask & (1 << i)) for i in range(start, start + int(m))))
        start += int(m)
    return tuple(counts)


def _orthogonal(rng: np.random.Generator, q: int) -> np.ndarray:
    qmat, r = np.linalg.qr(rng.normal(size=(q, q)))
    signs = np.sign(np.diag(r))
    signs[signs == 0.0] = 1.0
    return qmat * signs


def run_self_test() -> dict[str, object]:
    cases = []
    specs = [
        ([2, 2], [0.23, 0.71], [0.14, 0.58]),
        ([3, 2], [0.015, 0.985], [0.008, 0.992]),
        ([2, 3, 2], [0.19, 0.51, 0.83], [0.03, 0.47, 0.96]),
    ]
    for seed, (sizes, avec, eig) in enumerate(specs, start=731):
        rng = np.random.default_rng(seed)
        qmat = _orthogonal(rng, len(sizes))
        cmat = qmat @ np.diag(eig) @ qmat.T
        kernel = grouped_kernel(sizes, avec, cmat)
        direct = mobius_event_probabilities(kernel)
        entropy, mass_sum, rows = grouped_entropy(sizes, avec, cmat)
        lookup = event_probability_from_counts(rows)
        fast = np.asarray(
            [lookup[mask_counts(mask, sizes)] for mask in range(1 << sum(sizes))]
        )
        direct_entropy = -math.fsum(
            float(p) * math.log(float(p)) for p in direct if p > 0.0
        )
        cases.append(
            {
                "seed": seed,
                "group_sizes": sizes,
                "n": sum(sizes),
                "max_event_abs_error": float(np.max(np.abs(direct - fast))),
                "probability_sum_error": abs(mass_sum - 1.0),
                "entropy_abs_error": abs(entropy - direct_entropy),
                "kernel_lambda_min": float(np.linalg.eigvalsh(kernel)[0]),
                "kernel_one_minus_lambda_max": float(1.0 - np.linalg.eigvalsh(kernel)[-1]),
            }
        )
    thresholds = {
        "max_event_abs_error": 2e-10,
        "probability_sum_error": 2e-10,
        "entropy_abs_error": 2e-10,
    }
    passed = all(
        case[key] <= value for case in cases for key, value in thresholds.items()
    )
    return {"status": "PASS" if passed else "FAIL", "thresholds": thresholds, "cases": cases}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if not args.self_test:
        parser.error("currently supported action: --self-test")
    result = run_self_test()
    text = json.dumps(result, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
