"""Predeclared non-even scalar Toeplitz full Hessians. Floating point only."""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key]='1'
import argparse,datetime,hashlib,json,resource,sys,time
from fractions import Fraction
import numpy as np
import scipy

def symbol_matrix(n,p,a,b):
    k=np.eye(n,dtype=complex)*p
    for distance,(aa,bb) in enumerate(zip(a,b),1):
        for i in range(n-distance):
            k[i+distance,i]=(aa-1j*bb)/2
            k[i,i+distance]=(aa+1j*bb)/2
    return k

def directions(n,m):
    z=np.zeros(m)
    ds=[symbol_matrix(n,1,z,z)]
    ds.extend(symbol_matrix(n,0,np.eye(m)[r],z) for r in range(m))
    ds.extend(symbol_matrix(n,0,z,np.eye(m)[r]) for r in range(m))
    return np.array(ds)

def direction_record(v,F,A,Q):
    return {'coefficients':v.tolist(),'fisher':float(v@F@v),'acceleration':float(v@A@v),
            'hessian':float(v@Q@v)}

def evaluate(n,p,a,b):
    k=symbol_matrix(n,p,a,b);m=len(a);ds=directions(n,m);d=len(ds)
    F=np.zeros((d,d));A=np.zeros((d,d));gradient=np.zeros(d)
    mass=0.;massfirst=np.zeros(d);masssecond=np.zeros((d,d));entropy=0.
    minq=1.;maxscore=0.;imagres=0.
    gauge=np.r_[0,np.arange(1,m+1)*b,-np.arange(1,m+1)*a]
    gauge2=np.r_[0,-np.arange(1,m+1)**2*a,-np.arange(1,m+1)**2*b]
    gauge_first_max=0.
    for mask in range(1<<n):
        zero=np.array([1-((mask>>j)&1) for j in range(n)])
        M=k-np.diag(zero)
        qc=(-1)**int(zero.sum())*np.linalg.det(M)
        q=qc.real; assert q>0
        prod=np.linalg.inv(M)[None,:,:]@ds
        scorec=np.trace(prod,axis1=1,axis2=2)
        score=scorec.real
        secondc=q*(np.outer(scorec,scorec)-np.einsum('rij,sji->rs',prod,prod))
        second=secondc.real
        imagres=max(imagres,abs(qc.imag),float(abs(scorec.imag).max()),float(abs(secondc.imag).max()))
        F+=q*np.outer(score,score)
        A-=second*np.log(q)
        gradient-=q*score*np.log(q)
        mass+=q;massfirst+=q*score;masssecond+=second
        entropy-=q*np.log(q);minq=min(minq,q);maxscore=max(maxscore,float(abs(score).max()))
        gauge_first_max=max(gauge_first_max,abs(q*score@gauge))
    assert abs(mass-1)<1e-11
    F=(F+F.T)/2;A=(A+A.T)/2;Q=A-F
    eig,v=np.linalg.eigh(Q);aeig,av=np.linalg.eigh(A)
    gauge_norm=gauge/np.linalg.norm(gauge)
    best=v[:,-1]
    return {'n':n,'dimension':d,'entropy':entropy,'fisher_matrix':F.tolist(),
            'acceleration_matrix':A.tolist(),'hessian_matrix':Q.tolist(),
            'hessian_eigenvalues':eig.tolist(),'fisher_eigenvalues':np.linalg.eigvalsh(F).tolist(),
            'acceleration_eigenvalues':aeig.tolist(),'gradient':gradient.tolist(),
            'top_hessian_direction':direction_record(best,F,A,Q),
            'top_acceleration_direction':direction_record(av[:,-1],F,A,Q),
            'gauge_tangent':direction_record(gauge_norm,F,A,Q),
            'top_hessian_gauge_alignment':float(abs(best@gauge_norm)),
            'gauge_second_identity_residual':float(abs(gauge@Q@gauge+gradient@gauge2)),
            'gauge_event_first_derivative_max':gauge_first_max,
            'cos_sin_hessian_block_max':float(abs(Q[1:m+1,m+1:]).max()),
            'probability_sum_error':abs(mass-1),'first_mass_max':float(abs(massfirst).max()),
            'second_mass_max':float(abs(masssecond).max()),'min_probability':minq,
            'max_event_score':maxscore,'max_imaginary_residual':imagres}

def run(inp):
    results=[]
    for center in inp['centers']:
        p=Fraction(center['p']);budget=Fraction(center['budget_fraction'])
        total=sum(abs(i) for i in center['A']+center['B']);scale=p*budget/total
        a=[scale*i for i in center['A']];b=[scale*i for i in center['B']]
        assert a[0]>0 and b[0]==0 and b[1]>0
        result={'id':center['id'],'p':str(p),'a':list(map(str,a)),'b':list(map(str,b)),
                'triangle_margin':str(p*(1-budget)), 'diagnostics':[]}
        for n in inp['windows']:
            result['diagnostics'].append(evaluate(n,float(p),np.array(a,dtype=float),np.array(b,dtype=float)))
        results.append(result)
        top=result['diagnostics'][-1]['top_hessian_direction']
        print(json.dumps({'completed_center':center['id'],'windows':inp['windows'],'top_hessian':top['hessian'],
                          'fisher':top['fisher'],'acceleration':top['acceleration']}),flush=True)
    return results

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--input',required=True);parser.add_argument('--output',required=True)
    args=parser.parse_args();resource.setrlimit(resource.RLIMIT_AS,(4*1024**3,4*1024**3))
    start=time.time()
    with open(args.input) as handle:inp=json.load(handle)
    meta={'status':'RUNNING','pid':os.getpid(),'seed':None,'randomness':'none','utc_start':datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__,'argv':sys.argv,
          'input_sha256':hashlib.sha256(open(args.input,'rb').read()).hexdigest(),
          'source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest(),
          'threads':{key:os.environ[key] for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS')},
          'address_space_limit_bytes':4*1024**3}
    print(json.dumps(meta),flush=True)
    try:
        results=run(inp);meta.update(status='COMPLETED',exit_status=0,elapsed_seconds=time.time()-start,
                                     max_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                                     centers_completed=len(results),hessians_completed=sum(len(r['diagnostics']) for r in results),
                                     event_evaluations=sum(2**d['n'] for r in results for d in r['diagnostics']))
        with open(args.output,'w') as handle:json.dump({'results':results,'metadata':meta},handle,indent=2)
        print(json.dumps(meta),flush=True)
    except BaseException as error:
        meta.update(status='FAILED',exit_status=1,error=repr(error))
        with open(args.output,'w') as handle:json.dump({'metadata':meta},handle,indent=2)
        raise
