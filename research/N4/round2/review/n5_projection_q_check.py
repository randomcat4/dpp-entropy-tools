#!/usr/bin/env python3
"""Minimal exact certificate for the five-point projection q entropy gate."""

from __future__ import annotations

import hashlib
import json
import os
import sys
from fractions import Fraction
from itertools import combinations
from pathlib import Path


F = Fraction


def fs(x: F) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def dec(x: F) -> str:
    return f"{x.numerator / x.denominator:.17g}"


def det(a):
    n = len(a)
    if n == 0:
        return F(1)
    m = [row[:] for row in a]
    sign = F(1)
    denom = F(1)
    for k in range(n - 1):
        if m[k][k] == 0:
            pivot = None
            for r in range(k + 1, n):
                if m[r][k] != 0:
                    pivot = r
                    break
            if pivot is None:
                return F(0)
            m[k], m[pivot] = m[pivot], m[k]
            sign = -sign
        p = m[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                m[i][j] = (m[i][j] * p - m[i][k] * m[k][j]) / denom
        denom = p
        for i in range(k + 1, n):
            m[i][k] = F(0)
    return sign * m[-1][-1]


def householder(w):
    norm = sum(x * x for x in w)
    n = len(w)
    return [[(F(1) if i == j else F(0)) - 2 * w[i] * w[j] / norm for j in range(n)] for i in range(n)]


def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def log_interval_atanh(x: F, terms: int):
    if x == 1:
        return F(0), F(0)
    r = (x - 1) / (x + 1)
    ar = abs(r)
    r2 = r * r
    power = r
    total = F(0)
    for n in range(terms):
        if n:
            power *= r2
        total += power / (2 * n + 1)
    approx = 2 * total
    tail = 2 * (ar ** (2 * terms + 1)) / ((2 * terms + 1) * (1 - ar * ar))
    return approx - tail, approx + tail


class LogBounds:
    def __init__(self, terms: int):
        self.terms = terms
        self.calls = 0
        self.log2 = log_interval_atanh(F(2), terms)

    @staticmethod
    def ge_power(k: int, q: F) -> bool:
        if k >= 0:
            return q.numerator >= q.denominator * (1 << k)
        return q.numerator * (1 << (-k)) >= q.denominator

    def floor_log2(self, q: F) -> int:
        k = q.numerator.bit_length() - q.denominator.bit_length()
        while not self.ge_power(k, q):
            k -= 1
        while self.ge_power(k + 1, q):
            k += 1
        return k

    @staticmethod
    def scale(k: int, lo: F, hi: F):
        if k >= 0:
            return k * lo, k * hi
        return k * hi, k * lo

    def log(self, q: F):
        if q <= 0:
            raise ValueError("log requires a positive rational")
        self.calls += 1
        if q == 1:
            return F(0), F(0)
        k = self.floor_log2(q)
        x = q / (1 << k) if k >= 0 else q * (1 << (-k))
        lo, hi = log_interval_atanh(x, self.terms)
        l2, u2 = self.scale(k, *self.log2)
        return l2 + lo, u2 + hi


def main() -> int:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("n5_projection_q_certificate.json")
    terms = int(sys.argv[2]) if len(sys.argv) > 2 else 180
    script = Path(__file__).resolve()
    a = [F(x) for x in (1, 2, 3, 4, 5)]
    b = [F(x) for x in (2, -1, 3, -2, 1)]
    u = [row[:3] for row in mm(householder(a), householder(b))]
    weights = []
    for rows in combinations(range(5), 3):
        minor = [[u[i][j] for j in range(3)] for i in rows]
        q = det(minor) ** 2
        weights.append(("".join(str(i + 1) for i in rows), q))

    logs = LogBounds(terms)
    h_lo = F(0)
    h_hi = F(0)
    for _, q in weights:
        lo, hi = logs.log(q)
        h_lo += -q * hi
        h_hi += -q * lo

    result = {
        "pid": os.getpid(),
        "argv": sys.argv,
        "python": sys.version,
        "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
        "exit_status": 0,
        "log_terms": terms,
        "log_interval_calls": logs.calls,
        "weights": [{"S": s, "q": fs(q)} for s, q in weights],
        "sum_q": fs(sum(q for _, q in weights)),
        "all_q_positive": all(q > 0 for _, q in weights),
        "H_lower_decimal": dec(h_lo),
        "H_upper_decimal": dec(h_hi),
        "H_lower_minus_3_over_2_decimal": dec(h_lo - F(3, 2)),
        "H_greater_than_3_over_2": h_lo > F(3, 2),
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
