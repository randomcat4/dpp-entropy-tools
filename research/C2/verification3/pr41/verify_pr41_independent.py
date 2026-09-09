#!/usr/bin/env python3
"""Independent exact verification for PR41 / issue 45.

This checker replays the author-side script as a subprocess, then performs an
independent SymPy reconstruction from principal minors and Mobius inversion.
It does not import the author verifier or use floating point arithmetic.
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import subprocess
import sys
import time
import traceback
from itertools import combinations
from pathlib import Path
from typing import Any, Callable

import sympy as sp


EVENTS_3 = [(), (0,), (1,), (0, 1), (2,), (0, 2), (1, 2), (0, 1, 2)]
EVENT_LABELS_3 = ["0", "1", "2", "12", "3", "13", "23", "123"]
EVENTS_2 = [(), (0,), (1,), (0, 1)]
EVENT_LABELS_2 = ["0", "1", "2", "12"]


class CheckFailure(AssertionError):
    pass


def exact_zero(expr: sp.Expr, context: str) -> None:
    got = sp.factor(sp.cancel(sp.together(sp.simplify(expr))))
    if got != 0:
        raise CheckFailure(f"{context}: nonzero remainder {got}")


def no_float_atoms(exprs: list[sp.Expr], context: str) -> None:
    floats: set[sp.Float] = set()
    for expr in exprs:
        floats |= expr.atoms(sp.Float)
    if floats:
        raise CheckFailure(f"{context}: found Float atoms {sorted(map(str, floats))}")


def powerset_from(items: list[int]) -> list[tuple[int, ...]]:
    out: list[tuple[int, ...]] = []
    for r in range(len(items) + 1):
        out.extend(tuple(c) for c in combinations(items, r))
    return out


def principal_det(K: sp.Matrix, subset: tuple[int, ...]) -> sp.Expr:
    if not subset:
        return sp.Integer(1)
    return sp.factor(K.extract(subset, subset).det())


def event_probability(K: sp.Matrix, event: tuple[int, ...]) -> sp.Expr:
    n = K.rows
    event_set = set(event)
    remaining = [i for i in range(n) if i not in event_set]
    total = sp.Integer(0)
    for extra in powerset_from(remaining):
        superset = tuple(sorted(event + extra))
        sign = -1 if (len(superset) - len(event)) % 2 else 1
        total += sign * principal_det(K, superset)
    return sp.factor(total)


def event_probabilities(K: sp.Matrix, events: list[tuple[int, ...]]) -> list[sp.Expr]:
    return [event_probability(K, event) for event in events]


def affine_jets(
    K0: sp.Matrix, D: sp.Matrix, tau: sp.Symbol, events: list[tuple[int, ...]]
) -> tuple[list[sp.Expr], list[sp.Expr], list[sp.Expr]]:
    ps = event_probabilities(K0 + tau * D, events)
    p0 = [sp.factor(p.subs(tau, 0)) for p in ps]
    p1 = [sp.factor(sp.diff(p, tau).subs(tau, 0)) for p in ps]
    p2 = [sp.factor(sp.diff(p, tau, 2).subs(tau, 0)) for p in ps]
    no_float_atoms(p0 + p1 + p2, "affine jets")
    return p0, p1, p2


def membership(event: tuple[int, ...], n: int) -> tuple[int, ...]:
    event_set = set(event)
    return tuple(1 if i in event_set else 0 for i in range(n))


def matrix_entries(
    expr: sp.Expr, variables: list[sp.Symbol]
) -> list[list[str]]:
    poly = sp.Poly(sp.expand(expr), *variables)
    rows: list[list[str]] = []
    for vi in variables:
        row: list[str] = []
        for vj in variables:
            coeff = poly.coeff_monomial(vi * vj)
            if vi != vj:
                coeff = coeff / 2
            row.append(str(sp.factor(coeff)))
        rows.append(row)
    return rows


def source_file(rel: str, source_round2: Path) -> str:
    return str((source_round2 / rel).as_posix())


def replay_author_script(source_round2: Path) -> dict[str, Any]:
    script = source_round2 / "code" / "verify_symbolic.py"
    if not script.exists():
        raise FileNotFoundError(script)
    started = time.time()
    proc = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(source_round2),
        text=True,
        capture_output=True,
        timeout=1800,
        check=False,
    )
    return {
        "status": "PASS" if proc.returncode == 0 else "FAIL",
        "returncode": proc.returncode,
        "duration_seconds": round(time.time() - started, 6),
        "stdout": proc.stdout.splitlines(),
        "stderr": proc.stderr.splitlines(),
        "source_lines": [
            "README.md:21-31",
            "code/verify_symbolic.py:329-335",
            "outputs/verify_symbolic.txt:1-6",
        ],
    }


def check_strong_family() -> dict[str, Any]:
    tau = sp.symbols("tau", real=True)
    k = sp.symbols("k", real=True, nonzero=True)
    d1, d2, d3, h12, h13, h23 = sp.symbols(
        "d1 d2 d3 h12 h13 h23", real=True
    )
    K0 = sp.Matrix(
        [
            [sp.Rational(1, 2), 0, k],
            [0, sp.Rational(1, 2), k],
            [k, k, sp.Rational(1, 2)],
        ]
    )
    D = sp.Matrix([[d1, h12, h13], [h12, d2, h23], [h13, h23, d3]])
    p0, p1, p2 = affine_jets(K0, D, tau, EVENTS_3)

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
    for label, got, want in zip(EVENT_LABELS_3, p0, expected_p0):
        exact_zero(got - want, f"R2-T1 event probability {label}")
    exact_zero(sum(p0) - 1, "R2-T1 total probability")
    exact_zero(sum(p1), "R2-T1 total first derivative")
    exact_zero(sum(p2), "R2-T1 total second derivative")

    P, Delta, Z, R, H, N = sp.symbols("P Delta Z R H N", real=True)
    coordinate_sub = {
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
    for label, got, want in zip(EVENT_LABELS_3, p1, expected_4p1):
        exact_zero(4 * got.subs(coordinate_sub) - want, f"R2-T1 first jet {label}")

    group_minus = sp.factor((p2[0] + p2[7]).subs(coordinate_sub))
    group_plus = sp.factor((p2[3] + p2[4]).subs(coordinate_sub))
    group_zero = sp.factor(sum(p2[i] for i in (1, 2, 5, 6)).subs(coordinate_sub))
    exact_zero(
        group_minus
        + (Delta**2 + 2 * H**2 + 2 * N**2 - P**2 - 4 * P * Z + 4 * R**2)
        / 2,
        "R2-T1 p'' group A_-",
    )
    exact_zero(
        group_plus
        + (Delta**2 - 2 * H**2 - 2 * N**2 - P**2 + 4 * P * Z + 4 * R**2)
        / 2,
        "R2-T1 p'' group A_+",
    )
    exact_zero(
        group_zero - (Delta**2 - P**2 + 4 * R**2),
        "R2-T1 p'' group A_0",
    )

    fisher = sp.factor(sum((pp.subs(coordinate_sub)) ** 2 / p for pp, p in zip(p1, p0)))
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
    exact_zero(fisher - fisher_expected.subs(s, s_k), "R2-T1 full Fisher")

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
    exact_zero(acceleration_mg - acceleration_expected, "R2-T1 acceleration")

    G = Fmat + sp.Matrix([[m / 2, -g, 0], [-g, 0, 0], [0, 0, -2 * m]])
    combined_expected = (
        (vec.T * G * vec)[0]
        + (g + 4 * s / Ds) * H**2
        + (2 - m / 2) * Delta**2
        + (g + 4 * s) * N**2
    )
    exact_zero(
        fisher_expected + acceleration_expected - combined_expected,
        "R2-T1 combined G/scalar block",
    )

    return {
        "events_checked": EVENT_LABELS_3,
        "event_probabilities": [str(sp.factor(x)) for x in expected_p0],
        "fisher_block": matrix_entries((vec.T * Fmat * vec)[0], [P, Z, R]),
        "acceleration_group_sums": {
            "A_minus": str(sp.factor(group_minus)),
            "A_plus": str(sp.factor(group_plus)),
            "A_0": str(sp.factor(group_zero)),
        },
        "source_lines": [
            "frozen_statement.md:7-25",
            "frozen_statement.md:27-59",
            "proof.md:22-50",
            "proof.md:52-137",
            "proof.md:139-213",
        ],
    }


def check_strong_family_positivity_certificate() -> dict[str, Any]:
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
            exact_zero(Gp[i, j] - Gp_expected[i, j], f"R2-T1 G' entry {i},{j}")
    minor1 = sp.factor(Gp[0, 0])
    minor2 = sp.factor(Gp[:2, :2].det())
    minor3 = sp.factor(Gp.det())
    exact_zero(minor1 - s * (s**4 - s**2 + 1) / Ds**2, "R2-T1 G' minor 1")
    exact_zero(minor2 - s**2 * (s**4 - s**2 + 4) / Ds**3, "R2-T1 G' minor 2")
    exact_zero(minor3 - 48 * s**3 / Ds**3, "R2-T1 G' determinant")
    G0 = sp.Matrix([[sp.limit(G[i, j], s, 0, dir="+") for j in range(3)] for i in range(3)])
    exact_zero(G0[0, 0] - 2, "R2-T1 G0[0,0]")
    exact_zero(G0[1, 1] - 4, "R2-T1 G0[1,1]")
    exact_zero(G0[2, 2], "R2-T1 G0[2,2]")
    for i, j in ((0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)):
        exact_zero(G0[i, j], f"R2-T1 G0 off diagonal {i},{j}")

    q = sp.symbols("q", positive=True)
    exact_zero(
        sp.diff(q - 1 / q - 2 * sp.log(q), q) - (q - 1) ** 2 / q**2,
        "log inequality derivative identity",
    )

    return {
        "G0": [[str(G0[i, j]) for j in range(3)] for i in range(3)],
        "Gprime_leading_minors": [str(minor1), str(minor2), str(minor3)],
        "positive_interval_reasoning": [
            "0<s<1 gives Ds=(1-s)(1+s)>0",
            "s^4-s^2+1=(s^2-1/2)^2+3/4>0",
            "s^4-s^2+4>0",
            "s^4-3*s^2+3=(s^2-3/2)^2+3/4>0",
        ],
        "source_lines": ["proof.md:215-283"],
    }


def check_strong_family_sigma_conjugation() -> dict[str, Any]:
    tau = sp.symbols("tau", real=True)
    k = sp.symbols("k", real=True, nonzero=True)
    d1, d2, d3, h12, h13, h23 = sp.symbols(
        "d1 d2 d3 h12 h13 h23", real=True
    )
    D = sp.Matrix([[d1, h12, h13], [h12, d2, h23], [h13, h23, d3]])
    K_plus = sp.Matrix(
        [[sp.Rational(1, 2), 0, k], [0, sp.Rational(1, 2), k], [k, k, sp.Rational(1, 2)]]
    )
    K_minus = sp.Matrix(
        [[sp.Rational(1, 2), 0, k], [0, sp.Rational(1, 2), -k], [k, -k, sp.Rational(1, 2)]]
    )
    S = sp.diag(1, -1, 1)
    D_conj = S * D * S
    plus_jets = affine_jets(K_plus, D_conj, tau, EVENTS_3)
    minus_jets = affine_jets(K_minus, D, tau, EVENTS_3)
    for order, (plus, minus) in enumerate(zip(plus_jets, minus_jets)):
        for label, got, want in zip(EVENT_LABELS_3, minus, plus):
            exact_zero(got - want, f"sigma=-1 conjugation jet {order} event {label}")
    return {
        "direction_map": {
            "d1": "d1",
            "d2": "d2",
            "d3": "d3",
            "h12": "-h12",
            "h13": "h13",
            "h23": "-h23",
        },
        "jets_compared": ["p", "p'", "p''"],
        "source_lines": ["frozen_statement.md:38-48", "proof.md:281-283"],
    }


def check_strong_family_rational_witness() -> dict[str, Any]:
    k = sp.Rational(1, 3)
    K = sp.Matrix(
        [[sp.Rational(1, 2), 0, k], [0, sp.Rational(1, 2), k], [k, k, sp.Rational(1, 2)]]
    )
    I = sp.eye(3)
    ps = event_probabilities(K, EVENTS_3)
    expected = [
        sp.Rational(1, 72),
        sp.Rational(1, 8),
        sp.Rational(1, 8),
        sp.Rational(17, 72),
        sp.Rational(17, 72),
        sp.Rational(1, 8),
        sp.Rational(1, 8),
        sp.Rational(1, 72),
    ]
    for label, got, want in zip(EVENT_LABELS_3, ps, expected):
        exact_zero(got - want, f"k=1/3 witness event {label}")
    det_k = sp.factor(K.det())
    det_i_minus_k = sp.factor((I - K).det())
    exact_zero(det_k - sp.Rational(1, 72), "k=1/3 det K")
    exact_zero(det_i_minus_k - sp.Rational(1, 72), "k=1/3 det I-K")
    exact_zero(8 * k**2 - sp.Rational(8, 9), "k=1/3 s")
    exact_zero(4 * k - sp.Rational(4, 3), "k=1/3 normalized edge")
    exact_zero(8 * sp.Rational(1, 16) ** 2 - sp.Rational(1, 32), "old weak-domain s")
    return {
        "k": "1/3",
        "s": "8/9",
        "event_probabilities": [str(x) for x in ps],
        "det_K": str(det_k),
        "det_I_minus_K": str(det_i_minus_k),
        "old_domain": {"abs_kappa_bound": "1/16", "s_bound": "1/32"},
        "source_lines": [
            "frozen_statement.md:61-67",
            "proof.md:285-314",
            "inputs/exact_inputs.json:4-17",
        ],
    }


def check_two_point_conditional_entropy_algebra() -> dict[str, Any]:
    y, w, e, U, V = sp.symbols("y w e U V", nonzero=True)
    r = y * (1 - y)
    d = y * U + (1 - y) * V - w * e
    qprime = (1 - 2 * y) * e * w + r * (V - U)
    delta_from_affine = d * e - qprime**2 / (4 * r * w)
    delta_claim = e * (U + V) / 2 - w * e**2 / (4 * r) - r * (V - U) ** 2 / (4 * w)
    exact_zero(delta_from_affine - delta_claim, "two-point delta identity")

    Au, Av, L = sp.symbols("Au Av L", positive=True)
    M = sp.Matrix([[y * Au, -L * r / w], [-L * r / w, (1 - y) * Av]])
    exact_zero(M.det() - (r * Au * Av - L**2 * r**2 / w**2), "two-point matrix determinant")
    q = sp.symbols("q", positive=True)
    exact_zero(
        sp.diff(q - 1 / q - 2 * sp.log(q), q) - (q - 1) ** 2 / q**2,
        "two-point log inequality derivative",
    )
    return {
        "checked_identities": ["delta formula", "2x2 determinant", "log-inequality derivative"],
        "analytic_sign_step_not_mechanized": "For q>=1, q-1/q-2log(q) has nonnegative derivative and vanishes at q=1.",
        "source_lines": ["frozen_statement.md:89-95", "proof.md:316-463"],
    }


def check_block_factorization() -> dict[str, Any]:
    tau = sp.symbols("tau", real=True)
    x, y, z0, a = sp.symbols("x y z a", real=True)
    d1, d2, d3, h12, h13, h23 = sp.symbols(
        "d1 d2 d3 h12 h13 h23", real=True
    )
    K0 = sp.Matrix([[x, a, 0], [a, y, 0], [0, 0, z0]])
    D = sp.Matrix([[d1, h12, h13], [h12, d2, h23], [h13, h23, d3]])
    p0, p1, p2 = affine_jets(K0, D, tau, EVENTS_3)

    A0 = sp.Matrix([[x, a], [a, y]])
    E = sp.Matrix([[d1, h12], [h12, d2]])
    u0, u1, u2 = affine_jets(A0, E, tau, EVENTS_2)
    w0 = [1 - z0, z0]
    w1 = [-d3, d3]
    event_to_pair_single = [(EVENTS_2.index(tuple(i for i in ev if i < 2)), 1 if 2 in ev else 0) for ev in EVENTS_3]

    for idx, (pair_idx, single_idx) in enumerate(event_to_pair_single):
        label = EVENT_LABELS_3[idx]
        exact_zero(p0[idx] - u0[pair_idx] * w0[single_idx], f"block p {label}")
        exact_zero(
            p1[idx] - (u1[pair_idx] * w0[single_idx] + u0[pair_idx] * w1[single_idx]),
            f"block p' {label}",
        )

    for pair_idx, pair_label in enumerate(EVENT_LABELS_2):
        inds = [i for i, (pidx, _) in enumerate(event_to_pair_single) if pidx == pair_idx]
        exact_zero(sum(p2[i] for i in inds) - u2[pair_idx], f"block p'' pair marginal {pair_label}")
    for single_idx, single_label in enumerate(["not3", "3"]):
        inds = [i for i, (_, sidx) in enumerate(event_to_pair_single) if sidx == single_idx]
        exact_zero(sum(p2[i] for i in inds), f"block p'' singleton marginal {single_label}")

    fisher_full = sum(pp**2 / p for pp, p in zip(p1, p0))
    fisher_pair = sum(pp**2 / u for pp, u in zip(u1, u0))
    fisher_single = d3**2 / (z0 * (1 - z0))
    exact_zero(fisher_full - fisher_pair - fisher_single, "block Fisher factorization")

    lu = sp.symbols("lu0 lu1 lu2 lu12", real=True)
    lw0, lw1 = sp.symbols("lw0 lw1", real=True)
    accel_full = sp.Integer(0)
    for idx, (pair_idx, single_idx) in enumerate(event_to_pair_single):
        accel_full += p2[idx] * (lu[pair_idx] + (lw1 if single_idx else lw0))
    accel_pair = sum(u2[i] * lu[i] for i in range(4))
    exact_zero(sp.expand(accel_full - accel_pair), "block acceleration cancellation")

    normalized_edge = sp.Rational(49, 100) / sp.sqrt(sp.Rational(1, 4) * sp.Rational(1, 4))
    exact_zero(normalized_edge - sp.Rational(49, 25), "block input normalized edge convention")
    return {
        "events_checked": EVENT_LABELS_3,
        "identities": ["p factorization", "p' factorization", "p'' marginal sums", "Fisher split", "acceleration cancellation"],
        "source_lines": [
            "frozen_statement.md:69-96",
            "proof.md:465-517",
            "inputs/exact_inputs.json:19-27",
        ],
    }


def check_missing_edge_transform() -> dict[str, Any]:
    tau = sp.symbols("tau", real=True)
    x, y, z0, b, c = sp.symbols("x y z b c", real=True, nonzero=True)
    d1, d2, d3, h12, h13, h23 = sp.symbols(
        "d1 d2 d3 h12 h13 h23", real=True
    )
    K0 = sp.Matrix([[x, 0, b], [0, y, c], [b, c, z0]])
    D = sp.Matrix([[d1, h12, h13], [h12, d2, h23], [h13, h23, d3]])
    p0, p1, _p2 = affine_jets(K0, D, tau, EVENTS_3)

    v1 = x * (1 - x)
    v2 = y * (1 - y)
    event_index = {membership(ev, 3): idx for idx, ev in enumerate(EVENTS_3)}
    T_claims: dict[tuple[int, int], sp.Expr] = {}
    t_claims: dict[tuple[int, int], sp.Expr] = {}
    Pij: dict[tuple[int, int], sp.Expr] = {}
    Pij_prime: dict[tuple[int, int], sp.Expr] = {}

    for i, j in ((0, 0), (1, 0), (0, 1), (1, 1)):
        idx0 = event_index[(i, j, 0)]
        idx1 = event_index[(i, j, 1)]
        phi = (i - x) / v1
        psi = (j - y) / v2
        P = (x if i else 1 - x) * (y if j else 1 - y)
        Pp = P * (d1 * phi + d2 * psi)
        t_claim = z0 - b**2 * phi - c**2 * psi
        T_claim = (
            d3
            + b**2 * d1 * phi**2
            + c**2 * d2 * psi**2
            - 2 * b * h13 * phi
            - 2 * c * h23 * psi
            + 2 * b * c * h12 * phi * psi
        )
        exact_zero(p0[idx0] + p0[idx1] - P, f"missing-edge marginal P_{i}{j}")
        exact_zero(p0[idx0] - P * (1 - t_claim), f"missing-edge event p {i}{j}0")
        exact_zero(p0[idx1] - P * t_claim, f"missing-edge event p {i}{j}1")
        exact_zero(p1[idx0] + p1[idx1] - Pp, f"missing-edge marginal derivative P_{i}{j}")
        exact_zero(p1[idx0] - (Pp * (1 - t_claim) - P * T_claim), f"missing-edge event p' {i}{j}0")
        exact_zero(p1[idx1] - (Pp * t_claim + P * T_claim), f"missing-edge event p' {i}{j}1")
        T_claims[(i, j)] = T_claim
        t_claims[(i, j)] = t_claim
        Pij[(i, j)] = P
        Pij_prime[(i, j)] = Pp

    directions = [d1, d2, d3, h12, h13, h23]
    outputs = [d1, d2] + [T_claims[pair] for pair in ((0, 0), (1, 0), (0, 1), (1, 1))]
    J = sp.Matrix([[sp.diff(out, var) for var in directions] for out in outputs])
    exact_zero(J.det() - 8 * b**2 * c**2 / (v1**2 * v2**2), "missing-edge Jacobian")

    T00, T10, T01, T11 = sp.symbols("T00 T10 T01 T11", real=True)
    barT = (
        (1 - x) * (1 - y) * T00
        + x * (1 - y) * T10
        + (1 - x) * y * T01
        + x * y * T11
    )
    A1 = (1 - y) * (T10 - T00) + y * (T11 - T01)
    A2 = (1 - x) * (T01 - T00) + x * (T11 - T10)
    Delta12T = T11 - T10 - T01 + T00
    inverse_sub = {
        h12: v1 * v2 * Delta12T / (2 * b * c),
        h13: b * (1 - 2 * x) * d1 / (2 * v1) - v1 * A1 / (2 * b),
        h23: c * (1 - 2 * y) * d2 / (2 * v2) - v2 * A2 / (2 * c),
        d3: barT - b**2 * d1 / v1 - c**2 * d2 / v2,
    }
    target_Ts = {(0, 0): T00, (1, 0): T10, (0, 1): T01, (1, 1): T11}
    for pair, expr in T_claims.items():
        exact_zero(expr.subs(inverse_sub) - target_Ts[pair], f"missing-edge inverse T_{pair[0]}{pair[1]}")

    for pair in ((0, 0), (1, 0), (0, 1), (1, 1)):
        P = Pij[pair]
        Pp = Pij_prime[pair]
        t = t_claims[pair]
        T = T_claims[pair]
        pair_fisher = (Pp * (1 - t) - P * T) ** 2 / (P * (1 - t))
        pair_fisher += (Pp * t + P * T) ** 2 / (P * t)
        pair_expected = Pp**2 / P + P * T**2 / (t * (1 - t))
        exact_zero(pair_fisher - pair_expected, f"missing-edge conditional Fisher pair {pair[0]}{pair[1]}")
    marginal_fisher = sum(Pij_prime[pair] ** 2 / Pij[pair] for pair in ((0, 0), (1, 0), (0, 1), (1, 1)))
    exact_zero(
        marginal_fisher - d1**2 / v1 - d2**2 / v2,
        "missing-edge Bernoulli marginal Fisher",
    )

    return {
        "conditional_events": ["00", "10", "01", "11"],
        "jacobian": "8*b**2*c**2/(x**2*y**2*(x - 1)**2*(y - 1)**2)",
        "inverse_checked": ["h12", "h13", "h23", "d3"],
        "fisher_expression_checked": True,
        "source_lines": ["frozen_statement.md:108-119", "proof.md:519-612"],
    }


def atomic_json(path: Path, obj: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    os.replace(tmp, path)


def run_check(
    evidence: dict[str, Any],
    output_path: Path,
    name: str,
    func: Callable[[], dict[str, Any]],
) -> None:
    started = time.time()
    record: dict[str, Any] = {"name": name, "status": "RUNNING", "started_at_unix": started}
    evidence["checks"].append(record)
    atomic_json(output_path, evidence)
    try:
        details = func()
        record.update(
            {
                "status": "PASS",
                "duration_seconds": round(time.time() - started, 6),
                "details": details,
            }
        )
    except Exception as exc:  # noqa: BLE001
        record.update(
            {
                "status": "FAIL",
                "duration_seconds": round(time.time() - started, 6),
                "error": repr(exc),
                "traceback": traceback.format_exc().splitlines(),
            }
        )
    atomic_json(output_path, evidence)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-round2", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    started = time.time()
    source_round2 = args.source_round2.resolve()
    evidence: dict[str, Any] = {
        "task": "C2 verification3 PR41 / issue 45",
        "status": "RUNNING",
        "started_at_unix": started,
        "pid": os.getpid(),
        "argv": sys.argv,
        "source_round2": source_round2.as_posix(),
        "frozen_pr_commit": "6fd61dcd299417fc3a4eab3af682c03dd816b670",
        "domain": {
            "entropy": "complete-configuration Shannon entropy for finite DPPs",
            "kernel": "real symmetric 3x3 strict contraction",
            "directions": "all six real symmetric affine directions",
        },
        "algorithm": [
            "Build principal-minor determinants for every subset.",
            "Apply Mobius inclusion-exclusion for all full events.",
            "Differentiate p(K+tD) at t=0 for first and second jets.",
            "Compare exact Fisher, acceleration, block, and coordinate identities.",
            "Use SymPy exact simplification only; no floating point proof steps.",
        ],
        "runtime": {
            "python": sys.version,
            "platform": platform.platform(),
            "sympy": sp.__version__,
            "env_thread_limits": {
                key: os.environ.get(key)
                for key in [
                    "OMP_NUM_THREADS",
                    "OPENBLAS_NUM_THREADS",
                    "MKL_NUM_THREADS",
                    "NUMEXPR_NUM_THREADS",
                    "VECLIB_MAXIMUM_THREADS",
                    "PYTHONHASHSEED",
                ]
            },
        },
        "dependencies": {"sympy": sp.__version__},
        "source_files": {
            "frozen_statement": source_file("frozen_statement.md", source_round2),
            "handoff": source_file("HANDOFF.md", source_round2),
            "proof": source_file("proof.md", source_round2),
            "author_verifier": source_file("code/verify_symbolic.py", source_round2),
            "requirements": source_file("requirements.txt", source_round2),
            "inputs": source_file("inputs/exact_inputs.json", source_round2),
        },
        "checks": [],
    }
    atomic_json(args.out, evidence)

    def replay() -> dict[str, Any]:
        result = replay_author_script(source_round2)
        if result["returncode"] != 0:
            raise CheckFailure(f"author replay failed with return code {result['returncode']}")
        return result

    checks: list[tuple[str, Callable[[], dict[str, Any]]]] = [
        ("author_script_replay_subprocess", replay),
        ("independent_strong_family_full_events_jets_fisher_acceleration", check_strong_family),
        ("independent_strong_family_G_certificate", check_strong_family_positivity_certificate),
        ("independent_sigma_minus_conjugation", check_strong_family_sigma_conjugation),
        ("independent_rational_strong_coupling_witness", check_strong_family_rational_witness),
        ("independent_two_point_conditional_entropy_algebra", check_two_point_conditional_entropy_algebra),
        ("independent_block_factorization", check_block_factorization),
        ("independent_missing_edge_transform_and_fisher", check_missing_edge_transform),
    ]
    for name, func in checks:
        run_check(evidence, args.out, name, func)

    failed = [check for check in evidence["checks"] if check["status"] != "PASS"]
    evidence["status"] = "FAIL" if failed else "PASS"
    evidence["duration_seconds"] = round(time.time() - started, 6)
    evidence["limitations"] = [
        "This is a bounded exact computational review, not a C1 analytic review of the full theorem.",
        "It verifies stated finite symbolic identities and the recorded one-dimensional positivity certificate.",
        "It does not prove the unresolved general connected missing-edge 6x6 inequality.",
        "It does not certify novelty.",
        "It is not a proof-assistant formalization.",
    ]
    atomic_json(args.out, evidence)
    print(f"STATUS {evidence['status']}")
    print(f"EVIDENCE {args.out}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
