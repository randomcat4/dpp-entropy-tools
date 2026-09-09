"""Exact rational outward-rounded interval certificate on one fixed affine family."""
import hashlib,json,math,os,sys,time
from pathlib import Path
from fractions import Fraction as R
import mpmath as mp
from beta_affine_probe import BASELINE,families,midpoint,feasible,mm,data,fmt
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'falsification'))
from rank2_projection_check import log_bound

BITS=240; DEN=2**BITS
class I:
    def __init__(self,a,b=None):
        if isinstance(a,I): self.lo,self.hi=a.lo,a.hi;return
        a=R(a);b=a if b is None else R(b);assert a<=b
        self.lo=R((a*DEN).__floor__(),DEN);self.hi=R((b*DEN).__ceil__(),DEN)
    def __add__(self,o):
        o=I(o);return I(self.lo+o.lo,self.hi+o.hi)
    __radd__=__add__
    def __neg__(self):return I(-self.hi,-self.lo)
    def __sub__(self,o):return self+-I(o)
    def __rsub__(self,o):return I(o)+-self
    def __mul__(self,o):
        o=I(o);v=[a*b for a in [self.lo,self.hi] for b in [o.lo,o.hi]];return I(min(v),max(v))
    __rmul__=__mul__
    def __truediv__(self,o):
        o=I(o);assert not o.lo<=0<=o.hi,'zero interval pivot'
        return self*I(1/o.hi,1/o.lo)
    def __rtruediv__(self,o):return I(o)/self

def eye(n):return [[I(i==j) for j in range(n)] for i in range(n)]
def prod(A,B):return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def transpose(A):return [list(x) for x in zip(*A)]
def tr(A):return sum(A[i][i] for i in range(len(A)))
def det(A):return A[0][0]*(A[1][1]*A[2][2]-A[1][2]*A[2][1])-A[0][1]*(A[1][0]*A[2][2]-A[1][2]*A[2][0])+A[0][2]*(A[1][0]*A[2][1]-A[1][1]*A[2][0])
def cof(A,i,j):
    r=[k for k in range(3) if k!=i];c=[k for k in range(3) if k!=j]
    return (-1)**(i+j)*(A[r[0]][c[0]]*A[r[1]][c[1]]-A[r[0]][c[1]]*A[r[1]][c[0]])
def solve(A,b):
    A=[list(row)+[b[i]] for i,row in enumerate(A)];n=len(b)
    for k in range(n):
        # Fixed-pivot Gaussian elimination. Any zero-containing pivot aborts.
        for j in range(k+1,n):
            q=A[j][k]/A[k][k]
            for l in range(k+1,n+1):A[j][l]=A[j][l]-q*A[k][l]
            A[j][k]=I(0)
    x=[I(0)]*n
    for k in reversed(range(n)):x[k]=(A[k][n]-sum(A[k][j]*x[j] for j in range(k+1,n)))/A[k][k]
    return x
def logi(x):
    assert x.lo>0
    return I(log_bound(x.lo)[0],log_bound(x.hi)[1])
def event_data(K):
    p=[];J=[];pairs=[(0,0),(1,1),(2,2),(0,1),(0,2),(1,2)]
    for mask in range(8):
        M=[list(row) for row in K]
        for i in range(3):
            if not (mask>>i)&1:M[i][i]=M[i][i]-1
        s=(-1)**(3-mask.bit_count());p.append(s*det(M))
        J.append([s*(cof(M,i,j)+(cof(M,j,i) if i!=j else 0)) for i,j in pairs])
    return p,J,pairs

def certify(A,B,tlo,thi):
    t=I(tlo,thi);K=[[I(A[i][j])+t*(B[i][j]-A[i][j]) for j in range(3)] for i in range(3)]
    p,J,pairs=event_data(K);assert min(x.lo for x in p)>0
    Z=sum(1/x for x in p);s=[(-1)**(3-i.bit_count()) for i in range(8)]
    g=[sum(s[k]*J[k][j]/p[k] for k in range(8)) for j in range(6)]
    Fpair=[[sum(J[k][i]*J[k][j]/p[k] for k in range(8))-g[i]*g[j]/Z for j in range(6)] for i in range(6)]
    ell=[logi(p[0]*p[6]/(p[2]*p[4])),logi(p[0]*p[5]/(p[1]*p[4])),logi(p[0]*p[3]/(p[1]*p[2]))]
    lam=logi(p[7]*p[1]*p[2]*p[4]/(p[0]*p[3]*p[5]*p[6]))
    N=[[-lam*K[i][j]-(ell[i] if i==j else I(0)) for j in range(3)] for i in range(3)]
    d=det(N);assert d.lo>0
    adj=[[cof(N,j,i) for j in range(3)] for i in range(3)]
    E=[]
    for i,j in pairs:
        e=[[I(0) for _ in range(3)] for _ in range(3)];e[i][j]=I(1);e[j][i]=I(1);E.append(e)
    ae=[tr(prod(adj,e)) for e in E]
    Ht=[[d*Fpair[i][j]+tr(prod(prod(prod(adj,E[i]),adj),E[j])) for j in range(6)] for i in range(6)]
    h=solve(Ht,ae);b=sum(g[i]*h[i] for i in range(6));da=sum(ae[i]*h[i] for i in range(6))
    return dict(beta_times_sqrtZ=b,dalpha=da,min_p=I(min(x.lo for x in p),min(x.hi for x in p)),detN=d)

def serial(obj):
    if isinstance(obj,I):
        n=10**35;lo=(obj.lo*n).__floor__();hi=(obj.hi*n).__ceil__()
        return dict(lower=str(R(lo,n)),upper=str(R(hi,n)),approx_lower=mp.nstr(mp.mpf(lo)/n,25),approx_upper=mp.nstr(mp.mpf(hi)/n,25))
    if isinstance(obj,dict):return {k:serial(v) for k,v in obj.items()}
    return obj

def main():
    start=time.time();mp.mp.dps=160
    f=next(x for x in families() if x['name']=='rank_one_to_twisted_complement_100');A,B=f['A'],f['B']
    assert feasible(A) and feasible(B)
    left=R(0);right=R(1,8);track=[]
    # 42 finite bisection steps locate one root bracket; no random exploration.
    for _ in range(42):
        mid=(left+right)/2;b,da,rho=data(mm(midpoint(A,B,mid)))
        track.append(dict(t=str(mid),beta=mp.nstr(b,40)))
        if b<0:left=mid
        else:right=mid
    certified={}
    for name,l,r in [('original_negative',R(0),R(0)),('original_positive',R(1,8),R(1,8)),('root_left',left,left),('root_right',right,right),('root_entire_bracket',left,right)]:
        certified[name]=certify(A,B,l,r)
    assert certified['original_negative']['beta_times_sqrtZ'].hi<0
    assert certified['original_positive']['beta_times_sqrtZ'].lo>0
    assert certified['root_left']['beta_times_sqrtZ'].hi<0
    assert certified['root_right']['beta_times_sqrtZ'].lo>0
    assert certified['root_entire_bracket']['dalpha'].hi<1
    out=dict(status='CERTIFIED_BETA_ZERO_EXISTS_WITH_DALPHA_LT_ONE',baseline=BASELINE,pid=os.getpid(),
             source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),python=sys.version,mpmath=mp.__version__,
             seed=None,interval_bits=BITS,family=f['name'],A=fmt(A),B=fmt(B),
             bisection_calls=42,interval_calls=5,rejected=0,root_bracket=[str(left),str(right)],
             certificate=serial(certified),bisection_trace=track,elapsed_seconds=time.time()-start,exit_status=0)
    Path('research/N3/round2/falsification/root_certificate.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['status','pid','bisection_calls','interval_calls','root_bracket','certificate','elapsed_seconds']}))

if __name__=='__main__':main()
