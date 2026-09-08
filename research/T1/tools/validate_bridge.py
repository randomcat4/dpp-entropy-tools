"""Bounded regression and diagnostic run; not a proof by search."""
import copy
import itertools
import json
import math
import os
import platform
import resource
import time
from fractions import Fraction as Q
from pathlib import Path
from bridge_check import check, graph_bridges


def family(blocks):
    n = 3*blocks
    k = [[Q(i == j, 2) for j in range(n)] for i in range(n)]
    a = [[Q(0) for _ in range(n)] for _ in range(n)]
    for b in range(blocks):
        for i, j in itertools.combinations(range(3*b, 3*b+3), 2):
            k[i][j] = k[j][i] = Q(1, 20)
    for b in range(blocks-1):
        i, j = 3*b+2, 3*b+3
        k[i][j] = k[j][i] = Q(1, 40)
        a[i][j], a[j][i] = Q(b+1, 30), -Q(b+1, 30)
    return {'K': [[str(x) for x in row] for row in k],
            'A': [[str(x) for x in row] for row in a]}


def numerical_curvature(raw):
    k = [[float(Q(x)) for x in row] for row in raw['K']]
    d = [[1j*float(Q(x)) for x in row] for row in raw['A']]
    n = len(k)
    total, score_max, mass, d2mass = 0., 0., 0., 0.
    for bits in itertools.product((0, 1), repeat=n):
        absent = [1-b for b in bits]
        m = [[complex(k[i][j] - (absent[i] if i == j else 0)) for j in range(n)]
             + d[i][:] for i in range(n)]
        det = complex(1)
        for col in range(n):
            pivot = max(range(col, n), key=lambda i: abs(m[i][col]))
            if pivot != col:
                m[col], m[pivot] = m[pivot], m[col]
                det = -det
            factor = m[col][col]
            assert abs(factor) > 1e-15
            det *= factor
            m[col] = [x/factor for x in m[col]]
            for i in range(n):
                if i != col:
                    factor = m[i][col]
                    m[i] = [x-factor*y for x,y in zip(m[i], m[col])]
        p = ((-1)**sum(absent)*det).real
        assert p > 0
        v = [row[n:] for row in m]
        trace = sum(v[i][i] for i in range(n))
        dp = p*trace
        d2p = p*(trace**2-sum(v[i][j]*v[j][i] for i in range(n) for j in range(n)))
        total += (-dp**2/p - d2p*math.log(p)).real
        score_max = max(score_max, abs(dp))
        mass += p
        d2mass += d2p.real
    assert abs(mass-1) < 1e-12 and abs(d2mass) < 1e-12
    return {'n': n, 'events': 2**n, 'H_second_float64': total,
            'max_abs_p_first': score_max, 'mass': mass, 'second_mass': d2mass,
            'role': 'floating diagnostic, not a numerical certificate'}


def run():
    started = time.time()
    out = Path(__file__).resolve().parents[1]/'artifacts'
    out.mkdir(exist_ok=True)
    cases = []
    for blocks in (2, 10):
        raw = family(blocks)
        (out/f'triangles_{blocks}.json').write_text(json.dumps(raw, indent=2)+'\n')
        result = check(raw)
        assert result['status'] == 'APPLICABLE' and result['curvature_sign'] == 'negative'
        assert len(result['active_edges']) == blocks-1
        cases.append({'case': f'{blocks} triangles joined by bridges', 'result': result})
    raw = family(2)
    zero = copy.deepcopy(raw)
    zero['A'] = [[0]*6 for _ in range(6)]
    assert check(zero)['curvature_sign'] == 'zero'
    cycle = copy.deepcopy(raw)
    cycle['A'][0][1], cycle['A'][1][0] = '1/30', '-1/30'
    assert check(cycle)['status'] == 'INCONCLUSIVE'
    absent = copy.deepcopy(raw)
    absent['A'][0][5], absent['A'][5][0] = '1/30', '-1/30'
    assert check(absent)['status'] == 'INCONCLUSIVE'
    assert check({'K': [[0]], 'A': [[0]]})['status'] == 'OUTSIDE_DOMAIN'
    assert check({'K': [[0.5]], 'A': [[0]]})['status'] == 'INVALID_INPUT'
    assert check({'K': [['1/2']], 'A': [[1]]})['status'] == 'INVALID_INPUT'
    assert check({'K': [['1/2', 0],[1,'1/2']], 'A': [[0,0],[0,0]]})['status'] == 'INVALID_INPUT'
    # Exhaustive graph-only cross-check, n<=4, against deleting each edge.
    graph_count = 0
    for n in range(1, 5):
        pairs = list(itertools.combinations(range(n), 2))
        for mask in range(2**len(pairs)):
            edges = {e for z, e in enumerate(pairs) if mask >> z & 1}
            k = [[int(tuple(sorted((i,j))) in edges) for j in range(n)] for i in range(n)]
            expected = set()
            for edge in edges:
                seen = {edge[0]}; todo = [edge[0]]
                while todo:
                    v = todo.pop()
                    for x, y in edges-{edge}:
                        w = y if x == v else x if y == v else None
                        if w is not None and w not in seen:
                            seen.add(w); todo.append(w)
                if edge[1] not in seen:
                    expected.add(edge)
            assert graph_bridges(k) == expected
            graph_count += 1
    diagnostics = [numerical_curvature(raw)]
    assert diagnostics[0]['H_second_float64'] < 0
    result = {'exit_status': 0, 'pid': os.getpid(), 'python': platform.python_version(),
              'command': 'python3 research/T1/tools/validate_bridge.py',
              'thread_limit': 1, 'elapsed_seconds': time.time()-started,
              'max_rss_KiB': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'structural_cases': cases, 'other_interface_cases_passed': 7,
              'graph_cases_passed': graph_count, 'diagnostics': diagnostics,
              'certification': 'exact input checks; theorem independently reviewed separately'}
    (out/'validation.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'structural_cases'}, indent=2))


if __name__ == '__main__':
    run()
