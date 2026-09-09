"""Bounded four-point fixed-nullspace pilot; proper events only, no full atom."""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key]='1'
import hashlib,itertools,json,platform,time
from fractions import Fraction as F
from pathlib import Path
import numpy as np

def house(w):
    n=len(w);den=sum(x*x for x in w)
    return [[F(i==j)-F(2*w[i]*w[j],den) for j in range(n)] for i in range(n)]
def mm(a,b):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def tr(a):return list(map(list,zip(*a)))
def det(a):
    if not a:return F(1)
    a=[r[:] for r in a];s=F(1)
    for k in range(len(a)):
        p=next((i for i in range(k,len(a)) if a[i][k]),None)
        if p is None:return F(0)
        if p!=k:a[k],a[p]=a[p],a[k];s=-s
        v=a[k][k];s*=v
        for i in range(k+1,len(a)):
            fac=a[i][k]/v
            for j in range(k+1,len(a)):a[i][j]-=fac*a[k][j]
    return s
def exact_support(u,a):
    k=mm(mm(u,a),tr(u));ps=[]
    for s in range(16):
        m=[[k[i][j]-F(i==j and not(s>>i&1)) for j in range(4)] for i in range(4)]
        ps.append((-1)**(4-s.bit_count())*det(m))
    assert all(p>0 for p in ps[:15]) and ps[15]==0 and sum(ps)==1
    return [str(p) for p in ps]
def basis():
    out=[]
    for i in range(3):
        for j in range(i,3):
            b=np.zeros((3,3));b[i,j]=b[j,i]=1 if i==j else 1/np.sqrt(2);out.append(b)
    return np.array(out)
def atoms(k):
    masks=range(15);a=np.array([k-np.diag([not(s>>i&1) for i in range(4)]) for s in masks])
    sg,lp=np.linalg.slogdet(a);expected=np.array([(-1)**(4-s.bit_count()) for s in masks])
    assert np.all(sg==expected)
    p=np.exp(lp);assert abs(sum(p)-1)<1e-11
    return p,lp,a
def h(k):
    p,lp,_=atoms(k);return -p@lp
def curvature(u,a):
    k=u@a@u.T;b=np.einsum('ij,pjk,lk->pil',u,basis(),u)
    p,lp,m=atoms(k);inv=np.linalg.inv(m)
    score=np.einsum('sij,pji->sp',inv,b)
    prod=np.einsum('sij,pjk->spik',inv,b)
    pp=p[:,None,None]*(score[:,:,None]*score[:,None,:]-np.einsum('spij,sqji->spq',prod,prod))
    fisher=-np.einsum('s,sp,sq->pq',p,score,score)
    acceleration=-np.einsum('s,spq->pq',lp,pp)
    total=fisher+acceleration;total=(total+total.T)/2
    vals,vecs=np.linalg.eigh(total);c=vecs[:,-1];v=np.einsum('p,pij->ij',c,basis())
    vphys=u@v@u.T;g=score@c;p1=p*g;p2=np.einsum('p,spq,q->s',c,pp,c)
    bounds=[]
    for mat in (a,np.eye(3)-a):
        x,q=np.linalg.eigh(mat);z=(q/np.sqrt(x))@q.T
        bounds.append(1/max(abs(np.linalg.eigvalsh(z@v@z))))
    r=min(bounds);chords=[]
    for alpha in (.1,.5,.9):
        t=alpha*r;am=a-t*v;ap=a+t*v
        chords.append(dict(t=t,delta=float((h(u@am@u.T)+h(u@ap@u.T))/2-h(k)),
            latent_margin=float(min(np.linalg.eigvalsh(am)[0],np.linalg.eigvalsh(ap)[0],1-np.linalg.eigvalsh(am)[-1],1-np.linalg.eigvalsh(ap)[-1]))))
    step=1e-4*r;fd=(h(k+step*vphys)+h(k-step*vphys)-2*h(k))/(step*step)
    return dict(K=k.tolist(),A=a.tolist(),V=v.tolist(),D=vphys.tolist(),radius=float(r),
        hessian=total.tolist(),hessian_spectrum=vals.tolist(),fisher_along_top=float(c@fisher@c),
        acceleration_along_top=float(c@acceleration@c),commutator=float(np.linalg.norm(a@v-v@a)),
        proper_events=[dict(mask=s,p=float(p[s]),p1=float(p1[s]),p2=float(p2[s])) for s in range(15)],
        zero_full_event='identically zero from fixed common nullspace; not evaluated numerically',
        derivative_sums=[float(sum(p1)),float(sum(p2))],finite_difference=float(fd),chords=chords)

def main():
    out=Path(__file__).parent/'results';out.mkdir(exist_ok=False);start=time.time()
    report=dict(status='RUNNING',pid=os.getpid(),threads=1,seed=None,python=platform.python_version(),
        numpy=np.__version__,source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        source_commit='edc5d9b (frozen definition); new pilot source bound by SHA256',
        command='python research/N4/round2/pilot/face_pilot.py',start_unix=start)
    (out/'manifest.json').write_text(json.dumps(report,indent=2))
    rot=house([1,2,3]);diag=lambda xs:[[F(xs[i]) if i==j else F(0) for j in range(3)] for i in range(3)]
    aa=[diag([F(1,7),F(3,7),F(6,7)]),mm(mm(rot,diag([F(1,20),F(2,5),F(19,20)])),tr(rot)),diag([F(2,5)]*3)]
    rows=[]
    for w in ([1,1,1,1],[1,2,2,1],[1,2,3,4],[1,2,3,8]):
        q=house(w);u=[row[:3] for row in q];null=[row[3] for row in q]
        assert all(null) and mm(tr(u),u)==diag([1]*3)
        for idx,a in enumerate(aa):
            masses=exact_support(u,a)
            row=curvature(np.array(u,dtype=float),np.array(a,dtype=float))
            row.update(index=len(rows),frame_w=w,A_family=idx,U_rational=[[str(x) for x in r] for r in u],
                A_rational=[[str(x) for x in r] for r in a],null_rational=list(map(str,null)),exact_events=masses)
            rows.append(row)
    with (out/'cases.jsonl').open('w') as f:
        for row in rows:f.write(json.dumps(row)+'\n')
    best=max(rows,key=lambda row:row['hessian_spectrum'][-1]);(out/'best.json').write_text(json.dumps(best,indent=2))
    report.update(status='SCOUT_COMPLETE',exit_code=0,centers=len(rows),face_hessians=len(rows),
        exact_support_event_masses=16*len(rows),retained_chords=3*len(rows),
        finite_difference_checks=len(rows),entropy_calls=10*len(rows),
        max_curvature=best['hessian_spectrum'][-1],max_gap=max(c['delta'] for r in rows for c in r['chords']),
        elapsed_seconds=time.time()-start,warning='finite scout only; no face-class theorem or positive certificate')
    (out/'manifest.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
if __name__=='__main__':main()
