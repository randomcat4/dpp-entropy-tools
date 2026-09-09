"""One exact rational point; rigorously enclose log terms of the obstruction."""
import hashlib,json,os,sys,time
from fractions import Fraction as R
from pathlib import Path
import mpmath as mp

BASELINE='fa504ec74e16843fafc395880d7ba99b4c1d2129'

def log_unit(x,terms=80):
    assert R(1)<=x<=R(2)
    z=(x-1)/(x+1)
    lo=2*sum((z**(2*j+1)/R(2*j+1) for j in range(terms)),R(0))
    tail=2*z**(2*terms+1)/(R(2*terms+1)*(1-z*z))
    return lo,lo+tail

def log_bound(x):
    assert x>0
    power=0
    while x>=2: x/=2; power+=1
    while x<1: x*=2; power-=1
    lo,hi=log_unit(x); l2,u2=log_unit(R(2))
    return (lo+power*l2,hi+power*u2) if power>=0 else (lo+power*u2,hi+power*l2)

def add(a,b): return a[0]+b[0],a[1]+b[1]
def scale(c,a): return (c*a[0],c*a[1]) if c>=0 else (c*a[1],c*a[0])
def fmt(x):return f'{x.numerator}/{x.denominator}'
def interval_decimal(a,places=30):
    n=10**places
    def dec(k):
        sign='-' if k<0 else ''; k=abs(k)
        return sign+str(k//n)+'.'+str(k%n).zfill(places)
    lo=(a[0]*n).__floor__(); hi=(a[1]*n).__ceil__()
    return [dec(lo),dec(hi)]
def m(x):return mp.mpf(x.numerator)/x.denominator

def main():
    start=time.time(); eps=R(1,10**12); a=[R(1,14),R(2,7),R(9,14)]
    p=[R(0)]*8; v=[R(0)]*8
    p[0]=(1-eps)/4; v[0]=-R(5,4)+eps; p[7]=eps/4;v[7]=R(1,4)+eps
    for i in range(3):
        p[1<<i]=(1-a[i]+(2*a[i]-1)*eps)/4
        v[1<<i]=(2*a[i]-1)/4-a[i]*eps
        mask=7^(1<<i)
        p[mask]=(a[i]+(1-2*a[i])*eps)/4
        v[mask]=(1+2*a[i])/4-a[i]*eps
    assert sum(p)==1 and sum(v)==0 and min(p)>0
    s=[R((-1)**(3-mask.bit_count())) for mask in range(8)]
    F=sum(vv*vv/pp for vv,pp in zip(v,p)); Z=sum(1/pp for pp in p)
    lp=sum(ss*vv/pp for ss,vv,pp in zip(s,v,p)); Fpair=F-lp*lp/Z
    C=(R(0),R(0))
    for i,j in [(0,1),(0,2),(1,2)]:
        ell=log_bound(p[0]*p[(1<<i)|(1<<j)]/(p[1<<i]*p[1<<j]))
        C=add(C,scale(R(-2),ell))
    lam=log_bound(p[7]*p[1]*p[2]*p[4]/(p[0]*p[3]*p[5]*p[6]))
    C=add(C,scale(-2*(1+eps),lam))
    gap=add((Fpair,Fpair),scale(-1,C)); B=add((F,F),scale(-1,C))
    assert gap[1]<0 and B[0]>0
    # Same-point independent projection through the six centered statistics.
    mp.mp.dps=120
    feats=[[R((mask&sub)==sub) for sub in [1,2,4,3,5,6]] for mask in range(8)]
    mean=[sum(p[k]*feats[k][i] for k in range(8)) for i in range(6)]
    cov=mp.matrix([[m(sum(p[k]*feats[k][i]*feats[k][j] for k in range(8))-mean[i]*mean[j]) for j in range(6)] for i in range(6)])
    deriv=mp.matrix([m(sum(v[k]*feats[k][i] for k in range(8))) for i in range(6)])
    direct=(deriv.T*mp.lu_solve(cov,deriv))[0]
    assert abs(direct-m(Fpair))<mp.mpf('1e-90')
    out=dict(status='RATIONAL_LOG_CERTIFICATE_PASSED',baseline=BASELINE,pid=os.getpid(),
             source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             python=sys.version,mpmath=mp.__version__,seed=None,kernel_calls=1,rejected=0,
             thread_env={k:os.environ.get(k) for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']},
             epsilon=fmt(eps),direction='I',feasible_chord_t=fmt(eps/2),
             endpoint_eigenvalues={sgn:[fmt(R(1,2)+j*eps/2)]*2+[fmt(eps+j*eps/2)] for sgn,j in [('minus',-1),('plus',1)]},
             event_order='empty,1,2,12,3,13,23,123',p=[fmt(x) for x in p],v=[fmt(x) for x in v],
             F_pair_exact=fmt(Fpair),F_pair=mp.nstr(m(Fpair),60),limit='577/18',
             C_interval=interval_decimal(C),F_pair_minus_C_interval=interval_decimal(gap),
             actual_B_interval=interval_decimal(B),
             covariance_projection_error=mp.nstr(abs(direct-m(Fpair)),10),
             logarithm_rule='80-term rational atanh series after exact reduction to [1,2); positive geometric tail',
             elapsed_seconds=time.time()-start,exit_status=0)
    Path('research/N3/falsification/rank2_projection_check.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out))

if __name__=='__main__':main()
