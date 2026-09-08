"""Independent bounded audit of round6; no imports from author evaluators."""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key]='1'
import numpy as np
import csv, json, time, hashlib
from pathlib import Path
BASE=Path(__file__).resolve().parent
SOURCE=BASE.parent/'results_server_round6'

def atoms(K):
    n=len(K); masks=np.arange(1<<n,dtype=np.int64)
    absent=1-((masks[:,None]>>np.arange(n))&1)
    mixed=np.broadcast_to(K,(len(masks),n,n)).copy()
    mixed[:,np.arange(n),np.arange(n)]-=absent
    sign,lp=np.linalg.slogdet(mixed)
    assert np.all(sign*((-1.)**absent.sum(axis=1))>0)
    return np.exp(lp),lp,mixed

def mobius(K):
    n=len(K); p=np.empty(1<<n)
    for s in range(1<<n):
        ids=[j for j in range(n) if s>>j&1]
        p[s]=np.linalg.det(K[np.ix_(ids,ids)])
    for i in range(n):
        for s in range(1<<n):
            if not s>>i&1: p[s]-=p[s|(1<<i)]
    return p

def lens(K):
    n=len(K); L=np.linalg.solve(np.eye(n)-K,K)
    logbase=np.linalg.slogdet(np.eye(n)-K)[1]
    p=np.empty(1<<n)
    for s in range(1<<n):
        ids=[j for j in range(n) if s>>j&1]
        sign,ld=np.linalg.slogdet(L[np.ix_(ids,ids)])
        assert sign>0
        p[s]=np.exp(logbase+ld)
    return p

def directional(K,D):
    p,lp,mixed=atoms(K)
    X=np.linalg.solve(mixed,np.broadcast_to(D,mixed.shape))
    score=np.trace(X,axis1=1,axis2=2)
    acc=score**2-np.einsum('qij,qji->q',X,X)
    fisher=np.sum(p*score**2); acceleration=-np.sum(p*lp*acc)
    return {'H':-float(p@lp),'Fisher_positive':float(fisher),'acceleration':float(acceleration),
            'H2':float(acceleration-fisher),'rho':float(acceleration/fisher),
            'normalization_error':float(p.sum()-1),'sum_p1':float(p@score),'sum_p2':float(p@acc),
            'min_probability':float(p.min()),'probabilities':p,'acc_terms':-p*lp*acc,
            'fisher_terms':p*score**2}

def matrices(K):
    n=len(K); coords=[(i,j) for i in range(n) for j in range(i,n)]
    basis=np.zeros((len(coords),n,n))
    for a,(i,j) in enumerate(coords):
        basis[a,i,j]=basis[a,j,i]=1 if i==j else 1/np.sqrt(2)
    p,lp,mixed=atoms(K); m=len(coords)
    F=np.zeros((m,m)); A=np.zeros((m,m))
    for first in range(0,len(p),32):
        last=min(first+32,len(p)); B=np.linalg.inv(mixed[first:last])
        score=np.einsum('qij,aij->qa',B,basis)
        be=np.einsum('qij,ajk->qaik',B,basis,optimize=True)
        tr=np.einsum('qaij,qbji->qab',be,be,optimize=True)
        F+=np.einsum('q,qa,qb->ab',p[first:last],score,score,optimize=True)
        A+=np.einsum('q,qab->ab',p[first:last]*lp[first:last],tr,optimize=True)
        A-=np.einsum('q,qa,qb->ab',p[first:last]*lp[first:last],score,score,optimize=True)
    F=(F+F.T)/2; A=(A+A.T)/2
    eig,U=np.linalg.eigh(F); assert eig[0]>0
    W=U/np.sqrt(eig)[None,:]
    rho,V=np.linalg.eigh(W.T@A@W)
    v=W@V[:,-1]; D=np.einsum('a,aij->ij',v,basis)
    residual=np.linalg.norm(A@v-rho[-1]*(F@v))/(np.linalg.norm(A@v)+np.linalg.norm(F@v))
    D/=np.linalg.norm(D,2)
    return {'rho_max':float(rho[-1]),'fisher_eigen_min':float(eig[0]),
            'fisher_eigen_max':float(eig[-1]),'fisher_condition':float(eig[-1]/eig[0]),
            'generalized_residual':float(residual),'total_hessian_max':float(np.linalg.eigvalsh(A-F)[-1]),
            'direction':D,'fisher_matrix':F,'acceleration_matrix':A,'basis':basis}

def serial_result(row):
    return {k:v for k,v in row.items() if not isinstance(v,np.ndarray)}

def main():
    start=time.time(); records=[]
    allrows=list(csv.DictReader((SOURCE/'candidate_ledger.csv').open(encoding='utf-8')))
    groups=[]
    for n in (12,13):
        for mode in range(4):
            rows=[r for r in allrows if int(r['n'])==n and int(r['mode'])==mode]
            groups.append({'n':n,'mode':mode,'centers':len(rows),
                           'rho_max':max(float(r['mechanism_ratio']) for r in rows),
                           'margin_min':min(float(r['margin']) for r in rows),
                           'positive_total_count':sum(float(r['lambda_max'])>0 for r in rows)})
    for name in ('best_mechanism_case','best_case'):
        data=np.load(SOURCE/(name+'.npz')); rawK=data['kernel']; rawD=data['direction']
        K=(rawK+rawK.T)/2; D=(rawD+rawD.T)/2
        point=directional(K,D); full=matrices(K)
        direct=mobius(K); lp=lens(K); p=point['probabilities']
        spectrum=np.linalg.eigvalsh(K)
        row={'case':name,'n':len(K),'raw_kernel_asymmetry':float(np.max(abs(rawK-rawK.T))),
             'raw_direction_asymmetry':float(np.max(abs(rawD-rawD.T))),
             'kernel_spectrum':spectrum.tolist(),'direction_spectrum':np.linalg.eigvalsh(D).tolist(),
             'commutator_frobenius':float(np.linalg.norm(K@D-D@K)),
             'mobius_max_abs_error':float(np.max(abs(direct-p))),
             'mobius_max_relative_error':float(np.max(abs(direct-p)/p)),
             'mobius_negative_atoms':int(np.sum(direct<0)),
             'L_ensemble_max_relative_error':float(np.max(abs(lp-p)/p)),
             'directional':serial_result(point),'generalized':serial_result(full)}
        if name=='best_mechanism_case':
            overlap=abs(np.sum(D*full['direction']))/(np.linalg.norm(D)*np.linalg.norm(full['direction']))
            row['frozen_vs_new_direction_cosine']=float(overlap)
            contributions=[]
            for cutoff in (1e-12,1e-10,1e-8,1e-6,1e-4):
                sel=p<cutoff
                contributions.append({'cutoff':cutoff,'atoms':int(sel.sum()),
                                      'probability_mass':float(p[sel].sum()),
                                      'Fisher':float(point['fisher_terms'][sel].sum()),
                                      'acceleration':float(point['acc_terms'][sel].sum())})
            row['rare_event_contributions']=contributions
            np.savez_compressed(BASE/'independent_frozen.npz',kernel=K,direction=D,new_direction=full['direction'])
            params={key:[[repr(float(x)) for x in line] for line in value] for key,value in [('kernel',K),('direction',D)]}
            (BASE/'rational_decimal_parameters.json').write_text(json.dumps(params,indent=2),encoding='utf-8')
            regularized=[]
            # Deterministic boundary-distance homotopy; no random samples or optimizer.
            for epsilon in (0.0001,0.001,0.01,0.05,0.1):
                M=(1-2*epsilon)*K+epsilon*np.eye(len(K))
                a=directional(M,D); opt=matrices(M)
                regularized.append({'epsilon':epsilon,'margin':float(min(np.linalg.eigvalsh(M)[0],1-np.linalg.eigvalsh(M)[-1])),
                                    'frozen_direction':serial_result(a),'reoptimized_direction':serial_result(opt),
                                    'reoptimized_direction_spectrum':np.linalg.eigvalsh(opt['direction']).tolist()})
            row['interior_homotopy']=regularized
        records.append(row)
        print(name,json.dumps({'rho_max':full['rho_max'],'directional':serial_result(point)}),flush=True)
    out={'status':'INDEPENDENT_FLOAT_RECHECK','source_center_denominator':len(allrows),
         'source_groups':groups,'independently_recomputed_centers':7,'source_seed':2026090815,
         'random_draws':0,'records':records,'exit_code':0,'elapsed_seconds':time.time()-start}
    (BASE/'float_recheck.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print('elapsed',out['elapsed_seconds'],flush=True)

if __name__=='__main__': main()
