"""Exact-law diagnostics; not a general proof certificate."""
from fractions import Fraction as F
from math import log, log1p
import json

def entropy(q):
    return -sum(float(x)*log(float(x)) for x in q if x)

def h(x):
    return -x*log(x)-(1-x)*log1p(-x)

def law(a,b,t2):
    q=((1-a)*(1-b)-t2,a*(1-b)+t2,(1-a)*b+t2,a*b-t2)
    assert all(v>=0 for v in q)
    assert sum(q)==1
    assert q[1]+q[3]==a and q[2]+q[3]==b
    return q

rows=[]
for p in [F(1,10),F(1,100),F(1,1000),F(1,10000),F(1,100000)]:
    for theta in [F(1),F(1,2)]:
        t2=theta*p*(1-p)
        q=law(p,1-p,t2)
        loss=entropy(law(p,1-p,F(0)))-entropy(q)
        if theta==1:
            assert q==(0,p,1-p,0)
            assert abs(loss-h(float(p)))<1e-14
        rows.append({"p":str(p),"theta":str(theta),"entropy_loss":loss,
                     "frobenius_squared":float(2*t2),"ratio":loss/float(2*t2)})
dims=[]
c=0.25
for m in [1,16,256,4096,65536]:
    t=c*m**(-0.25)
    x=2*t*t
    loss_pair=(0.5-x)*log1p(-2*x)+(0.5+x)*log1p(2*x)
    dims.append({"m":m,"operator_error":t,"total_loss":m*loss_pair,
                 "limiting_total_loss":8*c**4,"per_site_loss":loss_pair/2})
print(json.dumps({"status":"diagnostic_not_certificate","B2_exact_law_cases":rows,
                  "B1_scaling_cases":dims,
                  "coverage":{"planned_exact_law":10,"completed_exact_law":10,
                              "planned_scaling":5,"completed_scaling":5,
                              "failed":0,"independently_certified":0}},indent=2))
