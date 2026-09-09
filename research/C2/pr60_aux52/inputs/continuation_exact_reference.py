"""Exact post-checkpoint obstruction and entropy checks (author, not independent).
All log bounds are rational; no float is used in the acceptance tests.
"""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
import json
import argparse
import sympy as s

K=s.Matrix([[s.Rational(11,100),0,s.Rational(33,500)],
 [0,s.Rational(1,200),s.Rational(3,1000)],
 [s.Rational(33,500),s.Rational(3,1000),s.Rational(199,200)]])
D=s.Matrix([[0,-1,0],[-1,-s.Rational(1,50),s.Rational(2,25)],[0,s.Rational(2,25),0]])
C=K-s.diag(*K.diagonal())
N=60

def frac(q):
    q=s.Rational(q);return F(int(q.p),int(q.q))

def add(I,J):return I[0]+J[0],I[1]+J[1]
def scale(c,I):return (c*I[0],c*I[1]) if c>=0 else (c*I[1],c*I[0])

def log_reduced(y):
    assert F(1)<=y<=F(2)
    w=(y-1)/(y+1);w2=w*w;power=w;total=F(0)
    for j in range(N):
        total+=2*power/(2*j+1);power*=w2
    error=2*power/((2*N+1)*(1-w2))
    return total,total+error

LOG2=log_reduced(F(2))
def log_interval(q):
    q=F(q);assert q>0
    m=0
    while q<1:q*=2;m-=1
    while q>=2:q/=2;m+=1
    return add(scale(m,LOG2),log_reduced(q))

def outward(I,digits=35):
    mult=10**digits
    lo=(I[0]*mult).numerator//(I[0]*mult).denominator
    a=I[1]*mult;hi=-((-a.numerator)//a.denominator)
    def text(n):
        sig='-' if n<0 else '';n=abs(n)
        return sig+str(n//mult)+'.'+str(n%mult).zfill(digits)
    return [text(lo),text(hi)]

def atoms(A):
    p=[]
    for S in range(8):
        value=0
        for T in range(8):
            if T&S==S:
                inds=[i for i in range(3) if T>>i&1]
                value+=(-1)**((T^S).bit_count())*(A.extract(inds,inds).det() if inds else 1)
        p.append(s.expand(value))
    return p

def legal(A):
    vals=[]
    for B in (A,s.eye(3)-A):
        vals.extend(B[:k,:k].det() for k in (1,2,3))
    assert all(q>0 for q in vals)
    return list(map(str,vals))

def entropy(A):
    I=(F(0),F(0))
    for p in atoms(A):
        p=frac(p);assert p>0;I=add(I,scale(-p,log_interval(p)))
    return I

def run(out=None):
    e,d=s.symbols('e d')
    polys=atoms(K+e*D+d*C)
    jets=[];B=(F(0),F(0));M=(F(0),F(0))
    for P in polys:
        p,a,b,c,f,g=[frac(s.diff(P,e,ne,d,nd).subs({e:0,d:0})) for ne,nd in ((0,0),(1,0),(2,0),(0,1),(1,1),(2,1))]
        jets.append([str(q) for q in (p,a,b,c,f,g)])
        logp=log_interval(p)
        B=add(B,add((a*a/p,a*a/p),scale(b,logp)))
        rational=2*a*f/p-a*a*c/(p*p)+b*c/p
        M=add(M,add((rational,rational),scale(g,logp)))
    assert M[1]<0 and B[0]>0
    tau=s.Rational(1,100000)
    legality={'minus':legal(K-tau*D),'center':legal(K),'plus':legal(K+tau*D)}
    J=add(scale(F(1,2),add(entropy(K-tau*D),entropy(K+tau*D))),scale(-1,entropy(K)))
    assert J[1]<0
    radial_legality={'999/1000':legal(K-s.Rational(1,1000)*C),'1001/1000':legal(K+s.Rational(1,1000)*C)}
    b0=K[0,2];c0=K[1,2];x=K[0,0];y=K[1,1];z=K[2,2]
    rK=s.factor(z/(b0*b0/x+c0*c0/y));rI=s.factor((1-z)/(b0*b0/(1-x)+c0*c0/(1-y)))
    radius2=min(rK,rI);assert radius2>1
    p=atoms(K);ratio=s.factor(p[7]*p[1]*p[2]*p[4]/(p[0]*p[3]*p[5]*p[6]));assert ratio>1
    res={'status':'AUTHOR_EXACT_PASS_NOT_INDEPENDENT_REVIEW','claim':'fixed-diagonal radial Hessian monotonicity fails, not entropy concavity',
         'K':[[str(x) for x in row] for row in K.tolist()], 'D':[[str(x) for x in row] for row in D.tolist()],
         'C':[[str(x) for x in row] for row in C.tolist()], 'event_order':['0','1','2','12','3','13','23','123'],
         'jet_columns':['p','p_e','p_ee','p_d','p_ed','p_eed'],'jets':jets,
         'M_D_interval':outward(M),'minus_H_DD_interval':outward(B),'jensen_Delta_interval':outward(J),
         'tau':str(tau),'symmetric_log_tail_N':N,'radial_legal_radius_squared':str(radius2),
         'radial_endpoint_checks':radial_legality,'jensen_three_kernel_checks':legality,'exp_Lambda':str(ratio)}
    if out:
        out.mkdir(parents=True,exist_ok=True);(out/'continuation_summary.json').write_text(json.dumps(res,indent=2))
    print(json.dumps(res,indent=2));print('ALL POST-CHECKPOINT EXACT CHECKS PASSED')
    return res

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--out',type=Path);args=parser.parse_args();run(args.out)
