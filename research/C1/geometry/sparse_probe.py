"""Six fixed points in the previously excluded support-loss boundary layer."""
from probe import *
mp.mp.dps=110
rows=[]
lam=mp.mpf(7)/10
for exponent in [12,24]:
    eps=mp.mpf(10)**(-exponent); L=-mp.log(eps)
    for kap in [mp.mpf(1)/10,mp.mpf(1),mp.mpf(10)]:
        w3=kap*eps
        weights=[(1-w3)*mp.mpf(2)/5,(1-w3)*mp.mpf(3)/5,w3]
        u=mp.matrix([mp.sqrt(x) for x in weights])
        da,beta,raw,pmin=calc(eps*mp.eye(3)+lam*u*u.T)
        rows.append(dict(epsilon=st(eps),kappa=st(kap),dalpha=st(da),beta=st(beta),
            scaled_raw=st(raw*L),scaled_beta=st(beta*L/eps),pmin=st(pmin)))
print(json.dumps(dict(pid=os.getpid(),python=sys.version,mpmath=mp.__version__,digits=mp.mp.dps,
    inputs=dict(lam='7/10',split='2/5',exponents=[12,24],kappas=['1/10','1','10']),rows=rows),indent=2))
