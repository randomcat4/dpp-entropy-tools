"""Four fixed exact-derivative diagnostics; floating logs, not interval certificates."""
import json
import os
import platform
import time
from fractions import Fraction as F
from math import log
from bridge_certificate import certify
from test_bridge_certificate import make_case


def det_inverse(M):
    n=len(M)
    B=[list(row)+[F(int(i==j)) for j in range(n)] for i,row in enumerate(M)]
    det=F(1)
    for j in range(n):
        pivot=next(i for i in range(j,n) if B[i][j])
        if pivot!=j:B[j],B[pivot]=B[pivot],B[j];det=-det
        value=B[j][j];det*=value
        B[j]=[x/value for x in B[j]]
        for i in range(n):
            if i!=j:
                value=B[i][j]
                B[i]=[x-value*y for x,y in zip(B[i],B[j])]
    return det,[row[n:] for row in B]


def derivatives(K,A):
    n=len(K);H2=0.;total=F(0)
    for bits in range(1<<n):
        missing=[i for i in range(n) if not(bits>>i&1)]
        M=[row[:] for row in K]
        for i in missing:M[i][i]-=1
        determinant,inverse=det_inverse(M)
        p=(-1)**len(missing)*determinant
        assert p>0
        Z=[[sum(inverse[i][k]*A[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
        assert sum(Z[i][i] for i in range(n))==0
        p2=p*sum(Z[i][j]*Z[j][i] for i in range(n) for j in range(n))
        H2-=float(p2)*log(float(p));total+=p
    return H2,total


def conditional_formula(K,A):
    n=len(K);result=0.
    for u in range(n):
        for v in range(u+1,n):
            if A[u][v]==0:continue
            R=[i for i in range(n) if i not in (u,v)];U=[u,v]
            e_derivative=0.
            for bits in range(1<<len(R)):
                missing=[j for j in range(len(R)) if not(bits>>j&1)]
                Q=[[K[i][j] for j in R] for i in R]
                for j in missing:Q[j][j]-=1
                determinant,inverse=det_inverse(Q)
                weight=(-1)**len(missing)*determinant
                M=[[K[u0][v0]-sum(K[u0][R[i]]*inverse[i][j]*K[R[j]][v0]
                    for i in range(len(R)) for j in range(len(R))) for v0 in U] for u0 in U]
                a,b=M[0][0],M[1][1];q=K[u][v]**2
                assert M[0][1]==K[u][v]
                p11=a*b-q;p00=(1-a)*(1-b)-q
                p10=a*(1-b)+q;p01=(1-a)*b+q
                assert p11*p00-p10*p01==-q
                e_derivative+=float(weight)*log(float(p11*p00/(p10*p01)))
            result+=2*float(A[u][v]**2)*e_derivative
    return result


start=time.monotonic()
cases=[('two_point',make_case(2,[(0,1)],[(0,1)])),
       ('three_path',make_case(3,[(0,1),(1,2)],[(0,1),(1,2)])),
       ('two_triangles',make_case(6,[(0,1),(1,2),(0,2),(3,4),(4,5),(3,5),(2,3)],[(2,3)])),
       ('diagonal_zero_direction',make_case(3,[],[]))]
results=[]
for name,payload in cases:
    K=[[F(x) for x in row] for row in payload['K']]
    A=[[F(x) for x in row] for row in payload['A']]
    exact=certify(payload)
    direct,mass=derivatives(K,A)
    conditional=conditional_formula(K,A)
    assert abs(direct-conditional)<1e-10 and mass==1
    assert direct<0 if any(x for row in A for x in row) else abs(direct)<1e-12
    results.append({'name':name,'n':len(K),'full_events_diagnostic_only':1<<len(K),
                    'direct_curvature':direct,'bridge_formula_curvature':conditional,
                    'absolute_difference':abs(direct-conditional),'p_prime_exactly_zero':True,
                    'probability_sum_exact':str(mass),'exact_premise_certificate':exact['status']})
print(json.dumps({'status':'DIAGNOSTICS_PASSED_NOT_A_PROOF','pid':os.getpid(),
                  'python':platform.python_version(),'third_party_dependencies':[],
                  'threads':{k:os.environ.get(k) for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']},
                  'elapsed_seconds':time.monotonic()-start,'cases':results},indent=2))
