#!/usr/bin/env python3
"""Fresh nonauthor FIRST checker for the PR57 r=0 certificate chain.

This script is intentionally self-contained.  It reconstructs the displayed
four-by-four Schur complement from the frozen STRUCTURE formulas, derives the
determinant residual P, builds the positive-orthant Q, and only then opens the
archived P/Q comparison targets and candidate artifacts.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import os
import re
import sys
import time
import traceback
from pathlib import Path
from typing import Any


THREAD_LIMIT_ENV = {
    "OMP_NUM_THREADS": "1",
    "OPENBLAS_NUM_THREADS": "1",
    "MKL_NUM_THREADS": "1",
    "NUMEXPR_NUM_THREADS": "1",
    "VECLIB_MAXIMUM_THREADS": "1",
    "BLIS_NUM_THREADS": "1",
}

for _name, _value in THREAD_LIMIT_ENV.items():
    os.environ.setdefault(_name, _value)

import sympy as sp
from sympy.matrices.matrixbase import MatrixBase
from sympy.parsing.sympy_parser import (
    convert_xor,
    parse_expr,
    standard_transformations,
)


BOX = (4, 4, 16)
TRANSFORMS = standard_transformations + (convert_xor,)


class CheckError(RuntimeError):
    pass


def utc_now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def is_forbidden_canglan(path: Path) -> bool:
    text = str(path.resolve()).replace("/", "\\").lower()
    return text == "c:\\canglan" or text.startswith("c:\\canglan\\")


def jsonable(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, (sp.Integer, sp.Rational, sp.Basic)):
        return str(value)
    if isinstance(value, Path):
        return value.name
    if isinstance(value, dict):
        return {str(k): jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [jsonable(v) for v in value]
    return str(value)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(jsonable(payload), f, indent=2, sort_keys=True)
        f.write("\n")
    tmp.replace(path)


class Context:
    def __init__(self, candidate_root: Path, out: Path, wall_seconds: int, deadline_epoch: int | None) -> None:
        self.candidate_root = candidate_root.resolve()
        self.out = out.resolve()
        self.wall_seconds = wall_seconds
        self.started_wall = time.time()
        self.started_mono = time.monotonic()
        internal_deadline = int(self.started_wall + wall_seconds)
        self.deadline_epoch = min(internal_deadline, deadline_epoch) if deadline_epoch else internal_deadline
        self.index = 0
        self.sanitize_tokens = {
            str(self.candidate_root): "<CANDIDATE_ROOT>",
            str(self.out): "<OUT>",
            str(Path.cwd().resolve()): "<CWD>",
        }

    def elapsed(self) -> float:
        return time.monotonic() - self.started_mono

    def remaining(self) -> float:
        return self.deadline_epoch - time.time()

    def sanitize(self, text: str) -> str:
        result = text
        for raw, replacement in self.sanitize_tokens.items():
            result = result.replace(raw, replacement)
        return result

    def checkpoint(self, label: str, **details: Any) -> None:
        self.index += 1
        safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", label).strip("_") or "checkpoint"
        payload = {
            "index": self.index,
            "label": label,
            "utc": utc_now(),
            "elapsed_seconds": round(self.elapsed(), 3),
            "remaining_seconds": max(0.0, round(self.remaining(), 3)),
            "details": details,
        }
        write_json(self.out / "checkpoints" / f"{self.index:04d}_{safe}.json", payload)

    def check_deadline(self, label: str) -> None:
        if self.remaining() < 0:
            self.checkpoint("deadline_exceeded", during=label)
            raise TimeoutError(f"deadline exceeded during {label}")

    def fail(self, exc: BaseException) -> None:
        payload = {
            "status": "FAIL",
            "utc": utc_now(),
            "elapsed_seconds": round(self.elapsed(), 3),
            "exception_type": type(exc).__name__,
            "exception": self.sanitize(str(exc)),
            "traceback": self.sanitize(traceback.format_exc()),
        }
        write_json(self.out / "FAILURE.json", payload)


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def ensure_no_float(label: str, obj: Any) -> None:
    floats: set[sp.Float] = set()

    def visit(value: Any) -> None:
        if isinstance(value, MatrixBase):
            for entry in list(value):
                visit(entry)
        elif isinstance(value, sp.Basic):
            floats.update(value.atoms(sp.Float))
        elif isinstance(value, dict):
            for item in value.values():
                visit(item)
        elif isinstance(value, (list, tuple, set)):
            for item in value:
                visit(item)

    visit(obj)
    if floats:
        raise CheckError(f"{label} contains Float atoms: {sorted(map(str, floats))}")


def is_zero_expr(expr: Any) -> bool:
    if isinstance(expr, MatrixBase):
        for entry in list(expr):
            if sp.cancel(sp.together(entry)) != 0:
                return False
        return True
    return sp.cancel(sp.together(expr)) == 0


def assert_zero(label: str, expr: Any) -> dict[str, Any]:
    ensure_no_float(label, expr)
    if not is_zero_expr(expr):
        raise CheckError(f"{label} is not exactly zero")
    return {"label": label, "zero": True}


def poly_zz(label: str, expr: sp.Expr, variables: tuple[sp.Symbol, ...]) -> sp.Poly:
    ensure_no_float(label, expr)
    poly = sp.Poly(sp.expand(expr), *variables, domain=sp.ZZ)
    if sp.expand(poly.as_expr() - sp.expand(expr)) != 0:
        raise CheckError(f"{label} changed during ZZ coercion")
    return poly


def matrix_rows(matrix: sp.Matrix) -> list[list[str]]:
    return [[str(sp.cancel(matrix[i, j])) for j in range(matrix.cols)] for i in range(matrix.rows)]


def perm_sign(perm: tuple[int, ...]) -> int:
    inversions = 0
    for i in range(len(perm)):
        for j in range(i + 1, len(perm)):
            if perm[i] > perm[j]:
                inversions += 1
    return -1 if inversions % 2 else 1


def determinant_by_permutations(matrix: sp.Matrix, ctx: Context) -> sp.Expr:
    total = sp.Integer(0)
    for count, perm in enumerate(itertools.permutations(range(matrix.rows)), start=1):
        ctx.check_deadline(f"determinant permutation {count}")
        term = sp.Integer(perm_sign(perm))
        for i, j in enumerate(perm):
            term *= matrix[i, j]
        total += term
    return sp.cancel(sp.together(total))


def parse_sympy_expr(text: str, symbols: dict[str, sp.Symbol]) -> sp.Expr:
    return parse_expr(text, local_dict=symbols, transformations=TRANSFORMS, evaluate=True)


def require_source_fragments(candidate_root: Path) -> dict[str, Any]:
    structure_path = candidate_root / "inputs" / "source" / "structure" / "STRUCTURE.md"
    seed_path = candidate_root / "inputs" / "source" / "structure" / "POSITIVE_SEED.md"
    author_proof = candidate_root / "author_proof.md"
    implementation = candidate_root / "implementation" / "verify_r0_chain_independent.py"
    required = [structure_path, seed_path, author_proof, implementation]
    missing = [path.name for path in required if not path.exists()]
    if missing:
        raise CheckError(f"missing required candidate files: {missing}")
    for path in required:
        if is_forbidden_canglan(path):
            raise CheckError("refusing forbidden C:\\canglan path")

    structure = read_text(structure_path)
    seed = read_text(seed_path)
    proof = read_text(author_proof)
    implementation_text = read_text(implementation)

    fragments = [
        "Rstar =",
        "R0 = 4(R^T G + G R + G')",
        "ell_alpha",
        "ell_beta",
        "a=b=1/2",
        "n1=n2=4u/J",
        "n3=4u^3/J",
    ]
    missing_fragments = [fragment for fragment in fragments if fragment not in structure]
    if missing_fragments:
        raise CheckError(f"STRUCTURE.md missing expected displayed fragments: {missing_fragments}")

    import_lines = [
        line.strip()
        for line in implementation_text.splitlines()
        if re.match(r"^\s*(from|import)\s+", line)
    ]
    suspicious_imports = [
        line
        for line in import_lines
        if any(token in line.lower() for token in ["pr55", "lambda_zero52", "verify_r0", "r0_coefficient"])
    ]
    return {
        "structure_fragments_present": fragments,
        "seed_note_mentions_seed": "mu=nu=r=0" in seed and "Rstar" in seed,
        "author_proof_mentions_scope": "r=0" in proof and "full-r attempt" in proof.lower(),
        "implementation_static_suspicious_imports": suspicious_imports,
        "implementation_read_only_scan": "no import was performed",
    }


def build_displayed_rstar(ctx: Context) -> dict[str, Any]:
    ctx.check_deadline("build_displayed_rstar")
    mu, nu, u = sp.symbols("mu nu u")
    a = sp.Rational(1, 2)
    b = sp.Rational(1, 2)
    v = (1 - mu**2) / 4
    w = (1 - nu**2) / 4
    J = 1 - u**4
    d0 = (1 / J + 1) / 2
    d1 = (1 / J - 1) / 2
    d0p = 2 * u**3 / J**2
    d1p = 2 * u**3 / J**2

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
    Gp = d0p * D + d1p * S
    R = sp.diag(0, 1 / u, 1 / u, 2 / u)
    n1 = 4 * u / J
    n2 = 4 * u / J
    n3 = 4 * u**3 / J
    d_alpha = sp.cancel(n2 * a * u**2 * v / 2)
    d_beta = sp.cancel(n1 * b * u**2 * w / 2)

    R0 = 4 * (R.T * G + G * R + Gp) + sp.diag(
        0,
        n2 * v / (2 * u**2 * a),
        n1 * w / (2 * u**2 * b),
        n3 * v * w / (2 * u**4 * a * b),
    )
    R0 = R0.applyfunc(lambda entry: sp.cancel(sp.together(entry)))

    theta = (mu + nu) / 2
    ell_alpha = sp.Matrix([[8 * u * v * d1 * (-1), 8 * u * v * d1 * theta, 0, 8 * u * v * d1 * w]])
    ell_beta = sp.Matrix([[8 * u * w * d1 * (-1), 0, 8 * u * w * d1 * theta, 8 * u * w * d1 * v]])
    ell_alpha = ell_alpha.applyfunc(lambda entry: sp.cancel(sp.together(entry)))
    ell_beta = ell_beta.applyfunc(lambda entry: sp.cancel(sp.together(entry)))

    Rstar = R0 - (ell_alpha.T * ell_alpha) / (4 * d_alpha) - (ell_beta.T * ell_beta) / (4 * d_beta)
    Rstar = Rstar.applyfunc(lambda entry: sp.cancel(sp.together(entry)))

    m, p, q, h = sp.symbols("m p q h")
    y = sp.Matrix([m, p, q, h])
    U_alpha = sp.Matrix([2 * u * a * v, -u * a * mu, 0, 0])
    U_beta = sp.Matrix([2 * u * b * w, 0, -u * b * nu, 0])
    L_alpha_raw = (8 * (U_alpha.T * G * y)[0] - 2 * n2 * v * m + n2 * mu * v * p)
    L_beta_raw = (8 * (U_beta.T * G * y)[0] - 2 * n1 * w * m + n1 * nu * w * q)

    identities = [
        assert_zero("reflection S D^{-1} S = D", S * D.inv() * S - D),
        assert_zero("r=0 invisible mixed coefficient cancellation", u**2 * (n2 * b + n1 * a) - n3),
        assert_zero("d_alpha specialization", d_alpha - u**3 * v / J),
        assert_zero("d_beta specialization", d_beta - u**3 * w / J),
        assert_zero("ell_alpha raw coupling equals displayed row", L_alpha_raw - (ell_alpha * y)[0]),
        assert_zero("ell_beta raw coupling equals displayed row", L_beta_raw - (ell_beta * y)[0]),
    ]
    ensure_no_float("displayed Rstar", [R0, ell_alpha, ell_beta, Rstar])
    ctx.checkpoint("displayed Rstar built", identities=len(identities))
    return {
        "symbols": (mu, nu, u),
        "J": J,
        "v": v,
        "w": w,
        "d_alpha": d_alpha,
        "d_beta": d_beta,
        "Rstar": Rstar,
        "R0": R0,
        "ell_alpha": ell_alpha,
        "ell_beta": ell_beta,
        "identities": identities,
    }


def extract_p_from_determinant(ctx: Context, built: dict[str, Any]) -> dict[str, Any]:
    mu, nu, u = built["symbols"]
    J = built["J"]
    Rstar = built["Rstar"]
    ctx.checkpoint("before determinant", method="explicit 24-term permutation sum")
    det_perm = determinant_by_permutations(Rstar, ctx)
    ctx.checkpoint("after determinant", expression_chars=len(str(det_perm)))

    det_builtin = sp.cancel(sp.together(Rstar.det(method="berkowitz")))
    identities = [
        assert_zero("permutation determinant equals berkowitz determinant", det_perm - det_builtin),
    ]
    P_expr = sp.cancel(sp.together(det_perm * 2 * J**5 / ((1 - mu**2) ** 2 * (1 - nu**2) ** 2)))
    num, den = sp.together(P_expr).as_numer_denom()
    if sp.cancel(den - 1) != 0:
        raise CheckError(f"P extraction left denominator {den}")
    P_expr = sp.expand(num)
    P_poly = poly_zz("P", P_expr, (mu, nu, u))
    degree_box = tuple(P_poly.degree(var) for var in (mu, nu, u))
    if degree_box != BOX:
        raise CheckError(f"P degree box {degree_box} != {BOX}")
    if len(P_poly.as_dict()) != 26:
        raise CheckError(f"P term count {len(P_poly.as_dict())} != 26")
    identities.append(assert_zero("determinant/P identity", det_perm - ((1 - mu**2) ** 2 * (1 - nu**2) ** 2 * P_expr) / (2 * J**5)))

    ctx.checkpoint("P extracted", term_count=len(P_poly.as_dict()), degree_box=list(degree_box))
    return {
        "determinant": det_perm,
        "P_expr": P_expr,
        "P_poly": P_poly,
        "identities": identities,
    }


def compare_p_targets(ctx: Context, built: dict[str, Any], p_data: dict[str, Any]) -> dict[str, Any]:
    mu, nu, u = built["symbols"]
    P_expr = p_data["P_expr"]
    symbols = {"mu": mu, "nu": nu, "u": u}
    comparisons: list[dict[str, Any]] = []

    report_path = ctx.candidate_root / "inputs" / "source" / "resume" / "coefficient_outputs" / "r0_coefficient_report.json"
    report = read_json(report_path)
    archived = parse_sympy_expr(report["source_factor"], symbols)
    assert_zero("fresh P equals archived source_factor", P_expr - archived)
    comparisons.append({"target": "archived source_factor", "status": "matched"})

    artifact_path = ctx.candidate_root / "outputs" / "author01" / "artifacts" / "P_polynomial.json"
    artifact = read_json(artifact_path)
    artifact_text = artifact.get("P", {}).get("text")
    if not isinstance(artifact_text, str):
        raise CheckError("candidate P artifact does not contain P.text")
    artifact_expr = parse_sympy_expr(artifact_text, symbols)
    assert_zero("fresh P equals candidate P artifact", P_expr - artifact_expr)

    sparse = {}
    for row in artifact.get("sparse_coefficients", []):
        exp = tuple(int(x) for x in row["exponents"])
        coeff = int(row["coefficient"])
        if exp in sparse:
            raise CheckError(f"duplicate candidate P exponent {exp}")
        sparse[exp] = coeff
    if sparse != {tuple(exp): int(coeff) for exp, coeff in p_data["P_poly"].as_dict().items()}:
        raise CheckError("candidate P sparse coefficients do not match fresh P")
    comparisons.append({"target": "candidate P_polynomial.json", "status": "matched"})

    ctx.checkpoint("P targets compared", comparisons=comparisons)
    return {"status": "matched", "comparisons": comparisons}


def build_q(ctx: Context, built: dict[str, Any], p_data: dict[str, Any]) -> dict[str, Any]:
    mu, nu, u = built["symbols"]
    P_expr = p_data["P_expr"]
    P_poly = p_data["P_poly"]
    X, Y, U = sp.symbols("X Y U")
    ctx.checkpoint("before Q transform", methods=["direct homogeneous substitution", "coefficient binomial expansion"])

    direct = sp.together(
        (X + 1) ** BOX[0]
        * (Y + 1) ** BOX[1]
        * (U + 1) ** BOX[2]
        * P_expr.subs({mu: (X - 1) / (X + 1), nu: (Y - 1) / (Y + 1), u: U / (U + 1)})
    )
    num, den = direct.as_numer_denom()
    if sp.cancel(den - 1) != 0:
        raise CheckError(f"direct Q transform left denominator {den}")
    direct_poly = poly_zz("direct Q", sp.expand(num), (X, Y, U))

    combinatorial = sp.Integer(0)
    for (i, j, k), coeff in P_poly.as_dict().items():
        combinatorial += (
            coeff
            * (X - 1) ** i
            * (X + 1) ** (BOX[0] - i)
            * (Y - 1) ** j
            * (Y + 1) ** (BOX[1] - j)
            * U**k
            * (U + 1) ** (BOX[2] - k)
        )
    combinatorial_poly = poly_zz("combinatorial Q", sp.expand(combinatorial), (X, Y, U))
    assert_zero("direct Q equals combinatorial Q", direct_poly.as_expr() - combinatorial_poly.as_expr())

    q_dict = {tuple(exp): int(coeff) for exp, coeff in direct_poly.as_dict().items()}
    out_of_box = [exp for exp in q_dict if any(exp[i] < 0 or exp[i] > BOX[i] for i in range(3))]
    if out_of_box:
        raise CheckError(f"Q has exponents outside declared box: {out_of_box[:5]}")

    full = {}
    negatives = []
    positives = []
    zeros = 0
    for i in range(BOX[0] + 1):
        for j in range(BOX[1] + 1):
            for k in range(BOX[2] + 1):
                exp = (i, j, k)
                coeff = q_dict.get(exp, 0)
                full[exp] = coeff
                if coeff < 0:
                    negatives.append((exp, coeff))
                elif coeff > 0:
                    positives.append(coeff)
                else:
                    zeros += 1
    if negatives:
        raise CheckError(f"Q has negative coefficients: {negatives[:10]}")
    summary = {
        "nonzero_count": len(positives),
        "zero_count": zeros,
        "min_positive": min(positives),
        "max_positive": max(positives),
        "full_box_count": (BOX[0] + 1) * (BOX[1] + 1) * (BOX[2] + 1),
    }
    expected = {
        "nonzero_count": 389,
        "zero_count": 36,
        "min_positive": 192,
        "max_positive": 99220032,
        "full_box_count": 425,
    }
    if summary != expected:
        raise CheckError(f"Q coefficient summary {summary} != expected {expected}")

    ctx.checkpoint("Q built", **summary)
    return {
        "symbols": (X, Y, U),
        "Q_poly": direct_poly,
        "q_dict": q_dict,
        "full_dict": full,
        "summary": summary,
    }


def parse_coeff_rows(rows: Any, powers_key: str = "powers") -> dict[tuple[int, int, int], int]:
    if not isinstance(rows, list):
        raise CheckError("coefficient table is not a list")
    result: dict[tuple[int, int, int], int] = {}
    for row in rows:
        if not isinstance(row, dict):
            raise CheckError("coefficient row is not an object")
        key = powers_key if powers_key in row else "exponents"
        exp = tuple(int(x) for x in row[key])
        coeff = int(row["coefficient"])
        if exp in result:
            raise CheckError(f"duplicate coefficient exponent {exp}")
        result[exp] = coeff
    return result


def compare_q_targets(ctx: Context, q_data: dict[str, Any]) -> dict[str, Any]:
    full = q_data["full_dict"]
    comparisons: list[dict[str, Any]] = []

    archived_path = ctx.candidate_root / "inputs" / "source" / "resume" / "coefficient_outputs" / "r0_coefficient_table.json"
    archived_rows = read_json(archived_path)
    archived = parse_coeff_rows(archived_rows, "powers")
    mismatches = []
    for exp, actual in full.items():
        reference = archived.get(exp, 0)
        if actual != reference:
            mismatches.append({"exp": exp, "actual": actual, "reference": reference})
    archived_out = [exp for exp in archived if exp not in full]
    if mismatches or archived_out:
        raise CheckError(f"archived Q mismatch count={len(mismatches)}, out_of_box={archived_out[:5]}")
    comparisons.append({"target": "archived r0_coefficient_table.json", "status": "matched", "entries": len(archived)})

    candidate_path = ctx.candidate_root / "outputs" / "author01" / "artifacts" / "Q_polynomial_full_box.json"
    candidate_rows = read_json(candidate_path)
    candidate_full = parse_coeff_rows(candidate_rows.get("full_degree_box_coefficients"), "exponents")
    if candidate_full != full:
        raise CheckError("candidate Q full-degree box does not match fresh Q")
    comparisons.append({"target": "candidate Q_polynomial_full_box.json", "status": "matched", "entries": len(candidate_full)})

    result_path = ctx.candidate_root / "outputs" / "author01" / "RESULT.json"
    result = read_json(result_path)
    if result.get("status") != "PASS":
        raise CheckError("candidate RESULT.json is not PASS")
    comparisons.append({"target": "candidate RESULT.json", "status": "PASS"})

    ctx.checkpoint("Q targets compared", comparisons=comparisons)
    return {"status": "matched", "comparisons": comparisons}


def seed_certificate(ctx: Context, built: dict[str, Any]) -> dict[str, Any]:
    mu, nu, u = built["symbols"]
    Rstar = built["Rstar"]
    seed = Rstar.subs({mu: 0, nu: 0, u: sp.Rational(1, 2)}).applyfunc(lambda entry: sp.cancel(entry))
    denoms = [int(sp.denom(entry)) for entry in list(seed)]
    scale = math.lcm(*denoms)
    scaled = (scale * seed).applyfunc(lambda entry: sp.cancel(entry))
    expected_scaled = sp.Matrix(
        [
            [16144, 0, 0, 6076],
            [0, 94336, 6016, 0],
            [0, 6016, 94336, 0],
            [6076, 0, 0, 46129],
        ]
    )
    if scale != 14400 or scaled != expected_scaled:
        raise CheckError("seed matrix does not match the displayed POSITIVE_SEED matrix")
    margins = []
    for i in range(4):
        diag = int(scaled[i, i])
        off_sum = sum(abs(int(scaled[i, j])) for j in range(4) if j != i)
        margins.append(diag - off_sum)
    if margins != [10068, 88320, 88320, 40053]:
        raise CheckError(f"seed margins mismatch: {margins}")
    if any(m <= 0 for m in margins):
        raise CheckError("seed matrix is not strictly diagonally dominant")

    ctx.checkpoint("seed checked", scale=scale, margins=margins)
    return {
        "status": "positive",
        "scale": scale,
        "margins": margins,
        "scaled_Rstar": matrix_rows(scaled),
    }


def write_review_result(
    ctx: Context,
    source: dict[str, Any],
    built: dict[str, Any],
    p_data: dict[str, Any],
    p_compare: dict[str, Any],
    q_data: dict[str, Any],
    q_compare: dict[str, Any],
    seed: dict[str, Any],
) -> None:
    payload = {
        "status": "PASS",
        "reviewer": "fresh nonauthor FIRST r=0 checker",
        "utc": utc_now(),
        "elapsed_seconds": round(ctx.elapsed(), 3),
        "scope": {
            "public_commit": "ba890f6294272849fa0a20d5c7e0e9f97d171d51",
            "local_equivalent": "0e339c0a8b7ecfc263418fb64b3608298161e590",
            "chain": "displayed Rstar -> det -> P -> Q -> nonvanishing -> inertia -> six-direction Schur lift",
            "excluded": ["general r", "entropy counterexample", "novelty", "Lean claim"],
        },
        "source_scan": source,
        "displayed_formula_checks": built["identities"],
        "determinant": {
            "method": "explicit 24-term permutation determinant, checked against Berkowitz determinant",
            "determinant_expression_chars": len(str(p_data["determinant"])),
            "identity_checks": p_data["identities"],
        },
        "P": {
            "term_count": len(p_data["P_poly"].as_dict()),
            "degree_box": [p_data["P_poly"].degree(v) for v in built["symbols"]],
            "target_comparison": p_compare,
        },
        "Q": {
            "degree_box": list(BOX),
            "coefficient_summary": q_data["summary"],
            "target_comparison": q_compare,
            "omitted_archived_entries_treated_as_zero": True,
        },
        "seed": seed,
        "domain_and_lift_review": {
            "domain": "(-1,1) x (-1,1) x (0,1)",
            "domain_connected": True,
            "positive_denominators": [
                "u",
                "J=1-u^4",
                "1-mu^2",
                "1-nu^2",
                "v=(1-mu^2)/4",
                "w=(1-nu^2)/4",
                "d_alpha=u^3*v/J",
                "d_beta=u^3*w/J",
            ],
            "cayley_bijection": "mu=(X-1)/(X+1), nu=(Y-1)/(Y+1), u=U/(1+U) bijects to X,Y,U>0 with positive clearing factors",
            "nonvanishing": "Q has only positive nonzero coefficients and is not the zero polynomial, so P>0 and det Rstar is nonzero on the open domain",
            "inertia": "real symmetric continuous Rstar on a connected domain plus one positive seed and nonzero determinant fixes four positive eigenvalues everywhere",
            "six_direction_lift": "accepted Schur reduction has positive eliminated block and invertible fixed-direction coordinate map at r=0",
            "bareiss_note": "no domain nonvanishing is inferred from Bareiss pivots; this checker does not use them for the inertia argument",
        },
        "verdict": "CORRECT within the frozen r=0 scope, conditional only on the already-accepted main Schur reduction to the displayed Rstar",
    }
    write_json(ctx.out / "RESULT.json", payload)
    ctx.checkpoint("result written", status="PASS")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-root", required=True, help="root containing inputs/, outputs/author01/, implementation/, author_proof.md")
    parser.add_argument("--out", required=True, help="review output directory")
    parser.add_argument("--wall-seconds", type=int, default=900)
    parser.add_argument("--deadline-epoch", type=int, default=None)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    candidate_root = Path(args.candidate_root)
    out = Path(args.out)
    if args.wall_seconds <= 0:
        raise SystemExit("--wall-seconds must be positive")
    if is_forbidden_canglan(candidate_root) or is_forbidden_canglan(out):
        raise SystemExit("refusing C:\\canglan")
    out.mkdir(parents=True, exist_ok=True)
    ctx = Context(candidate_root, out, args.wall_seconds, args.deadline_epoch)
    try:
        write_json(
            ctx.out / "run_manifest.json",
            {
                "status": "STARTED",
                "utc": utc_now(),
                "argv_sanitized": [ctx.sanitize(arg) for arg in sys.argv],
                "thread_env": {name: os.environ.get(name) for name in THREAD_LIMIT_ENV},
                "deadline_epoch": ctx.deadline_epoch,
                "candidate_root": "<CANDIDATE_ROOT>",
                "out": "<OUT>",
            },
        )
        ctx.checkpoint("preflight begin")
        source = require_source_fragments(ctx.candidate_root)
        ctx.checkpoint("preflight complete")
        built = build_displayed_rstar(ctx)
        p_data = extract_p_from_determinant(ctx, built)
        p_compare = compare_p_targets(ctx, built, p_data)
        q_data = build_q(ctx, built, p_data)
        q_compare = compare_q_targets(ctx, q_data)
        seed = seed_certificate(ctx, built)
        write_review_result(ctx, source, built, p_data, p_compare, q_data, q_compare, seed)
        return 0
    except BaseException as exc:
        ctx.fail(exc)
        return 124 if isinstance(exc, TimeoutError) else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
