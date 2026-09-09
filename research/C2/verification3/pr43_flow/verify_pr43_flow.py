#!/usr/bin/env python3
"""Exact verifier for PR43 task D.

The state convention is explicit: state strings are b3b2b1 in the order
000,001,...,111, and the rightmost bit records occupation of matrix
coordinate 1. Thus 001 means coordinate 1 is occupied and coordinates 2,3
are absent.

The verifier reconstructs the DPP full-event law from inclusion determinants
by Mobius inversion, forms G(T)=V^T (C-E_{T^c})^{-1} V and det(G(T)), builds
the stationary-flow adjoint generator equations, and verifies one exact
certificate.

Farkas convention used here: for A r = b, r >= 0, infeasibility is certified
by a rational vector y with A^T y >= 0 and b^T y < 0.
"""

from __future__ import annotations

import argparse
import itertools
import json
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Iterable


C_LITERAL = [
    ["1/2", "1/12", "1/15"],
    ["1/12", "2/5", "1/20"],
    ["1/15", "1/20", "3/5"],
]

V_LITERAL = [
    ["1", "0"],
    ["0", "1"],
    ["1", "1"],
]

STATE_ORDER = ["000", "001", "010", "011", "100", "101", "110", "111"]
FEATURES = ["G11", "G12", "G22", "detG"]
LAMBDA = {"G11": Fraction(-1), "G12": Fraction(-1), "G22": Fraction(-1), "detG": Fraction(-2)}


def q(value: object) -> Fraction:
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int):
        return Fraction(value, 1)
    if isinstance(value, str):
        return Fraction(value)
    raise TypeError(f"cannot parse rational value {value!r}")


def qs(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def matrix_from_literal(data: list[list[str]]) -> list[list[Fraction]]:
    return [[q(x) for x in row] for row in data]


def det(matrix: list[list[Fraction]]) -> Fraction:
    n = len(matrix)
    if n == 0:
        return Fraction(1)
    a = [row[:] for row in matrix]
    sign = 1
    out = Fraction(1)
    for col in range(n):
        pivot = None
        for row in range(col, n):
            if a[row][col] != 0:
                pivot = row
                break
        if pivot is None:
            return Fraction(0)
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            sign *= -1
        pivot_value = a[col][col]
        out *= pivot_value
        for row in range(col + 1, n):
            factor = a[row][col] / pivot_value
            if factor == 0:
                continue
            for k in range(col, n):
                a[row][k] -= factor * a[col][k]
    return out * sign


def inverse(matrix: list[list[Fraction]]) -> list[list[Fraction]]:
    n = len(matrix)
    a = [row[:] + [Fraction(int(i == j)) for j in range(n)] for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = None
        for row in range(col, n):
            if a[row][col] != 0:
                pivot = row
                break
        if pivot is None:
            raise ValueError("singular matrix")
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
        pivot_value = a[col][col]
        for k in range(2 * n):
            a[col][k] /= pivot_value
        for row in range(n):
            if row == col:
                continue
            factor = a[row][col]
            if factor == 0:
                continue
            for k in range(2 * n):
                a[row][k] -= factor * a[col][k]
    return [row[n:] for row in a]


def transpose(matrix: list[list[Fraction]]) -> list[list[Fraction]]:
    return [list(row) for row in zip(*matrix)]


def matmul(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    rows = len(a)
    inner = len(b)
    cols = len(b[0])
    return [[sum(a[i][k] * b[k][j] for k in range(inner)) for j in range(cols)] for i in range(rows)]


def submatrix(matrix: list[list[Fraction]], indices: Iterable[int]) -> list[list[Fraction]]:
    idx = list(indices)
    return [[matrix[i][j] for j in idx] for i in idx]


def state_bits(state: str) -> tuple[int, int, int]:
    if len(state) != 3 or any(ch not in "01" for ch in state):
        raise ValueError(f"invalid state {state!r}")
    # Return bits in matrix-coordinate order (1,2,3). The state string is b3b2b1.
    return tuple(int(ch) for ch in reversed(state))


def occupied_indices(state: str) -> list[int]:
    return [i for i, bit in enumerate(state_bits(state)) if bit]


def dpp_full_event_probability(c: list[list[Fraction]], state: str) -> Fraction:
    occupied = set(occupied_indices(state))
    absent = [i for i in range(len(c)) if i not in occupied]
    total = Fraction(0)
    for size in range(len(absent) + 1):
        for extra in itertools.combinations(absent, size):
            include = sorted(occupied.union(extra))
            total += ((-1) ** size) * det(submatrix(c, include))
    return total


@dataclass(frozen=True)
class Instance:
    state_order: list[str]
    variables: list[str]
    equations: list[str]
    a: list[list[Fraction]]
    b: list[Fraction]
    mu: list[Fraction]
    g: list[list[list[Fraction]]]
    detg: list[Fraction]
    feature_values: dict[str, list[Fraction]]


def build_instance() -> Instance:
    c = matrix_from_literal(C_LITERAL)
    v = matrix_from_literal(V_LITERAL)
    vt = transpose(v)

    mu: list[Fraction] = []
    g_values: list[list[list[Fraction]]] = []
    detg: list[Fraction] = []
    for state in STATE_ORDER:
        mu.append(dpp_full_event_probability(c, state))
        y = [row[:] for row in c]
        occupied = set(occupied_indices(state))
        for i in range(3):
            if i not in occupied:
                y[i][i] -= 1
        g = matmul(matmul(vt, inverse(y)), v)
        g_values.append(g)
        detg.append(det(g))

    feature_values = {
        "G11": [g[0][0] for g in g_values],
        "G12": [g[0][1] for g in g_values],
        "G22": [g[1][1] for g in g_values],
        "detG": detg,
    }

    ordered_pairs = [(x, y) for x in STATE_ORDER for y in STATE_ORDER if x != y]
    variables = [f"r_{x}_{y}" for x, y in ordered_pairs]
    equations: list[str] = []
    rows: list[list[Fraction]] = []
    rhs: list[Fraction] = []

    pair_index = {pair: i for i, pair in enumerate(ordered_pairs)}
    for state in STATE_ORDER:
        row = [Fraction(0) for _ in variables]
        for other in STATE_ORDER:
            if other == state:
                continue
            row[pair_index[(state, other)]] += 1
            row[pair_index[(other, state)]] -= 1
        equations.append(f"balance:{state}")
        rows.append(row)
        rhs.append(Fraction(0))

    for feature in FEATURES:
        values = feature_values[feature]
        lam = LAMBDA[feature]
        for target_index, target in enumerate(STATE_ORDER):
            row = [Fraction(0) for _ in variables]
            target_value = values[target_index]
            for source_index, source in enumerate(STATE_ORDER):
                if source == target:
                    continue
                row[pair_index[(source, target)]] = values[source_index] - target_value
            equations.append(f"adjoint:{feature}:{target}")
            rows.append(row)
            rhs.append(mu[target_index] * lam * target_value)

    return Instance(STATE_ORDER[:], variables, equations, rows, rhs, mu, g_values, detg, feature_values)


def vector_from_json(data: object, names: list[str]) -> list[Fraction]:
    if isinstance(data, list):
        if len(data) != len(names):
            raise ValueError(f"expected {len(names)} entries, got {len(data)}")
        return [q(x) for x in data]
    if isinstance(data, dict):
        missing = [name for name in names if name not in data]
        extra = [name for name in data if name not in set(names)]
        if missing:
            raise ValueError(f"missing entries: {missing[:5]}")
        if extra:
            raise ValueError(f"unknown entries: {extra[:5]}")
        return [q(data[name]) for name in names]
    raise TypeError("certificate vector must be a list or object")


def dot(left: list[Fraction], right: list[Fraction]) -> Fraction:
    return sum(x * y for x, y in zip(left, right))


def matvec(rows: list[list[Fraction]], vector: list[Fraction]) -> list[Fraction]:
    return [dot(row, vector) for row in rows]


def transpose_matvec(rows: list[list[Fraction]], vector: list[Fraction]) -> list[Fraction]:
    cols = len(rows[0])
    return [sum(rows[i][j] * vector[i] for i in range(len(rows))) for j in range(cols)]


def exact_instance_json(instance: Instance) -> dict[str, object]:
    return {
        "source_commit": "4e1369ef2a59ccfaba3ca8fce95d85e78857bf78",
        "task": "CODEX_VERIFICATION_TASKS_v2.md:D",
        "bit_to_coordinate_convention": {
            "state_string": "b3b2b1",
            "rightmost_bit_b1": "coordinate_1",
            "b2": "coordinate_2",
            "leftmost_bit_b3": "coordinate_3",
            "example": "001 occupies coordinate_1 only",
        },
        "flow_model": "directed stationary flow variables r_xy=mu(x) q_xy for all ordered x!=y; no reversibility constraint r_xy=r_yx is imposed.",
        "C": C_LITERAL,
        "V": V_LITERAL,
        "state_order": instance.state_order,
        "mu": {state: qs(instance.mu[i]) for i, state in enumerate(instance.state_order)},
        "G": {
            state: [[qs(x) for x in row] for row in instance.g[i]]
            for i, state in enumerate(instance.state_order)
        },
        "detG": {state: qs(instance.detg[i]) for i, state in enumerate(instance.state_order)},
        "features": {
            name: {state: qs(values[i]) for i, state in enumerate(instance.state_order)}
            for name, values in instance.feature_values.items()
        },
        "farkas_convention": "For A r = b, r >= 0, y certifies infeasibility if A^T y >= 0 and b^T y < 0.",
        "variables": instance.variables,
        "equations": instance.equations,
        "A": [[qs(x) for x in row] for row in instance.a],
        "b": [qs(x) for x in instance.b],
    }


def verify_flow(instance: Instance, cert: dict[str, object]) -> dict[str, object]:
    flow_data = cert.get("flow")
    flow = vector_from_json(flow_data, instance.variables)
    negative = [(instance.variables[i], flow[i]) for i in range(len(flow)) if flow[i] < 0]
    residual = [lhs - rhs for lhs, rhs in zip(matvec(instance.a, flow), instance.b)]
    bad_equations = [(instance.equations[i], residual[i]) for i in range(len(residual)) if residual[i] != 0]
    ok = not negative and not bad_equations
    return {
        "ok": ok,
        "outcome": "FEASIBLE_FLOW",
        "nonzero_flow_count": sum(1 for x in flow if x != 0),
        "negative_count": len(negative),
        "bad_equation_count": len(bad_equations),
        "min_flow": qs(min(flow)),
        "max_abs_residual": qs(max([abs(x) for x in residual] or [Fraction(0)])),
        "first_negative": [(name, qs(value)) for name, value in negative[:5]],
        "first_bad_equations": [(name, qs(value)) for name, value in bad_equations[:5]],
    }


def verify_farkas(instance: Instance, cert: dict[str, object]) -> dict[str, object]:
    y_data = cert.get("y")
    y = vector_from_json(y_data, instance.equations)
    at_y = transpose_matvec(instance.a, y)
    bad_columns = [(instance.variables[i], at_y[i]) for i in range(len(at_y)) if at_y[i] < 0]
    b_dot_y = dot(instance.b, y)
    ok = not bad_columns and b_dot_y < 0
    return {
        "ok": ok,
        "outcome": "FARKAS_INFEASIBILITY",
        "min_AT_y": qs(min(at_y)),
        "zero_AT_y_count": sum(1 for x in at_y if x == 0),
        "bad_column_count": len(bad_columns),
        "b_dot_y": qs(b_dot_y),
        "first_bad_columns": [(name, qs(value)) for name, value in bad_columns[:5]],
    }


def verify_certificate(instance: Instance, certificate_path: Path) -> dict[str, object]:
    cert = json.loads(certificate_path.read_text(encoding="utf-8"))
    outcome = cert.get("outcome")
    if outcome == "FEASIBLE_FLOW":
        return verify_flow(instance, cert)
    if outcome == "FARKAS_INFEASIBILITY":
        return verify_farkas(instance, cert)
    raise ValueError(f"unknown certificate outcome {outcome!r}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-instance", type=Path)
    parser.add_argument("--certificate", type=Path)
    parser.add_argument("--write-summary", type=Path)
    args = parser.parse_args()

    instance = build_instance()
    result: dict[str, object] = {
        "instance_reconstructed": True,
        "states": instance.state_order,
        "variable_count": len(instance.variables),
        "equation_count": len(instance.equations),
        "mu_positive": all(x > 0 for x in instance.mu),
        "mu_sum": qs(sum(instance.mu)),
    }
    if args.write_instance:
        args.write_instance.write_text(
            json.dumps(exact_instance_json(instance), indent=2, sort_keys=True),
            encoding="utf-8",
        )
        result["instance_written"] = str(args.write_instance)
    if args.certificate:
        result["certificate"] = verify_certificate(instance, args.certificate)

    text = json.dumps(result, indent=2, sort_keys=True)
    if args.write_summary:
        args.write_summary.write_text(text + "\n", encoding="utf-8")
    print(text)
    if args.certificate and not result["certificate"]["ok"]:  # type: ignore[index]
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
