#!/usr/bin/env python3
from __future__ import annotations

import os
import platform
import sys
import time

import sympy as sp


def log(message: str) -> None:
    print(message, flush=True)


def exact_zero(expr: sp.Expr, label: str) -> None:
    got = sp.factor(sp.cancel(sp.together(sp.simplify(expr))))
    if got != 0:
        raise AssertionError(f"{label}: nonzero remainder {got}")
    log(f"OK {label}")


def check_gs_derivative_certificate() -> None:
    log("PHASE gs-derivative start")
    s = sp.symbols("s", positive=True)
    ds = 1 - s**2
    m = sp.log(1 - s**2)
    g = sp.log((1 + s) / (1 - s))
    gs = sp.Matrix(
        [
            [
                m / 2 + (4 - 2 * s**2 - s**4) / (2 * ds),
                s * (2 - s**2) / ds - g,
                s**4 / ds,
            ],
            [
                s * (2 - s**2) / ds - g,
                2 * (2 - s**2) / ds,
                2 * s**3 / ds,
            ],
            [
                s**4 / ds,
                2 * s**3 / ds,
                -2 * m + 2 * s**2 * (2 - s**2) / ds,
            ],
        ]
    )
    gp = gs.diff(s)
    gp_expected = sp.Matrix(
        [
            [s * (s**4 - s**2 + 1), s**2 * (s**2 + 1), 2 * s**3 * (2 - s**2)],
            [s**2 * (s**2 + 1), 4 * s, 2 * s**2 * (3 - s**2)],
            [
                2 * s**3 * (2 - s**2),
                2 * s**2 * (3 - s**2),
                4 * s * (s**4 - 3 * s**2 + 3),
            ],
        ]
    ) / ds**2
    for row in range(3):
        for col in range(3):
            exact_zero(gp[row, col] - gp_expected[row, col], f"Gp entry {row},{col}")
    exact_zero(gp[0, 0] - s * (s**4 - s**2 + 1) / ds**2, "Delta1(Gp)")
    exact_zero(gp[:2, :2].det() - s**2 * (s**4 - s**2 + 4) / ds**3, "Delta2(Gp)")
    exact_zero(gp.det() - 48 * s**3 / ds**3, "det(Gp)")
    g0 = sp.Matrix([[sp.limit(gs[i, j], s, 0, dir="+") for j in range(3)] for i in range(3)])
    if g0 != sp.diag(2, 4, 0):
        raise AssertionError(f"G0 mismatch: {g0}")
    log("OK G0 diag(2,4,0)")
    log("PHASE gs-derivative done")


def check_two_point_conditional_certificate() -> None:
    log("PHASE two-point-conditional start")
    y, w, e, u_dir, v_dir = sp.symbols("y w e U V", nonzero=True)
    r = y * (1 - y)
    d = y * u_dir + (1 - y) * v_dir - w * e
    qprime = (1 - 2 * y) * e * w + r * (v_dir - u_dir)
    delta_from_affine = d * e - qprime**2 / (4 * r * w)
    delta_claim = (
        e * (u_dir + v_dir) / 2
        - w * e**2 / (4 * r)
        - r * (v_dir - u_dir) ** 2 / (4 * w)
    )
    exact_zero(delta_from_affine - delta_claim, "delta identity")

    L, au, av = sp.symbols("L Au Av", positive=True)
    reduced_fisher = y * au * u_dir**2 + (1 - y) * av * v_dir**2
    direct_form = reduced_fisher - 2 * L * delta_claim
    matrix = sp.Matrix([[y * au, -L * r / w], [-L * r / w, (1 - y) * av]])
    square = L * w * (e - r * (u_dir + v_dir) / w) ** 2 / (2 * r)
    completed = square + (sp.Matrix([[u_dir, v_dir]]) * matrix * sp.Matrix([u_dir, v_dir]))[0]
    exact_zero(direct_form - completed, "square completion")
    exact_zero(matrix.det() - (r * au * av - L**2 * r**2 / w**2), "2x2 determinant")

    q = sp.symbols("q", positive=True)
    inequality_gap = q - 1 / q - 2 * sp.log(q)
    exact_zero(sp.diff(inequality_gap, q) - (q - 1) ** 2 / q**2, "log-inequality derivative")
    exact_zero(inequality_gap.subs(q, 1), "log-inequality base value")
    log("PHASE two-point-conditional done")


def main() -> None:
    start = time.time()
    log(f"PID {os.getpid()}")
    log(f"Python {sys.version.split()[0]}")
    log(f"platform {platform.platform()}")
    log(f"sympy {sp.__version__}")
    check_gs_derivative_certificate()
    check_two_point_conditional_certificate()
    log(f"EXIT 0 elapsed_seconds {time.time() - start:.3f}")


if __name__ == "__main__":
    main()
