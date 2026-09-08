"""Independent exact-event and layer checks; no author curvature imports.

Author simplex function is loaded only for its explicit singular-matrix unit
test, not for the event/entropy calculations.
"""
import ast
import hashlib
import json
import math
import os
from decimal import Decimal, localcontext
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path

for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key]='1'
import numpy as np
HERE=Path(__file__).resolve().parent
AUTHOR=HERE.parent

def eye(n): return [[F(i==j) for j in range(n)] for i in range(n)]
def transpose(a): return [list(row) for row in zip(*a)]
def product(a,b): return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def inverse(a):
    n=len(a); b=[row[:]+unit for row,unit in zip(a,eye(n))]
    for j in range(n):
        pivot=next(i for i in range(j,n) if b[i][j])
        b[j],b[pivot]=b[pivot],b[j]
        scale=b[j][j]; b[j]=[x/scale for x in b[j]]
        for i in range(n):
            if i!=j:
                scale=b[i][j]; b[i]=[x-scale*y for x,y in zip(b[i],b[j])]
    return [row[n:] for row in b]

def rational_orthogonal(q):
    q=[[F(str(x)) for x in row] for row in q]; unit=eye(3)
    left=[[q[i][j]-unit[i][j] for j in range(3)] for i in range(3)]
    right=[[q[i][j]+unit[i][j] for j in range(3)] for i in range(3)]
    a=product(left,inverse(right))
    skew=[[(a[i][j]-a[j][i])/2 for j in range(3)] for i in range(3)]
    q=product([[unit[i][j]+skew[i][j] for j in range(3)] for i in range(3)],
              inverse([[unit[i][j]-skew[i][j] for j in range(3)] for i in range(3)]))
    assert product(transpose(q),q)==unit
    return q

def poly_mul(a,b):
    c=[F(0)]*4
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            if i+j<4: c[i+j]+=x*y
    return c

def poly_det(a):
    n=len(a); result=[F(0)]*4
    for perm in permutations(range(n)):
        sign=(-1)**sum(perm[i]>perm[j] for i in range(n) for j in range(i+1,n))
        term=[F(sign),F(0),F(0),F(0)]
        for i in range(n): term=poly_mul(term,a[i][perm[i]])
        result=[x+y for x,y in zip(result,term)]
    return result

def event_polynomials(q,theta,v):
    k=[[[sum(q[a][i]*q[b][i]*theta[i] for i in range(3)),
          sum(q[a][i]*q[b][i]*v[i] for i in range(3)),F(0),F(0)]
         for b in range(3)] for a in range(3)]
    probabilities=[]
    for mask in range(8):
        indices=[i for i in range(3) if mask>>i&1]
        probabilities.append(poly_det([[k[i][j] for j in indices] for i in indices]))
    for i in range(3):
        for mask in range(8):
            if not mask>>i&1:
                probabilities[mask]=[x-y for x,y in zip(probabilities[mask],probabilities[mask|1<<i])]
    channel=[[F(0)]*4 for _ in range(8)]
    raw=[]
    for mask in range(8):
        term=[F(1),F(0),F(0),F(0)]
        for i in range(3):
            term=poly_mul(term,[theta[i],v[i]] if mask>>i&1 else [1-theta[i],-v[i]])
        raw.append(term)
    channel[0]=raw[0]; channel[7]=raw[7]
    for a in range(3):
        channel[1<<a]=[sum(q[a][i]**2*raw[1<<i][j] for i in range(3)) for j in range(4)]
        channel[7^(1<<a)]=[sum(q[a][i]**2*raw[7^(1<<i)][j] for i in range(3)) for j in range(4)]
    assert probabilities==channel
    assert [sum(row[j] for row in probabilities) for j in range(4)]==[1,0,0,0]
    assert min(row[0] for row in probabilities)>0
    return probabilities

def dec(x): return Decimal(x.numerator)/Decimal(x.denominator)

def log_bounds(x,terms=8):
    """Exact rational bounds, using range reduction and positive atanh tail."""
    assert x>0
    exponent=0
    while x<1: x*=2; exponent-=1
    while x>=2: x/=2; exponent+=1
    def series(z):
        lo=2*sum(z**(2*k+1)/F(2*k+1) for k in range(terms))
        error=2*z**(2*terms+1)/(F(2*terms+1)*(1-z*z))
        return lo,lo+error
    lo,hi=series((x-1)/(x+1))
    a,b=series(F(1,3))
    return (lo+exponent*a,hi+exponent*b) if exponent>=0 else (lo+exponent*b,hi+exponent*a)

def layer_interval(polys,n):
    rows=[row for mask,row in enumerate(polys) if mask.bit_count()==n]
    pi=sum(row[0] for row in rows); pi1=sum(row[1] for row in rows)
    constant=-sum(row[1]**2/row[0] for row in rows)+pi1*pi1/pi
    lo=hi=constant
    for row in rows:
        a,b=log_bounds(row[0]/pi); coefficient=-2*row[2]
        lo+=coefficient*(a if coefficient>=0 else b)
        hi+=coefficient*(b if coefficient>=0 else a)
    return lo,hi

def short_enclosure(interval):
    scale=10**9; lo,hi=interval
    return [str(F((lo*scale).numerator//(lo*scale).denominator,scale)),
            str(F(-((-hi*scale).numerator//(-hi*scale).denominator),scale))]

def entropy_curvature_interval(rows):
    lo=hi=-sum(row[1]**2/row[0] for row in rows)
    for row in rows:
        a,b=log_bounds(row[0]); coefficient=-2*row[2]
        lo+=coefficient*(a if coefficient>=0 else b)
        hi+=coefficient*(b if coefficient>=0 else a)
    return lo,hi

def statistics(polys):
    jets=[[dec(row[0]),dec(row[1]),2*dec(row[2])] for row in polys]
    def entropy(items): return -sum(p*p.ln() for p,_,_ in items)
    def h2(items): return -sum(p1*p1/p+p2*p.ln() for p,p1,p2 in items)
    counts=[[sum(jets[mask][j] for mask in range(8) if mask.bit_count()==n) for j in range(3)] for n in range(4)]
    def layer(n):
        items=[jets[mask] for mask in range(8) if mask.bit_count()==n]
        pi,pi1,pi2=counts[n]
        return -sum(p1*p1/p for p,p1,p2 in items)+pi1*pi1/pi-sum(p2*(p/pi).ln() for p,p1,p2 in items)
    result=dict(H=entropy(jets),count_H=entropy(counts),total=h2(jets),count=h2(counts),singleton=layer(1),pair=layer(2))
    result['psi']=result['singleton']+result['pair']
    result['decomposition_residual']=result['total']-result['count']-result['psi']
    g=sum(-sum(p*(p/counts[n][0]).ln() for mask,(p,_,_) in enumerate(jets) if mask.bit_count()==n) for n in (1,2))
    result['entropy_decomposition_residual']=result['H']-result['count_H']-g
    return result

def main():
    joint=json.loads((HERE/'joint_replay.json').read_text())
    sphere=json.loads((HERE/'sphere_replay.json').read_text())
    records={key:joint[key] for key in ('best_total_simplex','best_psi_simplex','best_singleton_layer_simplex','best_pair_layer_simplex')}
    records['best_total_sphere']=sphere['best_total_sphere']
    checks={}
    with localcontext() as ctx:
        ctx.prec=80
        for name,row in records.items():
            q=rational_orthogonal(row['Q'])
            theta=[F(str(x)) for x in row['theta']]
            v=[F(str(x)) for x in row.get('v',row.get('v_unit'))]
            polys=event_polynomials(q,theta,v)
            stats=statistics(polys)
            radius=min(min(t,1-t)/a for t,a in zip(theta,v) if a)/2
            checks[name]=dict(Q=[[str(x) for x in line] for line in q],theta=[str(x) for x in theta],v=[str(x) for x in v],
                              Q_change_max=str(max(abs(q[i][j]-F(str(row['Q'][i][j]))) for i in range(3) for j in range(3))),
                              radius=str(radius),atoms=[[str(x) for x in line] for line in polys],
                              components={key:str(x) for key,x in stats.items()},
                              author_component_errors={key:str(abs(stats[key]-Decimal(str(row['components'][key])))) for key in ('total','count','psi','singleton','pair')})
            if name in ('best_psi_simplex','best_singleton_layer_simplex','best_pair_layer_simplex'):
                one=layer_interval(polys,1); two=layer_interval(polys,2)
                paired=(one[0]+two[0],one[1]+two[1])
                total_interval=entropy_curvature_interval(polys)
                checks[name]['exact_log_intervals']=dict(singleton=short_enclosure(one),pair=short_enclosure(two),psi=short_enclosure(paired),total=short_enclosure(total_interval),atanh_terms=8,outer_rounding_denominator=10**9)
                selected=paired if name=='best_psi_simplex' else one if name=='best_singleton_layer_simplex' else two
                assert selected[0]>0
                assert total_interval[1]<0
            assert stats['total']<0
            assert abs(stats['decomposition_residual'])<Decimal('1e-70')
            assert abs(stats['entropy_decomposition_residual'])<Decimal('1e-70')
        assert Decimal(checks['best_psi_simplex']['components']['psi'])>0
        assert Decimal(checks['best_singleton_layer_simplex']['components']['singleton'])>0
        assert Decimal(checks['best_pair_layer_simplex']['components']['pair'])>0
    # Run only the author's simplex function for a deterministic unit test.
    tree=ast.parse((HERE/'original_simplex_snapshot.py').read_text())
    function=next(node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name=='max_quadratic_on_simplex')
    namespace={'np':np}
    exec(compile(ast.Module(body=[function],type_ignores=[]),'author_simplex_unit_test','exec'),namespace)
    m=np.ones((3,3))-3*np.eye(3)
    observed,vector=namespace['max_quadratic_on_simplex'](m)
    assert abs(observed+.5)<1e-14
    scaled=(6*np.ones((3,3))-16*np.eye(3))*1e14
    scaled_value,scaled_vector=namespace['max_quadratic_on_simplex'](scaled)
    assert scaled_value<0 and np.ones(3)@scaled@np.ones(3)/9>0
    # Bordered KKT solves the missed singular interior point exactly.
    augmented=[[F(int(m[i,j])) for j in range(3)]+[F(-1)] for i in range(3)]+[[F(1)]*3+[F(0)]]
    exact=product(inverse(augmented),[[F(0)],[F(0)],[F(0)],[F(1)]])
    assert [row[0] for row in exact]==[F(1,3)]*3+[F(0)]
    report=dict(frozen_points=checks,singular_simplex=dict(M=m.tolist(),author_max=observed,author_vector=vector.tolist(),true_max='0',true_argmax=['1/3']*3),
                scale_simplex=dict(M=scaled.tolist(),author_max=scaled_value,author_vector=scaled_vector.tolist(),true_max='200000000000000/3',true_argmax=['1/3']*3),
                denominators=dict(frozen_points=5,exact_event_polynomials=40,coefficients_per_event=4,precision=80,algorithm_counterexamples=2),
                audited_original_search_sha256='e691fb766e5a3a41357205e3656e07bed308f2a27f9b6c884df9f6f91446da9d',
                version_drift_note='Author revised live script after completed replay. Unit tests bind the saved original function. One interim live-function AST execution failed with NameError; no mathematical calculation failed.',
                hashes=json.loads((HERE/'initial_author_hashes.json').read_text()),
                frozen_input_hashes={name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in ('joint_replay.json','sphere_replay.json','original_simplex_snapshot.py')},exit_code=0)
    (HERE/'independent_check.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({name:row['components'] for name,row in checks.items()},indent=2))
    print('EXIT_CODE=0')

if __name__=='__main__': main()
