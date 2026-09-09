"""C2 bounded weak-low-layer mechanism, version 1.1; run with one BLAS thread."""
import os, sys, json, hashlib, itertools, platform, time
from pathlib import Path
import numpy as np
import scipy, scipy.linalg as la
import sympy as sp
import mpmath as mp

OUT=Path(__file__).resolve().parent
SUB=[s for k in range(4) for s in itertools.combinations(range(5),k)]
SIZES=np.array(list(map(len,SUB)))
I=sp.eye(3)
a=sp.Matrix([1,2,3,4,5]); b=sp.Matrix([2,-1,3,-2,1])
U=((sp.eye(5)-2*a*a.T/(a.dot(a)))*(sp.eye(5)-2*b*b.T/(b.dot(b))))[:,:3]
x=sp.symbols('x0:6'); AA=sp.Matrix([[x[0],x[3],x[4]],[x[3],x[1],x[5]],[x[4],x[5],x[2]]])
ES=[AA.diff(z) for z in x]; EN=np.array([np.array(e,float) for e in ES]); MET=np.diag([1,1,1,2,2,2])
d=sp.expand(AA.det()); adj=AA.adjugate()
pol=[]
for s in SUB:
    if len(s)==0: v=(I-AA).det()
    elif len(s)==1:
        r=U[s[0],:].T; v=(r.T*(AA*AA+(1-sp.trace(AA))*AA+d*I)*r)[0]
    elif len(s)==2:
        w=U[s[0],:].T.cross(U[s[1],:].T); v=(w.T*(adj-d*I)*w)[0]
    else: v=d*U[list(s),:].det()**2
    pol.append(sp.expand(v))
PP=sp.Matrix(pol); JJ=PP.jacobian(x); HH=[sp.hessian(v,x) for v in pol]
pf=sp.lambdify([x],PP,'numpy'); jf=sp.lambdify([x],JJ,'numpy'); hf=sp.lambdify([x],HH,'numpy')
q=[U[list(s),:].det()**2 for s in SUB if len(s)==3]
c=float(-sum(v*sp.log(v) for v in q)); df=sp.lambdify([x],sp.hessian(d,x),'numpy')
def coords(A): return np.array([A[0,0],A[1,1],A[2,2],A[0,1],A[0,2],A[1,2]])
def mat(v): return np.einsum('i,ijk->jk',v,EN)
def jets(A):
    xx=coords(A); return np.asarray(pf(xx)).ravel(),np.asarray(jf(xx)),np.asarray(hf(xx))
def inclusion(A):
    """Independent determinant derivative rule followed by Mobius inversion."""
    un=np.array(U,float); K=un@A@un.T; Ds=np.array([un@e@un.T for e in EN])
    m=np.zeros(26); j=np.zeros((26,6)); h=np.zeros((26,6,6)); m[0]=1
    for n,s in enumerate(SUB[1:],1):
        ix=np.ix_(s,s); k=K[ix]; ds=np.array([dd[ix] for dd in Ds]); det=np.linalg.det(k)
        z=np.array([np.linalg.solve(k,dd) for dd in ds]); tr=np.trace(z,axis1=1,axis2=2)
        m[n]=det; j[n]=det*tr; h[n]=det*(np.outer(tr,tr)-np.einsum('aij,bji->ab',z,z))
    p=np.zeros(26); J=np.zeros((26,6)); H=np.zeros((26,6,6))
    for n,s in enumerate(SUB):
        for k,t in enumerate(SUB):
            if set(s)<=set(t):
                sign=(-1)**(len(t)-len(s)); p[n]+=sign*m[k]; J[n]+=sign*j[k]; H[n]+=sign*h[k]
    return p,J,H
def matrices(A):
    p,J,B=jets(A); F=[]; L=[]
    for k in range(4):
        sel=SIZES==k; F.append(J[sel].T@(J[sel]/p[sel,None])); L.append(-np.einsum('s,sij->ij',np.log(p[sel]),B[sel]))
    return p,J,B,np.array(F),np.array(L)
def record(A,v,label,cid):
    v=v/np.sqrt(v@MET@v); V=mat(v); p,J,B,F,L=matrices(A)
    f=np.einsum('i,kij,j->k',v,F,v); l=np.einsum('i,kij,j->k',v,L,v)
    eigA=la.eigvalsh(A); ia=la.inv(la.sqrtm(A)); ic=la.inv(la.sqrtm(np.eye(3)-A))
    step=1/max(np.max(np.abs(la.eigvalsh(ia@V@ia))),np.max(np.abs(la.eigvalsh(ic@V@ic))))
    geom=float(c*v@df(coords(A))@v)
    return dict(center=cid,mode=label,A=A.tolist(),V=V.tolist(),fisher=f.tolist(),log_acceleration=l.tolist(),curvature=(l-f).tolist(),total=float(sum(l-f)),geometry=geom,low_fisher=float(sum(f[:3])),top_geometry_over_fisher=float(geom/f[3]) if f[3]>1e-20 else None,commutator_norm=float(la.norm(A@V-V@A)),spectrum=eigA.tolist(),symmetric_step_limit=float(step))

def preflight():
    Ar=sp.Matrix([[sp.Rational(3,5),sp.Rational(1,20),sp.Rational(-1,30)],[sp.Rational(1,20),sp.Rational(2,3),sp.Rational(1,40)],[sp.Rational(-1,30),sp.Rational(1,40),sp.Rational(7,10)]])
    A=np.array(Ar,float); p,J,H=jets(A); pp,jj,hh=inclusion(A)
    exact_m=[]; K=U*Ar*U.T
    for s in SUB: exact_m.append(K[list(s),list(s)].det())
    exact_p=[sum((-1)**(len(t)-len(s))*exact_m[k] for k,t in enumerate(SUB) if set(s)<=set(t)) for s in SUB]
    mapping=dict(zip(x,[Ar[0,0],Ar[1,1],Ar[2,2],Ar[0,1],Ar[0,2],Ar[1,2]]))
    assert all(sp.cancel(v.subs(mapping)-w)==0 for v,w in zip(pol,exact_p))
    assert sp.expand(sum(pol))==1 and sum(q)==1 and U.T*U==I
    errs=[float(np.max(abs(p-pp))),float(np.max(abs(J-jj))),float(np.max(abs(H-hh)))]
    assert max(errs)<1e-11
    vv=np.array([.2,-.3,.4,.5,-.1,.25]); V=mat(vv); hhstep=1e-4
    plus=jets(A+hhstep*V)[0]; minus=jets(A-hhstep*V)[0]
    fd1=float(max(abs((plus-minus)/(2*hhstep)-J@vv)))
    fd2=float(max(abs((plus-2*p+minus)/hhstep**2-np.einsum('i,sij,j->s',vv,H,vv))))
    assert fd1<1e-7 and fd2<1e-7
    return dict(exact_probability_calibration=True,exact_normalization=True,independent_jet_errors=errs,fd1_error=fd1,fd2_error=fd2,normalization_jet=[float(sum(p)-1),float(max(abs(sum(J)))),float(np.max(abs(sum(H))))])

def exact_certificate(rec,name):
    """Rationalize one negative fixture; exact polynomial jets and interval logs."""
    A=sp.Matrix([[sp.Rational(str(z)).limit_denominator(100000) for z in row] for row in rec['A']])
    V=sp.Matrix([[sp.Rational(str(z)).limit_denominator(10000) for z in row] for row in rec['V']])
    t=sp.symbols('t'); h=sp.Rational(1,100); sub=dict(zip(x,[ (A+t*V)[i,j] for i,j in [(0,0),(1,1),(2,2),(0,1),(0,2),(1,2)]]))
    poly=[sp.Poly(v.subs(sub),t) for v in pol]
    ps=[v.nth(0) for v in poly]; p1=[v.nth(1) for v in poly]; p2=[2*v.nth(2) for v in poly]
    ends=[[v.eval(z) for v in poly] for z in [-h,0,h]]
    assert all(z>0 for row in ends for z in row)
    minors=[]
    for z in [-h,0,h]:
        for M in [A+z*V,I-A-z*V]:
            mm=[M[:k,:k].det() for k in [1,2,3]]; assert all(w>0 for w in mm); minors.append([str(w) for w in mm])
    mp.iv.dps=70
    def ivrat(z): return mp.iv.mpf(int(sp.numer(z)))/mp.iv.mpf(int(sp.denom(z)))
    def entropy(row): return -sum(ivrat(z)*mp.iv.log(ivrat(z)) for z in row)
    layer=[]
    for k in range(4):
        inds=[i for i,s in enumerate(SUB) if len(s)==k]
        f=sum(ivrat(p1[i])**2/ivrat(ps[i]) for i in inds)
        l=-sum(ivrat(p2[i])*mp.iv.log(ivrat(ps[i])) for i in inds)
        layer.append(dict(fisher=str(f),log_acceleration=str(l),curvature=str(l-f)))
    cur=-sum(ivrat(p1[i])**2/ivrat(ps[i])+ivrat(p2[i])*mp.iv.log(ivrat(ps[i])) for i in range(26))
    chord=(entropy(ends[0])+entropy(ends[2]))/2-entropy(ends[1])
    assert cur<0 and chord<0
    data=dict(A=[[str(z) for z in row] for row in A.tolist()],V=[[str(z) for z in row] for row in V.tolist()],h=str(h),events=[list(s) for s in SUB],p=[str(z) for z in ps],p_prime=[str(z) for z in p1],p_second=[str(z) for z in p2],probabilities_minus_center_plus=[[str(z) for z in row] for row in ends],sylvester_minors=minors,layers=layer,curvature_interval=str(cur),chord_interval=str(chord),interval_precision=70)
    (OUT/f'{name}.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
    return dict(name=name,curvature_interval=str(cur),chord_interval=str(chord))

def main():
    check=preflight(); (OUT/'preflight.json').write_text(json.dumps(check,indent=2),encoding='utf-8'); print('PREFLIGHT',check,flush=True)
    spectra=[[.2,.4,.6],[.3,.5,.7],[.4,.6,.8],[.2,.65,.95],[.35,.75,.9],[.55,.65,.8],[.58,.67,.75],[.65,.65,.65]]
    rr=[np.eye(3)]
    for vec in [[1,2,3],[2,-1,1]]:
        z=np.array(vec,float); rr.append(np.eye(3)-2*np.outer(z,z)/(z@z))
    rows=[]; centers=[]
    for rot,R in enumerate(rr):
        for si,spec in enumerate(spectra):
            A=R@np.diag(spec)@R.T; cid=f'r{rot}s{si}'; p,J,B,F,L=matrices(A); FL=sum(F[:3]); HT=sum(L-F)
            we,wv=la.eigh(FL,MET); he,hv=la.eigh(HT,MET); ge,gv=la.eigh(HT,FL); te,tv=la.eigh(c*df(coords(A)),FL)
            je,jv=la.eigh(J[SIZES<=2].T@J[SIZES<=2],MET)
            modes=[('weak_fisher',wv[:,0]),('weak_jacobian',jv[:,0]),('max_full',hv[:,-1]),('max_full_per_low_fisher',gv[:,-1]),('max_geometry_per_low_fisher',tv[:,-1])]
            if abs(sum(spec)-2)<1e-8: modes.append(('pair_null',coords(A@(np.eye(3)-A))))
            for label,v in modes: rows.append(record(A,v,label,cid))
            centers.append(dict(id=cid,spectrum=spec,orientation=rot,low_fisher_eigenvalues=we.tolist(),full_hessian_eigenvalues=he.tolist(),generalized_full_eigenvalues=ge.tolist(),geometry_over_low_fisher_max=float(te[-1])))
    best=max(rows,key=lambda z:z['total']); geometry=max((z for z in rows if z['commutator_norm']>1e-6 and z['geometry']>0),key=lambda z:(z['top_geometry_over_fisher'] or -1))
    (OUT/'all_candidates.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
    assert all(z['total']<0 for z in rows), 'POSITIVE CANDIDATE: preserve and rationalize before further research'
    certs=[exact_certificate(best,'representative_best_full'),exact_certificate(geometry,'representative_noncommuting_top_excess')]
    payload=dict(status='PARTIAL',centers=centers,directions=rows,best=best,top_excess=geometry,certificates=certs,versions=dict(python=sys.version,numpy=np.__version__,scipy=scipy.__version__,sympy=sp.__version__,mpmath=mp.__version__),threads={k:os.environ.get(k) for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']},script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),pid=os.getpid())
    (OUT/'results.json').write_text(json.dumps(payload,indent=2),encoding='utf-8')
    print(json.dumps(dict(center_count=len(centers),direction_count=len(rows),best=best,top_excess=geometry,certificates=certs),indent=2),flush=True)

if __name__=='__main__': main()
