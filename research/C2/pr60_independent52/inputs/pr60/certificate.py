"""Exact full-domain Lambda-zero certificate; author verification, not independent review.
Run: python certificate.py --out outputs
Python >=3.10, SymPy 1.14.0. No floating arithmetic is used.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
from itertools import permutations
from math import comb
from pathlib import Path
import json
import time
import sympy as s
from sympy.polys.rings import ring
from sympy.polys.domains import QQ

mu,nu,r,t=s.symbols('mu nu r t')
VARS=(mu,nu,r,t)

def residual_polynomial():
    c40=t**3*(r-1)**4*(r+1)**2*(t-1)*(r*r*t-1)*(r*r*t-r*r+r-1)
    c31=-2*t*t*(r-1)**3*(r+1)*(2*r**6*t**4-4*r**6*t**3+2*r**6*t*t+2*r**5*t**4-3*r**5*t**3+r**5*t*t+2*r**4*t**4-2*r**4*t**3-7*r**4*t*t+3*r**4*t-3*r**3*t**3+4*r**3*t*t-r**3*t-4*r*r*t**3-7*r*r*t*t+28*r*r*t-9*r*r+r*t*t-r*t+2*t*t+3*t-9)
    c22=2*t*t*(r-1)**2*(r+1)**2*(3*r**6*t**4-6*r**6*t**3+3*r**6*t*t+3*r**4*t**4-2*r**4*t**3-16*r**4*t*t+7*r**4*t-6*r*r*t**3-16*r*r*t*t+56*r*r*t-18*r*r+3*t*t+7*t-18)
    c20=2*t*(r-1)**2*(6*r**6*t**5-24*r**6*t**4-11*r**6*t**3+r**6*t*t-30*r**5*t**4-6*r**5*t**3-12*r**5*t*t-24*r**4*t**4-26*r**4*t**3+89*r**4*t*t-3*r**4*t-6*r**3*t**3+48*r**3*t*t+54*r**3*t-11*r*r*t**3+89*r*r*t*t-48*r*r*t-18*r*r-12*r*t*t+54*r*t-90*r+t*t-3*t-18)
    c11=-4*(r-1)*(r+1)*(6*r**6*t**6-24*r**6*t**5-11*r**6*t**4+r**6*t**3-24*r**4*t**5-56*r**4*t**4+155*r**4*t**3-15*r**4*t*t-11*r*r*t**4+155*r*r*t**3-144*r*r*t*t-36*r*r*t+t**3-15*t*t-36*t+54)
    c00=-24*(2*r*r*t-r*r-1)*(3*r**4*t**4+3*r**4*t**3-2*r**4*t*t+3*r*r*t**3-8*r*r*t*t-3*r*r*t-2*t*t-3*t+9)
    return s.Poly(c40*mu**4+c31*mu**3*nu+c22*mu**2*nu**2+c31.subs(r,-r)*mu*nu**3+c40.subs(r,-r)*nu**4+c20*mu**2+c11*mu*nu+c20.subs(r,-r)*nu**2+c00,*VARS)

def reduced_matrix():
    a=(1+r)/2;b=(1-r)/2;v=(1-mu**2)/4;w=(1-nu**2)/4
    J=1-t;L=1-r*r*t;C=1-r*r*t*t
    D=s.diag(1,v,w,v*w)
    S=s.Matrix([[mu*nu,2*v*nu,2*w*mu,4*v*w],[2*v*nu,-mu*nu*v,4*v*w,-2*mu*v*w],[2*w*mu,4*v*w,-mu*nu*w,-2*nu*v*w],[4*v*w,-2*mu*v*w,-2*nu*v*w,mu*nu*v*w]])
    G=(1/J+1/L)/2*D+(1/J-1/L)/2*S
    N=s.diag(0,1,1,2);theta=a*nu+b*mu
    la=s.Matrix([-2*b,theta,0,2*a*w]);lb=s.Matrix([-2*a,0,theta,2*b*v])
    RB=N*G+G*N+4*t*G.diff(t)+s.diag(0,v*(1-r*t)/(J*L),w*(1+r*t)/(J*L),2*v*w/(J*L))
    RB-=4*v*b*b*t*t/(J*L*(1-r*t))*la*la.T
    RB-=4*w*a*a*t*t/(J*L*(1+r*t))*lb*lb.T
    return RB,D,2*J**2*L**2*C

def chart(data,axis,degree,lo,hi):
    """Multiply by (1+X)^degree and substitute (lo+hi*X)/(1+X)."""
    out=defaultdict(int)
    coeffs={}
    for k in range(degree+1):
        arr=[0]*(degree+1)
        for i in range(k+1):
            for j in range(degree-k+1):
                arr[i+j]+=comb(k,i)*lo**(k-i)*hi**i*comb(degree-k,j)
        coeffs[k]=arr
    for exp,c in data.items():
        for i,d in enumerate(coeffs[exp[axis]]):
            if d:
                e=list(exp);e[axis]=i;out[tuple(e)]+=c*d
    return {e:c for e,c in out.items() if c}

def run(out: Path | None = None):
    started=time.monotonic()
    P=residual_polynomial()
    assert P.degree_list()==(4,4,10,6)
    assert len(P.terms())==279
    assert s.Poly(P.as_expr()-P.as_expr().xreplace({mu:-mu,nu:-nu}),*VARS).is_zero
    assert s.Poly(P.as_expr()-P.as_expr().xreplace({mu:nu,nu:mu,r:-r}),*VARS).is_zero
    RB,D,den=reduced_matrix()
    R,mm,nn,rr,tt=ring('mu,nu,r,t',QQ)
    A=[]
    for i in range(4):
        row=[]
        for j in range(4):
            f=s.cancel(den*RB[i,j]/D[i,i])
            _,bottom=s.fraction(f)
            assert not bottom.free_symbols
            row.append(R.from_expr(f))
        A.append(row)
    det=R.zero
    for p in permutations(range(4)):
        product=R.one
        for i in range(4): product*=A[i][p[i]]
        inversions=sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))
        det+=(-1)**inversions*product
    expected=8*tt*(1-tt)**3*(1-rr*rr*tt)**3*(1-rr*rr*tt*tt)**3*R.from_expr(P.as_expr())
    assert det==expected, 'the complete determinant coefficient identity failed'
    seed=RB.subs({mu:0,nu:0,r:0,t:s.Rational(1,16)})
    minors=[s.factor(seed[:k,:k].det()) for k in range(1,5)]
    assert all(z>0 for z in minors)
    data={e:int(c) for e,c in P.terms()}
    for axis,(lo,hi) in enumerate([(-1,1),(-1,1),(0,1),(0,1)]):
        data=chart(data,axis,P.degree_list()[axis],lo,hi)
    assert len(data)==1731
    assert min(data.values())==192
    assert data[(0,0,0,0)]==432
    assert all(c>0 for c in data.values())
    table=[]
    for i in range(5):
        row=[]
        for j in range(5):
            vals=[c for e,c in data.items() if e[:2]==(i,j)]
            row.append([len(vals),min(vals) if vals else None])
        table.append(row)
    summary={'status':'AUTHOR_EXACT_PASS_NOT_INDEPENDENT_REVIEW','P_degrees':list(P.degree_list()),'P_nonzero_terms':279,'determinant_coefficient_residual':0,'chart_degrees':[4,4,10,6],'Q_nonzero_terms':len(data),'Q_negative_terms':0,'Q_min_positive':min(data.values()),'Q_constant':data[(0,0,0,0)],'seed_Rbar_leading_minors':list(map(str,minors)),'Q_group_count_and_min':table,'sympy':s.__version__}
    if out is not None:
        out.mkdir(parents=True,exist_ok=True)
        (out/'P.json').write_text(json.dumps({'variables':['mu','nu','r','t'],'terms':[[list(e),int(c)] for e,c in P.terms()]},indent=2))
        (out/'Q.json').write_text(json.dumps({'variables':['X','Y','R','T'],'terms':[[list(e),c] for e,c in sorted(data.items())]},indent=2))
        (out/'summary.json').write_text(json.dumps(summary,indent=2))
    print(json.dumps(summary,indent=2))
    print('ALL EXACT CERTIFICATE CHECKS PASSED')
    print('Elapsed seconds (not part of certificate):',round(time.monotonic()-started,3))
    return summary

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path)
    args=parser.parse_args()
    run(args.out)
