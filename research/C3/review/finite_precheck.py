#!/usr/bin/env python3
"""Finite exact-row DPP jet checks for the C3 review.

This script uses only Python's standard library.  It implements exact rational
complex arithmetic and computes event probabilities as exact-row determinants.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations
import math
import platform
import sys


VERSION = "finite_precheck.py 2026-09-09.a"


class CR:
    __slots__ = ("re", "im")

    def __init__(self, re=0, im=0):
        self.re = re if isinstance(re, Fraction) else Fraction(re)
        self.im = im if isinstance(im, Fraction) else Fraction(im)

    def __add__(self, other):
        other = as_cr(other)
        return CR(self.re + other.re, self.im + other.im)

    __radd__ = __add__

    def __neg__(self):
        return CR(-self.re, -self.im)

    def __sub__(self, other):
        return self + (-as_cr(other))

    def __rsub__(self, other):
        return as_cr(other) + (-self)

    def __mul__(self, other):
        other = as_cr(other)
        return CR(
            self.re * other.re - self.im * other.im,
            self.re * other.im + self.im * other.re,
        )

    __rmul__ = __mul__

    def __eq__(self, other):
        other = as_cr(other)
        return self.re == other.re and self.im == other.im

    def __bool__(self):
        return self.re != 0 or self.im != 0

    def conj(self):
        return CR(self.re, -self.im)

    def to_complex(self):
        return complex(float(self.re), float(self.im))

    def real_fraction(self):
        if self.im != 0:
            raise ValueError(f"expected real CR, got {self}")
        return self.re

    def __repr__(self):
        if self.im == 0:
            return str(self.re)
        if self.re == 0:
            return f"{self.im}*i"
        sign = "+" if self.im > 0 else "-"
        return f"{self.re}{sign}{abs(self.im)}*i"


def as_cr(x):
    return x if isinstance(x, CR) else CR(x)


ZERO = CR(0)
ONE = CR(1)
IUNIT = CR(0, 1)


def cfrac(num, den=1):
    return CR(Fraction(num, den))


def ccomplex(re_num, re_den, im_num=0, im_den=1):
    return CR(Fraction(re_num, re_den), Fraction(im_num, im_den))


def poly_add(a, b):
    out = [ZERO] * max(len(a), len(b))
    for idx, val in enumerate(a):
        out[idx] = out[idx] + val
    for idx, val in enumerate(b):
        out[idx] = out[idx] + val
    return out


def poly_mul(a, b):
    out = [ZERO] * (len(a) + len(b) - 1)
    for i, av in enumerate(a):
        if not av:
            continue
        for j, bv in enumerate(b):
            if bv:
                out[i + j] = out[i + j] + av * bv
    return out


def perm_sign(perm):
    inv = 0
    for i in range(len(perm)):
        for j in range(i + 1, len(perm)):
            inv += perm[i] > perm[j]
    return -1 if inv % 2 else 1


def det_poly(A0, A1):
    n = len(A0)
    out = [ZERO] * (n + 1)
    for perm in permutations(range(n)):
        term = [ONE]
        for i, j in enumerate(perm):
            term = poly_mul(term, [A0[i][j], A1[i][j]])
        if perm_sign(perm) < 0:
            term = [-x for x in term]
        out = poly_add(out, term)
    return out


def coeff_lookup(coeffs, k):
    if k in coeffs:
        return coeffs[k]
    if -k in coeffs:
        return coeffs[-k].conj()
    return ZERO


def toeplitz(n, coeffs):
    return [[coeff_lookup(coeffs, (i + 1) - (j + 1)) for j in range(n)] for i in range(n)]


def direction_D(K):
    n = len(K)
    return [
        [IUNIT * Fraction((i + 1) - (j + 1)) * K[i][j] for j in range(n)]
        for i in range(n)
    ]


def direction_E(K):
    n = len(K)
    return [
        [Fraction(((i + 1) - (j + 1)) ** 2) * K[i][j] for j in range(n)]
        for i in range(n)
    ]


def event_row_matrices(K, X, mask):
    n = len(K)
    A0 = []
    A1 = []
    for i in range(n):
        in_s = (mask >> i) & 1
        row0 = []
        row1 = []
        for j in range(n):
            delta = ONE if i == j else ZERO
            if in_s:
                row0.append(K[i][j])
                row1.append(X[i][j])
            else:
                row0.append(delta - K[i][j])
                row1.append(-X[i][j])
        A0.append(row0)
        A1.append(row1)
    return A0, A1


def event_name(mask, n):
    s = [str(i + 1) for i in range(n) if (mask >> i) & 1]
    return "{" + ",".join(s) + "}"


def real_float(z):
    return float(z.real_fraction())


def analyze_object(name, coeffs, exact_table):
    n = max(abs(k) for k in coeffs) + 1
    K = toeplitz(n, coeffs)
    D = direction_D(K)
    E = direction_E(K)
    nonzero_D = sum(1 for row in D for x in row if x)

    row_bounds = []
    for i in range(n):
        b = Fraction(0)
        for j in range(n):
            if i == j:
                continue
            z = K[i][j]
            # Rational L1 bound on |z|, sufficient for Gershgorin.
            b += abs(z.re) + abs(z.im)
        row_bounds.append(b)

    print()
    print(f"OBJECT {name}")
    print(f"n={n}")
    print(f"c0={coeffs[0]}")
    print(f"row_l1_bounds={','.join(str(x) for x in row_bounds)}")
    print(f"strict_contraction_by_gershgorin={max(row_bounds) < Fraction(1, 2)}")
    print(f"nonzero_D_entries={nonzero_D}")

    sum_p = ZERO
    sum_pd = ZERO
    sum_pdd = ZERO
    sum_pe = ZERO
    min_p = None
    hdd = 0.0
    bad = []

    print("events:")
    for mask in range(1 << n):
        A0D, A1D = event_row_matrices(K, D, mask)
        polyD = det_poly(A0D, A1D)
        A0E, A1E = event_row_matrices(K, E, mask)
        polyE = det_poly(A0E, A1E)

        p = polyD[0]
        pd = polyD[1] if len(polyD) > 1 else ZERO
        pdd = (polyD[2] if len(polyD) > 2 else ZERO) * 2
        pe = polyE[1] if len(polyE) > 1 else ZERO

        if pd != ZERO:
            bad.append((mask, "pD_prime", pd))
        if pdd != pe:
            bad.append((mask, "pD_second_minus_pE_prime", pdd - pe))

        pr = p.real_fraction()
        pddr = pdd.real_fraction()
        per = pe.real_fraction()
        sum_p += p
        sum_pd += pd
        sum_pdd += pdd
        sum_pe += pe
        min_p = pr if min_p is None else min(min_p, pr)
        hdd += -float(pddr) * math.log(float(pr))

        if exact_table:
            print(
                f"  mask={mask:0{n}b} S={event_name(mask, n)} "
                f"p={pr} pD_prime={pd} pD_second={pddr} pE_prime={per} "
                f"relation_exact={pdd == pe}"
            )
        else:
            print(
                f"  mask={mask:0{n}b} S={event_name(mask, n)} "
                f"p≈{float(pr):.12g} pD_prime={pd} "
                f"pD_second≈{float(pddr):+.12g} pE_prime≈{float(per):+.12g} "
                f"relation_exact={pdd == pe}"
            )

    print(f"sum_p={sum_p}")
    print(f"sum_pD_prime={sum_pd}")
    print(f"sum_pD_second={sum_pdd}")
    print(f"sum_pE_prime={sum_pe}")
    print(f"min_p={min_p} ({float(min_p):.12g})")
    print(f"all_exact_checks_pass={not bad}")
    if bad:
        print(f"bad_checks={bad!r}")
    print(f"Hdd_affine_D_equals_dH_E≈{hdd:+.17g}")
    print(f"Hdd_sign={'positive' if hdd > 0 else 'negative' if hdd < 0 else 'zero'}")


def main():
    print(VERSION)
    print("python", sys.version.replace("\n", " "))
    print("platform", platform.platform())
    print("arithmetic=exact rational complex coefficients; entropy logs=float only")

    analyze_object(
        "A_real_symmetric_toeplitz_n3",
        {
            0: cfrac(1, 2),
            1: cfrac(1, 10),
            2: cfrac(1, 20),
        },
        exact_table=True,
    )

    analyze_object(
        "B_complex_hermitian_toeplitz_n4",
        {
            0: cfrac(1, 2),
            1: ccomplex(1, 20, 1, 30),
            2: ccomplex(-1, 40, 1, 50),
            3: ccomplex(1, 100, -1, 120),
        },
        exact_table=False,
    )


if __name__ == "__main__":
    main()
