#!/usr/bin/env python3
"""Discover an exact PR43 task-D flow or Farkas certificate.

This script may use scipy/sympy for discovery. The companion verifier is the
portable exact checker and should be used to validate the emitted certificate.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.optimize import linprog

import verify_pr43_flow as vf


def to_float_matrix(rows: list[list[Fraction]]) -> np.ndarray:
    return np.array([[float(x) for x in row] for row in rows], dtype=float)


def to_float_vector(vec: list[Fraction]) -> np.ndarray:
    return np.array([float(x) for x in vec], dtype=float)


def to_sympy_matrix(rows: list[list[Fraction]]) -> sp.Matrix:
    return sp.Matrix([[sp.Rational(x.numerator, x.denominator) for x in row] for row in rows])


def to_sympy_vector(vec: list[Fraction]) -> sp.Matrix:
    return sp.Matrix([sp.Rational(x.numerator, x.denominator) for x in vec])


def qs(value: sp.Rational | Fraction | int) -> str:
    if isinstance(value, Fraction):
        return vf.qs(value)
    value = sp.Rational(value)
    if value.q == 1:
        return str(value.p)
    return f"{value.p}/{value.q}"


def solve_exact_on_support(
    a_sym: sp.Matrix,
    b_sym: sp.Matrix,
    support: list[int],
) -> list[sp.Rational] | None:
    if not support:
        return None
    sub = a_sym[:, support]
    if sub.rank() != len(support):
        return None
    try:
        sol = sub.gauss_jordan_solve(b_sym)[0]
    except ValueError:
        return None
    if any(value < 0 for value in sol):
        return None
    residual = sub * sol - b_sym
    if any(value != 0 for value in residual):
        return None
    full = [sp.Rational(0) for _ in range(a_sym.shape[1])]
    for idx, value in zip(support, sol):
        full[idx] = sp.Rational(value)
    return full


def greedy_independent_support(
    a_sym: sp.Matrix,
    candidate_support: list[int],
    scores: np.ndarray,
    rng: random.Random,
) -> list[int]:
    if not candidate_support:
        return []
    if rng.random() < 0.5:
        ordered = sorted(candidate_support, key=lambda i: (-scores[i], i))
    else:
        ordered = candidate_support[:]
        rng.shuffle(ordered)
    selected: list[int] = []
    rank = 0
    for idx in ordered:
        trial = selected + [idx]
        trial_rank = a_sym[:, trial].rank()
        if trial_rank > rank:
            selected = trial
            rank = trial_rank
    return selected


def try_recover_flow(
    instance: vf.Instance,
    solution: np.ndarray,
    a_sym: sp.Matrix,
    b_sym: sp.Matrix,
    out_dir: Path,
    rng: random.Random,
) -> list[sp.Rational] | None:
    thresholds = [1e-7, 1e-8, 1e-9, 1e-10, 1e-11, 1e-12]
    for threshold in thresholds:
        support = [i for i, value in enumerate(solution) if value > threshold]
        exact = solve_exact_on_support(a_sym, b_sym, support)
        if exact is not None:
            return exact
        for _ in range(50):
            selected = greedy_independent_support(a_sym, support, solution, rng)
            exact = solve_exact_on_support(a_sym, b_sym, selected)
            if exact is not None:
                return exact
    # Last resort: rationalize the numerical support and preserve it as a failed candidate.
    approx = [Fraction(str(max(0.0, float(x)))).limit_denominator(10**9) for x in solution]
    residual = [
        sum(instance.a[i][j] * approx[j] for j in range(len(approx))) - instance.b[i]
        for i in range(len(instance.a))
    ]
    failed = {
        "note": "Rationalized numerical flow did not exactly verify.",
        "max_abs_residual": vf.qs(max(abs(x) for x in residual)),
        "support_count": sum(1 for x in approx if x != 0),
    }
    (out_dir / "failed_rationalized_flow.json").write_text(json.dumps(failed, indent=2), encoding="utf-8")
    return None


def discover_flow(instance: vf.Instance, out_dir: Path, rng: random.Random) -> tuple[list[sp.Rational] | None, dict[str, object]]:
    a_np = to_float_matrix(instance.a)
    b_np = to_float_vector(instance.b)
    a_sym = to_sympy_matrix(instance.a)
    b_sym = to_sympy_vector(instance.b)
    bounds = [(0, None)] * len(instance.variables)
    attempts: list[dict[str, object]] = []
    objectives: list[np.ndarray] = [np.zeros(len(instance.variables))]
    for _ in range(80):
        objectives.append(np.array([rng.uniform(-1.0, 1.0) for _ in instance.variables], dtype=float))
    for attempt_index, objective in enumerate(objectives):
        res = linprog(
            c=objective,
            A_eq=a_np,
            b_eq=b_np,
            bounds=bounds,
            method="highs",
            options={"primal_feasibility_tolerance": 1e-10, "dual_feasibility_tolerance": 1e-10},
        )
        attempts.append(
            {
                "attempt": attempt_index,
                "success": bool(res.success),
                "status": int(res.status),
                "message": str(res.message),
                "objective": float(res.fun) if res.success else None,
                "support_gt_1e-9": int(np.sum(res.x > 1e-9)) if res.success else None,
            }
        )
        if res.success:
            exact = try_recover_flow(instance, res.x, a_sym, b_sym, out_dir, rng)
            if exact is not None:
                return exact, {"primal_attempts": attempts}
    return None, {"primal_attempts": attempts}


def solve_exact_farkas_from_active(
    a_sym: sp.Matrix,
    b_sym: sp.Matrix,
    y_float: np.ndarray,
    active_columns: list[int],
    rng: random.Random,
) -> list[sp.Rational] | None:
    rows = [list(a_sym[:, j].T) for j in active_columns]
    rows.append(list(b_sym.T))
    rhs = [sp.Rational(0)] * len(active_columns) + [sp.Rational(-1)]
    eq = sp.Matrix(rows)
    val = sp.Matrix(rhs)
    for _ in range(200):
        selected_rows: list[int] = []
        rank = 0
        order = list(range(eq.rows))
        if rng.random() < 0.7:
            order.sort(key=lambda i: 0 if i == eq.rows - 1 else 1)
        else:
            rng.shuffle(order)
        for idx in order:
            trial = selected_rows + [idx]
            trial_rank = eq[trial, :].rank()
            if trial_rank > rank:
                selected_rows = trial
                rank = trial_rank
        try:
            sol = eq[selected_rows, :].gauss_jordan_solve(val[selected_rows, :])[0]
        except ValueError:
            continue
        if sol.rows != a_sym.rows:
            continue
        at_y = a_sym.T * sol
        b_dot_y = (b_sym.T * sol)[0]
        if all(value >= 0 for value in at_y) and b_dot_y < 0:
            return [sp.Rational(value) for value in sol]
    # Direct rationalization can work when HiGHS returns a simple certificate.
    rat = sp.Matrix([sp.Rational(Fraction(str(float(x))).limit_denominator(10**9).numerator,
                            Fraction(str(float(x))).limit_denominator(10**9).denominator) for x in y_float])
    at_y = a_sym.T * rat
    b_dot_y = (b_sym.T * rat)[0]
    if all(value >= 0 for value in at_y) and b_dot_y < 0:
        return [sp.Rational(value) for value in rat]
    return None


def discover_farkas(instance: vf.Instance, rng: random.Random) -> tuple[list[sp.Rational] | None, dict[str, object]]:
    a_np = to_float_matrix(instance.a)
    b_np = to_float_vector(instance.b)
    a_sym = to_sympy_matrix(instance.a)
    b_sym = to_sympy_vector(instance.b)
    m = len(instance.equations)
    # y is free. Constraints are -A^T y <= 0 and b^T y == -1.
    res = linprog(
        c=np.zeros(m),
        A_ub=-a_np.T,
        b_ub=np.zeros(len(instance.variables)),
        A_eq=b_np.reshape(1, -1),
        b_eq=np.array([-1.0]),
        bounds=[(None, None)] * m,
        method="highs",
        options={"primal_feasibility_tolerance": 1e-10, "dual_feasibility_tolerance": 1e-10},
    )
    details: dict[str, object] = {
        "dual_success": bool(res.success),
        "dual_status": int(res.status),
        "dual_message": str(res.message),
    }
    if not res.success:
        return None, details
    at_y_float = a_np.T @ res.x
    active = [i for i, value in enumerate(at_y_float) if abs(value) < 1e-8]
    details["active_columns_at_1e-8"] = len(active)
    exact = solve_exact_farkas_from_active(a_sym, b_sym, res.x, active, rng)
    return exact, details


def write_flow_certificate(instance: vf.Instance, flow: list[sp.Rational], path: Path) -> None:
    nonzero = {
        instance.variables[i]: qs(value)
        for i, value in enumerate(flow)
        if value != 0
    }
    cert = {
        "outcome": "FEASIBLE_FLOW",
        "source_commit": "4e1369ef2a59ccfaba3ca8fce95d85e78857bf78",
        "task": "CODEX_VERIFICATION_TASKS_v2.md:D",
        "variable_order": instance.variables,
        "flow": {name: "0" for name in instance.variables},
        "nonzero_flow": nonzero,
    }
    for name, value in nonzero.items():
        cert["flow"][name] = value
    path.write_text(json.dumps(cert, indent=2, sort_keys=True), encoding="utf-8")


def write_farkas_certificate(instance: vf.Instance, y: list[sp.Rational], path: Path) -> None:
    cert = {
        "outcome": "FARKAS_INFEASIBILITY",
        "source_commit": "4e1369ef2a59ccfaba3ca8fce95d85e78857bf78",
        "task": "CODEX_VERIFICATION_TASKS_v2.md:D",
        "convention": "For A r = b, r >= 0, y certifies infeasibility if A^T y >= 0 and b^T y < 0.",
        "equation_order": instance.equations,
        "y": {name: qs(y[i]) for i, name in enumerate(instance.equations)},
    }
    path.write_text(json.dumps(cert, indent=2, sort_keys=True), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, default=Path("."))
    parser.add_argument("--seed", type=int, default=4310043)
    parser.add_argument("--no-farkas", action="store_true")
    args = parser.parse_args()

    os.environ.setdefault("OMP_NUM_THREADS", "1")
    os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
    os.environ.setdefault("MKL_NUM_THREADS", "1")
    os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")

    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    rng = random.Random(args.seed)
    instance = vf.build_instance()
    instance_path = out_dir / "instance.json"
    instance_path.write_text(json.dumps(vf.exact_instance_json(instance), indent=2, sort_keys=True), encoding="utf-8")

    flow, flow_details = discover_flow(instance, out_dir, rng)
    discovery: dict[str, object] = {
        "seed": args.seed,
        "variable_count": len(instance.variables),
        "equation_count": len(instance.equations),
        "flow_details": flow_details,
    }
    if flow is not None:
        cert_path = out_dir / "flow_certificate.json"
        write_flow_certificate(instance, flow, cert_path)
        verify_summary = out_dir / "verify_flow_summary.json"
        subprocess.run(
            [sys.executable, str(Path(__file__).with_name("verify_pr43_flow.py")), "--certificate", str(cert_path), "--write-summary", str(verify_summary)],
            cwd=out_dir,
            check=True,
        )
        discovery["outcome"] = "FEASIBLE_FLOW"
        discovery["certificate"] = str(cert_path)
        (out_dir / "discovery_summary.json").write_text(json.dumps(discovery, indent=2, sort_keys=True), encoding="utf-8")
        print(json.dumps(discovery, indent=2, sort_keys=True))
        return 0

    if not args.no_farkas:
        y, farkas_details = discover_farkas(instance, rng)
        discovery["farkas_details"] = farkas_details
        if y is not None:
            cert_path = out_dir / "farkas_certificate.json"
            write_farkas_certificate(instance, y, cert_path)
            verify_summary = out_dir / "verify_farkas_summary.json"
            subprocess.run(
                [sys.executable, str(Path(__file__).with_name("verify_pr43_flow.py")), "--certificate", str(cert_path), "--write-summary", str(verify_summary)],
                cwd=out_dir,
                check=True,
            )
            discovery["outcome"] = "FARKAS_INFEASIBILITY"
            discovery["certificate"] = str(cert_path)
            (out_dir / "discovery_summary.json").write_text(json.dumps(discovery, indent=2, sort_keys=True), encoding="utf-8")
            print(json.dumps(discovery, indent=2, sort_keys=True))
            return 0

    discovery["outcome"] = "UNRESOLVED"
    (out_dir / "discovery_summary.json").write_text(json.dumps(discovery, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(discovery, indent=2, sort_keys=True))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
