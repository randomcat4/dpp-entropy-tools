#!/usr/bin/env python3
from __future__ import annotations

from itertools import combinations
import sys
import sympy as sp

sys.set_int_max_str_digits(100000)
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

def subsets(n):
    for mask in range(1 << n):
        yield tuple(i for i in range(n) if mask & (1 << i))

def event_matrix(K, S):
    X = K.copy()
    Sin = set(S)
    for i in range(K.rows):
        if i not in Sin:
            X[i,i] -= 1
    return X

def event_prob(K, S):
    return (-1) ** (K.rows - len(S)) * event_matrix(K, S).det()

pA = {S: event_prob(A, S) for S in subsets(3)}
pC = {T: event_prob(C, T) for T in subsets(3)}
assert all(v > 0 for v in pA.values())
assert all(v > 0 for v in pC.values())
assert sum(pA.values()) == 1 and sum(pC.values()) == 1

rows = []
for S in subsets(3):
    GA = U.T * event_matrix(A, S).inv() * U
    for T in subsets(3):
        GC = V.T * event_matrix(C, T).inv() * V
        a = sp.trace(GA * GC)
        b = GA.det() * GC.det()
        mu = pA[S] * pC[T]
        rows.append((S,T,mu,a,b))

assert sum(mu*a for _,_,mu,a,b in rows) == 0
assert sum(mu*b for _,_,mu,a,b in rows) == 0

Amax = max(abs(a) for _,_,_,a,b in rows)
Bmax = max(abs(b) for _,_,_,a,b in rows)
Ea2 = sp.factor(sum(mu*a*a for _,_,mu,a,b in rows))
Eab = sp.factor(sum(mu*a*b for _,_,mu,a,b in rows))
Eb2 = sp.factor(sum(mu*b*b for _,_,mu,a,b in rows))

# Exact extrema of q_s=1-sa+s^2 b on a rational s interval.
def q_range(L, R):
    qlo = None
    qhi = None
    for _,_,_,a,b in rows:
        cand = [L, R]
        if b != 0:
            sv = sp.cancel(a/(2*b))
            if L <= sv <= R:
                cand.append(sv)
        vals = [sp.cancel(1 - x*a + x*x*b) for x in cand]
        lo = min(vals)
        hi = max(vals)
        qlo = lo if qlo is None or lo < qlo else qlo
        qhi = hi if qhi is None or hi > qhi else qhi
    return sp.factor(qlo), sp.factor(qhi)

# A rational interval certificate. It deliberately allows W<0.
def certify_interval(L, R):
    qminus, qplus = q_range(L, R)
    assert qminus > 0
    umax = max(1-qminus, qplus-1)
    # For 0<q<=1, -log q <= (1-q)/q; for q>=1, log q <= q-1.
    log_bound = max((1-qminus)/qminus, qplus-1)
    Psi = sp.factor(8*umax/qminus + 10*log_bound)

    # E[u_s^2]=s^2(Ea2-2sEab+s^2Eb2).
    # Eab>0 here; discard +s^2 Eb2 and use L<=s<=R.
    assert Eab > 0 and Ea2 - 2*R*Eab > 0
    M2lower = sp.factor(L**2 * (Ea2 - 2*R*Eab))

    # Accepted normal form plus Cauchy:
    # t^2 I'' >= P+A-(1/2)sqrt(A Rpsi)
    # >= 4 M2/qplus - R^2 Psi sqrt(Eb2*qplus/qminus).
    left = sp.factor(4*M2lower/qplus)
    right_sq = sp.factor(R**4 * Psi**2 * Eb2 * qplus/qminus)
    margin_sq = sp.factor(left**2 - right_sq)
    assert left > 0 and right_sq > 0 and margin_sq > 0
    return qminus, qplus, Psi, M2lower, left, margin_sq

pieces = [(Q(3),Q(9)), (Q(8),Q(12)), (Q(11),Q(14)), (Q(14),Q(15))]
certs = [(L,R,*certify_interval(L,R)) for L,R in pieces]

# Exact atanh log interval, used only to show W(10)<0 while total curvature remains positive.
def log_interval(x, N=80):
    z = sp.cancel((x - 1) / (x + 1))
    partial = Q(0)
    zz = z
    for k in range(N):
        partial += 2 * zz / Q(2*k + 1)
        zz *= z*z
    rem = 2 * abs(z)**(2*N + 1) / (Q(2*N + 1) * (1 - z*z))
    if z >= 0:
        return sp.cancel(partial), sp.cancel(partial + rem)
    return sp.cancel(partial - rem), sp.cancel(partial)

def add_interval(lo, hi, coeff, a, b):
    if coeff >= 0:
        return lo + coeff*a, hi + coeff*b
    return lo + coeff*b, hi + coeff*a

s0 = Q(10)
Wlo = Wup = Q(0)
Tlo = Tup = Q(0)
minq = None

for _,_,mu,a,b in rows:
    u = sp.cancel(-s0*a + s0**2*b)
    y = sp.cancel(s0**2*b)
    q = sp.cancel(1 + u)
    minq = q if minq is None or q < minq else minq
    llo, lhi = log_interval(q)

    psilo = sp.cancel(8*u/q + 10*llo)
    psih = sp.cancel(8*u/q + 10*lhi)
    Wlo, Wup = add_interval(Wlo, Wup, mu*b, psilo, psih)

    # Phi + 4 y^2/q + y psi:
    # rational part = 4u^2/q + 4y^2/q + 8yu/q,
    # log coefficient = 2u + 10y.
    base = sp.cancel(4*u*u/q + 4*y*y/q + 8*y*u/q)
    coeff = sp.cancel(2*u + 10*y)
    term_lo = base + coeff*(llo if coeff >= 0 else lhi)
    term_hi = base + coeff*(lhi if coeff >= 0 else llo)
    Tlo += mu*term_lo
    Tup += mu*term_hi

assert minq > 0
assert Wup < 0
assert Tlo > 0

print("I05-23 middle compensation exact check: PASS")
print("rank(B) =", B.rank(), "; complete events =", len(rows))
print("Amax =", Amax)
print("Bmax =", Bmax)
for L,R,qminus,qplus,Psi,M2lower,left,margin_sq in certs:
    print("piece", L, R, "qminus", qminus, "qplus", qplus)
    print("  Psi <=", Psi)
    print("  M2 >=", M2lower)
    print("  left =", left)
    print("  squared strict margin =", margin_sq)
print("therefore H''(t)<0 for the union 3 <= t^2 <= 15")
print("s=10 min q =", minq)
print("W(10) interval =", sp.N(Wlo, 55), sp.N(Wup, 55))
print("W(10) interval width =", sp.N(Wup-Wlo, 12))
print("t^2 I'' at s=10 interval =", sp.N(Tlo, 55), sp.N(Tup, 55))
print("curvature interval width =", sp.N(Tup-Tlo, 12))
