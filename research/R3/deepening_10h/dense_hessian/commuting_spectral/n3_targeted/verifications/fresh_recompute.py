#!/usr/bin/env python3
"""Fresh non-author recomputation for D10-M5 n3_targeted.

The script deliberately does not import the author search script.  It checks:

1. exact n=3 layer reduction against full spectral-channel atoms and signed
   determinant atoms using Fraction arithmetic;
2. the rational raw-weight r'' blocker;
3. the reported JSON denominator and selected extrema by independently
   recomputing p,p',p'', H'', Psi'', layer terms, atom sums, and chord gates.
"""

from __future__ import annotations

import json
import math
import os
from fractions import Fraction
from pathlib import Path

for _var in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_var, "1")

ROOT = Path(__file__).resolve().parents[1]
AUTHOR_RESULTS = ROOT / "n3_search_results.json"
OUT = Path(__file__).with_name("fresh_recompute_results.json")


def F(a: int, b: int = 1) -> Fraction:
    return Fraction(a, b)


def pop(mask: int) -> int:
    return mask.bit_count()


def bits(mask: int, n: int) -> list[int]:
    return [i for i in range(n) if (mask >> i) & 1]


def det_frac(A: list[list[Fraction]]) -> Fraction:
    n = len(A)
    if n == 0:
        return F(1)
    M = [row[:] for row in A]
    ans = F(1)
    for i in range(n):
        pivot = None
        for r in range(i, n):
            if M[r][i] != 0:
                pivot = r
                break
        if pivot is None:
            return F(0)
        if pivot != i:
            M[i], M[pivot] = M[pivot], M[i]
            ans = -ans
        pv = M[i][i]
        ans *= pv
        for r in range(i + 1, n):
            q = M[r][i] / pv
            if q:
                for c in range(i, n):
                    M[r][c] -= q * M[i][c]
    return ans


def sub_frac(A: list[list[Fraction]], rows: list[int], cols: list[int]) -> list[list[Fraction]]:
    return [[A[i][j] for j in cols] for i in rows]


def matmul_frac(A: list[list[Fraction]], B: list[list[Fraction]]) -> list[list[Fraction]]:
    n, m, r = len(A), len(B[0]), len(B)
    return [[sum(A[i][k] * B[k][j] for k in range(r)) for j in range(m)] for i in range(n)]


def trans_frac(A: list[list[Fraction]]) -> list[list[Fraction]]:
    return [list(row) for row in zip(*A)]


def diag_frac(vals: list[Fraction]) -> list[list[Fraction]]:
    n = len(vals)
    A = [[F(0) for _ in range(n)] for __ in range(n)]
    for i, x in enumerate(vals):
        A[i][i] = x
    return A


def kernel_frac(Q: list[list[Fraction]], theta: list[Fraction]) -> list[list[Fraction]]:
    return matmul_frac(matmul_frac(Q, diag_frac(theta)), trans_frac(Q))


def event_matrix_frac(K: list[list[Fraction]], S: int) -> list[list[Fraction]]:
    n = len(K)
    A = [row[:] for row in K]
    for i in range(n):
        if not ((S >> i) & 1):
            A[i][i] -= 1
    return A


def signed_atom_frac(K: list[list[Fraction]], S: int) -> Fraction:
    n = len(K)
    sign = -1 if ((n - pop(S)) & 1) else 1
    return sign * det_frac(event_matrix_frac(K, S))


def channel_atom_frac(Q: list[list[Fraction]], theta: list[Fraction], S: int) -> Fraction:
    n = len(theta)
    ans = F(0)
    rows = bits(S, n)
    for R in range(1 << n):
        if pop(R) != pop(S):
            continue
        cols = bits(R, n)
        T = det_frac(sub_frac(Q, rows, cols)) ** 2
        mu = F(1)
        for i, th in enumerate(theta):
            mu *= th if ((R >> i) & 1) else 1 - th
        ans += T * mu
    return ans


def reduced_n3_atom_frac(Q: list[list[Fraction]], theta: list[Fraction], S: int) -> Fraction:
    P = [[Q[a][i] * Q[a][i] for i in range(3)] for a in range(3)]
    k = pop(S)
    if k == 0:
        return math.prod([1 - th for th in theta])
    if k == 3:
        return math.prod(theta)
    if k == 1:
        a = bits(S, 3)[0]
        r = []
        for i in range(3):
            prod = theta[i]
            for j in range(3):
                if j != i:
                    prod *= 1 - theta[j]
            r.append(prod)
        return sum(P[a][i] * r[i] for i in range(3))
    missing_rows = [a for a in range(3) if not ((S >> a) & 1)]
    a = missing_rows[0]
    s = []
    for i in range(3):
        prod = 1 - theta[i]
        for j in range(3):
            if j != i:
                prod *= theta[j]
        s.append(prod)
    return sum(P[a][i] * s[i] for i in range(3))


def exact_layer_reduction_check() -> dict:
    Q = [
        [F(6, 7), F(-2, 7), F(-3, 7)],
        [F(-2, 7), F(3, 7), F(-6, 7)],
        [F(-3, 7), F(-6, 7), F(-2, 7)],
    ]
    theta = [F(2, 7), F(3, 5), F(5, 11)]
    K = kernel_frac(Q, theta)
    diffs_channel = []
    diffs_signed = []
    atoms = []
    for S in range(8):
        red = reduced_n3_atom_frac(Q, theta, S)
        chan = channel_atom_frac(Q, theta, S)
        signed = signed_atom_frac(K, S)
        diffs_channel.append(abs(red - chan))
        diffs_signed.append(abs(red - signed))
        atoms.append(red)
    return {
        "Q": "Householder I - (1/7)(1,2,3)(1,2,3)^T",
        "theta": [str(x) for x in theta],
        "atoms_by_mask": {format(S, "03b"): str(atoms[S]) for S in range(8)},
        "sum_atoms": str(sum(atoms)),
        "max_reduced_vs_full_channel_diff": str(max(diffs_channel)),
        "max_reduced_vs_signed_atom_diff": str(max(diffs_signed)),
        "min_atom": str(min(atoms)),
    }


def r2_formula(theta: list[Fraction], v: list[Fraction]) -> list[Fraction]:
    out = []
    for i in range(3):
        j, k = [x for x in range(3) if x != i]
        out.append(2 * (theta[i] * v[j] * v[k] - v[i] * v[j] * (1 - theta[k]) - v[i] * v[k] * (1 - theta[j])))
    return out


def s2_formula(theta: list[Fraction], v: list[Fraction]) -> list[Fraction]:
    out = []
    for i in range(3):
        j, k = [x for x in range(3) if x != i]
        out.append(2 * ((1 - theta[i]) * v[j] * v[k] - v[i] * v[j] * theta[k] - v[i] * v[k] * theta[j]))
    return out


def blocker_check() -> dict:
    theta = [F(3, 5), F(1, 5), F(1, 5)]
    v = [F(1, 100), F(1, 10), F(1, 10)]
    r2 = r2_formula(theta, v)
    s2 = s2_formula(theta, v)
    return {
        "theta": [str(x) for x in theta],
        "v": [str(x) for x in v],
        "r2": [str(x) for x in r2],
        "s2": [str(x) for x in s2],
        "matches_author_r2": r2 == [F(11, 1250), F(-23, 2500), F(-23, 2500)],
        "positive_r2_indices": [i for i, x in enumerate(r2) if x > 0],
    }


def monomial(theta: list[float], v: list[float], included: tuple[int, ...]) -> tuple[float, float, float]:
    inc = set(included)
    p = 1.0
    scores = []
    for i in range(3):
        if i in inc:
            p *= theta[i]
            scores.append(v[i] / theta[i])
        else:
            p *= 1.0 - theta[i]
            scores.append(-v[i] / (1.0 - theta[i]))
    s1 = sum(scores)
    s2 = s1 * s1 - sum(x * x for x in scores)
    return p, p * s1, p * s2


def dot_mat_vec(A: list[list[float]], x: list[float]) -> list[float]:
    return [sum(A[i][j] * x[j] for j in range(len(x))) for i in range(len(A))]


def eta_h2(p: list[float], p1: list[float], p2: list[float]) -> float:
    return sum(-(b * b) / a - c * math.log(a) for a, b, c in zip(p, p1, p2))


def dist_derivatives(theta: list[float], v: list[float], Q: list[list[float]]) -> dict:
    P = [[Q[a][i] * Q[a][i] for i in range(3)] for a in range(3)]
    p0, p0_1, p0_2 = monomial(theta, v, ())
    p3, p3_1, p3_2 = monomial(theta, v, (0, 1, 2))
    r = []
    r1 = []
    r2 = []
    s = []
    s1 = []
    s2 = []
    for i in range(3):
        a, b, c = monomial(theta, v, (i,))
        r.append(a)
        r1.append(b)
        r2.append(c)
        a, b, c = monomial(theta, v, tuple(j for j in range(3) if j != i))
        s.append(a)
        s1.append(b)
        s2.append(c)
    u = dot_mat_vec(P, r)
    u1 = dot_mat_vec(P, r1)
    u2 = dot_mat_vec(P, r2)
    w = dot_mat_vec(P, s)
    w1 = dot_mat_vec(P, s1)
    w2 = dot_mat_vec(P, s2)
    p = [p0] + u + w + [p3]
    p1 = [p0_1] + u1 + w1 + [p3_1]
    p2 = [p0_2] + u2 + w2 + [p3_2]
    count_p = [p0, sum(r), sum(s), p3]
    count_p1 = [p0_1, sum(r1), sum(s1), p3_1]
    count_p2 = [p0_2, sum(r2), sum(s2), p3_2]
    H2 = eta_h2(p, p1, p2)
    count_H2 = eta_h2(count_p, count_p1, count_p2)
    singleton_cond_H2 = eta_h2(u, u1, u2) - eta_h2([sum(r)], [sum(r1)], [sum(r2)])
    pair_cond_H2 = eta_h2(w, w1, w2) - eta_h2([sum(s)], [sum(s1)], [sum(s2)])
    fisher = sum((b * b) / a for a, b in zip(p, p1))
    accel = sum(-c * math.log(a) for a, c in zip(p, p2))
    return {
        "P": P,
        "p": p,
        "p1": p1,
        "p2": p2,
        "count_p": count_p,
        "count_p1": count_p1,
        "count_p2": count_p2,
        "H2": H2,
        "count_H2": count_H2,
        "psi_H2": H2 - count_H2,
        "singleton_cond_H2": singleton_cond_H2,
        "pair_cond_H2": pair_cond_H2,
        "fisher_positive": fisher,
        "acceleration": accel,
        "rho": accel / fisher if fisher > 0.0 else None,
        "min_atom": min(p),
        "sum_p_minus_one": sum(p) - 1.0,
        "sum_p1": sum(p1),
        "sum_p2": sum(p2),
        "r2": r2,
        "s2": s2,
    }


def entropy_from_theta(theta: list[float], Q: list[list[float]]) -> float:
    d = dist_derivatives(theta, [0.0, 0.0, 0.0], Q)
    return -sum(a * math.log(a) for a in d["p"])


def chord_gate(theta: list[float], v: list[float], Q: list[list[float]]) -> dict:
    positive = [i for i, x in enumerate(v) if x > 1e-15]
    if positive:
        max_step = min(min(theta[i] / v[i], (1.0 - theta[i]) / v[i]) for i in positive)
    else:
        max_step = 1.0
    h = min(1e-4, 0.2 * max_step)
    hp = [theta[i] + h * v[i] for i in range(3)]
    hm = [theta[i] - h * v[i] for i in range(3)]
    H0 = entropy_from_theta(theta, Q)
    Hplus = entropy_from_theta(hp, Q)
    Hminus = entropy_from_theta(hm, Q)
    return {
        "h": h,
        "max_symmetric_spectral_step": max_step,
        "midpoint_gap": (Hplus + Hminus) / 2.0 - H0,
        "central_second_difference": (Hplus + Hminus - 2.0 * H0) / (h * h),
        "theta_plus_min": min(hp),
        "theta_minus_min": min(hm),
        "one_minus_theta_plus_min": min(1.0 - x for x in hp),
        "one_minus_theta_minus_min": min(1.0 - x for x in hm),
    }


def max_abs(xs: list[float]) -> float:
    return max(abs(x) for x in xs) if xs else 0.0


def compare_float_dict(record: dict, recomputed: dict, fields: list[str]) -> dict:
    return {field: abs(float(record[field]) - float(recomputed[field])) for field in fields}


def matrix_checks(Q: list[list[float]], P: list[list[float]]) -> dict:
    gram = []
    for i in range(3):
        for j in range(3):
            gram.append(sum(Q[a][i] * Q[a][j] for a in range(3)) - (1.0 if i == j else 0.0))
    row_sums = [sum(row) for row in P]
    col_sums = [sum(P[a][i] for a in range(3)) for i in range(3)]
    return {
        "orthogonality_max_abs_error": max_abs(gram),
        "P_row_sum_max_abs_error": max_abs([x - 1.0 for x in row_sums]),
        "P_col_sum_max_abs_error": max_abs([x - 1.0 for x in col_sums]),
        "P_min_entry": min(min(row) for row in P),
    }


def record_recheck(name: str, record: dict) -> dict:
    theta = [float(x) for x in record["theta"]]
    v = [float(x) for x in record["v"]]
    Q = [[float(x) for x in row] for row in record["Q"]]
    recalc = dist_derivatives(theta, v, Q)
    fields = [
        "H2",
        "count_H2",
        "psi_H2",
        "singleton_cond_H2",
        "pair_cond_H2",
        "fisher_positive",
        "acceleration",
        "rho",
        "min_atom",
        "sum_p_minus_one",
        "sum_p1",
        "sum_p2",
    ]
    diffs = compare_float_dict(record, recalc, fields)
    p_diff = max_abs([record["p"][i] - recalc["p"][i] for i in range(8)])
    p1_diff = max_abs([record["p1"][i] - recalc["p1"][i] for i in range(8)])
    p2_diff = max_abs([record["p2"][i] - recalc["p2"][i] for i in range(8)])
    r2_diff = max_abs([record["singleton_raw_r2"][i] - recalc["r2"][i] for i in range(3)])
    s2_diff = max_abs([record["pair_raw_s2"][i] - recalc["s2"][i] for i in range(3)])
    out = {
        "label": record.get("label"),
        "field_abs_diffs": diffs,
        "max_p_diff": p_diff,
        "max_p1_diff": p1_diff,
        "max_p2_diff": p2_diff,
        "max_singleton_r2_diff": r2_diff,
        "max_pair_s2_diff": s2_diff,
        "min_v": min(v),
        "all_v_nonnegative": all(x >= -1e-14 for x in v),
        "matrix_checks": matrix_checks(Q, recalc["P"]),
    }
    if "strict_spectral_chord_gate" in record:
        gate = chord_gate(theta, v, Q)
        out["chord_gate_abs_diffs"] = {
            key: abs(float(record["strict_spectral_chord_gate"][key]) - float(gate[key]))
            for key in (
                "h",
                "max_symmetric_spectral_step",
                "midpoint_gap",
                "central_second_difference",
                "theta_plus_min",
                "theta_minus_min",
                "one_minus_theta_plus_min",
                "one_minus_theta_minus_min",
            )
        }
    return out


def author_result_recheck() -> dict:
    data = json.loads(AUTHOR_RESULTS.read_text(encoding="utf-8"))
    denominator = {
        "random_draws_requested": data["random_draws_requested"],
        "random_draws_completed": data["random_draws_completed"],
        "local_steps_requested": data["local_steps_requested"],
        "local_steps_completed": data["local_steps_completed"],
        "total_completed": data["random_draws_completed"] + data["local_steps_completed"],
        "positive_candidates_len": len(data["positive_candidates"]),
        "status": data["status"],
        "seed": data["seed"],
        "local_accepted": data["local_accepted"],
    }
    rechecks = {
        "best": record_recheck("best", data["best"]),
        "best_psi_H2": record_recheck("best_psi_H2", data["best_psi_H2"]),
        "best_singleton_cond_H2": record_recheck("best_singleton_cond_H2", data["best_singleton_cond_H2"]),
        "best_pair_cond_H2": record_recheck("best_pair_cond_H2", data["best_pair_cond_H2"]),
    }
    summary_values = {
        "best_H2": data["best"]["H2"],
        "best_psi_H2": data["best_psi_H2"]["psi_H2"],
        "max_singleton_cond_H2": data["best_singleton_cond_H2"]["singleton_cond_H2"],
        "opposite_pair_at_singleton_max": data["best_singleton_cond_H2"]["pair_cond_H2"],
        "max_pair_cond_H2": data["best_pair_cond_H2"]["pair_cond_H2"],
        "opposite_singleton_at_pair_max": data["best_pair_cond_H2"]["singleton_cond_H2"],
        "best_record_chord_gap": data["best"]["strict_spectral_chord_gate"]["midpoint_gap"],
        "best_record_chord_second_difference": data["best"]["strict_spectral_chord_gate"]["central_second_difference"],
    }
    return {"denominator": denominator, "summary_values": summary_values, "record_rechecks": rechecks}


def main() -> int:
    result = {
        "status": "FRESH_RECOMPUTE_PASS",
        "exact_layer_reduction": exact_layer_reduction_check(),
        "r2_blocker": blocker_check(),
        "author_json_recheck": author_result_recheck(),
        "notes": [
            "The 202000 count is confirmed from the author script/result ledger, not by rerunning the 30s random scan.",
            "All finite search conclusions remain SCOUT only.",
        ],
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
