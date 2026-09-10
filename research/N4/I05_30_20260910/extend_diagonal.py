#!/usr/bin/env python3
"""Exact full-diagonal certificate for the fixed I05-30 canonical family.
No import from adjacent author scripts; no search or optimizer.
"""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import json
import sympy as sp

Q=sp.Rational
TERMS=32
BOXES=256

def fq(x):
    x=Q(x); return F(int(x.p),int(x.q))
def add(a,b): return a[0]+b[0],a[1]+b[1]
def scale(a,c):
    c=fq(c)
    return (a[0]*c,a[1]*c) if c>=0 else (a[1]*c,a[0]*c)
def mul(a,b):
    z=(a[0]*b[0],a[0]*b[1],a[1]*b[0],a[1]*b[1])
    return min(z),max(z)
def sub(a,b): return add(a,scale(b,-1))
def atanh_iv(z):
    z=fq(z); assert 0<=z<=F(1,3)
    zz=z*z; term=z; total=F(0)
    for j in range(TERMS):
        total += 2*term/(2*j+1); term*=zz
    tail=2*term/((2*TERMS+1)*(1-zz))
    return total,total+tail
LOG2=atanh_iv(F(1,3))
@lru_cache(None)
def logiv(x):
    x=fq(x); assert x>0
    k=x.numerator.bit_length()-x.denominator.bit_length()
    p=F(2)**k
    while x<p: k-=1; p/=2
    while x>=2*p: k+=1; p*=2
    y=x/p; z=(y-1)/(y+1)
    return add(scale(LOG2,k),atanh_iv(z))
def etaiv(x):
    x=fq(x)
    return (F(0),F(0)) if x==0 else scale(logiv(x),-x)
def entropy(vals):
    a=(F(0),F(0))
    for v in vals:a=add(a,etaiv(v))
    return a
def dec(x,d=24,upper=False):
    x=fq(x); q=10**d
    n=-((-x.numerator*q)//x.denominator) if upper else x.numerator*q//x.denominator
    sign='-' if n<0 else ''; n=abs(n)
    return f"{sign}{n//q}.{n%q:0{d}d}"
def show(a,d=24): return [dec(a[0],d),dec(a[1],d,True)]
def subsets(n):
    return [tuple(i for i in range(n) if mask>>i&1) for mask in range(1<<n)]
def signed_law(K):
    n=K.rows; out={}
    for S in subsets(n):
        E=sp.diag(*[0 if i in S else 1 for i in range(n)])
        out[S]=sp.factor((-1)**(n-len(S))*(K-E).det())
    return out
def mobius_law(K):
    n=K.rows; ss=subsets(n)
    d={S:(sp.factor(K.extract(S,S).det()) if S else sp.Integer(1)) for S in ss}
    out={S:sp.factor(sum((-1)**(len(T)-len(S))*d[T]
                           for T in ss if set(S)<=set(T))) for S in ss}
    assert out==signed_law(K)
    return out
def range_quadratic(p,x,lo,hi):
    P=sp.Poly(p,x); vals=[fq(P.eval(Q(lo.numerator,lo.denominator))),
                          fq(P.eval(Q(hi.numerator,hi.denominator)))]
    D=P.diff()
    if D.degree()==1:
        r=-D.nth(0)/D.nth(1); rf=fq(r)
        if lo<=rf<=hi: vals.append(fq(P.eval(r)))
    else:
        assert D.degree()<=0 or D.is_zero
    return min(vals),max(vals)

def main():
    A=sp.Matrix([[Q(2,5),Q(6,25)],[Q(6,25),Q(2,5)]])
    B=sp.Matrix([[Q(3,5),Q(9,25)],[Q(9,25),Q(3,5)]])
    c,s,x=sp.symbols('c s x',real=True)
    E=sp.eye(4)[:,:2]
    V=sp.Matrix([[c,0],[0,c],[s,0],[0,s]])
    X=E*A*E.T; Y=V*B*V.T; M=(X+Y)/2
    raw=signed_law(M)
    px={}
    for S,p in raw.items():
        P=sp.Poly(sp.expand(p),s)
        assert all(mon[0]%2==0 for mon,co in P.terms())
        pc=sum(co*(1-c*c)**(mon[0]//2) for mon,co in P.terms())
        C=sp.Poly(sp.expand(pc),c)
        assert all(mon[0]%2==0 for mon,co in C.terms())
        px[S]=sp.factor(sum(co*x**(mon[0]//2) for mon,co in C.terms()))
    assert sp.factor(sum(px.values())-1)==0
    assert all(p.subs(x,Q(1,2))>0 for p in px.values())
    for cv in [Q(0),Q(3,5),Q(1)]:
        sv=Q(1) if cv==0 else Q(0) if cv==1 else Q(4,5)
        VV=V.subs({c:cv,s:sv})
        direct=mobius_law((X+VV*B*VV.T)/2)
        assert all(sp.factor(direct[S]-px[S].subs(x,cv*cv))==0 for S in px)
    q={}; m={}
    for S,p in px.items():
        m[S]=sum(i in S for i in (2,3))
        q[S]=sp.factor(p/(1-x)**m[S])
        assert sp.factor(p-(1-x)**m[S]*q[S])==0
        assert q[S].subs(x,0)>0 and q[S].subs(x,1)>0
    assert sp.factor(sum(m[S]*sp.diff(px[S],x) for S in px)+Q(3,5))==0
    uppers=[]; records=[]
    for j in range(BOXES):
        lo,hi=F(j,BOXES),F(j+1,BOXES)
        total=(F(0),F(0))
        for S in subsets(4):
            dr=range_quadratic(sp.diff(px[S],x),x,lo,hi)
            qr=range_quadratic(q[S],x,lo,hi)
            lr=(logiv(qr[0])[0],logiv(qr[1])[1])
            total=add(total,mul((-dr[1],-dr[0]),lr))
        if lo==0:
            total=(F(-10**1000),total[1]+F(3,5)*logiv(hi)[1])
        else:
            total=add(total,scale((logiv(lo)[0],logiv(hi)[1]),F(3,5)))
        assert total[1]<0
        uppers.append(total[1]); records.append(dec(total[1],18,True))
    pA=[F(189,625),F(186,625),F(186,625),F(64,625)]
    pB=[F(19,625),F(231,625),F(231,625),F(144,625)]
    pT=[F(4,25),F(17,50),F(17,50),F(4,25)]
    anchor=sub(entropy(pT),scale(add(entropy(pA),entropy(pB)),F(1,2)))
    assert anchor[0]>0
    out={
      "status":"AUTHOR EXACT INTERVAL CERTIFICATE; PENDING_EXTERNAL_REVIEW",
      "parameter":"t1=t2=t, c=(1-t^2)/(1+t^2), x=c^2 in [0,1]",
      "full_atoms":{','.join(str(i+1) for i in S):str(px[S]) for S in subsets(4)},
      "factor_orders_bottom":{','.join(str(i+1) for i in S):m[S] for S in subsets(4)},
      "regular_factors_q":{','.join(str(i+1) for i in S):str(q[S]) for S in subsets(4)},
      "derivative_identity":"G_x'=-sum_S p'_S log q_S+(3/5)log x",
      "partition_denominator":BOXES,
      "maximum_box_upper":dec(max(uppers),24,True),
      "maximum_box_index":uppers.index(max(uppers)),
      "G_prime_upper_by_box":records,
      "minimum_anchor_x_1_G_interval":show(anchor),
      "log_terms":TERMS,
      "log_remainder":"2*z^(2*N+1)/((2*N+1)*(1-z^2)), 0<=z<=1/3"
    }
    target=Path(__file__).with_name('diagonal_extension_certificate.json')
    target.write_text(json.dumps(out,indent=2)+'\n')
    print('PASS',target)
    print('max derivative upper',out['maximum_box_upper'],'box',out['maximum_box_index'])
    print('minimum G',out['minimum_anchor_x_1_G_interval'])
if __name__=='__main__':main()
