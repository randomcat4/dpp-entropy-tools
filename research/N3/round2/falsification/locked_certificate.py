"""One rational Lambda-tangent obstruction; retain exact full event Fisher."""
import hashlib,json,os,sys,time
from pathlib import Path
from fractions import Fraction as R
import mpmath as mp
from locked_probe import BASELINE,LOCKED_SOURCE,exact_objects,kernels,feasible,fmt
from beta_root_certificate import I,logi,serial,cof

def quad(M,d):return sum(d[i]*M[i][j]*d[j] for i in range(6) for j in range(6))

def main():
    start=time.time();mp.mp.dps=100
    K=next(K for name,K in kernels() if name=='negative_beta_A')
    p,J,g,F,Q,P,pivot=exact_objects(K);assert pivot==0
    # Fixed thousandth rounding of five scout coordinates, then exact projection.
    d=[R(0),-R(89,100),-R(1),-R(371,1000),-R(1,100),R(3,125)]
    d[0]=-sum(g[i]*d[i] for i in range(1,6))/g[0]
    assert sum(g[i]*d[i] for i in range(6))==0
    D=[[d[0],d[3],d[4]],[d[3],d[1],d[5]],[d[4],d[5],d[2]]]
    adj=[[cof(D,j,i) for j in range(3)] for i in range(3)]
    q=[quad(q,d) for q in Q];f=quad(F,d);assert all(f>=x for x in q)
    ell=[logi(I(p[0]*p[6]/(p[2]*p[4]))),logi(I(p[0]*p[5]/(p[1]*p[4]))),logi(I(p[0]*p[3]/(p[1]*p[2])))]
    lam=logi(I(p[7]*p[1]*p[2]*p[4]/(p[0]*p[3]*p[5]*p[6])))
    trKadj=sum(K[i][j]*adj[j][i] for i in range(3) for j in range(3))
    C=-2*sum(ell[i]*adj[i][i] for i in range(3))-2*lam*trKadj
    gap=I(max(q))-C;actual=I(f)-C
    assert gap.hi<0 and actual.lo>0
    odds=[]
    for k in range(3):
        other=[i for i in range(3) if i!=k];ev=[]
        for state in [0,1]:
            idx=[(state<<k)|((b&1)<<other[0])|(((b>>1)&1)<<other[1]) for b in range(4)]
            dp=[sum(J[i][j]*d[j] for j in range(6)) for i in idx]
            ev.append(sum(sign*dd/p[i] for sign,dd,i in zip([1,-1,-1,1],dp,idx)))
        assert ev[0]==ev[1];odds.append([str(x) for x in ev])
    t=R(1,1000);endpoints=[[[K[i][j]+sign*t*D[i][j] for j in range(3)] for i in range(3)] for sign in [-1,1]]
    assert all(feasible(M) for M in endpoints)
    out=dict(status='DISPROVED_LOCKED_DOMINANCE_ONLY',baseline=BASELINE,locked_source=LOCKED_SOURCE,pid=os.getpid(),
             source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),python=sys.version,mpmath=mp.__version__,
             thread_env={k:os.environ.get(k) for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']},
             seed=None,kernel_calls=1,direction_calls=1,rejected=0,K=fmt(K),D=fmt(D),direction=[str(x) for x in d],
             exact_g=[str(x) for x in g],exact_g_dot_D='0',locked_odds_derivatives=odds,
             Qlock=[str(x) for x in q],Qlock_approx=[mp.nstr(mp.mpf(x.numerator)/x.denominator,40) for x in q],
             F_exact=str(f),F_approx=mp.nstr(mp.mpf(f.numerator)/f.denominator,40),
             C=serial(C),max_Qlock_minus_C=serial(gap),actual_B=serial(actual),
             feasible_step=str(t),endpoints=[fmt(M) for M in endpoints],
             interval_bits=240,log_series_terms=80,elapsed_seconds=time.time()-start,exit_status=0)
    Path('research/N3/round2/falsification/locked_certificate.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['status','pid','direction','Qlock_approx','F_approx','C','max_Qlock_minus_C','actual_B','elapsed_seconds']}))

if __name__=='__main__':main()
