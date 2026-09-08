"""U4 exact multivariate entropy jets; standard library, no random search."""
from fractions import Fraction as F
from itertools import permutations,combinations
from pathlib import Path
import hashlib
import json
import time

HERE=Path(__file__).resolve().parent
def add(*polys):
    out={}
    for p in polys:
        for e,x in p.items(): out[e]=out.get(e,F(0))+x
    return {e:x for e,x in out.items() if x}
def scale(c,p): return {e:c*x for e,x in p.items() if c*x}
def mul(a,b,cap):
    out={}
    for e,x in a.items():
        for f,y in b.items():
            g=tuple(i+j for i,j in zip(e,f))
            if sum(g)<=cap: out[g]=out.get(g,F(0))+x*y
    return {e:x for e,x in out.items() if x}
def det(a,dim,cap):
    out={}
    for perm in permutations(range(len(a))):
        sign=(-1)**sum(perm[i]>perm[j] for i in range(len(a)) for j in range(i+1,len(a)))
        term={(0,)*dim:F(sign)}
        for i,j in enumerate(perm): term=mul(term,a[i][j],cap)
        out=add(out,term)
    return out
def atoms(theta,Z,dim,cap):
    n=len(theta); zero=(0,)*dim
    K=[[({zero:theta[i]} if i==j else Z[i][j]) for j in range(n)] for i in range(n)]
    inc=[]
    for mask in range(2**n):
        ids=[i for i in range(n) if mask>>i&1]
        inc.append(det([[K[i][j] for j in ids] for i in ids],dim,cap))
    probs=[]
    for mask in range(2**n):
        p=add(*(scale((-1)**(sup.bit_count()-mask.bit_count()),inc[sup]) for sup in range(2**n) if sup&mask==mask))
        shifted=[[add(K[i][j],{zero:-F(i==j and not(mask>>i&1))}) for j in range(n)] for i in range(n)]
        assert p==scale((-1)**(n-mask.bit_count()),det(shifted,dim,cap))
        probs.append(p)
    assert add(*probs)=={zero:F(1)}
    for i in range(n): assert add(*(p for mask,p in enumerate(probs) if mask>>i&1))=={zero:theta[i]}
    return probs
def entropy_series(probs,dim,cap):
    zero=(0,)*dim; out={}
    for p in probs:
        p0=p[zero]; r=scale(1/p0,add(p,{zero:-p0}))
        assert not any(sum(e)<2 for e in r)
        power=r
        for k in range(2,cap//2+1):
            power=mul(power,r,cap)
            out=add(out,scale(F((-1)**(k+1),k*(k-1))*p0,power))
    return out
def encode(p): return [dict(exponents=list(e),coefficient=str(x)) for e,x in sorted(p.items())]
def main():
    start=time.time(); records=[]
    centers=((F(1,3),F(3,5)),(F(1,5),F(2,5),F(4,5)),(F(1,5),F(1,3),F(3,5),F(3,4)))
    for theta in centers:
        n=len(theta); edges=list(combinations(range(n),2)); dim=len(edges); zero=(0,)*dim
        Z=[[{} for _ in range(n)] for _ in range(n)]
        for index,(i,j) in enumerate(edges):
            e=list(zero); e[index]=1; Z[i][j]=Z[j][i]={tuple(e):F(1)}
        probs=atoms(theta,Z,dim,6); ent=entropy_series(probs,dim,6)
        w=[1/(x*(1-x)) for x in theta]; t=[(1-2*x)/(x*x*(1-x)**2) for x in theta]
        expected={}
        for index,(i,j) in enumerate(edges):
            e=list(zero); e[index]=4; expected[tuple(e)]=-w[i]*w[j]/2
            e=list(zero); e[index]=6
            if t[i]*t[j]: expected[tuple(e)]=-t[i]*t[j]/6
        for i,j,k in combinations(range(n),3):
            e=list(zero)
            for pair in ((i,j),(i,k),(j,k)): e[edges.index(pair)]=2
            expected[tuple(e)]=-3*w[i]*w[j]*w[k]
        assert ent==expected
        assert not any(sum(e)==5 for e in ent)
        records.append(dict(n=n,theta=list(map(str,theta)),edges=edges,atoms=[encode(p) for p in probs],
            entropy_degree_4_to_6=encode(ent),all_fifth_coefficients_zero=True,
            exact_sixth_formula_matches=True))

    # n=3 path/star: coefficient in the missing edge (1,3).
    theta=centers[1]; w=[1/(x*(1-x)) for x in theta]
    a,b=F(2,5),-F(3,7)
    path=dict(theta=list(map(str,theta)),support_edges=[[0,1],[1,2]],weights=[str(a),str(b)],
        supported_hessian_epsilon2_coefficients=[str(-6*w[0]*w[1]*a*a),str(-6*w[1]*w[2]*b*b)],
        missing_hessian_epsilon4_coefficient=str(-6*w[0]*w[1]*w[2]*a*a*b*b),
        statement='path and three-vertex star are relabellings; full conclusion uses analytic block proof')

    # n=4 P4 with variable epsilon and one independent missing edge variable t.
    # This is one bounded higher-distance SCOUT, not a full-Hessian theorem.
    theta=centers[2]; weights=(F(1,3),-F(2,5),F(3,7)); Z=[[{} for _ in range(4)] for _ in range(4)]
    for pair,weight in zip(((0,1),(1,2),(2,3)),weights):
        i,j=pair; Z[i][j]=Z[j][i]={(1,0):weight}
    Z[0][3]=Z[3][0]={(0,1):F(1)}
    p4=atoms(theta,Z,2,8); ent4=entropy_series(p4,2,8)
    missing_curvature={e[0]:2*c for e,c in ent4.items() if e[1]==2}
    productw=F(1)
    for x in theta: productw/=x*(1-x)
    expected_lead=-6*productw
    for weight in weights: expected_lead*=weight*weight
    assert missing_curvature=={6:expected_lead}
    longpath=dict(status='SCOUT_ONLY_ONE_ENTRY_NOT_FULL_HESSIAN',theta=list(map(str,theta)),
        path_weights=list(map(str,weights)),atoms=[encode(p) for p in p4],
        entropy_through_degree8=encode(ent4),missing_edge=[0,3],
        missing_curvature_through_epsilon6={str(k):str(v) for k,v in missing_curvature.items()})

    # Exact n=3 single-edge obstruction: first jet of a cross-component edge
    # vanishes and all block-event marginals have zero second jet.
    theta=centers[1]; Z=[[{} for _ in range(3)] for _ in range(3)]
    Z[0][1]=Z[1][0]={(1,0):F(2,5)}
    Z[0][2]=Z[2][0]={(0,1):F(1)}
    probs=atoms(theta,Z,2,6)
    assert not any(e[1]==1 for p in probs for e in p)
    for block in ((0,1),(2,)):
        for bits in range(2**len(block)):
            selected=[p for mask,p in enumerate(probs) if all(((mask>>i)&1)==((bits>>j)&1) for j,i in enumerate(block))]
            marginal=add(*selected)
            assert not any(e[1]>0 for e in marginal)
    single=dict(theta=list(map(str,theta)),present_edge=[0,1],cross_component_test_edge=[0,2],
        exact_zero_first_cross_jet=True,block_marginals_constant_in_cross_variable=True,
        curvature='EXACTLY_ZERO_BY_ANALYTIC_BLOCK_LOG_CANCELLATION',atoms=[encode(p) for p in probs])
    report=dict(status='AUTHOR_ANALYTIC_CANDIDATES_PENDING_REVIEW; FINITE_CHECKS_SCOUT',
        general_jet_cases=records,n3_path=path,n3_single_edge=single,n4_long_path=longpath,
        counts=dict(general_centers=3,general_atom_polynomials=28,single_edge_atom_polynomials=8,
                    long_path_atom_polynomials=16,total_atom_polynomials=52,random_draws=0,failed_checks=0),
        elapsed_seconds=time.time()-start,exit_code=0,
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (HERE/'sanity_results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(counts=report['counts'],n3_path=path,n4_missing_curvature=longpath['missing_curvature_through_epsilon6'],elapsed_seconds=report['elapsed_seconds'],exit_code=0),indent=2))
if __name__=='__main__': main()
