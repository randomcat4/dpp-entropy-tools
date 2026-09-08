"""Bounded, deterministic asymmetric three-point DPP probe; no R1 imports."""
import os
for name in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:
    os.environ[name]='1'
import argparse, itertools, json, math, platform, time
from fractions import Fraction as F
from pathlib import Path
import numpy as np
import scipy
from scipy.optimize import minimize

ROOT=Path(__file__).resolve().parent
COUNT=0
def matrix(v):
    a,b,c,x,y,z=v
    return np.array([[a,x,y],[x,b,z],[y,z,c]],float)
def jet(v,g=None,h=None):
    return (float(v),np.zeros(6) if g is None else g,np.zeros((6,6)) if h is None else h)
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def scale(a,t): return tuple(x*t for x in a)
def mul(a,b):
    av,ag,ah=a; bv,bg,bh=b
    return av*bv,ag*bv+bg*av,ah*bv+bh*av+np.outer(ag,bg)+np.outer(bg,ag)
def events_jet(v):
    j=[jet(v[i],np.eye(6)[i]) for i in range(6)]
    out=[]
    for mask in range(8):
        s=[1 if mask>>i&1 else -1 for i in range(3)]
        d=[j[i] if s[i]==1 else add(jet(1),scale(j[i],-1)) for i in range(3)]
        p=mul(mul(d[0],d[1]),d[2])
        for i,k,edge in [(0,1,3),(0,2,4),(1,2,5)]:
            p=add(p,scale(mul(mul(j[edge],j[edge]),d[3-i-k]),-s[i]*s[k]))
        p=add(p,scale(mul(mul(j[3],j[4]),j[5]),2*np.prod(s)))
        out.append(p)
    return np.array([t[0] for t in out]),np.array([t[1] for t in out]),np.array([t[2] for t in out])
def events_independent(v):
    K=matrix(v)
    minors=[]
    for mask in range(8):
        ids=[i for i in range(3) if mask>>i&1]
        minors.append(np.linalg.det(K[np.ix_(ids,ids)]) if ids else 1.)
    return np.array([sum((-1)**((t^s).bit_count())*minors[t] for t in range(8) if t&s==s) for s in range(8)])
def entropy(v):
    global COUNT
    COUNT+=1
    p=events_independent(v)
    if min(p)<=0: raise ValueError('nonpositive event')
    return -float(p@np.log(p))
def hessian(v):
    global COUNT
    COUNT+=1
    p,g,h=events_jet(v)
    if min(p)<=0: raise ValueError('nonpositive event')
    fisher=-(g.T/p)@g
    accel=-np.einsum('s,sij->ij',np.log(p),h)
    # Orthonormal Frobenius coordinates for the symmetric matrix direction.
    w=np.array([1,1,1,1/math.sqrt(2),1/math.sqrt(2),1/math.sqrt(2)])
    Q=(fisher+accel)*w[:,None]*w[None,:]
    ev,U=np.linalg.eigh(Q)
    return float(ev[-1]),U[:,-1]*w,p,fisher,accel
def feasible(v):
    e=np.linalg.eigvalsh(matrix(v))
    return min(e[0],1-e[-1])
def minors3(v,complement=False):
    a,b,c,x,y,z=v
    if complement: a,b,c,x,y,z=1-a,1-b,1-c,-x,-y,-z
    return [a,b,c,a*b-x*x,a*c-y*y,b*c-z*z,a*b*c+2*x*y*z-a*z*z-b*y*y-c*x*x]
def exact_feasible(v): return min(minors3(v)+minors3(v,True))>0
DIAGONALS=[(F(1,2),F(1,3),F(2,3)),(F(1,16),F(1,3),F(3,4)),(F(1,256),F(1,4),F(3,4)),(F(1,32),F(1,16),F(3,4)),(F(1,1024),F(1,8),F(1,2)),(F(1,256),F(255,256),F(1,3)),(F(1,16),F(1,8),F(1,4)),(F(1,1024),F(1,64),F(1,4))]
RATIOS=[(1,2,3),(1,3,7),(1,1,8),(1,8,1)]
RADII=[F(1,64),F(1,8),F(1,2),F(7,8),F(63,64),F(255,256),F(4095,4096),F(65535,65536)]
def centers():
    for di,d in enumerate(DIAGONALS):
        for ri,r in enumerate(RATIOS):
            for sign in [-1,1]:
                edges=[F(r[0]),F(r[1]),F(sign*r[2])]
                lo,hi=F(0),F(1)
                # Fixed 48 rational bisections, always retaining strict feasibility.
                for _ in range(48):
                    mid=(lo+hi)/2
                    if exact_feasible(list(d)+[mid*x for x in edges]): lo=mid
                    else: hi=mid
                for qi,q in enumerate(RADII):
                    yield dict(id=f'd{di}-r{ri}-s{sign}-q{qi}',diagonal=di,ratio=ri,cycle_sign=sign,radius=str(q),threshold_lower=str(lo),threshold_upper=str(hi),exact=[str(x) for x in list(d)+[q*lo*x for x in edges]])
def save(path,obj): path.write_text(json.dumps(obj,indent=2,allow_nan=False)+'\n')
def smoke():
    rng=np.random.default_rng(2026090801)
    rows=[]
    for i in range(8):
        v=np.array([.2,.45,.7,.03,.06,(-1)**i*.09])+rng.uniform(-.01,.01,6)
        p,g,h=events_jet(v)
        pe=events_independent(v)
        lam,d,p,fi,ac=hessian(v)
        eps=2e-5
        fd=(entropy(v+eps*d)+entropy(v-eps*d)-2*entropy(v))/eps**2
        analytic=float(d@(fi+ac)@d)
        row=dict(id=i,prob_error=float(max(abs(pe-p))),sum_p=float(sum(p)),sum_gradient=float(max(abs(g.sum(0)))),sum_hessian=float(max(abs(h.sum(0)).ravel())),finite_difference=fd,analytic=analytic,error=abs(fd-analytic))
        assert row['prob_error']<2e-15 and row['sum_gradient']<2e-15 and row['sum_hessian']<2e-15 and row['error']<1e-5,row
        rows.append(row)
    save(ROOT/'smoke.json',dict(status='PASS',seed=2026090801,checks=rows,target_calls=COUNT,pid=os.getpid()))
def formal():
    assert json.loads((ROOT/'smoke.json').read_text())['status']=='PASS'
    start=time.time(); rows=[]
    for spec in centers():
        exact=list(map(F,spec['exact'])); assert exact_feasible(exact)
        v=np.array(list(map(float,exact)))
        lam,d,p,fi,ac=hessian(v)
        margin=feasible(v); t=margin/(4*np.linalg.norm(matrix(d),2))
        delta=(entropy(v-t*d)+entropy(v+t*d))/2-entropy(v)
        # The chord is floating and has no certifying status.
        row=dict(**spec,lambda_max=lam,scaled_lambda=lam/float(v[3:]@v[3:]),margin=margin,min_event=float(min(p)),direction=d.tolist(),t=t,delta=delta,fisher_q=float(d@fi@d),acceleration_q=float(d@ac@d))
        rows.append(row)
    save(ROOT/'centers.json',rows)
    # Twelve starts: best scaled curvature per (diagonal, cycle sign), then top 12.
    groups={}
    for row in rows:
        key=(row['diagonal'],row['cycle_sign'])
        if key not in groups or row['scaled_lambda']>groups[key]['scaled_lambda']: groups[key]=row
    starts=sorted(groups.values(),key=lambda r:r['scaled_lambda'],reverse=True)[:12]
    refinements=[]
    class Budget(Exception): pass
    for row in starts:
        calls=[]; best=None
        def objective(v):
            nonlocal best
            global COUNT
            if len(calls)>=250: raise Budget()
            margin=feasible(v)
            if margin<1e-9 or np.linalg.norm(v[3:])<1e-6:
                COUNT+=1
                value=1e3+1e6*max(0,1e-9-margin)
                calls.append(dict(v=v.tolist(),status='rejected_domain',margin=margin,value=value)); return value
            try:
                lam,d,p,fi,ac=hessian(v)
                value=-lam/float(v[3:]@v[3:])
                rec=dict(v=v.tolist(),status='evaluated',margin=margin,lambda_max=lam,value=value,direction=d.tolist())
                calls.append(rec)
                if best is None or value<best['value']: best=rec
                return value
            except ValueError as e:
                calls.append(dict(v=v.tolist(),status='event_failure',margin=margin,error=str(e),value=1e6)); return 1e6
        try:
            result=minimize(objective,np.array(list(map(float,map(F,row['exact'])))),method='Nelder-Mead',options=dict(maxfev=250,maxiter=250,xatol=1e-9,fatol=1e-9,adaptive=True))
            reason=str(result.message)
        except Budget: reason='hard 250-call cap'
        refinements.append(dict(start_id=row['id'],termination=reason,best=best,calls=calls))
    save(ROOT/'refinements.json',refinements)
    candidates=[dict(kind='center',id=r['id'],lambda_max=r['lambda_max']) for r in rows if r['lambda_max']>1e-9 or r['delta']>1e-12]
    candidates += [dict(kind='refinement',id=r['start_id'],best=r['best']) for r in refinements if r['best'] and r['best']['lambda_max']>1e-9]
    save(ROOT/'summary.json',dict(status='FLOAT_CANDIDATES' if candidates else 'INCOMPLETE',centers=len(rows),refinements=len(refinements),refinement_calls=sum(len(r['calls']) for r in refinements),target_calls=COUNT,positive_candidates=candidates,best_center=max(rows,key=lambda r:r['lambda_max']),best_scaled_center=max(rows,key=lambda r:r['scaled_lambda']),best_refinement=min((r['best'] for r in refinements if r['best']),key=lambda r:r['value']),elapsed_seconds=time.time()-start,pid=os.getpid(),python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,threads={k:os.environ[k] for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']},seed=None))
    assert COUNT<=6000
if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('mode',choices=['smoke','formal']); args=parser.parse_args()
    globals()[args.mode]()
