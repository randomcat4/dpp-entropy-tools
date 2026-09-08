"""Independent exact polynomial Mobius/orthogonal-minor checks; no author imports."""
from fractions import Fraction as F
from itertools import permutations,combinations
from pathlib import Path
import json,time
BASE=Path(__file__).resolve().parent

def multiply(a,b):
    out=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return out

def determinant_polynomial(matrix,n):
    m=len(matrix);out=[F(0)]*(n+1)
    for perm in permutations(range(m)):
        sign=(-1)**sum(perm[i]>perm[j] for i in range(m) for j in range(i+1,m))
        prod=[F(sign)]
        for i in range(m):prod=multiply(prod,matrix[i][perm[i]])
        for i,x in enumerate(prod):out[i]+=x
    return out

def model(Q,lam,v):
    n=len(lam)
    assert [[sum(Q[i][k]*Q[j][k] for k in range(n)) for j in range(n)] for i in range(n)]==[[F(i==j) for j in range(n)] for i in range(n)]
    K=[[[sum(Q[i][k]*lam[k]*Q[j][k] for k in range(n)),
          sum(Q[i][k]*v[k]*Q[j][k] for k in range(n))] for j in range(n)] for i in range(n)]
    moments=[]
    for s in range(1<<n):
        ids=[i for i in range(n) if s>>i&1]
        moments.append(determinant_polynomial([[K[i][j] for j in ids] for i in ids],n))
    atoms=[row[:] for row in moments]
    for i in range(n):
        for s in range(1<<n):
            if not s>>i&1:atoms[s]=[x-y for x,y in zip(atoms[s],atoms[s|(1<<i)])]
    assert [sum(p[k] for p in atoms) for k in range(n+1)]==[F(1)]+[F(0)]*n
    assert min(p[0] for p in atoms)>0
    # Independent Cauchy-Binet spectral exact-event formula, all cardinality layers.
    spectral=[]
    for s in range(1<<n):
        ids=[i for i in range(n) if s>>i&1];total=[F(0)]*(n+1)
        for js in combinations(range(n),len(ids)):
            sub=[[[Q[i][j]] for j in js] for i in ids]
            minor=determinant_polynomial(sub,n)[0]
            weight=[minor*minor]
            for j in range(n):
                weight=multiply(weight,[lam[j],v[j]] if j in js else [1-lam[j],-v[j]])
            total=[x+y for x,y in zip(total,weight)]
        spectral.append(total)
    assert atoms==spectral
    return atoms

def log_bounds(x,N=24):
    assert x>0
    def atanh_series(z):
        u=(z-1)/(z+1)
        lo=2*sum(u**(2*k+1)/F(2*k+1) for k in range(N))
        tail=2*u**(2*N+1)/(F(2*N+1)*(1-u*u))
        return lo,lo+tail
    k=0
    while x<1:x*=2;k+=1
    assert x<2
    lo,hi=atanh_series(x);l2,h2=atanh_series(F(2))
    return lo-k*h2,hi-k*l2

def rounded_interval(lo,hi,denominator=10**10):
    lower=(lo.numerator*denominator)//lo.denominator
    upper=-((-hi.numerator*denominator)//hi.denominator)
    return [str(F(lower,denominator)),str(F(upper,denominator))]

def curvature_certificate(atoms):
    fisher=sum(p[1]**2/p[0] for p in atoms)
    lo=hi=-fisher
    for p in atoms:
        a,b=log_bounds(p[0]); coefficient=-2*p[2]
        lo+=coefficient*(a if coefficient>=0 else b)
        hi+=coefficient*(b if coefficient>=0 else a)
    assert hi<0
    return {'Fisher_exact':str(fisher),'H2_rational_interval':rounded_interval(lo,hi),
            'H2_interval_float':[float(lo),float(hi)],'log_series_terms':24,
            'strict_negative_certified':True}

def main():
    start=time.time();rows=[]
    cases=[
      ('rotation',[[F(3,5),F(-4,5)],[F(4,5),F(3,5)]],[F(1,4),F(2,3)],[F(1,5),F(3,7)]),
      ('reflection',[[F(3,5),F(4,5)],[F(4,5),F(-3,5)]],[F(1,4),F(2,3)],[F(1,5),F(3,7)]),
      ('identity_rank1',[[F(1),F(0)],[F(0),F(1)]],[F(2,5),F(4,7)],[F(1,3),F(0)]),
      ('swap_rank1',[[F(0),F(1)],[F(1),F(0)]],[F(5,8),F(1,6)],[F(0),F(2,5)]),
      ('repeated_spectrum',[[F(3,5),F(-4,5)],[F(4,5),F(3,5)]],[F(1,2),F(1,2)],[F(1),F(1)]),
    ]
    for label,Q,lam,v in cases:
        p=model(Q,lam,v)
        assert 2*p[1][2]==2*p[2][2]==-2*v[0]*v[1]
        rows.append({'label':label,'atoms_polynomial':[[str(x) for x in r] for r in p],
                     'lambda':list(map(str,lam)),'v':list(map(str,v)),**curvature_certificate(p)})
    Q=[[F(6,7),F(-2,7),F(-3,7)], [F(-2,7),F(3,7),F(-6,7)], [F(-3,7),F(-6,7),F(-2,7)]]
    lam=[F(3,4),F(1,2),F(1,2)];v=[F(1,100),F(1),F(1)]
    p=model(Q,lam,v)
    assert 2*p[1][2]==F(2339,2450)
    brackets=[]
    for a in range(3):
        b,c=[j for j in range(3) if j!=a]
        brackets.append(lam[a]*v[b]*v[c]-v[a]*v[b]*(1-lam[c])-v[a]*v[c]*(1-lam[b]))
    blocker={'Q':[[str(x) for x in r] for r in Q],'lambda':list(map(str,lam)),
             'v':list(map(str,v)),'raw_brackets':list(map(str,brackets)),
             'twice_brackets':list(map(str,[2*x for x in brackets])),
             'singleton_second_derivatives':[str(2*p[1<<i][2]) for i in range(3)],
             'all_atoms_polynomial':[[str(x) for x in r] for r in p],
             'feasible_interval':['-1/10','1/10'],'uniform_spectral_margin':'249/1000',
             **curvature_certificate(p)}
    for t in (F(-1,10),F(1,10)):
        assert min(min(l+t*r,1-l-t*r) for l,r in zip(lam,v))>=F(249,1000)
    report={'status':'EXACT_CHECK_PASS','n2_cases':rows,'n3_blocker':blocker,
            'event_polynomials':5*4+8,'random_draws':0,'exit_code':0,
            'elapsed_seconds':time.time()-start}
    (BASE/'fresh_exact_check.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps({'status':report['status'],'n3':blocker['singleton_second_derivatives'],
                      'n3_H2_interval':blocker['H2_rational_interval'],'seconds':report['elapsed_seconds']}))

if __name__=='__main__':main()
