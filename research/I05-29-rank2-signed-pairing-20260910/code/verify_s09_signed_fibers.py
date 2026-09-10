#!/usr/bin/env python3
from fractions import Fraction as F
from itertools import combinations
import sys
import sympy as sp

sys.set_int_max_str_digits(100000)
Q=sp.Rational

A=sp.Matrix([
 [Q(219,500),-Q(47,1000), Q(73,1000)],
 [-Q(47,1000),Q(461,1000),Q(23,1000)],
 [Q(73,1000),Q(23,1000),Q(43,100)]])
C=sp.Matrix([
 [Q(231,500),Q(1,50),-Q(49,1000)],
 [Q(1,50),Q(43,100),Q(11,200)],
 [-Q(49,1000),Q(11,200),Q(3,5)]])
U=sp.Matrix([
 [Q(7,40),-Q(22,125)],
 [Q(339,1000),Q(13,250)],
 [Q(229,500),-Q(231,500)]])
V=sp.Matrix([
 [Q(141,200),Q(981,1000)],
 [-Q(343,1000),Q(113,250)],
 [Q(187,250),Q(577,1000)]])
B=U*V.T
s=Q(9,10)


def ff(z):
    return F(int(sp.numer(z)),int(sp.denom(z)))

def em(K,mask):
    X=K.copy()
    for i in range(K.rows):
        if not ((mask>>i)&1):
            X[i,i]-=1
    return X

def ep(K,mask):
    return (-1)**(K.rows-int(mask).bit_count())*em(K,mask).det()

def all_pm(K):
    n=K.rows
    for r in range(1,n+1):
        for S in combinations(range(n),r):
            if K.extract(S,S).det()<=0:
                return False
    return True

assert B.rank()==2 and all(x!=0 for x in B)
assert all_pm(A) and all_pm(sp.eye(3)-A)
assert all_pm(C) and all_pm(sp.eye(3)-C)
MK=B.T*A.inv()*B
MI=B.T*(sp.eye(3)-A).inv()*B
assert all_pm(C-s*MK)
assert all_pm(sp.eye(3)-C-s*MI)

pA=[ff(ep(A,i)) for i in range(8)]
pC=[ff(ep(C,j)) for j in range(8)]
assert all(x>0 for x in pA+pC)
assert sum(pA)==sum(pC)==1

# Pure-rational outward logarithm enclosure.
def atanh_log_iv_unit(x,N=90):
    x=F(x)
    z=(x-1)/(x+1)
    zz=z*z
    term=z
    sm=F(0)
    for k in range(N):
        if k:
            term*=zz
        sm += term/F(2*k+1)
    center=2*sm
    az=abs(z)
    rem=2*(az**(2*N+1))/F(2*N+1)/(1-az*az)
    return center-rem,center+rem

LOG2_IV=atanh_log_iv_unit(F(2),90)

def log_iv(x,N=90):
    x=F(x)
    k=0
    m=x
    while m>2:
        m/=2; k+=1
    while m<F(1,2):
        m*=2; k-=1
    lo,hi=atanh_log_iv_unit(m,N)
    if k>=0:
        return lo+k*LOG2_IV[0],hi+k*LOG2_IV[1]
    return lo+k*LOG2_IV[1],hi+k*LOG2_IV[0]

def iv_add(a,b):
    return a[0]+b[0],a[1]+b[1]

def iv_scale(c,a):
    c=F(c)
    return (c*a[0],c*a[1]) if c>=0 else (c*a[1],c*a[0])

def L_iv(q1,q2):
    if q1==q2:
        return F(1,q1),F(1,q1)
    l1=log_iv(q1); l2=log_iv(q2)
    d=q1-q2
    return iv_scale(F(1,d),(l1[0]-l2[1],l1[1]-l2[0]))

def ratio_F_iv(q1,q2,r):
    L=L_iv(q1,q2)
    rat=F(2)*(1+r*r)/(q1+q2)+r*F(4)/(q1*q2)
    return iv_add(iv_scale(1+5*r,L),(rat,rat))

def integrand_iv(q,u,y):
    # Exact square completion:
    # 4(u+y)^2/q + 2(u+5y) log q.
    rat=F(4)*(u+y)*(u+y)/q
    return iv_add((rat,rat),iv_scale(F(2)*(u+5*y),log_iv(q)))

# (a,b,q,u,y), all exact rational.
data={}
minq=None
for sm in range(8):
    GA=U.T*em(A,sm).inv()*U
    alpha=GA.det()
    for tm in range(8):
        GC=V.T*em(C,tm).inv()*V
        beta=GC.det()
        a=sp.trace(GA*GC)
        b=alpha*beta
        q=1-s*a+s*s*b
        assert q>0
        vals=tuple(ff(z) for z in (a,b,q,q-1,s*s*b))
        data[(sm,tm)]=vals
        minq=vals[2] if minq is None or vals[2]<minq else minq

# Verify fixed-margin coefficient cancellations exactly on every fiber.
for sm in range(8):
    assert sum(pC[tm]*data[(sm,tm)][0] for tm in range(8))==0
    assert sum(pC[tm]*data[(sm,tm)][1] for tm in range(8))==0
for tm in range(8):
    assert sum(pA[sm]*data[(sm,tm)][0] for sm in range(8))==0
    assert sum(pA[sm]*data[(sm,tm)][1] for sm in range(8))==0

# Cheap falsification of the PR80 ratio-cone on both conditional orientations.
left_bad=[]
right_bad=[]
for sm in range(8):
    for t1,t2 in combinations(range(8),2):
        q1,u1,y1=data[(sm,t1)][2:]
        q2,u2,y2=data[(sm,t2)][2:]
        du=u1-u2
        if du:
            r=(y1-y2)/du
            fi=ratio_F_iv(q1,q2,r)
            if fi[1]<0:
                left_bad.append((fi,sm,t1,t2,r,q1,q2))
for tm in range(8):
    for s1,s2 in combinations(range(8),2):
        q1,u1,y1=data[(s1,tm)][2:]
        q2,u2,y2=data[(s2,tm)][2:]
        du=u1-u2
        if du:
            r=(y1-y2)/du
            fi=ratio_F_iv(q1,q2,r)
            if fi[1]<0:
                right_bad.append((fi,tm,s1,s2,r,q1,q2))
assert len(left_bad)==75
assert len(right_bad)==66
worstL=min(left_bad,key=lambda z: z[0][0])
worstR=min(right_bad,key=lambda z: z[0][0])
assert worstL[0][1]<0 and worstR[0][1]<0

# Exact algebra behind the corrected strictness clause: for every event pair and x=u,y,
# q q'(q+q') times the Cauchy slack equals (q'x+qx')^2.
for fixed_left in (True,False):
    for outer in range(8):
        for i,j in combinations(range(8),2):
            z1=data[(outer,i)] if fixed_left else data[(i,outer)]
            z2=data[(outer,j)] if fixed_left else data[(j,outer)]
            q1,u1,y1=z1[2:]
            q2,u2,y2=z2[2:]
            for x1,x2 in ((u1,u2),(y1,y2)):
                lhs=x1*x1/q1+x2*x2/q2-(x1-x2)**2/(q1+q2)
                rhs=(q2*x1+q1*x2)**2/(q1*q2*(q1+q2))
                assert lhs==rhs and lhs>=0

# Complete signed one-event integrand and conditional fiber averages.
negative_events=[]
left_fibers=[]
right_fibers=[]
for sm in range(8):
    iv=(F(0),F(0))
    for tm in range(8):
        q,u,y=data[(sm,tm)][2:]
        one=integrand_iv(q,u,y)
        if one[1]<0:
            negative_events.append((sm,tm,one))
        iv=iv_add(iv,iv_scale(pC[tm],one))
    assert iv[0]>0
    left_fibers.append(iv)
for tm in range(8):
    iv=(F(0),F(0))
    for sm in range(8):
        q,u,y=data[(sm,tm)][2:]
        iv=iv_add(iv,iv_scale(pA[sm],integrand_iv(q,u,y)))
    assert iv[0]>0
    right_fibers.append(iv)

assert [(x[0],x[1]) for x in negative_events]==[(0,6),(1,5),(2,5),(3,0)]

globalL=(F(0),F(0)); globalR=(F(0),F(0))
for sm in range(8):
    globalL=iv_add(globalL,iv_scale(pA[sm],left_fibers[sm]))
for tm in range(8):
    globalR=iv_add(globalR,iv_scale(pC[tm],right_fibers[tm]))
assert globalL==globalR and globalL[0]>0

print('I05-29 s=9/10 signed-fiber certificate: PASS')
print('rank(B)=2, dense:',all(x!=0 for x in B))
print('strict legal, min q approx:',float(minq))
print('left unordered ratio pairs: 224; rigorously negative F:',len(left_bad))
print('right unordered ratio pairs: 224; rigorously negative F:',len(right_bad))
print('worst left F enclosure approx:',float(worstL[0][0]),float(worstL[0][1]),'fiber/pair=',worstL[1:4])
print('worst right F enclosure approx:',float(worstR[0][0]),float(worstR[0][1]),'fiber/pair=',worstR[1:4])
print('negative complete one-event integrands:',[(x[0],x[1]) for x in negative_events])
print('left fiber curvature lower/upper approximations:')
for i,iv in enumerate(left_fibers): print(i,float(iv[0]),float(iv[1]))
print('right fiber curvature lower/upper approximations:')
for i,iv in enumerate(right_fibers): print(i,float(iv[0]),float(iv[1]))
print("global true t^2 I'' enclosure approx:",float(globalL[0]),float(globalL[1]))
print('strict: every left and right complete conditional fiber average is positive')
print('strict: ratio-cone fails on both orientations; this is a method failure, not entropy failure')
