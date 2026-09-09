"""Bounded phase diagnostics; floating point evidence, never a rate certificate."""
import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[name] = '1'
import argparse, datetime, hashlib, json, resource, sys, time
from fractions import Fraction
import numpy as np
import scipy

def kernel(n, p, a, b=None, t=0):
    k = np.eye(n, dtype=complex)*p
    if b is None: b = np.zeros(len(a))
    for d, (aa, bb) in enumerate(zip(a,b),1):
        for j in range(n-d):
            k[j+d,j] = (aa-1j*t*bb)/2
            k[j,j+d] = (aa+1j*t*bb)/2
    return k

def events(k):
    n = len(k)
    vals=[]
    maximag=0.
    for mask in range(1<<n):
        zero = np.array([1-((mask>>j)&1) for j in range(n)])
        q = (-1)**int(sum(zero))*np.linalg.det(k-np.diag(zero))
        maximag=max(maximag,abs(q.imag))
        vals.append(q.real)
    q=np.array(vals)
    assert q.min()>0
    assert abs(q.sum()-1)<1e-11
    return q, maximag

def entropy(k):
    q, im=events(k)
    return float(-q@np.log(q)), float(q.min()), float(abs(q.sum()-1)), im

def hessian(n,p,a):
    k=kernel(n,p,a)
    ds=[kernel(n,0,np.zeros(len(a)),np.eye(len(a))[j],1) for j in range(len(a))]
    hh=np.zeros((len(a),len(a)))
    qsum=0.; maxfirst=0.; secondmass=np.zeros_like(hh)
    for mask in range(1<<n):
        zero=np.array([1-((mask>>j)&1) for j in range(n)])
        mat=k-np.diag(zero)
        q=((-1)**int(sum(zero))*np.linalg.det(mat)).real
        assert q>0
        inv=np.linalg.inv(mat)
        prod=np.array([inv@d for d in ds])
        first=np.trace(prod,axis1=1,axis2=2)
        tr=np.einsum('kij,lji->kl',prod,prod)
        maxfirst=max(maxfirst,float(np.max(np.abs(q*first))))
        q2=(q*(np.outer(first,first)-tr)).real
        hh-=q2*np.log(q)
        secondmass+=q2
        qsum+=q
    eig,vec=np.linalg.eigh((hh+hh.T)/2)
    return {'n':n,'hessian':hh.tolist(),'eigenvalues':eig.tolist(),
            'top_eigenvector':vec[:,-1].tolist(),'probability_sum_error':abs(qsum-1),
            'max_event_first_derivative':maxfirst,
            'second_mass_max':float(abs(secondmass).max())}

def run():
    centers=[]
    # Hypothesis: odd triangle signs and density alter cycle acceleration;
    # 2 densities x 4 genuinely different sign patterns, no random search.
    for p in (Fraction(1,2),Fraction(1,4)):
        scale=2*p
        for s2,s3 in ((1,1),(1,-1),(-1,1),(-1,-1)):
            a=[scale*Fraction(3,10),scale*s2*Fraction(3,25),scale*s3*Fraction(1,25)]
            center={'p':str(p),'a':list(map(str,a)), 'diagnostics':[]}
            for n in (4,6,8):
                d=hessian(n,float(p),np.array(a,dtype=float))
                center['diagnostics'].append(d)
            centers.append(center)
    p=Fraction(1,2);a=list(map(Fraction,('3/10','3/25','1/25')))
    b=list(map(Fraction,('0','3/25','-1/25')));tau=Fraction(1,8)
    candidate={'p':str(p),'a':list(map(str,a)),'b':list(map(str,b)),'tau':str(tau),
               'proved_triangle_margin':'1/50','diagnostics':[]}
    for n in range(1,11):
        vals={str(t):entropy(kernel(n,float(p),np.array(a,dtype=float),np.array(b,dtype=float),float(t))) for t in (-tau,Fraction(0),tau)}
        delta=(vals[str(-tau)][0]+vals[str(tau)][0])/2-vals['0'][0]
        candidate['diagnostics'].append({'n':n,'entropy_minprob_masserror_maximag':vals,'delta':delta})
    return {'center_screen':centers,'fixed_candidate':candidate}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
    resource.setrlimit(resource.RLIMIT_AS,(4*1024**3,4*1024**3))
    start=time.time()
    meta={'status':'RUNNING','pid':os.getpid(),'seed':0,'randomness':'none; deterministic predefined coverage',
          'utc_start':datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest(),
          'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__,
          'argv':sys.argv,'threads':{name:os.environ[name] for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS')},
          'address_space_limit_bytes':4*1024**3}
    print(json.dumps(meta),flush=True)
    try:
        result=run();meta.update(status='COMPLETED',exit_status=0,elapsed_seconds=time.time()-start,
                                max_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        result['metadata']=meta
        with open(args.output,'w') as out:json.dump(result,out,indent=2)
        print(json.dumps(meta),flush=True)
    except BaseException as e:
        meta.update(status='FAILED',exit_status=1,error=repr(e),elapsed_seconds=time.time()-start)
        with open(args.output,'w') as out:json.dump({'metadata':meta},out,indent=2)
        raise
