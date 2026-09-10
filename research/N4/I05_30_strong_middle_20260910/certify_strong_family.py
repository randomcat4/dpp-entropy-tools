#!/usr/bin/env python3
"""Exact two-parameter full-chord cover for a strong rank-two endpoint family.

The endpoint high eigenvalue ranges over [4/5,9/10]. Every complete event is
reconstructed from signed determinants. Endpoint factors, full acceleration,
and one-coordinate complete-Fisher lower bounds are certified by exact rational
tensor-product Bernstein arithmetic and outward fixed-point logarithms.
"""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
from math import comb
import json
import platform
import sys
import time
sys.set_int_max_str_digits(0)
import sympy as sp

Q=sp.Rational
NLOG=64
NT=32
NL=16
SCALE=1<<192
SS=[tuple(i for i in range(4) if m>>i&1) for m in range(16)]

def fq(x):
    x=Q(x)
    return F(int(x.p),int(x.q))
def add(a,b): return a[0]+b[0],a[1]+b[1]
def scale(a,c):
    c=fq(c)
    return (a[0]*c,a[1]*c) if c>=0 else (a[1]*c,a[0]*c)
def mul(a,b):
    q=(a[0]*b[0],a[0]*b[1],a[1]*b[0],a[1]*b[1])
    return min(q),max(q)
def ceildiv(a,b): return -((-a)//b)
def atanh_iv(z):
    z=fq(z)
    assert 0<=z<=F(1,3)
    lo=z.numerator*SCALE//z.denominator
    hi=ceildiv(z.numerator*SCALE,z.denominator)
    z2lo=lo*lo//SCALE
    z2hi=ceildiv(hi*hi,SCALE)
    plo,phi=lo,hi
    slo=shi=0
    for j in range(NLOG):
        slo += 2*plo//(2*j+1)
        shi += ceildiv(2*phi,2*j+1)
        plo=plo*z2lo//SCALE
        phi=ceildiv(phi*z2hi,SCALE)
    # Since z<=1/3, the true tail is at most
    # (9/4)*3^(-(2*NLOG+1))/(2*NLOG+1).
    shi += ceildiv(9*SCALE,4*(2*NLOG+1)*3**(2*NLOG+1))
    return F(slo,SCALE),F(shi,SCALE)
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
def show(a,d=30):
    def one(x,upper):
        den=10**d; n=x.numerator*den
        z=-((-n)//x.denominator) if upper else n//x.denominator
        sign='-' if z<0 else ''
        z=abs(z)
        return f'{sign}{z//den}.{z%den:0{d}d}'
    return [one(a[0],False),one(a[1],True)]
def R(q):
    return sp.Matrix([[(1-q*q)/(1+q*q),-2*q/(1+q*q)],
                      [2*q/(1+q*q),(1-q*q)/(1+q*q)]])
def mat(lo,hi,q):
    rr=R(q)
    return rr*sp.diag(lo,hi)*rr.T
def signed_law(K):
    out={}
    for S in SS:
        M=sp.Matrix(K)
        for i in range(4):
            if i not in S:
                M[i,i]-=1
        out[S]=sp.expand((-1)**(4-len(S))*M.det(method='domain-ge'))
    assert sp.expand(sum(out.values())-1)==0
    return out
def coeff_affine(e0,e1,x):
    """Coefficients of e(x,ell)=e0(x)+ell*(e1(x)-e0(x))."""
    p0=sp.Poly(sp.expand(e0),x)
    pd=sp.Poly(sp.expand(e1-e0),x)
    out={}
    for (i,),c in p0.terms():
        out[i,0]=fq(c)
    for (i,),c in pd.terms():
        out[i,1]=fq(c)
    return out
def bern_iv(c,a,b,u,v):
    """Exact tensor-product Bernstein enclosure on [a,b]x[u,v]."""
    if not c:
        return F(0),F(0)
    n=max(i for i,j in c)
    m=max(j for i,j in c)
    dx=b-a; dy=v-u
    local={}
    for r in range(n+1):
        for s in range(m+1):
            z=F(0)
            for (i,j),cc in c.items():
                if i>=r and j>=s:
                    z += (cc*comb(i,r)*a**(i-r)*dx**r*
                          comb(j,s)*u**(j-s)*dy**s)
            local[r,s]=z
    values=[]
    for k in range(n+1):
        for ell_index in range(m+1):
            z=F(0)
            for r in range(k+1):
                for s in range(ell_index+1):
                    den=(comb(n,r) if n else 1)*(comb(m,s) if m else 1)
                    z += local[r,s]*F(comb(k,r)*comb(ell_index,s),den)
            values.append(z)
    return min(values),max(values)

def main():
    start=time.time()
    t=sp.symbols('t',nonnegative=True)
    h=sp.symbols('h',nonnegative=True)
    A=mat(Q(3,100),Q(9,10),Q(1,13))
    t1,t2,phi,psi=Q(1,5),Q(7,10),Q(1,6),Q(1,6)
    C=sp.diag((1-t1*t1)/(1+t1*t1),(1-t2*t2)/(1+t2*t2))
    S=sp.diag(2*t1/(1+t1*t1),2*t2/(1+t2*t2))
    V=(R(phi)*C).col_join(R(psi)*S)
    E=sp.eye(4)[:,:2]
    X=E*A*E.T
    def Y(ell):
        return V*mat(Q(3,20),ell,Q(3,7))*V.T

    Y0,Y1=Y(Q(0)),Y(Q(1))
    p0=signed_law((1-t)*X+t*Y0)
    p1=signed_law((1-t)*X+t*Y1)

    # B(ell) is a fixed rank-one affine update, hence every signed event
    # determinant is affine in ell. Verify the interpolation at 17/20.
    center=Q(17,20)
    direct=signed_law((1-t)*X+t*Y(center))
    assert all(sp.expand(direct[U]-(p0[U]+center*(p1[U]-p0[U])))==0
               for U in SS)

    q_left={}; p2_left={}; q_right={}; p2_right={}
    for U in SS:
        bottom=int(2 in U)+int(3 in U)
        q0=sp.cancel(p0[U]/t**bottom)
        q1=sp.cancel(p1[U]/t**bottom)
        sp.Poly(q0,t); sp.Poly(q1,t)
        q_left[U]=coeff_affine(q0,q1,t)
        p2_left[U]=coeff_affine(sp.diff(p0[U],t,2),sp.diff(p1[U],t,2),t)

        order=max(len(U)-2,0)
        ph0=sp.expand(p0[U].subs(t,1-h))
        ph1=sp.expand(p1[U].subs(t,1-h))
        qr0=sp.cancel(ph0/h**order)
        qr1=sp.cancel(ph1/h**order)
        sp.Poly(qr0,h); sp.Poly(qr1,h)
        q_right[U]=coeff_affine(qr0,qr1,h)
        p2_right[U]=coeff_affine(sp.diff(p0[U],t,2).subs(t,1-h),
                                  sp.diff(p1[U],t,2).subs(t,1-h),h)

    assert sp.expand(sum((int(2 in U)+int(3 in U))*sp.diff(p0[U],t,2)
                         for U in SS))==0
    assert sp.expand(sum((int(2 in U)+int(3 in U))*sp.diff(p1[U],t,2)
                         for U in SS))==0

    R0=sp.expand(sum(max(len(U)-2,0)*p0[U] for U in SS))
    R1=sp.expand(sum(max(len(U)-2,0)*p1[U] for U in SS))
    R2_right=coeff_affine(sp.diff(R0,t,2).subs(t,1-h),
                           sp.diff(R1,t,2).subs(t,1-h),h)

    ell_lo,ell_hi=F(4,5),F(9,10)
    def cover(qs,p2s,right=False):
        best=None; arg=None; minimum_q=None; rows=[]; max_R2=None
        for i in range(NT):
            a,b=F(i,2*NT),F(i+1,2*NT)
            row_upper=None
            for j in range(NL):
                u=ell_lo+(ell_hi-ell_lo)*F(j,NL)
                v=ell_lo+(ell_hi-ell_lo)*F(j+1,NL)
                total=(F(0),F(0)); box_min_q=None
                for U in SS:
                    qi=bern_iv(qs[U],a,b,u,v)
                    assert qi[0]>0,(right,i,j,U,qi)
                    li=(logiv(qi[0])[0],logiv(qi[1])[1])
                    p2i=bern_iv(p2s[U],a,b,u,v)
                    total=add(total,scale(mul(p2i,li),-1))
                    box_min_q=qi[0] if box_min_q is None else min(box_min_q,qi[0])
                if right:
                    rr=bern_iv(R2_right,a,b,u,v)
                    assert rr[1]<=0,(i,j,rr)
                    max_R2=rr[1] if max_R2 is None else max(max_R2,rr[1])
                if best is None or total[1]>best:
                    best=total[1]; arg=(i,j)
                row_upper=total[1] if row_upper is None else max(row_upper,total[1])
                minimum_q=box_min_q if minimum_q is None else min(minimum_q,box_min_q)
            rows.append(show((row_upper,row_upper),18)[1])
        return best,arg,minimum_q,rows,max_R2

    left=cover(q_left,p2_left)
    right=cover(q_right,p2_right,True)
    acceleration_upper=max(left[0],right[0])

    D0=Y0-X; D1=Y1-X
    d0=fq(D0[1,1]); d1=fq(D1[1,1])
    assert d0<d1<0
    d_at_hi=d1*ell_hi+d0*(1-ell_hi)
    fisher_lower=4*d_at_hi*d_at_hi
    assert fisher_lower>F(289,100)
    assert acceleration_upper<F(239,100)
    assert acceleration_upper-fisher_lower<-F(1,2)

    # Midpoint acceleration remains positive over the entire strength interval.
    def affine_scalar(e0,e1):
        return fq(e0),fq(e1-e0)
    midpoint_acc_lo=None; midpoint_acc_hi=None
    for j in range(NL):
        u=ell_lo+(ell_hi-ell_lo)*F(j,NL)
        v=ell_lo+(ell_hi-ell_lo)*F(j+1,NL)
        acc=(F(0),F(0))
        for U in SS:
            a0,ad=affine_scalar(p0[U].subs(t,Q(1,2)),p1[U].subs(t,Q(1,2)))
            b0,bd=affine_scalar(sp.diff(p0[U],t,2).subs(t,Q(1,2)),
                                sp.diff(p1[U],t,2).subs(t,Q(1,2)))
            pp=(a0+ad*(u if ad>=0 else v),a0+ad*(v if ad>=0 else u))
            assert pp[0]>0
            p2=(b0+bd*(u if bd>=0 else v),b0+bd*(v if bd>=0 else u))
            acc=add(acc,scale(mul(p2,(logiv(pp[0])[0],logiv(pp[1])[1])),-1))
        midpoint_acc_lo=acc[0] if midpoint_acc_lo is None else min(midpoint_acc_lo,acc[0])
        midpoint_acc_hi=acc[1] if midpoint_acc_hi is None else max(midpoint_acc_hi,acc[1])
    assert midpoint_acc_lo>0

    ell=sp.symbols('ell')
    Bsym=mat(Q(3,20),ell,Q(3,7))
    sigma_A=sp.factor(A.det()/A[0,0])
    sigma_B=sp.factor(Bsym.det()/Bsym[0,0])
    out={
      'status':'AUTHOR EXACT TWO-PARAMETER FULL-CHORD COVER; PENDING_REVIEW',
      'python':platform.python_version(),'sympy':sp.__version__,
      'family':{
        'A_eigenvalues':['3/100','9/10'],
        'B_eigenvalues':['3/20','ell'],
        'ell_interval':['4/5','9/10'],
        'support_parameters':{
          't1':'1/5','t2':'7/10','top_rotation':'1/6','bottom_rotation':'1/6'},
        'direction':'rank 4, inertia (2,2), disjoint endpoint supports throughout'},
      'Schur':{
        'A':str(sigma_A),'B_of_ell':str(sigma_B),
        'mismatch_at_4_over_5':str(sp.factor(sigma_A-sigma_B.subs(ell,Q(4,5)))),
        'mismatch_at_9_over_10':str(sp.factor(sigma_A-sigma_B.subs(ell,Q(9,10))))},
      'complete_Fisher':{
        'D22_at_ell_9_over_10':str(d_at_hi),
        'minimum_lower':str(fisher_lower),'simple_lower':'289/100'},
      'acceleration_cover':{
        't_boxes_each_half':NT,'ell_boxes':NL,'boxes_each_half':NT*NL,
        'left_upper':show((left[0],left[0]),36)[1],
        'left_argmax':list(left[1]),'left_min_q':str(left[2]),
        'right_upper':show((right[0],right[0]),36)[1],
        'right_argmax':list(right[1]),'right_min_q':str(right[2]),
        'right_R_second_max':str(right[4]),
        'global_upper':show((acceleration_upper,acceleration_upper),36)[1],
        'simple_upper':'239/100'},
      'midpoint_acceleration_family_interval':
        show((midpoint_acc_lo,midpoint_acc_hi),36),
      'conclusion':{
        'H_second_upper':show((acceleration_upper-fisher_lower,
                               acceleration_upper-fisher_lower),36)[1],
        'exact_simple_claim':
          'H_second < -1/2 for every 0<t<1 and every 4/5<=ell<=9/10',
        'midpoint_G_lower_from_curvature':'1/16'},
      'row_acceleration_upper_left':left[3],
      'row_acceleration_upper_right':right[3],
      'log_terms':NLOG,
      'log_tail':'2*z^(2N+1)/((2N+1)*(1-z^2)), 0<=z<=1/3',
      'runtime_seconds':round(time.time()-start,3)}

    target=Path(__file__).with_name('strong_family_certificate.json')
    target.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print('PASS',target)
    print('acc',float(acceleration_upper),'fish',float(fisher_lower),
          'h2',float(acceleration_upper-fisher_lower))
    print('midacc',float(midpoint_acc_lo),float(midpoint_acc_hi))
    print('args',left[1],right[1],'runtime',out['runtime_seconds'])

if __name__=='__main__':
    main()
