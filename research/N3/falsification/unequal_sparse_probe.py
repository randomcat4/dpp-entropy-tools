"""Bounded actual-event n=3 scout; no concavity certificate is inferred."""
import argparse, hashlib, itertools, json, os, platform, sys, time
from pathlib import Path
import mpmath as mp
import numpy as np
import scipy

BASELINE = 'fa504ec74e16843fafc395880d7ba99b4c1d2129'
SEED = 2026090913
PAIRS = [(0,0),(1,1),(2,2),(0,1),(0,2),(1,2)]

def det3(a):
    return (a[0,0]*(a[1,1]*a[2,2]-a[1,2]*a[2,1])
            -a[0,1]*(a[1,0]*a[2,2]-a[1,2]*a[2,0])
            +a[0,2]*(a[1,0]*a[2,1]-a[1,1]*a[2,0]))

def cofactor(a,i,j):
    r=[k for k in range(3) if k!=i]; c=[k for k in range(3) if k!=j]
    return (-1)**(i+j)*(a[r[0],c[0]]*a[r[1],c[1]]-a[r[0],c[1]]*a[r[1],c[0]])

def events(K):
    p=[]; jac=mp.matrix(8,6)
    for mask in range(8):
        M=mp.matrix(K)
        for i in range(3):
            if not (mask>>i)&1: M[i,i]-=1
        sign=(-1)**(3-mask.bit_count())
        p.append(sign*det3(M))
        for a,(i,j) in enumerate(PAIRS):
            jac[mask,a]=sign*(cofactor(M,i,j)+(cofactor(M,j,i) if i!=j else 0))
    return p,jac

def evaluate(K):
    p,J=events(K)
    if min(p)<=0: raise ValueError('nonpositive_event')
    ell=[mp.log(p[0]*p[6]/(p[2]*p[4])),mp.log(p[0]*p[5]/(p[1]*p[4])),mp.log(p[0]*p[3]/(p[1]*p[2]))]
    lam=mp.log(p[7]*p[1]*p[2]*p[4]/(p[0]*p[3]*p[5]*p[6]))
    N=-mp.diag(ell)-lam*K
    mp.cholesky(N)
    inv=N**-1; det=det3(N)
    E=[]
    for i,j in PAIRS:
        e=mp.zeros(3); e[i,j]=1; e[j,i]=1; E.append(e)
    eta=mp.matrix([sum((inv*e)[i,i] for i in range(3)) for e in E])
    F=J.T*mp.diag([1/x for x in p])*J
    A=F+mp.matrix(6,6)
    for i in range(6):
        for j in range(6):
            a=inv*E[i]*inv*E[j]
            A[i,j]+=det*sum(a[k,k] for k in range(3))
    d=mp.lu_solve(A,eta); rho=det*(eta.T*d)[0]
    D=sum((d[i]*E[i] for i in range(6)),mp.zeros(3))
    D/=max(abs(x) for x in D)
    return dict(rho=mp.nstr(rho,60), deficit=mp.nstr(1-rho,60), min_p=mp.nstr(min(p),15),
                K=[[mp.nstr(K[i,j],70) for j in range(3)] for i in range(3)],
                D=[[mp.nstr(D[i,j],70) for j in range(3)] for i in range(3)],
                normalization_residual=mp.nstr(abs(sum(p)-1),5))

def kernel(spec):
    ep=mp.mpf(10)**(-spec['digits'])
    soft=[mp.mpf(c)*ep**a for c,a in zip(['0.3','0.7','0.9'],spec['rates'])]
    raw=mp.matrix([mp.mpf(c)*ep**b for c,b in zip(['1','1.7','-0.6'],spec['sparse'])])
    theta={'fixed02':mp.mpf('.2'),'fixed07':mp.mpf('.7'),'fixed098':mp.mpf('.98'),
           'theta_to_zero':ep**mp.mpf('.5'),'theta_to_one':1-mp.sqrt(ep)}[spec['theta']]
    K=mp.diag(soft)+theta*(raw*raw.T)/(raw.T*raw)[0]
    # Sufficient strict feasibility: soft_i>0 and theta+max(soft)<1.
    assert min(soft)>0 and theta+max(soft)<1
    return K

def run(mode,out):
    begin=time.time()
    result=dict(status='RUNNING',baseline=BASELINE,source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                seed=SEED,randomness='none: deterministic parameter product',pid=os.getpid(),
                python=sys.version,numpy=np.__version__,scipy=scipy.__version__,mpmath=mp.__version__,
                thread_env={k:os.environ.get(k) for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']},
                command=f'python research/N3/falsification/unequal_sparse_probe.py --mode {mode} --output {out}',
                calls=0,accepted=0,rejected=0,anomalies=[],rows=[])
    specs=[dict(digits=d,rates=a,sparse=b,theta=t) for d,a,b,t in itertools.product(
        [3,9,18],[(1,2,3),(1,3,5),(3,1,2)],[(0,1,2),(0,0,1),(0,1,3),(0,2,2)],
        ['fixed02','fixed07','fixed098','theta_to_zero','theta_to_one'])]
    if mode=='smoke': specs=specs[:1]
    for spec in specs:
        result['calls']+=1
        mp.mp.dps=100+3*spec['digits']*max(spec['rates'])
        try:
            row=dict(spec=spec,dps=mp.mp.dps,**evaluate(kernel(spec)))
            result['accepted']+=1; result['rows'].append(row)
            if mp.mpf(row['rho'])>1: result['anomalies'].append(row)
        except (ValueError, ZeroDivisionError) as exc:
            result['rejected']+=1; result['anomalies'].append(dict(spec=spec,error=str(exc)))
    result['best']=sorted(result['rows'],key=lambda r:mp.mpf(r['rho']),reverse=True)[:8]
    result['status']='INCOMPLETE'; result['exit_status']=0; result['elapsed_seconds']=time.time()-begin
    Path(out).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','pid','calls','accepted','rejected','elapsed_seconds']}))
    print('best_rho',result['best'][0]['rho'])

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--mode',choices=['smoke','batch'],default='batch')
    parser.add_argument('--output',required=True); args=parser.parse_args(); run(args.mode,args.output)
