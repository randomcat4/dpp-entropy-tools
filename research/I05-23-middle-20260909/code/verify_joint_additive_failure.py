#!/usr/bin/env python3
from fractions import Fraction as F
from itertools import combinations
import sympy as sp

Q=sp.Rational
A=sp.Matrix([[Q(219,500),-Q(47,1000),Q(73,1000)],[-Q(47,1000),Q(461,1000),Q(23,1000)],[Q(73,1000),Q(23,1000),Q(43,100)]])
C=sp.Matrix([[Q(231,500),Q(1,50),-Q(49,1000)],[Q(1,50),Q(43,100),Q(11,200)],[-Q(49,1000),Q(11,200),Q(3,5)]])
U=sp.Matrix([[Q(7,40),-Q(22,125)],[Q(339,1000),Q(13,250)],[Q(229,500),-Q(231,500)]])
V=sp.Matrix([[Q(141,200),Q(981,1000)],[-Q(343,1000),Q(113,250)],[Q(187,250),Q(577,1000)]])
B=U*V.T
s=Q(9,10)

def subs(n):
    return range(1<<n)

def em(K,mask):
    X=K.copy()
    for i in range(K.rows):
        if not ((mask>>i)&1): X[i,i]-=1
    return X

def ep(K,mask):
    return (-1)**(K.rows-int(mask).bit_count())*em(K,mask).det()

def all_pm(K):
    n=K.rows
    for r in range(1,n+1):
        for S in combinations(range(n),r):
            if K.extract(S,S).det()<=0: return False
    return True

assert B.rank()==2 and all(x!=0 for x in B)
assert all_pm(A) and all_pm(sp.eye(3)-A)
assert all_pm(C) and all_pm(sp.eye(3)-C)
MK=B.T*A.inv()*B
MI=B.T*(sp.eye(3)-A).inv()*B
assert all_pm(C-s*MK)
assert all_pm(sp.eye(3)-C-s*MI)

pA=[ep(A,i) for i in subs(3)]
pC=[ep(C,j) for j in subs(3)]
assert all(x>0 for x in pA+pC)
assert sum(pA)==sum(pC)==1

def _atanh_log_iv_unit(x,N=70):
    z=(x-1)/(x+1); zz=z*z; term=z; sm=F(0)
    for k in range(N):
        if k: term*=zz
        sm += term/F(2*k+1)
    center=2*sm; az=abs(z)
    rem=2*(az**(2*N+1))/F(2*N+1)/(1-az*az)
    return center-rem, center+rem

LOG2_IV=_atanh_log_iv_unit(F(2),70)

def log_iv(x,N=70):
    x=F(int(sp.numer(x)),int(sp.denom(x))); k=0; m=x
    while m>2: m/=2; k+=1
    while m<F(1,2): m*=2; k-=1
    lo,hi=_atanh_log_iv_unit(m,N)
    if k>=0: return lo+k*LOG2_IV[0], hi+k*LOG2_IV[1]
    return lo+k*LOG2_IV[1], hi+k*LOG2_IV[0]

def iv_add(a,b): return (a[0]+b[0],a[1]+b[1])
def iv_scale(c,a):
    c=F(c)
    return (c*a[0],c*a[1]) if c>=0 else (c*a[1],c*a[0])

dual=[[-20,-14,-10,9,-26,-9,15,55],[-15,-8,-9,3,-13,4,8,30],[-11,-5,35,16,-21,-23,28,-19],[2,1,20,7,-7,-17,9,-15],[-10,9,-13,-10,14,44,-17,-17],[-8,7,-10,-8,12,33,-13,-13],[36,6,-7,-10,24,-18,-17,-14],[26,4,-6,-7,17,-14,-13,-7]]
assert all(sum(r)==0 for r in dual)
assert all(sum(dual[i][j] for i in range(8))==0 for j in range(8))

P0=(F(0),F(0)); true=(F(0),F(0)); dual_num=(F(0),F(0)); W=(F(0),F(0))
A2=F(0); dual_den=F(0); minq=None
for sm in subs(3):
    GA=U.T*em(A,sm).inv()*U; alpha=GA.det()
    for tm in subs(3):
        GC=V.T*em(C,tm).inv()*V; beta=GC.det()
        a=sp.trace(GA*GC); b=alpha*beta; mu=pA[sm]*pC[tm]
        q=1-s*a+s*s*b
        assert q>0
        minq=q if minq is None or q<minq else minq
        u=q-1; y=s*s*b; lr=log_iv(q)
        phi_rat=4*u*u/q
        phi_iv=iv_add((F(phi_rat),F(phi_rat)),iv_scale(F(2*u),lr))
        P0=iv_add(P0,iv_scale(F(mu),phi_iv))
        psi_iv=iv_add((F(8*u/q),F(8*u/q)),iv_scale(10,lr))
        A2 += F(mu)*F(4*y*y/q)
        W=iv_add(W,iv_scale(F(mu*b),psi_iv))
        one=iv_add(phi_iv,(F(4*y*y/q),F(4*y*y/q)))
        one=iv_add(one,iv_scale(F(y),psi_iv))
        true=iv_add(true,iv_scale(F(mu),one))
        cij=dual[sm][tm]
        dual_num=iv_add(dual_num,iv_scale(cij,psi_iv))
        Patom=F(mu*q)
        dual_den += F(cij*cij)/Patom

assert dual_num[0] > 0
absnum_lo=dual_num[0]
Rdual_lo=absnum_lo*absnum_lo/dual_den
threshold_hi=4*(P0[1]+A2)*(P0[1]+A2)/A2
assert Rdual_lo > threshold_hi
assert true[0] > 0
assert W[1] < 0

print('PR58 additive-criterion obstruction fixture: PASS')
print('rank(B)=2, dense:', all(x!=0 for x in B))
print('s=9/10 legal, min q =', minq)
print('P0 interval approx =', float(P0[0]), float(P0[1]))
print('A2 exact approx =', float(A2))
print('W interval approx =', float(W[0]), float(W[1]))
print("true t^2 I'' interval approx =", float(true[0]), float(true[1]))
print('dual R_add lower bound approx =', float(Rdual_lo))
print('criterion failure threshold upper approx =', float(threshold_hi))
print('strict: R_add >= dual lower > threshold, so joint-additive sufficient margin < 0')
print("strict: true t^2 I'' > 0, so entropy curvature H'' < 0 at t=sqrt(9/10)")