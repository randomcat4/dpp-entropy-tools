"""Exact finite checks supporting the radial-slice proof; not its proof."""
import itertools
import json
import os
import platform
import sys
import time
from pathlib import Path
import sympy as sp


def minor(K, mask):
    ids = [i for i in range(K.rows) if mask & (1 << i)]
    return K.extract(ids, ids).det() if ids else sp.Integer(1)


def events(K):
    n = K.rows
    return [sp.factor(sum((-1) ** ((T ^ S).bit_count()) * minor(K, T)
                         for T in range(1 << n) if T & S == S))
            for S in range(1 << n)]


def run(out):
    start = time.time()
    a, d, x, c, s, v, w, t, r = sp.symbols('a d x c s v w t r', real=True)
    A = sp.Matrix([[a, x], [x, d]])
    z = sp.Matrix([v, w])
    W = z*z.T
    K = A.row_join(s*z).col_join(sp.Matrix([[s*v, s*w, c]]))
    C1 = A-s*s*W/c
    C0 = A+s*s*W/(1-c)
    p = events(K)
    q0, q1 = events(C0), events(C1)
    checks = []
    for mask in range(4):
        checks.append(sp.cancel(p[mask]-(1-c)*q0[mask]) == 0)
        checks.append(sp.cancel(p[mask+4]-c*q1[mask]) == 0)
    checks.append(sp.factor(sum(p)-1) == 0)
    assert all(checks)
    b0,b1,b2=sp.symbols('b0 b1 b2', real=True)
    B=sp.Matrix([[b0,b1],[b1,b2]])
    accel1=(A+t*B-(s+t*r)**2*W/c).diff(t,2)
    accel0=(A+t*B+(s+t*r)**2*W/(1-c)).diff(t,2)
    assert sp.simplify(accel1+2*r*r*W/c)==sp.zeros(2)
    assert sp.simplify(accel0-2*r*r*W/(1-c))==sp.zeros(2)
    rankone_events=events(A+t*W)
    assert all(sp.diff(q,t,2)==0 for q in rankone_events)
    sample={a:sp.Rational(2,5),d:sp.Rational(3,5),x:sp.Rational(1,15),
            c:sp.Rational(1,2),s:sp.Integer(1),v:sp.Rational(1,7),w:sp.Rational(1,9)}
    K0=K.subs(sample)
    D=sp.Matrix([[sp.Rational(1,20),sp.Rational(1,30),sp.Rational(1,70)],
                 [sp.Rational(1,30),-sp.Rational(1,25),sp.Rational(1,90)],
                 [sp.Rational(1,70),sp.Rational(1,90),0]])
    kernels=[K0-D,K0,K0+D]
    exact=[]
    ent=[]
    for M in kernels:
        minors=[[minor(N,(1<<i)-1) for i in range(1,4)] for N in [M,sp.eye(3)-M]]
        assert all(q>0 for row in minors for q in row)
        ev=events(M)
        assert all(q>0 for q in ev) and sum(ev)==1
        assert all(M[i,j]!=0 for i,j in [(0,1),(0,2),(1,2)])
        exact.append({'K':[[str(q) for q in row] for row in M.tolist()],
                      'sylvester_K_IminusK':[[str(q) for q in row] for row in minors],
                      'events':[str(q) for q in ev]})
        ent.append(-sum(q*sp.log(q) for q in ev))
    result={'status':'EXACT_CHECKS_PASSED','symbolic_event_identities':8,
            'normalization_identities':1,'acceleration_matrix_identities':2,
            'rankone_affine_event_identities':4,'exact_chord_kernel_count':3,
            'samples':exact,'gap_80digit_diagnostic':str(sp.N((ent[0]+ent[2])/2-ent[1],80)),
            'gap_diagnostic_is_certificate':False,'seed':None,'random_trials':0,
            'pid':os.getpid(),'python':platform.python_version(),'sympy':sp.__version__,
            'elapsed_seconds':time.time()-start,'exit_code':0}
    Path(out).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='samples'},indent=2))


if __name__ == '__main__':
    run(sys.argv[1])
