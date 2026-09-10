#!/usr/bin/env python3
"""Exact continuum certificate for the integrated unequal-strength half-leaf core.

The theorem certified here is:
    E(a,b)>0 for every 1/4 <= a,b <= 4,
where E=L-C(F+R)^{-1}C^T is the exact integrated occupied-side Schur core
from the complete four selected events of a strict half-leaf DPP after
normalizing the rare selected corner to one.

The proof covers the whole square, not a point sample.  It partitions
r=a/(1+a), s=b/(1+b) uniformly into 32 rational intervals each.  On every
one of the 1024 boxes it encloses the full six-dimensional quadratic form
M=[[Y,C^T],[C,L]] by exact fixed-point interval arithmetic.  A floating
Cholesky factor is used only to choose a rational upper-triangular
preconditioner P.  The final check that P^T M P is uniformly strictly
diagonally dominant uses exact integers and rigorous log intervals.

Natural logarithms are enclosed by the positive atanh series with an exact
geometric tail.  No sampled sign, optimizer, prior PR checker, or pointwise
resolvent positivity is used.
"""
from __future__ import annotations

from fractions import Fraction as F
from functools import lru_cache
import math
import resource
import time

# Exact certificate parameters.
FIX_BITS = 140
SCALE = 1 << FIX_BITS
LOG_TERMS = 56
PRECOND_BITS = 44
PRECOND_SCALE = 1 << PRECOND_BITS
GRID = 32
R_LO = F(1, 5)   # a=1/4
R_HI = F(4, 5)   # a=4


def floor_div(n: int, d: int) -> int:
    if d <= 0:
        raise ValueError("positive denominator required")
    return n // d


def ceil_div(n: int, d: int) -> int:
    if d <= 0:
        raise ValueError("positive denominator required")
    return -((-n) // d)


class Interval:
    """Closed interval [lo/SCALE, hi/SCALE] with exact outward rounding."""

    __slots__ = ("lo", "hi")

    def __init__(self, lo: int, hi: int | None = None) -> None:
        self.lo = int(lo)
        self.hi = int(lo if hi is None else hi)
        if self.lo > self.hi:
            raise ValueError("reversed interval")

    @staticmethod
    def from_fraction(x: F | int) -> "Interval":
        x = F(x)
        return Interval(
            floor_div(x.numerator * SCALE, x.denominator),
            ceil_div(x.numerator * SCALE, x.denominator),
        )

    def __add__(self, other: "Interval" | F | int) -> "Interval":
        other = other if isinstance(other, Interval) else Interval.from_fraction(other)
        return Interval(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self) -> "Interval":
        return Interval(-self.hi, -self.lo)

    def __sub__(self, other: "Interval" | F | int) -> "Interval":
        other = other if isinstance(other, Interval) else Interval.from_fraction(other)
        return self + (-other)

    def __rsub__(self, other: "Interval" | F | int) -> "Interval":
        return Interval.from_fraction(other) - self

    def __mul__(self, other: "Interval" | F | int) -> "Interval":
        other = other if isinstance(other, Interval) else Interval.from_fraction(other)
        products = (
            self.lo * other.lo,
            self.lo * other.hi,
            self.hi * other.lo,
            self.hi * other.hi,
        )
        return Interval(
            floor_div(min(products), SCALE),
            ceil_div(max(products), SCALE),
        )

    __rmul__ = __mul__

    def reciprocal(self) -> "Interval":
        if self.lo <= 0 <= self.hi:
            raise ZeroDivisionError("interval contains zero")
        endpoints: list[tuple[int, int]] = []
        for n in (self.lo, self.hi):
            if n > 0:
                endpoints.append(
                    (floor_div(SCALE * SCALE, n), ceil_div(SCALE * SCALE, n))
                )
            else:
                p = -n
                endpoints.append(
                    (-ceil_div(SCALE * SCALE, p), -floor_div(SCALE * SCALE, p))
                )
        return Interval(
            min(x[0] for x in endpoints), max(x[1] for x in endpoints)
        )

    def __truediv__(self, other: "Interval" | F | int) -> "Interval":
        other = other if isinstance(other, Interval) else Interval.from_fraction(other)
        return self * other.reciprocal()

    def max_abs_scaled(self) -> int:
        return max(abs(self.lo), abs(self.hi))


ZERO = Interval.from_fraction(0)
ONE = Interval.from_fraction(1)


@lru_cache(maxsize=None)
def log_fraction(x: F) -> Interval:
    """Rigorous enclosure of log(x), x positive rational."""
    if x <= 0:
        raise ValueError("log argument must be positive")

    y = x
    power_two = 0
    while y < 1:
        y *= 2
        power_two -= 1
    while y >= 2:
        y /= 2
        power_two += 1

    def atanh_log_unit(zarg: F) -> tuple[F, F]:
        # Valid for 1 <= zarg <= 2.  z=(zarg-1)/(zarg+1) lies in [0,1/3].
        z = (zarg - 1) / (zarg + 1)
        z2 = z * z
        term = z
        partial = F(0)
        for j in range(LOG_TERMS):
            partial += 2 * term / (2 * j + 1)
            term *= z2
        # term is z^(2*LOG_TERMS+1).  All omitted terms are nonnegative.
        tail = 2 * term / ((2 * LOG_TERMS + 1) * (1 - z2))
        return partial, partial + tail

    lo, hi = atanh_log_unit(y)
    log2_lo, log2_hi = atanh_log_unit(F(2))
    if power_two >= 0:
        lo += power_two * log2_lo
        hi += power_two * log2_hi
    else:
        lo += power_two * log2_hi
        hi += power_two * log2_lo

    return Interval(
        floor_div(lo.numerator * SCALE, lo.denominator),
        ceil_div(hi.numerator * SCALE, hi.denominator),
    )


def hull_monotone(low_value: Interval, high_value: Interval) -> Interval:
    return Interval(low_value.lo, high_value.hi)


def point_H(a: F, b: F) -> Interval:
    # H=log((1+a)(1+b)/(1+a+b)) is increasing in both variables.
    return log_fraction((1 + a) * (1 + b) / (1 + a + b))


def point_ell(a: F, b: F) -> Interval:
    # ell=(log(1+a)+log(1+a+b)-log(1+b))/2.
    return log_fraction((1 + a) * (1 + a + b) / (1 + b)) / 2


def point_k(a: F, b: F) -> Interval:
    return log_fraction((1 + b) * (1 + a + b) / (1 + a)) / 2


def point_J(a: F, b: F) -> Interval:
    # J=int_0^a int_0^b (1+x+y)^(-1) dy dx; increasing in a,b.
    c0, ca, cb = 1 + a + b, 1 + a, 1 + b
    return c0 * log_fraction(c0) - ca * log_fraction(ca) - cb * log_fraction(cb)


def parameter_interval(lo: F, hi: F) -> Interval:
    ilo, ihi = Interval.from_fraction(lo), Interval.from_fraction(hi)
    return Interval(ilo.lo, ihi.hi)


def full_form_interval(a0: F, a1: F, b0: F, b1: F) -> list[list[Interval]]:
    """Enclose M=[[Y,C^T],[C,L]] throughout one parameter box."""
    if not (0 < a0 <= a1 and 0 < b0 <= b1):
        raise ValueError("illegal parameter box")

    # Exact monotonicity is used before any interval operation.
    H = hull_monotone(point_H(a0, b0), point_H(a1, b1))
    # ell increases in a and decreases in b; k has the exchanged monotonicity.
    ell = hull_monotone(point_ell(a0, b1), point_ell(a1, b0))
    kval = hull_monotone(point_k(a1, b0), point_k(a0, b1))
    J = hull_monotone(point_J(a0, b0), point_J(a1, b1))

    A = parameter_interval(a0, a1)
    B = parameter_interval(b0, b1)

    d0 = parameter_interval(F(1, 1 + a1 + b1), F(1, 1 + a0 + b0))
    d1 = parameter_interval(F(1, 1 + b1), F(1, 1 + b0))
    d2 = parameter_interval(F(1, 1 + a1), F(1, 1 + a0))
    d3 = ONE

    rows = (
        (F(1), F(-1, 2), F(-1, 2), F(1, 4)),
        (F(1), F(1, 2), F(-1, 2), F(-1, 4)),
        (F(1), F(-1, 2), F(1, 2), F(-1, 4)),
        (F(1), F(1, 2), F(1, 2), F(1, 4)),
    )
    weights = (d0, d1, d2, d3)

    # Complete selected-event Fisher block.
    Y = [[ZERO for _ in range(4)] for _ in range(4)]
    for z in range(4):
        for i in range(4):
            for j in range(4):
                Y[i][j] = Y[i][j] + F(1, 4) * rows[z][i] * rows[z][j] * weights[z]

    # Full retained acceleration block. lambda=-H and n=(1+(a+b)/2)H.
    Y[1][1] = Y[1][1] + ell / (8 * A)
    Y[2][2] = Y[2][2] + kval / (8 * B)
    Y[1][3] = Y[1][3] + H / (32 * A)
    Y[3][1] = Y[1][3]
    Y[2][3] = Y[2][3] + H / (32 * B)
    Y[3][2] = Y[2][3]
    nval = (ONE + (A + B) / 2) * H
    Y[3][3] = Y[3][3] + nval / (32 * A * B)

    C = (
        (-ell, ZERO, -H / 4, ZERO),
        (-kval, -H / 4, ZERO, ZERO),
    )
    L = ((2 * A * ell, J), (J, 2 * B * kval))

    M = [[ZERO for _ in range(6)] for _ in range(6)]
    for i in range(4):
        for j in range(4):
            M[i][j] = Y[i][j]
    for i in range(2):
        for j in range(4):
            M[4 + i][j] = C[i][j]
            M[j][4 + i] = C[i][j]
    for i in range(2):
        for j in range(2):
            M[4 + i][4 + j] = L[i][j]
    return M


def evaluate_midpoint_form(a: float, b: float) -> list[list[float]]:
    """Floating evaluation used only to choose a rational preconditioner."""
    u, v, w = math.log1p(a), math.log1p(b), math.log1p(a + b)
    H = u + v - w
    ell, kval = u - H / 2, v - H / 2
    J = (1 + a + b) * w - (1 + a) * u - (1 + b) * v
    nval = (1 + (a + b) / 2) * H

    rows = (
        (1.0, -0.5, -0.5, 0.25),
        (1.0, 0.5, -0.5, -0.25),
        (1.0, -0.5, 0.5, -0.25),
        (1.0, 0.5, 0.5, 0.25),
    )
    weights = (1 / (1 + a + b), 1 / (1 + b), 1 / (1 + a), 1.0)
    Y = [[0.0] * 4 for _ in range(4)]
    for z in range(4):
        for i in range(4):
            for j in range(4):
                Y[i][j] += 0.25 * weights[z] * rows[z][i] * rows[z][j]
    Y[1][1] += ell / (8 * a)
    Y[2][2] += kval / (8 * b)
    Y[1][3] += H / (32 * a)
    Y[3][1] = Y[1][3]
    Y[2][3] += H / (32 * b)
    Y[3][2] = Y[2][3]
    Y[3][3] += nval / (32 * a * b)

    C = ((-ell, 0.0, -H / 4, 0.0), (-kval, -H / 4, 0.0, 0.0))
    L = ((2 * a * ell, J), (J, 2 * b * kval))
    M = [[0.0] * 6 for _ in range(6)]
    for i in range(4):
        for j in range(4):
            M[i][j] = Y[i][j]
    for i in range(2):
        for j in range(4):
            M[4 + i][j] = M[j][4 + i] = C[i][j]
    for i in range(2):
        for j in range(2):
            M[4 + i][4 + j] = L[i][j]
    return M


def cholesky(A: list[list[float]]) -> list[list[float]]:
    n = len(A)
    L = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            value = A[i][j] - sum(L[i][k] * L[j][k] for k in range(j))
            if i == j:
                if value <= 0:
                    raise AssertionError("midpoint heuristic was not SPD")
                L[i][j] = math.sqrt(value)
            else:
                L[i][j] = value / L[j][j]
    return L


def inverse_lower(L: list[list[float]]) -> list[list[float]]:
    n = len(L)
    X = [[0.0] * n for _ in range(n)]
    for col in range(n):
        for i in range(n):
            rhs = 1.0 if i == col else 0.0
            X[i][col] = (
                rhs - sum(L[i][k] * X[k][col] for k in range(i))
            ) / L[i][i]
    return X


def rational_preconditioner(a: float, b: float) -> list[list[F]]:
    L = cholesky(evaluate_midpoint_form(a, b))
    Linv = inverse_lower(L)
    # P=L^{-T}; quantization is part of the exact certificate.
    P = [[Linv[j][i] for j in range(6)] for i in range(6)]
    result = [
        [F(round(P[i][j] * PRECOND_SCALE), PRECOND_SCALE) for j in range(6)]
        for i in range(6)
    ]
    # P is exactly upper triangular with a strictly positive rational diagonal.
    for i in range(6):
        if result[i][i] <= 0:
            raise AssertionError("singular rational preconditioner")
        for j in range(i):
            if result[i][j] != 0:
                raise AssertionError("preconditioner lost triangularity")
    return result


def congruence(M: list[list[Interval]], P: list[list[F]]) -> list[list[Interval]]:
    n = 6
    temp = [[ZERO for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            value = ZERO
            for k in range(n):
                value = value + M[i][k] * P[k][j]
            temp[i][j] = value

    B = [[ZERO for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            value = ZERO
            for k in range(n):
                value = value + P[k][i] * temp[k][j]
            B[i][j] = value
    return B


def diagonal_dominance_margin(B: list[list[Interval]]) -> int:
    """Return a SCALE-scaled lower bound for lambda_min(B)."""
    bounds = []
    for i in range(6):
        radius = sum(B[i][j].max_abs_scaled() for j in range(6) if j != i)
        bounds.append(B[i][i].lo - radius)
    return min(bounds)


def r_to_a(r: F) -> F:
    return r / (1 - r)


def certify_box(r0: F, r1: F, s0: F, s1: F) -> int:
    a0, a1 = r_to_a(r0), r_to_a(r1)
    b0, b1 = r_to_a(s0), r_to_a(s1)
    rc, sc = (r0 + r1) / 2, (s0 + s1) / 2
    P = rational_preconditioner(float(r_to_a(rc)), float(r_to_a(sc)))
    M = full_form_interval(a0, a1, b0, b1)
    return diagonal_dominance_margin(congruence(M, P))


def main() -> None:
    start = time.perf_counter()
    step = (R_HI - R_LO) / GRID
    edges = [R_LO + i * step for i in range(GRID + 1)]

    minimum: int | None = None
    minimum_box: tuple[int, int] | None = None
    boxes = 0
    for i in range(GRID):
        for j in range(GRID):
            margin = certify_box(edges[i], edges[i + 1], edges[j], edges[j + 1])
            boxes += 1
            if margin <= 0:
                raise AssertionError(f"uncertified box {(i, j)}: margin={margin}")
            if minimum is None or margin < minimum:
                minimum = margin
                minimum_box = (i, j)

    assert minimum is not None and minimum_box is not None and boxes == GRID * GRID
    i, j = minimum_box
    a0, a1 = r_to_a(edges[i]), r_to_a(edges[i + 1])
    b0, b1 = r_to_a(edges[j]), r_to_a(edges[j + 1])
    elapsed = time.perf_counter() - start
    peak_kib = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    print("OBJECT=integrated complete-event occupied-side Hessian")
    print("PATH=true affine K+tD; all six real-symmetric physical directions")
    print("NORMALIZED_DOMAIN=1/4 <= a=A/q <= 4, 1/4 <= b=B/q <= 4")
    print(f"R_GRID=[1/5,4/5], GRID={GRID}x{GRID}, BOXES={boxes}")
    print(f"FIXED_POINT_BITS={FIX_BITS}, PRECONDITIONER_BITS={PRECOND_BITS}")
    print(f"LOG_ATANH_TERMS={LOG_TERMS}, exact positive-series tail retained")
    print("CERTIFICATE=for each box, exact rational P is nonsingular and")
    print("P^T M(a,b) P is uniformly strictly diagonally dominant with positive diagonal")
    print(f"MIN_GERSHGORIN_MARGIN_SCALED={minimum}")
    print(f"MIN_GERSHGORIN_MARGIN={minimum}/{SCALE}")
    print(f"MIN_MARGIN_BOX_INDEX={minimum_box}")
    print(f"MIN_MARGIN_A_INTERVAL=[{a0},{a1}]")
    print(f"MIN_MARGIN_B_INTERVAL=[{b0},{b1}]")
    print(f"MIN_MARGIN_DECIMAL={minimum / SCALE:.17g}")
    print("PASS: full 1024-box continuum square certified; M(a,b)>0 everywhere")
    print("CONCLUSION: E(a,b)>0 and integrated G1'' is positive definite on the square")
    print("NONCLAIM: no pointwise-in-r resolvent positivity and no all-a,b theorem")
    print(f"WALL_SECONDS={elapsed:.6f}")
    print(f"PEAK_RSS_KIB={peak_kib}")


if __name__ == "__main__":
    main()
