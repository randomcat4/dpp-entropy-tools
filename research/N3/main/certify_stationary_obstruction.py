"""One-point rigorous enclosure of the exact A-optimizer and its Q_k gaps."""
import certify_score_obstruction as earlier
from fractions import Fraction as Q
from pathlib import Path
import json,os,time,hashlib
g=earlier.g; proj=earlier.proj; HERE=Path(__file__).resolve().parent
S=2**180

class I:
    def __init__(self,x=0,hi=None):
        if hi is not None: self.lo,self.hi=x,hi
        elif isinstance(x,I): self.lo,self.hi=x.lo,x.hi
        else:
            x=Q(x)*S; self.lo=x.__floor__(); self.hi=x.__ceil__()
    def __add__(self,b):
        b=I(b); return I(self.lo+b.lo,self.hi+b.hi)
    __radd__=__add__
    def __neg__(self): return I(-self.hi,-self.lo)
    def __sub__(self,b): return self+-I(b)
    def __rsub__(self,b): return I(b)+-self
    def __mul__(self,b):
        b=I(b); products=[a*c for a in (self.lo,self.hi) for c in (b.lo,b.hi)]
        return I(min(products)//S,-((-max(products))//S))
    __rmul__=__mul__
    def reciprocal(self):
        assert self.lo*self.hi>0, 'zero-containing denominator'
        return I((S*S)//self.hi,-((-S*S)//self.lo))
    def __truediv__(self,b): return self*I(b).reciprocal()
    def __rtruediv__(self,b): return I(b)*self.reciprocal()
    def square(self): return self*self
    def out(self): return earlier.compact(Q(self.lo,S),Q(self.hi,S))

def mm(A,B): return [[sum((A[i][k]*B[k][j] for k in range(len(B))),I()) for j in range(len(B[0]))] for i in range(len(A))]
def tr(A): return sum((A[i][i] for i in range(len(A))),I())
def det(A):
    return A[0][0]*(A[1][1]*A[2][2]-A[1][2]*A[2][1])-A[0][1]*(A[1][0]*A[2][2]-A[1][2]*A[2][0])+A[0][2]*(A[1][0]*A[2][1]-A[1][1]*A[2][0])
def solve(A,b):
    a=[[I(x) for x in row]+[I(b[i])] for i,row in enumerate(A)]; pivots=[]
    for k in range(len(a)):
        pivot=a[k][k]; assert pivot.lo>0; pivots.append(pivot)
        a[k]=[x/pivot for x in a[k]]
        for i in range(k+1,len(a)):
            c=a[i][k]; a[i]=[x-c*y for x,y in zip(a[i],a[k])]
    x=[I() for _ in a]
    for i in reversed(range(len(a))):
        x[i]=(a[i][-1]-sum((a[i][j]*x[j] for j in range(i+1,len(a))),I()))/a[i][i]
    return x,pivots
def inv(A):
    columns=[solve(A,[int(i==j) for i in range(len(A))])[0] for j in range(len(A))]
    return [list(row) for row in zip(*columns)]
def quad(M,d): return sum((d[i]*M[i][j]*d[j] for i in range(len(d)) for j in range(len(d))),I())

def main():
    start=time.time()
    K=[[Q(v,100) for v in row] for row in ((51,24,-24),(24,48,-24),(-24,-24,52))]
    assert g.feasible(K)
    k=[K[i][j] for i,j in g.COORDS]; p=[g.ev(f,k) for f in g.POLYS]
    jac=[[g.ev(f,k) for f in row] for row in g.GRAD]
    Fisher=[[sum(jac[s][i]*jac[s][j]/p[s] for s in range(8)) for j in range(6)] for i in range(6)]
    logs=[]
    for prob in p:
        lo,hi=earlier.log_bounds(prob)
        logs.append(I((lo*S).__floor__(),(hi*S).__ceil__()))
    odds=[logs[0]+logs[3]-logs[1]-logs[2],logs[0]+logs[5]-logs[1]-logs[4],logs[0]+logs[6]-logs[2]-logs[4]]
    lam=logs[7]+logs[1]+logs[2]+logs[4]-logs[0]-logs[3]-logs[5]-logs[6]
    N=[[-lam*K[i][j]-(odds[2-i] if i==j else 0) for j in range(3)] for i in range(3)]
    inverse=inv(N); determinant=det(N); assert determinant.lo>0
    basis=[]
    for i,j in g.COORDS:
        E=[[I() for _ in range(3)] for _ in range(3)]; E[i][j]=E[j][i]=I(1); basis.append(E)
    W=[mm(inverse,E) for E in basis]; eta=[tr(M) for M in W]
    A=[[I(Fisher[i][j])+determinant*tr(mm(W[i],W[j])) for j in range(6)] for i in range(6)]
    d,pivots=solve(A,eta)
    normalizer=sum((a*b for a,b in zip(eta,d)),I()); assert normalizer.lo>0
    D=[[I() for _ in range(3)] for _ in range(3)]
    for v,(i,j) in zip(d,g.COORDS): D[i][j]=D[j][i]=v
    Y=mm(inverse,D)
    C=determinant*(tr(Y).square()-tr(mm(Y,Y)))
    lower=proj.lower_matrices(K); gaps=[quad(M,d)-C for M in lower]
    true_B=quad(Fisher,d)-C; energy=quad(A,d)
    assert all(x.hi<0 for x in gaps), 'stationary shortcut not refuted'
    assert true_B.lo>0 and energy.lo>0
    report=dict(status='EXACT_STATIONARY_SHORTCUT_COUNTEREXAMPLE_NOT_ENTROPY_COUNTEREXAMPLE',
                K=K,p=p,exact_feasibility=True,definition='d=A^-1 eta; D_star=d/(eta^T d)',
                d_intervals=[v.out() for v in d],normalizer_interval=normalizer.out(),
                normalized_D_star_intervals=[(v/normalizer).out() for v in d],
                Q_minus_C_intervals=[v.out() for v in gaps],
                gap_over_A_intervals=[(v/energy).out() for v in gaps],
                true_B_over_A_interval=(true_B/energy).out(),rho_interval=(determinant*normalizer).out(),
                A_elimination_pivot_intervals=[v.out() for v in pivots],
                dyadic_precision_bits=180,interval_method='outward rounded integer arithmetic; rational log bounds',
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                dependencies={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in
                              [HERE/'certify_score_obstruction.py',HERE/'projected_metric_probe.py',HERE/'conditional_score_probe.py',proj.base.DEP,proj.base.DEP.parent/'global_probe.py']},
                pid=os.getpid(),threads=1,seed=None,deterministic=True,executed_centers=1,
                command='python research/N3/main/certify_stationary_obstruction.py',
                elapsed_seconds=time.time()-start,exit_code=0)
    (HERE/'stationary_obstruction_certificate.json').write_text(json.dumps(g.encode(report),indent=2)+'\n')
    print(json.dumps(g.encode({k:v for k,v in report.items() if k not in ('dependencies','p','A_elimination_pivot_intervals')}),indent=2),flush=True)

if __name__=='__main__': main()
