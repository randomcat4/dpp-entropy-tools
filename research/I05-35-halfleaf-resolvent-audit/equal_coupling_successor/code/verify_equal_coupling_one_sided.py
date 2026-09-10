#!/usr/bin/env python3
"""Exact algebra audit for the equal-coupling half-leaf one-sided theorem.

This script starts from the four leaf events and their true affine K-jets,
builds the full six-coordinate Hessian of G1, performs the leaf-swap block
reduction, and checks the scalar determinant identities used in the proof.
It does not sample parameters or call any PR81/PR104 checker.
"""
from itertools import product
import sympy as s

# Normalized one-sided corner q=1, equal normalized couplings a=b=t>0.
t = s.symbols("t", positive=True)
C, V = s.symbols("C V", positive=True)  # C=log(1+2t), V=2log(1+t)-C
x, y, u, w, r, z = s.symbols("x y u w r z", real=True)
coords = (x, y, u, w, r, z)

# Corner logs in sign order: (+,+):0, mixed: (C+V)/2, (-,-):C.
def corner_log(eps, eta):
    if (eps, eta) == (1, 1):
        return s.Integer(0)
    if eps != eta:
        return (C + V) / 2
    return C

Q = 0
for eps, eta in product((1, -1), repeat=2):
    q0 = 1 + t * (1 - eps) / 2 + t * (1 - eta) / 2
    ell = corner_log(eps, eta)
    P1 = (eps * x + eta * y) / 2
    P2 = 2 * eps * eta * (x * y - w**2 / (4 * t**2))
    T = u + eps * eta * w - eps * r - eta * z
    E1 = r - 2 * eps * t * x - eta * w
    E2 = z - eps * w - 2 * eta * t * y
    q2 = -eps * E1**2 / t - eta * E2**2 / t
    Q += P2 * q0 * ell + 2 * P1 * (ell + 1) * T
    Q += s.Rational(1, 4) * (T**2 / q0 + (ell + 1) * q2)

M = s.simplify(s.hessian(s.expand(Q), coords) / 2)

# Leaf-symmetric / antisymmetric coordinates
rt2 = s.sqrt(2)
Tmat = s.zeros(6)
# old order x,y,u,w,r,z; new order x+,x-,u,w,r+,r-
Tmat[0, 0] = Tmat[0, 1] = 1 / rt2
Tmat[1, 0] = 1 / rt2
Tmat[1, 1] = -1 / rt2
Tmat[2, 2] = 1
Tmat[3, 3] = 1
Tmat[4, 4] = Tmat[4, 5] = 1 / rt2
Tmat[5, 4] = 1 / rt2
Tmat[5, 5] = -1 / rt2
N = s.simplify(Tmat.T * M * Tmat)

minus = N.extract((1, 5), (1, 5))
minus_target = s.Matrix([
    [(t + 1) * V, -V / 2],
    [-V / 2, (C * (t + 1) + 4 * t) / (4 * t * (t + 1))],
])
assert s.simplify(minus - minus_target) == s.zeros(2)

plus = N.extract((0, 2, 3, 4), (0, 2, 3, 4))
y11 = (t**2 + 4*t + 2) / (2*(t+1)*(2*t+1))
y12 = t**2 / (2*(t+1)*(2*t+1))
y13 = -rt2*t / (2*(2*t+1))
y22 = y11 + V*(t+1)/(2*t**2)
y23 = -rt2*((2*t+1)*V + 2*t**2)/(4*t*(2*t+1))
y33 = (t+1)/(2*t+1) + C/(4*t)
plus_target = s.Matrix([
    [2*C*t-(t+1)*V, -C/rt2, 0, V/2],
    [-C/rt2, y11, y12, y13],
    [0, y12, y22, y23],
    [V/2, y13, y23, y33],
])
assert s.simplify(plus - plus_target) == s.zeros(4)

Y = plus[1:, 1:]
minor1 = s.factor(Y[0, 0])
minor2 = s.factor(Y[:2, :2].det())
minor3 = s.factor(Y.det())
assert s.simplify(minor1 - y11) == 0
assert s.simplify(minor2 - (V*(t**2+4*t+2)+4*t**2)/(4*t**2*(2*t+1))) == 0
assert s.simplify(minor3 - ((t+1)*C-t*V+4*t)*(V*(t**2+4*t+2)+4*t**2)
                  /(16*t**3*(t+1)*(2*t+1))) == 0

rho = s.symbols("rho", positive=True)
P = (C**3*V*rho**2 - C**3*V + C**3*rho**4 - 2*C**3*rho**2
     - C**2*V**2*rho**3 + C**2*V**2*rho + 2*C**2*V*rho**3
     + C*V**2*rho**2 - 2*C*V**2 - 8*C*V*rho**4 + 12*C*V*rho**2
     + 32*C*rho**4 + 4*V**2*rho**3 - 8*V**2*rho - 16*V*rho**3)
assert s.simplify(plus.det().subs(t, rho/(1-rho))
                  - (1-rho)*P/(16*rho**3*(1+rho))) == 0

G = s.symbols("G", real=True)
PG = s.expand(P.subs(V, rho*C-G))
Rcurv = (2-rho**2)*(C+4*rho)-C**2*rho*(1-rho**2)
assert s.simplify(s.diff(PG, G, 2) + 2*Rcurv) == 0

k, omega, R = s.symbols("k omega R", positive=True)
# Endpoint identities: substitute C=k*rho, omega=1-rho^2, R=k^2*omega.
low = s.factor(PG.subs(G, rho**2).subs(C, k*rho) / rho**5)
high = s.factor(PG.subs(G, 2*rho**2).subs(C, k*rho) / rho**5)
low_target = k*(19-omega-R*(5-2*omega)) + R*(9-omega-R) + 12-4*omega
high_target = k*(4*(5-omega)-2*R*(3-2*omega)) + R*(4*(4-omega)-R) + 16*(1-omega)
subs_rel = {rho**2: 1-omega, k**2*omega: R}
# Groebner reduction is robust against powers of rho/k in the raw expression.
rels = [rho**2 + omega - 1, k**2*omega - R]
vars_poly = (rho, k, omega, R)
assert s.reduced(s.together(low-low_target), rels, *vars_poly)[1] == 0
assert s.reduced(s.together(high-high_target), rels, *vars_poly)[1] == 0

print("PASS: full four-event G1 Hessian reconstructed in all six physical directions")
print("PASS: exact 2x2 antisymmetric and 4x4 symmetric block decomposition")
print("PASS: positive conditional pivot minors and scalar determinant polynomial")
print("PASS: scalar concavity and both endpoint decompositions")
print("NO SAMPLING; analytic inequality proof is in equal_coupling_one_sided_theorem.md")
