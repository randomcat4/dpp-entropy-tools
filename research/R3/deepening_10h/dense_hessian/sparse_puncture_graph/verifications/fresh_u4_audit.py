"""Fresh non-author audit for D10-U4 sparse puncture graph.

This script intentionally does not import the author's sanity.py.  It rebuilds
exact-event atoms from inclusion determinants by Mobius inversion and checks the
low-degree entropy jets with rational arithmetic.
"""

from __future__ import annotations

import hashlib
import json
import re
import time
from fractions import Fraction
from itertools import combinations, permutations
from pathlib import Path


ROOT = Path(__file__).resolve().parents[6]
TARGET = ROOT / "research" / "R3" / "deepening_10h" / "dense_hessian" / "sparse_puncture_graph"
OUT = TARGET / "verifications" / "fresh_u4_audit.json"


F = Fraction


def clean(poly):
    return {e: c for e, c in poly.items() if c}


def pzero(dim):
    return {}


def pone(dim):
    return {(0,) * dim: F(1)}


def pconst(dim, c):
    return {} if c == 0 else {(0,) * dim: F(c)}


def pvar(dim, i, c=F(1)):
    e = [0] * dim
    e[i] = 1
    return {tuple(e): F(c)}


def padd(*polys):
    out = {}
    for poly in polys:
        for e, c in poly.items():
            out[e] = out.get(e, F(0)) + c
    return clean(out)


def pscale(poly, c):
    c = F(c)
    if c == 0:
        return {}
    return clean({e: c * v for e, v in poly.items()})


def pmul(a, b, cap):
    out = {}
    for ea, ca in a.items():
        for eb, cb in b.items():
            e = tuple(x + y for x, y in zip(ea, eb))
            if sum(e) <= cap:
                out[e] = out.get(e, F(0)) + ca * cb
    return clean(out)


def det_poly(mat, dim, cap):
    m = len(mat)
    if m == 0:
        return pone(dim)
    out = pzero(dim)
    for perm in permutations(range(m)):
        inv = sum(1 for i in range(m) for j in range(i + 1, m) if perm[i] > perm[j])
        term = pconst(dim, -1 if inv % 2 else 1)
        for i, j in enumerate(perm):
            term = pmul(term, mat[i][j], cap)
            if not term:
                break
        out = padd(out, term)
    return out


def all_edges(n):
    return list(combinations(range(n), 2))


def atom_polys(theta, edge_expr, dim, cap):
    """Exact atoms from p(S)=sum_{T superset S} (-1)^{|T|-|S|} det K_T."""
    n = len(theta)
    zero = (0,) * dim
    K = [[pzero(dim) for _ in range(n)] for __ in range(n)]
    for i in range(n):
        K[i][i] = pconst(dim, theta[i])
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
                sign = -1 if ((sup.bit_count() - mask.bit_count()) % 2) else 1
                terms.append(pscale(inc[sup], sign))
        probs.append(padd(*terms))

    mass = padd(*probs)
    assert mass == {zero: F(1)}, mass
    for i, xi in enumerate(theta):
        marg = padd(*(p for mask, p in enumerate(probs) if (mask >> i) & 1))
        assert marg == {zero: xi}, (i, marg, xi)
    return probs


def base_atom(theta, mask):
    out = F(1)
    for i, x in enumerate(theta):
        out *= x if ((mask >> i) & 1) else (1 - x)
    return out


def entropy_offset_series(theta, probs, dim, cap):
    """Series for H(X+Z)-H(X), after exact mass/singleton cancellation.

    Since log a_S is affine in the singleton indicators, the atom mass and
    singleton identities checked above kill the linear log-a term exactly.
    """
    out = pzero(dim)
    zero = (0,) * dim
    for mask, p in enumerate(probs):
        a = base_atom(theta, mask)
        assert p.get(zero, F(0)) == a
        r = pscale(padd(p, {zero: -a}), F(1, 1) / a)
        if not r:
            continue
        assert all(sum(e) >= 2 for e in r), r
        power = pone(dim)
        for k in range(1, cap + 1):
            power = pmul(power, r, cap)
            if not power:
                break
            if k == 1:
                continue
            coeff = F((-1) ** (k + 1), k * (k - 1))
            out = padd(out, pscale(power, a * coeff))
    return out


def degree_part(poly, degree):
    return {e: c for e, c in poly.items() if sum(e) == degree}


def truncate_degrees(poly, degrees):
    degrees = set(degrees)
    return {e: c for e, c in poly.items() if sum(e) in degrees}


def expected_degree_4_6(theta):
    n = len(theta)
    edges = all_edges(n)
    dim = len(edges)
    zero = [0] * dim
    w = [F(1, 1) / (x * (1 - x)) for x in theta]
    t = [(1 - 2 * x) / (x * x * (1 - x) * (1 - x)) for x in theta]
    expected = {}
    for k, (i, j) in enumerate(edges):
        e4 = zero.copy()
        e4[k] = 4
        expected[tuple(e4)] = -w[i] * w[j] / 2
        if t[i] * t[j]:
            e6 = zero.copy()
            e6[k] = 6
            expected[tuple(e6)] = -t[i] * t[j] / 6
    for i, j, k in combinations(range(n), 3):
        et = zero.copy()
        for pair in ((i, j), (i, k), (j, k)):
            et[edges.index(pair)] = 2
        expected[tuple(et)] = expected.get(tuple(et), F(0)) - 3 * w[i] * w[j] * w[k]
    return clean(expected)


def encode_fraction(x):
    return str(x)


def encode_poly(poly):
    return [
        {"exponents": list(e), "coefficient": str(c)}
        for e, c in sorted(poly.items())
    ]


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_run_log_hashes():
    text = (TARGET / "run_log.md").read_text(encoding="utf-8")
    script = re.search(r"Script SHA256:\s*\n`([0-9a-f]+)`", text)
    result = re.search(r"Result SHA256:\s*\n`([0-9a-f]+)`", text)
    return {
        "script_sha256_in_log": script.group(1) if script else None,
        "result_sha256_in_log": result.group(1) if result else None,
        "script_sha256_actual": sha256(TARGET / "sanity.py"),
        "result_sha256_actual": sha256(TARGET / "sanity_results.json"),
    }


def check_general_jets():
    centers = [
        (F(1, 3), F(3, 5)),
        (F(1, 5), F(2, 5), F(4, 5)),
        (F(1, 5), F(1, 3), F(3, 5), F(3, 4)),
    ]
    records = []
    atoms_total = 0
    for theta in centers:
        n = len(theta)
        edges = all_edges(n)
        dim = len(edges)
        edge_expr = {edge: pvar(dim, k) for k, edge in enumerate(edges)}
        probs = atom_polys(theta, edge_expr, dim, 6)
        atoms_total += len(probs)
        ent = entropy_offset_series(theta, probs, dim, 6)
        expected = expected_degree_4_6(theta)
        low = truncate_degrees(ent, {4, 5, 6})
        if low != expected:
            raise AssertionError(
                {"n": n, "actual": encode_poly(low), "expected": encode_poly(expected)}
            )
        records.append(
            {
                "n": n,
                "theta": [str(x) for x in theta],
                "atom_polynomials": len(probs),
                "all_degree_5_coefficients_zero": degree_part(ent, 5) == {},
                "degree_4_6_formula_matches": True,
                "nonzero_degree_4_6_terms": len(expected),
            }
        )
    return records, atoms_total


def check_n3_path():
    theta = (F(1, 5), F(2, 5), F(4, 5))
    w = [F(1, 1) / (x * (1 - x)) for x in theta]
    a = F(2, 5)
    b = -F(3, 7)
    dim = 2
    eps = 0
    y = 1

    def expr_eps(c):
        return pvar(dim, eps, c)

    def expr_y():
        return pvar(dim, y)

    # Supported edge 01 perturbation: z01=a*eps+y, z12=b*eps.
    edge_expr = {
        (0, 1): padd(expr_eps(a), expr_y()),
        (1, 2): expr_eps(b),
    }
    ent = entropy_offset_series(theta, atom_polys(theta, edge_expr, dim, 6), dim, 6)
    supp01 = 2 * ent.get((2, 2), F(0))
    # Supported edge 12 perturbation: z01=a*eps, z12=b*eps+y.
    edge_expr = {
        (0, 1): expr_eps(a),
        (1, 2): padd(expr_eps(b), expr_y()),
    }
    ent = entropy_offset_series(theta, atom_polys(theta, edge_expr, dim, 6), dim, 6)
    supp12 = 2 * ent.get((2, 2), F(0))
    # Missing edge 02 perturbation: z01=a*eps, z12=b*eps, z02=y.
    edge_expr = {
        (0, 1): expr_eps(a),
        (1, 2): expr_eps(b),
        (0, 2): expr_y(),
    }
    ent = entropy_offset_series(theta, atom_polys(theta, edge_expr, dim, 6), dim, 6)
    miss02 = 2 * ent.get((4, 2), F(0))
    expected_supp01 = -6 * w[0] * w[1] * a * a
    expected_supp12 = -6 * w[1] * w[2] * b * b
    expected_miss02 = -6 * w[0] * w[1] * w[2] * a * a * b * b
    assert supp01 == expected_supp01
    assert supp12 == expected_supp12
    assert miss02 == expected_miss02
    return {
        "theta": [str(x) for x in theta],
        "weights": {"A01": str(a), "A12": str(b)},
        "supported_epsilon2_coefficients": [str(supp01), str(supp12)],
        "missing_epsilon4_coefficient": str(miss02),
    }


def check_disconnected_single_edge():
    theta = (F(1, 5), F(2, 5), F(4, 5))
    dim = 2
    edge_expr = {
        (0, 1): pvar(dim, 0, F(2, 5)),  # present within component
        (0, 2): pvar(dim, 1, F(1)),  # tested cross-component direction
    }
    probs = atom_polys(theta, edge_expr, dim, 6)
    first_cross_coefficients = []
    for mask, p in enumerate(probs):
        for e, c in p.items():
            if e[1] == 1:
                first_cross_coefficients.append((mask, e, c))
    assert first_cross_coefficients == []

    block_checks = []
    for block in [(0, 1), (2,)]:
        for block_bits in range(1 << len(block)):
            marginal = pzero(dim)
            for mask, p in enumerate(probs):
                ok = True
                for local, vertex in enumerate(block):
                    if ((mask >> vertex) & 1) != ((block_bits >> local) & 1):
                        ok = False
                        break
                if ok:
                    marginal = padd(marginal, p)
            cross_terms = {e: c for e, c in marginal.items() if e[1] > 0}
            assert cross_terms == {}, (block, block_bits, cross_terms)
            block_checks.append({"block": block, "event": block_bits, "cross_variable_terms": 0})
    return {
        "theta": [str(x) for x in theta],
        "present_edge": [0, 1],
        "cross_component_test_edge": [0, 2],
        "atom_polynomials": len(probs),
        "all_exact_atom_first_cross_derivatives_zero": True,
        "all_block_marginals_constant_in_cross_variable": True,
        "checked_block_events": len(block_checks),
    }


def check_p4_endpoint_scout():
    theta = (F(1, 5), F(1, 3), F(3, 5), F(3, 4))
    weights = (F(1, 3), -F(2, 5), F(3, 7))
    dim = 2
    edge_expr = {
        (0, 1): pvar(dim, 0, weights[0]),
        (1, 2): pvar(dim, 0, weights[1]),
        (2, 3): pvar(dim, 0, weights[2]),
        (0, 3): pvar(dim, 1),
    }
    probs = atom_polys(theta, edge_expr, dim, 8)
    ent = entropy_offset_series(theta, probs, dim, 8)
    missing_curvature = {e[0]: 2 * c for e, c in ent.items() if e[1] == 2}
    expected = F(-6)
    for x in theta:
        expected *= F(1, 1) / (x * (1 - x))
    for a in weights:
        expected *= a * a
    assert missing_curvature == {6: expected}
    return {
        "status": "SCOUT_ONLY_ONE_ENTRY_NOT_FULL_HESSIAN",
        "theta": [str(x) for x in theta],
        "path_weights": [str(a) for a in weights],
        "missing_edge": [0, 3],
        "atom_polynomials": len(probs),
        "missing_curvature_by_epsilon_power": {str(k): str(v) for k, v in missing_curvature.items()},
    }


def compare_author_json(fresh):
    author = json.loads((TARGET / "sanity_results.json").read_text(encoding="utf-8"))
    comparisons = {
        "author_exit_code_zero": author.get("exit_code") == 0,
        "author_counts_match_log_denominator": author.get("counts")
        == {
            "general_centers": 3,
            "general_atom_polynomials": 28,
            "single_edge_atom_polynomials": 8,
            "long_path_atom_polynomials": 16,
            "total_atom_polynomials": 52,
            "random_draws": 0,
            "failed_checks": 0,
        },
        "fresh_general_atom_total_matches_author": fresh["counts"]["general_atom_polynomials"] == 28,
        "fresh_total_atom_denominator_matches_author": fresh["counts"]["total_atom_polynomials"] == 52,
        "n3_path_coefficients_match_author": author["n3_path"][
            "supported_hessian_epsilon2_coefficients"
        ]
        == fresh["n3_path"]["supported_epsilon2_coefficients"]
        and author["n3_path"]["missing_hessian_epsilon4_coefficient"]
        == fresh["n3_path"]["missing_epsilon4_coefficient"],
        "p4_missing_curvature_matches_author": author["n4_long_path"][
            "missing_curvature_through_epsilon6"
        ]
        == fresh["n4_p4_endpoint_scout"]["missing_curvature_by_epsilon_power"],
    }
    if not all(comparisons.values()):
        raise AssertionError(comparisons)
    return comparisons


def main():
    start = time.time()
    general, general_atoms = check_general_jets()
    n3_path = check_n3_path()
    disconnected = check_disconnected_single_edge()
    p4 = check_p4_endpoint_scout()
    hashes = parse_run_log_hashes()
    fresh = {
        "status": "PASS",
        "scope": "fresh non-author rational exact-event checks plus analytic proof audit; no author module imported",
        "hashes": hashes,
        "general_jets": general,
        "n3_path": n3_path,
        "n3_disconnected_single_edge": disconnected,
        "n4_p4_endpoint_scout": p4,
        "counts": {
            "general_centers": 3,
            "general_atom_polynomials": general_atoms,
            "single_edge_atom_polynomials": disconnected["atom_polynomials"],
            "long_path_atom_polynomials": p4["atom_polynomials"],
            "total_atom_polynomials": general_atoms
            + disconnected["atom_polynomials"]
            + p4["atom_polynomials"],
            "random_draws": 0,
            "failed_checks": 0,
        },
        "analytic_audit_flags": {
            "f5_zero": "verified by character parity/orthogonality and by exact rational n=2,3,4 jets",
            "f6_two_classes": "verified by edge-triple incidence classification and exact rational n=2,3,4 jets",
            "diameter_two_missing_block": "common-neighbor coefficient -6*w_i*w_j*w_k*A_ik^2*A_jk^2 per witness",
            "p4_probe": "scout only; not used for general connected support",
        },
        "elapsed_seconds": None,
        "script_sha256": None,
    }
    fresh["author_comparisons"] = compare_author_json(fresh)
    fresh["elapsed_seconds"] = time.time() - start
    fresh["script_sha256"] = sha256(Path(__file__))
    OUT.write_text(json.dumps(fresh, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "counts": fresh["counts"], "hashes": hashes}, indent=2))


if __name__ == "__main__":
    main()
