"""Bounded mixed-centre diagnostic. Finite floating jets are not rate certificates."""
import argparse
from fractions import Fraction as F
import hashlib
import json
import os
from pathlib import Path
import platform
import resource
import subprocess
import time
import numpy as np
from scipy.linalg import toeplitz


def kernel(c,t,n):
    first=np.zeros(n,dtype=complex)
    first[0]=float(F(c['p'])+F(t)*F(c['dp']))
    for k,(a,b,da,db) in enumerate(zip(c['a'],c['b'],c['da'],c['db']),1):
        if k<n:first[k]=complex(float(F(a)+F(t)*F(da)),-float(F(b)+F(t)*F(db)))/2
    return toeplitz(first,first.conj())


def bases(m,n):
    result=[np.eye(n,dtype=complex)]
    for imaginary in [False,True]:
        for k in range(1,m+1):
            col=np.zeros(n,dtype=complex)
            if k<n:col[k]=(-1j if imaginary else 1)/2
            result.append(toeplitz(col,col.conj()))
    return np.array(result)


def masses(K):
    n=len(K)
    zero=1-((np.arange(2**n)[:,None]>>np.arange(n))&1)
    M=np.broadcast_to(K,(2**n,n,n)).copy()
    M[:,np.arange(n),np.arange(n)]-=zero
    vals=(-1.)**zero.sum(axis=1)*np.linalg.det(M)
    if max(abs(vals.imag))>1e-10 or vals.real.min()<=0:raise RuntimeError('invalid event masses')
    return vals.real,M


def jets(c,n):
    K=kernel(c,F(0),n);D=bases(len(c['a']),n);p,M=masses(K)
    inv=np.linalg.inv(M)
    B=np.einsum('xij,ajk->xaik',inv,D)
    s=np.einsum('xaii->xa',B)
    tr2=np.einsum('xaij,xbji->xab',B,B)
    p1=p[:,None]*s
    p2=p[:,None,None]*(s[:,:,None]*s[:,None,:]-tr2)
    fisher=np.einsum('xa,xb,x->ab',p1,p1,1/p).real
    acceleration=-np.einsum('xab,x->ab',p2,np.log(p)).real
    H=acceleration-fisher
    H=(H+H.T)/2
    ev,V=np.linalg.eigh(H);v=V[:,-1]
    d=np.array([float(F(c['dp']))]+[float(F(x)) for x in c['da']+c['db']])
    entropies=[]
    for t in [-F(c['tau']),F(0),F(c['tau'])]:
        pt,_=masses(kernel(c,t,n));entropies.append(float(-pt@np.log(pt)))
    def split(w):return {'fisher':float(w@fisher@w),'acceleration':float(w@acceleration@w),'total':float(w@H@w)}
    return {'n':n,'basis':['mean']+['cos'+str(k) for k in range(1,len(c['a'])+1)]+['sin'+str(k) for k in range(1,len(c['a'])+1)],
            'hessian':H.tolist(),'fisher':fisher.tolist(),'acceleration':acceleration.tolist(),
            'hessian_eigenvalues':ev.tolist(),'fisher_eigenvalues':np.linalg.eigvalsh(fisher).tolist(),
            'maximum_direction':v.tolist(),'maximum_direction_split':split(v),'frozen_direction_split':split(d),
            'three_entropies_minus_center_plus':entropies,'finite_gap':sum([entropies[0]/2,entropies[2]/2,-entropies[1]]),
            'max_event_first_derivative':float(np.max(abs(p1))),
            'normalization_error':float(abs(p.sum()-1)),'first_mass_sum_error':float(np.max(abs(p1.sum(axis=0)))),
            'second_mass_sum_error':float(np.max(abs(p2.sum(axis=0)))),
            'imaginary_jet_error':float(max(np.max(abs(p1.imag)),np.max(abs(p2.imag)))),
            'actual_event_evaluations':4*2**n}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--candidate',required=True);ap.add_argument('--output',required=True);args=ap.parse_args()
    start=time.time();cp=Path(args.candidate);c=json.loads(cp.read_text())
    margin=min(F(c['p']),1-F(c['p']))-sum(abs(F(x)) for x in c['a']+c['b'])-F(c['tau'])*(abs(F(c['dp']))+sum(abs(F(x)) for x in c['da']+c['db']))
    if margin<F(c['uniform_margin']) or margin<=0:raise AssertionError('margin failed')
    rows=[jets(c,n) for n in [6,8]]
    out={'status':'COMPLETED_FLOAT_DIAGNOSTIC_NOT_CERTIFICATE','exit_status':0,'pid':os.getpid(),'seed':None,'randomness':'none',
         'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'candidate_sha256':hashlib.sha256(cp.read_bytes()).hexdigest(),
         'git_head':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'python':platform.python_version(),'numpy':np.__version__,
         'threads':{k:os.environ.get(k) for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']},
         'seconds':time.time()-start,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
         'proved_triangle_margin':str(margin),'unique_centres':1,'actual_windows':[6,8],
         'actual_event_evaluations':sum(r['actual_event_evaluations'] for r in rows),'rows':rows}
    Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['status','pid','seconds','actual_event_evaluations']}))
    print(json.dumps([{'n':r['n'],'lambda_max':r['hessian_eigenvalues'][-1],'gap':r['finite_gap'],'split':r['frozen_direction_split']} for r in rows]))


if __name__=='__main__':main()
