"""Independent S5 audit: multivariate cubic atoms, no author-module import.

Only stdlib. A different logarithm enclosure uses the unscaled negative atanh
series at each probability. Author data are read only for post-hoc comparison.
"""
from fractions import Fraction as F
from decimal import Decimal, localcontext
from pathlib import Path
from itertools import combinations
import hashlib
import json
import sys
import time
sys.set_int_max_str_digits(0)
HERE=Path(__file__).resolve().parent
AUTHOR=HERE.parent
N=6
zero=(0,)*N
coords=((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))
files=('frozen_problem.md','analysis.md','verdict.md','run_log.md','full_psd_hessian.py','hessian_scout.json')
def hashes(): return {name:hashlib.sha256((AUTHOR/name).read_bytes()).hexdigest() for name in files}
def add(*polys):
    result={}
    for p in polys:
        for k,v in p.items(): result[k]=result.get(k,F(0))+v
    return {k:v for k,v in result.items() if v}
def scale(c,p): return {k:c*v for k,v in p.items() if c*v}
def mul(a,b):
    result={}
    for e,x in a.items():
        for f,y in b.items():
            k=tuple(i+j for i,j in zip(e,f)); result[k]=result.get(k,F(0))+x*y
    return {k:v for k,v in result.items() if v}
def var(i,c):
    e=list(zero); e[i]=1
    return {zero:c,tuple(e):F(1)}
def dec(x): return Decimal(x.numerator)/Decimal(x.denominator)
def compact(bounds,places=28):
    a,b=bounds; den=10**places
    return F((a*den).__floor__(),den),F((b*den).__ceil__(),den)
def log_interval(p):
    assert 0<p<1
    z=(1-p)/(1+p)
    partial=2*sum(z**(2*k+1)/F(2*k+1) for k in range(128))
    tail=2*z**257/(257*(1-z*z))
    return compact((-partial-tail,-partial))
def linear_interval(terms):
    lo=hi=F(0)
    for weight,(a,b) in terms:
        lo+=weight*(a if weight>=0 else b); hi+=weight*(b if weight>=0 else a)
    return lo,hi
def matrix_product(a,b): return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def det3(a):
    return a[0][0]*a[1][1]*a[2][2]+2*a[0][1]*a[0][2]*a[1][2]-a[0][0]*a[1][2]**2-a[1][1]*a[0][2]**2-a[2][2]*a[0][1]**2
def principal(a):
    return [a[i][i] for i in range(3)]+[a[i][i]*a[j][j]-a[i][j]**2 for i,j in combinations(range(3),2)]+[det3(a)]
def serial(obj):
    if isinstance(obj,F): return str(obj)
    if isinstance(obj,Decimal): return str(obj)
    if isinstance(obj,(list,tuple)): return [serial(x) for x in obj]
    if isinstance(obj,dict): return {k:serial(v) for k,v in obj.items()}
    return obj
def main():
    start=time.time(); frozen=hashes()
    w=(1,2,-3); U=[[F(1,3)]*3 for _ in range(3)]
    V=[[F(i*j,14) for j in w] for i in w]
    W=[[F(i==j)-U[i][j]-V[i][j] for j in range(3)] for i in range(3)]
    frame=(U,V,W); theta=(F(1,5),F(7,10),F(71,100)); rates=(F(1,5),F(1,3),F(2,3))
    K=[[sum(theta[a]*frame[a][i][j] for a in range(3)) for j in range(3)] for i in range(3)]
    D=[[sum(rates[a]*frame[a][i][j] for a in range(3)) for j in range(3)] for i in range(3)]
    for i,a in enumerate(frame):
        assert sum(a[j][j] for j in range(3))==1
        for j,b in enumerate(frame): assert matrix_product(a,b)==(a if i==j else [[F(0)]*3 for _ in range(3)])
    a,b,c,u,v,wpoly=[var(index,K[i][j]) for index,(i,j) in enumerate(coords)]
    inclusion=[{zero:F(1)},a,b,add(mul(a,b),scale(-1,mul(u,u))),c,
               add(mul(a,c),scale(-1,mul(v,v))),add(mul(b,c),scale(-1,mul(wpoly,wpoly))),
               add(mul(mul(a,b),c),scale(2,mul(mul(u,v),wpoly)),scale(-1,mul(a,mul(wpoly,wpoly))),
                   scale(-1,mul(b,mul(v,v))),scale(-1,mul(c,mul(u,u))))]
    atoms=[]
    for mask in range(8):
        atoms.append(add(*(scale((-1)**(sup.bit_count()-mask.bit_count()),inclusion[sup]) for sup in range(8) if sup&mask==mask)))
    assert add(*atoms)=={zero:F(1)}
    p=[atom.get(zero,F(0)) for atom in atoms]
    assert min(p)>0
    grad=[]; jets=[]
    for atom in atoms:
        g=[]; h=[]
        for i in range(N):
            e=list(zero); e[i]=1; g.append(atom.get(tuple(e),F(0)))
            row=[]
            for j in range(N):
                e=list(zero); e[i]+=1; e[j]+=1
                row.append(atom.get(tuple(e),F(0))*(2 if i==j else 1))
            h.append(row)
        grad.append(g); jets.append(h)
    li=[log_interval(x) for x in p]
    B=[]
    for i in range(N):
        row=[]
        for j in range(N):
            rational=sum(g[i]*g[j]/prob for g,prob in zip(grad,p))
            lo,hi=linear_interval([(h[i][j],log) for h,log in zip(jets,li)])
            row.append(compact((rational+lo,rational+hi)))
        B.append(row)
    margins=[B[i][i][0]-sum(max(abs(B[i][j][0]),abs(B[i][j][1])) for j in range(N) if j!=i) for i in range(N)]
    assert min(margins)>F(172,100)
    author=json.loads((AUTHOR/'hessian_scout.json').read_text())
    assert K==[[F(x) for x in row] for row in author['K_star']]
    assert p==[F(x) for x in author['base_atoms']]
    xd=[D[i][j] for i,j in coords]
    dinterval=linear_interval([(-xd[i]*xd[j],B[i][j]) for i in range(N) for j in range(N)])
    with localcontext() as ctx:
        ctx.prec=90
        H=[[ -sum(dec(g[i]*g[j]/prob)+dec(h[i][j])*dec(prob).ln() for g,h,prob in zip(grad,jets,p)) for j in range(N)] for i in range(N)]
        matrix_error=max(abs(H[i][j]-Decimal(author['entropy_hessian_matrix_decimal'][i][j])) for i in range(N) for j in range(N))
        assert matrix_error<Decimal('1e-80')
        h2=sum(dec(xd[i]*xd[j])*H[i][j] for i in range(N) for j in range(N))
        assert abs(h2-Decimal(author['commuting_D_star_H2']))<Decimal('1e-80')
        best=[[F(x) for x in row] for row in author['rationalized_best_direction_den_le_2000']]
        assert best==list(map(list,zip(*best)))
        minors=principal(best); assert min(minors)>0
        xb=[best[i][j] for i,j in coords]; norm=sum(x*x for row in best for x in row)
        bestinterval=linear_interval([(-xb[i]*xb[j]/norm,B[i][j]) for i in range(N) for j in range(N)])
        bestval=sum(dec(xb[i]*xb[j]/norm)*H[i][j] for i in range(N) for j in range(N))
        assert abs(bestval-Decimal(author['rationalized_best_H2_per_frob2']))<Decimal('1e-80')
        # Concrete Frobenius-gradient discrepancy at D=I/3.
        identity_coordinates=[F(1,3)]*3+[F(0)]*3
        coord_gradient=[2*sum(H[i][j]*dec(identity_coordinates[j]) for j in range(N)) for i in range(N)]
        scout_gradient_error=[str(coord_gradient[i]/2) for i in range(3,6)]
        report=dict(status='INDEPENDENT_CHECK_COMPLETE',author_hashes_before=frozen,
            coordinate_convention='x=(D11,D22,D33,D12,D13,D23); offdiagonal variable changes BOTH symmetric entries by x, no sqrt(2)',
            K=K,D_star=D,spectral_margin=min(min(x,1-x) for x in theta),atoms=p,
            atom_multivariate_polynomials=[[[list(e),c] for e,c in sorted(atom.items())] for atom in atoms],
            atom_gradients=grad,atom_hessians=jets,log_intervals=li,minus_entropy_hessian_intervals=B,
            gershgorin_row_margins=margins,gershgorin_margins_decimal=[str(dec(x)) for x in margins],
            rational_common_margin=F(172,100),decimal_matrix_error=matrix_error,D_star_H2_interval=dinterval,
            D_star_H2_decimal=h2,D_star_frob2=sum(x*x for row in D for x in row),
            rationalized_scout_direction=best,rationalized_scout_psd_minors=minors,
            rationalized_scout_normalized_H2_interval=bestinterval,rationalized_scout_normalized_H2=bestval,
            scout_frobenius_gradient_offdiagonal_error_at_I_over_3=scout_gradient_error,
            scope=dict(exact_atoms=8,variables=6,atom_first_partials=48,atom_second_partials=288,hessian_entries=36,log_terms=128,
                       replayed_random_search=False,optimization_claim='SCOUT_ONLY_WITH_GRADIENT_METRIC_DEFECT'),
            author_hashes_after=hashes(),elapsed_seconds=time.time()-start,exit_code=0)
    assert report['author_hashes_after']==frozen, 'author version drift'
    report['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (HERE/'independent_results.json').write_text(json.dumps(serial(report),indent=2)+'\n')
    print(json.dumps(serial({k:report[k] for k in ('gershgorin_margins_decimal','D_star_H2_decimal','decimal_matrix_error','rationalized_scout_normalized_H2','elapsed_seconds','exit_code')}),indent=2))
if __name__=='__main__': main()
