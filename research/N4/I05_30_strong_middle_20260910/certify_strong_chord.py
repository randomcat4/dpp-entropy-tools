#!/usr/bin/env python3
"""Exact full-chord certificate for one strong Schur-mismatched rank-two pair.

All complete event polynomials are regenerated from signed determinants. The
left and right endpoint singular factors are removed exactly. Every decisive
logarithm uses a rational atanh expansion with an explicit tail. No scan over
new endpoint inputs, random optimization, event truncation, or floating-point
sign decision is used.
"""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import json
import platform
import sys
sys.set_int_max_str_digits(0)
import sympy as sp

Q=sp.Rational
NLOG=32
NBOX=32
SS=[tuple(i for i in range(4) if mask>>i&1) for mask in range(16)]

def fq(x):
    x=Q(x)
    return F(int(x.p),int(x.q))
def add(a,b): return a[0]+b[0],a[1]+b[1]
def scale(a,c):
    c=fq(c)
    return (a[0]*c,a[1]*c) if c>=0 else (a[1]*c,a[0]*c)
def mul(a,b):
    z=[a[0]*b[0],a[0]*b[1],a[1]*b[0],a[1]*b[1]]
    return min(z),max(z)
def sub(a,b): return add(a,scale(b,-1))
def atanh_iv(z):
    z=fq(z)
    assert 0<=z<=F(1,3)
    term=z; z2=z*z; lo=F(0)
    for j in range(NLOG):
        lo+=2*term/(2*j+1)
        term*=z2
    return lo,lo+2*term/((2*NLOG+1)*(1-z2))
LOG2=atanh_iv(F(1,3))
@lru_cache(None)
def logiv(x):
    x=fq(x)
    assert x>0
    k=0; y=x
    while y<1:
        y*=2; k-=1
    while y>=2:
        y/=2; k+=1
    return add(scale(LOG2,k),atanh_iv((y-1)/(y+1)))
def etaiv(x):
    x=fq(x)
    return (F(0),F(0)) if x==0 else scale(logiv(x),-x)
def entropy(p):
    a=(F(0),F(0))
    for x in p.values():
        a=add(a,etaiv(x))
    return a
def show(a,d=30):
    def one(x,up):
        den=10**d; n=x.numerator*den
        v=-((-n)//x.denominator) if up else n//x.denominator
        sg='-' if v<0 else ''
        v=abs(v)
        return f'{sg}{v//den}.{v%den:0{d}d}'
    return [one(a[0],False),one(a[1],True)]
def R(q):
    return sp.Matrix([[(1-q*q)/(1+q*q),-2*q/(1+q*q)],
                      [2*q/(1+q*q),(1-q*q)/(1+q*q)]])
def mat(l,h,q):
    rr=R(q)
    return rr*sp.diag(l,h)*rr.T
def poly_iv(expr,x,a,b):
    P=sp.Poly(sp.expand(expr),x)
    lo=hi=F(0)
    for (k,),coef in P.terms():
        c=fq(coef); al=a**k; bh=b**k
        if c>=0:
            lo+=c*al; hi+=c*bh
        else:
            lo+=c*bh; hi+=c*al
    return lo,hi
def signed_law(K):
    out={}
    for S in SS:
        M=sp.Matrix(K)
        for i in range(4):
            if i not in S:
                M[i,i]-=1
        out[S]=sp.factor((-1)**(4-len(S))*M.det())
    assert sp.factor(sum(out.values())-1)==0
    return out

def main():
    A=mat(Q(3,100),Q(9,10),Q(1,13))
    B=mat(Q(3,20),Q(17,20),Q(3,7))
    t1,t2,phi,psi=Q(1,5),Q(7,10),Q(1,6),Q(1,6)
    C=sp.diag((1-t1*t1)/(1+t1*t1),(1-t2*t2)/(1+t2*t2))
    S=sp.diag(2*t1/(1+t1*t1),2*t2/(1+t2*t2))
    V=(R(phi)*C).col_join(R(psi)*S)
    E=sp.eye(4)[:,:2]
    X=E*A*E.T
    Y=V*B*V.T
    D=sp.simplify(Y-X)
    assert A.det()>0 and (sp.eye(2)-A).det()>0
    assert B.det()>0 and (sp.eye(2)-B).det()>0
    assert sp.Matrix.hstack(E,V).det()!=0 and D.det()>0

    t=sp.symbols('t',nonnegative=True)
    K=(1-t)*X+t*Y
    pol=signed_law(K)
    p0={S:sp.factor(p.subs(t,0)) for S,p in pol.items()}
    p1={S:sp.factor(p.subs(t,1)) for S,p in pol.items()}
    pm={S:sp.factor(p.subs(t,Q(1,2))) for S,p in pol.items()}
    assert all(v>=0 for v in p0.values())
    assert all(v>=0 for v in p1.values())
    assert all(v>0 for v in pm.values())
    G=sub(entropy({S:fq(v) for S,v in pm.items()}),
          scale(add(entropy({S:fq(v) for S,v in p0.items()}),
                    entropy({S:fq(v) for S,v in p1.items()})),F(1,2)))
    assert G[0]>0

    # Complete midpoint Hessian, separated by cardinality.
    fisher=F(0); acc=(F(0),F(0)); layers={}
    for card in range(5):
        lf=F(0); la=(F(0),F(0))
        for S0,p in pol.items():
            if len(S0)!=card:
                continue
            pv=fq(p.subs(t,Q(1,2)))
            p1v=fq(sp.diff(p,t).subs(t,Q(1,2)))
            p2v=fq(sp.diff(p,t,2).subs(t,Q(1,2)))
            lf+=p1v*p1v/pv
            la=add(la,scale(logiv(pv),-p2v))
        layers[str(card)]={
            'Fisher_exact':str(lf),
            'acceleration_interval':show(la,36),
            'H_second_interval':show(sub(la,(lf,lf)),36)}
        fisher+=lf
        acc=add(acc,la)
    h2=sub(acc,(fisher,fisher))
    assert acc[0]>0 and h2[1]<0

    # Global complete-Fisher lower from actual occupancy bit 2.
    dcoord=fq(D[1,1])
    fisher_lower=4*dcoord*dcoord

    # Left endpoint factorization p=t^b q, b=# occupied bottom coordinates.
    qL={}; p2L={}
    for S0,p in pol.items():
        btm=int(2 in S0)+int(3 in S0)
        q=sp.factor(p/t**btm)
        assert sp.factor(p-t**btm*q)==0 and q.subs(t,0)>0
        qL[S0]=q
        p2L[S0]=sp.diff(p,t,2)
    assert sp.factor(sum((int(2 in S0)+int(3 in S0))*sp.diff(p,t,2)
                         for S0,p in pol.items()))==0

    # Right endpoint factorization in h=1-t, order=max(|S|-2,0).
    h=sp.symbols('h',nonnegative=True)
    qR={}; p2R={}
    for S0,p in pol.items():
        r=max(len(S0)-2,0)
        ph=sp.factor(p.subs(t,1-h))
        q=sp.factor(ph/h**r)
        assert sp.factor(ph-h**r*q)==0 and q.subs(h,0)>0
        qR[S0]=q
        p2R[S0]=sp.diff(p,t,2).subs(t,1-h)
    Rmass=sp.factor(sum(max(len(S0)-2,0)*p for S0,p in pol.items()))
    R2=sp.factor(sp.diff(Rmass,t,2))
    assert R2.subs(t,Q(1,2))<0 and R2.subs(t,1)<0

    def regular_cover(qs,p2s,x):
        best=None; arg=None; rows=[]
        for i in range(NBOX):
            a=F(i,2*NBOX); b=F(i+1,2*NBOX)
            total=(F(0),F(0)); minq=None
            for S0 in SS:
                qi=poly_iv(qs[S0],x,a,b)
                assert qi[0]>0
                li=(logiv(qi[0])[0],logiv(qi[1])[1])
                p2i=poly_iv(p2s[S0],x,a,b)
                total=add(total,scale(mul(p2i,li),-1))
                minq=qi[0] if minq is None else min(minq,qi[0])
            if best is None or total[1]>best:
                best=total[1]; arg=i
            rows.append({
                'i':i,'a':str(a),'b':str(b),
                'acc_upper_outward_18':show((total[1],total[1]),18)[1],
                'min_regular_q':str(minq)})
        return best,arg,rows

    left_upper,left_arg,left_rows=regular_cover(qL,p2L,t)
    right_upper,right_arg,right_rows=regular_cover(qR,p2R,h)
    acc_upper=max(left_upper,right_upper)
    assert acc_upper<F(41,20)
    assert fisher_lower>F(57,20)
    assert acc_upper<fisher_lower
    global_h2_upper=acc_upper-fisher_lower
    assert global_h2_upper<-F(4,5)

    # The omitted right singular term -R'' log(1-t) is nonpositive.
    num=sp.factor(-R2*Q(146871524371234000,9))
    assert num.subs(t,Q(1,2))>0
    assert sp.diff(num,t).subs(t,Q(1,2))>0
    assert sp.diff(num,t,2)>0

    sigA=sp.factor(A.det()/A[0,0])
    sigB=sp.factor(B.det()/B[0,0])
    out={
      'status':'AUTHOR EXACT FULL-CHORD CERTIFICATE; PENDING_INDEPENDENT_REVIEW',
      'python':platform.python_version(),'sympy':sp.__version__,
      'log_terms':NLOG,
      'log_tail':'2*z^(2*N+1)/((2*N+1)*(1-z^2)), 0<=z<=1/3',
      'input':{
        'A':[[str(x) for x in row] for row in A.tolist()],
        'B':[[str(x) for x in row] for row in B.tolist()],
        'V':[[str(x) for x in row] for row in V.tolist()],
        'Kminus':[[str(x) for x in row] for row in X.tolist()],
        'Kplus':[[str(x) for x in row] for row in Y.tolist()]},
      'geometry':{
        'endpoint_ranks':[X.rank(),Y.rank()],
        'support_union_rank':sp.Matrix.hstack(E,V).rank(),
        'direction_rank':D.rank(),
        'direction_det':str(sp.factor(D.det())),
        'direction_inertia':'(2 positive,2 negative) by congruence to diag(-A,B)',
        'A_eigenvalues':['3/100','9/10'],
        'B_eigenvalues':['3/20','17/20'],
        'Schur_A':str(sigA),'Schur_B':str(sigB),
        'Schur_mismatch':str(sp.factor(sigA-sigB))},
      'full_event_polynomials':{
        ','.join(str(i+1) for i in S0):str(p) for S0,p in pol.items()},
      'midpoint':{
        'G_interval':show(G,36),
        'Fisher_exact':str(fisher),
        'acceleration_interval':show(acc,36),
        'H_second_interval':show(h2,36),
        'cardinality_layers':layers,
        'all_16_atoms_positive':True},
      'global_proof':{
        'coordinate':'2','D_22':str(D[1,1]),
        'complete_Fisher_lower':'4*D_22^2 = '+str(fisher_lower),
        'left_regular_identity':'p_S=t^(# occupied coordinates in {3,4}) q_S; log(t) coefficient cancels because expected bottom count is affine',
        'right_regular_identity':'p_S=(1-t)^max(|S|-2,0) q_S; omitted log(1-t) term is nonpositive on [1/2,1]',
        'boxes_each_half':NBOX,
        'left_regular_acc_upper_outward':show((left_upper,left_upper),36)[1],
        'left_argmax_box':left_arg,
        'right_regular_acc_upper_outward':show((right_upper,right_upper),36)[1],
        'right_argmax_box':right_arg,
        'global_acceleration_upper_outward':show((acc_upper,acc_upper),36)[1],
        'simple_acceleration_upper':'41/20',
        'simple_Fisher_lower':'57/20',
        'global_H_second_upper_outward':show((global_h2_upper,global_h2_upper),36)[1],
        'exact_comparison':'acceleration < 41/20 and Fisher > 57/20, hence global_H_second < -4/5',
        'simple_H_second_claim':'H_second < -4/5 on the entire open chord'},
      'endpoint_linear_masses':{},
      'cover_rows':{'left':left_rows,'right':right_rows}
    }
    for endpoint,var in [(0,t),(1,h)]:
        beta=Q(0); orders={}
        for S0,p in pol.items():
            pp=sp.expand(p if endpoint==0 else p.subs(t,1-h))
            P=sp.Poly(pp,var)
            val=pp.subs(var,0)
            if val==0:
                order=min(k[0] for k,c in P.terms() if c!=0)
                coef=P.coeff_monomial(var**order)
                orders[','.join(str(i+1) for i in S0)]={
                    'order':order,'leading':str(sp.factor(coef))}
                if order==1:
                    beta+=coef
        out['endpoint_linear_masses'][str(endpoint)]={
            'beta':str(sp.factor(beta)),'zero_atoms':orders}

    target=Path(__file__).with_name('strong_middle_certificate.json')
    target.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print('PASS',target)
    print('G',show(G,30))
    print('mid Acc',show(acc,30),'F',fisher,'H2',show(h2,30))
    print('F lower',float(fisher_lower),'acc upper',float(acc_upper),
          'global H2 upper',float(global_h2_upper),'args',left_arg,right_arg)

if __name__=='__main__':
    main()
