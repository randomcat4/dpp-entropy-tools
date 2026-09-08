"""Sanity checks for the analytic small-coupling curvature theorem.

This script is deliberately small and deterministic.  It is not a search for
counterexamples.  It checks:

1. the beta=0 entropy Hessian equals the product-Bernoulli formula;
2. small nonzero beta examples remain negative and close to beta=0;
3. the same O(n^2) jet interface from D10-B3 is used without finite differences.

No third-party packages are required.
"""

from __future__ import annotations

import importlib.util
import json
import math
import os
import sys
from pathlib import Path


sys.dont_write_bytecode = True
os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")


HERE = Path(__file__).resolve()
GENERAL_FAMILY = HERE.parent.parent
JET_PATH = GENERAL_FAMILY / "jet_hessian" / "jet_hessian.py"


def load_jet_module():
    spec = importlib.util.spec_from_file_location("d10_b3_jet_hessian", JET_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load jet module from {JET_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


jet = load_jet_module()


def deterministic_tau(n: int) -> list[float]:
    return [
        0.21 + 0.53 * (((7 * i + 3) % (n + 5)) + 1) / (n + 6)
        for i in range(n)
    ]


def deterministic_delta(n: int) -> list[float]:
    raw = [
        math.sin(0.73 * (i + 1)) + 0.35 * math.cos(1.17 * (i + 2))
        for i in range(n)
    ]
    norm = math.sqrt(sum(x * x for x in raw))
    return [x / norm for x in raw]


def deterministic_beta(n: int, eps: float) -> list[float]:
    return [
        ((-1.0) ** i) * eps * (0.62 + 0.07 * ((3 * i + 1) % 5))
        for i in range(n - 1)
    ]


def diagonal_h2_formula(tau: list[float], delta: list[float]) -> float:
    return -sum(d * d / (t * (1.0 - t)) for t, d in zip(tau, delta))


def run() -> dict[str, object]:
    diagonal_cases = []
    small_coupling_cases = []

    for n in (3, 5, 8, 12):
        tau = deterministic_tau(n)
        delta = deterministic_delta(n)
        beta0 = [0.0] * (n - 1)
        h2_expected = diagonal_h2_formula(tau, delta)
        h2_jet = jet.entropy_jet_tau(beta0, tau, delta)["H2"]
        diagonal_cases.append(
            {
                "n": n,
                "H2_formula": h2_expected,
                "H2_jet": h2_jet,
                "absolute_error": abs(h2_jet - h2_expected),
            }
        )

        for eps in (1e-4, 1e-3, 1e-2):
            beta = deterministic_beta(n, eps)
            h2_small = jet.entropy_jet_tau(beta, tau, delta)["H2"]
            small_coupling_cases.append(
                {
                    "n": n,
                    "eps": eps,
                    "H2_beta0_formula": h2_expected,
                    "H2_small_beta_jet": h2_small,
                    "difference_from_beta0": h2_small - h2_expected,
                    "negative": h2_small < 0.0,
                }
            )

    diagonal_max_error = max(row["absolute_error"] for row in diagonal_cases)
    all_small_negative = all(row["negative"] for row in small_coupling_cases)
    result = {
        "status": "PASS" if diagonal_max_error < 1e-12 and all_small_negative else "FAIL",
        "purpose": "deterministic sanity for the analytic small-coupling theorem; not a finite global proof",
        "jet_module": str(JET_PATH.relative_to(GENERAL_FAMILY.parent.parent.parent.parent.parent)),
        "diagonal_cases": diagonal_cases,
        "diagonal_max_abs_error": diagonal_max_error,
        "small_coupling_cases": small_coupling_cases,
        "small_coupling_all_negative": all_small_negative,
        "thread_limits": {
            "OMP_NUM_THREADS": os.environ.get("OMP_NUM_THREADS"),
            "OPENBLAS_NUM_THREADS": os.environ.get("OPENBLAS_NUM_THREADS"),
            "MKL_NUM_THREADS": os.environ.get("MKL_NUM_THREADS"),
            "NUMEXPR_NUM_THREADS": os.environ.get("NUMEXPR_NUM_THREADS"),
        },
    }
    return result


def main() -> None:
    result = run()
    out_path = HERE.parent / "results" / "weak_coupling_sanity.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
