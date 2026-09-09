"""U5: bounded targeted falsification of the projection at the actual A optimizer."""
import projected_metric_probe as proj
from fractions import Fraction as Q
from decimal import Decimal,localcontext
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from scipy.special import expit
import json,os,time,hashlib
g=proj.g; r=proj.r; HERE=Path(__file__).resolve().parent

def center(x):
    rotation=np.eye(3)
    for angle,(i,j) in zip(x[3:],((0,1),(0,2),(1,2))):
        R=np.eye(3); R[i,i]=R[j,j]=np.cos(angle); R[i,j]=-np.sin(angle); R[j,i]=np.sin(angle)
        rotation=rotation@R
    K=rotation@np.diag(expit(x[:3]))@rotation.T
    out=[[Q(0)]*3 for _ in range(3)]
    for i in range(3):
        for j in range(i,3): out[i][j]=out[j][i]=Q(float(K[i,j])).limit_denominator(10**12)
    return out

def evaluate(K):
    assert g.feasible(K)
    red=r.reduction(K,110); mats=proj.lower_matrices(K)
    with localcontext() as ctx:
        ctx.prec=95
        raw=[red['schur_direction'][i][j] for i,j in g.COORDS]
        size=max(map(abs,raw)); d=[Q(str(v/size)) for v in raw]
        qs=[sum(d[i]*M[i][j]*d[j] for i in range(6) for j in range(6)) for M in mats]
        A=sum(g.dec(d[i])*red['A'][i][j]*g.dec(d[j]) for i in range(6) for j in range(6))
        trace=sum(g.dec(d[i])*red['eta'][i] for i in range(6))
        correction=red['N_determinant']*trace**2
        D=[[Decimal(0)]*3 for _ in range(3)]
        for v,(i,j) in zip(d,g.COORDS): D[i][j]=D[j][i]=g.dec(v)
        W=r.mm(r.inverse(red['N']),D)
        geometry=red['N_determinant']*r.trace(r.mm(W,W))
        cofactor=correction-geometry
        gap=(g.dec(max(qs))-cofactor)/A
        return dict(gap=gap,true_B_over_A=(A-correction)/A,rho=red['rho'],K=K,d=d,
                    cofactor_over_A=cofactor/A,precision=110)

def main():
    start=time.time(); ledger=[]; best=None; outcomes=[]
    starts=[[-12,-1.4,1.4,.8,.4,1.1],[-2.2,-.7,2.2,.2,1.2,.7],
            [-1.4,-.8,.8,1.3,.6,2.0],[-.04,0,.04,.5,.9,1.4]]
    for idx,x0 in enumerate(starts):
        def objective(x):
            nonlocal best
            try:
                rec=evaluate(center(x)); value=float(rec['gap']); rec['status']='EVALUATED'
                if best is None or rec['gap']<best['gap']: best=rec
                row={k:v for k,v in rec.items() if k not in ('K','d')}
            except (AssertionError,ZeroDivisionError,ValueError) as e:
                value=10.; row=dict(status='REJECTED',reason=type(e).__name__)
            ledger.append(dict(start=idx,x=[float(v) for v in x],objective=value,**row))
            return value
        result=minimize(objective,x0,method='Nelder-Mead',bounds=[(-18,18)]*3+[(-3.14159,3.14159)]*3,
                        options=dict(maxfev=128,xatol=1e-6,fatol=1e-10))
        outcomes.append(dict(start=idx,nfev=result.nfev,success=bool(result.success),message=str(result.message),fun=float(result.fun)))
    report=dict(status='SCOUT_ONLY',pid=os.getpid(),threads=1,seed=None,deterministic=True,
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                dependency_sha256=hashlib.sha256((HERE/'projected_metric_probe.py').read_bytes()).hexdigest(),
                command='python research/N3/main/stationary_projection_search.py',starts=starts,
                call_limit_per_start=128,actual_calls=len(ledger),rejections=sum(x['status']=='REJECTED' for x in ledger),
                negative_projection_gaps=sum(x.get('gap',0)<0 for x in ledger),outcomes=outcomes,best=best,ledger=ledger,
                elapsed_seconds=time.time()-start,exit_code=0)
    (HERE/'stationary_projection_results.json').write_text(json.dumps(g.encode(report),indent=2)+'\n')
    print(json.dumps(g.encode({k:v for k,v in report.items() if k not in ('ledger','best')}),indent=2),flush=True)
    print('best gap',str(best['gap']),'rho',str(best['rho']),flush=True)

if __name__=='__main__': main()
