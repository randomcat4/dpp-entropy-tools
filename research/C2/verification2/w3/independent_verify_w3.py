#!/usr/bin/env python3
"""Independent scoped verifier for W3 T1.

The script uses only exact rational arithmetic plus rigorous rational log
intervals.  Floating point values are never used for proof decisions.
"""

from __future__ import annotations

import itertools
import json
import platform
import time
from dataclasses import dataclass
from fractions import Fraction as F
from pathlib import Path


def check(cond: bool, label: str) -> None:
    if not cond:
        raise AssertionError(label)


def dot(x, y):
    return sum((a * b for a, b in zip(x, y)), F(0))


def transpose(A):
    return [list(row) for row in zip(*A)]


def mm(A, B):
    Bt = transpose(B)
    return [[dot(row, col) for col in Bt] for row in A]


def add(A, B):
    return [[x + y for x, y in zip(r1, r2)] for r1, r2 in zip(A, B)]


def sub(A, B):
    return [[x - y for x, y in zip(r1, r2)] for r1, r2 in zip(A, B)]


def scale(A, s):
    return [[s * x for x in row] for row in A]


def eye(n):
    return [[F(1 if i == j else 0) for j in range(n)] for i in range(n)]


def trace(A):
    return sum((A[i][i] for i in range(len(A))), F(0))


def outer(x, y):
    return [[a * b for b in y] for a in x]


def cross(x, y):
    return [
        x[1] * y[2] - x[2] * y[1],
        x[2] * y[0] - x[0] * y[2],
        x[0] * y[1] - x[1] * y[0],
    ]


def det3(A):
    return dot(A[0], cross(A[1], A[2]))


def adj3(A):
    tr = trace(A)
    e2 = (tr * tr - trace(mm(A, A))) / 2
    return add(sub(mm(A, A), scale(A, tr)), scale(eye(3), e2))


def trprod(A, B):
    return trace(mm(A, B))


def quad(A, x):
    return dot(x, [dot(row, x) for row in A])


def sum_matrices(mats):
    mats = list(mats)
    n = len(mats[0])
    out = [[F(0) for _ in range(n)] for _ in range(n)]
    for A in mats:
        out = add(out, A)
    return out


def sym_vec(x):
    return [
        x[0] ** 2,
        x[1] ** 2,
        x[2] ** 2,
        2 * x[0] * x[1],
        2 * x[0] * x[2],
        2 * x[1] * x[2],
    ]


def det_bareiss(A):
    """Fraction-free determinant, exact over Fraction entries."""
    M = [row[:] for row in A]
    n = len(M)
    if n == 0:
        return F(1)
    sign = F(1)
    prev = F(1)
    for k in range(n - 1):
        if M[k][k] == 0:
            swap = next((i for i in range(k + 1, n) if M[i][k] != 0), None)
            if swap is None:
                return F(0)
            M[k], M[swap] = M[swap], M[k]
            sign *= -1
        pivot = M[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                M[i][j] = (M[i][j] * pivot - M[i][k] * M[k][j]) / prev
        prev = pivot
        for i in range(k + 1, n):
            M[i][k] = F(0)
        for j in range(k + 1, n):
            M[k][j] = F(0)
    return sign * M[-1][-1]


def leading_principal_minors(A):
    return [det_bareiss([row[:k] for row in A[:k]]) for k in range(1, len(A) + 1)]


def p_add(a, b):
    out = [F(0)] * max(len(a), len(b))
    for i, x in enumerate(a):
        out[i] += x
    for i, x in enumerate(b):
        out[i] += x
    return out


def p_mul(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def minor_poly(K, D, S):
    n = len(S)
    if n == 0:
        return [F(1)]
    out = [F(0)] * (n + 1)
    for perm in itertools.permutations(range(n)):
        inversions = sum(perm[i] > perm[j] for i in range(n) for j in range(i + 1, n))
        prod = [F(-1 if inversions % 2 else 1)]
        for i, j in enumerate(perm):
            prod = p_mul(prod, [K[S[i]][S[j]], D[S[i]][S[j]]])
        out = p_add(out, prod)
    return out


@dataclass(frozen=True)
class Interval:
    lo: F
    hi: F

    def __post_init__(self):
        check(self.lo <= self.hi, "interval order")

    def __add__(self, other):
        other = as_interval(other)
        return Interval(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self):
        return Interval(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + (-as_interval(other))

    def __rsub__(self, other):
        return as_interval(other) + (-self)

    def __mul__(self, other):
        other = as_interval(other)
        values = [self.lo * other.lo, self.lo * other.hi, self.hi * other.lo, self.hi * other.hi]
        return Interval(min(values), max(values))

    __rmul__ = __mul__


def as_interval(x):
    return x if isinstance(x, Interval) else Interval(F(x), F(x))


def log_interval(x: F, terms: int = 40) -> Interval:
    check(x > 0, "positive log input")
    k = 0
    y = x
    while y < 1:
        y *= 2
        k -= 1
    while y >= 2:
        y /= 2
        k += 1

    def series(z):
        partial = sum((2 * z ** (2 * j + 1) / F(2 * j + 1) for j in range(terms)), F(0))
        tail = 2 * z ** (2 * terms + 1) / (F(2 * terms + 1) * (1 - z * z))
        return Interval(partial, partial + tail)

    return series((y - 1) / (y + 1)) + k * series(F(1, 3))


def interval_lt(x: Interval, q: F) -> bool:
    return x.hi < q


def interval_gt(x: Interval, q: F) -> bool:
    return x.lo > q


def interval_contains(outer_lo: F, x: Interval, outer_hi: F) -> bool:
    return outer_lo <= x.lo and x.hi <= outer_hi


def floor_grid(x: F, scale: int = 10**30) -> F:
    return F((x.numerator * scale) // x.denominator, scale)


def ceil_grid(x: F, scale: int = 10**30) -> F:
    return -floor_grid(-x, scale)


def stringify(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, Interval):
        return {"lo": str(floor_grid(x.lo)), "hi": str(ceil_grid(x.hi))}
    if isinstance(x, list):
        return [stringify(y) for y in x]
    if isinstance(x, dict):
        return {str(k): stringify(v) for k, v in x.items()}
    return x


def main():
    started = time.time()
    out_dir = Path(__file__).resolve().parent / "independent_output"
    out_dir.mkdir(parents=True, exist_ok=True)

    M = [
        [615, 120, -702],
        [240, 735, 246],
        [-630, 30, -71],
        [480, -620, 492],
        [-170, -390, -540],
    ]
    U = [[F(x, 1045) for x in row] for row in M]
    check(mm(transpose(U), U) == eye(3), "frozen U is an isometry")

    pairs = list(itertools.combinations(range(5), 2))
    triples = list(itertools.combinations(range(5), 3))
    allsets = [S for k in range(6) for S in itertools.combinations(range(5), k)]
    rows = U
    crosses = [cross(rows[i], rows[j]) for i, j in pairs]
    g = [dot(x, x) for x in rows]
    h = [dot(x, x) for x in crosses]
    q = [det3([U[i] for i in S]) ** 2 for S in triples]

    check(all(x > 0 for x in g + h + q), "26 positive support weights")
    check(sum(g) == 3 and sum(h) == 3 and sum(q) == 1, "weight sums 1+3+3+1")
    check(sum_matrices(outer(x, x) for x in rows) == eye(3), "row tight frame")
    check(sum_matrices(outer(x, x) for x in crosses) == eye(3), "cross tight frame")

    logg = [log_interval(x) for x in g]
    logh = [log_interval(x) for x in h]
    logq = [log_interval(x) for x in q]
    tg = sum((weight * logx for weight, logx in zip(g, logg)), as_interval(F(0)))
    th = sum((weight * logx for weight, logx in zip(h, logh)), as_interval(F(0)))
    c = -sum((weight * logx for weight, logx in zip(q, logq)), as_interval(F(0)))
    tt = tg + th
    beta = th - tg + c
    T = [
        [
            sum((x[i] * x[j] * z for x, z in zip(rows + crosses, logg + logh)), as_interval(F(0)))
            for j in range(3)
        ]
        for i in range(3)
    ]
    m0 = 2 * tg - F(2, 3) * tt
    m1 = 2 * (th + c) - F(2, 3) * tt
    Egeo = [[2 * T[i][j] - (F(2, 3) * tt if i == j else F(0)) for j in range(3)] for i in range(3)]

    check(interval_gt(m0, F(1, 4)) and interval_lt(m0, F(1, 2)), "C2 endpoint m(0)")
    check(interval_gt(m1, F(1, 4)) and interval_lt(m1, F(1, 2)), "C2 endpoint m(1)")
    check(interval_gt(beta, F(0)) and interval_lt(beta, F(1, 8)), "C4 beta")

    e = F(1, 1_000_000)
    E0 = [
        [F(71, 1_000_000), F(72_690, 1_000_000), F(52_507, 1_000_000)],
        [F(72_690, 1_000_000), F(-42_720, 1_000_000), F(-74_600, 1_000_000)],
        [F(52_507, 1_000_000), F(-74_600, 1_000_000), F(42_650, 1_000_000)],
    ]
    for i in range(3):
        for j in range(3):
            check(interval_contains(E0[i][j] - e, Egeo[i][j], E0[i][j] + e), "Egeo entry enclosure")
    frob_upper = sum((abs(E0[i][j]) + e) ** 2 for i in range(3) for j in range(3))
    check(frob_upper < F(1, 25), "C3 Frobenius bound")
    E_plus = add(scale(eye(3), F(3, 20) - 3 * e), E0)
    E_minus = sub(scale(eye(3), F(3, 20) - 3 * e), E0)
    E_plus_minors = leading_principal_minors(E_plus)
    E_minus_minors = leading_principal_minors(E_minus)
    check(all(x > 0 for x in E_plus_minors), "C3 plus operator certificate")
    check(all(x > 0 for x in E_minus_minors), "C3 minus operator certificate")

    Fmat = [
        [
            sum((2 * sym_vec(x)[i] * sym_vec(x)[j] / dot(x, x) for x in rows + crosses), F(0))
            for j in range(6)
        ]
        for i in range(6)
    ]
    metric = [[F([1, 1, 1, 2, 2, 2][i]) if i == j else F(0) for j in range(6)] for i in range(6)]
    Cmat = sub(Fmat, scale(metric, F(1, 4)))
    C_minors = leading_principal_minors(Cmat)
    check(all(x > 0 for x in C_minors), "C1 Fisher leading minors")

    rho = F(1, 2000)
    check(F(9, 10) / (1 + rho) ** 3 > F(7, 8), "Fisher transfer discount")
    transfer = F(119, 1600) - F(243, 250000) - F(66, 1999) - F(1, 16000)
    check(transfer == F(161215319, 3998000000), "margin identity")
    check(transfer > F(1, 25), "margin exceeds 1/25")

    eta = F(1, 10000)
    A = add(scale(eye(3), F(1, 2)), [[eta, 0, 0], [0, -eta, 0], [0, 0, 0]])
    V = add(eye(3), [[0, F(1, 10), 0], [F(1, 10), 0, 0], [0, 0, 0]])
    d = det3(A)
    d1 = trprod(adj3(A), V)
    J = adj3(V)
    d2 = 2 * trprod(A, J)
    tau = trace(V)
    trA = trace(A)
    D1 = add(add(mm(A, A), scale(A, 1 - trA)), scale(eye(3), d))
    D2 = sub(adj3(A), scale(eye(3), d))
    D1p = add(sub(add(add(mm(A, V), mm(V, A)), scale(V, 1 - trA)), scale(A, tau)), scale(eye(3), d1))
    adjp = add(
        sub(sub(add(mm(A, V), mm(V, A)), scale(A, tau)), scale(V, trA)),
        scale(eye(3), trA * tau - trprod(A, V)),
    )
    D2p = sub(adjp, scale(eye(3), d1))
    D1pp = sub(scale(J, 2), scale(eye(3), 2 * trprod(sub(eye(3), A), J)))
    D2pp = sub(scale(J, 2), scale(eye(3), d2))

    data = {(): [det3(sub(eye(3), A)), -trprod(adj3(sub(eye(3), A)), V), 2 * trprod(sub(eye(3), A), J)]}
    for i in range(5):
        data[(i,)] = [quad(D1, rows[i]), quad(D1p, rows[i]), quad(D1pp, rows[i])]
    for S, x in zip(pairs, crosses):
        data[S] = [quad(D2, x), quad(D2p, x), quad(D2pp, x)]
    for S, z in zip(triples, q):
        data[S] = [d * z, d1 * z, d2 * z]
    for S in allsets:
        data.setdefault(S, [F(0), F(0), F(0)])

    positive = sum(1 for S in allsets if data[S][0] > 0)
    zero = sum(1 for S in allsets if data[S][0] == 0)
    check((positive, zero) == (26, 6), "32 event split")
    check([sum(data[S][j] for S in allsets) for j in range(3)] == [1, 0, 0], "mass derivatives")
    check([sum(len(S) * data[S][j] for S in allsets) for j in range(3)] == [trace(A), trace(V), 0], "first moment derivatives")

    K = mm(mm(U, A), transpose(U))
    D = mm(mm(U, V), transpose(U))
    minors = {S: minor_poly(K, D, S) for S in allsets}
    for S in allsets:
        poly = [F(0)] * 6
        setS = set(S)
        for Tset in allsets:
            if setS.issubset(Tset):
                poly = p_add(poly, [(-1) ** (len(Tset) - len(S)) * coeff for coeff in minors[Tset]])
        check([poly[0], poly[1], 2 * poly[2]] == data[S], f"containment coefficients {S}")
        check(all(coeff == 0 for coeff in poly[4:]), f"degree cap {S}")

    result = {
        "status": "PASS_SCOPED_EXACT_CHECKS",
        "elapsed_seconds": time.time() - started,
        "python": platform.python_version(),
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "support_counts": {"positive": positive, "zero": zero},
        "m0": m0,
        "m1": m1,
        "beta": beta,
        "frob_E_upper": frob_upper,
        "E_plus_leading_minors": E_plus_minors,
        "E_minus_leading_minors": E_minus_minors,
        "Fisher_C_leading_minors": C_minors,
        "uniform_margin": transfer,
        "uniform_margin_minus_one_over_25": transfer - F(1, 25),
        "example": {
            "A": A,
            "V": V,
            "d": d,
            "d_first": d1,
            "d_second": d2,
        },
    }
    (out_dir / "independent_certificate.json").write_text(json.dumps(stringify(result), indent=2), encoding="utf-8")
    print("PASS_SCOPED_EXACT_CHECKS")
    print("positive_support=26 zero_events=6")
    print("uniform_margin=" + str(transfer))
    print("margin_minus_1_over_25=" + str(transfer - F(1, 25)))
    print("output=" + str(out_dir / "independent_certificate.json"))


if __name__ == "__main__":
    main()
