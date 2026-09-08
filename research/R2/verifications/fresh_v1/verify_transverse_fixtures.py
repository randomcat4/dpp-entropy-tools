from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

from dpp_exact import (
    LogIntervalConfig,
    chord_gap_interval,
    det_fraction,
    entropy_interval,
    exact_event_probabilities,
    fraction_to_json,
    interval_to_json,
    mat_add,
    mat_mul,
    mat_scale,
    matrix_to_json,
    submatrix,
    transpose,
)


def col_matrix(columns: list[list[Fraction]]) -> list[list[Fraction]]:
    return [list(row) for row in zip(*columns)]


def kernel_from_data(U, V, B, tau: Fraction, x: Fraction, y: Fraction, sigma: int):
    n = len(U)
    eps = x * x
    P = mat_mul(U, transpose(U))
    Q = mat_add([[Fraction(int(i == j), 1) for j in range(n)] for i in range(n)], mat_scale(Fraction(-1, 1), P))
    VBt = mat_mul(V, transpose(B))
    UBVt = mat_mul(mat_mul(U, B), transpose(V))
    D = mat_add(UBVt, transpose(UBVt))
    M = mat_add(mat_scale(1 - eps, P), mat_scale(eps, Q))
    t = tau * x * y
    return mat_add(M, mat_scale(Fraction(sigma, 1) * t, D))


def psi_phi(U, V, B):
    n = len(U)
    r = len(U[0])
    VBt = mat_mul(V, transpose(B))
    out = []
    for mask in range(1 << n):
        if mask.bit_count() != r:
            continue
        rows = [i for i in range(n) if (mask >> i) & 1]
        base = submatrix(U, rows, list(range(r)))
        psi = det_fraction(base)
        phi = Fraction(0, 1)
        for c in range(r):
            varied = [row[:] for row in base]
            replacement = [VBt[i][c] for i in rows]
            for rr in range(r):
                varied[rr][c] = replacement[rr]
            phi += det_fraction(varied)
        out.append({"mask": mask, "psi": psi, "phi": phi})
    return out


def frobenius_sq(B) -> Fraction:
    return sum(x * x for row in B for x in row)


def fixture_report(name: str, U, V, B, tau: Fraction, pythagorean_uv: tuple[int, int]):
    # q=a/b, x=2q/(1+q^2), y=(1-q^2)/(1+q^2).
    a, b = pythagorean_uv
    q_num = Fraction(a, b)
    x = 2 * q_num / (1 + q_num * q_num)
    y = (1 - q_num * q_num) / (1 + q_num * q_num)
    k_plus = kernel_from_data(U, V, B, tau, x, y, +1)
    k_minus = kernel_from_data(U, V, B, tau, x, y, -1)
    cfg = LogIntervalConfig(terms=220, decimal_digits=90)
    gap = chord_gap_interval(k_minus, k_plus, cfg)
    pp = psi_phi(U, V, B)
    Z = sum(item["phi"] * item["phi"] for item in pp if item["psi"] == 0)
    F = frobenius_sq(B)
    coefficient = tau * tau * (Z - 2 * F)
    eps = x * x
    return {
        "name": name,
        "n": len(U),
        "r": len(U[0]),
        "U": matrix_to_json(U),
        "V": matrix_to_json(V),
        "B": matrix_to_json(B),
        "tau": fraction_to_json(tau),
        "pythagorean_q": {"num": a, "den": b},
        "x": fraction_to_json(x),
        "sqrt_1_minus_x2": fraction_to_json(y),
        "epsilon": fraction_to_json(eps),
        "K_minus": matrix_to_json(k_minus),
        "K_plus": matrix_to_json(k_plus),
        "plucker": [
            {
                "mask": item["mask"],
                "psi": fraction_to_json(item["psi"]),
                "phi": fraction_to_json(item["phi"]),
            }
            for item in pp
        ],
        "Z": fraction_to_json(Z),
        "F": fraction_to_json(F),
        "leading_coefficient": fraction_to_json(coefficient),
        "probability_checks": {
            key: fraction_to_json(value) if hasattr(value, "numerator") else value
            for key, value in gap["checks"].items()
        },
        "entropy_interval": {
            key: interval_to_json(value, 90) for key, value in gap["entropy_interval"].items()
        },
        "gap_interval": interval_to_json(gap["gap_interval"], 90),
        "strict_positive": gap["strict_positive"],
        "strict_negative": gap["strict_negative"],
        "event_probabilities": {
            key: [
                {
                    "mask": mask,
                    "p": fraction_to_json(prob),
                }
                for mask, prob in enumerate(probs)
            ]
            for key, probs in gap["event_probabilities"].items()
        },
    }


def main() -> int:
    if hasattr(sys, "set_int_max_str_digits"):
        sys.set_int_max_str_digits(0)
    F = Fraction
    reports = []
    # Plucker-zero fixture: P projects onto span(e1,e2), so rank-2 events
    # {1,3} and {2,3} have psi=0 and nonzero transverse derivatives.
    U_zero = [
        [F(1), F(0)],
        [F(0), F(1)],
        [F(0), F(0)],
    ]
    V_zero = [
        [F(0)],
        [F(0)],
        [F(1)],
    ]
    B_zero = [
        [F(1)],
        [F(2)],
    ]
    reports.append(fixture_report("plucker_zero_rank2_n3", U_zero, V_zero, B_zero, F(1, 4), (1, 50)))

    # Generic rank-1 fixture with rational orthogonal frame and no zero
    # coordinate in U.
    U_generic = [
        [F(2, 3)],
        [F(1, 3)],
        [F(2, 3)],
    ]
    V_generic = [
        [F(-2, 3), F(1, 3)],
        [F(2, 3), F(2, 3)],
        [F(1, 3), F(-2, 3)],
    ]
    B_generic = [
        [F(1), F(1)],
    ]
    reports.append(fixture_report("generic_rank1_n3", U_generic, V_generic, B_generic, F(1, 3), (1, 50)))

    out = {
        "status": "fixture_check_complete",
        "notes": [
            "All probabilities are exact-event masses obtained by Mobius inversion from principal inclusion determinants.",
            "The displayed gap intervals use rational atanh-series log enclosures, not floating logs.",
            "Negative finite-epsilon gaps are consistency checks for the frozen theorem; they are not global concavity evidence.",
        ],
        "fixtures": reports,
    }
    out_path = Path("fixture_verification_report.json")
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps({
        "status": out["status"],
        "fixture_summaries": [
            {
                "name": item["name"],
                "Z": item["Z"],
                "F": item["F"],
                "leading_coefficient": item["leading_coefficient"],
                "gap_interval": item["gap_interval"],
                "strict_negative": item["strict_negative"],
                "min_probs": {
                    "minus": item["probability_checks"]["min_minus"],
                    "plus": item["probability_checks"]["min_plus"],
                    "mid": item["probability_checks"]["min_mid"],
                },
                "zeros": {
                    "minus": item["probability_checks"]["zero_minus"],
                    "plus": item["probability_checks"]["zero_plus"],
                    "mid": item["probability_checks"]["zero_mid"],
                },
            }
            for item in reports
        ],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

