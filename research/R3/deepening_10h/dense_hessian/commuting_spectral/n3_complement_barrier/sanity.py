"""Bounded exact-rational sanity for M7; no random search or external modules.

31 uniform-layer cases, 3 general cases, one asymmetric certified interval.
The proof is in Markdown; finite tests are not its universal justification.
"""
from decimal import Decimal, localcontext
from fractions import Fraction as F
from itertools import permutations, combinations
from pathlib import Path
import hashlib
import json
import time

HERE=Path(__file__).resolve().parent
ZERO=F(0)
ONE=F(1)

def eye(): return [[F(i==j) for j in range(3)] for i in range(3)]
def matmul(a,b): return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def project(vector):
    norm=sum(x*x for x in vector)
    return [[F(x*y,norm) for y in vector] for x in vector]

def symmetric_frame(w):
    u=[[F(1,3)]*3 for _ in range(3)]; v=project(w)
    z=[[F(i==j)-u[i][j]-v[i][j] for j in range(3)] for i in range(3)]
    return [u,v,z]

def householder_frame(w):
    p=project(w); q=[[F(i==j)-2*p[i][j] for j in range(3)] for i in range(3)]
    return [[[q[i][a]*q[j][a] for j in range(3)] for i in range(3)] for a in range(3)]

def check_frame(frame):
    for i,a in enumerate(frame):
        assert matmul(a,a)==a and sum(a[j][j] for j in range(3))==1
        for j,b in enumerate(frame):
            if i!=j: assert matmul(a,b)==[[ZERO]*3 for _ in range(3)]
    assert [[sum(a[i][j] for a in frame) for j in range(3)] for i in range(3)]==eye()

def pmul(a,b):
    result=[ZERO]*4
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            if i+j<4: result[i+j]+=x*y
    return result

def pdet(a):
    n=len(a); result=[ZERO]*4
    for perm in permutations(range(n)):
        sign=(-1)**sum(perm[i]>perm[j] for i in range(n) for j in range(i+1,n))
        term=[F(sign),ZERO,ZERO,ZERO]
        for i in range(n): term=pmul(term,a[i][perm[i]])
        result=[x+y for x,y in zip(result,term)]
    return result

def raw_polynomials(theta,rates):
    rows=[]
    for mask in range(8):
        term=[ONE,ZERO,ZERO,ZERO]
        for i in range(3):
            factor=[theta[i],rates[i]] if mask>>i&1 else [1-theta[i],-rates[i]]
            term=pmul(term,factor)
        rows.append(term)
    return rows

def exact_events(frame,theta,rates):
    check_frame(frame)
    k=[[sum(theta[a]*frame[a][i][j] for a in range(3)) for j in range(3)] for i in range(3)]
    d=[[sum(rates[a]*frame[a][i][j] for a in range(3)) for j in range(3)] for i in range(3)]
    p=[[frame[a][i][i] for a in range(3)] for i in range(3)]
    events=[]
    for mask in range(8):
        indices=[i for i in range(3) if mask>>i&1]
        events.append(pdet([[[k[i][j],d[i][j]] for j in indices] for i in indices]))
    for i in range(3):
        for mask in range(8):
            if not mask>>i&1:
                events[mask]=[x-y for x,y in zip(events[mask],events[mask|1<<i])]
    raw=raw_polynomials(theta,rates)
    channel=[[ZERO]*4 for _ in range(8)]; channel[0]=raw[0]; channel[7]=raw[7]
    for i in range(3):
        channel[1<<i]=[sum(p[i][a]*raw[1<<a][j] for a in range(3)) for j in range(4)]
        channel[7^(1<<i)]=[sum(p[i][a]*raw[7^(1<<a)][j] for a in range(3)) for j in range(4)]
    assert events==channel
    assert [sum(row[j] for row in events) for j in range(4)]==[1,0,0,0]
    assert all(row[0]>0 for row in events)
    complement=raw_polynomials([1-x for x in theta],rates)
    for i in range(3):
        assert raw[7^(1<<i)]==[(-1)**j*x for j,x in enumerate(complement[1<<i])]
        j,k2=[a for a in range(3) if a!=i]
        assert 2*(raw[1<<i][2]+raw[7^(1<<i)][2])==2*(rates[j]*rates[k2]-rates[i]*rates[j]-rates[i]*rates[k2])
    cross=sum(rates[i]*rates[j] for i,j in combinations(range(3),2))
    assert sum(abs(2*raw[mask][2]) for mask in (1,2,4,6,5,3))<=6*cross
    return k,d,p,events

def dec(x): return Decimal(x.numerator)/Decimal(x.denominator)
def log_bounds(x,terms=16):
    assert x>0
    exponent=0
    while x<1: x*=2; exponent-=1
    while x>=2: x/=2; exponent+=1
    def series(z):
        lower=2*sum(z**(2*j+1)/F(2*j+1) for j in range(terms))
        error=2*z**(2*terms+1)/(F(2*terms+1)*(1-z*z))
        return lower,lower+error
    lo,hi=series((x-1)/(x+1)); a,b=series(F(1,3))
    return (lo+exponent*a,hi+exponent*b) if exponent>=0 else (lo+exponent*b,hi+exponent*a)

def rounded_interval(bounds,scale=10**18):
    lo,hi=bounds; a=lo*scale; b=hi*scale
    return [str(F(a.numerator//a.denominator,scale)),str(F(-((-b.numerator)//b.denominator),scale))]

def negative_h2_interval(rows):
    lo=hi=sum(row[1]**2/row[0] for row in rows)
    for row in rows:
        a,b=log_bounds(row[0]); weight=2*row[2]
        lo+=weight*(a if weight>=0 else b); hi+=weight*(b if weight>=0 else a)
    return lo,hi

def entropy_interval(probabilities):
    lo=hi=ZERO
    for p in probabilities:
        a,b=log_bounds(p); lo-=p*b; hi-=p*a
    return lo,hi

def layer_parts(rows):
    mass=[sum(row[j] for row in rows) for j in range(4)]
    fisher=sum(row[1]**2/row[0] for row in rows)-mass[1]**2/mass[0]
    sos=sum((rows[b][0]*rows[a][1]-rows[a][0]*rows[b][1])**2/(mass[0]*rows[a][0]*rows[b][0]) for a,b in combinations(range(3),2))
    assert fisher==sos and fisher>=0
    accel=sum(dec(2*row[2])*dec(row[0]/mass[0]).ln() for row in rows)
    residual=sum(dec(2*row[2])*dec(3*row[0]/mass[0]).ln() for row in rows)
    return mass,fisher,accel,residual

def summarize(events,rates,uniform):
    singleton=[events[1<<i] for i in range(3)]
    pair=[events[7^(1<<i)] for i in range(3)]
    r,dr,ar,rr=layer_parts(singleton); s,ds,as_,rs=layer_parts(pair)
    counts=[events[0],r,s,events[7]]
    def barrier(rows): return sum(dec(row[1])**2/dec(row[0])+dec(2*row[2])*dec(row[0]).ln() for row in rows)
    b=barrier(events); count_b=barrier(counts)
    cross=sum(rates[i]*rates[j] for i,j in combinations(range(3),2))
    decomposed=count_b+dec(dr+ds)+2*Decimal(3).ln()*dec(cross)+rr+rs
    assert abs(b-decomposed)<Decimal('1e-65')
    assert 2*(r[2]+s[2])==-2*cross
    record=dict(B=str(b),count_barrier=str(count_b),D_r=str(dr),D_s=str(ds),complement_baseline=str(2*Decimal(3).ln()*dec(cross)),residual=str(rr+rs),decomposition_error=str(b-decomposed),min_atom=str(min(row[0] for row in events)))
    if uniform:
        assert len(set(row[0] for row in singleton))==len(set(row[0] for row in pair))==1
        assert rr+rs==0
        assert b>0
        b_interval=negative_h2_interval(events)
        norm2=sum(x*x for x in rates)
        # All subclass examples have spectral margin at least 1/5.
        eps=F(1,5); coefficient=2*eps*(1-eps)*norm2/9
        _lo,ln3hi=log_bounds(F(3))
        assert b_interval[0]>coefficient*ln3hi
        record['B_interval']=rounded_interval(b_interval)
        record['c_epsilon_norm2']=str(dec(coefficient)*Decimal(3).ln())
    return record

def string_matrix(a): return [[str(x) for x in row] for row in a]

def main():
    started=time.time(); records=[]
    bases=[(F(1,5),F(7,10)),(F(4,5),F(3,10)),(F(1,2),F(1,2))]
    frames=[symmetric_frame((1,2,-3)),symmetric_frame((2,3,-5))]
    directions=[(ONE,ZERO,ZERO),(ZERO,ONE,ZERO),(ZERO,ZERO,ONE),(F(1,5),F(1,3),F(2,3)),(F(1,7),F(2,5),ZERO)]
    cases=[]
    for a,b in bases:
        for fi,frame in enumerate(frames):
            for ri,rate in enumerate(directions):
                cases.append((f'uniform_{a}_{b}_frame{fi}_rate{ri}',frame,[a,b,b],list(rate),True))
    hh=householder_frame((1,2,3))
    cases.append(('scalar_arbitrary_basis',hh,[F(1,2)]*3,[F(2,7),F(1,3),F(3,5)],True))
    for index,theta in enumerate(([F(1,5),F(2,5),F(4,5)],[F(3,4),F(1,2),F(1,3)],[F(1,7),F(2,3),F(5,6)])):
        cases.append((f'general_identity_{index}',hh,theta,[F(1,7),F(2,5),F(3,8)],False))
    asymmetric_theta=[F(1,5),F(7,10),F(71,100)]
    cases.append(('asymmetric_interval_center',frames[0],asymmetric_theta,list(directions[3]),False))
    with localcontext() as context:
        context.prec=80
        for name,frame,theta,rate,uniform in cases:
            k,d,p,events=exact_events(frame,theta,rate)
            record=dict(name=name,uniform_subclass=uniform,theta=[str(x) for x in theta],rates=[str(x) for x in rate],rank=sum(x>0 for x in rate),K=string_matrix(k),D=string_matrix(d),P=string_matrix(p),event_polynomials=string_matrix(events),**summarize(events,rate,uniform))
            record['connected']=all(k[i][j]!=0 for i,j in combinations(range(3),2))
            records.append(record)
        asymmetric=exact_events(frames[0],asymmetric_theta,list(directions[3]))
        interval_step=F(1,20)
        interval_constraints=[]
        for masks in ((1,2,4),(6,5,3)):
            mass=[sum(asymmetric[3][mask][j] for mask in masks) for j in range(4)]
            for mask in masks:
                atom=asymmetric[3][mask]
                for label,coeff in [('lower', [4*x-y for x,y in zip(atom,mass)]),('upper',[4*y-9*x for x,y in zip(atom,mass)])]:
                    bound=coeff[0]-sum(abs(coeff[j])*interval_step**j for j in range(1,4))
                    assert bound>0, (mask,label,bound)
                    interval_constraints.append(dict(mask=mask,side=label,coefficients=[str(x) for x in coeff],uniform_lower_bound=str(bound)))
        interval_margin=min(min(t+sign*interval_step*v,1-t-sign*interval_step*v) for t,v in zip(asymmetric_theta,directions[3]) for sign in (-1,1))
        assert interval_margin>F(1,10)
        assert len(set(asymmetric_theta))==3
        assert len(set(asymmetric[0][i][i] for i in range(3)))==3
        assert all(asymmetric[0][i][j]!=0 for i,j in combinations(range(3),2))
        interval_certificate=dict(step=str(interval_step),spectral_margin=str(interval_margin),constraints=interval_constraints,
            theorem='Theorem E, whole interval, fixed eigenvectors and positive rates',
            gap_upper_bound='-134*log(81/64)/22500*h^2 for |h|<=1/20',
            rates_norm_squared=str(sum(x*x for x in directions[3])))
        example=exact_events(frames[0],[F(1,5),F(7,10),F(7,10)],list(directions[3]))
        center=entropy_interval([row[0] for row in example[3]])
        chords=[]
        for step in (F(1,100),F(1,1000),F(1,10000)):
            endpoints=[]
            for sign in (-1,1):
                probabilities=[sum(x*(sign*step)**j for j,x in enumerate(row)) for row in example[3]]
                assert min(probabilities)>0
                endpoints.append(entropy_interval(probabilities))
            gap=((endpoints[0][0]+endpoints[1][0])/2-center[1],(endpoints[0][1]+endpoints[1][1])/2-center[0])
            assert gap[1]<0
            margin=min(min(t+sign*step*v,1-t-sign*step*v) for t,v in zip([F(1,5),F(7,10),F(7,10)],directions[3]) for sign in (-1,1))
            assert margin>F(1,10)
            chords.append(dict(step=str(step),gap_interval=rounded_interval(gap),spectral_margin=str(margin)))
    report=dict(status='AUTHOR_SANITY_ONLY_PENDING_REVIEW',seed=None,parameter_design='deterministic rational finite set, not a search',
                counts=dict(total_cases=len(records),uniform_subclass=31,general_identity_only=3,asymmetric_interval=1,exact_events=8*len(records),polynomial_coefficients=32*len(records),interval_constraints=len(interval_constraints),negative_chords=3,positive_total_candidates=sum(Decimal(row['B'])<0 for row in records),failed_assertions=0),
                cases=records,chords=chords,interval_certificate=interval_certificate,script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),elapsed_seconds=time.time()-started,exit_code=0)
    (HERE/'sanity_results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(counts=report['counts'],chords=chords,elapsed_seconds=report['elapsed_seconds'],exit_code=0),indent=2))

if __name__=='__main__': main()
