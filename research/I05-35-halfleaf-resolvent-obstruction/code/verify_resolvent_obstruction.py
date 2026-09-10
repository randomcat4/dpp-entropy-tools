#!/usr/bin/env python3
"""Independent exact checkpoint for the half-leaf pointwise resolvent obstruction.

Standard library only. The checker starts from the true affine kernel K+tD,
reconstructs every complete event twice (principal-minor Mobius inversion and
shifted determinant), groups the leaf marginals, differentiates the rational
resolvent directly, and encloses logarithmic curvatures by a rational atanh tail.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import combinations
from typing import Dict, Iterable, List, Sequence, Tuple

N = 3
LOG_TERMS = 60
Poly = Tuple[Q, Q, Q, Q]
ZERO: Poly = (Q(0), Q(0), Q(0), Q(0))
ONE: Poly = (Q(1), Q(0), Q(0), Q(0))


def poly_affine(x: Q | int, dx: Q | int) -> Poly:
    return (Q(x), Q(dx), Q(0), Q(0))


def padd(a: Poly, b: Poly) -> Poly:
    return tuple(a[i] + b[i] for i in range(4))  # type: ignore[return-value]


def pneg(a: Poly) -> Poly:
    return tuple(-x for x in a)  # type: ignore[return-value]


def psub(a: Poly, b: Poly) -> Poly:
    return padd(a, pneg(b))


def pmul(a: Poly, b: Poly) -> Poly:
    out = [Q(0)] * 4
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if i + j < 4:
                out[i + j] += x * y
    return tuple(out)  # type: ignore[return-value]


def pscale(a: Poly, c: Q | int) -> Poly:
    c = Q(c)
    return tuple(c * x for x in a)  # type: ignore[return-value]


def det_poly(M: Sequence[Sequence[Poly]]) -> Poly:
    n = len(M)
    if n == 0:
        return ONE
    if n == 1:
        return M[0][0]
    if n == 2:
        return psub(pmul(M[0][0], M[1][1]), pmul(M[0][1], M[1][0]))
    if n != 3:
        raise ValueError("only sizes 0..3 are used")
    pos = padd(
        padd(pmul(pmul(M[0][0], M[1][1]), M[2][2]),
             pmul(pmul(M[0][1], M[1][2]), M[2][0])),
        pmul(pmul(M[0][2], M[1][0]), M[2][1]),
    )
    neg = padd(
        padd(pmul(pmul(M[0][2], M[1][1]), M[2][0]),
             pmul(pmul(M[0][1], M[1][0]), M[2][2])),
        pmul(pmul(M[0][0], M[1][2]), M[2][1]),
    )
    return psub(pos, neg)


def principal_minor(K: Sequence[Sequence[Poly]], subset: Tuple[int, ...]) -> Poly:
    return det_poly([[K[i][j] for j in subset] for i in subset])


def powerset(xs: Sequence[int]) -> Iterable[Tuple[int, ...]]:
    for k in range(len(xs) + 1):
        yield from combinations(xs, k)


def mobius_events(K: Sequence[Sequence[Poly]]) -> Dict[Tuple[int, ...], Poly]:
    vertices = tuple(range(N))
    minors = {S: principal_minor(K, S) for S in powerset(vertices)}
    events: Dict[Tuple[int, ...], Poly] = {}
    for R in powerset(vertices):
        comp = tuple(i for i in vertices if i not in R)
        val = ZERO
        for T in powerset(comp):
            U = tuple(sorted(R + T))
            val = padd(val, pscale(minors[U], -1 if len(T) % 2 else 1))
        events[R] = val
    return events


def shifted_events(K: Sequence[Sequence[Poly]]) -> Dict[Tuple[int, ...], Poly]:
    vertices = tuple(range(N))
    events: Dict[Tuple[int, ...], Poly] = {}
    for R in powerset(vertices):
        zeros = set(vertices) - set(R)
        M = [[K[i][j] for j in vertices] for i in vertices]
        M = [row[:] for row in M]
        for i in zeros:
            M[i][i] = psub(M[i][i], ONE)
        events[R] = pscale(det_poly(M), -1 if len(zeros) % 2 else 1)
    return events


def jets(p: Poly) -> Tuple[Q, Q, Q]:
    return p[0], p[1], 2 * p[2]


def ratio_jets(n: Tuple[Q, Q, Q], d: Tuple[Q, Q, Q]) -> Tuple[Q, Q, Q]:
    n0, n1, n2 = n
    d0, d1, d2 = d
    q0 = n0 / d0
    q1 = n1 / d0 - n0 * d1 / d0**2
    q2 = n2 / d0 - n0 * d2 / d0**2 - 2 * n1 * d1 / d0**2 + 2 * n0 * d1**2 / d0**3
    return q0, q1, q2


@dataclass(frozen=True)
class Interval:
    lo: Q
    hi: Q

    def __post_init__(self) -> None:
        if self.lo > self.hi:
            raise ValueError("reversed interval")

    @staticmethod
    def point(x: Q | int) -> "Interval":
        x = Q(x)
        return Interval(x, x)

    def __add__(self, other: "Interval" | Q | int) -> "Interval":
        if not isinstance(other, Interval):
            other = Interval.point(other)
        return Interval(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def scale(self, c: Q | int) -> "Interval":
        c = Q(c)
        if c >= 0:
            return Interval(c * self.lo, c * self.hi)
        return Interval(c * self.hi, c * self.lo)


def atanh_log_unit(y: Q, terms: int = LOG_TERMS) -> Interval:
    if not (Q(1) <= y <= Q(2)):
        raise ValueError(f"range reduction failed: {y}")
    w = (y - 1) / (y + 1)
    partial = Q(0)
    wpow = w
    for k in range(terms):
        partial += 2 * wpow / (2 * k + 1)
        wpow *= w * w
    tail = 2 * w ** (2 * terms + 1) / ((2 * terms + 1) * (1 - w * w))
    return Interval(partial, partial + tail)


LOG2 = atanh_log_unit(Q(2))


def log_interval(x: Q) -> Interval:
    if x <= 0:
        raise ValueError("log argument not positive")
    y = x
    k = 0
    while y < 1:
        y *= 2
        k -= 1
    while y > 2:
        y /= 2
        k += 1
    return atanh_log_unit(y) + LOG2.scale(k)


def side_curvature(leaf_data: Sequence[Tuple[Tuple[Q,Q,Q], Tuple[Q,Q,Q]]], occupied: bool) -> Interval:
    total = Interval.point(0)
    for Pj, pj in leaf_data:
        x0, x1, x2 = ratio_jets(pj, Pj)
        if not occupied:
            x0, x1, x2 = 1 - x0, -x1, -x2
        P0, P1, P2 = Pj
        lx = log_interval(x0)
        total += lx.scale(P2 * x0)
        total += (lx + 1).scale(2 * P1 * x1)
        total += Interval.point(P0 * x1 * x1 / x0)
        total += (lx + 1).scale(P0 * x2)
    return total


def full_negative_entropy_curvature(events: Dict[Tuple[int,...], Poly]) -> Interval:
    ans = Interval.point(0)
    for p in events.values():
        p0, p1, p2 = jets(p)
        ans += Interval.point(p1 * p1 / p0)
        ans += log_interval(p0).scale(p2)
    return ans


def dec(x: Q, digits: int = 30) -> str:
    sign = "-" if x < 0 else ""
    x = abs(x)
    n, d = x.numerator, x.denominator
    whole, rem = divmod(n, d)
    ds = []
    for _ in range(digits):
        rem *= 10
        digit, rem = divmod(rem, d)
        ds.append(str(digit))
    return f"{sign}{whole}." + "".join(ds)


def main() -> None:
    A = Q(1, 4)
    B = Q(16, 25)
    q = Q(109, 1000)
    qbar = Q(1, 1000)
    r = Q(1, 50000)
    b = Q(1, 4)
    c = Q(2, 5)
    z = q + (A + B) / 2
    assert 1 - A - B - q == qbar
    Dvals = (Q(-18), Q(-72), Q(40), Q(146), Q(108), Q(5))
    d11, d22, d33, d12, d13, d23 = Dvals

    K0 = ((Q(1,2), Q(0), b), (Q(0), Q(1,2), c), (b, c, z))
    D0 = ((d11,d12,d13),(d12,d22,d23),(d13,d23,d33))
    K: List[List[Poly]] = [[poly_affine(K0[i][j], D0[i][j]) for j in range(3)] for i in range(3)]

    mob = mobius_events(K)
    shifted = shifted_events(K)
    assert mob == shifted
    assert len(mob) == 8
    assert all(p[0] > 0 for p in mob.values())
    total = ZERO
    for p in mob.values():
        total = padd(total, p)
    assert total == ONE

    leaf_data: List[Tuple[Tuple[Q,Q,Q], Tuple[Q,Q,Q]]] = []
    phi2 = Q(0)
    for x1 in (0,1):
        for x2 in (0,1):
            R0 = tuple(i for i,bit in enumerate((x1,x2,0)) if bit)
            R1 = tuple(i for i,bit in enumerate((x1,x2,1)) if bit)
            p0poly, p1poly = mob[R0], mob[R1]
            Ppoly = padd(p0poly, p1poly)
            Pj, pj = jets(Ppoly), jets(p1poly)
            leaf_data.append((Pj,pj))
            P0,P1,P2=Pj
            p0,p1,p2=pj
            n0=P0*P0
            n1=2*P0*P1
            n2=2*(P1*P1+P0*P2)
            h0=p0+r*P0
            h1=p1+r*P1
            h2=p2+r*P2
            phi2 += n2/h0 - 2*n1*h1/h0**2 - n0*h2/h0**2 + 2*n0*h1**2/h0**3

            s1=2*x1-1; s2=2*x2-1
            ts=q+A*Q(1-s1,2)+B*Q(1-s2,2)
            assert P0 == Q(1,4) and p0 == P0*ts
            assert P1 == Q(s1*d11+s2*d22,2)
            assert P2 == 2*s1*s2*(d11*d22-d12*d12)
            qp=d33+A*d11+B*d22+2*s1*s2*Q(2,5)*d12-2*s1*Q(1,2)*d13-2*s2*Q(4,5)*d23
            e1=d13-(s1*Q(1,2)*d11+s2*Q(4,5)*d12)
            e2=d23-(s1*Q(1,2)*d12+s2*Q(4,5)*d22)
            qpp=-4*(s1*e1*e1+s2*e2*e2)
            assert ratio_jets(pj,Pj) == (ts,qp,qpp)

    expected = Q(
        -47488558049748267993080620088778228551027375300000000000,
         2044542058422113103788725284171055940635901533282467,
    )
    assert phi2 == expected and phi2 < 0

    G1 = side_curvature(leaf_data, occupied=True)
    G0 = side_curvature(leaf_data, occupied=False)
    marginal = 4*(d11*d11+d22*d22)
    decomposed = G1 + G0 + marginal
    direct_full = full_negative_entropy_curvature(mob)
    assert G1.lo > 0 and G0.lo > 0 and decomposed.lo > 0 and direct_full.lo > 0
    assert not (decomposed.hi < direct_full.lo or direct_full.hi < decomposed.lo)

    print("INPUT")
    print(f"A={A}, B={B}, q={q}, qbar={qbar}, r={r}")
    print(f"K=[[1/2,0,{b}],[0,1/2,{c}],[{b},{c},{z}]]")
    print("D=(d11,d22,d33,d12,d13,d23)=(-18,-72,40,146,108,5)")
    print(f"LOG_TERMS={LOG_TERMS}")
    print("PASS: all 8 complete-event polynomials reconstructed by principal-minor Mobius inversion")
    print("PASS: all 8 Mobius events equal the independently shifted determinant formula")
    print("PASS: normalization polynomial is identically 1 and all 8 center atoms are positive")
    print("PASS: grouped leaf and conditional jets equal the independent Schur formulas")
    print(f"PHI_R_SECOND_EXACT={phi2.numerator}/{phi2.denominator}")
    print(f"PHI_R_SECOND_DECIMAL={dec(phi2,35)}")
    print("PASS: pointwise universal Phi_r'' >= 0 claim is false on a true six-direction K-affine line")
    print(f"G1_SECOND_INTERVAL=[{dec(G1.lo,35)},{dec(G1.hi,35)}]")
    print(f"G0_SECOND_INTERVAL=[{dec(G0.lo,35)},{dec(G0.hi,35)}]")
    print(f"LEAF_MARGINAL_NEGATIVE_HESSIAN={marginal}")
    print(f"DECOMPOSED_FULL_NEGATIVE_HESSIAN_INTERVAL=[{dec(decomposed.lo,35)},{dec(decomposed.hi,35)}]")
    print(f"DIRECT_8_EVENT_NEGATIVE_HESSIAN_INTERVAL=[{dec(direct_full.lo,35)},{dec(direct_full.hi,35)}]")
    print("PASS: this witness is a pointwise-resolvent METHOD obstruction, not an entropy counterexample")
    print("ALL I05-35 INDEPENDENT CHECKS PASSED")


if __name__ == "__main__":
    main()
