#!/usr/bin/env python3
"""Independent C2 formula/certificate checks for the five-point rank-three face.

This script intentionally rebuilds the five-point U, all exact event
probability polynomials, and the low-order matrix formulas from scratch.
It uses only rational arithmetic for algebraic comparisons. Decimal output
is used only for entropy/log diagnostics and finite-difference calibration.
"""

from __future__ import annotations

import itertools
import json
import math
import platform
from fractions import Fraction
from pathlib import Path

import mpmath as mp


OUT_DIR = Path(__file__).resolve().parent
EVENT_TSV = OUT_DIR / "event_jets.tsv"
INPUT_JSON = OUT_DIR / "exact_input.json"


def F(n: int, d: int = 1) -> Fraction:
    return Fraction(n, d)


def fstr(x: Fraction) -> str:
    if x.denominator == 1:
        return str(x.numerator)
    return f"{x.numerator}/{x.denominator}"


def poly_trim(p):
    q = list(p)
    while len(q) > 1 and q[-1] == 0:
        q.pop()
    return q


def poly_zero():
    return [F(0)]


def poly_one():
    return [F(1)]


def poly_const(c):
    return [Fraction(c)]


def poly_linear(c0, c1):
    return poly_trim([Fraction(c0), Fraction(c1)])


def poly_add(a, b):
    m = max(len(a), len(b))
    out = [F(0)] * m
    for i in range(m):
        out[i] = (a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)
    return poly_trim(out)


def poly_neg(a):
    return [-x for x in a]


def poly_sub(a, b):
    return poly_add(a, poly_neg(b))


def poly_mul(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[i + j] += ai * bj
    return poly_trim(out)


def poly_scale(a, c):
    return poly_trim([Fraction(c) * x for x in a])


def poly_eval_frac(p, t):
    total = F(0)
    power = F(1)
    for coeff in p:
        total += coeff * power
        power *= t
    return total


def poly_eval_mp(p, t):
    total = mp.mpf("0")
    power = mp.mpf("1")
    for coeff in p:
        total += mp.mpf(coeff.numerator) / mp.mpf(coeff.denominator) * power
        power *= t
    return total


def jet(p):
    c0 = p[0] if len(p) > 0 else F(0)
    c1 = p[1] if len(p) > 1 else F(0)
    c2 = p[2] if len(p) > 2 else F(0)
    return c0, c1, 2 * c2


def parity(perm):
    inv = 0
    for i in range(len(perm)):
        for j in range(i + 1, len(perm)):
            inv += perm[i] > perm[j]
    return -1 if inv % 2 else 1


def det_poly(mat):
    n = len(mat)
    if n == 0:
        return poly_one()
    total = poly_zero()
    for perm in itertools.permutations(range(n)):
        prod = poly_one()
        for i, j in enumerate(perm):
            prod = poly_mul(prod, mat[i][j])
        if parity(perm) == 1:
            total = poly_add(total, prod)
        else:
            total = poly_sub(total, prod)
    return total


def det_frac(mat):
    return det_poly([[poly_const(x) for x in row] for row in mat])[0]


def matmul_frac(A, B):
    rows = len(A)
    cols = len(B[0])
    inner = len(B)
    return [[sum(A[i][k] * B[k][j] for k in range(inner)) for j in range(cols)] for i in range(rows)]


def transpose(A):
    return [list(row) for row in zip(*A)]


def householder(v):
    n = len(v)
    vv = sum(x * x for x in v)
    return [[(F(1) if i == j else F(0)) - 2 * v[i] * v[j] / vv for j in range(n)] for i in range(n)]


def build_U():
    a = [F(1), F(2), F(3), F(4), F(5)]
    b = [F(2), F(-1), F(3), F(-2), F(1)]
    H_a = householder(a)
    H_b = householder(b)
    H = matmul_frac(H_a, H_b)
    return [row[:3] for row in H]


def cross(u, v):
    return [
        u[1] * v[2] - u[2] * v[1],
        u[2] * v[0] - u[0] * v[2],
        u[0] * v[1] - u[1] * v[0],
    ]


def dot_frac(u, v):
    return sum(x * y for x, y in zip(u, v))


def mat_poly_add(A, B):
    return [[poly_add(A[i][j], B[i][j]) for j in range(len(A[0]))] for i in range(len(A))]


def mat_poly_sub(A, B):
    return [[poly_sub(A[i][j], B[i][j]) for j in range(len(A[0]))] for i in range(len(A))]


def mat_poly_mul(A, B):
    rows = len(A)
    cols = len(B[0])
    inner = len(B)
    out = [[poly_zero() for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            acc = poly_zero()
            for k in range(inner):
                acc = poly_add(acc, poly_mul(A[i][k], B[k][j]))
            out[i][j] = acc
    return out


def mat_poly_scalar_mul(P, A):
    return [[poly_mul(P, A[i][j]) for j in range(len(A[0]))] for i in range(len(A))]


def identity_poly(n, scale=None):
    if scale is None:
        scale = poly_one()
    return [[scale if i == j else poly_zero() for j in range(n)] for i in range(n)]


def submatrix(M, rows, cols):
    return [[M[i][j] for j in cols] for i in rows]


def minor_poly(M, row, col):
    rows = [i for i in range(len(M)) if i != row]
    cols = [j for j in range(len(M)) if j != col]
    return det_poly(submatrix(M, rows, cols))


def adjugate_poly(M):
    n = len(M)
    out = [[poly_zero() for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            cofactor = minor_poly(M, j, i)
            if (i + j) % 2:
                cofactor = poly_neg(cofactor)
            out[i][j] = cofactor
    return out


def quad_form_const_poly(vec, M):
    acc = poly_zero()
    for i in range(len(vec)):
        for j in range(len(vec)):
            acc = poly_add(acc, poly_scale(M[i][j], vec[i] * vec[j]))
    return acc


def build_A_V():
    A = [
        [F(1, 5), F(0), F(0)],
        [F(0), F(1, 3), F(0)],
        [F(0), F(0), F(1, 2)],
    ]
    V = [
        [F(1, 50), F(1, 200), F(-1, 180)],
        [F(1, 200), F(1, 30), F(1, 210)],
        [F(-1, 180), F(1, 210), F(1, 20)],
    ]
    return A, V


def matrix_poly_from_A_V(A, V):
    return [[poly_linear(A[i][j], V[i][j]) for j in range(3)] for i in range(3)]


def build_K_poly(U, A_poly):
    n = len(U)
    K = [[poly_zero() for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            acc = poly_zero()
            for a in range(3):
                for b in range(3):
                    acc = poly_add(acc, poly_scale(A_poly[a][b], U[i][a] * U[j][b]))
            K[i][j] = acc
    return K


def all_subsets(n):
    items = range(n)
    for r in range(n + 1):
        for combo in itertools.combinations(items, r):
            yield combo


def subset_label(S):
    if not S:
        return "empty"
    return "".join(str(i + 1) for i in S)


def event_polys_inclusion(K):
    n = len(K)
    minors = {}
    for T in all_subsets(n):
        minors[T] = det_poly(submatrix(K, T, T))
    events = {}
    all_items = set(range(n))
    for S in all_subsets(n):
        comp = sorted(all_items - set(S))
        p = poly_zero()
        for extra_len in range(len(comp) + 1):
            for extra in itertools.combinations(comp, extra_len):
                T = tuple(sorted(S + extra))
                term = minors[T]
                if extra_len % 2:
                    p = poly_sub(p, term)
                else:
                    p = poly_add(p, term)
        events[S] = p
    return events, minors


def event_polys_low_formula(U, A_poly):
    n = len(U)
    d = det_poly(A_poly)
    I3 = identity_poly(3)
    A2 = mat_poly_mul(A_poly, A_poly)
    trA = poly_add(poly_add(A_poly[0][0], A_poly[1][1]), A_poly[2][2])
    one_minus_trA = poly_sub(poly_one(), trA)
    singleton_M = mat_poly_add(mat_poly_add(A2, mat_poly_scalar_mul(one_minus_trA, A_poly)), identity_poly(3, d))
    adjA = adjugate_poly(A_poly)
    pair_M = mat_poly_sub(adjA, identity_poly(3, d))
    events = {}
    for S in all_subsets(n):
        if len(S) == 0:
            IA = mat_poly_sub(I3, A_poly)
            events[S] = det_poly(IA)
        elif len(S) == 1:
            r = U[S[0]]
            events[S] = quad_form_const_poly(r, singleton_M)
        elif len(S) == 2:
            w = cross(U[S[0]], U[S[1]])
            events[S] = quad_form_const_poly(w, pair_M)
        elif len(S) == 3:
            U_S = [U[i] for i in S]
            q = det_frac(U_S) ** 2
            events[S] = poly_scale(d, q)
        else:
            events[S] = poly_zero()
    return events, d


def entropy_from_event_polys(events, t):
    H = mp.mpf("0")
    for p_poly in events.values():
        p = poly_eval_mp(p_poly, t)
        if abs(p) < mp.mpf("1e-90"):
            continue
        if p <= 0:
            raise ValueError(f"nonpositive probability {p} at t={t}")
        H -= p * mp.log(p)
    return H


def mp_frac(x):
    return mp.mpf(x.numerator) / mp.mpf(x.denominator)


def analytic_by_size(events):
    out = {}
    sums = {"p": F(0), "p1": F(0), "p2": F(0)}
    for S, p_poly in events.items():
        p0, p1, p2 = jet(p_poly)
        sums["p"] += p0
        sums["p1"] += p1
        sums["p2"] += p2
        k = len(S)
        if k not in out:
            out[k] = {"count_pos": 0, "count_zero": 0, "fisher": mp.mpf("0"), "log_accel": mp.mpf("0")}
        if p0 == 0:
            out[k]["count_zero"] += 1
            if p1 != 0 or p2 != 0:
                out[k]["zero_nonzero_jet"] = True
            continue
        out[k]["count_pos"] += 1
        p0m = mp_frac(p0)
        p1m = mp_frac(p1)
        p2m = mp_frac(p2)
        out[k]["fisher"] += (p1m * p1m) / p0m
        out[k]["log_accel"] += -p2m * mp.log(p0m)
    for k in out:
        out[k]["curvature"] = -out[k]["fisher"] + out[k]["log_accel"]
    return out, sums


def q_values(U):
    qs = {}
    for S in itertools.combinations(range(len(U)), 3):
        qs[S] = det_frac([U[i] for i in S]) ** 2
    return qs


def frobenius_commutator_norm2(A, V):
    AV = matmul_frac(A, V)
    VA = matmul_frac(V, A)
    C = [[AV[i][j] - VA[i][j] for j in range(3)] for i in range(3)]
    return sum(C[i][j] * C[i][j] for i in range(3) for j in range(3))


def charpoly_coeffs_3x3(M):
    tr = sum(M[i][i] for i in range(3))
    trM2 = sum(M[i][j] * M[j][i] for i in range(3) for j in range(3))
    e2 = (tr * tr - trM2) / 2
    d = det_frac(M)
    return tr, e2, d


def gershgorin_bounds(M):
    lower = None
    upper = None
    for i in range(len(M)):
        center = M[i][i]
        radius = sum(abs(M[i][j]) for j in range(len(M)) if j != i)
        lo = center - radius
        hi = center + radius
        lower = lo if lower is None else min(lower, lo)
        upper = hi if upper is None else max(upper, hi)
    return lower, upper


def det_derivatives_from_poly(d):
    d0, d1, d2 = jet(d)
    return d0, d1, d2


def write_exact_input(U, A, V, q):
    obj = {
        "indexing": "events use 1-based labels in output; matrices use row order 1..5 and columns 1..3",
        "a": [fstr(x) for x in [F(1), F(2), F(3), F(4), F(5)]],
        "b": [fstr(x) for x in [F(2), F(-1), F(3), F(-2), F(1)]],
        "U": [[fstr(x) for x in row] for row in U],
        "A": [[fstr(x) for x in row] for row in A],
        "V": [[fstr(x) for x in row] for row in V],
        "q_by_triple": {subset_label(S): fstr(val) for S, val in q.items()},
    }
    INPUT_JSON.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_event_tsv(events, formula_events):
    lines = ["event\tsize\tp\tp_prime\tp_second\tformula_match"]
    for S in all_subsets(5):
        p0, p1, p2 = jet(events[S])
        lines.append(
            "\t".join(
                [
                    subset_label(S),
                    str(len(S)),
                    fstr(p0),
                    fstr(p1),
                    fstr(p2),
                    str(poly_trim(events[S]) == poly_trim(formula_events[S])),
                ]
            )
        )
    EVENT_TSV.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    mp.mp.dps = 100
    U = build_U()
    A, V = build_A_V()
    A_poly = matrix_poly_from_A_V(A, V)
    K_poly = build_K_poly(U, A_poly)
    inclusion_events, minors = event_polys_inclusion(K_poly)
    formula_events, d_poly = event_polys_low_formula(U, A_poly)
    q = q_values(U)

    write_exact_input(U, A, V, q)
    write_event_tsv(inclusion_events, formula_events)

    formula_mismatches = [subset_label(S) for S in all_subsets(5) if poly_trim(inclusion_events[S]) != poly_trim(formula_events[S])]
    zero_events = [subset_label(S) for S, p in inclusion_events.items() if jet(p)[0] == 0]
    positive_events = [subset_label(S) for S, p in inclusion_events.items() if jet(p)[0] > 0]
    zero_bad_jets = [subset_label(S) for S, p in inclusion_events.items() if jet(p)[0] == 0 and (jet(p)[1] != 0 or jet(p)[2] != 0)]

    q_prompt = {
        (0, 1, 2): F(123201, 1092025),
        (0, 1, 3): F(374544, 1092025),
        (0, 1, 4): F(1296, 43681),
        (0, 2, 3): F(144, 3025),
        (0, 2, 4): F(49284, 1092025),
        (0, 3, 4): F(254016, 1092025),
        (1, 2, 3): F(576, 9025),
        (1, 2, 4): F(30276, 1092025),
        (1, 3, 4): F(28224, 1092025),
        (2, 3, 4): F(3136, 43681),
    }
    q_mismatches = [subset_label(S) for S in q if q[S] != q_prompt[S]]
    q_sum = sum(q.values(), F(0))
    c = -sum(mp_frac(val) * mp.log(mp_frac(val)) for val in q.values())

    by_size, sums = analytic_by_size(inclusion_events)
    Hpp = sum((v["curvature"] for v in by_size.values()), mp.mpf("0"))

    H0 = entropy_from_event_polys(inclusion_events, mp.mpf("0"))
    fd_rows = []
    for k in [8, 12, 16, 20]:
        h = mp.power(2, -k)
        fd = (entropy_from_event_polys(inclusion_events, h) - 2 * H0 + entropy_from_event_polys(inclusion_events, -h)) / (h * h)
        fd_rows.append((f"2^-{k}", fd, fd - Hpp))

    d0, d1, d2 = det_derivatives_from_poly(d_poly)
    F_top = (mp_frac(d1) * mp_frac(d1)) / mp_frac(d0)
    c_d2 = c * mp_frac(d2)
    bound_rhs = (mp.mpf(2) * c / 3) * F_top

    comm_norm2 = frobenius_commutator_norm2(A, V)
    A_gersh = gershgorin_bounds(A)
    I_minus_A = [[(F(1) if i == j else F(0)) - A[i][j] for j in range(3)] for i in range(3)]
    IA_gersh = gershgorin_bounds(I_minus_A)
    max_h = F(1, 256)
    A_plus = [[A[i][j] + max_h * V[i][j] for j in range(3)] for i in range(3)]
    A_minus = [[A[i][j] - max_h * V[i][j] for j in range(3)] for i in range(3)]
    Ap_gersh = gershgorin_bounds(A_plus)
    Am_gersh = gershgorin_bounds(A_minus)
    I_minus_Ap = [[(F(1) if i == j else F(0)) - A_plus[i][j] for j in range(3)] for i in range(3)]
    I_minus_Am = [[(F(1) if i == j else F(0)) - A_minus[i][j] for j in range(3)] for i in range(3)]
    IAp_gersh = gershgorin_bounds(I_minus_Ap)
    IAm_gersh = gershgorin_bounds(I_minus_Am)

    print("independent_c2_verify.py")
    print(f"python: {platform.python_version()}")
    print(f"mpmath: {mp.__version__}")
    print()
    print("exact input written:", INPUT_JSON.name)
    print("event jet table written:", EVENT_TSV.name)
    print()
    print("support and formula checks")
    print("positive support count:", len(positive_events), positive_events)
    print("zero event count:", len(zero_events), zero_events)
    print("zero event nonzero derivative jets:", zero_bad_jets)
    print("low-order formula mismatches:", formula_mismatches)
    print("q mismatches against prompt:", q_mismatches)
    print("sum q:", fstr(q_sum))
    print("c = -sum q log q:", mp.nstr(c, 80))
    print()
    print("normalization jets")
    print("sum p:", fstr(sums["p"]))
    print("sum p_prime:", fstr(sums["p1"]))
    print("sum p_second:", fstr(sums["p2"]))
    print()
    print("chosen rational A,V diagnostics")
    print("A diagonal:", [[fstr(x) for x in row] for row in A])
    print("V:", [[fstr(x) for x in row] for row in V])
    print("[A,V] Frobenius^2:", fstr(comm_norm2))
    print("A Gershgorin lower/upper:", fstr(A_gersh[0]), fstr(A_gersh[1]))
    print("I-A Gershgorin lower/upper:", fstr(IA_gersh[0]), fstr(IA_gersh[1]))
    print("A +/- 2^-8 V Gershgorin lower/upper:")
    print("  A+hV:", fstr(Ap_gersh[0]), fstr(Ap_gersh[1]))
    print("  A-hV:", fstr(Am_gersh[0]), fstr(Am_gersh[1]))
    print("I-(A+hV):", fstr(IAp_gersh[0]), fstr(IAp_gersh[1]))
    print("I-(A-hV):", fstr(IAm_gersh[0]), fstr(IAm_gersh[1]))
    print()
    print("by-cardinality entropy curvature decomposition")
    print("size count_pos count_zero Fisher_cost log_accel curvature")
    for k in sorted(by_size):
        row = by_size[k]
        print(
            k,
            row["count_pos"],
            row["count_zero"],
            mp.nstr(row["fisher"], 50),
            mp.nstr(row["log_accel"], 50),
            mp.nstr(row["curvature"], 50),
        )
    print("total H_second:", mp.nstr(Hpp, 60))
    print()
    print("top determinant check")
    print("d:", fstr(d0))
    print("d_prime:", fstr(d1))
    print("d_second:", fstr(d2))
    print("F_top=(d_prime)^2/d:", mp.nstr(F_top, 50))
    print("c*d_second:", mp.nstr(c_d2, 50))
    print("(2c/3)*F_top:", mp.nstr(bound_rhs, 50))
    print("c*d_second <= (2c/3)*F_top:", c_d2 <= bound_rhs)
    print()
    print("central finite-difference calibration")
    print("h finite_difference minus_analytic")
    for label, fd, diff in fd_rows:
        print(label, mp.nstr(fd, 60), mp.nstr(diff, 30))


if __name__ == "__main__":
    main()
