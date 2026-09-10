#!/usr/bin/env python3
"""Rigorous fixed-family full-square Jensen certificate for I05-30.

Copied from frozen PR86 head bd12e6094e098499fae7e01729a4b29f021a14e2.
It reconstructs all 16 complete midpoint atoms from signed determinants, removes
both marking singularities algebraically, and covers [0,1]^2 by 64^2 exact
rational interval boxes. No random search, optimizer, or adjacent import.
"""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import json
import platform
import sympy as sp

Q=sp.Rational
TERMS=32
NBOX=64

def fq(x):
    x=Q(x); return F(int(x.p),int(x.q))
def add(a,b): return a[0]+b[0],a[1]+b[1]
def scale(a,c):
    c=fq(c)
    return (a[0]*c,a[1]*c) if c>=0 else (a[1]*c,a[0]*c)
def sub(a,b): return add(a,scale(b,-1))
def atanh_iv(z):
    z=fq(z); assert 0<=z<=F(1,3)
    zz=z*z; term=z; total=F(0)
    for j in range(TERMS):
        total+=2*term/(2*j+1); term*=zz
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
    out=(F(0),F(0))
    for x in vals: out=add(out,etaiv(x))
    return out
def dec(x,digits=18,upper=False):
    x=fq(x); den=10**digits
    z=-((-x.numerator*den)//x.denominator) if upper else x.numerator*den//x.denominator
    sign='-' if z<0 else ''; z=abs(z)
    return f"{sign}{z//den}.{z%den:0{digits}d}"
def show(a,digits=24): return [dec(a[0],digits),dec(a[1],digits,True)]
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
    assert sp.factor(sum(out.values())-1)==0
    return out
def coefficient_dict(poly,x,y):
    P=sp.Poly(sp.expand(poly),x,y)
    return {mon:fq(coef) for mon,coef in P.terms()}
def polynomial_interval(coeff,a,b,c,d):
    lo=hi=F(0)
    for (i,j),coef in coeff.items():
        ml=a**i*c**j; mh=b**i*d**j
        if coef>=0: lo+=coef*ml; hi+=coef*mh
        else: lo+=coef*mh; hi+=coef*ml
    return lo,hi
def f_lower(a,b):
    if b<=F(3,5):
        return F(0) if b==0 else b*b*logiv(b*b)[0]
    if a>=F(61,100):
        return a*a*logiv(a*a)[0]
    return F(-3,8)

def main():
    A=sp.Matrix([[Q(2,5),Q(6,25)],[Q(6,25),Q(2,5)]])
    B=sp.Matrix([[Q(3,5),Q(9,25)],[Q(9,25),Q(3,5)]])
    assert A.det()>0 and (sp.eye(2)-A).det()>0
    assert B.det()>0 and (sp.eye(2)-B).det()>0
    c1,c2,s1,s2=sp.symbols('c1 c2 s1 s2',nonnegative=True,real=True)
    E=sp.eye(4)[:,:2]
    V=sp.Matrix([[c1,0],[0,c2],[s1,0],[0,s2]])
    X=E*A*E.T; Y=V*B*V.T; M=(X+Y)/2
    raw=signed_law(M)
    p={}
    for S,val in raw.items():
        P=sp.Poly(sp.expand(val),s1,s2)
        assert all(mon[0]%2==0 and mon[1]%2==0 for mon,coef in P.terms())
        p[S]=sp.factor(sum(coef*(1-c1*c1)**(mon[0]//2)*
                                      (1-c2*c2)**(mon[1]//2)
                           for mon,coef in P.terms()))
    assert sp.factor(sum(p.values())-1)==0
    for a,b,u,v in [(Q(0),Q(0),Q(1),Q(1)),
                    (Q(3,5),Q(5,13),Q(4,5),Q(12,13)),
                    (Q(1),Q(1),Q(0),Q(0))]:
        VV=V.subs({c1:a,c2:b,s1:u,s2:v})
        direct=mobius_law((X+VV*B*VV.T)/2)
        assert all(sp.factor(direct[S]-p[S].subs({c1:a,c2:b}))==0 for S in p)
    q={}; order={}
    for S,val in p.items():
        order[S]=(int(2 in S),int(3 in S))
        den=(1-c1*c1)**order[S][0]*(1-c2*c2)**order[S][1]
        q[S]=sp.factor(val/den)
        assert sp.factor(val-den*q[S])==0
    assert sp.factor(sum(order[S][0]*p[S] for S in p)-Q(3,10)*(1-c1*c1))==0
    assert sp.factor(sum(order[S][1]*p[S] for S in p)-Q(3,10)*(1-c2*c2))==0
    pc={S:coefficient_dict(v,c1,c2) for S,v in p.items()}
    qc={S:coefficient_dict(v,c1,c2) for S,v in q.items()}
    pA=[F(189,625),F(186,625),F(186,625),F(64,625)]
    pB=[F(19,625),F(231,625),F(231,625),F(144,625)]
    endpoint_constant=scale(add(entropy(pA),entropy(pB)),F(1,2))
    derivative_left=logiv(F(9,25))[1]+1
    derivative_right=logiv(F(3721,10000))[0]+1
    assert derivative_left<0<derivative_right
    row_minima=[]; row_argmins=[]; minimum=None; minimum_box=None
    min_q=F(1); max_q=F(0)
    for i in range(NBOX):
        a,b=F(i,NBOX),F(i+1,NBOX)
        row_min=None; row_arg=None
        for j in range(NBOX):
            c,d=F(j,NBOX),F(j+1,NBOX)
            lower=F(0)
            for S in subsets(4):
                pl,pu=polynomial_interval(pc[S],a,b,c,d)
                pl=max(pl,F(0))
                ql,qu=polynomial_interval(qc[S],a,b,c,d)
                assert 0<ql<=qu<1
                min_q=min(min_q,ql); max_q=max(max_q,qu)
                lower += pl*(-logiv(qu)[1])
            lower += F(3,10)*(f_lower(a,b)+f_lower(c,d))
            lower -= endpoint_constant[1]
            assert lower>0
            if minimum is None or lower<minimum:
                minimum=lower; minimum_box=(i,j)
            if row_min is None or lower<row_min:
                row_min=lower; row_arg=j
        row_minima.append(dec(row_min,12))
        row_argmins.append(row_arg)
    assert minimum>F(1,100)
    eps=F(1,100000); delta=1-(1-eps)**4
    hdelta=add(etaiv(delta),etaiv(1-delta))
    two_omega=scale(add(hdelta,scale(logiv(F(15)),delta)),F(2))
    assert F(1,100)-two_omega[1]>F(8893242,10**9)
    out={
      "status":"AUTHOR FIXED-FAMILY EXACT COVER; PENDING_EXTERNAL_REVIEW",
      "python":platform.python_version(),"sympy":sp.__version__,
      "family":{"A":[["2/5","6/25"],["6/25","2/5"]],
                "B":[["3/5","9/25"],["9/25","3/5"]],
                "parameters":"c1,c2 in [0,1], sj=sqrt(1-cj^2); true arithmetic midpoint"},
      "regular_entropy_identity":
        "G=-sum_S p_S log(q_S)+(3/10)c1^2 log(c1^2)+(3/10)c2^2 log(c2^2)-(H(A)+H(B))/2",
      "full_atoms":{','.join(str(k+1) for k in S):str(p[S]) for S in subsets(4)},
      "regular_factors_q":{','.join(str(k+1) for k in S):str(q[S]) for S in subsets(4)},
      "bottom_factor_orders":{','.join(str(k+1) for k in S):list(order[S]) for S in subsets(4)},
      "cover":{"grid":"64 x 64 closed rational boxes","box_count":NBOX*NBOX,
               "minimum_box_zero_based":list(minimum_box),
               "minimum_G_lower":dec(minimum,18),
               "proved_simple_uniform_lower":"1/100",
               "row_minimum_G_lowers_rounded_down_12dp":row_minima,
               "row_minimum_column_zero_based":row_argmins,
               "minimum_q_lower":str(min_q),"maximum_q_upper":str(max_q)},
      "scalar_term_bound":{
        "left_monotonicity_check_upper":dec(derivative_left,24,True),
        "right_monotonicity_check_lower":dec(derivative_right,24),
        "crossing_bound":"c^2 log(c^2)>-3/8 from e>8/3"},
      "endpoint_entropy_constant_interval":show(endpoint_constant),
      "strict_lift":{"epsilon":"1/100000","two_omega_upper":dec(two_omega[1],24,True),
                     "simple_lifted_G_lower":"0.008893242"},
      "log_terms":TERMS,
      "log_remainder":"2*z^(2*N+1)/((2*N+1)*(1-z^2)); 0<=z<=1/3"
    }
    target=Path(__file__).with_name("full_square_certificate.json")
    target.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print("PASS",target)
    print("boxes",NBOX*NBOX,"minimum lower",out["cover"]["minimum_G_lower"],"at",minimum_box)
    print("q range",min_q,max_q)
if __name__=="__main__":main()
