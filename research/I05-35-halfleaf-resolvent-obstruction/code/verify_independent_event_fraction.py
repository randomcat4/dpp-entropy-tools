#!/usr/bin/env python3
"""A second, minimal reconstruction of the PR124 pointwise-resolvent witness.

This file uses only Fraction arithmetic. It starts from inclusion principal
minors of K+tD, applies complete-event Mobius inversion, groups the four leaf
marginals, and differentiates P(t)^2/(p_1(t)+r P(t)) directly. It does not
import or call the longer PR124 checker.
"""
from fractions import Fraction as F
from itertools import combinations, permutations

N = 3
DEG = 3
ZERO = tuple(F(0) for _ in range(DEG + 1))
ONE = (F(1), F(0), F(0), F(0))


def add(a, b):
    return tuple(a[i] + b[i] for i in range(DEG + 1))


def scale(a, c):
    c = F(c)
    return tuple(c * x for x in a)


def mul(a, b):
    out = [F(0)] * (DEG + 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if i + j <= DEG:
                out[i + j] += x * y
    return tuple(out)


def affine(x, dx):
    return (F(x), F(dx), F(0), F(0))


def parity(p):
    inv = 0
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            inv += p[i] > p[j]
    return -1 if inv % 2 else 1


def determinant(m):
    n = len(m)
    if n == 0:
        return ONE
    ans = ZERO
    for p in permutations(range(n)):
        term = ONE
        for i, j in enumerate(p):
            term = mul(term, m[i][j])
        ans = add(ans, scale(term, parity(p)))
    return ans


def subsets(xs):
    xs = tuple(xs)
    for k in range(len(xs) + 1):
        yield from combinations(xs, k)


def principal_minor(kmat, subset):
    return determinant([[kmat[i][j] for j in subset] for i in subset])


def mobius_events(kmat):
    vertices = tuple(range(N))
    minors = {subset: principal_minor(kmat, subset) for subset in subsets(vertices)}
    events = {}
    for occupied in subsets(vertices):
        complement = tuple(i for i in vertices if i not in occupied)
        value = ZERO
        for extra in subsets(complement):
            sup = tuple(sorted(occupied + extra))
            value = add(value, scale(minors[sup], -1 if len(extra) % 2 else 1))
        events[occupied] = value
    return events


def jets(poly):
    return poly[0], poly[1], 2 * poly[2]


def quotient_second(num, den):
    n0, n1, n2 = jets(num)
    d0, d1, d2 = jets(den)
    return (
        n2 / d0
        - n0 * d2 / d0**2
        - 2 * n1 * d1 / d0**2
        + 2 * n0 * d1**2 / d0**3
    )


def main():
    k0 = [
        [F(1, 2), F(0), F(1, 4)],
        [F(0), F(1, 2), F(2, 5)],
        [F(1, 4), F(2, 5), F(277, 500)],
    ]
    direction = [
        [F(-18), F(146), F(108)],
        [F(146), F(-72), F(5)],
        [F(108), F(5), F(40)],
    ]
    r = F(1, 50000)
    kmat = [
        [affine(k0[i][j], direction[i][j]) for j in range(N)]
        for i in range(N)
    ]
    events = mobius_events(kmat)
    total_probability = ZERO
    for event in events.values():
        total_probability = add(total_probability, event)
    assert total_probability == ONE
    assert all(poly[0] > 0 for poly in events.values())

    total = F(0)
    for leaf in subsets((0, 1)):
        with_center = tuple(sorted(leaf + (2,)))
        p1 = events[with_center]
        p0 = events[leaf]
        marginal = add(p0, p1)
        numerator = mul(marginal, marginal)
        denominator = add(p1, scale(marginal, r))
        total += quotient_second(numerator, denominator)

    expected = -F(
        47488558049748267993080620088778228551027375300000000000,
        2044542058422113103788725284171055940635901533282467,
    )
    assert total == expected
    print(f"PHI_R_SECOND_EXACT={total.numerator}/{total.denominator}")
    print("PASS: independent 8-event Mobius reconstruction gives Phi_r'' < 0")
    print("ALL I05-35 INDEPENDENT EVENT CHECKS PASSED")


if __name__ == "__main__":
    main()
