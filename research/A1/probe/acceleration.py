"""One post-batch diagnostic: 512 fixed centers, no further optimization."""
import json
import numpy as np
import probe
rows=json.loads((probe.ROOT/'centers.json').read_text())
out=[]
for row in rows:
    v=np.array(list(map(float,map(probe.F,row['exact']))))
    lam,d,p,fi,ac=probe.hessian(v)
    eig,U=np.linalg.eigh(ac[3:,3:])
    q=ac.diagonal()[3:]/2
    L=sum((-1)**(3-mask.bit_count())*np.log(p[mask]) for mask in range(8))
    pred=np.zeros((6,6))
    for i,j,e in [(0,1,3),(0,2,4),(1,2,5)]:
        pred[i,j]=pred[j,i]=-q[e-3]
        pred[e,e]=2*q[e-3]
        k=3-i-j
        pred[k,e]=pred[e,k]=2*v[e]*L
    for i,j,k in [(3,4,5),(3,5,4),(4,5,3)]: pred[i,j]=pred[j,i]=-2*v[k]*L
    assert np.max(abs(ac-pred))<1e-10
    out.append(dict(id=row['id'],q=q.tolist(),L=L,offdiagonal_acceleration_max=float(eig[-1]),direction=U[:,-1].tolist(),identity_error=float(np.max(abs(ac-pred)))))
probe.save(probe.ROOT/'acceleration.json',dict(target_calls=probe.COUNT,centers=out,best=max(out,key=lambda r:r['offdiagonal_acceleration_max']),positive_count=sum(r['offdiagonal_acceleration_max']>1e-9 for r in out)))
