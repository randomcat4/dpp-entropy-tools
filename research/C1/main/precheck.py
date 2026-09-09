import json,sys,os,time
from pathlib import Path
import numpy as np
from core import data,atoms,det3

def run():
    A=np.eye(3)/100+3/5*np.outer([1,2,3],[1,2,3])/14
    S=np.diag([-1,1,1]); C=S@(np.eye(3)-A)@S
    t=(39791754487/17592186044416+79583508975/35184372088832)/2
    cases={'old_root_calibration':(1-t)*A+t*C,
           'connected_zero_edge':np.array([[.3,.06,.08],[.06,.4,0],[.08,0,.5]]),
           'dense_interior':np.array([[.3,.06,-.08],[.06,.4,.1],[-.08,.1,.5]])}
    out={'status':'FINITE_DIAGNOSTIC_ONLY','pid':os.getpid(),'python':sys.version,'numpy':np.__version__,'cases':{}}
    for name,K in cases.items():
        o=data(K); eig=np.linalg.eigvalsh(K)
        row={'K':K.tolist(),'p':o['p'].tolist(),'spectral_margin':float(min(eig.min(),1-eig.max())),
             'N_eigenvalues':np.linalg.eigvalsh(o['N']).tolist(),'M_eigenvalues':np.linalg.eigvalsh(o['M']).tolist(),
             'dalpha':float(o['dalpha']),'beta':float(o['beta']),'D_M':o['D'].tolist(),'Hpp_D_M':float(o['Hpp']),
             'Hessian_identity_residual':float(o['identity_residual']),'pair_cov_identity_residual':float(o['pair_residual']),
             'trace_normalization_residual':float(abs(o['eta']@o['dm']-1)),
             'optimizer_system_residual':float(np.max(abs(o['M']@o['dm']-o['eta']/o['alpha'])))}
        assert abs(sum(o['p'])-1)<1e-13
        assert row['Hessian_identity_residual']<1e-8
        assert row['pair_cov_identity_residual']<1e-8
        out['cases'][name]=row
    Path('precheck.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps(out,indent=2))

if __name__=='__main__':run()
