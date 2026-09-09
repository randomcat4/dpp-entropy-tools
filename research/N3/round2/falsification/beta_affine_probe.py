"""Twelve fixed real affine kernel segments; no tolerance is a beta zero."""
import hashlib,json,os,sys,time
from pathlib import Path
from fractions import Fraction as R
import mpmath as mp
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'falsification'))
from unequal_sparse_probe import events,det3,cofactor,PAIRS

BASELINE='e476db1bb056af57e883a47f470ea0f4443c1837'

def matrix(rows):return [[R(str(x)) for x in row] for row in rows]
def midpoint(A,B,t):return [[(1-t)*A[i][j]+t*B[i][j] for j in range(3)] for i in range(3)]
def d3(A):return A[0][0]*(A[1][1]*A[2][2]-A[1][2]*A[2][1])-A[0][1]*(A[1][0]*A[2][2]-A[1][2]*A[2][0])+A[0][2]*(A[1][0]*A[2][1]-A[1][1]*A[2][0])
def feasible(A):
    B=[[R(i==j)-A[i][j] for j in range(3)] for i in range(3)]
    return all(M[0][0]>0 and M[0][0]*M[1][1]-M[0][1]**2>0 and d3(M)>0 for M in [A,B])
def fmt(A):return [[str(x) for x in row] for row in A]
def mm(A,ctx=mp):return ctx.matrix([[ctx.mpf(x.numerator)/x.denominator for x in row] for row in A])

def families():
    out=[]
    def append(name,A,B):
        assert feasible(A) and feasible(B)
        out.append(dict(name=name,A=A,B=B))
    for k in range(3):
        A=matrix([[.25,.013,.021],[.013,.45,.034],[.021,.034,.65]])
        B=midpoint(A,A,R(0)); A[k][k]=R(1,50);B[k][k]=R(49,50)
        append(f'diagonal_sweep_{k}',A,B)
    for sign in [-1,0,1]:
        A=matrix([[.2,.05,.07],[.05,.5,-.14],[.07,-.14,.8]])
        B=matrix([[.2,.05,.07],[.05,.5,.14],[.07,.14,.8]])
        A[0][0]+=R(sign,50);B[2][2]-=R(sign,50)
        append(f'edge_sign_sweep_{sign}',A,B)
    for den in [100,10**4,10**8]:
        e=R(1,den); u=[R(1),R(2),R(3)]; a2=sum(x*x for x in u)
        A=[[(e if i==j else R(0))+R(3,5)*u[i]*u[j]/a2 for j in range(3)] for i in range(3)]
        B=[[R(i==j)-A[i][j] for j in range(3)] for i in range(3)]
        # Conjugating only endpoint B by diag(-1,1,1) breaks complement pairing.
        signs=[-1,1,1]; B=[[B[i][j]*signs[i]*signs[j] for j in range(3)] for i in range(3)]
        append(f'rank_one_to_twisted_complement_{den}',A,B)
    for den in [100,10**4,10**8]:
        e=R(1,den)
        A=matrix([[.31,.09,0],[.09,.46,0],[0,0,.73]])
        B=matrix([[.31,.09,0],[.09,.46,0],[0,0,.73]])
        A[0][2]=A[2][0]=e;A[1][2]=A[2][1]=2*e
        B[0][2]=B[2][0]=-3*e;B[1][2]=B[2][1]=e
        append(f'weak_bridge_rotation_{den}',A,B)
    return out

def data(K,ctx=mp):
    # Rational event/jet data are built before any logarithms.
    p,J=events(K)
    Z=sum(1/x for x in p); s=[(-1)**(3-i.bit_count()) for i in range(8)]
    g=ctx.matrix([sum(s[k]*J[k,j]/p[k] for k in range(8)) for j in range(6)])
    F=J.T*ctx.diag([1/x for x in p])*J; Fpair=F-g*g.T/Z
    ell=[ctx.log(p[0]*p[6]/(p[2]*p[4])),ctx.log(p[0]*p[5]/(p[1]*p[4])),ctx.log(p[0]*p[3]/(p[1]*p[2]))]
    lam=ctx.log(p[7]*p[1]*p[2]*p[4]/(p[0]*p[3]*p[5]*p[6]))
    N=-ctx.diag(ell)-lam*K; d=det3(N); adj=ctx.matrix([[cofactor(N,j,i) for j in range(3)] for i in range(3)])
    E=[]
    for i,j in PAIRS:
        e=ctx.zeros(3); e[i,j]=1;e[j,i]=1;E.append(e)
    ae=ctx.matrix([sum((adj*e)[i,i] for i in range(3)) for e in E])
    T=ctx.matrix(6,6)
    for i in range(6):
        for j in range(6):
            z=adj*E[i]*adj*E[j];T[i,j]=sum(z[k,k] for k in range(3))
    Htilde=d*Fpair+T; h=ctx.lu_solve(Htilde,ae)
    beta=(g.T*h)[0]/ctx.sqrt(Z); dalpha=(ae.T*h)[0]
    gamma=d*(g.T*ctx.lu_solve(Htilde,g))[0]/Z
    rho=dalpha-d*beta**2/(1+gamma)
    return beta,dalpha,rho

def main():
    start=time.time();mp.mp.dps=160; fs=families();rows=[];brackets=[];reject=0
    for f in fs:
        previous=None
        for num in range(9):
            t=R(num,8);A=midpoint(f['A'],f['B'],t);assert feasible(A)
            # Exact graph check, including zero edges.
            edges=[(i,j) for i,j in [(0,1),(0,2),(1,2)] if A[i][j]!=0]
            connected=len(edges)>=2
            if not connected:
                rows.append(dict(family=f['name'],t=str(t),rejection='disconnected',K=fmt(A)));reject+=1;previous=None;continue
            beta,da,rho=data(mm(A))
            row=dict(family=f['name'],t=str(t),K=fmt(A),beta=mp.nstr(beta,70),dalpha=mp.nstr(da,70),rho=mp.nstr(rho,70))
            rows.append(row)
            if previous and mp.mpf(previous['beta'])*beta<0:brackets.append([previous,row])
            previous=row
    accepted=[r for r in rows if 'beta' in r]
    result=dict(status='INCOMPLETE',baseline=BASELINE,source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                pid=os.getpid(),python=sys.version,mpmath=mp.__version__,dps=160,seed=None,
                thread_env={k:os.environ.get(k) for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']},
                families=[dict(name=f['name'],A=fmt(f['A']),B=fmt(f['B'])) for f in fs],
                attempted=len(rows),accepted=len(accepted),rejected=reject,rows=rows,sign_change_brackets=brackets,
                minimum_beta=min(accepted,key=lambda r:mp.mpf(r['beta'])),
                max_dalpha=max(accepted,key=lambda r:mp.mpf(r['dalpha'])),
                negative_count=sum(mp.mpf(r['beta'])<0 for r in accepted),
                elapsed_seconds=time.time()-start,exit_status=0)
    Path('research/N3/round2/falsification/affine_probe.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['pid','attempted','accepted','rejected','negative_count','minimum_beta','max_dalpha','elapsed_seconds']}))

if __name__=='__main__':main()
