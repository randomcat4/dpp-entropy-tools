#!/usr/bin/env python3
"""General symbolic check for PR32 round2 proof equation (3.9)."""
from __future__ import annotations

import json
import os
import platform
import sys
from pathlib import Path

import sympy as sp

OUT = Path(__file__).resolve().parent / "compute_outputs"
OUT.mkdir(exist_ok=True)


def main() -> int:
    os.environ["OMP_NUM_THREADS"] = "1"
    os.environ["OPENBLAS_NUM_THREADS"] = "1"
    os.environ["MKL_NUM_THREADS"] = "1"
    os.environ["NUMEXPR_NUM_THREADS"] = "1"

    A0, A1, A2, lam = sp.symbols("A0 A1 A2 lam")
    A3 = 1 - A0 - A1 - A2
    a = A1 + A3
    b = A2 + A3
    r = sp.factor(A1 * A2 - A0 * A3)
    P = sp.factor(A0 * A1 * A2 * A3)
    E = sp.factor(A0 * A3 * (A0 + A3) + A1 * A2 * (A1 + A2))

    G = sp.Matrix(
        [
            [1 / A0 + 1 / A1, 1 / A0, -1 / A0 - 1 / A1],
            [1 / A0, 1 / A0 + 1 / A2, -1 / A0 - 1 / A2],
            [-1 / A0 - 1 / A1, -1 / A0 - 1 / A2, 1 / A0 + 1 / A1 + 1 / A2 + 1 / A3],
        ]
    )
    Q = sp.Matrix([[0, sp.Rational(1, 2), 0], [sp.Rational(1, 2), 0, 0], [0, 0, 0]])
    v = sp.Matrix([b, a, -1])
    Q = Q - (v * v.T) / (4 * r)

    det_left = sp.factor((G - lam * Q).det())
    det_right = sp.factor((16 * r + 4 * lam * E - lam**3 * P) / (16 * r * P))
    numerator = sp.factor(sp.together(det_left - det_right).as_numer_denom()[0])
    denominator = sp.factor(sp.together(det_left - det_right).as_numer_denom()[1])
    status = sp.simplify(numerator) == 0
    if not status:
        raise AssertionError(f"nonzero numerator: {numerator}")

    result = {
        "python": platform.python_version(),
        "executable": sys.executable,
        "sympy": sp.__version__,
        "variables": ["A0", "A1", "A2", "A3=1-A0-A1-A2", "lam"],
        "identity": "det(G-lam*Q) - (16*r+4*lam*E-lam**3*P)/(16*r*P)",
        "difference_numerator_factor": str(numerator),
        "difference_denominator_factor": str(denominator),
        "verified_zero": status,
    }
    out_path = OUT / "w1_round2_pencil_symbolic_results.json"
    out_path.write_text(json.dumps(result, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
