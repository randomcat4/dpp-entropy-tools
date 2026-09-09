"""Bounded exact-input beta-slice diagnostic; no approximate zero is certified."""
import os,sys
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'): os.environ[key]='1'
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as Q
from decimal import Decimal,localcontext
import importlib.util,json,time,hashlib,platform
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[3]
DEP=ROOT/'research/N3/main/conditional_score_probe.py'
spec=importlib.util.spec_from_file_location('first_round_core',DEP)
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
g=base.g;r=base.r

def quantities(K,precision=100):
    assert g.feasible(K)
    result=r.reduction(K,precision)
    x=[K[i][j] for i,j in g.COORDS]
    p=[g.ev(f,x) for f in g.POLYS]
    jac=[[g.ev(f,x) for f in row] for row in g.GRAD]
    Z=sum(1/v for v in p)
    ell=[sum(Q((-1)**(3-s.bit_count()))*jac[s][i]/p[s] for s in range(8)) for i in range(6)]
    with localcontext() as ctx:
        ctx.prec=precision-10
        H=[[result['A'][i][j]-g.dec(ell[i]*ell[j]/Z) for j in range(6)] for i in range(6)]
        h=r.solve(H,result['eta'])
        alpha=sum(a*b for a,b in zip(h,result['eta']))
        beta_numerator=sum(g.dec(a)*b for a,b in zip(ell,h))
        v=[g.dec(a)/g.dec(Z).sqrt() for a in ell]
        beta=beta_numerator/g.dec(Z).sqrt()
        invv=r.solve(H,v);gamma=sum(a*b for a,b in zip(v,invv))
        d=result['N_determinant'];rho=d*(alpha-beta*beta/(1+gamma))
        assert abs(rho-result['rho'])<Decimal(10)**(-precision+30)
    return dict(K=K,alpha=alpha,beta=beta,beta_numerator=beta_numerator,
                gamma=gamma,d_alpha=d*alpha,rho=rho,Lambda=g.evaluate(K,precision)['triple'],
                precision=precision,strict_feasibility=True,min_probability=min(p))

def main():
    start=time.time();rows=[]
    families=[('half_path',(50,50,50),(12,17,0)),('half_triangle',(50,50,50),(12,17,8)),
              ('opposite_triangle',(50,50,50),(12,17,-8)),('asymmetric',(40,55,65),(12,17,8)),
              ('stationary_obstruction',(51,48,52),(24,-24,-24))]
    for name,diag,edges in families:
        K=[[Q(diag[i],100) if i==j else Q(0) for j in range(3)] for i in range(3)]
        for val,(i,j) in zip(edges,g.COORDS[3:]): K[i][j]=K[j][i]=Q(val,100)
        for shift in (Q(-1,20),Q(0),Q(1,20)):
            J=[[K[i][j]+shift*Q(i==j) for j in range(3)] for i in range(3)]
            if not g.feasible(J): rows.append(dict(family=name,shift=shift,status='INFEASIBLE'));continue
            row=quantities(J);row.update(family=name,shift=shift,status='SCOUT');rows.append(row)
    report=dict(status='SCOUT_NO_EXACT_ZERO_INFERENCE',pid=os.getpid(),threads=1,seed=None,deterministic=True,
                baseline='e476db1bb056af57e883a47f470ea0f4443c1837',python=platform.python_version(),
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                dependency_sha256=hashlib.sha256(DEP.read_bytes()).hexdigest(),
                command='python research/N3/round2/main/beta_probe.py',attempted_centers=len(rows),
                executed_centers=sum(x['status']=='SCOUT' for x in rows),rows=rows,
                elapsed_seconds=time.time()-start,exit_code=0)
    (HERE/'beta_probe.json').write_text(json.dumps(g.encode(report),indent=2)+'\n')
    for row in rows: print(row['family'],row['shift'],str(row.get('beta')),str(row.get('d_alpha')),flush=True)
    print('PID',report['pid'],'coverage',report['executed_centers'],'exit',0,flush=True)
if __name__=='__main__':main()
