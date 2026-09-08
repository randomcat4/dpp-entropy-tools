"""U10h standard-library author sanity, not independent certification.
All numerical evaluations are finite SCOUT. Run: python sanity.py
"""
import hashlib
import json
import math
import sys
from decimal import Decimal as D, localcontext
from fractions import Fraction as Q
from pathlib import Path

sys.dont_write_bytecode=True
sys.set_int_max_str_digits(0)
ROOT=Path(__file__).resolve().parent

class P:
    def __init__(self,v=0):
        self.c=({e:Q(t) for e,t in v.items() if t} if isinstance(v,dict)
                else ({(0,0):Q(v)} if v else {}))
    def __add__(self,b):
        b=b if isinstance(b,P) else P(b); d=self.c.copy()
        for e,t in b.c.items(): d[e]=d.get(e,0)+t
        return P(d)
    __radd__=__add__
    def __neg__(self): return P({e:-t for e,t in self.c.items()})
    def __sub__(self,b): return self+(-b if isinstance(b,P) else -Q(b))
    def __rsub__(self,b): return -self+b
    def __mul__(self,b):
        b=b if isinstance(b,P) else P(b); d={}
        for e,t in self.c.items():
            for f,u in b.c.items():
                k=(e[0]+f[0],e[1]+f[1]); d[k]=d.get(k,0)+t*u
        return P(d)
    __rmul__=__mul__
    def __pow__(self,n):
        p=P(1)
        for _ in range(n): p=p*self
        return p
    def __truediv__(self,n): return self*Q(1,n)
    def diff(self,i):
        d={}
        for e,t in self.c.items():
            if e[i]:
                f=list(e); f[i]-=1; d[tuple(f)]=t*e[i]
        return P(d)
    def ev(self,a,b): return sum(t*a**e[0]*b**e[1] for e,t in self.c.items())

a=P({(1,0):1}); b=P({(0,1):1})
uu=a+2*b-3*a*b; vv=2*a+b-3*a*b
ps=[(1-a)*(1-b)**2,(1-b)*uu/3,b*vv/3,a*b**2]
mult=[1,3,3,1]
assert not (sum(m*p for m,p in zip(mult,ps))-1).c
gr=[[p.diff(i) for i in range(2)] for p in ps]
hs=[[[p.diff(i).diff(j) for j in range(2)] for i in range(2)] for p in ps]
a0=a*(1-a); b0=b*(1-b)
knum=2*a0*b0*((1-b)*vv+b*uu); kden=uu*vv
common=P(1)
for p in ps: common=common*p
fnum=[[P(0) for _ in range(2)] for _ in range(2)]
for i in range(2):
    for j in range(2):
        for k in range(4):
            rest=P(1)
            for l in range(4):
                if l!=k: rest=rest*ps[l]
            fnum[i][j]+=mult[k]*gr[k][i]*gr[k][j]*rest
targets={(0,0):(a0*kden-knum,a0**2*kden),
         (0,1):(knum,a0*b0*kden),
         (1,1):(2*b0*kden-knum,b0**2*kden)}
for ij,(num,den) in targets.items():
    assert not (fnum[ij[0]][ij[1]]*den-num*common).c
ell_coeff=[1,-2,1,0]; lam_coeff=[-1,3,-3,1]
for k in range(4):
    assert not hs[k][0][0].c
    assert not (mult[k]*hs[k][0][1]-2*(ell_coeff[k]+b*lam_coeff[k])).c
    assert not (mult[k]*hs[k][1][1]-2*(ell_coeff[k]+a*lam_coeff[k])).c

def dec(v): return D(v.numerator)/D(v.denominator) if isinstance(v,Q) else D(v)
def evaluate(label,aa,bb,normalize=None,transverse=None):
    assert 0<aa<1 and 0<bb<1 and aa!=bb
    p=[x.ev(aa,bb) for x in ps]
    xx=(aa+2*bb)/3; off=(aa-bb)/3
    inc=[Q(1),xx,xx**2-off**2,aa*bb**2]
    mob=[sum((-1)**(j-k)*math.comb(3-k,j-k)*inc[j] for j in range(k,4)) for k in range(4)]
    assert mob==p and min(p)>0 and sum(m*t for m,t in zip(mult,p))==1
    g=[[x.ev(aa,bb) for x in row] for row in gr]
    h=[[[x.ev(aa,bb) for x in row] for row in z] for z in hs]
    f=[[sum(mult[k]*g[k][i]*g[k][j]/p[k] for k in range(4)) for j in range(2)] for i in range(2)]
    u=1/(aa*(1-aa)); v=1/(bb*(1-bb))
    kap=knum.ev(aa,bb)/kden.ev(aa,bb)
    assert f==[[u-kap*u*u,kap*u*v],[kap*u*v,2*v-kap*v*v]]
    with localcontext() as ctx:
        ctx.prec=150
        c=[[dec(f[i][j])+sum(mult[k]*dec(h[k][i][j])*dec(p[k]).ln() for k in range(4)) for j in range(2)] for i in range(2)]
        ell=dec(p[0]*p[2]/p[1]**2).ln()
        lam=dec(p[3]*p[1]**3/(p[0]*p[2]**3)).ln()
        na=-ell-dec(aa)*lam; nb=-ell-dec(bb)*lam
        assert min(na,nb)>0
        c2=[[dec(f[0][0]),dec(f[0][1])-2*nb],[dec(f[1][0])-2*nb,dec(f[1][1])-2*na]]
        error=max(abs(c[i][j]-c2[i][j]) for i in range(2) for j in range(2))
        assert error<D('1e-100')
        det=c[0][0]*c[1][1]-c[0][1]**2
        assert c[0][0]>0 and det>0
        row={'label':label,'alpha':str(aa),'beta':str(bb),'atoms_exact':list(map(str,p)),
             'kappa_exact':str(kap),'Delta_T':str(det),'Caa':str(c[0][0]),'Cab':str(c[0][1]),
             'Cbb':str(c[1][1]),'max_log_reduction_error':str(error),'status':'SCOUT'}
        if normalize:
            t=dec(transverse)
            ll=2/(t*(1-t))-2*(D(4)/3).ln()
            target={'alpha0':t*t*ll,'alpha1':(1-t)**2*ll,
                    'beta0':2/(1-t),'beta1':2/t}[label]
            value=dec(normalize)*det
            row.update(normalized_determinant=str(value),limit_target=str(target),
                       relative_limit_error=str(abs(value/target-1)))
        if label=='diagonal':
            row['Delta_over_difference_squared']=str(det/dec(aa-bb)**2)
            row['diagonal_limit']=str(2/(3*dec(xx)**3*(1-dec(xx))**3))
        return row

def factors(n):
    out={}; d=2
    while d*d<=n:
        while n%d==0: out[d]=out.get(d,0)+1; n//=d
        d+=1
    if n>1: out[n]=out.get(n,0)+1
    return out
def entropy_prime_coefficients(aa,bb):
    out={}
    for m,p in zip(mult,[v.ev(aa,bb) for v in ps]):
        for sign,n in [(1,p.numerator),(-1,p.denominator)]:
            for prime,e in factors(n).items(): out[prime]=out.get(prime,Q(0))-m*p*e*sign
    return out
cfirst=entropy_prime_coefficients(Q(1,5),Q(2,5)); csecond=entropy_prime_coefficients(Q(2,5),Q(1,5))
diff={p:cfirst.get(p,Q(0))-csecond.get(p,Q(0)) for p in set(cfirst)|set(csecond)}
diff={p:v for p,v in diff.items() if v}
den=math.lcm(*(v.denominator for v in diff.values()))
integer_exponents={str(p):int(v*den) for p,v in diff.items()}
assert integer_exponents
with localcontext() as ctx:
    ctx.prec=150
    entropy_difference=sum(dec(v)*D(p).ln() for p,v in diff.items())

cases=[]
for aa,bb in [(Q(1,5),Q(2,5)),(Q(2,5),Q(1,5)),(Q(1,100),Q(99,100)),
              (Q(99,100),Q(1,100)),(Q(1,4),Q(3,4)),(Q(3,4),Q(1,4))]:
    cases.append(('base',aa,bb,None,None))
for t in [Q(1,10),Q(1,4),Q(1,2),Q(3,4),Q(9,10)]:
    for exponent in [3,8,20]:
        e=Q(1,10**exponent)
        cases.extend([('alpha0',e,t,e,t),('alpha1',1-e,t,e,t),
                      ('beta0',t,e,e,t),('beta1',t,1-e,e,t)])
    for exponent in [4,12]:
        for sign in [-1,1]:
            off=Q(sign,10**exponent)
            cases.append(('diagonal',t+2*off,t-off,None,None))
rows=[evaluate(*case) for case in cases]
hashes={}
for name in ['frozen_problem.md','proof_or_blocker.md','sanity.py',
             '../exchangeable_triangle_subfamily/proof_or_blocker.md',
             '../exchangeable_triangle_subfamily/fresh_audit.md']:
    hashes[name]=hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
out={'status':'AUTHOR_CANDIDATES_PENDING_REVIEW_GLOBAL_INCOMPLETE','precision':150,
     'symbolic_checks':{'rational_Fisher_rank_one_identities':3,'log_acceleration_identities':8,
                         'alpha_alpha_acceleration_zero':4,'swap_entropy_inequality_exact':True},
     'denominators':{'base':6,'boundary':60,'diagonal':20,'total':86,'failures':0,'positive_curvature_candidates':0},
     'swap_blocker':{'alpha_beta_first':['1/5','2/5'],'second':['2/5','1/5'],
                     'clear_denominator':den,'integer_prime_log_exponents':integer_exponents,
                     'entropy_first_minus_second_decimal':str(entropy_difference),
                     'exact_nonzero_reason':'unique prime factorization after exponentiating the cleared log sum'},
     'rows':rows,'source_hashes':hashes}
(ROOT/'sanity.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':out['status'],'denominators':out['denominators'],
                  'symbolic_checks':out['symbolic_checks'],'swap_blocker':out['swap_blocker']},indent=2))
