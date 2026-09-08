"""Non-author exact arithmetic checks; never imports author evaluators."""
from fractions import Fraction as F
from decimal import Decimal as D, localcontext
from itertools import permutations
from pathlib import Path
import json,time
BASE=Path(__file__).resolve().parent
ZERO=(F(0),F(0),F(0));ONE=(F(1),F(0),F(0))

def add(a,b):return tuple(x+y for x,y in zip(a,b))
def neg(a):return tuple(-x for x in a)
def mul(a,b):return (a[0]*b[0],a[0]*b[1]+a[1]*b[0],a[0]*b[2]+a[1]*b[1]+a[2]*b[0])
def div(a,b):
    c0=a[0]/b[0];c1=(a[1]-b[1]*c0)/b[0]
    return c0,c1,(a[2]-b[1]*c1-b[2]*c0)/b[0]
def detjet(a):
    n=len(a);out=ZERO
    for p in permutations(range(n)):
        sign=(-1)**sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))
        term=(F(sign),F(0),F(0))
        for i in range(n):term=mul(term,a[i][p[i]])
        out=add(out,term)
    return out
def dec(x):return D(x.numerator)/D(x.denominator)
def covariance(p,x,y):
    ex=sum(a*b for a,b in zip(p,x));ey=sum(a*b for a,b in zip(p,y))
    return sum(a*(b-ex)*(c-ey) for a,b,c in zip(p,x,y))

def case(n):
    beta=[F((-1)**i,i+10) for i in range(n-1)]
    tau=[F(1,4),F(1,3),F(2,5),F(1,2)][:n]
    delta=[F(1,50),F(-1,60),F(1,70),F(-1,80)][:n]
    inv=[div(ONE,(x,d,F(0))) for x,d in zip(tau,delta)]
    L=[[ZERO for _ in range(n)] for _ in range(n)]
    for i in range(n):
        diag=inv[i]
        if i<n-1:diag=add(diag,mul((beta[i]**2,F(0),F(0)),inv[i+1]))
        L[i][i]=add(diag,neg(ONE))
        if i<n-1:L[i][i+1]=L[i+1][i]=mul((-beta[i],F(0),F(0)),inv[i+1])
    weights=[]
    for s in range(1<<n):
        ids=[i for i in range(n) if s>>i&1]
        weights.append(detjet([[L[i][j] for j in ids] for i in ids]))
    assert all(w[0]>0 for w in weights)
    Z=ZERO
    for w in weights:Z=add(Z,w)
    p=[div(w,Z) for w in weights]
    # Separate inclusion-principal-minor route, then Boolean Mobius.
    U=[[F(i==j) for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(i):U[i][j]=beta[i-1]*U[i-1][j]
    K=[[(F(i==j)-sum(U[i][k]*tau[k]*U[j][k] for k in range(n)),
          -sum(U[i][k]*delta[k]*U[j][k] for k in range(n)),F(0)) for j in range(n)] for i in range(n)]
    atoms=[]
    for s in range(1<<n):
        ids=[i for i in range(n) if s>>i&1]
        atoms.append(detjet([[K[i][j] for j in ids] for i in ids]))
    for i in range(n):
        for s in range(1<<n):
            if not s>>i&1:atoms[s]=add(atoms[s],neg(atoms[s|(1<<i)]))
    assert atoms==p
    pp=[dec(x[0]) for x in p]
    ell=[dec(w[0]).ln() for w in weights]
    A=[dec(w[1]/w[0]) for w in weights]
    B=[dec(2*w[2]/w[0]-(w[1]/w[0])**2) for w in weights]
    eell=sum(x*y for x,y in zip(pp,ell));ea=sum(x*y for x,y in zip(pp,A))
    variance=covariance(pp,A,A)
    covellb=covariance(pp,ell,B)
    third=sum(x*(l-eell)*(a-ea)**2 for x,l,a in zip(pp,ell,A))
    direct=-sum(dec(v[1]**2/v[0])+dec(2*v[2])*dec(v[0]).ln() for v in p)
    decomposed=-variance-covellb-third
    acceleration=-sum(dec(2*v[2])*dec(v[0]).ln() for v in p)
    assert abs(direct-decomposed)<D('1e-55')
    assert abs(acceleration+covellb+third)<D('1e-55')
    return {'n':n,'beta':list(map(str,beta)),'tau':list(map(str,tau)),
            'delta':list(map(str,delta)),'exact_Mobius_jet_matches_L_ensemble':True,
            'events':len(p),'variance':variance,'cov_ell_B':covellb,'centered_third':third,
            'H2_direct':direct,'H2_decomposition':decomposed,'residual':-covellb-third,
            'decomposition_abs_error':abs(direct-decomposed),
            'probability_jets':[[str(x) for x in v] for v in p]}

def main():
    start=time.time()
    tau=[F(1,2),F(1,2)];delta=[F(1),F(1)]
    h2=-sum(d*d/(t*(1-t)) for t,d in zip(tau,delta))
    bound=-4*sum(d*d for d in delta)
    assert h2==bound==F(-8)
    with localcontext() as ctx:
        ctx.prec=65
        report={'verdict_literal_Theorem1_strict_bound':'INCORRECT',
                'counterexample':{'n':2,'beta':['0'],'tau':list(map(str,tau)),
                                  'delta':list(map(str,delta)),'H2':str(h2),'bound':str(bound)},
                'decomposition_checks':[case(3),case(4)],'random_draws':0,
                'exit_code':0,'elapsed_seconds':time.time()-start}
    (BASE/'independent_check.json').write_text(json.dumps(report,indent=2,default=str),encoding='utf-8')
    print(json.dumps({'literal_Theorem1':'INCORRECT','decomposition_cases':2,'exit_code':0}))

if __name__=='__main__':main()
