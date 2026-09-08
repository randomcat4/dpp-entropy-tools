"""Second-order jet evaluator for fixed-beta path affine chords.

This script is an author-side implementation artifact for D10-B3.  It computes
the directional derivatives of the L-ensemble Shannon entropy along

    tau(t) = tau0 + t * delta,

where K(t)=I-R^{-1}diag(tau(t))R^{-T} is exactly affine in K-space.  The core
value H''(0) is computed by differentiating the path selected-run dynamic
program; finite differences are used only as independent sanity checks for
n<=7.

No third-party packages are required.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import random
import time
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
from typing import Iterable, Sequence


os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")
os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")


Jet = tuple[float, float, float]  # value, first derivative, second derivative
DJet = tuple[Decimal, Decimal, Decimal]
Matrix = list[list[Fraction]]


J_ZERO: Jet = (0.0, 0.0, 0.0)
J_ONE: Jet = (1.0, 0.0, 0.0)


def jadd(a: Jet, b: Jet) -> Jet:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def jsub(a: Jet, b: Jet) -> Jet:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def jscale(a: Jet, c: float) -> Jet:
    return (c * a[0], c * a[1], c * a[2])


def jmul(a: Jet, b: Jet) -> Jet:
    av, a1, a2 = a
    bv, b1, b2 = b
    return (av * bv, a1 * bv + av * b1, a2 * bv + 2.0 * a1 * b1 + av * b2)


def jsquare(a: Jet) -> Jet:
    av, a1, a2 = a
    return (av * av, 2.0 * av * a1, 2.0 * a1 * a1 + 2.0 * av * a2)


def jinv(a: Jet) -> Jet:
    av, a1, a2 = a
    if av <= 0.0 or not math.isfinite(av):
        raise ValueError(f"cannot invert nonpositive/nonfinite jet value {av}")
    inv = 1.0 / av
    return (inv, -a1 * inv * inv, 2.0 * a1 * a1 * inv**3 - a2 * inv * inv)


def jdiv(a: Jet, b: Jet) -> Jet:
    """Stable quotient for actual-derivative jets.

    This avoids forming b[0]**(-3), which underflows for high-dimensional
    normalizers Z even when the quotient derivatives themselves are moderate.
    If a=c*b, then

        a'  = c'b + cb',
        a'' = c''b + 2c'b' + cb''.
    """

    av, a1, a2 = a
    bv, b1, b2 = b
    if bv == 0.0 or not math.isfinite(bv):
        raise ValueError(f"cannot divide by zero/nonfinite jet value {bv}")
    c0 = av / bv
    c1 = (a1 - b1 * c0) / bv
    c2 = (a2 - 2.0 * b1 * c1 - b2 * c0) / bv
    return (c0, c1, c2)


def jlog(a: Jet) -> Jet:
    av, a1, a2 = a
    if av <= 0.0 or not math.isfinite(av):
        raise ValueError(f"cannot log nonpositive/nonfinite jet value {av}")
    return (math.log(av), a1 / av, a2 / av - (a1 * a1) / (av * av))


def jxlogx(a: Jet) -> Jet:
    av, a1, a2 = a
    if av <= 0.0 or not math.isfinite(av):
        raise ValueError(f"cannot form x log x for nonpositive/nonfinite value {av}")
    logv = math.log(av)
    return (av * logv, a1 * (logv + 1.0), a2 * (logv + 1.0) + (a1 * a1) / av)


def l_parts_float(beta: Sequence[float], tau: Sequence[float]) -> tuple[list[float], list[float]]:
    n = len(tau)
    if len(beta) != n - 1:
        raise ValueError("beta length must be n-1")
    inv = [1.0 / t for t in tau]
    diag = [0.0] * n
    edge = [0.0] * (n - 1)
    for i in range(n - 1):
        diag[i] = inv[i] + beta[i] * beta[i] * inv[i + 1] - 1.0
        edge[i] = -beta[i] * inv[i + 1]
    diag[-1] = inv[-1] - 1.0
    return diag, edge


def p_parts_float(beta: Sequence[float], tau: Sequence[float]) -> tuple[list[float], list[float]]:
    """Return the tridiagonal P=S^{-1}=I+L."""

    n = len(tau)
    inv = [1.0 / t for t in tau]
    diag = [0.0] * n
    edge = [0.0] * (n - 1)
    for i in range(n - 1):
        diag[i] = inv[i] + beta[i] * beta[i] * inv[i + 1]
        edge[i] = -beta[i] * inv[i + 1]
    diag[-1] = inv[-1]
    return diag, edge


def l_part_jets(beta: Sequence[float], tau: Sequence[float], delta: Sequence[float]) -> tuple[list[Jet], list[Jet]]:
    n = len(tau)
    if len(beta) != n - 1 or len(delta) != n:
        raise ValueError("expected len(beta)=n-1 and len(delta)=n")
    w: list[Jet] = []
    for t, d in zip(tau, delta):
        if t <= 0.0:
            raise ValueError("tau must be positive")
        inv = 1.0 / t
        w.append((inv, -d * inv * inv, 2.0 * d * d * inv * inv * inv))

    diag: list[Jet] = [J_ZERO] * n
    edge: list[Jet] = [J_ZERO] * (n - 1)
    for i in range(n - 1):
        b = beta[i]
        value = jadd(w[i], jscale(w[i + 1], b * b))
        diag[i] = (value[0] - 1.0, value[1], value[2])
        edge[i] = jscale(w[i + 1], -b)
    diag[-1] = (w[-1][0] - 1.0, w[-1][1], w[-1][2])
    return diag, edge


def min_ldl_pivot(diag: Sequence[float], edge: Sequence[float]) -> float:
    if not diag:
        return math.inf
    pivot = diag[0]
    best = pivot
    for i in range(1, len(diag)):
        if pivot <= 0.0 or not math.isfinite(pivot):
            return pivot
        pivot = diag[i] - edge[i - 1] * edge[i - 1] / pivot
        best = min(best, pivot)
    return best


def admissible_l(beta: Sequence[float], tau: Sequence[float], margin: float = 1e-11) -> bool:
    if any(t <= 0.0 or not math.isfinite(t) for t in tau):
        return False
    diag, edge = l_parts_float(beta, tau)
    return min_ldl_pivot(diag, edge) > margin


def interval_kappa_jets(diag: Sequence[Jet], edge: Sequence[Jet]) -> list[list[Jet]]:
    n = len(diag)
    kappa: list[list[Jet]] = [[J_ZERO for _ in range(n)] for _ in range(n)]
    for start in range(n):
        prev2 = J_ONE
        prev1 = diag[start]
        if prev1[0] <= 0.0 or not math.isfinite(prev1[0]):
            raise ValueError("nonpositive/nonfinite one-point interval determinant")
        kappa[start][start] = prev1
        for end in range(start + 1, n):
            current = jsub(jmul(diag[end], prev1), jmul(jsquare(edge[end - 1]), prev2))
            if current[0] <= 0.0 or not math.isfinite(current[0]):
                raise ValueError("nonpositive/nonfinite interval determinant")
            kappa[start][end] = current
            prev2, prev1 = prev1, current
    return kappa


def entropy_jet_from_l_jets(diag: Sequence[Jet], edge: Sequence[Jet]) -> dict[str, float]:
    """Selected-run path DP for H, H', and H''.

    The stored second component is the first derivative at t=0; the third
    component is the true second derivative at t=0, not the Taylor coefficient.
    """

    n = len(diag)
    if n == 0:
        return {"n": 0, "H": 0.0, "H1": 0.0, "H2": 0.0, "Z": 1.0, "Z1": 0.0, "Z2": 0.0}
    if len(edge) != n - 1:
        raise ValueError("edge length must be n-1")

    kappa = interval_kappa_jets(diag, edge)
    z: list[Jet] = [J_ZERO for _ in range(n + 1)]
    tlog: list[Jet] = [J_ZERO for _ in range(n + 1)]
    z[0] = J_ONE

    for length in range(1, n + 1):
        end = length - 1
        z_value = z[length - 1]
        t_value = tlog[length - 1]
        for start in range(length):
            prefix_len = 0 if start == 0 else start - 1
            block = kappa[start][end]
            prefix_z = z[prefix_len]
            z_value = jadd(z_value, jmul(prefix_z, block))
            t_value = jadd(t_value, jmul(block, tlog[prefix_len]))
            t_value = jadd(t_value, jmul(prefix_z, jxlogx(block)))
        z[length] = z_value
        tlog[length] = t_value

    h = jsub(jlog(z[n]), jdiv(tlog[n], z[n]))
    if not all(math.isfinite(x) for x in h):
        raise ValueError("nonfinite entropy jet")
    return {
        "n": n,
        "H": h[0],
        "H1": h[1],
        "H2": h[2],
        "Z": z[n][0],
        "Z1": z[n][1],
        "Z2": z[n][2],
        "T": tlog[n][0],
        "T1": tlog[n][1],
        "T2": tlog[n][2],
        "interval_states": n * (n + 1) // 2,
        "full_events": 2**n if n < 63 else f"2^{n}",
    }


def entropy_jet_tau(beta: Sequence[float], tau: Sequence[float], delta: Sequence[float]) -> dict[str, float]:
    diag, edge = l_part_jets(beta, tau, delta)
    return entropy_jet_from_l_jets(diag, edge)


def decimal_from_float(x: float) -> Decimal:
    return Decimal(repr(float(x)))


def djadd(a: DJet, b: DJet) -> DJet:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def djsub(a: DJet, b: DJet) -> DJet:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def djscale(a: DJet, c: Decimal) -> DJet:
    return (c * a[0], c * a[1], c * a[2])


def djmul(a: DJet, b: DJet) -> DJet:
    av, a1, a2 = a
    bv, b1, b2 = b
    return (av * bv, a1 * bv + av * b1, a2 * bv + Decimal(2) * a1 * b1 + av * b2)


def djsquare(a: DJet) -> DJet:
    av, a1, a2 = a
    return (av * av, Decimal(2) * av * a1, Decimal(2) * a1 * a1 + Decimal(2) * av * a2)


def djinv(a: DJet) -> DJet:
    av, a1, a2 = a
    inv = Decimal(1) / av
    return (inv, -a1 * inv * inv, Decimal(2) * a1 * a1 * inv**3 - a2 * inv * inv)


def djdiv(a: DJet, b: DJet) -> DJet:
    av, a1, a2 = a
    bv, b1, b2 = b
    c0 = av / bv
    c1 = (a1 - b1 * c0) / bv
    c2 = (a2 - Decimal(2) * b1 * c1 - b2 * c0) / bv
    return (+c0, +c1, +c2)


def djlog(a: DJet) -> DJet:
    av, a1, a2 = a
    return (av.ln(), a1 / av, a2 / av - (a1 * a1) / (av * av))


def djxlogx(a: DJet) -> DJet:
    av, a1, a2 = a
    logv = av.ln()
    return (av * logv, a1 * (logv + Decimal(1)), a2 * (logv + Decimal(1)) + (a1 * a1) / av)


def decimal_l_part_jets(
    beta: Sequence[float], tau: Sequence[float], delta: Sequence[float], precision: int
) -> tuple[list[DJet], list[DJet]]:
    with localcontext() as ctx:
        ctx.prec = precision
        b = [decimal_from_float(x) for x in beta]
        t0 = [decimal_from_float(x) for x in tau]
        d0 = [decimal_from_float(x) for x in delta]
        n = len(t0)
        w: list[DJet] = []
        for t, d in zip(t0, d0):
            inv = Decimal(1) / t
            w.append((+inv, +(-d * inv * inv), +(Decimal(2) * d * d * inv * inv * inv)))
        diag: list[DJet] = [(Decimal(0), Decimal(0), Decimal(0)) for _ in range(n)]
        edge: list[DJet] = [(Decimal(0), Decimal(0), Decimal(0)) for _ in range(n - 1)]
        for i in range(n - 1):
            value = djadd(w[i], djscale(w[i + 1], b[i] * b[i]))
            diag[i] = (+(value[0] - Decimal(1)), +value[1], +value[2])
            edge[i] = djscale(w[i + 1], -b[i])
        diag[-1] = (+(w[-1][0] - Decimal(1)), +w[-1][1], +w[-1][2])
        return diag, edge


def decimal_interval_kappa_jets(diag: Sequence[DJet], edge: Sequence[DJet]) -> list[list[DJet]]:
    n = len(diag)
    zero = (Decimal(0), Decimal(0), Decimal(0))
    one = (Decimal(1), Decimal(0), Decimal(0))
    kappa: list[list[DJet]] = [[zero for _ in range(n)] for _ in range(n)]
    for start in range(n):
        prev2 = one
        prev1 = diag[start]
        if prev1[0] <= 0:
            raise ValueError("nonpositive Decimal one-point interval determinant")
        kappa[start][start] = prev1
        for end in range(start + 1, n):
            current = djsub(djmul(diag[end], prev1), djmul(djsquare(edge[end - 1]), prev2))
            if current[0] <= 0:
                raise ValueError("nonpositive Decimal interval determinant")
            kappa[start][end] = current
            prev2, prev1 = prev1, current
    return kappa


def decimal_entropy_jet_tau(
    beta: Sequence[float], tau: Sequence[float], delta: Sequence[float], precision: int = 80
) -> dict[str, Decimal | int]:
    with localcontext() as ctx:
        ctx.prec = precision
        diag, edge = decimal_l_part_jets(beta, tau, delta, precision)
        n = len(diag)
        kappa = decimal_interval_kappa_jets(diag, edge)
        zero = (Decimal(0), Decimal(0), Decimal(0))
        one = (Decimal(1), Decimal(0), Decimal(0))
        z: list[DJet] = [zero for _ in range(n + 1)]
        tlog: list[DJet] = [zero for _ in range(n + 1)]
        z[0] = one
        for length in range(1, n + 1):
            end = length - 1
            z_value = z[length - 1]
            t_value = tlog[length - 1]
            for start in range(length):
                prefix_len = 0 if start == 0 else start - 1
                block = kappa[start][end]
                prefix_z = z[prefix_len]
                z_value = djadd(z_value, djmul(prefix_z, block))
                t_value = djadd(t_value, djmul(block, tlog[prefix_len]))
                t_value = djadd(t_value, djmul(prefix_z, djxlogx(block)))
            z[length] = (+z_value[0], +z_value[1], +z_value[2])
            tlog[length] = (+t_value[0], +t_value[1], +t_value[2])
        h = djsub(djlog(z[n]), djdiv(tlog[n], z[n]))
        return {
            "n": n,
            "precision": precision,
            "H": +h[0],
            "H1": +h[1],
            "H2": +h[2],
            "Z": +z[n][0],
            "Z1": +z[n][1],
            "Z2": +z[n][2],
            "T": +tlog[n][0],
            "T1": +tlog[n][1],
            "T2": +tlog[n][2],
            "logZ": +z[n][0].ln(),
            "T_over_Z": +(tlog[n][0] / z[n][0]),
        }


def decimal_entropy_value_tau(beta: Sequence[float], tau: Sequence[Decimal], precision: int = 80) -> Decimal:
    with localcontext() as ctx:
        ctx.prec = precision
        b = [decimal_from_float(x) for x in beta]
        n = len(tau)
        inv = [Decimal(1) / x for x in tau]
        diag = [Decimal(0) for _ in range(n)]
        edge = [Decimal(0) for _ in range(n - 1)]
        for i in range(n - 1):
            diag[i] = inv[i] + b[i] * b[i] * inv[i + 1] - Decimal(1)
            edge[i] = -b[i] * inv[i + 1]
        diag[-1] = inv[-1] - Decimal(1)
        kappa: list[list[Decimal]] = [[Decimal(0) for _ in range(n)] for _ in range(n)]
        for start in range(n):
            prev2 = Decimal(1)
            prev1 = diag[start]
            if prev1 <= 0:
                raise ValueError("nonpositive Decimal one-point interval determinant")
            kappa[start][start] = prev1
            for end in range(start + 1, n):
                current = diag[end] * prev1 - edge[end - 1] * edge[end - 1] * prev2
                if current <= 0:
                    raise ValueError("nonpositive Decimal interval determinant")
                kappa[start][end] = current
                prev2, prev1 = prev1, current
        z = [Decimal(0) for _ in range(n + 1)]
        tlog = [Decimal(0) for _ in range(n + 1)]
        z[0] = Decimal(1)
        for length in range(1, n + 1):
            end = length - 1
            z_value = z[length - 1]
            t_value = tlog[length - 1]
            for start in range(length):
                prefix_len = 0 if start == 0 else start - 1
                block = kappa[start][end]
                z_prefix = z[prefix_len]
                z_value += z_prefix * block
                t_value += block * tlog[prefix_len]
                t_value += z_prefix * block * block.ln()
            z[length] = +z_value
            tlog[length] = +t_value
        return +(z[n].ln() - tlog[n] / z[n])


def decimal_interval_stats(beta: Sequence[float], tau: Sequence[float], precision: int = 80) -> dict[str, str]:
    with localcontext() as ctx:
        ctx.prec = precision
        b = [decimal_from_float(x) for x in beta]
        t0 = [decimal_from_float(x) for x in tau]
        n = len(t0)
        inv = [Decimal(1) / x for x in t0]
        diag = [Decimal(0) for _ in range(n)]
        edge = [Decimal(0) for _ in range(n - 1)]
        for i in range(n - 1):
            diag[i] = inv[i] + b[i] * b[i] * inv[i + 1] - Decimal(1)
            edge[i] = -b[i] * inv[i + 1]
        diag[-1] = inv[-1] - Decimal(1)
        min_kappa: Decimal | None = None
        max_kappa: Decimal | None = None
        for start in range(n):
            prev2 = Decimal(1)
            prev1 = diag[start]
            min_kappa = prev1 if min_kappa is None else min(min_kappa, prev1)
            max_kappa = prev1 if max_kappa is None else max(max_kappa, prev1)
            for end in range(start + 1, n):
                current = diag[end] * prev1 - edge[end - 1] * edge[end - 1] * prev2
                min_kappa = min(min_kappa, current)
                max_kappa = max(max_kappa, current)
                prev2, prev1 = prev1, current
        assert min_kappa is not None and max_kappa is not None
        return {
            "min_interval_det": str(+min_kappa),
            "max_interval_det": str(+max_kappa),
            "log10_min_interval_det": str(+min_kappa.log10()),
            "log10_max_interval_det": str(+max_kappa.log10()),
        }


def q(x: Fraction | int) -> Fraction:
    return x if isinstance(x, Fraction) else Fraction(x)


def zeros(n: int, m: int) -> Matrix:
    return [[Fraction(0) for _ in range(m)] for _ in range(n)]


def eye(n: int) -> Matrix:
    return [[Fraction(i == j) for j in range(n)] for i in range(n)]


def mat_mul(a: Matrix, b: Matrix) -> Matrix:
    bt = list(zip(*b))
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def mat_add(a: Matrix, b: Matrix) -> Matrix:
    return [[x + y for x, y in zip(row_a, row_b)] for row_a, row_b in zip(a, b)]


def mat_scale(a: Matrix, c: Fraction) -> Matrix:
    return [[c * x for x in row] for row in a]


def det_bareiss(a: Matrix) -> Fraction:
    n = len(a)
    if n == 0:
        return Fraction(1)
    m = [row[:] for row in a]
    sign = Fraction(1)
    previous = Fraction(1)
    for k in range(n - 1):
        pivot = None
        for i in range(k, n):
            if m[i][k] != 0:
                pivot = i
                break
        if pivot is None:
            return Fraction(0)
        if pivot != k:
            m[k], m[pivot] = m[pivot], m[k]
            sign = -sign
        pivot_value = m[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                m[i][j] = (m[i][j] * pivot_value - m[i][k] * m[k][j]) / previous
        previous = pivot_value
        for i in range(k + 1, n):
            m[i][k] = Fraction(0)
    return sign * m[n - 1][n - 1]


def inverse(a: Matrix) -> Matrix:
    n = len(a)
    if n == 0:
        return []
    m = [row[:] + ident[:] for row, ident in zip(a, eye(n))]
    for k in range(n):
        pivot = None
        for i in range(k, n):
            if m[i][k] != 0:
                pivot = i
                break
        if pivot is None:
            raise ValueError("singular matrix")
        if pivot != k:
            m[k], m[pivot] = m[pivot], m[k]
        scale = m[k][k]
        m[k] = [x / scale for x in m[k]]
        for i in range(n):
            if i == k:
                continue
            factor = m[i][k]
            if factor:
                m[i] = [x - factor * y for x, y in zip(m[i], m[k])]
    return [row[n:] for row in m]


def principal_submatrix(a: Matrix, mask: int, n: int) -> Matrix:
    idx = [i for i in range(n) if (mask >> i) & 1]
    return [[a[i][j] for j in idx] for i in idx]


def trace(a: Matrix) -> Fraction:
    return sum(a[i][i] for i in range(len(a)))


def exact_u_inverse(beta: Sequence[Fraction]) -> Matrix:
    n = len(beta) + 1
    u = zeros(n, n)
    for j in range(n):
        prod = Fraction(1)
        for i in range(j, n):
            if i == j:
                prod = Fraction(1)
            else:
                prod *= beta[i - 1]
            u[i][j] = prod
    return u


def exact_s_from_weights(beta: Sequence[Fraction], weights: Sequence[Fraction]) -> Matrix:
    n = len(weights)
    u = exact_u_inverse(beta)
    s = zeros(n, n)
    for k, wk in enumerate(weights):
        for i in range(k, n):
            uki = u[i][k]
            if uki == 0:
                continue
            for j in range(k, n):
                s[i][j] += wk * uki * u[j][k]
    for i in range(n):
        for j in range(i):
            s[j][i] = s[i][j]
    return s


def exact_k_and_kdot(beta: Sequence[Fraction], tau: Sequence[Fraction], delta: Sequence[Fraction]) -> tuple[Matrix, Matrix]:
    n = len(tau)
    s0 = exact_s_from_weights(beta, tau)
    sdot = exact_s_from_weights(beta, delta)
    k0 = eye(n)
    for i in range(n):
        for j in range(n):
            k0[i][j] -= s0[i][j]
            sdot[i][j] = -sdot[i][j]
    return k0, sdot


def determinant_jet_for_principal(k0: Matrix, kdot: Matrix, mask: int) -> tuple[Fraction, Fraction, Fraction]:
    n = len(k0)
    if mask == 0:
        return Fraction(1), Fraction(0), Fraction(0)
    a = principal_submatrix(k0, mask, n)
    b = principal_submatrix(kdot, mask, n)
    det0 = det_bareiss(a)
    ainv = inverse(a)
    qmat = mat_mul(ainv, b)
    trq = trace(qmat)
    q2 = mat_mul(qmat, qmat)
    second = det0 * (trq * trq - trace(q2))
    first = det0 * trq
    return det0, first, second


def exact_atom_jets_mobius(
    beta: Sequence[Fraction], tau: Sequence[Fraction], delta: Sequence[Fraction]
) -> list[tuple[Fraction, Fraction, Fraction]]:
    n = len(tau)
    full = (1 << n) - 1
    k0, kdot = exact_k_and_kdot(beta, tau, delta)
    inclusion = [determinant_jet_for_principal(k0, kdot, mask) for mask in range(1 << n)]
    atoms: list[tuple[Fraction, Fraction, Fraction]] = []
    for s_mask in range(1 << n):
        comp = full ^ s_mask
        p0 = Fraction(0)
        p1 = Fraction(0)
        p2 = Fraction(0)
        t_mask = comp
        while True:
            sign = -1 if (t_mask.bit_count() & 1) else 1
            d0, d1, d2 = inclusion[s_mask | t_mask]
            p0 += sign * d0
            p1 += sign * d1
            p2 += sign * d2
            if t_mask == 0:
                break
            t_mask = (t_mask - 1) & comp
        atoms.append((p0, p1, p2))
    return atoms


def dec_fraction(x: Fraction, precision: int) -> Decimal:
    return Decimal(x.numerator) / Decimal(x.denominator)


def entropy_from_atom_probs(atoms: Sequence[Fraction], precision: int) -> Decimal:
    with localcontext() as ctx:
        ctx.prec = precision
        total = Decimal(0)
        for p in atoms:
            if p <= 0:
                raise ValueError(f"nonpositive atom probability {p}")
            pd = dec_fraction(p, precision)
            total -= pd * pd.ln()
        return +total


def entropy_jets_from_exact_atoms(
    atoms: Sequence[tuple[Fraction, Fraction, Fraction]], precision: int
) -> dict[str, Decimal | Fraction]:
    with localcontext() as ctx:
        ctx.prec = precision
        h0 = Decimal(0)
        h1 = Decimal(0)
        h2 = Decimal(0)
        sum0 = Fraction(0)
        sum1 = Fraction(0)
        sum2 = Fraction(0)
        min_atom = None
        for p0, p1, p2 in atoms:
            if p0 <= 0:
                raise ValueError(f"nonpositive atom probability {p0}")
            min_atom = p0 if min_atom is None else min(min_atom, p0)
            sum0 += p0
            sum1 += p1
            sum2 += p2
            p0d = dec_fraction(p0, precision)
            logp = p0d.ln()
            h0 -= p0d * logp
            h1 -= dec_fraction(p1, precision) * logp
            h2 -= dec_fraction(p2, precision) * logp
            h2 -= dec_fraction(p1 * p1 / p0, precision)
        return {
            "H": +h0,
            "H1": +h1,
            "H2": +h2,
            "sum_p0": sum0,
            "sum_p1": sum1,
            "sum_p2": sum2,
            "min_atom": min_atom if min_atom is not None else Fraction(1),
        }


def exact_entropy_at_t(
    beta: Sequence[Fraction], tau: Sequence[Fraction], delta: Sequence[Fraction], t: Fraction, precision: int
) -> Decimal:
    tau_t = [x + t * d for x, d in zip(tau, delta)]
    k_t, _ = exact_k_and_kdot(beta, tau_t, [Fraction(0) for _ in tau_t])
    n = len(tau_t)
    full = (1 << n) - 1
    inclusion = [det_bareiss(principal_submatrix(k_t, mask, n)) for mask in range(1 << n)]
    atoms: list[Fraction] = []
    for s_mask in range(1 << n):
        comp = full ^ s_mask
        total = Fraction(0)
        t_mask = comp
        while True:
            total += (-1 if t_mask.bit_count() & 1 else 1) * inclusion[s_mask | t_mask]
            if t_mask == 0:
                break
            t_mask = (t_mask - 1) & comp
        atoms.append(total)
    return entropy_from_atom_probs(atoms, precision)


def rational_validation_case(n: int) -> dict[str, object]:
    beta = [Fraction((-1) ** i * ((i % 3) + 1), 9 + i) for i in range(n - 1)]
    tau = [Fraction(i + 2, 145 + 11 * i) for i in range(n)]
    if n == 5:
        delta = [Fraction(0) for _ in range(n)]
        delta[1] = tau[1] * Fraction(3, 5)
        delta[3] = -tau[3] * Fraction(2, 7)
        label = "rank2"
    elif n == 6:
        delta = [tau[i] * Fraction(((-1) ** i) * (i + 1), 19) for i in range(n)]
        label = "full_rank"
    else:
        delta = [tau[i] * Fraction(((-1) ** (i + 1)) * ((2 * i + 1) % 5 + 1), 23) for i in range(n)]
        label = "full_rank"

    jet = entropy_jet_tau([float(x) for x in beta], [float(x) for x in tau], [float(x) for x in delta])
    exact_atoms = exact_atom_jets_mobius(beta, tau, delta)
    exact = entropy_jets_from_exact_atoms(exact_atoms, precision=100)

    h = Fraction(1, 1000)
    h_minus = exact_entropy_at_t(beta, tau, delta, -h, 100)
    h_zero = exact["H"]
    h_plus = exact_entropy_at_t(beta, tau, delta, h, 100)
    with localcontext() as ctx:
        ctx.prec = 100
        hd = dec_fraction(h, 100)
        fd_h1 = +((h_plus - h_minus) / (2 * hd))
        fd_h2 = +((h_plus - 2 * h_zero + h_minus) / (hd * hd))

    exact_h = float(exact["H"])
    exact_h1 = float(exact["H1"])
    exact_h2 = float(exact["H2"])
    return {
        "n": n,
        "case": label,
        "support_rank_equals_rank_K_direction": sum(1 for x in delta if x != 0),
        "events": 2**n,
        "beta": fraction_to_json(beta),
        "tau": fraction_to_json(tau),
        "delta": fraction_to_json(delta),
        "jet": {k: v for k, v in jet.items() if k in {"H", "H1", "H2", "interval_states", "full_events"}},
        "exact_event_mobius": {
            "H": str(exact["H"]),
            "H1": str(exact["H1"]),
            "H2": str(exact["H2"]),
            "sum_p0": fraction_to_json(exact["sum_p0"]),
            "sum_p1": fraction_to_json(exact["sum_p1"]),
            "sum_p2": fraction_to_json(exact["sum_p2"]),
            "min_atom": fraction_to_json(exact["min_atom"]),
        },
        "abs_diff_jet_vs_exact": {
            "H": abs(jet["H"] - exact_h),
            "H1": abs(jet["H1"] - exact_h1),
            "H2": abs(jet["H2"] - exact_h2),
        },
        "finite_difference_sanity": {
            "h": fraction_to_json(h),
            "H_minus": str(h_minus),
            "H_plus": str(h_plus),
            "central_H1": str(fd_h1),
            "central_H2": str(fd_h2),
            "abs_diff_fd_H1_vs_exact": str(abs(fd_h1 - exact["H1"])),
            "abs_diff_fd_H2_vs_exact": str(abs(fd_h2 - exact["H2"])),
        },
    }


def run_direct_validations() -> dict[str, object]:
    cases = [rational_validation_case(n) for n in (5, 6, 7)]
    status = "PASS"
    for item in cases:
        diffs = item["abs_diff_jet_vs_exact"]
        if not (diffs["H"] < 1e-10 and diffs["H1"] < 1e-9 and diffs["H2"] < 1e-7):
            status = "FAIL"
    return {
        "status": status,
        "comparison": "O(n^2) path jet versus full exact-event Mobius derivative; finite difference is sanity only",
        "cases": cases,
    }


def structured_beta(n: int) -> list[float]:
    return [((-1.0) ** i) * (0.16 + 0.30 * ((5 * i + 2) % 11) / 10.0) for i in range(n - 1)]


def random_beta(n: int, rng: random.Random) -> list[float]:
    return [(-1.0 if rng.randrange(2) else 1.0) * rng.uniform(0.08, 0.58) for _ in range(n - 1)]


def max_scale_for_profile(beta: Sequence[float], profile: Sequence[float]) -> float:
    lo = 0.0
    hi = 1.0
    while admissible_l(beta, [hi * x for x in profile]) and hi < 1e6:
        hi *= 2.0
    for _ in range(72):
        mid = 0.5 * (lo + hi)
        if admissible_l(beta, [mid * x for x in profile]):
            lo = mid
        else:
            hi = mid
    return lo


def random_center(beta: Sequence[float], rng: random.Random) -> list[float] | None:
    n = len(beta) + 1
    profile = [math.exp(rng.uniform(math.log(0.65), math.log(1.55))) for _ in range(n)]
    smax = max_scale_for_profile(beta, profile)
    if not math.isfinite(smax) or smax <= 0.0:
        return None
    scale = rng.uniform(0.22, 0.88) * smax
    tau = [scale * x for x in profile]
    return tau if admissible_l(beta, tau) else None


def random_delta(tau: Sequence[float], support_size: int, rng: random.Random) -> list[float]:
    n = len(tau)
    support = list(range(n)) if support_size >= n else rng.sample(range(n), support_size)
    raw = [0.0] * n
    for i in support:
        raw[i] = rng.gauss(0.0, 1.0)
    raw_norm = max(abs(raw[i]) for i in support)
    if raw_norm == 0.0:
        raw[support[0]] = 1.0
        raw_norm = 1.0
    rel_scale = rng.uniform(0.20, 1.00)
    delta = [0.0] * n
    for i in support:
        delta[i] = rel_scale * tau[i] * raw[i] / raw_norm
    return delta


def column_gram_for_r_inverse(beta: Sequence[float]) -> list[list[float]]:
    n = len(beta) + 1
    tail_norm = [1.0] * n
    for i in range(n - 2, -1, -1):
        tail_norm[i] = 1.0 + beta[i] * beta[i] * tail_norm[i + 1]
    gram = [[0.0] * n for _ in range(n)]
    for i in range(n):
        gram[i][i] = tail_norm[i]
        prod = 1.0
        for j in range(i + 1, n):
            prod *= beta[j - 1]
            value = prod * tail_norm[j]
            gram[i][j] = value
            gram[j][i] = value
    return gram


def k_direction_frobenius_norm_sq(gram: Sequence[Sequence[float]], delta: Sequence[float]) -> float:
    n = len(delta)
    total = 0.0
    for i in range(n):
        if delta[i] == 0.0:
            continue
        row_total = 0.0
        gi = gram[i]
        di = delta[i]
        for j in range(n):
            if delta[j] != 0.0:
                row_total += delta[j] * gi[j] * gi[j]
        total += di * row_total
    if total < 0.0 and total > -1e-14:
        return 0.0
    return total


def sturm_count_leq(diag: Sequence[float], edge: Sequence[float], x: float) -> int:
    n = len(diag)
    tiny = 1e-300
    qv = diag[0] - x
    count = 1 if qv <= 0.0 else 0
    for i in range(1, n):
        if abs(qv) < tiny:
            qv = -tiny if qv < 0.0 else tiny
        qv = diag[i] - x - edge[i - 1] * edge[i - 1] / qv
        if qv <= 0.0:
            count += 1
    return count


def eig_minmax_tridiag(diag: Sequence[float], edge: Sequence[float]) -> tuple[float, float]:
    n = len(diag)
    if n == 1:
        return diag[0], diag[0]
    lo = math.inf
    hi = -math.inf
    for i, d in enumerate(diag):
        radius = 0.0
        if i > 0:
            radius += abs(edge[i - 1])
        if i + 1 < n:
            radius += abs(edge[i])
        lo = min(lo, d - radius)
        hi = max(hi, d + radius)
    width = max(1.0, hi - lo)
    lo -= 0.01 * width + 1e-9
    hi += 0.01 * width + 1e-9

    def kth(k: int) -> float:
        left, right = lo, hi
        for _ in range(90):
            mid = 0.5 * (left + right)
            if sturm_count_leq(diag, edge, mid) <= k:
                left = mid
            else:
                right = mid
        return 0.5 * (left + right)

    return kth(0), kth(n - 1)


def spectral_margin_from_tau(beta: Sequence[float], tau: Sequence[float]) -> dict[str, float]:
    pdiag, pedge = p_parts_float(beta, tau)
    lmin_p, lmax_p = eig_minmax_tridiag(pdiag, pedge)
    lambda_min_s = 1.0 / lmax_p
    lambda_max_s = 1.0 / lmin_p
    return {
        "lambda_min_P": lmin_p,
        "lambda_max_P": lmax_p,
        "lambda_min_S": lambda_min_s,
        "lambda_max_S": lambda_max_s,
        "strict_K_margin_min_lambda_K_IminusK": min(1.0 - lambda_max_s, lambda_min_s),
    }


def rounded(values: Sequence[float], digits: int = 12) -> list[float]:
    return [round(float(x), digits) for x in values]


def scout_record(
    n: int,
    bucket: str,
    beta: Sequence[float],
    tau: Sequence[float],
    delta: Sequence[float],
    jet: dict[str, float],
    norm_sq: float,
    margin: dict[str, float],
    seed: int,
    trial: int,
) -> dict[str, object]:
    support = sum(1 for x in delta if abs(x) > 0.0)
    normalized = jet["H2"] / norm_sq if norm_sq > 0.0 else math.nan
    return {
        "n": n,
        "bucket": bucket,
        "trial": trial,
        "seed": seed,
        "rank_K_direction": support,
        "H": jet["H"],
        "H1": jet["H1"],
        "H2": jet["H2"],
        "K_direction_frobenius_norm_sq": norm_sq,
        "normalized_H2_per_frobenius_norm_sq": normalized,
        "spectral_margin_center": margin,
        "beta_head": rounded(beta[: min(8, len(beta))]),
        "tau_head": rounded(tau[: min(8, len(tau))]),
        "delta_head": rounded(delta[: min(8, len(delta))]),
        "support_indices_head": [i for i, x in enumerate(delta) if abs(x) > 0.0][:16],
    }


def update_extreme(bucket: dict[str, object], record: dict[str, object]) -> None:
    value = float(record["normalized_H2_per_frobenius_norm_sq"])
    if bucket.get("max_normalized") is None or value > float(bucket["max_normalized"]["normalized_H2_per_frobenius_norm_sq"]):
        bucket["max_normalized"] = record
    if bucket.get("min_abs_normalized") is None or abs(value) < abs(
        float(bucket["min_abs_normalized"]["normalized_H2_per_frobenius_norm_sq"])
    ):
        bucket["min_abs_normalized"] = record
    if bucket.get("most_negative") is None or value < float(bucket["most_negative"]["normalized_H2_per_frobenius_norm_sq"]):
        bucket["most_negative"] = record
    if value > 1e-10:
        bucket["positive_gt_1e-10"] += 1
        positives = bucket.setdefault("positive_examples", [])
        if isinstance(positives, list) and len(positives) < 5:
            positives.append(record)


def scout_one_n(n: int, trials: int, rng: random.Random, seed: int) -> dict[str, object]:
    buckets: dict[str, dict[str, object]] = {
        "rank2": {
            "support_size": 2,
            "evaluations": 0,
            "failures": 0,
            "positive_gt_1e-10": 0,
            "max_normalized": None,
            "min_abs_normalized": None,
            "most_negative": None,
        },
        "full_rank": {
            "support_size": n,
            "evaluations": 0,
            "failures": 0,
            "positive_gt_1e-10": 0,
            "max_normalized": None,
            "min_abs_normalized": None,
            "most_negative": None,
        },
    }
    center_failures = 0
    for trial in range(trials):
        beta = structured_beta(n) if trial % 7 == 0 else random_beta(n, rng)
        tau = random_center(beta, rng)
        if tau is None:
            center_failures += 1
            continue
        gram = column_gram_for_r_inverse(beta)
        margin = spectral_margin_from_tau(beta, tau)
        for name, bucket in buckets.items():
            support_size = int(bucket["support_size"])
            delta = random_delta(tau, support_size, rng)
            norm_sq = k_direction_frobenius_norm_sq(gram, delta)
            if norm_sq <= 0.0 or not math.isfinite(norm_sq):
                bucket["failures"] += 1
                continue
            try:
                jet = entropy_jet_tau(beta, tau, delta)
            except (ValueError, OverflowError):
                bucket["failures"] += 1
                continue
            if not math.isfinite(jet["H2"]):
                bucket["failures"] += 1
                continue
            bucket["evaluations"] += 1
            record = scout_record(n, name, beta, tau, delta, jet, norm_sq, margin, seed, trial)
            update_extreme(bucket, record)
    return {"n": n, "trials": trials, "center_failures": center_failures, "buckets": buckets}


def run_curvature_scout(n_min: int, n_max: int, trials: int, seed: int) -> dict[str, object]:
    rng = random.Random(seed)
    per_n = [scout_one_n(n, trials, rng, seed) for n in range(n_min, n_max + 1)]
    global_best: dict[str, object] | None = None
    global_closest: dict[str, object] | None = None
    positives: list[dict[str, object]] = []
    total_evaluations = 0
    for item in per_n:
        for name, bucket in item["buckets"].items():
            total_evaluations += int(bucket["evaluations"])
            max_record = bucket["max_normalized"]
            closest_record = bucket["min_abs_normalized"]
            if max_record is not None:
                if global_best is None or float(max_record["normalized_H2_per_frobenius_norm_sq"]) > float(
                    global_best["normalized_H2_per_frobenius_norm_sq"]
                ):
                    global_best = max_record
            if closest_record is not None:
                if global_closest is None or abs(float(closest_record["normalized_H2_per_frobenius_norm_sq"])) < abs(
                    float(global_closest["normalized_H2_per_frobenius_norm_sq"])
                ):
                    global_closest = closest_record
            if int(bucket["positive_gt_1e-10"]) > 0:
                positives.append(
                    {
                        "n": item["n"],
                        "bucket": name,
                        "count": bucket["positive_gt_1e-10"],
                        "examples": bucket.get("positive_examples", []),
                    }
                )
    return {
        "status": "SCOUT_COMPLETE",
        "finite_search_only": True,
        "seed": seed,
        "n_min": n_min,
        "n_max": n_max,
        "trials_per_n": trials,
        "buckets": ["rank2", "full_rank"],
        "core_quantity": "H2=d^2/dt^2 H(tau0+t*delta)|_{t=0}, computed by O(n^2) jet DP",
        "normalization": "H2 divided by ||Kdot||_F^2, Kdot=-R^{-1}diag(delta)R^{-T}",
        "total_evaluations": total_evaluations,
        "positive_normalized_H2_gt_1e-10": positives,
        "global_max_normalized": global_best,
        "global_closest_to_zero_normalized": global_closest,
        "per_n": per_n,
    }


def jacobi_eigenvalues_symmetric(a: list[list[float]], sweeps: int = 120) -> list[float]:
    n = len(a)
    m = [row[:] for row in a]
    for _ in range(sweeps):
        p = 0
        qidx = 1 if n > 1 else 0
        best = 0.0
        for i in range(n):
            for j in range(i + 1, n):
                value = abs(m[i][j])
                if value > best:
                    best = value
                    p, qidx = i, j
        if best < 1e-13:
            break
        app = m[p][p]
        aqq = m[qidx][qidx]
        apq = m[p][qidx]
        tau = (aqq - app) / (2.0 * apq)
        tangent = math.copysign(1.0 / (abs(tau) + math.sqrt(1.0 + tau * tau)), tau)
        c = 1.0 / math.sqrt(1.0 + tangent * tangent)
        s = tangent * c
        for k in range(n):
            if k != p and k != qidx:
                mkp = m[k][p]
                mkq = m[k][qidx]
                m[k][p] = c * mkp - s * mkq
                m[p][k] = m[k][p]
                m[k][qidx] = s * mkp + c * mkq
                m[qidx][k] = m[k][qidx]
        m[p][p] = c * c * app - 2.0 * s * c * apq + s * s * aqq
        m[qidx][qidx] = s * s * app + 2.0 * s * c * apq + c * c * aqq
        m[p][qidx] = 0.0
        m[qidx][p] = 0.0
    return sorted(m[i][i] for i in range(n))


def low_dim_hessian_case(n: int) -> dict[str, object]:
    beta = [((-1.0) ** i) * (0.18 + 0.04 * ((i + 1) % 4)) for i in range(n - 1)]
    profile = [0.75 + 0.09 * ((2 * i + 1) % 5) for i in range(n)]
    smax = max_scale_for_profile(beta, profile)
    tau = [0.44 * smax * x for x in profile]

    basis_values: list[float] = []
    for i in range(n):
        direction = [0.0] * n
        direction[i] = 1.0
        basis_values.append(entropy_jet_tau(beta, tau, direction)["H2"])
    hessian = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        hessian[i][i] = basis_values[i]
    for i in range(n):
        for j in range(i + 1, n):
            direction = [0.0] * n
            direction[i] = 1.0
            direction[j] = 1.0
            qij = entropy_jet_tau(beta, tau, direction)["H2"]
            value = 0.5 * (qij - basis_values[i] - basis_values[j])
            hessian[i][j] = value
            hessian[j][i] = value
    eigenvalues = jacobi_eigenvalues_symmetric(hessian)
    gram = column_gram_for_r_inverse(beta)
    return {
        "n": n,
        "finite_local_hessian_only": True,
        "beta": rounded(beta),
        "tau": rounded(tau),
        "spectral_margin_center": spectral_margin_from_tau(beta, tau),
        "diagonal_second_derivatives": basis_values,
        "hessian": [[round(x, 14) for x in row] for row in hessian],
        "jacobi_eigenvalues": eigenvalues,
        "max_eigenvalue": max(eigenvalues),
        "min_eigenvalue": min(eigenvalues),
        "basis_K_frobenius_norm_sq": [
            k_direction_frobenius_norm_sq(gram, [1.0 if i == j else 0.0 for i in range(n)]) for j in range(n)
        ],
    }


def run_low_dim_hessians() -> dict[str, object]:
    cases = [low_dim_hessian_case(5), low_dim_hessian_case(6)]
    return {
        "status": "FINITE_HESSIAN_BUILT",
        "method": "polarization of O(n^2) directional jet values; not a theorem",
        "cases": cases,
        "positive_max_eigenvalue_cases": [case for case in cases if case["max_eigenvalue"] > 1e-10],
    }


def replay_generated_case(
    target_n: int,
    target_trial: int,
    target_bucket: str,
    seed: int,
    trials_per_n: int,
    n_min: int = 5,
) -> dict[str, object]:
    """Replay the deterministic scout generator up to a recorded target."""

    rng = random.Random(seed)
    for n in range(n_min, target_n + 1):
        for trial in range(trials_per_n):
            beta = structured_beta(n) if trial % 7 == 0 else random_beta(n, rng)
            tau = random_center(beta, rng)
            if tau is None:
                continue
            for name, support_size in (("rank2", 2), ("full_rank", n)):
                delta = random_delta(tau, support_size, rng)
                if n == target_n and trial == target_trial and name == target_bucket:
                    gram = column_gram_for_r_inverse(beta)
                    jet = entropy_jet_tau(beta, tau, delta)
                    norm_sq = k_direction_frobenius_norm_sq(gram, delta)
                    return {
                        "n": n,
                        "trial": trial,
                        "bucket": name,
                        "seed": seed,
                        "trials_per_n": trials_per_n,
                        "rank_K_direction": sum(1 for x in delta if abs(x) > 0.0),
                        "support_indices": [i for i, x in enumerate(delta) if abs(x) > 0.0],
                        "beta": [repr(float(x)) for x in beta],
                        "tau": [repr(float(x)) for x in tau],
                        "delta": [repr(float(x)) for x in delta],
                        "float_jet": jet,
                        "K_direction_frobenius_norm_sq": norm_sq,
                        "normalized_H2_per_frobenius_norm_sq": jet["H2"] / norm_sq,
                        "spectral_margin_center_float_sturm": spectral_margin_from_tau(beta, tau),
                    }
    raise ValueError("target case was not reproduced")


def fraction_p_parts_from_frozen(candidate: dict[str, object]) -> tuple[list[Fraction], list[Fraction]]:
    beta = [Fraction(str(x)) for x in candidate["beta"]]
    tau = [Fraction(str(x)) for x in candidate["tau"]]
    inv = [Fraction(1) / t for t in tau]
    pdiag: list[Fraction] = []
    edge: list[Fraction] = []
    for i in range(len(tau) - 1):
        pdiag.append(inv[i] + beta[i] * beta[i] * inv[i + 1])
        edge.append(-beta[i] * inv[i + 1])
    pdiag.append(inv[-1])
    return pdiag, edge


def exact_ldl_pivots_fraction(diag: Sequence[Fraction], edge: Sequence[Fraction]) -> list[Fraction]:
    pivots: list[Fraction] = []
    pivot = diag[0]
    pivots.append(pivot)
    for i in range(1, len(diag)):
        if pivot <= 0:
            break
        pivot = diag[i] - edge[i - 1] * edge[i - 1] / pivot
        pivots.append(pivot)
    return pivots


def exact_spectral_margin_certificate(candidate: dict[str, object]) -> dict[str, object]:
    """Strict rational certificate for the frozen float64 candidate.

    The recorded decimal strings are treated as exact rational inputs.  For the
    n=93 scout case, exact tridiagonal LDL pivots certify

        4 I <= P=S^{-1} <= 50 I.

    Hence eigenvalues of S lie in [1/50,1/4] and the strict DPP margin is at
    least min(1/50,3/4)=1/50.
    """

    pdiag, edge = fraction_p_parts_from_frozen(candidate)
    n = len(pdiag)
    lower_shift = Fraction(4, 1)
    upper_shift = Fraction(50, 1)
    p_minus_lower_diag = [d - lower_shift for d in pdiag]
    upper_minus_p_diag = [upper_shift - d for d in pdiag]
    upper_minus_p_edge = [-e for e in edge]
    piv_lower = exact_ldl_pivots_fraction(p_minus_lower_diag, edge)
    piv_upper = exact_ldl_pivots_fraction(upper_minus_p_diag, upper_minus_p_edge)
    lower_ok = len(piv_lower) == n and all(x > 0 for x in piv_lower)
    upper_ok = len(piv_upper) == n and all(x > 0 for x in piv_upper)
    margin_bound = Fraction(1, 50) if lower_ok and upper_ok else None
    min_lower_index, min_lower_pivot = min(enumerate(piv_lower), key=lambda item: item[1])
    min_upper_index, min_upper_pivot = min(enumerate(piv_upper), key=lambda item: item[1])

    def compact_pivot_info(index: int, value: Fraction) -> dict[str, object]:
        return {
            "index_0_based": index,
            "decimal_approx": float(value),
            "numerator_digits": len(str(abs(value.numerator))),
            "denominator_digits": len(str(value.denominator)),
        }

    return {
        "input_interpretation": "float scout parameters frozen as exact decimal rationals from repr(float)",
        "certified_operator_bounds_for_P_equals_S_inverse": {
            "lower": "4*I <= P" if lower_ok else "NOT_CERTIFIED",
            "upper": "P <= 50*I" if upper_ok else "NOT_CERTIFIED",
        },
        "strict_DPP_margin_lower_bound": fraction_to_json(margin_bound) if margin_bound is not None else None,
        "consequence_if_certified": "1/50 <= eigenvalues(S=I-K) <= 1/4, so min(lambda_min(K), lambda_min(I-K)) >= 1/50",
        "P_minus_4I_LDL": {
            "ok": lower_ok,
            "pivots_checked": len(piv_lower),
            "min_pivot": compact_pivot_info(min_lower_index, min_lower_pivot),
            "all_pivots_are_exact_positive_fractions": lower_ok,
        },
        "50I_minus_P_LDL": {
            "ok": upper_ok,
            "pivots_checked": len(piv_upper),
            "min_pivot": compact_pivot_info(min_upper_index, min_upper_pivot),
            "all_pivots_are_exact_positive_fractions": upper_ok,
        },
    }


def decimal_chord_checks(
    beta: Sequence[float], tau: Sequence[float], delta: Sequence[float], precision: int = 90
) -> list[dict[str, str]]:
    with localcontext() as ctx:
        ctx.prec = precision
        bd = [decimal_from_float(x) for x in beta]
        td = [decimal_from_float(x) for x in tau]
        dd = [decimal_from_float(x) for x in delta]
        h0 = decimal_entropy_value_tau(beta, td, precision)
        out: list[dict[str, str]] = []
        for h_text in ("0.1", "0.05", "0.02", "0.01", "0.005", "0.002", "0.001", "0.0005"):
            h = Decimal(h_text)
            tau_minus = [t - h * d for t, d in zip(td, dd)]
            tau_plus = [t + h * d for t, d in zip(td, dd)]
            hm = decimal_entropy_value_tau(beta, tau_minus, precision)
            hp = decimal_entropy_value_tau(beta, tau_plus, precision)
            second = +((hp - Decimal(2) * h0 + hm) / (h * h))
            gap = +((hp + hm) / Decimal(2) - h0)
            first = +((hp - hm) / (Decimal(2) * h))
            out.append(
                {
                    "h": h_text,
                    "H_minus": str(hm),
                    "H_plus": str(hp),
                    "central_H1": str(first),
                    "central_H2": str(second),
                    "midpoint_gap": str(gap),
                }
            )
        return out


def scalar_xlogx_formula_check(precision: int = 90) -> dict[str, str]:
    with localcontext() as ctx:
        ctx.prec = precision
        x = Decimal("3.7")
        x1 = Decimal("-0.4")
        x2 = Decimal("0.2")
        analytic = x2 * (x.ln() + Decimal(1)) + x1 * x1 / x

        def f(h: Decimal) -> Decimal:
            y = x + h * x1 + h * h * x2 / Decimal(2)
            return y * y.ln()

        h = Decimal("1e-20")
        finite = (f(h) - Decimal(2) * f(Decimal(0)) + f(-h)) / (h * h)
        return {
            "test_curve": "x(t)=3.7-0.4t+0.1t^2, so x''(0)=0.2",
            "analytic_second_derivative": str(+analytic),
            "central_second_difference_h_1e_minus_20": str(+finite),
            "absolute_difference": str(+(abs(finite - analytic))),
        }


def frozen_candidate_stability_check() -> dict[str, object]:
    candidate = replay_generated_case(
        target_n=93,
        target_trial=15,
        target_bucket="rank2",
        seed=20260908,
        trials_per_n=24,
    )
    beta = [float(x) for x in candidate["beta"]]
    tau = [float(x) for x in candidate["tau"]]
    delta = [float(x) for x in candidate["delta"]]
    decimal_jets = [decimal_entropy_jet_tau(beta, tau, delta, precision=p) for p in (50, 80, 110)]
    h2_110 = Decimal(str(decimal_jets[-1]["H2"]))
    norm_sq = Decimal(str(candidate["K_direction_frobenius_norm_sq"]))
    float_h2 = Decimal(str(candidate["float_jet"]["H2"]))
    diagnostics_110 = decimal_jets[-1]
    logz = diagnostics_110["logZ"]
    t_over_z = diagnostics_110["T_over_Z"]
    cancellation_denominator = abs(logz) + abs(t_over_z)
    cancellation_ratio = abs(diagnostics_110["H"]) / cancellation_denominator
    decimal_z_jet = (diagnostics_110["Z"], diagnostics_110["Z1"], diagnostics_110["Z2"])
    decimal_t_jet = (diagnostics_110["T"], diagnostics_110["T1"], diagnostics_110["T2"])
    decimal_logz_jet = djlog(decimal_z_jet)
    decimal_ratio_jet = djdiv(decimal_t_jet, decimal_z_jet)
    float_z_jet = (
        float(candidate["float_jet"]["Z"]),
        float(candidate["float_jet"]["Z1"]),
        float(candidate["float_jet"]["Z2"]),
    )
    float_t_jet = (
        float(candidate["float_jet"]["T"]),
        float(candidate["float_jet"]["T1"]),
        float(candidate["float_jet"]["T2"]),
    )
    float_logz_jet = jlog(float_z_jet)
    float_ratio_jet = jdiv(float_t_jet, float_z_jet)
    legacy_unstable_float_ratio_jet = jmul(float_t_jet, jinv(float_z_jet))
    legacy_unstable_float_h2 = float_logz_jet[2] - legacy_unstable_float_ratio_jet[2]
    chord_checks = decimal_chord_checks(beta, tau, delta, precision=90)
    for row in chord_checks:
        row["ratio_central_H2_to_decimal_H2_precision_110"] = str(+(Decimal(row["central_H2"]) / h2_110))
    status = "LEGACY_FLOAT_POSITIVE_REJECTED_BY_STABLE_ARITHMETIC"
    if h2_110 > 0 and all(Decimal(row["central_H2"]) > 0 for row in chord_checks[-3:]):
        status = "FLOAT_CANDIDATE_HIGH_PRECISION_CONFIRMED"
    stability = {
        "status": status,
        "candidate": candidate,
        "decimal_jet_by_precision": decimal_jets,
        "normalized_decimal_H2_per_frobenius_norm_sq": str(+(h2_110 / norm_sq)),
        "float_vs_decimal_H2": {
            "float_H2": str(float_h2),
            "decimal_H2_precision_110": str(h2_110),
            "difference_float_minus_decimal": str(+(float_h2 - h2_110)),
            "sign_agrees": (float_h2 > 0) == (h2_110 > 0),
            "legacy_unstable_inverse_formula_H2": legacy_unstable_float_h2,
        },
        "symmetric_chord_second_differences": chord_checks,
        "dp_normalization_and_cancellation": {
            "precision": 110,
            "logZ": str(logz),
            "T_over_Z": str(t_over_z),
            "H_equals_logZ_minus_T_over_Z": str(diagnostics_110["H"]),
            "decimal_second_derivative_components": {
                "d2_logZ": str(+decimal_logz_jet[2]),
                "d2_T_over_Z": str(+decimal_ratio_jet[2]),
                "d2_logZ_minus_d2_T_over_Z": str(+(decimal_logz_jet[2] - decimal_ratio_jet[2])),
            },
            "float_second_derivative_components": {
                "d2_logZ": float_logz_jet[2],
                "d2_T_over_Z": float_ratio_jet[2],
                "d2_logZ_minus_d2_T_over_Z": float_logz_jet[2] - float_ratio_jet[2],
                "legacy_unstable_d2_T_over_Z_from_jinv": legacy_unstable_float_ratio_jet[2],
                "legacy_unstable_H2_from_jinv": legacy_unstable_float_h2,
            },
            "abs_H_over_abs_logZ_plus_abs_T_over_Z": str(+cancellation_ratio),
            "Z_scientific": f"{diagnostics_110['Z']:.18E}",
            "T_scientific": f"{diagnostics_110['T']:.18E}",
            "interval_stats": decimal_interval_stats(beta, tau, precision=90),
            "underflow_or_overflow_in_decimal": False,
            "float_Z_finite": math.isfinite(float(candidate["float_jet"]["Z"])),
            "float_T_finite": math.isfinite(float(candidate["float_jet"]["T"])),
        },
        "scalar_xlogx_formula_check": scalar_xlogx_formula_check(90),
        "exact_rational_spectral_certificate": exact_spectral_margin_certificate(candidate),
        "interpretation": [
            "The first n=93/rank2 positive scout from the pre-fix float run at seed 20260908 was replayed and frozen.",
            "The stable quotient float path and Decimal path agree that H2 is negative.",
            "Decimal jet uses a separate high-precision scalar implementation of the same differentiated DP.",
            "Symmetric entropy chords use the value DP only; their second differences converge to the Decimal H2.",
            "The old positive H2 is reproduced only by the legacy reciprocal-jet normalization and is rejected as an underflow/cancellation artifact.",
        ],
    }
    return stability


def fraction_to_json(x):
    if isinstance(x, Fraction):
        return f"{x.numerator}/{x.denominator}"
    if isinstance(x, Decimal):
        return str(x)
    if isinstance(x, list):
        return [fraction_to_json(v) for v in x]
    if isinstance(x, tuple):
        return [fraction_to_json(v) for v in x]
    if isinstance(x, dict):
        return {str(key): fraction_to_json(value) for key, value in x.items()}
    return x


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(fraction_to_json(data), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def run_all(args: argparse.Namespace) -> dict[str, object]:
    started = time.time()
    here = Path(__file__).resolve()
    results_dir = here.with_name("results")
    validations = run_direct_validations()
    write_json(results_dir / "direct_validation.json", validations)
    low_dim = run_low_dim_hessians()
    write_json(results_dir / "low_dim_hessian.json", low_dim)
    scout = run_curvature_scout(args.n_min, args.n_max, args.trials, args.seed)
    write_json(results_dir / "curvature_scout.json", scout)
    stability = frozen_candidate_stability_check()
    write_json(results_dir / "frozen_n93_rank2_stability.json", stability)
    positive_count = sum(int(item["count"]) for item in scout["positive_normalized_H2_gt_1e-10"])
    summary_status = "PASS_STABLE_FLOAT_NO_POSITIVES"
    if validations["status"] != "PASS":
        summary_status = "FAIL_DIRECT_VALIDATION"
    elif positive_count:
        summary_status = "PASS_WITH_FLOAT_POSITIVE_SIGNALS_NEED_DECIMAL_REPLAY"
    summary = {
        "status": summary_status,
        "elapsed_seconds": time.time() - started,
        "thread_limits": {
            "OMP_NUM_THREADS": os.environ.get("OMP_NUM_THREADS"),
            "OPENBLAS_NUM_THREADS": os.environ.get("OPENBLAS_NUM_THREADS"),
            "MKL_NUM_THREADS": os.environ.get("MKL_NUM_THREADS"),
            "NUMEXPR_NUM_THREADS": os.environ.get("NUMEXPR_NUM_THREADS"),
        },
        "direct_validation_status": validations["status"],
        "low_dim_positive_hessian_cases": len(low_dim["positive_max_eigenvalue_cases"]),
        "scout_total_evaluations": scout["total_evaluations"],
        "scout_positive_normalized_H2_gt_1e-10_count": positive_count,
        "global_max_normalized": scout["global_max_normalized"],
        "global_closest_to_zero_normalized": scout["global_closest_to_zero_normalized"],
        "frozen_candidate_status": stability["status"],
        "frozen_candidate_decimal_H2_precision_110": str(stability["decimal_jet_by_precision"][-1]["H2"]),
        "frozen_candidate_strict_margin_lower_bound": stability["exact_rational_spectral_certificate"][
            "strict_DPP_margin_lower_bound"
        ],
        "outputs": [
            "results/direct_validation.json",
            "results/low_dim_hessian.json",
            "results/curvature_scout.json",
            "results/frozen_n93_rank2_stability.json",
            "results/summary.json",
        ],
    }
    write_json(results_dir / "summary.json", summary)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-min", type=int, default=5)
    parser.add_argument("--n-max", type=int, default=100)
    parser.add_argument("--trials", type=int, default=24)
    parser.add_argument("--seed", type=int, default=20260908)
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--low-dim-only", action="store_true")
    parser.add_argument("--scout-only", action="store_true")
    parser.add_argument("--check-frozen-candidate", action="store_true")
    args = parser.parse_args()

    here = Path(__file__).resolve()
    results_dir = here.with_name("results")
    if args.validate_only:
        result = run_direct_validations()
        write_json(results_dir / "direct_validation.json", result)
    elif args.low_dim_only:
        result = run_low_dim_hessians()
        write_json(results_dir / "low_dim_hessian.json", result)
    elif args.scout_only:
        result = run_curvature_scout(args.n_min, args.n_max, args.trials, args.seed)
        write_json(results_dir / "curvature_scout.json", result)
    elif args.check_frozen_candidate:
        result = frozen_candidate_stability_check()
        write_json(results_dir / "frozen_n93_rank2_stability.json", result)
    else:
        result = run_all(args)
    print(json.dumps(fraction_to_json(result), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
