#!/usr/bin/env python3
"""Exact author checks for the local-channel proof and an explicit dense 3+3 lift.
No temporal sampling, finite differences, spectral-entropy substitution or floating
sign decisions. The second-derivative test uses an affine path with moving diagonals.
"""
import os
for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']: os.environ[key]='1'
import time, json, platform
from itertools import product, combinations
from pathlib import Path
import sympy as sp
from exact_core import F, logiv, ivscale, ivsum, disp, fraction_json
from fixtures import Q, ff, em, ep, pd, original, mode_base
START=time.perf_counter()
t=sp.Symbol('t')
s=sp.Symbol('s')

def event_polys(K):
    return [sp.Poly((-1)**(K.rows-m.bit_count())*em(K,m).det(method='domain-ge'),t,domain=sp.QQ) for m in range(1<<K.rows)]

def joint_polys(A,C,B):
    K=A.row_join(t*B).col_join((t*B.T).row_join(C))
    vals=event_polys(K)
    return {(i,j):vals[i+(j<<A.rows)] for i in range(1<<A.rows) for j in range(1<<C.rows)}

def refine(q0,q1):
    d=[y-x for x,y in zip(q0,q1)];P=[i for i in range(len(d)) if d[i]>0];N=[i for i in range(len(d)) if d[i]<0]
    M=sum(d[i] for i in P);out=[]
    if M:
        for p,n in product(P,N):
            gamma=d[p]*(-d[n])/M
            alpha=[Q(0)]*len(d);alpha[p]=gamma/d[p];alpha[n]=gamma/(-d[n])
            c=sum(q0[y]*alpha[y] for y in range(len(d)))
            a=q0[p]*alpha[p]/c;theta=gamma/c
            assert sum(q1[y]*alpha[y] for y in range(len(d)))==c
            assert 0<=a<a+theta<=1
            out.append((c,a,theta,p,n,alpha))
    for z in range(len(d)):
        if d[z]==0 and q0[z]>0:
            alpha=[Q(0)]*len(d);alpha[z]=Q(1)
            out.append((q0[z],Q(0),Q(0),z,z,alpha))
    assert sum(row[0] for row in out)==1
    for y in range(len(d)):
        if q0[y]+q1[y]:assert sum(row[5][y] for row in out)==1
    return out

def hessian_signature(ps,weight=Q(1)):
    """H''(0) as an exact rational plus rational coefficients of log primes.
    Unique factorization yields a sufficient exact algebraic equality check;
    no transcendental sign or numerical logarithm comparison is used here.
    """
    rat=Q(0);logs={}
    for poly in ps:
        poly=sp.Poly(poly,t,domain=sp.QQ)
        if poly.is_zero:continue
        p0,p1,p2=poly.eval(0),poly.diff().eval(0),poly.diff().diff().eval(0)
        assert p0>0
        rat-=weight*p1*p1/p0
        for x,sgn in [(sp.numer(p0),1),(sp.denom(p0),-1)]:
            for prime,power in sp.factorint(x).items():logs[prime]=logs.get(prime,Q(0))-weight*p2*sgn*power
    return rat,{p:c for p,c in logs.items() if c}

def main():
    q0=[Q(1,2),Q(1,3),Q(1,6)];q1=[Q(1,4),Q(1,4),Q(1,2)]
    rr=refine(q0,q1)
    assert [(x[0],x[1],x[2]) for x in rr]==[(Q(5,8),Q(1,5),Q(2,5)),(Q(3,8),Q(1,9),Q(2,9))]
    print('ASYMMETRIC TERNARY CHANNEL: exact selectors (c,a,theta)=',[(str(x[0]),str(x[1]),str(x[2])) for x in rr])
    # Actual K-affine test includes changes of both observed singleton means.
    K=sp.Matrix([[Q(2,5)+t/10,Q(1,10)+t/20],[Q(1,10)+t/20,Q(3,5)-t/15]])
    assert pd(K.subs(t,0)) and pd(sp.eye(2)-K.subs(t,0))
    px=event_polys(K);Qrows=[q0,q1]
    py=[]
    for y1,y2 in product(range(3),repeat=2):
        py.append(sum((px[x].as_expr()*Qrows[x&1][y1]*Qrows[(x>>1)&1][y2] for x in range(4)),sp.Integer(0)))
    left=hessian_signature(py)
    rational=Q(0);logs={};refined_checks=0
    for j,k in product(range(len(rr)),repeat=2):
        c1,a1,th1,p1,n1,al1=rr[j];c2,a2,th2,p2,n2,al2=rr[k]
        # In two dimensions the only offdiagonal dependence is its square.
        p11=(a1+th1*K[0,0])*(a2+th2*K[1,1])-th1*th2*K[0,1]**2
        pk=[1-(a1+th1*K[0,0])-(a2+th2*K[1,1])+p11,
            a1+th1*K[0,0]-p11,a2+th2*K[1,1]-p11,p11]
        for z in range(4):
            y1=p1 if z&1 else n1;y2=p2 if z&2 else n2
            lhs=py[3*y1+y2]*al1[y1]*al2[y2]
            assert sp.Poly(lhs-c1*c2*pk[z],t,domain=sp.QQ).is_zero
            refined_checks+=1
        rat,ll=hessian_signature(pk,c1*c2);rational+=rat
        for p,c in ll.items():logs[p]=logs.get(p,Q(0))+c
    assert left==(rational,{p:c for p,c in logs.items() if c})
    print('REFINED JOINT LAWS: exact polynomial identities',refined_checks)
    print('FULL HESSIAN WITH MOVING DIAGONALS: rational Fisher and all log-prime acceleration coefficients agree exactly')
    # Finite mode channels: half background and asymmetric backgrounds.
    A,C,B,W=mode_base();base=joint_polys(A,C,B);v=sp.Matrix([Q(3,5),Q(4,5)])
    def local_channel(eta):
        R=eta*(sp.eye(2)-v*v.T)
        return [[ep(R+x*v*v.T,m) for m in range(4)] for x in (0,1)]
    mode_counts=[]
    for etaL,etaR in [(Q(1,2),Q(1,2)),(Q(1,4),Q(2,3))]:
        AL=etaL*(sp.eye(3)-W*W.T)+W*A*W.T
        CL=etaR*(sp.eye(3)-W*W.T)+W*C*W.T;BL=W*B*W.T
        assert pd(AL) and pd(sp.eye(3)-AL) and pd(CL) and pd(sp.eye(3)-CL)
        assert BL.rank()==2 and all(x!=0 for x in BL)
        assert all(M[i,j]!=0 for M in (AL,CL) for i,j in combinations(range(3),2))
        full=joint_polys(AL,CL,BL);ql,qr=local_channel(etaL),local_channel(etaR)
        refine(*ql);refine(*qr)
        count=0
        for (i,j),actual in full.items():
            rhs=sp.Integer(0)
            for (x,y),pr in base.items():
                if (i>>2)==(x>>1) and (j>>2)==(y>>1):rhs+=pr.as_expr()*ql[x&1][i&3]*qr[y&1][j&3]
            assert actual==sp.Poly(rhs,t,domain=sp.QQ)
            count+=1
        mode_counts.append(count)
        print('ACTUAL OBSERVED MODE LAW: backgrounds',etaL,etaR,'all',count,'event polynomials exact')
    bad=local_channel(Q(1,3));assert bad[0][0]+bad[0][3]==Q(2,3) and bad[1][0]+bad[1][3]==Q(1,3)
    print('FAILED SHORTCUT PRESERVED: empty/full complement selector has probabilities 2/3 and 1/3 at eta=1/3, not input-independent')
    # Explicit half-filled observed lift: complete maximal legal endpoint.
    AL=(sp.eye(3)-W*W.T)/2+W*A*W.T;CL=(sp.eye(3)-W*W.T)/2+W*C*W.T;BL=W*B*W.T
    pK=sp.factor((C-s*(B.T*A.inv()*B)).det())
    pI=sp.factor((sp.eye(2)-C-s*(B.T*(sp.eye(2)-A).inv()*B)).det())
    assert sp.expand(pK-(300*s*s-4900*s+13799)/57600)==0
    assert sp.expand(pI-(60*s*s-2092*s+13799)/57600)==0
    rstar=Q(49,6)-sp.sqrt(4657)/15;rI=Q(523,30)-2*sp.sqrt(4159)/15
    assert 3<rstar<4<8<rI<9
    print('EXPLICIT 3+3 MAXIMAL s*: 49/6 - sqrt(4657)/15, in (3,4)')
    # A selected observed left full/empty pattern reveals base mask 1.
    M=BL.T*em(AL,3).inv()*BL;assert M==W*(B.T*em(A,1).inv()*B)*W.T
    assert B.T*em(A,1).inv()*B==sp.Matrix([[0,Q(1,24)],[Q(1,24),0]])
    Pstar=[];diff=[];fiber=(F(0),F(0));r=Q(1,48)
    for mask in range(8):
        h=2*sum((v[i]**2 for i in range(2) if mask&(1<<i)),sp.Integer(0))-1
        z=(mask>>2)&1
        pp=(Q(3,5) if z else Q(2,5))/4*(1-h/5)
        dd=r*r/2*(1-2*z)*h
        actual=sp.expand(ep(CL-s*M,mask))
        assert sp.expand(actual-pp-(1-2*s)**2*dd)==0
        assert pp>0 and pp+dd>0
        Pstar.append(ff(pp));diff.append(ff(dd))
    assert sum(Pstar)==1 and sum(diff)==0 and any(diff)
    fiber=ivsum(ivscale(-8*d,logiv((p+d)/p)) for p,d in zip(Pstar,diff))
    assert fiber[1]<0
    print('COMPLETE CONDITIONAL FIBER mask3, s=1/2:',disp(fiber,20),'<0')
    print('All eight conditional Fisher terms vanish exactly here; signed acceleration is retained')
    kappa=Q(337,625);constant=4*Q(1,6)**4*kappa;assert constant==Q(337,202500)
    print('WHOLE-CHORD CURVATURE COEFFICIENT:',constant,'from the exact channel theorem')
    # Proportional-row obstruction is for this representation only.
    _,_,U,V=original()
    minors=[[X.extract(list(pair),[0,1]).det() for pair in combinations(range(3),2)] for X in (U,V)]
    assert all(x!=0 for group in minors for x in group)
    print('ORIGINAL PR58 FRAME PAIR MINORS:',[[str(x) for x in row] for row in minors])
    print('Original PR58 fixture is not this grouped two-mode lift; its separate whole-chord proof is required')
    evidence={'status':'AUTHOR_CHECK_PENDING_REVIEW','asymmetric_selector_parameters':[[str(x[i]) for i in range(3)] for x in rr],
        'polynomial_identity_counts':{'refined_affine_law':refined_checks,'observed_half_mode':mode_counts[0],'observed_asymmetric_mode':mode_counts[1]},
        'moving_diagonal_full_hessian_identity':True,
        'explicit_observed_input':{name:[[str(x) for x in row] for row in mat.tolist()] for name,mat in [('A',AL),('C',CL),('B',BL)]},
        'negative_fiber_interval':[fraction_json(x) for x in fiber],
        'negative_fiber_pstar':[fraction_json(x) for x in Pstar],'negative_fiber_difference':[fraction_json(x) for x in diff],
        'curvature_coefficient':str(constant),'root_exact':str(rstar),'original_frame_pair_minors':[[str(x) for x in row] for row in minors],
        'execution':{'python':platform.python_version(),'sympy':sp.__version__,'elapsed_seconds':time.perf_counter()-START,'process_threads':1}}
    out=Path(__file__).resolve().parent.parent/'output'/'channel_certificate.json';out.write_text(json.dumps(evidence,indent=2)+'\n')
    print('PASS (author only); saved channel_certificate.json')
    print('Python',platform.python_version(),'SymPy',sp.__version__,'elapsed seconds',round(time.perf_counter()-START,3))

if __name__=='__main__':main()
