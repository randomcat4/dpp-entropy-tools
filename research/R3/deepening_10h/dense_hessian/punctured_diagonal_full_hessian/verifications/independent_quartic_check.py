"""U3/S9 independent multivariate quartic audit; no author import."""
from fractions import Fraction as F
from itertools import permutations,combinations
from pathlib import Path
import hashlib
import json
import time

HERE=Path(__file__).resolve().parent
AUTHOR=HERE.parent
def add(*polys):
    out={}
    for p in polys:
        for e,x in p.items(): out[e]=out.get(e,F(0))+x
    return {e:x for e,x in out.items() if x}
def scale(c,p): return {e:c*x for e,x in p.items() if c*x}
def mul(a,b):
    out={}
    for e,x in a.items():
        for f,y in b.items():
            g=tuple(i+j for i,j in zip(e,f))
            if sum(g)<=4: out[g]=out.get(g,F(0))+x*y
    return {e:x for e,x in out.items() if x}
def det(a,dim):
    out={}
    for perm in permutations(range(len(a))):
        sign=(-1)**sum(perm[i]>perm[j] for i in range(len(a)) for j in range(i+1,len(a)))
        term={(0,)*dim:F(sign)}
        for i,j in enumerate(perm): term=mul(term,a[i][j])
        out=add(out,term)
    return out
def encode(p): return [{'exponents':list(e),'coefficient':str(x)} for e,x in sorted(p.items())]
def main():
    start=time.time(); names=('frozen_problem.md','proof_candidate.md','verdict.md')
    hashes=lambda:{name:hashlib.sha256((AUTHOR/name).read_bytes()).hexdigest() for name in names}
    frozen=hashes(); records=[]
    for theta in ((F(1,3),F(3,5)),(F(1,5),F(2,5),F(4,5)),(F(1,5),F(1,3),F(3,5),F(3,4))):
        n=len(theta); edges=list(combinations(range(n),2)); d=len(edges); zero=(0,)*d
        matrix=[[{} for _ in range(n)] for _ in range(n)]
        for i in range(n): matrix[i][i]={zero:theta[i]}
        for k,(i,j) in enumerate(edges):
            e=list(zero); e[k]=1; matrix[i][j]=matrix[j][i]={tuple(e):F(1)}
        inclusion=[]
        for mask in range(2**n):
            ids=[i for i in range(n) if mask>>i&1]
            inclusion.append(det([[matrix[i][j] for j in ids] for i in ids],d))
        atoms=[add(*(scale((-1)**(sup.bit_count()-mask.bit_count()),inclusion[sup]) for sup in range(2**n) if sup&mask==mask)) for mask in range(2**n)]
        assert add(*atoms)=={zero:F(1)}
        for i in range(n): assert add(*(atom for mask,atom in enumerate(atoms) if mask>>i&1))=={zero:theta[i]}
        quartic={}
        for atom in atoms:
            assert not any(sum(e)==1 for e in atom)
            p0=atom[zero]; p2={e:x for e,x in atom.items() if sum(e)==2}
            quartic=add(quartic,scale(-1/(2*p0),mul(p2,p2)))
        expected={}
        for k,(i,j) in enumerate(edges):
            e=list(zero); e[k]=4
            expected[tuple(e)]=-1/(2*theta[i]*(1-theta[i])*theta[j]*(1-theta[j]))
        assert quartic==expected
        # Differentiate the full polynomial twice in every edge pair: no
        # cross-edge quadratic terms remain in the leading z-Hessian.
        hessian=[]
        for i in range(d):
            row=[]
            for j in range(d):
                derivative={}
                for exponent,coefficient in quartic.items():
                    e=list(exponent); weight=coefficient*e[i]; e[i]-=1
                    if not weight: continue
                    weight*=e[j]; e[j]-=1
                    if weight: derivative[tuple(e)]=weight
                if i!=j: assert not derivative
                else:
                    a,b=edges[i]; e=list(zero); e[i]=2
                    assert derivative=={tuple(e):-6/(theta[a]*(1-theta[a])*theta[b]*(1-theta[b]))}
                row.append(encode(derivative))
            hessian.append(row)
        records.append(dict(n=n,theta=[str(x) for x in theta],edges=edges,atoms=[encode(p) for p in atoms],
            quartic=encode(quartic),quartic_z_hessian=hessian,
            all_mixed_quartic_monomials_zero=True,quartic_matches_U2_tensor=True))
    assert hashes()==frozen,'author version drift'
    report=dict(status='PASS_EXACT_SANITY_NOT_A_UNIVERSAL_PROOF',author_hashes_before=frozen,author_hashes_after=hashes(),
        cases=records,counts=dict(dimensions=[2,3,4],parameter_centers=3,atom_polynomials=28,
            pure_quartic_coefficients=10,edge_hessian_entries=46,failed_checks=0,random_draws=0),
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),elapsed_seconds=time.time()-start,exit_code=0)
    (HERE/'independent_quartic_results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('author_hashes_before','counts','elapsed_seconds','exit_code')},indent=2))
if __name__=='__main__': main()
