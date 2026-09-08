"""Bounded U1 probe of a conditional-determinant Fisher lower bound."""
import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[name]='1'
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as Q
from decimal import Decimal, localcontext
import importlib.util, json, hashlib, time, platform
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
DEP=ROOT/'research/R3/deepening_10h/dense_hessian/n3_global_full_hessian/rank_one_recheck.py'
spec=importlib.util.spec_from_file_location('inherited_reduction',DEP)
r=importlib.util.module_from_spec(spec); spec.loader.exec_module(r)
g=r.g

def case(K):
    assert g.feasible(K)
    red=r.reduction(K,120)
    d0=[red['schur_direction'][i][j] for i,j in g.COORDS]
    largest=max(map(abs,d0))
    with localcontext() as ctx:
        ctx.prec=60
        d=[Q(str(v/largest)) for v in d0]
    k=[K[i][j] for i,j in g.COORDS]
    p=[g.ev(f,k) for f in g.POLYS]
    dp=[sum(g.ev(f,k)*di for f,di in zip(row,d)) for row in g.GRAD]
    fisher=sum(v*v/w for v,w in zip(dp,p))
    bounds=[]
    for c in range(3):
        pair=[i for i in range(3) if i!=c]
        bound=d[c]**2/(K[c][c]*(1-K[c][c]))
        for bit in (0,1):
            base=bit<<c
            ids=[base,base|(1<<pair[0]),base|(1<<pair[1]),base|(1<<pair[0])|(1<<pair[1])]
            a,b,cc,dd=[p[s] for s in ids]
            ap,bp,cp,ddp=[dp[s] for s in ids]
            m=a+b+cc+dd; mp=ap+bp+cp+ddp
            delta=a*dd-b*cc
            delta_prime=ap*dd+a*ddp-bp*cc-b*cp
            variance=a*dd*(a+dd)+b*cc*(b+cc)-4*delta**2/m
            centered=delta_prime-2*delta*mp/m
            assert variance>0
            bound+=centered**2/variance
        assert bound<=fisher
        bounds.append(bound)
    with localcontext() as ctx:
        ctx.prec=110
        D=[[Decimal(0)]*3 for _ in range(3)]
        for v,(i,j) in zip(d,g.COORDS): D[i][j]=D[j][i]=g.dec(v)
        inv=r.inverse(red['N']); W=r.mm(inv,D)
        cofactor=red['N_determinant']*(r.trace(W)**2-r.trace(r.mm(W,W)))
        residual=g.dec(fisher)-cofactor
        shortfall=g.dec(max(bounds))-cofactor
    return dict(K=K,d=d,rho=red['rho'],fisher=fisher,conditional_bounds=bounds,
                cofactor=cofactor,total_B=residual,best_bound_B=shortfall,
                bound_suffices_at_trace_optimizer=shortfall>=0,
                exact_feasibility=True,precision=120)

def main():
    start=time.time(); records=[]
    profiles=[(Q(1,7),Q(2,5),Q(5,6)),(Q(1,100),Q(1,9),Q(2,3)),
              (Q(1,10000),Q(1,100),Q(3,5)),(Q(1,10**8),Q(1,10**4),Q(7,10))]
    for quat in ((1,2,3,5),(2,1,4,3),(3,2,1,7)):
        for lam in profiles:
            row=case(g.spectral(g.quat(quat),lam)); row['quaternion']=quat; row['eigenvalues']=lam
            records.append(row)
    result=dict(status='BOUNDED_EXPLORATORY_PROBE',baseline='fa504ec74e16843fafc395880d7ba99b4c1d2129',
                pid=os.getpid(),seed=None,deterministic=True,python=platform.python_version(),
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                dependency_sha256=hashlib.sha256(DEP.read_bytes()).hexdigest(),
                atom_dependency_sha256=hashlib.sha256((DEP.parent/'global_probe.py').read_bytes()).hexdigest(),
                command='python research/N3/main/conditional_score_probe.py',
                threads=1,executed_centers=len(records),rejections=0,
                bound_failures=sum(not x['bound_suffices_at_trace_optimizer'] for x in records),
                entropy_violations=sum(x['total_B']<0 for x in records),records=records,
                elapsed_seconds=time.time()-start,exit_code=0)
    (HERE/'conditional_score_results.json').write_text(json.dumps(g.encode(result),indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2),flush=True)

if __name__=='__main__': main()
