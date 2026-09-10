#!/usr/bin/env python3
"""Fixed-scope audit plus matched-Schur axis/wedge continuation.

Reconstructs complete DPP atoms from signed determinants and Moebius inversion,
uses exact rationals, and encloses decisive logarithms by an atanh series with a
rational tail. No random search or numerical sign decision.
"""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
import json
import sympy as sp

Q = sp.Rational
NLOG = 64

def ff(x) -> F:
    x = Q(x); return F(int(x.p), int(x.q))
def iadd(a,b): return a[0]+b[0], a[1]+b[1]
def iscale(a,c):
    c=ff(c); return (a[0]*c,a[1]*c) if c>=0 else (a[1]*c,a[0]*c)
def isub(a,b): return iadd(a,iscale(b,-1))
def log_atanh(z:F):
    assert F(0)<=z<=F(1,3)
    term=z; z2=z*z; lo=F(0)
    for j in range(NLOG):
        lo += 2*term/(2*j+1); term *= z2
    return lo, lo+2*term/((2*NLOG+1)*(1-z2))
LOG2=log_atanh(F(1,3))
def log_iv(x):
    x=ff(x); assert x>0
    k=0; y=x
    while y<1: y*=2; k-=1
    while y>=2: y/=2; k+=1
    return iadd(iscale(LOG2,k),log_atanh((y-1)/(y+1)))
def eta_iv(x):
    x=ff(x); return (F(0),F(0)) if x==0 else iscale(log_iv(x),-x)
def h_iv(x):
    x=ff(x); return iadd(eta_iv(x),eta_iv(1-x))
def entropy_iv(p):
    out=(F(0),F(0))
    for x in p.values(): out=iadd(out,eta_iv(x))
    return out
def subsets(n): return [tuple(i for i in range(n) if mask>>i&1) for mask in range(1<<n)]
def signed_law(K):
    n=K.rows; out={}
    for S in subsets(n):
        M=K.copy(); st=set(S)
        for i in range(n):
            if i not in st: M[i,i]-=1
        out[S]=sp.factor((-1)**(n-len(S))*M.det())
    assert sp.factor(sum(out.values())-1)==0 and all(x>=0 for x in out.values())
    return out
def moebius_law(K):
    ss=subsets(K.rows)
    inc={S:(K.extract(S,S).det() if S else Q(1)) for S in ss}
    out={S:sp.factor(sum((-1)**(len(T)-len(S))*inc[T] for T in ss if set(S).issubset(T))) for S in ss}
    assert out==signed_law(K)
    return out
def gap_iv(px,py,pm): return isub(entropy_iv(pm),iscale(iadd(entropy_iv(px),entropy_iv(py)),F(1,2)))
def dec_out(x:F,digits=30,upper=False):
    x=ff(x); den=10**digits; num=x.numerator*den
    z=-((-num)//x.denominator) if upper else num//x.denominator
    sign='-' if z<0 else ''; z=abs(z)
    return f"{sign}{z//den}.{z%den:0{digits}d}"
def show(iv,digits=30): return [dec_out(iv[0],digits),dec_out(iv[1],digits,True)]
def frame(t1,t2):
    c1=(1-t1*t1)/(1+t1*t1); s1=2*t1/(1+t1*t1)
    c2=(1-t2*t2)/(1+t2*t2); s2=2*t2/(1+t2*t2)
    return sp.Matrix([[c1,0],[0,c2],[s1,0],[0,s2]])

def audit_pr86_atoms_and_examples():
    a,d,b,e,r,z,c1,c2,s1,s2=sp.symbols('a d b e r z c1 c2 s1 s2',real=True)
    A=sp.Matrix([[a,r],[r,d]]); B=sp.Matrix([[b,z],[z,e]])
    E=sp.eye(4)[:,:2]; V=sp.Matrix([[c1,0],[0,c2],[s1,0],[0,s2]])
    N=E*A*E.T+V*B*V.T; DA=a*d-r*r; DB=b*e-z*z
    expected={
      (0,1):DA+DB*c1*c1*c2*c2+a*e*c2*c2+d*b*c1*c1-2*r*z*c1*c2,
      (0,2):a*b*s1*s1,(0,3):(a*e+DB*c1*c1)*s2*s2,
      (1,2):(d*b+DB*c2*c2)*s1*s1,(1,3):d*e*s2*s2,(2,3):DB*s1*s1*s2*s2,
      (0,1,2):s1*s1*(b*DA+a*DB*c2*c2),(0,1,3):s2*s2*(e*DA+d*DB*c1*c1),
      (0,2,3):a*DB*s1*s1*s2*s2,(1,2,3):d*DB*s1*s1*s2*s2,
      (0,1,2,3):DA*DB*s1*s1*s2*s2}
    for S,rhs in expected.items(): assert sp.expand(N.extract(S,S).det()-rhs)==0
    A0=sp.Matrix([[Q(2,5),Q(6,25)],[Q(6,25),Q(2,5)]])
    B0=sp.Matrix([[Q(3,5),Q(9,25)],[Q(9,25),Q(3,5)]])
    E0=sp.eye(4)[:,:2]; X=E0*A0*E0.T; cases={}
    for name,t2 in [('intersection1',Q(0)),('intersection0',Q(1,50))]:
        Y=frame(Q(1,100),t2)*B0*frame(Q(1,100),t2).T; M=(X+Y)/2
        px,py,pm=map(moebius_law,(X,Y,M)); mix={S:(px[S]+py[S])/2 for S in px}
        G=gap_iv(px,py,pm); bridge=isub(entropy_iv(pm),entropy_iv(mix))
        assert G[0]>0 and bridge[1]<0
        cases[name]={'rank_mid':M.rank(),'G':show(G,27),'mid_minus_endpoint_mixture_entropy':show(bridge,27)}
    Ybase=E0*B0*E0.T
    Gbase=gap_iv(moebius_law(X),moebius_law(Ybase),moebius_law((X+Ybase)/2))
    wstar=Q(10000,6255001); deltastar=Q(31200,6255001)
    err=iadd(iadd(h_iv(deltastar),iscale(log_iv(15),deltastar)),iscale(h_iv(wstar),Q(3,5)))
    lower=isub(Gbase,err); assert lower[0]>F(19,1000)
    return {'symbolic_nontrivial_minors':len(expected),'fixed_cases':cases,
            'angular_box_replay':{'wstar':str(wstar),'deltastar':str(deltastar),
                                  'uniform_G_lower':show(lower,27),'claim_checked':'G>19/1000 on [0,1/50]^2'}}

def dilute_coefficient_audit():
    Fm=sp.Matrix([[1,0],[0,1],[Q(3,5),Q(4,5)],[Q(5,13),Q(12,13)]])
    G1=Fm.copy(); G1[3,1]*=-1
    G0=sp.Matrix([[1,0],[0,1],[Q(5,13),Q(12,13)],[Q(8,17),Q(15,17)]])
    def C_event(Z):
        n=Z.rows; a=[Z[i,i] for i in range(n)]
        dij={(i,j):sp.factor(Z.extract((i,j),(i,j)).det()) for i in range(n) for j in range(i+1,n)}
        E2=sum(dij.values()); tr=sum(a); ans=(ff(E2-tr*tr/2),ff(E2-tr*tr/2))
        for i in range(n):
            bi=sum(dij[min(i,j),max(i,j)] for j in range(n) if j!=i)
            if a[i]!=0: ans=iadd(ans,iscale(log_iv(a[i]),bi))
        for val in dij.values():
            if val!=0: ans=isub(ans,iscale(log_iv(val),val))
        return ans
    out={}
    for name,Gf in [('intersection1',G1),('intersection0',G0)]:
        X=Fm*Fm.T/4; Y=Gf*Gf.T/4; M=(X+Y)/2
        assert all(X[i,i]==Y[i,i]==Q(1,4) for i in range(4))
        beta=isub(C_event(M),iscale(iadd(C_event(X),C_event(Y)),F(1,2))); assert beta[0]>0
        out[name]={'rank_mid':M.rank(),'beta':show(beta,27)}
    return out

def new_axis_and_wedge():
    A=sp.Matrix([[Q(2,5),Q(1,5)],[Q(1,5),Q(2,5)]])
    B=sp.Matrix([[Q(3,5),Q(1,5)],[Q(1,5),Q(11,30)]])
    a,r,d=A[0,0],A[0,1],A[1,1]; b,z,e=B[0,0],B[0,1],B[1,1]
    sigmaA=sp.factor(d-r*r/a); sigmaB=sp.factor(e-z*z/b)
    assert sigmaA==sigmaB==Q(3,10)
    assert A.det()>0 and (sp.eye(2)-A).det()>0 and B.det()>0 and (sp.eye(2)-B).det()>0
    c,s=sp.symbols('c s',real=True)
    Km=sp.Matrix([[a,r,0],[r,d,0],[0,0,0]])
    Kp=sp.Matrix([[b*c*c,z*c,b*c*s],[z*c,e,z*s],[b*c*s,z*s,b*s*s]])
    assert sp.factor((Kp-Km).det()-a*b*s*s*(sigmaA-sigmaB))==0
    t1=Q(1,2); c1=Q(3,5); s1=Q(4,5)
    axis_lower=sp.factor(b*b*s1**4/2); assert axis_lower==Q(1152,15625)
    E4=sp.eye(4)[:,:2]; X4=E4*A*E4.T; Vaxis=frame(t1,Q(0)); Yaxis=Vaxis*B*Vaxis.T; Maxis=(X4+Yaxis)/2
    axis_G=gap_iv(*map(moebius_law,(X4,Yaxis,Maxis))); assert axis_G[0]>F(23,100)
    qmax=Q(3,100)
    mismatch_err=iadd(iadd(h_iv(qmax/2),iscale(log_iv(7),qmax/2)),
                      iscale(iadd(h_iv(qmax),iscale(log_iv(7),qmax)),Q(1,2)))
    mismatch_lower=isub(axis_G,mismatch_err); assert mismatch_lower[0]>F(3,100)
    for q in (-qmax,qmax):
        Bq=B.copy(); Bq[1,1]+=q; assert Bq.det()>0 and (sp.eye(2)-Bq).det()>0
        Yq=Vaxis*Bq*Vaxis.T; D=(Yq-X4).extract((0,1,2),(0,1,2)); assert D.det()!=0 and D.rank()==3
    DB=sp.factor(B.det()); Ctv=sp.factor((2*e+DB+a*e+2*abs(r*z)*c1+a*DB*s1*s1)/2)
    assert Ctv==Q(7213,12500)
    def fixed_wedge_lower(umax):
        s2=2*umax/(1+umax**2); w=sp.factor(s2*s2); delta=sp.factor(Ctv*w); assert delta<Q(15,16)
        return w,delta,isub(axis_G,iadd(iadd(h_iv(delta),iscale(log_iv(15),delta)),iscale(h_iv(w),e/2)))
    umax=Q(1,10); w,delta,wedge_lower=fixed_wedge_lower(umax)
    assert w==Q(400,10201) and delta==Q(28852,1275125) and wedge_lower[0]>F(3,100)
    def qerr(q):
        dm=Q(27,2)*q; assert dm<Q(15,16)
        return iadd(iadd(h_iv(dm),iscale(log_iv(15),dm)),iscale(iadd(h_iv(q),iscale(log_iv(15),q)),Q(1,2)))
    qrect=Q(1,5000); rect=isub(wedge_lower,qerr(qrect)); assert rect[0]>F(1,100)
    uw=Q(1,20); ww,dw,wlow=fixed_wedge_lower(uw); qwide=Q(1,1000); rectw=isub(wlow,qerr(qwide)); assert rectw[0]>F(3,50)
    direct={}
    for name,u in [('axis_t2_0',Q(0)),('wedge_edge_t2_1_over_20',uw),('wedge_edge_t2_1_over_10',umax)]:
        V=frame(t1,u); Y=V*B*V.T; M=(X4+Y)/2; G=gap_iv(*map(moebius_law,(X4,Y,M))); assert G[0]>0
        direct[name]={'rank_mid':M.rank(),'support_union_rank':sp.Matrix.hstack(E4,V).rank(),'G':show(G,27)}
    return {'A':[[str(x) for x in row] for row in A.tolist()],
            'B':[[str(x) for x in row] for row in B.tolist()],
            'matched_Schur_complement':str(sigmaA),
            'direction_determinant_identity':'det(Kplus-Kminus)=a*b*s1^2*(sigmaA-sigmaB)',
            'axis_Fisher_G_lower':str(axis_lower),'axis_exact_G':show(axis_G,30),
            'rank3_mismatch_slab':{'B22':'[11/30-3/100,11/30+3/100]','direction_rank':'3 except at matched center',
                                   'rigorous_G_lower':show(mismatch_lower,30),'simple_claim':'G>3/100'},
            'wedge':{'t1':'1/2','t2_interval':'[0,1/10]','TV_coefficient':str(Ctv),'w_max':str(w),'delta_max':str(delta),
                     'rigorous_G_lower':show(wedge_lower,30),'simple_claim':'G>3/100'},
            'rank3_rank4_rectangle_broad_angle':{'B22_shift_q':'[-1/5000,1/5000]','t2_interval':'[0,1/10]',
                'midpoint_q_TV_bound':'(27/2)*abs(q)','rigorous_G_lower':show(rect,30),'simple_claim':'G>1/100',
                'direction_ranks':'rank 3 on t2=0,q!=0; rank 4 on t2>0'},
            'rank3_rank4_rectangle_broad_mismatch':{'B22_shift_q':'[-1/1000,1/1000]','t2_interval':'[0,1/20]',
                'w_max':str(ww),'delta_max':str(dw),'rigorous_G_lower':show(rectw,30),'simple_claim':'G>3/50',
                'direction_ranks':'rank 3 on t2=0,q!=0; rank 4 on t2>0'},
            'direct_complete_law_checks':direct}

def main():
    result={'status':'FRESH_SAME_SESSION_REDERIVATION; NOT_EXTERNAL_INDEPENDENT_REVIEW',
            'log_terms':NLOG,'log_tail':'2*z^(2N+1)/((2N+1)*(1-z^2)), 0<=z<=1/3',
            'pr86_audit':audit_pr86_atoms_and_examples(),
            'dilute_second_coefficient_audit':dilute_coefficient_audit(),
            'new_axis_wedge':new_axis_and_wedge()}
    target=Path(__file__).with_name('audit_axis_wedge_certificate.json')
    target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2)); print('PASS',target)
if __name__=='__main__': main()
