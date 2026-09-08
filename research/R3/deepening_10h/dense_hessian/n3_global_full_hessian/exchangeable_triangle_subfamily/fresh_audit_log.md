# D10-U10f independent audit replay log

This is a non-author audit. Only the three fresh_audit files are written.
The complete independent implementation is embedded below to keep the
authorized output footprint to those three files. No author script/module
or previously computed Hessian cache is imported or executed.

Replay from this directory with Python 3.11+:

```text
python -c "from pathlib import Path; s=Path('fresh_audit_log.md').read_text(encoding='utf-8'); exec(compile(s.split('```python\n',1)[1].split('\n```',1)[0], 'independent_u10f_audit', 'exec'))"
```

The implementation generates exact multivariate inclusion determinants,
Möbius atoms, and symbolic derivatives. Fractions are evaluated first;
only the logarithms and subsequent Hessian arithmetic use Decimal, at 150
digits. Source hashes are frozen and checked before computation.

Execution record, 2026-09-08:

- Initial inventory/read command returned exit 1 because this author unit has
  proof_or_blocker.md, not a derivation.md. No computation or file mutation
  occurred in that failed read. The correct frozen file was then fully read.
- First independent replay: exit 0; all symbolic checks and 37/37
  high-precision cases passed.
- Strengthened replay with rational logarithm intervals: exit 0; additionally
  all 12 warning-point encodings have strictly positive certified invariant
  determinants. A final clean replay after freezing this log also passed.
- No author-version drift was found. No other author cache was executed;
  sanity_results.json supplies only frozen warning input coordinates and
  reported denominator metadata.
- The 57,360 grid + 120,000 generated random acceptance denominator was
  independently regenerated; the entire author floating sign batch was NOT
  replayed. This limitation is explicit in the JSON.
- Only fresh_audit.md, fresh_audit_results.json, and this log are written.

```python
import hashlib
import itertools
import json
import random
import sys
from decimal import Decimal as D, localcontext
from fractions import Fraction as Q
from pathlib import Path

sys.dont_write_bytecode = True
sys.set_int_max_str_digits(0)
ROOT = Path.cwd()
EXPECTED = {
 'frozen_problem.md':'c27369fe3785ac0a4f56e40e95a57ecca593e11d44d14ab92a54938177d3dacf',
 'proof_or_blocker.md':'8034ada41d90e34c79891e47b62e0bc20d5a14fd85f8a405a1ee4d5223039538',
 'hazards.md':'cb33b5683b06ae7716e11d3621737a373f7aa7e6e55085dc72c62d2cb7fdad2f',
 'verdict.md':'fb97c6d7d50e6f10c9a2cf90b5bd0c4c343957093fcff863d9124814f7f28188',
 'run_log.md':'c4fba32ebc918c30343fffd220b1a3b16e2346b2fb25a0e6fd584538791c8c28',
 'exchangeable_triangle_sanity.py':'c6b2ab23d3b0acfcdae3f1b5b0760ff24a1018980e0b77109584c4eb44a6d5cc',
 'sanity_results.json':'5f0909aaa4ea2a2934fcd23007837d68eb0daba29fbaf4118ee0998b52c1635e'}
actual = {p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in EXPECTED}
assert actual == EXPECTED, 'Frozen author version drift'

class P:
    def __init__(self, value=0):
        self.c = ({e:Q(v) for e,v in value.items() if v} if isinstance(value,dict)
                  else ({(0,)*6:Q(value)} if value else {}))
    def __add__(self, b):
        b = b if isinstance(b,P) else P(b)
        d = self.c.copy()
        for e,v in b.c.items(): d[e] = d.get(e,0)+v
        return P(d)
    __radd__ = __add__
    def __neg__(self): return P({e:-v for e,v in self.c.items()})
    def __sub__(self,b): return self+-b if isinstance(b,P) else self+(-Q(b))
    def __rsub__(self,b): return -self+b
    def __mul__(self,b):
        b = b if isinstance(b,P) else P(b)
        d = {}
        for e,v in self.c.items():
            for f,w in b.c.items():
                k = tuple(x+y for x,y in zip(e,f)); d[k] = d.get(k,0)+v*w
        return P(d)
    __rmul__ = __mul__
    def __pow__(self,n):
        r = P(1)
        for _ in range(n): r = r*self
        return r
    def __truediv__(self,n): return self*Q(1,n)
    def diff(self,i):
        d = {}
        for e,v in self.c.items():
            if e[i]:
                f=list(e); f[i]-=1; d[tuple(f)]=v*e[i]
        return P(d)
    def ev(self,vs):
        out=0
        for e,v in self.c.items():
            t=v
            for x,n in zip(vs,e): t=t*x**n
            out=out+t
        return out
    def equals(self,b): return not (self-b).c

def variable(i):
    e=[0]*6; e[i]=1; return P({tuple(e):1})

def determinant(a):
    if not a: return 1
    return sum((-1)**j*a[0][j]*determinant([r[:j]+r[j+1:] for r in a[1:]]) for j in range(len(a)))

vs=[variable(i) for i in range(6)]
K=[[vs[0],vs[3],vs[4]],[vs[3],vs[1],vs[5]],[vs[4],vs[5],vs[2]]]
inc=[]
for mask in range(8):
    ix=[i for i in range(3) if mask>>i&1]
    v=determinant([[K[i][j] for j in ix] for i in ix])
    inc.append(v if isinstance(v,P) else P(v))
events=[sum((-1)**((s^t).bit_count())*inc[t] for t in range(8) if s&t==s) for s in range(8)]
assert sum(events).equals(1)
grads=[[p.diff(i) for i in range(6)] for p in events]
hesses=[[[p.diff(i).diff(j) for j in range(6)] for i in range(6)] for p in events]
A,B=vs[:2]
xc=(A+2*B)/3; ac=(A-B)/3
ab_atoms=[p.ev([xc,xc,xc,ac,ac,ac]) for p in events]
layer=[(1-A)*(1-B)**2,(1-B)*(A+2*B-3*A*B)/3,B*(2*A+B-3*A*B)/3,A*B**2]
assert all(ab_atoms[s].equals(layer[s.bit_count()]) for s in range(8))
claimed_da=[-(1-B)**2,(1-B)*(1-3*B)/3,B*(2-3*B)/3,B**2]
claimed_db=[-2*(1-A)*(1-B),(2-4*A-4*B+6*A*B)/3,(2*A+2*B-6*A*B)/3,2*A*B]
claimed_dab=[2*(1-B),(-4+6*B)/3,(2-6*B)/3,2*B]
claimed_dbb=[2*(1-A),(-4+6*A)/3,(2-6*A)/3,2*A]
for k in range(4):
    assert layer[k].diff(0).equals(claimed_da[k])
    assert layer[k].diff(1).equals(claimed_db[k])
    assert layer[k].diff(0).diff(0).equals(0)
    assert layer[k].diff(0).diff(1).equals(claimed_dab[k])
    assert layer[k].diff(1).diff(1).equals(claimed_dbb[k])
x,a=vs[:2]
xa_atoms=[p.ev([x,x,x,a,a,a]) for p in events]
y=1-x
c2=[-3*y,2-3*x,3*x-1,-3*x]
c3=[P(-2),P(2),P(-2),P(2)]
mult=[1,3,3,1]
assert all(xa_atoms[s].equals(x**s.bit_count()*y**(3-s.bit_count())+c2[s.bit_count()]*a**2+c3[s.bit_count()]*a**3) for s in range(8))
assert sum(mult[k]*c2[k]**2*x**(3-k)*y**k for k in range(4)).equals(3*x*y)

def decimal(q): return D(q.numerator)/D(q.denominator) if isinstance(q,Q) else D(q)
def transpose(m): return list(map(list,zip(*m)))
def product(a,b): return [[sum(x*y for x,y in zip(r,c)) for c in transpose(b)] for r in a]
def pullback(mat,columns): return product(product(transpose(columns),mat),columns)
def ldls(a):
    a=[r[:] for r in a]; out=[]
    for k in range(len(a)):
        v=a[k][k]; out.append(v)
        if v<=0: return out
        for i in range(k+1,len(a)):
            for j in range(k+1,len(a)): a[i][j]-=a[i][k]*a[k][j]/v
    return out
def inverse(a):
    n=len(a); m=[r[:]+[D(i==j) for j in range(n)] for i,r in enumerate(a)]
    for j in range(n):
        z=m[j][j]; m[j]=[v/z for v in m[j]]
        for i in range(n):
            if i!=j:
                z=m[i][j]; m[i]=[u-z*v for u,v in zip(m[i],m[j])]
    return [r[n:] for r in m]
def matrix_from_coord(d): return [[d[0],d[3],d[4]],[d[3],d[1],d[5]],[d[4],d[5],d[2]]]
T=transpose([[Q(1)]*3+[Q(0)]*3,[Q(0)]*3+[Q(1)]*3])
U=transpose([[Q(1,3)]*6,[Q(2,3)]*3+[Q(-1,3)]*3])
W=transpose([[Q(1),Q(-1),Q(0),Q(0),Q(0),Q(0)],
             [Q(1),Q(1),Q(-2),Q(0),Q(0),Q(0)],
             [Q(0),Q(0),Q(0),Q(1),Q(-1),Q(0)],
             [Q(0),Q(0),Q(0),Q(1),Q(1),Q(-2)]])

def evaluate(label,alpha,beta):
    assert 0<alpha<1 and 0<beta<1 and alpha!=beta
    xx=(alpha+2*beta)/3; aa=(alpha-beta)/3
    vv=[xx]*3+[aa]*3
    p=[e.ev(vv) for e in events]
    g=[[e.ev(vv) for e in r] for r in grads]
    hh=[[[e.ev(vv) for e in r] for r in h] for h in hesses]
    assert min(p)>0 and sum(p)==1
    vals=[alpha,beta]+[Q(0)]*4
    assert all(p[s]==layer[s.bit_count()].ev(vals) for s in range(8))
    fd=[[sum(g[s][i]*g[s][j]/p[s] for s in range(8)) for j in range(6)] for i in range(6)]
    f=[[decimal(v) for v in r] for r in fd]
    mat=[[f[i][j]+sum(decimal(hh[s][i][j])*decimal(p[s]).ln() for s in range(8)) for j in range(6)] for i in range(6)]
    td=[[decimal(v) for v in r] for r in T]; ud=[[decimal(v) for v in r] for r in U]; wd=[[decimal(v) for v in r] for r in W]
    cab=pullback(mat,ud); cxa=pullback(mat,td); bw=pullback(mat,wd)
    cross=product(product(transpose(td),mat),wd)
    lp=[layer[k].ev(vals) for k in range(4)]
    table=[[sum(mult[k]*(decimal(layer[k].diff(i).ev(vals))*decimal(layer[k].diff(j).ev(vals))/decimal(lp[k])+decimal(layer[k].diff(i).diff(j).ev(vals))*decimal(lp[k]).ln()) for k in range(4)) for j in range(2)] for i in range(2)]
    table_error=max(abs(cab[i][j]-table[i][j]) for i in range(2) for j in range(2))
    cross_error=max(abs(v) for r in cross for v in r)
    ell=decimal(lp[0]*lp[2]/lp[1]**2).ln()
    lam=decimal(lp[3]*lp[1]**3/(lp[0]*lp[2]**3)).ln()
    nalpha=-ell-lam*decimal(alpha); nbeta=-ell-lam*decimal(beta)
    assert min(nalpha,nbeta)>0
    nn=[[(nbeta if i==j else D(0))+(nalpha-nbeta)/3 for j in range(3)] for i in range(3)]
    ni=inverse(nn); delta=nalpha*nbeta**2
    fullbasis=[matrix_from_coord([D(i==j) for j in range(6)]) for i in range(6)]
    eta=[sum(product(ni,b)[i][i] for i in range(3)) for b in fullbasis]
    u8=[[f[i][j]+delta*(sum(product(product(product(ni,fullbasis[i]),ni),fullbasis[j])[k][k] for k in range(3))-eta[i]*eta[j]) for j in range(6)] for i in range(6)]
    u8_error=max(abs(mat[i][j]-u8[i][j]) for i in range(6) for j in range(6))
    determinant_c=determinant(cab); trace_c=cab[0][0]+cab[1][1]
    disc=((cab[0][0]-cab[1][1])**2+4*cab[0][1]**2).sqrt()
    smallest=2*determinant_c/(trace_c+disc)
    assert min(ldls(bw))>0 and len(ldls(bw))==4
    assert cab[0][0]>0 and determinant_c>0
    assert max(table_error,cross_error,u8_error)<D('1e-100')
    return {'label':label,'alpha':str(alpha),'beta':str(beta),'x':str(xx),'a':str(aa),
            'atoms_exact':list(map(str,p)),'Delta_T':str(determinant_c),'smallest_invariant_eigenvalue':str(smallest),
            'N_eigenvalues':[str(nalpha),str(nbeta)],'W_LDL':list(map(str,ldls(bw))),
            'max_identity_error':str(max(table_error,cross_error,u8_error)),
            'Baa_over_a2':str(cxa[1][1]/decimal(aa)**2),'Bxa_over_a3':str(cxa[0][1]/decimal(aa)**3),
            'Baa_leading_expected':str(18/(decimal(xx)**2*(1-decimal(xx))**2)),
            'det_xa_over_a2':str(determinant(cxa)/decimal(aa)**2)}

author=json.loads((ROOT/'sanity_results.json').read_text(encoding='utf-8'))
frozen_scout=author['grid_and_random_scout']
points=[]
for aa,bb in [(Q(1,5),Q(4,5)),(Q(4,5),Q(1,5)),(Q(1,100),Q(99,100)),(Q(99,100),Q(1,100)),(Q(73,100),Q(41,100))]:
    points.append(('base',aa,bb))
warnings=[frozen_scout['best_min_eig']]+frozen_scout['float_cancellation_warning_examples']
for ix,row in enumerate(warnings):
    for interpretation in ['stored_decimal','binary64_exact']:
        convert=(lambda v:Q(str(v))) if interpretation=='stored_decimal' else Q.from_float
        points.append((f'warning_{ix}_{interpretation}',convert(row['alpha']),convert(row['beta'])))
for xx in [Q(1,10),Q(1,5),Q(1,2),Q(4,5),Q(9,10)]:
    for exponent in [5,15]:
        for sign in [-1,1]:
            aa=Q(sign,10**exponent); points.append(('local_taylor',xx+2*aa,xx-aa))
with localcontext() as ctx:
    ctx.prec=150
    results=[evaluate(*point) for point in points]

# Independent outward rational logarithm enclosure, not Decimal rounding.
# On 1<=y<=2 use log y=2 sum t^(2j+1)/(2j+1), t=(y-1)/(y+1)<=1/3.
# Fixed-point interval operations have outward integer rounding; the
# remaining tail after 100 terms is bounded using t<=1/3.
SCALE=10**80
def ceildiv(a,b): return -((-a)//b)
def log_mantissa(y):
    assert 1<=y<=2
    t=(y-1)/(y+1)
    tl=t.numerator*SCALE//t.denominator
    th=ceildiv(t.numerator*SCALE,t.denominator)
    t2l=tl*tl//SCALE; t2h=ceildiv(th*th,SCALE)
    pl,ph=tl,th; sl,sh=0,0
    for j in range(100):
        sl+=2*pl//(2*j+1); sh+=ceildiv(2*ph,2*j+1)
        pl=pl*t2l//SCALE; ph=ceildiv(ph*t2h,SCALE)
    tail=Q(2,1)*Q(1,3)**201/(201*(1-Q(1,9)))
    return Q(sl,SCALE),Q(sh,SCALE)+tail
LOG2=log_mantissa(Q(2))
def log_bounds(q):
    k=0; y=q
    while y<1: y*=2; k-=1
    while y>=2: y/=2; k+=1
    lo,hi=log_mantissa(y)
    return (lo+k*LOG2[0],hi+k*LOG2[1]) if k>=0 else (lo+k*LOG2[1],hi+k*LOG2[0])
def interval_mul(a,b):
    v=[x*y for x in a for y in b]; return min(v),max(v)
def interval_square(a):
    return (Q(0) if a[0]<=0<=a[1] else min(a[0]**2,a[1]**2),max(a[0]**2,a[1]**2))
def certified_warning(label,alpha,beta):
    vals=[alpha,beta]+[Q(0)]*4
    lp=[p.ev(vals) for p in layer]
    logs=[log_bounds(p) for p in lp]
    block=[]
    for i in range(2):
        row=[]
        for j in range(2):
            f=sum(mult[k]*layer[k].diff(i).ev(vals)*layer[k].diff(j).ev(vals)/lp[k] for k in range(4))
            lo,hi=f,f
            for k in range(4):
                coef=mult[k]*layer[k].diff(i).diff(j).ev(vals)
                v=interval_mul((coef,coef),logs[k]); lo+=v[0]; hi+=v[1]
            row.append((lo,hi))
        block.append(row)
    pos=interval_mul(block[0][0],block[1][1]); neg=interval_square(block[0][1])
    bounds=(pos[0]-neg[1],pos[1]-neg[0])
    assert block[0][0][0]>0 and bounds[0]>0
    return {'label':label,'alpha':str(alpha),'beta':str(beta),
            'Delta_T_lower_exact':str(bounds[0]),'Delta_T_upper_exact':str(bounds[1]),
            'Delta_T_lower_decimal':str(decimal(bounds[0])),
            'C_alpha_alpha_lower_exact':str(block[0][0][0]),
            'strict_invariant_positive':'RATIONAL_LOG_INTERVAL_CERTIFICATE'}
interval_warnings=[certified_warning(*p) for p in points if p[0].startswith('warning_')]

# Independently replay only the source proposal/acceptance denominator.
# No cached matrices or source function is used. This is not a replay of
# all 177360 sign calculations, and not a high-precision global scout.
rng=random.Random(20260908)
accepted_grid=sum(abs(i/241-j/241)>=1e-12 for i in range(1,241) for j in range(1,241))
accepted_random=0
for _ in range(120000):
    mode=rng.random()
    if mode<.25:
        bb=rng.random(); dd=(1 if rng.random()<.5 else -1)*10**rng.uniform(-10,-1)
        aa=min(1-1e-15,max(1e-15,bb+dd))
    elif mode<.5:
        aa=10**rng.uniform(-8,-.0001); bb=rng.random()
        if rng.random()<.5: aa=1-aa
    elif mode<.75:
        bb=10**rng.uniform(-8,-.0001); aa=rng.random()
        if rng.random()<.5: bb=1-bb
    else: aa=rng.random(); bb=rng.random()
    accepted_random+=int(0<aa<1 and 0<bb<1 and abs(aa-bb)>=1e-12)
assert accepted_grid==57360 and accepted_random==120000
assert accepted_grid+accepted_random==frozen_scout['checked']==177360
assert {p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in EXPECTED}==EXPECTED
out={'status':'CORRECT_SCOPED_GLOBAL_INCOMPLETE','precision':150,'author_hashes':actual,
     'symbolic_checks':{'exact_atom_polynomials':8,'derivative_table_entries':20,
                        'xa_atom_expansions':8,'quartic_KL_cleared_polynomial_identity':True},
     'denominators':{'base_points':5,'warning_points_two_encodings':12,'local_taylor_points':20,
                     'total_high_precision':len(results),'failures':0,'accepted_grid':accepted_grid,
                     'accepted_random':accepted_random,'full_author_sign_replay':False},
     'source_scout_claim':{'checked':177360,'bad_count':frozen_scout['bad_count'],
                           'warning_count':frozen_scout['float_cancellation_warning_count'],
                           'scope':'source report, with denominator regeneration and six warning cases independently rechecked'},
     'results':results,'rational_warning_certificates':interval_warnings,
     'log_interval_method':{'scale_digits':80,'atanh_terms':100,'normalized_t_bound':'1/3',
                            'warning_encodings_certified':12}}
out['independent_implementation_sha256']=hashlib.sha256((ROOT/'fresh_audit_log.md').read_bytes()).hexdigest()
(ROOT/'fresh_audit_results.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':out['status'],'denominators':out['denominators'],'symbolic_checks':out['symbolic_checks']},indent=2))
```
