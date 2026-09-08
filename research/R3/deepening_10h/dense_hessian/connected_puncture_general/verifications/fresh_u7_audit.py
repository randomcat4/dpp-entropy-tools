"""Fresh non-author sanity for D10-U7.

This file intentionally imports no author research module.  It rebuilds exact
atoms from the shifted determinant formula and uses the normalized
-(1+R)log(1+R) series with rational arithmetic.  The calculations are finite
sanity checks only; the accompanying audit report contains the proof review.
"""

from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations, permutations
from pathlib import Path
import hashlib
import json
import math
import time


HERE = Path(__file__).resolve().parent
ROUTE = HERE.parent


def put(poly, key, value):
    if value == 0:
        return
    poly[key] = poly.get(key, F(0)) + value
    if poly[key] == 0:
        del poly[key]


def add_poly(a, b):
    out = dict(a)
    for k, v in b.items():
        put(out, k, v)
    return out


def scale_poly(a, c):
    if c == 0:
        return {}
    return {k: v * c for k, v in a.items() if v * c}


def mul_poly(a, b, cap_total=None, marker_caps=None):
    out = {}
    for ea, ca in a.items():
        for eb, cb in b.items():
            e = tuple(x + y for x, y in zip(ea, eb))
            if cap_total is not None and sum(e) > cap_total:
                continue
            if marker_caps is not None:
                if any(e[i + 1] > marker_caps[i] for i in range(len(marker_caps))):
                    continue
            put(out, e, ca * cb)
    return out


def sub_poly(a, b):
    return add_poly(a, scale_poly(b, F(-1)))


def const_poly(c, dim):
    return {tuple([0] * dim): F(c)} if c else {}


def det_poly(mat, cap_total=None, marker_caps=None):
    n = len(mat)
    out = {}
    for perm in permutations(range(n)):
        inv = sum(perm[i] > perm[j] for i in range(n) for j in range(i + 1, n))
        term = const_poly(F(-1 if inv % 2 else 1), len(next(iter(mat[0][0].keys()))))
        ok = True
        for i, j in enumerate(perm):
            term = mul_poly(term, mat[i][j], cap_total=cap_total, marker_caps=marker_caps)
            if not term:
                ok = False
                break
        if ok:
            out = add_poly(out, term)
    return out


def atom_shifted_poly(n, x, weights, targets, S, cap_total, marker_caps):
    """Exact atom p_S=(-1)^|Sc| det(K-I_Sc)."""
    dim = 1 + len(targets)
    target_pos = {tuple(sorted(edge)): i for i, edge in enumerate(targets)}
    mat = []
    for i in range(n):
        row = []
        for j in range(n):
            if i == j:
                row.append(const_poly(x[i] if i in S else x[i] - 1, dim))
            else:
                edge = tuple(sorted((i, j)))
                p = {}
                if edge in weights:
                    e = [0] * dim
                    e[0] = 1
                    put(p, tuple(e), weights[edge])
                if edge in target_pos:
                    e = [0] * dim
                    e[1 + target_pos[edge]] = 1
                    put(p, tuple(e), F(1))
                row.append(p)
        mat.append(row)
    p = det_poly(mat, cap_total=cap_total, marker_caps=marker_caps)
    if (n - len(S)) % 2:
        p = scale_poly(p, F(-1))
    return p


def atom_mobius_numeric(n, K, S):
    total = F(0)
    rest = [i for i in range(n) if i not in S]
    for mask in range(1 << len(rest)):
        T = set(S)
        for b, v in enumerate(rest):
            if mask >> b & 1:
                T.add(v)
        sign = -1 if (len(T) - len(S)) % 2 else 1
        total += sign * det_numeric([[K[i][j] for j in T] for i in T])
    return total


def det_numeric(mat):
    n = len(mat)
    if n == 0:
        return F(1)
    total = F(0)
    for perm in permutations(range(n)):
        inv = sum(perm[i] > perm[j] for i in range(n) for j in range(i + 1, n))
        term = F(-1 if inv % 2 else 1)
        for i, j in enumerate(perm):
            term *= mat[i][j]
        total += term
    return total


def entropy_series(n, x, weights, targets, cap_total, marker_caps):
    dim = 1 + len(targets)
    H = {}
    for mask in range(1 << n):
        S = frozenset(i for i in range(n) if mask >> i & 1)
        p = atom_shifted_poly(n, x, weights, targets, S, cap_total, marker_caps)
        a = F(1)
        for i in range(n):
            a *= x[i] if i in S else 1 - x[i]
        R = scale_poly(sub_poly(p, const_poly(a, dim)), F(1, 1) / a)
        # -(1+R)log(1+R) = -R - R^2/2 + R^3/6 - R^4/12 + ...
        power = const_poly(F(1), dim)
        for k in range(1, cap_total + 1):
            power = mul_poly(power, R, cap_total=cap_total, marker_caps=marker_caps)
            if not power:
                break
            coeff = F(-1) if k == 1 else F((-1) ** (k + 1), k * (k - 1))
            H = add_poly(H, scale_poly(power, a * coeff))
    return H


def derivative_eps_series(H, orders):
    out = {}
    for exp, coeff in H.items():
        if tuple(exp[1:]) != tuple(orders):
            continue
        mult = F(1)
        for o in orders:
            mult *= math.factorial(o)
        put(out, exp[0], coeff * mult)
    return out


def graph_dist(n, edges, e):
    s, t = e
    if s == t:
        return 0
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    frontier = [(s, 0)]
    seen = {s}
    for u, d in frontier:
        for v in adj[u]:
            if v == t:
                return d + 1
            if v not in seen:
                seen.add(v)
                frontier.append((v, d + 1))
    return None


def all_shortest_paths(n, edges, e):
    s, t = e
    d = graph_dist(n, edges, e)
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    out = []

    def dfs(u, path):
        if len(path) - 1 > d:
            return
        if u == t:
            if len(path) - 1 == d:
                out.append(tuple(path))
            return
        for v in adj[u]:
            if v not in path:
                dfs(v, path + [v])

    dfs(s, [s])
    return out


def wvals(x):
    return [F(1, 1) / (u * (1 - u)) for u in x]


def expected_diag_coeff(n, x, weights, target):
    edges = list(weights)
    ws = wvals(x)
    total = F(0)
    for path in all_shortest_paths(n, edges, target):
        prod = F(1)
        for v in path:
            prod *= ws[v]
        for a, b in zip(path, path[1:]):
            prod *= weights[tuple(sorted((a, b)))] ** 2
        total += prod
    return -6 * total


def hessian_case(name, n, x, weights, targets, expected, cap_total):
    marker_caps = [2] if len(targets) == 1 else [1, 1]
    H = entropy_series(n, x, weights, targets, cap_total, marker_caps)
    orders = [2] if len(targets) == 1 else [1, 1]
    series = derivative_eps_series(H, orders)
    return {
        "name": name,
        "n": n,
        "targets": [list(e) for e in targets],
        "support_edges": [list(e) for e in weights],
        "distances": [graph_dist(n, list(weights), e) for e in targets],
        "series": {str(k): str(v) for k, v in sorted(series.items())},
        "expected": {str(k): str(v) for k, v in expected.items()},
        "pass": all(series.get(k, F(0)) == v for k, v in expected.items()),
    }


def matching_poly_cycle(m):
    out = {0: F(1)}
    for mask in range(1, 1 << m):
        if any((mask >> i) & 1 and (mask >> ((i + 1) % m)) & 1 for i in range(m)):
            continue
        out[mask] = F(-1 if mask.bit_count() % 2 else 1)
    return out


def cycle_matching_coeff(m):
    M = matching_poly_cycle(m)
    R = {k: v for k, v in M.items() if k}
    power = {0: F(1)}
    target = (1 << m) - 1
    coeff = F(0)
    ledger = []
    # f(M)=-M log M = -R -R^2/2+R^3/6-...
    for k in range(1, m + 1):
        nxt = {}
        for a, ca in power.items():
            for b, cb in R.items():
                if a & b:
                    continue
                put(nxt, a | b, ca * cb)
        power = nxt
        mult = F(-1) if k == 1 else F((-1) ** (k + 1), k * (k - 1))
        raw = power.get(target, F(0))
        coeff += mult * raw
        ledger.append({"k": k, "raw": str(raw), "contribution": str(mult * raw)})
    return {"m": m, "matching_part": str(coeff), "full_with_oriented_q2": str(coeff - 2), "pass": coeff == -1, "ledger": ledger}


def exact_event_gate():
    n = 4
    x = [F(1, 5), F(1, 3), F(3, 5), F(4, 5)]
    off = {
        (0, 1): F(1, 50),
        (0, 2): F(-1, 60),
        (0, 3): F(1, 70),
        (1, 2): F(1, 80),
        (1, 3): F(-1, 90),
        (2, 3): F(1, 100),
    }
    K = [[F(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        K[i][i] = x[i]
    for (i, j), v in off.items():
        K[i][j] = K[j][i] = v
    shifted = []
    mobius = []
    positive = True
    for mask in range(1 << n):
        S = frozenset(i for i in range(n) if mask >> i & 1)
        p_m = atom_mobius_numeric(n, K, S)
        mat = []
        for i in range(n):
            row = []
            for j in range(n):
                if i == j:
                    row.append({(0,): K[i][i] if i in S else K[i][i] - 1})
                else:
                    row.append({(0,): K[i][j]})
            mat.append(row)
        p_s = det_poly(mat)
        if (n - len(S)) % 2:
            p_s = scale_poly(p_s, F(-1))
        val_s = p_s.get((0,), F(0))
        shifted.append(str(val_s))
        mobius.append(str(p_m))
        positive = positive and p_m > 0
    return {
        "n": n,
        "atoms": 1 << n,
        "shifted_equals_mobius": shifted == mobius,
        "sum_atoms": str(sum(F(v) for v in mobius)),
        "all_atoms_positive": positive,
    }


def main():
    start = time.time()
    hashes = {}
    for name in [
        "frozen_claim.md",
        "proof_candidate.md",
        "hazards.md",
        "verdict.md",
        "run_log.md",
        "general_sanity.py",
        "sanity_results.json",
    ]:
        data = (ROUTE / name).read_bytes()
        hashes[name] = {"sha256": hashlib.sha256(data).hexdigest().upper(), "bytes": len(data)}

    cycles = [cycle_matching_coeff(m) for m in range(3, 9)]

    cases = []
    x5 = [F(1, 5), F(1, 3), F(2, 5), F(3, 5), F(4, 5)]
    p5 = {(0, 1): F(2, 7), (1, 2): F(-3, 8), (2, 3): F(5, 11), (3, 4): F(-7, 13)}
    e04 = (0, 4)
    cases.append(
        hessian_case(
            "P5_endpoint_distance4_diagonal",
            5,
            x5,
            p5,
            [e04],
            {k: F(0) for k in range(8)} | {8: expected_diag_coeff(5, x5, p5, e04)},
            10,
        )
    )
    cases.append(
        hessian_case(
            "P5_same_distance_shared_vertex_cross",
            5,
            x5,
            p5,
            [(0, 2), (2, 4)],
            {k: F(0) for k in range(5)},
            8,
        )
    )
    cases.append(
        hessian_case(
            "P5_same_distance_overlapping_cross",
            5,
            x5,
            p5,
            [(0, 3), (1, 4)],
            {k: F(0) for k in range(7)},
            8,
        )
    )
    x4 = [F(1, 5), F(1, 3), F(3, 5), F(4, 5)]
    c4 = {(0, 1): F(2, 5), (1, 2): F(-3, 7), (2, 3): F(5, 11), (0, 3): F(-7, 13)}
    cases.append(
        hessian_case(
            "C4_two_shortest_paths_diagonal",
            4,
            x4,
            c4,
            [(0, 2)],
            {k: F(0) for k in range(4)} | {4: expected_diag_coeff(4, x4, c4, (0, 2))},
            6,
        )
    )
    chord = {(0, 1): F(2, 5), (1, 2): F(-3, 7), (2, 3): F(5, 11), (0, 2): F(4, 9)}
    cases.append(
        hessian_case(
            "Chord_shortens_path_uses_true_geodesic",
            4,
            x4,
            chord,
            [(0, 3)],
            {k: F(0) for k in range(4)} | {4: expected_diag_coeff(4, x4, chord, (0, 3))},
            6,
        )
    )

    first_derivative = hessian_case(
        "P5_endpoint_first_derivative_locality",
        5,
        x5,
        p5,
        [e04],
        {k: F(0) for k in range(9)},
        10,
    )
    # Replace the two-derivative extraction above by a one-derivative extraction.
    H_first = entropy_series(5, x5, p5, [e04], 10, [1])
    series_first = derivative_eps_series(H_first, [1])
    first_derivative["series"] = {str(k): str(v) for k, v in sorted(series_first.items())}
    first_derivative["expected"] = {str(k): "0" for k in range(9)}
    first_derivative["pass"] = all(series_first.get(k, F(0)) == 0 for k in range(9))

    result = {
        "status": "PASS" if all(c["pass"] for c in cycles) and all(c["pass"] for c in cases) and first_derivative["pass"] else "FAIL",
        "author_input_hashes": hashes,
        "exact_event_gate": exact_event_gate(),
        "cycle_coefficients": cycles,
        "hessian_scout_cases": cases,
        "first_derivative_scout": first_derivative,
        "elapsed_seconds": time.time() - start,
        "scope": "finite exact Fraction sanity only; not a proof of the general theorem",
    }
    out = HERE / "fresh_u7_audit.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
