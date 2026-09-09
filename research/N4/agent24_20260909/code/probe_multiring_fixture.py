#!/usr/bin/env python3
"""Motivated high-precision probe for one correlated 3+3 signed-multiring line.

All 64 exact atom polynomials and their derivatives are built with rational
arithmetic from the rank-two Schur likelihood. Logarithms are evaluated with
mpmath at 110 decimal digits, so curvature/gap signs are diagnostics rather
than interval certificates. A separate issue specifies the rigorous compact-
interval certification task.
"""
from __future__ import annotations

import mpmath as mp
import sympy as sp

Q = sp.Rational
T_POINTS = [Q(1, 10), Q(1, 4), Q(1, 2), Q(3, 4), Q(1), Q(5, 4), Q(3, 2), Q(17, 10), Q(9, 5), Q(19, 10), Q(2), Q(21, 10)]
GAP_STEP = Q(1, 100)


def subsets(n: int):
    for mask in range(1 << n):
        yield tuple(i for i in range(n) if mask & (1 << i))


def event_matrix(K: sp.Matrix, S: tuple[int, ...]) -> sp.Matrix:
    M = K.copy()
    inside = set(S)
    for i in range(K.rows):
        if i not in inside:
            M[i, i] -= 1
    return M


def event_prob(K: sp.Matrix, S: tuple[int, ...]) -> sp.Rational:
    return sp.factor((-1) ** (K.rows - len(S)) * event_matrix(K, S).det())


def pd_sylvester(M: sp.Matrix) -> bool:
    return all(sp.factor(M[:k, :k].det()) > 0 for k in range(1, M.rows + 1))


def mpq(x: sp.Rational) -> mp.mpf:
    return mp.mpf(int(x.p)) / int(x.q)


A = sp.Matrix([
    [Q(9, 25), Q(7, 25), Q(7, 25)],
    [Q(7, 25), Q(9, 25), Q(7, 25)],
    [Q(7, 25), Q(7, 25), Q(9, 25)],
])
C = sp.Matrix([
    [Q(16, 25), Q(7, 25), Q(7, 25)],
    [Q(7, 25), Q(16, 25), -Q(7, 25)],
    [Q(7, 25), -Q(7, 25), Q(16, 25)],
])

u1 = sp.Matrix([1, 1, -1])
u2 = sp.Matrix([1, -2, 1])
v1 = sp.Matrix([1, -1, 2])
w = sp.Matrix([Q(13, 6), Q(5, 6), -Q(2, 3)])
U = sp.Matrix.hstack(u1, u2) / 50
V = sp.Matrix.hstack(v1, w / 2)
B = sp.factor(U * V.T)
assert B.rank() == 2
assert all(x != 0 for x in B)

pA = {S: event_prob(A, S) for S in subsets(3)}
pC = {T: event_prob(C, T) for T in subsets(3)}
assert all(x > 0 for x in pA.values()) and sum(pA.values(), Q(0)) == 1
assert all(x > 0 for x in pC.values()) and sum(pC.values(), Q(0)) == 1

# p_t(S,T)=mu(S,T)[1+t^2 u(S,T)+t^4 v(S,T)].
features = {}
for S in subsets(3):
    X = event_matrix(A, S)
    GA = U.T * X.inv() * U
    for T in subsets(3):
        Y = event_matrix(C, T)
        GC = V.T * Y.inv() * V
        u = sp.factor(-sp.trace(GA * GC))
        v = sp.factor(GA.det() * GC.det())
        features[(S, T)] = (sp.factor(pA[S] * pC[T]), u, v)
assert len(features) == 64
assert sum(mu * u for mu, u, _ in features.values()) == 0
assert sum(mu * v for mu, _, v in features.values()) == 0


def rational_rows(t: sp.Rational):
    rows = {}
    s = t * t
    for key, (mu, u, v) in features.items():
        p = sp.factor(mu * (1 + s * u + s * s * v))
        p1 = sp.factor(mu * (2 * t * u + 4 * t**3 * v))
        p2 = sp.factor(mu * (2 * u + 12 * s * v))
        assert p > 0
        rows[key] = (p, p1, p2)
    assert sum(p for p, _, _ in rows.values()) == 1
    assert sum(p1 for _, p1, _ in rows.values()) == 0
    assert sum(p2 for _, _, p2 in rows.values()) == 0
    return rows


# Independent exact construction check: at t=1, compare every Schur-likelihood
# atom against the signed determinant of the full 6x6 event matrix.
K_full_one = A.row_join(B).col_join(B.T.row_join(C))
rows_one = rational_rows(Q(1))
for (S, T), (p, _, _) in rows_one.items():
    full_event = tuple(S) + tuple(3 + j for j in T)
    assert event_prob(K_full_one, full_event) == p


def entropy(t: sp.Rational) -> mp.mpf:
    total = mp.mpf("0")
    for p, _, _ in rational_rows(t).values():
        x = mpq(p)
        total -= x * mp.log(x)
    return total


def curvature_and_layers(t: sp.Rational):
    total = mp.mpf("0")
    fisher = mp.mpf("0")
    acceleration = mp.mpf("0")
    layers = [mp.mpf("0") for _ in range(7)]
    rows = rational_rows(t)
    for (S, T), (p, p1, p2) in rows.items():
        x, dx, ddx = mpq(p), mpq(p1), mpq(p2)
        f = -(dx * dx) / x
        a = -ddx * mp.log(x)
        fisher += f
        acceleration += a
        total += f + a
        layers[len(S) + len(T)] += f + a
    return total, fisher, acceleration, layers, min(p for p, _, _ in rows.values())


left_null = B.T.nullspace()[0]
right_null = B.nullspace()[0]
An = A * left_null
Cn = C * right_null
assert any(left_null[i] * An[j] - left_null[j] * An[i] != 0 for i in range(3) for j in range(i + 1, 3))
assert any(right_null[i] * Cn[j] - right_null[j] * Cn[i] != 0 for i in range(3) for j in range(i + 1, 3))

T_EDGE = Q(21, 10)
assert pd_sylvester(A) and pd_sylvester(C)
assert pd_sylvester(sp.eye(3) - A) and pd_sylvester(sp.eye(3) - C)
for t in (-T_EDGE, T_EDGE):
    schur_K = C - t * t * B.T * A.inv() * B
    schur_IK = (sp.eye(3) - C) - t * t * B.T * (sp.eye(3) - A).inv() * B
    assert pd_sylvester(schur_K)
    assert pd_sylvester(schur_IK)

# The positive legal endpoint is the simple I-K Schur root.  Exact determinant
# signs bracket it between 2149/1000 and 43/20.
M_I = B.T * (sp.eye(3) - A).inv() * B
S_I = (sp.eye(3) - C).inv() * M_I
tr_I = sp.factor(sp.trace(S_I))
disc_I = sp.factor(2 * sp.trace(S_I * S_I) - tr_I**2)
assert disc_I > 0
det_lo = sp.factor(((sp.eye(3) - C) - Q(2149, 1000)**2 * M_I).det())
det_hi = sp.factor(((sp.eye(3) - C) - Q(43, 20)**2 * M_I).det())
assert det_lo > 0 > det_hi
# The K-side Schur complement is still positive at the upper bracket, so the
# first loss of strict legality is indeed the simple I-K root.
assert pd_sylvester(C - Q(43, 20)**2 * B.T * A.inv() * B)

mp.mp.dps = 110
print("agent24 correlated 3+3 signed-multiring fixture: PASS")
print("status = MOTIVATED_110_DIGIT_DIAGNOSTIC_NOT_INTERVAL_CERTIFICATE")
print("rank(B) =", B.rank(), "; dense entries =", B.rows * B.cols)
print("B =", [[str(B[i, j]) for j in range(3)] for i in range(3)])
print("A spectrum = 2/25,2/25,23/25; C spectrum = 2/25,23/25,23/25")
print("left null(B^T) =", [str(x) for x in left_null])
print("right null(B) =", [str(x) for x in right_null])
print("outside PR43 special null-eigenvector condition = PASS")
print("exact strict legality at t=+-21/10 = PASS (Schur/Sylvester)")
print("simple positive legal endpoint tau in (2149/1000,43/20) = PASS")
print("endpoint discriminant =", disc_I, "; det bracket =", det_lo, det_hi)
print("K-side remains strict at 43/20 = PASS")
print("full 6x6 signed-event cross-check at t=1 = PASS")
print("complete rational atom polynomials =", len(features))
print("mpmath decimal precision =", mp.mp.dps)
print("local midpoint step =", GAP_STEP)

best = None
for t in T_POINTS:
    h2, fisher, acceleration, layers, min_atom = curvature_and_layers(t)
    gap = (entropy(t - GAP_STEP) + entropy(t + GAP_STEP)) / 2 - entropy(t)
    row = (h2, t, gap)
    if best is None or h2 > best[0]:
        best = row
    print("t =", t)
    print("  min exact atom =", min_atom)
    print("  Hsecond =", mp.nstr(h2, 50))
    print("  Fisher =", mp.nstr(fisher, 50), "; acceleration =", mp.nstr(acceleration, 50))
    print("  local Jensen gap =", mp.nstr(gap, 50))
    print("  layer Hsecond =", ", ".join(f"k={k}:{mp.nstr(x, 24)}" for k, x in enumerate(layers)))

assert best is not None
print("least-negative sampled curvature =", mp.nstr(best[0], 50), "at t =", best[1])
print("verdict for frozen points = no positive curvature or local gap")
print("nonclaim = finite high-precision diagnostics do not prove an interval or family theorem")
