from sympy import symbols, Rational, factor, simplify

alpha, beta = symbols("alpha beta", positive=True)
r = alpha * (1 - alpha)
B0 = beta * (1 - beta)
d = beta - alpha

m0 = (1 - alpha) ** 2 * (1 - beta)
m1 = (1 - alpha) * (2 * alpha + beta - 3 * alpha * beta) / 3
m2 = alpha * (alpha + 2 * beta - 3 * alpha * beta) / 3
m3 = alpha ** 2 * beta

X = 2 * alpha + beta - 3 * alpha * beta
Y = alpha + 2 * beta - 3 * alpha * beta
D = factor(X * Y)
assert factor(D - (9 * r * B0 + 2 * d ** 2)) == 0

M2 = factor(2 * m0 * m3)
assert factor(M2 - 2 * r ** 2 * B0) == 0

MZ_direct = factor(6 * m3 * m1 + 6 * m0 * m2 + 6 * m1 * m2 + 2 * m0 * m3)
MZ_closed = factor(2 * r ** 2 + 4 * r * B0 * (1 - r) + Rational(4, 3) * r * d ** 2)
assert factor(MZ_direct - MZ_closed) == 0

C_ext = 4 * r * B0
C_mid = Rational(4, 3) * r * (d ** 2 + r)
C1 = factor(C_ext + C_mid)

L_from_orders = factor(2 * (5 * C1 - 4 * MZ_closed - 4 * M2))
L_closed = factor(Rational(8, 3) * r * (d ** 2 - r + 3 * (1 + 2 * r) * B0))
assert factor(L_from_orders - L_closed) == 0

G = factor(d ** 2 - r + 3 * (1 + 2 * r) * B0)
G_quadratic = (
    -2 * (1 + 3 * r) * beta ** 2
    + (3 + 6 * r - 2 * alpha) * beta
    + alpha * (2 * alpha - 1)
)
assert factor(G - G_quadratic) == 0
assert factor(G.subs({alpha: 1 - alpha, beta: 1 - beta}) - G) == 0

L_alpha01 = factor(L_closed.subs(alpha, Rational(1, 10)))
assert L_alpha01 == -Rational(3, 625) * (127 * beta ** 2 - 167 * beta + 4)

F_pole = factor(4 * C1)
assert F_pole == factor(Rational(16, 3) * r * (3 * B0 + d ** 2 + r))

Nb = (
    7 * alpha ** 2 * beta ** 2
    - 7 * alpha ** 2 * beta
    + 2 * alpha ** 2
    - 4 * alpha * beta ** 3
    - alpha * beta ** 2
    + alpha * beta
    + 2 * beta ** 3
)
assert factor(D - Nb) == 2 * beta * (1 - beta) * (
    (1 - alpha) * (alpha + beta) + alpha * (1 - beta)
)

x = symbols("x", nonnegative=True)
f0 = Rational(162, 125) / (1 + 5 * x) + Rational(12, 125) / (1 + 15 * x) + Rational(6, 125)
f1 = Rational(324, 125) / (3 + 5 * x) + Rational(162, 125) / (9 + 5 * x) + Rational(54, 125)
assert simplify(f0 - Rational(6, 125)) > 0
assert simplify(f1 - Rational(54, 125)) > 0
assert f0.subs(x, 0) == Rational(36, 25)
assert f1.subs(x, 0) == Rational(36, 25)

print("PASS: endpoint phase, Fisher pole, Mb bound, and two-scale crossover identities")
