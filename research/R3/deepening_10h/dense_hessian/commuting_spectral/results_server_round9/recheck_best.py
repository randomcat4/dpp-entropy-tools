"""Author-side high-precision gate for the strongest round-9 spectral scout.

The 20,000-row float search is only a scout.  This script freezes its strongest
row, checks exact-event semantics, recomputes the directional curvature with
Decimal elimination, evaluates actual entropy chords, and proves a rational
strict-feasibility interval for the decimal-rationalized matrices.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import time
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[key] = "1"
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

import numpy as np


HERE = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def mixed_atoms_float(kernel: np.ndarray) -> tuple[np.ndarray, list[np.ndarray]]:
    n = len(kernel)
    probabilities = np.empty(1 << n)
    matrices: list[np.ndarray] = []
    for mask in range(1 << n):
        matrix = kernel.copy()
        absent = n - mask.bit_count()
        for i in range(n):
            if not ((mask >> i) & 1):
                matrix[i, i] -= 1.0
        probabilities[mask] = ((-1.0) ** absent) * float(np.linalg.det(matrix))
        matrices.append(matrix)
    return probabilities, matrices


def mobius_atoms_float(kernel: np.ndarray) -> np.ndarray:
    n = len(kernel)
    values = np.empty(1 << n)
    for mask in range(1 << n):
        indices = [i for i in range(n) if (mask >> i) & 1]
        values[mask] = 1.0 if not indices else float(np.linalg.det(kernel[np.ix_(indices, indices)]))
    for bit_index in range(n):
        bit = 1 << bit_index
        for mask in range(1 << n):
            if not (mask & bit):
                values[mask] -= values[mask | bit]
    return values


def directional_float(kernel: np.ndarray, direction: np.ndarray) -> dict[str, float]:
    probabilities, matrices = mixed_atoms_float(kernel)
    fisher = 0.0
    acceleration = 0.0
    sum_p1 = 0.0
    sum_p2 = 0.0
    for probability, matrix in zip(probabilities, matrices):
        solved = np.linalg.solve(matrix, direction)
        score = float(np.trace(solved))
        second = score * score - float(np.trace(solved @ solved))
        fisher += probability * score * score
        acceleration -= probability * math.log(probability) * second
        sum_p1 += probability * score
        sum_p2 += probability * second
    return {
        "fisher": fisher,
        "acceleration": acceleration,
        "H2": acceleration - fisher,
        "rho": acceleration / fisher,
        "sum_p": float(probabilities.sum()),
        "sum_p1": sum_p1,
        "sum_p2": sum_p2,
        "min_atom": float(probabilities.min()),
    }


def decimal_matrix(matrix: np.ndarray) -> list[list[Decimal]]:
    return [[Decimal(repr(float(value))) for value in row] for row in matrix]


def decimal_det_solve(
    matrix_input: list[list[Decimal]], rhs_input: list[list[Decimal]] | None = None
) -> tuple[Decimal, list[list[Decimal]] | None]:
    matrix = [row[:] for row in matrix_input]
    rhs = None if rhs_input is None else [row[:] for row in rhs_input]
    n = len(matrix)
    determinant = Decimal(1)
    for column in range(n):
        pivot = max(range(column, n), key=lambda row: abs(matrix[row][column]))
        if matrix[pivot][column] == 0:
            raise ArithmeticError("singular mixed-event matrix")
        if pivot != column:
            matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
            if rhs is not None:
                rhs[column], rhs[pivot] = rhs[pivot], rhs[column]
            determinant = -determinant
        value = matrix[column][column]
        determinant *= value
        for row in range(column + 1, n):
            factor = matrix[row][column] / value
            matrix[row][column] = Decimal(0)
            for j in range(column + 1, n):
                matrix[row][j] -= factor * matrix[column][j]
            if rhs is not None:
                for j in range(n):
                    rhs[row][j] -= factor * rhs[column][j]
    if rhs is None:
        return determinant, None
    solution = [[Decimal(0) for _ in range(n)] for _ in range(n)]
    for row in range(n - 1, -1, -1):
        for j in range(n):
            tail = sum(matrix[row][k] * solution[k][j] for k in range(row + 1, n))
            solution[row][j] = (rhs[row][j] - tail) / matrix[row][row]
    return determinant, solution


def decimal_directional(
    kernel_np: np.ndarray, direction_np: np.ndarray, precision: int
) -> dict[str, str | int]:
    with localcontext() as context:
        context.prec = precision
        kernel = decimal_matrix(kernel_np)
        direction = decimal_matrix(direction_np)
        n = len(kernel)
        total = Decimal(0)
        entropy = Decimal(0)
        fisher = Decimal(0)
        acceleration = Decimal(0)
        sum_p1 = Decimal(0)
        sum_p2 = Decimal(0)
        minimum = Decimal(1)
        for mask in range(1 << n):
            matrix = [row[:] for row in kernel]
            absent = n - mask.bit_count()
            for i in range(n):
                if not ((mask >> i) & 1):
                    matrix[i][i] -= Decimal(1)
            determinant, solved = decimal_det_solve(matrix, direction)
            assert solved is not None
            probability = determinant * (Decimal(-1) if absent % 2 else Decimal(1))
            if probability <= 0:
                raise ArithmeticError("nonpositive Decimal exact atom")
            score = sum(solved[i][i] for i in range(n))
            trace_square = sum(solved[i][j] * solved[j][i] for i in range(n) for j in range(n))
            second = score * score - trace_square
            log_probability = probability.ln()
            total += probability
            entropy -= probability * log_probability
            fisher += probability * score * score
            acceleration -= probability * log_probability * second
            sum_p1 += probability * score
            sum_p2 += probability * second
            minimum = min(minimum, probability)
        h2 = acceleration - fisher
        return {
            "precision": precision,
            "entropy": str(+entropy),
            "fisher": str(+fisher),
            "acceleration": str(+acceleration),
            "H2": str(+h2),
            "rho": str(+(acceleration / fisher)),
            "sum_p": str(+total),
            "sum_p1": str(+sum_p1),
            "sum_p2": str(+sum_p2),
            "min_atom": str(+minimum),
        }


def decimal_entropy(kernel: list[list[Decimal]]) -> Decimal:
    n = len(kernel)
    entropy = Decimal(0)
    total = Decimal(0)
    for mask in range(1 << n):
        matrix = [row[:] for row in kernel]
        absent = n - mask.bit_count()
        for i in range(n):
            if not ((mask >> i) & 1):
                matrix[i][i] -= Decimal(1)
        determinant, _ = decimal_det_solve(matrix)
        probability = determinant * (Decimal(-1) if absent % 2 else Decimal(1))
        if probability <= 0:
            raise ArithmeticError("nonpositive Decimal chord atom")
        total += probability
        entropy -= probability * probability.ln()
    if abs(total - Decimal(1)) > Decimal("1e-55"):
        raise ArithmeticError("Decimal chord atoms do not normalize")
    return +entropy


def decimal_chords(
    kernel_np: np.ndarray, direction_np: np.ndarray, steps: list[str]
) -> list[dict[str, str]]:
    with localcontext() as context:
        context.prec = 70
        kernel = decimal_matrix(kernel_np)
        direction = decimal_matrix(direction_np)
        center = decimal_entropy(kernel)
        rows = []
        for step_string in steps:
            step = Decimal(step_string)
            minus = [[x - step * y for x, y in zip(a, b)] for a, b in zip(kernel, direction)]
            plus = [[x + step * y for x, y in zip(a, b)] for a, b in zip(kernel, direction)]
            h_minus = decimal_entropy(minus)
            h_plus = decimal_entropy(plus)
            gap = (h_minus + h_plus) / Decimal(2) - center
            rows.append(
                {
                    "step": step_string,
                    "Hminus": str(+h_minus),
                    "Hplus": str(+h_plus),
                    "midpoint_gap": str(+gap),
                    "central_H2": str(+((h_minus + h_plus - Decimal(2) * center) / (step * step))),
                }
            )
        return rows


def fraction_matrix(matrix: np.ndarray) -> list[list[Fraction]]:
    return [[Fraction(repr(float(value))) for value in row] for row in matrix]


def ldl_pivots(matrix: list[list[Fraction]]) -> list[Fraction]:
    n = len(matrix)
    lower = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    pivots: list[Fraction] = []
    for j in range(n):
        pivot = matrix[j][j] - sum(lower[j][k] ** 2 * pivots[k] for k in range(j))
        if pivot <= 0:
            raise ArithmeticError(f"nonpositive exact LDL pivot {j}")
        pivots.append(pivot)
        for i in range(j + 1, n):
            lower[i][j] = (
                matrix[i][j] - sum(lower[i][k] * lower[j][k] * pivots[k] for k in range(j))
            ) / pivot
    return pivots


def compact_pivots(pivots: list[Fraction]) -> dict[str, int | float | bool]:
    minimum = min(pivots)
    return {
        "count": len(pivots),
        "all_positive": all(value > 0 for value in pivots),
        "minimum_float": float(minimum),
        "minimum_numerator_digits": len(str(abs(minimum.numerator))),
        "minimum_denominator_digits": len(str(minimum.denominator)),
    }


def exact_feasibility(kernel_np: np.ndarray, direction_np: np.ndarray) -> dict[str, object]:
    kernel = fraction_matrix(kernel_np)
    direction = fraction_matrix(direction_np)
    n = len(kernel)
    radius = Fraction(1, 200)
    margin = Fraction(1, 2000)
    endpoints = []
    for step in (-radius, radius):
        shifted = [[kernel[i][j] + step * direction[i][j] for j in range(n)] for i in range(n)]
        lower = [[shifted[i][j] - margin * int(i == j) for j in range(n)] for i in range(n)]
        upper = [[(1 - margin) * int(i == j) - shifted[i][j] for j in range(n)] for i in range(n)]
        endpoints.append(
            {
                "step": str(step),
                "K_minus_margin_I": compact_pivots(ldl_pivots(lower)),
                "I_minus_K_minus_margin_I": compact_pivots(ldl_pivots(upper)),
            }
        )
    return {
        "interpretation": "symmetrized float entries interpreted as exact decimal rationals",
        "uniform_interval": [str(-radius), str(radius)],
        "strict_spectral_margin": str(margin),
        "endpoint_LDL": endpoints,
        "D_positive_definite": compact_pivots(ldl_pivots(direction)),
    }


def aggregate_ledgers() -> dict[str, object]:
    rows: list[dict[str, str]] = []
    manifests = []
    for shard in range(4):
        directory = HERE / f"results_{shard}"
        with (directory / "candidate_ledger.csv").open(encoding="utf-8", newline="") as handle:
            rows.extend(csv.DictReader(handle))
        manifests.append(json.loads((directory / "manifest.json").read_text(encoding="utf-8")))
    best = max(rows, key=lambda row: float(row["rho_psd"]))
    return {
        "row_count": len(rows),
        "positive_status_count": sum(row["status"] != "NO_HIT" for row in rows),
        "best_row": best,
        "manifests": manifests,
    }


def main() -> None:
    started = time.time()
    ledger = aggregate_ledgers()
    best_shard = max(range(4), key=lambda shard: float(ledger["manifests"][shard]["best_rho_psd"]))
    source = HERE / f"results_{best_shard}" / "best_case.npz"
    data = np.load(source)
    raw_kernel = np.asarray(data["kernel"], dtype=float)
    raw_direction = np.asarray(data["direction"], dtype=float)
    kernel = (raw_kernel + raw_kernel.T) / 2.0
    direction = (raw_direction + raw_direction.T) / 2.0
    mixed, _ = mixed_atoms_float(kernel)
    mobius = mobius_atoms_float(kernel)
    strongest_step = str(ledger["best_row"]["chord_step"])
    decimals = [decimal_directional(kernel, direction, precision) for precision in (50, 70)]
    chords = decimal_chords(kernel, direction, [strongest_step, "0.001", "0.0001"])
    certificate = exact_feasibility(kernel, direction)
    float_result = directional_float(kernel, direction)
    report = {
        "status": "HIGH_PRECISION_STABLE_NEGATIVE",
        "scope": "20,000-row float scout plus one frozen strongest-case gate; finite evidence only",
        "ledger": ledger,
        "strongest_shard": best_shard,
        "hashes": {
            "source_npz": sha256(HERE / "source.npz"),
            "best_case_npz": sha256(source),
            "search_script": sha256(HERE.parent / "commuting_spectral_search.py"),
        },
        "symmetrization": {
            "kernel_max_asymmetry": float(np.max(np.abs(raw_kernel - raw_kernel.T))),
            "direction_max_asymmetry": float(np.max(np.abs(raw_direction - raw_direction.T))),
        },
        "spectra_and_commutation": {
            "K_min": float(np.linalg.eigvalsh(kernel)[0]),
            "K_max": float(np.linalg.eigvalsh(kernel)[-1]),
            "D_min": float(np.linalg.eigvalsh(direction)[0]),
            "D_max": float(np.linalg.eigvalsh(direction)[-1]),
            "commutator_frobenius": float(np.linalg.norm(kernel @ direction - direction @ kernel)),
        },
        "event_semantics_float": {
            "event_count": len(mixed),
            "sum_p_minus_one": float(mixed.sum() - 1.0),
            "min_probability": float(mixed.min()),
            "mobius_max_abs_difference": float(np.max(np.abs(mixed - mobius))),
            "mobius_max_relative_difference": float(np.max(np.abs(mixed - mobius) / mixed)),
        },
        "directional_float": float_result,
        "decimal_directional": decimals,
        "decimal_chords": chords,
        "exact_fraction_feasibility": certificate,
        "checks": {
            "all_20000_rows_accounted": ledger["row_count"] == 20000,
            "no_float_candidate_status": ledger["positive_status_count"] == 0,
            "best_rho_below_one": float(ledger["best_row"]["rho_psd"]) < 1.0,
            "decimal_rho_below_one": all(Decimal(row["rho"]) < 1 for row in decimals),
            "decimal_H2_negative": all(Decimal(row["H2"]) < 0 for row in decimals),
            "all_decimal_chords_negative": all(Decimal(row["midpoint_gap"]) < 0 for row in chords),
            "exact_interval_feasible": True,
            "direction_exact_positive_definite": True,
        },
        "exit_code": 0,
        "elapsed_seconds": time.time() - started,
    }
    if not all(report["checks"].values()):
        report["status"] = "FAILED_GATE"
        report["exit_code"] = 1
    output = HERE / "recheck_best.json"
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if report["exit_code"]:
        raise SystemExit(report["exit_code"])


if __name__ == "__main__":
    main()
