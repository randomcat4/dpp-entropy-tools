"""Bounded, deterministic exact checks. Standard library only; no search.

All event probabilities use direct Boolean Mobius inversion of principal minors.
Generated artifacts remain beside this script. Numerical logs are diagnostics only.
"""
import os
for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[key] = '1'
from fractions import Fraction as F
from decimal import Decimal, localcontext
from math import lcm
from pathlib import Path
import json
import platform
import time

HERE = Path(__file__).resolve().parent
OUT = HERE / 'results'

def det_int(matrix):
    a = [row[:] for row in matrix]
    n = len(a)
    if not n:
        return 1
    last, sign = 1, 1
    for k in range(n-1):
        pivot = next((j for j in range(k, n) if a[j][k]), None)
        if pivot is None:
            return 0
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            sign = -sign
        v = a[k][k]
        for i in range(k+1, n):
            for j in range(k+1, n):
                numerator = a[i][j]*v-a[i][k]*a[k][j]
                assert numerator % last == 0
                a[i][j] = numerator // last
            a[i][k] = 0
        last = v
    return sign*a[-1][-1]

def det(a):
    den = lcm(*(x.denominator for row in a for x in row)) if a else 1
    return F(det_int([[int(x*den) for x in row] for row in a]), den**len(a))

def mobius(a):
    n = len(a)
    den = lcm(*(x.denominator for row in a for x in row))
    z = [[int(x*den) for x in row] for row in a]
    p = []
    for s in range(1 << n):
        ids = [i for i in range(n) if s >> i & 1]
        p.append(F(det_int([[z[i][j] for j in ids] for i in ids]), den**len(ids)))
    for bit in range(n):
        for s in range(1 << n):
            if not (s >> bit & 1):
                p[s] -= p[s | (1 << bit)]
    assert sum(p) == 1 and min(p) > 0
    return p

def solve(a, rhs):
    a = [row[:] + [b] for row, b in zip(a, rhs)]
    n = len(a)
    for k in range(n):
        j = next(j for j in range(k, n) if a[j][k])
        a[k], a[j] = a[j], a[k]
        v = a[k][k]
        a[k] = [x/v for x in a[k]]
        for j in range(n):
            if j != k:
                v = a[j][k]
                a[j] = [x-v*y for x, y in zip(a[j], a[k])]
    return [row[-1] for row in a]

def construct(n):
    m = n-2
    M = [[F(0) for _ in range(n)] for _ in range(n)]
    M[0][0] = M[1][1] = F(1,2)
    M[0][1] = M[1][0] = F(1,8)
    for j in range(m):
        y = F((-1)**j*(j+1), 200*m)
        M[0][j+2] = M[j+2][0] = M[1][j+2] = M[j+2][1] = y
        M[j+2][j+2] = F(1,3) + F(j+1, 3*(m+1))
        if j:
            M[j+1][j+2] = M[j+2][j+1] = F(1,100*m)
    D = [[F(0) for _ in range(n)] for _ in range(n)]
    D[0][0] = D[1][1] = F(1,5)
    D[0][1] = D[1][0] = F(1,10)
    return M, D

def add(M, D, t):
    return [[x+t*y for x, y in zip(r, s)] for r, s in zip(M, D)]

def margin(K):
    return min(min(row[i], 1-row[i])-sum(abs(x) for j,x in enumerate(row) if j != i)
               for i, row in enumerate(K))

def dec(x):
    return Decimal(x.numerator)/Decimal(x.denominator)

def entropy(p):
    return -sum(dec(x)*dec(x).ln() for x in p)

def conditional_check(K, p):
    n = len(K)
    B = [r[2:] for r in K[2:]]
    y = K[0][2:]
    weights = mobius(B)
    checked = 0
    for t in range(1 << (n-2)):
        Bt = [r[:] for r in B]
        for j in range(n-2):
            if not (t >> j & 1):
                Bt[j][j] -= 1
        sol = solve(Bt, y)
        eta = -sum(x*z for x, z in zip(y, sol))
        C = [[K[i][j]+eta for j in range(2)] for i in range(2)]
        assert C[0][0] == C[1][1]
        assert C[0][0] > 0 and det(C) > 0
        assert 1-C[0][0] > 0 and det([[1-C[0][0],-C[0][1]],[-C[1][0],1-C[1][1]]]) > 0
        cp = mobius(C)
        for s in range(4):
            assert cp[s]*weights[t] == p[s | (t << 2)]
            checked += 1
    return checked

def main():
    started = time.time()
    OUT.mkdir(exist_ok=True)
    records = []
    denominator = {'families':2,'centers':2,'directions':2,'rank_two_psd':2,
                   'kernel_points':6,'finite_chords':2,'random_draws':0,
                   'failed_assertions':0,'positive_gap_candidates':0}
    with localcontext() as ctx, (OUT/'exact_events.jsonl').open('w', encoding='utf-8') as events:
        ctx.prec = 70
        for n in (4, 11):
            M, D = construct(n)
            ts = (F(-1,2), F(0), F(1,2))
            probs = []
            for t in ts:
                K = add(M,D,t)
                g = margin(K)
                assert g > 0
                p = mobius(K)
                probs.append(p)
                # Independent signed full determinant check at every exact event.
                for s, value in enumerate(p):
                    Q = [r[:] for r in K]
                    for i in range(n):
                        if not (s >> i & 1):
                            Q[i][i] -= 1
                    assert value == (-1)**(n-s.bit_count())*det(Q)
                    events.write(json.dumps({'n':n,'t':str(t),'mask':s,'probability':str(value)})+'\n')
                records.append({'n':n,'t':str(t),'rank_D':2,'gershgorin_margin':str(g),
                                'min_probability':str(min(p)),'events':len(p),'entropy_decimal':str(entropy(p))})
            count = conditional_check(M,probs[1])
            h = F(1,2)
            pminus,p0,pplus = probs
            aa = [(v-u)/(2*h) for u,v in zip(pminus,pplus)]
            bb = [(u+v-2*w)/(2*h*h) for u,v,w in zip(pminus,pplus,p0)]
            assert sum(aa) == sum(bb) == 0
            hessian = -sum(dec(a*a/p)+2*dec(b)*dec(p).ln() for p,a,b in zip(p0,aa,bb))
            bound = -Decimal(3)/25*Decimal(2).ln()
            gap = (entropy(pminus)+entropy(pplus))/2-entropy(p0)
            assert hessian < bound and gap < 0
            records.append({'n':n,'conditional_event_identities':count,
                            'M':[[str(x) for x in row] for row in M],
                            'D':[[str(x) for x in row] for row in D],
                            'nonzero_rest_coupling':True,'non_thinning_rank_obstruction':True,
                            'hessian_decimal':str(hessian),'proved_upper_bound_decimal':str(bound),
                            'gap_decimal':str(gap),'sign_status':'NEGATIVE_DIAGNOSTIC'})
        # Exact mixed-Hessian shortcut counterexample; p_s p_t / p is rational.
        p = [F(5,36),F(5,36),F(13,36),F(13,36)]
        ds = [F(-5,6),F(1,6),F(1,3),F(1,3)]
        dt = [F(-1,6),F(5,6),F(-1,3),F(-1,3)]
        rational_fisher = -sum(a*b/c for a,b,c in zip(ds,dt,p))
        assert rational_fisher == -F(18,13)
        lower = 2*F(8,9)-F(18,13)
        assert lower == F(46,117) and lower > 0
        records.append({'shortcut':'PSD_rank_one_cross_Hessian_nonpositive',
                        'status':'EXACT_COUNTEREXAMPLE_NOT_MAIN_CLAIM',
                        'mixed_value':'2 log(13/5)-18/13', 'strict_rational_lower_bound':str(lower)})
    report = {'status':'SANITY_PASS_NOT_INDEPENDENT_REVIEW', 'python':platform.python_version(),
              'seed':None,'exit_code':0,'elapsed_seconds':time.time()-started,
              'denominator':denominator,'records':records}
    (OUT/'sanity.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps({'status':report['status'],'elapsed_seconds':report['elapsed_seconds'],
                      'denominator':denominator}))

if __name__ == '__main__':
    main()
