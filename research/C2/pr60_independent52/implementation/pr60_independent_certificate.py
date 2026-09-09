#!/usr/bin/env python3
"""Independent exact checker for the PR60 full-r issue52 certificate.

This script constructs the displayed Rstar and Rbar matrices, extracts P from
the determinant of Ahat, and only then compares against the static author
component strings.  It deliberately does not import or execute the PR60 author
checker files.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import os
import platform
import sys
import time
import traceback
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

for _thread_var in (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
):
    os.environ.setdefault(_thread_var, "1")

import sympy as sp


MU, NU, R, U, T = sp.symbols("mu nu r u t")
X, Y, RCHART, TCHART = sp.symbols("X Y R T")
VARS = (MU, NU, R, T)
CHART_VARS = (X, Y, RCHART, TCHART)


EXPECTED_Q_GROUP_COUNTS = [
    [63, 71, 71, 71, 57],
    [71, 71, 71, 71, 71],
    [71, 71, 71, 71, 71],
    [71, 71, 71, 71, 71],
    [57, 71, 71, 71, 63],
]

EXPECTED_Q_GROUP_MINIMA = [
    [432, 256, 448, 192, 256],
    [256, 1664, 2624, 1408, 192],
    [448, 2624, 4352, 2624, 448],
    [192, 1408, 2624, 1664, 256],
    [256, 192, 448, 256, 432],
]

EXPECTED_SEED_MINORS = [
    sp.Rational(1009, 7200),
    sp.Rational(743633, 6480000),
    sp.Rational(1137143, 12150000),
    sp.Rational(9016, 253125),
]


class DeadlineExceeded(RuntimeError):
    pass


class Checker:
    def __init__(self, input_root: Path, out_dir: Path, wall_seconds: int, memory_gib: int) -> None:
        self.input_root = input_root.resolve()
        self.out_dir = out_dir.resolve()
        self.out_dir.mkdir(parents=True, exist_ok=True)
        self.start_time = time.time()
        self.deadline_epoch = self._compute_deadline(wall_seconds)
        self.steps: list[dict[str, Any]] = []
        self.memory_limit_result = self._try_apply_memory_limit(memory_gib)
        self.metadata = self._metadata(wall_seconds, memory_gib)
        self.write_json("run_metadata.json", self.metadata)
        self.write_json("layer_results.json", {"steps": self.steps})

    def _compute_deadline(self, wall_seconds: int) -> float:
        candidates = [self.start_time + wall_seconds]
        raw = os.environ.get("C2_ABSOLUTE_DEADLINE_EPOCH")
        if raw:
            try:
                candidates.append(float(raw))
            except ValueError:
                pass
        return min(candidates)

    def _try_apply_memory_limit(self, memory_gib: int) -> dict[str, Any]:
        limit_bytes = int(memory_gib * (1024**3))
        try:
            import resource  # type: ignore

            soft, hard = resource.getrlimit(resource.RLIMIT_AS)
            new_soft = limit_bytes if soft in (-1, resource.RLIM_INFINITY) else min(soft, limit_bytes)
            new_hard = hard
            if hard in (-1, resource.RLIM_INFINITY):
                new_hard = limit_bytes
            else:
                new_hard = min(hard, limit_bytes)
            resource.setrlimit(resource.RLIMIT_AS, (new_soft, new_hard))
            return {"requested_bytes": limit_bytes, "applied": True, "soft": new_soft, "hard": new_hard}
        except Exception as exc:  # pragma: no cover - platform dependent
            return {"requested_bytes": limit_bytes, "applied": False, "reason": repr(exc)}

    def _metadata(self, wall_seconds: int, memory_gib: int) -> dict[str, Any]:
        binding = {}
        binding_path = self.input_root / "SOURCE_BINDING.json"
        if binding_path.exists():
            binding = json.loads(binding_path.read_text(encoding="utf-8"))
        return {
            "status": "RUNNING",
            "pid": os.getpid(),
            "argv": sys.argv,
            "start_utc": datetime.now(timezone.utc).isoformat(),
            "input_root": str(self.input_root),
            "out_dir": str(self.out_dir),
            "wall_seconds": wall_seconds,
            "deadline_epoch": self.deadline_epoch,
            "deadline_utc": datetime.fromtimestamp(self.deadline_epoch, timezone.utc).isoformat(),
            "python": sys.version,
            "sympy": sp.__version__,
            "platform": platform.platform(),
            "thread_env": {name: os.environ.get(name) for name in (
                "OMP_NUM_THREADS",
                "OPENBLAS_NUM_THREADS",
                "MKL_NUM_THREADS",
                "NUMEXPR_NUM_THREADS",
                "VECLIB_MAXIMUM_THREADS",
            )},
            "memory_limit": self.memory_limit_result,
            "source_binding": binding,
            "construction_guard": {
                "forbidden_author_scripts": [
                    str(self.input_root / "pr60" / "certificate.py"),
                    str(self.input_root / "pr60" / "bridge_checks.py"),
                ],
                "author_components_used_after_fresh_P": True,
            },
        }

    def check_deadline(self, label: str) -> None:
        if time.time() > self.deadline_epoch:
            raise DeadlineExceeded(f"deadline exceeded before {label}")

    def begin(self, name: str) -> None:
        self.check_deadline(name)
        self.steps.append({
            "name": name,
            "status": "RUNNING",
            "start_utc": datetime.now(timezone.utc).isoformat(),
        })
        self.write_json("layer_results.json", {"steps": self.steps})

    def pass_step(self, name: str, details: dict[str, Any] | None = None) -> None:
        for step in reversed(self.steps):
            if step["name"] == name and step["status"] == "RUNNING":
                step["status"] = "PASS"
                step["end_utc"] = datetime.now(timezone.utc).isoformat()
                step["elapsed_seconds"] = round(time.time() - self.start_time, 3)
                if details is not None:
                    step["details"] = details
                self.write_json("layer_results.json", {"steps": self.steps})
                self.check_deadline(name)
                return
        raise RuntimeError(f"internal step bookkeeping failure: {name}")

    def fail(self, exc: BaseException) -> None:
        for step in reversed(self.steps):
            if step["status"] == "RUNNING":
                step["status"] = "FAIL"
                step["end_utc"] = datetime.now(timezone.utc).isoformat()
                step["error"] = repr(exc)
                break
        self.metadata["status"] = "FAIL"
        self.metadata["end_utc"] = datetime.now(timezone.utc).isoformat()
        self.write_json("run_metadata.json", self.metadata)
        self.write_json("layer_results.json", {"steps": self.steps})
        self.write_json("FAILURE.json", {
            "status": "FAIL",
            "error": repr(exc),
            "traceback": traceback.format_exc(),
            "elapsed_seconds": round(time.time() - self.start_time, 3),
        })

    def success(self) -> None:
        self.metadata["status"] = "PASS"
        self.metadata["end_utc"] = datetime.now(timezone.utc).isoformat()
        self.metadata["elapsed_seconds"] = round(time.time() - self.start_time, 3)
        self.write_json("run_metadata.json", self.metadata)
        self.write_json("PASS.json", {
            "status": "MACHINE_PASS",
            "elapsed_seconds": self.metadata["elapsed_seconds"],
            "boundary": "C2 machine arithmetic only; C1 owns analytic bridge/theorem acceptance.",
        })

    def write_json(self, rel_path: str, payload: Any) -> None:
        path = self.out_dir / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = path.with_name(path.name + ".tmp")
        tmp_path.write_text(json.dumps(json_safe(payload), indent=2, sort_keys=True), encoding="utf-8")
        os.replace(tmp_path, path)


def json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(item) for item in value]
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, sp.Float):
        raise ValueError(f"refusing to serialize SymPy Float: {value}")
    if isinstance(value, sp.Integer):
        return int(value)
    if isinstance(value, sp.Rational):
        return rat_to_json(value)
    if isinstance(value, sp.Basic):
        return expr_string(value)
    return value


def reject_floats(obj: Any, label: str) -> None:
    floats: set[sp.Float] = set()
    if isinstance(obj, sp.MatrixBase):
        for entry in obj:
            floats.update(entry.atoms(sp.Float))
    elif isinstance(obj, sp.Poly):
        floats.update(obj.as_expr().atoms(sp.Float))
    elif isinstance(obj, sp.Basic):
        floats.update(obj.atoms(sp.Float))
    elif isinstance(obj, dict):
        for value in obj.values():
            reject_floats(value, label)
        return
    elif isinstance(obj, (list, tuple)):
        for value in obj:
            reject_floats(value, label)
        return
    if floats:
        raise ValueError(f"Float atoms detected in {label}: {sorted(map(str, floats))[:5]}")


def rat_to_json(value: Any) -> int | dict[str, int]:
    q = sp.Rational(value)
    if q.q == 1:
        return int(q.p)
    return {"num": int(q.p), "den": int(q.q)}


def expr_string(expr: sp.Expr) -> str:
    return sp.sstr(expr, order="lex")


def matrix_strings(mat: sp.MatrixBase) -> list[list[str]]:
    return [[expr_string(mat[i, j]) for j in range(mat.cols)] for i in range(mat.rows)]


def poly_from_expr(expr: sp.Expr, variables: tuple[sp.Symbol, ...], label: str) -> sp.Poly:
    expr = sp.cancel(sp.together(expr))
    reject_floats(expr, label)
    try:
        return sp.Poly(expr, *variables, domain=sp.QQ)
    except Exception as exc:
        num, den = sp.fraction(expr)
        raise ValueError(f"{label} is not a polynomial over QQ; denominator is {expr_string(den)}") from exc


def assert_zero_expr(expr: sp.Expr, variables: tuple[sp.Symbol, ...], label: str) -> None:
    poly = poly_from_expr(expr, variables, label)
    if not poly.is_zero:
        terms = poly.terms()[:10]
        raise AssertionError(f"{label} is nonzero; first terms {terms}")


def poly_summary(poly: sp.Poly, variables: tuple[sp.Symbol, ...]) -> dict[str, Any]:
    if poly.is_zero:
        return {
            "terms": 0,
            "degrees": [-1 for _ in variables],
            "total_degree": -1,
            "domain": str(poly.domain),
        }
    return {
        "terms": int(len(poly.terms())),
        "degrees": [int(poly.degree(var)) for var in variables],
        "total_degree": int(poly.total_degree()),
        "domain": str(poly.domain),
    }


def poly_coefficients(poly: sp.Poly, variables: tuple[sp.Symbol, ...]) -> list[dict[str, Any]]:
    normalized = sp.Poly(poly.as_expr(), *variables, domain=sp.QQ)
    items = []
    for monom, coeff in sorted(normalized.terms(), key=lambda item: item[0]):
        items.append({"exp": list(monom), "coeff": rat_to_json(coeff)})
    return items


def integer_coefficients(poly: sp.Poly, variables: tuple[sp.Symbol, ...], label: str) -> dict[tuple[int, ...], int]:
    normalized = sp.Poly(poly.as_expr(), *variables, domain=sp.QQ)
    out: dict[tuple[int, ...], int] = {}
    for monom, coeff in normalized.terms():
        coeff_q = sp.Rational(coeff)
        if coeff_q.q != 1:
            raise AssertionError(f"{label} has noninteger coefficient {coeff_q} at {monom}")
        out[tuple(int(e) for e in monom)] = int(coeff_q.p)
    return out


def common_scalars(time_var: sp.Symbol) -> dict[str, sp.Expr]:
    a = (1 + R) / 2
    b = (1 - R) / 2
    v = (1 - MU**2) / 4
    w = (1 - NU**2) / 4
    j = 1 - time_var
    ell = 1 - R**2 * time_var
    c = 1 - R**2 * time_var**2
    d0 = (1 / j + 1 / ell) / 2
    d1 = (1 / j - 1 / ell) / 2
    theta = a * NU + b * MU
    delta = sp.diag(1, v, w, v * w)
    s = sp.Matrix([
        [MU * NU, 2 * v * NU, 2 * w * MU, 4 * v * w],
        [2 * v * NU, -MU * NU * v, 4 * v * w, -2 * MU * v * w],
        [2 * w * MU, 4 * v * w, -MU * NU * w, -2 * NU * v * w],
        [4 * v * w, -2 * MU * v * w, -2 * NU * v * w, MU * NU * v * w],
    ])
    g = d0 * delta + d1 * s
    la = sp.Matrix([-2 * b, theta, 0, 2 * a * w])
    lb = sp.Matrix([-2 * a, 0, theta, 2 * b * v])
    return {
        "a": a,
        "b": b,
        "v": v,
        "w": w,
        "J": j,
        "L": ell,
        "C": c,
        "d0": d0,
        "d1": d1,
        "theta": theta,
        "Delta": delta,
        "S": s,
        "G": g,
        "la": la,
        "lb": lb,
    }


def build_rstar_u() -> sp.Matrix:
    scal = common_scalars(U**4)
    a, b, v, w = scal["a"], scal["b"], scal["v"], scal["w"]
    j, ell = scal["J"], scal["L"]
    g = scal["G"]
    d1 = scal["d1"]
    la, lb = scal["la"], scal["lb"]
    n1 = 4 * U * (1 / j - R / ell)
    n2 = 4 * U * (1 / j + R / ell)
    n3 = 4 * U**3 * (1 - R**2) / (j * ell)
    d_alpha = n2 * a * U**2 * v / 2
    d_beta = n1 * b * U**2 * w / 2
    r_diag = sp.diag(0, 1 / U, 1 / U, 2 / U)
    g_prime = g.applyfunc(lambda entry: sp.diff(entry, U))
    r0 = 4 * (r_diag.T * g + g * r_diag + g_prime) + sp.diag(
        0,
        n2 * v / (2 * U**2 * a),
        n1 * w / (2 * U**2 * b),
        n3 * v * w / (2 * U**4 * a * b),
    )
    ell_alpha = 8 * U * v * d1 * la
    ell_beta = 8 * U * w * d1 * lb
    rstar = r0 - (ell_alpha * ell_alpha.T) / (4 * d_alpha) - (ell_beta * ell_beta.T) / (4 * d_beta)
    return rstar.applyfunc(lambda entry: sp.cancel(sp.together(entry)))


def build_rbar_t() -> sp.Matrix:
    scal = common_scalars(T)
    a, b, v, w = scal["a"], scal["b"], scal["v"], scal["w"]
    j, ell = scal["J"], scal["L"]
    g = scal["G"]
    la, lb = scal["la"], scal["lb"]
    e_diag = sp.diag(0, 1, 1, 2)
    g_t = g.applyfunc(lambda entry: sp.diff(entry, T))
    rbar = (
        e_diag * g
        + g * e_diag
        + 4 * T * g_t
        + sp.diag(0, v * (1 - R * T) / (j * ell), w * (1 + R * T) / (j * ell), 2 * v * w / (j * ell))
        - 4 * v * b**2 * T**2 / (j * ell * (1 - R * T)) * (la * la.T)
        - 4 * w * a**2 * T**2 / (j * ell * (1 + R * T)) * (lb * lb.T)
    )
    return rbar.applyfunc(lambda entry: sp.cancel(sp.together(entry)))


def verify_bernoulli_gram() -> dict[str, Any]:
    scal = common_scalars(T)
    a, b, v, w = scal["a"], scal["b"], scal["v"], scal["w"]
    j, ell = scal["J"], scal["L"]
    g = scal["G"]
    alpha, beta, gamma, eta, xi, omega = sp.symbols("alpha beta gamma eta xi omega")
    qdot_vars = (MU, NU, R, U, alpha, beta, gamma, eta, xi, omega)
    m = gamma + U**2 * a * v * alpha + U**2 * b * w * beta
    p = -U**2 * a * MU * alpha - 2 * U * a * xi
    q = -U**2 * b * NU * beta - 2 * U * b * omega
    h = 2 * U**2 * a * b * eta

    gram = sp.zeros(4, 4)
    qdot_checks = []
    for i, leaf_i in enumerate((-1, 1)):
        for jj, leaf_j in enumerate((-1, 1)):
            e = sp.Rational(leaf_i, 2) - MU / 2
            f = sp.Rational(leaf_j, 2) - NU / 2
            pij = (1 + leaf_i * MU) * (1 + leaf_j * NU) / 4
            den = j if i == jj else ell
            basis = sp.Matrix([1, e, f, e * f])
            gram += pij * (basis * basis.T) / den
            qvec = sp.Matrix([
                U**2 * a * e**2,
                U**2 * b * f**2,
                1,
                2 * U**2 * a * b * e * f,
                -2 * U * a * e,
                -2 * U * b * f,
            ])
            zeta = sp.Matrix([alpha, beta, gamma, eta, xi, omega])
            reduced = m + p * e + q * f + h * e * f
            assert_zero_expr(qvec.dot(zeta) - reduced, qdot_vars, f"qdot_reduction_{i}_{jj}")
            qdot_checks.append([i, jj])
    for row in range(4):
        for col in range(4):
            assert_zero_expr(gram[row, col] - g[row, col], VARS, f"bernoulli_gram_{row}_{col}")
    delta = scal["Delta"]
    s = scal["S"]
    reflection_residual = s * delta.inv() * s - delta
    for row in range(4):
        for col in range(4):
            assert_zero_expr(reflection_residual[row, col], (MU, NU), f"reflection_identity_{row}_{col}")
    return {"qdot_reductions": qdot_checks, "gram_entries": 16, "reflection_entries": 16}


def build_ahat(rbar: sp.Matrix) -> tuple[sp.Matrix, list[list[sp.Poly]], dict[str, Any]]:
    scal = common_scalars(T)
    v, w = scal["v"], scal["w"]
    j, ell, c = scal["J"], scal["L"], scal["C"]
    row_scales = [1, 1 / v, 1 / w, 1 / (v * w)]
    ahat = sp.zeros(4, 4)
    ahat_polys: list[list[sp.Poly]] = [[sp.Poly(0, *VARS, domain=sp.QQ) for _ in range(4)] for _ in range(4)]
    summaries: list[dict[str, Any]] = []
    for row in range(4):
        for col in range(4):
            entry = 2 * j**2 * ell**2 * c * row_scales[row] * rbar[row, col]
            poly = poly_from_expr(entry, VARS, f"Ahat_{row}_{col}")
            ahat[row, col] = poly.as_expr()
            ahat_polys[row][col] = poly
            summaries.append({"entry": [row, col], **poly_summary(poly, VARS)})
    return ahat, ahat_polys, {"entry_summaries": summaries}


def poly_zero() -> sp.Poly:
    return sp.Poly(0, *VARS, domain=sp.QQ)


def poly_one() -> sp.Poly:
    return sp.Poly(1, *VARS, domain=sp.QQ)


def exact_poly_div(numer: sp.Poly, denom: sp.Poly, label: str) -> sp.Poly:
    if denom.is_zero:
        raise ZeroDivisionError(f"zero polynomial divisor in {label}")
    quotient, remainder = numer.div(denom)
    if not remainder.is_zero:
        raise AssertionError(f"non-exact polynomial division in {label}: {remainder.terms()[:10]}")
    return quotient


def determinant_bareiss_poly(mat: list[list[sp.Poly]]) -> tuple[sp.Poly, dict[str, Any]]:
    n = len(mat)
    work = [[mat[row][col] for col in range(n)] for row in range(n)]
    previous = poly_one()
    sign = 1
    pivots: list[dict[str, Any]] = []
    for k in range(n - 1):
        pivot_row = pivot_col = None
        for row in range(k, n):
            for col in range(k, n):
                if not work[row][col].is_zero:
                    pivot_row, pivot_col = row, col
                    break
            if pivot_row is not None:
                break
        if pivot_row is None or pivot_col is None:
            return poly_zero(), {"pivots": pivots, "zero_rank_at": k}
        if pivot_row != k:
            work[k], work[pivot_row] = work[pivot_row], work[k]
            sign *= -1
        if pivot_col != k:
            for row in range(n):
                work[row][k], work[row][pivot_col] = work[row][pivot_col], work[row][k]
            sign *= -1
        pivot = work[k][k]
        next_work = [[work[row][col] for col in range(n)] for row in range(n)]
        for row in range(k + 1, n):
            for col in range(k + 1, n):
                numer = work[row][col] * pivot - work[row][k] * work[k][col]
                next_work[row][col] = exact_poly_div(numer, previous, f"bareiss_step_{k}_{row}_{col}") if k else numer
        for row in range(k + 1, n):
            next_work[row][k] = poly_zero()
        for col in range(k + 1, n):
            next_work[k][col] = poly_zero()
        pivots.append({
            "step": k,
            "row_swap": [k, pivot_row] if pivot_row != k else None,
            "col_swap": [k, pivot_col] if pivot_col != k else None,
            "pivot_summary": poly_summary(pivot, VARS),
        })
        previous = pivot
        work = next_work
    det = work[n - 1][n - 1]
    if sign == -1:
        det = -det
    return det, {"pivots": pivots}


def determinant_by_permutation_poly(mat: list[list[sp.Poly]]) -> sp.Poly:
    total = poly_zero()
    for perm in itertools.permutations(range(4)):
        inv_count = sum(1 for i in range(4) for j in range(i + 1, 4) if perm[i] > perm[j])
        sign = -1 if inv_count % 2 else 1
        term = sp.Poly(sign, *VARS, domain=sp.QQ)
        for row, col in enumerate(perm):
            term *= mat[row][col]
        total = total + term
    return total


def extract_p_from_determinant(ahat_polys: list[list[sp.Poly]]) -> tuple[sp.Poly, sp.Poly, dict[str, Any]]:
    j = 1 - T
    ell = 1 - R**2 * T
    c = 1 - R**2 * T**2
    det_poly, bareiss_details = determinant_bareiss_poly(ahat_polys)
    reject_floats(det_poly, "determinant_bareiss_poly")
    det_perm = determinant_by_permutation_poly(ahat_polys)
    if not (det_poly - det_perm).is_zero:
        raise AssertionError(f"determinant Bareiss/permutation mismatch: {(det_poly - det_perm).terms()[:10]}")
    divisor_poly = sp.Poly(8 * T * j**3 * ell**3 * c**3, *VARS, domain=sp.QQ)
    quotient = exact_poly_div(det_poly, divisor_poly, "determinant_extract_P")
    p_ints = integer_coefficients(quotient, VARS, "P")
    p_summary = poly_summary(quotient, VARS)
    if p_summary["terms"] != 279:
        raise AssertionError(f"P term count mismatch: {p_summary['terms']}")
    if p_summary["degrees"] != [4, 4, 10, 6]:
        raise AssertionError(f"P degrees mismatch: {p_summary['degrees']}")
    scaling_residual = det_poly - divisor_poly * quotient
    if not scaling_residual.is_zero:
        raise AssertionError("internal determinant scaling residual became nonzero")
    details = {
        "determinant_summary": poly_summary(det_poly, VARS),
        "divisor_summary": poly_summary(divisor_poly, VARS),
        "P_summary": p_summary,
        "P_integer_terms": len(p_ints),
        "remainder_zero": True,
        "determinant_methods": ["own_fraction_free_bareiss_QQ_poly", "independent_24_product_QQ_poly"],
        "bareiss_details": bareiss_details,
    }
    return quotient, det_poly, details


def parse_component_expr(text: str, label: str) -> sp.Expr:
    normalized = text.replace("^", "**")
    locals_map = {
        "mu": MU,
        "nu": NU,
        "r": R,
        "t": T,
        "Integer": sp.Integer,
        "Rational": sp.Rational,
    }
    expr = sp.sympify(normalized, locals=locals_map)
    reject_floats(expr, label)
    return expr


def get_component_text(value: Any, key: str) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        for text_key in ("expr", "expression", "rhs", "value", "text", "literal"):
            if text_key in value and isinstance(value[text_key], str):
                return value[text_key]
    raise TypeError(f"reference component {key} is not a recognized expression string")


def load_author_components(input_root: Path) -> tuple[sp.Expr, dict[str, Any]]:
    path = input_root / "reference_P_components.json"
    raw = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(raw, dict) and "components" in raw and isinstance(raw["components"], dict):
        data = raw["components"]
    else:
        data = raw
    required = ("c40", "c31", "c22", "c20", "c11", "c00")
    missing = [key for key in required if key not in data]
    if missing:
        raise KeyError(f"missing reference components: {missing}")
    comp = {key: parse_component_expr(get_component_text(data[key], key), key) for key in required}
    p_ref = (
        comp["c40"] * MU**4
        + comp["c31"] * MU**3 * NU
        + comp["c22"] * MU**2 * NU**2
        + comp["c31"].subs(R, -R) * MU * NU**3
        + comp["c40"].subs(R, -R) * NU**4
        + comp["c20"] * MU**2
        + comp["c11"] * MU * NU
        + comp["c20"].subs(R, -R) * NU**2
        + comp["c00"]
    )
    summaries = {
        key: poly_summary(poly_from_expr(expr, (R, T), f"reference_{key}"), (R, T))
        for key, expr in comp.items()
    }
    p_ref_poly = sp.Poly(p_ref, *VARS, domain=sp.QQ)
    return p_ref_poly.as_expr(), summaries


def verify_p_symmetries(p_poly: sp.Poly) -> dict[str, Any]:
    p_expr = p_poly.as_expr()
    signflip = p_expr.subs([(MU, -MU), (NU, -NU)], simultaneous=True) - p_expr
    leafswap = p_expr.subs([(MU, NU), (NU, MU), (R, -R)], simultaneous=True) - p_expr
    assert_zero_expr(signflip, VARS, "P_signflip")
    assert_zero_expr(leafswap, VARS, "P_leafswap")
    return {"P_signflip": "PASS", "P_leafswap": "PASS"}


def axis_transform_array(k: int, degree: int, lo: int, hi: int) -> list[int]:
    arr = [0] * (degree + 1)
    for i in range(k + 1):
        left = math.comb(k, i) * (lo ** (k - i)) * (hi**i)
        if left == 0:
            continue
        for h in range(degree - k + 1):
            arr[i + h] += left * math.comb(degree - k, h)
    return arr


def transform_p_to_q_by_loops(p_poly: sp.Poly) -> dict[tuple[int, int, int, int], int]:
    p_coeffs = integer_coefficients(p_poly, VARS, "P")
    q_coeffs: defaultdict[tuple[int, int, int, int], int] = defaultdict(int)
    axis_specs = [(4, -1, 1), (4, -1, 1), (10, 0, 1), (6, 0, 1)]
    array_cache: dict[tuple[int, int, int, int], list[int]] = {}
    for monom, coeff in p_coeffs.items():
        arrays = []
        for k, (degree, lo, hi) in zip(monom, axis_specs):
            cache_key = (k, degree, lo, hi)
            if cache_key not in array_cache:
                array_cache[cache_key] = axis_transform_array(k, degree, lo, hi)
            arrays.append(array_cache[cache_key])
        for ix, cx in enumerate(arrays[0]):
            if cx == 0:
                continue
            for iy, cy in enumerate(arrays[1]):
                if cy == 0:
                    continue
                for ir, cr in enumerate(arrays[2]):
                    if cr == 0:
                        continue
                    for it, ct in enumerate(arrays[3]):
                        if ct:
                            q_coeffs[(ix, iy, ir, it)] += coeff * cx * cy * cr * ct
    return dict(q_coeffs)


def q_expr_from_coeffs(q_coeffs: dict[tuple[int, int, int, int], int]) -> sp.Expr:
    expr = sp.Integer(0)
    for (ix, iy, ir, it), coeff in q_coeffs.items():
        if coeff:
            expr += sp.Integer(coeff) * X**ix * Y**iy * RCHART**ir * TCHART**it
    return expr


def chart_axis_poly(k: int, degree: int, lo: int, hi: int, variable: sp.Symbol) -> sp.Poly:
    return sp.Poly((lo + hi * variable) ** k * (1 + variable) ** (degree - k), *CHART_VARS, domain=sp.ZZ)


def q_by_homogeneous_polynomial(p_poly: sp.Poly) -> sp.Poly:
    p_coeffs = integer_coefficients(p_poly, VARS, "P")
    axis_specs = [
        (4, -1, 1, X),
        (4, -1, 1, Y),
        (10, 0, 1, RCHART),
        (6, 0, 1, TCHART),
    ]
    cache: dict[tuple[int, int, int, int, sp.Symbol], sp.Poly] = {}
    total = sp.Poly(0, *CHART_VARS, domain=sp.ZZ)
    for monom, coeff in p_coeffs.items():
        term = sp.Poly(coeff, *CHART_VARS, domain=sp.ZZ)
        for k, (degree, lo, hi, variable) in zip(monom, axis_specs):
            key = (k, degree, lo, hi, variable)
            if key not in cache:
                cache[key] = chart_axis_poly(k, degree, lo, hi, variable)
            term *= cache[key]
        total += term
    return total


def verify_q_homogeneous_polynomial(p_poly: sp.Poly, q_coeffs: dict[tuple[int, int, int, int], int]) -> dict[str, Any]:
    direct_poly = q_by_homogeneous_polynomial(p_poly)
    reject_floats(direct_poly, "Q_homogeneous_polynomial")
    loop_poly = sp.Poly(q_expr_from_coeffs(q_coeffs), *CHART_VARS, domain=sp.ZZ)
    residual = sp.Poly(direct_poly.as_expr() - loop_poly.as_expr(), *CHART_VARS, domain=sp.QQ)
    if not residual.is_zero:
        raise AssertionError(f"Q homogeneous polynomial mismatch: {residual.terms()[:10]}")
    return {
        "homogeneous_summary": poly_summary(direct_poly, CHART_VARS),
        "loop_summary": poly_summary(loop_poly, CHART_VARS),
    }


def verify_q_box(q_coeffs: dict[tuple[int, int, int, int], int]) -> dict[str, Any]:
    positives = 0
    zeros = 0
    minimum: int | None = None
    group_counts = [[0 for _ in range(5)] for _ in range(5)]
    group_minima: list[list[int | None]] = [[None for _ in range(5)] for _ in range(5)]
    full_box = []
    for ix in range(5):
        for iy in range(5):
            for ir in range(11):
                for it in range(7):
                    key = (ix, iy, ir, it)
                    coeff = q_coeffs.get(key, 0)
                    if coeff > 0:
                        positives += 1
                        group_counts[ix][iy] += 1
                        minimum = coeff if minimum is None else min(minimum, coeff)
                        group_minima[ix][iy] = coeff if group_minima[ix][iy] is None else min(group_minima[ix][iy], coeff)
                    elif coeff == 0:
                        zeros += 1
                    else:
                        raise AssertionError(f"negative Q coefficient {coeff} at {key}")
                    full_box.append({"exp": [ix, iy, ir, it], "coeff": coeff})
    if positives != 1731:
        raise AssertionError(f"Q positive count mismatch: {positives}")
    if zeros != 194:
        raise AssertionError(f"Q zero count mismatch: {zeros}")
    if minimum != 192:
        raise AssertionError(f"Q minimum mismatch: {minimum}")
    if q_coeffs.get((0, 0, 0, 0), 0) != 432:
        raise AssertionError(f"Q constant mismatch: {q_coeffs.get((0, 0, 0, 0), 0)}")
    if group_counts != EXPECTED_Q_GROUP_COUNTS:
        raise AssertionError(f"Q group counts mismatch: {group_counts}")
    if group_minima != EXPECTED_Q_GROUP_MINIMA:
        raise AssertionError(f"Q group minima mismatch: {group_minima}")
    return {
        "positive": positives,
        "zero": zeros,
        "minimum": minimum,
        "constant": q_coeffs[(0, 0, 0, 0)],
        "group_counts": group_counts,
        "group_minima": group_minima,
        "full_box": full_box,
    }


def verify_seed_and_leafswap(rbar: sp.Matrix) -> dict[str, Any]:
    seed_matrix = rbar.subs({MU: 0, NU: 0, R: 0, T: sp.Rational(1, 16)})
    seed_minors = []
    for size in range(1, 5):
        minor = sp.cancel(sp.together(seed_matrix[:size, :size].det(method="bareiss")))
        seed_minors.append(minor)
    if seed_minors != EXPECTED_SEED_MINORS:
        raise AssertionError(f"seed leading minors mismatch: {seed_minors}")

    swap = sp.Matrix([
        [1, 0, 0, 0],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
    ])
    swapped_params = rbar.subs([(MU, NU), (NU, MU), (R, -R)], simultaneous=True)
    residual = rbar - swap.T * swapped_params * swap
    for row in range(4):
        for col in range(4):
            assert_zero_expr(residual[row, col], VARS, f"Rbar_leafswap_congruence_{row}_{col}")
    return {
        "seed_leading_minors": [expr_string(value) for value in seed_minors],
        "Rbar_leafswap_congruence": "PASS",
    }


def verify_det_scaling_summary(p_poly: sp.Poly, det_poly: sp.Poly) -> dict[str, Any]:
    j = 1 - T
    ell = 1 - R**2 * T
    c = 1 - R**2 * T**2
    rstar_det_formula = (1 - MU**2) ** 2 * (1 - NU**2) ** 2 * p_poly.as_expr() / (2 * j**5 * ell**5 * c)
    rbar_det_formula = T * rstar_det_formula / 256
    v = (1 - MU**2) / 4
    w = (1 - NU**2) / 4
    ahat_from_rbar_formula = (2 * j**2 * ell**2 * c) ** 4 * rbar_det_formula / (v**2 * w**2)
    assert_zero_expr(det_poly.as_expr() - ahat_from_rbar_formula, VARS, "detAhat_to_Rstar_scaling")
    return {
        "det_Rstar_formula": expr_string(rstar_det_formula),
        "det_Rbar_formula": expr_string(rbar_det_formula),
        "detAhat_scaling_to_Rstar": "PASS",
    }


def run(checker: Checker) -> None:
    checker.begin("input_presence")
    required = [
        checker.input_root / "pr60" / "proof.md",
        checker.input_root / "main" / "STRUCTURE.md",
        checker.input_root / "reference_P_components.json",
        checker.input_root / "SOURCE_BINDING.json",
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing required inputs: {missing}")
    checker.pass_step("input_presence", {"required_inputs": [str(path) for path in required]})

    checker.begin("bernoulli_gram_and_reflection")
    gram_details = verify_bernoulli_gram()
    checker.pass_step("bernoulli_gram_and_reflection", gram_details)

    checker.begin("rstar_rbar_entry_identity")
    rstar_u = build_rstar_u()
    rbar_t = build_rbar_t()
    reject_floats(rstar_u, "Rstar_u")
    reject_floats(rbar_t, "Rbar_t")
    rbar_from_rstar = (U * rstar_u / 4).subs(U**4, T)
    for row in range(4):
        for col in range(4):
            lhs = rbar_from_rstar[row, col].subs(T, U**4)
            rhs = rbar_t[row, col].subs(T, U**4)
            assert_zero_expr(lhs - rhs, (MU, NU, R, U), f"Rstar_to_Rbar_{row}_{col}")
    checker.write_json("Rstar_and_Rbar_entries.json", {
        "Rstar_u_entries": matrix_strings(rstar_u),
        "Rbar_short_t_entries": matrix_strings(rbar_t),
        "identity_checked": "Rbar(t=u^4) = u*Rstar(u)/4 entrywise",
    })
    checker.pass_step("rstar_rbar_entry_identity", {"entries_checked": 16})

    checker.begin("ahat_polynomial_entries")
    ahat, ahat_polys, ahat_details = build_ahat(rbar_t)
    reject_floats(ahat, "Ahat")
    checker.write_json("Ahat_entries.json", {"entries": matrix_strings(ahat), **ahat_details})
    checker.pass_step("ahat_polynomial_entries", ahat_details)

    checker.begin("determinant_extract_fresh_P")
    p_poly, det_poly, det_details = extract_p_from_determinant(ahat_polys)
    reject_floats(p_poly, "P")
    checker.write_json("determinant_and_P.json", {
        "determinant_summary": det_details["determinant_summary"],
        "divisor_summary": det_details["divisor_summary"],
        "P_summary": det_details["P_summary"],
        "determinant_expression": expr_string(det_poly.as_expr()),
        "P_expression": expr_string(p_poly.as_expr()),
        "P_coefficients": poly_coefficients(p_poly, VARS),
        "division_remainder": [],
        "remainder_zero": True,
    })
    checker.pass_step("determinant_extract_fresh_P", det_details)

    checker.begin("P_symmetry_and_author_comparison")
    sym_details = verify_p_symmetries(p_poly)
    p_ref_expr, component_summaries = load_author_components(checker.input_root)
    assert_zero_expr(p_poly.as_expr() - p_ref_expr, VARS, "P_fresh_vs_reference_components")
    checker.write_json("P_author_component_comparison.json", {
        "status": "PASS",
        "component_summaries": component_summaries,
        "assembled_after_fresh_P": True,
        **sym_details,
    })
    checker.pass_step("P_symmetry_and_author_comparison", {
        "fresh_vs_reference_components": "PASS",
        **sym_details,
    })

    checker.begin("Q_integer_chart")
    q_coeffs = transform_p_to_q_by_loops(p_poly)
    q_direct_details = verify_q_homogeneous_polynomial(p_poly, q_coeffs)
    q_box = verify_q_box(q_coeffs)
    checker.write_json("Q_full_box.json", {
        "variables": ["X", "Y", "R", "T"],
        "degrees": [4, 4, 10, 6],
        "coefficients": q_box["full_box"],
        "positive": q_box["positive"],
        "zero": q_box["zero"],
        "minimum": q_box["minimum"],
        "constant": q_box["constant"],
        "group_counts": q_box["group_counts"],
        "group_minima": q_box["group_minima"],
        "homogeneous_polynomial_cross_check": q_direct_details,
    })
    checker.pass_step("Q_integer_chart", {
        "positive": q_box["positive"],
        "zero": q_box["zero"],
        "minimum": q_box["minimum"],
        "constant": q_box["constant"],
        "group_counts": q_box["group_counts"],
        "group_minima": q_box["group_minima"],
        "homogeneous_polynomial_cross_check": q_direct_details,
    })

    checker.begin("seed_leafswap_and_scaling")
    seed_details = verify_seed_and_leafswap(rbar_t)
    scaling_details = verify_det_scaling_summary(p_poly, det_poly)
    checker.write_json("seed_leafswap_scaling.json", {**seed_details, **scaling_details})
    checker.pass_step("seed_leafswap_and_scaling", {**seed_details, "detAhat_scaling_to_Rstar": "PASS"})

    checker.success()


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the independent PR60 exact machine certificate.")
    parser.add_argument("--input-root", required=True, type=Path, help="Path to pr60_independent52/inputs.")
    parser.add_argument("--out", required=True, type=Path, help="Directory for machine artifacts.")
    parser.add_argument("--wall-seconds", type=int, default=2700, help="Internal wall-clock budget.")
    parser.add_argument("--memory-gib", type=int, default=16, help="Best-effort address-space cap.")
    args = parser.parse_args()

    checker = Checker(args.input_root, args.out, args.wall_seconds, args.memory_gib)
    try:
        run(checker)
    except BaseException as exc:
        checker.fail(exc)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
