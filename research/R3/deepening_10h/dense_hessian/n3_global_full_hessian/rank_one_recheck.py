"""Explicit n3 rank-one Schur reduction and bounded boundary asymptotic checks."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import importlib.util,json,hashlib,time
from fractions import Fraction as F
from decimal import Decimal,localcontext
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('own_global_probe',HERE/'global_probe.py')
g=importlib.util.module_from_spec(spec); spec.loader.exec_module(g)

def solve(M,b):
    n=len(M); a=[list(row)+[b[i]] for i,row in enumerate(M)]
    for k in range(n):
        pivot=max(range(k,n),key=lambda i:abs(a[i][k])); assert a[pivot][k]!=0
        a[k],a[pivot]=a[pivot],a[k]; v=a[k][k]
        for j in range(k,n+1): a[k][j]/=v
        for i in range(n):
            if i==k: continue
            v=a[i][k]
            for j in range(k,n+1): a[i][j]-=v*a[k][j]
    return [row[-1] for row in a]
def inverse(M):
    n=len(M); cols=[solve(M,[Decimal(int(i==j)) for i in range(n)]) for j in range(n)]
    return [[cols[j][i] for j in range(n)] for i in range(n)]
def mm(A,B): return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def trace(A): return sum(A[i][i] for i in range(len(A)))
def det3(A):
    a,b,c=A[0]; d,e,f=A[1]; h,i,j=A[2]
    return a*e*j+b*f*h+c*d*i-c*e*h-b*d*j-a*f*i

def reduction(K,prec=120):
    result=g.evaluate(K,prec); p=result['p']; k=[K[i][j] for i,j in g.COORDS]
    for i,j in g.COORDS[3:]:
        m=3-i-j; a=K[i][j]; bc=K[i][m]*K[j][m]; z=K[m][m]
        assert p[0]*p[(1<<i)|(1<<j)]-p[1<<i]*p[1<<j]==-((1-z)*a+bc)**2
        assert p[1<<m]*p[7]-p[(1<<i)|(1<<m)]*p[(1<<j)|(1<<m)]==-(z*a-bc)**2
    with localcontext() as ctx:
        ctx.prec=prec
        L=result['odds']; T=result['triple']; C=result['C']
        N=[[-T*g.dec(K[i][j]) for j in range(3)] for i in range(3)]
        for i in range(3): N[i][i]-=L[2-i]
        inv=inverse(N); det=det3(N); assert det>0
        basis=[]
        for i,j in g.COORDS:
            E=[[Decimal(0)]*3 for _ in range(3)]; E[i][j]=E[j][i]=Decimal(1); basis.append(E)
        W=[mm(inv,E) for E in basis]; eta=[trace(M) for M in W]
        grad=[[g.ev(poly,k) for poly in row] for row in g.GRAD]
        Fisher=[[g.dec(sum(grad[s][i]*grad[s][j]/p[s] for s in range(8))) for j in range(6)] for i in range(6)]
        A=[[Fisher[i][j]+det*trace(mm(W[i],W[j])) for j in range(6)] for i in range(6)]
        rebuilt=[[A[i][j]-det*eta[i]*eta[j] for j in range(6)] for i in range(6)]
        error=max(abs(rebuilt[i][j]-result['B'][i][j]) for i in range(6) for j in range(6))
        scale=max(abs(v) for row in A for v in row); assert error/max(Decimal(1),scale)<Decimal(10)**(-prec+15)
        solution=solve(A,eta); rho=det*sum(a*b for a,b in zip(eta,solution))
        D=[[Decimal(0)]*3 for _ in range(3)]
        for value,(i,j) in zip(solution,g.COORDS): D[i][j]=D[j][i]=value
        return dict(rho=rho,deficit=1-rho,N=N,N_determinant=det,eta=eta,A=A,schur_direction=D,
            rebuild_error=error,rebuild_relative_error=error/max(Decimal(1),scale),precision=prec,min_atom=min(p),K=K,
            conditional_odds_identities_exact=True)

def main():
    start=time.time(); scouts=json.loads((HERE/'scout_results.json').read_text())
    connected=[r for r in scouts['ledger'] if len(set(r['component_labels']))==1]
    selected=sorted(connected,key=lambda r:r['normalized_min_B'])[:4]
    checks=[]
    for r in selected:
        K=[[F(v) for v in row] for row in r['K']]; item=reduction(K)
        item['scout_index']=r['index']; checks.append(item)
    scalar_ledger=[]
    for r in connected:
        K=[[F(v) for v in row] for row in r['K']]; item=reduction(K,100)
        scalar_ledger.append(dict(scout_index=r['index'],rho=item['rho'],deficit=item['deficit'],rebuild_relative_error=item['rebuild_relative_error']))
    u=[F(1,3),F(2,3),F(2,3)]
    U=[[a*b for b in u] for a in u]; boundary=[]
    for theta in (F(1,10),F(1,2),F(9,10)):
        for exponent in (2,4,8,16,32,64):
            eps=F(1,10**exponent)
            K=[[eps*F(i==j)+(theta-eps)*U[i][j] for j in range(3)] for i in range(3)]
            item=reduction(K,max(120,3*exponent+80))
            with localcontext() as ctx:
                ctx.prec=item['precision']; L=-g.dec(eps).ln()
                scaled=item['deficit']*L
            boundary.append(dict(theta=theta,epsilon=eps,u=u,rho=item['rho'],deficit=item['deficit'],deficit_times_log=scaled,
                predicted_limit=1/theta,precision=item['precision'],rebuild_relative_error=item['rebuild_relative_error']))
    multirate=[]; Q=g.quat((1,2,3,4))
    for powers in ((1,2),(1,3),(2,3)):
        for exponent in (2,4,8,16):
            eps=F(1,10**exponent); lam=(eps**powers[0],eps**powers[1],F(1,2))
            item=reduction(g.spectral(Q,lam),max(120,3*max(powers)*exponent+80))
            multirate.append(dict(epsilon=eps,powers=powers,eigenvalues=lam,quaternion=(1,2,3,4),rho=item['rho'],deficit=item['deficit'],precision=item['precision'],rebuild_relative_error=item['rebuild_relative_error']))
    report=dict(status='SCOUT_ONLY_NO_GLOBAL_INFERENCE',frozen_point_checks=checks,boundary_checks=boundary,multirate_boundary_checks=multirate,scalar_ledger=scalar_ledger,
        all_frozen_rho_below_one=all(v['rho']<1 for v in checks),all_boundary_rho_below_one=all(v['rho']<1 for v in boundary+multirate),all_scout_rho_below_one=all(v['rho']<1 for v in scalar_ledger),
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),dependency_sha256=hashlib.sha256((HERE/'global_probe.py').read_bytes()).hexdigest(),
        elapsed_seconds=time.time()-start,exit_code=0)
    (HERE/'rank_one_results.json').write_text(json.dumps(g.encode(report),indent=2)+'\n')
    print('frozen',[(v['scout_index'],str(v['rho'])) for v in checks])
    print('boundary limit checks',[(str(v['theta']),str(v['epsilon']),str(v['deficit_times_log'])) for v in boundary])
    print('elapsed',report['elapsed_seconds'])
    print('scalar count/max',len(scalar_ledger),max(v['rho'] for v in scalar_ledger),'multirate count/max',len(multirate),max(v['rho'] for v in multirate))
if __name__=='__main__': main()
