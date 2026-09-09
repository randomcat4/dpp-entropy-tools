#!/usr/bin/env python3
"""Exact implementation for issue52 Lambda=0 radial derivative.

The script has two gates:
1. reconstruct the atom jets from DPP inclusion determinants and verify the
   literal matrix M = dF/du + Q from the frozen issue formula;
2. clear the common positive denominator and run bounded fraction-free
   determinant/factor attempts for r=0 and then full r.

No private paths or connection data are written by this script.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import os
import platform
import signal
import sys
import time
import traceback
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import sympy as sp


@dataclass
class Model:
    mu: sp.Symbol
    nu: sp.Symbol
    r: sp.Symbol
    u: sp.Symbol
    zvars: tuple[sp.Symbol, ...]
    aux: tuple[sp.Symbol, sp.Symbol]
    a: sp.Expr
    b: sp.Expr
    v: sp.Expr
    w: sp.Expr
    x: sp.Expr
    y: sp.Expr
    z: sp.Expr
    J: sp.Expr
    L: sp.Expr
    Fmat: sp.Matrix
    Q: sp.Matrix
    M: sp.Matrix


class StageTimeout(TimeoutError):
    pass


class Alarm:
    def __init__(self, seconds: int, label: str):
        self.seconds = max(1, int(seconds))
        self.label = label
        self.old_handler = None

    def __enter__(self):
        if hasattr(signal, "SIGALRM"):
            self.old_handler = signal.getsignal(signal.SIGALRM)
            signal.signal(signal.SIGALRM, self._handle)
            signal.alarm(self.seconds)
        return self

    def __exit__(self, exc_type, exc, tb):
        if hasattr(signal, "SIGALRM"):
            signal.alarm(0)
            signal.signal(signal.SIGALRM, self.old_handler)
        return False

    def _handle(self, signum, frame):
        raise StageTimeout(f"{self.label} exceeded {self.seconds} seconds")


def now_utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def atomic_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def atomic_json(path: Path, obj: Any) -> None:
    atomic_text(path, json.dumps(obj, indent=2, sort_keys=True) + "\n")


def sstr(expr: Any) -> str:
    return sp.sstr(expr)


def matrix_strings(M: sp.Matrix) -> list[list[str]]:
    return [[sstr(M[i, j]) for j in range(M.cols)] for i in range(M.rows)]


def sympy_env() -> dict[str, Any]:
    return {
        "python": sys.version.replace("\n", " "),
        "platform": platform.platform(),
        "sympy": sp.__version__,
        "pid": os.getpid(),
        "cwd_record": "present but not stored",
        "thread_env": {
            k: os.environ.get(k)
            for k in [
                "OMP_NUM_THREADS",
                "OPENBLAS_NUM_THREADS",
                "MKL_NUM_THREADS",
                "NUMEXPR_NUM_THREADS",
                "VECLIB_MAXIMUM_THREADS",
            ]
        },
    }


def build_model() -> Model:
    mu, nu, r, u = sp.symbols("mu nu r u")
    A, B, C, E, F, G = sp.symbols("A B C E F G")
    a = (1 + r) / 2
    b = (1 - r) / 2
    v = (1 - mu**2) / 4
    w = (1 - nu**2) / 4
    x = (1 + mu) / 2
    y = (1 + nu) / 2
    z = sp.Rational(1, 2) - u**2 * (a * mu + b * nu) / 2
    J = 1 - u**4
    L = 1 - r**2 * u**4

    zvars = (A, B, C, E, F, G)
    Fmat = sp.zeros(6)
    for i, j in itertools.product([0, 1], repeat=2):
        Pij = (1 + (2 * i - 1) * mu) * (1 + (2 * j - 1) * nu) / 4
        ei = i - x
        fj = j - y
        q = sp.Matrix(
            [
                u**2 * a * ei**2,
                u**2 * b * fj**2,
                1,
                2 * u**2 * a * b * ei * fj,
                -2 * u * a * ei,
                -2 * u * b * fj,
            ]
        )
        den = J if i == j else L
        Fmat += (4 * Pij / den) * (q * q.T)

    n1 = 4 * u * (1 / J - r / L)
    n2 = 4 * u * (1 / J + r / L)
    n3 = 4 * u**3 * (1 - r**2) / (J * L)
    Q = sp.zeros(6)

    def add_sym(i0: int, j0: int, val: sp.Expr) -> None:
        Q[i0, j0] += val
        if i0 != j0:
            Q[j0, i0] += val

    add_sym(0, 1, -n3 * v * w)
    add_sym(0, 2, -n2 * v)
    add_sym(1, 2, -n1 * w)
    add_sym(3, 3, 2 * n3 * a * b * v * w)
    add_sym(4, 4, 2 * n2 * a * v)
    add_sym(5, 5, 2 * n1 * b * w)

    M = Fmat.diff(u) + Q
    return Model(mu, nu, r, u, zvars, sp.symbols("rho sigma"), a, b, v, w, x, y, z, J, L, Fmat, Q, M)


def reduce_aux(expr: sp.Expr, model: Model) -> sp.Expr:
    rho, sigma = model.aux
    rho2 = model.u**2 * model.a * model.v
    sigma2 = model.u**2 * model.b * model.w
    expr = sp.expand(expr)
    poly = sp.Poly(expr, rho, sigma, domain="EX")
    out = sp.S.Zero
    bad_terms: list[tuple[tuple[int, int], sp.Expr]] = []
    for (i, j), coeff in poly.terms():
        if i % 2 or j % 2:
            bad_terms.append(((i, j), coeff))
            continue
        out += coeff * rho2 ** (i // 2) * sigma2 ** (j // 2)
    if bad_terms:
        raise ValueError(f"auxiliary reduction left odd powers: {bad_terms[:3]}")
    return sp.cancel(out)


def det_subset(M: sp.Matrix, subset: tuple[int, ...]) -> sp.Expr:
    if not subset:
        return sp.S.One
    return M.extract(subset, subset).det()


def atom_polynomial(bits: tuple[int, int, int], Kt: sp.Matrix) -> sp.Expr:
    ones = tuple(idx for idx, bit in enumerate(bits) if bit)
    out = sp.S.Zero
    for mask in range(8):
        T = tuple(idx for idx in range(3) if mask & (1 << idx))
        if all(idx in T for idx in ones):
            out += (-1) ** (len(T) - len(ones)) * det_subset(Kt, T)
    return sp.expand(out)


def linear_vector(expr: sp.Expr, zvars: tuple[sp.Symbol, ...]) -> sp.Matrix:
    poly = sp.Poly(sp.expand(expr), *zvars, domain="EX")
    return sp.Matrix([poly.coeff_monomial(z) for z in zvars])


def quadratic_matrix(expr: sp.Expr, zvars: tuple[sp.Symbol, ...]) -> sp.Matrix:
    poly = sp.Poly(sp.expand(expr), *zvars, domain="EX")
    n = len(zvars)
    M = sp.zeros(n)
    for i in range(n):
        M[i, i] = poly.coeff_monomial(zvars[i] ** 2)
        for j in range(i + 1, n):
            c = poly.coeff_monomial(zvars[i] * zvars[j])
            M[i, j] = c / 2
            M[j, i] = c / 2
    return M


def zero_expr(expr: sp.Expr) -> bool:
    return sp.cancel(sp.together(expr)) == 0


def zero_matrix(M: sp.Matrix) -> tuple[bool, list[dict[str, str]]]:
    failures: list[dict[str, str]] = []
    for i in range(M.rows):
        for j in range(M.cols):
            diff = sp.cancel(sp.together(M[i, j]))
            if diff != 0:
                failures.append({"entry": f"{i},{j}", "value": sstr(diff)})
    return (not failures), failures


def matrix_degree_bounds(M: sp.Matrix, vars_: tuple[sp.Symbol, ...]) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    total_max = 0
    per_var_max = [0 for _ in vars_]
    for i in range(M.rows):
        for j in range(M.cols):
            num, den = sp.fraction(sp.together(M[i, j]))
            for label, expr in [("num", num), ("den", den)]:
                try:
                    P = sp.Poly(sp.expand(expr), *vars_)
                    total = P.total_degree()
                    degrees = [P.degree(v) for v in vars_]
                    if label == "num":
                        total_max = max(total_max, total)
                        per_var_max = [max(a, b) for a, b in zip(per_var_max, degrees)]
                    entries.append(
                        {
                            "entry": f"{i},{j}",
                            "part": label,
                            "total_degree": total,
                            "degrees": dict(zip([str(v) for v in vars_], degrees)),
                            "terms": len(P.terms()),
                        }
                    )
                except Exception as exc:
                    entries.append({"entry": f"{i},{j}", "part": label, "error": repr(exc)})
    return {
        "entry_count": M.rows * M.cols,
        "max_numerator_total_degree": total_max,
        "max_numerator_degrees": dict(zip([str(v) for v in vars_], per_var_max)),
        "entries": entries,
    }


def determinant_degree_bound(M: sp.Matrix, vars_: tuple[sp.Symbol, ...]) -> dict[str, Any]:
    total_deg: list[list[int]] = []
    var_deg: list[list[list[int]]] = []
    term_counts: list[list[int]] = []
    for i in range(M.rows):
        total_row = []
        var_row = []
        term_row = []
        for j in range(M.cols):
            num, den = sp.fraction(sp.together(M[i, j]))
            if den != 1:
                num = sp.together(M[i, j]).as_numer_denom()[0]
            P = sp.Poly(sp.expand(num), *vars_)
            total_row.append(P.total_degree())
            var_row.append([P.degree(v) for v in vars_])
            term_row.append(len(P.terms()))
        total_deg.append(total_row)
        var_deg.append(var_row)
        term_counts.append(term_row)

    best_total = 0
    best_per_var = [0 for _ in vars_]
    for perm in itertools.permutations(range(M.cols)):
        best_total = max(best_total, sum(total_deg[i][perm[i]] for i in range(M.rows)))
        for k in range(len(vars_)):
            best_per_var[k] = max(best_per_var[k], sum(var_deg[i][perm[i]][k] for i in range(M.rows)))
    return {
        "leibniz_total_degree_bound": best_total,
        "leibniz_per_variable_degree_bounds": dict(zip([str(v) for v in vars_], best_per_var)),
        "entry_total_degrees": total_deg,
        "entry_term_counts": term_counts,
    }


def build_atom_jets(model: Model) -> dict[tuple[int, int, int], dict[str, sp.Expr]]:
    tau = sp.symbols("tau")
    A, B, C, E, F, G = model.zvars
    rho, sigma = model.aux
    K = sp.Matrix(
        [
            [model.x, 0, rho],
            [0, model.y, sigma],
            [rho, sigma, model.z],
        ]
    )
    D = sp.Matrix(
        [
            [model.v * A, rho * sigma * E / model.u**2, rho * F / model.u],
            [rho * sigma * E / model.u**2, model.w * B, sigma * G / model.u],
            [rho * F / model.u, sigma * G / model.u, C],
        ]
    )
    Kt = K + tau * D
    jets: dict[tuple[int, int, int], dict[str, sp.Expr]] = {}
    for bits in itertools.product([0, 1], repeat=3):
        poly = atom_polynomial(bits, Kt)
        jets[bits] = {
            "p0": reduce_aux(poly.coeff(tau, 0), model),
            "p1": reduce_aux(poly.coeff(tau, 1), model),
            "p2": reduce_aux(2 * poly.coeff(tau, 2), model),
        }
    return jets


def pair_data(model: Model, i: int, j: int) -> dict[str, sp.Expr]:
    A, B, C, E, F, G = model.zvars
    Pij = (1 + (2 * i - 1) * model.mu) * (1 + (2 * j - 1) * model.nu) / 4
    ei = i - model.x
    fj = j - model.y
    t = (1 - model.u**2) / 2 + model.u**2 * model.a * (1 - i) + model.u**2 * model.b * (1 - j)
    q = sp.Matrix(
        [
            model.u**2 * model.a * ei**2,
            model.u**2 * model.b * fj**2,
            1,
            2 * model.u**2 * model.a * model.b * ei * fj,
            -2 * model.u * model.a * ei,
            -2 * model.u * model.b * fj,
        ]
    )
    Pprime = Pij * (ei * A + fj * B)
    T = (q.T * sp.Matrix(model.zvars))[0]
    den = model.J if i == j else model.L
    return {"P": Pij, "e": ei, "f": fj, "t": t, "q": q, "Pprime": Pprime, "T": T, "den": den}


def derive(output: Path) -> dict[str, Any]:
    started = time.time()
    output.parent.mkdir(parents=True, exist_ok=True)
    model = build_model()
    report: dict[str, Any] = {
        "started_utc": now_utc(),
        "environment": sympy_env(),
        "domain": {
            "mu": "(-1,1)",
            "nu": "(-1,1)",
            "r": "(-1,1)",
            "u": "(0,1)",
        },
        "known_positive_factors": {
            "a": "(1+r)/2 > 0",
            "b": "(1-r)/2 > 0",
            "v": "(1-mu^2)/4 > 0",
            "w": "(1-nu^2)/4 > 0",
            "J": "1-u^4 > 0",
            "L": "1-r^2*u^4 > 0",
            "n1": "4*u*(1-r)*(1+r*u^4)/(J*L) > 0",
            "n2": "4*u*(1+r)*(1-r*u^4)/(J*L) > 0",
            "n3": "4*u^3*(1-r^2)/(J*L) > 0",
            "common_entry_denominator": "8*(1-u^4)^2*(1-r^2*u^4)^2 > 0",
        },
    }

    jets = build_atom_jets(model)
    checks: dict[str, Any] = {}

    p0_failures = []
    p1_failures = []
    fisher_pair_failures = []
    fisher_sum = sp.zeros(6)
    fisher_expected_sum = sp.zeros(6)
    for i, j in itertools.product([0, 1], repeat=2):
        pdata = pair_data(model, i, j)
        Pij, t, T, Pprime = pdata["P"], pdata["t"], pdata["T"], pdata["Pprime"]
        expected_p0_1 = sp.cancel(Pij * t)
        expected_p0_0 = sp.cancel(Pij * (1 - t))
        expected_p1_1 = sp.cancel(Pprime * t + Pij * T)
        expected_p1_0 = sp.cancel(Pprime * (1 - t) - Pij * T)
        for k, expected_p0, expected_p1 in [
            (1, expected_p0_1, expected_p1_1),
            (0, expected_p0_0, expected_p1_0),
        ]:
            bits = (i, j, k)
            if not zero_expr(jets[bits]["p0"] - expected_p0):
                p0_failures.append({"bits": bits, "diff": sstr(sp.cancel(jets[bits]["p0"] - expected_p0))})
            if not zero_expr(jets[bits]["p1"] - expected_p1):
                p1_failures.append({"bits": bits, "diff": sstr(sp.cancel(jets[bits]["p1"] - expected_p1))})

        l1 = linear_vector(jets[(i, j, 1)]["p1"], model.zvars)
        l0 = linear_vector(jets[(i, j, 0)]["p1"], model.zvars)
        pair_actual = l1 * l1.T / expected_p0_1 + l0 * l0.T / expected_p0_0
        pprime_vec = linear_vector(Pprime, model.zvars)
        q = pdata["q"]
        pair_expected = pprime_vec * pprime_vec.T / Pij + Pij * (q * q.T) / (t * (1 - t))
        ok, failures = zero_matrix(pair_actual - pair_expected)
        if not ok:
            fisher_pair_failures.append({"pair": [i, j], "failures": failures[:3]})
        fisher_sum += pair_actual
        fisher_expected_sum += pair_expected

    marginal = sp.diag(model.v, model.w, 0, 0, 0, 0)
    ok_fisher, fisher_failures = zero_matrix(fisher_sum - (marginal + model.Fmat))
    checks["atom_probabilities"] = {"ok": not p0_failures, "failures": p0_failures[:8]}
    checks["atom_first_jets"] = {"ok": not p1_failures, "failures": p1_failures[:8]}
    checks["pair_fisher_split"] = {"ok": not fisher_pair_failures, "failures": fisher_pair_failures[:4]}
    checks["complete_fisher_identity"] = {"ok": ok_fisher, "failures": fisher_failures[:8]}

    rho, sigma = model.aux
    A, B, C, E, F, G = model.zvars
    K = sp.Matrix(
        [
            [model.x, 0, rho],
            [0, model.y, sigma],
            [rho, sigma, model.z],
        ]
    )
    D = sp.Matrix(
        [
            [model.v * A, rho * sigma * E / model.u**2, rho * F / model.u],
            [rho * sigma * E / model.u**2, model.w * B, sigma * G / model.u],
            [rho * F / model.u, sigma * G / model.u, C],
        ]
    )
    detD12 = reduce_aux(D[0, 0] * D[1, 1] - D[0, 1] ** 2, model)
    detD13 = reduce_aux(D[0, 0] * D[2, 2] - D[0, 2] ** 2, model)
    detD23 = reduce_aux(D[1, 1] * D[2, 2] - D[1, 2] ** 2, model)
    adjD = D.adjugate()
    trKadjD = reduce_aux(sum(K[i, j] * adjD[j, i] for i in range(3) for j in range(3)), model)

    Lsym = {bits: sp.symbols("L%d%d%d" % bits) for bits in itertools.product([0, 1], repeat=3)}

    def psi(i: int, j: int) -> sp.Expr:
        return Lsym[(i, j, 1)] - Lsym[(i, j, 0)]

    ell0 = psi(0, 0) - psi(1, 0)
    k0 = psi(0, 0) - psi(0, 1)
    v0log = Lsym[(1, 0, 0)] + Lsym[(0, 1, 0)] - Lsym[(0, 0, 0)] - Lsym[(1, 1, 0)]
    v1log = Lsym[(1, 0, 1)] + Lsym[(0, 1, 1)] - Lsym[(0, 0, 1)] - Lsym[(1, 1, 1)]
    Lambda = v0log - v1log
    expected_log_expr = -2 * k0 * detD23 - 2 * ell0 * detD13 - 2 * v0log * detD12 + 2 * Lambda * trKadjD

    log_failures = []
    for bits, Lbit in Lsym.items():
        actual_matrix = quadratic_matrix(jets[bits]["p2"], model.zvars)
        expected_matrix = quadratic_matrix(reduce_aux(sp.expand(expected_log_expr).coeff(Lbit), model), model.zvars)
        ok, failures = zero_matrix(actual_matrix - expected_matrix)
        if not ok:
            log_failures.append({"bits": bits, "failures": failures[:3]})
    checks["log_acceleration_coefficients"] = {"ok": not log_failures, "failures": log_failures[:8]}

    n1 = 4 * model.u * (1 / model.J - model.r / model.L)
    n2 = 4 * model.u * (1 / model.J + model.r / model.L)
    n3 = 4 * model.u**3 * (1 - model.r**2) / (model.J * model.L)
    log_derivative_expr = -2 * n1 * detD23 - 2 * n2 * detD13 - 2 * n3 * detD12
    log_derivative_matrix = quadratic_matrix(sp.cancel(log_derivative_expr), model.zvars)
    ok_Q, Q_failures = zero_matrix(log_derivative_matrix - model.Q)
    checks["Q_from_log_derivative"] = {"ok": ok_Q, "failures": Q_failures[:8]}

    B0 = marginal + model.Fmat.subs(model.u, 0)
    expected_B0 = sp.diag(model.v, model.w, 4, 0, 0, 0)
    ok_B0, B0_failures = zero_matrix(B0 - expected_B0)
    checks["initial_negative_hessian"] = {"ok": ok_B0, "failures": B0_failures[:8]}

    common = 8 * model.J**2 * model.L**2
    cleared = sp.zeros(6)
    denom_failures = []
    for i in range(6):
        for j in range(6):
            entry = sp.cancel(common * model.M[i, j])
            num, den = sp.fraction(sp.together(entry))
            if den != 1:
                denom_failures.append({"entry": f"{i},{j}", "denominator": sstr(den)})
            cleared[i, j] = sp.expand(num / den)
    checks["common_denominator_clears_M"] = {"ok": not denom_failures, "failures": denom_failures[:8]}

    all_ok = all(item.get("ok", False) for item in checks.values())
    report.update(
        {
            "finished_utc": now_utc(),
            "elapsed_seconds": round(time.time() - started, 3),
            "checks": checks,
            "all_derivation_checks_ok": all_ok,
            "M_matrix": matrix_strings(model.M),
            "Q_matrix": matrix_strings(model.Q),
            "cleared_common_matrix_upper_triangle": [
                {"entry": [i + 1, j + 1], "polynomial": sstr(cleared[i, j])}
                for i in range(6)
                for j in range(i, 6)
            ],
            "cleared_common_entry_degrees": matrix_degree_bounds(cleared, (model.mu, model.nu, model.r, model.u)),
        }
    )
    atomic_json(output, report)
    if not all_ok:
        raise RuntimeError("derive gate failed; see output JSON")
    return report


def positive_seed_report(M: sp.Matrix, model: Model, case: str) -> dict[str, Any]:
    subs = {model.mu: sp.Rational(0), model.nu: sp.Rational(0), model.u: sp.Rational(1, 2)}
    if case == "full":
        subs[model.r] = sp.Rational(0)
    elif case == "r0":
        subs[model.r] = sp.Rational(0)
    Ms = sp.Matrix([[sp.cancel(M[i, j].subs(subs)) for j in range(6)] for i in range(6)])
    minors = []
    ok = True
    for k in range(1, 7):
        val = sp.cancel(Ms[:k, :k].det())
        minors.append(sstr(val))
        if not (val > 0):
            ok = False
    return {
        "point": {"mu": "0", "nu": "0", "r": "0", "u": "1/2"},
        "leading_principal_minors": minors,
        "sylvester_positive": ok,
    }


def normalize_factor(expr: sp.Expr, model: Model) -> tuple[sp.Expr, str]:
    expr = sp.factor(expr)
    positives = [
        1 + model.mu,
        1 - model.mu,
        1 + model.nu,
        1 - model.nu,
        1 + model.r,
        1 - model.r,
        model.u,
        model.J,
        model.L,
        1 + model.r * model.u**4,
        1 - model.r * model.u**4,
    ]
    for p in positives:
        if zero_expr(expr - p):
            return p, "positive_on_domain"
        if zero_expr(expr + p):
            return p, "positive_on_domain_times_minus_one"
    return expr, "unclassified"


def polynomial_gcd(values: list[sp.Expr], vars_: tuple[sp.Symbol, ...]) -> sp.Expr:
    nums = []
    for value in values:
        if value == 0:
            continue
        num, den = sp.fraction(sp.together(value))
        if den != 1:
            num = sp.together(value).as_numer_denom()[0]
        nums.append(sp.Poly(sp.expand(num), *vars_).as_expr())
    if not nums:
        return sp.S.One
    return sp.factor(sp.gcd_list(nums))


def extract_row_col_factors(N: sp.Matrix, vars_: tuple[sp.Symbol, ...], model: Model) -> tuple[sp.Matrix, dict[str, Any]]:
    R = sp.MutableDenseMatrix(N)
    row_factors = []
    col_factors = []
    determinant_factor = sp.S.One
    for i in range(R.rows):
        g = polynomial_gcd([R[i, j] for j in range(R.cols)], vars_)
        if g != 0 and g != 1 and g != -1:
            norm, sign = normalize_factor(g, model)
            row_factors.append({"row": i + 1, "factor": sstr(norm), "classification": sign})
            determinant_factor *= norm
            for j in range(R.cols):
                R[i, j] = sp.cancel(R[i, j] / norm)
    for j in range(R.cols):
        g = polynomial_gcd([R[i, j] for i in range(R.rows)], vars_)
        if g != 0 and g != 1 and g != -1:
            norm, sign = normalize_factor(g, model)
            col_factors.append({"column": j + 1, "factor": sstr(norm), "classification": sign})
            determinant_factor *= norm
            for i in range(R.rows):
                R[i, j] = sp.cancel(R[i, j] / norm)
    return sp.Matrix(R), {
        "row_factors": row_factors,
        "column_factors": col_factors,
        "determinant_factor_product": sstr(sp.factor(determinant_factor)),
    }


def clear_matrix_for_case(model: Model, case: str) -> tuple[sp.Matrix, tuple[sp.Symbol, ...], sp.Expr]:
    if case == "r0":
        M = model.M.subs(model.r, 0)
        J = model.J
        scale = 8 * J**2
        vars_ = (model.mu, model.nu, model.u)
    elif case == "full":
        M = model.M
        scale = 8 * model.J**2 * model.L**2
        vars_ = (model.mu, model.nu, model.r, model.u)
    else:
        raise ValueError(f"unknown case {case}")
    N = sp.zeros(6)
    for i in range(6):
        for j in range(6):
            N[i, j] = sp.expand(sp.cancel(scale * M[i, j]))
    return N, vars_, scale


def structure_reduction(model: Model, case: str) -> dict[str, Any]:
    alpha, beta, m, p, q, h = sp.symbols("alpha beta m p q h")
    newvars = (alpha, beta, m, p, q, h)
    M = model.M.subs(model.r, 0) if case == "r0" else model.M
    n1 = 4 * model.u * (1 / model.J - model.r / model.L)
    n2 = 4 * model.u * (1 / model.J + model.r / model.L)
    n3 = 4 * model.u**3 * (1 - model.r**2) / (model.J * model.L)
    if case == "r0":
        n1 = n1.subs(model.r, 0)
        n2 = n2.subs(model.r, 0)
        n3 = n3.subs(model.r, 0)
    a = model.a.subs(model.r, 0) if case == "r0" else model.a
    b = model.b.subs(model.r, 0) if case == "r0" else model.b

    P = sp.zeros(6)
    P[0, 0] = 1
    P[1, 1] = 1
    P[2, 0] = -model.u**2 * a * model.v
    P[2, 1] = -model.u**2 * b * model.w
    P[2, 2] = 1
    P[3, 5] = 1 / (2 * model.u**2 * a * b)
    P[4, 0] = -model.u * model.mu / 2
    P[4, 3] = -1 / (2 * model.u * a)
    P[5, 1] = -model.u * model.nu / 2
    P[5, 4] = -1 / (2 * model.u * b)

    Mnew = sp.Matrix([[sp.cancel(e) for e in row] for row in (P.T * M * P).tolist()])
    dalpha = sp.cancel(n2 * a * model.u**2 * model.v / 2)
    dbeta = sp.cancel(n1 * b * model.u**2 * model.w / 2)
    invisible_identity = sp.cancel(model.u**2 * (n2 * b + n1 * a) - n3)

    checks = {
        "alpha_beta_offdiag_zero": zero_expr(Mnew[0, 1]),
        "dalpha_identity": zero_expr(Mnew[0, 0] - dalpha),
        "dbeta_identity": zero_expr(Mnew[1, 1] - dbeta),
        "invisible_mixed_cancellation": zero_expr(invisible_identity),
    }

    yblock = Mnew[2:6, 2:6]
    balpha = sp.Matrix([Mnew[0, j] for j in range(2, 6)])
    bbeta = sp.Matrix([Mnew[1, j] for j in range(2, 6)])
    Rstar = sp.Matrix(
        [
            [
                sp.cancel(yblock[i, j] - balpha[i] * balpha[j] / dalpha - bbeta[i] * bbeta[j] / dbeta)
                for j in range(4)
            ]
            for i in range(4)
        ]
    )
    detP = sp.factor(P.det())
    if case == "r0":
        detP = sp.factor(detP.subs(model.r, 0))
        Rstar = sp.Matrix([[sp.cancel(e.subs(model.r, 0)) for e in row] for row in Rstar.tolist()])
        Mnew = sp.Matrix([[sp.cancel(e.subs(model.r, 0)) for e in row] for row in Mnew.tolist()])
        dalpha = sp.cancel(dalpha.subs(model.r, 0))
        dbeta = sp.cancel(dbeta.subs(model.r, 0))

    vars_ = (model.mu, model.nu, model.u) if case == "r0" else (model.mu, model.nu, model.r, model.u)
    return {
        "case": case,
        "new_variables": [str(v) for v in newvars],
        "sign_variables": [str(v) for v in vars_],
        "transform_old_from_new": matrix_strings(P),
        "transform_determinant": sstr(detP),
        "dalpha": sstr(dalpha),
        "dbeta": sstr(dbeta),
        "checks": checks,
        "M_in_new_coordinates_upper_triangle": [
            {"entry": [i + 1, j + 1], "value": sstr(Mnew[i, j])}
            for i in range(6)
            for j in range(i, 6)
        ],
        "Rstar": Rstar,
        "Rstar_strings": matrix_strings(Rstar),
        "Rstar_degree_bounds": matrix_degree_bounds(Rstar, vars_),
    }


def clear_rstar_by_square_lcm(Rstar: sp.Matrix, vars_: tuple[sp.Symbol, ...]) -> tuple[sp.Matrix, sp.Expr, dict[str, Any]]:
    denoms = []
    for entry in list(Rstar):
        den = sp.fraction(sp.together(entry))[1]
        denoms.append(sp.factor(den))
    lcm = sp.factor(sp.lcm_list(denoms)) if denoms else sp.S.One
    scale = sp.factor(lcm**2)
    S = sp.zeros(Rstar.rows)
    failures = []
    for i in range(Rstar.rows):
        for j in range(Rstar.cols):
            value = sp.cancel(scale * Rstar[i, j])
            num, den = sp.fraction(sp.together(value))
            if den != 1:
                failures.append({"entry": f"{i},{j}", "denominator": sstr(den)})
            S[i, j] = sp.expand(num / den)
    meta = {
        "denominator_lcm": sstr(lcm),
        "positive_scale_used": "denominator_lcm^2",
        "scale": sstr(scale),
        "clearing_failures": failures[:8],
        "scale_note": "A square scale is nonnegative wherever denominators are nonzero; denominator factors still need domain nonvanishing for a final global certificate.",
    }
    return S, scale, meta


def leading_principal_minor_reports(S: sp.Matrix, vars_: tuple[sp.Symbol, ...], outdir: Path, seconds: int) -> list[dict[str, Any]]:
    reports = []
    remaining = seconds
    for k in range(1, S.rows + 1):
        started = time.time()
        item: dict[str, Any] = {"minor_size": k, "started_utc": now_utc()}
        try:
            with Alarm(max(1, remaining), f"minor {k} determinant"):
                detk = sp.cancel(S[:k, :k].det(method="bareiss"))
            item["determinant_status"] = "computed"
            atomic_text(outdir / f"minor_{k}_det.txt", sstr(detk) + "\n")
            num, den = sp.fraction(sp.together(detk))
            P = sp.Poly(sp.expand(num), *vars_)
            item["stats"] = {
                "denominator": sstr(den),
                "terms": len(P.terms()),
                "total_degree": P.total_degree(),
                "degrees": {str(v): P.degree(v) for v in vars_},
            }
            factor_seconds = max(1, min(remaining - int(time.time() - started), max(10, remaining // 2)))
            try:
                with Alarm(factor_seconds, f"minor {k} factorization"):
                    factored = sp.factor(num)
                    flist = sp.factor_list(num)
                item["factor_status"] = "computed"
                item["factored"] = sstr(factored)
                item["factor_list"] = {
                    "content": sstr(flist[0]),
                    "factors": [{"factor": sstr(f), "multiplicity": m} for f, m in flist[1]],
                }
                atomic_text(outdir / f"minor_{k}_factored.txt", sstr(factored) + "\n")
            except StageTimeout as exc:
                item["factor_status"] = "timeout"
                item["factor_error"] = str(exc)
        except StageTimeout as exc:
            item["determinant_status"] = "timeout"
            item["determinant_error"] = str(exc)
            reports.append(item)
            atomic_json(outdir / "principal_minor_reports.json", reports)
            break
        item["elapsed_seconds"] = round(time.time() - started, 3)
        reports.append(item)
        atomic_json(outdir / "principal_minor_reports.json", reports)
        remaining -= max(1, int(time.time() - started))
        if remaining <= 1:
            break
    return reports


def positive_orthant_certificate(poly: sp.Expr, vars_: tuple[sp.Symbol, ...], seconds: int) -> dict[str, Any]:
    repl_symbols = sp.symbols("X0:%d" % len(vars_))
    subs = {}
    for old, new in zip(vars_, repl_symbols):
        if str(old) == "u":
            subs[old] = new / (1 + new)
        else:
            subs[old] = (new - 1) / (new + 1)
    with Alarm(seconds, "positive orthant transform"):
        transformed = sp.together(poly.subs(subs))
        num, den = sp.fraction(transformed)
        P = sp.Poly(sp.expand(num), *repl_symbols)
        coeffs = P.coeffs()
        all_positive = all(c > 0 for c in coeffs)
        all_negative = all(c < 0 for c in coeffs)
        return {
            "substitution": {
                str(old): sstr(subs[old])
                for old in vars_
            },
            "denominator": sstr(den),
            "terms": len(coeffs),
            "total_degree": P.total_degree(),
            "all_coefficients_positive": all_positive,
            "all_coefficients_negative": all_negative,
            "min_coefficient": sstr(min(coeffs)) if coeffs else "0",
            "max_coefficient": sstr(max(coeffs)) if coeffs else "0",
        }


def candidate_points() -> list[dict[str, str]]:
    vals = [sp.Rational(-1, 2), sp.Rational(0), sp.Rational(1, 2)]
    us = [sp.Rational(1, 3), sp.Rational(2, 3)]
    pts = []
    for mu, nu, r, u in itertools.product(vals, vals, vals, us):
        pts.append({"mu": sstr(mu), "nu": sstr(nu), "r": sstr(r), "u": sstr(u)})
        if len(pts) >= 54:
            break
    return pts


def exact_candidate_probe(M: sp.Matrix, model: Model, outdir: Path, seconds: int) -> dict[str, Any]:
    points = candidate_points()
    manifest = {
        "purpose": "bounded exact rational probe for possible negative M directions after determinant work stalls",
        "count": len(points),
        "seed": "deterministic grid: mu,nu,r in {-1/2,0,1/2}, u in {1/3,2/3}",
        "points": points,
        "direction_recovery": "only if exact matrix tests indicate indefiniteness; rational vector must be checked exactly",
        "created_utc": now_utc(),
    }
    atomic_json(outdir / "candidate_probe_manifest.json", manifest)

    results = []
    found = None
    zvars = list(model.zvars)
    simple_dirs = []
    for i in range(6):
        e = [sp.S.Zero] * 6
        e[i] = sp.S.One
        simple_dirs.append(e)
    for i in range(6):
        for j in range(i + 1, 6):
            for sgn in [1, -1]:
                e = [sp.S.Zero] * 6
                e[i] = sp.S.One
                e[j] = sp.Integer(sgn)
                simple_dirs.append(e)

    with Alarm(seconds, "candidate probe"):
        for p in points:
            subs = {
                model.mu: sp.Rational(p["mu"]),
                model.nu: sp.Rational(p["nu"]),
                model.r: sp.Rational(p["r"]),
                model.u: sp.Rational(p["u"]),
            }
            Mp = sp.Matrix([[sp.cancel(M[i, j].subs(subs)) for j in range(6)] for i in range(6)])
            min_diag = min(Mp[i, i] for i in range(6))
            witness = None
            for d in simple_dirs:
                z = sp.Matrix(d)
                val = sp.cancel((z.T * Mp * z)[0])
                if val < 0:
                    witness = {"zeta": [sstr(x) for x in d], "value": sstr(val)}
                    found = {"point": p, "witness": witness}
                    break
            results.append({"point": p, "min_diagonal": sstr(min_diag), "simple_direction_negative": witness})
            if found:
                break
    out = {"created_utc": now_utc(), "results": results, "found_exact_negative": found}
    atomic_json(outdir / "candidate_probe_results.json", out)
    return out


def factor_case(case: str, outdir: Path, wall_seconds: int) -> dict[str, Any]:
    started = time.time()
    outdir.mkdir(parents=True, exist_ok=True)
    model = build_model()
    N, vars_, scale = clear_matrix_for_case(model, case)
    if case == "r0":
        N = sp.Matrix([[sp.expand(e) for e in row] for row in N.tolist()])
    report: dict[str, Any] = {
        "case": case,
        "started_utc": now_utc(),
        "environment": sympy_env(),
        "common_scale": sstr(scale),
        "variables": [str(v) for v in vars_],
        "denominator_positive_argument": {
            "J": "1-u^4 > 0 for 0<u<1",
            "L": "1-r^2*u^4 > 0 for -1<r<1 and 0<u<1",
            "scale": "positive scalar multiplying all matrix entries; det(M) has the same sign as det(scaled M)",
        },
        "positive_seed": positive_seed_report(model.M, model, case),
    }
    atomic_json(outdir / f"{case}_stage_start.json", report)

    denom_failures = []
    for i in range(6):
        for j in range(6):
            num, den = sp.fraction(sp.together(N[i, j]))
            if den != 1:
                denom_failures.append({"entry": f"{i},{j}", "den": sstr(den)})
    report["cleared_entries_are_polynomial"] = not denom_failures
    report["clearing_failures"] = denom_failures[:8]
    report["scaled_matrix_upper_triangle"] = [
        {"entry": [i + 1, j + 1], "polynomial": sstr(N[i, j])}
        for i in range(6)
        for j in range(i, 6)
    ]
    report["scaled_entry_degrees"] = matrix_degree_bounds(N, vars_)
    report["determinant_degree_bound_before_extraction"] = determinant_degree_bound(N, vars_)
    atomic_json(outdir / f"{case}_pre_det.json", report)

    reduced, extraction = extract_row_col_factors(N, vars_, model)
    report["raw6_row_column_extraction_checkpoint"] = extraction
    report["raw6_reduced_entry_degrees"] = matrix_degree_bounds(reduced, vars_)
    report["raw6_determinant_degree_bound_after_extraction"] = determinant_degree_bound(reduced, vars_)
    report["raw6_determinant_not_attempted"] = "The structure reduction was used before any raw 6x6 determinant, per C2 scope."
    atomic_json(outdir / f"{case}_after_raw6_extraction_checkpoint.json", report)

    structure = structure_reduction(model, case)
    Rstar = structure.pop("Rstar")
    report["structure_reduction"] = structure
    if not all(structure["checks"].values()):
        report["structure_status"] = "failed"
        atomic_json(outdir / f"{case}_factor_report.json", report)
        raise RuntimeError(f"{case} structure reduction checks failed")
    report["structure_status"] = "ok"
    S4, scale4, clear_meta = clear_rstar_by_square_lcm(Rstar, vars_)
    report["Rstar_clearing"] = clear_meta
    report["Rstar_scaled_matrix_upper_triangle"] = [
        {"entry": [i + 1, j + 1], "polynomial": sstr(S4[i, j])}
        for i in range(4)
        for j in range(i, 4)
    ]
    report["Rstar_scaled_entry_degrees"] = matrix_degree_bounds(S4, vars_)
    report["Rstar_determinant_degree_bound"] = determinant_degree_bound(S4, vars_)
    atomic_json(outdir / f"{case}_Rstar_pre_minors.json", report)

    remaining = max(1, wall_seconds - int(time.time() - started) - 10)
    det_seconds = max(1, min(remaining, wall_seconds))
    try:
        minor_reports = leading_principal_minor_reports(S4, vars_, outdir, det_seconds)
        report["Rstar_principal_minor_reports"] = minor_reports
        if len(minor_reports) == 4 and all(x.get("determinant_status") == "computed" for x in minor_reports):
            report["determinant_status"] = "Rstar_all_leading_principal_minors_computed"
        else:
            report["determinant_status"] = "Rstar_principal_minor_timeout_or_partial"

        if minor_reports and minor_reports[-1].get("determinant_status") == "computed":
            last_det_path = outdir / f"minor_{minor_reports[-1]['minor_size']}_det.txt"
            if last_det_path.exists():
                num, _den = sp.fraction(sp.together(sp.sympify(last_det_path.read_text(encoding="utf-8").strip())))
                cert_seconds = max(1, min(120, wall_seconds - int(time.time() - started) - 10))
                if cert_seconds > 5:
                    try:
                        report["positive_orthant_certificate_attempt_last_minor"] = positive_orthant_certificate(num, vars_, cert_seconds)
                    except StageTimeout as exc:
                        report["positive_orthant_certificate_attempt_last_minor"] = {"status": "timeout", "error": str(exc)}
                    except Exception as exc:
                        report["positive_orthant_certificate_attempt_last_minor"] = {"status": "error", "error": repr(exc)}
    except StageTimeout as exc:
        report["determinant_status"] = "timeout"
        report["determinant_error"] = str(exc)

    remaining = wall_seconds - int(time.time() - started) - 5
    if case == "full" and report.get("determinant_status") != "Rstar_all_leading_principal_minors_computed" and remaining > 30:
        try:
            report["candidate_probe"] = exact_candidate_probe(model.M, model, outdir, min(120, remaining))
        except StageTimeout as exc:
            report["candidate_probe"] = {"status": "timeout", "error": str(exc)}
        except Exception as exc:
            report["candidate_probe"] = {"status": "error", "error": repr(exc), "traceback": traceback.format_exc()}

    report["finished_utc"] = now_utc()
    report["elapsed_seconds"] = round(time.time() - started, 3)
    atomic_json(outdir / f"{case}_factor_report.json", report)
    return report


def run_all(outdir: Path, wall_seconds: int, r0_seconds: int) -> dict[str, Any]:
    started = time.time()
    outdir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "started_utc": now_utc(),
        "wall_seconds": wall_seconds,
        "r0_seconds_target": r0_seconds,
        "process_pid": os.getpid(),
        "single_process_contract": "derive, r=0, and full-r run sequentially in this one Python process",
        "environment": sympy_env(),
    }
    atomic_json(outdir / "run_manifest.json", manifest)

    result: dict[str, Any] = {"manifest": manifest, "stages": []}
    derive_path = outdir / "lambda_zero_M.json"
    try:
        result["derive"] = derive(derive_path)
        result["stages"].append({"name": "derive", "status": "ok", "elapsed_since_start": round(time.time() - started, 3)})
    except Exception as exc:
        result["derive_error"] = {"error": repr(exc), "traceback": traceback.format_exc()}
        result["finished_utc"] = now_utc()
        result["elapsed_seconds"] = round(time.time() - started, 3)
        atomic_json(outdir / "run_final.json", result)
        raise

    elapsed = int(time.time() - started)
    r0_budget = max(1, min(r0_seconds, wall_seconds - elapsed - 30))
    if r0_budget > 1:
        try:
            result["r0"] = factor_case("r0", outdir / "r0", r0_budget)
            result["stages"].append({"name": "r0", "status": result["r0"].get("determinant_status"), "elapsed_since_start": round(time.time() - started, 3)})
        except Exception as exc:
            result["r0_error"] = {"error": repr(exc), "traceback": traceback.format_exc()}
            result["stages"].append({"name": "r0", "status": "error", "elapsed_since_start": round(time.time() - started, 3)})

    elapsed = int(time.time() - started)
    full_budget = max(1, wall_seconds - elapsed - 10)
    if full_budget > 1:
        try:
            result["full"] = factor_case("full", outdir / "full", full_budget)
            result["stages"].append({"name": "full", "status": result["full"].get("determinant_status"), "elapsed_since_start": round(time.time() - started, 3)})
        except Exception as exc:
            result["full_error"] = {"error": repr(exc), "traceback": traceback.format_exc()}
            result["stages"].append({"name": "full", "status": "error", "elapsed_since_start": round(time.time() - started, 3)})

    result["finished_utc"] = now_utc()
    result["elapsed_seconds"] = round(time.time() - started, 3)
    atomic_json(outdir / "run_final.json", result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["derive", "factor", "all"], required=True)
    parser.add_argument("--case", choices=["r0", "full"], default="r0")
    parser.add_argument("--output", type=Path, default=Path("lambda_zero_M.json"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    parser.add_argument("--wall-seconds", type=int, default=2700)
    parser.add_argument("--r0-seconds", type=int, default=600)
    args = parser.parse_args()

    if args.mode == "derive":
        derive(args.output)
    elif args.mode == "factor":
        factor_case(args.case, args.output_dir / args.case, args.wall_seconds)
    elif args.mode == "all":
        run_all(args.output_dir, args.wall_seconds, args.r0_seconds)


if __name__ == "__main__":
    main()
