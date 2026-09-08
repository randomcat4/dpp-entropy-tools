"""Exact algebraic construction for FT-B path-affine K chords.

This script works only inside the D10-B route directory.  It constructs
explicit rational triples of SPD tridiagonal L matrices such that

    Phi(L0) = (Phi(Lminus) + Phi(Lplus)) / 2,
    Phi(L) = L (I+L)^(-1).

The construction uses S=(I+L)^(-1).  If

    S(tau) = R^{-1} diag(tau) R^{-T}

with a fixed unit lower-bidiagonal R, then S is affine in tau, while

    I+L(tau) = S(tau)^(-1) = R^T diag(1/tau) R

is tridiagonal.  Hence tau0=(taum+taup)/2 gives an exact K-space midpoint.

For n<=8, the script also calls the existing NS-1 path_schur direct Mobius
validator after disabling bytecode writes, so the read-only dependency is not
modified.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
from typing import Iterable, Sequence


sys.dont_write_bytecode = True
os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")

Matrix = list[list[Fraction]]


def q(text: str | int | Fraction) -> Fraction:
    return text if isinstance(text, Fraction) else Fraction(text)


def frac_json(x):
    if isinstance(x, Fraction):
        return f"{x.numerator}/{x.denominator}"
    if isinstance(x, Decimal):
        return str(x)
    if isinstance(x, list):
        return [frac_json(v) for v in x]
    if isinstance(x, tuple):
        return [frac_json(v) for v in x]
    if isinstance(x, dict):
        return {k: frac_json(v) for k, v in x.items()}
    return x


def zeros(n: int, m: int) -> Matrix:
    return [[Fraction(0) for _ in range(m)] for _ in range(n)]


def eye(n: int) -> Matrix:
    return [[Fraction(i == j) for j in range(n)] for i in range(n)]


def mat_add(a: Matrix, b: Matrix) -> Matrix:
    return [[x + y for x, y in zip(row_a, row_b)] for row_a, row_b in zip(a, b)]


def mat_sub(a: Matrix, b: Matrix) -> Matrix:
    return [[x - y for x, y in zip(row_a, row_b)] for row_a, row_b in zip(a, b)]


def mat_scale(a: Matrix, c: Fraction) -> Matrix:
    return [[c * x for x in row] for row in a]


def mat_mul(a: Matrix, b: Matrix) -> Matrix:
    bt = list(zip(*b))
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def transpose(a: Matrix) -> Matrix:
    return [list(row) for row in zip(*a)]


def det_bareiss(a: Matrix) -> Fraction:
    n = len(a)
    if n == 0:
        return Fraction(1)
    m = [row[:] for row in a]
    sign = Fraction(1)
    previous = Fraction(1)
    for k in range(n - 1):
        pivot = None
        for i in range(k, n):
            if m[i][k] != 0:
                pivot = i
                break
        if pivot is None:
            return Fraction(0)
        if pivot != k:
            m[k], m[pivot] = m[pivot], m[k]
            sign = -sign
        pivot_value = m[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                m[i][j] = (m[i][j] * pivot_value - m[i][k] * m[k][j]) / previous
        previous = pivot_value
        for i in range(k + 1, n):
            m[i][k] = Fraction(0)
    return sign * m[n - 1][n - 1]


def inverse(a: Matrix) -> Matrix:
    n = len(a)
    aug = [row[:] + ident[:] for row, ident in zip(a, eye(n))]
    for k in range(n):
        pivot = None
        for i in range(k, n):
            if aug[i][k] != 0:
                pivot = i
                break
        if pivot is None:
            raise ValueError("singular matrix")
        if pivot != k:
            aug[k], aug[pivot] = aug[pivot], aug[k]
        scale = aug[k][k]
        aug[k] = [x / scale for x in aug[k]]
        for i in range(n):
            if i == k:
                continue
            factor = aug[i][k]
            if factor:
                aug[i] = [x - factor * y for x, y in zip(aug[i], aug[k])]
    return [row[n:] for row in aug]


def rank_fraction(a: Matrix) -> int:
    m = [row[:] for row in a]
    rows = len(m)
    cols = 0 if rows == 0 else len(m[0])
    rank = 0
    for col in range(cols):
        pivot = None
        for i in range(rank, rows):
            if m[i][col] != 0:
                pivot = i
                break
        if pivot is None:
            continue
        if pivot != rank:
            m[rank], m[pivot] = m[pivot], m[rank]
        scale = m[rank][col]
        m[rank] = [x / scale for x in m[rank]]
        for i in range(rows):
            if i == rank:
                continue
            factor = m[i][col]
            if factor:
                m[i] = [x - factor * y for x, y in zip(m[i], m[rank])]
        rank += 1
        if rank == rows:
            break
    return rank


def leading_principal_minors(a: Matrix) -> list[Fraction]:
    return [det_bareiss([row[:k] for row in a[:k]]) for k in range(1, len(a) + 1)]


def leading_continuants(diagonal: Sequence[Fraction], edge: Sequence[Fraction]) -> list[Fraction]:
    if not diagonal:
        return []
    out = [diagonal[0]]
    previous2 = Fraction(1)
    previous1 = diagonal[0]
    for i in range(1, len(diagonal)):
        current = diagonal[i] * previous1 - edge[i - 1] ** 2 * previous2
        out.append(current)
        previous2, previous1 = previous1, current
    return out


def lower_bidiagonal_r(beta: Sequence[Fraction]) -> Matrix:
    n = len(beta) + 1
    r = eye(n)
    for i, b in enumerate(beta, start=1):
        r[i][i - 1] = -b
    return r


def lower_bidiagonal_inverse(beta: Sequence[Fraction]) -> Matrix:
    n = len(beta) + 1
    t = zeros(n, n)
    for i in range(n):
        t[i][i] = Fraction(1)
        prod = Fraction(1)
        for j in range(i - 1, -1, -1):
            prod *= beta[j]
            t[i][j] = prod
    return t


def covariance_from_innovations(beta: Sequence[Fraction], tau: Sequence[Fraction]) -> Matrix:
    n = len(tau)
    if len(beta) != n - 1:
        raise ValueError("beta length must be n-1")
    t = lower_bidiagonal_inverse(beta)
    diag_tau = zeros(n, n)
    for i, value in enumerate(tau):
        diag_tau[i][i] = value
    return mat_mul(mat_mul(t, diag_tau), transpose(t))


def precision_from_innovations(beta: Sequence[Fraction], tau: Sequence[Fraction]) -> Matrix:
    n = len(tau)
    if len(beta) != n - 1:
        raise ValueError("beta length must be n-1")
    r = lower_bidiagonal_r(beta)
    w = zeros(n, n)
    for i, value in enumerate(tau):
        w[i][i] = 1 / value
    return mat_mul(mat_mul(transpose(r), w), r)


def tridiagonal_parts(a: Matrix) -> tuple[list[Fraction], list[Fraction]]:
    n = len(a)
    diagonal = [a[i][i] for i in range(n)]
    edge = [a[i][i + 1] for i in range(n - 1)]
    return diagonal, edge


def is_tridiagonal(a: Matrix) -> bool:
    n = len(a)
    return all(a[i][j] == 0 for i in range(n) for j in range(n) if abs(i - j) > 1)


def all_positive(values: Iterable[Fraction]) -> bool:
    return all(x > 0 for x in values)


def load_path_schur():
    here = Path(__file__).resolve()
    sparse_dir = here.parents[2] / "next_structures" / "sparse_schur"
    module_path = sparse_dir / "path_schur.py"
    spec = importlib.util.spec_from_file_location("d10b_readonly_path_schur", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, module_path


def entropy_gap(path_schur, triples: dict[str, dict[str, object]], precision: int) -> dict[str, object]:
    with localcontext() as ctx:
        ctx.prec = precision
        hm = triples["minus"]["entropy"]
        h0 = triples["zero"]["entropy"]
        hp = triples["plus"]["entropy"]
        return {
            "delta_endpoint_average_minus_midpoint": +((hm + hp) / Decimal(2) - h0),
            "sign_is_only_decimal_scout": True,
            "strict_positive_gap_certified": False,
        }


def analyze_case(name: str, beta_raw: Sequence[str], tau_minus_raw: Sequence[str], tau_plus_raw: Sequence[str], precision: int) -> dict[str, object]:
    beta = [q(x) for x in beta_raw]
    tau_minus = [q(x) for x in tau_minus_raw]
    tau_plus = [q(x) for x in tau_plus_raw]
    if len(tau_minus) != len(tau_plus):
        raise ValueError("tau endpoints must have same length")
    tau_zero = [(a + b) / 2 for a, b in zip(tau_minus, tau_plus)]
    n = len(tau_zero)

    path_schur, module_path = load_path_schur()

    by_point: dict[str, dict[str, object]] = {}
    s_mats: dict[str, Matrix] = {}
    k_mats: dict[str, Matrix] = {}
    l_mats: dict[str, Matrix] = {}

    for label, tau in [("minus", tau_minus), ("zero", tau_zero), ("plus", tau_plus)]:
        s = covariance_from_innovations(beta, tau)
        p = precision_from_innovations(beta, tau)
        l = mat_sub(p, eye(n))
        k = mat_sub(eye(n), s)
        k_from_l = path_schur.k_from_l(l)
        diag, edge = tridiagonal_parts(l)
        leading_l = leading_continuants(diag, edge)
        direct = path_schur.direct_validation_case(diag, edge, precision=precision)
        entropy = path_schur.path_entropy_dp(diag, edge, precision=precision)["entropy"]

        s_mats[label] = s
        k_mats[label] = k
        l_mats[label] = l

        by_point[label] = {
            "tau": tau,
            "L_diagonal": diag,
            "L_edge": edge,
            "L_matrix": l,
            "K_matrix": k,
            "P_equals_inverse_S": mat_mul(p, s) == eye(n),
            "Phi_L_equals_I_minus_S": k_from_l == k,
            "tridiagonal": is_tridiagonal(l),
            "connected_nonzero_adjacent_edges": all(e != 0 for e in edge),
            "heterogeneous_diagonal": len(set(diag)) > 1,
            "L_leading_minors": leading_l,
            "L_spd_by_sylvester": all_positive(leading_l),
            "S_leading_minors": leading_principal_minors(s),
            "S_spd_by_sylvester": all_positive(leading_principal_minors(s)),
            "entropy": entropy,
            "direct_mobius_validation": direct,
        }

    k_midpoint = mat_scale(mat_add(k_mats["minus"], k_mats["plus"]), Fraction(1, 2))
    s_midpoint = mat_scale(mat_add(s_mats["minus"], s_mats["plus"]), Fraction(1, 2))
    l_midpoint_linear = mat_scale(mat_add(l_mats["minus"], l_mats["plus"]), Fraction(1, 2))
    k_diff = mat_sub(k_mats["plus"], k_mats["minus"])
    s_diff = mat_sub(s_mats["plus"], s_mats["minus"])

    result = {
        "name": name,
        "n": n,
        "construction": "fixed-beta Gaussian-Markov covariance S(tau)=R^{-1}diag(tau)R^{-T}; L(tau)=S(tau)^(-1)-I",
        "beta": beta,
        "tau_minus": tau_minus,
        "tau_zero": tau_zero,
        "tau_plus": tau_plus,
        "shared_path_schur_dependency": str(module_path),
        "K_midpoint_identity_exact": k_mats["zero"] == k_midpoint,
        "S_midpoint_identity_exact": s_mats["zero"] == s_midpoint,
        "L_zero_is_endpoint_average": l_mats["zero"] == l_midpoint_linear,
        "not_an_L_line": l_mats["zero"] != l_midpoint_linear,
        "K_plus_minus_K_minus_rank_exact": rank_fraction(k_diff),
        "S_plus_minus_S_minus_rank_exact": rank_fraction(s_diff),
        "all_points_pass_FT_B_shape": all(
            by_point[label]["tridiagonal"]
            and by_point[label]["connected_nonzero_adjacent_edges"]
            and by_point[label]["heterogeneous_diagonal"]
            and by_point[label]["L_spd_by_sylvester"]
            for label in ("minus", "zero", "plus")
        ),
        "all_direct_mobius_validations_pass": all(
            by_point[label]["direct_mobius_validation"]["mismatch_count"] == 0
            and by_point[label]["direct_mobius_validation"]["mobius_sum"] == Fraction(1)
            and by_point[label]["direct_mobius_validation"]["l_ensemble_sum"] == Fraction(1)
            for label in ("minus", "zero", "plus")
        ),
        "points": by_point,
    }
    result["entropy_gap"] = entropy_gap(path_schur, by_point, precision=precision)
    return result


def build_evidence(precision: int) -> dict[str, object]:
    cases = [
        analyze_case(
            "n3_exact_markov_chord",
            beta_raw=["1/3", "-2/5"],
            tau_minus_raw=["1/40", "1/45", "1/50"],
            tau_plus_raw=["1/55", "1/35", "1/60"],
            precision=precision,
        ),
        analyze_case(
            "n4_exact_markov_chord",
            beta_raw=["1/4", "-1/3", "2/7"],
            tau_minus_raw=["1/30", "1/36", "1/42", "1/48"],
            tau_plus_raw=["1/45", "1/33", "1/55", "1/39"],
            precision=precision,
        ),
    ]
    return {
        "status": "PASS" if all(c["K_midpoint_identity_exact"] and c["all_points_pass_FT_B_shape"] and c["all_direct_mobius_validations_pass"] for c in cases) else "FAIL",
        "precision_decimal_digits": precision,
        "scope": "explicit exact rational FT-B triples for n=3 and n=4; not an exhaustive nonexistence theorem",
        "prior_art_blocker": {
            "source_as_given_by_parent": "https://sevenkplus.com/data/dpp.pdf",
            "claim_recorded_not_reproved": "Gu, Theorem 7 / Corollary 6: K-space rank-one directions and chords from 0 to K are concavity directions.",
            "relevance": "the constructed perturbations have rank n, not rank 1, so they are not excluded by the rank-one blocker; no chord-to-origin claim is made.",
        },
        "denominator_of_attempts": [
            "Exact fixed-beta innovation family tried for n=3 and n=4: succeeds for FT-B closure.",
            "No exhaustive finite search was run.",
            "No attempt is made here to certify a positive entropy gap; Decimal gaps are scout-only.",
        ],
        "cases": cases,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path(__file__).with_name("evidence.json"))
    parser.add_argument("--precision", type=int, default=100)
    args = parser.parse_args()
    evidence = frac_json(build_evidence(args.precision))
    text = json.dumps(evidence, indent=2, ensure_ascii=False)
    args.out.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
