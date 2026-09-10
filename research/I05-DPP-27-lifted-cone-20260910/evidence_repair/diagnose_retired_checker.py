#!/usr/bin/env python3
"""NEW, single-case author diagnostic; not an interval or independent checker.

The old act formula is a literal transcription of the published PR112 source
at 2c249eb5ebc11217d7f87b51a0ce8ea51fea21db. Only the first returned component
is changed in the corrected=True comparison. No other old assertions are
claimed to be repaired. This file was written during the evidence repair.
"""
from fractions import Fraction as F
from itertools import permutations
import json

B = F(1, 8)


def act(v, s, alpha, corrected=False):
    m, x, y, r, d = v
    a, c = alpha
    ac = a*c
    mass = (m/4-a*x/2-c*y/2 if corrected else m/4-c*x/2-a*y/2)
    return (
        mass+ac*(d+2*r-s*m),
        ac*B*B*(c*m/2-y),
        ac*(B*B*(a*m/2-x)+s*(c*m/2-y)-2*B*(s*m-r)),
        ac*(B*s*(c*m/2-y)-B*B*(s*m-r)),
        ac*B**4*m,
    )


def determinant(a):
    total = F(0)
    for p in permutations(range(len(a))):
        inversions = sum(p[i] > p[j] for i in range(len(a))
                         for j in range(i+1, len(a)))
        term = F((-1)**inversions)
        for i, j in enumerate(p):
            term *= a[i][j]
        total += term
    return total


def main():
    t, n, mask = F(1, 2), 4, 1
    q, s = t/16, t*t/256
    kernel = [[F(1, 2) if i == j else q if abs(i-j) == 1
               else B if abs(i-j) == 2 else F(0)
               for j in range(n)] for i in range(n)]
    event = [row[:] for row in kernel]
    for i in range(n):
        if not (mask >> i) & 1:
            event[i][i] -= 1
    direct = (-1)**(n-mask.bit_count())*determinant(event)
    mobius = F(0)
    for sup in range(1 << n):
        if sup & mask == mask:
            sites = [i for i in range(n) if (sup >> i) & 1]
            minor = [[kernel[i][j] for j in sites] for i in sites]
            mobius += (-1)**(sup.bit_count()-mask.bit_count())*determinant(minor)
    results = []
    for corrected in (False, True):
        v = (F(1), F(0), F(0), F(0), F(0))
        for j in reversed(range(n//2)):
            alpha = tuple(1 if (mask >> (2*j+k)) & 1 else -1 for k in (0, 1))
            v = act(v, s, alpha, corrected)
        results.append(v[0])
    old, corrected = results
    assert direct == mobius == F(65055, 1048576)
    assert old == F(65823, 1048576) and old != direct
    assert corrected == direct
    print(json.dumps({
        'status': 'REPRODUCED_OLD_CHECKER_FAILURE_SINGLE_CASE',
        'input': {'t': str(t), 'n': n, 'mask': mask},
        'old_formula_mass': str(old),
        'complete_signed_determinant_mass': str(direct),
        'complete_mobius_mass': str(mobius),
        'corrected_first_component_mass': str(corrected),
        'old_error': str(old-direct),
        'scope': 'One diagnostic case only. The old checker is retired, not validated.',
        'historical_production_evidence': False,
        'independent_review': False,
        'wide_interval_certificate': False
    }, indent=2))


if __name__ == '__main__':
    main()
