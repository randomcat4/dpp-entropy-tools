"""Exact rational/series certificate for one frozen n=11 rank-two PSD ray.

All proof bounds use Fraction, integer Bareiss determinants, and rational log
series remainders. Decimal is used only for optional display/sanity evaluation.
"""
import json, math, os, time
from fractions import Fraction as F
from decimal import Decimal, localcontext
from pathlib import Path

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'results'
GRID=10**24
TERMS=18
U=[-2,1,-3,3,-2,3,2,2,-1,2,3]
V=[-1,3,3,-1,2,3,-3,-2,-3,-1,-2]

def floor_scaled(x): return x.numerator*GRID//x.denominator
def ceil_scaled(x): return -((-x.numerator*GRID)//x.denominator)
def display(x):
    with localcontext() as c:
        c.prec=35; return str(Decimal(x.numerator)/Decimal(x.denominator))

def bareiss(A):
    A=[row[:] for row in A]; n=len(A)
    if n==0: return 1
    sign=1; prev=1
    for k in range(n-1):
        pivot=next((i for i in range(k,n) if A[i][k]),None)
        if pivot is None: return 0
        if pivot!=k: A[k],A[pivot]=A[pivot],A[k]; sign=-sign
        p=A[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                numerator=A[i][j]*p-A[i][k]*A[k][j]
                assert numerator%prev==0
                A[i][j]=numerator//prev
        for i in range(k+1,n): A[i][k]=0
        prev=p
    return sign*A[-1][-1]

def rational_det(A):
    if not A: return F(1)
    den=math.lcm(*(x.denominator for row in A for x in row))
    return F(bareiss([[int(x*den) for x in row] for row in A]),den**len(A))

def matrices(n):
    u,v=U[:n],V[:n]; uu=sum(x*x for x in u); vv=sum(x*x for x in v)
    M=[[F(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        M[i][i]=F(1,3)+F(i+1,3*(n+1))
        for j in range(i+1,n): M[i][j]=M[j][i]=2*((-1)**(i*j+i+j))*F(3+((i+1)*7+(j+1)*11)%5,20*n)
    D=[[F(u[i]*u[j],uu)+F(v[i]*v[j],2*vv) for j in range(n)] for i in range(n)]
    return M,D

def events(M):
    n=len(M); den=math.lcm(*(x.denominator for row in M for x in row)); J=[[int(x*den) for x in row] for row in M]; probs=[]
    for mask in range(1<<n):
        A=[row[:] for row in J]; missing=0
        for i in range(n):
            if not(mask>>i&1): A[i][i]-=den; missing+=1
        probs.append(F((-1)**missing*bareiss(A),den**n))
    return probs

def combine(M,D,t): return [[M[i][j]+t*D[i][j] for j in range(len(M))] for i in range(len(M))]

def exact_ldl(M,m,complement=False):
    n=len(M); A=[[(int(i==j)-M[i][j]) if complement else M[i][j] for j in range(n)] for i in range(n)]
    for i in range(n): A[i][i]-=m
    L=[[F(0) for _ in range(n)] for _ in range(n)]; d=[]
    for j in range(n):
        dj=A[j][j]-sum(L[j][r]**2*d[r] for r in range(j)); assert dj>0
        d.append(dj); L[j][j]=1
        for i in range(j+1,n): L[i][j]=(A[i][j]-sum(L[i][r]*L[j][r]*d[r] for r in range(j)))/dj
    return min(d)

def atanh_log_bounds(z):
    assert 1<=z<=2
    x=(z-1)/(z+1); x2=x*x; power=x; total=F(0)
    for j in range(TERMS): total+=2*power/(2*j+1); power*=x2
    tail=2*power/((2*TERMS+1)*(1-x2))
    return total,total+tail

LOG2=atanh_log_bounds(F(2))
def log_bounds(p):
    assert 0<p<=1
    k=max(0,p.denominator.bit_length()-p.numerator.bit_length()); z=p*(2**k)
    while z<1: k+=1; z*=2
    while z>=2: k-=1; z/=2
    lo,hi=atanh_log_bounds(z)
    # Fixed rational grid prevents denominator growth when summing event bounds.
    return F(floor_scaled(lo-k*LOG2[1]),GRID),F(ceil_scaled(hi-k*LOG2[0]),GRID)

def mobius_gate():
    M,D=matrices(4); result=[]
    for t in (F(-1,100),F(0),F(1,100)):
        K=combine(M,D,t); exact=events(K); moments=[]
        for mask in range(16):
            ids=[i for i in range(4) if mask>>i&1]; moments.append(rational_det([[K[i][j] for j in ids] for i in ids]))
        for i in range(4):
            for mask in range(16):
                if not(mask>>i&1): moments[mask]-=moments[mask|(1<<i)]
        assert moments==exact and sum(exact)==1 and min(exact)>0
        result.append(dict(n=4,step=str(t),events=16,exact_agreement=True))
    return result

def main():
    if OUT.exists(): raise FileExistsError('Existing exact certificate will not be overwritten')
    OUT.mkdir(parents=True); started=time.time(); gate=mobius_gate(); M,D=matrices(11)
    # The proposed margin is checked using exact rational arithmetic, not floats.
    m=F(1,10); pivots=[exact_ldl(M,m),exact_ldl(M,m,True)]
    p=events(M); plus=events(combine(M,D,F(1))); minus=events(combine(M,D,F(-1)))
    # +/-1 are polynomial evaluation nodes, not entropy kernels; probabilities
    # there may be signed. Only the coefficients and the strict center are used.
    a=[(x-y)/2 for x,y in zip(plus,minus)]; b=[(x+y)/2-z for x,y,z in zip(plus,minus,p)]
    assert sum(p)==1 and min(p)>0 and sum(a)==0 and sum(b)==0
    assert any(a) and any(b)
    L2lo=L2hi=L4lo=L4hi=Blo=Bhi=Fisherlo=Fisherhi=C4upper=0
    maxA=max(abs(x)/z for x,z in zip(a,p)); maxB=max(abs(x)/z for x,z in zip(b,p))
    for idx,(prob,alpha,beta) in enumerate(zip(p,a,b)):
        loglo,loghi=log_bounds(prob)
        bloglo,bloghi=(beta*loglo,beta*loghi) if beta>=0 else (beta*loghi,beta*loglo)
        fisher=alpha**2/prob
        L2lo+=floor_scaled(bloglo+fisher/2); L2hi+=ceil_scaled(bloghi+fisher/2)
        Blo+=floor_scaled(bloglo); Bhi+=ceil_scaled(bloghi)
        Fisherlo+=floor_scaled(fisher); Fisherhi+=ceil_scaled(fisher)
        c4=beta**2/(2*prob)-alpha**2*beta/(2*prob**2)+alpha**4/(12*prob**3)
        L4lo+=floor_scaled(c4); L4hi+=ceil_scaled(c4)
        Arel=abs(alpha)/prob; Brel=abs(beta)/prob; L=Arel+2*Brel
        # Uniform |H''''| bound for |t|<=1 and p(t)>=p/2.
        fourth_bound=prob*(24*Brel**2+48*L**2*Brel+16*L**4)
        C4upper+=ceil_scaled(fourth_bound)
        if idx%256==0: print(json.dumps(dict(events=idx,total=len(p),elapsed=time.time()-started)),flush=True)
    l2=F(L2lo,GRID); upper4=F(C4upper,GRID)
    assert l2>0
    radius=F(1,100)
    while not (radius<=1 and radius*maxA<=F(1,4) and radius*maxB<=F(1,4) and radius*F(3,2)<=m/2 and radius**2*upper4<=12*l2): radius/=2
    slope=F(3,2); guaranteed_margin=m-radius*slope
    # Exact sanity at the proved radius; logs below are displays, not proof inputs.
    display_checks=[]
    with localcontext() as ctx:
        ctx.prec=70
        dd=lambda x:Decimal(x.numerator)/Decimal(x.denominator)
        H=lambda q:-sum(dd(z)*dd(z).ln() for z in q)
        H0=H(p)
        for t in (radius/2,radius):
            pm=[z-t*x+t*t*y for z,x,y in zip(p,a,b)]; pp=[z+t*x+t*t*y for z,x,y in zip(p,a,b)]
            assert min(pm)>0 and min(pp)>0 and sum(pm)==sum(pp)==1
            gap=(H(pm)+H(pp))/2-H0
            display_checks.append(dict(step=str(t),decimal_gap=str(gap),analytic_upper_bound=str(-dd(l2*t*t/2))))
    result=dict(status='PROOF_CANDIDATE_PENDING_INDEPENDENT_REVIEW',dimension=11,u=U,v=V,c='1/2',uu=sum(x*x for x in U),vv=sum(x*x for x in V),uv=sum(x*y for x,y in zip(U,V)),direction_rank_exact=2,direction_trace='3/2',base_margin=str(m),base_ldl_minima=[str(x) for x in pivots],event_count=len(p),sum_probabilities=str(sum(p)),sum_a=str(sum(a)),sum_b=str(sum(b)),minimum_center_probability=str(min(p)),log_series_terms=TERMS,rounding_grid=GRID,B_interval=[str(F(Blo,GRID)),str(F(Bhi,GRID))],Fisher_interval=[str(F(Fisherlo,GRID)),str(F(Fisherhi,GRID))],L2_interval=[str(l2),str(F(L2hi,GRID))],L2_interval_decimal=[display(l2),display(F(L2hi,GRID))],L4_interval=[str(F(L4lo,GRID)),str(F(L4hi,GRID))],L4_interval_decimal=[display(F(L4lo,GRID)),display(F(L4hi,GRID))],uniform_fourth_derivative_upper=str(upper4),uniform_fourth_derivative_upper_decimal=display(upper4),max_relative_a=str(maxA),max_relative_b=str(maxB),radius=str(radius),radius_decimal=display(radius),uniform_spectral_margin=str(guaranteed_margin),gap_bound='Delta(t) <= -(L2_lower/2)*t^2 for 0<|t|<=radius',equality_cases='t=0 only on the certified closed interval',mobius_gate=gate,decimal_sanity_only=display_checks,elapsed=time.time()-started,pid=os.getpid(),exit_code=0)
    (OUT/'certificate.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    with (OUT/'exact_coefficients.jsonl').open('w',encoding='utf-8') as fp:
        for i,(z,x,y) in enumerate(zip(p,a,b)): fp.write(json.dumps(dict(mask=i,p=str(z),a=str(x),b=str(y)))+'\n')
    print(json.dumps({k:result[k] for k in ('status','L2_interval_decimal','L4_interval_decimal','radius','uniform_spectral_margin','elapsed','exit_code')}),flush=True)

if __name__=='__main__': main()
