#!/usr/bin/env python3
"""I05 fixed-input author check. No scan, independent review, or family certificate.
Adapted event interface from agent24/code/verify_rank1_midpoint.py at main
65e59a46b49cd2dbb5c779a4cfae8cef26441984. Python 3 + SymPy; exact integers
and rationals decide every sign. Run: python verify.py [certificate.json]
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import json
import platform
import sys
import time
import sympy as s

Q = s.Rational
SCALE = 1 << 192
TERMS = 80

def fq(x):
    if isinstance(x, F):
        return x
    x = Q(x)
    return F(int(x.p), int(x.q))

def ceildiv(a, b):
    return -((-a) // b)

def add(a, b):
    return a[0] + b[0], a[1] + b[1]

def mul(c, a):
    c = fq(c)
    return (c*a[0], c*a[1]) if c >= 0 else (c*a[1], c*a[0])

def sub(a, b):
    return add(a, mul(-1, b))

def atanh_log(z):
    """Enclose 2*atanh(z) for rational 0<=z<=1/3 by dyadic arithmetic."""
    assert 0 <= z <= F(1, 3)
    lo = z.numerator*SCALE//z.denominator
    hi = ceildiv(z.numerator*SCALE, z.denominator)
    z2lo, z2hi = lo*lo//SCALE, ceildiv(hi*hi, SCALE)
    powerlo, powerhi = lo, hi
    total_lo = total_hi = 0
    for k in range(TERMS):
        total_lo += 2*powerlo//(2*k+1)
        total_hi += ceildiv(2*powerhi, 2*k+1)
        powerlo = powerlo*z2lo//SCALE
        powerhi = ceildiv(powerhi*z2hi, SCALE)
    # True tail <= (9/4)*3^(-(2N+1))/(2N+1).
    total_hi += ceildiv(9*SCALE, 4*(2*TERMS+1)*3**(2*TERMS+1))
    return F(total_lo, SCALE), F(total_hi, SCALE)

LOG2 = atanh_log(F(1, 3))

@lru_cache(maxsize=None)
def log_bounds(x):
    x = fq(x)
    if x <= 0:
        raise ValueError('log needs a positive exact rational')
    m, k = x, 0
    while m < 1:
        m *= 2
        k -= 1
    while m >= 2:
        m /= 2
        k += 1
    return add(mul(k, LOG2), atanh_log((m-1)/(m+1)))

def entropy(p):
    ans = F(0), F(0)
    assert all(x >= 0 for x in p.values()) and sum(p.values()) == 1
    for x in p.values():
        if x != 0:
            ans = add(ans, mul(-fq(x), log_bounds(fq(x))))
    return ans

def decimal_integer(a, digits=36):
    sign = '-' if a < 0 else ''
    a = abs(a)
    whole, frac = divmod(a, 10**digits)
    return f'{sign}{whole}.{frac:0{digits}d}'

def bounds(a):
    assert a[0] <= a[1] and a[1]-a[0] < F(1, 10**45)
    den = 10**36
    return [decimal_integer(a[0].numerator*den//a[0].denominator),
            decimal_integer(ceildiv(a[1].numerator*den, a[1].denominator))]

def subsets(n):
    return [tuple(i for i in range(n) if mask >> i & 1) for mask in range(1 << n)]

def inclusions(K):
    return {T: K.extract(T,T).det(method='domain-ge') if T else Q(1)
            for T in subsets(K.rows)}

def signed_law(K):
    out = {}
    for T in subsets(K.rows):
        D = K.copy()
        for i in range(K.rows):
            if i not in T:
                D[i,i] -= 1
        out[T] = (-1)**(K.rows-len(T))*D.det(method='domain-ge')
    return out

def law(K):
    inc = inclusions(K)
    out = {T: sum((-1)**(len(U)-len(T))*x for U,x in inc.items()
                  if set(T).issubset(U)) for T in inc}
    assert out == signed_law(K)
    assert all(x >= 0 for x in out.values()) and sum(out.values()) == 1
    return out

def gap(pa, pb, pm):
    return sub(entropy(pm), mul(F(1,2), add(entropy(pa), entropy(pb))))

def rotation(n, i, j, r):
    R = s.eye(n)
    co, si = (1-r*r)/(1+r*r), 2*r/(1+r*r)
    R[i,i] = R[j,j] = co
    R[i,j], R[j,i] = -si, si
    assert R.T*R == s.eye(n)
    return R

def atom_rows(p):
    return [{'S':[i+1 for i in T], 'p':str(x)} for T,x in p.items()]

def omega(n, eps):
    delta = 1-(1-eps)**n
    assert 0 < delta <= 1-F(1,2**n)
    out = add(mul(-delta, log_bounds(delta)),
              mul(-(1-delta), log_bounds(1-delta)))
    return add(out, mul(delta, log_bounds(F(2**n-1))))

def method_fixture():
    P = s.zeros(4)
    P[:3,:3] = s.eye(3)-s.ones(3)/3
    R = rotation(4,0,3,Q(1,1000))
    V = rotation(4,1,3,Q(1,1000))*rotation(4,0,2,Q(1,1000))
    A = Q(7,10)*R*P*R.T
    B = Q(9,10)*R*V*P*V.T*R.T
    M = (A+B)/2
    assert P*P == P and P.rank() == 2
    assert A.rank() == B.rank() == 2 and M.rank() == 4
    assert all(x != 0 for x in A) and all(x != 0 for x in B)
    # Projection construction certifies endpoint spectra; convexity certifies M<=0.9 I.
    pa, pb, pm = map(law, (A,B,M))
    mix = {T:(pa[T]+pb[T])/2 for T in pa}
    bridge = sub(entropy(mix), entropy(pm))
    delta = mul(-1, gap(pa,pb,pm))
    assert bridge[0] > 0 and delta[1] < 0
    # Full weighted rational Cauchy--Binet check, including triples/quadruple.
    u = s.Matrix([1,-1,0,0]); v = s.Matrix([1,1,-2,0])
    frame = R*s.Matrix.hstack(u,v,V*u,V*v)
    weights = [Q(7,40),Q(7,120),Q(9,40),Q(9,120)]
    ia, ib, im = map(inclusions,(A,B,M))
    for T in subsets(4):
        cb = sum(frame.extract(T,J).det()**2*s.prod(weights[j] for j in J)
                 for J in combinations(range(4),len(T))) if T else Q(1)
        assert s.factor(cb-im[T]) == 0
    corrections = {T:s.factor(im[T]-(ia[T]+ib[T])/2)
                   for T in ia if len(T)==2}
    assert any(x>0 for x in corrections.values()) and any(x<0 for x in corrections.values())
    for T,x in corrections.items():
        assert x == -(B-A).extract(T,T).det()/4
    eps = F(1,10**6)
    om = omega(4,eps)
    bridge_lift = sub(bridge,mul(2,om))
    delta_lift = add(delta,mul(2,om))
    assert bridge_lift[0] > 0 and delta_lift[1] < 0
    return {'ranks':[2,2,4], 'bridge_Hmix_minus_Hmid':bounds(bridge),
            'true_Delta':bounds(delta), 'epsilon':str(eps),
            'lift_bridge_lower_bound_enclosure':bounds(bridge_lift),
            'lift_Delta_upper_bound_enclosure':bounds(delta_lift),
            'midpoint_quadruple_atom':str(pm[(0,1,2,3)]),
            'pair_inclusion_corrections':[{'S':[i+1 for i in T],'value':str(x)}
                                         for T,x in corrections.items()],
            'atoms_minus':atom_rows(pa),'atoms_plus':atom_rows(pb),'atoms_mid':atom_rows(pm)}

def common_mode_fixture():
    u = s.Matrix([1,2,3,4,5,6])
    v = s.Matrix([1,-1,1,0,0,0]); w = s.Matrix([1,2,-1,0,0,0])
    c,a,b = Q(1,200),Q(1,12),Q(1,20)
    la,lb = a*v*v.T,b*w*w.T
    A,B = c*u*u.T+la,c*u*u.T+lb
    M = (A+B)/2
    assert s.trace(A)<1 and s.trace(B)<1
    assert A.rank()==B.rank()==2 and M.rank()==3
    r = Q(77,200)
    assert c*(u[3:,0].T*u[3:,0])[0] == r
    full, low, empty = [], [], []
    for L,K in ((la,A),(lb,B),((la+lb)/2,M)):
        p = law(K); lj = L[:3,:3]
        pl = law(lj); pe = law(c/(1-r)*u[:3,0]*u[:3,0].T+lj)
        for T in subsets(6):
            tj = tuple(i for i in T if i<3); te = tuple(i for i in T if i>=3)
            val = (1-r)*pe[tj] if not te else c*u[te[0]]**2*pl[tj] if len(te)==1 else 0
            assert p[T] == val
        full.append(p);low.append(pl);empty.append(pe)
    g = gap(*full); gl = gap(*low); ge = gap(*empty)
    lower = mul(r,gl)
    # Identity checked exactly at the atom level above, not by decimal entropy equality.
    assert g[0]>0 and gl[0]>0 and ge[0]>=0
    eps = F(1,10**5)
    lift = sub(lower,mul(2,omega(6,eps)))
    assert lift[0]>0
    return {'ranks':[2,2,3],'r':str(r),'G':bounds(g),
            'r_times_rank1_G':bounds(lower),'empty_branch_G':bounds(ge),
            'epsilon':str(eps),'lift_G_lower_bound_enclosure':bounds(lift),
            'atoms_minus':atom_rows(full[0]),'atoms_plus':atom_rows(full[1]),
            'atoms_mid':atom_rows(full[2]),
            'D_diagonal':[str(x) for x in (B-A).diagonal()],
            'all_epsilon_G_lower_bound':'49*(1-2*epsilon)^2/7200'}

def multiring_fixture():
    n = s.Matrix([1,2,2])/3
    P = s.eye(3)-n*n.T
    A = s.eye(3)/5+Q(3,5)*n*n.T
    C = s.eye(3)-A
    B = Q(2,5)*P
    t = s.symbols('t')
    K = A.row_join(t*B).col_join((t*B).row_join(C))
    V = s.Matrix([[2,2],[-1,0],[0,-1]])
    U = Q(2,5)*V*(V.T*V).inv()
    assert U*V.T==B and B.rank()==2
    pa,pc = law(A),law(C)
    poly = {}
    for S in subsets(3):
        X = A-s.diag(*[0 if i in S else 1 for i in range(3)])
        GA = U.T*X.inv()*U
        for T in subsets(3):
            Y = C-s.diag(*[0 if i in T else 1 for i in range(3)])
            GC = V.T*Y.inv()*V
            E = S+tuple(3+i for i in T)
            poly[E] = s.expand(pa[S]*pc[T]*(1-t*t*s.trace(GA*GC)+t**4*GA.det()*GC.det()))
    assert s.expand(sum(poly.values()))==1
    assert s.expand(sum(s.diff(p,t) for p in poly.values()))==0
    assert s.expand(sum(s.diff(p,t,2) for p in poly.values()))==0
    for x in [Q(0),Q(1,2),Q(3,4),Q(9,10),Q(1)]:
        direct = law(K.subs(t,x))
        assert all(p.subs(t,x)==direct[T] for T,p in poly.items())
    beta=Q(0); layers={}
    for T,p in poly.items():
        if p.subs(t,1)==0:
            order=next(j for j in range(1,5) if s.diff(p,t,j).subs(t,1)!=0)
            slope=-s.diff(p,t).subs(t,1)
            assert slope>=0
            beta += slope
            key=f'cardinality={len(T)},order={order}'
            count,weight=layers.get(key,(0,Q(0)))
            layers[key]=(count+1,weight+slope)
    assert beta==Q(6784,16875)
    probes=[]
    for x in [Q(1,2),Q(3,4),Q(9,10)]:
        fisher=Q(0); acceleration=(F(0),F(0))
        for p in poly.values():
            q=p.subs(t,x); d=s.diff(p,t).subs(t,x); dd=s.diff(p,t,2).subs(t,x)
            assert q>0
            fisher += d*d/q
            acceleration=add(acceleration,mul(-dd,log_bounds(fq(q))))
        curvature=sub(acceleration,(fq(fisher),fq(fisher)))
        assert curvature[1]<0
        # Exact three-kernel local Jensen test at t+-1/100, not a frame curve.
        step=Q(1,100)
        left={T:p.subs(t,x-step) for T,p in poly.items()}
        right={T:p.subs(t,x+step) for T,p in poly.items()}
        center={T:p.subs(t,x) for T,p in poly.items()}
        delta=mul(-1,gap(left,right,center))
        assert delta[1]<0
        probes.append({'t':str(x),'Fisher_exact':str(fisher),
                       'acceleration':bounds(acceleration),'H_second':bounds(curvature),
                       'local_Delta_step_1_over_100':bounds(delta)})
    S=(1,)
    MS=B*(A-s.diag(1,0,1)).inv()*B
    tr=s.trace(MS); e2=s.factor((tr*tr-s.trace(MS*MS))/2)
    ratios=[s.cancel(C[i,j]/MS[i,j]) for i,j in combinations(range(3),2)]
    assert MS.rank()==2 and tr<0 and e2>0 and len(set(ratios))>1
    return {'beta':str(beta),'count_layer_lower_bound':'128/625',
            'zero_layers':{k:{'count':v[0],'linear_mass':str(v[1])} for k,v in layers.items()},
            'conditional_obstruction_S':[2], 'conditional_M':[[str(x) for x in row] for row in MS.tolist()],
            'conditional_trace':str(tr),'conditional_e2':str(e2),
            'offdiagonal_anchor_ratios':[str(x) for x in ratios],
            'probes':probes,
            'atom_polynomials':[{'S':[i+1 for i in T],
                                 'coefficients_t_0_2_4':[str(p.coeff(t,j)) for j in [0,2,4]]}
                                for T,p in sorted(poly.items(),key=lambda z:sum(1<<i for i in z[0]))]}

def main():
    begin=time.perf_counter()
    out={'status':'AUTHOR_RATIONAL_CERTIFICATES; PENDING_REVIEW',
         'python':platform.python_version(),'sympy':s.__version__,
         'log_scale_bits':192,'atanh_terms':80,'display_digits_outward':36,
         'method':method_fixture(),'common_mode':common_mode_fixture(),
         'multiring':multiring_fixture()}
    out['author_runtime_seconds']=round(time.perf_counter()-begin,3)
    text=json.dumps(out,ensure_ascii=False,indent=2)
    target=Path(sys.argv[1]) if len(sys.argv)>1 else Path('certificate.json')
    target.write_text(text+'\n',encoding='utf-8')
    print('PASS:',target,'runtime',out['author_runtime_seconds'],'seconds')
    for key in ['method','common_mode']:
        print(key,{k:v for k,v in out[key].items() if not k.startswith('atoms') and k!='pair_inclusion_corrections'})
    print('multiring beta',out['multiring']['beta'])
    for p in out['multiring']['probes']:
        print({k:v for k,v in p.items() if k!='Fisher_exact'})

if __name__=='__main__':
    main()
