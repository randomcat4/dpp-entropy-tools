#!/usr/bin/env python3
"""Source-independent exact reconstruction of the PR104 rational witness."""

from fractions import Fraction as Q
from itertools import permutations
import json


class Box:
    __slots__ = ("lo", "hi")

    def __init__(self, lo, hi=None):
        self.lo = Q(lo)
        self.hi = self.lo if hi is None else Q(hi)
        assert self.lo <= self.hi

    def __add__(self, other):
        other = other if isinstance(other, Box) else Box(other)
        return Box(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self):
        return Box(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + (-other if isinstance(other, Box) else -Box(other))

    def __rsub__(self, other):
        return Box(other) - self

    def __mul__(self, other):
        other = other if isinstance(other, Box) else Box(other)
        candidates = [self.lo * other.lo, self.lo * other.hi,
                      self.hi * other.lo, self.hi * other.hi]
        return Box(min(candidates), max(candidates))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = other if isinstance(other, Box) else Box(other)
        assert not (other.lo <= 0 <= other.hi)
        return self * Box(1 / other.hi, 1 / other.lo)

    def square(self):
        if self.lo >= 0:
            return Box(self.lo * self.lo, self.hi * self.hi)
        if self.hi <= 0:
            return Box(self.hi * self.hi, self.lo * self.lo)
        return Box(0, max(self.lo * self.lo, self.hi * self.hi))


def log_box(x, terms=30):
    x = Q(x)
    assert x > 0
    power = 0
    reduced = x
    while reduced < 1:
        reduced *= 2
        power -= 1
    while reduced >= 2:
        reduced /= 2
        power += 1

    def unit(y):
        w = (y - 1) / (y + 1)
        partial = 2 * sum((w ** (2 * j + 1) / (2 * j + 1) for j in range(terms)), Q(0))
        tail = 2 * w ** (2 * terms + 1) / ((2 * terms + 1) * (1 - w * w))
        return Box(partial, partial + tail)

    return unit(reduced) + unit(Q(2)) * power


def p_add(a, b, sign=1):
    out = [Q(0)] * max(len(a), len(b))
    for i, value in enumerate(a):
        out[i] += value
    for i, value in enumerate(b):
        out[i] += sign * value
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def p_mul(a, b):
    out = [Q(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def parity(perm):
    inversions = sum(perm[i] > perm[j] for i in range(len(perm)) for j in range(i + 1, len(perm)))
    return -1 if inversions & 1 else 1


def principal_det_polynomial(K, D, indices):
    if not indices:
        return [Q(1)]
    result = [Q(0)]
    for perm in permutations(range(len(indices))):
        term = [Q(1)]
        for row, column in enumerate(perm):
            i, j = indices[row], indices[column]
            term = p_mul(term, [K[i][j], D[i][j]])
        result = p_add(result, term, parity(perm))
    return result


def complete_event_jets(K, D):
    inclusions = []
    for mask in range(8):
        subset = [i for i in range(3) if mask & (1 << i)]
        inclusions.append(principal_det_polynomial(K, D, subset))
    events = []
    for event in range(8):
        polynomial = [Q(0)]
        for superset in range(8):
            if superset & event == event:
                sign = -1 if (superset.bit_count() - event.bit_count()) & 1 else 1
                polynomial = p_add(polynomial, inclusions[superset], sign)
        polynomial += [Q(0)] * (3 - len(polynomial))
        events.append((polynomial[0], polynomial[1], 2 * polynomial[2]))
    assert all(p0 > 0 for p0, _, _ in events)
    assert sum((p0 for p0, _, _ in events), Q(0)) == 1
    assert sum((p1 for _, p1, _ in events), Q(0)) == 0
    assert sum((p2 for _, _, p2 in events), Q(0)) == 0
    return events


def physical_direction(coordinates, A, B, b, c):
    da, db, x00, x10, x01, x11 = coordinates
    mean = (x00 + x10 + x01 + x11) / 4
    alpha = (x10 + x11 - x00 - x01) / 2
    beta = (x01 + x11 - x00 - x10) / 2
    mixed = x00 - x10 - x01 + x11
    return [
        [da, b * c * mixed / (2 * A * B), -b * alpha / (2 * A)],
        [b * c * mixed / (2 * A * B), db, -c * beta / (2 * B)],
        [-b * alpha / (2 * A), -c * beta / (2 * B), mean - A * da - B * db],
    ]


def curvature(K, D):
    events = complete_event_jets(K, D)
    answer = Box(0)
    for p0, p1, p2 in events:
        answer += Q(p1 * p1, p0) + log_box(p0) * p2
    return answer, events


def hessian(K, A, B, b, c):
    dimension = 6
    basis = [[Q(i == j) for i in range(dimension)] for j in range(dimension)]
    diagonal = []
    event_checks = 0
    for vector in basis:
        value, events = curvature(K, physical_direction(vector, A, B, b, c))
        diagonal.append(value)
        event_checks += len(events)
    matrix = [[Box(0) for _ in range(dimension)] for __ in range(dimension)]
    for i in range(dimension):
        matrix[i][i] = diagonal[i]
        for j in range(i + 1, dimension):
            vector = [basis[i][k] + basis[j][k] for k in range(dimension)]
            value, events = curvature(K, physical_direction(vector, A, B, b, c))
            matrix[i][j] = matrix[j][i] = (value - diagonal[i] - diagonal[j]) / 2
            event_checks += len(events)
    return matrix, event_checks


def determinant_box(matrix):
    n = len(matrix)
    total = Box(0)
    for perm in permutations(range(n)):
        term = Box(1)
        for row, column in enumerate(perm):
            term *= matrix[row][column]
        total += term if parity(perm) > 0 else -term
    return total


def logit(u, step):
    v = u + step
    return log_box(v * (1 - u) / (u * (1 - v)))


def f(t):
    return 1 / (t * (1 - t))


def kappa(u, step):
    h = logit(u, step)
    mean = h / step
    return (f(u) * f(u + step) - mean.square()) / (8 * (f(u) + f(u + step) - 2 * mean))


def parallel(left, right):
    return left * right / (left + right)


def main():
    A, B, q = Q(1, 9), Q(1, 10000), Q(1, 10000)
    b, c, z = Q(1, 6), Q(1, 200), Q(10027, 180000)
    K = [[Q(1, 2), Q(0), b], [Q(0), Q(1, 2), c], [b, c, z]]

    for matrix in (K, [[Q(i == j) - K[i][j] for j in range(3)] for i in range(3)]):
        for size in range(1, 4):
            assert principal_det_polynomial(matrix, [[Q(0)] * 3 for _ in range(3)], range(size))[0] > 0

    t00, t10, t01, t11 = q + A + B, q + B, q + A, q
    psi = lambda t: log_box(t) * t + log_box(1 - t) * (1 - t)
    interaction = psi(t00) + psi(t11) - psi(t01) - psi(t10)

    ka0, ka1 = kappa(q, A), kappa(q + B, A)
    kb0, kb1 = kappa(q, B), kappa(q + A, B)
    old_gap = parallel(ka0, ka1) + parallel(kb0, kb1) - interaction / (32 * A * B)

    ha0, ha1 = logit(q, A), logit(q + B, A)
    shared = ha0 * ha1 / ((ha0 + ha1) * (16 * A))
    new_core = (shared * (kb0 + kb1) + kb0 * kb1) / (4 * shared + kb0 + kb1)
    new_gap = new_core - interaction / (32 * A * B)
    assert old_gap.hi < 0 < new_gap.lo

    matrix, event_jet_count = hessian(K, A, B, b, c)
    minors = [determinant_box([row[:size] for row in matrix[:size]]) for size in range(1, 7)]
    assert all(item.lo > 0 for item in minors)

    result = {
        "status": "PASS",
        "head": "d980dbb04840bd21e6c62cf88ffd45a9b0d1b4f8",
        "independent_complete_event_jets_checked": event_jet_count,
        "old_parallel_gap_decimal": [float(old_gap.lo), float(old_gap.hi)],
        "old_parallel_gap_exact_upper_negative": old_gap.hi < 0,
        "new_shared_leaf_gap_decimal": [float(new_gap.lo), float(new_gap.hi)],
        "new_shared_leaf_gap_exact_lower_positive": new_gap.lo > 0,
        "leading_minor_lower_bounds_decimal": [float(item.lo) for item in minors],
        "all_leading_minor_exact_lower_bounds_positive": all(item.lo > 0 for item in minors),
        "all_eight_events_and_normalization_checked_per_direction": True,
        "strict_K_and_I_minus_K": True,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
