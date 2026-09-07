"""Block-exchangeable real DPP exact-event entropy and curvature search.
All computations float64 exploratory; no output is a certified counterexample.
"""
import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[name]='1'
import argparse, csv, itertools, json, math, time, traceback
from pathlib import Path
import numpy as np

class Family:
    def __init__(self, sizes):
        self.m=np.array(sizes); self.g=len(sizes); self.n=sum(sizes)
        self.counts=np.array(list(itertools.product(*[range(m+1) for m in sizes])))
        self.mult=np.array([math.prod(math.comb(m,int(k)) for m,k in zip(sizes,ks)) for ks in self.counts],float)
        self.pairs=list(zip(*np.triu_indices(self.g)))
        self.p=self.g+len(self.pairs)
        self.U=np.zeros((self.n,self.g)); off=0
        for j,m in enumerate(sizes): self.U[off:off+m,j]=1/np.sqrt(m); off+=m
        self.labels=np.repeat(np.arange(self.g),self.m)
        self.cnt=np.concatenate([self.counts,self.m-self.counts],axis=1)
        self.mask=self.cnt>0
        self.V=np.zeros((len(self.counts),2*self.g,self.g))
        for j in range(self.g):
            self.V[:,j,j]=np.sqrt(self.counts[:,j]/self.m[j])
            self.V[:,j+self.g,j]=np.sqrt((self.m[j]-self.counts[:,j])/self.m[j])
        self.res=np.maximum(self.cnt-1,0)
        self.bases=[]; self.dabase=[]
        for j in range(self.p):
            da=np.zeros(self.g); dc=np.zeros((self.g,self.g))
            if j<self.g: da[j]=1
            else:
                r,s=self.pairs[j-self.g]; dc[r,s]=dc[s,r]=1
            dr=np.einsum('qij,jk,qlk->qil',self.V,dc-np.diag(da),self.V)
            diag=np.tile(da,2)[None,:]*self.mask
            dr[:,np.arange(2*self.g),np.arange(2*self.g)]+=diag
            self.bases.append(dr); self.dabase.append(np.tile(da,2))
        self.bases=np.array(self.bases).transpose(1,0,2,3)
        self.dabase=np.array(self.dabase)

    def unpack(self,x):
        a=np.array(x[:self.g]); C=np.zeros((self.g,self.g))
        for t,(i,j) in zip(x[self.g:],self.pairs): C[i,j]=C[j,i]=t
        return a,C
    def pack(self,a,C): return np.r_[a,[C[i,j] for i,j in self.pairs]]
    def matrix(self,x):
        a,C=self.unpack(x)
        return np.diag(a[self.labels])+self.U@(C-np.diag(a))@self.U.T
    def margin(self,x):
        a,C=self.unpack(x); vals=np.r_[a,np.linalg.eigvalsh(C)]
        return float(min(vals.min(),1-vals.max()))
    def evaluate(self,x,hessian=False):
        a,C=self.unpack(x); g=self.g
        d=np.r_[a,a-1][None,:]*np.ones_like(self.cnt)
        d=np.where(self.mask,d,1.)
        R=np.einsum('qij,jk,qlk->qil',self.V,C-np.diag(a),self.V)
        R[:,np.arange(2*g),np.arange(2*g)]+=d
        signs,lds=np.linalg.slogdet(R)
        expect=(-1.)**np.sum(self.m-self.counts,axis=1)
        rsign=(-1.)**np.sum(self.res[:,g:],axis=1)
        if not np.all(signs*rsign==expect): raise ArithmeticError('event determinant sign')
        logp=lds+np.sum(self.res*np.log(abs(d)),axis=1)
        probs=np.exp(logp); w=probs*self.mult
        if abs(w.sum()-1)>2e-8: raise ArithmeticError('normalization '+str(w.sum()))
        H=-w@logp
        if not hessian: return float(H),probs
        inv=np.linalg.inv(R)
        Q=np.einsum('qij,qpjk->qpik',inv,self.bases,optimize=True)
        grad=np.trace(Q,axis1=2,axis2=3)+np.einsum('qj,pj->qp',self.res/d,self.dabase)
        hlog=-np.einsum('qpij,qrji->qpr',Q,Q,optimize=True)-np.einsum('qj,pj,rj->qpr',self.res/d**2,self.dabase,self.dabase,optimize=True)
        hh=-np.einsum('q,q,qp,qr->pr',w,logp+1,grad,grad,optimize=True)-np.einsum('q,q,qpr->pr',w,logp,hlog,optimize=True)
        return float(H),probs,(hh+hh.T)/2
    def lprobs(self,x):
        a,C=self.unpack(x); l=a/(1-a)
        T=np.linalg.inv(np.eye(self.g)-C)-np.eye(self.g)-np.diag(l)
        W=np.sqrt(self.counts/(self.m*l))
        Z=np.eye(self.g)[None,:,:]+W[:,:,None]*T[None,:,:]*W[:,None,:]
        sign,ld=np.linalg.slogdet(Z)
        assert np.all(sign>0)
        pre=np.sum((self.m-1)*np.log1p(-a))+np.linalg.slogdet(np.eye(self.g)-C)[1]
        return np.exp(pre+self.counts@np.log(l)+ld)

def mobius(K):
    n=len(K); p=np.ones(1<<n)
    for mask in range(1,1<<n):
        ids=[i for i in range(n) if mask>>i&1]
        p[mask]=np.linalg.det(K[np.ix_(ids,ids)])
    for i in range(n):
        for mask in range(1<<n):
            if not(mask>>i&1): p[mask]-=p[mask|(1<<i)]
    return p

def random_x(f,rng,mode):
    if mode==0: a=rng.uniform(.08,.92,f.g); ev=rng.uniform(.04,.96,f.g)
    elif mode==1: a=np.clip(rng.beta(.35,.35,f.g),1e-5,1-1e-5); ev=np.clip(rng.beta(.35,.35,f.g),1e-5,1-1e-5)
    elif mode==2: a=np.full(f.g,.5); ev=np.clip(rng.beta(.15,.15,f.g),1e-6,1-1e-6)
    else: a=np.clip(rng.beta(.15,.15,f.g),1e-6,1-1e-6); ev=rng.uniform(.1,.9,f.g)
    Q,_=np.linalg.qr(rng.normal(size=(f.g,f.g)))
    return f.pack(a,(Q*ev)@Q.T)

def validate(out,seed):
    rng=np.random.default_rng(seed); rows=[]
    for sizes in ([2,2],[2,3],[2,2,2],[3,3,2]):
        f=Family(sizes)
        for trial in range(8):
            x=random_x(f,rng,trial%2); H,p,hh=f.evaluate(x,True); pl=f.lprobs(x); pm=mobius(f.matrix(x))
            mapped=[]
            lookup={tuple(k):j for j,k in enumerate(f.counts)}
            for mask in range(1<<f.n):
                k=tuple(sum(bool(mask>>i&1) for i in range(f.n) if f.labels[i]==g) for g in range(f.g))
                mapped.append(p[lookup[k]])
            d=rng.normal(size=f.p); d/=np.linalg.norm(d); step=min(1e-4,f.margin(x)*.001)
            fd=(f.evaluate(x+step*d)[0]+f.evaluate(x-step*d)[0]-2*H)/step**2
            row=dict(sizes=sizes,trial=trial,seed=seed,min_margin=f.margin(x),event_error=float(np.max(abs(pm-mapped))),l_error=float(max(abs(pl-p))),entropy_error=float(abs(-sum(v*np.log(v) for v in pm if v>0)-H)),hessian_analytic=float(d@hh@d),hessian_fd=float(fd),fd_step=step)
            if row['event_error']>1e-10 or row['l_error']>1e-10: raise AssertionError(row)
            rows.append(row)
    (out/'validation.json').write_text(json.dumps(rows,indent=2))
    print(json.dumps({'validation_cases':len(rows),'max_event_error':max(r['event_error'] for r in rows),'max_L_error':max(r['l_error'] for r in rows)}),flush=True)

def run(args):
    out=Path(args.out); out.mkdir(parents=True,exist_ok=True)
    ledger=out/'candidate_ledger.csv'
    if ledger.exists() and not args.resume: raise FileExistsError('Existing ledger: use --resume to continue without repeating evaluated points')
    completed=[]
    if args.resume and ledger.exists():
        completed=list(csv.DictReader(ledger.open()))
        old=json.loads((out/'run_manifest.json').read_text())
        if old['seed']!=args.seed or old.get('sizes')!=args.sizes: raise ValueError('Resume seed/sizes mismatch')
    manifest=dict(vars(args),numpy=np.__version__,threads=1,start=time.time(),status='RUNNING')
    (out/'run_manifest.json').write_text(json.dumps(manifest,indent=2))
    if args.validate and not completed: validate(out,args.seed)
    rng=np.random.default_rng(args.seed); sizesets=json.loads(args.sizes) if args.sizes else [[4,4,4],[6,6],[3,3,3,3],[8,8,8],[2,4,8],[10,10,10]]
    fs=[Family(s) for s in sizesets]; best=max([float(r['largest_hessian_eigenvalue']) for r in completed if r['largest_hessian_eigenvalue']]+[-float('inf')]); count=len(completed)
    fields=['index','seed','sizes','mode','margin','H','largest_hessian_eigenvalue','step','gap','endpoint_margin','status','parameters','direction','error']
    with ledger.open('a' if completed else 'w',newline='') as fp:
        wr=csv.DictWriter(fp,fieldnames=fields)
        if not completed: wr.writeheader()
        for i in range(args.trials):
            f=fs[i%len(fs)]; mode=(i//len(fs))%4; x=random_x(f,rng,mode)
            if i<len(completed): continue
            row=dict(index=i,seed=args.seed,sizes=json.dumps(f.m.tolist()),mode=mode,parameters=json.dumps(x.tolist()))
            try:
                H,p,hh=f.evaluate(x,True); ev,V=np.linalg.eigh(hh); d=V[:,-1]; lam=float(ev[-1])
                lo=0.; hi=1.
                while min(f.margin(x-hi*d),f.margin(x+hi*d))>1e-8: hi*=2
                for _ in range(50):
                    t=(lo+hi)/2
                    if min(f.margin(x-t*d),f.margin(x+t*d))>1e-8: lo=t
                    else: hi=t
                step=.2*lo; gap=(f.evaluate(x-step*d)[0]+f.evaluate(x+step*d)[0])/2-H
                row.update(margin=f.margin(x),H=H,largest_hessian_eigenvalue=lam,step=step,gap=gap,endpoint_margin=min(f.margin(x-step*d),f.margin(x+step*d)),status='CANDIDATE' if gap>1e-10 else 'NO_HIT',direction=json.dumps(d.tolist()))
                if lam>best:
                    best=lam; (out/'best_curvature.json').write_text(json.dumps(row,indent=2))
                if gap>1e-10:
                    (out/f'candidate_{i}.json').write_text(json.dumps(row,indent=2)); print('CANDIDATE '+json.dumps(row),flush=True)
            except Exception as ex:
                row.update(status='FAILED',error=repr(ex))
            wr.writerow(row); fp.flush(); count+=1
            if i%20==0: print(json.dumps(dict(completed=count,total=args.trials,best_curvature=best,elapsed=time.time()-manifest['start'])),flush=True)
    manifest.update(status='INCOMPLETE',exit_code=0,completed=count,elapsed=time.time()-manifest['start'],best_curvature=best)
    (out/'run_manifest.json').write_text(json.dumps(manifest,indent=2)); print(json.dumps(manifest),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--out',default='.'); p.add_argument('--seed',type=int,default=2026090803); p.add_argument('--trials',type=int,default=240); p.add_argument('--validate',action='store_true'); p.add_argument('--sizes'); p.add_argument('--resume',action='store_true'); run(p.parse_args())
