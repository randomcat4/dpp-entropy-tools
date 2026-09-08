"""Standard-library exact event Hessian / reflection-block sanity, no author imports."""
import sys
sys.dont_write_bytecode=True
sys.set_int_max_str_digits(0)
from fractions import Fraction as Q
from decimal import Decimal as R,localcontext
from itertools import permutations
from pathlib import Path
import json,hashlib,time
HERE=Path(__file__).resolve().parent
COORD=((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))
def dec(x):return R(x.numerator)/R(x.denominator) if isinstance(x,Q) else R(x)
def mul(a,b):return [sum(a[k]*b[j-k] for k in range(j+1)) for j in range(3)]
def event_jet(K,D,s):
    out=[Q(0)]*3
    for perm in permutations(range(3)):
        sign=(-1)**(3-s.bit_count()+sum(perm[i]>perm[j] for i in range(3) for j in range(i+1,3)))
        v=[Q(sign),Q(0),Q(0)]
        for i,j in enumerate(perm):
            v=mul(v,[K[i][j]-Q(i==j and not(s>>i&1)),D[i][j],Q(0)])
        out=[a+b for a,b in zip(out,v)]
    return out[0],out[1],2*out[2]
def mat(v):
    a=[[Q(0)]*3 for _ in range(3)]
    for x,(i,j) in zip(v,COORD):a[i][j]=a[j][i]=x
    return a
def form(B,v,w):return sum(v[i]*B[i][j]*w[j] for i in range(len(v)) for j in range(len(w)))
def ldl(B):
    a=[r[:] for r in B];out=[]
    for k in range(len(a)):
        d=a[k][k];assert d>0;out.append(d)
        for i in range(k+1,len(a)):
            for j in range(i,len(a)):a[j][i]=a[i][j]=a[i][j]-a[i][k]*a[k][j]/d
    return out
def calc(x,a):
    K=[[x,a,Q(0)],[a,x,a],[Q(0),a,x]];basis=[mat([Q(i==j) for i in range(6)]) for j in range(6)]
    jd=[[event_jet(K,E,s) for s in range(8)] for E in basis]
    p=[v[0] for v in jd[0]];g=[[jd[i][s][1] for i in range(6)] for s in range(8)]
    assert min(p)>0 and sum(p)==1
    h=[[[Q(0)]*6 for _ in range(6)] for _ in range(8)]
    for i in range(6):
        for s in range(8):h[s][i][i]=jd[i][s][2]
        for j in range(i):
            E=[[basis[i][k][l]+basis[j][k][l] for l in range(3)] for k in range(3)]
            for s in range(8):h[s][i][j]=h[s][j][i]=(event_jet(K,E,s)[2]-jd[i][s][2]-jd[j][s][2])/2
    with localcontext() as ctx:
        ctx.prec=120
        P=list(map(dec,p));logs=[v.ln() for v in P]
        B=[[dec(sum(g[s][i]*g[s][j]/p[s] for s in range(8)))+sum(dec(h[s][i][j])*logs[s] for s in range(8)) for j in range(6)] for i in range(6)]
        bp=ldl(B)
        od=[list(map(R,v)) for v in ((1,0,-1,0,0,0),(0,0,0,1,0,-1))]
        ev=[list(map(R,v)) for v in ((1,0,1,0,0,0),(0,1,0,0,0,0),(0,0,0,1,0,1),(0,0,0,0,1,0))]
        cross=max(abs(form(B,v,w)) for v in od for w in ev)
        assert cross<R('1e-105')
        Bd=[[form(B,v,w) for w in ev] for v in ev]
        ell=(P[0]*P[3]/(P[1]*P[2])).ln();kappa=(P[0]*P[5]/P[1]**2).ln()
        lam=(P[7]*P[1]*P[2]*P[4]/(P[0]*P[3]*P[5]*P[6])).ln()
        n=-ell-lam*dec(x);m=-kappa-lam*dec(x);aa=dec(a)
        Fe=[[sum(dec(sum(g[s][z]*Q(v[z]) for z in range(6)))*dec(sum(g[s][z]*Q(w[z]) for z in range(6)))/P[s] for s in range(8)) for w in ev] for v in ev]
        correction=[[R(0)]*4 for _ in range(4)]
        correction[0][0]=-2*m;correction[0][1]=correction[1][0]=-2*n
        correction[2][2]=4*n;correction[3][3]=2*m
        correction[0][2]=correction[2][0]=-4*lam*aa
        correction[2][3]=correction[3][2]=4*lam*aa
        err=max(abs(Bd[i][j]-Fe[i][j]-correction[i][j]) for i in range(4) for j in range(4))
        assert err<R('1e-105')
        out={'x':x,'a':a,'p':p,'strict_K_pivots':ldl(K),'strict_I_minus_K_pivots':ldl([[Q(i==j)-K[i][j] for j in range(3)] for i in range(3)]),
             'B_pivots':bp,'reflection_cross_error':cross,'even_formula_error':err,'full_B_negative_entropy_curvature':True}
        if x==Q(1,2):
            r=8*dec(a*a);u=r*r;L=1-u;v=2-u
            nn=((1+r)/(1-r)).ln();mm=-(1-r*r).ln();z=r*nn-mm
            C=[[4-2*u-u*u-mm*L,r*v-nn*L,u*u],[r*v-nn*L,v,r*u],[u*u,r*u,u*v+mm*L]]
            ind=(0,1,3)
            coreerr=max(abs(Bd[ind[i]][ind[j]]-2*C[i][j]/L) for i in range(3) for j in range(3))
            assert coreerr<R('1e-103') and max(abs(Bd[2][j]) for j in ind)<R('1e-105')
            numerator=mm*(8-L*nn*nn)+8*u*z+16*u-v*z*z
            assert numerator>4*mm+12*u and L*nn*nn<4 and 0<z<2*u
            out['center_proof_sanity']={'r':r,'n':nn,'m':mm,'z':z,'det_numerator':numerator,
                 'lower_bound_4m_plus_12u':4*mm+12*u,'core_formula_error':coreerr,'C_pivots':ldl(C)}
        return out
class Poly:
    def __init__(self,x):self.c=x if isinstance(x,dict) else {(0,0,0):Q(x)}
    def __add__(self,b):
        if not isinstance(b,Poly):b=Poly(b)
        out=self.c.copy()
        for k,v in b.c.items():out[k]=out.get(k,Q(0))+v
        return Poly({k:v for k,v in out.items() if v})
    __radd__=__add__
    def __neg__(self):return Poly({k:-v for k,v in self.c.items()})
    def __sub__(self,b):return self+-b if isinstance(b,Poly) else self+(-Poly(b))
    def __rsub__(self,b):return Poly(b)+(-self)
    def __mul__(self,b):
        if not isinstance(b,Poly):b=Poly(b)
        out={}
        for k,v in self.c.items():
            for l,w in b.c.items():
                s=tuple(k[i]+l[i] for i in range(3));out[s]=out.get(s,Q(0))+v*w
        return Poly({k:v for k,v in out.items() if v})
    __rmul__=__mul__
    def __pow__(self,n):
        out=Poly(1)
        for _ in range(n):out=out*self
        return out
def symbolic():
    r,n,m=[Poly({tuple(int(i==j) for i in range(3)):Q(1)}) for j in range(3)]
    u=r*r;L=1-u;v=2-u;z=r*n-m
    det=(4*v+2*r*n*v-m*v-L*n*n)*(m*v+4*u)-(r**3*n)**2
    target=v*(m*(8-L*n*n)+8*u*z+16*u-v*z*z)
    residual=det-target;assert not residual.c
    return {'polynomial_variables':['r','n','m'],'determinant_identity_exact_zero':True,'residual_coefficients':{}}
def encode(x):
    if isinstance(x,(Q,R)):return str(x)
    if isinstance(x,(list,tuple)):return [encode(v) for v in x]
    if isinstance(x,dict):return {k:encode(v) for k,v in x.items()}
    return x
def main():
    started=time.time();rows=[]
    for x in (Q(1,10),Q(1,4),Q(1,2),Q(3,4),Q(9,10)):
        for scale in (Q(1,4),Q(1,2),Q(2,3)):rows.append(calc(x,min(x,1-x)*scale))
    rows.append(calc(Q(1,2),Q(7,20)))
    report={'status':'SCOUT_PLUS_SYMBOLIC_IDENTITY_NOT_GLOBAL_PROOF','rows':rows,'denominator':len(rows),'symbolic':symbolic(),
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'elapsed_seconds':time.time()-started,'exit_code':0}
    (HERE/'sanity.json').write_text(json.dumps(encode(report),indent=2),encoding='utf-8')
    print('exit=0 centers=',len(rows),'symbolic identity=',report['symbolic'])
if __name__=='__main__':main()
