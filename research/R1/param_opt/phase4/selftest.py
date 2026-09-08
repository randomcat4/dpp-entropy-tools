import json
import numpy as np
from n3core import E,jets,hessian,signed_probs,sample,decode

def run():
    errors=[]
    for idx in range(24):
        x,kind,signs,o=sample(20260908401,idx)
        x[3:6]=np.maximum(x[3:6],-3);x[6]=np.log(.08);x[7]=1
        k=decode(x,kind,signs,o);p,g,h,_=jets(k)
        pc,gc,hc,_=jets(np.eye(3)-k)
        v=np.random.default_rng(idx).normal(size=6);v/=np.linalg.norm(v)
        V=np.einsum('a,aij->ij',v,E);t=2e-4
        pp=jets(k+t*V)[0];pm=jets(k-t*V)[0]
        dp=g@v;ddp=np.einsum('a,sab,b->s',v,h,v)
        directional=-sum(dp*dp/p+(1+np.log(p))*ddp)
        entropy=lambda q:-sum(q*np.log(q))
        fd=(entropy(pp)+entropy(pm)-2*entropy(p))/(t*t)
        err=dict(events=float(np.max(abs(p-signed_probs(k)))),complement=float(np.max(abs(p-pc[::-1]))),
          gradient_complement=float(np.max(abs(g+gc[::-1]))),hessian_complement=float(np.max(abs(h-hc[::-1]))),
          first_mass=float(np.max(abs(g.sum(axis=0)))),second_mass=float(np.max(abs(h.sum(axis=0)))),
          probability_fd=float(np.max(abs((pp+pm-2*p)/(t*t)-ddp))),entropy_fd=float(abs(fd-directional)))
        errors.append(err)
    maxima={key:max(z[key] for z in errors) for key in errors[0]}
    assert max(maxima[z] for z in maxima if z!='entropy_fd')<1e-7,maxima
    assert maxima['entropy_fd']<3e-4,maxima
    return dict(status='PASS',calls=24,seed=20260908401,maxima=maxima)
if __name__=='__main__':print(json.dumps(run(),indent=2))
