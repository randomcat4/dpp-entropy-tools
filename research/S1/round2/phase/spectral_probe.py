"""Second frozen unit; exact rational spectral coefficients, floating Hessians."""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key]='1'
import argparse,datetime,hashlib,json,resource,sys,time
from fractions import Fraction as R
import numpy as np
import scipy
from full_hessian import evaluate

def multiply(x,y):return (x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def conjugate(x):return (x[0],-x[1])

def exact_center(c):
    P=c['P'];eps=R(c['epsilon']);L=R(c['L']);radii=list(map(R,c['radius_bounds']))
    assert sum(radii)==L
    assert all(r>=0 and r*r>=x*x+y*y for r,(x,y) in zip(radii,P))
    corr=[]
    for k in range(len(P)):
        terms=[multiply(P[j+k],conjugate(P[j])) for j in range(len(P)-k)]
        corr.append((sum(x[0] for x in terms),sum(x[1] for x in terms)))
    inv=multiply(multiply(corr[1],corr[1]),conjugate(corr[2]))
    assert list(inv)==c['unnormalized_cycle_invariant'] and inv[1]!=0
    scale=(1-2*eps)/(L*L)
    p=eps+scale*corr[0][0]
    a=[2*scale*x for x,y in corr[1:]];b=[-2*scale*y for x,y in corr[1:]]
    old_margin=min(p,1-p)-sum(map(abs,a+b))
    assert old_margin<0
    if 'control' in c['id']:
        lower=eps+scale
        assert abs(P[0][0])-sum(radii[1:])>=1 and P[0][1]==0
    else:
        assert sum(x[0] for x in P)==0 and sum(x[1] for x in P)==0
        lower=eps
    return p,a,b,{'autocorrelation_gaussian_integer':corr,'spectral_scale':str(scale),
                   'proved_uniform_margin':str(eps),'proved_lower_bound':str(lower),
                   'old_coefficient_triangle_margin':str(old_margin),
                   'cycle_invariant_real':str(scale**3*inv[0]),'cycle_invariant_imag':str(scale**3*inv[1])}

def run(inp):
    rows=[]
    for c in inp['centers']:
        p,a,b,evidence=exact_center(c)
        row={'id':c['id'],'p':str(p),'a':list(map(str,a)),'b':list(map(str,b)),
             'exact_evidence':evidence,'diagnostics':[]}
        for n in inp['windows']:
            row['diagnostics'].append(evaluate(n,float(p),np.array(a,dtype=float),np.array(b,dtype=float)))
        rows.append(row)
        print(json.dumps({'completed_center':c['id'],'top':row['diagnostics'][-1]['top_hessian_direction']}),flush=True)
    return rows

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--input',required=True);parser.add_argument('--output',required=True)
    args=parser.parse_args();resource.setrlimit(resource.RLIMIT_AS,(4*1024**3,4*1024**3))
    with open(args.input) as handle:inp=json.load(handle)
    start=time.time();base=os.path.dirname(__file__)
    meta={'status':'RUNNING','pid':os.getpid(),'seed':None,'randomness':'none',
          'utc_start':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__,
          'argv':sys.argv,'input_sha256':hashlib.sha256(open(args.input,'rb').read()).hexdigest(),
          'source_sha256':{name:hashlib.sha256(open(os.path.join(base,name),'rb').read()).hexdigest() for name in ('spectral_probe.py','full_hessian.py')},
          'threads':{key:os.environ[key] for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS')},
          'address_space_limit_bytes':4*1024**3}
    print(json.dumps(meta),flush=True)
    try:
        rows=run(inp);meta.update(status='COMPLETED',exit_status=0,elapsed_seconds=time.time()-start,
                                 max_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                                 centers_completed=len(rows),hessians_completed=sum(len(r['diagnostics']) for r in rows),
                                 event_evaluations=sum(2**d['n'] for r in rows for d in r['diagnostics']))
        with open(args.output,'w') as handle:json.dump({'results':rows,'metadata':meta},handle,indent=2)
        print(json.dumps(meta),flush=True)
    except BaseException as error:
        meta.update(status='FAILED',exit_status=1,error=repr(error))
        with open(args.output,'w') as handle:json.dump({'metadata':meta},handle,indent=2)
        raise
