"""Bounded deterministic examples and meaningful exact checks; no search."""
import json
import os
from pathlib import Path
import platform
import time
from fractions import Fraction as F
import block_transfer as bt


def chain(m):
    out = []
    for diagonal in ('3/10', '7/10'):
        a = [['0']*(2*m) for _ in range(2*m)]
        for i in range(2*m):
            a[i][i] = diagonal
        for b in range(m):
            a[2*b][2*b+1] = a[2*b+1][2*b] = '1/10'
        for b in range(m-1):
            for c in range(2):
                i, j = 2*b+c, 2*(b+1)+(1-c)
                a[i][j] = a[j][i] = '3/100'
        out.append(a)
    return {'K0': out[0], 'K1': out[1], 'blocks': [[2*b, 2*b+1] for b in range(m)], 't': '1/2'}


def checks():
    count = 0
    a = bt.matrix([['3/10', '1/10'], ['1/10', '3/10']])
    assert bt.probabilities(a) == [F(12,25), F(11,50), F(11,50), F(2,25)]
    count += 1
    assert bt.log_interval(F(1)) == (0, 0)
    low2, high2 = bt.log_interval(F(2))
    low4, high4 = bt.log_interval(F(4))
    assert low4 == 2*low2 and high4 == 2*high2
    assert high2-low2 < F(1,10**23)
    count += 1
    for m in (1, 2):
        raw = chain(m)
        result = bt.transfer(raw)
        a0, a1 = bt.matrix(raw['K0']), bt.matrix(raw['K1'])
        at = [[(x+y)/2 for x,y in zip(r,s)] for r,s in zip(a0,a1)]
        intervals = [bt.entropy_interval(k) for k in (a0,a1,at)]
        direct = (intervals[2][0]-(intervals[0][1]+intervals[1][1])/2,
                  intervals[2][1]-(intervals[0][0]+intervals[1][0])/2)
        low, high = map(F, result['full_jensen_interval_nats'])
        assert low <= direct[0] <= direct[1] <= high
        assert result['sign_from_exact_enclosure'] == 'POSITIVE'
        count += 1
    for t in ('0', '1'):
        raw = chain(2)
        raw['t'] = t
        result = bt.transfer(raw)
        low, high = map(F, result['full_jensen_interval_nats'])
        assert low <= 0 <= high
        count += 1
    for blocks in ([[0],[0]], [[0]], [[0,1],[]], [[False,1]]):
        try:
            bt.partition(blocks,2)
        except ValueError:
            count += 1
        else:
            raise AssertionError('invalid partition accepted')
    for value in (0.5, True):
        try:
            bt.rational(value)
        except ValueError:
            count += 1
        else:
            raise AssertionError('inexact input accepted')
    projection = bt.matrix([['1/10', '3/10'], ['3/10','9/10']])
    assert bt.probabilities(projection) == [0,F(1,10),F(9,10),0]
    try:
        bt.loss_bound(projection, [[0],[1]])
    except ValueError:
        count += 1  # this feasible matrix shows sufficient test rejection is inconclusive
    else:
        raise AssertionError('unexpected Gershgorin acceptance')
    return count


def main():
    start = time.perf_counter()
    root = Path(__file__).resolve().parent
    passed = checks()
    raw4 = chain(4)
    (root/'chain4_input.json').write_text(json.dumps(raw4,indent=2)+'\n')
    result4 = bt.transfer(raw4)
    result32 = bt.transfer(chain(32))
    report = {
        'status': 'completed', 'pid': os.getpid(), 'python': platform.python_version(),
        'command': 'python3 research/T2/artifacts/demo_checks.py',
        'resource_limit': 'one CPU thread; 8 GiB address-space cap imposed by launcher',
        'test_cases_passed': passed,
        'examples': [result4, result32],
        'full_enumeration_crosscheck_dimensions': [2,4],
        'full_enumeration_masses_evaluated': 3*(4+16),
        'search_parameter_draws': 0,
        'elapsed_seconds': time.perf_counter()-start,
        'exit_status': 0,
        'coverage': 'exact computations for listed inputs; not a global proof or broad scan',
    }
    (root/'demo_results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
