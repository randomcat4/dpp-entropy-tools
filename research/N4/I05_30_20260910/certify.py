#!/usr/bin/env python3
"""Narrow exact verifier for I05-30/#84. No scan or optimizer.
The event-determinant check follows agent24/code/verify_rank1_midpoint.py;
independent Mobius inversion, rational log enclosures and fixed rank-two inputs
are added. All displayed intervals are rounded OUTWARD using integers.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import combinations
from math import comb, factorial
from pathlib import Path
import json
import sympy as sp
Q=sp.Rational
TERMS=48
SS=[tuple(i for i in range(4) if mask>>i&1) for mask in range(16)]

def frac(x):
    x=sp.Rational(x)
    return F(int(x.p),int(x.q))
def ivadd(a,b): return (a[0]+b[0],a[1]+b[1])
def ivscale(a,c):
    c=frac(c)
    return (a[0]*c,a[1]*c) if c>=0 else (a[1]*c,a[0]*c)
def ivsub(a,b): return ivadd(a,ivscale(b,-1))
def atanh_series(z):
    z=frac(z); assert 0<=z<=F(1,3)
    zz=z*z; term=z; v=F(0)
    for j in range(TERMS):
        v+=2*term/(2*j+1);term*=zz
    tail=2*term/((2*TERMS+1)*(1-zz))
    return v,v+tail
LOG2=atanh_series(F(1,3))
def logiv(x):
    x=frac(x);assert x>0
    k=x.numerator.bit_length()-x.denominator.bit_length()
    power=F(2)**k
    while x<power: k-=1;power/=2
    while x>=2*power:k+=1;power*=2
    y=x/power;z=(y-1)/(y+1)
    return ivadd(ivscale(LOG2,k),atanh_series(z))
def etaiv(x):
    x=frac(x);assert x>=0
    return (F(0),F(0)) if x==0 else ivscale(logiv(x),-x)
def entropy(p):
    out=(F(0),F(0))
    for x in p.values():out=ivadd(out,etaiv(x))
    return out
def h2(x):return ivadd(etaiv(x),etaiv(1-x))
def dec(x,digits=24,upper=False):
    x=frac(x);den=10**digits
    v=-((-x.numerator*den)//x.denominator) if upper else x.numerator*den//x.denominator
    sign='-' if v<0 else '';v=abs(v)
    return sign+str(v//den)+'.'+str(v%den).zfill(digits)
def ivshow(iv):return [dec(iv[0]),dec(iv[1],upper=True)]
def signed_law(K):
    out={}
    for S in SS:
        E=sp.diag(*[0 if i in S else 1 for i in range(4)])
        out[S]=sp.factor((-1)**(4-len(S))*(K-E).det())
    return out
def law(K):
    ds={S:sp.factor(K.extract(S,S).det()) if S else Q(1) for S in SS}
    out={S:sp.factor(sum((-1)**(len(T)-len(S))*ds[T] for T in SS if set(S)<=set(T))) for S in SS}
    assert sum(out.values())==1 and all(v>=0 for v in out.values())
    assert out==signed_law(K)
    return out
def frame(t,u):
    c1=(1-t*t)/(1+t*t);s1=2*t/(1+t*t)
    c2=(1-u*u)/(1+u*u);s2=2*u/(1+u*u)
    return sp.Matrix([[c1,0],[0,c2],[s1,0],[0,s2]])
def gap(px,py,pm):return ivsub(entropy(pm),ivscale(ivadd(entropy(px),entropy(py)),Q(1,2)))
def legal_psd(K):
    for n in range(1,5):
        for S in combinations(range(4),n):
            assert K.extract(S,S).det()>=0
            assert (sp.eye(4)-K).extract(S,S).det()>0

def symbolic_minors():
    a,d,r,b,e,z,c1,c2,s1,s2=sp.symbols('a d r b e z c1 c2 s1 s2',real=True)
    AA=sp.Matrix([[a,r],[r,d]]);BB=sp.Matrix([[b,z],[z,e]])
    E=sp.eye(4)[:,:2];V=sp.Matrix([[c1,0],[0,c2],[s1,0],[0,s2]])
    N=E*AA*E.T+V*BB*V.T;da=a*d-r*r;db=b*e-z*z
    expected={
    (0,1):da+db*c1*c1*c2*c2+a*e*c2*c2+d*b*c1*c1-2*r*z*c1*c2,
    (0,2):a*b*s1*s1,(0,3):(a*e+db*c1*c1)*s2*s2,
    (1,2):(d*b+db*c2*c2)*s1*s1,(1,3):d*e*s2*s2,
    (2,3):db*s1*s1*s2*s2,
    (0,1,2):s1*s1*(b*da+a*db*c2*c2),
    (0,1,3):s2*s2*(e*da+d*db*c1*c1),
    (0,2,3):a*db*s1*s1*s2*s2,(1,2,3):d*db*s1*s1*s2*s2,
    (0,1,2,3):da*db*s1*s1*s2*s2}
    for S,v in expected.items():assert sp.expand(N.extract(S,S).det()-v)==0
    return len(expected)
def jet_certificate(X,Y):
    t=sp.Symbol('t');K=X+t*(Y-X)
    minors={S:sp.Poly(K.extract(S,S).det(),t) if S else sp.Poly(1,t) for S in SS}
    pol={S:sum((-1)**(len(T)-len(S))*minors[T] for T in SS if set(S)<=set(T)) for S in SS}
    values={S:tuple(sp.factor(pol[S].diff((t,j)).eval(Q(1,2))) if j else sp.factor(pol[S].eval(Q(1,2))) for j in range(3)) for S in SS}
    assert sum(v[0] for v in values.values())==1
    assert sum(v[1] for v in values.values())==sum(v[2] for v in values.values())==0
    fisher=Q(0);acc=(F(0),F(0))
    for p,p1,p2 in values.values():
        if not p: assert p1==p2==0;continue
        fisher+=p1*p1/p;acc=ivadd(acc,ivscale(logiv(p),-p2))
    curv=ivsub(acc,(frac(fisher),frac(fisher)))
    return {'Fisher_exact':str(fisher),'acceleration_interval':ivshow(acc),'H_second_interval':ivshow(curv),'jets':{','.join(str(i+1) for i in S):[str(x) for x in v] for S,v in values.items()}}
def bitflip(p,eps):
    result={}
    for S in SS:
        result[S]=sp.factor(sum(v*eps**len(set(S)^set(T))*(1-eps)**(4-len(set(S)^set(T))) for T,v in p.items()))
    return result

def run():
    print('symbolic minors checked:',symbolic_minors())
    A=sp.Matrix([[Q(2,5),Q(6,25)],[Q(6,25),Q(2,5)]])
    B=sp.Matrix([[Q(3,5),Q(9,25)],[Q(9,25),Q(3,5)]])
    E=sp.eye(4)[:,:2];X=E*A*E.T
    out={'log_terms':TERMS,'log_remainder':'2*z^(2*N+1)/((2*N+1)*(1-z^2)); z in [0,1/3]','cases':{}}
    for name,u in [('intersection1',Q(0)),('intersection0',Q(1,50))]:
        V=frame(Q(1,100),u);Y=V*B*V.T;M=(X+Y)/2
        for K in [X,Y,M]:legal_psd(K)
        px,py,pm=map(law,[X,Y,M]);mix={S:(px[S]+py[S])/2 for S in SS}
        gg=gap(px,py,pm);bridge=ivsub(entropy(pm),entropy(mix))
        assert gg[0]>0 and bridge[1]<0
        anti=V*sp.diag(1,-1)*B*sp.diag(1,-1)*V.T
        pa=law((X+anti)/2)
        transfer=pa[(0,1)]-pm[(0,1)]
        for S in SS:
            expected=transfer if S in [(),(0,1)] else -transfer if S in [(0,),(1,)] else 0
            assert pa[S]-pm[S]==expected
        align_diff=ivsub(entropy(pa),entropy(pm));assert align_diff[0]>0
        jets=jet_certificate(X,Y);assert F(jets['H_second_interval'][1])<0
        eps=Q(1,100000);deltaflip=1-(1-eps)**4
        omega=ivadd(h2(deltaflip),ivscale(logiv(15),deltaflip))
        lifted_G_lower=gg[0]-2*omega[1];lifted_bridge_upper=bridge[1]+2*omega[1]
        assert lifted_G_lower>0 and lifted_bridge_upper<0
        for K,p in [(X,px),(Y,py),(M,pm)]:
            lifted=eps*sp.eye(4)+(1-2*eps)*K
            lp=law(lifted);assert lp==bitflip(p,eps) and all(x>0 for x in lp.values())
        record={'X':[[str(x) for x in row] for row in X.tolist()], 'Y':[[str(x) for x in row] for row in Y.tolist()],
        'rank_mid':M.rank(),'commutator_Frobenius_squared':str(sp.trace((X*Y-Y*X).T*(X*Y-Y*X))),
        'G_interval':ivshow(gg),'mixture_bridge_interval':ivshow(bridge),'anti_minus_aligned_interval':ivshow(align_diff),
        'atoms':{tag:{','.join(str(i+1) for i in S):str(v) for S,v in pp.items()} for tag,pp in [('minus',px),('plus',py),('mid',pm)]},
        'jet_certificate':jets,'epsilon':str(eps),'two_omega_upper':dec(2*omega[1],upper=True),
        'lifted_G_lower':dec(lifted_G_lower),'lifted_bridge_upper':dec(lifted_bridge_upper,upper=True)}
        out['cases'][name]=record
        print(name,json.dumps({k:v for k,v in record.items() if k not in ['X','Y','atoms','jet_certificate']}))
        print('curvature',jets['H_second_interval'])
    Y0=E*B*E.T;Gbase=gap(law(X),law(Y0),law((X+Y0)/2))
    w=Q(10000,6255001)
    delta_bound=Q(39,25)*2*w
    assert 0<delta_bound<Q(15,16)
    err=ivadd(h2(delta_bound),ivscale(logiv(15),delta_bound))
    err=ivadd(err,ivscale(h2(w),Q(3,5)))
    margin=ivsub(Gbase,err)
    print('raw angular margin',ivshow(margin)); assert margin[0]>Q(19,1000)
    out['angular_box']={'t1_t2':'[0,1/50]','max_sine_squared':str(w),'TV_bound':str(delta_bound),
                        'base_G_interval':ivshow(Gbase),'error_upper':dec(err[1],upper=True),'uniform_G_lower':dec(margin[0]),'claimed_simple_lower':'19/1000'}
    print('angular_box',json.dumps(out['angular_box']))
    Path(__file__).with_name('certificate.json').write_text(json.dumps(out,indent=2)+'\n')

if __name__=='__main__':run()
