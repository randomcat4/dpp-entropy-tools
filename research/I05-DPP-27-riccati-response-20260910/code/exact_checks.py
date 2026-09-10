#!/usr/bin/env python3
"""Bounded author checks for the fixed two-harmonic DPP Riccati response.
Standard library only. All proof assertions use exact Fraction arithmetic.
This is not an independent review or a continuum curvature computation.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product, permutations
import json, platform, sys, time
from pathlib import Path
from datetime import datetime, timezone

class Jet:
    """Value, first derivative, second derivative (not Taylor coefficients)."""
    __slots__ = ('v', 'd', 'dd')
    def __init__(self, v=0, d=0, dd=0):
        self.v, self.d, self.dd = F(v), F(d), F(dd)
    @staticmethod
    def cast(a): return a if isinstance(a, Jet) else Jet(a)
    def __add__(self, a):
        a = self.cast(a)
        return Jet(self.v+a.v, self.d+a.d, self.dd+a.dd)
    __radd__ = __add__
    def __neg__(self): return Jet(-self.v, -self.d, -self.dd)
    def __sub__(self, a): return self + (-self.cast(a))
    def __rsub__(self, a): return self.cast(a) + (-self)
    def __mul__(self, a):
        a = self.cast(a)
        return Jet(self.v*a.v, self.d*a.v+self.v*a.d,
                   self.dd*a.v+2*self.d*a.d+self.v*a.dd)
    __rmul__ = __mul__
    def inv(self):
        if self.v == 0: raise ZeroDivisionError('zero jet base')
        return Jet(1/self.v, -self.d/self.v**2,
                   2*self.d**2/self.v**3-self.dd/self.v**2)
    def __truediv__(self, a): return self*self.cast(a).inv()
    def __eq__(self, a):
        a = self.cast(a)
        return (self.v,self.d,self.dd)==(a.v,a.d,a.dd)
    def record(self): return [str(self.v),str(self.d),str(self.dd)]


def tr(A): return [list(x) for x in zip(*A)]
def mm(A,B):
    return [[sum(A[i][k]*B[k][j] for k in range(len(B)))
             for j in range(len(B[0]))] for i in range(len(A))]
def det2(A): return A[0][0]*A[1][1]-A[0][1]*A[1][0]
def inv2(A):
    d=det2(A)
    return [[A[1][1]/d,-A[0][1]/d],[-A[1][0]/d,A[0][0]/d]]
def matrix_layer(A,k):
    return [[(a.v,a.d,a.dd)[k] for a in row] for row in A]
def spectral_bound(A,b):
    for sg in (-1,1):
        B=[[b-sg*A[0][0],-sg*A[0][1]],[-sg*A[1][0],b-sg*A[1][1]]]
        assert B[0][0]>=0 and B[1][1]>=0 and det2(B)>=0

def step(Q,t,alpha):
    q=t/16; E=[[Jet(F(1,8)),Jet()],[q,Jet(F(1,8))]]
    a,b=alpha
    M=[[Jet(F(a,2))-Q[0][0],q-Q[0][1]],
       [q-Q[1][0],Jet(F(b,2))-Q[1][1]]]
    g=a*b*det2(M)
    return g,mm(mm(E,inv2(M)),tr(E))

def determinant(A):
    n=len(A)
    if n==0: return Jet(1)
    result=Jet()
    for p in permutations(range(n)):
        sg=(-1)**sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))
        term=Jet(sg)
        for i,j in enumerate(p):
            term=term*A[i][j]
            if term==0: break
        result+=term
    return result

def kernel(t,n):
    return [[Jet(F(1,2)) if i==j else t/16 if abs(i-j)==1
             else Jet(F(1,8)) if abs(i-j)==2 else Jet()
             for j in range(n)] for i in range(n)]

def mobius_events(t,n):
    K=kernel(t,n); out=[]
    for mask in range(1<<n):
        ii=[i for i in range(n) if (mask>>i)&1]
        out.append(determinant([[K[i][j] for j in ii] for i in ii]))
    for bit in range(n):
        for mask in range(1<<n):
            if not ((mask>>bit)&1): out[mask]-=out[mask|(1<<bit)]
    return out

def run():
    start=time.monotonic(); utc=datetime.now(timezone.utc).isoformat()
    k=F(34,81); beta=F(4363,5184); r=F(32,9)
    e2=F(17,512); e=F(3,16); c=F(1,16); D=F(3,8)
    assert F(9,512)*F(9,1024)-F(3,256)**2==F(9,524288)>0
    assert e2*r==F(17,144)<F(1,8)
    assert e2*r*r==k<1
    assert k+D*F(9,8)==beta<1
    assert F(130,1024)<F(3,8)**2
    j=F(1,5); h=F(3,4)
    first=2*c*e*r+k*c
    second=2*c*c*r+4*c*e*r*r*(c+j)+2*e2*r**3*(c+j)**2
    assert j*(1-k)-first==F(7,1080)>0
    assert h*(1-k)-second==F(187,4050)>0
    a=F(1,6); b=F(1,8); P=F(9,4); P_t=F(7,64); P_tt=F(1,32); P_tQ=F(3,8)
    B2=2*D+2*P*k+2*k*r
    Ct=D*P_t/2+a; Ctt=D*P_tt/2+2*P_t*a+b
    mixed=2*c*e*r*r+2*e2*r**3*c
    partial2=2*c*c*r+4*c*e*r*r*c+2*e2*r**3*c*c
    assert first*F(3,2)<a and partial2*F(3,2)<b
    assert mixed<F(1,2)
    assert D*P_tQ/2+P_t*k+P*a+F(1,2)<1
    R1=1/(1-beta); R22=1/(1-k*k); R21=B2*R1*R22
    ch=(a*a+2*Ct*R1*k*a)/2
    cl=(Ctt*R1+2*Ct*R1*R1)/2
    C01=cl+ch*R21; C02=ch*R22; C11=Ct*R1
    assert C01<13 and C02<F(1,8) and C11<F(6,5)
    assert R1/2<F(16,5)
    TQQ=2*k*r; TQQQ=6*k*r*r
    TtQQ=4*c*e*r**3+6*e2*c*r**4
    TttQ=2*c*c*r*r+8*c*c*e*r**3+6*e2*c*c*r**4
    assert TQQ*F(3,10)+mixed<F(3,2)
    assert 2*TQQ*F(3,10)+2*mixed<3
    assert TQQ*F(9,8)+TQQQ*F(9,100)+2*TtQQ*F(3,10)+TttQ<10
    assert TtQQ<5 and TttQ<F(1,2)
    rows=[]; all_matches=0; branch_checks=0; layer_checks=0
    for t0 in (F(1,2),F(5,4),F(3,2)):
        t=Jet(t0,1); nodes=[([],[[Jet(),Jet()],[Jet(),Jet()]],Jet(1))]
        for m in range(1,4):
            new=[]
            for word,Q,p in nodes:
                branches=[(al,*step(Q,t,al)) for al in product((-1,1),repeat=2)]
                assert sum(g for al,g,T in branches)==1
                for i,jj in product(range(2),repeat=2):
                    assert sum(g*T[i][jj] for al,g,T in branches)==0
                assert sum(g*det2(T) for al,g,T in branches)==0
                for al,g,T in branches:
                    assert g.v>=F(81,1024)
                    spectral_bound(matrix_layer(T,0),F(1,8))
                    spectral_bound(matrix_layer(T,1),F(1,5))
                    spectral_bound(matrix_layer(T,2),F(3,4))
                    new.append((list(al)+word,T,p*g)); branch_checks+=1
            nodes=new; n=2*m; probs=mobius_events(t,n)
            assert sum(p for word,Q,p in nodes)==1
            for word,Q,p in nodes:
                mask=sum(1<<i for i,s in enumerate(word) if s==1)
                assert p==probs[mask]
                all_matches+=1
            layer_checks+=1
            rows.append({'t':str(t0),'cells':m,'events':len(nodes),
                         'mass_jet':sum(p for word,Q,p in nodes).record(),
                         'minimum_probability':str(min(p.v for word,Q,p in nodes))})
    outside=[[Jet(1),Jet()],[Jet(),Jet(1)]]
    g,_=step(outside,Jet(1,1),(1,-1))
    assert g.v==F(-191,256)
    return {'status':'AUTHOR_MACHINE_CHECK_PASS_NOT_INDEPENDENT_REVIEW',
            'utc_start':utc,'elapsed_seconds_display_only':time.monotonic()-start,
            'python':sys.version,'platform':platform.platform(),
            'arithmetic':'fractions.Fraction; derivative jets contain exact first/second derivatives',
            'input':{'symbol':'1/2+cos(4*pi*theta)/4+t*cos(2*pi*theta)/8',
                     'theory_interval':['1/2','3/2'],'test_parameters':['1/2','5/4','3/2'],
                     'event_lengths':[2,4,6]},
            'constants':{key:str(val) for key,val in dict(kappa=k,beta=beta,
                branch_lower=F(81,1024),first_jet_margin=j*(1-k)-first,
                second_jet_margin=h*(1-k)-second,B2=B2,Ct=Ct,Ctt=Ctt,
                residual_L1=C01,residual_H2=C02,response_residual_L1=C11).items()},
            'event_value_first_second_jet_matches':all_matches,
            'branch_state_jet_checks':branch_checks,'normalization_layers':layer_checks,
            'weighted_state_and_determinant_identity':'all value/first/second jets checked at every parent',
            'outside_domain_negative_weight':str(g.v),'rows':rows,
            'failure_ledger':[],
            'not_certified':['whole-interval curvature sign','independent review','novelty']}

if __name__=='__main__':
    dest=Path(sys.argv[1]) if len(sys.argv)>1 else None
    try:
        result=run()
    except Exception as exc:
        result={'status':'FAIL','exception':repr(exc)}
        if dest: dest.write_text(json.dumps(result,indent=2)+'\n')
        raise
    text=json.dumps(result,indent=2)+'\n'
    if dest: dest.write_text(text)
    print(text,end='')
