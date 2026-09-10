#!/usr/bin/env python3
"""Fresh narrow recheck/extension for PR86.

No import from the author scripts.  It independently reconstructs the two
one-parameter edge laws from signed determinants, certifies a full
one-dimensional support-intersection edge by rational log intervals, and
certifies a rank-four zero-intersection edge by an exact Bernstein polynomial.
This is not a generic scanner.
"""
from __future__ import annotations
from fractions import Fraction as F
from functools import lru_cache
from math import comb
from pathlib import Path
import json
import sympy as sp

Q = sp.Rational
LOG_TERMS = 32
BOXES = 256

def frac(x):
    x = Q(x)
    return F(int(x.p), int(x.q))

def ivadd(a,b): return a[0]+b[0], a[1]+b[1]
def ivscale(a,c):
    c=frac(c)
    return (a[0]*c,a[1]*c) if c>=0 else (a[1]*c,a[0]*c)
def ivmul(a,b):
    z=(a[0]*b[0],a[0]*b[1],a[1]*b[0],a[1]*b[1])
    return min(z),max(z)
def ivsub(a,b): return ivadd(a,ivscale(b,-1))

def atanh_iv(z):
    z=frac(z); assert 0<=z<=F(1,3)
    zz=z*z; term=z; total=F(0)
    for j in range(LOG_TERMS):
        total += 2*term/(2*j+1)
        term *= zz
    tail = 2*term/((2*LOG_TERMS+1)*(1-zz))
    return total,total+tail

LOG2=atanh_iv(F(1,3))

@lru_cache(None)
def logiv(x):
    x=frac(x); assert x>0
    k=x.numerator.bit_length()-x.denominator.bit_length()
    p=F(2)**k
    while x<p: k-=1; p/=2
    while x>=2*p: k+=1; p*=2
    y=x/p; z=(y-1)/(y+1)
    return ivadd(ivscale(LOG2,k),atanh_iv(z))

def etaiv(x):
    x=frac(x)
    return (F(0),F(0)) if x==0 else ivscale(logiv(x),-x)

def entropy_iv(probs):
    ans=(F(0),F(0))
    for p in probs: ans=ivadd(ans,etaiv(p))
    return ans

def dec(x,digits=24,upper=False):
    x=frac(x); scale=10**digits
    z=(-((-x.numerator*scale)//x.denominator)
       if upper else (x.numerator*scale)//x.denominator)
    sign='-' if z<0 else ''; z=abs(z)
    return f"{sign}{z//scale}.{z%scale:0{digits}d}"

def ivshow(x,digits=24):
    return [dec(x[0],digits),dec(x[1],digits,True)]

def subsets(n):
    return [tuple(i for i in range(n) if mask>>i&1) for mask in range(1<<n)]

def signed_law(K):
    n=K.rows; out={}
    for S in subsets(n):
        E=sp.diag(*[0 if i in S else 1 for i in range(n)])
        out[S]=sp.factor((-1)**(n-len(S))*(K-E).det())
    return out

def replace_even_s(expr,s,c):
    poly=sp.Poly(sp.expand(expr),s)
    assert all(k[0]%2==0 for k,_ in poly.terms())
    return sp.factor(sum(a*(1-c*c)**(k[0]//2) for k,a in poly.terms()))

A=sp.Matrix([[Q(2,5),Q(6,25)],[Q(6,25),Q(2,5)]])
B=sp.Matrix([[Q(3,5),Q(9,25)],[Q(9,25),Q(3,5)]])
E4=sp.eye(4)[:,:2]

def laws_from_determinants():
    c,s=sp.symbols('c s', real=True)
    X=E4*A*E4.T
    # Edge I: t2=0, effective coordinates 1,2,3.
    E3=sp.eye(3)[:,:2]
    V3=sp.Matrix([[c,0],[0,1],[s,0]])
    pm3=signed_law((E3*A*E3.T+V3*B*V3.T)/2)
    pm3={S:replace_even_s(v,s,c) for S,v in pm3.items()}
    expected3=[
      (305-54*c-51*c*c)/1250,
      (92+54*c+279*c*c)/1250,
      (395+54*c-24*c*c)/1250,
      (83-54*c+171*c*c)/1250,
      177*(1-c*c)/1250,51*(1-c*c)/1250,
      123*(1-c*c)/1250,24*(1-c*c)/1250]
    for S,v in zip(subsets(3),expected3):
        assert sp.factor(pm3[S]-v)==0
    # Edge II: t2=1. Put u=c^2 after determinant reconstruction.
    V4=sp.Matrix([[c,0],[0,0],[s,0],[0,1]])
    pm4=signed_law((X+V4*B*V4.T)/2)
    pm4c={S:replace_even_s(v,s,c) for S,v in pm4.items()}
    u=sp.symbols('u',real=True)
    pm4u={}
    for S,v in pm4c.items():
        poly=sp.Poly(sp.expand(v),c)
        assert all(k[0] in (0,2) for k,_ in poly.terms())
        pm4u[S]=sp.factor(sum(a*u**(k[0]//2) for k,a in poly.terms()))
    assert sp.factor(sum(pm3.values())-1)==0
    assert sp.factor(sum(pm4u.values())-1)==0
    return c,u,pm3,pm4u

def qrange(Ac,Bc,Cc,l,u):
    vals=[Ac*l*l+Bc*l+Cc,Ac*u*u+Bc*u+Cc]
    if Ac:
        v=-Bc/(2*Ac)
        if l<=v<=u: vals.append(Ac*v*v+Bc*v+Cc)
    return min(vals),max(vals)

def certify_intersection_edge(c,pm3):
    top=[pm3[S] for S in [(),(0,),(1,),(0,1)]]
    alpha=[F(177,1250),F(51,1250),F(123,1250),F(24,1250)]
    assert sum(alpha)==F(3,10)
    C=(F(0),F(0))
    for x in alpha: C=ivadd(C,ivscale(logiv(x),x))
    coeff=[]
    for p in top:
        poly=sp.Poly(p,c)
        coeff.append(tuple(frac(poly.nth(j)) for j in (2,1,0)))
    uppers=[]
    records=[]
    for j in range(BOXES):
        l,u=F(j,BOXES),F(j+1,BOXES)
        total=(F(0),F(0))
        for aa,bb,dd in coeff:
            pr=qrange(aa,bb,dd,l,u)
            lr=(logiv(pr[0])[0],logiv(pr[1])[1])
            dr=sorted((2*aa*l+bb,2*aa*u+bb))
            total=ivadd(total,ivmul((-dr[1],-dr[0]),lr))
        total=ivadd(total,ivmul((2*l,2*u),C))
        # On the first box, (3/5)c log(c^2) only needs the valid upper bound 0.
        if j:
            logs=(logiv(l*l)[0],logiv(u*u)[1])
            total=ivadd(total,ivscale(ivmul((l,u),logs),F(3,5)))
        upper=total[1]
        assert upper<0
        uppers.append(upper)
        records.append(dec(upper,18,True))
    pA=[F(189,625),F(186,625),F(186,625),F(64,625)]
    pB=[F(19,625),F(231,625),F(231,625),F(144,625)]
    pT=[F(4,25),F(17,50),F(17,50),F(4,25)]
    G1=ivsub(entropy_iv(pT),ivscale(ivadd(entropy_iv(pA),entropy_iv(pB)),F(1,2)))
    assert G1[0]>0
    return {
      "parameter":"c=(1-t1^2)/(1+t1^2), t2=0, c in [0,1]",
      "active_midpoint_atoms":[str(v) for v in [pm3[S] for S in subsets(3)]],
      "derivative_identity":"G'=-sum_top p'_S log p_S+2*c*sum(alpha log alpha)+(3/5)c log(c^2)",
      "partition_denominator":BOXES,
      "maximum_box_upper":dec(max(uppers),24,True),
      "maximum_box_index":uppers.index(max(uppers)),
      "minimum_anchor_c_1_G_interval":ivshow(G1),
      "G_prime_upper_by_box":records}

def bernstein_coefficients(poly,var):
    P=sp.Poly(poly,var); n=P.degree()
    a=[P.nth(j) for j in range(n+1)]
    return [sp.factor(sum(a[j]*sp.binomial(k,j)/sp.binomial(n,j)
                          for j in range(k+1))) for k in range(n+1)]

def certify_zero_intersection_edge(u,pm4u):
    vanish={S:sp.factor(p/(1-u)) for S,p in pm4u.items() if p.subs(u,1)==0}
    non={S:p for S,p in pm4u.items() if p.subs(u,1)!=0}
    assert len(vanish)==len(non)==8
    assert sp.factor(sum(vanish.values())-Q(3,10))==0
    slopes={S:sp.diff(p,u) for S,p in non.items()}
    assert sp.factor(sum(slopes.values())-Q(3,10))==0
    R=sp.factor(Q(3,10)/u-sum(slopes[S]**2/non[S] for S in non))
    num,_=map(sp.factor,sp.fraction(R))
    content,primitive=sp.Poly(num,u).primitive()
    b=bernstein_coefficients(primitive,u)
    assert all(x>0 for x in b)
    for S,p in non.items():
        assert p.subs(u,0)>0 and p.subs(u,1)>0
    C=(F(0),F(0))
    for x in vanish.values(): C=ivadd(C,ivscale(logiv(x),x))
    d1=C
    for S,p in non.items():
        d1=ivsub(d1,ivscale(logiv(p.subs(u,1)),slopes[S]))
    assert d1[1]<0
    pm=[frac(pm4u[S].subs(u,1)) for S in subsets(4)]
    pA=[F(189,625),F(186,625),F(186,625),F(64,625)]
    pB=[F(19,625),F(231,625),F(231,625),F(144,625)]
    G1=ivsub(entropy_iv(pm),ivscale(ivadd(entropy_iv(pA),entropy_iv(pB)),F(1,2)))
    assert G1[0]>0
    return {
      "parameter":"u=c1^2 in [0,1], t2=1",
      "active_midpoint_atoms":[str(pm4u[S]) for S in subsets(4)],
      "convexity_identity":"G''=3/(10*u)-sum_nonvanishing (p'_S)^2/p_S",
      "numerator_content":str(content),
      "primitive_power_coefficients":[str(sp.Poly(primitive,u).nth(j))
                                      for j in range(sp.degree(primitive,u)+1)],
      "primitive_Bernstein_coefficients":[str(x) for x in b],
      "all_Bernstein_positive":True,
      "limiting_G_prime_at_u_1_interval":ivshow(d1),
      "minimum_anchor_u_1_G_interval":ivshow(G1)}

def law_mobius(K):
    n=K.rows; ss=subsets(n)
    d={S:(sp.factor(K.extract(S,S).det()) if S else sp.Integer(1)) for S in ss}
    out={S:sp.factor(sum((-1)**(len(T)-len(S))*d[T]
                           for T in ss if set(S)<=set(T))) for S in ss}
    assert out==signed_law(K)
    assert sp.factor(sum(out.values())-1)==0
    assert all(x>=0 for x in out.values())
    return out

def gap_iv(px,py,pm):
    return ivsub(entropy_iv([frac(x) for x in pm.values()]),
                 ivscale(ivadd(entropy_iv([frac(x) for x in px.values()]),
                               entropy_iv([frac(x) for x in py.values()])),F(1,2)))

def curvature_midpoint(X,Y):
    z=sp.symbols('z',real=True); K=X+z*(Y-X); n=K.rows
    vals=[]
    for S in subsets(n):
        E=sp.diag(*[0 if i in S else 1 for i in range(n)])
        p=sp.Poly(sp.expand((-1)**(n-len(S))*(K-E).det()),z)
        vals.append((sp.factor(p.eval(Q(1,2))),
                     sp.factor(p.diff().eval(Q(1,2))),
                     sp.factor(p.diff().diff().eval(Q(1,2)))))
    assert sp.factor(sum(x[0] for x in vals)-1)==0
    assert sp.factor(sum(x[1] for x in vals))==0
    assert sp.factor(sum(x[2] for x in vals))==0
    fisher=F(0); acc=(F(0),F(0))
    for p,p1,p2 in vals:
        if p==0:
            assert p1==p2==0
            continue
        fisher += frac(p1*p1/p)
        acc=ivadd(acc,ivscale(logiv(p),-p2))
    return fisher,acc,ivsub(acc,(fisher,fisher))

def recheck_pr86_fixed_claims():
    def frame(t1,t2):
        c1=(1-t1*t1)/(1+t1*t1); s1=2*t1/(1+t1*t1)
        c2=(1-t2*t2)/(1+t2*t2); s2=2*t2/(1+t2*t2)
        return sp.Matrix([[c1,0],[0,c2],[s1,0],[0,s2]])
    X=E4*A*E4.T; out={}
    for name,t2 in [('intersection1',Q(0)),('intersection0',Q(1,50))]:
        V=frame(Q(1,100),t2); Y=V*B*V.T; M=(X+Y)/2
        px,py,pm=map(law_mobius,(X,Y,M))
        mix={S:(px[S]+py[S])/2 for S in px}
        g=gap_iv(px,py,pm)
        bridge=ivsub(entropy_iv([frac(x) for x in pm.values()]),
                     entropy_iv([frac(x) for x in mix.values()]))
        fish,acc,curv=curvature_midpoint(X,Y)
        assert g[0]>0 and bridge[1]<0 and curv[1]<0
        out[name]={"G_interval":ivshow(g),"bridge_interval":ivshow(bridge),
                   "Fisher_exact":str(fish),"acceleration_interval":ivshow(acc),
                   "H_second_interval":ivshow(curv)}
    pA=[F(189,625),F(186,625),F(186,625),F(64,625)]
    pB=[F(19,625),F(231,625),F(231,625),F(144,625)]
    pT=[F(4,25),F(17,50),F(17,50),F(4,25)]
    base=ivsub(entropy_iv(pT),ivscale(ivadd(entropy_iv(pA),entropy_iv(pB)),F(1,2)))
    w=F(10000,6255001); delta=F(31200,6255001)
    h=lambda x:ivadd(etaiv(x),etaiv(1-x))
    err=ivadd(h(delta),ivscale(logiv(15),delta))
    err=ivadd(err,ivscale(h(w),F(3,5)))
    margin=ivsub(base,err)
    assert margin[0]>F(19,1000)
    out["angular_box"]={"base_G_interval":ivshow(base),"error_interval":ivshow(err),
                         "uniform_G_lower":dec(margin[0],24)}
    return out

def main():
    c,u,pm3,pm4u=laws_from_determinants()
    first=certify_intersection_edge(c,pm3)
    second=certify_zero_intersection_edge(u,pm4u)
    old=recheck_pr86_fixed_claims()
    out={"status":"FRESH SAME-SESSION RECHECK; NOT EXTERNAL REVIEW",
         "rechecked_PR86_fixed_claims":old,
         "python_log_terms":LOG_TERMS,
         "log_remainder":"2*z^(2*N+1)/((2*N+1)*(1-z^2)), 0<=z<=1/3",
         "intersection_edge":first,
         "zero_intersection_edge":second}
    target=Path(__file__).with_name("edge_extension_certificate.json")
    target.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print("PASS",target)
    print("intersection max G' upper",first["maximum_box_upper"],
          "minimum G",first["minimum_anchor_c_1_G_interval"])
    print("zero-intersection G'(1)",second["limiting_G_prime_at_u_1_interval"],
          "minimum G",second["minimum_anchor_u_1_G_interval"])
if __name__=="__main__":
    main()
