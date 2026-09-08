"""Exact full-event checks for frozen A2 v2; no floating sign decisions.

Python 3.12 + sympy 1.14.0. Run --mode smoke before any bounded batch.
All files are written only when --output is supplied. Default: stdout.
The symbolic mode records probabilities; it does not prove a uniform remainder.
"""
from __future__ import annotations

import argparse
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from fractions import Fraction as F
import hashlib
import json
import os
from pathlib import Path
import platform
import sys
import time

import sympy as sp


def full_law(K):
    """Inclusion-exclusion over ALL principal minors; mask -> exact mass."""
    n = K.rows
    minors = {}
    for mask in range(1 << n):
        ids = [i for i in range(n) if mask >> i & 1]
        minors[mask] = K.extract(ids, ids).det() if ids else sp.S.One
    masses = {}
    for mask in range(1 << n):
        masses[mask] = sp.factor(sum(
            (-1) ** ((other ^ mask).bit_count()) * det
            for other, det in minors.items() if other & mask == mask))
    return masses, minors


def row_law(K):
    n = K.rows
    out = {}
    for mask in range(1 << n):
        J = sp.eye(n) - K
        for i in range(n):
            if mask >> i & 1:
                J[i, :] = K[i, :]
        out[mask] = sp.factor(J.det(method="domain-ge"))
    return out


def kernel(t, x, sigma):
    c, s = (1 - t*t)/(1 + t*t), 2*t/(1 + t*t)
    Q = sp.eye(4)
    Q[1, 1], Q[1, 2], Q[2, 1], Q[2, 2] = c, -s, s, c
    # U=Q A / sqrt(2); products are rational without an irrational intermediate.
    A = Q * sp.Matrix([[1, 0], [1, 0], [0, 1], [0, 1]])
    P = A*A.T/2
    X = sp.Matrix([[0, x], [x, 0]])
    return (t*sp.eye(4) + (1-2*t)*P + sigma*t*A*X*A.T/2).applyfunc(sp.factor)


def ff(q):
    return F(int(sp.numer(q)), int(sp.denom(q)))


def dyadic_out(lo, hi, bits=256):
    scale = 1 << bits
    return (F((lo.numerator*scale)//lo.denominator, scale),
            F(-((-hi.numerator*scale)//hi.denominator), scale))


def log_unit_interval(q, terms=96):
    """q in [1,2]; atanh series with a positive rational tail bound."""
    assert 1 <= q <= 2
    z = (q-1)/(q+1)
    z2 = z*z
    power = z
    total = F(0)
    for k in range(terms):
        total += 2*power/(2*k+1)
        power *= z2
    tail = 2*power/((2*terms+1)*(1-z2))
    return total, total+tail


def log_interval(q):
    assert q > 0
    k, r = 0, q
    while r < 1:
        r *= 2
        k -= 1
    while r >= 2:
        r /= 2
        k += 1
    a, b = log_unit_interval(r)
    c, d = log_unit_interval(F(2))
    if k >= 0:
        return dyadic_out(a+k*c, b+k*d)
    return dyadic_out(a+k*d, b+k*c)


def entropy_interval(law):
    lo, hi = F(0), F(0)
    for mass in law.values():
        p = ff(mass)
        assert p >= 0
        if p:
            a, b = log_interval(p)
            lo -= p*b
            hi -= p*a
    return lo, hi


def decimal_out(q, rounding):
    with localcontext() as ctx:
        ctx.prec = 48
        ctx.rounding = rounding
        return str(Decimal(q.numerator)/Decimal(q.denominator))


def enclosure(lo, hi):
    assert lo <= hi
    return {"lower": decimal_out(lo, ROUND_FLOOR),
            "upper": decimal_out(hi, ROUND_CEILING),
            "sign": "NEGATIVE" if hi < 0 else "POSITIVE" if lo > 0 else "UNRESOLVED"}


def check_rational(t, x):
    matrices, laws, entropies, mins = {}, {}, {}, {}
    for sigma in (-1, 0, 1):
        K = kernel(t, x, sigma)
        assert K == K.T
        law, minors = full_law(K)
        direct = row_law(K)
        assert law == direct
        assert sum(law.values()) == 1 and min(law.values()) >= 0
        _, complement = full_law(sp.eye(4)-K)
        assert all(v > 0 for m, v in minors.items() if m)
        assert all(v > 0 for m, v in complement.items() if m)
        matrices[sigma], laws[sigma] = K, law
        entropies[sigma] = entropy_interval(law)
        mins[sigma] = str(min(law.values()))
    assert matrices[0] == (matrices[-1]+matrices[1])/2
    lo = (entropies[-1][0]+entropies[1][0])/2-entropies[0][1]
    hi = (entropies[-1][1]+entropies[1][1])/2-entropies[0][0]
    return {"t": str(t), "x": str(x), "n": 4,
            "events_per_kernel": 16, "kernels_checked": 3,
            "all_principal_minors_K_and_I_minus_K_positive": True,
            "actual_arithmetic_midpoint": True,
            "mobius_equals_mixed_row_determinant": True,
            "minimum_event_mass": mins, "delta": enclosure(lo, hi)}


def symbolic_laws():
    t, x = sp.symbols("t x", positive=True)
    data = {}
    for sigma in (-1, 0, 1):
        K = kernel(t, x, sigma)
        law = row_law(K)
        assert sp.factor(sum(law.values())-1) == 0
        data[str(sigma)] = {}
        for mask, mass in law.items():
            # Fixed x in (0,1): symbolic cancellations are retained.
            jet = sp.series(mass, t, 0, 4).removeO().expand()
            data[str(sigma)][str(mask)] = {
                "event": [i+1 for i in range(4) if mask >> i & 1],
                "probability": str(mass), "jet_through_t3": str(jet)}
    return data


def smoke():
    K = sp.diag(sp.Rational(1, 3), sp.Rational(2, 5))
    law, _ = full_law(K)
    assert law == {0: sp.Rational(2, 5), 1: sp.Rational(1, 5),
                   2: sp.Rational(4, 15), 3: sp.Rational(2, 15)}
    assert law == row_law(K)
    assert log_interval(F(1))[0] <= 0 <= log_interval(F(1))[1]
    return {"toy_full_law_fixture": "PASS",
            "family_smoke": check_rational(sp.Rational(1, 8), sp.Rational(1, 2))}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["smoke", "symbolic", "certify"], default="smoke")
    parser.add_argument("--output")
    args = parser.parse_args()
    start = time.time()
    record = {"mode": args.mode, "pid": os.getpid(), "seed": None,
              "deterministic": True, "python": platform.python_version(),
              "sympy": sp.__version__, "command": " ".join(sys.argv),
              "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "threads_requested": 1, "gpu": False, "started_unix": start}
    if args.mode == "smoke":
        record["results"] = smoke()
        record["completed_chords"] = 1
    elif args.mode == "symbolic":
        record["results"] = symbolic_laws()
        record["completed_symbolic_events"] = 48
    else:
        pairs = [(d, x) for x in (sp.Rational(1, 4), sp.Rational(1, 2), sp.Rational(3, 4))
                 for d in (16, 64)]
        record["planned_chords"] = len(pairs)
        record["results"] = [check_rational(sp.Rational(1, d), x) for d, x in pairs]
        record["completed_chords"] = len(pairs)
    record["elapsed_seconds"] = time.time()-start
    record["exit_code"] = 0
    rendered = json.dumps(record, indent=2)+"\n"
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
