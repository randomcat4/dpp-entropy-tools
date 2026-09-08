"""Exact rational-log congruence gate for one frozen global-scout point."""
import sys
sys.dont_write_bytecode=True
sys.set_int_max_str_digits(0)
from pathlib import Path
from fractions import Fraction as F
import importlib.util,json,time,hashlib
import numpy as np
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('own_global_probe',HERE/'global_probe.py'); g=importlib.util.module_from_spec(spec); spec.loader.exec_module(g)

def unit_log(x,N=32):
    assert 1<=x<=2; z=(x-1)/(x+1)
    lo=2*sum(z**(2*k+1)/F(2*k+1) for k in range(N))
    return lo,lo+2*z**(2*N+1)/(F(2*N+1)*(1-z*z))
def log_bounds(x):
    k=0
    while x<1: x*=2; k-=1
    while x>=2: x/=2; k+=1
    lo,hi=unit_log(x); a,b=unit_log(F(2))
    return (lo+k*a,hi+k*b) if k>=0 else (lo+k*b,hi+k*a)
def main():
    start=time.time(); scout=json.loads((HERE/'scout_results.json').read_text()); r=scout['worst']
    K=[[F(v) for v in row] for row in r['K']]; k=[K[i][j] for i,j in g.COORDS]
    p=[g.ev(poly,k) for poly in g.POLYS]; logs=[log_bounds(x) for x in p]
    grad=[[g.ev(poly,k) for poly in row] for row in g.GRAD]
    hess=[[[g.ev(poly,k) for poly in row] for row in mat] for mat in g.HESS]
    B=[]
    for i in range(6):
        row=[]
        for j in range(6):
            fish=sum(grad[s][i]*grad[s][j]/p[s] for s in range(8)); lo=hi=fish
            for s in range(8):
                c=hess[s][i][j]; a,b=logs[s]
                lo+=c*(a if c>=0 else b); hi+=c*(b if c>=0 else a)
            row.append((lo,hi))
        B.append(row)
    midpoint=np.array([[float((a+b)/2) for a,b in row] for row in B]); proposal=np.linalg.inv(np.linalg.cholesky(midpoint).T)
    attempts=[]
    for cap in (4096,65536,1000000):
        P=[[F(float(proposal[i,j])).limit_denominator(cap) if i<=j else F(0) for j in range(6)] for i in range(6)]
        assert min(P[i][i] for i in range(6))>0
        T=[]
        for a in range(6):
            row=[]
            for b in range(6):
                lo=hi=F(0)
                for i in range(6):
                    for j in range(6):
                        c=P[i][a]*P[j][b]; l,u=B[i][j]
                        lo+=c*(l if c>=0 else u); hi+=c*(u if c>=0 else l)
                row.append((lo,hi))
            T.append(row)
        rows=[T[i][i][0]-sum(max(map(abs,T[i][j])) for j in range(6) if j!=i) for i in range(6)]
        attempts.append(dict(cap=cap,P=P,transformed=T,row_margins=rows,passed=min(rows)>0))
        if min(rows)>0: break
    assert attempts[-1]['passed']
    margin=F(1,2000000); left=[[K[i][j]-margin*F(i==j) for j in range(3)] for i in range(3)]
    right=[[F(i==j)-K[i][j]-margin*F(i==j) for j in range(3)] for i in range(3)]
    piv1,piv2=g.ldl(left),g.ldl(right); assert piv1 and piv2
    report=dict(status='FROZEN_POINT_PD_CERTIFICATE_CANDIDATE_ONLY',scout_index=r['index'],K=K,atoms=p,B_intervals=B,attempts=attempts,
        spectral_margin=margin,ldl_K_minus_margin=piv1,ldl_I_minus_K_minus_margin=piv2,
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),dependency_sha256=hashlib.sha256((HERE/'global_probe.py').read_bytes()).hexdigest(),elapsed_seconds=time.time()-start,exit_code=0)
    (HERE/'point_interval_results.json').write_text(json.dumps(g.encode(report),indent=2)+'\n')
    print('index',r['index'],'cap',attempts[-1]['cap'],'margin',float(min(attempts[-1]['row_margins'])),'elapsed',report['elapsed_seconds'])
if __name__=='__main__': main()
