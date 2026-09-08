from fractions import Fraction as F
from decimal import Decimal, getcontext
from itertools import combinations
getcontext().prec = 80

def matmul(A,B):
    return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]

def transpose(A):
    return [list(row) for row in zip(*A)]

def eye(n):
    return [[F(int(i==j),1) for j in range(n)] for i in range(n)]

def add(A,B):
    return [[A[i][j]+B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def scale(c,A):
    return [[c*x for x in row] for row in A]

def submatrix(A, ids):
    return [[A[i][j] for j in ids] for i in ids]

def det(A):
    n=len(A)
    if n==0: return F(1)
    M=[row[:] for row in A]
    sign=1
    prev=F(1)
    for k in range(n-1):
        piv=None
        for i in range(k,n):
            if M[i][k]!=0:
                piv=i; break
        if piv is None: return F(0)
        if piv!=k:
            M[k],M[piv]=M[piv],M[k]
            sign*=-1
        pivot=M[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                M[i][j]=(M[i][j]*pivot-M[i][k]*M[k][j])/prev
        prev=pivot
        for i in range(k+1,n):
            M[i][k]=F(0)
    return sign*M[n-1][n-1]

def kernel(t,x,sigma):
    c=(1-t*t)/(1+t*t)
    s=2*t/(1+t*t)
    Q=eye(4)
    Q[1][1]=c; Q[1][2]=-s; Q[2][1]=s; Q[2][2]=c
    A=matmul(Q, [[F(1),F(0)],[F(1),F(0)],[F(0),F(1)],[F(0),F(1)]])
    AAT=matmul(A,transpose(A))
    X=[[F(0),x],[x,F(0)]]
    AXAT=matmul(matmul(A,X),transpose(A))
    return add(add(scale(t,eye(4)), scale((1-2*t)/2,AAT)), scale(sigma*t/2,AXAT))

def principal_minors(K):
    out={}
    for mask in range(16):
        ids=[i for i in range(4) if mask>>i & 1]
        out[mask]=det(submatrix(K,ids))
    return out

def full_law(K):
    minors=principal_minors(K)
    masses={}
    for mask in range(16):
        total=F(0)
        for other,val in minors.items():
            if other & mask == mask:
                total += ((-1)**((other^mask).bit_count()))*val
        masses[mask]=total
    return masses,minors

def dec(q):
    return Decimal(q.numerator)/Decimal(q.denominator)

def entropy(law):
    total=Decimal(0)
    for p in law.values():
        if p:
            dp=dec(p)
            total -= dp*dp.ln()
    return total

def check(t,x):
    Ks={sig: kernel(t,x,sig) for sig in (-1,0,1)}
    assert Ks[0] == [[(Ks[-1][i][j]+Ks[1][i][j])/2 for j in range(4)] for i in range(4)]
    rows=[]
    for sig,K in Ks.items():
        law,minors=full_law(K)
        comp=full_law([[F(int(i==j),1)-K[i][j] for j in range(4)] for i in range(4)])[1]
        assert sum(law.values()) == 1
        assert min(law.values()) > 0
        assert all(v>0 for m,v in minors.items() if m)
        assert all(v>0 for m,v in comp.items() if m)
        rows.append((sig, min(law.values())))
    laws={sig: full_law(Ks[sig])[0] for sig in (-1,0,1)}
    delta=(entropy(laws[-1])+entropy(laws[1]))/2-entropy(laws[0])
    return rows, delta

for t,x in [(F(1,8),F(1,2)),(F(1,16),F(1,4)),(F(1,64),F(1,4)),(F(1,16),F(1,2)),(F(1,64),F(1,2)),(F(1,16),F(3,4)),(F(1,64),F(3,4))]:
    rows,delta=check(t,x)
    print(f"t={t} x={x} min_masses={rows} delta={delta}")
