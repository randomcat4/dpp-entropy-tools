#!/usr/bin/env python3
"""Exact/rational-log certificate for an actual half-leaf method obstruction.

This script uses only the Python standard library.  It
  * reconstructs all eight complete-event jets by Mobius inversion;
  * checks the exact six-coordinate corner quadratic against those jets;
  * rigorously encloses the accepted parallel-edge criterion at one rational K;
  * proves that criterion fails while the full complete-event Hessian is positive.

Natural logarithms are enclosed by a fixed atanh series with a rational tail.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, getcontext
from fractions import Fraction as F
from itertools import permutations
from typing import Dict, Iterable, List, Sequence, Tuple
import sys
sys.set_int_max_str_digits(0)

NLOG = 24
DIM = 6


@dataclass(frozen=True)
class I:
    lo: F
    hi: F

    def __post_init__(self) -> None:
        if self.lo > self.hi:
            raise ValueError("reversed interval")

    @staticmethod
    def point(x: F | int) -> "I":
        x = F(x)
        return I(x, x)

    def __add__(self, other: "I" | F | int) -> "I":
        other = other if isinstance(other, I) else I.point(other)
        return I(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self) -> "I":
        return I(-self.hi, -self.lo)

    def __sub__(self, other: "I" | F | int) -> "I":
        other = other if isinstance(other, I) else I.point(other)
        return self + (-other)

    def __rsub__(self, other: "I" | F | int) -> "I":
        return I.point(other) - self

    def __mul__(self, other: "I" | F | int) -> "I":
        other = other if isinstance(other, I) else I.point(other)
        vals = (
            self.lo * other.lo,
            self.lo * other.hi,
            self.hi * other.lo,
            self.hi * other.hi,
        )
        return I(min(vals), max(vals))

    __rmul__ = __mul__

    def reciprocal(self) -> "I":
        if self.lo <= 0 <= self.hi:
            raise ZeroDivisionError("interval contains zero")
        return I(F(1, 1) / self.hi, F(1, 1) / self.lo)

    def __truediv__(self, other: "I" | F | int) -> "I":
        other = other if isinstance(other, I) else I.point(other)
        return self * other.reciprocal()

    def square(self) -> "I":
        if self.lo >= 0:
            return I(self.lo * self.lo, self.hi * self.hi)
        if self.hi <= 0:
            return I(self.hi * self.hi, self.lo * self.lo)
        return I(F(0), max(self.lo * self.lo, self.hi * self.hi))


def atanh_log_unit(y: F, n: int = NLOG) -> I:
    """Enclose log(y) for 1 <= y <= 2 by the atanh series."""
    if not (F(1) <= y <= F(2)):
        raise ValueError(y)
    w = (y - 1) / (y + 1)
    partial = F(0)
    wpow = w
    for j in range(n):
        partial += F(2) * wpow / (2 * j + 1)
        wpow *= w * w
    tail = F(2) * (w ** (2 * n + 1)) / ((2 * n + 1) * (1 - w * w))
    return I(partial, partial + tail)


_LOG2 = atanh_log_unit(F(2), NLOG)


def log_q(x: F, n: int = NLOG) -> I:
    if x <= 0:
        raise ValueError("log argument must be positive")
    y = x
    k = 0
    while y < 1:
        y *= 2
        k -= 1
    while y >= 2:
        y /= 2
        k += 1
    base = atanh_log_unit(y, n)
    return base + _LOG2 * k


def f_rat(t: F) -> F:
    return F(1) / (t * (1 - t))


def logit_edge(u: F, s: F) -> I:
    v = u + s
    return log_q(v * (1 - u) / (u * (1 - v)))


def psi_i(t: F) -> I:
    return log_q(t) * t + log_q(1 - t) * (1 - t)


def kappa_i(u: F, s: F) -> I:
    f0, f1 = f_rat(u), f_rat(u + s)
    h = logit_edge(u, s)
    m = h / s
    num = I.point(f0 * f1) - m.square()
    den = (I.point(f0 + f1) - m * 2) * 8
    if num.lo <= 0 or den.lo <= 0:
        raise AssertionError("failed positive edge gates")
    return num / den


def parallel_i(x: I, y: I) -> I:
    return x * y / (x + y)


@dataclass
class LA:
    const: F
    logs: Dict[F, F]

    @staticmethod
    def zero() -> "LA":
        return LA(F(0), {})

    @staticmethod
    def rational(x: F | int) -> "LA":
        return LA(F(x), {})

    @staticmethod
    def log(x: F, coeff: F | int = 1) -> "LA":
        return LA(F(0), {x: F(coeff)})

    def clean(self) -> "LA":
        self.logs = {k: v for k, v in self.logs.items() if v}
        return self

    def __add__(self, other: "LA" | F | int) -> "LA":
        other = other if isinstance(other, LA) else LA.rational(other)
        out = dict(self.logs)
        for k, v in other.logs.items():
            out[k] = out.get(k, F(0)) + v
        return LA(self.const + other.const, out).clean()

    __radd__ = __add__

    def __neg__(self) -> "LA":
        return LA(-self.const, {k: -v for k, v in self.logs.items()})

    def __sub__(self, other: "LA" | F | int) -> "LA":
        other = other if isinstance(other, LA) else LA.rational(other)
        return self + (-other)

    def scale(self, c: F | int) -> "LA":
        c = F(c)
        return LA(c * self.const, {k: c * v for k, v in self.logs.items()}).clean()

    def interval(self) -> I:
        ans = I.point(self.const)
        for x, c in self.logs.items():
            ans += log_q(x) * c
        return ans

    def key(self) -> Tuple[F, Tuple[Tuple[F, F], ...]]:
        return self.const, tuple(sorted(self.logs.items()))


def la_log_event(p: F) -> LA:
    return LA.log(p)


def la_logit_diff(v: F, u: F) -> LA:
    # Use event probabilities /4, so all log(4) constants cancel exactly.
    return (
        la_log_event(v / 4)
        - la_log_event((1 - v) / 4)
        - la_log_event(u / 4)
        + la_log_event((1 - u) / 4)
    )


def la_psi(t: F) -> LA:
    return la_log_event(t / 4).scale(t) + la_log_event((1 - t) / 4).scale(1 - t)


def zero_la_matrix(n: int) -> List[List[LA]]:
    return [[LA.zero() for _ in range(n)] for __ in range(n)]


def add_quadratic(M: List[List[LA]], i: int, j: int, c: LA | F | int) -> None:
    c = c if isinstance(c, LA) else LA.rational(c)
    if i == j:
        M[i][i] = M[i][i] + c
    else:
        half = c.scale(F(1, 2))
        M[i][j] = M[i][j] + half
        M[j][i] = M[j][i] + half


def corner_la_matrix(q: F, A: F, B: F) -> List[List[LA]]:
    t00, t10, t01, t11 = q + A + B, q + B, q + A, q
    fs = [f_rat(t00), f_rat(t10), f_rat(t01), f_rat(t11)]
    ap = la_logit_diff(t00, t10)
    am = la_logit_diff(t01, t11)
    bp = la_logit_diff(t00, t01)
    bm = la_logit_diff(t10, t11)
    J = la_psi(t00) + la_psi(t11) - la_psi(t01) - la_psi(t10)

    M = zero_la_matrix(DIM)
    add_quadratic(M, 0, 0, 4)
    add_quadratic(M, 1, 1, 4)
    add_quadratic(M, 0, 1, J.scale(2))
    cv = [0, 0, 1, -1, -1, 1]
    cell = J.scale(-F(1, 32) / (A * B))
    for i in range(DIM):
        for j in range(DIM):
            if cv[i] and cv[j]:
                M[i][j] = M[i][j] + cell.scale(cv[i] * cv[j])

    def add_edge(s: F, h: LA, X: int, Y: int, delta: int, p: F, r: F) -> None:
        add_quadratic(M, delta, delta, h.scale(s))
        add_quadratic(M, delta, X, h.scale(-F(1, 2)))
        add_quadratic(M, delta, Y, h.scale(-F(1, 2)))
        add_quadratic(M, X, X, h.scale(F(1, 16) / s) + p / 8)
        add_quadratic(M, Y, Y, h.scale(F(1, 16) / s) + r / 8)
        add_quadratic(M, X, Y, h.scale(-F(1, 8) / s))

    add_edge(A, ap, 2, 3, 0, fs[0], fs[1])
    add_edge(A, am, 4, 5, 0, fs[2], fs[3])
    add_edge(B, bp, 2, 4, 1, fs[0], fs[2])
    add_edge(B, bm, 3, 5, 1, fs[1], fs[3])
    return M


def poly_add(a: Sequence[F], b: Sequence[F], sign: int = 1) -> List[F]:
    n = max(len(a), len(b))
    out = [F(0)] * n
    for i, x in enumerate(a):
        out[i] += x
    for i, x in enumerate(b):
        out[i] += sign * x
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def poly_mul(a: Sequence[F], b: Sequence[F]) -> List[F]:
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def perm_sign(p: Sequence[int]) -> int:
    inv = sum(p[i] > p[j] for i in range(len(p)) for j in range(i + 1, len(p)))
    return -1 if inv % 2 else 1


def det_poly(K: Sequence[Sequence[F]], D: Sequence[Sequence[F]], inds: Sequence[int]) -> List[F]:
    n = len(inds)
    if n == 0:
        return [F(1)]
    ans = [F(0)]
    for p in permutations(range(n)):
        term = [F(1)]
        for i in range(n):
            r, c = inds[i], inds[p[i]]
            term = poly_mul(term, [K[r][c], D[r][c]])
        ans = poly_add(ans, term, perm_sign(p))
    return ans


def all_event_polys(K: Sequence[Sequence[F]], D: Sequence[Sequence[F]]) -> List[List[F]]:
    inclusion: List[List[F]] = []
    for mask in range(8):
        inds = [i for i in range(3) if mask >> i & 1]
        inclusion.append(det_poly(K, D, inds))
    events: List[List[F]] = []
    for S in range(8):
        p = [F(0)]
        for T in range(8):
            if T & S == S:
                sign = -1 if ((T.bit_count() - S.bit_count()) & 1) else 1
                p = poly_add(p, inclusion[T], sign)
        events.append(p)
    return events


def physical_direction(z: Sequence[F], A: F, B: F, b: F, c: F) -> List[List[F]]:
    d, e, T00, T10, T01, T11 = z
    m = (T00 + T10 + T01 + T11) / 4
    alpha = (T10 + T11 - T00 - T01) / 2
    beta = (T01 + T11 - T00 - T10) / 2
    gamma = T00 - T10 - T01 + T11
    D33 = m - A * d - B * e
    D13 = -b * alpha / (2 * A)
    D23 = -c * beta / (2 * B)
    D12 = b * c * gamma / (2 * A * B)
    return [
        [d, D12, D13],
        [D12, e, D23],
        [D13, D23, D33],
    ]


def q_event_la(K: Sequence[Sequence[F]], D: Sequence[Sequence[F]]) -> LA:
    ps = all_event_polys(K, D)
    total = LA.zero()
    p2sum = F(0)
    for poly in ps:
        poly = list(poly) + [F(0)] * (4 - len(poly))
        p0, p1, c2 = poly[0], poly[1], poly[2]
        p2 = 2 * c2
        if p0 <= 0:
            raise AssertionError("nonpositive complete event")
        total += F(p1 * p1, p0)
        total += la_log_event(p0).scale(p2)
        p2sum += p2
    if p2sum != 0:
        raise AssertionError("second-jet normalization failed")
    return total.clean()


def event_la_matrix(K: Sequence[Sequence[F]], A: F, B: F, b: F, c: F) -> List[List[LA]]:
    basis = [[F(int(i == j)) for i in range(DIM)] for j in range(DIM)]
    diag: List[LA] = []
    for z in basis:
        diag.append(q_event_la(K, physical_direction(z, A, B, b, c)))
    M = zero_la_matrix(DIM)
    for i in range(DIM):
        M[i][i] = diag[i]
    for i in range(DIM):
        for j in range(i + 1, DIM):
            z = [basis[i][k] + basis[j][k] for k in range(DIM)]
            qij = q_event_la(K, physical_direction(z, A, B, b, c))
            off = (qij - diag[i] - diag[j]).scale(F(1, 2))
            M[i][j] = M[j][i] = off
    return M


def interval_matrix(M: Sequence[Sequence[LA]]) -> List[List[I]]:
    return [[x.interval() for x in row] for row in M]


def det_interval(M: Sequence[Sequence[I]]) -> I:
    n = len(M)
    ans = I.point(0)
    for p in permutations(range(n)):
        term = I.point(1)
        for i in range(n):
            term *= M[i][p[i]]
        ans += term if perm_sign(p) > 0 else -term
    return ans


def decimal(x: F, digits: int = 40) -> str:
    getcontext().prec = digits + 10
    return format(Decimal(x.numerator) / Decimal(x.denominator), f".{digits}E")


def show_interval(name: str, x: I, raw: bool = False) -> None:
    print(f"{name}: [{decimal(x.lo)}, {decimal(x.hi)}]")
    if raw:
        print(f"{name}_RAW_LO={x.lo.numerator}/{x.lo.denominator}")
        print(f"{name}_RAW_HI={x.hi.numerator}/{x.hi.denominator}")


def main() -> None:
    # Rational physical arrow: b^2=A/4 and c^2=B/4 are rational squares.
    A = F(1, 9)
    q = B = F(1, 10000)
    b, c = F(1, 6), F(1, 200)
    z = F(10027, 180000)
    qbar = 1 - A - B - q
    K = [
        [F(1, 2), F(0), b],
        [F(0), F(1, 2), c],
        [b, c, z],
    ]
    assert qbar == F(39991, 45000) and qbar > 0

    t00, t10, t01, t11 = q + A + B, q + B, q + A, q
    J = psi_i(t00) + psi_i(t11) - psi_i(t01) - psi_i(t10)

    kAminus = kappa_i(q, A)
    kAplus = kappa_i(q + B, A)
    kBminus = kappa_i(q, B)
    kBplus = kappa_i(q + A, B)
    KA = parallel_i(kAminus, kAplus)
    KB = parallel_i(kBminus, kBplus)
    accepted_gap = KA + KB - J / (32 * A * B)
    assert accepted_gap.hi < 0

    a_minus = logit_edge(q, A)
    a_plus = logit_edge(q + B, A)
    H_A = a_plus * a_minus / ((a_plus + a_minus) * (16 * A))
    C_A = (H_A * (kBplus + kBminus) + kBplus * kBminus) / (
        H_A * 4 + kBplus + kBminus
    )
    common_gap = C_A - J / (32 * A * B)
    assert common_gap.lo > 0

    corner = corner_la_matrix(q, A, B)
    event = event_la_matrix(K, A, B, b, c)
    for i in range(DIM):
        for j in range(DIM):
            if corner[i][j].key() != event[i][j].key():
                raise AssertionError(f"complete-event/corner mismatch at {(i,j)}")

    Mint = interval_matrix(corner)
    minors: List[I] = []
    for n in range(1, DIM + 1):
        m = det_interval([row[:n] for row in Mint[:n]])
        if m.lo <= 0:
            raise AssertionError(f"Sylvester minor {n} unresolved")
        minors.append(m)

    print("INPUT")
    print(f"A={A}, B=q={q}, qbar={qbar}")
    print("K=[[1/2,0,1/6],[0,1/2,1/200],[1/6,1/200,10027/180000]]")
    print("All eight complete events are positive; K and I-K are strict by q,qbar,A,B>0.")
    print(f"LOG_SERIES_TERMS={NLOG}")
    print("PASS: exact Mobius eight-event jets and normalization")
    print("PASS: exact event Hessian equals the shared-corner 6x6 quadratic")
    show_interval("ACCEPTED_PARALLEL_GAP", accepted_gap)
    print("PASS: accepted strict parallel-edge criterion fails at this actual DPP rectangle")
    show_interval("COMMON_D_GAP", common_gap)
    print("PASS: new common-leaf-diagonal criterion succeeds")
    for i, m in enumerate(minors, 1):
        show_interval(f"FULL_HESSIAN_LEADING_MINOR_{i}", m)
    print("PASS: full complete-event -H'' matrix is positive definite by Sylvester")
    print("CLASSIFICATION: METHOD_OBSTRUCTION_ONLY; NOT_AN_ENTROPY_COUNTEREXAMPLE")
    print("ALL RATIONAL HALF-LEAF BOUNDARY CHECKS PASSED")


if __name__ == "__main__":
    main()
