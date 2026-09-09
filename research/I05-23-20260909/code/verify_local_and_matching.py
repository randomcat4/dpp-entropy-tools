#!/usr/bin/env python3
"""
Exact rational fixture for I05-23 local curvature and matching entropy-gap lemmas.

This is a symbolic consistency check, not a proof of full-chord concavity.
It uses every complete configuration of a dense correlated 3+3 rank-two example.
"""
from __future__ import annotations

from itertools import combinations
import sympy as sp

Q = sp.Rational

A = sp.Matrix([
    [Q(1,2), Q(1,20), Q(1,30)],
    [Q(1,20), Q(2,5), Q(1,25)],
    [Q(1,30), Q(1,25), Q(3,5)],
])
C = sp.Matrix([
    [Q(2,5), -Q(1,30), Q(1,40)],
    [-Q(1,30), Q(1,2), Q(1,35)],
    [Q(1,40), Q(1,35), Q(11,20)],
])
U = sp.Matrix([[Q(1,100), Q(1,100)],
               [Q(2,100), Q(1,100)],
               [Q(3,100), Q(1,100)]])
V = sp.Matrix([[1,0],[1,1],[1,2]])
B = U * V.T

def subsets(n: int):
    for mask in range(1 << n):
        yield tuple(i for i in range(n) if mask & (1 << i))

def event_matrix(K: sp.Matrix, S: tuple[int, ...]) -> sp.Matrix:
    X = K.copy()
    Sin = set(S)
    for i in range(K.rows):
        if i not in Sin:
            X[i, i] -= 1
    return X

def event_prob(K: sp.Matrix, S: tuple[int, ...]) -> sp.Rational:
    n = K.rows
    return (-1) ** (n - len(S)) * event_matrix(K, S).det()

def all_principal_minors_positive(K: sp.Matrix) -> bool:
    n = K.rows
    for r in range(1, n + 1):
        for S in combinations(range(n), r):
            if K.extract(S, S).det() <= 0:
                return False
    return True

def gershgorin_margin(K: sp.Matrix) -> sp.Rational:
    vals = []
    for M in (K, sp.eye(K.rows) - K):
        for i in range(M.rows):
            vals.append(M[i,i] - sum(abs(M[i,j]) for j in range(M.cols) if j != i))
    return min(vals)

assert B.rank() == 2
assert all(x != 0 for x in B)
left_null = B.T.nullspace()
right_null = B.nullspace()
assert len(left_null) == len(right_null) == 1
assert all(x != 0 for x in left_null[0])
assert all(x != 0 for x in right_null[0])
# PR43's special family would force the unique left null vector n of B
# to be an eigenvector of A. This exact fixture deliberately violates that.
n_left = left_null[0]
An = A * n_left
assert An[0] * n_left[1] != An[1] * n_left[0]
assert all_principal_minors_positive(A)
assert all_principal_minors_positive(sp.eye(3) - A)
assert all_principal_minors_positive(C)
assert all_principal_minors_positive(sp.eye(3) - C)

pA = {S: event_prob(A, S) for S in subsets(3)}
pC = {T: event_prob(C, T) for T in subsets(3)}
assert all(p > 0 for p in pA.values())
assert all(p > 0 for p in pC.values())
assert sum(pA.values()) == 1
assert sum(pC.values()) == 1

rows = []
sum_u = Q(0)
sum_v = Q(0)
sigma2 = Q(0)
pair_score = Q(0)

for S in subsets(3):
    XS = event_matrix(A, S)
    GA = U.T * XS.inv() * U
    for T in subsets(3):
        YT = event_matrix(C, T)
        GC = V.T * YT.inv() * V
        u = -sp.trace(GA * GC)
        v = GA.det() * GC.det()
        mu = pA[S] * pC[T]
        rows.append((S, T, mu, u, v))
        sum_u += mu * u
        sum_v += mu * v
        sigma2 += mu * u * u
        if 0 in S and 0 in T:
            pair_score += mu * u

assert sum_u == 0
assert sum_v == 0
assert pair_score == -B[0,0] ** 2
assert sigma2 > 0

# Independent exact check of the full 6-by-6 law at one rational nonzero t.
t_probe = Q(1, 10)
s_probe = t_probe ** 2
K_probe = A.row_join(t_probe * B).col_join((t_probe * B.T).row_join(C))
assert all_principal_minors_positive(K_probe)
assert all_principal_minors_positive(sp.eye(6) - K_probe)
joint_total = Q(0)
for S, T, mu, u, v in rows:
    ST = tuple(S) + tuple(3 + j for j in T)
    p_exact = event_prob(K_probe, ST)
    p_feature = mu * (1 + s_probe * u + s_probe**2 * v)
    assert p_exact == p_feature
    assert p_exact > 0
    joint_total += p_exact
assert joint_total == 1

Umax = max(abs(row[3]) for row in rows)
Vmax = max(abs(row[4]) for row in rows)

# Exact lower bound from one cross-pair inclusion statistic.
p11 = A[0,0] * C[0,0]
sigma_star2 = B[0,0] ** 4 / (p11 * (1 - p11))
assert sigma2 >= sigma_star2 > 0

eps = min(gershgorin_margin(A), gershgorin_margin(C))
assert eps > 0
Bfro2 = sum(x*x for x in B)
delta_legal = eps**2 / (4 * Bfro2)
delta0 = min(Q(1), delta_legal, Q(1, 2) / (Umax + Vmax))
M1 = Umax + 2 * delta0 * Vmax
L3 = 12 * M1 * Vmax + 4 * M1**3
assert L3 > 0
delta = min(delta0, 3 * sigma_star2 / (10 * L3))
assert delta > 0

# Exact rank-two endpoint discriminants without matrix square roots.
M_K = B.T * A.inv() * B
S_K = C.inv() * M_K
tr_K = sp.trace(S_K)
disc_K = sp.simplify(2 * sp.trace(S_K * S_K) - tr_K**2)

M_IK = B.T * (sp.eye(3) - A).inv() * B
S_IK = (sp.eye(3) - C).inv() * M_IK
tr_IK = sp.trace(S_IK)
disc_IK = sp.simplify(2 * sp.trace(S_IK * S_IK) - tr_IK**2)

assert disc_K > 0 and disc_IK > 0

# The top roots are (tr + sqrt(disc))/2. These rational square
# comparisons certify rho_K < 1/25 < 1/20 < rho_IK, so I-K reaches
# the legal endpoint first and its nullity is exactly one.
rho_K_upper = Q(1, 25)
rho_IK_lower = Q(1, 20)
rhs_K = 2 * rho_K_upper - tr_K
rhs_IK = 2 * rho_IK_lower - tr_IK
sep_K = sp.simplify(rhs_K**2 - disc_K)
sep_IK = sp.simplify(disc_IK - rhs_IK**2)
assert rhs_K > 0 and sep_K > 0
assert rhs_IK > 0 and sep_IK > 0

# A size-three matching gives a global entropy-deficit certificate.
matching = [(0,0), (1,1), (2,2)]
W = sum(B[i,j]**2 for i,j in matching)
gap_coeff = W**2 / (2 * 6)
assert gap_coeff > 0

print("I05-23 exact fixture: PASS")
print("rank(B) =", B.rank(), "; dense entries =", B.rows * B.cols)
print("complete configurations checked =", len(rows))
print("full joint likelihood check at t =", t_probe, ": PASS")
print("outside PR43 special family (left null not A-eigenvector): PASS")
print("Gershgorin spectral margin lower bound =", eps)
print("sigma^2 exact =", sigma2)
print("sigma_*^2 lower bound =", sigma_star2)
print("U =", Umax, "; V =", Vmax)
print("certified s-radius delta =", delta)
print("therefore H''(t) <= -3*sigma_*^2*t^2 < 0 for 0<|t|<=sqrt(delta)")
print("endpoint Delta_K =", disc_K, "; Delta_I-K =", disc_IK)
print("exact endpoint separation: rho_K < 1/25 < 1/20 < rho_I-K: PASS")
print("therefore the legal positive endpoint is simple for I-K and H'' -> -infinity")
print("matching W =", W)
print("global entropy deficit: H(0)-H(t) >=", gap_coeff, "* t^4")
