"""Frozen rational input and complete-event coefficient construction.
The PR58 input is copied from ADDENDUM_JOINT_ADDITIVE.md at
89aa874c24dd5a3ea98f8474826392560b1d0397. No fixture is inferred from outputs.
"""
from fractions import Fraction as F
import sympy as sp
Q=sp.Rational

def original():
    A=sp.Matrix([[Q(219,500),-Q(47,1000),Q(73,1000)],[-Q(47,1000),Q(461,1000),Q(23,1000)],[Q(73,1000),Q(23,1000),Q(43,100)]])
    C=sp.Matrix([[Q(231,500),Q(1,50),-Q(49,1000)],[Q(1,50),Q(43,100),Q(11,200)],[-Q(49,1000),Q(11,200),Q(3,5)]])
    U=sp.Matrix([[Q(7,40),-Q(22,125)],[Q(339,1000),Q(13,250)],[Q(229,500),-Q(231,500)]])
    V=sp.Matrix([[Q(141,200),Q(981,1000)],[-Q(343,1000),Q(113,250)],[Q(187,250),Q(577,1000)]])
    return A,C,U,V

def mode_base():
    A=sp.Matrix([[Q(1,3),Q(1,6)],[Q(1,6),Q(1,3)]])
    C=sp.Matrix([[Q(2,5),Q(1,48)],[Q(1,48),Q(3,5)]])
    B=sp.Matrix([[1,1],[2,-1]])/12
    W=sp.Matrix([[Q(3,5),0],[Q(4,5),0],[0,1]])
    return A,C,B,W

def ff(z):return F(int(sp.numer(z)),int(sp.denom(z)))
def em(K,m):return K-sp.diag(*[1-((m>>i)&1) for i in range(K.rows)])
def ep(K,m):return (-1)**(K.rows-m.bit_count())*em(K,m).det()
def pd(K):
    assert K==K.T
    return all(K[:i,:i].det()>0 for i in range(1,K.rows+1))

def coefficients(A,C,U,V):
    """All (i,j,mu,a,b,(p0,p1,p2)) records in i-major subset-mask order."""
    B=U*V.T
    assert B.rank()==2
    assert all(pd(K) for K in [A,C,sp.eye(A.rows)-A,sp.eye(C.rows)-C])
    pa=[ff(ep(A,i)) for i in range(1<<A.rows)]
    pc=[ff(ep(C,j)) for j in range(1<<C.rows)]
    assert min(pa+pc)>0 and sum(pa)==sum(pc)==1
    GA=[U.T*em(A,i).inv()*U for i in range(len(pa))]
    GC=[V.T*em(C,j).inv()*V for j in range(len(pc))]
    rows=[]
    for i in range(len(pa)):
        for j in range(len(pc)):
            a,b=ff(sp.trace(GA[i]*GC[j])),ff(GA[i].det()*GC[j].det())
            mu=pa[i]*pc[j];rows.append((i,j,mu,a,b,(mu,-mu*a,mu*b)))
    for i in range(len(pa)):
        for c in [3,4]:assert sum(pc[j]*rows[len(pc)*i+j][c] for j in range(len(pc)))==0
    for j in range(len(pc)):
        for c in [3,4]:assert sum(pa[i]*rows[len(pc)*i+j][c] for i in range(len(pa)))==0
    assert sum(z[5][0] for z in rows)==1
    assert sum(z[5][1] for z in rows)==sum(z[5][2] for z in rows)==0
    return pa,pc,rows

def direct_mobius_check(A,C,B,rows):
    """A second author algebra route: every principal minor then full Mobius inversion.
    This is not an independent non-author computation or temporal interpolation.
    """
    t=sp.Symbol('t');m=A.rows;n=m+C.rows
    K=A.row_join(t*B).col_join((t*B.T).row_join(C))
    minors=[]
    for mask in range(1<<n):
        ids=[i for i in range(n) if (mask>>i)&1]
        z=sp.Integer(1) if not ids else K.extract(ids,ids).det(method='domain-ge')
        minors.append(sp.Poly(z,t,domain=sp.QQ))
    for i,j,mu,a,b,pr in rows:
        mask=i+(j<<m);summ=sp.Poly(0,t,domain=sp.QQ)
        for M in range(1<<n):
            if (M&mask)==mask:summ+=(-1)**((M^mask).bit_count())*minors[M]
        expected=sp.Poly(sum(Q(x.numerator,x.denominator)*t**(2*k) for k,x in enumerate(pr)),t,domain=sp.QQ)
        assert summ==expected, ('Mobius mismatch',i,j)
    return len(minors),len(rows)
