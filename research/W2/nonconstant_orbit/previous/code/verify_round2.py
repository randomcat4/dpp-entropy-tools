#!/usr/bin/env python3
"""Exact finite audit for I05-W2 round 2. Not an independent mathematical review.

All probabilities and polynomial jets are rational (Gaussian rationals in K).
Log intervals use an explicit atanh-series tail, evaluated with Fraction only.
No numerical optimization, Fourier scan, or floating-point sign decision is used.
Run from the package root: python code/verify_round2.py
"""
from __future__ import annotations
import json
import sys
import platform
import hashlib
from dataclasses import dataclass
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'inputs/exact_inputs.json').read_text())
NLOG = DATA['log_terms']
GRID = 10**60
EXACT_OBJECTS = {}

@dataclass(frozen=True)
class Interval:
    lo: F
    hi: F
    def __post_init__(self):
        # Certified fixed-grid outward rounding prevents denominator explosion.
        # All operations before rounding are still exact integer/rational arithmetic.
        lo,hi=F(self.lo),F(self.hi)
        l=(lo.numerator*GRID)//lo.denominator
        u=-((-hi.numerator*GRID)//hi.denominator)
        object.__setattr__(self, 'lo', F(l,GRID))
        object.__setattr__(self, 'hi', F(u,GRID))
    def __add__(self, other):
        if not isinstance(other, Interval): other = Interval(F(other), F(other))
        return Interval(self.lo + other.lo, self.hi + other.hi)
    __radd__ = __add__
    def __neg__(self): return Interval(-self.hi, -self.lo)
    def __sub__(self, other): return self + (-other if isinstance(other, Interval) else -F(other))
    def __mul__(self, c):
        c = F(c)
        return Interval(self.lo*c, self.hi*c) if c >= 0 else Interval(self.hi*c, self.lo*c)
    __rmul__ = __mul__
    def __truediv__(self, c): return self * (1/F(c))
    def contains_zero(self): return self.lo <= 0 <= self.hi
    def out(self, digits=22):
        # Exact outward rounding to decimal strings; float is never used.
        scale = 10**digits
        l = (self.lo.numerator*scale)//self.lo.denominator
        u = -((-self.hi.numerator*scale)//self.hi.denominator)
        def fmt(v):
            sign = '-' if v < 0 else ''
            z = str(abs(v)).rjust(digits+1, '0')
            return sign + z[:-digits] + '.' + z[-digits:]
        return [fmt(l), fmt(u)]

ZERO = Interval(F(0), F(0))

def log_1_to_2(x: F) -> Interval:
    assert 1 <= x <= 2
    z = (x-1)/(x+1)
    zz = z*z
    power = z
    total = F(0)
    for k in range(NLOG):
        total += 2*power/(2*k+1)
        power *= zz
    tail = 2*power/((2*NLOG+1)*(1-zz))
    return Interval(total, total+tail)

@lru_cache(maxsize=None)
def logq(x: F) -> Interval:
    x = F(x)
    if x <= 0: raise ValueError('log requires a positive rational')
    exponent = 0
    while x < 1:
        x *= 2; exponent -= 1
    while x >= 2:
        x /= 2; exponent += 1
    return log_1_to_2(x) + exponent*log_1_to_2(F(2))

def entropy(p):
    assert all(x >= 0 for x in p) and sum(p) == 1
    return sum((-x*logq(x) for x in p if x), ZERO)

def kl(p, q):
    assert all(a == 0 or b > 0 for a,b in zip(p,q))
    return sum((a*logq(a/b) for a,b in zip(p,q) if a), ZERO)

def binary_kl(r, a): return kl([r,1-r], [a,1-a])

def E(p, i, refs):
    b = 1 << i
    a = refs[i]
    return [(a if x&b else 1-a)*(p[x&~b]+p[x|b]) for x in range(len(p))]

def G(p,i,refs): return [x-y for x,y in zip(p,E(p,i,refs))]

def channel(p,s,refs):
    p=list(p)
    for i in range(len(refs)):
        ep=E(p,i,refs)
        p=[s*x+(1-s)*y for x,y in zip(p,ep)]
    return p

def jets(p,s,refs):
    v=channel(p,s,refs)
    n=len(refs)
    d=[F(0)]*len(p); dd=[F(0)]*len(p)
    for i in range(n):
        gi=G(v,i,refs)
        d=[x+y/s for x,y in zip(d,gi)]
        for j in range(n):
            if j != i:
                gij=G(gi,j,refs)
                dd=[x+y/(s*s) for x,y in zip(dd,gij)]
    assert sum(v)==1 and sum(d)==sum(dd)==0
    return v,d,dd

def dissipation(p,q,j,refs):
    total=ZERO
    bit=1<<j
    # Directed off-diagonal refresh transitions x -> y=x xor bit.
    for x in range(len(p)):
        y=x^bit
        rate=refs[j] if y&bit else 1-refs[j]
        u=p[x]/q[x]; v=p[y]/q[y]
        if u == v: continue
        b=u*logq(u/v)-u+v
        total += rate*q[x]*b
    return total

def audit_curvature(initial,s,refs):
    p,d,dd=jets(initial,s,refs)
    assert min(p)>0
    direct=Interval(-sum(x*x/y for x,y in zip(d,p)), -sum(x*x/y for x,y in zip(d,p)))
    direct -= sum((x*logq(y) for x,y in zip(dd,p)), ZERO)
    own=F(0); cross=ZERO
    for i in range(len(refs)):
        q=E(p,i,refs)
        own += sum((x-y)**2/x for x,y in zip(p,q))
        for j in range(len(refs)):
            if i != j:
                term=dissipation(p,q,j,refs)+dissipation(q,p,j,refs)
                assert term.lo>=0, ('nonnegative term not certified',i,j,term.out())
                cross += term
    decomposed=-(own+cross)/(s*s)
    residual=direct-decomposed
    assert residual.contains_zero()
    assert residual.hi-residual.lo < F(1,10**26)
    assert direct.hi < 0
    return {'retention':str(s), 'direct_H_second':direct.out(),
            'decomposition_H_second':decomposed.out(),
            'identity_residual':residual.out(30),
            'probability_jet':{'P':[str(x) for x in p], 'first':[str(x) for x in d], 'second':[str(x) for x in dd]},
            'own_chi_square_sum':str(own),
            'cross_dissipation_sum':cross.out()}, direct

def sf(q):
    q=F(q); return sp.Rational(q.numerator,q.denominator)

def ff(q):
    q=sp.simplify(q)
    assert q.is_Rational, repr(q)
    return F(int(q.p),int(q.q))

def symbol_coeffs(item):
    p=F(item['mean'])
    cs={int(k):sf(F(a))+sp.I*sf(F(b)) for k,(a,b) in item['positive_fourier'].items()}
    return p,cs

def matrix_for(item,n):
    p,cs=symbol_coeffs(item)
    def coef(k):
        if k==0:return sf(p)
        return cs.get(k,0) if k>0 else sp.conjugate(cs.get(-k,0))
    return sp.Matrix(n,n,lambda i,j:coef(i-j))

def exact_law(K, check_rows=False):
    n=K.rows
    inc=[]
    for mask in range(1<<n):
        ix=[i for i in range(n) if mask>>i&1]
        inc.append(ff(K.extract(ix,ix).det(method='domain-ge')) if ix else F(1))
    p=inc.copy()
    for i in range(n):
        for mask in range(1<<n):
            if not mask>>i&1:p[mask]-=p[mask|(1<<i)]
    assert all(a>=0 for a in p) and sum(p)==1
    if check_rows:
        for mask in range(1<<n):
            R=sp.Matrix(n,n,lambda i,j: K[i,j] if mask>>i&1 else (int(i==j)-K[i,j]))
            assert ff(R.det(method='domain-ge'))==p[mask]
    matrix=[[str(K[i,j]) for j in range(n)] for i in range(n)]
    key=hashlib.sha256(json.dumps(matrix).encode()).hexdigest()
    prev=EXACT_OBJECTS.get(key,{})
    EXACT_OBJECTS[key]={'n':n,'matrix':matrix,
      'event_probabilities_mask_order':[str(x) for x in p],
      'bit_order':'coordinate i is bit 2**i',
      'independent_row_determinants_checked':check_rows or prev.get('independent_row_determinants_checked',False)}
    return p

def polynomial_jets(K, A, s):
    t=sp.Symbol('t')
    M=A+t*(K-A)
    n=K.rows
    pol=[]
    for mask in range(1<<n):
        ix=[i for i in range(n) if mask>>i&1]
        pol.append(sp.expand(M.extract(ix,ix).det(method='domain-ge')) if ix else sp.Integer(1))
    for i in range(n):
        for mask in range(1<<n):
            if not mask>>i&1:pol[mask]=sp.expand(pol[mask]-pol[mask|(1<<i)])
    return tuple([[ff(sp.diff(e,t,k).subs(t,sf(s))) for e in pol] for k in range(3)])

def match_pairs(n,k):
    ans=[]
    for r in range(min(k,n)):
        chain=list(range(r,n,k))
        ans.extend(zip(chain[::2],chain[1::2]))
    assert len({i for e in ans for i in e})==2*len(ans)
    return ans

def main():
    out={'task_id':DATA['task_id'], 'status':'PASS',
         'scope':'finite exact author self-check; not independent review or a general-conjecture proof',
         'python':platform.python_version(),'sympy':sp.__version__, 'log_series_terms':NLOG, 'interval_grid':'1e-60 (outward integer rounding)',
         'refresh':[], 'symbol_validity':{}, 'affine_diagonal':[], 'pinching':[], 'quartic':[]}
    for item in DATA['refresh_cases']:
        initial=[F(x,sum(item['weights'])) for x in item['weights']]
        refs=list(map(F,item['reference']))
        for s in map(F,item['retentions']):
            record,_=audit_curvature(initial,s,refs)
            out['refresh'].append({'case':item['name'],**record})
            print('checked refresh',item['name'],s,flush=True)
    for name,item in DATA['symbols'].items():
        p=F(item['mean'])
        radius=2*sum((abs(F(a))+abs(F(b)) for a,b in item['positive_fourier'].values()),F(0))
        assert p-radius>0 and p+radius<1
        out['symbol_validity'][name]={'lower_bound':str(p-radius),'upper_bound':str(p+radius),
          'method':'2 sum (abs(real Fourier)+abs(imag Fourier)); a conservative exact uniform bound'}
    print('checking affine diagonal',flush=True)
    cfg=DATA['affine_diagonal']
    K=matrix_for(DATA['symbols'][cfg['symbol']],cfg['window'])
    base=exact_law(K,True)
    refs=list(map(F,cfg['reference']))
    A=sp.diag(*map(sf,refs))
    assert K*A!=A*K
    out['noncommuting_diagonal_endpoint_verified']=True
    for s in map(F,cfg['retentions']):
        a=jets(base,s,refs)
        b=polynomial_jets(K,A,s)
        assert a==b
        assert a[0]==exact_law((1-sf(s))*A+sf(s)*K,True)
        rec,second=audit_curvature(base,s,refs)
        diagonal_bound=4*sum((ff(K[i,i])-refs[i])**2 for i in range(K.rows))
        assert (-second-diagonal_bound).lo>0
        rec['general_diagonal_quadratic_curvature_lower_bound']=str(diagonal_bound)
        out['affine_diagonal'].append({'all_probability_and_first_two_jet_equalities':'exact',**rec})
    brefs=list(map(F,cfg['boundary_reference']))
    BA=sp.diag(*map(sf,brefs)); z=F(1,2)
    bp=channel(base,z,brefs)
    assert bp==exact_law((1-sf(z))*BA+sf(z)*K,True)
    gap=entropy(bp)-(entropy(channel(base,F(0),brefs))+entropy(base))/2
    assert gap.lo>0
    boundary_barrier=sum((ff(K[i,i])-brefs[i])**2 for i in range(K.rows))/2
    assert (gap-boundary_barrier).lo>0
    out['boundary_diagonal']={'channel_identity':'exact','midpoint_entropy_gap':gap.out(),'quadratic_Jensen_lower_bound':str(boundary_barrier)}
    print('checking pinching',flush=True)
    cfg=DATA['pinching']; n=cfg['window']; k=cfg['lag']
    item=DATA['symbols'][cfg['symbol']]; p,cs=symbol_coeffs(item)
    K=matrix_for(item,n); pk=exact_law(K,True)
    ck2=ff(cs[k]*sp.conjugate(cs[k]))
    pairs=match_pairs(n,k)
    rate_lower=max(binary_kl(p*p-ck2,p*p).lo,
                   binary_kl((1-p)**2-ck2,(1-p)**2).lo)/2
    assert rate_lower>=ck2*ck2
    for q in cfg['moduli']:
        assert k%q
        Q=sp.Matrix(n,n,lambda i,j:K[i,j] if (i-j)%q==0 else 0)
        pq=exact_law(Q,True)
        diff=entropy(pq)-entropy(pk); div=kl(pk,pq)
        assert (diff-div).contains_zero()
        bound=len(pairs)*binary_kl(p*p-ck2,p*p)
        slack=diff-bound
        assert slack.lo>0
        out['pinching'].append({'q':q,'n':n,'lag':k,'matching':pairs,
            'entropy_loss':diff.out(),'KL':div.out(),
            'matching_KL_lower_bound':bound.out(),'certified_slack':slack.out(),
            'rate_lower_bound_display':Interval(rate_lower,rate_lower).out(),
            'fourier_fourth_power':str(ck2*ck2)})
    print('checking quartic',flush=True)
    cfg=DATA['quartic']; n=cfg['window']; k=cfg['lag']; item=DATA['symbols'][cfg['symbol']]
    p,cs=symbol_coeffs(item); K=matrix_for(item,n); initial=exact_law(K,True)
    refs=[p]*n; ck4=ff(cs[k]*sp.conjugate(cs[k]))**2
    for s in map(F,cfg['retentions']):
        rec,direct=audit_curvature(initial,s,refs)
        bound=16*(n-k)*s*s*ck4
        assert (-direct-bound).lo>0
        out['quartic'].append({**rec,'curvature_magnitude_lower_bound':str(bound),
                                'certified_slack':(-direct-bound).out()})
    r1,r2=map(F,cfg['chord']); lam=F(cfg['lambda']); r0=(1-lam)*r1+lam*r2
    def signed_law(r):return exact_law(sf(p)*sp.eye(n)+sf(r)*(K-sf(p)*sp.eye(n)))
    for r in [r1,r2,r0]:assert signed_law(r)==signed_law(-r)
    gap=entropy(signed_law(r0))-(1-lam)*entropy(signed_law(r1))-lam*entropy(signed_law(r2))
    barrier=F(4,3)*(n-k)*ck4*((1-lam)*r1**4+lam*r2**4-r0**4)
    assert barrier>0 and (gap-barrier).lo>0
    out['signed_half_translation_chord']={'n':n,'signed_parameters':[str(r1),str(r2)],
       'lambda':str(lam),'middle':str(r0),'law_symmetry':'exact for each tested parameter',
       'entropy_gap':gap.out(),'quartic_Jensen_lower_bound':str(barrier),
       'certified_slack':(gap-barrier).out()}
    cfg=DATA['extended_radial']; n=cfg['window']; k=cfg['lag']
    item=DATA['symbols'][cfg['symbol']]; p,cs=symbol_coeffs(item)
    K=matrix_for(item,n); initial=exact_law(K,True); refs=[p]*n
    ck4=ff(cs[k]*sp.conjugate(cs[k]))**2
    out['extended_radial']=[]
    radius=2*sum((abs(F(a))+abs(F(b)) for a,b in item['positive_fourier'].values()),F(0))
    for s in map(F,cfg['parameters']):
        assert p-abs(s)*radius>0 and p+abs(s)*radius<1
        # T_s is only a polynomial identity here, NOT a stochastic channel
        # for s outside [0,1]. The resulting law is positive by DPP validity.
        exact=exact_law(sf(p)*sp.eye(n)+sf(s)*(K-sf(p)*sp.eye(n)),True)
        assert exact==channel(initial,s,refs)
        rec,second=audit_curvature(initial,s,refs)
        lower=16*(n-k)*s*s*ck4
        assert (-second-lower).lo>0
        out['extended_radial'].append({**rec,'K_affine_polynomial_identity':'exact',
            'curvature_lower_bound':str(lower),'slack':(-second-lower).out(),
            'uniform_symbol_bounds':[str(p-abs(s)*radius),str(p+abs(s)*radius)]})
    # Complementary chord: constant midpoint 1/2, but endpoint mean is 2/5.
    r1,r2=F(-2,3),F(1,2); lam=F(2,5); r0=(1-lam)*r1+lam*r2
    def complement_ray(r):
        return exact_law(sp.eye(n)/2+sf(r)*(K-sp.eye(n)/2))
    for r in [r1,r2,r0]:
        pl=complement_ray(r); ml=complement_ray(-r)
        assert pl==list(reversed(ml))
    cg=entropy(complement_ray(r0))-(1-lam)*entropy(complement_ray(r1))-lam*entropy(complement_ray(r2))
    cb=2*n*(p-F(1,2))**2*((1-lam)*r1*r1+lam*r2*r2-r0*r0)
    assert (cg-cb).lo>0
    out['complementary_chord']={'midpoint':'1/2','endpoint_mean':str(p),
          'entropy_gap':cg.out(),'quadratic_lower_bound':str(cb),'slack':(cg-cb).out()}
    # Exact two-point obstruction to replacement by a correlated reference:
    # K=L, off-diagonal 1/4, diagonal 1/2. Target unchanged, selector output is not.
    corr=F(1,4); sel=F(1,2)
    true11=F(1,4)-corr*corr
    selector11=F(1,4)-(sel*sel+(1-sel)**2)*corr*corr
    assert selector11-true11==F(1,32)
    out['correlated_reference_obstruction']={'true_affine_DPP_P11':str(true11),
       'independent_selector_P11':str(selector11),'difference':str(selector11-true11)}
    (ROOT/'output').mkdir(exist_ok=True)
    (ROOT/'output/exact_finite_distributions.json').write_text(json.dumps(EXACT_OBJECTS,indent=2)+'\n')
    out['exact_finite_kernel_count']=len(EXACT_OBJECTS)
    (ROOT/'output/exact_audit.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
    print('PASS: exact channel, K-affine jets, curvature identity, pinching KL, and quartic lower bounds.')
    print(f'Logarithms: {NLOG} terms, rigorous rational tails; {logq.cache_info().currsize} cached positive arguments.')
    print('Certified results: output/exact_audit.json')

if __name__=='__main__':
    main()
