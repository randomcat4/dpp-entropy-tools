"""Independent exact full-event derivative reconstruction; Python standard library.

Two implementations are compared: 5x5 principal-minor inclusion-exclusion,
and the fixed rank-three event formulas. No author validation code is imported.
Coordinates are (A11,A22,A33,A12,A13,A23), with symmetric off-diagonals.
"""
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path
import argparse
import json
import platform
import time

N = 6
PAIRS = [(i, j) for i in range(N) for j in range(i, N)]
ZERO = F(0)


class Jet:
    def __init__(self, c=0, g=None, h=None):
        self.c = F(c)
        self.g = tuple(g) if g is not None else (ZERO,) * N
        self.h = tuple(h) if h is not None else (ZERO,) * len(PAIRS)

    def __add__(self, other):
        b = other if isinstance(other, Jet) else Jet(other)
        return Jet(self.c+b.c, [x+y for x,y in zip(self.g,b.g)],
                   [x+y for x,y in zip(self.h,b.h)])

    __radd__ = __add__

    def __neg__(self):
        return Jet(-self.c, [-x for x in self.g], [-x for x in self.h])

    def __sub__(self, other):
        return self + -(other if isinstance(other, Jet) else Jet(other))

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        b = other if isinstance(other, Jet) else Jet(other)
        return Jet(self.c*b.c,
                   [self.g[i]*b.c+self.c*b.g[i] for i in range(N)],
                   [self.h[k]*b.c+self.c*b.h[k]+self.g[i]*b.g[j]+self.g[j]*b.g[i]
                    for k,(i,j) in enumerate(PAIRS)])

    __rmul__ = __mul__

    def values(self):
        return (self.c, *self.g, *self.h)

    def serial(self):
        return {'p':str(self.c), 'gradient':[str(x) for x in self.g],
                'hessian_upper':[str(x) for x in self.h]}


def det(m):
    out = Jet(0)
    for perm in permutations(range(len(m))):
        sign = (-1) ** sum(perm[i] > perm[j] for i in range(len(m))
                           for j in range(i+1,len(m)))
        term = Jet(sign)
        for i,j in enumerate(perm):
            term = term*m[i][j]
        out = out+term
    return out


def matmul(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a):
    return [list(row) for row in zip(*a)]


U = [[F(x,1045) for x in r] for r in
     [[615,120,-702],[240,735,246],[-630,30,-71],
      [480,-620,492],[-170,-390,-540]]]


def input_jets(a):
    coords = {(0,0):0,(1,1):1,(2,2):2,(0,1):3,(0,2):4,(1,2):5}
    return [[Jet(a[i][j],[F(k==coords[tuple(sorted((i,j)))]) for k in range(N)])
             for j in range(3)] for i in range(3)]


def inclusion_events(a):
    k = matmul(matmul(U,input_jets(a)),transpose(U))
    minors = {}
    for mask in range(32):
        ids = [i for i in range(5) if mask >> i & 1]
        minors[mask] = det([[k[i][j] for j in ids] for i in ids])
    events = []
    for mask in range(32):
        events.append(sum(((-1)**(top.bit_count()-mask.bit_count()))*value
                          for top,value in minors.items() if top & mask == mask))
    return events


def formula_events(a):
    a = input_jets(a)
    tr = sum(a[i][i] for i in range(3))
    aa = matmul(a,a)
    e2 = (tr*tr-sum(aa[i][i] for i in range(3)))*F(1,2)
    d = det(a)
    adj = [[aa[i][j]-tr*a[i][j]+(e2 if i==j else 0) for j in range(3)]
           for i in range(3)]
    d1 = [[aa[i][j]+(1-tr)*a[i][j]+(d if i==j else 0) for j in range(3)]
          for i in range(3)]
    d2 = [[adj[i][j]-(d if i==j else 0) for j in range(3)] for i in range(3)]
    events = []
    for mask in range(32):
        ids = [i for i in range(5) if mask >> i & 1]
        if len(ids)==0:
            value = det([[(1 if i==j else 0)-a[i][j] for j in range(3)]
                         for i in range(3)])
        elif len(ids)==1:
            r = U[ids[0]]
            value = sum(r[i]*d1[i][j]*r[j] for i in range(3) for j in range(3))
        elif len(ids)==2:
            r,s = (U[k] for k in ids)
            w = [r[1]*s[2]-r[2]*s[1],r[2]*s[0]-r[0]*s[2],r[0]*s[1]-r[1]*s[0]]
            value = sum(w[i]*d2[i][j]*w[j] for i in range(3) for j in range(3))
        elif len(ids)==3:
            q = det([U[i] for i in ids]).c**2
            value = q*d
        else:
            value = Jet(0)
        events.append(value)
    return events


def diag(values):
    return [[F(values[i]) if i==j else ZERO for j in range(3)] for i in range(3)]


def frozen_inputs(input_path=None):
    if input_path:
        spec = json.loads(Path(input_path).read_text(encoding='utf-8-sig'))
        cases = []
        for item in spec['centers']:
            q = [[F(x) for x in row] for row in spec['rotations'][item['rotation']]]
            assert matmul(transpose(q),q)==diag([1,1,1])
            assert all(F(1,4)<=F(x)<=F(3,4) for x in item['eigenvalues'])
            a = matmul(matmul(q,diag(item['eigenvalues'])),transpose(q))
            cases.append((item['name'],a))
        return cases
    v = [F(1),F(2),F(3)]
    q = [[F(i==j)-v[i]*v[j]/7 for j in range(3)] for i in range(3)]
    diagonal = diag(['1/4','1/2','3/4'])
    repeated = diag(['1/4','1/4','3/4'])
    return [('scalar_half',diag(['1/2']*3)), ('spectral_endpoints',diagonal),
            ('rotated_endpoints',matmul(matmul(q,diagonal),transpose(q))),
            ('rotated_repeated',matmul(matmul(q,repeated),transpose(q)))]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output',required=True)
    parser.add_argument('--inputs',help='Optional frozen Hessian-center specification')
    args = parser.parse_args()
    start = time.monotonic()
    output = {'scope':'Frozen exact centers; full six-coordinate probability jets only. '
                       'This is not a concavity or spectral-domain covering certificate.',
              'python':platform.python_version(), 'coordinates':['11','22','33','12','13','23'],
              'hessian_upper_order':PAIRS, 'cases':[]}
    assert matmul(transpose(U),U) == diag([1,1,1])
    for name,a in frozen_inputs(args.inputs):
        left,right = inclusion_events(a),formula_events(a)
        assert all(x.values()==y.values() for x,y in zip(left,right))
        assert sum(left).values()==Jet(1).values()
        trace = sum(input_jets(a)[i][i] for i in range(3))
        assert sum(mask.bit_count()*p for mask,p in enumerate(left)).values()==trace.values()
        assert all((p.c>0 if mask.bit_count()<=3 else p.values()==Jet().values())
                   for mask,p in enumerate(left))
        pmin = min(p.c for p in left if p.c>0)
        output['cases'].append({'name':name,'A':[[str(x) for x in row] for row in a],
                                'all_jets_equal':True,'positive_events':26,'zero_events':6,
                                'min_positive_probability':str(pmin),
                                'events':[{'mask':mask,**p.serial()} for mask,p in enumerate(left)]})
        print(name, 'ALL 32 EVENT JETS EXACTLY MATCH; min p =',pmin,flush=True)
    output['elapsed_seconds'] = time.monotonic()-start
    Path(args.output).write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print('ALL INDEPENDENT EVENT CHECKS PASSED',flush=True)


if __name__=='__main__':
    main()
