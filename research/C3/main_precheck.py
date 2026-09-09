"""Bounded mechanism preflight; finite diagnostics, never a rate certificate."""
import hashlib,json,os,platform,time
from pathlib import Path
import numpy as np
import sympy as sp

def mass(K):
    n=len(K); bits=(np.arange(2**n)[:,None]>>np.arange(n))&1
    M=np.broadcast_to(K,(2**n,n,n)).copy()
    M[:,np.arange(n),np.arange(n)]-=1-bits
    z=np.linalg.det(M)*(-1.)**(n-bits.sum(1))
    assert np.max(abs(z.imag))<1e-12 and min(z.real)>0
    return z.real,M,bits

def channel(P,ps,rs):
    out=P.copy();n=len(ps)
    for i,(p,r) in enumerate(zip(ps,rs)):
        for j in range(2**n):
            if not (j>>i)&1:
                k=j+(1<<i);v=out[j]+out[k]
                out[j],out[k]=r*out[j]+(1-r)*(1-p)*v,r*out[k]+(1-r)*p*v
    return out

def radial_check(K,ps,r):
    P,_,_=mass(K); n=len(K);B=np.diag(ps);A=K-B
    p,M,_=mass(B+r*A);inv=np.linalg.inv(M);X=inv@A
    p1=(p*np.trace(X,axis1=1,axis2=2)).real
    p2=(p*(np.trace(X,axis1=1,axis2=2)**2-np.trace(X@X,axis1=1,axis2=2))).real
    fisher=float(np.sum(p1*p1/p));acc=float(-p2@np.log(p))
    channel_error=float(np.max(abs(p-channel(P,ps,[r]*n))))
    assert channel_error<1e-12 and acc-fisher<1e-10
    return dict(r=r,channel_mass_error=channel_error,fisher=fisher,acceleration=acc,H_second=acc-fisher)

def exact_gauge():
    n=3;c=[sp.Rational(2,5),sp.Rational(1,12)+sp.I/30,sp.Rational(1,25)-sp.I/40]
    K=sp.Matrix(n,n,lambda i,j:c[i-j] if i>=j else sp.conjugate(c[j-i]))
    D=sp.Matrix(n,n,lambda i,j:sp.I*(i-j)*K[i,j]);E=sp.Matrix(n,n,lambda i,j:(i-j)**2*K[i,j])
    out=[]
    for mask in range(2**n):
        M=K-sp.diag(*[1-((mask>>i)&1) for i in range(n)]);sgn=(-1)**(n-mask.bit_count())
        p=sp.simplify(sgn*M.det());B=M.inv()*D
        p1=sp.simplify(p*sp.trace(B));p2=sp.simplify(p*(sp.trace(B)**2-sp.trace(B*B)))
        pe=sp.simplify(p*sp.trace(M.inv()*E))
        assert p>0 and p1==0 and sp.simplify(p2-pe)==0
        out.append(dict(mask=mask,p=str(p),p1=str(p1),p2=str(p2),p_E=str(pe)))
    return out

def main():
    started=time.time();n=5
    cs=[.45,.075+.025j,.035-.015j,.02+.01j]
    K=np.array([[cs[i-j] if 0<=i-j<len(cs) else np.conj(cs[j-i]) if 0<=j-i<len(cs) else 0 for j in range(n)] for i in range(n)])
    ps=np.array([.31,.42,.57,.63,.38])
    # Explicit deterministic noncommuting diagonal anchor, and a Toeplitz constant anchor.
    rows=[dict(anchor=p.tolist(),checks=[radial_check(K,p,r) for r in [.2,.6,1.]]) for p in [ps,np.full(n,.45)]]
    out=dict(status='COMPLETED_PREFLIGHT',pid=os.getpid(),exit_status=0,python=platform.python_version(),numpy=np.__version__,sympy=sp.__version__,threads={k:os.getenv(k) for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']},seed=None,source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),exact_gauge_atoms=exact_gauge(),radial_rows=rows,seconds=time.time()-started)
    Path('main_precheck.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(status=out['status'],pid=out['pid'],gauge_atoms=len(out['exact_gauge_atoms']),radial_H_second=[c['H_second'] for row in rows for c in row['checks']],seconds=out['seconds'])))

if __name__=='__main__':main()
