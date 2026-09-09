#!/usr/bin/env python3
"""Exact author-side checks for I05-W4 round 2.

This script checks finite algebraic identities with SymPy.  It is not an
independent review and does not use numerical sampling as proof.
"""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


def z(expr: sp.Expr) -> None:
    """Assert exact symbolic zero after simplification."""
    got = sp.factor(sp.cancel(sp.together(sp.simplify(expr))))
    if got != 0:
        raise AssertionError(f"nonzero symbolic remainder: {got}")


def event_polynomials(K: sp.Matrix) -> list[sp.Expr]:
    x, y, z0 = K[0, 0], K[1, 1], K[2, 2]
    a, b, c = K[0, 1], K[0, 2], K[1, 2]
    q12 = x * y - a**2
    q13 = x * z0 - b**2
    q23 = y * z0 - c**2
    r = x * y * z0 + 2 * a * b * c - x * c**2 - y * b**2 - z0 * a**2
    return [
        1 - x - y - z0 + q12 + q13 + q23 - r,
        x - q12 - q13 + r,
        y - q12 - q23 + r,
        q12 - r,
        z0 - q13 - q23 + r,
        q13 - r,
        q23 - r,
        r,
    ]


def check_symmetric_connected_family() -> None:
    tau = sp.symbols("tau", real=True)
    k = sp.symbols("k", real=True, nonzero=True)
    d1, d2, d3, h12, h13, h23 = sp.symbols(
        "d1 d2 d3 h12 h13 h23", real=True
    )
    Kt = sp.Matrix(
        [
            [sp.Rational(1, 2) + tau * d1, tau * h12, k + tau * h13],
            [tau * h12, sp.Rational(1, 2) + tau * d2, k + tau * h23],
            [k + tau * h13, k + tau * h23, sp.Rational(1, 2) + tau * d3],
        ]
    )
    ps = event_polynomials(Kt)
    p0 = [sp.factor(p.subs(tau, 0)) for p in ps]
    p1 = [sp.factor(sp.diff(p, tau).subs(tau, 0)) for p in ps]
    p2 = [sp.factor(sp.diff(p, tau, 2).subs(tau, 0)) for p in ps]

    s_k = 8 * k**2
    expected_p0 = [
        (1 - s_k) / 8,
        sp.Rational(1, 8),
        sp.Rational(1, 8),
        (1 + s_k) / 8,
        (1 + s_k) / 8,
        sp.Rational(1, 8),
        sp.Rational(1, 8),
        (1 - s_k) / 8,
    ]
    for got, want in zip(p0, expected_p0):
        z(got - want)
    z(sum(p0) - 1)
    z(sum(p1))
    z(sum(p2))

    P, Delta, Z, R, H, N = sp.symbols("P Delta Z R H N", real=True)
    sub_dir = {
        d1: (P + Delta) / 2,
        d2: (P - Delta) / 2,
        d3: Z,
        h12: R,
        h13: (H + N) / 2,
        h23: (H - N) / 2,
    }
    expected_4p1 = [
        -4 * k * H + 4 * k**2 * P - P - 8 * k**2 * R - Z,
        Delta + 4 * k * N - 4 * k**2 * P + 8 * k**2 * R - Z,
        -Delta - 4 * k * N - 4 * k**2 * P + 8 * k**2 * R - Z,
        4 * k * H + 4 * k**2 * P + P - 8 * k**2 * R - Z,
        4 * k * H - 4 * k**2 * P - P + 8 * k**2 * R + Z,
        Delta - 4 * k * N + 4 * k**2 * P - 8 * k**2 * R + Z,
        -Delta + 4 * k * N + 4 * k**2 * P - 8 * k**2 * R + Z,
        -4 * k * H - 4 * k**2 * P + P + 8 * k**2 * R + Z,
    ]
    for got, want in zip(p1, expected_4p1):
        z(4 * got.subs(sub_dir) - want)

    group_minus = sp.factor((p2[0] + p2[7]).subs(sub_dir))
    group_plus = sp.factor((p2[3] + p2[4]).subs(sub_dir))
    group_zero = sp.factor(sum(p2[i] for i in (1, 2, 5, 6)).subs(sub_dir))
    z(
        group_minus
        + (Delta**2 + 2 * H**2 + 2 * N**2 - P**2 - 4 * P * Z + 4 * R**2) / 2
    )
    z(
        group_plus
        + (Delta**2 - 2 * H**2 - 2 * N**2 - P**2 + 4 * P * Z + 4 * R**2) / 2
    )
    z(group_zero - (Delta**2 - P**2 + 4 * R**2))

    fisher = sp.factor(sum(pp**2 / p for pp, p in zip(p1, p0)).subs(sub_dir))
    s = sp.symbols("s", real=True)
    Ds = 1 - s**2
    vec = sp.Matrix([P, Z, R])
    Fmat = sp.Matrix(
        [
            [(4 - 2 * s**2 - s**4) / 2, s * (2 - s**2), s**4],
            [s * (2 - s**2), 2 * (2 - s**2), 2 * s**3],
            [s**4, 2 * s**3, 2 * s**2 * (2 - s**2)],
        ]
    ) / Ds
    fisher_expected = (
        (vec.T * Fmat * vec)[0]
        + 4 * s * H**2 / Ds
        + 2 * Delta**2
        + 4 * s * N**2
    )
    z(fisher - fisher_expected.subs(s, s_k))

    lm, lp, l0 = sp.symbols("lm lp l0", real=True)
    acceleration = sp.expand(group_minus * lm + group_plus * lp + group_zero * l0)
    m, g = sp.symbols("m g", real=True)
    acceleration_mg = sp.expand(
        acceleration.subs({lm: l0 + (m - g) / 2, lp: l0 + (m + g) / 2})
    )
    acceleration_expected = (
        m * (P**2 - Delta**2 - 4 * R**2) / 2
        + g * (H**2 + N**2 - 2 * P * Z)
    )
    z(acceleration_mg - acceleration_expected)

    # Exact positivity certificate for the final 3x3 block.
    s = sp.symbols("s", positive=True)
    Ds = 1 - s**2
    mfun = sp.log(1 - s**2)
    gfun = sp.log((1 + s) / (1 - s))
    G = sp.Matrix(
        [
            [
                mfun / 2 + (4 - 2 * s**2 - s**4) / (2 * Ds),
                s * (2 - s**2) / Ds - gfun,
                s**4 / Ds,
            ],
            [
                s * (2 - s**2) / Ds - gfun,
                2 * (2 - s**2) / Ds,
                2 * s**3 / Ds,
            ],
            [
                s**4 / Ds,
                2 * s**3 / Ds,
                -2 * mfun + 2 * s**2 * (2 - s**2) / Ds,
            ],
        ]
    )
    Gp = sp.simplify(G.diff(s))
    Gp_expected = sp.Matrix(
        [
            [s * (s**4 - s**2 + 1), s**2 * (s**2 + 1), 2 * s**3 * (2 - s**2)],
            [s**2 * (s**2 + 1), 4 * s, 2 * s**2 * (3 - s**2)],
            [
                2 * s**3 * (2 - s**2),
                2 * s**2 * (3 - s**2),
                4 * s * (s**4 - 3 * s**2 + 3),
            ],
        ]
    ) / Ds**2
    for i in range(3):
        for j in range(3):
            z(Gp[i, j] - Gp_expected[i, j])
    z(Gp[0, 0] - s * (s**4 - s**2 + 1) / Ds**2)
    z(Gp[:2, :2].det() - s**2 * (s**4 - s**2 + 4) / Ds**3)
    z(Gp.det() - 48 * s**3 / Ds**3)

    # Rational strong-coupling witness k=1/3.
    kval = sp.Rational(1, 3)
    witness = [sp.factor(p.subs(k, kval)) for p in expected_p0]
    expected_witness = [
        sp.Rational(1, 72),
        sp.Rational(1, 8),
        sp.Rational(1, 8),
        sp.Rational(17, 72),
        sp.Rational(17, 72),
        sp.Rational(1, 8),
        sp.Rational(1, 8),
        sp.Rational(1, 72),
    ]
    assert witness == expected_witness
    print("symmetric connected family: exact checks passed")


def check_two_point_conditional_entropy() -> None:
    y, w, e, U, V = sp.symbols("y w e U V", nonzero=True)
    r = y * (1 - y)
    d = y * U + (1 - y) * V - w * e
    qprime = (1 - 2 * y) * e * w + r * (V - U)
    delta_from_affine = d * e - qprime**2 / (4 * r * w)
    delta_claim = e * (U + V) / 2 - w * e**2 / (4 * r) - r * (V - U) ** 2 / (4 * w)
    z(delta_from_affine - delta_claim)

    Au, Av, L = sp.symbols("Au Av L", positive=True)
    M = sp.Matrix([[y * Au, -L * r / w], [-L * r / w, (1 - y) * Av]])
    z(M.det() - (r * Au * Av - L**2 * r**2 / w**2))
    print("two-point conditional entropy lemma: algebraic checks passed")


def check_block_factorization() -> None:
    tau = sp.symbols("tau", real=True)
    x, y, z0, a = sp.symbols("x y z a", real=True)
    d1, d2, d3, h12, h13, h23 = sp.symbols(
        "d1 d2 d3 h12 h13 h23", real=True
    )
    Kt = sp.Matrix(
        [
            [x + tau * d1, a + tau * h12, tau * h13],
            [a + tau * h12, y + tau * d2, tau * h23],
            [tau * h13, tau * h23, z0 + tau * d3],
        ]
    )
    ps = event_polynomials(Kt)
    p0 = [sp.factor(p.subs(tau, 0)) for p in ps]
    p1 = [sp.factor(sp.diff(p, tau).subs(tau, 0)) for p in ps]
    p2 = [sp.factor(sp.diff(p, tau, 2).subs(tau, 0)) for p in ps]

    q = x * y - a**2
    us = [1 - x - y + q, x - q, y - q, q]  # 0,1,2,12
    At = sp.Matrix([[x + tau * d1, a + tau * h12], [a + tau * h12, y + tau * d2]])
    qt = At[0, 0] * At[1, 1] - At[0, 1] ** 2
    uts = [1 - At[0, 0] - At[1, 1] + qt, At[0, 0] - qt, At[1, 1] - qt, qt]
    u1 = [sp.diff(u, tau).subs(tau, 0) for u in uts]
    u2 = [sp.diff(u, tau, 2).subs(tau, 0) for u in uts]
    ws = [1 - z0, z0]
    w1 = [-d3, d3]

    # Map full event order to pair-state and singleton-state.
    map_sk = [(0, 0), (1, 0), (2, 0), (3, 0), (0, 1), (1, 1), (2, 1), (3, 1)]
    for idx, (si, ki) in enumerate(map_sk):
        z(p0[idx] - us[si] * ws[ki])
        z(p1[idx] - (u1[si] * ws[ki] + us[si] * w1[ki]))

    for si in range(4):
        inds = [idx for idx, pair in enumerate(map_sk) if pair[0] == si]
        z(sum(p2[idx] for idx in inds) - u2[si])
    for ki in range(2):
        inds = [idx for idx, pair in enumerate(map_sk) if pair[1] == ki]
        z(sum(p2[idx] for idx in inds))

    fisher_full = sum(pp**2 / p for pp, p in zip(p1, p0))
    fisher_pair = sum(pp**2 / u for pp, u in zip(u1, us))
    fisher_single = d3**2 / (z0 * (1 - z0))
    z(fisher_full - fisher_pair - fisher_single)
    print("block factorization: all eight-event checks passed")


def check_general_missing_edge_coordinates() -> None:
    tau = sp.symbols("tau", real=True)
    x, y, z0, b, c = sp.symbols("x y z b c", real=True, nonzero=True)
    d1, d2, d3, h12, h13, h23 = sp.symbols(
        "d1 d2 d3 h12 h13 h23", real=True
    )
    Kt = sp.Matrix(
        [
            [x + tau * d1, tau * h12, b + tau * h13],
            [tau * h12, y + tau * d2, c + tau * h23],
            [b + tau * h13, c + tau * h23, z0 + tau * d3],
        ]
    )
    ps = event_polynomials(Kt)
    # event index by (i,j,k)
    event_index = {
        (0, 0, 0): 0,
        (1, 0, 0): 1,
        (0, 1, 0): 2,
        (1, 1, 0): 3,
        (0, 0, 1): 4,
        (1, 0, 1): 5,
        (0, 1, 1): 6,
        (1, 1, 1): 7,
    }
    v1 = x * (1 - x)
    v2 = y * (1 - y)
    Ts: list[sp.Expr] = []
    for i, j in ((0, 0), (1, 0), (0, 1), (1, 1)):
        p1_event = ps[event_index[(i, j, 1)]]
        p0_event = ps[event_index[(i, j, 0)]]
        cond = sp.cancel(p1_event / (p1_event + p0_event))
        center = sp.factor(cond.subs(tau, 0))
        deriv = sp.factor(sp.diff(cond, tau).subs(tau, 0))
        phi = (i - x) / v1
        psi = (j - y) / v2
        center_claim = z0 - b**2 * phi - c**2 * psi
        deriv_claim = (
            d3
            + b**2 * d1 * phi**2
            + c**2 * d2 * psi**2
            - 2 * b * h13 * phi
            - 2 * c * h23 * psi
            + 2 * b * c * h12 * phi * psi
        )
        z(center - center_claim)
        z(deriv - deriv_claim)
        Ts.append(deriv_claim)

    directions = [d1, d2, d3, h12, h13, h23]
    outputs = [d1, d2] + Ts
    J = sp.Matrix([[sp.diff(out, var) for var in directions] for out in outputs])
    z(J.det() - 8 * b**2 * c**2 / (v1**2 * v2**2))
    print("general missing-edge event coordinates: exact checks passed")


def check_inputs_file() -> None:
    path = Path(__file__).resolve().parents[1] / "inputs" / "exact_inputs.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["symmetric_connected_strong_example"]["s"] == "8/9"
    assert data["block_strong_example"]["normalized_block_edge"] == "49/25"
    print("exact input manifest: parsed")


def main() -> None:
    check_symmetric_connected_family()
    check_two_point_conditional_entropy()
    check_block_factorization()
    check_general_missing_edge_coordinates()
    check_inputs_file()
    print("ALL SYMBOLIC CHECKS PASSED")


if __name__ == "__main__":
    main()
