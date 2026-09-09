"""U2: test all directions of the averaged conditional-score lower bound."""
import conditional_score_probe as base
from fractions import Fraction as Q
from decimal import Decimal, localcontext
from pathlib import Path
import numpy as np
import os,json,time,hashlib
g=base.g; r=base.r; HERE=Path(__file__).resolve().parent

def lower_matrices(K):
    k=[K[i][j] for i,j in g.COORDS]
    p=[g.ev(f,k) for f in g.POLYS]
    jac=[[g.ev(f,k) for f in row] for row in g.GRAD]
    matrices=[]
    for c in range(3):
        M=[[Q(0)]*6 for _ in range(6)]
        M[c][c]=1/(K[c][c]*(1-K[c][c]))
        pair=[i for i in range(3) if i!=c]
        for bit in (0,1):
            b0=bit<<c; ids=[b0,b0|1<<pair[0],b0|1<<pair[1],b0|1<<pair[0]|1<<pair[1]]
            a,b,cc,d=[p[s] for s in ids]; m=a+b+cc+d; delta=a*d-b*cc
            V=a*d*(a+d)+b*cc*(b+cc)-4*delta**2/m
            v=[d*jac[ids[0]][j]-cc*jac[ids[1]][j]-b*jac[ids[2]][j]+a*jac[ids[3]][j]
               -2*delta*sum(jac[s][j] for s in ids)/m for j in range(6)]
            for i in range(6):
                for j in range(6): M[i][j]+=v[i]*v[j]/V
        matrices.append(M)
    return matrices

def main():
    start=time.time(); records=[]; witnesses=[]
    profiles=[(Q(1,7),Q(2,5),Q(5,6)),(Q(1,100),Q(1,9),Q(2,3)),
              (Q(1,10000),Q(1,100),Q(3,5)),(Q(1,10**8),Q(1,10**4),Q(7,10)),
              (Q(49,100),Q(1,2),Q(51,100)),(Q(1,10**8),Q(1,5),Q(4,5))]
    for quat in ((1,2,3,5),(2,1,4,3),(3,2,1,7),(10,1,1,1),(1,0,2,4),(1,3,10,2)):
        for lam in profiles:
            K=g.spectral(g.quat(quat),lam); assert g.feasible(K)
            ev=g.evaluate(K,120); mats=lower_matrices(K)
            kval=[K[i][j] for i,j in g.COORDS]; p=ev['p']
            jac=[[g.ev(f,kval) for f in row] for row in g.GRAD]
            F=[[sum(jac[s][i]*jac[s][j]/p[s] for s in range(8)) for j in range(6)] for i in range(6)]
            with localcontext() as ctx:
                ctx.prec=110
                Qavg=[[sum(M[i][j] for M in mats)/3 for j in range(6)] for i in range(6)]
                Bq=[[ev['B'][i][j]-g.dec(F[i][j])+g.dec(Qavg[i][j]) for j in range(6)] for i in range(6)]
                scales=[max(abs(Bq[i][i]),Decimal('1e-100')).sqrt() for i in range(6)]
                norm=np.array([[float(Bq[i][j]/scales[i]/scales[j]) for j in range(6)] for i in range(6)])
                values,vecs=np.linalg.eigh(norm)
                d=[Q(float(vecs[i,0]/float(scales[i]))).limit_denominator(10**10) for i in range(6)]
                qs=[sum(d[i]*M[i][j]*d[j] for i in range(6) for j in range(6)) for M in mats]
                total=sum(g.dec(d[i])*ev['B'][i][j]*g.dec(d[j]) for i in range(6) for j in range(6))
                fish=sum(d[i]*F[i][j]*d[j] for i in range(6) for j in range(6))
                cof=g.dec(fish)-total
                gaps=[g.dec(x)-cof for x in qs]
            row=dict(quaternion=quat,eigenvalues=lam,minimum_normalized_eigenvalue=float(values[0]),
                     max_bound_gap=max(gaps),average_bound_gap=sum(gaps)/3,true_B=total)
            records.append(row)
            if values[0]<-1e-9:
                witnesses.append(dict(row,K=K,d=d,individual_bounds=qs,Fisher=fish,cofactor=cof))
    report=dict(status='SCOUT_ONLY',pid=os.getpid(),threads=1,deterministic=True,seed=None,
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                source_dependency_sha256=hashlib.sha256((HERE/'conditional_score_probe.py').read_bytes()).hexdigest(),
                command='python research/N3/main/projected_metric_probe.py',executed_centers=len(records),
                averaged_bound_failures=len(witnesses),max_bound_witnesses=sum(x['max_bound_gap']<0 for x in witnesses),
                records=records,witnesses=witnesses,elapsed_seconds=time.time()-start,exit_code=0)
    (HERE/'projected_metric_results.json').write_text(json.dumps(g.encode(report),indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('records','witnesses')},indent=2),flush=True)

if __name__=='__main__': main()
