"""M8 bounded rational sanity; six fixed centers, no random search."""
from fractions import Fraction as F
from decimal import Decimal, localcontext
from itertools import permutations, combinations
from math import lcm, prod
from pathlib import Path
import json
import hashlib
import time

HERE=Path(__file__).resolve().parent
def pmul(a,b):
    out=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): out[i+j]+=x*y
    return out
def padd(a,b):
    return [(a[i] if i<len(a) else F(0))+(b[i] if i<len(b) else F(0)) for i in range(max(len(a),len(b)))]
def det(a):
    out=[F(0)]
    for perm in permutations(range(len(a))):
        term=[F((-1)**sum(perm[i]>perm[j] for i in range(len(a)) for j in range(i+1,len(a))))]
        for i in range(len(a)): term=pmul(term,a[i][perm[i]])
        out=padd(out,term)
    return out
def dec(x): return Decimal(x.numerator)/Decimal(x.denominator)
def logs(x):
    k=0
    while x<1: x*=2; k-=1
    while x>=2: x/=2; k+=1
    def ser(z):
        lo=2*sum(z**(2*j+1)/F(2*j+1) for j in range(16))
        return lo,lo+2*z**33/(33*(1-z*z))
    a,b=ser((x-1)/(x+1)); c,d=ser(F(1,3))
    return (a+k*c,b+k*d) if k>=0 else (a+k*d,b+k*c)
def linsum(terms):
    lo=hi=F(0)
    for weight,arg in terms:
        a,b=logs(arg); lo+=weight*(a if weight>=0 else b); hi+=weight*(b if weight>=0 else a)
    return lo,hi
def interval(bounds):
    scale=10**18; a,b=bounds
    return [str(F((a*scale).__floor__(),scale)),str(F((b*scale).__ceil__(),scale))]
def stringify(x):
    if isinstance(x,F): return str(x)
    if isinstance(x,list): return [stringify(a) for a in x]
    if isinstance(x,dict): return {k:stringify(v) for k,v in x.items()}
    return x
def build(theta,v):
    w=(1,2,-3)
    u=[[F(1,3)]*3 for _ in range(3)]
    vv=[[F(x*y,14) for y in w] for x in w]
    ww=[[F(i==j)-u[i][j]-vv[i][j] for j in range(3)] for i in range(3)]
    frame=[u,vv,ww]
    for i,a in enumerate(frame):
        for j,b in enumerate(frame):
            product=[[sum(a[r][k]*b[k][s] for k in range(3)) for s in range(3)] for r in range(3)]
            assert product==(a if i==j else [[F(0)]*3 for _ in range(3)])
    k=[[sum(theta[a]*frame[a][i][j] for a in range(3)) for j in range(3)] for i in range(3)]
    d=[[sum(v[a]*frame[a][i][j] for a in range(3)) for j in range(3)] for i in range(3)]
    p=[[frame[a][i][i] for a in range(3)] for i in range(3)]
    raw=[]
    for mask in range(8):
        term=[F(1)]
        for i in range(3): term=pmul(term,[theta[i],v[i]] if mask>>i&1 else [1-theta[i],-v[i]])
        raw.append(term)
    event=[]
    for mask in range(8):
        indices=[i for i in range(3) if mask>>i&1]
        poly=det([[[k[i][j],d[i][j]] for j in indices] for i in indices])
        event.append(poly+[F(0)]*(4-len(poly)))
    for i in range(3):
        for mask in range(8):
            if not mask>>i&1: event[mask]=[a-b for a,b in zip(event[mask],event[mask|1<<i])]
    for a in range(3):
        for maskseq in ((1,2,4),(6,5,3)):
            assert event[maskseq[a]]==[sum(p[a][i]*raw[maskseq[i]][j] for i in range(3)) for j in range(4)]
    assert event[0]==raw[0] and event[7]==raw[7]
    assert [sum(row[j] for row in event) for j in range(4)]==[1,0,0,0]
    return k,d,p,event
def main():
    start=time.time()
    cases=[(F(1,5),F(1,2),F(4,5)),(F(1,5),F(3,5),F(4,5)),(F(1,10),F(1,2),F(4,5)),(F(1,5),F(2,5),F(4,5)),(F(1,10),F(1,5),F(9,10)),(F(1,5),F(13,20),F(4,5))]
    v=[F(1,5),F(1,3),F(2,3)]; records=[]
    with localcontext() as ctx:
        ctx.prec=80
        for index,theta in enumerate(cases):
            k,d,p,ev=build(theta,v)
            y=[ev[i] for i in (1,2,4)]; z=[ev[i] for i in (6,5,3)]
            r=[sum(row[j] for row in y) for j in range(4)]; t=[sum(row[j] for row in z) for j in range(4)]
            alpha=[row[0]/r[0] for row in y]; beta=[row[0]/t[0] for row in z]
            cs=[]; cinterval=[]; rational_signs=[]
            for i in range(3):
                terms=[(p[a][i],alpha[a]*beta[a]) for a in range(3)]
                terms += [(-(1-theta[i]),x) for x in alpha]+[(-theta[i],x) for x in beta]
                cs.append(sum(dec(weight)*dec(arg).ln() for weight,arg in terms))
                cinterval.append(linsum(terms))
                denominator=lcm(*(weight.denominator for weight,arg in terms))
                ratio=prod(arg**int(weight*denominator) for weight,arg in terms)
                assert (ratio>1)==(cinterval[-1][0]>0)
                rational_signs.append(dict(clearing_denominator=denominator,power_ratio=ratio,sign=(ratio>1)-(ratio<1)))
            accel=sum(dec(2*row[2])*dec(row[0]/mass[0]).ln() for layer,mass in ((y,r),(z,t)) for row in layer)
            paired=2*sum(dec(v[j]*v[kk])*cs[i] for i in range(3) for j,kk in [tuple(a for a in range(3) if a!=i)])
            assert abs(accel-paired)<Decimal('1e-65')
            m=min(a*b for a,b in zip(alpha,beta)); ln_lower=dec(27*m).ln()
            assert min(cs)>=ln_lower-Decimal('1e-65')
            fisher=sum(row[1]**2/row[0] for row in ev)
            blo,bhi=linsum([(2*row[2],row[0]) for row in ev]); blo+=fisher; bhi+=fisher
            certificate=[]
            for step in (F(1,100),F(1,1000)):
                constraints=[]
                for a in range(3):
                    poly=padd([27*x for x in pmul(y[a],z[a])],[-x for x in pmul(r,t)])
                    lower=poly[0]-sum(abs(poly[j])*step**j for j in range(1,7))
                    constraints.append(dict(coefficients=poly,lower_bound=lower))
                margin=min(min(th+sign*step*rate,1-th-sign*step*rate) for th,rate in zip(theta,v) for sign in (-1,1))
                certificate.append(dict(step=step,passed=all(c['lower_bound']>0 for c in constraints),constraints=constraints,spectral_margin=margin))
            record=dict(index=index,theta=list(theta),rates=v,rank=3,K=k,D=d,P=p,events=ev,alpha=alpha,beta=beta,
                min_product=m,old_rectangle=all(F(1,4)<=x<=F(4,9) for x in alpha+beta),new_one_fifth=all(x>=F(1,5) for x in alpha+beta),
                product_condition=m>F(1,27),exact_coefficient_condition=all(a>0 for a,b in cinterval),
                C=[str(x) for x in cs],C_intervals=[interval(x) for x in cinterval],C_rational_signs=rational_signs,B_interval=interval((blo,bhi)),
                paired_identity_error=str(accel-paired),interval_attempts=certificate,
                connected=all(k[i][j]!=0 for i,j in combinations(range(3),2)))
            records.append(record)
    report=dict(status='SCOUT_SANITY_FOR_ANALYTIC_CANDIDATE',seed=None,random_draws=0,cases=records,
        counts=dict(centers=len(records),exact_event_polynomials=8*len(records),coefficients=32*len(records),interval_attempts=2*len(records),
                    product_pass=sum(r['product_condition'] for r in records),new_one_fifth_pass=sum(r['new_one_fifth'] for r in records),
                    coefficient_pass=sum(r['exact_coefficient_condition'] for r in records),old_pass=sum(r['old_rectangle'] for r in records)),
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),elapsed_seconds=time.time()-start,exit_code=0)
    (HERE/'sanity_results.json').write_text(json.dumps(stringify(report),indent=2)+'\n')
    print(json.dumps(report['counts']))
    for row in records: print(row['index'],row['old_rectangle'],row['new_one_fifth'],row['product_condition'],row['exact_coefficient_condition'],str(min(row['alpha']+row['beta'])),str(row['min_product']),[c['passed'] for c in row['interval_attempts']])
if __name__=='__main__': main()
