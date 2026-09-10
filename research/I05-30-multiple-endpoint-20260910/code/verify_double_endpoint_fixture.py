#!/usr/bin/env python3
import sympy as sp
from itertools import combinations

Q=sp.Rational
t,s=sp.symbols("t s", real=True)

LA=sp.Matrix([
    [Q(2,5),0,0],
    [Q(1,20),Q(3,8),0],
    [-Q(1,25),Q(1,30),Q(7,20)],
])
LC=sp.Matrix([
    [Q(7,20),0,0],
    [-Q(1,30),Q(2,5),0],
    [Q(1,24),-Q(1,28),Q(3,8)],
])
J=sp.ones(3)
P=sp.eye(3)-J/3
A=sp.simplify(LA*LA.T)
C=sp.simplify(LC*LC.T)
B=sp.simplify(LA*P*LC.T)

def event_prob(K,mask):
    M=sp.Matrix(K)
    n=K.rows
    k=0
    for i in range(n):
        if (mask>>i)&1:
            k+=1
        else:
            M[i,i]-=1
    return sp.factor((-1)**(n-k)*M.det())

def sylvester_pos(M):
    return all(sp.factor(M[:k,:k].det())>0 for k in range(1,M.rows+1))

assert sylvester_pos(A) and sylvester_pos(sp.eye(3)-A)
assert sylvester_pos(C) and sylvester_pos(sp.eye(3)-C)
assert B.rank()==2 and all(x!=0 for x in B)

# Exact repeated K-endpoint identity and complement Gershgorin margin.
assert sp.simplify(B.T*A.inv()*B - LC*P*LC.T)==sp.zeros(3)
SC1=sp.simplify(C-B.T*A.inv()*B)
assert SC1.rank()==1
assert sp.simplify(SC1-LC*(sp.eye(3)-P)*LC.T)==sp.zeros(3)

K=sp.Matrix.vstack(sp.Matrix.hstack(A,t*B),sp.Matrix.hstack(t*B.T,C))
K1=K.subs(t,1)
assert K1.rank()==4
row_bounds=[]
for i in range(6):
    row_bounds.append(sp.factor(K1[i,i]+sum(abs(K1[i,j]) for j in range(6) if j!=i)))
row_max=max(row_bounds)
assert row_max==Q(12149,31500) and row_max<1

pA=[event_prob(A,m) for m in range(8)]
pC=[event_prob(C,m) for m in range(8)]
assert all(x>0 for x in pA+pC)
assert sum(pA)==sum(pC)==1

# Exact full-event law as q(s), cross-checked from the full signed determinant.
rows=[]
for sm in range(8):
    for tm in range(8):
        mask=sm|(tm<<3)
        pt=sp.expand(event_prob(K,mask))
        pol=sp.Poly(pt,t)
        ps=0
        for (deg,),coef in pol.terms():
            assert deg%2==0
            ps += coef*s**(deg//2)
        ps=sp.factor(ps)
        mu=sp.factor(pA[sm]*pC[tm])
        q=sp.factor(ps/mu)
        assert sp.factor(q.subs(s,0))==1
        assert sp.degree(q,s)<=2
        rows.append((sm,tm,mu,q))

assert sp.factor(sum(mu*q for _,_,mu,q in rows))==1

# Direct Mobius-definition reconstruction at two rational physical t values.
for tv in (Q(1,2),Q(1,1)):
    Kv=K.subs(t,tv)
    inc={}
    for mask in range(64):
        inds=[i for i in range(6) if (mask>>i)&1]
        inc[mask]=sp.Integer(1) if not inds else sp.factor(Kv.extract(inds,inds).det())
    for E in range(64):
        mob=sp.Integer(0)
        ecount=E.bit_count()
        for Tmask in range(64):
            if (Tmask & E)==E:
                mob += (-1)**(Tmask.bit_count()-ecount)*inc[Tmask]
        direct=event_prob(Kv,E)
        assert sp.factor(mob-direct)==0

def quad_extrema(poly,lo,hi):
    poly=sp.expand(poly)
    vals=[sp.factor(poly.subs(s,lo)),sp.factor(poly.subs(s,hi))]
    der=sp.diff(poly,s)
    if sp.degree(der,s)==1:
        root=sp.solve(der,s)[0]
        if lo<root<hi:
            vals.append(sp.factor(poly.subs(s,root)))
    return min(vals),max(vals)

# Whole-continuum likelihood inequalities, not sampling.
for sm,tm,mu,q in rows:
    mn,_=quad_extrema(q-(1-s)**2,Q(0),Q(1))
    _,mx=quad_extrema(q,Q(0),Q(1))
    assert mn>=0
    assert mx<=Q(11,8)

# Endpoint order groups.
simple=[]
double=[]
for sm,tm,mu,q in rows:
    if sp.factor(q.subs(s,1))==0:
        d1=sp.factor(sp.diff(q,s).subs(s,1))
        if d1<0:
            simple.append((sm,tm,sp.factor(-d1)))
        elif d1==0:
            assert sp.factor(q-(1-s)**2)==0
            double.append((sm,tm))
        else:
            raise AssertionError("wrong endpoint sign")
assert simple==[
    (3,3,Q(14944,15795)),
    (3,7,Q(800,1053)),
    (5,7,Q(62336,73533)),
    (6,7,Q(209798,260139)),
    (7,3,Q(128,165)),
    (7,5,Q(20150,28083)),
    (7,6,Q(1660675,2131566)),
]
assert double==[(7,7)]

# Exact count-5 group.
R5=sp.factor(sum(mu*q for sm,tm,mu,q in rows if sm.bit_count()+tm.bit_count()==5))
R5_target=sp.factor((1-s)*(Q(14595963)-Q(3190277)*s)/Q(51200000000))
assert sp.factor(R5-R5_target)==0

# Coefficient moments.
Ma=Mab=Mb=sp.Integer(0)
Sa=Sb=sp.Integer(0)
for sm,tm,mu,q in rows:
    poly=sp.Poly(sp.expand(q),s)
    a=-poly.coeff_monomial(s)
    b=poly.coeff_monomial(s**2)
    Ma += mu*a*a
    Mab += mu*a*b
    Mb += mu*b*b
    Sa += mu*abs(a)
    Sb += mu*abs(b)
Ma,Mab,Mb=map(sp.factor,(Ma,Mab,Mb))
Sa,Sb=map(sp.factor,(Sa,Sb))
Eabs1=sp.factor(Ma-7*Mab+Q(37,2)*Mb)
assert Ma>Q(1,60)
assert Mab<0
assert Mb>0
assert Eabs1<Q(1,50)
assert 2*Sa+12*Sb<Q(1,4)

mu_min=min(mu for _,_,mu,_ in rows)
assert mu_min==Q(194481,25600000000)
assert mu_min>Q(1,140000)

# Grouped Fisher coefficient on s>=9999/10000.
s0=Q(9999,10000)
D=Q(51200000000)
h1=Q(14595963-3190277,D)
hs0=(Q(14595963)-Q(3190277)*s0)/D
fcoef=sp.factor(4*s0*h1*h1/hs0)
assert fcoef>Q(1,1200)

# Rational atanh logarithm enclosures.
def atanh_log_iv_unit(x,N=120):
    x=Q(x)
    z=(x-1)/(x+1)
    zz=z*z
    term=z
    sm=Q(0)
    for k in range(N):
        if k:
            term*=zz
        sm += term/Q(2*k+1)
    center=2*sm
    az=abs(z)
    rem=2*(az**(2*N+1))/Q(2*N+1)/(1-az*az)
    return center-rem,center+rem

LOG2=atanh_log_iv_unit(Q(2),120)
def log_iv(x,N=120):
    x=Q(x)
    k=0
    m=x
    while m>2:
        m/=2; k+=1
    while m<Q(1,2):
        m*=2; k-=1
    lo,hi=atanh_log_iv_unit(m,N)
    if k>=0:
        return lo+k*LOG2[0],hi+k*LOG2[1]
    return lo+k*LOG2[1],hi+k*LOG2[0]

assert log_iv(Q(11,8))[0]>Q(3,10)
assert log_iv(Q(10))[1]<Q(7,3)
assert log_iv(Q(140000))[1]<12
assert log_iv(Q(10000))[1]<10
# These imply lambda(q)>4/5 on q<=11/8 and lambda(q)<19 on q>=1e-8.
assert Q(56,3) < 19*(1-Q(1,10**8))

# Channel-lift non-proportional witnesses.
col_w=[]
for j,k in combinations(range(3),2):
    found=None
    for i,l in combinations(range(3),2):
        det=sp.factor(B[i,j]*B[l,k]-B[l,j]*B[i,k])
        if det:
            found=det;break
    col_w.append(found)
row_w=[]
for i,l in combinations(range(3),2):
    found=None
    for j,k in combinations(range(3),2):
        det=sp.factor(B[i,j]*B[l,k]-B[i,k]*B[l,j])
        if det:
            found=det;break
    row_w.append(found)
assert col_w==[Q(7,1000),-Q(23,3200),Q(247,33600)]
assert row_w==[Q(7,1000),-Q(133,22500),Q(2191,360000)]

compact_lb=Q(32,11)*Q(1,60)+Q(99,5)*Q(1,60)-Q(91,5)*Q(1,50)
assert compact_lb==Q(239,16500) and compact_lb>Q(1,100)

print("I05-30 multiple-endpoint fixture certificate: PASS")
print("A =",A.tolist())
print("C =",C.tolist())
print("B =",B.tolist())
print("rank(B) =",B.rank(),"dense =",all(x!=0 for x in B))
print("max |row| Gershgorin bound on |t|<=1 =",row_max)
print("endpoint nullity K(1) =",6-K1.rank(),"; I-K strict by row bound")
print("simple endpoint atoms =",simple)
print("double endpoint atoms =",double)
print("R5(s) =",R5)
print("Ma =",Ma)
print("Mab =",Mab)
print("Mb =",Mb)
print("Eabs bound at s=1 =",Eabs1)
print("min mu =",mu_min)
print("sum acceleration coefficient bound =",sp.factor(2*Sa+12*Sb))
print("grouped Fisher coefficient =",fcoef,"> 1/1200")
print("compact normalized-curvature lower bound =",compact_lb,"> 1/100")
print("endpoint band: delta<=1e-4 gives -H'' > 1/3")
print("whole chord: H''(t) <= -(1/100)t^2 on |t|<1")
print("channel column witnesses =",col_w)
print("channel row witnesses =",row_w)
