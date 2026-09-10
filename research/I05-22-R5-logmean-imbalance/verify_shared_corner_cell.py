#!/usr/bin/env python3
"""Exact same-author checker for the I05-22 shared-corner cell theorem.

This does not certify logarithmic inequalities or replace independent review.
It checks the algebraic coordinate transforms, the complete corner-basis
quadratic decomposition, the one-edge curvature identity, and independently
reconstructs the fixed rational relaxed witness recorded in PR81.
"""
from __future__ import annotations

import sympy as s


def assert_zero(expr: s.Expr, label: str) -> None:
    if s.simplify(s.expand(expr)) != 0:
        raise AssertionError(label)


def leading_minors(M: s.Matrix) -> list[s.Expr]:
    return [s.factor(M[:i, :i].det()) for i in range(1, M.rows + 1)]


# ---------------------------------------------------------------------------
# 1. Half-leaf corner coordinate transform.
# ---------------------------------------------------------------------------
A, B = s.symbols("A B", positive=True)
ell, k, lam, J = s.symbols("ell k lam J", real=True)
m, alpha, beta, gamma = s.symbols("m alpha beta gamma", real=True)
d, e = s.symbols("d e", real=True)
T00, T10, T01, T11 = s.symbols("T00 T10 T01 T11", real=True)

E = s.Matrix(
    [
        [1, -s.Rational(1, 2), -s.Rational(1, 2), s.Rational(1, 4)],
        [1, s.Rational(1, 2), -s.Rational(1, 2), -s.Rational(1, 4)],
        [1, -s.Rational(1, 2), s.Rational(1, 2), -s.Rational(1, 4)],
        [1, s.Rational(1, 2), s.Rational(1, 2), s.Rational(1, 4)],
    ]
)
assert E.det() != 0
Einv = E.inv()
T = s.Matrix([T00, T10, T01, T11])

a_plus = ell + lam / 2
a_minus = ell - lam / 2
b_plus = k + lam / 2
b_minus = k - lam / 2
n = A * k + B * ell - J

C = s.Matrix([[-ell, 0, lam / 4, 0], [-k, lam / 4, 0, 0]])
C_corner_expected = s.Matrix(
    [
        [-a_plus / 4, -a_plus / 4, -a_minus / 4, -a_minus / 4],
        [-b_plus / 4, -b_minus / 4, -b_plus / 4, -b_minus / 4],
    ]
)
assert C * Einv == C_corner_expected

R = s.zeros(4)
R[1, 1] = ell / (8 * A)
R[2, 2] = k / (8 * B)
R[1, 3] = R[3, 1] = -lam / (32 * A)
R[2, 3] = R[3, 2] = -lam / (32 * B)
R[3, 3] = n / (32 * A * B)
R_corner = s.simplify(Einv.T * R * Einv)
Delta = T00 - T10 - T01 + T11
R_corner_quadratic = s.expand((T.T * R_corner * T)[0])
R_edge_quadratic = (
    a_plus * (T00 - T10) ** 2 / (16 * A)
    + a_minus * (T01 - T11) ** 2 / (16 * A)
    + b_plus * (T00 - T01) ** 2 / (16 * B)
    + b_minus * (T10 - T11) ** 2 / (16 * B)
    - J * Delta**2 / (32 * A * B)
)
assert_zero(R_corner_quadratic - R_edge_quadratic, "R corner decomposition")

# ---------------------------------------------------------------------------
# 2. Exact complete quadratic decomposition.
# ---------------------------------------------------------------------------
f00, f10, f01, f11 = s.symbols("f00 f10 f01 f11", positive=True)
F_corner = s.diag(f00, f10, f01, f11) / 4
L = s.Matrix([[2 * A * ell, J], [J, 2 * B * k]])
M = 4 * s.eye(2)
delta = s.Matrix([d, e])
C_corner = C * Einv

Q_matrix = (delta.T * (L + M) * delta)[0]
Q_matrix += 2 * (delta.T * C_corner * T)[0]
Q_matrix += (T.T * (F_corner + R_corner) * T)[0]


def edge_energy(
    length: s.Expr,
    h: s.Expr,
    X: s.Expr,
    Y: s.Expr,
    direction: s.Expr,
    fX: s.Expr,
    fY: s.Expr,
) -> s.Expr:
    return (
        length * h * direction**2
        - h * direction * (X + Y) / 2
        + h * (X - Y) ** 2 / (16 * length)
        + (fX * X**2 + fY * Y**2) / 8
    )


Q_edges = (
    edge_energy(A, a_plus, T00, T10, d, f00, f10)
    + edge_energy(A, a_minus, T01, T11, d, f01, f11)
    + edge_energy(B, b_plus, T00, T01, e, f00, f01)
    + edge_energy(B, b_minus, T10, T11, e, f10, f11)
    + 4 * d**2
    + 4 * e**2
    + 2 * J * d * e
    - J * Delta**2 / (32 * A * B)
)
assert_zero(Q_matrix - Q_edges, "full corner quadratic decomposition")

# ---------------------------------------------------------------------------
# 3. One-edge 3/8 curvature identity.
# ---------------------------------------------------------------------------
t = s.symbols("t", real=True)
u = t * (1 - t)
r = 1 / u - 3
wfun = s.sqrt(u / (1 - 3 * u))
wsecond_expected = (
    -s.sqrt(u / (1 - 3 * u))
    * (1 - 6 * u) ** 2
    / (4 * u**2 * (1 - 3 * u) ** 2)
)
assert_zero(s.diff(wfun, t, 2) - wsecond_expected, "edge inverse-root curvature")

p, r_endpoint, h, length, X, Y = s.symbols(
    "p r_endpoint h length X Y", positive=True
)
edge = (
    length * h * d**2
    - h * d * (X + Y) / 2
    + h * (X - Y) ** 2 / (16 * length)
    + (p * X**2 + r_endpoint * Y**2) / 8
)
completed = length * h * (d - (X + Y) / (4 * length)) ** 2
residual = s.expand(edge - completed - s.Rational(3, 8) * (X - Y) ** 2)
residual_expected = (
    (p - 3) * X**2
    + 2 * (3 - h / length) * X * Y
    + (r_endpoint - 3) * Y**2
) / 8
assert_zero(residual - residual_expected, "edge 3/8 completion")

# ---------------------------------------------------------------------------
# 4. Independent exact reconstruction of the prior fixed relaxed witness.
# ---------------------------------------------------------------------------
q0 = s.Rational(11, 144)
A0 = s.Rational(1, 4)
B0 = s.Rational(4, 9)


def f_scalar(x: s.Expr) -> s.Expr:
    return 1 / (x * (1 - x))


F = s.zeros(4)
for i, j in [(0, 0), (1, 0), (0, 1), (1, 1)]:
    tij = q0 + A0 * (1 - i) + B0 * (1 - j)
    avec = s.Matrix(
        [
            1,
            s.Rational(2 * i - 1, 2),
            s.Rational(2 * j - 1, 2),
            s.Rational((2 * i - 1) * (2 * j - 1), 4),
        ]
    )
    F += s.Rational(1, 4) * f_scalar(tij) * (avec * avec.T)

rel_ell = s.Rational(10)
rel_k = s.Rational(15)
rel_lam = s.Rational(-8)
rel_J = s.Rational(4, 3)
rel_n = A0 * rel_k + B0 * rel_ell - rel_J

Lr = s.Matrix([[2 * A0 * rel_ell, rel_J], [rel_J, 2 * B0 * rel_k]])
Cr = s.Matrix(
    [[-rel_ell, 0, rel_lam / 4, 0], [-rel_k, rel_lam / 4, 0, 0]]
)
Rr = s.zeros(4)
Rr[1, 1] = rel_ell / (8 * A0)
Rr[2, 2] = rel_k / (8 * B0)
Rr[1, 3] = Rr[3, 1] = -rel_lam / (32 * A0)
Rr[2, 3] = Rr[3, 2] = -rel_lam / (32 * B0)
Rr[3, 3] = rel_n / (32 * A0 * B0)
Yr = F + Rr
Er = Lr + 4 * s.eye(2) - Cr * Yr.inv() * Cr.T

expected_minors = [
    s.Rational(1007133237504, 141900356675),
    s.Rational(73499877824256, 1560903923425),
    s.Rational(16957014248520, 62436156937),
    s.Rational(1966230941289057, 3567780396400),
]
assert leading_minors(Yr) == expected_minors
assert s.factor(Er.det()) == -s.Rational(
    121782415397102417605, 391498427421110016
)

q = s.symbols("q")
fq = lambda z: 1 / (z * (1 - z))
ell_prime = (
    fq(q + A0 + B0) - fq(q + B0) + fq(q + A0) - fq(q)
) / 2
k_prime = (
    fq(q + A0 + B0) - fq(q + A0) + fq(q + B0) - fq(q)
) / 2
lam_prime = fq(q + A0 + B0) - fq(q + B0) - fq(q + A0) + fq(q)
assert s.factor(ell_prime.subs(q, q0)) == -s.Rational(
    565563230208, 141900356675
)
assert s.factor(k_prime.subs(q, q0)) == -s.Rational(
    642389409792, 141900356675
)
assert s.factor(lam_prime.subs(q, q0)) == s.Rational(
    1600526352384, 141900356675
)

# ---------------------------------------------------------------------------
# 5. Exact rational gates for the fixed-shape corollary.
# ---------------------------------------------------------------------------
assert 12 * A0 * B0 == s.Rational(4, 3)
exp_lower = (
    1
    + s.Rational(7, 10)
    + s.Rational(7, 10) ** 2 / 2
    + s.Rational(7, 10) ** 3 / 6
)
assert exp_lower == s.Rational(12013, 6000)
assert exp_lower > 2
assert s.Rational(13, 10) < s.Rational(4, 3)

# ---------------------------------------------------------------------------
# 6. Direct complete-eight-event comparison at the fixed rational center.
# ---------------------------------------------------------------------------
sline = s.symbols("sline")
Kx = s.Rational(1, 2)
Ky = s.Rational(1, 2)
Kz = s.Rational(61, 144)
Ka = s.Rational(0)
Kb = s.Rational(1, 4)
Kc = s.Rational(1, 3)


def direct_complete_curvature(direction: tuple[s.Rational, ...]) -> s.Expr:
    D11, D22, D33, D12, D13, D23 = direction
    xx = Kx + sline * D11
    yy = Ky + sline * D22
    zz = Kz + sline * D33
    aa = Ka + sline * D12
    bb = Kb + sline * D13
    cc = Kc + sline * D23
    q12 = xx * yy - aa**2
    q13 = xx * zz - bb**2
    q23 = yy * zz - cc**2
    detk = (
        xx * yy * zz
        + 2 * aa * bb * cc
        - xx * cc**2
        - yy * bb**2
        - zz * aa**2
    )
    atoms = [
        1 - xx - yy - zz + q12 + q13 + q23 - detk,
        xx - q12 - q13 + detk,
        yy - q12 - q23 + detk,
        q12 - detk,
        zz - q13 - q23 + detk,
        q13 - detk,
        q23 - detk,
        detk,
    ]
    values = [s.simplify(atom.subs(sline, 0)) for atom in atoms]
    first = [s.simplify(s.diff(atom, sline).subs(sline, 0)) for atom in atoms]
    second = [
        s.simplify(s.diff(atom, sline, 2).subs(sline, 0)) for atom in atoms
    ]
    assert sum(values) == 1
    assert sum(first) == 0
    assert sum(second) == 0
    assert all(value > 0 for value in values)
    return s.expand_log(
        sum(
            first[i] ** 2 / values[i] + second[i] * s.log(values[i])
            for i in range(8)
        ),
        force=True,
    )


def corner_curvature(direction: tuple[s.Rational, ...]) -> s.Expr:
    D11, D22, D33, D12, D13, D23 = direction
    m_value = D33 + A0 * D11 + B0 * D22
    alpha_value = -2 * A0 * D13 / Kb
    beta_value = -2 * B0 * D23 / Kc
    gamma_value = 2 * A0 * B0 * D12 / (Kb * Kc)
    t_values = E * s.Matrix([m_value, alpha_value, beta_value, gamma_value])

    t00 = q0 + A0 + B0
    t10 = q0 + B0
    t01 = q0 + A0
    t11 = q0
    logit = lambda z: s.log(z / (1 - z))
    potential = lambda z: z * s.log(z) + (1 - z) * s.log(1 - z)
    a_plus_value = logit(t00) - logit(t10)
    a_minus_value = logit(t01) - logit(t11)
    b_plus_value = logit(t00) - logit(t01)
    b_minus_value = logit(t10) - logit(t11)
    ell_value = (a_plus_value + a_minus_value) / 2
    k_value = (b_plus_value + b_minus_value) / 2
    lam_value = a_plus_value - a_minus_value
    J_value = (
        potential(t00)
        + potential(t11)
        - potential(t10)
        - potential(t01)
    )

    substitution = {
        A: A0,
        B: B0,
        ell: ell_value,
        k: k_value,
        lam: lam_value,
        J: J_value,
        d: D11,
        e: D22,
        T00: t_values[0],
        T10: t_values[1],
        T01: t_values[2],
        T11: t_values[3],
        f00: f_scalar(t00),
        f10: f_scalar(t10),
        f01: f_scalar(t01),
        f11: f_scalar(t11),
    }
    return s.expand_log(Q_matrix.subs(substitution), force=True)


directions = [
    (
        s.Rational(2, 7),
        s.Rational(-3, 11),
        s.Rational(5, 13),
        s.Rational(1, 17),
        s.Rational(-2, 19),
        s.Rational(3, 23),
    ),
    (
        s.Rational(0),
        s.Rational(0),
        s.Rational(4, 15),
        s.Rational(-2, 21),
        s.Rational(5, 18),
        s.Rational(-1, 14),
    ),
    (
        s.Rational(-3, 10),
        s.Rational(7, 20),
        s.Rational(-2, 9),
        s.Rational(4, 25),
        s.Rational(0),
        s.Rational(5, 27),
    ),
]
for index, direction in enumerate(directions, start=1):
    assert_zero(
        direct_complete_curvature(direction) - corner_curvature(direction),
        f"direct complete-event comparison {index}",
    )

# ---------------------------------------------------------------------------
# 7. Fixed-shape quantitative lower Gram matrix.
# ---------------------------------------------------------------------------
zvec = s.Matrix([d, e, T00, T10, T01, T11])
Qstar = (
    s.Rational(27, 10) * (d**2 + e**2)
    + s.Rational(3, 320) * Delta**2
    + s.Rational(1, 4)
    * ((d - T00 - T10) ** 2 + (d - T01 - T11) ** 2)
    + s.Rational(64, 81)
    * (
        (e - s.Rational(9, 16) * (T00 + T01)) ** 2
        + (e - s.Rational(9, 16) * (T10 + T11)) ** 2
    )
)
Gstar = s.hessian(Qstar, zvec) / 2
expected_Gstar_minors = [
    s.Rational(16, 5),
    s.Rational(27736, 2025),
    s.Rational(1969009, 324000),
    s.Rational(11805091, 5184000),
    s.Rational(261937, 345600),
    s.Rational(6059, 64000),
]
assert leading_minors(Gstar) == expected_Gstar_minors
assert s.trace(Gstar) == s.Rational(12335, 1296)
alpha_bound = s.factor(Gstar.det() / s.trace(Gstar) ** 5)
assert alpha_bound == s.Rational(
    43266921852229632, 35694868153272307421875
)

print(f"SymPy {s.__version__}")
print("PASS: half-leaf corner transform and R edge/cell decomposition")
print("PASS: complete six-coordinate quadratic decomposition")
print("PASS: inverse-root curvature and one-edge 3/8 completion")
print("PASS: independent exact reconstruction of prior relaxed witness")
print("PASS: exact fixed-shape rational gates")
print("PASS: direct original eight-event comparisons in three physical directions")
print("PASS: fixed-shape quantitative Gram minors")
print("ALL SHARED-CORNER CELL CHECKS PASSED")
