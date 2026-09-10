from sympy import Matrix, Rational, symbols, diag, factor, expand, Poly, simplify
from collections import defaultdict

t, s = symbols("t s")
Q = Matrix.ones(3, 3) / 3
P = Matrix.eye(3) - Q
A = Rational(1, 10) * P + Rational(1, 3) * Q
C = Rational(9, 10) * P + Rational(2, 3) * Q
B = Rational(3, 10) * P
K = A.row_join(t * B).col_join((t * B).T.row_join(C))


def atom(M, mask):
    n = M.rows
    D = diag(*[0 if (mask >> i) & 1 else 1 for i in range(n)])
    return factor((-1) ** (n - mask.bit_count()) * (M - D).det())


rows = []
for L in range(8):
    muL = atom(A, L)
    for R in range(8):
        muR = atom(C, R)
        mu = factor(muL * muR)
        p = atom(K, L | (R << 3))
        q = factor(p / mu)
        pol = Poly(expand(q), t)
        a = factor(-pol.coeff_monomial(t ** 2))
        b = factor(pol.coeff_monomial(t ** 4))
        assert simplify(q - (1 - a * t ** 2 + b * t ** 4)) == 0
        rows.append((L, R, mu, a, b, q))

G = defaultdict(lambda: [Rational(0), 0])
for _, _, mu, a, b, q in rows:
    G[(expand(q), a, b)][0] += mu
    G[(expand(q), a, b)][1] += 1

assert len(G) == 11
assert simplify(sum(v[0] for v in G.values()) - 1) == 0
assert simplify(sum(mu * a for _, _, mu, a, b, q in rows)) == 0
assert simplify(sum(mu * b for _, _, mu, a, b, q in rows)) == 0

bad = []
for (q, a, b), (w, mult) in G.items():
    z = factor((a - s * b) * (a - 6 * s * b))
    if (a, b) in [
        (Rational(2), Rational(1)),
        (Rational(-14, 13), Rational(-27, 13)),
        (Rational(302, 1521), Rational(9, 169)),
    ]:
        bad.append((q, a, b, w, mult, z))
assert len(bad) == 3

W = Rational(67, 750)
c0 = 16 * Rational(9, 2500)
c4 = 2 * Rational(13, 5000) * Rational(1225, 1014)
c7 = 2 * Rational(507, 5000) * Rational(3128, 177957)
reserve = factor(2 * W - c0 - c4 - c7)
assert reserve == Rational(195191, 1755000)
assert reserve > 0

assert B[0, 0] == Rational(1, 5)
fisher_c = 16 * B[0, 0] ** 4
assert fisher_c == Rational(16, 625)
quartic_c = factor(fisher_c / 12)
assert quartic_c == Rational(4, 1875)

print("PASS")
print("events=64 groups=11")
print("acceleration_reserve =", reserve)
print("fisher_normalized_lower =", fisher_c)
print("quartic_correction =", quartic_c)
print("group table:")
for (q, a, b), (w, mult) in sorted(G.items(), key=lambda kv: str(kv[0][0])):
    print("mult", mult, "weight", factor(w), "a", a, "b", b, "q", factor(q))
