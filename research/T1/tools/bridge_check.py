"""Exact rational applicability checker for T1 frozen theorem v1 (D = i A)."""
from fractions import Fraction as Q
import argparse
import json


def rational_matrix(raw):
    if not isinstance(raw, list) or not raw:
        raise ValueError('expected a nonempty square matrix')
    n = len(raw)
    if any(not isinstance(row, list) or len(row) != n for row in raw):
        raise ValueError('expected a square matrix')
    if any(type(x) not in (str, int) for row in raw for x in row):
        raise ValueError('use integer entries or exact rational strings; floats rejected')
    return [[Q(x) for x in row] for row in raw]


def positive_pivots(m):
    """Exact unpivoted LDL: positive pivots iff a real symmetric matrix is PD."""
    n = len(m)
    l = [[Q(0) for _ in range(n)] for _ in range(n)]
    pivots = []
    for j in range(n):
        p = m[j][j] - sum(l[j][k]**2 * pivots[k] for k in range(j))
        if p <= 0:
            return None
        pivots.append(p)
        l[j][j] = Q(1)
        for i in range(j + 1, n):
            l[i][j] = (m[i][j] - sum(l[i][k]*l[j][k]*pivots[k]
                                      for k in range(j))) / p
    return pivots


def graph_bridges(k):
    """Iterative Tarjan traversal, O(n^2) construction plus O(n+m) traversal."""
    n = len(k)
    adj = [[j for j in range(n) if j != i and k[i][j] != 0] for i in range(n)]
    disc = [-1] * n
    low = [0] * n
    parent = [-1] * n
    tick = 0
    bridges = set()
    for root in range(n):
        if disc[root] >= 0:
            continue
        disc[root] = low[root] = tick
        tick += 1
        stack = [(root, iter(adj[root]))]
        while stack:
            v, it = stack[-1]
            w = next(it, None)
            if w is None:
                stack.pop()
                p = parent[v]
                if p >= 0:
                    low[p] = min(low[p], low[v])
                    if low[v] > disc[p]:
                        bridges.add(tuple(sorted((p, v))))
            elif w != parent[v]:
                if disc[w] < 0:
                    parent[w] = v
                    disc[w] = low[w] = tick
                    tick += 1
                    stack.append((w, iter(adj[w])))
                else:
                    low[v] = min(low[v], disc[w])
    return bridges


def check(raw):
    try:
        k, a = rational_matrix(raw['K']), rational_matrix(raw['A'])
        n = len(k)
        if len(a) != n:
            raise ValueError('K and A dimensions differ')
        if any(k[i][j] != k[j][i] for i in range(n) for j in range(n)):
            raise ValueError('K must be real symmetric')
        if any(a[i][j] != -a[j][i] for i in range(n) for j in range(n)):
            raise ValueError('A must be real skew-symmetric; D=iA')
        kp = positive_pivots(k)
        ip = positive_pivots([[Q(i == j)-k[i][j] for j in range(n)] for i in range(n)])
        if kp is None or ip is None:
            return {'status': 'OUTSIDE_DOMAIN', 'reason': 'strict contraction required'}
        bridges = graph_bridges(k)
        active = [(i, j) for i in range(n) for j in range(i+1, n) if a[i][j]]
        invalid = [edge for edge in active if edge not in bridges]
        if invalid:
            return {'status': 'INCONCLUSIVE', 'reason': 'active non-bridge or absent edge',
                    'unsupported_edges': invalid}
        return {'status': 'APPLICABLE', 'curvature_sign': 'negative' if active else 'zero',
                'theorem': 'frozen_theorem_v1', 'n': n,
                'bridges': sorted(bridges), 'active_edges': active,
                'K_ldl_pivots': list(map(str, kp)), 'I_minus_K_ldl_pivots': list(map(str, ip)),
                'event_probabilities_evaluated': 0,
                'arithmetic': 'exact rational; sign relies on the cited theorem'}
    except (KeyError, TypeError, ValueError, ZeroDivisionError) as exc:
        return {'status': 'INVALID_INPUT', 'reason': str(exc)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', help='JSON object with rational K and A; direction is iA')
    args = parser.parse_args()
    with open(args.input, encoding='utf-8') as f:
        print(json.dumps(check(json.load(f)), indent=2))
