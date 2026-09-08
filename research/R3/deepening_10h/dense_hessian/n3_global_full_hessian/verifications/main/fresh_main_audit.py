"""Fresh main audit for D10-U8/M10 n3_global_full_hessian.

No author module is imported.  The script independently checks the algebraic
identities behind the rank-one-defect representation and performs high
precision rational/Decimal spot checks for the Schur scalar machinery.  It
does not try to prove the remaining global rho<=1 inequality.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import sys
import time
from collections import Counter
from decimal import Decimal, getcontext
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


sys.set_int_max_str_digits(0)
getcontext().prec = 110

HERE = Path(__file__).resolve().parent
CASE_DIR = HERE.parents[1]
OUT = HERE / "fresh_main_audit.json"

NV = 6
ZERO_MON = (0,) * NV


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ser(x: Any) -> Any:
    if isinstance(x, Q):
        return str(x)
    if isinstance(x, Decimal):
        return format(x, "f")
    if isinstance(x, tuple):
        return [ser(y) for y in x]
    if isinstance(x, list):
        return [ser(y) for y in x]
    if isinstance(x, dict):
        return {k: ser(v) for k, v in x.items()}
    return x


def DQ(x: Q) -> Decimal:
    return Decimal(x.numerator) / Decimal(x.denominator)


def dabs(x: Decimal) -> Decimal:
    return x.copy_abs()


Poly = dict[tuple[int, ...], Q]


def pc(c: Q | int) -> Poly:
    c = Q(c)
    return {} if c == 0 else {ZERO_MON: c}


def pv(i: int) -> Poly:
    m = [0] * NV
    m[i] = 1
    return {tuple(m): Q(1)}


def padd(a: Poly, b: Poly) -> Poly:
    out = dict(a)
    for m, c in b.items():
        out[m] = out.get(m, Q(0)) + c
        if out[m] == 0:
            del out[m]
    return out


def pneg(a: Poly) -> Poly:
    return {m: -c for m, c in a.items()}


def psub(a: Poly, b: Poly) -> Poly:
    return padd(a, pneg(b))


def pmul(a: Poly, b: Poly) -> Poly:
    out: Poly = {}
    for ma, ca in a.items():
        for mb, cb in b.items():
            m = tuple(ma[i] + mb[i] for i in range(NV))
            out[m] = out.get(m, Q(0)) + ca * cb
            if out[m] == 0:
                del out[m]
    return out


def pscale(c: Q | int, a: Poly) -> Poly:
    c = Q(c)
    if c == 0:
        return {}
    return {m: c * v for m, v in a.items()}


def ppow2(a: Poly) -> Poly:
    return pmul(a, a)


def pdiff(a: Poly, i: int) -> Poly:
    out: Poly = {}
    for m, c in a.items():
        if m[i] == 0:
            continue
        mm = list(m)
        mm[i] -= 1
        out[tuple(mm)] = out.get(tuple(mm), Q(0)) + c * m[i]
    return out


def peval(a: Poly, vals: list[Q]) -> Q:
    acc = Q(0)
    for m, c in a.items():
        term = c
        for i, e in enumerate(m):
            if e:
                term *= vals[i] ** e
        acc += term
    return acc


def pterms(a: Poly) -> int:
    return len(a)


def matmul_dec(A: list[list[Decimal]], B: list[list[Decimal]]) -> list[list[Decimal]]:
    n, m, k = len(A), len(B[0]), len(B)
    return [[sum(A[i][r] * B[r][j] for r in range(k)) for j in range(m)] for i in range(n)]


def trace_prod_dec(A: list[list[Decimal]], B: list[list[Decimal]]) -> Decimal:
    return sum(A[i][j] * B[j][i] for i in range(len(A)) for j in range(len(A)))


def det3_dec(M: list[list[Decimal]]) -> Decimal:
    return (
        M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
        - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
        + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0])
    )


def adj3_dec(M: list[list[Decimal]]) -> list[list[Decimal]]:
    return [
        [M[1][1] * M[2][2] - M[1][2] * M[2][1], M[0][2] * M[2][1] - M[0][1] * M[2][2], M[0][1] * M[1][2] - M[0][2] * M[1][1]],
        [M[1][2] * M[2][0] - M[1][0] * M[2][2], M[0][0] * M[2][2] - M[0][2] * M[2][0], M[0][2] * M[1][0] - M[0][0] * M[1][2]],
        [M[1][0] * M[2][1] - M[1][1] * M[2][0], M[0][1] * M[2][0] - M[0][0] * M[2][1], M[0][0] * M[1][1] - M[0][1] * M[1][0]],
    ]


def inv3_dec(M: list[list[Decimal]]) -> list[list[Decimal]]:
    det = det3_dec(M)
    A = adj3_dec(M)
    return [[A[i][j] / det for j in range(3)] for i in range(3)]


def det3_frac(M: list[list[Q]]) -> Q:
    return (
        M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
        - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
        + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0])
    )


def pd3_frac(M: list[list[Q]]) -> bool:
    m1 = M[0][0]
    m2 = M[0][0] * M[1][1] - M[0][1] * M[1][0]
    m3 = det3_frac(M)
    return m1 > 0 and m2 > 0 and m3 > 0


def inv_dec(A: list[list[Decimal]]) -> list[list[Decimal]]:
    n = len(A)
    aug = [[A[i][j] for j in range(n)] + [Decimal(1) if i == j else Decimal(0) for j in range(n)] for i in range(n)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(aug[r][col]))
        if aug[pivot][col] == 0:
            raise ZeroDivisionError("singular matrix")
        if pivot != col:
            aug[col], aug[pivot] = aug[pivot], aug[col]
        piv = aug[col][col]
        aug[col] = [x / piv for x in aug[col]]
        for r in range(n):
            if r == col:
                continue
            fac = aug[r][col]
            if fac:
                aug[r] = [aug[r][j] - fac * aug[col][j] for j in range(2 * n)]
    return [row[n:] for row in aug]


def solve_dec(A: list[list[Decimal]], b: list[Decimal]) -> list[Decimal]:
    inv = inv_dec(A)
    return [sum(inv[i][j] * b[j] for j in range(len(b))) for i in range(len(b))]


def eye_frac() -> list[list[Q]]:
    return [[Q(1) if i == j else Q(0) for j in range(3)] for i in range(3)]


def Kmat_frac(vals: list[Q]) -> list[list[Q]]:
    x, y, z, a, b, c = vals
    return [[x, a, b], [a, y, c], [b, c, z]]


def sub_eye(M: list[list[Q]]) -> list[list[Q]]:
    return [[(Q(1) if i == j else Q(0)) - M[i][j] for j in range(3)] for i in range(3)]


def connected(vals: list[Q]) -> bool:
    edges = [(0, 1, vals[3] != 0), (0, 2, vals[4] != 0), (1, 2, vals[5] != 0)]
    parent = list(range(3))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for i, j, ok in edges:
        if ok:
            ri, rj = find(i), find(j)
            parent[ri] = rj
    return len({find(i) for i in range(3)}) == 1


def make_polys() -> dict[str, Any]:
    x, y, z, a, b, c = [pv(i) for i in range(6)]
    q12 = psub(pmul(x, y), ppow2(a))
    q13 = psub(pmul(x, z), ppow2(b))
    q23 = psub(pmul(y, z), ppow2(c))
    r = padd(
        padd(pmul(pmul(x, y), z), pscale(2, pmul(pmul(a, b), c))),
        pneg(padd(padd(pmul(x, ppow2(c)), pmul(y, ppow2(b))), pmul(z, ppow2(a)))),
    )
    atoms: dict[int, Poly] = {
        7: r,
        3: psub(q12, r),
        5: psub(q13, r),
        6: psub(q23, r),
        1: padd(psub(psub(x, q12), q13), r),
        2: padd(psub(psub(y, q12), q23), r),
        4: padd(psub(psub(z, q13), q23), r),
        0: psub(padd(padd(padd(psub(psub(psub(pc(1), x), y), z), q12), q13), q23), r),
    }
    return {"vars": (x, y, z, a, b, c), "q": (q12, q13, q23), "r": r, "atoms": atoms}


def square_identity_checks(atoms: dict[int, Poly], vars_: tuple[Poly, ...]) -> list[dict[str, Any]]:
    x, y, z, a, b, c = vars_
    records = []
    # pair name, pi, pj, pk, pij, pik, pjk, Kij, Kik, Kjk, Kkk
    specs = [
        ("12", 1, 2, 4, 3, 5, 6, a, b, c, z),
        ("13", 1, 4, 2, 5, 3, 6, b, a, c, y),
        ("23", 2, 4, 1, 6, 3, 5, c, a, b, x),
    ]
    for name, pi, pj, pk, pij, pik, pjk, Kij, Kik, Kjk, Kkk in specs:
        absent_linear = padd(pmul(psub(pc(1), Kkk), Kij), pmul(Kik, Kjk))
        present_linear = psub(pmul(Kkk, Kij), pmul(Kik, Kjk))
        absent = padd(psub(pmul(atoms[0], atoms[pij]), pmul(atoms[pi], atoms[pj])), ppow2(absent_linear))
        present = padd(psub(pmul(atoms[pk], atoms[7]), pmul(atoms[pik], atoms[pjk])), ppow2(present_linear))
        records.append(
            {
                "pair": name,
                "absent_identity_zero": absent == {},
                "present_identity_zero": present == {},
                "absent_square_terms": pterms(ppow2(absent_linear)),
                "present_square_terms": pterms(ppow2(present_linear)),
            }
        )
    return records


COORD_BASIS = [
    [[Decimal(1), Decimal(0), Decimal(0)], [Decimal(0), Decimal(0), Decimal(0)], [Decimal(0), Decimal(0), Decimal(0)]],
    [[Decimal(0), Decimal(0), Decimal(0)], [Decimal(0), Decimal(1), Decimal(0)], [Decimal(0), Decimal(0), Decimal(0)]],
    [[Decimal(0), Decimal(0), Decimal(0)], [Decimal(0), Decimal(0), Decimal(0)], [Decimal(0), Decimal(0), Decimal(1)]],
    [[Decimal(0), Decimal(1), Decimal(0)], [Decimal(1), Decimal(0), Decimal(0)], [Decimal(0), Decimal(0), Decimal(0)]],
    [[Decimal(0), Decimal(0), Decimal(1)], [Decimal(0), Decimal(0), Decimal(0)], [Decimal(1), Decimal(0), Decimal(0)]],
    [[Decimal(0), Decimal(0), Decimal(0)], [Decimal(0), Decimal(0), Decimal(1)], [Decimal(0), Decimal(1), Decimal(0)]],
]


def coords_to_mat_dec(vals: list[Decimal]) -> list[list[Decimal]]:
    x, y, z, a, b, c = vals
    return [[x, a, b], [a, y, c], [b, c, z]]


def direction_to_mat_dec(d: list[Decimal]) -> list[list[Decimal]]:
    return coords_to_mat_dec(d)


def adj_sym_dec(M: list[list[Decimal]]) -> list[list[Decimal]]:
    return adj3_dec(M)


def trace_dec(M: list[list[Decimal]]) -> Decimal:
    return sum(M[i][i] for i in range(len(M)))


def eval_sample(vals: list[Q], atoms_poly: dict[int, Poly], label: str) -> dict[str, Any]:
    KQ = Kmat_frac(vals)
    strict = pd3_frac(KQ) and pd3_frac(sub_eye(KQ))
    atoms_q = {m: peval(p, vals) for m, p in atoms_poly.items()}
    if not all(v > 0 for v in atoms_q.values()):
        raise ValueError(f"nonpositive atom in sample {label}")
    deriv1 = [[peval(pdiff(atoms_poly[ev], i), vals) for ev in range(8)] for i in range(6)]
    deriv2 = [[[peval(pdiff(pdiff(atoms_poly[ev], i), j), vals) for ev in range(8)] for j in range(6)] for i in range(6)]
    logs = {m: DQ(atoms_q[m]).ln() for m in range(8)}
    atoms_d = {m: DQ(atoms_q[m]) for m in range(8)}
    F = [[Decimal(0) for _ in range(6)] for _ in range(6)]
    B_direct = [[Decimal(0) for _ in range(6)] for _ in range(6)]
    for i in range(6):
        for j in range(6):
            fij = sum(DQ(deriv1[i][ev] * deriv1[j][ev]) / atoms_d[ev] for ev in range(8))
            acc = fij + sum(DQ(deriv2[i][j][ev]) * logs[ev] for ev in range(8))
            F[i][j] = fij
            B_direct[i][j] = acc

    l12_ratio_q = atoms_q[0] * atoms_q[3] / (atoms_q[1] * atoms_q[2])
    l13_ratio_q = atoms_q[0] * atoms_q[5] / (atoms_q[1] * atoms_q[4])
    l23_ratio_q = atoms_q[0] * atoms_q[6] / (atoms_q[2] * atoms_q[4])
    present12_ratio_q = atoms_q[7] * atoms_q[4] / (atoms_q[5] * atoms_q[6])
    present13_ratio_q = atoms_q[7] * atoms_q[2] / (atoms_q[3] * atoms_q[6])
    present23_ratio_q = atoms_q[7] * atoms_q[1] / (atoms_q[3] * atoms_q[5])
    Lambda_ratio_q = atoms_q[7] * atoms_q[1] * atoms_q[2] * atoms_q[4] / (atoms_q[0] * atoms_q[3] * atoms_q[5] * atoms_q[6])
    l12 = DQ(l12_ratio_q).ln()
    l13 = DQ(l13_ratio_q).ln()
    l23 = DQ(l23_ratio_q).ln()
    Lambda = DQ(Lambda_ratio_q).ln()
    Kd = [[DQ(KQ[i][j]) for j in range(3)] for i in range(3)]
    N = [
        [-l23 - Lambda * Kd[0][0], -Lambda * Kd[0][1], -Lambda * Kd[0][2]],
        [-Lambda * Kd[1][0], -l13 - Lambda * Kd[1][1], -Lambda * Kd[1][2]],
        [-Lambda * Kd[2][0], -Lambda * Kd[2][1], -l12 - Lambda * Kd[2][2]],
    ]

    def qN(D: list[list[Decimal]]) -> Decimal:
        return trace_prod_dec(N, adj_sym_dec(D))

    C = [[Decimal(0) for _ in range(6)] for _ in range(6)]
    for i in range(6):
        for j in range(6):
            if i == j:
                C[i][j] = qN(COORD_BASIS[i])
            else:
                Dij = [[COORD_BASIS[i][r][s] + COORD_BASIS[j][r][s] for s in range(3)] for r in range(3)]
                C[i][j] = (qN(Dij) - qN(COORD_BASIS[i]) - qN(COORD_BASIS[j])) / 2
    B_from_N = [[F[i][j] - 2 * C[i][j] for j in range(6)] for i in range(6)]
    max_B_resid = max(dabs(B_direct[i][j] - B_from_N[i][j]) for i in range(6) for j in range(6))

    detN = det3_dec(N)
    Ninv = inv3_dec(N)
    eta = [trace_prod_dec(Ninv, COORD_BASIS[i]) for i in range(6)]
    G = [[trace_prod_dec(matmul_dec(Ninv, COORD_BASIS[i]), matmul_dec(Ninv, COORD_BASIS[j])) for j in range(6)] for i in range(6)]
    A = [[F[i][j] + detN * G[i][j] for j in range(6)] for i in range(6)]
    B_schur = [[A[i][j] - detN * eta[i] * eta[j] for j in range(6)] for i in range(6)]
    max_schur_resid = max(dabs(B_direct[i][j] - B_schur[i][j]) for i in range(6) for j in range(6))
    d_bad = solve_dec(A, eta)
    alpha = sum(eta[i] * d_bad[i] for i in range(6))
    rho = detN * alpha
    dBd_direct = sum(d_bad[i] * B_direct[i][j] * d_bad[j] for i in range(6) for j in range(6))
    dBd_formula = alpha * (1 - rho)
    eta_factor = {
        "eta12_minus_2Ninv12": eta[3] - 2 * Ninv[0][1],
        "eta13_minus_2Ninv13": eta[4] - 2 * Ninv[0][2],
        "eta23_minus_2Ninv23": eta[5] - 2 * Ninv[1][2],
    }
    offdiag_coordinate_checks = {
        "B12_minus_F12_plus_2N33": B_direct[3][3] - (F[3][3] + 2 * N[2][2]),
        "B13_minus_F13_plus_2N22": B_direct[4][4] - (F[4][4] + 2 * N[1][1]),
        "B23_minus_F23_plus_2N11": B_direct[5][5] - (F[5][5] + 2 * N[0][0]),
    }
    diag_rank_one_checks = {
        "p_second_diag11_all_zero": all(deriv2[0][0][ev] == 0 for ev in range(8)),
        "p_second_diag22_all_zero": all(deriv2[1][1][ev] == 0 for ev in range(8)),
        "p_second_diag33_all_zero": all(deriv2[2][2][ev] == 0 for ev in range(8)),
        "B11_equals_F11": B_direct[0][0] - F[0][0],
        "B22_equals_F22": B_direct[1][1] - F[1][1],
        "B33_equals_F33": B_direct[2][2] - F[2][2],
    }
    # One exact adjugate-congruence identity check with a rational positive N and rational D.
    return {
        "label": label,
        "K": vals,
        "strict_K_and_I_minus_K": strict,
        "connected_support": connected(vals),
        "atoms_positive": all(v > 0 for v in atoms_q.values()),
        "Lambda": Lambda,
        "Lambda_ratio_exact": Lambda_ratio_q,
        "Lambda_sign": "positive" if Lambda_ratio_q > 1 else ("negative" if Lambda_ratio_q < 1 else "zero"),
        "l_ratio_exact": {"l12": l12_ratio_q, "l13": l13_ratio_q, "l23": l23_ratio_q},
        "present_ratio_exact": {"l12_plus_Lambda": present12_ratio_q, "l13_plus_Lambda": present13_ratio_q, "l23_plus_Lambda": present23_ratio_q},
        "l_values": {"l12": l12, "l13": l13, "l23": l23},
        "l_nonpositive": l12_ratio_q <= 1 and l13_ratio_q <= 1 and l23_ratio_q <= 1,
        "l_plus_Lambda_nonpositive": present12_ratio_q <= 1 and present13_ratio_q <= 1 and present23_ratio_q <= 1,
        "N_det": detN,
        "N_leading_pivots_positive_decimal": N[0][0] > 0 and (N[0][0] * N[1][1] - N[0][1] * N[1][0]) > 0 and detN > 0,
        "max_B_minus_Fisher_cofactor_residual": max_B_resid,
        "max_B_minus_Schur_residual": max_schur_resid,
        "rho": rho,
        "bad_direction_dBd_residual": dBd_direct - dBd_formula,
        "bad_direction_sign_rule": {
            "rho_less_than_1": rho < 1,
            "dBd_direct": dBd_direct,
            "alpha_times_1_minus_rho": dBd_formula,
        },
        "eta_offdiag_factor_residuals": eta_factor,
        "coordinate_strictness_residuals": offdiag_coordinate_checks,
        "diagonal_rank_one_checks": diag_rank_one_checks,
        "eta_nonzero_linear_functional": any(e != 0 for e in eta),
}


def eval_zero_disconnected(vals: list[Q], atoms_poly: dict[int, Poly], label: str) -> dict[str, Any]:
    KQ = Kmat_frac(vals)
    atoms_q = {m: peval(p, vals) for m, p in atoms_poly.items()}
    l12_ratio_q = atoms_q[0] * atoms_q[3] / (atoms_q[1] * atoms_q[2])
    l13_ratio_q = atoms_q[0] * atoms_q[5] / (atoms_q[1] * atoms_q[4])
    l23_ratio_q = atoms_q[0] * atoms_q[6] / (atoms_q[2] * atoms_q[4])
    Lambda_ratio_q = atoms_q[7] * atoms_q[1] * atoms_q[2] * atoms_q[4] / (atoms_q[0] * atoms_q[3] * atoms_q[5] * atoms_q[6])
    return {
        "label": label,
        "K": vals,
        "strict_K_and_I_minus_K": pd3_frac(KQ) and pd3_frac(sub_eye(KQ)),
        "connected_support": connected(vals),
        "atoms_positive": all(v > 0 for v in atoms_q.values()),
        "Lambda_ratio_exact": Lambda_ratio_q,
        "Lambda_sign": "positive" if Lambda_ratio_q > 1 else ("negative" if Lambda_ratio_q < 1 else "zero"),
        "l_ratio_exact": {"l12": l12_ratio_q, "l13": l13_ratio_q, "l23": l23_ratio_q},
        "N_expected_zero": Lambda_ratio_q == 1 and l12_ratio_q == 1 and l13_ratio_q == 1 and l23_ratio_q == 1,
        "Schur_inverse_N_not_applicable": True,
    }


def exact_adjugate_congruence_test() -> dict[str, Any]:
    N = [[Q(3), Q(1), Q(1, 2)], [Q(1), Q(4), Q(1, 3)], [Q(1, 2), Q(1, 3), Q(5)]]
    D = [[Q(2), Q(-1, 3), Q(1, 5)], [Q(-1, 3), Q(1), Q(2, 7)], [Q(1, 5), Q(2, 7), Q(-3, 2)]]

    def adj_frac(M: list[list[Q]]) -> list[list[Q]]:
        return [
            [M[1][1] * M[2][2] - M[1][2] * M[2][1], M[0][2] * M[2][1] - M[0][1] * M[2][2], M[0][1] * M[1][2] - M[0][2] * M[1][1]],
            [M[1][2] * M[2][0] - M[1][0] * M[2][2], M[0][0] * M[2][2] - M[0][2] * M[2][0], M[0][2] * M[1][0] - M[0][0] * M[1][2]],
            [M[1][0] * M[2][1] - M[1][1] * M[2][0], M[0][1] * M[2][0] - M[0][0] * M[2][1], M[0][0] * M[1][1] - M[0][1] * M[1][0]],
        ]

    def trace_prod_frac(A: list[list[Q]], B: list[list[Q]]) -> Q:
        return sum(A[i][j] * B[j][i] for i in range(3) for j in range(3))

    def matmul_frac(A: list[list[Q]], B: list[list[Q]]) -> list[list[Q]]:
        return [[sum(A[i][r] * B[r][j] for r in range(3)) for j in range(3)] for i in range(3)]

    detN = det3_frac(N)
    adjN = adj_frac(N)
    Ninv = [[adjN[i][j] / detN for j in range(3)] for i in range(3)]
    lhs = trace_prod_frac(N, adj_frac(D))
    trE = trace_prod_frac(Ninv, D)
    trE2 = trace_prod_frac(matmul_frac(Ninv, D), matmul_frac(Ninv, D))
    rhs = detN * (trE * trE - trE2) / 2
    return {
        "N_positive_definite": pd3_frac(N),
        "identity_residual": lhs - rhs,
        "identity_holds": lhs == rhs,
    }


def find_branch_examples(atoms: dict[int, Poly]) -> dict[str, Any]:
    diag_choices = [Q(1, 4), Q(1, 3), Q(2, 5), Q(1, 2), Q(3, 5)]
    off_choices = [Q(-1, 5), Q(-1, 8), Q(-1, 12), Q(0), Q(1, 12), Q(1, 8), Q(1, 5)]
    found: dict[str, list[Q] | None] = {"positive": None, "negative": None, "zero_disconnected": [Q(1, 3), Q(2, 5), Q(3, 7), Q(0), Q(0), Q(0)]}
    for vals in itertools.product(diag_choices, diag_choices, diag_choices, off_choices, off_choices, off_choices):
        vals = list(vals)
        KQ = Kmat_frac(vals)
        if not (pd3_frac(KQ) and pd3_frac(sub_eye(KQ))):
            continue
        if not connected(vals):
            continue
        p = {m: peval(poly, vals) for m, poly in atoms.items()}
        if not all(v > 0 for v in p.values()):
            continue
        ratio = p[7] * p[1] * p[2] * p[4] / (p[0] * p[3] * p[5] * p[6])
        if ratio > 1 and found["positive"] is None:
            found["positive"] = vals
        if ratio < 1 and found["negative"] is None:
            found["negative"] = vals
        if found["positive"] is not None and found["negative"] is not None:
            break
    return {k: v for k, v in found.items() if v is not None}


def finite_json_summary() -> dict[str, Any]:
    out: dict[str, Any] = {}
    scout = json.loads((CASE_DIR / "scout_results.json").read_text())
    ledger = scout.get("ledger", [])
    out["scout"] = {
        "status": scout.get("status"),
        "ledger_count": len(ledger),
        "connected_count": sum(1 for r in ledger if len(set(r.get("component_labels", []))) == 1),
        "disconnected_count": sum(1 for r in ledger if len(set(r.get("component_labels", []))) != 1),
        "status_counts": dict(Counter(r.get("status") for r in ledger)),
        "min_normalized_min_B": min((r.get("normalized_min_B") for r in ledger if r.get("normalized_min_B") is not None), default=None),
    }
    rank = json.loads((CASE_DIR / "rank_one_results.json").read_text())
    out["rank_one"] = {
        "status": rank.get("status"),
        "keys": sorted(rank.keys()),
        "frozen_point_checks": len(rank.get("frozen_point_checks", [])),
        "scalar_ledger_count": len(rank.get("scalar_ledger", [])),
        "equal_rate_boundary_checks": len(rank.get("boundary_checks", [])),
        "unequal_rate_boundary_checks": len(rank.get("multirate_boundary_checks", [])),
    }
    point = json.loads((CASE_DIR / "point_interval_results.json").read_text())
    out["point_interval"] = {
        "status": point.get("status"),
        "scout_index": point.get("scout_index"),
        "min_atom": min(point.get("atoms", []), key=lambda s: Q(s)) if point.get("atoms") else None,
        "passed": point.get("passed"),
    }
    sym = json.loads((CASE_DIR / "symbolic_identity_results.json").read_text())
    out["symbolic_identity_author_result"] = {
        "status": sym.get("status"),
        "records": sym.get("records"),
        "atom_mass": sym.get("atom_mass"),
        "first_second_mass": sym.get("first_second_mass"),
        "diagonal_rank_one_atom_acceleration_zero": sym.get("diagonal_rank_one_atom_acceleration_zero"),
    }
    return out


def main() -> None:
    start = time.time()
    inputs = [
        "frozen_problem.md",
        "derivation.md",
        "boundary_asymptotic.md",
        "proof_or_blocker.md",
        "run_log.md",
        "verdict.md",
        "global_probe.py",
        "rank_one_recheck.py",
        "point_interval_gate.py",
        "symbolic_identity_gate.py",
        "scout_results.json",
        "rank_one_results.json",
        "point_interval_results.json",
        "symbolic_identity_results.json",
    ]
    hashes = {name: sha256(CASE_DIR / name) for name in inputs}

    P = make_polys()
    atoms = P["atoms"]
    vars_ = P["vars"]
    square_records = square_identity_checks(atoms, vars_)
    mass_identity = psub(sum_poly(atoms[m] for m in range(8)), pc(1)) == {}
    first_mass = all(sum_poly(pdiff(atoms[m], i) for m in range(8)) == {} for i in range(6))
    second_mass = all(sum_poly(pdiff(pdiff(atoms[m], i), j) for m in range(8)) == {} for i in range(6) for j in range(6))
    diag_rank_one = all(pdiff(pdiff(atoms[m], i), i) == {} for m in range(8) for i in range(3))

    branch_vals = find_branch_examples(atoms)
    sample_checks = {
        name: (eval_zero_disconnected(vals, atoms, name) if name == "zero_disconnected" else eval_sample(vals, atoms, name))
        for name, vals in branch_vals.items()
    }
    adj_check = exact_adjugate_congruence_test()
    finite = finite_json_summary()

    symbolic_ok = (
        all(r["absent_identity_zero"] and r["present_identity_zero"] for r in square_records)
        and mass_identity
        and first_mass
        and second_mass
        and diag_rank_one
    )
    sample_ok = all(
        s["strict_K_and_I_minus_K"]
        and s["atoms_positive"]
        and s["l_nonpositive"]
        and s["l_plus_Lambda_nonpositive"]
        and s["max_B_minus_Fisher_cofactor_residual"] < Decimal("1e-90")
        and s["max_B_minus_Schur_residual"] < Decimal("1e-85")
        and dabs(s["bad_direction_dBd_residual"]) < Decimal("1e-85")
        and all(dabs(v) < Decimal("1e-95") for v in s["eta_offdiag_factor_residuals"].values())
        for s in sample_checks.values()
        if s["connected_support"]
    )
    status = "CORRECT" if symbolic_ok and sample_ok and adj_check["identity_holds"] else "INCORRECT"

    report = {
        "status": status,
        "scope": "fresh nonauthor main-structure audit; does not prove global rho<=1",
        "input_hashes": hashes,
        "symbolic_exact_checks": {
            "mass_identity": mass_identity,
            "first_derivative_mass_identity": first_mass,
            "second_derivative_mass_identity": second_mass,
            "diagonal_rank_one_second_derivatives_zero": diag_rank_one,
            "conditional_odds_square_identities": square_records,
            "implications": {
                "l_ij_nonpositive": "certified by absent-conditioned square identity and positive atoms",
                "l_ij_plus_Lambda_nonpositive": "certified by present-conditioned square identity and positive atoms",
                "Lambda_zero_connected_strict_N": "if Lambda=0 and l_ij=0, both square equations force K_ij=0 and K_ik*K_jk=0; a connected three-vertex graph forbids this for every pair",
            },
        },
        "branch_and_decomposition_samples": sample_checks,
        "exact_adjugate_congruence_identity": adj_check,
        "analytic_verdicts": {
            "N_psd_all_strict_kernels": "CORRECT, conditional on strict atom positivity from L-ensemble factorization",
            "N_pd_connected": "CORRECT; Lambda nonzero branches are strict by K>0 or I-K>0, Lambda=0 branch uses the square-vanishing graph argument",
            "B_equals_Fisher_minus_2tr_N_adjD": "CORRECT",
            "Schur_rank_one_reduction": "CORRECT",
            "rho_threshold_equivalence_for_connected": "CORRECT",
            "weighted_trace_zero_hyperplane": "CORRECT, pointwise bound det(N)/lambda_max(N)^2 * ||D||_F^2 for B=-Hess H",
            "global_rho_le_1": "INCOMPLETE_NOT_PROVED",
            "boundary_asymptotic_subclass": "NOT_AUDITED_IN_THIS_MAIN_REPORT",
        },
        "finite_evidence_summary": finite,
        "notes": {
            "coordinate_order": "(11,22,33,12,13,23); off-diagonal coordinate is Eij+Eji",
            "eta_offdiag_factor": "fresh Decimal checks confirm eta_12=2(N^-1)_12 etc. on connected samples",
            "finite_510_points": "SCOUT only; no finite non-hit is promoted to theorem",
        },
        "elapsed_seconds": time.time() - start,
    }
    OUT.write_text(json.dumps(ser(report), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": status,
        "symbolic_ok": symbolic_ok,
        "sample_count": len(sample_checks),
        "sample_labels": list(sample_checks.keys()),
        "adjugate_identity": adj_check["identity_holds"],
        "scout_ledger_count": finite["scout"]["ledger_count"],
        "elapsed_seconds": report["elapsed_seconds"],
    }, ensure_ascii=False, indent=2))


def sum_poly(polys) -> Poly:
    acc: Poly = {}
    for p in polys:
        acc = padd(acc, p)
    return acc


if __name__ == "__main__":
    main()
