"""D10-U5 connected puncture distance exploration.

Author-side exploratory code.  It uses exact-event Mobius atoms and rational
formal entropy series for the P4 leading Hessian calculation.  The n<=5
floating checks at the end are scout-only and are not used as proof.
"""

from __future__ import annotations

import hashlib
import itertools as it
import json
import math
import time
from collections import deque
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "scout_results.json"
F = Fraction


def clean(poly):
    return {e: c for e, c in poly.items() if c}


def padd(*polys):
    out = {}
    for p in polys:
        for e, c in p.items():
            out[e] = out.get(e, F(0)) + c
    return clean(out)


def pscale(p, c):
    c = F(c)
    if c == 0:
        return {}
    return clean({e: c * v for e, v in p.items()})


def pmul(a, b, cap):
    out = {}
    for ea, ca in a.items():
        for eb, cb in b.items():
            e = tuple(x + y for x, y in zip(ea, eb))
            if sum(e) <= cap:
                out[e] = out.get(e, F(0)) + ca * cb
    return clean(out)


def pconst(dim, c):
    c = F(c)
    return {} if c == 0 else {(0,) * dim: c}


def pvar(dim, k, c=F(1)):
    e = [0] * dim
    e[k] = 1
    return {tuple(e): F(c)}


def det_poly(mat, dim, cap):
    n = len(mat)
    if n == 0:
        return pconst(dim, 1)
    out = {}
    for perm in it.permutations(range(n)):
        inv = sum(1 for i in range(n) for j in range(i + 1, n) if perm[i] > perm[j])
        term = pconst(dim, -1 if inv % 2 else 1)
        for i, j in enumerate(perm):
            term = pmul(term, mat[i][j], cap)
            if not term:
                break
        out = padd(out, term)
    return out


def all_edges(n):
    return list(it.combinations(range(n), 2))


def atom_polys(theta, edge_expr, dim, cap):
    n = len(theta)
    zero = (0,) * dim
    K = [[{} for _ in range(n)] for __ in range(n)]
    for i, x in enumerate(theta):
        K[i][i] = pconst(dim, x)
    for (i, j), expr in edge_expr.items():
        K[i][j] = expr
        K[j][i] = expr
    inc = []
    for mask in range(1 << n):
        ids = [i for i in range(n) if (mask >> i) & 1]
        inc.append(det_poly([[K[i][j] for j in ids] for i in ids], dim, cap))
    probs = []
    for mask in range(1 << n):
        terms = []
        for sup in range(1 << n):
            if sup & mask == mask:
                sign = -1 if ((sup.bit_count() - mask.bit_count()) & 1) else 1
                terms.append(pscale(inc[sup], sign))
        probs.append(padd(*terms))
    assert padd(*probs) == {zero: F(1)}
    for i, x in enumerate(theta):
        marg = padd(*(p for mask, p in enumerate(probs) if (mask >> i) & 1))
        assert marg == {zero: x}
    return probs


def base_atom(theta, mask):
    p = F(1)
    for i, x in enumerate(theta):
        p *= x if ((mask >> i) & 1) else (1 - x)
    return p


def entropy_offset_series(theta, probs, dim, cap):
    """Formal series of H(diag(theta)+Z)-H(diag(theta)) through total degree cap."""
    zero = (0,) * dim
    out = {}
    for mask, p in enumerate(probs):
        a = base_atom(theta, mask)
        assert p.get(zero, F(0)) == a
        r = pscale(padd(p, {zero: -a}), F(1, 1) / a)
        if not r:
            continue
        assert all(sum(e) >= 2 for e in r)
        power = pconst(dim, 1)
        for k in range(1, cap + 1):
            power = pmul(power, r, cap)
            if not power:
                break
            if k == 1:
                continue
            coeff = F((-1) ** (k + 1), k * (k - 1))
            out = padd(out, pscale(power, a * coeff))
    return out


def second_derivative_poly(poly, a, b):
    out = {}
    for e, c in poly.items():
        ea = e[a]
        eb = e[b]
        if a == b:
            if ea < 2:
                continue
            factor = ea * (ea - 1)
            ne = list(e)
            ne[a] -= 2
        else:
            if ea < 1 or eb < 1:
                continue
            factor = ea * eb
            ne = list(e)
            ne[a] -= 1
            ne[b] -= 1
        out[tuple(ne)] = out.get(tuple(ne), F(0)) + c * factor
    return clean(out)


def evaluate_at_path_base(poly, edge_list, support_weights):
    """Substitute z_e=weight_e*eps for support edges and z_e=0 otherwise."""
    series = {}
    for exp, c in poly.items():
        deg = 0
        coeff = c
        ok = True
        for k, power in enumerate(exp):
            edge = edge_list[k]
            if power == 0:
                continue
            if edge not in support_weights:
                ok = False
                break
            deg += power
            coeff *= support_weights[edge] ** power
        if ok:
            series[deg] = series.get(deg, F(0)) + coeff
    return {d: c for d, c in sorted(series.items()) if c}


def shortest_distances(n, support_edges):
    adj = [[] for _ in range(n)]
    for i, j in support_edges:
        adj[i].append(j)
        adj[j].append(i)
    dist = {}
    for s in range(n):
        q = deque([s])
        seen = {s: 0}
        while q:
            u = q.popleft()
            for v in adj[u]:
                if v not in seen:
                    seen[v] = seen[u] + 1
                    q.append(v)
        for t, d in seen.items():
            if s < t:
                dist[(s, t)] = d
    return dist


def leading(series):
    if not series:
        return None
    d = min(series)
    return d, series[d]


def p4_exact_scaled_offdiag():
    theta = (F(1, 5), F(1, 3), F(3, 5), F(3, 4))
    n = 4
    edges = all_edges(n)
    dim = len(edges)
    edge_expr = {e: pvar(dim, k) for k, e in enumerate(edges)}
    probs = atom_polys(theta, edge_expr, dim, 8)
    ent = entropy_offset_series(theta, probs, dim, 8)
    support = {(0, 1): F(1, 3), (1, 2): -F(2, 5), (2, 3): F(3, 7)}
    dist = shortest_distances(n, support.keys())
    leading_entries = {}
    scaled_constant = [[F(0) for _ in edges] for __ in edges]
    bad_orders = []
    for a, ea in enumerate(edges):
        for b, eb in enumerate(edges):
            hp = second_derivative_poly(ent, a, b)
            series = evaluate_at_path_base(hp, edges, support)
            lead = leading(series)
            expected_scale = dist[ea] + dist[eb]
            leading_entries[f"{ea}-{eb}"] = {
                "series": {str(k): str(v) for k, v in series.items()},
                "distance_sum": expected_scale,
                "leading": None if lead is None else [lead[0], str(lead[1])],
            }
            if lead is not None:
                if lead[0] < expected_scale:
                    bad_orders.append((ea, eb, lead, expected_scale))
                if lead[0] == expected_scale:
                    scaled_constant[a][b] = lead[1]
    assert not bad_orders, bad_orders
    expected_diag = {
        (0, 1): -6
        * (F(1, 1) / (theta[0] * (1 - theta[0])))
        * (F(1, 1) / (theta[1] * (1 - theta[1])))
        * support[(0, 1)] ** 2,
        (1, 2): -6
        * (F(1, 1) / (theta[1] * (1 - theta[1])))
        * (F(1, 1) / (theta[2] * (1 - theta[2])))
        * support[(1, 2)] ** 2,
        (2, 3): -6
        * (F(1, 1) / (theta[2] * (1 - theta[2])))
        * (F(1, 1) / (theta[3] * (1 - theta[3])))
        * support[(2, 3)] ** 2,
        (0, 2): -6
        * math.prod(F(1, 1) / (theta[i] * (1 - theta[i])) for i in (0, 1, 2))
        * support[(0, 1)] ** 2
        * support[(1, 2)] ** 2,
        (1, 3): -6
        * math.prod(F(1, 1) / (theta[i] * (1 - theta[i])) for i in (1, 2, 3))
        * support[(1, 2)] ** 2
        * support[(2, 3)] ** 2,
        (0, 3): -6
        * math.prod(F(1, 1) / (theta[i] * (1 - theta[i])) for i in (0, 1, 2, 3))
        * support[(0, 1)] ** 2
        * support[(1, 2)] ** 2
        * support[(2, 3)] ** 2,
    }
    for k, e in enumerate(edges):
        assert scaled_constant[k][k] == expected_diag[e], (e, scaled_constant[k][k], expected_diag[e])
    for a in range(len(edges)):
        for b in range(len(edges)):
            if a != b:
                assert scaled_constant[a][b] == 0, (edges[a], edges[b], scaled_constant[a][b])
    return {
        "theta": [str(x) for x in theta],
        "support_weights": {str(k): str(v) for k, v in support.items()},
        "edge_order": [str(e) for e in edges],
        "graph_distance_by_edge": {str(e): dist[e] for e in edges},
        "scaled_constant_matrix": [[str(x) for x in row] for row in scaled_constant],
        "expected_diagonal_constants": {str(k): str(v) for k, v in expected_diag.items()},
        "leading_entries": leading_entries,
        "atom_polynomials": len(probs),
        "entropy_terms_through_degree_8": len(ent),
    }


def offdiag_entropy_polynomial(theta, cap):
    n = len(theta)
    edges = all_edges(n)
    dim = len(edges)
    edge_expr = {e: pvar(dim, k) for k, e in enumerate(edges)}
    probs = atom_polys(theta, edge_expr, dim, cap)
    ent = entropy_offset_series(theta, probs, dim, cap)
    return edges, ent, len(probs)


def scaled_constant_matrix_from_entropy(edges, ent, support):
    n = max(max(e) for e in edges) + 1
    dist = shortest_distances(n, support.keys())
    matrix = [[F(0) for _ in edges] for __ in edges]
    bad_orders = []
    for a, ea in enumerate(edges):
        for b, eb in enumerate(edges):
            hp = second_derivative_poly(ent, a, b)
            series = evaluate_at_path_base(hp, edges, support)
            lead = leading(series)
            scale = dist[ea] + dist[eb]
            if lead is not None:
                if lead[0] < scale:
                    bad_orders.append((ea, eb, lead, scale))
                if lead[0] == scale:
                    matrix[a][b] = lead[1]
    if bad_orders:
        raise AssertionError(bad_orders)
    return matrix, dist


def positive_definite_ldl_pivots(mat):
    n = len(mat)
    L = [[F(0) for _ in range(n)] for __ in range(n)]
    D = [F(0) for _ in range(n)]
    for i in range(n):
        L[i][i] = F(1)
        diag = mat[i][i] - sum(L[i][k] * L[i][k] * D[k] for k in range(i))
        if diag <= 0:
            return False, D[:i] + [diag]
        D[i] = diag
        for j in range(i + 1, n):
            num = mat[j][i] - sum(L[j][k] * L[i][k] * D[k] for k in range(i))
            L[j][i] = num / diag
    return True, D


def n4_all_connected_scaled_matrix_scout():
    theta = (F(1, 5), F(1, 3), F(3, 5), F(3, 4))
    edges, ent, atoms = offdiag_entropy_polynomial(theta, 8)
    records = []
    for salt, chosen in enumerate(connected_graphs(4)):
        support = {edge: deterministic_weight(edge, salt) for edge in chosen}
        matrix, dist = scaled_constant_matrix_from_entropy(edges, ent, support)
        ok, pivots = positive_definite_ldl_pivots([[-x for x in row] for row in matrix])
        assert ok, (chosen, matrix, pivots)
        records.append(
            {
                "support_edges": [str(e) for e in chosen],
                "diameter": max(dist.values()),
                "ldl_pivots_of_negative_scaled_matrix": [str(p) for p in pivots],
            }
        )
    return {
        "status": "EXACT_N4_ALL_CONNECTED_OFFDIAG_SCALED_CONSTANT_SCOUT",
        "theta": [str(x) for x in theta],
        "edge_order": [str(e) for e in edges],
        "connected_labeled_graphs": len(records),
        "atom_polynomials_per_graph_model": atoms,
        "all_negative_definite_by_fraction_ldl": True,
        "records": records,
    }


def simple_paths_of_length(n, support_edges, start, stop, length):
    adj = [[] for _ in range(n)]
    for i, j in support_edges:
        adj[i].append(j)
        adj[j].append(i)
    out = []

    def dfs(u, path):
        if len(path) - 1 == length:
            if u == stop:
                out.append(tuple(path))
            return
        for v in adj[u]:
            if v not in path:
                dfs(v, path + [v])

    dfs(start, [start])
    return out


def canonical_edge(i, j):
    return (i, j) if i < j else (j, i)


def two_variable_curvature_leading(n, theta, support_weights, target):
    """Exact y-y curvature leading series at z_support=eps*A, z_target += y."""
    target = canonical_edge(*target)
    dist = shortest_distances(n, support_weights.keys())[target]
    cap = 2 * dist + 2
    dim = 2
    edge_expr = {}
    for edge, weight in support_weights.items():
        edge_expr[edge] = pvar(dim, 0, weight)
    if target in edge_expr:
        edge_expr[target] = padd(edge_expr[target], pvar(dim, 1))
    else:
        edge_expr[target] = pvar(dim, 1)
    probs = atom_polys(theta, edge_expr, dim, cap)
    ent = entropy_offset_series(theta, probs, dim, cap)
    curvature = {e[0]: 2 * c for e, c in ent.items() if e[1] == 2}
    lead = leading(curvature)

    w = [F(1, 1) / (x * (1 - x)) for x in theta]
    expected = F(0)
    for path in simple_paths_of_length(n, support_weights.keys(), target[0], target[1], dist):
        term = F(1)
        for v in path:
            term *= w[v]
        for a, b in zip(path, path[1:]):
            term *= support_weights[canonical_edge(a, b)] ** 2
        expected += term
    expected *= -6
    assert lead is not None, (n, target, curvature)
    assert lead[0] == 2 * dist, (n, target, dist, lead, curvature)
    assert lead[1] == expected, (n, target, dist, lead, expected, curvature)
    return {
        "target": str(target),
        "distance": dist,
        "leading_power": lead[0],
        "leading_coefficient": str(lead[1]),
        "shortest_paths": [str(p) for p in simple_paths_of_length(n, support_weights.keys(), target[0], target[1], dist)],
        "atom_polynomials": len(probs),
    }


def deterministic_weight(edge, salt):
    i, j = edge
    raw = ((i + 1) * 11 + (j + 1) * 7 + salt * 5) % 23 - 11
    if raw == 0:
        raw = 9
    return F(raw, 29)


def exact_distance_coefficient_scout():
    """Finite exact scout for the proposed distance-2d leading diagonal rule."""
    n4_theta = (F(1, 5), F(1, 3), F(3, 5), F(3, 4))
    n4_cases = []
    for salt, chosen in enumerate(connected_graphs(4)):
        support = {edge: deterministic_weight(edge, salt) for edge in chosen}
        targets = [
            two_variable_curvature_leading(4, n4_theta, support, edge)
            for edge in all_edges(4)
        ]
        n4_cases.append({"support_edges": [str(e) for e in chosen], "targets": targets})

    n5_theta = (F(1, 5), F(1, 3), F(2, 5), F(3, 5), F(3, 4))
    n5_graphs = [
        {
            "name": "P5_path_diameter_4",
            "edges": [(0, 1), (1, 2), (2, 3), (3, 4)],
            "weights": [F(1, 3), -F(2, 5), F(3, 7), -F(4, 11)],
        },
        {
            "name": "C5_cycle",
            "edges": [(0, 1), (1, 2), (2, 3), (3, 4), (0, 4)],
            "weights": [F(1, 3), -F(2, 5), F(3, 7), -F(4, 11), F(5, 13)],
        },
        {
            "name": "diameter_3_branched_tree",
            "edges": [(0, 1), (1, 2), (2, 3), (2, 4)],
            "weights": [F(2, 7), -F(3, 8), F(4, 9), -F(5, 11)],
        },
        {
            "name": "diameter_2_K23",
            "edges": [(0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4)],
            "weights": [F(1, 7), -F(2, 9), F(3, 11), -F(4, 13), F(5, 17), -F(6, 19)],
        },
    ]
    n5_cases = []
    for case in n5_graphs:
        support = {edge: weight for edge, weight in zip(case["edges"], case["weights"])}
        targets = [
            two_variable_curvature_leading(5, n5_theta, support, edge)
            for edge in all_edges(5)
        ]
        n5_cases.append({"name": case["name"], "support_edges": [str(e) for e in case["edges"]], "targets": targets})

    return {
        "status": "EXACT_TWO_VARIABLE_SCOUT_FOR_DIAGONAL_COORDINATE_LEADING_TERMS",
        "rule_checked": "-6 * sum over shortest paths P of prod_{v in P} w_v * prod_{e in P} A_e^2 at epsilon^(2 distance)",
        "n4_all_connected_labeled_graphs": len(n4_cases),
        "n4_total_pair_targets": sum(len(c["targets"]) for c in n4_cases),
        "n5_selected_graphs": n5_cases,
    }


def connected_graphs(n):
    edges = all_edges(n)
    for bits in range(1, 1 << len(edges)):
        chosen = [edges[k] for k in range(len(edges)) if (bits >> k) & 1]
        dist = shortest_distances(n, chosen)
        if len(dist) == n * (n - 1) // 2:
            yield chosen


def scout_numeric_connected():
    rng = np.random.default_rng(20260908)
    cases = []
    for n in (4, 5):
        theta = np.linspace(0.22, 0.78, n)
        count = 0
        positive = 0
        worst = -1e100
        worst_case = None
        for chosen in connected_graphs(n):
            if count >= (40 if n == 4 else 60):
                break
            A = np.zeros((n, n))
            for idx, (i, j) in enumerate(chosen):
                raw = ((idx * 37 + n * 11) % 17) - 8
                if raw == 0:
                    raw = 5
                val = raw / 23.0
                A[i, j] = A[j, i] = val
            # Two additional random sign/weight perturbations for nontrivial cancellation scouts.
            if count % 7 == 0:
                for i, j in chosen:
                    A[i, j] = A[j, i] = rng.choice([-1.0, 1.0]) * rng.uniform(0.08, 0.5)
            eps = 2e-3
            K = np.diag(theta) + eps * A
            eig = np.linalg.eigvalsh(K)
            if eig[0] <= 0 or eig[-1] >= 1:
                continue
            H = numeric_hessian(K, h=2e-5)
            lam_max = float(np.linalg.eigvalsh((H + H.T) / 2)[-1])
            if lam_max >= 0:
                positive += 1
            if lam_max > worst:
                worst = lam_max
                worst_case = {
                    "n": n,
                    "edges": chosen,
                    "lam_max": lam_max,
                    "epsilon": eps,
                    "theta": theta.tolist(),
                    "A_upper": [[i, j, A[i, j]] for i, j in chosen],
                }
            count += 1
        cases.append({"n": n, "tested_connected_graphs": count, "positive_lam_max_count": positive, "worst_case": worst_case})
    return {"status": "SCOUT_FLOAT_FINITE_DIFFERENCE_ONLY", "rng_seed": 20260908, "cases": cases}


def main():
    start = time.time()
    p4 = p4_exact_scaled_offdiag()
    n4_scaled = n4_all_connected_scaled_matrix_scout()
    scout = exact_distance_coefficient_scout()
    report = {
        "status": "AUTHOR_EXPLORATION",
        "p4_exact_scaled_offdiag": p4,
        "n4_all_connected_scaled_matrix_scout": n4_scaled,
        "exact_distance_coefficient_scout": scout,
        "disabled_numeric_note": "Naive full finite-difference Hessians at epsilon=0.002 were discarded: distance-3 and distance-4 curvatures are below double precision noise.",
        "elapsed_seconds": time.time() - start,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "status": report["status"],
                "p4_scaled_diag": p4["expected_diagonal_constants"],
                "n4_scaled": {
                    "connected_labeled_graphs": n4_scaled["connected_labeled_graphs"],
                    "all_negative_definite_by_fraction_ldl": n4_scaled["all_negative_definite_by_fraction_ldl"],
                },
                "scout": scout,
                "elapsed_seconds": report["elapsed_seconds"],
            },
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
