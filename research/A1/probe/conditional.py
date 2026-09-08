"""Four hand-written rational diagnostics, separately authorized after batch."""
import json, os
from fractions import Fraction as F
import mpmath as mp
import probe
mp.mp.dps=80
def log_interval(q,N=256):
    # Exact rational atanh series, after powers-of-two range reduction.
    k=0
    while q>2: q/=2; k+=1
    while q<1: q*=2; k-=1
    def base(x):
        z=(x-1)/(x+1)
        s=2*sum((z**(2*j+1)/F(2*j+1) for j in range(N)),F(0))
        err=2*z**(2*N+1)/(F(2*N+1)*(1-z*z))
        return s,s+err
    lo,hi=base(q); l2,h2=base(F(2))
    return (lo+k*l2,hi+k*h2) if k>=0 else (lo+k*h2,hi+k*l2)
def add(I,J): return I[0]+J[0],I[1]+J[1]
def times(q,I): return (q*I[0],q*I[1]) if q>=0 else (q*I[1],q*I[0])
def gradient_intervals(v):
    a,b,r=v; d=a*b-r*r
    p=[1-a-b+d,a-d,b-d,d]
    jac=[[b-1,1-b,-b,b],[a-1,-a,1-a,a],[-r,r,r,-r]]
    out=[]
    for row in jac:
        I=(F(0),F(0))
        for coeff,q in zip(row,p): I=add(I,times(-coeff,log_interval(q)))
        out.append(I)
    return out,p
def dec(q): return mp.mpf(q.numerator)/q.denominator
def exact_events(v):
    a,b,c,x,y,z=v; out=[]
    for mask in range(8):
        s=[1 if mask>>i&1 else -1 for i in range(3)]
        d=[t if sign==1 else 1-t for t,sign in zip([a,b,c],s)]
        out.append(d[0]*d[1]*d[2]-s[0]*s[1]*x*x*d[2]-s[0]*s[2]*y*y*d[1]-s[1]*s[2]*z*z*d[0]+2*s[0]*s[1]*s[2]*x*y*z)
    return out
def outward(I):
    den=10**18
    return [str(F(I[0].numerator*den//I[0].denominator,den)),str(F(-((-I[1].numerator*den)//I[1].denominator),den))]
rows=[]
for bz in [F(0),F(1,1000),F(1,100),F(-1,100)]:
    v=[F(1,4),F(3,4),F(1,2),F(1,10),F(1,10),bz]
    assert probe.exact_feasible(v)
    a,b,c,r,x,y=v
    C1=[a-x*x/c,b-y*y/c,r-x*y/c]
    C0=[a+x*x/(1-c),b+y*y/(1-c),r+x*y/(1-c)]
    g0,p0=gradient_intervals(C0); g1,p1=gradient_intervals(C1)
    D=[add(i,times(F(-1),j)) for i,j in zip(g0,g1)]
    # Hand direction w=e2; correction = 2 D_22.
    I=times(F(2),D[1])
    pp=exact_events(v[:-1]+[v[-1]+1]); pm=exact_events(v[:-1]+[v[-1]-1]); p=exact_events(v)
    dp=[(r-l)/2 for r,l in zip(pp,pm)]; ddp=[r+l-2*q for r,l,q in zip(pp,pm,p)]
    H2=(-sum(d*d/q for d,q in zip(dp,p)),)*2
    for d,q in zip(ddp,p): H2=add(H2,times(-d,log_interval(q)))
    rows.append(dict(K=[str(t) for t in v],C0=[str(t) for t in C0],C1=[str(t) for t in C1],min_principal_minor=str(min(probe.minors3(v)+probe.minors3(v,True))),event_probabilities_C0=[str(t) for t in p0],event_probabilities_C1=[str(t) for t in p1],w=['0','1'],positive_certified=I[0]>0,correction_rational_outer_interval=outward(I),correction_interval_decimal=[str(dec(t)) for t in I],full_H_second_rational_outer_interval=outward(H2),full_H_second_negative_certified=H2[1]<0,log_series_terms=256))
probe.save(probe.ROOT/'conditional.json',dict(status='DISPROVED_AUXILIARY_ONLY' if any(r['positive_certified'] for r in rows) else 'INCOMPLETE',manual_centers=4,entropy_gradient_evaluations=8,full_H_second_certificates=4,pid=os.getpid(),certificates=rows))
