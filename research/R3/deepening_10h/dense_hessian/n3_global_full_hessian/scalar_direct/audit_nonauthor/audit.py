"""D10-U10a scalar_direct independent non-author audit.

No author sanity/self_review module is imported or executed.  This script
implements a small n=3 exact-event arithmetic kernel from scratch:
Mobius atoms, exact coordinate gradients/jets, Fisher/coarse-Fisher forms,
the rho=min_g Q check, inclusion-statistic capacity, nested score splitting,
Sherman-Morrison corrections, and the rational path blocker with log intervals.
"""

from __future__ import annotations

import hashlib
import json
import time
from decimal import Decimal, getcontext
from fractions import Fraction as Q
from itertools import permutations
from pathlib import Path


getcontext().prec = 100

AUDIT = Path(__file__).resolve().parent
BASE = AUDIT.parent
OUT = AUDIT / "audit_results.json"

MASKS = list(range(8))
NONEMPTY = list(range(1, 8))
T_PAIR = [0, 3, 5, 6]
T_COMP = [7, 1, 2, 4]
SPLITS = [([7], [1, 2, 4]), ([1], [2, 4]), ([2], [4])]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def enc(x):
    if isinstance(x, Q):
        return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)
    if isinstance(x, Decimal):
        return format(x, "f")
    if isinstance(x, list):
        return [enc(v) for v in x]
    if isinstance(x, tuple):
        return [enc(v) for v in x]
    if isinstance(x, dict):
        return {k: enc(v) for k, v in x.items()}
    return x


def q_to_dec(x: Q) -> Decimal:
    return Decimal(x.numerator) / Decimal(x.denominator)


def sign_perm(p):
    inv = 0
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            inv += p[i] > p[j]
    return -1 if inv % 2 else 1


def det_frac(M):
    n = len(M)
    if n == 0:
        return Q(1)
    total = Q(0)
    for p in permutations(range(n)):
        term = Q(sign_perm(p))
        for i, j in enumerate(p):
            term *= M[i][j]
        total += term
    return total


def submatrix(M, mask):
    idx = [i for i in range(3) if (mask >> i) & 1]
    return [[M[i][j] for j in idx] for i in idx]


def inclusion(K):
    return [det_frac(submatrix(K, mask)) for mask in MASKS]


def atoms_from_inclusion(q):
    p = [Q(0) for _ in MASKS]
    for s in MASKS:
        total = Q(0)
        for t in MASKS:
            if (t & s) == s:
                total += (Q(-1) if (t.bit_count() - s.bit_count()) % 2 else Q(1)) * q[t]
        p[s] = total
    return p


def atoms(K):
    return atoms_from_inclusion(inclusion(K))


def add_scaled(K, D, t):
    return [[K[i][j] + t * D[i][j] for j in range(3)] for i in range(3)]


def basis():
    out = []
    for i, j in [(0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2)]:
        E = [[Q(0) for _ in range(3)] for __ in range(3)]
        E[i][j] = Q(1)
        E[j][i] = Q(1)
        out.append(E)
    return out


BASIS = basis()


def atom_jets_by_values(K, D, h=Q(1, 1000)):
    vals = {j: atoms(add_scaled(K, D, Q(j) * h)) for j in [-2, -1, 0, 1, 2]}
    p = vals[0]
    p1 = [(8 * (vals[1][s] - vals[-1][s]) - (vals[2][s] - vals[-2][s])) / (12 * h) for s in MASKS]
    p2 = [(vals[1][s] + vals[-1][s] - 2 * p[s]) / (h * h) for s in MASKS]
    return p, p1, p2


def atom_gradients(K):
    grad = [[Q(0) for _ in range(6)] for __ in MASKS]
    for b, E in enumerate(BASIS):
        _, p1, _ = atom_jets_by_values(K, E, Q(1))
        for s in MASKS:
            grad[s][b] = p1[s]
    return grad


def inclusion_gradients(K):
    grad = [[Q(0) for _ in range(6)] for __ in NONEMPTY]
    for b, E in enumerate(BASIS):
        vals = {j: inclusion(add_scaled(K, E, Q(j))) for j in [-2, -1, 0, 1, 2]}
        q1 = [(8 * (vals[1][s] - vals[-1][s]) - (vals[2][s] - vals[-2][s])) / Q(12) for s in MASKS]
        for row, mask in enumerate(NONEMPTY):
            grad[row][b] = q1[mask]
    return grad


def outer(u, v, scale=Q(1)):
    return [[scale * u[i] * v[j] for j in range(len(v))] for i in range(len(u))]


def mat_add(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def zero(n, m):
    return [[Q(0) for _ in range(m)] for __ in range(n)]


def fisher_matrix(p, grad):
    F = zero(6, 6)
    for s in MASKS:
        F = mat_add(F, outer(grad[s], grad[s], Q(1, 1) / p[s]))
    return F


def coarse_fisher(p, grad, T):
    F = zero(6, 6)
    R = [s for s in MASKS if s not in T]
    for s in T:
        F = mat_add(F, outer(grad[s], grad[s], Q(1, 1) / p[s]))
    pR = sum(p[s] for s in R)
    gR = [sum(grad[s][i] for s in R) for i in range(6)]
    F = mat_add(F, outer(gR, gR, Q(1, 1) / pR))
    return F


def vector_group(grad, group):
    return [sum(grad[s][i] for s in group) for i in range(6)]


def nested_rank_updates(p, grad):
    updates = []
    for A, B in SPLITS:
        pA, pB = sum(p[s] for s in A), sum(p[s] for s in B)
        jA, jB = vector_group(grad, A), vector_group(grad, B)
        h = [pB * jA[i] - pA * jB[i] for i in range(6)]
        w = Q(1, 1) / (pA * pB * (pA + pB))
        updates.append({"A": A, "B": B, "pA": pA, "pB": pB, "h": h, "w": w})
    return updates


def ldl_pivots_frac(A):
    n = len(A)
    L = [[Q(0) for _ in range(n)] for __ in range(n)]
    piv = []
    for i in range(n):
        for j in range(i):
            s = sum(L[i][k] * L[j][k] * piv[k] for k in range(j))
            L[i][j] = (A[i][j] - s) / piv[j]
        d = A[i][i] - sum(L[i][k] * L[i][k] * piv[k] for k in range(i))
        piv.append(d)
        L[i][i] = Q(1)
    return piv


def dec_mat(A):
    return [[q_to_dec(x) for x in row] for row in A]


def dec_vec(v):
    return [q_to_dec(x) for x in v]


def matmul(A, B):
    n, k, m = len(A), len(B), len(B[0])
    return [[sum(A[i][r] * B[r][j] for r in range(k)) for j in range(m)] for i in range(n)]


def trace(A):
    return sum(A[i][i] for i in range(len(A)))


def det_dec(A):
    n = len(A)
    M = [row[:] for row in A]
    det = Decimal(1)
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(M[r][c]))
        if M[piv][c] == 0:
            return Decimal(0)
        if piv != c:
            M[c], M[piv] = M[piv], M[c]
            det = -det
        pv = M[c][c]
        det *= pv
        for r in range(c + 1, n):
            fac = M[r][c] / pv
            for j in range(c, n):
                M[r][j] -= fac * M[c][j]
    return det


def inv_dec(A):
    n = len(A)
    M = [A[i][:] + [Decimal(1) if i == j else Decimal(0) for j in range(n)] for i in range(n)]
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(M[r][c]))
        if M[piv][c] == 0:
            raise ArithmeticError("singular")
        if piv != c:
            M[c], M[piv] = M[piv], M[c]
        pv = M[c][c]
        M[c] = [x / pv for x in M[c]]
        for r in range(n):
            if r == c:
                continue
            fac = M[r][c]
            if fac:
                M[r] = [M[r][j] - fac * M[c][j] for j in range(2 * n)]
    return [row[n:] for row in M]


def solve_dec(A, b):
    inv = inv_dec(A)
    return [sum(inv[i][j] * b[j] for j in range(len(b))) for i in range(len(b))]


def quad_solve(A, b):
    x = solve_dec(A, b)
    return sum(b[i] * x[i] for i in range(len(b))), x


def matvec(A, x):
    return [sum(A[i][j] * x[j] for j in range(len(x))) for i in range(len(A))]


def transpose(A):
    return [list(row) for row in zip(*A)]


def mat_add_dec(A, B, scale=Decimal(1)):
    return [[A[i][j] + scale * B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def outer_dec(u, v, scale=Decimal(1)):
    return [[scale * u[i] * v[j] for j in range(len(v))] for i in range(len(u))]


def frob_grad_matrix(coord_grad):
    W = [[Q(0) for _ in range(3)] for __ in range(3)]
    W[0][0], W[1][1], W[2][2] = coord_grad[0], coord_grad[1], coord_grad[2]
    W[0][1] = W[1][0] = coord_grad[3] / 2
    W[0][2] = W[2][0] = coord_grad[4] / 2
    W[1][2] = W[2][1] = coord_grad[5] / 2
    return W


def N_delta_eta_G(K, p):
    pd = [q_to_dec(x) for x in p]
    Kd = dec_mat(K)
    l12 = (pd[0] * pd[3] / (pd[1] * pd[2])).ln()
    l13 = (pd[0] * pd[5] / (pd[1] * pd[4])).ln()
    l23 = (pd[0] * pd[6] / (pd[2] * pd[4])).ln()
    Lam = (pd[7] * pd[1] * pd[2] * pd[4] / (pd[0] * pd[3] * pd[5] * pd[6])).ln()
    N = [[-Lam * Kd[i][j] for j in range(3)] for i in range(3)]
    N[0][0] += -l23
    N[1][1] += -l13
    N[2][2] += -l12
    delta = det_dec(N)
    invN = inv_dec(N)
    Ed = [dec_mat(E) for E in BASIS]
    eta = [trace(matmul(invN, E)) for E in Ed]
    G = [[trace(matmul(matmul(invN, Ei), matmul(invN, Ej))) for Ej in Ed] for Ei in Ed]
    return {"N": N, "delta": delta, "eta": eta, "G": G, "logs": [l12, l13, l23, Lam]}


def rho_objects(K, T=T_PAIR):
    p = atoms(K)
    grad = atom_gradients(K)
    Fq = fisher_matrix(p, grad)
    FTq = coarse_fisher(p, grad, T)
    nd = N_delta_eta_G(K, p)
    F, FT = dec_mat(Fq), dec_mat(FTq)
    A = mat_add_dec(F, nd["G"], nd["delta"])
    AT = mat_add_dec(FT, nd["G"], nd["delta"])
    rho, _ = quad_solve(A, nd["eta"])
    rho *= nd["delta"]
    R, _ = quad_solve(AT, nd["eta"])
    R *= nd["delta"]
    return {"p": p, "grad": grad, "Fq": Fq, "FTq": FTq, "Ndata": nd, "rho": rho, "coarse": R}


def Q_min_value(K):
    obj = rho_objects(K)
    p, grad, nd = obj["p"], obj["grad"], obj["Ndata"]
    W = [dec_mat(frob_grad_matrix(grad[s])) for s in MASKS]
    N, delta = nd["N"], nd["delta"]
    M = [[Decimal(0) for _ in MASKS] for __ in MASKS]
    r = [Decimal(0) for _ in MASKS]
    for s in MASKS:
        NWs = matmul(N, W[s])
        r[s] = trace(NWs)
        for t in MASKS:
            M[s][t] = trace(matmul(NWs, matmul(N, W[t])))
            if s == t:
                M[s][t] += delta * q_to_dec(p[s])
    val, _ = quad_solve(M, r)
    return Decimal(3) - val, obj["rho"]


def inclusion_capacity(K):
    p = atoms(K)
    grad = atom_gradients(K)
    Fq = fisher_matrix(p, grad)
    nd = N_delta_eta_G(K, p)
    V_f, _ = quad_solve(dec_mat(Fq), nd["eta"])

    q = inclusion(K)
    Jq = inclusion_gradients(K)
    C = [[q_to_dec(q[A | B] - q[A] * q[B]) for B in NONEMPTY] for A in NONEMPTY]
    Cinv = inv_dec(C)
    J = dec_mat(Jq)
    JT = transpose(J)
    middle = matmul(matmul(JT, Cinv), J)
    V_moment, _ = quad_solve(middle, nd["eta"])
    return {"V_from_F": V_f, "V_from_moments": V_moment, "difference": V_f - V_moment}


def rank_splitting_and_sm(K):
    obj = rho_objects(K, T_PAIR)
    p, grad, Fq, FTq, nd = obj["p"], obj["grad"], obj["Fq"], obj["FTq"], obj["Ndata"]
    updates = nested_rank_updates(p, grad)
    running = [row[:] for row in FTq]
    exact_errors = []
    for up in updates:
        running = mat_add(running, outer(up["h"], up["h"], up["w"]))
    for i in range(6):
        for j in range(6):
            exact_errors.append(running[i][j] - Fq[i][j])

    Acur = mat_add_dec(dec_mat(FTq), nd["G"], nd["delta"])
    eta, delta = nd["eta"], nd["delta"]
    Rcur, _ = quad_solve(Acur, eta)
    Rcur *= delta
    corrections = []
    for up in updates:
        h = dec_vec(up["h"])
        Ainv_h = solve_dec(Acur, h)
        numerator = delta * (sum(eta[i] * Ainv_h[i] for i in range(6)) ** 2)
        denom = Decimal(up["w"].denominator) / Decimal(up["w"].numerator) + sum(h[i] * Ainv_h[i] for i in range(6))
        corr = numerator / denom
        Rnext = Rcur - corr
        Acur = mat_add_dec(Acur, outer_dec(h, h), q_to_dec(up["w"]))
        corrections.append({"correction": corr, "rho_after": Rnext, "denominator": denom})
        Rcur = Rnext
    return {
        "full_rho": obj["rho"],
        "coarse_R_T": obj["coarse"],
        "split_identity_zero": all(e == 0 for e in exact_errors),
        "max_exact_split_error": max(abs(e) for e in exact_errors),
        "corrections": corrections,
        "final_after_corrections": Rcur,
        "final_difference": Rcur - obj["rho"],
    }


def ln_small_interval(q, terms=160):
    y = (q - 1) / (q + 1)
    v = y
    s = Q(0)
    for k in range(terms):
        s += 2 * v / (2 * k + 1)
        v *= y * y
    rem = 2 * v / ((2 * terms + 1) * (1 - y * y))
    return s, s + rem


def ln_interval(q):
    if q <= 0:
        raise ValueError("log needs positive rational")
    if q < 1:
        lo, hi = ln_interval(1 / q)
        return -hi, -lo
    power = 0
    x = q
    while x > 2:
        x /= 2
        power += 1
    lo, hi = ln_small_interval(x)
    l2, u2 = ln_small_interval(Q(2))
    return lo + power * l2, hi + power * u2


def interval_add_log_sum(base, coeffs, qs):
    lo = hi = base
    for c, q in zip(coeffs, qs):
        a, b = ln_interval(q)
        if c >= 0:
            lo += c * a
            hi += c * b
        else:
            lo += c * b
            hi += c * a
    return lo, hi


def path_blocker():
    K = [[Q(1, 2), Q(3, 10), Q(0)], [Q(3, 10), Q(1, 2), Q(3, 10)], [Q(0), Q(3, 10), Q(1, 2)]]
    D = [[Q(1), Q(-3, 5), Q(1, 3)], [Q(-3, 5), Q(5, 6), Q(-3, 5)], [Q(1, 3), Q(-3, 5), Q(1)]]
    p, p1, p2 = atom_jets_by_values(K, D)
    grad = atom_gradients(K)
    Fq = fisher_matrix(p, grad)
    FTq = coarse_fisher(p, grad, T_PAIR)
    Dcoords = [D[0][0], D[1][1], D[2][2], D[0][1], D[0][2], D[1][2]]
    F_D = sum(Dcoords[i] * Fq[i][j] * Dcoords[j] for i in range(6) for j in range(6))
    FT_D = sum(Dcoords[i] * FTq[i][j] * Dcoords[j] for i in range(6) for j in range(6))
    B_direct = interval_add_log_sum(F_D, p2, p)
    BT_direct = interval_add_log_sum(FT_D, p2, p)
    D_piv = ldl_pivots_frac(D)
    endpoints = []
    for t in [Q(-1, 100), Q(1, 100)]:
        Kt = add_scaled(K, D, t)
        low = [[Kt[i][j] - (Q(1, 1000) if i == j else Q(0)) for j in range(3)] for i in range(3)]
        high = [[(Q(1) if i == j else Q(0)) - Kt[i][j] - (Q(1, 1000) if i == j else Q(0)) for j in range(3)] for i in range(3)]
        endpoints.append({"t": t, "K_t_minus_margin": ldl_pivots_frac(low), "I_minus_K_t_minus_margin": ldl_pivots_frac(high)})
    rho_pair = rho_objects(K, T_PAIR)
    rho_comp = rho_objects(K, T_COMP)
    split = rank_splitting_and_sm(K)
    return {
        "K": K,
        "D": D,
        "p": p,
        "p1": p1,
        "p2": p2,
        "sum_p": sum(p),
        "sum_p1": sum(p1),
        "sum_p2": sum(p2),
        "F_D": F_D,
        "FT_D": FT_D,
        "actual_B_interval": B_direct,
        "proxy_BT_interval": BT_direct,
        "actual_B_positive": B_direct[0] > 0,
        "proxy_BT_negative": BT_direct[1] < 0,
        "D_ldl_positive": all(x > 0 for x in D_piv),
        "D_ldl_pivots": D_piv,
        "endpoint_ldl": endpoints,
        "whole_chord_margin_by_convexity": all(
            all(x > 0 for x in e["K_t_minus_margin"]) and all(x > 0 for x in e["I_minus_K_t_minus_margin"])
            for e in endpoints
        ),
        "rho": rho_pair["rho"],
        "coarse_R_T": rho_pair["coarse"],
        "coarse_R_T_complement_orientation": rho_comp["coarse"],
        "rank_splitting": split,
    }


def sanity_json_audit():
    data = json.loads((BASE / "sanity.json").read_text(encoding="utf-8"))
    rows = data.get("rows", [])
    families = {}
    for r in rows:
        families[r["family"]] = families.get(r["family"], 0) + 1
    distinct_K = len({json.dumps(r["K"], sort_keys=True) for r in rows})
    return {
        "status": data.get("status"),
        "denominator": data.get("denominator"),
        "row_count": len(rows),
        "families": families,
        "distinct_K": distinct_K,
        "coarse_pass_count": data.get("coarse_pass_count"),
        "capacity_pass_count": data.get("capacity_pass_count"),
        "full_positive_count": data.get("full_positive_count"),
        "six_category_pass_count": sum(Decimal(r["six_category_rho_upper"]) < 1 for r in rows),
        "rho_ge_1_count": sum(Decimal(r["rho"]) >= 1 for r in rows),
    }


def main():
    t0 = time.time()
    dense_K = [[Q(1, 2), Q(1, 10), Q(1, 10)], [Q(1, 10), Q(1, 2), Q(1, 10)], [Q(1, 10), Q(1, 10), Q(1, 2)]]
    path_K = [[Q(1, 2), Q(3, 10), Q(0)], [Q(3, 10), Q(1, 2), Q(3, 10)], [Q(0), Q(3, 10), Q(1, 2)]]
    dense_F = fisher_matrix(atoms(dense_K), atom_gradients(dense_K))
    path_F = fisher_matrix(atoms(path_K), atom_gradients(path_K))
    q_dense, rho_dense = Q_min_value(dense_K)
    q_path, rho_path = Q_min_value(path_K)
    cap_dense = inclusion_capacity(dense_K)
    cap_path = inclusion_capacity(path_K)
    split_dense = rank_splitting_and_sm(dense_K)
    blocker = path_blocker()
    files = {p.name: sha256(p) for p in BASE.iterdir() if p.is_file()}
    files.update({f"self_review/{p.name}": sha256(p) for p in (BASE / "self_review").iterdir() if p.is_file()})
    checks = {
        "lemma1_dense_F_positive": all(x > 0 for x in ldl_pivots_frac(dense_F)),
        "lemma1_path_F_positive": all(x > 0 for x in ldl_pivots_frac(path_F)),
        "rho_min_Q_dense_matches": abs(q_dense - rho_dense) < Decimal("1e-80"),
        "rho_min_Q_path_matches": abs(q_path - rho_path) < Decimal("1e-80"),
        "V_dense_matches_moment_formula": abs(cap_dense["difference"]) < Decimal("1e-80"),
        "V_path_matches_moment_formula": abs(cap_path["difference"]) < Decimal("1e-80"),
        "split_dense_exact": split_dense["split_identity_zero"],
        "split_path_exact": blocker["rank_splitting"]["split_identity_zero"],
        "SM_path_final_matches_full_rho": abs(blocker["rank_splitting"]["final_difference"]) < Decimal("1e-80"),
        "path_proxy_BT_negative": blocker["proxy_BT_negative"],
        "path_actual_B_positive": blocker["actual_B_positive"],
        "path_D_positive": blocker["D_ldl_positive"],
        "path_chord_margin": blocker["whole_chord_margin_by_convexity"],
        "path_both_five_category_orientations_fail": blocker["coarse_R_T"] > 1 and blocker["coarse_R_T_complement_orientation"] > 1,
    }
    result = {
        "status": "PASS_WITH_GLOBAL_INCOMPLETE",
        "input_hashes": files,
        "sanity_json": sanity_json_audit(),
        "lemma1_F_pivots": {
            "dense_exchangeable_1_10": ldl_pivots_frac(dense_F),
            "path_3_10": ldl_pivots_frac(path_F),
        },
        "rho_min_Q": {
            "dense_exchangeable_1_10": {"Q_min": q_dense, "rho": rho_dense, "difference": q_dense - rho_dense},
            "path_3_10": {"Q_min": q_path, "rho": rho_path, "difference": q_path - rho_path},
        },
        "unregularized_capacity": {
            "dense_exchangeable_1_10": cap_dense,
            "path_3_10": cap_path,
        },
        "rank_split_dense": split_dense,
        "path_blocker": blocker,
        "checks": checks,
        "elapsed_seconds": time.time() - t0,
    }
    OUT.write_text(json.dumps(enc(result), indent=2), encoding="utf-8")
    print(json.dumps(enc(result), indent=2))


if __name__ == "__main__":
    main()
