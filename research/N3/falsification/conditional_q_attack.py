"""Test the proposed conditional-determinant Fisher lower bound, not H itself."""
import hashlib,json,os,sys,time
from pathlib import Path
import numpy as np
import mpmath as mp
from scipy.optimize import minimize
from unequal_sparse_probe import BASELINE, PAIRS, events, kernel, det3

def objects(K):
    p,J=events(K)
    ell=[mp.log(p[0]*p[6]/(p[2]*p[4])),mp.log(p[0]*p[5]/(p[1]*p[4])),mp.log(p[0]*p[3]/(p[1]*p[2]))]
    lam=mp.log(p[7]*p[1]*p[2]*p[4]/(p[0]*p[3]*p[5]*p[6]))
    N=-mp.diag(ell)-lam*K; inv=N**-1; det=det3(N)
    E=[]
    for i,j in PAIRS:
        e=mp.zeros(3); e[i,j]=1; e[j,i]=1; E.append(e)
    eta=mp.matrix([sum((inv*e)[i,i] for i in range(3)) for e in E])
    G=mp.matrix(6,6)
    for i in range(6):
        for j in range(6):
            z=inv*E[i]*inv*E[j]; G[i,j]=det*sum(z[k,k] for k in range(3))
    Q=[]
    for k in range(3):
        q=mp.zeros(6); q[k,k]=1/(K[k,k]*(1-K[k,k]))
        others=[i for i in range(3) if i!=k]
        for state in [0,1]:
            idx=[(state<<k)|((b&1)<<others[0])|(((b>>1)&1)<<others[1]) for b in range(4)]
            a,b,c,d=[p[i] for i in idx]; m=a+b+c+d; delta=a*d-b*c
            V=a*d*(a+d)+b*c*(b+c)-4*delta**2/m
            assert V>0
            v=mp.matrix([d*J[idx[0],j]+a*J[idx[3],j]-c*J[idx[1],j]-b*J[idx[2],j]
                         -2*delta*sum(J[i,j] for i in idx)/m for j in range(6)])
            q+=v*v.T/V
        Q.append(q)
    return Q,G,eta,det,E

def attack(spec):
    mp.mp.dps=110+3*spec['digits']*max(spec['rates'])
    K=kernel(spec); Q,G,eta,det,E=objects(K)
    calls=0
    def calc(weights):
        nonlocal calls
        calls+=1
        A=G+sum((mp.mpf(float(weights[i]))*Q[i] for i in range(3)),mp.zeros(6))
        v=mp.lu_solve(A,eta); d=v/(eta.T*v)[0]
        h=1/((eta.T*v)[0]*det)
        grad=[(d.T*q*d)[0]/det for q in Q]
        return h,grad,d
    def fun(w):
        h,g,_=calc(w); return -float(h),-np.array([float(x) for x in g])
    opt=minimize(fun,[1/3]*3,jac=True,method='SLSQP',bounds=[(0,1)]*3,
                 constraints=[dict(type='eq',fun=lambda w:sum(w)-1,jac=lambda w:np.ones(3))],
                 options=dict(maxiter=120,ftol=1e-12))
    h,_,d=calc(opt.x)
    C=det-(d.T*G*d)[0]
    gaps=[((d.T*q*d)[0]-C)/det for q in Q]
    D=sum((d[i]*E[i] for i in range(6)),mp.zeros(3)); D/=max(abs(x) for x in D)
    return dict(spec=spec,optimizer_success=bool(opt.success),optimizer_message=opt.message,
                optimizer_calls=calls,weights=opt.x.tolist(),minimax_dual=mp.nstr(h,45),
                normalized_gaps=[mp.nstr(x,45) for x in gaps],max_gap=mp.nstr(max(gaps),45),
                D=[[mp.nstr(D[i,j],60) for j in range(3)] for i in range(3)])

def main():
    start=time.time(); rows=json.loads(Path('research/N3/falsification/batch.json').read_text())['rows']
    selected=sorted(rows,key=lambda r:mp.mpf(r['rho']),reverse=True)[:36]
    results=[attack(r['spec']) for r in selected]
    out=dict(status='INCOMPLETE',baseline=BASELINE,pid=os.getpid(),seed=None,
             selection='36 highest actual DPP rho among the fixed 180 first-unit points',
             source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             calls=len(results),rejected=0,optimizer_calls=sum(x['optimizer_calls'] for x in results),
             rows=results,best=min(results,key=lambda r:mp.mpf(r['max_gap'])),
             elapsed_seconds=time.time()-start,exit_status=0)
    Path('research/N3/falsification/conditional_q.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['status','pid','calls','optimizer_calls','elapsed_seconds']})); print(json.dumps(out['best']))

if __name__=='__main__': main()
