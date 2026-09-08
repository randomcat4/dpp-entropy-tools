"""Nine-center diagnostic, not a new random search. Writes only own results."""
from probe import *

def hessian(K):
    n=len(K); E=Events(n); p,inv=E.evaluate(K,True); lp=np.log(p)
    pairs=list(zip(*np.triu_indices(n))); basis=[]
    for i,j in pairs:
        B=np.zeros((n,n)); B[i,j]=B[j,i]=1 if i==j else 1/np.sqrt(2); basis.append(B)
    basis=np.array(basis); Q=np.einsum('qij,pjk->qpik',inv,basis,optimize=True)
    grad=np.trace(Q,axis1=2,axis2=3)
    hhlog=-np.einsum('qpij,qrji->qpr',Q,Q,optimize=True)
    HH=-np.einsum('q,q,qp,qr->pr',p,lp+1,grad,grad,optimize=True)-np.einsum('q,q,qpr->pr',p,lp,hhlog,optimize=True)
    return (HH+HH.T)/2,pairs,basis

def main():
    target=OUT/'mi_hessian_diagnostic.json'
    if target.exists(): raise FileExistsError('Diagnostic already exists')
    rows=[]; started=time.time()
    for n in (6,8,11):
        na=n//2
        for gamma in (F(1),F(2),F(5,2)):
            M=baseline(n,gamma); K=arr(M); E=Events(n)
            he,pairs,basis=hessian(K); ha,paira,_=hessian(K[:na,:na]); hb,pairb,_=hessian(K[na:,na:])
            marg=np.zeros_like(he); index={pair:i for i,pair in enumerate(pairs)}
            ia=[index[p] for p in paira]; ib=[index[(i+na,j+na)] for i,j in pairb]
            marg[np.ix_(ia,ia)]=ha; marg[np.ix_(ib,ib)]=hb
            hi=marg-he; eig,U=np.linalg.eigh(hi); direction=U[:,0]; Df=np.einsum('p,pij->ij',direction,basis)
            D=[[F(int(round(Df[i,j]*10**9)),10**9) for j in range(n)] for i in range(n)]
            d=arr(D); vals=np.linalg.eigvalsh(d); rank=int(sum(abs(vals)>1e-7))
            cap=limit(M,D,na); step=F(max(1,math.floor(cap*.4*10**6)),10**6)
            infos=[E.info(E.evaluate(arr(combine(M,D,s*step)))) for s in (-1,0,1)]
            gap=(infos[0]['E']+infos[2]['E'])/2-infos[1]['E']; da=(infos[0]['A']+infos[2]['A'])/2-infos[1]['A']; db=(infos[0]['B']+infos[2]['B'])/2-infos[1]['B']; bump=infos[1]['I']-(infos[0]['I']+infos[2]['I'])/2
            h=min(float(step)*.02,1e-4); fd=(E.info(E.evaluate(K-h*d))['I']+E.info(E.evaluate(K+h*d))['I']-2*infos[1]['I'])/h**2
            row=dict(n=n,gamma=str(gamma),minimum_MI_hessian_eigenvalue=float(eig[0]),maximum_entropy_hessian_eigenvalue=float(np.linalg.eigvalsh(he)[-1]),direction_rank_float=rank,direction_numerators=[[int(x*10**9) for x in row] for row in D],direction_denominator=10**9,step=str(step),MI_curvature_fd=fd,Delta_E=gap,Delta_A=da,Delta_B=db,MI_bump=bump,marginal_deficit_sum=-da-db,information_identity_residual=gap-da-db-bump,certificates=[certificate(combine(M,D,s*step)) for s in (-1,0,1)],cross_norm_min=coupling_min_exact(M,D,step,na),status='FLOAT_CANDIDATE' if gap>0 else 'NO_SIGNAL')
            if gap>0: row['high_precision']=[high_precision(M,D,step,60),high_precision(M,D,step,100)]
            rows.append(row); print(json.dumps({k:row[k] for k in ('n','gamma','minimum_MI_hessian_eigenvalue','Delta_E','MI_bump')}),flush=True)
    result=dict(planned_centers=9,completed_centers=len(rows),random_samples_added=0,elapsed=time.time()-started,exit_code=0,rows=rows)
    target.write_text(json.dumps(result,indent=2),encoding='utf-8')

if __name__=='__main__': main()
