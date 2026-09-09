"""Deterministic author checks; no interval certification or random scan."""
import os, sys, json, platform
import mpmath as mp
mp.mp.dps = 100
E=[]
for i,j in [(0,0),(1,1),(2,2),(0,1),(0,2),(1,2)]:
    e=mp.zeros(3); e[i,j]=1; e[j,i]=1; E.append(e)
def trace(a): return sum(a[i,i] for i in range(3))
def event(v):
    x,y,z,a,b,c=v
    q=[x*y-a*a,x*z-b*b,y*z-c*c]
    r=x*y*z+2*a*b*c-x*c*c-y*b*b-z*a*a
    return mp.matrix([1-x-y-z+sum(q)-r,x-q[0]-q[1]+r,y-q[0]-q[2]+r,z-q[1]-q[2]+r,q[0]-r,q[1]-r,q[2]-r,r])
def calc(K):
    coords=[K[0,0],K[1,1],K[2,2],K[0,1],K[0,2],K[1,2]]
    p=event(coords); dp=mp.zeros(8,6)
    for i in range(6):
        vec=mp.diff(lambda t:event([coords[j]+(t if i==j else 0) for j in range(6)]),0)
        for s in range(8): dp[s,i]=vec[s]
    signs=mp.matrix([-1,1,1,1,-1,-1,-1,1])
    logs=mp.matrix([mp.log(t) for t in p]); Lam=(signs.T*logs)[0]
    ell=[mp.log(p[0]*p[4]/(p[1]*p[2])),mp.log(p[0]*p[5]/(p[1]*p[3])),mp.log(p[0]*p[6]/(p[2]*p[3]))]
    N=-mp.diag([ell[2],ell[1],ell[0]])-Lam*K
    inv=N**-1; d=mp.det(N)
    eta=mp.matrix([trace(inv*e) for e in E])
    G=mp.matrix([[trace(inv*e*inv*f) for f in E] for e in E])
    F=dp.T*mp.diag([1/t for t in p])*dp
    Z=sum(1/t for t in p)
    g=dp.T*mp.matrix([signs[s]/p[s] for s in range(8)])
    M=F-g*g.T/Z+d*G
    h=mp.lu_solve(M,eta); alpha=(eta.T*h)[0]; b=(g.T*h)[0]
    return d*alpha,b/mp.sqrt(Z),b,min(p)
def st(x): return mp.nstr(x,35)
def main():
    lam=mp.mpf(7)/10
    weights=[mp.mpf(1)/5,mp.mpf(3)/10,mp.mpf(1)/2]
    u=mp.matrix([mp.sqrt(x) for x in weights]); v=mp.matrix([-u[0],u[1],u[2]])
    delta=1-(u.T*v)[0]**2
    rows=[]
    for exponent in [6,12,24]:
        tau=mp.mpf(10)**(-exponent); L=-mp.log(tau)
        for r in [mp.mpf(0),mp.mpf(1)/4,mp.mpf(1)]:
            eps=tau*(1-r); t=tau*r
            K=(eps+t-2*eps*t)*mp.eye(3)+lam*((1-t)*u*u.T-t*v*v.T)
            da,beta,b,pmin=calc(K)
            detB=1-lam*r*delta
            rows.append(dict(tau=st(tau),r=st(r),dalpha=st(da),beta=st(beta),
                beta_ratio=st(beta/(-tau*mp.sqrt(detB)/(mp.sqrt(lam)*L))),
                gap_ratio=st((1-da)*lam*L),raw_beta_ratio=st(-lam*L*b),pmin=st(pmin)))
    print(json.dumps(dict(pid=os.getpid(),python=sys.version,platform=platform.platform(),mpmath=mp.__version__,digits=mp.mp.dps,
        thread_env={k:os.environ.get(k) for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']},
        inputs=dict(lam='7/10',weights=['1/5','3/10','1/2'],exponents=[6,12,24],ratios=['0','1/4','1']),rows=rows),indent=2))
if __name__=='__main__': main()
