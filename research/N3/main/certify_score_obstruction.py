"""Exact rational/log-interval certificate for a failed Fisher shortcut."""
import projected_metric_probe as proj
from fractions import Fraction as Q
from pathlib import Path
import json,os,time,hashlib
g=proj.g; HERE=Path(__file__).resolve().parent

def unit_log_bounds(x,terms=70):
    assert 1<=x<=2
    z=(x-1)/(x+1)
    lower=2*sum((z**(2*j+1)/Q(2*j+1) for j in range(terms)),Q(0))
    upper=lower+2*z**(2*terms+1)/(Q(2*terms+1)*(1-z*z))
    return lower,upper

def log_bounds(x):
    assert x>0
    power=0
    while x<1: x*=2; power-=1
    while x>2: x/=2; power+=1
    lo,hi=unit_log_bounds(x); l2,h2=unit_log_bounds(Q(2))
    return (lo+power*l2,hi+power*h2) if power>=0 else (lo+power*h2,hi+power*l2)

def compact(lo,hi):
    n=10**12
    return [str(Q((lo*n).__floor__(),n)),str(Q((hi*n).__ceil__(),n))]

def main():
    start=time.time()
    K=[[Q(v,100) for v in row] for row in ((30,29,15),(29,33,10),(15,10,16))]
    d=[Q(1),Q(1),Q(1,3),Q(0),Q(0),Q(0)]
    D=[[d[i] if i==j else Q(0) for j in range(3)] for i in range(3)]
    step=Q(1,100000)
    assert g.feasible(K) and g.feasible(g.ray(K,D,step)) and g.feasible(g.ray(K,D,-step))
    k=[K[i][j] for i,j in g.COORDS]
    p=[g.ev(f,k) for f in g.POLYS]
    dp=[sum(g.ev(f,k)*v for f,v in zip(row,d)) for row in g.GRAD]
    ddp=[sum(g.ev(row[i][j],k)*d[i]*d[j] for i in range(6) for j in range(6)) for row in g.HESS]
    F=sum(x*x/y for x,y in zip(dp,p))
    matrices=proj.lower_matrices(K)
    qs=[sum(d[i]*M[i][j]*d[j] for i in range(6) for j in range(6)) for M in matrices]
    clo=Q(0); chi=Q(0)
    for prob,acc in zip(p,ddp):
        lo,hi=log_bounds(prob); coeff=-acc
        clo+=coeff*(lo if coeff>=0 else hi)
        chi+=coeff*(hi if coeff>=0 else lo)
    assert max(qs)-clo<0, 'simplified witness does not refute shortcut'
    assert F-chi>0, 'must remain negative entropy curvature'
    report=dict(status='EXACT_SHORTCUT_COUNTEREXAMPLE_NOT_ENTROPY_COUNTEREXAMPLE',
                K=K,d=d,t=step,exact_feasibility=True,p=p,
                fisher_interval=compact(F,F),Q_intervals=[compact(v,v) for v in qs],
                cofactor_interval=compact(clo,chi),
                shortcut_gap_interval=compact(max(qs)-chi,max(qs)-clo),
                true_B_interval=compact(F-chi,F-clo),
                log_series_terms=70,log_remainder='2*z^(2*n+1)/((2*n+1)*(1-z^2)), |z|<=1/3',
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                dependencies={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                              [HERE/'projected_metric_probe.py',HERE/'conditional_score_probe.py',proj.base.DEP,proj.base.DEP.parent/'global_probe.py']},
                pid=os.getpid(),threads=1,deterministic=True,seed=None,executed_centers=1,
                command='python research/N3/main/certify_score_obstruction.py',
                elapsed_seconds=time.time()-start,exit_code=0)
    (HERE/'score_obstruction_certificate.json').write_text(json.dumps(g.encode(report),indent=2)+'\n')
    print(json.dumps(g.encode(report),indent=2),flush=True)

if __name__=='__main__': main()
