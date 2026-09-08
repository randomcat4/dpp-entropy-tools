"""Exact event determinants + interval logs for the fixed residual-enclosed pair."""
import argparse
from fractions import Fraction as F
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import resource
import sys
import time
import mpmath as mp
from boundary_residual import Z, add, sub, neg, conj, mul, scale


def divide_exact(a,b):
    d=b[0]*b[0]+b[1]*b[1]
    re=a[0]*b[0]+a[1]*b[1]; im=a[1]*b[0]-a[0]*b[1]
    if not d or re%d or im%d: raise ArithmeticError('non-exact Bareiss division')
    return (re//d,im//d)


def event_masses(K):
    n=len(K); denominator=1
    for row in K:
        for x in row:
            denominator=math.lcm(denominator,x[0].denominator,x[1].denominator)
    A=[[(int(x[0]*denominator),int(x[1]*denominator)) for x in row] for row in K]
    output=[]
    for event in range(2**n):
        Q=[row.copy() for row in A]; zeros=0
        for i in range(n):
            if not ((event>>i)&1):
                Q[i][i]=(Q[i][i][0]-denominator,Q[i][i][1]);zeros+=1
        previous=(1,0)
        for k in range(n-1):
            pivot=Q[k][k]
            if pivot==(0,0):raise ArithmeticError('zero principal event pivot')
            for i in range(k+1,n):
                for j in range(k+1,n):
                    Q[i][j]=divide_exact(sub(mul(Q[i][j],pivot),mul(Q[i][k],Q[k][j])),previous)
            previous=pivot
        det=Q[-1][-1]
        if det[1]:raise ArithmeticError('nonreal Hermitian determinant')
        p=F((-1)**zeros*det[0],denominator**n)
        if p<=0:raise ArithmeticError('nonpositive strict-interior event')
        output.append(p)
    if sum(output)!=1:raise ArithmeticError('exact mass normalization failed')
    return output


def ivf(x):return mp.iv.mpf(x.numerator)/mp.iv.mpf(x.denominator)
def binary(x):
    if x in (0,1):return mp.iv.mpf(0)
    z=ivf(x)
    return -z*mp.iv.log(z)-(1-z)*mp.iv.log(1-z)
def rational_endpoint(x,upper):
    q=x._mpi_[1 if upper else 0]
    sign,man,exponent,_=q
    return F((-1 if sign else 1)*man)*F(2)**exponent
def interval_string(x):return {'lower':str(rational_endpoint(x,False)),'upper':str(rational_endpoint(x,True)),
                               'lower_float':float(rational_endpoint(x,False)),'upper_float':float(rational_endpoint(x,True))}
def interval_bounds(lower,upper):return mp.iv.mpf([ivf(lower).a,ivf(upper).b])


def symbol_kernel(candidate,t,n):
    cs=[(F(candidate['p']),F(0))]+[(F(a)/2,-t*F(b)/2) for a,b in zip(candidate['a'],candidate['b'])]
    m=len(cs)-1
    def c(k):return cs[k] if 0<=k<=m else conj(cs[-k]) if -m<=k<0 else Z
    return [[c(i-j) for j in range(n)] for i in range(n)]


def case_bound(candidate,record,t,n):
    m=len(candidate['a']);eps=F(candidate['uniform_margin']);K=symbol_kernel(candidate,t,n+1)
    raw=event_masses(K)
    extreme=[];errors=[]
    for complement in [False,True]:
        case=next(c for c in record['cases'] if F(c['t'])==t and c['complement_symbol']==complement)
        A=[row.copy() for row in K]
        for i in range(m):
            for j in range(m):
                value=tuple(map(F,case['corner_rational'][i][j]))
                if complement:value=sub((F(int(i==j)),F(0)),value)
                A[i][j]=value
        probs=event_masses(A)
        extreme.append(probs)
        delta=F(case['operator_error_upper_rational'])
        if delta>=eps:raise ArithmeticError('kernel error exceeds margin')
        errors.append(delta*(1+((1+delta)/(eps-delta))**2))
    lower=mp.iv.mpf(0);upper=mp.iv.mpf(0);width=mp.iv.mpf(0)
    min_interval=F(1);max_interval=F(0)
    for event in range(2**n):
        idx1=event+(1<<n)
        weight=raw[event]+raw[idx1]
        q=raw[idx1]/weight
        q1=extreme[0][idx1]/(extreme[0][event]+extreme[0][idx1])
        q0=extreme[1][idx1]/(extreme[1][event]+extreme[1][idx1])
        lo=max(eps,q1-errors[0]);hi=min(1-eps,q0+errors[1])
        if lo>hi or q<lo or q>hi:raise ArithmeticError('extreme-past conditional order failed')
        # Binary entropy is concave; minimum over an interval is at an endpoint.
        h_lo=binary(lo);h_hi=binary(hi)
        low=min(rational_endpoint(h_lo,False),rational_endpoint(h_hi,False))
        high=min(rational_endpoint(h_lo,True),rational_endpoint(h_hi,True))
        lower+=ivf(weight)*interval_bounds(low,high)
        upper+=ivf(weight)*binary(q)
        width+=ivf(weight)*ivf(hi-lo)
        min_interval=min(min_interval,lo);max_interval=max(max_interval,hi)
    return {'t':str(t),'past_length':n,'lower_bound_interval':interval_string(lower),
            'upper_bound_interval':interval_string(upper),'weighted_extreme_width':interval_string(width),
            'conditional_error_bounds':[str(e) for e in errors],
            'exact_determinants':3*2**(n+1),'normalization':'EXACT_FRACTION_EQUALITY',
            'conditional_range':[str(min_interval),str(max_interval)]}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--candidate',required=True);parser.add_argument('--boundary',required=True)
    parser.add_argument('--output',required=True);parser.add_argument('--n',type=int,default=8);args=parser.parse_args()
    if not 3<=args.n<=12:raise ValueError('bounded unit supports 3<=n<=12')
    started=time.time();mp.iv.dps=45
    candidate_path=Path(args.candidate);boundary_path=Path(args.boundary)
    candidate=json.loads(candidate_path.read_text());record=json.loads(boundary_path.read_text())
    cases=[case_bound(candidate,record,t,args.n) for t in [F(0),F(candidate['tau'])]]
    center,endpoint=cases
    gaplo=F(endpoint['lower_bound_interval']['lower'])-F(center['upper_bound_interval']['upper'])
    gaphi=F(endpoint['upper_bound_interval']['upper'])-F(center['lower_bound_interval']['lower'])
    out={'status':'RATE_ENCLOSURE_COMPUTED_PROOF_REVIEW_PENDING','pid':os.getpid(),'exit_status':0,
         'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'boundary_source_sha256':hashlib.sha256(Path(__file__).with_name('boundary_residual.py').read_bytes()).hexdigest(),
         'candidate_sha256':hashlib.sha256(candidate_path.read_bytes()).hexdigest(),
         'boundary_sha256':hashlib.sha256(boundary_path.read_bytes()).hexdigest(),
         'python':platform.python_version(),'mpmath':mp.__version__,'interval_dps':mp.iv.dps,'argv':sys.argv,
         'seed':None,'randomness':'none','threads':{k:os.environ.get(k) for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']},
         'seconds':time.time()-started,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
         'actual_determinants':sum(c['exact_determinants'] for c in cases),'cases':cases,
         'gap_enclosure':{'lower':str(gaplo),'upper':str(gaphi),'lower_float':float(gaplo),'upper_float':float(gaphi)},
         'classification':'NEGATIVE_PAIR_GAP' if gaphi<0 else 'POSITIVE_COUNTEREXAMPLE_CANDIDATE' if gaplo>0 else 'INCONCLUSIVE'}
    Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['status','pid','seconds','peak_rss_kib','actual_determinants','classification']}))
    print(json.dumps(out['gap_enclosure']))


if __name__=='__main__':main()
