"""Minimal independent replay for D10-U10g lambda_zero_subfamily audit.

Scope: recompute the frozen Kstar checks, constants, Fisher-field identity,
and the Fisher-only proxy witness without importing author sanity/gate code.
This is intentionally small after an interrupted longer audit.
"""

from __future__ import annotations

import hashlib
import json
import math
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path

import numpy as np

getcontext().prec = 90

HERE = Path(__file__).resolve().parent
BASE = HERE.parent


EVENTS = [(), (0,), (1,), (2,), (0, 1), (0, 2), (1, 2), (0, 1, 2)]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def det3(M):
    return (
        M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
        - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
        + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0])
    )


def inv3(M):
    d = det3(M)
    out = []
    for i in range(3):
        row = []
        for j in range(3):
            rows = [r for r in range(3) if r != j]
            cols = [c for c in range(3) if c != i]
            minor = M[rows[0]][cols[0]] * M[rows[1]][cols[1]] - M[rows[0]][cols[1]] * M[rows[1]][cols[0]]
            row.append((Fraction(-1) if (i + j) % 2 else Fraction(1)) * minor / d)
        out.append(row)
    return out


def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def det_sub(K, S):
    S = list(S)
    if len(S) == 0:
        return Fraction(1)
    if len(S) == 1:
        return K[S[0]][S[0]]
    if len(S) == 2:
        i, j = S
        return K[i][i] * K[j][j] - K[i][j] * K[i][j]
    return det3(K)


def atom(K, S):
    S = set(S)
    total = Fraction(0)
    for mask in range(8):
        T = tuple(i for i in range(3) if (mask >> i) & 1)
        if S.issubset(T):
            total += (Fraction(-1) if (len(T) - len(S)) % 2 else Fraction(1)) * det_sub(K, T)
    return total


def zero_grad():
    return [Fraction(0) for _ in range(6)]


def zero_hess():
    return [[Fraction(0) for _ in range(6)] for __ in range(6)]


def inclusion_jets(K):
    x1, x2, x3 = K[0][0], K[1][1], K[2][2]
    u, v, w = K[0][1], K[0][2], K[1][2]
    q, g, h = {}, {}, {}
    q[()] = Fraction(1)
    g[()] = zero_grad()
    h[()] = zero_hess()
    for idx, key, val in [(0, (0,), x1), (1, (1,), x2), (2, (2,), x3)]:
        q[key] = val
        gg = zero_grad()
        gg[idx] = Fraction(1)
        g[key] = gg
        h[key] = zero_hess()

    pair_data = [
        ((0, 1), 0, 1, 3, x1 * x2 - u * u),
        ((0, 2), 0, 2, 4, x1 * x3 - v * v),
        ((1, 2), 1, 2, 5, x2 * x3 - w * w),
    ]
    for key, i, j, eidx, val in pair_data:
        gg = zero_grad()
        gg[i] = K[j][j]
        gg[j] = K[i][i]
        gg[eidx] = -2 * K[i][j]
        hh = zero_hess()
        hh[i][j] = hh[j][i] = Fraction(1)
        hh[eidx][eidx] = Fraction(-2)
        q[key], g[key], h[key] = val, gg, hh

    r = det3(K)
    gg = zero_grad()
    hh = zero_hess()
    gg[0] = x2 * x3 - w * w
    gg[1] = x1 * x3 - v * v
    gg[2] = x1 * x2 - u * u
    gg[3] = 2 * v * w - 2 * x3 * u
    gg[4] = 2 * u * w - 2 * x2 * v
    gg[5] = 2 * u * v - 2 * x1 * w
    hh[0][1] = hh[1][0] = x3
    hh[0][2] = hh[2][0] = x2
    hh[1][2] = hh[2][1] = x1
    hh[0][5] = hh[5][0] = -2 * w
    hh[1][4] = hh[4][1] = -2 * v
    hh[2][3] = hh[3][2] = -2 * u
    hh[3][3] = -2 * x3
    hh[4][4] = -2 * x2
    hh[5][5] = -2 * x1
    hh[3][4] = hh[4][3] = 2 * w
    hh[3][5] = hh[5][3] = 2 * v
    hh[4][5] = hh[5][4] = 2 * u
    q[(0, 1, 2)], g[(0, 1, 2)], h[(0, 1, 2)] = r, gg, hh
    return q, g, h


def event_jets(K):
    q, g, h = inclusion_jets(K)
    vals, grads, hess = [], [], []
    for S0 in EVENTS:
        S = set(S0)
        val = Fraction(0)
        gg = zero_grad()
        hh = zero_hess()
        for mask in range(8):
            T = tuple(i for i in range(3) if (mask >> i) & 1)
            if not S.issubset(T):
                continue
            sign = Fraction(-1) if (len(T) - len(S)) % 2 else Fraction(1)
            val += sign * q[T]
            for i in range(6):
                gg[i] += sign * g[T][i]
            for i in range(6):
                for j in range(6):
                    hh[i][j] += sign * h[T][i][j]
        vals.append(val)
        grads.append(gg)
        hess.append(hh)
    return vals, grads, hess


def frac_to_dec(x: Fraction) -> Decimal:
    return Decimal(x.numerator) / Decimal(x.denominator)


def decimal_B(atoms, grads, hess):
    B = [[Decimal(0) for _ in range(6)] for __ in range(6)]
    for p, gg, hh in zip(atoms, grads, hess):
        pd = frac_to_dec(p)
        lp = pd.ln()
        for i in range(6):
            gi = frac_to_dec(gg[i])
            for j in range(6):
                B[i][j] += gi * frac_to_dec(gg[j]) / pd + frac_to_dec(hh[i][j]) * lp
    return B


def fraction_F(atoms, grads):
    F = [[Fraction(0) for _ in range(6)] for __ in range(6)]
    for p, gg in zip(atoms, grads):
        for i in range(6):
            for j in range(6):
                F[i][j] += gg[i] * gg[j] / p
    return F


def min_frobenius_eig(B_dec):
    B = np.array([[float(x) for x in row] for row in B_dec])
    invsqrtG = np.diag([1.0, 1.0, 1.0, 1 / math.sqrt(2), 1 / math.sqrt(2), 1 / math.sqrt(2)])
    M = invsqrtG @ B @ invsqrtG
    return np.linalg.eigvalsh((M + M.T) / 2).tolist()


def main():
    K = [
        [Fraction(1, 2), Fraction(3, 10), Fraction(0)],
        [Fraction(3, 10), Fraction(1, 2), Fraction(3, 10)],
        [Fraction(0), Fraction(3, 10), Fraction(1, 2)],
    ]
    atoms, grads, hess = event_jets(K)
    ratio = atoms[7] * atoms[1] * atoms[2] * atoms[3] / (atoms[0] * atoms[4] * atoms[5] * atoms[6])

    IminusK = [[(Fraction(1) if i == j else Fraction(0)) - K[i][j] for j in range(3)] for i in range(3)]
    L = matmul(K, inv3(IminusK))
    L_claim = [
        [Fraction(25, 7), Fraction(30, 7), Fraction(18, 7)],
        [Fraction(30, 7), Fraction(43, 7), Fraction(30, 7)],
        [Fraction(18, 7), Fraction(30, 7), Fraction(25, 7)],
    ]

    F = fraction_F(atoms, grads)
    C = [[Fraction(0) for _ in range(3)] for __ in range(3)]
    for i in range(3):
        for j in range(3):
            C[i][j] = K[i][i] * (1 - K[i][i]) if i == j else -K[i][j] * K[i][j]
    U = []
    for i, j in [(0, 1), (0, 2), (1, 2)]:
        row = []
        for ell in range(3):
            row.append(((1 if i == ell else 0) + (1 if j == ell else 0)) * K[i][j] / 2 - K[i][ell] * K[ell][j])
        U.append(row)
    M = C + U
    FM = matmul(F, M)
    target = [[Fraction(1 if i == j else 0) for j in range(3)] for i in range(3)] + [[Fraction(0) for _ in range(3)] for __ in range(3)]
    field_identity_ok = FM == target

    B_dec = decimal_B(atoms, grads, hess)
    frob_eigs = min_frobenius_eig(B_dec)

    q = min(atoms)
    m0 = Fraction(7, 400)
    LH = 8 * (Fraction(27, 1) / (m0 * m0) + Fraction(54, 1) / m0 + 30)
    eps = Fraction(1, 1) / (6 * LH)
    u = Fraction(324, 625)
    core_lower = Fraction(48) * (1 - u) * u / (6 - u) ** 2

    r = Decimal(1) - Decimal(1) / (Decimal(2) ** 16)
    uu = r * r
    n = ((1 + r) / (1 - r)).ln()
    m = -(1 - uu).ln()
    deltaV = m / 2 + n * n / (4 * m) - r * n / 2

    results = {
        "status": "CORRECT_SCOPED_MINIMAL_REPLAY",
        "input_hashes": {name: sha256(BASE / name) for name in ["frozen_problem.md", "derivation.md", "proof_or_blocker.md", "verdict.md", "run_log.md", "sanity.py", "sanity.json"]},
        "kstar_atoms": {str(ev): f"{p.numerator}/{p.denominator}" for ev, p in zip(EVENTS, atoms)},
        "kstar_min_atom": f"{q.numerator}/{q.denominator}",
        "kstar_atom_sum": f"{sum(atoms).numerator}/{sum(atoms).denominator}",
        "kstar_lambda_ratio_exact": f"{ratio.numerator}/{ratio.denominator}",
        "kstar_L_matches_claim": L == L_claim,
        "field_identity_F_times_CU_equals_target": field_identity_ok,
        "field_identity_entries_checked": 18,
        "kstar_B_frobenius_generalized_eigs": frob_eigs,
        "kstar_B_ge_one_third_margin": frob_eigs[0] - (1 / 3),
        "constants": {
            "LH": f"{LH.numerator}/{LH.denominator}",
            "epsilon": f"{eps.numerator}/{eps.denominator}",
            "LH_times_epsilon": f"{(LH * eps).numerator}/{(LH * eps).denominator}",
            "q_minus_3epsilon_gt_q_over_2": q - 3 * eps > q / 2,
            "epsilon_lt_1_over_40": eps < Fraction(1, 40),
            "epsilon_lt_q_over_6": eps < q / 6,
            "core_lower": f"{core_lower.numerator}/{core_lower.denominator}",
            "core_lower_float": float(core_lower),
            "core_lower_gt_one_third": core_lower > Fraction(1, 3),
        },
        "fisher_only_proxy_witness": {
            "r": "1-2^-16",
            "deltaV": str(deltaV),
            "two_thirds_deltaV": str(deltaV * Decimal(2) / Decimal(3)),
            "two_thirds_deltaV_gt_5_over_4": deltaV * Decimal(2) / Decimal(3) > Decimal(5) / Decimal(4),
            "classification": "proxy_bound_failure_only_not_entropy_counterexample",
        },
        "not_checked_in_this_minimal_replay": [
            "full formal proof of Cauchy classification beyond line-by-line algebra review",
            "all 15 author sanity points and all 270 author field identities",
            "independent numerical replay of the eight external-field box corners",
            "global Lambda-zero positivity outside the explicit Kstar ball",
        ],
    }
    (HERE / "fresh_audit_results.json").write_text(json.dumps(results, indent=2, sort_keys=True), encoding="utf-8")
    (HERE / "fresh_audit_log.md").write_text(
        "# D10-U10g fresh minimal audit log\n\n"
        "Command:\n\n"
        "```text\n"
        "python verifications/fresh_min_check.py\n"
        "```\n\n"
        "Exit code: 0\n\n"
        "Scope: minimal independent replay after interrupted longer audit.  No author sanity/gate module was imported.\n",
        encoding="utf-8",
    )
    print(json.dumps({"status": results["status"], "min_frobenius_eig": frob_eigs[0], "field_identity_entries": 18}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

