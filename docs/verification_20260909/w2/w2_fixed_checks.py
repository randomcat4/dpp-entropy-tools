import json, os, time
from pathlib import Path
import sympy as sp
import mpmath as mp
mp.mp.dps=100
t=sp.Symbol('t',real=True)
Q=sp.Rational
def atoms(A,D):
    n=A.rows; K=A+t*D
    minors={0:sp.Integer(1)}
    for mask in range(1,1<<n):
        ids=[i for i in range(n) if mask>>i&1]
        minors[mask]=sp.Poly(K.extract(ids,ids).det(method='domain-ge'),t).as_expr()
    return [sp.Poly(sum((-1)**((b^a).bit_count())*minors[b] for b in range(1<<n) if b&a==a),t).as_expr() for a in range(1<<n)]
def E(p,i,a):
    return [(a if x>>i&1 else 1-a)*(p[x&~(1<<i)]+p[x|(1<<i)]) for x in range(len(p))]
def m(x):
    x=sp.simplify(x)
    assert sp.im(x)==0
    return mp.mpf(str(sp.N(x,110)))
def H(p): return -sum(x*mp.log(x) for x in p if x)
def bern_d(r,a):
    return (r*mp.log(r/a) if r else 0)+((1-r)*mp.log((1-r)/(1-a)) if r!=1 else 0)
def diss(P,R,j,a):
    out=mp.mpf('0')
    for x in range(len(P)):
        y=x^(1<<j); rate=a if y>>j&1 else 1-a
        u=P[x]/R[x]; v=P[y]/R[y]
        out += rate*R[x]*(u*mp.log(u/v)-u+v)
    return out
def case(label,A,D,toeplitz=False):
    n=A.rows; pol=atoms(A,D); p1=[sp.diff(x,t) for x in pol]; p2=[sp.diff(x,t,2) for x in pol]
    assert sp.simplify(sum(pol)-1)==0
    rows=[]
    for s in map(Q,['-3/2','-1/2','0','1/2','3/2']):
        pe=[sp.simplify(x.subs(t,s)) for x in pol]
        dpe=[sp.simplify(x.subs(t,s)) for x in p1]
        ddpe=[sp.simplify(x.subs(t,s)) for x in p2]
        assert all(x>0 for x in pe)
        assert all(sp.simplify(s*dpe[x]-sum(pe[x]-E(pe,i,A[i,i])[x] for i in range(n)))==0 for x in range(1<<n))
        P=list(map(m,pe)); dP=list(map(m,dpe)); ddP=list(map(m,ddpe))
        negcurv=sum(dP[x]**2/P[x]+ddP[x]*mp.log(P[x]) for x in range(1<<n))
        rec={'s':str(s),'negative_entropy_curvature':mp.nstr(negcurv,40)}
        assert negcurv>=-mp.mpf('1e-80')
        if s:
            rhs=mp.mpf('0')
            for i in range(n):
                R=E(P,i,m(A[i,i]))
                rhs+=sum((P[x]-R[x])**2/P[x] for x in range(len(P)))
                for j in range(n):
                    if j!=i:
                        rhs+=diss(P,R,j,m(A[j,j]))+diss(R,P,j,m(A[j,j]))
            rhs/=m(s)**2
            error=abs(rhs-negcurv)
            assert error<mp.mpf('1e-80')
            rec['dissipation_identity_error']=mp.nstr(error,8)
        if toeplitz:
            gamma=m(Q(1,144)); bound=16*(n-1)*m(s)**2*gamma**2
            assert negcurv>=bound-mp.mpf('1e-80')
            rec['quartic_curvature_residual']=mp.nstr(negcurv-bound,40)
            gap=n*mp.log(2)-H(P)
            match=(n//2)*bern_d(mp.mpf('0.25')-m(s)**2*gamma,mp.mpf('0.25'))
            assert gap>=match-mp.mpf('1e-80')
            rec['parity_gap']=mp.nstr(gap,40)
            rec['matching_bound']=mp.nstr(match,40)
        rows.append(rec)
    return {'label':label,'n':n,'cases':rows}
start=time.time()
A=sp.diag(Q(1,3),Q(2,5),Q(3,5),Q(2,3))
D=sp.Matrix([[Q(1,100),Q(1,40),0,Q(1,60)],[Q(1,40),-Q(1,100),Q(1,50),0],[0,Q(1,50),0,Q(1,40)],[Q(1,60),0,Q(1,40),Q(1,100)]])
complexD=sp.Matrix([[0,Q(1,30)*(1+sp.I),Q(1,40)],[Q(1,30)*(1-sp.I),0,sp.I/35],[Q(1,40),-sp.I/35,0]])
toeD=sp.zeros(6)
for i in range(5):toeD[i,i+1]=toeD[i+1,i]=Q(1,12)
rows=[case('heterogeneous_noncommuting',A,D),case('complex_hermitian',sp.eye(3)/2,complexD),case('fixed_toeplitz_k1',sp.eye(6)/2,toeD,True)]
out={'status':'PASS','author_pr':34,'author_head':'838c20b12907d94a9d6e023cc03f48c3f3b36c5c','precision_digits':mp.mp.dps,'scope':'15 deterministic finite checks; high precision, not interval bounds or rate extrapolation','elapsed_seconds':time.time()-start,'cases':rows}
Path('w2_fixed_checks.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':'PASS','cases':15,'elapsed_seconds':out['elapsed_seconds']}))
