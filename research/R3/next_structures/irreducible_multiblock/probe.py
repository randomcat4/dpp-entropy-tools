"""NS-2 bounded scout. Exact rational kernels; floating entropy probes only.
No hostname, credential, or remote launch configuration is stored here.
"""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key]='1'
import argparse, csv, json, math, time, traceback
from fractions import Fraction
from pathlib import Path
import numpy as np

DEN=10**12
EDGE_FLOOR=.025
DIAG_SEP=.001
SEED=202609081702

def graph(n):
    sizes={8:[3,3,2],11:[4,4,3],12:[4,4,4]}[n]
    cuts=np.cumsum([0]+sizes).tolist()
    cycle=[tuple(sorted((i,(i+1)%n))) for i in range(n)]
    defects=[(cuts[g],cuts[g+1]-1) for g in range(3) if sizes[g]>=3]
    edges=sorted(set(cycle+defects))
    bridges=[tuple(sorted((cuts[g+1]-1,cuts[(g+1)%3]))) for g in range(3)]
    return sizes,edges,cycle,bridges

def fraction_margin_certificate(J):
    """Exact rational LDL positivity for K-mI and (1-m)I-K.
    Every arithmetic operation in the returned positivity assertion is rational.
    """
    n=len(J); K=np.array(J,dtype=float)/DEN
    eig=np.linalg.eigvalsh(K)
    suggested=min(float(eig[0]),float(1-eig[-1]))
    m=Fraction(max(1,math.floor(suggested*500000)),10**6)
    pivot_min=[]
    for complement in (False,True):
        A=[[Fraction(int(J[i][j]),DEN) for j in range(n)] for i in range(n)]
        if complement:
            A=[[(int(i==j)-A[i][j]) for j in range(n)] for i in range(n)]
        for i in range(n): A[i][i]-=m
        L=[[Fraction(0) for _ in range(n)] for _ in range(n)]; piv=[]
        for j in range(n):
            dj=A[j][j]-sum(L[j][r]**2*piv[r] for r in range(j))
            if dj<=0: raise ArithmeticError('exact LDL nonpositive pivot')
            piv.append(dj); L[j][j]=1
            for i in range(j+1,n):
                L[i][j]=(A[i][j]-sum(L[i][r]*L[j][r]*piv[r] for r in range(j)))/dj
        pivot_min.append(float(min(piv)))
    return {'margin_rational':str(m),'margin':float(m),'minimum_exact_positive_pivots_as_float':pivot_min,'eigen_margin_float':suggested}

def fingerprint(J):
    n=len(J); K=np.array(J,dtype=float)/DEN; sizes,edges,cycle,bridges=graph(n)
    diag=np.diag(K); sep=min(abs(diag[i]-diag[j]) for i in range(n) for j in range(i))
    edge_min=min(abs(K[i,j]) for i,j in edges)
    bridge_min=min(abs(K[i,j]) for i,j in bridges)
    product=int(np.prod([np.sign(K[i,j]) for i,j in cycle]))
    if sep<DIAG_SEP: raise ArithmeticError('diagonal separation failed')
    if edge_min<EDGE_FLOOR: raise ArithmeticError('coupling floor failed')
    if product!=-1: raise ArithmeticError('frustrated cycle signature failed')
    return dict(sizes=sizes,edge_count=len(edges),min_diagonal_separation=float(sep),min_supported_edge=float(edge_min),min_cross_block_bridge=float(bridge_min),cycle_sign_product=product,nontrivial_exchangeable_partition_possible=False)

class Probe:
    def __init__(self,n):
        self.n=n; self.sizes,self.edges,self.cycle,self.bridges=graph(n)
        self.p=n+len(self.edges)
        self.bits=((np.arange(1<<n)[:,None]>>np.arange(n))&1).astype(float)
        self.sign=(-1.)**(n-self.bits.sum(axis=1))
        basis=[]
        for i in range(n):
            B=np.zeros((n,n)); B[i,i]=1; basis.append(B)
        for i,j in self.edges:
            B=np.zeros((n,n)); B[i,j]=B[j,i]=1/np.sqrt(2); basis.append(B)
        self.B=np.array(basis)
    def event(self,K,need_hessian=False):
        A=np.broadcast_to(K,(1<<self.n,self.n,self.n)).copy()
        A[:,np.arange(self.n),np.arange(self.n)]-=1-self.bits
        sign,lp=np.linalg.slogdet(A)
        if not np.array_equal(sign,self.sign): raise ArithmeticError('mixed determinant probability sign')
        pr=np.exp(lp); residual=float(abs(pr.sum()-1))
        if residual>1e-10: raise ArithmeticError('normalization residual '+str(residual))
        H=float(-pr@lp)
        if not need_hessian: return H,pr,residual
        inv=np.linalg.inv(A)
        Q=np.einsum('qij,pjk->qpik',inv,self.B,optimize=True)
        grad=np.trace(Q,axis1=2,axis2=3)
        hlog=-np.einsum('qpij,qrji->qpr',Q,Q,optimize=True)
        hess=-np.einsum('q,q,qp,qr->pr',pr,lp+1,grad,grad,optimize=True)-np.einsum('q,q,qpr->pr',pr,lp,hlog,optimize=True)
        return H,pr,residual,(hess+hess.T)/2
    def mobius(self,K):
        out=np.ones(1<<self.n)
        for mask in range(1,1<<self.n):
            ids=np.flatnonzero(self.bits[mask])
            out[mask]=np.linalg.det(K[np.ix_(ids,ids)])
        for j in range(self.n):
            for mask in range(1<<self.n):
                if not(mask>>j&1): out[mask]-=out[mask|(1<<j)]
        return out

def make_kernel(P,rng,mode):
    n=P.n; A=np.zeros((n,n))
    h=np.linspace(-.52,.52,n)+rng.uniform(-.012,.012,n)
    rng.shuffle(h); np.fill_diagonal(A,h)
    for i,j in P.edges:
        A[i,j]=A[j,i]=rng.choice([-1,1])*rng.uniform(.75,1.25)
    product=np.prod([np.sign(A[i,j]) for i,j in P.cycle])
    if product>0:
        i,j=P.bridges[-1]; A[i,j]*=-1; A[j,i]*=-1
    rho=(.27,.44,.495)[mode]
    M=.5*np.eye(n)+rho*A/np.max(abs(np.linalg.eigvalsh(A)))
    J=np.rint(M*DEN).astype(np.int64)
    return J,dict(mode=mode,rho=rho)

def safe(J):
    try:
        fingerprint(J)
        K=np.array(J,dtype=float)/DEN; vals=np.linalg.eigvalsh(K)
        return min(vals.min(),1-vals.max())>2e-5
    except ArithmeticError: return False

def step_limit(J,D):
    K=np.array(J,dtype=float)/DEN; n=len(J); _,edges,_,_=graph(n)
    bounds=[1.]
    for i,j in edges:
        if abs(D[i,j])>1e-15: bounds.append((abs(K[i,j])-EDGE_FLOOR-2/DEN)/abs(D[i,j]))
    for i in range(n):
        for j in range(i):
            diff=abs(D[i,i]-D[j,j])
            if diff>1e-15: bounds.append((abs(K[i,i]-K[j,j])-DIAG_SEP-2/DEN)/diff)
    lo,hi=0.,max(0.,min(bounds))
    for _ in range(45):
        t=(lo+hi)/2; R=np.rint(t*D*DEN).astype(np.int64)
        if safe(J-R) and safe(J+R): lo=t
        else: hi=t
    return lo

def hp_replay(J,R,dps):
    import mpmath as mp
    with mp.workdps(dps):
        n=len(J); entropies=[]; norms=[]; minima=[]
        for u in (-1,0,1):
            K=mp.matrix([[mp.mpf(int(J[i,j])+u*int(R[i,j]))/DEN for j in range(n)] for i in range(n)])
            probs=[]
            for mask in range(1<<n):
                A=K.copy(); missing=0
                for i in range(n):
                    if not(mask>>i&1): A[i,i]-=1; missing+=1
                p=(-1)**missing*mp.det(A)
                if p<=0: raise ArithmeticError('high precision probability nonpositive')
                probs.append(p)
            entropies.append(-mp.fsum(p*mp.log(p) for p in probs)); norms.append(mp.fsum(probs)-1); minima.append(min(probs))
        return dict(dps=dps,gap=mp.nstr((entropies[0]+entropies[2])/2-entropies[1],dps-5),entropies=[mp.nstr(z,dps-5) for z in entropies],normalization_residuals=[mp.nstr(z,10) for z in norms],minimum_probabilities=[mp.nstr(z,20) for z in minima])

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--out',default='results'); args=parser.parse_args()
    out=Path(args.out)
    if out.exists(): raise FileExistsError('Results already exist; bounded job will not be repeated')
    out.mkdir(parents=True); (out/'kernels').mkdir()
    started=time.time(); rng=np.random.default_rng(SEED)
    manifest=dict(seed=SEED,denominator=DEN,planned_bases={'8':6,'11':12,'12':12},steps=[.15,.4,.8],threads=1,pid=os.getpid(),numpy=np.__version__,start=started,exit_code=None)
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2))
    fields=['base_id','n','mode','kind','step_fraction','step','status','gap','curvature','H_mid','H_minus','H_plus','min_probability','normalization_residual','mobius_max_error','finite_difference_curvature','min_diagonal_separation','min_cross_block_bridge','min_supported_edge','exact_margin_mid','exact_margin_minus','exact_margin_plus','error']
    rows=[]; failures=0
    with (out/'candidate_ledger.csv').open('w',newline='') as fp:
        writer=csv.DictWriter(fp,fieldnames=fields); writer.writeheader()
        def append(row):
            rows.append(row); writer.writerow(row); fp.flush()
        for n,total in ((8,6),(11,12),(12,12)):
            P=Probe(n)
            for index in range(total):
                mode=index%3; key=f'n{n}_{index:02d}'; core=dict(base_id=key,n=n,mode=mode)
                try:
                    J,meta=make_kernel(P,rng,mode); M=J.astype(float)/DEN
                    fprint=fingerprint(J); cert=fraction_margin_certificate(J)
                    H,probs,norm,hh=P.event(M,True); eig,V=np.linalg.eigh(hh); d=V[:,-1]; D=np.einsum('p,pij->ij',d,P.B)
                    limit=step_limit(J,D); small=min(limit*.03,1e-4)
                    fd=(P.event(M+small*D)[0]+P.event(M-small*D)[0]-2*H)/small**2
                    mob_err=None
                    if n==8:
                        pm=P.mobius(M); mob_err=float(np.max(abs(pm-probs)))
                        if mob_err>1e-11: raise ArithmeticError('Mobius comparison failed')
                    if abs(fd-eig[-1])/(1+abs(eig[-1]))>2e-4: raise ArithmeticError('Hessian finite difference failed')
                    payload=dict(base_id=key,denominator=DEN,matrix_numerators=J.tolist(),basis_edges=P.edges,meta=meta,fingerprint=fprint,certificate=cert,largest_hessian_eigenvalue=float(eig[-1]),largest_hessian_direction=d.tolist(),step_limit=float(limit),chords=[])
                    base=core|dict(kind='BASE',status='NO_SIGNAL',curvature=float(eig[-1]),H_mid=H,min_probability=float(probs.min()),normalization_residual=norm,mobius_max_error=mob_err,finite_difference_curvature=float(fd),min_diagonal_separation=fprint['min_diagonal_separation'],min_cross_block_bridge=fprint['min_cross_block_bridge'],min_supported_edge=fprint['min_supported_edge'],exact_margin_mid=cert['margin'])
                    append(base)
                    for fraction in (.15,.4,.8):
                        t=fraction*limit; R=np.rint(t*D*DEN).astype(np.int64)
                        cf0=fraction_margin_certificate(J-R); cf1=fraction_margin_certificate(J+R)
                        fm=fingerprint(J-R); fp1=fingerprint(J+R)
                        Hm,pm,nm=P.event((J-R).astype(float)/DEN); Hp,pp,np1=P.event((J+R).astype(float)/DEN)
                        gap=(Hm+Hp)/2-H
                        row=core|dict(kind='CHORD',step_fraction=fraction,step=t,status='FLOAT_CANDIDATE' if gap>0 else 'NO_SIGNAL',gap=gap,curvature=float(eig[-1]),H_mid=H,H_minus=Hm,H_plus=Hp,min_probability=float(min(probs.min(),pm.min(),pp.min())),normalization_residual=max(norm,nm,np1),min_diagonal_separation=min(fprint['min_diagonal_separation'],fm['min_diagonal_separation'],fp1['min_diagonal_separation']),min_cross_block_bridge=min(fprint['min_cross_block_bridge'],fm['min_cross_block_bridge'],fp1['min_cross_block_bridge']),min_supported_edge=min(fprint['min_supported_edge'],fm['min_supported_edge'],fp1['min_supported_edge']),exact_margin_mid=cert['margin'],exact_margin_minus=cf0['margin'],exact_margin_plus=cf1['margin'])
                        chord=dict(fraction=fraction,difference_numerators=R.tolist(),minus_certificate=cf0,plus_certificate=cf1,gap_float=gap)
                        if gap>0:
                            chord['high_precision']=[hp_replay(J,R,60),hp_replay(J,R,100)]
                        payload['chords'].append(chord); append(row)
                    (out/'kernels'/f'{key}.json').write_text(json.dumps(payload,indent=2))
                except Exception as exc:
                    failures+=1; append(core|dict(kind='FAILURE',status='FAILED',error=repr(exc)))
                    (out/f'failure_{key}.txt').write_text(traceback.format_exc())
                    if n==8: raise
                print(json.dumps(dict(base=key,elapsed=time.time()-started,failures=failures)),flush=True)
    base_rows=[r for r in rows if r['kind']=='BASE']; chord_rows=[r for r in rows if r['kind']=='CHORD']
    summary=dict(status='SCOUT',bases=len(base_rows),chords=len(chord_rows),failures=failures,float_candidates=sum(r['status']=='FLOAT_CANDIDATE' for r in rows),max_curvature=max(r['curvature'] for r in base_rows),max_gap=max(r['gap'] for r in chord_rows),max_mobius_error=max(r['mobius_max_error'] for r in base_rows if r['mobius_max_error'] is not None),max_hessian_fd_error=max(abs(r['finite_difference_curvature']-r['curvature']) for r in base_rows),min_cross_block_bridge=min(r['min_cross_block_bridge'] for r in chord_rows),min_supported_edge=min(r['min_supported_edge'] for r in chord_rows),min_diagonal_separation=min(r['min_diagonal_separation'] for r in chord_rows),minimum_exact_margin=min(min(r['exact_margin_mid'],r['exact_margin_minus'],r['exact_margin_plus']) for r in chord_rows),minimum_event_probability=min(r['min_probability'] for r in chord_rows),max_normalization_residual=max(r['normalization_residual'] for r in chord_rows))
    manifest.update(elapsed=time.time()-started,exit_code=0,complete=True)
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)); (out/'summary.json').write_text(json.dumps(summary,indent=2)); print(json.dumps(summary),flush=True)

if __name__=='__main__': main()
