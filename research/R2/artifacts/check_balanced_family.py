#!/usr/bin/env python3
"""Bounded exact-law diagnostic for R2 frozen theorem v1.

All matrices and all event probabilities are rational.  Decimal logarithms are
diagnostic only; the script does not claim an interval certificate.
"""

from __future__ import annotations

import argparse
import itertools
import json
import os
import platform
import time
from decimal import Decimal, getcontext
from fractions import Fraction as F


getcontext().prec = 90


def eye(n):
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def transpose(a):
    return [list(row) for row in zip(*a)]


def matmul(a, b):
    bt = transpose(b)
    return [[sum((x * y for x, y in zip(row, col)), F(0)) for col in bt]
            for row in a]


def add(a, b, alpha=F(1)):
    return [[x + alpha * y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def scale(a, c):
    return [[c * x for x in row] for row in a]


def columns(a, js):
    return [[row[j] for j in js] for row in a]


def principal(a, js):
    return [[a[i][j] for j in js] for i in js]


def det(a):
    n = len(a)
    if n == 0:
        return F(1)
    b = [row[:] for row in a]
    out = F(1)
    for j in range(n):
        pivot = next((i for i in range(j, n) if b[i][j]), None)
        if pivot is None:
            return F(0)
        if pivot != j:
            b[j], b[pivot] = b[pivot], b[j]
            out = -out
        p = b[j][j]
        out *= p
        for k in range(j + 1, n):
            b[j][k] /= p
        for i in range(j + 1, n):
            q = b[i][j]
            if q:
                for k in range(j + 1, n):
                    b[i][k] -= q * b[j][k]
    return out


def givens(n, i, j, c, s):
    g = eye(n)
    g[i][i], g[i][j] = c, -s
    g[j][i], g[j][j] = s, c
    return g


def rational_orthogonal(n, rotations):
    w = eye(n)
    for i, j, c, s in rotations:
        assert c * c + s * s == 1
        w = matmul(givens(n, i, j, c, s), w)
    assert matmul(transpose(w), w) == eye(n)
    return w


def projection(frame):
    return matmul(frame, transpose(frame))


def exact_probabilities(k):
    n = len(k)
    inclusion = []
    for mask in range(1 << n):
        js = [i for i in range(n) if mask >> i & 1]
        inclusion.append(det(principal(k, js)))
    probs = []
    for smask in range(1 << n):
        total = F(0)
        for tmask in range(1 << n):
            if tmask & smask == smask:
                parity = (tmask.bit_count() - smask.bit_count()) & 1
                total += -inclusion[tmask] if parity else inclusion[tmask]
        probs.append(total)
    return probs


def psd_by_principal_minors(a):
    n = len(a)
    return all(det(principal(a, [i for i in range(n) if mask >> i & 1])) >= 0
               for mask in range(1 << n))


def entropy(probs):
    out = Decimal(0)
    for p in probs:
        if p:
            x = Decimal(p.numerator) / Decimal(p.denominator)
            out -= x * x.ln()
    return out


def derivative_minor(u, x, rows):
    r = len(u[0])
    total = F(0)
    for j in range(r):
        a = [[u[i][q] for q in range(r)] for i in rows]
        for q, i in enumerate(rows):
            a[q][j] = x[i][j]
        total += det(a)
    return total


def frac_text(x):
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def dec_text(x):
    return format(x, ".35E")


def fixture(name, n, r, rotations, b, tau):
    w = rational_orthogonal(n, rotations)
    u = columns(w, range(r))
    v = columns(w, range(r, n))
    p = projection(u)
    q = add(eye(n), p, F(-1))
    d = add(matmul(matmul(u, b), transpose(v)),
            matmul(matmul(v, transpose(b)), transpose(u)))
    x = matmul(v, transpose(b))
    frob = sum((z * z for row in b for z in row), F(0))
    zzero = F(0)
    zero_plucker = 0
    for rows in itertools.combinations(range(n), r):
        psi = det([[u[i][j] for j in range(r)] for i in rows])
        phi = derivative_minor(u, x, rows)
        if psi == 0:
            zero_plucker += 1
            zzero += phi * phi
    assert F(0) <= zzero <= frob
    assert tau * tau * frob < 1  # sufficient for tau*||B||op<1
    return {"name": name, "n": n, "r": r, "P": p, "Q": q, "D": d,
            "tau": tau, "F": frob, "Z": zzero,
            "zero_plucker": zero_plucker}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output")
    args = parser.parse_args()
    started = time.time()
    rotations4 = [
        (0, 1, F(3, 5), F(4, 5)),
        (1, 2, F(5, 13), F(12, 13)),
        (2, 3, F(7, 25), F(24, 25)),
        (0, 3, F(8, 17), F(15, 17)),
    ]
    rotations3 = [
        (0, 1, F(3, 5), F(4, 5)),
        (1, 2, F(5, 13), F(12, 13)),
        (0, 2, F(7, 25), F(24, 25)),
    ]
    fixtures = [
        fixture("coordinate-r2-n4", 4, 2, [],
                [[F(1, 4), F(1, 5)], [F(1, 6), F(-1, 7)]], F(1, 2)),
        fixture("generic-r2-n4", 4, 2, rotations4,
                [[F(1, 4), F(-1, 8)], [F(1, 9), F(1, 7)]], F(2, 3)),
        fixture("generic-r1-n3", 3, 1, rotations3,
                [[F(2, 7), F(-1, 5)]], F(3, 4)),
    ]
    ks = [3, 7, 15, 31, 63, 127, 255, 511, 1023, 2047]
    rows = []
    checks = 0
    failures = []
    for case in fixtures:
        predicted = case["tau"] ** 2 * (case["Z"] - 2 * case["F"])
        for kval in ks:
            eps = F(1, 1 + kval * kval)
            root = F(kval, 1 + kval * kval)  # sqrt(eps*(1-eps))
            t = case["tau"] * root
            m = add(scale(case["P"], 1 - eps), scale(case["Q"], eps))
            km = add(m, case["D"], -t)
            kp = add(m, case["D"], t)
            for label, a in (("minus", km), ("mid", m), ("plus", kp)):
                ok_psd = psd_by_principal_minors(a)
                ok_comp = psd_by_principal_minors(add(eye(case["n"]), a, F(-1)))
                probs = exact_probabilities(a)
                checks += len(probs)
                if not (ok_psd and ok_comp and min(probs) >= 0 and sum(probs, F(0)) == 1):
                    failures.append({"fixture": case["name"], "k": kval, "point": label})
                if label == "minus":
                    hminus = entropy(probs)
                elif label == "mid":
                    hmid = entropy(probs)
                else:
                    hplus = entropy(probs)
            delta = (hminus + hplus) / Decimal(2) - hmid
            de = Decimal(eps.numerator) / Decimal(eps.denominator)
            normalizer = de * (-de.ln())
            normalized = delta / normalizer
            rows.append({
                "fixture": case["name"], "k": kval,
                "epsilon": frac_text(eps),
                "delta": dec_text(delta),
                "normalized": dec_text(normalized),
                "predicted_limit": frac_text(predicted),
                "strict_negative": delta < 0,
            })
    payload = {
        "status": "completed" if not failures else "failed",
        "purpose": "bounded diagnostic, not an interval certificate",
        "implementation": "independent exact Mobius enumeration with rational matrices",
        "python": platform.python_version(),
        "pid": os.getpid(),
        "thread_caps": {k: os.environ.get(k) for k in
                        ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS")},
        "fixtures_planned": len(fixtures),
        "fixtures_completed": len(fixtures),
        "epsilon_values_per_fixture": len(ks),
        "chords_completed": len(rows),
        "event_masses_checked": checks,
        "failures": failures,
        "fixture_coefficients": [
            {"name": c["name"], "n": c["n"], "r": c["r"],
             "F": frac_text(c["F"]), "Z": frac_text(c["Z"]),
             "zero_plucker": c["zero_plucker"]}
            for c in fixtures
        ],
        "rows": rows,
        "wall_seconds": round(time.time() - started, 6),
    }
    text = json.dumps(payload, indent=2, sort_keys=True)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text + "\n")
    print(text)
    return 0 if not failures and all(row["strict_negative"] for row in rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
