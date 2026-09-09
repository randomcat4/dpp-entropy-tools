#!/usr/bin/env python3
"""Finite-suffix entropy-rate bounds for scalar stationary DPP candidates.

This script is a numerical witness builder, not a rigorous interval prover.
It implements the finite objects proved in ../proof_or_gap.md:

* U_r(f) = H(X_0 | X_{-r},...,X_{-1});
* an extreme-past interval [alpha_w, beta_w] for each suffix word w;
* L_r(f) = sum_w P(w) min_{q in [alpha_w,beta_w]} h_2(q).

The benchmark is the first S1 candidate supplied by the route owner.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import platform
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np


@dataclass(frozen=True)
class Symbol:
    p: float
    a: tuple[float, ...]
    b: tuple[float, ...]
    t: float

    @property
    def degree(self) -> int:
        return len(self.a)

    def coeffs(self) -> dict[int, complex]:
        c: dict[int, complex] = {0: complex(self.p)}
        for idx, (ak, bk) in enumerate(zip(self.a, self.b), start=1):
            c[idx] = complex(ak, -self.t * bk) / 2.0
            c[-idx] = np.conjugate(c[idx])
        return c

    def complement(self) -> "Symbol":
        return Symbol(
            p=1.0 - self.p,
            a=tuple(-x for x in self.a),
            b=tuple(-x for x in self.b),
            t=self.t,
        )


def h2(q: float) -> float:
    q = min(1.0, max(0.0, q))
    if q <= 0.0 or q >= 1.0:
        return 0.0
    return -q * math.log(q) - (1.0 - q) * math.log(1.0 - q)


def toeplitz_kernel(symbol: Symbol, sites: Iterable[int]) -> np.ndarray:
    sites = list(sites)
    c = symbol.coeffs()
    n = len(sites)
    k = np.empty((n, n), dtype=np.complex128)
    for i, si in enumerate(sites):
        for j, sj in enumerate(sites):
            k[i, j] = c.get(si - sj, 0.0)
    return k


def exact_pattern_probability(k: np.ndarray, bits: int, n: int) -> float:
    """P(X_0...X_{n-1}=bits), bit i attached to row/site i."""
    m = np.array(k, copy=True)
    for i in range(n):
        if ((bits >> i) & 1) == 0:
            m[i, :] *= -1.0
            m[i, i] += 1.0
    val = np.linalg.det(m)
    real = float(np.real_if_close(val, tol=1000).real)
    if real < 0.0 and real > -1.0e-10:
        real = 0.0
    return real


def conditional_upper(symbol: Symbol, r: int) -> dict[str, float]:
    """Exact finite conditional entropy U_r and H_{r+1}-H_r check."""
    k = toeplitz_kernel(symbol, range(-r, 1))
    total_suffix = 1 << r
    u = 0.0
    min_prob = 1.0
    neg_mass = 0.0
    sum_mass = 0.0
    entropy_joint = 0.0
    entropy_suffix = 0.0
    for w in range(total_suffix):
        bits0 = w
        bits1 = w | (1 << r)
        p0 = exact_pattern_probability(k, bits0, r + 1)
        p1 = exact_pattern_probability(k, bits1, r + 1)
        for p in (p0, p1):
            if p < 0.0:
                neg_mass += -p
            if p > 0.0:
                entropy_joint -= p * math.log(p)
            sum_mass += p
        pw = p0 + p1
        if pw < min_prob:
            min_prob = pw
        if pw > 0.0:
            q = p1 / pw
            u += pw * h2(q)
            entropy_suffix -= pw * math.log(pw)
    return {
        "r": r,
        "U_r": u,
        "joint_entropy": entropy_joint,
        "suffix_entropy": entropy_suffix,
        "joint_minus_suffix": entropy_joint - entropy_suffix,
        "mass_sum": sum_mass,
        "min_suffix_probability": min_prob,
        "negative_mass_clipped": neg_mass,
    }


def spectral_factor_outer(symbol: Symbol) -> tuple[np.ndarray, dict[str, object]]:
    """Return outer polynomial coefficients v_j with |sum v_j z^j|^2 = f.

    The factor is selected with all zeros outside the unit disk and positive
    constant term, by pairing reciprocal roots of z^m f(z).
    """
    c = symbol.coeffs()
    m = symbol.degree
    q_ascending = np.array([c.get(r - m, 0.0) for r in range(2 * m + 1)], dtype=np.complex128)
    roots = np.roots(q_ascending[::-1])
    outside = [z for z in roots if abs(z) > 1.0]
    inside = [z for z in roots if abs(z) <= 1.0]
    if len(outside) != m:
        outside = sorted(roots, key=lambda z: abs(z), reverse=True)[:m]
        inside = sorted(roots, key=lambda z: abs(z))[:m]
    alpha = np.array([1.0 / z for z in outside], dtype=np.complex128)
    poly = np.array([1.0 + 0.0j])
    for a in alpha:
        poly = np.convolve(poly, np.array([1.0 + 0.0j, -a], dtype=np.complex128))
    # q(0) = c[-m] = B^2 * (-1)^m * conjugate(prod(alpha)).
    denom = ((-1) ** m) * np.conjugate(np.prod(alpha))
    b2 = c[-m] / denom
    b2_real = float(np.real_if_close(b2, tol=1000).real)
    if b2_real <= 0.0:
        raise ValueError(f"outer factor normalization failed: B^2={b2!r}")
    coeff = math.sqrt(b2_real) * poly
    recon = reconstruct_fourier(coeff)
    max_err = 0.0
    for kk in range(-m, m + 1):
        max_err = max(max_err, abs(recon.get(kk, 0.0) - c.get(kk, 0.0)))
    return coeff, {
        "degree": m,
        "roots_abs_min": float(np.min(np.abs(roots))),
        "roots_abs_max": float(np.max(np.abs(roots))),
        "inside_count_by_unit_cut": len(inside),
        "outside_count_by_unit_cut": len(outside),
        "outer_zero_abs_min": float(np.min(np.abs(outside))) if outside else None,
        "outer_zero_abs_max": float(np.max(np.abs(outside))) if outside else None,
        "factor_coefficients_real_imag": [[float(z.real), float(z.imag)] for z in coeff],
        "max_fourier_reconstruction_error": float(max_err),
    }


def reconstruct_fourier(coeff: np.ndarray) -> dict[int, complex]:
    d = len(coeff) - 1
    out: dict[int, complex] = {}
    for k in range(-d, d + 1):
        s = 0.0 + 0.0j
        for ell in range(d + 1):
            j = ell + k
            if 0 <= j <= d:
                s += coeff[j] * np.conjugate(coeff[ell])
        out[k] = s
    return out


def boundary_kernel_from_outer(coeff: np.ndarray, n: int) -> np.ndarray:
    d = len(coeff) - 1
    a = np.zeros((n, n), dtype=np.complex128)
    for j in range(n):
        for k in range(n):
            s = 0.0 + 0.0j
            for ell in range(min(j, k) + 1):
                cj = coeff[j - ell] if 0 <= j - ell <= d else 0.0
                ck = coeff[k - ell] if 0 <= k - ell <= d else 0.0
                s += cj * np.conjugate(ck)
            a[j, k] = s
    return a


def boundary_one_probability(boundary_k: np.ndarray, word: int, r: int) -> float:
    p_w = exact_pattern_probability(boundary_k[:r, :r], word, r)
    p_w1 = exact_pattern_probability(boundary_k[: r + 1, : r + 1], word | (1 << r), r + 1)
    if p_w <= 0.0:
        return float("nan")
    return p_w1 / p_w


def interval_lower(symbol: Symbol, r: int) -> dict[str, object]:
    """Lower bound L_r from extreme-past intervals."""
    coeff_f, factor_f = spectral_factor_outer(symbol)
    coeff_c, factor_c = spectral_factor_outer(symbol.complement())
    bf = boundary_kernel_from_outer(coeff_f, r + 1)
    bc = boundary_kernel_from_outer(coeff_c, r + 1)
    kt = toeplitz_kernel(symbol, range(-r, 0))
    total = 1 << r
    lower = 0.0
    interval_width_max = 0.0
    bad_order = 0
    min_suffix_prob = 1.0
    min_alpha = 1.0
    max_beta = 0.0
    for w in range(total):
        pw = exact_pattern_probability(kt, w, r)
        min_suffix_prob = min(min_suffix_prob, pw)
        alpha = boundary_one_probability(bf, w, r)
        wc = ((1 << r) - 1) ^ w
        beta = 1.0 - boundary_one_probability(bc, wc, r)
        if alpha > beta + 1.0e-9:
            bad_order += 1
        lo = min(alpha, beta)
        hi = max(alpha, beta)
        interval_width_max = max(interval_width_max, hi - lo)
        min_alpha = min(min_alpha, lo)
        max_beta = max(max_beta, hi)
        lower += pw * min(h2(lo), h2(hi))
    return {
        "r": r,
        "L_r": lower,
        "max_interval_width": interval_width_max,
        "bad_interval_order_count": bad_order,
        "min_suffix_probability": min_suffix_prob,
        "min_interval_endpoint": min_alpha,
        "max_interval_endpoint": max_beta,
        "outer_factor_f": factor_f,
        "outer_factor_1_minus_f": factor_c,
    }


def block_entropy(symbol: Symbol, n: int) -> dict[str, float]:
    k = toeplitz_kernel(symbol, range(n))
    h = 0.0
    total = 0.0
    min_p = 1.0
    for bits in range(1 << n):
        p = exact_pattern_probability(k, bits, n)
        total += p
        if p > 0.0:
            h -= p * math.log(p)
            min_p = min(min_p, p)
    return {"n": n, "H_n": h, "H_n_over_n": h / n, "mass_sum": total, "min_atom_probability": min_p}


def benchmark_symbol(tau_sign: float) -> Symbol:
    tau = 0.25 * tau_sign
    return Symbol(
        p=0.5,
        a=(9.0 / 50.0, -3.0 / 25.0, 2.0 / 25.0),
        b=(1.0 / 10.0, 2.0 / 25.0, -3.0 / 50.0),
        t=tau,
    )


def run(max_r: int, block_n: int) -> dict[str, object]:
    symbols = {"minus": benchmark_symbol(-1.0), "zero": benchmark_symbol(0.0), "plus": benchmark_symbol(1.0)}
    out: dict[str, object] = {
        "status": "NUMERICAL_WITNESS_ONLY",
        "python": sys.version,
        "platform": platform.platform(),
        "numpy": np.__version__,
        "pid": os.getpid(),
        "thread_env": {k: os.environ.get(k) for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "BLIS_NUM_THREADS")},
        "parameters": {
            "p": 0.5,
            "a": [9.0 / 50.0, -3.0 / 25.0, 2.0 / 25.0],
            "b": [1.0 / 10.0, 2.0 / 25.0, -3.0 / 50.0],
            "tau": 0.25,
            "triangle_margin_certificate": 0.5 - sum(abs(x) for x in (9.0 / 50.0, -3.0 / 25.0, 2.0 / 25.0)) - 0.25 * sum(abs(x) for x in (1.0 / 10.0, 2.0 / 25.0, -3.0 / 50.0)),
        },
        "max_r": max_r,
        "block_n": block_n,
        "symbols": {},
        "certificate_gaps": [],
    }
    for name, sym in symbols.items():
        sym_out: dict[str, object] = {"upper": [], "lower": [], "block_entropy": []}
        for r in range(1, max_r + 1):
            sym_out["upper"].append(conditional_upper(sym, r))
            sym_out["lower"].append(interval_lower(sym, r))
        for n in range(1, block_n + 1):
            sym_out["block_entropy"].append(block_entropy(sym, n))
        out["symbols"][name] = sym_out
    plus = out["symbols"]["plus"]
    zero = out["symbols"]["zero"]
    minus = out["symbols"]["minus"]
    for r in range(1, max_r + 1):
        lp = plus["lower"][r - 1]["L_r"]
        lm = minus["lower"][r - 1]["L_r"]
        uz = zero["upper"][r - 1]["U_r"]
        up = plus["upper"][r - 1]["U_r"]
        um = minus["upper"][r - 1]["U_r"]
        lz = zero["lower"][r - 1]["L_r"]
        out["certificate_gaps"].append(
            {
                "r": r,
                "counterexample_gate_symmetric": 0.5 * (lp + lm) - uz,
                "counterexample_gate_plus_only_reflection": lp - uz,
                "negative_exclusion_gate_symmetric": 0.5 * (up + um) - lz,
            }
        )
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-r", type=int, default=10)
    ap.add_argument("--block-n", type=int, default=12)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    result = run(args.max_r, args.block_n)
    script_bytes = Path(__file__).read_bytes()
    result["script_sha256"] = hashlib.sha256(script_bytes).hexdigest()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")


if __name__ == "__main__":
    main()
