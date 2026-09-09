#!/usr/bin/env python3
"""Compare the outer-factor boundary kernel with the main residual certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

from rate_bounds import benchmark_symbol, boundary_kernel_from_outer, spectral_factor_outer


def rational_pair_to_complex(pair: list[str]) -> complex:
    return complex(float(Fraction(pair[0])), float(Fraction(pair[1])))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--residual-json", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    residual = json.loads(args.residual_json.read_text(encoding="utf-8"))
    rows = []
    for case in residual["cases"]:
        t = float(Fraction(case["t"]))
        complement = bool(case["complement_symbol"])
        if abs(t) < 1.0e-15:
            sym = benchmark_symbol(0.0)
        elif abs(t - 0.25) < 1.0e-15:
            sym = benchmark_symbol(1.0)
        elif abs(t + 0.25) < 1.0e-15:
            sym = benchmark_symbol(-1.0)
        else:
            continue
        if complement:
            sym = sym.complement()
        coeff, factor = spectral_factor_outer(sym)
        outer = boundary_kernel_from_outer(coeff, sym.degree)[: sym.degree, : sym.degree]
        certified = np.array(
            [[rational_pair_to_complex(cell) for cell in row] for row in case["corner_rational"]],
            dtype=np.complex128,
        )
        diff = outer - certified
        rows.append(
            {
                "t": case["t"],
                "complement_symbol": complement,
                "operator_error_upper_float": case["operator_error_upper_float"],
                "outer_factor_reconstruction_error": factor["max_fourier_reconstruction_error"],
                "max_abs_corner_difference": float(np.max(np.abs(diff))),
                "frobenius_corner_difference": float(np.linalg.norm(diff)),
            }
        )
    out = {
        "status": "NUMERICAL_CROSS_CHECK_ONLY",
        "python": sys.version,
        "numpy": np.__version__,
        "residual_json_basename": args.residual_json.name,
        "residual_sha256": hashlib.sha256(args.residual_json.read_bytes()).hexdigest(),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "comparisons": rows,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out, indent=2, sort_keys=True), encoding="utf-8")


if __name__ == "__main__":
    main()
