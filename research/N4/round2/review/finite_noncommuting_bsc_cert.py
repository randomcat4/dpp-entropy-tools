#!/usr/bin/env python3
"""Low-denominator independent face and BSC-lift certificate.

This is a diagnostic certificate on a rational noncommuting fixture.  It proves
the event identities and the sign of one finite chord, but it is not a search
over the frozen theorem.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import os
import sys
from fractions import Fraction
from pathlib import Path


F = Fraction


def fs(x: F) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def dec(x: F) -> str:
    return f"{x.numerator / x.denominator:.17g}"


def mat(n, m, val=F(0)):
    return [[val for _ in range(m)] for _ in range(n)]


def eye(n):
    a = mat(n, n)
    for i in range(n):
        a[i][i] = F(1)
    return a


def transpose(a):
    return [list(row) for row in zip(*a)]


def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def madd(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def msub(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def mscale(c, a):
    return [[c * a[i][j] for j in range(len(a[0]))] for i in range(len(a))]


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


def leading_minors(a):
    return [det([row[:k] for row in a[:k]]) for k in range(1, len(a) + 1)]


def poly_trim(p):
    q = p[:]
    while len(q) > 1 and q[-1] == 0:
        q.pop()
    return q


def padd(a, b):
    n = max(len(a), len(b))
    out = [F(0) for _ in range(n)]
    for i in range(n):
        if i < len(a):
            out[i] += a[i]
        if i < len(b):
            out[i] += b[i]
    return poly_trim(out)


def pneg(a):
    return [-x for x in a]


def psub(a, b):
    return padd(a, pneg(b))


def pmul(a, b):
    out = [F(0) for _ in range(len(a) + len(b) - 1)]
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[i + j] += ai * bj
    return poly_trim(out)


def pscale(c, p):
    return poly_trim([c * x for x in p])


def peval(p, x):
    y = F(0)
    for c in reversed(p):
        y = y * x + c
    return y


def perm_sign(perm):
    inv = 0
    for i in range(len(perm)):
        for j in range(i + 1, len(perm)):
            inv += perm[i] > perm[j]
    return -1 if inv % 2 else 1


def det_poly(a):
    total = [F(0)]
    for perm in itertools.permutations(range(len(a))):
        term = [F(1)]
        for i, j in enumerate(perm):
            term = pmul(term, a[i][j])
        if perm_sign(perm) < 0:
            term = pneg(term)
        total = padd(total, term)
    return poly_trim(total)


def event_poly(ka, kv, mask):
    n = len(ka)
    m = [[[ka[i][j], kv[i][j]] for j in range(n)] for i in range(n)]
    bits = 0
    for i in range(n):
        if (mask >> i) & 1:
            bits += 1
        else:
            m[i][i] = psub(m[i][i], [F(1)])
    p = det_poly(m)
    if (n - bits) % 2:
        p = pneg(p)
    return poly_trim(p)


def event_prob(k, mask):
    n = len(k)
    m = [row[:] for row in k]
    bits = 0
    for i in range(n):
        if (mask >> i) & 1:
            bits += 1
        else:
            m[i][i] -= 1
    p = det(m)
    if (n - bits) % 2:
        p = -p
    return p


def householder_fixture():
    z = [F(1, 5), F(2, 5), F(2, 5), F(4, 5)]
    a_vec = [F(-1), F(-2), F(-2), F(1)]
    h = mat(4, 4)
    for i in range(4):
        for j in range(4):
            h[i][j] = (F(1) if i == j else F(0)) - a_vec[i] * a_vec[j] / 5
    u = [row[:3] for row in h]
    a = [
        [F(2, 5), F(1, 20), F(1, 30)],
        [F(1, 20), F(1, 3), F(-1, 25)],
        [F(1, 30), F(-1, 25), F(1, 2)],
    ]
    v = [
        [F(1, 7), F(2, 15), F(-1, 18)],
        [F(2, 15), F(-1, 8), F(1, 20)],
        [F(-1, 18), F(1, 20), F(1, 10)],
    ]
    return u, z, a, v


def make_k(u, a):
    return mm(mm(u, a), transpose(u))


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
    def __init__(self, terms):
        self.terms = terms
        self.calls = 0
        self.log2 = log_interval_atanh(F(2), terms)

    @staticmethod
    def ge_power(k, q):
        if k >= 0:
            return q.numerator >= q.denominator * (1 << k)
        return q.numerator * (1 << (-k)) >= q.denominator

    def floor_log2(self, q):
        k = q.numerator.bit_length() - q.denominator.bit_length()
        while not self.ge_power(k, q):
            k -= 1
        while self.ge_power(k + 1, q):
            k += 1
        return k

    @staticmethod
    def scale(k, lo, hi):
        if k >= 0:
            return k * lo, k * hi
        return k * hi, k * lo

    def log(self, q):
        if q <= 0:
            raise ValueError("log requires positive rational")
        self.calls += 1
        if q == 1:
            return F(0), F(0)
        k = self.floor_log2(q)
        x = q / (1 << k) if k >= 0 else q * (1 << (-k))
        lo, hi = log_interval_atanh(x, self.terms)
        l2, u2 = self.scale(k, *self.log2)
        return l2 + lo, u2 + hi


def entropy_delta_interval(events_minus, events_zero, events_plus, masks, terms):
    logs = LogBounds(terms)
    lo = F(0)
    hi = F(0)
    for mask in masks:
        for coeff, q in [(-events_minus[mask] / 2, events_minus[mask]), (events_zero[mask], events_zero[mask]), (-events_plus[mask] / 2, events_plus[mask])]:
            lq, uq = logs.log(q)
            if coeff >= 0:
                lo += coeff * lq
                hi += coeff * uq
            else:
                lo += coeff * uq
                hi += coeff * lq
    return lo, hi, logs.calls


def feasibility_latent(a, v, t):
    out = {}
    ident = eye(3)
    for label, sign in [("minus", -1), ("plus", 1)]:
        m = madd(a, mscale(sign * t, v))
        comp = msub(ident, m)
        mins = leading_minors(m)
        cmins = leading_minors(comp)
        out[label] = {
            "leading_minors_A": [fs(x) for x in mins],
            "leading_minors_I_minus_A": [fs(x) for x in cmins],
            "sylvester_strict": all(x > 0 for x in mins + cmins),
        }
    return out


def feasibility_kernel(kernels):
    out = {}
    ident = eye(4)
    for label, k in kernels.items():
        mins = leading_minors(k)
        cmins = leading_minors(msub(ident, k))
        out[label] = {
            "leading_minors_K": [fs(x) for x in mins],
            "leading_minors_I_minus_K": [fs(x) for x in cmins],
            "sylvester_strict": all(x > 0 for x in mins + cmins),
        }
    return out


def main() -> int:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("finite_noncommuting_bsc_certificate.json")
    terms = int(sys.argv[2]) if len(sys.argv) > 2 else 48
    script = Path(__file__).resolve()
    u, z, a, v = householder_fixture()
    t = F(1, 20)
    epsilon = F(1, 100)
    ka = make_k(u, a)
    kv = make_k(u, v)
    polys = {mask: event_poly(ka, kv, mask) for mask in range(16)}
    center = {mask: peval(polys[mask], F(0)) for mask in range(16)}
    minus = {mask: peval(polys[mask], -t) for mask in range(16)}
    plus = {mask: peval(polys[mask], t) for mask in range(16)}
    p1 = {mask: (polys[mask][1] if len(polys[mask]) > 1 else F(0)) for mask in range(16)}
    p2 = {mask: (2 * polys[mask][2] if len(polys[mask]) > 2 else F(0)) for mask in range(16)}
    face_lo, face_hi, face_calls = entropy_delta_interval(minus, center, plus, range(15), terms)

    k_minus = make_k(u, madd(a, mscale(-t, v)))
    k_zero = ka
    k_plus = make_k(u, madd(a, mscale(t, v)))
    lifted = {
        "minus": madd(mscale(1 - 2 * epsilon, k_minus), mscale(epsilon, eye(4))),
        "zero": madd(mscale(1 - 2 * epsilon, k_zero), mscale(epsilon, eye(4))),
        "plus": madd(mscale(1 - 2 * epsilon, k_plus), mscale(epsilon, eye(4))),
    }
    lift_events = {name: {mask: event_prob(k, mask) for mask in range(16)} for name, k in lifted.items()}
    lift_lo, lift_hi, lift_calls = entropy_delta_interval(lift_events["minus"], lift_events["zero"], lift_events["plus"], range(16), terms)

    av = mm(a, v)
    va = mm(v, a)
    result = {
        "pid": os.getpid(),
        "argv": sys.argv,
        "python": sys.version,
        "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
        "exit_status": 0,
        "fixture": {
            "z": [fs(x) for x in z],
            "U": [[fs(x) for x in row] for row in u],
            "U_column_gram": [[fs(x) for x in row] for row in mm(transpose(u), u)],
            "Utz": [fs(row[0]) for row in mm(transpose(u), [[zi] for zi in z])],
            "A": [[fs(x) for x in row] for row in a],
            "V": [[fs(x) for x in row] for row in v],
            "A_V_commutator_nonzero": any(av[i][j] != va[i][j] for i in range(3) for j in range(3)),
            "t": fs(t),
            "epsilon": fs(epsilon),
        },
        "latent_feasibility": feasibility_latent(a, v, t),
        "face_events": {
            "full_event_poly": [fs(x) for x in polys[15]],
            "full_event_exact_zero": all(x == 0 for x in polys[15]),
            "proper_center_positive": all(center[m] > 0 for m in range(15)),
            "proper_endpoint_positive": {"minus": all(minus[m] > 0 for m in range(15)), "plus": all(plus[m] > 0 for m in range(15))},
            "proper_sum_p0": fs(sum(center[m] for m in range(15))),
            "proper_sum_p1": fs(sum(p1[m] for m in range(15))),
            "proper_sum_p2": fs(sum(p2[m] for m in range(15))),
            "center": {str(m): fs(center[m]) for m in range(16)},
            "minus": {str(m): fs(minus[m]) for m in range(16)},
            "plus": {str(m): fs(plus[m]) for m in range(16)},
        },
        "face_delta_interval": {
            "log_terms": terms,
            "log_interval_calls": face_calls,
            "lower_decimal": dec(face_lo),
            "upper_decimal": dec(face_hi),
            "strictly_negative": face_hi < 0,
            "strictly_positive": face_lo > 0,
        },
        "bsc_lift": {
            "kernel_feasibility": feasibility_kernel(lifted),
            "all_events_positive": {name: all(q > 0 for q in events.values()) for name, events in lift_events.items()},
            "delta_interval": {
                "log_terms": terms,
                "log_interval_calls": lift_calls,
                "lower_decimal": dec(lift_lo),
                "upper_decimal": dec(lift_hi),
                "strictly_negative": lift_hi < 0,
                "strictly_positive": lift_lo > 0,
            },
        },
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
