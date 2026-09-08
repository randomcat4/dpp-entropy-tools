"""Fresh rational checks for the fixed-beta general family.

The computations here are intentionally independent of general_family/search.py.
They instantiate the theorem's rational template at n=6 and verify, with
Fraction arithmetic where algebraic, the shape, positivity, K-midpoint closure,
rank formula, exact atom semantics, and path entropy DP recurrence.
"""

from __future__ import annotations

import json
from decimal import Decimal, localcontext
from fractions import Fraction
from typing import Iterable, Sequence


Matrix = list[list[Fraction]]


def q(x) -> Fraction:
    return x if isinstance(x, Fraction) else Fraction(x)


def dec(x: Fraction, precision: int) -> Decimal:
    return Decimal(x.numerator) / Decimal(x.denominator)


def zeros(n: int, m: int) -> Matrix:
    return [[Fraction(0) for _ in range(m)] for _ in range(n)]


def eye(n: int) -> Matrix:
    return [[Fraction(i == j) for j in range(n)] for i in range(n)]


def transpose(a: Matrix) -> Matrix:
    return [list(row) for row in zip(*a)]


def mat_add(a: Matrix, b: Matrix) -> Matrix:
    return [[x + y for x, y in zip(row_a, row_b)] for row_a, row_b in zip(a, b)]


def mat_sub(a: Matrix, b: Matrix) -> Matrix:
    return [[x - y for x, y in zip(row_a, row_b)] for row_a, row_b in zip(a, b)]


def mat_scale(c: Fraction, a: Matrix) -> Matrix:
    return [[c * x for x in row] for row in a]


def mat_mul(a: Matrix, b: Matrix) -> Matrix:
    bt = transpose(b)
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def diag_matrix(values: Sequence[Fraction]) -> Matrix:
    n = len(values)
    out = zeros(n, n)
    for i, value in enumerate(values):
        out[i][i] = q(value)
    return out


def principal(a: Matrix, items: Sequence[int]) -> Matrix:
    return [[a[i][j] for j in items] for i in items]


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


def rank_fraction(a: Matrix) -> int:
    m = [row[:] for row in a]
    rows = len(m)
    cols = 0 if rows == 0 else len(m[0])
    rank = 0
    col = 0
    while rank < rows and col < cols:
        pivot = None
        for i in range(rank, rows):
            if m[i][col] != 0:
                pivot = i
                break
        if pivot is None:
            col += 1
            continue
        m[rank], m[pivot] = m[pivot], m[rank]
        scale = m[rank][col]
        m[rank] = [x / scale for x in m[rank]]
        for i in range(rows):
            if i != rank and m[i][col] != 0:
                factor = m[i][col]
                m[i] = [x - factor * y for x, y in zip(m[i], m[rank])]
        rank += 1
        col += 1
    return rank


def leading_principal_minors(a: Matrix) -> list[Fraction]:
    return [det_bareiss([row[:k] for row in a[:k]]) for k in range(1, len(a) + 1)]


def lower_bidiagonal(beta: Sequence[Fraction]) -> Matrix:
    n = len(beta) + 1
    out = eye(n)
    for i, value in enumerate(beta):
        out[i + 1][i] = -q(value)
    return out


def inverse_lower_bidiagonal(beta: Sequence[Fraction]) -> Matrix:
    n = len(beta) + 1
    out = zeros(n, n)
    for j in range(n):
        out[j][j] = Fraction(1)
        product = Fraction(1)
        for i in range(j + 1, n):
            product *= q(beta[i - 1])
            out[i][j] = product
    return out


def s_matrix(beta: Sequence[Fraction], tau: Sequence[Fraction]) -> Matrix:
    rinv = inverse_lower_bidiagonal(beta)
    return mat_mul(mat_mul(rinv, diag_matrix(tau)), transpose(rinv))


def p_matrix(beta: Sequence[Fraction], tau: Sequence[Fraction]) -> Matrix:
    r = lower_bidiagonal(beta)
    inv_tau = [Fraction(1, 1) / q(t) for t in tau]
    return mat_mul(mat_mul(transpose(r), diag_matrix(inv_tau)), r)


def l_parts(beta: Sequence[Fraction], tau: Sequence[Fraction]) -> tuple[list[Fraction], list[Fraction]]:
    n = len(tau)
    inv = [Fraction(1, 1) / q(t) for t in tau]
    diag = [Fraction(0) for _ in range(n)]
    edge = [Fraction(0) for _ in range(n - 1)]
    for i in range(n - 1):
        diag[i] = inv[i] + q(beta[i]) * q(beta[i]) * inv[i + 1] - 1
        edge[i] = -q(beta[i]) * inv[i + 1]
    diag[-1] = inv[-1] - 1
    return diag, edge


def tridiagonal(diag: Sequence[Fraction], edge: Sequence[Fraction]) -> Matrix:
    n = len(diag)
    out = zeros(n, n)
    for i, value in enumerate(diag):
        out[i][i] = q(value)
    for i, value in enumerate(edge):
        out[i][i + 1] = q(value)
        out[i + 1][i] = q(value)
    return out


def leading_continuants(diag: Sequence[Fraction], edge: Sequence[Fraction]) -> list[Fraction]:
    if not diag:
        return []
    prev2 = Fraction(1)
    prev1 = q(diag[0])
    out = [prev1]
    for i in range(1, len(diag)):
        current = q(diag[i]) * prev1 - q(edge[i - 1]) ** 2 * prev2
        out.append(current)
        prev2, prev1 = prev1, current
    return out


def interval_determinants(diag: Sequence[Fraction], edge: Sequence[Fraction]) -> list[list[Fraction]]:
    n = len(diag)
    out = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for start in range(n):
        prev2 = Fraction(1)
        prev1 = q(diag[start])
        out[start][start] = prev1
        for end in range(start + 1, n):
            current = q(diag[end]) * prev1 - q(edge[end - 1]) ** 2 * prev2
            out[start][end] = current
            prev2, prev1 = prev1, current
    return out


def det_i_plus_l(diag: Sequence[Fraction], edge: Sequence[Fraction]) -> Fraction:
    return leading_continuants([q(x) + 1 for x in diag], edge)[-1]


def bit_indices(mask: int, n: int) -> list[int]:
    return [i for i in range(n) if (mask >> i) & 1]


def path_weight(mask: int, kappa: list[list[Fraction]], n: int) -> Fraction:
    weight = Fraction(1)
    i = 0
    while i < n:
        if not ((mask >> i) & 1):
            i += 1
            continue
        start = i
        while i + 1 < n and ((mask >> (i + 1)) & 1):
            i += 1
        weight *= kappa[start][i]
        i += 1
    return weight


def event_atoms_mobius(k: Matrix) -> list[Fraction]:
    n = len(k)
    full = (1 << n) - 1
    inclusion = [
        det_bareiss(principal(k, bit_indices(mask, n))) for mask in range(1 << n)
    ]
    atoms: list[Fraction] = []
    for event in range(1 << n):
        comp = full ^ event
        total = Fraction(0)
        sub = comp
        while True:
            total += (-1 if sub.bit_count() & 1 else 1) * inclusion[event | sub]
            if sub == 0:
                break
            sub = (sub - 1) & comp
        atoms.append(total)
    return atoms


def direct_entropy(atoms: Sequence[Fraction], precision: int) -> Decimal:
    with localcontext() as ctx:
        ctx.prec = precision
        total = Decimal(0)
        for atom in atoms:
            if atom:
                p = dec(atom, precision)
                total -= p * p.ln()
        return +total


def dp_entropy(diag: Sequence[Fraction], edge: Sequence[Fraction], precision: int) -> dict[str, object]:
    n = len(diag)
    kappa = interval_determinants(diag, edge)
    z = [Fraction(0) for _ in range(n + 1)]
    t_log = [Decimal(0) for _ in range(n + 1)]
    z[0] = Fraction(1)
    with localcontext() as ctx:
        ctx.prec = precision
        for length in range(1, n + 1):
            end = length - 1
            z_value = z[length - 1]
            t_value = t_log[length - 1]
            for start in range(length):
                prefix_len = 0 if start == 0 else start - 1
                block = kappa[start][end]
                z_prefix = z[prefix_len]
                z_value += z_prefix * block
                block_dec = dec(block, precision)
                t_value += block_dec * t_log[prefix_len]
                t_value += dec(z_prefix, precision) * block_dec * block_dec.ln()
            z[length] = z_value
            t_log[length] = +t_value
        z_dec = dec(z[-1], precision)
        entropy = +(z_dec.ln() - t_log[-1] / z_dec)
    return {
        "Z": z[-1],
        "det_I_plus_L": det_i_plus_l(diag, edge),
        "entropy": entropy,
        "state_count": n * (n + 1) // 2,
    }


def max_abs_row_sum(a: Matrix) -> Fraction:
    return max(sum(abs(x) for x in row) for row in a)


def fstr(x) -> str:
    if isinstance(x, Fraction):
        return f"{x.numerator}/{x.denominator}"
    if isinstance(x, Decimal):
        return str(x)
    if isinstance(x, list):
        return [fstr(v) for v in x]
    if isinstance(x, dict):
        return {k: fstr(v) for k, v in x.items()}
    return x


def check_point(beta: Sequence[Fraction], tau: Sequence[Fraction], precision: int) -> dict[str, object]:
    n = len(tau)
    ident = eye(n)
    s = s_matrix(beta, tau)
    p = p_matrix(beta, tau)
    diag, edge = l_parts(beta, tau)
    l_mat = tridiagonal(diag, edge)
    k = mat_sub(ident, s)
    k_from_phi = mat_mul(l_mat, s)
    atoms = event_atoms_mobius(k)
    kappa = interval_determinants(diag, edge)
    z = det_i_plus_l(diag, edge)
    l_atoms = [path_weight(mask, kappa, n) / z for mask in range(1 << n)]
    dp = dp_entropy(diag, edge, precision)
    h_direct = direct_entropy(atoms, precision)
    return {
        "tau": list(tau),
        "s_row_sum_bound": max_abs_row_sum(s),
        "Rinv_D_RinvT_times_RT_Dinv_R_is_I": mat_mul(s, p) == ident,
        "L_equals_P_minus_I": l_mat == mat_sub(p, ident),
        "K_equals_I_minus_S_equals_L_times_S": k == k_from_phi,
        "L_tridiagonal": all(l_mat[i][j] == 0 for i in range(n) for j in range(n) if abs(i - j) > 1),
        "connected_edges_nonzero": all(e != 0 for e in edge),
        "heterogeneous_diagonal": len(set(diag)) > 1,
        "L_leading_continuants_positive": all(x > 0 for x in leading_continuants(diag, edge)),
        "K_leading_principal_minors_positive": all(x > 0 for x in leading_principal_minors(k)),
        "events_checked": 1 << n,
        "mobius_sum": sum(atoms, Fraction(0)),
        "l_ensemble_sum": sum(l_atoms, Fraction(0)),
        "atom_mismatch_count": sum(1 for a, b in zip(atoms, l_atoms) if a != b),
        "min_atom": min(atoms),
        "dp_Z_matches_det_I_plus_L": dp["Z"] == dp["det_I_plus_L"],
        "dp_state_count": dp["state_count"],
        "dp_entropy": dp["entropy"],
        "direct_entropy": h_direct,
        "entropy_abs_diff": abs(dp["entropy"] - h_direct),
        "entropy_abs_diff_within_1e_minus_80": abs(dp["entropy"] - h_direct) <= Decimal("1e-80"),
    }


def rank_delta(beta: Sequence[Fraction], delta_tau: Sequence[Fraction]) -> int:
    rinv = inverse_lower_bidiagonal(beta)
    delta_s = mat_mul(mat_mul(rinv, diag_matrix(delta_tau)), transpose(rinv))
    return rank_fraction(delta_s)


def main() -> None:
    n = 6
    precision = 90
    beta = [Fraction(1, 2) for _ in range(n - 1)]
    u = [Fraction(i + 1) for i in range(1, n + 1)]
    v = [Fraction(2 * i + 1) for i in range(1, n + 1)]
    midpoint_template = [(x + y) / 2 for x, y in zip(u, v)]
    row_bound = max(max_abs_row_sum(s_matrix(beta, w)) for w in (u, v, midpoint_template))
    epsilon = Fraction(1, 2) / row_bound
    tau_minus = [epsilon * x for x in u]
    tau_plus = [epsilon * x for x in v]
    tau_zero = [(x + y) / 2 for x, y in zip(tau_minus, tau_plus)]

    checks = {
        "minus": check_point(beta, tau_minus, precision),
        "zero": check_point(beta, tau_zero, precision),
        "plus": check_point(beta, tau_plus, precision),
    }
    k_minus = mat_sub(eye(n), s_matrix(beta, tau_minus))
    k_zero = mat_sub(eye(n), s_matrix(beta, tau_zero))
    k_plus = mat_sub(eye(n), s_matrix(beta, tau_plus))
    delta_full = [b - a for a, b in zip(tau_minus, tau_plus)]
    rank_support_checks = [
        {"support_size": 1, "rank": rank_delta(beta, [Fraction(1) if i == 0 else Fraction(0) for i in range(n)])},
        {"support_size": 2, "rank": rank_delta(beta, [Fraction(1) if i in (1, 4) else Fraction(0) for i in range(n)])},
        {"support_size": n, "rank": rank_delta(beta, delta_full)},
    ]
    status = "PASS"
    predicates = [
        mat_scale(Fraction(2), k_zero) == mat_add(k_minus, k_plus),
        all(item["rank"] == item["support_size"] for item in rank_support_checks),
    ]
    for point in checks.values():
        predicates.extend(
            [
                point["s_row_sum_bound"] < 1,
                point["Rinv_D_RinvT_times_RT_Dinv_R_is_I"],
                point["L_equals_P_minus_I"],
                point["K_equals_I_minus_S_equals_L_times_S"],
                point["L_tridiagonal"],
                point["connected_edges_nonzero"],
                point["heterogeneous_diagonal"],
                point["L_leading_continuants_positive"],
                point["K_leading_principal_minors_positive"],
                point["mobius_sum"] == 1,
                point["l_ensemble_sum"] == 1,
                point["atom_mismatch_count"] == 0,
                point["dp_Z_matches_det_I_plus_L"],
                point["entropy_abs_diff_within_1e_minus_80"],
            ]
        )
    if not all(predicates):
        status = "FAIL"
    result = {
        "status": status,
        "n": n,
        "beta": beta,
        "template": {
            "u": u,
            "v": v,
            "midpoint": midpoint_template,
            "row_bound_max_unscaled": row_bound,
            "epsilon": epsilon,
            "epsilon_times_row_bound": epsilon * row_bound,
        },
        "K_midpoint_exact": mat_scale(Fraction(2), k_zero) == mat_add(k_minus, k_plus),
        "rank_support_checks": rank_support_checks,
        "points": checks,
        "notes": [
            "All algebraic predicates use Fraction arithmetic.",
            "Entropy uses Decimal logarithms; both direct and DP forms produce the same Decimal value at the selected precision.",
            "DP state count n(n+1)/2 is compared with all 2^n exact events in the direct Mobius check.",
        ],
    }
    print(json.dumps(fstr(result), indent=2))


if __name__ == "__main__":
    main()
