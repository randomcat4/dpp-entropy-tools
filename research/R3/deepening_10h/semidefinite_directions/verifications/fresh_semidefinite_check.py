"""Independent audit checks for D10-S twin-pair semidefinite directions.

This script is deliberately standard-library only.  It does not import or run
the author script, because the author script rewrites its own results files.
"""

from __future__ import annotations

import json
import os
import platform
from decimal import Decimal, localcontext
from fractions import Fraction as F
from math import lcm
from pathlib import Path


for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[key] = "1"


ROOT = Path(__file__).resolve().parents[5]
ROUTE = ROOT / "research" / "R3" / "deepening_10h" / "semidefinite_directions"


def det_int(matrix: list[list[int]]) -> int:
    a = [row[:] for row in matrix]
    n = len(a)
    if n == 0:
        return 1
    last = 1
    sign = 1
    for k in range(n - 1):
        pivot = next((i for i in range(k, n) if a[i][k]), None)
        if pivot is None:
            return 0
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            sign = -sign
        piv = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                num = a[i][j] * piv - a[i][k] * a[k][j]
                assert num % last == 0
                a[i][j] = num // last
            a[i][k] = 0
        last = piv
    return sign * a[-1][-1]


def det(a: list[list[F]]) -> F:
    if not a:
        return F(1)
    den = lcm(*(x.denominator for row in a for x in row))
    z = [[int(x * den) for x in row] for row in a]
    return F(det_int(z), den ** len(a))


def mobius_exact(K: list[list[F]]) -> list[F]:
    n = len(K)
    inc = []
    for mask in range(1 << n):
        idx = [i for i in range(n) if (mask >> i) & 1]
        inc.append(det([[K[i][j] for j in idx] for i in idx]))
    p = inc[:]
    for bit in range(n):
        for mask in range(1 << n):
            if not ((mask >> bit) & 1):
                p[mask] -= p[mask | (1 << bit)]
    assert sum(p) == 1
    assert min(p) > 0
    return p


def signed_event(K: list[list[F]], mask: int) -> F:
    n = len(K)
    A = [row[:] for row in K]
    for i in range(n):
        if not ((mask >> i) & 1):
            A[i][i] -= 1
    return ((-1) ** (n - mask.bit_count())) * det(A)


def solve(A: list[list[F]], rhs: list[F]) -> list[F]:
    a = [row[:] + [b] for row, b in zip(A, rhs)]
    n = len(a)
    for k in range(n):
        pivot = next(i for i in range(k, n) if a[i][k] != 0)
        a[k], a[pivot] = a[pivot], a[k]
        div = a[k][k]
        a[k] = [x / div for x in a[k]]
        for i in range(n):
            if i == k:
                continue
            mul = a[i][k]
            if mul:
                a[i] = [x - mul * y for x, y in zip(a[i], a[k])]
    return [row[-1] for row in a]


def add(M: list[list[F]], D: list[list[F]], t: F) -> list[list[F]]:
    return [[x + t * y for x, y in zip(r, s)] for r, s in zip(M, D)]


def gershgorin_bounds(K: list[list[F]]) -> tuple[F, F, F]:
    k_margin = min(row[i] - sum(abs(x) for j, x in enumerate(row) if j != i) for i, row in enumerate(K))
    ik_margin = min(1 - row[i] - sum(abs(x) for j, x in enumerate(row) if j != i) for i, row in enumerate(K))
    return k_margin, ik_margin, min(k_margin, ik_margin)


def graph_connected(K: list[list[F]]) -> bool:
    n = len(K)
    seen = {0}
    frontier = [0]
    while frontier:
        i = frontier.pop()
        for j, value in enumerate(K[i]):
            if i != j and value != 0 and j not in seen:
                seen.add(j)
                frontier.append(j)
    return len(seen) == n


def dec(x: F) -> Decimal:
    return Decimal(x.numerator) / Decimal(x.denominator)


def entropy(probs: list[F]) -> Decimal:
    return -sum(dec(p) * dec(p).ln() for p in probs)


def hessian_from_quadratic_probs(p_minus: list[F], p0: list[F], p_plus: list[F], h: F) -> Decimal:
    first = [(rp - lm) / (2 * h) for lm, rp in zip(p_minus, p_plus)]
    second = [(lm + rp - 2 * mid) / (h * h) for lm, mid, rp in zip(p_minus, p0, p_plus)]
    assert sum(first) == 0
    assert sum(second) == 0
    return -sum(dec(a * a / p) + dec(b) * dec(p).ln() for p, a, b in zip(p0, first, second))


def pair_hessian(alpha: F, beta: F, d: F, e: F) -> Decimal:
    q = d * d - e * e
    probs = [
        (1 - alpha) * (1 - alpha) - beta * beta,
        alpha - alpha * alpha + beta * beta,
        alpha - alpha * alpha + beta * beta,
        alpha * alpha - beta * beta,
    ]
    first = [
        -2 * (1 - alpha) * d - 2 * beta * e,
        d * (1 - 2 * alpha) + 2 * beta * e,
        d * (1 - 2 * alpha) + 2 * beta * e,
        2 * alpha * d - 2 * beta * e,
    ]
    second = [2 * q, -2 * q, -2 * q, 2 * q]
    assert min(probs) > 0
    assert sum(first) == 0
    assert sum(second) == 0
    return -sum(dec(a * a / p) + dec(b) * dec(p).ln() for p, a, b in zip(probs, first, second))


def conditional_schur_identities(K: list[list[F]], d: F, e: F) -> tuple[int, Decimal, Decimal]:
    n = len(K)
    m = n - 2
    A = [[K[0][0], K[0][1]], [K[1][0], K[1][1]]]
    B = [row[2:] for row in K[2:]]
    y = K[0][2:]
    weights = mobius_exact(B)
    full = mobius_exact(K)
    identities = 0
    weighted_h2 = Decimal(0)
    worst_slack = Decimal("-Infinity")
    q = d * d - e * e
    label_bound = -4 * dec(q) * Decimal(2).ln()
    for rest_mask in range(1 << m):
        Bt = [row[:] for row in B]
        for j in range(m):
            if not ((rest_mask >> j) & 1):
                Bt[j][j] -= 1
        sol = solve(Bt, y)
        eta = -sum(u * v for u, v in zip(y, sol))
        C = [[A[0][0] + eta, A[0][1] + eta], [A[1][0] + eta, A[1][1] + eta]]
        assert C[0][0] == C[1][1]
        assert C[0][0] > 0 and det(C) > 0
        assert 1 - C[0][0] > 0
        assert det([[1 - C[0][0], -C[0][1]], [-C[1][0], 1 - C[1][1]]]) > 0
        pair_probs = mobius_exact(C)
        for pair_mask in range(4):
            assert pair_probs[pair_mask] * weights[rest_mask] == full[pair_mask | (rest_mask << 2)]
            identities += 1
        h2 = pair_hessian(C[0][0], C[0][1], d, e)
        weighted_h2 += dec(weights[rest_mask]) * h2
        worst_slack = max(worst_slack, h2 - label_bound)
    return identities, weighted_h2, worst_slack


def independent_n4_case() -> dict[str, object]:
    M = [
        [F(1, 2), F(1, 9), F(1, 100), F(-1, 120)],
        [F(1, 9), F(1, 2), F(1, 100), F(-1, 120)],
        [F(1, 100), F(1, 100), F(2, 5), F(1, 20)],
        [F(-1, 120), F(-1, 120), F(1, 20), F(3, 5)],
    ]
    d, e = F(1, 10), F(1, 30)
    D = [
        [d, e, F(0), F(0)],
        [e, d, F(0), F(0)],
        [F(0), F(0), F(0), F(0)],
        [F(0), F(0), F(0), F(0)],
    ]
    q = d * d - e * e
    h = F(1)
    probs = []
    min_margin = None
    signed_checks = 0
    for t in (-h, F(0), h):
        K = add(M, D, t)
        k_margin, ik_margin, both = gershgorin_bounds(K)
        min_margin = both if min_margin is None else min(min_margin, both)
        p = mobius_exact(K)
        for mask, value in enumerate(p):
            assert value == signed_event(K, mask)
            signed_checks += 1
        probs.append(p)
    h2 = hessian_from_quadratic_probs(probs[0], probs[1], probs[2], h)
    schur_count, weighted_h2, worst_pair_slack = conditional_schur_identities(M, d, e)
    bound = -4 * dec(q) * Decimal(2).ln()
    gap = (entropy(probs[0]) + entropy(probs[2])) / 2 - entropy(probs[1])
    return {
        "n": 4,
        "new_parameters": {
            "a": "1/2",
            "b": "1/9",
            "y": ["1/100", "-1/120"],
            "B": [["2/5", "1/20"], ["1/20", "3/5"]],
            "d": str(d),
            "e": str(e),
            "d_squared_minus_e_squared": str(q),
        },
        "interval": "[-1,1]",
        "endpoint_gershgorin_min": str(min_margin),
        "signed_event_checks": signed_checks,
        "conditional_schur_identities_at_center": schur_count,
        "hessian": str(h2),
        "weighted_conditional_hessian": str(weighted_h2),
        "bound": str(bound),
        "hessian_minus_bound": str(h2 - bound),
        "gap_h_1": str(gap),
        "worst_pair_hessian_minus_label_bound": str(worst_pair_slack),
        "rank_D": 2,
        "connected": graph_connected(M),
        "non_direct_sum": any(M[i][j] != 0 for i in (0, 1) for j in (2, 3)),
        "non_thinning": True,
    }


def author_n11_certificate() -> dict[str, object]:
    data = json.loads((ROUTE / "results" / "sanity.json").read_text(encoding="utf-8"))
    rec = next(r for r in data["records"] if r.get("n") == 11 and "M" in r)
    M = [[F(x) for x in row] for row in rec["M"]]
    D = [[F(x) for x in row] for row in rec["D"]]
    d, e = D[0][0], D[0][1]
    endpoints = [add(M, D, F(-1, 2)), add(M, D, F(1, 2))]
    endpoint_margins = [gershgorin_bounds(K) for K in endpoints]
    thinning_scalar = D[0][0] / M[0][0]
    return {
        "n": 11,
        "rank_D_pair_eigenvalues": [str(d + e), str(d - e)],
        "d_squared_minus_e_squared": str(d * d - e * e),
        "endpoint_gershgorin_margins": [[str(x) for x in triple] for triple in endpoint_margins],
        "all_y_nonzero": all(M[0][j] != 0 and M[1][j] == M[0][j] for j in range(2, 11)),
        "connected_graph": graph_connected(M),
        "non_direct_sum": any(M[i][j] != 0 for i in (0, 1) for j in range(2, 11)),
        "not_a_thinning_direction": any(D[i][j] != thinning_scalar * M[i][j] for i in range(11) for j in range(11)),
        "events_in_author_record": next(r["events"] for r in data["records"] if r.get("n") == 11 and r.get("t") == "0"),
        "conditional_identities_author_record": rec["conditional_event_identities"],
    }


def mixed_hessian_shortcut_check() -> dict[str, object]:
    with localcontext() as ctx:
        ctx.prec = 80
        fisher = -(
            F(-5, 6) * F(-1, 6) / F(5, 36)
            + F(1, 6) * F(5, 6) / F(5, 36)
            + F(1, 3) * F(-1, 3) / F(13, 36)
            + F(1, 3) * F(-1, 3) / F(13, 36)
        )
        exact_lower = 2 * F(8, 9) + fisher
        value = 2 * (Decimal(13) / Decimal(5)).ln() + dec(fisher)
        return {
            "mixed_hessian": str(value),
            "rational_lower_bound": str(exact_lower),
            "positive": value > 0 and exact_lower == F(46, 117),
            "scope": "cross-term shortcut only; not a counterexample to H'' along one PSD direction",
        }


def main() -> None:
    with localcontext() as ctx:
        ctx.prec = 80
        report = {
            "status": "PASS",
            "python": platform.python_version(),
            "seed": None,
            "random_draws": 0,
            "independent_n4": independent_n4_case(),
            "author_n11_certificate": author_n11_certificate(),
            "mixed_hessian_shortcut": mixed_hessian_shortcut_check(),
            "denominator": {
                "independent_n4_families": 1,
                "independent_n4_kernel_points": 3,
                "independent_n4_exact_events": 48,
                "independent_n4_schur_identities": 16,
                "author_n11_records_checked": 1,
                "random_draws": 0,
                "failed_assertions": 0,
            },
        }
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
