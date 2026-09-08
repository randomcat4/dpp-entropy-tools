"""Read recorded diagnostic directions; no new candidate generation."""
from probe import *

def exact_rank(A):
    A=[row[:] for row in A]; row=0
    for col in range(len(A[0])):
        pivot=next((i for i in range(row,len(A)) if A[i][col]),None)
        if pivot is None: continue
        A[row],A[pivot]=A[pivot],A[row]; value=A[row][col]
        for j in range(col,len(A[0])): A[row][j]/=value
        for i in range(row+1,len(A)):
            value=A[i][col]
            for j in range(col,len(A[0])): A[i][j]-=value*A[row][j]
        row+=1
    return row

data=json.loads((OUT/'mi_hessian_diagnostic.json').read_text(encoding='utf-8')); rows=[]
for r in data['rows']:
    n=r['n']; na=n//2; M=baseline(n,F(r['gamma'])); D=[[F(x,r['direction_denominator']) for x in row] for row in r['direction_numerators']]; t=F(r['step']); E=Events(n)
    proportional=all(D[i][j]*M[0][0]==M[i][j]*D[0][0] for i in range(n) for j in range(n))
    rank=exact_rank(D)
    if rank<2 or proportional: raise AssertionError('Known-direction exclusion failed')
    k=arr(M); d=arr(D); alpha=float(np.sum(k*d)/np.sum(k*k)); mobs=[]
    if n<=8:
        for sign in (-1,1):
            K=arr(combine(M,D,sign*t)); mobs.append(float(max(abs(E.evaluate(K)-E.mobius(K)))))
    rows.append(dict(n=n,gamma=r['gamma'],exact_rational_direction_rank=rank,exact_thinning_proportionality=proportional,relative_distance_from_radial_direction=float(np.linalg.norm(d-alpha*k)/np.linalg.norm(d)),direction_norm_A=float(np.linalg.norm(d[:na,:na])),direction_norm_B=float(np.linalg.norm(d[na:,na:])),direction_norm_X=float(np.linalg.norm(d[:na,na:])),endpoint_mobius_errors=mobs))
(OUT/'diagnostic_validation.json').write_text(json.dumps(dict(rows=rows,endpoint_mobius_checks=sum(len(r['endpoint_mobius_errors']) for r in rows),max_endpoint_mobius_error=max(v for r in rows for v in r['endpoint_mobius_errors']),exit_code=0),indent=2),encoding='utf-8')
print(json.dumps({'verified_directions':len(rows),'endpoint_mobius_checks':sum(len(r['endpoint_mobius_errors']) for r in rows),'max_error':max(v for r in rows for v in r['endpoint_mobius_errors'])}))
