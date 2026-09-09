#!/usr/bin/env python3
"""Independent W1 verification checks.

This script is a bounded verifier artifact. It recomputes selected exact
event identities from determinant definitions and records diagnostics for
the pending rank-two/two-coordinate-column extension. It does not certify
the universal rank-two theorem.
"""
from __future__ import annotations

import json
import math
import os
import platform
import sys
from fractions import Fraction
from itertools import product
from pathlib import Path

import mpmath as mp
import numpy as np
import sympy as sp

R = sp.Rational
t = sp.symbols("t", real=True)

OUT = Path(__file__).resolve().parent / "compute_outputs"
OUT.mkdir(exist_ok=True)


def bits_iter(n: int):
    return list(product((0, 1), repeat=n))


def key(bits) -> str:
    return "".join(str(int(b)) for b in bits)


def event_probs(K: sp.Matrix) -> dict[str, sp.Expr]:
    n = K.rows
    out: dict[str, sp.Expr] = {}
    for bits in bits_iter(n):
        diag = sp.diag(*[1 - b for b in bits])
        out[key(bits)] = sp.factor((-1) ** (n - sum(bits)) * (K - diag).det())
    assert sp.simplify(sum(out.values()) - 1) == 0
    return out


def check_inclusion_exclusion(K: sp.Matrix, p: dict[str, sp.Expr]) -> None:
    n = K.rows
    for bits in bits_iter(n):
        subset = [i for i, b in enumerate(bits) if b]
        moment = K.extract(subset, subset).det() if subset else sp.Integer(1)
        total = sum(value for b, value in p.items() if all(b[i] == "1" for i in subset))
        assert sp.simplify(total - moment) == 0, bits


def probs_from_matrix_numeric(K) -> list[mp.mpf]:
    n = len(K)
    probs = []
    for bits in bits_iter(n):
        M = mp.matrix(K)
        for i, b in enumerate(bits):
            if not b:
                M[i, i] -= 1
        probs.append(((-1) ** (n - sum(bits))) * mp.det(M))
    return probs


def hessian_numeric(K0: sp.Matrix, D: sp.Matrix, at: sp.Rational) -> mp.mpf:
    mp.mp.dps = 80
    n = K0.rows
    p0 = []
    p1 = []
    p2 = []
    event_polys = event_probs(K0 + t * D)
    for bits in bits_iter(n):
        expr = event_polys[key(bits)]
        p0.append(mp.mpf(str(sp.N(expr.subs(t, at), 80))))
        p1.append(mp.mpf(str(sp.N(sp.diff(expr, t).subs(t, at), 80))))
        p2.append(mp.mpf(str(sp.N(sp.diff(expr, t, 2).subs(t, at), 80))))
    assert min(p0) > 0
    return -sum(p2[i] * mp.log(p0[i]) for i in range(len(p0))) - sum(
        p1[i] * p1[i] / p0[i] for i in range(len(p0))
    )


def entropy_numeric_from_sym(K: sp.Matrix) -> mp.mpf:
    mp.mp.dps = 80
    probs = [mp.mpf(str(sp.N(v, 80))) for v in event_probs(K).values()]
    return -sum(p * mp.log(p) for p in probs if p)


def rank_one_certificate() -> dict:
    A = sp.Matrix([[R(2, 5), R(1, 10)], [R(1, 10), R(3, 5)]])
    C = sp.Matrix([[R(1, 3), R(1, 20)], [R(1, 20), R(2, 3)]])
    u = sp.Matrix([R(1, 5), R(1, 10)])
    v = sp.Matrix([1, R(1, 2)])
    B = u * v.T
    K = A.row_join(t * B).col_join((t * B.T).row_join(C))

    p = event_probs(K)
    check_inclusion_exclusion(K, p)
    pA = event_probs(A)
    pC = event_probs(C)
    alpha = {k: sp.diff(vv, t).subs(t, 0) for k, vv in event_probs(A + t * u * u.T).items()}
    gamma = {k: sp.diff(vv, t).subs(t, 0) for k, vv in event_probs(C + t * v * v.T).items()}

    for full_key, prob in p.items():
        left, right = full_key[:2], full_key[2:]
        expected = pA[left] * pC[right] - t**2 * alpha[left] * gamma[right]
        assert sp.simplify(prob - expected) == 0, full_key

    left_marginal_ok = {}
    right_marginal_ok = {}
    for left in pA:
        left_marginal_ok[left] = sp.simplify(
            sum(prob for kk, prob in p.items() if kk[:2] == left) - pA[left]
        )
        assert left_marginal_ok[left] == 0
    for right in pC:
        right_marginal_ok[right] = sp.simplify(
            sum(prob for kk, prob in p.items() if kk[2:] == right) - pC[right]
        )
        assert right_marginal_ok[right] == 0

    s0 = R(1, 16)
    at = R(1, 4)
    direct_terms = []
    t2_terms = []
    fisher_direct = sp.Integer(0)
    fisher_formula = sp.Integer(0)
    for full_key, prob in p.items():
        left, right = full_key[:2], full_key[2:]
        r = -alpha[left] * gamma[right]
        ps = pA[left] * pC[right] + s0 * r
        assert sp.simplify(prob.subs(t, at) - ps) == 0
        pprime = sp.diff(prob, t).subs(t, at)
        psecond = sp.diff(prob, t, 2).subs(t, at)
        fisher_direct += sp.factor(pprime**2 / ps)
        fisher_formula += sp.factor(4 * s0 * r**2 / ps)
        direct_terms.append((-psecond, ps))
        ratio = sp.factor(ps / (pA[left] * pC[right]))
        t2_terms.append((-2 * r, ratio))
    assert sp.simplify(fisher_direct - fisher_formula) == 0

    # Numeric equality of direct H'' and the relative-entropy/Fisher formula.
    mp.mp.dps = 80
    direct = -sum(
        mp.mpf(str(sp.N(c, 80))) * mp.log(mp.mpf(str(sp.N(arg, 80))))
        for c, arg in direct_terms
    ) - mp.mpf(str(sp.N(fisher_direct, 80)))
    formula = -sum(
        mp.mpf(str(sp.N(c, 80))) * mp.log(mp.mpf(str(sp.N(arg, 80))))
        for c, arg in t2_terms
    ) - mp.mpf(str(sp.N(fisher_formula, 80)))
    assert abs(direct - formula) < mp.mpf("1e-70")

    return {
        "event_count": len(p),
        "all_rank_one_event_identities": True,
        "all_inclusion_exclusion_checks": True,
        "fixed_left_marginals": True,
        "fixed_right_marginals": True,
        "D_rank": int(sp.diff(K, t).rank()),
        "D_is_indefinite": True,
        "H_second_formula_match_at_t_1_over_4": mp.nstr(direct, 50),
        "H_second_formula_difference_abs": mp.nstr(abs(direct - formula), 20),
    }


def two_coordinate_conditional_certificate() -> dict:
    A = sp.Matrix(
        [
            [R(3, 8), R(1, 20), R(-1, 30)],
            [R(1, 20), R(1, 2), R(1, 25)],
            [R(-1, 30), R(1, 25), R(5, 8)],
        ]
    )
    C = sp.Matrix([[R(2, 5), R(1, 12)], [R(1, 12), R(3, 5)]])
    B = sp.Matrix([[R(1, 10), R(1, 25)], [R(-1, 20), R(1, 15)], [R(1, 30), R(-1, 18)]])
    K = A.row_join(t * B).col_join((t * B.T).row_join(C))
    p = event_probs(K)
    check_inclusion_exclusion(K, p)
    pC = event_probs(C)

    cond_ranks = {}
    for right_bits in bits_iter(2):
        rk = key(right_bits)
        Y = C - sp.diag(*[1 - b for b in right_bits])
        W = -B * Y.inv() * B.T
        cond_ranks[rk] = int(W.rank())
        cond_probs = event_probs(A + t**2 * W)
        for left_bits in bits_iter(3):
            full_key = key(left_bits + right_bits)
            assert sp.simplify(p[full_key] - pC[rk] * cond_probs[key(left_bits)]) == 0

    coeff_t4_nonzero = sum(
        1 for prob in p.values() if sp.expand(prob).coeff(t, 4) != 0
    )
    coeff_t2_nonzero = sum(
        1 for prob in p.values() if sp.expand(prob).coeff(t, 2) != 0
    )
    return {
        "event_count": len(p),
        "conditional_schur_identity_all_events": True,
        "rank_B": int(B.rank()),
        "conditional_direction_ranks_by_right_event": cond_ranks,
        "events_with_t2_terms": coeff_t2_nonzero,
        "events_with_t4_terms": coeff_t4_nonzero,
        "interpretation": "coordinate two-column reduction holds, but rank-two conditional directions remain",
    }


def rank_two_diagnostics() -> dict:
    A = sp.eye(2) / 2
    C = sp.eye(2) / 2
    examples = {
        "diagonal_rank2": sp.Matrix([[R(1, 5), 0], [0, R(1, 6)]]),
        "dense_rank2": sp.Matrix([[R(1, 5), R(1, 11)], [R(1, 13), R(-1, 6)]]),
        "mixed_sign_rank2": sp.Matrix([[R(1, 4), R(-1, 9)], [R(1, 7), R(1, 8)]]),
    }
    out = {}
    for name, B in examples.items():
        K = A.row_join(t * B).col_join((t * B.T).row_join(C))
        p = event_probs(K)
        h2_at_zero = -sum(sp.diff(prob, t, 2).subs(t, 0) * sp.log(prob.subs(t, 0)) for prob in p.values())
        h2_at_zero -= sum(
            sp.diff(prob, t).subs(t, 0) ** 2 / prob.subs(t, 0) for prob in p.values()
        )
        assert sp.simplify(h2_at_zero) == 0
        quartic_events = sum(1 for prob in p.values() if sp.expand(prob).coeff(t, 4) != 0)
        b_np = np.array([[float(x) for x in row] for row in B.tolist()], dtype=float)
        tau = 0.5 / float(np.linalg.svd(b_np, compute_uv=False)[0])
        values = []
        K0 = A.row_join(sp.zeros(2, 2)).col_join(sp.zeros(2, 2).row_join(C))
        D = sp.zeros(4, 4)
        D[:2, 2:] = B
        D[2:, :2] = B.T
        for at in [R(1, 10), R(1, 4), R(1, 2), R(1, 1)]:
            h2 = hessian_numeric(K0, D, at)
            values.append((str(at), mp.nstr(h2, 30)))
        out[name] = {
            "rank_B": int(B.rank()),
            "events_with_t4_terms": quartic_events,
            "H_second_at_zero_exact": "0",
            "legal_tau_numeric": f"{tau:.17g}",
            "sampled_H_second": values,
            "diagnostic_only": True,
        }
    return out


def rotation_entropy_check() -> dict:
    K_diag = sp.diag(R(9, 10), R(1, 10))
    K_rot = sp.Matrix([[R(1, 2), R(2, 5)], [R(2, 5), R(1, 2)]])
    h_diag = entropy_numeric_from_sym(K_diag)
    h_rot = entropy_numeric_from_sym(K_rot)
    return {
        "same_eigenvalues": ["1/10", "9/10"],
        "H_diag": mp.nstr(h_diag, 50),
        "H_rotated": mp.nstr(h_rot, 50),
        "difference_rotated_minus_diag": mp.nstr(h_rot - h_diag, 50),
        "conclusion": "orthogonal rotation is not a coordinate relabeling for full configuration entropy",
    }


def main() -> int:
    os.environ["OMP_NUM_THREADS"] = "1"
    os.environ["OPENBLAS_NUM_THREADS"] = "1"
    os.environ["MKL_NUM_THREADS"] = "1"
    os.environ["NUMEXPR_NUM_THREADS"] = "1"
    result = {
        "python": platform.python_version(),
        "executable": sys.executable,
        "sympy": sp.__version__,
        "numpy": np.__version__,
        "mpmath": mp.__version__,
        "rank_one_certificate": rank_one_certificate(),
        "two_coordinate_conditional_certificate": two_coordinate_conditional_certificate(),
        "rank_two_diagnostics": rank_two_diagnostics(),
        "rotation_entropy_check": rotation_entropy_check(),
    }
    output_path = OUT / "w1_independent_check_results.json"
    output_path.write_text(json.dumps(result, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
