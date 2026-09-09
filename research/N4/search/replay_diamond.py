"""80-digit author replay of the strongest gain and smallest full curvature."""
import json,os,time,hashlib,argparse
from pathlib import Path
import mpmath as mp
mp.mp.dps=80
root=Path(__file__).parent
parser=argparse.ArgumentParser();parser.add_argument('--batch',default='batch2');parser.add_argument('--indices',default='0,22');args=parser.parse_args()
def mat(x):return mp.matrix([[mp.mpf(float(v)) for v in row] for row in x])
def tr(M):return sum(M[i,i] for i in range(M.rows))
def Hmat(K,basis):
    m=len(basis);H=mp.matrix(m);F=mp.matrix(m);A=mp.matrix(m)
    for s in range(16):
        M=K.copy()
        for i in range(4):M[i,i]-=1-((s>>i)&1)
        p=(-1)**(4-s.bit_count())*mp.det(M);assert p>0
        X=[M**-1*B for B in basis];g=[tr(Y) for Y in X]
        for i in range(m):
            for j in range(m):
                F[i,j]-=p*g[i]*g[j];A[i,j]-=p*mp.log(p)*(g[i]*g[j]-tr(X[i]*X[j]))
    return F+A,F,A
def entropy(K):
    value=mp.mpf(0)
    for s in range(16):
        M=K.copy()
        for i in range(4):M[i,i]-=1-((s>>i)&1)
        p=(-1)**(4-s.bit_count())*mp.det(M);assert p>0;value-=p*mp.log(p)
    return value
def invsqrt(M):
    e,Q=mp.eigsy(M);assert min(e)>0
    return Q*mp.diag([1/mp.sqrt(x) for x in e])*Q.T,e
def strings(M):return [[str(M[i,j]) for j in range(M.cols)] for i in range(M.rows)]
basis=[]
for i,j in ((0,2),(1,2),(0,3),(1,3)):
    B=mp.matrix(4);B[i,j]=B[j,i]=1;basis.append(B)
records=[json.loads(line) for line in (root/args.batch/'cases.jsonl').read_text().splitlines()]
results=[];start=time.time()
for index in map(int,args.indices.split(',')):
    rec=records[index];K=mat(rec['K']);H,F,A=Hmat(K,basis)
    L=H[:2,:2];R=H[2:,2:];C=H[:2,2:];Wl,el=invsqrt(-L);Wr,er=invsqrt(-R)
    W=Wl*C*Wr;gain=mp.sqrt(max(mp.eigsy(W.T*W,eigvals_only=True)))
    dr=next(d for d in rec['directions'] if d['name']=='full_top');D=mat(dr['D']);HD,FD,AD=Hmat(K,[D]);h0=entropy(K)
    chords=[]
    for c in dr['chords']:
        t=mp.mpf(float(c['t']));chords.append({'t':str(t),'Delta':str((entropy(K+t*D)+entropy(K-t*D))/2-h0)})
    results.append({'index':index,'cross_gain':str(gain),'single_column_defect3':[str(x) for x in el],'single_column_defect4':[str(x) for x in er],'restricted_Hessian':strings(H),'full_top_direction_curvature':str(HD[0,0]),'full_top_chords':chords})
report={'status':'AUTHOR_HIGH_PRECISION_CHECK_ONLY','pid':os.getpid(),'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'precision':80,'mpmath':mp.__version__,'binary64_exact_inputs':True,'restricted_Hessian_calls':len(results),'directional_curvature_calls':len(results),'entropy_calls':7*len(results),'event_evaluations':144*len(results),'results':results,'elapsed_seconds':time.time()-start,'exit_code':0}
(root/args.batch/'selected_replay.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
