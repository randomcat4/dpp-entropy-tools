#!/usr/bin/env python3
import sympy as sp
from collections import defaultdict

Q=sp.Rational
t,s=sp.symbols('t s', real=True)
J=sp.ones(3)
QQ=J/3
P=sp.eye(3)-QQ
A=Q(1,5)*P+Q(2,5)*QQ
C=Q(4,5)*P+Q(3,5)*QQ
B=Q(2,5)*P


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


def extrema_quad(poly,lo,hi):
    poly=sp.expand(poly)
    vals=[sp.factor(poly.subs(s,lo)),sp.factor(poly.subs(s,hi))]
    der=sp.diff(poly,s)
    if sp.degree(der,s)==1:
        r=sp.solve(der,s)[0]
        if lo<r<hi:
            vals.append(sp.factor(poly.subs(s,r)))
    return min(vals),max(vals)

assert A+C==sp.eye(3)
assert B.rank()==2 and all(x!=0 for x in B)
assert all(A[i,j]!=0 for i in range(3) for j in range(3))
assert all(C[i,j]!=0 for i in range(3) for j in range(3))

# Exact legality and simultaneous multiplicity.
assert sp.simplify(C-B*A.inv()*B - Q(3,5)*QQ)==sp.zeros(3)
assert sp.simplify(A-B*C.inv()*B - Q(2,5)*QQ)==sp.zeros(3)
K=sp.Matrix.vstack(sp.Matrix.hstack(A,t*B),sp.Matrix.hstack(t*B,C))
assert K.subs(t,1).rank()==4
assert (sp.eye(6)-K.subs(t,1)).rank()==4

pA=[event_prob(A,m) for m in range(8)]
pC=[event_prob(C,m) for m in range(8)]
assert all(x>0 for x in pA+pC) and sum(pA)==sum(pC)==1

rows=[]
for sm in range(8):
    for tm in range(8):
        E=sm|(tm<<3)
        pt=sp.expand(event_prob(K,E))
        ps=sp.Integer(0)
        for (deg,),coef in sp.Poly(pt,t).terms():
            assert deg%2==0
            ps += coef*s**(deg//2)
        mu=sp.factor(pA[sm]*pC[tm])
        q=sp.factor(ps/mu)
        poly=sp.Poly(sp.expand(q),s)
        a=-poly.coeff_monomial(s)
        b=poly.coeff_monomial(s**2)
        assert poly.coeff_monomial(1)==1 and sp.degree(q,s)<=2
        rows.append((sm,tm,mu,a,b,q))
assert sp.factor(sum(mu*q for _,_,mu,_,_,q in rows))==1

# Inclusion/Mobius definition check at two exact physical points.
for tv in (Q(1,2),Q(1)):
    Kv=K.subs(t,tv)
    inc=[]
    for mask in range(64):
        inds=[i for i in range(6) if (mask>>i)&1]
        inc.append(sp.Integer(1) if not inds else sp.factor(Kv.extract(inds,inds).det()))
    for E in range(64):
        mob=sp.Integer(0)
        for Tm in range(64):
            if (Tm&E)==E:
                mob += (-1)**(Tm.bit_count()-E.bit_count())*inc[Tm]
        assert sp.factor(mob-event_prob(Kv,E))==0

# Compress the 64 observed complete events by exact q-type.
types=defaultdict(lambda:[sp.Integer(0),0,None,None])
for sm,tm,mu,a,b,q in rows:
    types[q][0]+=mu
    types[q][1]+=1
    types[q][2]=a
    types[q][3]=b
assert len(types)==13
assert sp.factor(sum(v[0] for v in types.values()))==1

# Expected exact type table as a set of (q,weight,multiplicity).
expected={
    (sp.factor((16*s**2+248*s+361)/361),Q(722,46875),6),
    (sp.factor((4*s+1)*(4*s+361)/361),Q(361,46875),3),
    (sp.factor((4*s+1)**2),Q(4,15625),1),
    (sp.factor((64*s**2-223*s+784)/784),Q(6272,46875),6),
    (sp.factor((8*s**2+84*s+133)/133),Q(4256,46875),12),
    (sp.factor((s+4)*(16*s+49)/196),Q(3136,46875),3),
    (sp.factor((s+4)**2/16),Q(2304,15625),1),
    (sp.factor((s-1)*(8*s-133)/133),Q(2128,46875),6),
    (sp.factor((s-1)**2),Q(192,15625),2),
    (sp.factor(-(4*s-19)*(4*s+1)/19),Q(76,15625),6),
    (sp.factor(-(s+4)*(2*s-7)/28),Q(5376,15625),6),
    (sp.factor(-(s-1)*(8*s+7)/7),Q(224,15625),6),
    (sp.factor(-(s-1)*(s+19)/19),Q(1824,15625),6),
}
actual={(q,sp.factor(v[0]),v[1]) for q,v in types.items()}
assert actual==expected

# Endpoint vanishing orders and cardinality groups.
simple=double=0
for sm,tm,mu,a,b,q in rows:
    if q.subs(s,1)==0:
        if sp.diff(q,s).subs(s,1)!=0:
            simple+=1
        else:
            assert sp.factor(q-(1-s)**2)==0
            double+=1
assert (simple,double)==(18,2)
R={}
for k in range(7):
    R[k]=sp.factor(sum(mu*q for sm,tm,mu,a,b,q in rows if sm.bit_count()+tm.bit_count()==k))
assert R[0]==R[6]==Q(96,15625)*(1-s)**2
assert R[1]==R[5]==Q(16,15625)*(1-s)*(11*s+64)

# PR94 grouped-channel noncoverage: every row/column pair has a nonzero 2x2 witness.
for j in range(3):
    for k in range(j+1,3):
        assert any(sp.factor(B[i,j]*B[l,k]-B[l,j]*B[i,k])!=0 for i in range(3) for l in range(i+1,3))
for i in range(3):
    for l in range(i+1,3):
        assert any(sp.factor(B[i,j]*B[l,k]-B[i,k]*B[l,j])!=0 for j in range(3) for k in range(j+1,3))

# Universal observed-event bound q >= (1-s)^2 and exact acceleration coefficient budget.
Sa=Sb=sp.Integer(0)
for sm,tm,mu,a,b,q in rows:
    mn,_=extrema_quad(q-(1-s)**2,Q(0),Q(1))
    assert mn>=0
    Sa+=mu*abs(a); Sb+=mu*abs(b)
acc=sp.factor(2*Sa+12*Sb)
assert acc==Q(101408,46875) and acc<Q(11,5)
assert min(mu for _,_,mu,_,_,_ in rows)==Q(4,15625)>Q(1,4000)

# Compact type lower bound helper.
def compact_certificate(lo,hi):
    good=sp.Integer(0)
    bad=[]
    for q,(w,count,a,b) in types.items():
        z=sp.expand((a-s*b)*(a-6*s*b))
        zmin,_=extrema_quad(z,lo,hi)
        v2=sp.expand((a-2*s*b)**2)
        vmin,_=extrema_quad(v2,lo,hi)
        qmin,qmax=extrema_quad(q,lo,hi)
        if zmin>=0:
            good += sp.factor(4*w*vmin/qmax)
        else:
            bad.append((q,w,zmin,qmin))
    return sp.factor(good),bad

good1,bad1=compact_certificate(Q(0),Q(9,10))
assert good1>Q(19,20) and len(bad1)==4
# Match exact negative minima and use the lambda caps stated in the proof.
byq1={sp.factor(q):(w,zmin,qmin) for q,w,zmin,qmin in bad1}
qD=sp.factor((1-s)**2)
qE=sp.factor(-(s-1)*(8*s+7)/7)
qN=sp.factor((64*s**2-223*s+784)/784)
qL=sp.factor(-(4*s-19)*(4*s+1)/19)
assert byq1[qD][1]==-Q(187,50) and byq1[qD][2]==Q(1,100)
assert byq1[qE][1]==-Q(25,1176)
assert byq1[qN][1]==-Q(506951,15366400)
assert byq1[qL][1]==-Q(20736,9025)
# On the actual negative-z regions: qE>=1, qN>4/5, qL>1.
assert qE.subs(s,Q(1,8))==1 and qE.subs(s,Q(1,48))>1
assert qN.subs(s,Q(9,10))>Q(4,5)
assert qL.subs(s,Q(3,4))>1
neg1=(2*Q(192,15625)*Q(187,50)*5
      +2*Q(224,15625)*Q(25,1176)
      +2*Q(6272,46875)*Q(506951,15366400)*Q(5,4)
      +2*Q(76,15625)*Q(20736,9025))
assert sp.factor(neg1)==Q(717986643,1454687500) and neg1<Q(1,2)

good2,bad2=compact_certificate(Q(9,10),Q(99,100))
assert good2>8 and len(bad2)==3
byq2={sp.factor(q):(w,zmin,qmin) for q,w,zmin,qmin in bad2}
assert byq2[qD][1]==-Q(19897,5000) and byq2[qD][2]==Q(1,10000)
assert byq2[qN][1]==-Q(15680639,384160000) and byq2[qN][2]>Q(3,4)
assert byq2[qL][1]==-Q(808704,225625) and byq2[qL][2]>1
neg2=(2*Q(192,15625)*Q(19897,5000)*10
      +2*Q(6272,46875)*Q(15680639,384160000)*Q(4,3)
      +2*Q(76,15625)*Q(808704,225625))
assert sp.factor(neg2)==Q(223389457,218203125) and neg2<Q(11,10)

# Rational atanh logarithm enclosure for the only coarse log claims.
def atanh_log_iv_unit(x,N=100):
    x=Q(x); z=(x-1)/(x+1); zz=z*z; term=z; sm=Q(0)
    for k in range(N):
        if k: term*=zz
        sm+=term/Q(2*k+1)
    center=2*sm; az=abs(z)
    rem=2*az**(2*N+1)/Q(2*N+1)/(1-az*az)
    return center-rem,center+rem
LOG2=atanh_log_iv_unit(Q(2))
def log_iv(x):
    x=Q(x); m=x; k=0
    while m>2: m/=2; k+=1
    while m<Q(1,2): m*=2; k-=1
    lo,hi=atanh_log_iv_unit(m)
    if k>=0: return lo+k*LOG2[0],hi+k*LOG2[1]
    return lo+k*LOG2[1],hi+k*LOG2[0]
assert log_iv(Q(100))[1]<Q(99,20)          # lambda(1/100)<5
assert log_iv(Q(10000))[1]<Q(9999,1000)   # lambda(1/10000)<10
assert log_iv(Q(4000))[1]<9
assert log_iv(Q(100))[1]<Q(14,3)

# Two true cardinality groups give >1/(2 delta) Fisher for s>=9/10.
# A deliberately coarse exact lower bound uses s>=9/10, 22s+53>72, 11s+64<75.
fisher_coeff=sp.factor(2*64*Q(9,10)*72**2/(15625*75))
assert fisher_coeff==Q(995328,1953125)>Q(1,2)

print('I05-30 simultaneous endpoint certificate: PASS')
print('rank(B)=2, dense:',all(x!=0 for x in B))
print('endpoint nullities: ker K(1)=',6-K.subs(t,1).rank(),', ker(I-K(1))=',6-(sp.eye(6)-K.subs(t,1)).rank())
print('endpoint zero atoms: simple=',simple,'double=',double)
print('cardinality R0=R6 =',R[0])
print('cardinality R1=R5 =',R[1])
print('13 exact likelihood types verified; all 64 events retained')
print('compact [0,9/10]: good rational reserve > 19/20; bad log budget < 1/2')
print('compact [9/10,99/100]: good rational reserve > 8; bad log budget < 11/10')
print('endpoint grouped Fisher coefficient =',fisher_coeff,'> 1/2')
print('acceleration coefficient budget =',acc,'< 11/5')
print('whole chord author bound: Hdd(t) <= -(1/10)t^2 for 0<|t|<1')
