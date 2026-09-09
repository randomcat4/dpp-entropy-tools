#!/usr/bin/env python3
"""Exact, small author checks for the W2 nonconstant-centre proof.

Run from any directory: python code/audit_new.py
Inputs are in ../inputs/new.json; output is ../output/new_audit.json.
No network, server, sampling, entropy-rate extrapolation, or independent review.
All checks use exact SymPy rationals (including Gaussian rationals).
"""
from __future__ import annotations
import json
from pathlib import Path
import platform
import time
import sympy as s

ROOT = Path(__file__).resolve().parents[1]
R = s.Rational

def indices(mask: int, n: int) -> list[int]:
    return [i for i in range(n) if mask >> i & 1]

def minors(K: s.Matrix) -> list[s.Expr]:
    n = K.rows
    return [s.S.One if m == 0 else s.factor(K.extract(indices(m, n), indices(m, n)).det())
            for m in range(1 << n)]

def law(K: s.Matrix) -> list[s.Expr]:
    """Inclusion-exclusion, not principal minors mistaken for exact events."""
    n = K.rows
    p = minors(K)
    for i in range(n):
        for m in range(1 << n):
            if not (m >> i & 1):
                p[m] = s.factor(p[m] - p[m | (1 << i)])
    return p

def kernel(spec: dict, t: s.Expr) -> s.Matrix:
    n = int(spec['window'])
    mu = R(spec['mean'])
    a2 = R(spec['c_cos_2']) / 2
    # Convention: fhat(k) = integral f(theta) exp(+2*pi*i*k*theta).
    b1 = (R(spec['g_cos_1']) + s.I * R(spec['g_sin_1'])) / 2
    def entry(i: int, j: int) -> s.Expr:
        d = i-j
        if d == 0: return mu
        if abs(d) == 2: return a2
        if d == 1: return t*b1
        if d == -1: return t*s.conjugate(b1)
        return s.S.Zero
    return s.Matrix(n, n, entry)

def serial(vals):
    if isinstance(vals, dict): return {k: serial(v) for k, v in vals.items()}
    if isinstance(vals, (list, tuple)): return [serial(v) for v in vals]
    if isinstance(vals, s.Basic): return str(s.factor(vals))
    return vals

def audit_example(spec: dict) -> dict:
    n = int(spec['window']); k = int(spec['k'])
    K = kernel(spec, R(1,2)); p = law(K)
    assert K == K.conjugate().T
    assert sum(p) == 1 and all(v > 0 for v in p)
    B = 2*K-s.eye(n)
    bm = minors(B)
    for mask in range(1 << n):
        sig = [1 if mask >> i & 1 else -1 for i in range(n)]
        exact = s.factor((s.eye(n)+s.diag(*sig)*B).det()/2**n)
        assert exact == p[mask]
    for subset in range(1 << n):
        moment = sum(p[m]*(-1)**((subset & ((1 << n)-1-m)).bit_count())
                     for m in range(1 << n))
        assert s.factor(moment-bm[subset]) == 0
    assert law(kernel(spec, -R(1,2))) == p
    p0, p1, p2 = [law(kernel(spec, R(t))) for t in (0,1,2)]
    u4 = [s.factor((z-4*y+3*x)/12) for x,y,z in zip(p0,p1,p2)]
    u2 = [s.factor(y-x-v) for x,y,v in zip(p0,p1,u4)]
    assert sum(u2) == 0 and sum(u4) == 0
    assert [s.factor(q+u/4+v/16) for q,u,v in zip(p0,u2,u4)] == p
    A4 = s.factor(sum(u*u/(2*q) for q,u in zip(p0,u2)))
    A6 = s.factor(sum(u*v/q-u**3/(6*q*q) for q,u,v in zip(p0,u2,u4)))
    A8 = s.factor(sum(v*v/(2*q)-u*u*v/(2*q*q)+u**4/(12*q**3)
                       for q,u,v in zip(p0,u2,u4)))
    gamma = s.factor((R(spec['g_cos_1'])**2+R(spec['g_sin_1'])**2)/4)
    lower = R(4,3)*(n-k)*gamma**2
    assert A4 >= lower
    aa, bb = R(spec['a']), R(spec['b_upper'])
    RR, rho, MM, TT = [R(spec[z]) for z in ('R','rho','M_upper','T')]
    assert RR == (1-aa)/(2*bb) and rho == aa+bb*RR
    assert 2*R(spec['c_cos_2']) <= aa
    # Squaring certifies the upper bound even for the non-even example.
    assert 16*gamma <= bb**2
    assert 2*TT <= RR
    residual = s.factor(8*gamma**2*RR**6 - 54*MM*TT**2)
    assert residual > 0
    return {'status': 'PASS_EXACT_AUTHOR_CHECK', 'n': n,
            'probabilities_t_half': p, 'probabilities_t_zero': p0,
            'polynomial_coefficient_t2': u2, 'polynomial_coefficient_t4': u4,
            'KL_coefficients': {'t4': A4, 't6': A6, 't8': A8},
            'gamma': gamma, 'quartic_lower_bound': lower,
            'parameter_inequality_residual': residual,
            'rate_quartic_correction': R(2,3)*gamma**2}

def audit_walks(spec: dict, conf: dict) -> dict:
    t = R(conf['parameter']); L = int(conf['max_length'])
    K = kernel(spec, t); n = K.rows; B = 2*K-s.eye(n)
    p, bm = law(K), minors(B)
    adj = [[j for j in range(n) if B[i,j] != 0] for i in range(n)]
    sigmats = [s.diag(*[1 if m >> i & 1 else -1 for i in range(n)])*B
               for m in range(1 << n)]
    powers = [s.eye(n) for _ in sigmats]
    rows = []; partial = s.S.Zero
    for ell in range(1, L+1):
        powers = [X*Y for X,Y in zip(powers, sigmats)]
        lhs = s.factor(sum(q*X.trace() for q,X in zip(p,powers)))
        total = s.S.Zero; count = 0
        def walk(root, current, left, mask, weight):
            nonlocal total, count
            if left == 0:
                if current == root:
                    total += weight*bm[mask]; count += 1
                return
            for j in adj[current]:
                walk(root, j, left-1, mask ^ (1 << current), weight*B[current,j])
        for root in range(n): walk(root, root, ell, 0, s.S.One)
        rhs = s.factor(total)
        assert rhs == lhs
        partial += R((-1)**(ell+1), ell)*rhs
        rows.append({'length': ell, 'nonzero_closed_walks': count, 'expected_trace': lhs})
    rho = max(sum(abs(B[i,j]) for j in range(n)) for i in range(n))
    assert 0 < rho < 1
    tail = s.factor(n*rho**(L+1)/((L+1)*(1-rho)))
    return {'status': 'PASS_EXACT_AUTHOR_CHECK', 'terms': rows,
            'F_partial': s.factor(partial), 'absolute_tail_bound_from_proof': tail,
            'actual_row_norm': rho,
            'scope': 'Exact identity checks; tail is the theorem bound, not an independent entropy-rate enclosure.'}

def audit_channel(conf: dict) -> dict:
    d,w,eps,r = [R(conf[k]) for k in ('diagonal','within_block','epsilon','r')]
    A = s.Matrix([[d,w],[w,d]])
    def K(t): return A.row_join(t*eps*s.eye(2)).col_join((t*eps*s.eye(2)).row_join(A))
    assert all(x > 0 and x < 1 for x in K(1).eigenvals())
    p0,p1,pr = [s.factor(K(t).det()) for t in (0,1,r)]
    predicted = s.factor(p0+r*r*(p1-p0)); diff=s.factor(predicted-pr)
    assert diff == eps**4*r*r*(1-r*r) and diff > 0
    # Derivatives in three positive rank-one directions span the zero-mass space.
    mu = s.Matrix(law(A)); columns=[]
    delta=R(1,128)
    for v in (s.Matrix([1,0]), s.Matrix([0,1]), s.Matrix([1,1])):
        columns.append((s.Matrix(law(A+delta*v*v.T))-mu)/delta)
    rank=s.Matrix.hstack(*columns).rank()
    assert rank == 3
    # A fixed exact rank-one joint configuration factorization.
    v=s.Matrix([1,2]); ww=s.Matrix([1,-1]); ee=R(1,128)
    uv=(s.Matrix(law(A+delta*v*v.T))-mu)/delta
    vw=(s.Matrix(law(A+delta*ww*ww.T))-mu)/delta
    C=ee*v*ww.T
    joint=law(A.row_join(C).col_join(C.T.row_join(A)))
    for x in range(4):
        for y in range(4):
            assert s.factor(joint[x+4*y]-(mu[x]*mu[y]-ee**2*uv[x]*vw[y])) == 0
    return {'status': 'PASS_EXACT_AUTHOR_CHECK', 'eigenvalues_K1': list(K(1).eigenvals()),
            'derivative_span_rank': rank, 'all_occupied_actual': pr,
            'all_occupied_forced_by_local_channels': predicted, 'difference': diff,
            'rank_one_factorization': 'PASS',
            'scope': 'Failure of a universal local channel, not an entropy counterexample.'}

def main() -> None:
    started=time.monotonic()
    data=json.loads((ROOT/'inputs/new.json').read_text())
    x=s.symbols('x')
    series=s.factor((s.diff(1/(1-x*x),x,2)-2-12*x*x)/x**4)
    series_half=s.factor(series.subs(x,R(1,2)))
    assert series_half == R(1424,27) and series_half < 54
    # Exact elementary certificate used for M < 3/8.
    assert sum(R(1,s.factorial(j)) for j in range(5)) > R(8,3)
    out={'status':'PASS_EXACT_AUTHOR_CHECK_NOT_INDEPENDENT_REVIEW',
         'example':audit_example(data['example']),
         'non_even_example':audit_example(data['non_even_example']),
         'walks':audit_walks(data['example'],data['closed_walk']),
         'channel':audit_channel(data['channel_obstruction']),
         'tail_series_at_half':series_half,
         'versions':{'python':platform.python_version(),'sympy':s.__version__},
         'seconds':round(time.monotonic()-started,3)}
    path=ROOT/'output/new_audit.json'; path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(serial(out),ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'seconds':out['seconds'],'output':str(path)},indent=2))

if __name__ == '__main__':
    main()
