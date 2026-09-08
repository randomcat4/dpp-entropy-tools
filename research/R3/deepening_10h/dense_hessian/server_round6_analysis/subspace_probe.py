"""Deterministic mechanism-subspace comparison at the single frozen center."""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[key]='1'
import numpy as np
import json,time
from pathlib import Path
from recheck import matrices,directional,serial_result
BASE=Path(__file__).resolve().parent

def main():
    start=time.time(); frozen=np.load(BASE/'independent_frozen.npz')
    K,D=frozen['kernel'],frozen['direction']; n=len(K)
    full=matrices(K);F,A,basis=[full[k] for k in ('fisher_matrix','acceleration_matrix','basis')]
    eig,U=np.linalg.eigh(K)
    spaces={'commuting_with_K':np.einsum('ij,kj->jik',U,U),
            'physical_diagonal':np.asarray([np.diag(np.eye(n)[i]) for i in range(n)]),
            'identity_only':np.eye(n)[None,:,:]}
    rows=[]
    for label,projectors in spaces.items():
        C=np.einsum('aij,bij->ab',basis,projectors)
        f=C.T@F@C; a=C.T@A@C
        lam,V=np.linalg.eigh(f);W=V/np.sqrt(lam)[None,:]
        rho,vec=np.linalg.eigh(W.T@a@W);v=W@vec[:,-1]
        direction=np.einsum('a,aij->ij',v,projectors)
        direction/=np.linalg.norm(direction,2)
        if np.trace(direction)<0: direction=-direction
        rows.append({'subspace':label,'dimension':len(projectors),'rho_max':float(rho[-1]),
                     'directional_recheck':serial_result(directional(K,direction)),
                     'direction_eigenvalues':np.linalg.eigvalsh(direction).tolist(),
                     'commutator_frobenius':float(np.linalg.norm(K@direction-direction@K))})
    transformed=U.T@D@U
    spectral_diag=U@np.diag(np.diag(transformed))@U.T
    rows.append({'subspace':'frozen_direction_commuting_projection','dimension':1,
                 'directional_recheck':serial_result(directional(K,spectral_diag)),
                 'removed_offdiagonal_frobenius':float(np.linalg.norm(D-spectral_diag)),
                 'full_direction_frobenius':float(np.linalg.norm(D))})
    # How much acceleration is carried by off-diagonal eigenbasis motion?
    B=D-spectral_diag
    a0=directional(K,spectral_diag); a1=directional(K,B); allv=directional(K,D)
    cross={k:(allv[k]-a0[k]-a1[k])/2 for k in ('Fisher_positive','acceleration','H2')}
    out={'status':'BOUNDED_SUBSPACE_DIAGNOSTIC','center_count':1,'subspaces':rows,
         'full_rho':full['rho_max'],'decomposition':{
             'commuting_part':serial_result(a0),'noncommuting_part':serial_result(a1),
             'mixed_bilinear':cross},'random_draws':0,'exit_code':0,'elapsed_seconds':time.time()-start}
    (BASE/'subspace_probe.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
