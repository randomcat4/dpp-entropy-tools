#!/usr/bin/env python3
"""Independent exact-arithmetic review for N4 DPP entropy candidates."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import os
import platform
import subprocess
import sys
import time
from dataclasses import dataclass
from decimal import Decimal, localcontext
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable


DEFAULT_LOG_TERMS = (80, 120, 180, 260, 380, 560, 820, 1200)

try:
    sys.set_int_max_str_digits(0)
except AttributeError:
    pass


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def git_head() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL
        ).strip()
    except Exception:
        return "UNKNOWN"


def decimal_to_fraction(x: Any) -> Fraction:
    if isinstance(x, Fraction):
        return x
    if isinstance(x, int):
        return Fraction(x, 1)
    if isinstance(x, Decimal):
        return Fraction(x)
    if isinstance(x, str):
        return Fraction(Decimal(x))
    if isinstance(x, float):
        return Fraction(Decimal(repr(x)))
    raise TypeError(f"cannot convert {type(x).__name__} to Fraction")


def fraction_to_decimal_string(q: Fraction, digits: int = 48) -> str:
    if q.denominator == 1:
        return str(q.numerator)
    with localcontext() as ctx:
        ctx.prec = digits
        return format(Decimal(q.numerator) / Decimal(q.denominator), "f")


def fraction_to_string(q: Fraction) -> str:
    if q.denominator == 1:
        return str(q.numerator)
    return f"{q.numerator}/{q.denominator}"


def fraction_obj(q: Fraction, digits: int = 48, full_digit_limit: int = 240) -> dict[str, Any]:
    num_s = str(q.numerator)
    den_s = str(q.denominator)
    rep = num_s if q.denominator == 1 else f"{num_s}/{den_s}"
    base: dict[str, Any] = {
        "decimal": fraction_to_decimal_string(q, digits),
        "sign": (q > 0) - (q < 0),
        "num_digits": len(num_s.lstrip("-")),
        "den_digits": len(den_s),
        "fraction_sha256": hashlib.sha256(rep.encode("ascii")).hexdigest(),
    }
    if base["num_digits"] <= full_digit_limit and base["den_digits"] <= full_digit_limit:
        base["num"] = q.numerator
        base["den"] = q.denominator
    else:
        base["exact_fraction_omitted"] = "too_large_reproducible_from_script_terms"
    return base


def interval_obj(lo: Fraction, hi: Fraction, digits: int = 48) -> dict[str, Any]:
    return {
        "lower": fraction_obj(lo, digits),
        "upper": fraction_obj(hi, digits),
        "width": fraction_obj(hi - lo, digits),
    }


def matrix_to_strings(M: list[list[Fraction]]) -> list[list[str]]:
    return [[fraction_to_string(x) for x in row] for row in M]


def max_denominator_matrix(M: list[list[Fraction]]) -> int:
    return max((x.denominator for row in M for x in row), default=1)


def ensure_square_matrix(raw: Any, name: str) -> list[list[Fraction]]:
    if not isinstance(raw, list) or not raw:
        raise ValueError(f"{name} is not a nonempty matrix")
    n = len(raw)
    out: list[list[Fraction]] = []
    for row in raw:
        if not isinstance(row, list) or len(row) != n:
            raise ValueError(f"{name} is not square")
        out.append([decimal_to_fraction(x) for x in row])
    return out


@dataclass
class SymRationalization:
    matrix: list[list[Fraction]]
    max_abs_source_error: Fraction
    max_pair_asymmetry: Fraction
    max_denominator: int


def rationalize_symmetric_matrix(
    raw: Any, name: str, max_denominator: int
) -> SymRationalization:
    exact = ensure_square_matrix(raw, name)
    n = len(exact)
    M = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    max_error = Fraction(0)
    max_asym = Fraction(0)
    for i in range(n):
        for j in range(i, n):
            if i == j:
                center = exact[i][i]
                q = center.limit_denominator(max_denominator)
                max_error = max(max_error, abs(q - exact[i][i]))
                M[i][i] = q
            else:
                a = exact[i][j]
                b = exact[j][i]
                max_asym = max(max_asym, abs(a - b))
                center = (a + b) / 2
                q = center.limit_denominator(max_denominator)
                max_error = max(max_error, abs(q - a), abs(q - b))
                M[i][j] = q
                M[j][i] = q
    return SymRationalization(M, max_error, max_asym, max_denominator_matrix(M))


def rationalize_scalar(raw: Any, max_denominator: int) -> tuple[Fraction, Fraction]:
    exact = decimal_to_fraction(raw)
    q = exact.limit_denominator(max_denominator)
    return q, abs(q - exact)


def eye(n: int) -> list[list[Fraction]]:
    return [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]


def mat_add(A: list[list[Fraction]], B: list[list[Fraction]]) -> list[list[Fraction]]:
    n = len(A)
    return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]


def mat_sub(A: list[list[Fraction]], B: list[list[Fraction]]) -> list[list[Fraction]]:
    n = len(A)
    return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]


def mat_scale(c: Fraction, A: list[list[Fraction]]) -> list[list[Fraction]]:
    n = len(A)
    return [[c * A[i][j] for j in range(n)] for i in range(n)]


def det_fraction(A: list[list[Fraction]]) -> Fraction:
    n = len(A)
    M = [[Fraction(x) for x in row] for row in A]
    det = Fraction(1)
    for col in range(n):
        pivot = None
        for row in range(col, n):
            if M[row][col] != 0:
                pivot = row
                break
        if pivot is None:
            return Fraction(0)
        if pivot != col:
            M[col], M[pivot] = M[pivot], M[col]
            det = -det
        p = M[col][col]
        det *= p
        for row in range(col + 1, n):
            if M[row][col] == 0:
                continue
            factor = M[row][col] / p
            for j in range(col, n):
                M[row][j] -= factor * M[col][j]
    return det


def leading_principal(A: list[list[Fraction]], k: int) -> list[list[Fraction]]:
    return [[A[i][j] for j in range(k)] for i in range(k)]


def sylvester_report(A: list[list[Fraction]]) -> dict[str, Any]:
    minors = [det_fraction(leading_principal(A, k)) for k in range(1, len(A) + 1)]
    return {
        "ok": all(x > 0 for x in minors),
        "leading_principal_minors": [fraction_obj(x) for x in minors],
        "min_minor_decimal": fraction_to_decimal_string(min(minors), 48),
    }


def feasibility_report(
    K: list[list[Fraction]], D: list[list[Fraction]], t: Fraction
) -> dict[str, Any]:
    n = len(K)
    I = eye(n)
    K_minus = mat_sub(K, mat_scale(t, D))
    K_plus = mat_add(K, mat_scale(t, D))
    matrices = {
        "K": K,
        "I_minus_K": mat_sub(I, K),
        "K_minus_tD": K_minus,
        "I_minus_K_minus_tD": mat_sub(I, K_minus),
        "K_plus_tD": K_plus,
        "I_minus_K_plus_tD": mat_sub(I, K_plus),
    }
    reports = {name: sylvester_report(M) for name, M in matrices.items()}
    return {
        "strict_open_domain": all(rep["ok"] for rep in reports.values()),
        "checks": reports,
    }


def event_matrix(K: list[list[Fraction]], S_mask: int) -> list[list[Fraction]]:
    n = len(K)
    A = [[K[i][j] for j in range(n)] for i in range(n)]
    for i in range(n):
        if not (S_mask >> i) & 1:
            A[i][i] -= 1
    return A


def event_probability(K: list[list[Fraction]], S_mask: int) -> Fraction:
    n = len(K)
    sign = -1 if (n - S_mask.bit_count()) % 2 else 1
    return sign * det_fraction(event_matrix(K, S_mask))


def event_probabilities(K: list[list[Fraction]]) -> list[Fraction]:
    return [event_probability(K, mask) for mask in range(1 << len(K))]


def permutation_sign(perm: tuple[int, ...]) -> int:
    inv = 0
    for i in range(len(perm)):
        for j in range(i + 1, len(perm)):
            inv += perm[i] > perm[j]
    return -1 if inv % 2 else 1


def poly_add(a: list[Fraction], b: list[Fraction]) -> list[Fraction]:
    n = max(len(a), len(b))
    out = [Fraction(0) for _ in range(n)]
    for i in range(n):
        if i < len(a):
            out[i] += a[i]
        if i < len(b):
            out[i] += b[i]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def poly_mul(a: list[Fraction], b: list[Fraction]) -> list[Fraction]:
    out = [Fraction(0) for _ in range(len(a) + len(b) - 1)]
    for i, av in enumerate(a):
        if av == 0:
            continue
        for j, bv in enumerate(b):
            if bv:
                out[i + j] += av * bv
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def det_linear_poly(A0: list[list[Fraction]], A1: list[list[Fraction]]) -> list[Fraction]:
    n = len(A0)
    total = [Fraction(0)]
    for perm in itertools.permutations(range(n)):
        term = [Fraction(permutation_sign(perm))]
        for i, j in enumerate(perm):
            term = poly_mul(term, [A0[i][j], A1[i][j]])
        total = poly_add(total, term)
    return total


def event_probability_poly(
    K: list[list[Fraction]], D: list[list[Fraction]], S_mask: int
) -> list[Fraction]:
    n = len(K)
    sign = Fraction(-1 if (n - S_mask.bit_count()) % 2 else 1)
    A0 = event_matrix(K, S_mask)
    coeffs = det_linear_poly(A0, D)
    return [sign * c for c in coeffs]


def event_jets(K: list[list[Fraction]], D: list[list[Fraction]]) -> list[dict[str, Any]]:
    rows = []
    for mask in range(1 << len(K)):
        coeffs = event_probability_poly(K, D, mask)
        p0 = coeffs[0] if len(coeffs) > 0 else Fraction(0)
        p1 = coeffs[1] if len(coeffs) > 1 else Fraction(0)
        p2 = 2 * coeffs[2] if len(coeffs) > 2 else Fraction(0)
        rows.append({"mask": mask, "p": p0, "dp": p1, "ddp": p2, "poly": coeffs})
    return rows


def pow2_fraction(k: int) -> Fraction:
    if k >= 0:
        return Fraction(1 << k, 1)
    return Fraction(1, 1 << (-k))


def reduced_log_argument(x: Fraction) -> tuple[int, Fraction]:
    if x <= 0:
        raise ValueError("log argument must be positive")
    k = x.numerator.bit_length() - x.denominator.bit_length()
    y = x / pow2_fraction(k)
    while y < 1:
        k -= 1
        y *= 2
    while y >= 2:
        k += 1
        y /= 2
    return k, y


@lru_cache(maxsize=None)
def log_y_interval_cached(num: int, den: int, terms: int) -> tuple[Fraction, Fraction]:
    y = Fraction(num, den)
    if y == 1:
        return Fraction(0), Fraction(0)
    if not (1 <= y <= 2):
        raise ValueError(f"reduced log argument outside [1,2]: {y}")
    u = (y - 1) / (y + 1)
    u2 = u * u
    power = u
    total = Fraction(0)
    for j in range(terms):
        if j > 0:
            power *= u2
        total += power / (2 * j + 1)
    lower = 2 * total
    tail_first = power * u2
    if tail_first == 0:
        return lower, lower
    tail_upper = 2 * tail_first / ((2 * terms + 1) * (1 - u2))
    return lower, lower + tail_upper


@lru_cache(maxsize=None)
def ln2_interval(terms: int) -> tuple[Fraction, Fraction]:
    return log_y_interval_cached(2, 1, terms)


@lru_cache(maxsize=None)
def log_interval_cached(num: int, den: int, terms: int) -> tuple[Fraction, Fraction]:
    x = Fraction(num, den)
    k, y = reduced_log_argument(x)
    l2, u2 = ln2_interval(terms)
    ly, uy = log_y_interval_cached(y.numerator, y.denominator, terms)
    if k >= 0:
        return k * l2 + ly, k * u2 + uy
    return k * u2 + ly, k * l2 + uy


def log_interval(x: Fraction, terms: int) -> tuple[Fraction, Fraction]:
    return log_interval_cached(x.numerator, x.denominator, terms)


def interval_scale(c: Fraction, lo: Fraction, hi: Fraction) -> tuple[Fraction, Fraction]:
    if c >= 0:
        return c * lo, c * hi
    return c * hi, c * lo


def entropy_interval_from_probs(
    probs: list[Fraction], terms: int
) -> tuple[Fraction, Fraction]:
    lo = Fraction(0)
    hi = Fraction(0)
    for p in probs:
        if p <= 0:
            raise ValueError(f"nonpositive event probability {p}")
        lp_lo, lp_hi = log_interval(p, terms)
        term_lo, term_hi = interval_scale(-p, lp_lo, lp_hi)
        lo += term_lo
        hi += term_hi
    return lo, hi


def entropy_gap_interval(
    K: list[list[Fraction]], D: list[list[Fraction]], t: Fraction, terms: int
) -> tuple[Fraction, Fraction, dict[str, Any]]:
    H0 = entropy_interval_from_probs(event_probabilities(K), terms)
    Hm = entropy_interval_from_probs(event_probabilities(mat_sub(K, mat_scale(t, D))), terms)
    Hp = entropy_interval_from_probs(event_probabilities(mat_add(K, mat_scale(t, D))), terms)
    lo = (Hm[0] + Hp[0]) / 2 - H0[1]
    hi = (Hm[1] + Hp[1]) / 2 - H0[0]
    detail = {"H0": interval_obj(*H0), "H_minus": interval_obj(*Hm), "H_plus": interval_obj(*Hp)}
    return lo, hi, detail


def hessian_interval(
    K: list[list[Fraction]], D: list[list[Fraction]], terms: int
) -> tuple[Fraction, Fraction, dict[str, Any]]:
    jets = event_jets(K, D)
    fisher = Fraction(0)
    lo = Fraction(0)
    hi = Fraction(0)
    sum_p = Fraction(0)
    sum_dp = Fraction(0)
    sum_ddp = Fraction(0)
    for row in jets:
        p = row["p"]
        dp = row["dp"]
        ddp = row["ddp"]
        if p <= 0:
            raise ValueError(f"nonpositive midpoint event probability at mask {row['mask']}: {p}")
        fisher -= dp * dp / p
        lp_lo, lp_hi = log_interval(p, terms)
        term_lo, term_hi = interval_scale(-ddp, lp_lo, lp_hi)
        lo += term_lo
        hi += term_hi
        sum_p += p
        sum_dp += dp
        sum_ddp += ddp
    lo += fisher
    hi += fisher
    return lo, hi, {
        "fisher_exact": fraction_obj(fisher),
        "sum_p": fraction_obj(sum_p),
        "sum_dp": fraction_obj(sum_dp),
        "sum_ddp": fraction_obj(sum_ddp),
        "jet_rows": [
            {
                "mask": format(row["mask"], f"0{len(K)}b"),
                "p": fraction_to_string(row["p"]),
                "dp": fraction_to_string(row["dp"]),
                "ddp": fraction_to_string(row["ddp"]),
            }
            for row in jets
        ],
    }


def gradient_directional_interval(
    K: list[list[Fraction]], D: list[list[Fraction]], terms: int
) -> tuple[Fraction, Fraction, dict[str, Any]]:
    jets = event_jets(K, D)
    lo = Fraction(0)
    hi = Fraction(0)
    sum_dp = Fraction(0)
    for row in jets:
        p = row["p"]
        dp = row["dp"]
        if p <= 0:
            raise ValueError(f"nonpositive event probability at mask {row['mask']}: {p}")
        lp_lo, lp_hi = log_interval(p, terms)
        term_lo, term_hi = interval_scale(-dp, lp_lo, lp_hi)
        lo += term_lo
        hi += term_hi
        sum_dp += dp
    return lo, hi, {"sum_dp": fraction_obj(sum_dp)}


def adaptive_interval(
    kind: str,
    K: list[list[Fraction]],
    D: list[list[Fraction]],
    t: Fraction | None,
    schedule: Iterable[int],
) -> dict[str, Any]:
    last: dict[str, Any] | None = None
    for terms in schedule:
        if kind == "gap":
            if t is None:
                raise ValueError("gap interval requires t")
            lo, hi, detail = entropy_gap_interval(K, D, t, terms)
        elif kind == "hessian":
            lo, hi, detail = hessian_interval(K, D, terms)
        else:
            raise ValueError(kind)
        status = "POSITIVE" if lo > 0 else "NEGATIVE" if hi < 0 else "INCONCLUSIVE"
        last = {
            "terms": terms,
            "status": status,
            "interval": interval_obj(lo, hi),
            "detail": detail,
        }
        if status != "INCONCLUSIVE":
            return last
    assert last is not None
    return last


def graph_signature(
    K: list[list[Fraction]], D: list[list[Fraction]] | None = None
) -> dict[str, Any]:
    n = len(K)
    edges_K = []
    edges_D = []
    edges_union = set()
    for i in range(n):
        for j in range(i + 1, n):
            if K[i][j] != 0:
                edges_K.append([i, j])
                edges_union.add((i, j))
            if D is not None and D[i][j] != 0:
                edges_D.append([i, j])
                edges_union.add((i, j))
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for a, b in edges_union:
        union(a, b)
    components = len({find(i) for i in range(n)})
    m_union = len(edges_union)
    cycle_rank_union = m_union - n + components
    mK = len(edges_K)
    return {
        "n": n,
        "K_edges": edges_K,
        "D_edges": edges_D,
        "union_edges": [list(e) for e in sorted(edges_union)],
        "K_edge_count": mK,
        "union_edge_count": m_union,
        "union_components": components,
        "union_cycle_rank": cycle_rank_union,
        "K4_support": n == 4 and mK == 6,
        "diamond_support": n == 4 and mK == 5,
        "multi_ring_union": cycle_rank_union >= 2,
    }


def outer(u: list[Fraction], v: list[Fraction]) -> list[list[Fraction]]:
    return [[u[i] * v[j] for j in range(len(v))] for i in range(len(u))]


def symmetric_rank2(u: list[Fraction], e: list[Fraction]) -> list[list[Fraction]]:
    n = len(u)
    return [[u[i] * e[j] + e[i] * u[j] for j in range(n)] for i in range(n)]


def interval_add(
    a: tuple[Fraction, Fraction], b: tuple[Fraction, Fraction]
) -> tuple[Fraction, Fraction]:
    return a[0] + b[0], a[1] + b[1]


def interval_sub(
    a: tuple[Fraction, Fraction], b: tuple[Fraction, Fraction]
) -> tuple[Fraction, Fraction]:
    return a[0] - b[1], a[1] - b[0]


def interval_mul(
    a: tuple[Fraction, Fraction], b: tuple[Fraction, Fraction]
) -> tuple[Fraction, Fraction]:
    values = [a[0] * b[0], a[0] * b[1], a[1] * b[0], a[1] * b[1]]
    return min(values), max(values)


def interval_square(a: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
    lo, hi = a
    if lo <= 0 <= hi:
        return Fraction(0), max(lo * lo, hi * hi)
    values = [lo * lo, hi * hi]
    return min(values), max(values)


def J_hessian_quadratic_interval(
    A: list[list[Fraction]],
    w: list[Fraction],
    e: list[Fraction],
    terms: int,
) -> tuple[Fraction, Fraction, dict[str, Any]]:
    K_w = mat_sub(A, outer(w, w))
    X = symmetric_rank2(w, e)
    E = outer(e, e)
    hess_lo, hess_hi, hess_detail = hessian_interval(K_w, X, terms)
    grad_A = gradient_directional_interval(A, E, terms)
    grad_Kw = gradient_directional_interval(K_w, E, terms)
    grad_diff = interval_sub((grad_A[0], grad_A[1]), (grad_Kw[0], grad_Kw[1]))
    doubled = interval_scale(Fraction(2), grad_diff[0], grad_diff[1])
    total = interval_add((hess_lo, hess_hi), doubled)
    return total[0], total[1], {
        "Hess_h_A_minus_wwT": interval_obj(hess_lo, hess_hi),
        "grad_A_direction": interval_obj(grad_A[0], grad_A[1]),
        "grad_A_minus_wwT_direction": interval_obj(grad_Kw[0], grad_Kw[1]),
        "twice_gradient_difference": interval_obj(doubled[0], doubled[1]),
        "hessian_detail": hess_detail,
    }


def J_hessian_matrix_interval(
    A: list[list[Fraction]], w: list[Fraction], terms: int
) -> dict[str, Any]:
    basis = [[Fraction(1), Fraction(0)], [Fraction(0), Fraction(1)], [Fraction(1), Fraction(1)]]
    q1 = J_hessian_quadratic_interval(A, w, basis[0], terms)
    q2 = J_hessian_quadratic_interval(A, w, basis[1], terms)
    q12 = J_hessian_quadratic_interval(A, w, basis[2], terms)
    l11 = (q1[0], q1[1])
    l22 = (q2[0], q2[1])
    off_sum = interval_sub(interval_sub((q12[0], q12[1]), l11), l22)
    l12 = interval_scale(Fraction(1, 2), off_sum[0], off_sum[1])
    prod = interval_mul(l11, l22)
    off_sq = interval_square(l12)
    det_iv = interval_sub(prod, off_sq)
    neg_def = l11[1] < 0 and det_iv[0] > 0
    return {
        "w": [fraction_to_string(x) for x in w],
        "matrix_interval": {
            "L11": interval_obj(*l11),
            "L12": interval_obj(*l12),
            "L22": interval_obj(*l22),
            "det": interval_obj(*det_iv),
        },
        "strict_negative_definite": neg_def,
        "quadratic_checks": {
            "e1": interval_obj(q1[0], q1[1]),
            "e2": interval_obj(q2[0], q2[1]),
            "e1_plus_e2": interval_obj(q12[0], q12[1]),
        },
    }


def run_p2_benchmark(args: argparse.Namespace) -> dict[str, Any]:
    A = [[Fraction(1, 2), Fraction(1, 10)], [Fraction(1, 10), Fraction(1, 3)]]
    u = [Fraction(1, 5), Fraction(1, 6)]
    v = [Fraction(1, 7), Fraction(-1, 8)]
    report = base_report()
    checks = {
        "A": feasibility_report(A, [[Fraction(0), Fraction(0)], [Fraction(0), Fraction(0)]], Fraction(0)),
        "A_minus_uuT": feasibility_report(
            mat_sub(A, outer(u, u)),
            [[Fraction(0), Fraction(0)], [Fraction(0), Fraction(0)]],
            Fraction(0),
        ),
        "A_minus_vvT": feasibility_report(
            mat_sub(A, outer(v, v)),
            [[Fraction(0), Fraction(0)], [Fraction(0), Fraction(0)]],
            Fraction(0),
        ),
    }
    Lu = J_hessian_matrix_interval(A, u, args.p2_terms)
    Lv = J_hessian_matrix_interval(A, v, args.p2_terms)
    status = "CORRECT" if Lu["strict_negative_definite"] and Lv["strict_negative_definite"] else "CRITICAL_GAPS"
    report.update(
        {
            "mode": "p2_benchmark",
            "statement": "Certify Lu and Lv for the requested two-column P2 benchmark.",
            "log_terms": args.p2_terms,
            "A": matrix_to_strings(A),
            "u": [fraction_to_string(x) for x in u],
            "v": [fraction_to_string(x) for x in v],
            "domain_checks": checks,
            "Lu": Lu,
            "Lv": Lv,
            "status": status,
        }
    )
    return report


def probability_report(K: list[list[Fraction]]) -> dict[str, Any]:
    probs = event_probabilities(K)
    return {
        "sum": fraction_obj(sum(probs)),
        "min": fraction_obj(min(probs)),
        "max": fraction_obj(max(probs)),
        "all_positive": all(p > 0 for p in probs),
        "probabilities": [
            {"mask": format(i, f"0{len(K)}b"), "p": fraction_to_string(p)}
            for i, p in enumerate(probs)
        ],
    }


def choose_strict_t(
    K: list[list[Fraction]],
    D: list[list[Fraction]],
    radius: Fraction,
    requested_factor: Fraction,
    max_halvings: int = 20,
) -> tuple[Fraction, dict[str, Any]]:
    t = radius * requested_factor
    attempts = []
    for _ in range(max_halvings + 1):
        feas = feasibility_report(K, D, t)
        attempts.append({"t": fraction_obj(t), "strict_open_domain": feas["strict_open_domain"]})
        if feas["strict_open_domain"]:
            return t, {"factor_start": fraction_obj(requested_factor), "attempts": attempts}
        t /= 2
    raise ValueError("could not find strict feasible t by halving")


def base_report() -> dict[str, Any]:
    script = Path(__file__)
    return {
        "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "pid": os.getpid(),
        "python": sys.version.replace("\n", " "),
        "platform": platform.platform(),
        "cwd": str(Path.cwd()),
        "git_head": git_head(),
        "script_path": str(script),
        "script_sha256": sha256_file(script) if script.exists() else "UNKNOWN",
        "argv": sys.argv,
    }


def smoke_objects() -> tuple[list[list[Fraction]], list[list[Fraction]], Fraction]:
    K = [
        [Fraction(1, 5), Fraction(1, 50), Fraction(-1, 60), Fraction(1, 70)],
        [Fraction(1, 50), Fraction(3, 10), Fraction(1, 80), Fraction(-1, 90)],
        [Fraction(-1, 60), Fraction(1, 80), Fraction(2, 5), Fraction(1, 100)],
        [Fraction(1, 70), Fraction(-1, 90), Fraction(1, 100), Fraction(3, 5)],
    ]
    D = [
        [Fraction(1, 7), Fraction(1, 6), Fraction(-1, 11), Fraction(1, 13)],
        [Fraction(1, 6), Fraction(-1, 8), Fraction(-1, 17), Fraction(1, 19)],
        [Fraction(-1, 11), Fraction(-1, 17), Fraction(1, 9), Fraction(-1, 23)],
        [Fraction(1, 13), Fraction(1, 19), Fraction(-1, 23), Fraction(-1, 10)],
    ]
    return K, D, Fraction(1, 100)


def run_smoke(args: argparse.Namespace) -> dict[str, Any]:
    K, D, t = smoke_objects()
    report = base_report()
    report.update(
        {
            "mode": "smoke",
            "description": "Self-designed full K4, unequal diagonal, rational K,D,t smoke check.",
            "K": matrix_to_strings(K),
            "D": matrix_to_strings(D),
            "t": fraction_obj(t),
            "max_denominators": {
                "K": max_denominator_matrix(K),
                "D": max_denominator_matrix(D),
                "t": t.denominator,
            },
            "graph": graph_signature(K, D),
            "feasibility": feasibility_report(K, D, t),
            "events_midpoint": probability_report(K),
            "events_minus": probability_report(mat_sub(K, mat_scale(t, D))),
            "events_plus": probability_report(mat_add(K, mat_scale(t, D))),
            "hessian": adaptive_interval("hessian", K, D, None, args.log_terms),
            "entropy_gap": adaptive_interval("gap", K, D, t, args.log_terms),
        }
    )
    return report


def load_candidate(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh, parse_float=Decimal, parse_int=int)
    if not isinstance(data, dict):
        raise ValueError(f"{path} does not contain a top-level object")
    radius_key = "radius" if "radius" in data else "t" if "t" in data else None
    if radius_key is None:
        raise ValueError(f"{path} has no radius/t field")
    return {"K": data["K"], "D": data["D"], "radius_key": radius_key, "radius": data[radius_key]}


def review_one_candidate(
    path: Path, args: argparse.Namespace, radius_factor: Fraction
) -> dict[str, Any]:
    raw = load_candidate(path)
    Kr = rationalize_symmetric_matrix(raw["K"], "K", args.max_denominator)
    Dr = rationalize_symmetric_matrix(raw["D"], "D", args.max_denominator)
    radius, radius_error = rationalize_scalar(raw["radius"], args.max_denominator)
    t, t_choice = choose_strict_t(Kr.matrix, Dr.matrix, radius, radius_factor)
    midpoint_probs = probability_report(Kr.matrix)
    hess = adaptive_interval("hessian", Kr.matrix, Dr.matrix, None, args.log_terms)
    gap = adaptive_interval("gap", Kr.matrix, Dr.matrix, t, args.log_terms)
    return {
        "path_name": path.name,
        "source_sha256": sha256_file(path),
        "source_fields_used": ["K", "D", raw["radius_key"]],
        "rationalization": {
            "max_denominator_request": args.max_denominator,
            "K_max_abs_source_error": fraction_obj(Kr.max_abs_source_error),
            "K_max_pair_asymmetry": fraction_obj(Kr.max_pair_asymmetry),
            "D_max_abs_source_error": fraction_obj(Dr.max_abs_source_error),
            "D_max_pair_asymmetry": fraction_obj(Dr.max_pair_asymmetry),
            "radius_abs_source_error": fraction_obj(radius_error),
            "max_denominators": {
                "K": Kr.max_denominator,
                "D": Dr.max_denominator,
                "radius": radius.denominator,
                "t": t.denominator,
            },
        },
        "K": matrix_to_strings(Kr.matrix),
        "D": matrix_to_strings(Dr.matrix),
        "radius": fraction_obj(radius),
        "t": fraction_obj(t),
        "t_choice": t_choice,
        "graph": graph_signature(Kr.matrix, Dr.matrix),
        "feasibility": feasibility_report(Kr.matrix, Dr.matrix, t),
        "events_midpoint": midpoint_probs,
        "hessian": hess,
        "entropy_gap": gap,
    }


def interval_mid_decimal(interval: dict[str, Any]) -> Decimal:
    with localcontext() as ctx:
        ctx.prec = 80
        return (Decimal(interval["lower"]["decimal"]) + Decimal(interval["upper"]["decimal"])) / 2


def run_review_json(args: argparse.Namespace) -> dict[str, Any]:
    radius_factor = Fraction(args.radius_factor)
    report = base_report()
    candidates = [review_one_candidate(Path(p), args, radius_factor) for p in args.inputs]
    negative_candidates = [
        c for c in candidates if c["hessian"]["status"] == "NEGATIVE"
    ]
    if negative_candidates:
        selected = max(
            negative_candidates,
            key=lambda c: interval_mid_decimal(c["hessian"]["interval"]),
        )
        selection_rule = "weakest_certified_negative_hessian_midpoint"
    else:
        selected = min(
            candidates,
            key=lambda c: abs(interval_mid_decimal(c["hessian"]["interval"])),
        )
        selection_rule = "closest_hessian_interval_midpoint_no_certified_negative"
    report.update(
        {
            "mode": "pilot_json_review",
            "selection_rule": selection_rule,
            "selected_path_name": selected["path_name"],
            "candidate_count": len(candidates),
            "candidate_summaries": [
                {
                    "path_name": c["path_name"],
                    "source_sha256": c["source_sha256"],
                    "hessian_status": c["hessian"]["status"],
                    "hessian_interval": c["hessian"]["interval"],
                    "gap_status": c["entropy_gap"]["status"],
                    "gap_interval": c["entropy_gap"]["interval"],
                    "strict_open_domain": c["feasibility"]["strict_open_domain"],
                    "all_midpoint_events_positive": c["events_midpoint"]["all_positive"],
                    "graph": c["graph"],
                    "max_denominators": c["rationalization"]["max_denominators"],
                }
                for c in candidates
            ],
            "selected_candidate": selected,
        }
    )
    return report


def parse_terms(raw: str | None) -> tuple[int, ...]:
    if raw is None:
        return DEFAULT_LOG_TERMS
    terms = tuple(int(x.strip()) for x in raw.split(",") if x.strip())
    if not terms or any(x <= 0 for x in terms):
        raise ValueError("log terms must be positive integers")
    return terms


def write_report(report: dict[str, Any], out_path: Path | None) -> None:
    text = json.dumps(report, indent=2, sort_keys=True)
    if out_path is None:
        print(text)
    else:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--log-terms", type=parse_terms)
    sub = parser.add_subparsers(dest="cmd", required=True)

    smoke = sub.add_parser("smoke")
    smoke.set_defaults(func=run_smoke)

    review = sub.add_parser("review-json")
    review.add_argument("inputs", nargs="+")
    review.add_argument("--max-denominator", type=int, default=1_000_000)
    review.add_argument("--radius-factor", default="1/2")
    review.set_defaults(func=run_review_json)

    p2 = sub.add_parser("p2-benchmark")
    p2.add_argument("--p2-terms", type=int, default=120)
    p2.set_defaults(func=run_p2_benchmark)

    args = parser.parse_args(argv)
    if args.log_terms is None:
        args.log_terms = DEFAULT_LOG_TERMS
    report = args.func(args)
    write_report(report, args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
