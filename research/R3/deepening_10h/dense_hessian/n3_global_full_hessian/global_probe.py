"""Bounded rational structured n=3 full-Hessian scout; no research-module imports."""
import os,sys
os.environ['OPENBLAS_NUM_THREADS']='1'
sys.set_int_max_str_digits(0)
from fractions import Fraction as F
from decimal import Decimal,localcontext
from itertools import permutations,product
from pathlib import Path
import json,time,hashlib
import numpy as np

HERE=Path(__file__).resolve().parent; COORDS=((0,0),(1,1),(2,2),(0,1),(0,2),(1,2)); ZERO=(0,)*6

def put(p,e,c):
    p[e]=p.get(e,F(0))+c
    if not p[e]: del p[e]
def term(indices,c=1):
    e=[0]*6
    for i in indices: e[i]+=1
    return {tuple(e):F(c)}
def combine(*items):
    out={}
    for p,c in items:
        for e,v in p.items(): put(out,e,v*c)
    return out
def derivative(p,i):
    out={}
    for e,c in p.items():
        if e[i]:
            ne=list(e); ne[i]-=1; put(out,tuple(ne),c*e[i])
    return out
def ev(p,k):
    total=F(0)
    for e,c in p.items():
        for v,power in zip(k,e):
            if power: c*=v**power
        total+=c
    return total

def atoms_polys():
    d=combine((term((0,1,2)),1),(term((3,4,5)),2),(term((0,5,5)),-1),(term((1,4,4)),-1),(term((2,3,3)),-1))
    inc={0:term(()) ,1:term((0,)),2:term((1,)),4:term((2,)),3:combine((term((0,1)),1),(term((3,3)),-1)),5:combine((term((0,2)),1),(term((4,4)),-1)),6:combine((term((1,2)),1),(term((5,5)),-1)),7:d}
    return [combine(*[(inc[t],(-1)**(t.bit_count()-s.bit_count())) for t in range(8) if t&s==s]) for s in range(8)]
POLYS=atoms_polys(); GRAD=[[derivative(p,i) for i in range(6)] for p in POLYS]; HESS=[[[derivative(g,j) for j in range(6)] for g in row] for row in GRAD]

def dec(q): return Decimal(q.numerator)/Decimal(q.denominator)
def eye(): return [[F(int(i==j)) for j in range(3)] for i in range(3)]
def ldl(M):
    L=[[F(int(i==j)) for j in range(3)] for i in range(3)]; d=[]
    for i in range(3):
        p=M[i][i]-sum(L[i][k]**2*d[k] for k in range(i))
        if p<=0: return None
        d.append(p)
        for j in range(i+1,3): L[j][i]=(M[j][i]-sum(L[j][k]*L[i][k]*d[k] for k in range(i)))/p
    return d
def feasible(K): return ldl(K) is not None and ldl([[F(i==j)-K[i][j] for j in range(3)] for i in range(3)]) is not None
def quat(q):
    a,b,c,d=map(F,q); n=a*a+b*b+c*c+d*d
    Q=[[a*a+b*b-c*c-d*d,2*(b*c-a*d),2*(b*d+a*c)], [2*(b*c+a*d),a*a-b*b+c*c-d*d,2*(c*d-a*b)], [2*(b*d-a*c),2*(c*d+a*b),a*a-b*b-c*c+d*d]]
    Q=[[v/n for v in row] for row in Q]
    assert [[sum(Q[i][k]*Q[j][k] for k in range(3)) for j in range(3)] for i in range(3)]==eye()
    return Q
def spectral(Q,lam): return [[sum(Q[i][k]*lam[k]*Q[j][k] for k in range(3)) for j in range(3)] for i in range(3)]
def ray(X,A,s): return [[X[i][j]+s*A[i][j] for j in range(3)] for i in range(3)]
def ray_limit(X,A):
    lo=F(0); hi=F(1)
    while feasible(ray(X,A,hi)): hi*=2
    for _ in range(32):
        mid=(lo+hi)/2
        if feasible(ray(X,A,mid)): lo=mid
        else: hi=mid
    assert lo>0
    return lo,hi
def components(K):
    comp=[-1]*3; count=0
    for root in range(3):
        if comp[root]>=0: continue
        todo=[root]; comp[root]=count
        while todo:
            i=todo.pop()
            for j in range(3):
                if i!=j and K[i][j] and comp[j]<0: comp[j]=count; todo.append(j)
        count+=1
    return comp

def evaluate(K,prec=80):
    k=[K[i][j] for i,j in COORDS]; p=[ev(poly,k) for poly in POLYS]
    assert min(p)>0 and sum(p)==1
    g=[[ev(poly,k) for poly in row] for row in GRAD]
    h=[[[ev(poly,k) for poly in row] for row in mat] for mat in HESS]
    assert all(sum(g[s][i] for s in range(8))==0 for i in range(6))
    with localcontext() as ctx:
        ctx.prec=prec; logs=[dec(v).ln() for v in p]
        B=[[Decimal(0)]*6 for _ in range(6)]
        for i in range(6):
            for j in range(i,6):
                fisher=sum(g[s][i]*g[s][j]/p[s] for s in range(8))
                value=dec(fisher)+sum(dec(h[s][i][j])*logs[s] for s in range(8))
                B[i][j]=B[j][i]=value
        odds=[logs[0]+logs[3]-logs[1]-logs[2],logs[0]+logs[5]-logs[1]-logs[4],logs[0]+logs[6]-logs[2]-logs[4]]
        triple=logs[7]+logs[1]+logs[2]+logs[4]-logs[0]-logs[3]-logs[5]-logs[6]
        C=[odds[i]+dec(k[2-i])*triple for i in range(3)]
        comp=components(K); active=[i for i,(a,b) in enumerate(COORDS) if comp[a]==comp[b]]
        flat=[i for i in range(6) if i not in active]
        flatmax=max((abs(B[i][j]) for i in flat for j in range(6)),default=Decimal(0))
        assert flatmax<Decimal('1e-55')
        diag=[B[i][i] for i in active]
        if min(diag)<=0:
            return dict(p=p,B=B,active=active,odds=odds,triple=triple,C=C,negative_diagonal=True,score=-1e100,flatmax=flatmax)
        scales=[v.sqrt() for v in diag]
        corr=np.array([[float(B[i][j]/scales[a]/scales[b]) for b,j in enumerate(active)] for a,i in enumerate(active)])
        vals,vecs=np.linalg.eigh(corr)
        direction=[F(0)]*6
        for a,i in enumerate(active): direction[i]=F(float(vecs[a,0]/float(scales[a])))
        normal=max(map(abs,direction)); direction=[v/normal for v in direction]
        acc=np.array([[float((-2*C[i] if i==j else 2*triple*dec(k[5-i-j]))) for j in range(3)] for i in range(3)])
        # For i!=j, k[5-i-j] gives c,b,a for pairs (0,1),(0,2),(1,2)?
        # Correct mapping is explicitly overwritten to avoid index convention ambiguity.
        acc[0,1]=acc[1,0]=float(2*triple*dec(k[5])); acc[0,2]=acc[2,0]=float(2*triple*dec(k[4])); acc[1,2]=acc[2,1]=float(2*triple*dec(k[3]))
        return dict(p=p,B=B,active=active,odds=odds,triple=triple,C=C,negative_diagonal=False,score=float(vals[0]),direction=direction,
            flatmax=flatmax,acceleration_offdiag_min_eigenvalue=float(np.linalg.eigvalsh(acc)[0]))

def cases():
    qs=[(1,2,3,4),(3,1,2,2),(5,1,1,2),(2,0,1,3),(1,1,1,0),(1,0,0,0)]
    for delta in (F(1,20),F(1,1000),F(1,1000000)):
        profiles=set(product((delta,1-delta),repeat=3))
        profiles.update(permutations((delta,F(1,4),F(3,4))))
        profiles.update(permutations((delta,delta,F(1,2))))
        profiles.update(permutations((1-delta,1-delta,F(1,2))))
        for q in qs:
            Q=quat(q)
            for lam in sorted(profiles): yield dict(family='rational_spectral',quaternion=q,eigenvalues=lam),spectral(Q,lam)
    diagonals=[(F(1,2),)*3,(F(1,5),F(2,5),F(7,10)),(F(1,10),F(1,10),F(9,10)),(F(1,100),F(1,2),F(99,100)),(F(1,3),F(17,50),F(7,20))]
    patterns=[(1,1,0),(1,0,2),(1,1,-1),(1,2,3),(1,2,-3)]
    for x in diagonals:
        X=[[x[i] if i==j else F(0) for j in range(3)] for i in range(3)]
        for edges in patterns:
            A=[[F(0)]*3 for _ in range(3)]
            for val,(i,j) in zip(edges,COORDS[3:]): A[i][j]=A[j][i]=F(val)
            lo,hi=ray_limit(X,A)
            for ratio in (F(1,100),F(1,10),F(1,2),F(9,10),F(99,100),F(9999,10000)):
                yield dict(family='boundary_ray',diagonal=x,pattern=edges,boundary_bracket=(lo,hi),boundary_fraction=ratio),ray(X,A,ratio*lo)

def encode(o):
    if isinstance(o,(F,Decimal)): return str(o)
    if isinstance(o,dict): return {str(k):encode(v) for k,v in o.items()}
    if isinstance(o,(list,tuple)): return [encode(v) for v in o]
    return o
def main():
    start=time.time(); ledger=[]; frozen=[]; failures=[]; worst=None; accworst=None
    for idx,(params,K) in enumerate(cases()):
        assert idx<1000 and feasible(K)
        result=evaluate(K); record=dict(index=idx,parameters=params,K=K,component_labels=components(K),min_atom=min(result['p']),
            normalized_min_B=result['score'],triple_log_odds=result['triple'],acceleration_offdiag_min=result.get('acceleration_offdiag_min_eigenvalue'),status='SCOUT')
        if worst is None or result['score']<worst['normalized_min_B']: worst=record
        if result.get('acceleration_offdiag_min_eigenvalue') is not None and (accworst is None or result['acceleration_offdiag_min_eigenvalue']<accworst['acceleration_offdiag_min']): accworst=record
        if result['score']<-1e-8:
            record['status']='FLOAT_CANDIDATE'; frozen.append(dict(record=record,details=result))
        ledger.append(record)
        if idx%100==0: print('processed',idx+1,'worst normalized',worst['normalized_min_B'],'candidates',len(frozen),flush=True)
    report=dict(status='SCOUT_ONLY' if not frozen else 'FLOAT_CANDIDATES_PENDING_RIGOROUS_RECHECK',ledger=ledger,candidates=frozen,
        worst=worst,worst_offdiag_acceleration=accworst,failures=failures,total=len(ledger),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),elapsed_seconds=time.time()-start,exit_code=0)
    (HERE/'scout_results.json').write_text(json.dumps(encode(report),indent=2)+'\n')
    print('done',len(ledger),'candidates',len(frozen),'elapsed',report['elapsed_seconds'])
if __name__=='__main__': main()
