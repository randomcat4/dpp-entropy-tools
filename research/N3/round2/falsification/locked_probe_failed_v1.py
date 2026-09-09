"""Eight fixed optimizer starts over four exact Lambda-tangent nullspaces."""
import hashlib,json,os,sys,time
from pathlib import Path
from fractions import Fraction as R
import numpy as np
import mpmath as mp
import scipy
from scipy.optimize import minimize
from beta_affine_probe import BASELINE,families,midpoint,feasible,fmt,mm
from beta_root_certificate import event_data

LOCKED_SOURCE='99205d9ac552355c148f011bb053731a8b1349f0'

def exact_objects(K):
    p,J,pairs=event_data(K);assert min(p)>0
    g=[sum(R((-1)**(3-s.bit_count()))*J[s][j]/p[s] for s in range(8)) for j in range(6)]
    F=[[sum(J[s][i]*J[s][j]/p[s] for s in range(8)) for j in range(6)] for i in range(6)]
    pivot=max(range(6),key=lambda i:abs(g[i]));assert g[pivot]!=0
    others=[i for i in range(6) if i!=pivot]
    P=[[R(i==j) if i!=pivot else -g[j]/g[pivot] for j in others] for i in range(6)]
    assert all(sum(g[i]*P[i][j] for i in range(6))==0 for j in range(5))
    Q=[]
    for k in range(3):
        q=[[R(0) for _ in range(6)] for _ in range(6)]
        q[k][k]=1/(K[k][k]*(1-K[k][k]));cond=[]
        other=[i for i in range(3) if i!=k]
        for state in [0,1]:
            idx=[(state<<k)|((b&1)<<other[0])|(((b>>1)&1)<<other[1]) for b in range(4)]
            a,b,c,d=[p[i] for i in idx];mass=a+b+c+d;delta=a*d-b*c
            V=a*d*(a+d)+b*c*(b+c)-4*delta*delta/mass
            W=1/a+1/b+1/c+1/d;residual=W-mass*mass/V
            L=[d*J[idx[0]][j]+a*J[idx[3]][j]-c*J[idx[1]][j]-b*J[idx[2]][j]
               -2*delta*sum(J[i][j] for i in idx)/mass for j in range(6)]
            assert V>0 and residual>=0
            cond.append((mass,L,V,residual))
            for i in range(6):
                for j in range(6):q[i][j]+=L[i]*L[j]/V
        m0,L0,V0,R0=cond[0];m1,L1,V1,R1=cond[1];assert R0+R1>0
        w=[m0*L0[j]/V0-m1*L1[j]/V1 for j in range(6)]
        for i in range(6):
            for j in range(6):q[i][j]+=w[i]*w[j]/(R0+R1)
        Q.append(q)
    return p,J,g,F,Q,P,pivot

def cofactor_matrix(K,p):
    def m(x):return mp.mpf(x.numerator)/x.denominator
    K=mm(K);p=[m(x) for x in p]
    ell=[mp.log(p[0]*p[6]/(p[2]*p[4])),mp.log(p[0]*p[5]/(p[1]*p[4])),mp.log(p[0]*p[3]/(p[1]*p[2]))]
    lam=mp.log(p[7]*p[1]*p[2]*p[4]/(p[0]*p[3]*p[5]*p[6]));N=-mp.diag(ell)-lam*K
    E=[]
    for i,j in [(0,0),(1,1),(2,2),(0,1),(0,2),(1,2)]:
        e=mp.zeros(3);e[i,j]=e[j,i]=1;E.append(e)
    def value(D):
        adj=mp.matrix([[(-1)**(i+j)*mp.det(mp.matrix([[D[r,c] for c in range(3) if c!=i] for r in range(3) if r!=j])) for j in range(3)] for i in range(3)])
        return 2*sum((N*adj)[i,i] for i in range(3))
    C=mp.matrix(6,6)
    for i in range(6):
        C[i,i]=value(E[i])
        for j in range(i):C[i,j]=C[j,i]=(value(E[i]+E[j])-C[i,i]-C[j,j])/2
    return np.array(C.tolist(),dtype=float)

def kernels():
    def mat(rows):return [[R(x,100) for x in row] for row in rows]
    f=next(x for x in families() if x['name']=='rank_one_to_twisted_complement_100')
    L=R(39791754487,17592186044416);U=R(79583508975,35184372088832)
    return [('stationary',mat([[51,24,-24],[24,48,-24],[-24,-24,52]])),
            ('negative_beta_A',f['A']),('root_bracket_midpoint',midpoint(f['A'],f['B'],(L+U)/2)),
            ('main_tangent',mat([[50,4,6],[4,50,8],[6,8,50]]))]

def main():
    start=time.time();mp.mp.dps=100;results=[];total=0
    for name,K in kernels():
        assert feasible(K)
        p,J,g,F,Q,P,pivot=exact_objects(K)
        Pn=np.array(P,dtype=float); U,Rqr=np.linalg.qr(Pn);Cn=cofactor_matrix(K,p)
        matrices=[U.T@(np.array(q,dtype=float)-Cn)@U for q in Q]
        # Exactly two deterministic spectral starts per kernel, eight in total.
        starts=[np.linalg.eigh(sum(matrices)/3)[1][:,0],np.linalg.eigh(matrices[0])[1][:,0]]
        runs=[]
        for sidx,z in enumerate(starts):
            calls=0
            def fun(w):
                nonlocal calls
                calls+=1;return w[-1]
            constraints=[dict(type='eq',fun=lambda w:w[:5]@w[:5]-1,
                              jac=lambda w:np.r_[2*w[:5],0])]
            for M in matrices:
                constraints.append(dict(type='ineq',fun=lambda w,M=M:w[-1]-w[:5]@M@w[:5],
                                        jac=lambda w,M=M:np.r_[-2*M@w[:5],1]))
            w=np.r_[z,max(z@M@z for M in matrices)]
            opt=minimize(fun,w,jac=lambda w:np.r_[np.zeros(5),1],constraints=constraints,
                         method='SLSQP',options=dict(maxiter=160,ftol=1e-12))
            coeff=np.linalg.solve(Rqr,opt.x[:5]);yr=[R(str(float(x))).limit_denominator(10**8) for x in coeff]
            d=[sum(P[i][j]*yr[j] for j in range(5)) for i in range(6)]
            scale=max(abs(x) for x in d);d=[x/scale for x in d]
            assert sum(g[i]*d[i] for i in range(6))==0
            dn=np.array(d,dtype=float);qn=[float(dn@np.array(q,dtype=float)@dn) for q in Q];C=float(dn@Cn@dn)
            runs.append(dict(start=sidx,optimizer_success=bool(opt.success),message=opt.message,objective_calls=calls,
                             rational_direction=[str(x) for x in d],exact_g_dot_D='0',Qlock=qn,C=C,
                             max_gap=max(qn)-C,actual_B=float(dn@np.array(F,dtype=float)@dn)-C))
            total+=calls
        results.append(dict(name=name,K=fmt(K),g=[str(x) for x in g],nullspace_pivot=pivot,runs=runs))
    best=min([dict(kernel=r['name'],K=r['K'],**x) for r in results for x in r['runs']],key=lambda x:x['max_gap'])
    out=dict(status='FLOAT_SCOUT_ONLY',baseline=BASELINE,locked_source=LOCKED_SOURCE,pid=os.getpid(),
             source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),python=sys.version,
             numpy=np.__version__,scipy=scipy.__version__,mpmath=mp.__version__,seed=None,
             kernel_calls=4,optimizer_starts=8,objective_calls=total,rejected=0,results=results,best=best,
             elapsed_seconds=time.time()-start,exit_status=0)
    Path('research/N3/round2/falsification/locked_probe.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['pid','kernel_calls','optimizer_starts','objective_calls','best','elapsed_seconds']}))

if __name__=='__main__':main()
