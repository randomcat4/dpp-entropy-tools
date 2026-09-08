"""P4-10C exact finite polynomial identities, not a numerical grid.

The proof of uniform Hessian signs is in diagonal_perturbation_candidate.md.
This script only checks all eight event identities and the degree <=7 Taylor
coefficients with symbolic independent centered moments.
"""
from fractions import Fraction as F

class P:
    n=6
    def __init__(self,terms=0):
        if isinstance(terms,P):self.t=dict(terms.t)
        elif isinstance(terms,dict):self.t={k:F(v) for k,v in terms.items() if v}
        else:self.t={} if not terms else {(0,)*self.n:F(terms)}
    def __add__(self,b):
        out=dict(self.t)
        for k,v in P(b).t.items():out[k]=out.get(k,F(0))+v
        return P(out)
    __radd__=__add__
    def __neg__(self):return P({k:-v for k,v in self.t.items()})
    def __sub__(self,b):return self+-P(b)
    def __rsub__(self,b):return P(b)+-self
    def __mul__(self,b):
        out={}
        for k,v in self.t.items():
            for l,w in P(b).t.items():
                m=tuple(a+b for a,b in zip(k,l));out[m]=out.get(m,F(0))+v*w
        return P(out)
    __rmul__=__mul__
    def __pow__(self,n):
        out=P(1)
        for _ in range(n):out=out*self
        return out
    def __eq__(self,b):return self.t==P(b).t
def var(i):
    k=[0]*P.n;k[i]=1;return P({tuple(k):1})

def events():
    d1,d2,d3,x,y,z=map(var,range(6));ds=[d1,d2,d3]
    q=[P(1),d1,d2,d1*d2-x*x,d3,d1*d3-y*y,d2*d3-z*z,
       d1*d2*d3-d3*x*x-d2*y*y-d1*z*z+2*x*y*z]
    p=list(q)
    for i in range(3):
        for mask in range(8):
            if not(mask>>i&1):p[mask]=p[mask]-p[mask|1<<i]
    for mask in range(8):
        sign=[1 if mask>>i&1 else -1 for i in range(3)]
        marginal=[ds[i] if mask>>i&1 else 1-ds[i] for i in range(3)]
        rhs=marginal[0]*marginal[1]*marginal[2]
        rhs-=x*x*sign[0]*sign[1]*marginal[2]
        rhs-=y*y*sign[0]*sign[2]*marginal[1]
        rhs-=z*z*sign[1]*sign[2]*marginal[0]
        rhs+=2*x*y*z*sign[0]*sign[1]*sign[2]
        assert p[mask]==rhs,mask
    assert sum(p,P(0))==1
    print('PASS: all 8 Mobius full-event polynomials and probability mass')

def taylor():
    # In this ring variables are x,y,z,psi1,psi2,psi3.
    x,y,z,u,v,w=map(var,range(6))
    g=-(x*x*u*v+y*y*u*w+z*z*v*w)+2*x*y*z*u*v*w
    raw=-F(1,2)*g**2+F(1,6)*g**3
    # Expectation ring key: edge exponents, then powers of a1,a2,a3,b1,b2,b3.
    # E psi_i=0, E psi_i^2=a_i, E psi_i^3=b_i.
    actual={}
    for k,c in raw.t.items():
        if sum(k[:3])>7 or 1 in k[3:]:continue
        key=list(k[:3])+[0]*6
        for i,n in enumerate(k[3:]):
            if n==2:key[3+i]+=1
            elif n==3:key[6+i]+=1
            elif n!=0:raise AssertionError(('unneeded moment',n))
        key=tuple(key);actual[key]=actual.get(key,F(0))+c
    actual={k:v for k,v in actual.items() if v}
    expected={}
    def term(edge,aa,bb,coef):expected[tuple(edge)+tuple(aa)+tuple(bb)]=F(coef)
    term((4,0,0),(1,1,0),(0,0,0),-F(1,2))
    term((0,4,0),(1,0,1),(0,0,0),-F(1,2))
    term((0,0,4),(0,1,1),(0,0,0),-F(1,2))
    term((6,0,0),(0,0,0),(1,1,0),-F(1,6))
    term((0,6,0),(0,0,0),(1,0,1),-F(1,6))
    term((0,0,6),(0,0,0),(0,1,1),-F(1,6))
    term((2,2,2),(1,1,1),(0,0,0),-3)
    term((3,3,1),(0,1,1),(1,0,0),2)
    term((3,1,3),(1,0,1),(0,1,0),2)
    term((1,3,3),(1,1,0),(0,0,1),2)
    assert actual==expected
    assert all(sum(k[:3]) in (4,6,7) for k in actual)
    print('PASS: exact degree 4, 6, 7 entropy coefficients; degree 5 is zero')

if __name__=='__main__':events();taylor()
