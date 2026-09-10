#!/usr/bin/env python3
"""Exact finite companion; author check, not an independent review.

Run: python check_exact.py
No third-party dependency, logs, floating arithmetic, or SHA256 procedures.
The mathematical proofs are in lifted_cone.md and explicit_rate_interval.md.
This file's publication alone is not an execution record.
"""
from fractions import Fraction as F
from itertools import product
import json

SIGNS = tuple(product((-1, 1), repeat=2))
B = F(1, 8)


def act(v, s, alpha):
    m, x, y, r, d = v
    a, c = alpha
    ac = a*c
    return (
        m/4-c*x/2-a*y/2+ac*(d+2*r-s*m),
        ac*B*B*(c*m/2-y),
        ac*(B*B*(a*m/2-x)+s*(c*m/2-y)-2*B*(s*m-r)),
        ac*(B*s*(c*m/2-y)-B*B*(s*m-r)),
        ac*B**4*m,
    )


def det(matrix):
    a = [list(row) for row in matrix]
    n = len(a)
    ans = F(1)
    for k in range(n):
        pivot = next((i for i in range(k, n) if a[i][k]), None)
        if pivot is None:
            return F(0)
        if pivot != k:
            a[pivot], a[k] = a[k], a[pivot]
            ans = -ans
        p = a[k][k]
        ans *= p
        for i in range(k+1, n):
            factor = a[i][k]/p
            for j in range(k+1, n):
                a[i][j] -= factor*a[k][j]
    return ans


def mobius_events(t, n):
    q = t/16
    def entry(i, j):
        d = abs(i-j)
        return F(1, 2) if d == 0 else q if d == 1 else B if d == 2 else F(0)
    masses = []
    for mask in range(1 << n):
        sites = [i for i in range(n) if (mask >> i) & 1]
        masses.append(det([[entry(i, j) for j in sites] for i in sites]))
    for bit in range(n):
        for mask in range(1 << n):
            if not ((mask >> bit) & 1):
                masses[mask] -= masses[mask | (1 << bit)]
    return masses


def main():
    count = 0
    for t in (F(1, 2), F(1), F(5, 4), F(3, 2)):
        s = t*t/256
        for n in (2, 4, 6):
            masses = mobius_events(t, n)
            assert sum(masses) == 1 and min(masses) > 0
            for mask, expected in enumerate(masses):
                v = (F(1), F(0), F(0), F(0), F(0))
                for j in reversed(range(n//2)):
                    alpha = tuple(1 if (mask >> (2*j+k)) & 1 else -1 for k in (0, 1))
                    v = act(v, s, alpha)
                assert v[0] == expected, (t, n, mask, v[0], expected)
                count += 1
    # Each moment identity is a polynomial of degree <=2 in s.
    # Three distinct exact interpolation nodes therefore check every coefficient.
    for s in (F(0), F(1, 256), F(9, 1024)):
        for j in range(5):
            v = tuple(F(int(i == j)) for i in range(5))
            total = tuple(sum(act(v, s, alpha)[i] for alpha in SIGNS) for i in range(5))
            assert total == (v[0], F(0), F(0), F(0), F(0))
            moments = [F(0) for _ in range(4)]
            for alpha, beta in product(SIGNS, repeat=2):
                p = act(act(v, s, beta), s, alpha)[0]
                a, c = alpha
                e, f = beta
                for k, obs in enumerate((f, e, e*f, a*e*f)):
                    moments[k] += p*obs
            m, x, y, r, d = v
            assert moments == [-2*x, -2*y, 4*(d+2*r-s*m),
                               8*B*B*x+8*s*y+16*B*s*m-16*B*r]
    inverse_frobenius_upper = F(1861, 1024)+20*F(1, 64)**2
    assert inverse_frobenius_upper == F(933, 512) < 2
    s0 = F(1, 128)
    for s in (F(0), F(1, 256), F(9, 1024)):
        total = F(0)
        for alpha in SIGNS:
            g, nx, ny, nr, nd = act((F(1), F(0), F(0), F(0), F(0)), s, alpha)
            total -= (nr-nx/16+nd/2)**2/g
        assert total == -F(17, 256)*(s-s0)**2/(1-16*s*s)
    s = F(1, 256)
    derivative = -F(17, 128)*(s-s0)*(1-16*s*s0)/(1-16*s*s)**2
    assert derivative == F(34799, 67076100) > 0
    conditional_constant_upper = F(7, 2)**3*F(7, 40)**2*F(13, 50)**2
    assert conditional_constant_upper == F(2840383, 32000000) < F(1, 10)
    sigma, rho = F(9, 8), F(2, 3)
    assert sigma*rho**4 == F(2, 9)
    h_majorant = sigma**3*F(27, 16)+sigma**4/(25*(1-sigma*rho**4))
    assert h_majorant == F(3562623, 1433600) < F(5, 2)
    variation = F(61440, 2**27)
    assert variation == F(15, 32768) < F(1, 2000)
    print(json.dumps({
        'status': 'AUTHOR_EXACT_PASS',
        'complete_event_values_checked': count,
        'moment_polynomial_degree': 2,
        'moment_interpolation_nodes': 3,
        'inverse_frobenius_squared_upper': str(inverse_frobenius_upper),
        'method_counterexample_derivative': str(derivative),
        'complex_h_majorant': str(h_majorant),
        'physical_interval_center': '1',
        'physical_interval_halfwidth': '1/134217728',
        'physical_curvature_upper_threshold': '-1/2000',
        'execution_does_not_constitute_independent_review': True
    }, indent=2))


if __name__ == '__main__':
    main()
