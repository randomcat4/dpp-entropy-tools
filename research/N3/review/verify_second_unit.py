#!/usr/bin/env python3
"""Second N3 non-author audit unit.

Checks:
1. the fixed stationary A-optimizer obstruction at commit 449221b;
2. the rank-two boundary pair-projection obstruction at commit f8a75e0;
3. the finite-dimensional Sherman-Morrison optimizer lemma at commit c0964be.

The script uses only review-owned exact event/projection helpers from the
first review unit and does not import author N3 modules.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
import time
from fractions import Fraction as Q
from pathlib import Path

from verify_score_obstruction import (
    COORDS,
    SUBSETS,
    compact,
    direction_from_coords,
    event_jets,
    feasible,
    fisher,
    log_bounds,
    q_values_for_all_k,
)


MAIN_COMMIT = "449221bc3639c2de1239707f15dd938d6e230b9d"
FALSIFICATION_COMMIT = "f8a75e077c4ca449307e251ceef5f5c2bb6d218c"
SHERMAN_COMMIT = "c0964be794705bc89e6b3ba6ecdc98afa6c81e32"

MAIN_OBJECTS = [
    "research/N3/main/stationary_obstruction_v1.md",
    "research/N3/main/pair_score_identity_v1.md",
    "research/N3/main/certify_stationary_obstruction.py",
    "research/N3/main/stationary_obstruction_certificate.json",
]
FALSIFICATION_OBJECTS = [
    "research/N3/falsification/rank2_projection_obstruction.md",
    "research/N3/falsification/rank2_projection_check.py",
    "research/N3/falsification/rank2_projection_check.json",
]
SHERMAN_OBJECTS = [
    "research/N3/inequality/optimizer_sherman_morrison_lemma.md",
]

DYADIC_BITS = 180
DYADIC_SCALE = 2**DYADIC_BITS


def floor_int(x: Q) -> int:
    return x.numerator // x.denominator


def ceil_int(x: Q) -> int:
    return -((-x.numerator) // x.denominator)


class Interval:
    def __init__(self, value: Q | int = 0, hi_ticks: int | None = None):
        if hi_ticks is None:
            scaled = Q(value) * DYADIC_SCALE
            self.lo = floor_int(scaled)
            self.hi = ceil_int(scaled)
        else:
            self.lo = int(value)
            self.hi = int(hi_ticks)
        assert self.lo <= self.hi

    @classmethod
    def bounds(cls, lo: Q, hi: Q) -> "Interval":
        return cls(floor_int(lo * DYADIC_SCALE), ceil_int(hi * DYADIC_SCALE))

    @classmethod
    def ticks(cls, lo: int, hi: int) -> "Interval":
        return cls(lo, hi)

    def frac_bounds(self) -> tuple[Q, Q]:
        return Q(self.lo, DYADIC_SCALE), Q(self.hi, DYADIC_SCALE)

    def __add__(self, other: object) -> "Interval":
        other = as_interval(other)
        return Interval.ticks(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self) -> "Interval":
        return Interval.ticks(-self.hi, -self.lo)

    def __sub__(self, other: object) -> "Interval":
        return self + (-as_interval(other))

    def __rsub__(self, other: object) -> "Interval":
        return as_interval(other) + (-self)

    def __mul__(self, other: object) -> "Interval":
        other = as_interval(other)
        products = [a * b for a in (self.lo, self.hi) for b in (other.lo, other.hi)]
        return Interval.ticks(floor_int(Q(min(products), DYADIC_SCALE)), ceil_int(Q(max(products), DYADIC_SCALE)))

    __rmul__ = __mul__

    def reciprocal(self) -> "Interval":
        assert self.lo > 0 or self.hi < 0, "division interval contains zero"
        lo, hi = self.frac_bounds()
        vals = [1 / lo, 1 / hi]
        return Interval.bounds(min(vals), max(vals))

    def __truediv__(self, other: object) -> "Interval":
        return self * as_interval(other).reciprocal()

    def __rtruediv__(self, other: object) -> "Interval":
        return as_interval(other) * self.reciprocal()

    def square(self) -> "Interval":
        if self.lo <= 0 <= self.hi:
            hi = max(self.lo * self.lo, self.hi * self.hi)
            return Interval.ticks(0, ceil_int(Q(hi, DYADIC_SCALE)))
        return self * self

    def compact(self) -> list[str]:
        lo, hi = self.frac_bounds()
        return compact(lo, hi)

    def __repr__(self) -> str:
        return f"Interval({self.compact()})"


def as_interval(value: object) -> Interval:
    if isinstance(value, Interval):
        return value
    return Interval(Q(value))


def interval_from_log(x: Q, terms: int = 70) -> Interval:
    lo, hi, _ = log_bounds(x, terms=terms)
    return Interval.bounds(lo, hi)


def matmul(A: list[list[Interval]], B: list[list[Interval]]) -> list[list[Interval]]:
    return [
        [sum((A[i][k] * B[k][j] for k in range(len(B))), Interval()) for j in range(len(B[0]))]
        for i in range(len(A))
    ]


def trace(A: list[list[Interval]]) -> Interval:
    return sum((A[i][i] for i in range(len(A))), Interval())


def det3_interval(A: list[list[Interval]]) -> Interval:
    return (
        A[0][0] * (A[1][1] * A[2][2] - A[1][2] * A[2][1])
        - A[0][1] * (A[1][0] * A[2][2] - A[1][2] * A[2][0])
        + A[0][2] * (A[1][0] * A[2][1] - A[1][1] * A[2][0])
    )


def solve_interval(A: list[list[Interval]], b: list[Interval]) -> tuple[list[Interval], list[Interval]]:
    rows = [[as_interval(x) for x in row] + [as_interval(b[i])] for i, row in enumerate(A)]
    pivots: list[Interval] = []
    n = len(rows)
    for k in range(n):
        pivot = rows[k][k]
        assert pivot.lo > 0, f"non-positive pivot at {k}: {pivot}"
        pivots.append(pivot)
        rows[k] = [x / pivot for x in rows[k]]
        for i in range(k + 1, n):
            factor = rows[i][k]
            rows[i] = [x - factor * y for x, y in zip(rows[i], rows[k])]
    x = [Interval() for _ in range(n)]
    for i in reversed(range(n)):
        tail = sum((rows[i][j] * x[j] for j in range(i + 1, n)), Interval())
        x[i] = (rows[i][-1] - tail) / rows[i][i]
    return x, pivots


def inverse_interval(A: list[list[Interval]]) -> tuple[list[list[Interval]], list[list[Interval]]]:
    columns = []
    all_pivots = []
    for j in range(len(A)):
        e = [Interval(1 if i == j else 0) for i in range(len(A))]
        col, pivots = solve_interval(A, e)
        columns.append(col)
        all_pivots.append(pivots)
    return [list(row) for row in zip(*columns)], all_pivots


def quad_interval(M: list[list[Q | Interval]], d: list[Interval]) -> Interval:
    return sum((d[i] * as_interval(M[i][j]) * d[j] for i in range(len(d)) for j in range(len(d))), Interval())


def git_show(repo: Path, commit: str, path: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), "show", f"{commit}:{path}"], text=True)


def git_blob(repo: Path, commit: str, path: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), "rev-parse", f"{commit}:{path}"], text=True).strip()


def sibling_repo(name: str) -> Path:
    return Path.cwd().parent.parent / name / "repo"


def exact_jacobian(K: list[list[Q]]) -> tuple[dict[tuple[int, ...], Q], list[list[Q]]]:
    zero = [[Q(0) for _ in range(3)] for _ in range(3)]
    p, _, _ = event_jets(K, zero)
    cols = []
    for j in range(6):
        dcoords = [Q(0) for _ in range(6)]
        dcoords[j] = Q(1)
        _, dp, _ = event_jets(K, direction_from_coords(dcoords))
        cols.append([dp[S] for S in SUBSETS])
    J = [[cols[j][s] for j in range(6)] for s in range(8)]
    return p, J


def fisher_matrix(K: list[list[Q]]) -> tuple[dict[tuple[int, ...], Q], list[list[Q]]]:
    p, J = exact_jacobian(K)
    F = [[sum(J[s][i] * J[s][j] / p[SUBSETS[s]] for s in range(8)) for j in range(6)] for i in range(6)]
    return p, F


def q_matrices(K: list[list[Q]]) -> list[list[list[Q]]]:
    mats = [[[Q(0) for _ in range(6)] for _ in range(6)] for _ in range(3)]
    basis_values: list[list[Q]] = []
    for i in range(6):
        dcoords = [Q(0) for _ in range(6)]
        dcoords[i] = Q(1)
        basis_values.append(q_values_for_all_k(K, direction_from_coords(dcoords))["Q"])
    for k in range(3):
        for i in range(6):
            mats[k][i][i] = basis_values[i][k]
    for i in range(6):
        for j in range(i + 1, 6):
            dcoords = [Q(0) for _ in range(6)]
            dcoords[i] = Q(1)
            dcoords[j] = Q(1)
            qsum = q_values_for_all_k(K, direction_from_coords(dcoords))["Q"]
            for k in range(3):
                mats[k][i][j] = mats[k][j][i] = (qsum[k] - basis_values[i][k] - basis_values[j][k]) / 2
    return mats


def interval_basis() -> list[list[list[Interval]]]:
    out = []
    for i, j in COORDS:
        E = [[Interval() for _ in range(3)] for _ in range(3)]
        E[i][j] = Interval(1)
        E[j][i] = Interval(1)
        out.append(E)
    return out


def cofactor_from_coords(N_inv: list[list[Interval]], det_N: Interval, d: list[Interval]) -> Interval:
    D = [[Interval() for _ in range(3)] for _ in range(3)]
    for value, (i, j) in zip(d, COORDS):
        D[i][j] = value
        D[j][i] = value
    Y = matmul(N_inv, D)
    return det_N * (trace(Y).square() - trace(matmul(Y, Y)))


def stationary_audit(repo: Path) -> dict[str, object]:
    K = [[Q(v, 100) for v in row] for row in [(51, 24, -24), (24, 48, -24), (-24, -24, 52)]]
    assert feasible(K)
    p, Fisher = fisher_matrix(K)
    q_mats = q_matrices(K)

    logs = {S: interval_from_log(p[S], terms=70) for S in SUBSETS}
    ell12 = logs[()] + logs[(0, 1)] - logs[(0,)] - logs[(1,)]
    ell13 = logs[()] + logs[(0, 2)] - logs[(0,)] - logs[(2,)]
    ell23 = logs[()] + logs[(1, 2)] - logs[(1,)] - logs[(2,)]
    lam = logs[(0, 1, 2)] + logs[(0,)] + logs[(1,)] + logs[(2,)] - logs[()] - logs[(0, 1)] - logs[(0, 2)] - logs[(1, 2)]
    diag_ell = [ell23, ell13, ell12]
    N = [[-lam * K[i][j] - (diag_ell[i] if i == j else Interval()) for j in range(3)] for i in range(3)]
    N_inv, N_pivots = inverse_interval(N)
    det_N = det3_interval(N)
    assert det_N.lo > 0

    basis = interval_basis()
    W = [matmul(N_inv, E) for E in basis]
    eta = [trace(M) for M in W]
    A = [
        [as_interval(Fisher[i][j]) + det_N * trace(matmul(W[i], W[j])) for j in range(6)]
        for i in range(6)
    ]
    A_minus_F_00 = A[0][0] - Fisher[0][0]
    assert A_minus_F_00.lo > 0
    d, A_pivots = solve_interval(A, eta)
    normalizer = sum((eta[i] * d[i] for i in range(6)), Interval())
    assert normalizer.lo > 0
    d_star = [x / normalizer for x in d]

    C = cofactor_from_coords(N_inv, det_N, d)
    C_star = cofactor_from_coords(N_inv, det_N, d_star)
    gaps = [quad_interval(M, d) - C for M in q_mats]
    gaps_star = [quad_interval(M, d_star) - C_star for M in q_mats]
    true_B = quad_interval(Fisher, d) - C
    true_B_star = quad_interval(Fisher, d_star) - C_star
    energy = quad_interval(A, d)
    assert energy.lo > 0
    gap_ratios = [g / energy for g in gaps]
    true_ratio = true_B / energy
    rho = det_N * normalizer

    author = json.loads(git_show(repo, MAIN_COMMIT, "research/N3/main/stationary_obstruction_certificate.json"))
    exact_match_fields = {
        "d_intervals": [x.compact() for x in d],
        "normalizer_interval": normalizer.compact(),
        "normalized_D_star_intervals": [x.compact() for x in d_star],
        "Q_minus_C_intervals": [x.compact() for x in gaps],
        "gap_over_A_intervals": [x.compact() for x in gap_ratios],
        "true_B_over_A_interval": true_ratio.compact(),
        "rho_interval": rho.compact(),
        "A_elimination_pivot_intervals": [x.compact() for x in A_pivots],
    }
    mismatches = [
        key for key, value in exact_match_fields.items() if author.get(key) != value
    ]

    return {
        "status": "PASS",
        "target_commit": MAIN_COMMIT,
        "target_blobs": {path: git_blob(repo, MAIN_COMMIT, path) for path in MAIN_OBJECTS},
        "exact_feasibility": True,
        "A_uses_F_plus_detN_G_not_F_only": A_minus_F_00.lo > 0,
        "A_minus_F_00_interval": A_minus_F_00.compact(),
        "N_inverse_pivots_positive": all(pivot.lo > 0 for row in N_pivots for pivot in row),
        "A_solve_pivots_positive": all(pivot.lo > 0 for pivot in A_pivots),
        "normalizer_positive": normalizer.lo > 0,
        "all_raw_gaps_negative": all(g.hi < 0 for g in gaps),
        "all_normalized_gaps_negative": all(g.hi < 0 for g in gaps_star),
        "true_B_positive_raw": true_B.lo > 0,
        "true_B_positive_normalized": true_B_star.lo > 0,
        "all_gap_over_A_below_minus_0_1015": all(r.hi < Q(-203, 2000) for r in gap_ratios),
        "true_B_over_A_interval": true_ratio.compact(),
        "gap_over_A_intervals": [x.compact() for x in gap_ratios],
        "rho_interval": rho.compact(),
        "d_intervals": [x.compact() for x in d],
        "normalizer_interval": normalizer.compact(),
        "author_certificate_exact_match": len(mismatches) == 0,
        "author_certificate_mismatched_fields": mismatches,
        "dyadic_precision_bits": DYADIC_BITS,
    }


def interval_add(a: tuple[Q, Q], b: tuple[Q, Q]) -> tuple[Q, Q]:
    return a[0] + b[0], a[1] + b[1]


def interval_scale(c: Q, a: tuple[Q, Q]) -> tuple[Q, Q]:
    return (c * a[0], c * a[1]) if c >= 0 else (c * a[1], c * a[0])


def decimal_interval(a: tuple[Q, Q], places: int = 30) -> list[str]:
    scale = 10**places

    def dec(ticks: int) -> str:
        sign = "-" if ticks < 0 else ""
        ticks = abs(ticks)
        return sign + str(ticks // scale) + "." + str(ticks % scale).zfill(places)

    return [dec(floor_int(a[0] * scale)), dec(ceil_int(a[1] * scale))]


def rank2_recompute() -> dict[str, object]:
    eps = Q(1, 10**12)
    a = [Q(1, 14), Q(2, 7), Q(9, 14)]
    p = [Q(0) for _ in range(8)]
    v = [Q(0) for _ in range(8)]
    p[0], v[0] = (1 - eps) / 4, -Q(5, 4) + eps
    p[7], v[7] = eps / 4, Q(1, 4) + eps
    for i in range(3):
        p[1 << i] = (1 - a[i] + (2 * a[i] - 1) * eps) / 4
        v[1 << i] = (2 * a[i] - 1) / 4 - a[i] * eps
        mask = 7 ^ (1 << i)
        p[mask] = (a[i] + (1 - 2 * a[i]) * eps) / 4
        v[mask] = (1 + 2 * a[i]) / 4 - a[i] * eps
    assert sum(p) == 1 and sum(v) == 0 and min(p) > 0
    signs = [Q((-1) ** (3 - mask.bit_count())) for mask in range(8)]
    F = sum(v[i] * v[i] / p[i] for i in range(8))
    Z = sum(1 / x for x in p)
    lambda_prime = sum(signs[i] * v[i] / p[i] for i in range(8))
    F_pair = F - lambda_prime * lambda_prime / Z

    C = (Q(0), Q(0))
    for i, j in [(0, 1), (0, 2), (1, 2)]:
        ell = log_bounds(p[0] * p[(1 << i) | (1 << j)] / (p[1 << i] * p[1 << j]), terms=80)[:2]
        C = interval_add(C, interval_scale(Q(-2), ell))
    lam = log_bounds(p[7] * p[1] * p[2] * p[4] / (p[0] * p[3] * p[5] * p[6]), terms=80)[:2]
    C = interval_add(C, interval_scale(-2 * (1 + eps), lam))
    gap = interval_add((F_pair, F_pair), interval_scale(Q(-1), C))
    B = interval_add((F, F), interval_scale(Q(-1), C))
    assert gap[1] < 0 and B[0] > 0

    limit = Q(13) + sum(1 / x for x in a)
    B0 = (1 - a[0]) * (1 - a[1]) * (1 - a[2])
    return {
        "status": "PASS",
        "epsilon": str(eps),
        "probabilities_positive": min(p) > 0,
        "sum_p_one": sum(p) == 1,
        "sum_v_zero": sum(v) == 0,
        "F_pair_exact": str(F_pair),
        "limit_577_over_18": str(limit),
        "limit_matches_577_over_18": limit == Q(577, 18),
        "B0_constant": str(B0),
        "B0_matches_325_over_1372": B0 == Q(325, 1372),
        "C_interval": decimal_interval(C),
        "F_pair_minus_C_interval": decimal_interval(gap),
        "actual_B_interval": decimal_interval(B),
        "gap_negative": gap[1] < 0,
        "actual_B_positive": B[0] > 0,
        "p": [str(x) for x in p],
        "v": [str(x) for x in v],
    }


def pair_score_identity_checks() -> dict[str, object]:
    p = [Q(3), Q(5), Q(7), Q(11), Q(13), Q(17), Q(19), Q(23)]
    total = sum(p)
    p = [x / total for x in p]
    v = [Q(2), Q(-3), Q(5), Q(-7), Q(11), Q(-13), Q(17), Q(-12)]
    mean_v = sum(v)
    v[-1] -= mean_v
    assert sum(v) == 0
    signs = [Q((-1) ** (3 - mask.bit_count())) for mask in range(8)]
    degree_le_2_masks = [0, 1, 2, 4, 3, 5, 6]
    orthogonal = []
    for sub in degree_le_2_masks:
        orthogonal.append(sum(signs[mask] * (1 if (mask & sub) == sub else 0) for mask in range(8)) == 0)
    F = sum(v[i] * v[i] / p[i] for i in range(8))
    Z = sum(1 / x for x in p)
    lam_prime = sum(signs[i] * v[i] / p[i] for i in range(8))
    c_star = lam_prime / Z
    variational_derivative_zero = sum(signs[i] * (v[i] - c_star * signs[i]) / p[i] for i in range(8)) == 0
    min_value = sum((v[i] - c_star * signs[i]) ** 2 / p[i] for i in range(8))
    F_pair = F - lam_prime * lam_prime / Z
    return {
        "status": "PASS",
        "degree_le_2_orthogonality": orthogonal,
        "all_orthogonality_checks_passed": all(orthogonal),
        "variational_derivative_zero": variational_derivative_zero,
        "P1_equals_P2_min_value": min_value == F_pair,
        "mass_preserving_score": sum(v) == 0,
    }


def git_read_rank2(repo: Path) -> dict[str, object]:
    author = json.loads(git_show(repo, FALSIFICATION_COMMIT, "research/N3/falsification/rank2_projection_check.json"))
    own = rank2_recompute()
    compared = {
        "p": own["p"] == author.get("p"),
        "v": own["v"] == author.get("v"),
        "F_pair_exact": own["F_pair_exact"] == author.get("F_pair_exact"),
        "C_interval": own["C_interval"] == author.get("C_interval"),
        "F_pair_minus_C_interval": own["F_pair_minus_C_interval"] == author.get("F_pair_minus_C_interval"),
        "actual_B_interval": own["actual_B_interval"] == author.get("actual_B_interval"),
    }
    return {
        "status": "PASS" if all(compared.values()) and own["gap_negative"] and own["actual_B_positive"] else "FAIL",
        "target_commit": FALSIFICATION_COMMIT,
        "target_blobs": {path: git_blob(repo, FALSIFICATION_COMMIT, path) for path in FALSIFICATION_OBJECTS},
        "independent_recompute": own,
        "author_json_matches_recompute": compared,
        "all_author_json_compared_fields_match": all(compared.values()),
    }


def mat_inverse_fraction(A: list[list[Q]]) -> list[list[Q]]:
    n = len(A)
    aug = [[A[i][j] for j in range(n)] + [Q(1 if i == j else 0) for j in range(n)] for i in range(n)]
    for k in range(n):
        pivot = aug[k][k]
        assert pivot != 0
        aug[k] = [x / pivot for x in aug[k]]
        for i in range(n):
            if i == k:
                continue
            factor = aug[i][k]
            aug[i] = [x - factor * y for x, y in zip(aug[i], aug[k])]
    return [row[n:] for row in aug]


def mat_vec(A: list[list[Q]], x: list[Q]) -> list[Q]:
    return [sum(A[i][j] * x[j] for j in range(len(x))) for i in range(len(A))]


def dot(a: list[Q], b: list[Q]) -> Q:
    return sum(x * y for x, y in zip(a, b))


def outer(a: list[Q], b: list[Q]) -> list[list[Q]]:
    return [[x * y for y in b] for x in a]


def add_mats(A: list[list[Q]], B: list[list[Q]]) -> list[list[Q]]:
    return [[A[i][j] + B[i][j] for j in range(len(A))] for i in range(len(A))]


def scale_vec(c: Q, x: list[Q]) -> list[Q]:
    return [c * y for y in x]


def sub_vec(a: list[Q], b: list[Q]) -> list[Q]:
    return [x - y for x, y in zip(a, b)]


def quad_fraction(A: list[list[Q]], x: list[Q]) -> Q:
    return dot(x, mat_vec(A, x))


def sherman_morrison_checks(repo: Path) -> dict[str, object]:
    H = [[Q(0) for _ in range(6)] for _ in range(6)]
    diag = [Q(2), Q(3), Q(5), Q(7), Q(11), Q(13)]
    for i, value in enumerate(diag):
        H[i][i] = value
    H[0][1] = H[1][0] = Q(1, 5)
    H[2][4] = H[4][2] = Q(-1, 7)
    H[3][5] = H[5][3] = Q(1, 11)
    c = [Q(1), Q(2), Q(-1), Q(1, 3), Q(-2, 5), Q(1, 7)]
    v = [Q(2, 3), Q(-1, 2), Q(3, 5), Q(1, 4), Q(-2, 7), Q(5, 6)]
    H_inv = mat_inverse_fraction(H)
    Hic = mat_vec(H_inv, c)
    Hiv = mat_vec(H_inv, v)
    alpha = dot(c, Hic)
    beta = dot(v, Hic)
    gamma = dot(v, Hiv)
    s = alpha - beta * beta / (1 + gamma)
    A = add_mats(H, outer(v, v))
    A_inv = mat_inverse_fraction(A)
    Aic = mat_vec(A_inv, c)
    DA_direct = scale_vec(1 / dot(c, Aic), Aic)
    DA_formula = scale_vec(1 / s, sub_vec(Hic, scale_vec(beta / (1 + gamma), Hiv)))
    DH = scale_vec(1 / alpha, Hic)
    numerator_H_DA = alpha - ((2 + gamma) * beta * beta) / ((1 + gamma) * (1 + gamma))
    d_scalar = Q(3, 2)
    return {
        "status": "PASS",
        "target_commit": SHERMAN_COMMIT,
        "target_blobs": {path: git_blob(repo, SHERMAN_COMMIT, path) for path in SHERMAN_OBJECTS},
        "DA_formula_matches_direct_A_solve": DA_formula == DA_direct,
        "c_DA_equals_one": dot(c, DA_formula) == 1,
        "A_DA_DA_equals_one_over_s": quad_fraction(A, DA_formula) == 1 / s,
        "v_DA_formula": dot(v, DA_formula) == beta / ((1 + gamma) * s),
        "cauchy_beta2_le_alpha_gamma": beta * beta <= alpha * gamma,
        "suppression_holds": abs(dot(v, DA_formula)) <= abs(dot(v, DH)),
        "suppression_ratio_formula": (
            beta == 0
            or abs(dot(v, DA_formula)) / abs(dot(v, DH)) == alpha / ((1 + gamma) * s)
        ),
        "full_scalar_equivalence": (quad_fraction(A, DA_formula) >= d_scalar) == (s <= 1 / d_scalar),
        "SM_close_equivalence": (s <= 1 / d_scalar)
        == (beta * beta / (1 + gamma) >= alpha - 1 / d_scalar),
        "H_DA_numerator_formula": quad_fraction(H, DA_formula) == numerator_H_DA / (s * s),
        "F2_at_DA_scalar_equivalence": (quad_fraction(H, DA_formula) >= d_scalar)
        == (numerator_H_DA >= d_scalar * s * s),
        "alpha": str(alpha),
        "beta": str(beta),
        "gamma": str(gamma),
        "s": str(s),
    }


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="research/N3/review/second_unit_audit_results.json")
    ns = parser.parse_args()
    start = time.time()
    repo = Path.cwd()
    falsification_repo = sibling_repo("falsification")

    stationary = stationary_audit(repo)
    rank2 = git_read_rank2(falsification_repo)
    pair_identity = pair_score_identity_checks()
    sherman = sherman_morrison_checks(repo)

    pass_checks = [
        stationary["author_certificate_exact_match"],
        stationary["A_uses_F_plus_detN_G_not_F_only"],
        stationary["A_solve_pivots_positive"],
        stationary["N_inverse_pivots_positive"],
        stationary["all_raw_gaps_negative"],
        stationary["all_normalized_gaps_negative"],
        stationary["all_gap_over_A_below_minus_0_1015"],
        stationary["true_B_positive_raw"],
        stationary["true_B_positive_normalized"],
        rank2["status"] == "PASS",
        rank2["all_author_json_compared_fields_match"],
        pair_identity["all_orthogonality_checks_passed"],
        pair_identity["variational_derivative_zero"],
        pair_identity["P1_equals_P2_min_value"],
    ]
    pass_checks.extend(value for key, value in sherman.items() if isinstance(value, bool))

    script_path = Path(__file__).resolve()
    result = {
        "status": "PASS" if all(pass_checks) else "FAIL",
        "purpose": "Second N3 non-author review unit; local obstructions and finite-dimensional lemma only.",
        "script": str(script_path),
        "script_sha256": sha256_file(script_path),
        "argv": sys.argv,
        "pid": os.getpid(),
        "cwd": os.getcwd(),
        "python": sys.version,
        "executable": sys.executable,
        "platform": platform.platform(),
        "env_threads": {
            k: os.environ.get(k)
            for k in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"]
        },
        "stationary_obstruction": stationary,
        "rank2_projection_obstruction": rank2,
        "pair_score_identity": pair_identity,
        "sherman_morrison": sherman,
        "coverage": {
            "stationary_fixed_objects": len(MAIN_OBJECTS),
            "stationary_exact_centers": 1,
            "stationary_interval_bits": DYADIC_BITS,
            "rank2_fixed_objects": len(FALSIFICATION_OBJECTS),
            "rank2_exact_epsilon_points": 1,
            "pair_score_identity_rational_samples": 1,
            "sherman_morrison_rational_instances": 1,
        },
        "non_coverage": [
            "No proof of the frozen N3 entropy theorem or global rho<=1.",
            "No DPP alignment lower bound for the Sherman-Morrison beta term.",
            "No claim that either obstruction is an entropy counterexample.",
            "No global parameter scan, Lean proof, or all-domain interval certificate.",
        ],
        "elapsed_seconds": time.time() - start,
    }
    output = Path(ns.output)
    output.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(f"STATUS {result['status']}")
    print(f"wrote {output}")
    print(f"pid {result['pid']}")
    print(f"stationary_certificate_match {stationary['author_certificate_exact_match']}")
    print(f"rank2_certificate_match {rank2['all_author_json_compared_fields_match']}")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
