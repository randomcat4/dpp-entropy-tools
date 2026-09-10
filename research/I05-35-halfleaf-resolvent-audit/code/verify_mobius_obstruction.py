#!/usr/bin/env python3
"""Fresh exact audit of a pointwise-resolvent claim for a strict half-leaf DPP.

This script does not import any earlier project checker. It starts from the
true affine matrix K+tD, reconstructs all eight complete-event polynomials by
the determinant/Mobius law, and differentiates the displayed rational
functional exactly.

It also gives rigorous rational intervals for the two one-sided logarithmic
Hessians and the full directional negative Shannon Hessian. Logarithms are
enclosed by a fixed atanh series with an explicit geometric tail.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, getcontext
from fractions import Fraction as F
from itertools import permutations, product
from typing import Dict, Iterable, List, Sequence, Tuple

NLOG = 32


# ---------- Exact univariate polynomials, low degree only ----------

Poly = List[F]


def trim(a: Poly) -> Poly:
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def padd(a: Sequence[F], b: Sequence[F]) -> Poly:
    out = [F(0)] * max(len(a), len(b))
    for i, x in enumerate(a):
        out[i] += x
    for i, x in enumerate(b):
        out[i] += x
    return trim(out)


def pscale(a: Sequence[F], c: F | int) -> Poly:
    c = F(c)
    return trim([c * x for x in a])


def pmul(a: Sequence[F], b: Sequence[F]) -> Poly:
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return trim(out)


def permutation_sign(p: Sequence[int]) -> int:
    inversions = sum(
        1 for i in range(len(p)) for j in range(i + 1, len(p)) if p[i] > p[j]
    )
    return -1 if inversions & 1 else 1


def determinant_polynomial(matrix: Sequence[Sequence[Poly]]) -> Poly:
    n = len(matrix)
    out: Poly = [F(0)]
    for perm in permutations(range(n)):
        term: Poly = [F(1)]
        for i, j in enumerate(perm):
            term = pmul(term, matrix[i][j])
        out = padd(out, pscale(term, permutation_sign(perm)))
    return out


def jets(poly: Sequence[F]) -> Tuple[F, F, F]:
    """Return value, first derivative, second derivative at t=0."""
    return (
        poly[0],
        poly[1] if len(poly) > 1 else F(0),
        2 * poly[2] if len(poly) > 2 else F(0),
    )


# ---------- Outward rational intervals and certified logarithms ----------

@dataclass(frozen=True)
class Interval:
    lo: F
    hi: F

    def __post_init__(self) -> None:
        if self.lo > self.hi:
            raise ValueError("reversed interval")

    @staticmethod
    def point(x: F | int) -> "Interval":
        x = F(x)
        return Interval(x, x)

    def __add__(self, other: "Interval" | F | int) -> "Interval":
        other = other if isinstance(other, Interval) else Interval.point(other)
        return Interval(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self) -> "Interval":
        return Interval(-self.hi, -self.lo)

    def __sub__(self, other: "Interval" | F | int) -> "Interval":
        other = other if isinstance(other, Interval) else Interval.point(other)
        return self + (-other)

    def __rsub__(self, other: "Interval" | F | int) -> "Interval":
        return Interval.point(other) - self

    def __mul__(self, other: "Interval" | F | int) -> "Interval":
        other = other if isinstance(other, Interval) else Interval.point(other)
        values = (
            self.lo * other.lo,
            self.lo * other.hi,
            self.hi * other.lo,
            self.hi * other.hi,
        )
        return Interval(min(values), max(values))

    __rmul__ = __mul__


def log_unit_interval(y: F, n: int = NLOG) -> Interval:
    """Enclose log(y) for 1 <= y <= 2.

    log(y)=2*atanh((y-1)/(y+1)). The omitted positive terms are bounded
    geometrically using 1/(2j+1) <= 1/(2n+1).
    """
    if not F(1) <= y <= F(2):
        raise ValueError("unit logarithm argument outside [1,2]")
    w = (y - 1) / (y + 1)
    partial = F(0)
    for j in range(n):
        partial += 2 * w ** (2 * j + 1) / (2 * j + 1)
    tail = 2 * w ** (2 * n + 1) / ((2 * n + 1) * (1 - w * w))
    return Interval(partial, partial + tail)


_LOG2 = log_unit_interval(F(2))


def log_fraction(x: F) -> Interval:
    if x <= 0:
        raise ValueError("logarithm argument must be positive")
    y = x
    k = 0
    while y < 1:
        y *= 2
        k -= 1
    while y > 2:
        y /= 2
        k += 1
    return log_unit_interval(y) + k * _LOG2


def decimal(x: F, digits: int = 70) -> str:
    getcontext().prec = digits
    return str(Decimal(x.numerator) / Decimal(x.denominator))


def show_interval(name: str, value: Interval, digits: int = 55) -> None:
    print(f"{name}: [{decimal(value.lo, digits)}, {decimal(value.hi, digits)}]")


# ---------- Frozen exact physical input ----------

A = F(1, 4)
B = F(16, 25)
q = F(109, 1000)
qbar = F(1, 1000)
sqrt_A = F(1, 2)
sqrt_B = F(4, 5)
sqrt_AB = F(2, 5)
b = F(1, 4)
c = F(2, 5)
z = q + (A + B) / 2

K: List[List[F]] = [
    [F(1, 2), F(0), b],
    [F(0), F(1, 2), c],
    [b, c, z],
]

d11, d22, d33, d12, d13, d23 = map(F, (-18, -72, 40, 146, 108, 5))
D: List[List[F]] = [
    [d11, d12, d13],
    [d12, d22, d23],
    [d13, d23, d33],
]
r = F(1, 50000)


def complete_event_polynomial(bits: Tuple[int, int, int]) -> Poly:
    """p_bits(t)=(-1)^|Z| det(K+tD-I_Z), Z={j: bits[j]=0}."""
    matrix: List[List[Poly]] = []
    zero_count = 0
    for i in range(3):
        row: List[Poly] = []
        for j in range(3):
            base = K[i][j]
            if i == j and bits[i] == 0:
                base -= 1
            row.append([base, D[i][j]])
        matrix.append(row)
        if bits[i] == 0:
            zero_count += 1
    sign = -1 if zero_count & 1 else 1
    return pscale(determinant_polynomial(matrix), sign)


events: Dict[Tuple[int, int, int], Poly] = {
    bits: complete_event_polynomial(bits) for bits in product((0, 1), repeat=3)
}


def sum_polys(polys: Iterable[Sequence[F]]) -> Poly:
    out: Poly = [F(0)]
    for p in polys:
        out = padd(out, p)
    return out


normalization = sum_polys(events.values())
assert normalization == [F(1)]
assert all(poly[0] > 0 for poly in events.values())

# The strict half-leaf conditions are transparent and imply K,I-K > 0.
assert A > 0 and B > 0 and q > 0 and qbar > 0
assert A + B + q + qbar == 1
assert b * b == A / 4 and c * c == B / 4

leaf: Dict[Tuple[int, int], Dict[str, Poly]] = {}
for i, j in product((0, 1), repeat=2):
    selected = events[(i, j, 1)]
    vacant = events[(i, j, 0)]
    leaf[(i, j)] = {
        "selected": selected,
        "vacant": vacant,
        "P": padd(selected, vacant),
    }


def quotient_jets(
    numerator: Tuple[F, F, F], denominator: Tuple[F, F, F]
) -> Tuple[F, F, F]:
    n0, n1, n2 = numerator
    d0, d1, d2 = denominator
    return (
        n0 / d0,
        n1 / d0 - n0 * d1 / d0**2,
        n2 / d0 - 2 * n1 * d1 / d0**2
        - n0 * d2 / d0**2 + 2 * n0 * d1**2 / d0**3,
    )


# Cross-check the direct event quotient against an independently derived
# Schur-complement formula. This is not used in the Phi calculation below.
conditional_jets: Dict[Tuple[int, int], Tuple[F, F, F]] = {}
for i, j in product((0, 1), repeat=2):
    s1 = F(1 if i else -1)
    s2 = F(1 if j else -1)
    direct = quotient_jets(jets(leaf[(i, j)]["selected"]), jets(leaf[(i, j)]["P"]))

    t0 = q + A * (1 - s1) / 2 + B * (1 - s2) / 2
    t1 = (
        d33 + A * d11 + B * d22
        + 2 * s1 * s2 * sqrt_AB * d12
        - 2 * s1 * sqrt_A * d13
        - 2 * s2 * sqrt_B * d23
    )
    e1 = d13 - (s1 * sqrt_A * d11 + s2 * sqrt_B * d12)
    e2 = d23 - (s1 * sqrt_A * d12 + s2 * sqrt_B * d22)
    t2 = -4 * (s1 * e1 * e1 + s2 * e2 * e2)
    assert direct == (t0, t1, t2)
    conditional_jets[(i, j)] = direct

    P0, P1, P2 = jets(leaf[(i, j)]["P"])
    assert P0 == F(1, 4)
    assert P1 == (s1 * d11 + s2 * d22) / 2
    assert P2 == 2 * s1 * s2 * (d11 * d22 - d12 * d12)


def quotient_second(
    n0: F, n1: F, n2: F, d0: F, d1: F, d2: F
) -> F:
    return (
        n2 / d0 - 2 * n1 * d1 / d0**2
        - n0 * d2 / d0**2 + 2 * n0 * d1**2 / d0**3
    )


# Direct Mobius-event evaluation of
#   Phi_r = sum_{i,j} P_ij(t)^2 / (p_ij1(t)+r P_ij(t)).
# No conditional-probability formula is used in this differentiation.
phi_second = F(0)
for i, j in product((0, 1), repeat=2):
    P0, P1, P2 = jets(leaf[(i, j)]["P"])
    p0, p1, p2 = jets(leaf[(i, j)]["selected"])
    n0 = P0 * P0
    n1 = 2 * P0 * P1
    n2 = 2 * (P1 * P1 + P0 * P2)
    d0 = p0 + r * P0
    d1 = p1 + r * P1
    d2 = p2 + r * P2
    phi_second += quotient_second(n0, n1, n2, d0, d1, d2)

EXPECTED_NUMERATOR = -47488558049748267993080620088778228551027375300000000000
EXPECTED_DENOMINATOR = 2044542058422113103788725284171055940635901533282467
assert phi_second == F(EXPECTED_NUMERATOR, EXPECTED_DENOMINATOR)
assert phi_second < 0


def side_log_hessian(side: int) -> Interval:
    """Rigorous interval for sum p log(p/P), twice differentiated."""
    total = Interval.point(0)
    for i, j in product((0, 1), repeat=2):
        p0, p1, p2 = jets(events[(i, j, side)])
        P0, P1, P2 = jets(leaf[(i, j)]["P"])
        ratio = p0 / P0

        # [p log(p/P)]'' =
        # p'^2/p - 2p'P'/P - pP''/P + p(P')^2/P^2
        # + p''(log(p/P)+1).
        rational_part = (
            p1 * p1 / p0
            - 2 * p1 * P1 / P0
            - p0 * P2 / P0
            + p0 * P1 * P1 / P0**2
            + p2
        )
        total += Interval.point(rational_part) + p2 * log_fraction(ratio)
    return total


G1_second = side_log_hessian(1)
G0_second = side_log_hessian(0)
marginal_second = 4 * (d11 * d11 + d22 * d22)
full_negative_entropy_second = (
    G1_second + G0_second + Interval.point(marginal_second)
)

assert G1_second.lo > 0
assert G0_second.lo > 0
assert full_negative_entropy_second.lo > 0


print("FROZEN_INPUT")
print("A=1/4, B=16/25, q=109/1000, qbar=1/1000")
print("K=[[1/2,0,1/4],[0,1/2,2/5],[1/4,2/5,277/500]]")
print("D=[[-18,146,108],[146,-72,5],[108,5,40]]")
print("r=1/50000")
print(f"LOG_SERIES_TERMS={NLOG}")
print("COMPLETE_EVENT_POLYNOMIALS_COEFFICIENTS")
for bits in product((0, 1), repeat=3):
    coeffs = ",".join(f"{x.numerator}/{x.denominator}" for x in events[bits])
    print(f"p_{bits[0]}{bits[1]}{bits[2]}=[{coeffs}]")
print("CONDITIONAL_JETS_VALUE_FIRST_SECOND")
for i, j in product((0, 1), repeat=2):
    values = ",".join(
        f"{x.numerator}/{x.denominator}" for x in conditional_jets[(i, j)]
    )
    print(f"q_{i}{j}=[{values}]")
print("PASS: all 8 complete-event polynomials reconstructed from true K+tD")
print("PASS: exact event normalization through determinant degree")
print("PASS: all 8 center probabilities strictly positive")
print("PASS: direct Mobius quotient jets equal independent Schur jets")
print("PHI_R_SECOND_EXACT=")
print(f"{phi_second.numerator}/{phi_second.denominator}")
print(f"PHI_R_SECOND_DECIMAL={decimal(phi_second, 60)}")
print("PASS: universal pointwise Phi_r''>0 claim is false")
show_interval("G1_SECOND_INTERVAL", G1_second)
show_interval("G0_SECOND_INTERVAL", G0_second)
print(f"LEAF_MARGINAL_NEGATIVE_HESSIAN={marginal_second}")
show_interval("FULL_NEGATIVE_ENTROPY_SECOND_INTERVAL", full_negative_entropy_second)
print("PASS: same direction is not a one-sided or full Shannon counterexample")
print("CLASSIFICATION=EXACT_POINTWISE_RESOLVENT_METHOD_COUNTEREXAMPLE")
print("REVIEW_STATUS=FRESH_SAME-AUTHOR_RECONSTRUCTION_PENDING_EXTERNAL_REVIEW")
