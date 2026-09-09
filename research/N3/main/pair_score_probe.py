"""U4: retain all one/two-site scores, omit only the triple-log score."""
import conditional_score_probe as base
from fractions import Fraction as Q
from decimal import Decimal,localcontext
from pathlib import Path
import numpy as np
import json,os,hashlib,time
g=base.g; r=base.r; HERE=Path(__file__).resolve().parent

def main():
    start=time.time(); records=[]; witnesses=[]
    inputs=json.loads((HERE/'projected_metric_results.json').read_text())['records']
    for item in inputs:
        K=g.spectral(g.quat(item['quaternion']),list(map(Q,item['eigenvalues'])))
        ev=g.evaluate(K,120); k=[K[i][j] for i,j in g.COORDS]; p=ev['p']
        jac=[[g.ev(f,k) for f in row] for row in g.GRAD]
        z=sum(1/x for x in p)
        ell=[sum(Q((-1)**(3-s.bit_count()))*jac[s][i]/p[s] for s in range(8)) for i in range(6)]
        with localcontext() as ctx:
            ctx.prec=110
            loss=[[g.dec(ell[i]*ell[j]/z) for j in range(6)] for i in range(6)]
            M=[[ev['B'][i][j]-loss[i][j] for j in range(6)] for i in range(6)]
            scales=[max(abs(M[i][i]),Decimal('1e-100')).sqrt() for i in range(6)]
            vals,vecs=np.linalg.eigh([[float(M[i][j]/scales[i]/scales[j]) for j in range(6)] for i in range(6)])
            d=[Q(float(vecs[i,0]/float(scales[i]))).limit_denominator(10**10) for i in range(6)]
            gap=sum(g.dec(d[i])*M[i][j]*g.dec(d[j]) for i in range(6) for j in range(6))
            true_B=sum(g.dec(d[i])*ev['B'][i][j]*g.dec(d[j]) for i in range(6) for j in range(6))
            red=r.reduction(K,120); opt=[red['schur_direction'][i][j] for i,j in g.COORDS]
            opt_gap=sum(opt[i]*M[i][j]*opt[j] for i in range(6) for j in range(6))
        row=dict(quaternion=item['quaternion'],eigenvalues=item['eigenvalues'],
                 minimum_normalized_eigenvalue=float(vals[0]),pair_projection_B=gap,true_B=true_B,
                 at_trace_optimizer_B=opt_gap)
        records.append(row)
        if gap<0: witnesses.append(dict(row,K=K,d=d))
    report=dict(status='SCOUT_ONLY',pid=os.getpid(),threads=1,seed=None,deterministic=True,
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                dependency_sha256=hashlib.sha256((HERE/'conditional_score_probe.py').read_bytes()).hexdigest(),
                input_sha256=hashlib.sha256((HERE/'projected_metric_results.json').read_bytes()).hexdigest(),
                command='python research/N3/main/pair_score_probe.py',executed_centers=len(records),
                pair_projection_failures=len(witnesses),trace_optimizer_failures=sum(x['at_trace_optimizer_B']<0 for x in records),
                records=records,witnesses=witnesses,elapsed_seconds=time.time()-start,exit_code=0)
    (HERE/'pair_score_results.json').write_text(json.dumps(g.encode(report),indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('records','witnesses')},indent=2),flush=True)

if __name__=='__main__': main()
