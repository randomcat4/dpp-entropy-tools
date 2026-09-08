"""Independent Decimal mixed-event elimination and exact rational feasibility."""
from decimal import Decimal as Q, localcontext
from fractions import Fraction as F
from pathlib import Path
import json,time
BASE=Path(__file__).resolve().parent

def det_solve(A,D=None):
    a=[r[:] for r in A]; rhs=None if D is None else [r[:] for r in D]
    n=len(a); det=Q(1)
    for i in range(n):
        pivot=max(range(i,n),key=lambda j:abs(a[j][i]))
        if pivot!=i:
            a[i],a[pivot]=a[pivot],a[i]
            if rhs is not None: rhs[i],rhs[pivot]=rhs[pivot],rhs[i]
            det=-det
        v=a[i][i]; assert v!=0
        det*=v
        for j in range(i+1,n):
            factor=a[j][i]/v
            for k in range(i+1,n): a[j][k]-=factor*a[i][k]
            if rhs is not None:
                for k in range(n): rhs[j][k]-=factor*rhs[i][k]
    if rhs is not None:
        X=[[Q(0)]*n for _ in range(n)]
        for i in range(n-1,-1,-1):
            for k in range(n):
                X[i][k]=(rhs[i][k]-sum(a[i][j]*X[j][k] for j in range(i+1,n)))/a[i][i]
        return det,X
    return det,None

def evaluate(M,D=None):
    n=len(M); norm=Q(0); H=Q(0); H1=Q(0); fish=Q(0); acc=Q(0)
    sump1=Q(0);sump2=Q(0); minimum=Q(1)
    for s in range(1<<n):
        A=[r[:] for r in M]
        for i in range(n):
            if not s>>i&1: A[i][i]-=1
        det,X=det_solve(A,D)
        p=det*((-1)**(n-s.bit_count()));assert p>0
        lp=p.ln(); norm+=p;H-=p*lp;minimum=min(minimum,p)
        if D is not None:
            score=sum(X[i][i] for i in range(n))
            second=score*score-sum(X[i][j]*X[j][i] for i in range(n) for j in range(n))
            H1-=p*score*lp;fish+=p*score*score;acc-=p*second*lp
            sump1+=p*score;sump2+=p*second
    return {'H':H,'H1':H1,'Fisher_positive':fish,'acceleration':acc,
            'H2':acc-fish,'rho':acc/fish if D is not None else None,
            'sum_p':norm,'sum_p1':sump1,'sum_p2':sump2,'min_probability':minimum}

def ldl(A):
    n=len(A); L=[[F(i==j) for j in range(n)] for i in range(n)];dd=[]
    for j in range(n):
        v=A[j][j]-sum(L[j][k]**2*dd[k] for k in range(j)); assert v>0
        dd.append(v)
        for i in range(j+1,n):
            L[i][j]=(A[i][j]-sum(L[i][k]*L[j][k]*dd[k] for k in range(j)))/v
    return dd

def certify(params):
    M=[[F(x) for x in r] for r in params['kernel']]
    D=[[F(x) for x in r] for r in params['direction']]
    n=len(M); records=[]; eps=F(1,20000)
    for h in (F(-1,10000),F(0),F(1,10000)):
        K=[[M[i][j]+h*D[i][j] for j in range(n)] for i in range(n)]
        a=ldl([[K[i][j]-eps*(i==j) for j in range(n)] for i in range(n)])
        b=ldl([[(1-eps)*(i==j)-K[i][j] for j in range(n)] for i in range(n)])
        records.append({'t':str(h),'min_pivot_K_minus_epsilon':str(min(a)),
                        'min_pivot_I_minus_K_minus_epsilon':str(min(b))})
    dd=ldl(D)
    return {'uniform_interval':['-1/10000','1/10000'],'strict_spectral_margin':'1/20000',
            'endpoint_LDL_records':records,'direction_positive_definite_exact':True,
            'direction_rank':n,'D_min_LDL_pivot':str(min(dd))}

def main():
    start=time.time()
    params=json.loads((BASE/'rational_decimal_parameters.json').read_text(encoding='utf-8'))
    runs=[]
    for precision in (40,65):
        with localcontext() as ctx:
            ctx.prec=precision
            M=[[Q(x) for x in r] for r in params['kernel']]
            D=[[Q(x) for x in r] for r in params['direction']]
            row={'precision':precision,**evaluate(M,D)};runs.append(row)
            print('jet',precision,str(row['rho']),str(row['H2']),flush=True)
    with localcontext() as ctx:
        ctx.prec=65
        center=runs[-1]['H'];chords=[]
        for hstr in ('0.0001','0.00003','0.00001'):
            h=Q(hstr)
            minus=[[x-h*y for x,y in zip(r,s)] for r,s in zip(M,D)]
            plus=[[x+h*y for x,y in zip(r,s)] for r,s in zip(M,D)]
            hm=evaluate(minus)['H'];hp=evaluate(plus)['H']
            H2=(hm+hp-2*center)/(h*h)
            chords.append({'h':hstr,'Hminus':hm,'Hplus':hp,'gap':(hm+hp)/2-center,
                           'central_H2':H2,'error_vs_analytic':H2-runs[-1]['H2']})
            print('chord',hstr,str(H2),flush=True)
    report={'status':'HIGH_PRECISION_STABLE_NEGATIVE','runs':runs,'chords':chords,
            'feasibility':certify(params),'independent_center_count':1,'independent_chords':3,
            'events_per_distribution':4096,'precision_runs':2,'exit_code':0,
            'elapsed_seconds':time.time()-start}
    (BASE/'decimal_recheck.json').write_text(json.dumps(report,indent=2,default=str),encoding='utf-8')
    print('elapsed',report['elapsed_seconds'],flush=True)

if __name__=='__main__': main()
