#!/usr/bin/env python3
"""Fixed independent checks for PR32 round2.

The script targets named proof obligations only. It is not an open-ended
counterexample search.
"""
from __future__ import annotations

import json
import os
import platform
import sys
from itertools import product
from pathlib import Path

import mpmath as mp
import numpy as np
import sympy as sp

R = sp.Rational
t, z, lam = sp.symbols("t z lam", real=True)

OUT = Path(__file__).resolve().parent / "compute_outputs"
OUT.mkdir(exist_ok=True)


def bit_tuples(n: int):
    return list(product((0, 1), repeat=n))


def key(bits) -> str:
    return "".join(str(int(b)) for b in bits)


def event_probs(K: sp.Matrix, var=None) -> dict[str, sp.Expr]:
    n = K.rows
    out = {}
    for bits in bit_tuples(n):
        diag = sp.diag(*[1 - b for b in bits])
        out[key(bits)] = sp.factor((-1) ** (n - sum(bits)) * (K - diag).det())
    assert sp.simplify(sum(out.values()) - 1) == 0
    return out


def entropy_from_probs(prob_values) -> mp.mpf:
    mp.mp.dps = 80
    total = mp.mpf("0")
    for value in prob_values:
        p = mp.mpf(str(sp.N(value, 80)))
        if p != 0:
            total -= p * mp.log(p)
    return total


def hessian_at(K_expr: sp.Matrix, var, at) -> mp.mpf:
    mp.mp.dps = 80
    probs = event_probs(K_expr)
    total = mp.mpf("0")
    for prob in probs.values():
        p0 = mp.mpf(str(sp.N(prob.subs(var, at), 80)))
        p1 = mp.mpf(str(sp.N(sp.diff(prob, var).subs(var, at), 80)))
        p2 = mp.mpf(str(sp.N(sp.diff(prob, var, 2).subs(var, at), 80)))
        assert p0 > 0
        total += -p2 * mp.log(p0) - p1 * p1 / p0
    return total


def principal_minors_positive(M: sp.Matrix) -> bool:
    n = M.rows
    for r in range(1, n + 1):
        for idx in product((0, 1), repeat=n):
            if sum(idx) != r:
                continue
            subset = [i for i, b in enumerate(idx) if b]
            if sp.simplify(M.extract(subset, subset).det()) <= 0:
                return False
    return True


def check_conditional_mx2() -> dict:
    A = sp.Matrix(
        [
            [R(2, 5), R(1, 30), R(-1, 40)],
            [R(1, 30), R(11, 20), R(1, 35)],
            [R(-1, 40), R(1, 35), R(3, 5)],
        ]
    )
    C = sp.Matrix([[R(9, 20), R(1, 11)], [R(1, 11), R(7, 12)]])
    B = sp.Matrix([[R(1, 9), R(-1, 10)], [R(1, 13), R(1, 8)], [R(-1, 14), R(1, 15)]])
    K = A.row_join(t * B).col_join((t * B.T).row_join(C))
    p = event_probs(K)
    pA = event_probs(A)
    all_ok = True
    second_derivative_left_sums = {}
    second_derivative_right_sums = {}
    cond_strict_at = R(1, 5)
    cond_strict = {}
    for left_bits in bit_tuples(3):
        lk = key(left_bits)
        X = A - sp.diag(*[1 - b for b in left_bits])
        M = B.T * X.inv() * B
        C_s = C - t**2 * M
        p_cond = event_probs(C_s)
        for right_bits in bit_tuples(2):
            rk = key(right_bits)
            full = key(left_bits + right_bits)
            all_ok = all_ok and sp.simplify(p[full] - pA[lk] * p_cond[rk]) == 0
        C_eval = sp.simplify(C_s.subs(t, cond_strict_at))
        cond_strict[lk] = bool(
            principal_minors_positive(C_eval)
            and principal_minors_positive(sp.eye(2) - C_eval)
        )
    assert all_ok
    assert all(cond_strict.values())
    for left_bits in bit_tuples(3):
        lk = key(left_bits)
        second_derivative_left_sums[lk] = sp.simplify(
            sum(sp.diff(prob, t, 2).subs(t, 0) for kk, prob in p.items() if kk[:3] == lk)
        )
        assert second_derivative_left_sums[lk] == 0
    for right_bits in bit_tuples(2):
        rk = key(right_bits)
        second_derivative_right_sums[rk] = sp.simplify(
            sum(sp.diff(prob, t, 2).subs(t, 0) for kk, prob in p.items() if kk[3:] == rk)
        )
        assert second_derivative_right_sums[rk] == 0
    h2_zero = hessian_at(K, t, 0)
    chord = (
        entropy_from_probs(event_probs(K.subs(t, R(1, 5))).values())
        + entropy_from_probs(event_probs(K.subs(t, R(-1, 5))).values())
    ) / 2 - entropy_from_probs(event_probs(K.subs(t, 0)).values())
    return {
        "events": len(p),
        "all_event_conditional_identity": True,
        "rank_B": int(B.rank()),
        "all_conditional_kernels_strict_at_t_1_over_5": True,
        "H_second_at_zero_log_coefficients_cancel_exactly": True,
        "H_second_at_zero": mp.nstr(h2_zero, 40),
        "central_chord_step_1_over_5": mp.nstr(chord, 40),
    }


def check_two_actual_coordinate_columns() -> dict:
    A = sp.Matrix([[R(7, 16), R(1, 30)], [R(1, 30), R(9, 16)]])
    C = sp.Matrix(
        [
            [R(2, 5), R(1, 40), R(1, 50), R(-1, 60)],
            [R(1, 40), R(9, 20), R(1, 45), R(1, 55)],
            [R(1, 50), R(1, 45), R(11, 20), R(-1, 70)],
            [R(-1, 60), R(1, 55), R(-1, 70), R(3, 5)],
        ]
    )
    B = sp.zeros(2, 4)
    B[:, 1] = sp.Matrix([R(1, 8), R(-1, 11)])
    B[:, 3] = sp.Matrix([R(1, 10), R(1, 12)])
    K = A.row_join(t * B).col_join((t * B.T).row_join(C))
    p = event_probs(K)
    pA = event_probs(A)
    support_ok = True
    identity_ok = True
    support_columns = []
    for j in range(4):
        if any(B[i, j] != 0 for i in range(2)):
            support_columns.append(j)
    for left_bits in bit_tuples(2):
        lk = key(left_bits)
        X = A - sp.diag(*[1 - b for b in left_bits])
        M = sp.simplify(B.T * X.inv() * B)
        for i in range(4):
            for j in range(4):
                if (i not in support_columns or j not in support_columns) and M[i, j] != 0:
                    support_ok = False
        p_cond = event_probs(C - t**2 * M)
        for right_bits in bit_tuples(4):
            rk = key(right_bits)
            full = key(left_bits + right_bits)
            identity_ok = identity_ok and sp.simplify(p[full] - pA[lk] * p_cond[rk]) == 0
    assert support_ok and identity_ok
    return {
        "events": len(p),
        "actual_nonzero_columns_zero_based": support_columns,
        "rank_B": int(B.rank()),
        "conditional_identity_all_events": True,
        "M_S_support_stays_inside_actual_two_columns": True,
    }


def check_two_by_two_hessian_lemma() -> dict:
    a, b, c = R(9, 20), R(2, 5), R(1, 7)
    u, v, w = R(1, 6), R(-1, 5), R(1, 8)
    L = sp.Matrix([[a, c], [c, b]])
    V = sp.Matrix([[u, w], [w, v]])
    Kz = L + z * V
    probs = list(event_probs(Kz).values())
    h2_direct = hessian_at(Kz, z, 0)

    d = a * b - c * c
    q = u * v - w * w
    alpha = b * u + a * v - 2 * c * w
    A0, A1, A2, A3 = 1 - a - b + d, a - d, b - d, d
    x = [-u - v + alpha, u - alpha, v - alpha, alpha]
    F = sum(xi * xi / Ai for xi, Ai in zip(x, [A0, A1, A2, A3]))
    Lambda_arg = sp.factor((A1 * A2) / (A0 * A3))
    h2_formula = -mp.mpf(str(sp.N(F, 80))) + 2 * mp.mpf(str(sp.N(q, 80))) * mp.log(
        mp.mpf(str(sp.N(Lambda_arg, 80)))
    )
    assert abs(h2_direct - h2_formula) < mp.mpf("1e-70")

    r = c * c
    P = A0 * A1 * A2 * A3
    E = A0 * A3 * (A0 + A3) + A1 * A2 * (A1 + A2)
    G = sp.Matrix(
        [
            [1 / A0 + 1 / A1, 1 / A0, -1 / A0 - 1 / A1],
            [1 / A0, 1 / A0 + 1 / A2, -1 / A0 - 1 / A2],
            [-1 / A0 - 1 / A1, -1 / A0 - 1 / A2, sum(1 / Ai for Ai in [A0, A1, A2, A3])],
        ]
    )
    Q = sp.Matrix([[0, R(1, 2), 0], [R(1, 2), 0, 0], [0, 0, 0]]) - (
        sp.Matrix([b, a, -1]) * sp.Matrix([[b, a, -1]]) / (4 * r)
    )
    det_left = sp.factor((G - lam * Q).det())
    det_right = sp.factor((16 * r + 4 * lam * E - lam**3 * P) / (16 * r * P))
    assert sp.simplify(det_left - det_right) == 0

    diag_center = sp.eye(2) / 2 + z * sp.Matrix([[0, 1], [1, 0]])
    h2_diag_center = hessian_at(diag_center, z, 0)
    h2_off_center = hessian_at(diag_center, z, R(1, 10))
    chord = (
        entropy_from_probs(event_probs(diag_center.subs(z, R(1, 10))).values())
        + entropy_from_probs(event_probs(diag_center.subs(z, R(-1, 10))).values())
    ) / 2 - entropy_from_probs(event_probs(diag_center.subs(z, 0)).values())
    return {
        "fixed_c_nonzero_direct_H_second": mp.nstr(h2_direct, 40),
        "fixed_c_nonzero_formula_H_second": mp.nstr(h2_formula, 40),
        "determinant_pencil_identity_fixed_rational": True,
        "diagonal_center_pure_offdiag_H_second_at_0": mp.nstr(h2_diag_center, 40),
        "same_line_H_second_at_z_1_over_10": mp.nstr(h2_off_center, 40),
        "same_line_central_chord_step_1_over_10": mp.nstr(chord, 40),
    }


def check_harmful_q_example() -> dict:
    A = sp.Matrix([[R(9, 20), R(1, 4)], [R(1, 4), R(1, 4)]])
    C = sp.Matrix([[R(17, 20), R(-1, 5)], [R(-1, 5), R(2, 5)]])
    B = sp.Matrix([[R(3, 2), R(-11, 10)], [R(-3, 10), R(-3, 10)]])
    s0 = R(1, 100)
    t0 = R(1, 10)
    K = A.row_join(t * B).col_join((t * B.T).row_join(C))
    p = event_probs(K)
    p0 = {kk: sp.simplify(vv.subs(t, 0)) for kk, vv in p.items()}
    rcoef = {kk: sp.expand(vv).coeff(t, 2) for kk, vv in p.items()}
    qcoef = {kk: sp.expand(vv).coeff(t, 4) for kk, vv in p.items()}
    ps = {kk: sp.simplify(vv.subs(t, t0)) for kk, vv in p.items()}
    mp.mp.dps = 100
    qlog = mp.mpf("0")
    J = mp.mpf("0")
    Fterm = mp.mpf("0")
    for kk in p:
        P0 = mp.mpf(str(sp.N(p0[kk], 100)))
        Rcoef = mp.mpf(str(sp.N(rcoef[kk], 100)))
        Qcoef = mp.mpf(str(sp.N(qcoef[kk], 100)))
        Ps = mp.mpf(str(sp.N(ps[kk], 100)))
        log_ratio = mp.log(Ps / P0)
        qlog += Qcoef * log_ratio
        J += (Ps - P0) * log_ratio
        Fterm += (Rcoef + 2 * mp.mpf(str(sp.N(s0, 100))) * Qcoef) ** 2 / Ps
    h2 = hessian_at(K, t, t0)
    refresh_diff_nonzero = any(qcoef[kk] != 0 for kk in p)
    min_prob = min(ps.values())
    return {
        "rank_B": int(B.rank()),
        "det_B": str(B.det()),
        "min_probability_at_t_1_over_10": str(min_prob),
        "Q_log_ratio": mp.nstr(qlog, 50),
        "minus_10s_Q_log_ratio": mp.nstr(-10 * mp.mpf(str(sp.N(s0, 100))) * qlog, 50),
        "J": mp.nstr(J, 50),
        "Fterm": mp.nstr(Fterm, 50),
        "H_second": mp.nstr(h2, 50),
        "refresh_diff_Q_nonzero": refresh_diff_nonzero,
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
        "conditional_mx2": check_conditional_mx2(),
        "two_actual_coordinate_columns": check_two_actual_coordinate_columns(),
        "two_by_two_hessian_lemma": check_two_by_two_hessian_lemma(),
        "harmful_q_example": check_harmful_q_example(),
    }
    out_path = OUT / "w1_round2_check_results.json"
    out_path.write_text(json.dumps(result, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
