#!/usr/bin/env python3
"""Independent r=0 exact certificate-chain verifier.

This script intentionally starts from the displayed four-by-four Schur
formula in STRUCTURE.md.  It does not import any old checker, saved Rstar
matrix, or old P/Q polynomial.  Frozen coefficient data under source_root is
opened only after the fresh determinant, P extraction, and Q transform have
already been constructed.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import os
import platform
import re
import sys
import time
import traceback
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable


THREAD_ENV_DEFAULTS = {
    "OMP_NUM_THREADS": "1",
    "OPENBLAS_NUM_THREADS": "1",
    "MKL_NUM_THREADS": "1",
    "NUMEXPR_NUM_THREADS": "1",
    "VECLIB_MAXIMUM_THREADS": "1",
    "BLIS_NUM_THREADS": "1",
    "SYMPY_USE_CACHE": "yes",
}

for _env_name, _env_value in THREAD_ENV_DEFAULTS.items():
    os.environ.setdefault(_env_name, _env_value)

import sympy as sp
from sympy.matrices.matrixbase import MatrixBase
from sympy.parsing.sympy_parser import convert_xor, parse_expr, standard_transformations


MU_NAME = "mu"
NU_NAME = "nu"
U_NAME = "u"
X_NAME = "X"
Y_NAME = "Y"
CAP_U_NAME = "U"

P_BOX = (4, 4, 16)


class CertificateError(RuntimeError):
    """Raised when an exact certificate check fails."""


class DeadlineExceeded(TimeoutError):
    """Raised when the internal wall-clock guard is reached."""


def utc_now_text() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def read_text_utf8(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def safe_rel(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.name


def is_forbidden_canglan(path: Path) -> bool:
    text = str(path.resolve()).replace("/", "\\").lower()
    return text == "c:\\canglan" or text.startswith("c:\\canglan\\")


def compact_expr(expr: Any) -> dict[str, Any]:
    text = str(expr)
    return {
        "chars": len(text),
        "text": text,
    }


def int_text(value: Any) -> str:
    return str(int(value)) if isinstance(value, bool) is False else str(value)


def to_jsonable(value: Any) -> Any:
    if value is None or isinstance(value, (str, bool)):
        return value
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return value
    if isinstance(value, Path):
        return value.name
    if isinstance(value, sp.Integer):
        return str(value)
    if isinstance(value, sp.Rational):
        return str(value)
    if isinstance(value, sp.Basic):
        return str(value)
    if isinstance(value, dict):
        return {str(k): to_jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_jsonable(v) for v in value]
    if isinstance(value, set):
        return sorted(to_jsonable(v) for v in value)
    return str(value)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(to_jsonable(payload), f, indent=2, sort_keys=True)
        f.write("\n")
    tmp.replace(path)


def ensure_no_float_atoms(label: str, obj: Any) -> None:
    atoms: set[sp.Float] = set()

    def visit(value: Any) -> None:
        if isinstance(value, sp.Basic):
            atoms.update(value.atoms(sp.Float))
        elif isinstance(value, MatrixBase):
            for entry in list(value):
                visit(entry)
        elif isinstance(value, dict):
            for item in value.values():
                visit(item)
        elif isinstance(value, (list, tuple, set)):
            for item in value:
                visit(item)

    visit(obj)
    if atoms:
        raise CertificateError(f"{label} contains SymPy Float atoms: {sorted(map(str, atoms))}")


def assert_zero_expr(label: str, expr: Any) -> dict[str, Any]:
    if isinstance(expr, MatrixBase):
        simplified_matrix = expr.applyfunc(lambda entry: sp.cancel(sp.together(entry)))
        ensure_no_float_atoms(label, simplified_matrix)
        nonzero_entries = []
        for i in range(simplified_matrix.rows):
            for j in range(simplified_matrix.cols):
                if simplified_matrix[i, j] != 0:
                    nonzero_entries.append({"entry": [i, j], "value": str(simplified_matrix[i, j])})
        if nonzero_entries:
            raise CertificateError(f"{label} has nonzero matrix entries: {nonzero_entries[:10]}")
        return {"label": label, "zero": True, "remainder": "0"}
    simplified = sp.cancel(sp.together(expr))
    ensure_no_float_atoms(label, simplified)
    if simplified != 0:
        raise CertificateError(f"{label} is not exactly zero: {simplified}")
    return {"label": label, "zero": True, "remainder": "0"}


def assert_poly_domain_zz(label: str, expr: Any, variables: tuple[sp.Symbol, ...]) -> sp.Poly:
    ensure_no_float_atoms(label, expr)
    poly = sp.Poly(sp.expand(expr), *variables, domain=sp.ZZ)
    if sp.expand(poly.as_expr() - sp.expand(expr)) != 0:
        raise CertificateError(f"{label} changed while coercing to ZZ polynomial")
    return poly


def poly_degrees(poly: sp.Poly, variables: tuple[sp.Symbol, ...]) -> tuple[int, ...]:
    return tuple(poly.degree(var) for var in variables)


def full_degree_box_rows(
    poly: sp.Poly,
    box: tuple[int, int, int],
) -> tuple[list[dict[str, Any]], dict[tuple[int, int, int], int]]:
    sparse = {tuple(exp): int(coeff) for exp, coeff in poly.as_dict().items()}
    rows: list[dict[str, Any]] = []
    for i in range(box[0] + 1):
        for j in range(box[1] + 1):
            for k in range(box[2] + 1):
                c = sparse.get((i, j, k), 0)
                rows.append({"exponents": [i, j, k], "coefficient": str(c)})
    return rows, sparse


def sparse_rows(poly: sp.Poly) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for exp, coeff in sorted(poly.as_dict().items()):
        rows.append({"exponents": list(exp), "coefficient": str(coeff)})
    return rows


def matrix_to_rows(matrix: sp.Matrix) -> list[list[str]]:
    return [[str(sp.cancel(matrix[i, j])) for j in range(matrix.cols)] for i in range(matrix.rows)]


def sign_of_permutation(perm: tuple[int, ...]) -> int:
    inversions = 0
    for i in range(len(perm)):
        for j in range(i + 1, len(perm)):
            if perm[i] > perm[j]:
                inversions += 1
    return -1 if inversions % 2 else 1


@dataclass
class RunContext:
    source_root: Path
    out: Path
    wall_seconds: int
    external_deadline_epoch: int | None = None
    started_wall: float = field(default_factory=time.time)
    started_monotonic: float = field(default_factory=time.monotonic)
    checkpoint_index: int = 0
    sanitized_tokens: dict[str, str] = field(default_factory=dict)

    @property
    def checkpoints_dir(self) -> Path:
        return self.out / "checkpoints"

    @property
    def artifacts_dir(self) -> Path:
        return self.out / "artifacts"

    @property
    def internal_deadline_epoch(self) -> int:
        return int(self.started_wall + self.wall_seconds)

    @property
    def deadline_epoch(self) -> int:
        if self.external_deadline_epoch is None:
            return self.internal_deadline_epoch
        return min(self.internal_deadline_epoch, self.external_deadline_epoch)

    def elapsed(self) -> float:
        return time.monotonic() - self.started_monotonic

    def remaining(self) -> float:
        return self.deadline_epoch - time.time()

    def sanitize_text(self, text: str) -> str:
        result = text
        for raw, replacement in self.sanitized_tokens.items():
            if raw:
                result = result.replace(raw, replacement)
        return result

    def check_deadline(self, label: str) -> None:
        if self.remaining() < 0:
            self.checkpoint(
                label,
                "DEADLINE_EXCEEDED",
                {
                    "elapsed_seconds": self.elapsed(),
                    "requested_wall_seconds": self.wall_seconds,
                    "effective_deadline_epoch": self.deadline_epoch,
                    "external_deadline_epoch": self.external_deadline_epoch,
                },
            )
            raise DeadlineExceeded(f"deadline exceeded before or during {label}")

    def checkpoint(self, label: str, status: str, details: dict[str, Any] | None = None) -> None:
        self.checkpoint_index += 1
        safe_label = re.sub(r"[^A-Za-z0-9_.-]+", "_", label).strip("_") or "checkpoint"
        payload = {
            "index": self.checkpoint_index,
            "label": label,
            "status": status,
            "utc": utc_now_text(),
            "elapsed_seconds": round(self.elapsed(), 3),
            "remaining_seconds": max(0.0, round(self.remaining(), 3)),
            "details": details or {},
        }
        write_json(self.checkpoints_dir / f"{self.checkpoint_index:04d}_{safe_label}_{status}.json", payload)

    def begin(self, label: str, details: dict[str, Any] | None = None) -> None:
        self.checkpoint(label, "BEGIN", details)
        self.check_deadline(label)

    def end(self, label: str, details: dict[str, Any] | None = None) -> None:
        self.check_deadline(label)
        self.checkpoint(label, "END", details)

    def fail(self, exc: BaseException) -> None:
        tb = traceback.format_exc()
        payload = {
            "status": "FAIL",
            "exception_type": type(exc).__name__,
            "exception": self.sanitize_text(str(exc)),
            "traceback": self.sanitize_text(tb),
            "utc": utc_now_text(),
            "elapsed_seconds": round(self.elapsed(), 3),
        }
        write_json(self.out / "FAILURE.json", payload)


@dataclass
class RStarBuild:
    mu: sp.Symbol
    nu: sp.Symbol
    u: sp.Symbol
    J: sp.Expr
    v: sp.Expr
    w: sp.Expr
    d_alpha: sp.Expr
    d_beta: sp.Expr
    Rstar: sp.Matrix
    R0: sp.Matrix
    ell_alpha: sp.Matrix
    ell_beta: sp.Matrix
    identities: list[dict[str, Any]]
    denominator_factors: dict[str, str]


@dataclass
class DeterminantBuild:
    det_expr: sp.Expr
    common_denominator: sp.Expr
    cleared_matrix: sp.Matrix
    bareiss_det_cleared: sp.Expr
    bareiss_records: list[dict[str, Any]]
    equality_checks: list[dict[str, Any]]


@dataclass
class PBuild:
    P_expr: sp.Expr
    P_poly: sp.Poly
    identities: list[dict[str, Any]]
    degree_box: tuple[int, int, int]


@dataclass
class QBuild:
    X: sp.Symbol
    Y: sp.Symbol
    U: sp.Symbol
    Q_expr: sp.Expr
    Q_poly: sp.Poly
    direct_summary: dict[str, Any]
    combinatorial_summary: dict[str, Any]
    identities: list[dict[str, Any]]
    full_rows: list[dict[str, Any]]
    sparse_dict: dict[tuple[int, int, int], int]
    nonzero_count: int
    min_coeff: int
    max_coeff: int
    zero_count: int


def source_file_checks(ctx: RunContext) -> dict[str, Any]:
    structure = ctx.source_root / "structure" / "STRUCTURE.md"
    seed = ctx.source_root / "structure" / "POSITIVE_SEED.md"
    coeff_table = ctx.source_root / "resume" / "coefficient_outputs" / "r0_coefficient_table.json"
    coeff_report = ctx.source_root / "resume" / "coefficient_outputs" / "r0_coefficient_report.json"
    required = [structure, seed, coeff_table, coeff_report]
    for path in required:
        if not path.exists():
            raise CertificateError(f"required source file is missing: {safe_rel(path, ctx.source_root)}")
        if is_forbidden_canglan(path):
            raise CertificateError("forbidden C:\\canglan source path")

    structure_text = read_text_utf8(structure)
    seed_text = read_text_utf8(seed)
    required_fragments = [
        "Rstar =",
        "R0 = 4(R^T G + G R + G')",
        "ell_alpha",
        "ell_beta",
        "a=b=1/2",
        "n1=n2=4u/J",
        "n3=4u^3/J",
    ]
    missing = [fragment for fragment in required_fragments if fragment not in structure_text]
    if missing:
        raise CertificateError(f"STRUCTURE.md is missing frozen fragments: {missing}")
    if "mu=nu=r=0" not in seed_text or "Rstar" not in seed_text:
        raise CertificateError("POSITIVE_SEED.md does not look like the frozen seed note")

    return {
        "source_root_kind": "relative formulas plus downstream coefficient references",
        "read_before_construction": [
            {"path": "structure/STRUCTURE.md"},
            {"path": "structure/POSITIVE_SEED.md"},
        ],
        "reference_source_factor_reserved_until_after_fresh_p": "resume/coefficient_outputs/r0_coefficient_report.json",
        "reference_coefficient_table_reserved_until_after_fresh_q": "resume/coefficient_outputs/r0_coefficient_table.json",
    }


def build_r0_displayed_rstar(ctx: RunContext) -> RStarBuild:
    ctx.begin("build_displayed_rstar", {"construction": "fresh symbolic r=0 Gram/Schur formula"})
    mu, nu, u = sp.symbols(f"{MU_NAME} {NU_NAME} {U_NAME}")
    a = b = sp.Rational(1, 2)
    v = (1 - mu**2) / 4
    w = (1 - nu**2) / 4
    J = 1 - u**4
    L = sp.Integer(1)
    rho = 1 / J
    lam = sp.Integer(1)
    d0 = (rho + lam) / 2
    d1 = (rho - lam) / 2
    d0_prime = 2 * u**3 / J**2
    d1_prime = 2 * u**3 / J**2

    D = sp.diag(1, v, w, v * w)
    S = sp.Matrix(
        [
            [mu * nu, 2 * v * nu, 2 * w * mu, 4 * v * w],
            [2 * v * nu, -mu * nu * v, 4 * v * w, -2 * mu * v * w],
            [2 * w * mu, 4 * v * w, -mu * nu * w, -2 * nu * v * w],
            [4 * v * w, -2 * mu * v * w, -2 * nu * v * w, mu * nu * v * w],
        ]
    )
    G = d0 * D + d1 * S
    G_prime = d0_prime * D + d1_prime * S
    R = sp.diag(0, 1 / u, 1 / u, 2 / u)
    n1 = 4 * u / J
    n2 = 4 * u / J
    n3 = 4 * u**3 / J
    d_alpha = sp.cancel(n2 * a * u**2 * v / 2)
    d_beta = sp.cancel(n1 * b * u**2 * w / 2)
    theta = (mu + nu) / 2

    diag_correction = sp.diag(
        0,
        n2 * v / (2 * u**2 * a),
        n1 * w / (2 * u**2 * b),
        n3 * v * w / (2 * u**4 * a * b),
    )
    R0 = 4 * (R.T * G + G * R + G_prime) + diag_correction
    R0 = R0.applyfunc(sp.cancel)

    ell_alpha = sp.Matrix([[8 * u * v * d1 * (-1), 8 * u * v * d1 * theta, 0, 8 * u * v * d1 * w]])
    ell_beta = sp.Matrix([[8 * u * w * d1 * (-1), 0, 8 * u * w * d1 * theta, 8 * u * w * d1 * v]])
    ell_alpha = ell_alpha.applyfunc(sp.cancel)
    ell_beta = ell_beta.applyfunc(sp.cancel)

    Rstar = R0 - (ell_alpha.T * ell_alpha) / (4 * d_alpha) - (ell_beta.T * ell_beta) / (4 * d_beta)
    Rstar = Rstar.applyfunc(lambda entry: sp.cancel(sp.together(entry)))

    m, p, q, h = sp.symbols("m p q h")
    y = sp.Matrix([m, p, q, h])
    U_alpha = sp.Matrix([2 * u * a * v, -u * a * mu, 0, 0])
    U_beta = sp.Matrix([2 * u * b * w, 0, -u * b * nu, 0])
    L_alpha_unsimplified = (8 * (U_alpha.T * G * y)[0] - 2 * n2 * v * m + n2 * mu * v * p)
    L_beta_unsimplified = (8 * (U_beta.T * G * y)[0] - 2 * n1 * w * m + n1 * nu * w * q)
    L_alpha_simplified = (ell_alpha * y)[0]
    L_beta_simplified = (ell_beta * y)[0]

    identities = [
        assert_zero_expr("reflection identity S D^{-1} S - D", S * D.inv() * S - D),
        assert_zero_expr("null block mixed coefficient identity", u**2 * (n2 * b + n1 * a) - n3),
        assert_zero_expr("ell_alpha displayed row equals unsimplified coupling", L_alpha_unsimplified - L_alpha_simplified),
        assert_zero_expr("ell_beta displayed row equals unsimplified coupling", L_beta_unsimplified - L_beta_simplified),
    ]
    ensure_no_float_atoms("r=0 Rstar construction", [Rstar, R0, ell_alpha, ell_beta])

    denominator_factors = {
        "u": "positive on 0<u<1",
        "J=1-u^4": "positive on 0<u<1",
        "1-mu^2": "positive on |mu|<1",
        "1-nu^2": "positive on |nu|<1",
        "v=(1-mu^2)/4": "positive on |mu|<1",
        "w=(1-nu^2)/4": "positive on |nu|<1",
        "d_alpha=u^3*v/J": "positive on the open r=0 domain",
        "d_beta=u^3*w/J": "positive on the open r=0 domain",
    }

    artifact = {
        "status": "built",
        "variables": [MU_NAME, NU_NAME, U_NAME],
        "denominator_factors": denominator_factors,
        "identities": identities,
        "R0": matrix_to_rows(R0),
        "ell_alpha": matrix_to_rows(ell_alpha),
        "ell_beta": matrix_to_rows(ell_beta),
        "Rstar": matrix_to_rows(Rstar),
    }
    write_json(ctx.artifacts_dir / "rstar_from_displayed_formula.json", artifact)
    ctx.end("build_displayed_rstar", {"identities": len(identities), "artifact": "rstar_from_displayed_formula.json"})
    return RStarBuild(mu, nu, u, J, v, w, d_alpha, d_beta, Rstar, R0, ell_alpha, ell_beta, identities, denominator_factors)


def clear_matrix_denominators(matrix: sp.Matrix, variables: tuple[sp.Symbol, ...]) -> tuple[sp.Matrix, sp.Expr, list[dict[str, Any]]]:
    denoms: list[sp.Expr] = []
    entry_data: list[dict[str, Any]] = []
    for index, entry in enumerate(list(matrix)):
        num, den = sp.together(entry).as_numer_denom()
        den = sp.Poly(sp.expand(den), *variables, domain=sp.QQ).as_expr()
        denoms.append(den)
        entry_data.append({"entry": index, "denominator": str(den)})
    try:
        common = sp.lcm_list(denoms)
    except Exception:
        common = sp.prod(denoms)
    common = sp.Poly(sp.expand(common), *variables, domain=sp.QQ).as_expr()

    cleared_entries: list[sp.Expr] = []
    for entry in list(matrix):
        candidate = sp.cancel(sp.together(entry * common))
        num, den = sp.together(candidate).as_numer_denom()
        if sp.cancel(den - 1) != 0:
            raise CertificateError(f"matrix denominator clearing failed; residual denominator {den}")
        cleared_entries.append(sp.expand(num))

    cleared = sp.Matrix(matrix.rows, matrix.cols, cleared_entries)
    ensure_no_float_atoms("cleared determinant matrix", cleared)
    return cleared, common, entry_data


def exact_poly_division(
    numerator: sp.Expr,
    divisor: sp.Expr,
    variables: tuple[sp.Symbol, ...],
    label: str,
) -> tuple[sp.Expr, dict[str, Any]]:
    numerator_poly = sp.Poly(sp.expand(numerator), *variables, domain=sp.QQ)
    divisor_poly = sp.Poly(sp.expand(divisor), *variables, domain=sp.QQ)
    quotient_poly, remainder_poly = numerator_poly.div(divisor_poly)
    if not remainder_poly.is_zero:
        raise CertificateError(f"{label} Bareiss division has nonzero remainder: {remainder_poly.as_expr()}")
    quotient = quotient_poly.as_expr()
    return quotient, {
        "label": label,
        "divisor": compact_expr(divisor),
        "numerator": compact_expr(numerator),
        "remainder": "0",
        "quotient": compact_expr(quotient),
    }


def bareiss_det_polynomial(
    matrix: sp.Matrix,
    variables: tuple[sp.Symbol, ...],
    ctx: RunContext,
) -> tuple[sp.Expr, list[dict[str, Any]]]:
    if matrix.rows != matrix.cols:
        raise CertificateError("Bareiss determinant needs a square matrix")
    n = matrix.rows
    A = [[sp.Poly(sp.expand(matrix[i, j]), *variables, domain=sp.QQ).as_expr() for j in range(n)] for i in range(n)]
    sign = 1
    previous = sp.Integer(1)
    records: list[dict[str, Any]] = []
    for k in range(n - 1):
        ctx.check_deadline(f"bareiss_step_{k}")
        pivot = A[k][k]
        if sp.Poly(sp.expand(pivot), *variables, domain=sp.QQ).is_zero:
            swap_row = None
            for candidate_row in range(k + 1, n):
                candidate = sp.Poly(sp.expand(A[candidate_row][k]), *variables, domain=sp.QQ)
                if not candidate.is_zero:
                    swap_row = candidate_row
                    break
            if swap_row is None:
                return sp.Integer(0), records + [{"step": k, "pivot": "0", "determinant": "0"}]
            A[k], A[swap_row] = A[swap_row], A[k]
            sign *= -1
            pivot = A[k][k]
            records.append({"step": k, "row_swap": [k, swap_row]})

        records.append(
            {
                "step": k,
                "pivot": compact_expr(pivot),
                "note": (
                    "Symbolic Bareiss pivot used only for an exact polynomial "
                    "division certificate; no global nonvanishing of this pivot is claimed."
                ),
            }
        )
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = sp.expand(A[i][j] * pivot - A[i][k] * A[k][j])
                if k == 0:
                    updated = numerator
                    records.append(
                        {
                            "step": k,
                            "entry": [i, j],
                            "division": "none_first_step",
                            "updated": compact_expr(updated),
                        }
                    )
                else:
                    updated, division_record = exact_poly_division(
                        numerator,
                        previous,
                        variables,
                        f"step {k} entry ({i},{j})",
                    )
                    division_record["step"] = k
                    division_record["entry"] = [i, j]
                    records.append(division_record)
                A[i][j] = sp.expand(updated)
        for i in range(k + 1, n):
            A[i][k] = sp.Integer(0)
        for j in range(k + 1, n):
            A[k][j] = sp.Integer(0)
        previous = pivot
    det_expr = sp.expand(sign * A[n - 1][n - 1])
    ensure_no_float_atoms("Bareiss determinant", det_expr)
    return det_expr, records


def leibniz_det(matrix: sp.Matrix, ctx: RunContext) -> sp.Expr:
    n = matrix.rows
    total = sp.Integer(0)
    for perm in itertools.permutations(range(n)):
        ctx.check_deadline("leibniz_determinant")
        term = sp.Integer(sign_of_permutation(perm))
        for i, j in enumerate(perm):
            term *= matrix[i, j]
        total += term
    return sp.cancel(sp.together(total))


def compute_determinant(ctx: RunContext, build: RStarBuild) -> DeterminantBuild:
    ctx.begin("determinant", {"methods": ["cleared polynomial Bareiss", "direct 24-term Leibniz"]})
    variables = (build.mu, build.nu, build.u)
    cleared, common_denominator, denominator_records = clear_matrix_denominators(build.Rstar, variables)
    write_json(
        ctx.artifacts_dir / "determinant_cleared_matrix_before_bareiss.json",
        {
            "status": "cleared",
            "variables": [MU_NAME, NU_NAME, U_NAME],
            "common_denominator": str(common_denominator),
            "entry_denominators": denominator_records,
            "cleared_matrix": matrix_to_rows(cleared),
        },
    )

    bareiss_det_cleared, bareiss_records = bareiss_det_polynomial(cleared, variables, ctx)
    det_bareiss = sp.cancel(sp.together(bareiss_det_cleared / (common_denominator**build.Rstar.rows)))
    write_json(
        ctx.artifacts_dir / "determinant_bareiss_certificate.json",
        {
            "status": "computed",
            "common_denominator": compact_expr(common_denominator),
            "cleared_determinant": compact_expr(bareiss_det_cleared),
            "determinant": compact_expr(det_bareiss),
            "bareiss_records": bareiss_records,
        },
    )

    det_leibniz = leibniz_det(build.Rstar, ctx)
    equality_checks = [
        assert_zero_expr("Bareiss determinant equals Leibniz determinant", det_bareiss - det_leibniz)
    ]
    write_json(
        ctx.artifacts_dir / "determinant_independent_equality.json",
        {
            "status": "checked",
            "det_bareiss": compact_expr(det_bareiss),
            "det_leibniz": compact_expr(det_leibniz),
            "equality_checks": equality_checks,
        },
    )
    ctx.end("determinant", {"bareiss_records": len(bareiss_records), "equality_checks": len(equality_checks)})
    return DeterminantBuild(det_bareiss, common_denominator, cleared, bareiss_det_cleared, bareiss_records, equality_checks)


def extract_p(ctx: RunContext, build: RStarBuild, det: DeterminantBuild) -> PBuild:
    ctx.begin("extract_P", {"identity": "det Rstar=(1-mu^2)^2(1-nu^2)^2 P/[2(1-u^4)^5]"})
    mu, nu, u = build.mu, build.nu, build.u
    P_expr = sp.cancel(sp.together(det.det_expr * 2 * build.J**5 / ((1 - mu**2) ** 2 * (1 - nu**2) ** 2)))
    p_num, p_den = sp.together(P_expr).as_numer_denom()
    if sp.cancel(p_den - 1) != 0:
        raise CertificateError(f"P extraction has residual denominator: {p_den}")
    P_expr = sp.expand(p_num)
    P_poly = assert_poly_domain_zz("P", P_expr, (mu, nu, u))
    degrees = poly_degrees(P_poly, (mu, nu, u))
    if degrees != P_BOX:
        raise CertificateError(f"P degree box {degrees} does not match frozen box {P_BOX}")
    identities = [
        assert_zero_expr(
            "frozen determinant/P rational identity",
            det.det_expr - ((1 - mu**2) ** 2 * (1 - nu**2) ** 2 * P_expr) / (2 * build.J**5),
        )
    ]
    write_json(
        ctx.artifacts_dir / "P_polynomial.json",
        {
            "status": "computed",
            "variables": [MU_NAME, NU_NAME, U_NAME],
            "degree_box": list(P_BOX),
            "term_count": len(P_poly.as_dict()),
            "identities": identities,
            "P": compact_expr(P_expr),
            "sparse_coefficients": sparse_rows(P_poly),
        },
    )
    ctx.end("extract_P", {"degree_box": degrees, "term_count": len(P_poly.as_dict())})
    return PBuild(P_expr, P_poly, identities, P_BOX)


def parse_archived_polynomial(text: str, variables: tuple[sp.Symbol, ...]) -> sp.Expr:
    local_dict = {str(var): var for var in variables}
    transformations = standard_transformations + (convert_xor,)
    return parse_expr(text, local_dict=local_dict, transformations=transformations, evaluate=True)


def compare_archived_p_source_factor(ctx: RunContext, p_build: PBuild) -> dict[str, Any]:
    ctx.begin(
        "compare_archived_P_source_factor",
        {"note": "coefficient_report source_factor is first opened here, after fresh P construction"},
    )
    report_path = ctx.source_root / "resume" / "coefficient_outputs" / "r0_coefficient_report.json"
    report_data = load_json(report_path)
    if not isinstance(report_data, dict) or "source_factor" not in report_data:
        raise CertificateError("archived coefficient report has no top-level source_factor field")
    source_factor = report_data["source_factor"]
    if not isinstance(source_factor, str):
        source_factor = str(source_factor)
    variables = p_build.P_poly.gens
    archived_expr = parse_archived_polynomial(source_factor, variables)
    ensure_no_float_atoms("archived P source_factor", archived_expr)
    archived_poly = assert_poly_domain_zz("archived P source_factor", sp.expand(archived_expr), variables)
    archived_degrees = poly_degrees(archived_poly, variables)
    if archived_degrees != p_build.degree_box:
        raise CertificateError(f"archived P source_factor degree box {archived_degrees} does not match {p_build.degree_box}")
    identity = assert_zero_expr("fresh P equals archived source_factor", p_build.P_expr - archived_poly.as_expr())

    fresh_sparse = {tuple(exp): int(coeff) for exp, coeff in p_build.P_poly.as_dict().items()}
    archived_sparse = {tuple(exp): int(coeff) for exp, coeff in archived_poly.as_dict().items()}
    mismatches: list[dict[str, Any]] = []
    for i in range(p_build.degree_box[0] + 1):
        for j in range(p_build.degree_box[1] + 1):
            for k in range(p_build.degree_box[2] + 1):
                exp = (i, j, k)
                fresh = fresh_sparse.get(exp, 0)
                archived = archived_sparse.get(exp, 0)
                if fresh != archived:
                    mismatches.append({"exponents": [i, j, k], "fresh": fresh, "archived": archived})
    if mismatches:
        raise CertificateError(f"fresh P/source_factor coefficient mismatches: {mismatches[:10]}")
    outside = [
        {"exponents": list(exp), "coefficient": coeff}
        for exp, coeff in sorted(archived_sparse.items())
        if any(exp[idx] < 0 or exp[idx] > p_build.degree_box[idx] for idx in range(3))
    ]
    if outside:
        raise CertificateError(f"archived P source_factor has out-of-box terms: {outside[:10]}")

    result = {
        "status": "matched",
        "source": "resume/coefficient_outputs/r0_coefficient_report.json[source_factor]",
        "degree_box": list(p_build.degree_box),
        "identity": identity,
        "full_degree_box_entries_checked": (
            (p_build.degree_box[0] + 1) * (p_build.degree_box[1] + 1) * (p_build.degree_box[2] + 1)
        ),
        "source_factor": source_factor,
        "selected_scalar_facts": selected_scalar_facts(report_data),
    }
    write_json(ctx.artifacts_dir / "archived_P_source_factor_comparison.json", result)
    ctx.end("compare_archived_P_source_factor", {"status": "matched"})
    return result


def direct_q_transform(ctx: RunContext, p_build: PBuild) -> tuple[sp.Poly, dict[str, Any]]:
    ctx.begin("transform_Q_direct", {"method": "homogeneous rational substitution"})
    mu, nu, u = p_build.P_poly.gens
    X, Y, U = sp.symbols(f"{X_NAME} {Y_NAME} {CAP_U_NAME}")
    dx, dy, du = p_build.degree_box
    multiplier = (X + 1) ** dx * (Y + 1) ** dy * (U + 1) ** du
    substituted = p_build.P_expr.subs({mu: (X - 1) / (X + 1), nu: (Y - 1) / (Y + 1), u: U / (U + 1)})
    Q_candidate = sp.cancel(sp.together(multiplier * substituted))
    q_num, q_den = sp.together(Q_candidate).as_numer_denom()
    if sp.cancel(q_den - 1) != 0:
        raise CertificateError(f"direct Q transform has residual denominator: {q_den}")
    Q_expr = sp.expand(q_num)
    Q_poly = assert_poly_domain_zz("Q direct", Q_expr, (X, Y, U))
    ensure_no_float_atoms("Q direct transform", Q_expr)
    summary = {
        "variables": [X_NAME, Y_NAME, CAP_U_NAME],
        "degree_box": list(poly_degrees(Q_poly, (X, Y, U))),
        "term_count": len(Q_poly.as_dict()),
        "Q_direct": compact_expr(Q_expr),
    }
    write_json(ctx.artifacts_dir / "Q_direct_transform.json", {"status": "computed", **summary})
    ctx.end("transform_Q_direct", {"term_count": len(Q_poly.as_dict())})
    return Q_poly, summary


def signed_pm_factor(power_minus: int, power_plus: int) -> dict[int, int]:
    result: dict[int, int] = {}
    for a in range(power_minus + 1):
        c_minus = math.comb(power_minus, a) * ((-1) ** (power_minus - a))
        for b in range(power_plus + 1):
            degree = a + b
            result[degree] = result.get(degree, 0) + c_minus * math.comb(power_plus, b)
    return {degree: coeff for degree, coeff in result.items() if coeff != 0}


def u_factor(power_u: int, clear_degree: int) -> dict[int, int]:
    result: dict[int, int] = {}
    for b in range(clear_degree - power_u + 1):
        result[power_u + b] = math.comb(clear_degree - power_u, b)
    return result


def combinatorial_q_transform(ctx: RunContext, p_build: PBuild) -> tuple[sp.Poly, dict[str, Any]]:
    ctx.begin("transform_Q_combinatorial", {"method": "coefficient binomial expansion"})
    X, Y, U = sp.symbols(f"{X_NAME} {Y_NAME} {CAP_U_NAME}")
    dx, dy, du = p_build.degree_box
    q_terms: dict[tuple[int, int, int], int] = {}
    basis_x = {(i, dx - i): signed_pm_factor(i, dx - i) for i in range(dx + 1)}
    basis_y = {(j, dy - j): signed_pm_factor(j, dy - j) for j in range(dy + 1)}
    basis_u = {k: u_factor(k, du) for k in range(du + 1)}
    for (i, j, k), coeff in sorted(p_build.P_poly.as_dict().items()):
        ctx.check_deadline("transform_Q_combinatorial_terms")
        c = int(coeff)
        x_part = basis_x[(i, dx - i)]
        y_part = basis_y[(j, dy - j)]
        u_part = basis_u[k]
        for ix, cx in x_part.items():
            for iy, cy in y_part.items():
                for iu, cu in u_part.items():
                    exp = (ix, iy, iu)
                    q_terms[exp] = q_terms.get(exp, 0) + c * cx * cy * cu
    q_terms = {exp: coeff for exp, coeff in q_terms.items() if coeff != 0}
    Q_poly = sp.Poly.from_dict(q_terms, (X, Y, U), domain=sp.ZZ)
    ensure_no_float_atoms("Q combinatorial transform", Q_poly.as_expr())
    summary = {
        "variables": [X_NAME, Y_NAME, CAP_U_NAME],
        "degree_box": list(poly_degrees(Q_poly, (X, Y, U))),
        "term_count": len(Q_poly.as_dict()),
        "Q_combinatorial": compact_expr(Q_poly.as_expr()),
    }
    write_json(ctx.artifacts_dir / "Q_combinatorial_transform.json", {"status": "computed", **summary})
    ctx.end("transform_Q_combinatorial", {"term_count": len(Q_poly.as_dict())})
    return Q_poly, summary


def build_q(ctx: RunContext, p_build: PBuild) -> QBuild:
    direct_poly, direct_summary = direct_q_transform(ctx, p_build)
    comb_poly, combinatorial_summary = combinatorial_q_transform(ctx, p_build)
    ctx.begin("validate_Q", {"checks": ["direct equals combinatorial", "positive sparse terms", "full degree box including zeros"]})
    identities = [assert_zero_expr("direct Q transform equals coefficient-combinatorial Q", direct_poly.as_expr() - comb_poly.as_expr())]
    Q_poly = direct_poly
    degrees = poly_degrees(Q_poly, Q_poly.gens)
    if degrees != P_BOX:
        raise CertificateError(f"Q degree box {degrees} does not match frozen box {P_BOX}")
    full_rows, sparse = full_degree_box_rows(Q_poly, P_BOX)
    outside = [exp for exp in sparse if any(exp[idx] < 0 or exp[idx] > P_BOX[idx] for idx in range(3))]
    if outside:
        raise CertificateError(f"Q has terms outside frozen degree box: {outside[:10]}")
    nonzero_coeffs = [coeff for coeff in sparse.values() if coeff != 0]
    if not nonzero_coeffs:
        raise CertificateError("Q has no nonzero coefficients")
    nonpositive = [(exp, coeff) for exp, coeff in sparse.items() if coeff <= 0]
    if nonpositive:
        raise CertificateError(f"Q has nonpositive recorded coefficients: {nonpositive[:10]}")
    nonzero_count = len(nonzero_coeffs)
    min_coeff = min(nonzero_coeffs)
    max_coeff = max(nonzero_coeffs)
    zero_count = (P_BOX[0] + 1) * (P_BOX[1] + 1) * (P_BOX[2] + 1) - nonzero_count
    write_json(
        ctx.artifacts_dir / "Q_polynomial_full_box.json",
        {
            "status": "computed",
            "variables": [X_NAME, Y_NAME, CAP_U_NAME],
            "degree_box": list(P_BOX),
            "nonzero_count": nonzero_count,
            "zero_count_in_box": zero_count,
            "min_positive_coefficient": min_coeff,
            "max_positive_coefficient": max_coeff,
            "identities": identities,
            "sparse_coefficients": sparse_rows(Q_poly),
            "full_degree_box_coefficients": full_rows,
        },
    )
    ctx.end("validate_Q", {"nonzero_count": nonzero_count, "zero_count_in_box": zero_count, "min_coeff": min_coeff})
    return QBuild(
        Q_poly.gens[0],
        Q_poly.gens[1],
        Q_poly.gens[2],
        Q_poly.as_expr(),
        Q_poly,
        direct_summary,
        combinatorial_summary,
        identities,
        full_rows,
        sparse,
        nonzero_count,
        min_coeff,
        max_coeff,
        zero_count,
    )


def parse_int_like(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        s = value.strip()
        if re.fullmatch(r"[+-]?\d+", s):
            return int(s)
    return None


def parse_exponents_from_key(key: str) -> tuple[int, int, int] | None:
    stripped = key.strip()
    ints = re.findall(r"[+-]?\d+", stripped)
    if len(ints) == 3:
        return tuple(int(v) for v in ints)  # type: ignore[return-value]
    return None


def parse_exponents_from_entry(entry: dict[str, Any]) -> tuple[int, int, int] | None:
    vector_keys = ["exponents", "powers", "power", "monomial", "degrees", "degree", "indices", "index"]
    for key in vector_keys:
        value = entry.get(key)
        if isinstance(value, (list, tuple)) and len(value) >= 3:
            parsed = [parse_int_like(value[idx]) for idx in range(3)]
            if all(v is not None for v in parsed):
                return (int(parsed[0]), int(parsed[1]), int(parsed[2]))  # type: ignore[arg-type]
        if isinstance(value, dict):
            direct = parse_direct_exponent_fields(value)
            if direct is not None:
                return direct
    return parse_direct_exponent_fields(entry)


def parse_direct_exponent_fields(entry: dict[str, Any]) -> tuple[int, int, int] | None:
    key_sets = [
        ["X", "x", "i", "ix", "x_exp", "degree_x", "deg_x", "mu", "mu_exp", "degree_mu"],
        ["Y", "y", "j", "iy", "y_exp", "degree_y", "deg_y", "nu", "nu_exp", "degree_nu"],
        ["U", "u", "k", "iu", "u_exp", "degree_u", "deg_u"],
    ]
    out: list[int] = []
    for keys in key_sets:
        found: int | None = None
        for key in keys:
            if key in entry:
                parsed = parse_int_like(entry[key])
                if parsed is not None:
                    found = parsed
                    break
        if found is None:
            return None
        out.append(found)
    return (out[0], out[1], out[2])


def parse_coeff_from_entry(entry: dict[str, Any]) -> int | None:
    for key in ["coefficient", "coeff", "value", "c"]:
        if key in entry:
            return parse_int_like(entry[key])
    return None


@dataclass
class CoeffCandidate:
    source_path: str
    json_path: str
    coeffs: dict[tuple[int, int, int], int]
    raw_entries: int
    duplicates: list[dict[str, Any]]


def try_list_table(value: list[Any], source_path: str, json_path: str) -> CoeffCandidate | None:
    coeffs: dict[tuple[int, int, int], int] = {}
    duplicates: list[dict[str, Any]] = []
    parsed_count = 0
    for item in value:
        exp: tuple[int, int, int] | None = None
        coeff: int | None = None
        if isinstance(item, dict):
            exp = parse_exponents_from_entry(item)
            coeff = parse_coeff_from_entry(item)
        elif isinstance(item, (list, tuple)) and len(item) >= 4:
            parsed_exp = [parse_int_like(item[idx]) for idx in range(3)]
            parsed_coeff = parse_int_like(item[3])
            if all(v is not None for v in parsed_exp) and parsed_coeff is not None:
                exp = (int(parsed_exp[0]), int(parsed_exp[1]), int(parsed_exp[2]))  # type: ignore[arg-type]
                coeff = parsed_coeff
        if exp is None or coeff is None:
            continue
        parsed_count += 1
        if exp in coeffs:
            duplicates.append({"exponents": list(exp), "first": coeffs[exp], "second": coeff})
        coeffs[exp] = coeff
    if parsed_count == 0:
        return None
    return CoeffCandidate(source_path, json_path, coeffs, parsed_count, duplicates)


def try_mapping_table(value: dict[str, Any], source_path: str, json_path: str) -> CoeffCandidate | None:
    coeffs: dict[tuple[int, int, int], int] = {}
    duplicates: list[dict[str, Any]] = []
    parsed_count = 0
    for key, item in value.items():
        exp = parse_exponents_from_key(str(key))
        coeff = parse_int_like(item)
        if exp is None or coeff is None:
            continue
        parsed_count += 1
        if exp in coeffs:
            duplicates.append({"exponents": list(exp), "first": coeffs[exp], "second": coeff})
        coeffs[exp] = coeff
    if parsed_count == 0:
        return None
    return CoeffCandidate(source_path, json_path, coeffs, parsed_count, duplicates)


def try_nested_int_key_table(value: dict[str, Any], source_path: str, json_path: str) -> CoeffCandidate | None:
    coeffs: dict[tuple[int, int, int], int] = {}
    duplicates: list[dict[str, Any]] = []
    parsed_count = 0

    def walk(node: Any, exps: list[int]) -> None:
        nonlocal parsed_count
        if len(exps) == 3:
            coeff = parse_int_like(node)
            if coeff is None:
                return
            exp = (exps[0], exps[1], exps[2])
            parsed_count += 1
            if exp in coeffs:
                duplicates.append({"exponents": list(exp), "first": coeffs[exp], "second": coeff})
            coeffs[exp] = coeff
            return
        if not isinstance(node, dict):
            return
        for key, child in node.items():
            parsed_key = parse_int_like(str(key))
            if parsed_key is not None:
                walk(child, exps + [parsed_key])

    walk(value, [])
    if parsed_count == 0:
        return None
    return CoeffCandidate(source_path, json_path, coeffs, parsed_count, duplicates)


def find_coefficient_candidates(obj: Any, source_path: str, json_path: str = "$") -> list[CoeffCandidate]:
    candidates: list[CoeffCandidate] = []
    if isinstance(obj, list):
        candidate = try_list_table(obj, source_path, json_path)
        if candidate is not None:
            candidates.append(candidate)
        for idx, item in enumerate(obj):
            candidates.extend(find_coefficient_candidates(item, source_path, f"{json_path}[{idx}]"))
    elif isinstance(obj, dict):
        candidate = try_mapping_table(obj, source_path, json_path)
        if candidate is not None:
            candidates.append(candidate)
        nested_candidate = try_nested_int_key_table(obj, source_path, json_path)
        if nested_candidate is not None:
            candidates.append(nested_candidate)
        for key, item in obj.items():
            candidates.extend(find_coefficient_candidates(item, source_path, f"{json_path}.{key}"))
    return candidates


def compare_candidate_to_q(
    candidate: CoeffCandidate,
    q_build: QBuild,
    box: tuple[int, int, int],
) -> dict[str, Any]:
    mismatches: list[dict[str, Any]] = []
    for i in range(box[0] + 1):
        for j in range(box[1] + 1):
            for k in range(box[2] + 1):
                exp = (i, j, k)
                actual = q_build.sparse_dict.get(exp, 0)
                reference = candidate.coeffs.get(exp, 0)
                if actual != reference:
                    mismatches.append({"exponents": [i, j, k], "actual": actual, "reference": reference})
    out_of_bounds = [
        {"exponents": list(exp), "coefficient": coeff}
        for exp, coeff in sorted(candidate.coeffs.items())
        if any(exp[idx] < 0 or exp[idx] > box[idx] for idx in range(3))
    ]
    return {
        "source_path": candidate.source_path,
        "json_path": candidate.json_path,
        "raw_entries": candidate.raw_entries,
        "unique_entries": len(candidate.coeffs),
        "duplicates": candidate.duplicates,
        "out_of_bounds": out_of_bounds,
        "mismatch_count": len(mismatches),
        "mismatches": mismatches[:100],
    }


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def compare_reference_coefficients(ctx: RunContext, q_build: QBuild) -> dict[str, Any]:
    ctx.begin(
        "compare_archived_coefficients",
        {"note": "reference coefficient files are first opened here, after fresh Q construction"},
    )
    table_path = ctx.source_root / "resume" / "coefficient_outputs" / "r0_coefficient_table.json"
    report_path = ctx.source_root / "resume" / "coefficient_outputs" / "r0_coefficient_report.json"
    data = load_json(table_path)
    candidates = find_coefficient_candidates(data, "resume/coefficient_outputs/r0_coefficient_table.json")
    if not candidates:
        raise CertificateError("could not parse any coefficient table from archived r0_coefficient_table.json")
    comparisons = [compare_candidate_to_q(candidate, q_build, P_BOX) for candidate in candidates]
    comparisons.sort(key=lambda item: (item["mismatch_count"], len(item["duplicates"]), len(item["out_of_bounds"])))
    best = comparisons[0]
    if best["duplicates"]:
        raise CertificateError(f"archived coefficient table contains duplicate exponents: {best['duplicates'][:10]}")
    if best["out_of_bounds"]:
        raise CertificateError(f"archived coefficient table contains out-of-bounds exponents: {best['out_of_bounds'][:10]}")
    if best["mismatch_count"] != 0:
        raise CertificateError(f"archived coefficient table mismatch count is {best['mismatch_count']}")

    report_summary: dict[str, Any] = {"read": False}
    if report_path.exists():
        report_data = load_json(report_path)
        report_summary = {
            "read": True,
            "selected_scalar_facts": selected_scalar_facts(report_data),
        }

    result = {
        "status": "matched",
        "candidate_count": len(candidates),
        "best_comparison": best,
        "all_comparisons_summary": [
            {
                "json_path": item["json_path"],
                "raw_entries": item["raw_entries"],
                "unique_entries": item["unique_entries"],
                "mismatch_count": item["mismatch_count"],
                "duplicate_count": len(item["duplicates"]),
                "out_of_bounds_count": len(item["out_of_bounds"]),
            }
            for item in comparisons
        ],
        "full_degree_box_entries_checked": (P_BOX[0] + 1) * (P_BOX[1] + 1) * (P_BOX[2] + 1),
        "omitted_reference_entries_treated_as_zero": True,
        "report_summary": report_summary,
    }
    write_json(ctx.artifacts_dir / "archived_coefficient_comparison.json", result)
    ctx.end("compare_archived_coefficients", {"candidate_count": len(candidates), "best_mismatch_count": 0})
    return result


def selected_scalar_facts(obj: Any, path: str = "$") -> list[dict[str, Any]]:
    facts: list[dict[str, Any]] = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            child = f"{path}.{key}"
            if isinstance(value, (dict, list)):
                facts.extend(selected_scalar_facts(value, child))
            else:
                key_l = str(key).lower()
                if any(token in key_l for token in ["count", "min", "max", "degree", "positive", "zero"]):
                    parsed = parse_int_like(value)
                    if parsed is not None or isinstance(value, str):
                        facts.append({"path": child, "value": value})
    elif isinstance(obj, list):
        for idx, value in enumerate(obj):
            if isinstance(value, (dict, list)):
                facts.extend(selected_scalar_facts(value, f"{path}[{idx}]"))
    return facts[:200]


def positive_seed_certificate(ctx: RunContext, build: RStarBuild) -> dict[str, Any]:
    ctx.begin("positive_seed", {"point": "mu=nu=r=0,u=1/2", "source": "rebuilt Rstar"})
    mu, nu, u = build.mu, build.nu, build.u
    seed_matrix = build.Rstar.subs({mu: 0, nu: 0, u: sp.Rational(1, 2)}).applyfunc(sp.cancel)
    denoms = [sp.denom(entry) for entry in list(seed_matrix)]
    scale = math.lcm(*[int(den) for den in denoms]) if denoms else 1
    scaled = (scale * seed_matrix).applyfunc(sp.cancel)
    for entry in list(scaled):
        if not bool(entry.is_Integer):
            raise CertificateError(f"positive seed scale did not clear entry: {entry}")
    row_margins: list[int] = []
    for i in range(scaled.rows):
        diagonal = int(scaled[i, i])
        off_sum = sum(abs(int(scaled[i, j])) for j in range(scaled.cols) if j != i)
        row_margins.append(diagonal - off_sum)
    if any(margin <= 0 for margin in row_margins):
        raise CertificateError(f"positive seed is not strictly diagonally dominant: {row_margins}")

    leading_minors: list[str] = []
    for size in range(1, scaled.rows + 1):
        minor = scaled[:size, :size].det(method="bareiss")
        leading_minors.append(str(minor))
        if minor <= 0:
            raise CertificateError(f"positive seed leading principal minor {size} is not positive: {minor}")
    ensure_no_float_atoms("positive seed", seed_matrix)

    result = {
        "status": "positive",
        "seed": {"mu": "0", "nu": "0", "u": "1/2", "r": "0"},
        "scale": scale,
        "Rstar_at_seed": matrix_to_rows(seed_matrix),
        "scaled_Rstar_at_seed": matrix_to_rows(scaled),
        "strict_diagonal_dominance_margins_before_division": row_margins,
        "leading_principal_minors_of_scaled_Rstar": leading_minors,
        "denominator_factors_at_seed": {
            "u": "1/2",
            "J=1-u^4": "15/16",
            "1-mu^2": "1",
            "1-nu^2": "1",
            "v": "1/4",
            "w": "1/4",
            "d_alpha": str(build.d_alpha.subs({mu: 0, nu: 0, u: sp.Rational(1, 2)})),
            "d_beta": str(build.d_beta.subs({mu: 0, nu: 0, u: sp.Rational(1, 2)})),
        },
    }
    write_json(ctx.artifacts_dir / "positive_seed_certificate.json", result)
    ctx.end("positive_seed", {"scale": scale, "row_margins": row_margins})
    return result


def domain_inertia_certificate(ctx: RunContext, build: RStarBuild, p_build: PBuild, q_build: QBuild) -> dict[str, Any]:
    ctx.begin("domain_inertia_certificate", {"scope": "r=0, |mu|<1, |nu|<1, 0<u<1"})
    result = {
        "status": "conditional_on_exact_artifacts",
        "domain": "|mu|<1, |nu|<1, 0<u<1, r=0",
        "domain_connectedness": (
            "The domain is the Cartesian product (-1,1) x (-1,1) x (0,1), "
            "hence open and connected."
        ),
        "positive_denominators": build.denominator_factors,
        "determinant_identity": (
            "det Rstar=(1-mu^2)^2(1-nu^2)^2 P/[2(1-u^4)^5]"
        ),
        "cayley_map": {
            "mu": "(X-1)/(X+1)",
            "nu": "(Y-1)/(Y+1)",
            "u": "U/(1+U)",
            "image": "X>0, Y>0, U>0 maps into |mu|<1, |nu|<1, 0<u<1",
            "inverse": "X=(1+mu)/(1-mu), Y=(1+nu)/(1-nu), U=u/(1-u)",
        },
        "Q_positive_orthant_certificate": {
            "degree_box": list(P_BOX),
            "nonzero_count": q_build.nonzero_count,
            "zero_count_in_box": q_build.zero_count,
            "min_positive_coefficient": q_build.min_coeff,
            "max_positive_coefficient": q_build.max_coeff,
            "reason": (
                "Every nonzero Q coefficient is positive and every omitted degree-box "
                "coefficient is explicitly checked as zero, so Q(X,Y,U)>0 for X,Y,U>0."
            ),
        },
        "nonvanishing": (
            "The positive-denominator Cayley clearing gives sign(P)=sign(Q) on the "
            "open domain, so P>0 and det Rstar never vanishes there."
        ),
        "inertia_continuation": (
            "Rstar is real symmetric and its entries are continuous on the open domain. "
            "Since det Rstar is nonzero throughout the connected domain, no eigenvalue "
            "can cross zero.  The exact positive seed fixes all four eigenvalues of "
            "Rstar as positive everywhere."
        ),
        "schur_lift_to_six_directions": (
            "The eliminated alpha,beta block has positive diagonal coefficients "
            "d_alpha,d_beta.  The Schur complement criterion therefore lifts "
            "Rstar positive definiteness to the full six fixed physical directions "
            "of the original M assertion through the displayed inverse coordinate map."
        ),
        "bareiss_scope_note": (
            "Bareiss pivots in the determinant artifact certify exact symbolic "
            "divisions after denominator clearing.  They are not used as domain-wide "
            "nonvanishing assumptions."
        ),
    }
    write_json(ctx.artifacts_dir / "domain_inertia_certificate.json", result)
    ctx.end("domain_inertia_certificate", {"status": result["status"]})
    return result


def write_result(
    ctx: RunContext,
    source_checks: dict[str, Any],
    rstar: RStarBuild,
    det: DeterminantBuild,
    p_build: PBuild,
    p_reference: dict[str, Any],
    q_build: QBuild,
    reference: dict[str, Any],
    seed: dict[str, Any],
    domain: dict[str, Any],
) -> None:
    ctx.begin("write_result", {"status": "PASS"})
    result = {
        "status": "PASS",
        "utc": utc_now_text(),
        "elapsed_seconds": round(ctx.elapsed(), 3),
        "requested_wall_seconds": ctx.wall_seconds,
        "internal_deadline_epoch": ctx.internal_deadline_epoch,
        "external_deadline_epoch": ctx.external_deadline_epoch,
        "effective_deadline_epoch": ctx.deadline_epoch,
        "remaining_seconds_at_result": max(0.0, round(ctx.remaining(), 3)),
        "source_checks": source_checks,
        "determinant": {
            "common_denominator": compact_expr(det.common_denominator),
            "bareiss_record_count": len(det.bareiss_records),
            "equality_checks": det.equality_checks,
        },
        "P": {
            "degree_box": list(p_build.degree_box),
            "term_count": len(p_build.P_poly.as_dict()),
            "identity_count": len(p_build.identities),
            "archived_source_factor_comparison": p_reference["status"],
        },
        "Q": {
            "degree_box": list(P_BOX),
            "nonzero_count": q_build.nonzero_count,
            "zero_count_in_box": q_build.zero_count,
            "min_positive_coefficient": q_build.min_coeff,
            "max_positive_coefficient": q_build.max_coeff,
            "identity_count": len(q_build.identities),
        },
        "reference": {
            "status": reference["status"],
            "full_degree_box_entries_checked": reference["full_degree_box_entries_checked"],
            "best_table_path": reference["best_comparison"]["json_path"],
        },
        "positive_seed": {
            "status": seed["status"],
            "scale": seed["scale"],
            "row_margins": seed["strict_diagonal_dominance_margins_before_division"],
        },
        "domain_inertia": domain,
        "artifacts": [
            "run_manifest.json",
            "artifacts/rstar_from_displayed_formula.json",
            "artifacts/determinant_cleared_matrix_before_bareiss.json",
            "artifacts/determinant_bareiss_certificate.json",
            "artifacts/determinant_independent_equality.json",
            "artifacts/P_polynomial.json",
            "artifacts/archived_P_source_factor_comparison.json",
            "artifacts/Q_direct_transform.json",
            "artifacts/Q_combinatorial_transform.json",
            "artifacts/Q_polynomial_full_box.json",
            "artifacts/archived_coefficient_comparison.json",
            "artifacts/positive_seed_certificate.json",
            "artifacts/domain_inertia_certificate.json",
        ],
        "acceptance_boundary": (
            "This is an author-produced exact artifact.  It is not an independent "
            "nonauthor FIRST acceptance."
        ),
    }
    write_json(ctx.out / "RESULT.json", result)
    ctx.end("write_result", {"result": "RESULT.json"})


def make_manifest(ctx: RunContext, argv: list[str]) -> dict[str, Any]:
    env = {name: os.environ.get(name) for name in THREAD_ENV_DEFAULTS}
    manifest = {
        "status": "STARTED",
        "utc_start": utc_now_text(),
        "pid": os.getpid(),
        "python": sys.version,
        "platform": platform.platform(),
        "sympy_version": sp.__version__,
        "argv_sanitized": [ctx.sanitize_text(arg) for arg in argv],
        "requested_wall_seconds": ctx.wall_seconds,
        "internal_deadline_epoch": ctx.internal_deadline_epoch,
        "external_deadline_epoch": ctx.external_deadline_epoch,
        "effective_deadline_epoch": ctx.deadline_epoch,
        "remaining_seconds_at_manifest": max(0.0, round(ctx.remaining(), 3)),
        "thread_environment": env,
        "scope": "independent r=0 Rstar -> det -> P -> Q author run",
        "forbidden_inputs": [
            "old checker imports",
            "saved Rstar matrices",
            "old P/Q before fresh construction",
            "C:\\canglan",
        ],
    }
    write_json(ctx.out / "run_manifest.json", manifest)
    return manifest


def external_deadline_from_env() -> int | None:
    raw = os.environ.get("C2_ABSOLUTE_DEADLINE_EPOCH")
    if raw is None or raw.strip() == "":
        return None
    try:
        value = int(raw.strip())
    except ValueError as exc:
        raise CertificateError(f"C2_ABSOLUTE_DEADLINE_EPOCH is not an integer: {raw!r}") from exc
    return value


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Independent exact r=0 certificate-chain verifier")
    parser.add_argument("--source-root", required=True, help="source directory containing structure/ and resume/")
    parser.add_argument("--out", required=True, help="output directory for checkpoints and artifacts")
    parser.add_argument("--wall-seconds", required=True, type=int, help="absolute wall budget for this process")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    source_root = Path(args.source_root).resolve()
    out = Path(args.out).resolve()
    if is_forbidden_canglan(source_root) or is_forbidden_canglan(out):
        raise SystemExit("refusing to read or write C:\\canglan")
    if args.wall_seconds <= 0:
        raise SystemExit("--wall-seconds must be positive")
    out.mkdir(parents=True, exist_ok=True)
    ctx = RunContext(
        source_root=source_root,
        out=out,
        wall_seconds=args.wall_seconds,
        external_deadline_epoch=external_deadline_from_env(),
    )
    ctx.sanitized_tokens = {
        str(source_root): "<SOURCE_ROOT>",
        str(out): "<OUT>",
        str(Path.cwd().resolve()): "<CWD>",
    }
    try:
        make_manifest(ctx, sys.argv)
        ctx.begin("preflight", {"source_root": "<SOURCE_ROOT>", "out": "<OUT>"})
        source_checks = source_file_checks(ctx)
        ctx.end("preflight", source_checks)

        rstar = build_r0_displayed_rstar(ctx)
        det = compute_determinant(ctx, rstar)
        p_build = extract_p(ctx, rstar, det)
        p_reference = compare_archived_p_source_factor(ctx, p_build)
        q_build = build_q(ctx, p_build)
        reference = compare_reference_coefficients(ctx, q_build)
        seed = positive_seed_certificate(ctx, rstar)
        domain = domain_inertia_certificate(ctx, rstar, p_build, q_build)
        write_result(ctx, source_checks, rstar, det, p_build, p_reference, q_build, reference, seed, domain)
        return 0
    except BaseException as exc:
        ctx.fail(exc)
        if isinstance(exc, DeadlineExceeded):
            return 124
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
