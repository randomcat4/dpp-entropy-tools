"""Exact formal polynomial checks, not a parameter scan or sign certificate."""
from fractions import Fraction as Q
from itertools import permutations
import json

N = 8
class P:
    def __init__(self, value=0):
        self.d = value if isinstance(value, dict) else ({(0,)*N: Q(value)} if value else {})
        self.d = {k: Q(v) for k,v in self.d.items() if v}
    def __add__(self, other):
        other = coerce(other); d = dict(self.d)
        for k,v in other.d.items(): d[k] = d.get(k,Q(0))+v
        return P(d)
    __radd__ = __add__
    def __neg__(self): return P({k:-v for k,v in self.d.items()})
    def __sub__(self, other): return self+-coerce(other)
    def __rsub__(self, other): return coerce(other)+-self
    def __mul__(self, other):
        other = coerce(other); d = {}
        for k,v in self.d.items():
            for l,w in other.d.items():
                s = tuple(x+y for x,y in zip(k,l)); d[s] = d.get(s,Q(0))+v*w
        return P(d)
    __rmul__ = __mul__
    def __truediv__(self, scalar): return self*Q(1,scalar)
    def __pow__(self, n):
        z = P(1)
        for _ in range(n): z=z*self
        return z
    def __eq__(self, other): return self.d == coerce(other).d

def coerce(x): return x if isinstance(x,P) else P(x)
def var(i): return P({tuple(int(j==i) for j in range(N)):Q(1)})
def outer(v): return [[x*y for y in v] for x in v]
def add(*ms): return [[sum(m[i][j] for m in ms) for j in range(len(ms[0][0]))] for i in range(len(ms[0]))]
def scale(a,m): return [[a*x for x in row] for row in m]
def congr(m,cols):
    return [[sum(cols[i][k]*m[k][l]*cols[j][l] for k in range(len(m)) for l in range(len(m))) for j in range(len(cols))] for i in range(len(cols))]
def determinant(m):
    n=len(m); out=P(0)
    for p in permutations(range(n)):
        sign=(-1)**sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))
        z=P(sign)
        for i in range(n): z=z*m[i][p[i]]
        out=out+z
    return out

def check_blocks():
    a,c,w0,w1,w2,w3,de,A=[var(i) for i in range(8)]
    lam=a-c; d=a+c
    U=[1,1,1,0,0,0]; Qv=[0,0,0,1,1,1]
    full=[lam*d*U[j]-2*lam*c*Qv[j] for j in range(6)]
    empty=[(2*a-1)*U[j]-2*c*Qv[j]-full[j] for j in range(6)]
    singles=[]; pairs=[]
    for i in range(3):
        singles.append([(1-a)*int(j==i)-a*U[j]+2*c*(Qv[j]-int(j==3+i))+full[j] for j in range(6)])
        pairs.append([a*(U[j]-int(j==i))-2*c*int(j==3+i)-full[j] for j in range(6)])
    jets=[empty]+singles+pairs+[full]
    weights=[w0]+[w1]*3+[w2]*3+[w3]
    F=add(*[scale(w,outer(v)) for w,v in zip(weights,jets)])
    assert all(sum(v[j] for v in jets)==0 for j in range(6))
    tau=[[P(0) for _ in range(6)] for _ in range(6)]
    for i in range(3):
        tau[3+i][3+i]=-2*a; tau[i][3+i]=tau[3+i][i]=-2*c
        for j in range(i):
            tau[i][j]=tau[j][i]=a; tau[3+i][3+j]=tau[3+j][3+i]=2*c
    sig=[[P(0) for _ in range(6)] for _ in range(6)]
    sig[1][2]=sig[2][1]=P(1); sig[3][3]=P(-2)
    M=add(F,scale(-de,tau),scale(-A,sig))
    fs=[[w1*(1-a)**2+w2*a*a,2*c*(w2*a-w1*(1-a))],
        [2*c*(w2*a-w1*(1-a)),4*c*c*(w1+w2)]]
    S=add(fs,scale(de,[[a,2*c],[2*c,2*d]]))
    v3=[lam*d,-2*lam*c]; v0=[2*a-1-lam*d,-2*c+2*lam*c]
    b1=[1-4*a+3*lam*d,(4-6*lam)*c]; b2=[2*a-3*lam*d,(6*lam-2)*c]
    ft=add(scale(3*w0,outer(v0)),scale(w1,outer(b1)),scale(w2,outer(b2)),scale(3*w3,outer(v3)))
    T=add(ft,scale(-de,[[2*a,-2*c],[-2*c,4*c-2*a]]))
    t11,t12,t22=T[0][0],T[0][1],T[1][1]
    s11,s12,s22=S[0][0],S[0][1],S[1][1]
    even=[[3*t11-2*A,3*t12,2*A,0],[3*t12,3*t22+2*A,0,4*A],
          [2*A,0,6*s11-2*A,6*s12],[0,4*A,6*s12,6*s22+8*A]]
    odd=scale(2,add(S,[[A,0],[0,0]]))
    cols=[[0,1,-1,0,0,0],[0,0,0,0,1,-1],
          [1,1,1,0,0,0],[0,0,0,1,1,1],
          [2,-1,-1,0,0,0],[0,0,0,2,-1,-1]]
    got=congr(M,cols)
    for i in range(6):
        for j in range(6):
            expect=odd[i][j] if i<2 and j<2 else (even[i-2][j-2] if i>=2 and j>=2 else 0)
            assert got[i][j]==expect, (i,j)
    return {'mass_jet_identities':6,'full_congruence_entries':36,'symbolic_event_weights':'independent reciprocal p0,p1,p2,p3'}

def check_det():
    t11,t12,t22,s11,s12,s22,A=[var(i) for i in range(7)]
    dt=t11*t22-t12*t12; ds=s11*s22-s12*s12
    E=[[3*t11-2*A,3*t12,2*A,0],[3*t12,3*t22+2*A,0,4*A],
       [2*A,0,6*s11-2*A,6*s12],[0,4*A,6*s12,6*s22+8*A]]
    L=(2*t11-2*t22)*ds+(4*s11-s22)*dt
    J=2*ds+2*dt+4*t22*s11+t11*s22+4*t12*s12
    phi=9*dt*ds+3*A*L-2*A*A*J
    assert determinant(E)==36*phi
    uu=2*t22*ds+s22*dt; vv=t11*ds+2*s11*dt; ww=-t12*ds+s12*dt
    assert uu*vv-2*ww*ww==dt*ds*J
    assert determinant([[2*(s11+A),2*s12],[2*s12,2*s22]])==4*(ds+A*s22)
    return {'even_determinant_identity':True,'Gram_numerator_identity':True,'odd_determinant_identity':True,
            'phi_expanded_monomials':len(phi.d)}

if __name__=='__main__':
    print(json.dumps({'status':'PASS_FORMAL_IDENTITIES_ONLY','parameter_evaluations':0,
                      'blocks':check_blocks(),'determinants':check_det(),
                      'unproved':'Phi>=0 on all 0<mu<lambda<1'},indent=2))
