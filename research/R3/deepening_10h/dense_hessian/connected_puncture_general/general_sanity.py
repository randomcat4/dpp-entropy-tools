"""Bounded exact U7 sanity; standard library, no other research-module imports.

The proof is analytic. These finite cycle/graph checks remain SCOUT.
"""
from fractions import Fraction as F
from itertools import combinations,permutations
from pathlib import Path
import json,hashlib,time

HERE=Path(__file__).resolve().parent

def put(poly,key,value):
    poly[key]=poly.get(key,F(0))+value
    if not poly[key]: del poly[key]

def matching_cycle(m):
    out={0:F(1)}
    for mask in range(1,1<<m):
        if any(mask>>i&1 and mask>>((i+1)%m)&1 for i in range(m)): continue
        out[mask]=F((-1)**mask.bit_count())
    return out

def cycle_matching_entropy_coefficient(m):
    M=matching_cycle(m); R={k:v for k,v in M.items() if k}; power={0:F(1)}
    target=(1<<m)-1; coeff=F(0); ledger=[]
    for k in range(1,m+1):
        nxt={}
        for a,ca in power.items():
            for b,cb in R.items():
                if not a&b: put(nxt,a|b,ca*cb)
        power=nxt
        multiplier=F(-1) if k==1 else F((-1)**(k+1),k*(k-1))
        contribution=multiplier*power.get(target,F(0)); coeff+=contribution
        ledger.append(dict(power=k,raw_coefficient=str(power.get(target,F(0))),entropy_contribution=str(contribution)))
    assert coeff==-1
    return dict(m=m,matching_part=str(coeff),full_doubled_cycle_coefficient=str(coeff-2),terms=ledger)

def verify_cycle_determinant(m):
    edges=[tuple(sorted((i,(i+1)%m))) for i in range(m)]
    got={}
    for perm in permutations(range(m)):
        inv=sum(perm[i]>perm[j] for i in range(m) for j in range(i+1,m))
        exp=[0]*m; valid=True
        for i,j in enumerate(perm):
            if i==j: continue
            edge=tuple(sorted((i,j)))
            if edge not in edges: valid=False; break
            exp[edges.index(edge)]+=1
        if valid: put(got,tuple(exp),F((-1)**inv))
    expected={tuple(2*int(mask>>i&1) for i in range(m)):c for mask,c in matching_cycle(m).items()}
    put(expected,(1,)*m,F(2*(-1)**(m-1)))
    assert got==expected
    return dict(m=m,determinant_monomials=len(got),permutations_checked=__import__('math').factorial(m))

def char_likelihood(n,weights,targets,marker_caps,total_cap):
    # Three formal variables: epsilon and up to two marked coordinates.
    dim=1+len(targets); out={}
    expr={}
    for edge,w in weights.items(): expr[edge]=[(tuple([1]+[0]*len(targets)),w)]
    for j,edge in enumerate(targets):
        e=[0]*dim; e[j+1]=1
        expr.setdefault(edge,[]).append((tuple(e),F(1)))
    for size in range(2,n+1):
        for ids in combinations(range(n),size):
            moment=tuple(int(i in ids) for i in range(n))
            for perm in permutations(ids):
                if any(i==j for i,j in zip(ids,perm)): continue
                sign=(-1)**sum(perm[i]>perm[j] for i in range(size) for j in range(i+1,size))
                terms={(0,)*dim:F(sign)}
                for i,j in zip(ids,perm):
                    factors=expr.get(tuple(sorted((i,j))),[]); nxt={}
                    for e,c in terms.items():
                        for f,d in factors:
                            g=tuple(a+b for a,b in zip(e,f))
                            if sum(g)<=total_cap and all(g[k+1]<=marker_caps[k] for k in range(len(targets))): put(nxt,g,c*d)
                    terms=nxt
                    if not terms: break
                for e,c in terms.items(): put(out,(e,moment),c)
    return out

def char_product(a,b,marker_caps,cap):
    out={}
    for (ea,ma),ca in a.items():
        for (eb,mb),cb in b.items():
            e=tuple(x+y for x,y in zip(ea,eb))
            if sum(e)>cap or any(e[i+1]>m for i,m in enumerate(marker_caps)): continue
            put(out,(e,tuple(x+y for x,y in zip(ma,mb))),ca*cb)
    return out

def entropy_target(n,weights,targets,marker_caps,residual_cap):
    cap=residual_cap+sum(marker_caps); dim=len(targets)+1
    R=char_likelihood(n,weights,targets,marker_caps,cap)
    current={((0,)*dim,(0,)*n):F(1)}; out={}; sizes=[]
    for k in range(1,cap//2+1):
        current=char_product(current,R,marker_caps,cap); sizes.append(len(current))
        if k==1: continue
        factor=F((-1)**(k+1),k*(k-1))
        for (e,m),c in current.items():
            if tuple(e[1:])!=tuple(marker_caps) or 1 in m: continue
            if e[0]<=residual_cap: put(out,(e[0],m),c*factor)
    derivative_factor=F(1)
    for k in marker_caps:
        if k==2: derivative_factor*=2
    return {key:c*derivative_factor for key,c in out.items()},dict(likelihood_terms=len(R),power_sizes=sizes)

def shortest_paths(n,weights,target):
    start,stop=target; paths=[]
    def visit(path):
        if path[-1]==stop: paths.append(path); return
        for j in range(n):
            if j not in path and tuple(sorted((path[-1],j))) in weights: visit(path+[j])
    visit([start]); d=min(len(p)-1 for p in paths)
    return d,[p for p in paths if len(p)==d+1]

def graph_probe(name,n,weights,targets,kind):
    distances=[shortest_paths(n,weights,e)[0] for e in targets]
    caps=[2] if kind=='diagonal' else [1,1]
    residual_cap=2*distances[0] if kind=='diagonal' else sum(distances)
    got,stats=entropy_target(n,weights,targets,caps,residual_cap)
    expected={}
    if kind=='diagonal':
        d,paths=shortest_paths(n,weights,targets[0])
        for path in paths:
            c=F(-6)
            for a,b in zip(path,path[1:]): c*=weights[tuple(sorted((a,b)))]**2
            m=tuple(2*int(i in path) for i in range(n))
            put(expected,(2*d,m),c)
    assert got==expected,(name,got,expected)
    return dict(name=name,n=n,weights=[dict(edge=e,value=str(w)) for e,w in weights.items()],targets=targets,kind=kind,
        x_scope='arbitrary strict x: vertex moments retained as independent formal symbols',distances=distances,
        residual_order_checked_through=residual_cap,all_lower_and_mixed_terms_zero=True,
        terms=[dict(power=p,vertex_moment_orders=m,coefficient=str(c)) for (p,m),c in got.items()],stats=stats)

def locality_cancellation():
    # Two disconnected support edges and two connecting marked chords.
    # The allowed degree-four-per-vertex monomial a^3*b^3*y*z nevertheless
    # cancels: minimum degree alone cannot prove the graph-distance bound.
    weights={(0,1):F(2,3),(2,3):-F(3,5)}
    got,stats=entropy_target(4,weights,[(0,3),(1,2)],[1,1],6)
    assert not got
    return dict(name='disconnected_residual_support_cross_Hessian',through_residual_degree=6,terms=[],stats=stats)

def direct_mobius_gate():
    n=4; x=[F(1,5),F(1,3),F(3,5),F(3,4)]
    weights={(0,1):F(1,3),(1,2):-F(2,5),(2,3):F(3,7),(0,3):F(2,9)}
    targets=[(0,2),(1,3)]; values=[F(1,100),F(1,200),-F(1,150)]
    R=char_likelihood(n,weights,targets,[4,4],4)
    K=[[F(0)]*n for _ in range(n)]
    for i in range(n): K[i][i]=x[i]
    for (i,j),w in weights.items(): K[i][j]=K[j][i]=values[0]*w
    for k,(i,j) in enumerate(targets): K[i][j]+=values[k+1]; K[j][i]+=values[k+1]
    inc={}
    for mask in range(1<<n):
        ids=[i for i in range(n) if mask>>i&1]; ans=F(0)
        for perm in permutations(ids):
            term=F((-1)**sum(perm[i]>perm[j] for i in range(len(ids)) for j in range(i+1,len(ids))))
            for i,j in zip(ids,perm): term*=K[i][j]
            ans+=term
        inc[mask]=ans
    atoms=[]
    for mask in range(1<<n):
        atom=sum((-1)**(sup.bit_count()-mask.bit_count())*inc[sup] for sup in range(1<<n) if sup&mask==mask)
        base=F(1); zeta=[]
        for i,xi in enumerate(x):
            base*=xi if mask>>i&1 else 1-xi
            zeta.append(1/xi if mask>>i&1 else -1/(1-xi))
        r=F(0)
        for (e,m),c in R.items():
            for v,k in zip(values,e): c*=v**k
            for v,k in zip(zeta,m): c*=v**k
            r+=c
        assert atom==base*(1+r); atoms.append(atom)
    assert min(atoms)>0 and sum(atoms)==1
    return dict(n=n,x=list(map(str,x)),variables=list(map(str,values)),atoms=list(map(str,atoms)),all_16_equal=True)

def main():
    start=time.time()
    cycles=[cycle_matching_entropy_coefficient(m) for m in range(3,11)]
    determinants=[verify_cycle_determinant(m) for m in range(3,8)]
    P6={(i,i+1):F((-1)**i*(i+1),2*i+3) for i in range(5)}
    C6=dict(P6); C6[(0,5)]=F(6,13)
    cases=[
        graph_probe('P6_distance5_endpoint',6,P6,[(0,5)],'diagonal'),
        graph_probe('P6_remote_mixed_distances5_and3',6,P6,[(0,5),(1,4)],'mixed'),
        graph_probe('C6_two_shortest_paths',6,C6,[(0,3)],'diagonal'),
        graph_probe('C6_distinct_same_distance_pairs',6,C6,[(0,3),(1,4)],'mixed'),
        graph_probe('C6_unequal_distance_pairs',6,C6,[(0,3),(0,2)],'mixed')]
    report=dict(status='EXACT_SYMBOLIC_SCOUT_ONLY',cycles=cycles,cycle_determinants=determinants,
        graph_probes=cases,locality_cancellation=locality_cancellation(),direct_mobius_gate=direct_mobius_gate(),
        scope='Finite tests support but do not prove the general analytic argument.',
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),elapsed_seconds=time.time()-start,exit_code=0)
    (HERE/'sanity_results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status=report['status'],cycles=len(cycles),determinants=len(determinants),graph_probes=len(cases),elapsed_seconds=report['elapsed_seconds']),indent=2))

if __name__=='__main__': main()
