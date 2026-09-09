"""One bounded analytic-mechanism diagnostic; no random scan."""
import os,sys,json
from pathlib import Path
import numpy as np
from core import data,E,PAIRS

def cv(A):return np.array([A[i,j] for i,j in PAIRS])
def main():
    K=np.array([[.3,.06,-.08],[.06,.4,.1],[-.08,.1,.5]])
    o=data(K); tilts=[]
    for i in range(3):
        A=np.zeros((3,3));A[i,i]=1
        Q=A@K+K@A-2*K@A@K; q=cv(Q)
        target=np.zeros(6);target[i]=2
        tilts.append({'i':i,'Q':Q.tolist(),'Lambda_derivative':float(o['g']@q),
          'score_identity_error':float(np.max(abs(o['J']@q/o['p']-2*(np.array([s>>i&1 for s in range(8)])-K[i,i])))),
          'F_mixed_identity_error':float(np.max(abs(o['F']@q-target)))})
    rows=[]
    # Exactly 8 fixed star cases, primarily a check of beta sign speculation.
    for x in [.05,.3,.5,.95]:
        for v in [.1,.5]:
            K=np.diag([x,.3,.7]);K[0,1]=K[1,0]=v*np.sqrt(x*(1-x)*.3*.7)
            K[0,2]=K[2,0]=v*np.sqrt(x*(1-x)*.7*.3)
            o=data(K)
            rows.append({'x':x,'edge_scale':v,'beta':float(o['beta']),'dalpha':float(o['dalpha']),
                         'Fpair_rank':int(np.linalg.matrix_rank(o['Fpair']))})
    out={'status':'FINITE_DIAGNOSTIC_ONLY','pid':os.getpid(),'python':sys.version,'tilt_identities':tilts,'fixed_stars':rows}
    Path('tilt_probe.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
