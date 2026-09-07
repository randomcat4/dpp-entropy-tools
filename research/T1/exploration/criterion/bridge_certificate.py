#!/usr/bin/env python3
"""Exact rational premise checker for T1 frozen theorem v1; no event enumeration."""
from fractions import Fraction
import json
import sys


def rational(x):
    if isinstance(x, bool) or not isinstance(x, (int, str)):
        raise ValueError("entries must be integers or rational strings; floats are not exact inputs")
    return Fraction(x)


def matrix(raw, name):
    if not isinstance(raw, list) or not raw:
        raise ValueError(name + " must be a nonempty square matrix")
    n = len(raw)
    if any(not isinstance(row, list) or len(row) != n for row in raw):
        raise ValueError(name + " must be square")
    return [[rational(x) for x in row] for row in raw]


def positive_ldl_pivots(M):
    """Return exact LDL^T diagonal pivots; raise on a nonpositive pivot."""
    n = len(M)
    L = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    pivots = []
    for j in range(n):
        p = M[j][j] - sum(L[j][k] ** 2 * pivots[k] for k in range(j))
        if p <= 0:
            raise ValueError("nonpositive LDL pivot at index " + str(j))
        pivots.append(p)
        L[j][j] = 1
        for i in range(j + 1, n):
            L[i][j] = (M[i][j] - sum(L[i][k] * L[j][k] * pivots[k]
                                    for k in range(j))) / p
    return pivots


def graph_bridges(adjacency):
    """Iterative undirected DFS low links: O(n+m), no recursion limit."""
    n = len(adjacency)
    discovery = [-1] * n
    low = [-1] * n
    parent = [-1] * n
    clock = 0
    bridges = set()
    for root in range(n):
        if discovery[root] >= 0:
            continue
        discovery[root] = low[root] = clock
        clock += 1
        stack = [(root, iter(adjacency[root]))]
        while stack:
            v, neighbors = stack[-1]
            w = next(neighbors, None)
            if w is None:
                stack.pop()
                p = parent[v]
                if p >= 0:
                    if low[v] > discovery[p]:
                        bridges.add(tuple(sorted((p, v))))
                    low[p] = min(low[p], low[v])
            elif w != parent[v]:
                if discovery[w] < 0:
                    parent[w] = v
                    discovery[w] = low[w] = clock
                    clock += 1
                    stack.append((w, iter(adjacency[w])))
                else:
                    low[v] = min(low[v], discovery[w])
    return bridges


def certify(payload):
    try:
        K, A = matrix(payload['K'], 'K'), matrix(payload['A'], 'A')
        n = len(K)
        if len(A) != n:
            raise ValueError('K and A dimensions differ')
        if any(K[i][j] != K[j][i] for i in range(n) for j in range(n)):
            raise ValueError('K is not symmetric')
        if any(A[i][j] != -A[j][i] for i in range(n) for j in range(n)):
            raise ValueError('A is not skew-symmetric')
        k_pivots = positive_ldl_pivots(K)
        complement = [[Fraction(int(i == j)) - K[i][j] for j in range(n)] for i in range(n)]
        complement_pivots = positive_ldl_pivots(complement)
    except (KeyError, TypeError, ValueError, ZeroDivisionError) as err:
        return {'status': 'INVALID_INPUT', 'reason': str(err)}
    adjacency = [[j for j in range(n) if j != i and K[i][j] != 0] for i in range(n)]
    bridges = graph_bridges(adjacency)
    support = {(i, j) for i in range(n) for j in range(i + 1, n) if A[i][j] != 0}
    rejected = support - bridges
    if rejected:
        return {'status': 'NOT_APPLICABLE', 'reason': 'direction includes a nonbridge or absent edge',
                'rejected_edges_zero_based': sorted(rejected),
                'curvature': 'NO_CONCLUSION'}
    return {'status': 'THEOREM_CONDITIONS_SATISFIED',
            'theorem': 'research/T1/frozen_theorem_v1.md',
            'theorem_independent_verification': 'PENDING',
            'dimension': n,
            'curvature_by_theorem': 'STRICTLY_NEGATIVE' if support else 'ZERO',
            'bridges_zero_based': sorted(bridges),
            'direction_edges_zero_based': sorted(support),
            'K_ldl_pivots': list(map(str, k_pivots)),
            'I_minus_K_ldl_pivots': list(map(str, complement_pivots)),
            'event_probabilities_evaluated': 0}


if __name__ == '__main__':
    try:
        if len(sys.argv) != 2:
            raise ValueError('usage: bridge_certificate.py INPUT.json')
        with open(sys.argv[1], encoding='utf-8') as handle:
            result = certify(json.load(handle))
    except (OSError, ValueError) as err:
        result = {'status': 'INVALID_INPUT', 'reason': str(err)}
    print(json.dumps(result, indent=2))
    sys.exit(0 if result['status'] == 'THEOREM_CONDITIONS_SATISFIED' else 2)
