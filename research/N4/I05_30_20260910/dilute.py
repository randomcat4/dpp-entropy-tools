#!/usr/bin/env python3
"""Fixed dense equal-diagonal rank-two inputs; full-law Taylor remainders.
Imports the exact log/atom primitives of the adjacent narrow verifier.
No sampling, optimization, omitted events, or floating-point sign decisions.
"""
from math import comb, factorial
from fractions import Fraction as F
from pathlib import Path
import json
import sympy as sp
from certify import Q, SS, frac, logiv, ivadd, ivsub, ivscale, ivshow, dec, law, gap, legal_psd

def poly_data(K):
    ds={S:frac(K.extract(S,S).det()) if S else F(1) for S in SS}
    result={}
    for S in SS:
        m=len(S)
        coeff=[sum(((-1)**k)*ds[T] for T in SS if set(S)<=set(T) and len(T)==m+k) for k in range(5-m)]
        if ds[S]==0:
            assert all(c==0 for c in coeff)
        else:
            assert coeff[0]==ds[S]
            result[S]=coeff
    return result

def rho_of(data):
    rho=F(1,2)
    for cs in data.values():
        aa=sum(abs(c) for c in cs[1:])
        if aa:rho=min(rho,cs[0]/(2*aa))
    return rho

def falling(k,j):return factorial(k)//factorial(k-j)

def third_bound(data,rho):
    total=F(0)
    for S,cs in data.items():
        m=len(S);d=cs[0]
        QQ=[sum(falling(k,j)*abs(cs[k])*rho**(k-j) for k in range(j,len(cs))) for j in range(4)]
        PP=[sum(falling(m+k,j)*abs(cs[k])*rho**(m+k-j) for k in range(len(cs)) if m+k>=j) for j in range(4)]
        L0=logiv(2/d)[1]
        L1=2*QQ[1]/d
        L2=2*QQ[2]/d+4*QQ[1]**2/d**2
        L3=2*QQ[3]/d+12*QQ[1]*QQ[2]/d**2+16*QQ[1]**3/d**3
        LL=[L0,L1,L2,L3]
        total+=sum(comb(3,j)*PP[j]*LL[3-j] for j in range(4))
    return total

def psi(u,z):
    u,z=frac(u),frac(z)
    if u==0:assert z==0;return F(0),F(0)
    d=u-z*z;assert d>=0
    return (z*z,z*z) if d==0 else ivadd((z*z,z*z),ivscale(logiv(d/u),d))

def second(K):
    ans=-sum(frac(K[i,i])**2 for i in range(4))/2
    ans=(ans,ans)
    for i in range(4):
        for j in range(i+1,4):ans=ivsub(ans,psi(K[i,i]*K[j,j],K[i,j]))
    return ans

def coef_direct(K):
    ds={S:frac(K.extract(S,S).det()) if S else F(1) for S in SS}
    T=frac(sp.trace(K));E2=sum(ds[S] for S in SS if len(S)==2)
    result=(E2-T*T/2,E2-T*T/2)
    for i in range(4):
        bi=sum(ds[S] for S in SS if len(S)==2 and i in S)
        if K[i,i]:result=ivadd(result,ivscale(logiv(K[i,i]),bi))
    for S in SS:
        if len(S)==2 and ds[S]:result=ivsub(result,ivscale(logiv(ds[S]),ds[S]))
    return result

def run():
    FF=sp.Matrix([[1,0],[0,1],[Q(3,5),Q(4,5)],[Q(5,13),Q(12,13)]])
    G1=FF.copy();G1[3,1]=-G1[3,1]
    G0=sp.Matrix([[1,0],[0,1],[Q(5,13),Q(12,13)],[Q(8,17),Q(15,17)]])
    output={}
    for name,GG in [('dense_intersection1',G1),('dense_intersection0',G0)]:
        X=FF*FF.T/4;Y=GG*GG.T/4;M=(X+Y)/2
        assert all(X[i,i]==Y[i,i]==Q(1,4) for i in range(4))
        assert X.rank()==Y.rank()==2 and M.rank()==(3 if name.endswith('1') else 4)
        for K in [X,Y,M]:legal_psd(K)
        comm=sp.trace((X*Y-Y*X).T*(X*Y-Y*X));assert comm>0
        beta=ivsub(second(M),ivscale(ivadd(second(X),second(Y)),Q(1,2)))
        assert beta[0]>0
        # The two coefficient formulas agree within their exact log enclosures;
        # their symbolic identity is proved in dilute_chord_theorem.md.
        for K in [X,Y,M]:
            e=ivsub(second(K),coef_direct(K));assert e[0]<=0<=e[1]
        data=[poly_data(K) for K in [X,Y,M]]
        rho=min(map(rho_of,data))
        bb=(third_bound(data[2],rho)+(third_bound(data[0],rho)+third_bound(data[1],rho))/2)/6
        Bceil=-((-bb.numerator)//bb.denominator)
        threshold=min(rho,beta[0]/(2*(Bceil+1)))
        lam=F(1)
        while lam>threshold:lam/=10
        theoretical=lam*lam*beta[0]/2
        lx=sp.Rational(lam.numerator,lam.denominator)
        direct=gap(*[law(lx*K) for K in [X,Y,M]])
        assert direct[0]>theoretical>0
        full_G=gap(*[law(K) for K in [X,Y,M]])
        record={'F':[[str(x) for x in row] for row in FF.tolist()],
                'G_frame':[[str(x) for x in row] for row in GG.tolist()],
                'rank_mid':M.rank(),'commutator_Frobenius_squared':str(comm),
                'first_order_gap':'0 (exact equal diagonal)', 'second_order_gap_interval':ivshow(beta),
                'rho':str(rho),'remainder_B_upper_integer':Bceil,
                'certified_all_lambda_interval':'(0,'+str(lam)+']',
                'at_upper_lambda_theoretical_G_lower':dec(theoretical,digits=36),
                'at_upper_lambda_direct_G_interval':[dec(direct[0],digits=36),dec(direct[1],digits=36,upper=True)],
                'full_intensity_G_interval':ivshow(full_G),
                'q_polynomials':{name2:{','.join(str(i+1) for i in S):[str(v) for v in cs] for S,cs in dt.items()} for name2,dt in zip(['minus','plus','mid'],data)}}
        output[name]=record
        print(name,json.dumps({k:v for k,v in record.items() if k not in ['q_polynomials','F','G_frame']}))
    Path(__file__).with_name('dilute_certificate.json').write_text(json.dumps(output,indent=2)+'\n')
if __name__=='__main__':run()
