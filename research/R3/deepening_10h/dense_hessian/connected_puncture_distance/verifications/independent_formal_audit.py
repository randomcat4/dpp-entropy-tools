"""Independent U5 character/moment formal audit; no author module imports."""
from fractions import Fraction as F
from itertools import combinations, permutations, product
from collections import Counter
from pathlib import Path
import json, hashlib, time

HERE=Path(__file__).resolve().parent
EDGES=list(combinations(range(4),2)); DIST=(1,2,3,1,2,1); SUPPORT={0,3,5}
ZERO=(0,)*6

def add(out,k,v):
    out[k]=out.get(k,F(0))+v
    if not out[k]: del out[k]

def likelihood_terms():
    terms={}
    for size in range(2,5):
        for ids in combinations(range(4),size):
            moment=tuple(int(i in ids) for i in range(4))
            for perm in permutations(ids):
                if any(i==j for i,j in zip(ids,perm)): continue
                inv=sum(perm[i]>perm[j] for i in range(size) for j in range(i+1,size))
                exp=[0]*6
                for i,j in zip(ids,perm): exp[EDGES.index(tuple(sorted((i,j))))]+=1
                add(terms,(tuple(exp),moment),F((-1)**inv))
    return terms

def multiply(a,b):
    out={}
    for (ea,ma),ca in a.items():
        for (eb,mb),cb in b.items():
            ec=tuple(x+y for x,y in zip(ea,eb))
            if sum(ec)<=8: add(out,(ec,tuple(x+y for x,y in zip(ma,mb))),ca*cb)
    return out

def moment_expand(m):
    # Variables are w_1,...,w_4,q_1,...,q_4. q_i=E zeta_i^3.
    # E zeta=0, E zeta^2=w, E zeta^4=w^3-3w^2.
    if 1 in m: return {}
    choices=[]
    for i,k in enumerate(m):
        z=[0]*8
        if k==0: choices.append([(tuple(z),F(1))])
        elif k==2: z[i]=1; choices.append([(tuple(z),F(1))])
        elif k==3: z[i+4]=1; choices.append([(tuple(z),F(1))])
        elif k==4:
            z[i]=3; y=z.copy(); y[i]=2
            choices.append([(tuple(z),F(1)),(tuple(y),F(-3))])
        else: raise AssertionError(k)
    out={}
    for selected in product(*choices):
        exp=tuple(sum(item[0][j] for item in selected) for j in range(8))
        coeff=F(1)
        for _,c in selected: coeff*=c
        add(out,exp,coeff)
    return out

def entropy_formal(R):
    current={(ZERO,(0,)*4):F(1)}; ent={}
    for k in range(1,5):
        current=multiply(current,R)
        if k==1: continue
        coeff=F((-1)**(k+1),k*(k-1))
        for (edgeexp,mom),c in current.items():
            for me,mc in moment_expand(mom).items(): add(ent,(edgeexp,me),coeff*c*mc)
    return ent

def jet_at_path(ent,derivatives):
    out={}
    for (e,m),c in ent.items():
        e=list(e)
        for i in derivatives:
            c*=e[i]; e[i]-=1
            if c==0: break
        if not c or any(e[i] for i in range(6) if i not in SUPPORT): continue
        # Keep all a,b,c and all moment symbols formal.
        key=(sum(e),tuple(e[i] for i in (0,3,5)),m)
        add(out,key,c)
    return out

def determinant_numeric(M):
    n=len(M); ans=F(0)
    for p in permutations(range(n)):
        c=F((-1)**sum(p[i]>p[j] for i in range(n) for j in range(i+1,n)))
        for i,j in enumerate(p): c*=M[i][j]
        ans+=c
    return ans

def mobius_gate(R):
    x=(F(1,5),F(1,3),F(3,5),F(3,4))
    z=tuple(F(i+1,100) for i in range(6)); K=[[F(0)]*4 for _ in range(4)]
    for i in range(4): K[i][i]=x[i]
    for (i,j),v in zip(EDGES,z): K[i][j]=K[j][i]=v
    inc={mask:determinant_numeric([[K[i][j] for j in range(4) if mask>>j&1] for i in range(4) if mask>>i&1]) for mask in range(16)}
    atoms=[]
    for mask in range(16):
        p=sum((-1)**(sup.bit_count()-mask.bit_count())*inc[sup] for sup in range(16) if sup&mask==mask)
        base=F(1); zet=[]
        for i,xi in enumerate(x):
            base*=xi if mask>>i&1 else 1-xi
            zet.append(1/xi if mask>>i&1 else -1/(1-xi))
        r=F(0)
        for (e,m),coef in R.items():
            for value,exp in zip(z,e): coef*=value**exp
            for value,exp in zip(zet,m): coef*=value**exp
            r+=coef
        assert p==base*(1+r)
        atoms.append(str(p))
    assert sum(map(F,atoms))==1 and min(map(F,atoms))>0
    return atoms

def eval_term_map(poly,x,weights):
    w=[1/(v*(1-v)) for v in x]; q=[(1-2*v)*wi**2 for v,wi in zip(x,w)]
    out={}
    for (power,ae,me),c in poly.items():
        for a,e in zip(weights,ae): c*=a**e
        for a,e in zip(w+q,me): c*=a**e
        add(out,power,c)
    return out

def graph_count():
    records=[]
    for bits in range(64):
        chosen=[e for i,e in enumerate(EDGES) if bits>>i&1]; seen={0}
        while True:
            nxt=seen|{j for i,j in chosen if i in seen}|{i for i,j in chosen if j in seen}
            if nxt==seen: break
            seen=nxt
        if len(seen)==4: records.append(tuple(chosen))
    return records

def replay_n4(ent,x,graphs,records):
    w=[1/(v*(1-v)) for v in x]; q=[(1-2*v)*wi**2 for v,wi in zip(x,w)]
    numeric={}
    for (edgeexp,me),c in ent.items():
        for val,power in zip(w+q,me): c*=val**power
        add(numeric,edgeexp,c)
    ledger=[]
    for salt,chosen in enumerate(graphs):
        weights={}
        for i,j in chosen:
            raw=((i+1)*11+(j+1)*7+salt*5)%23-11
            weights[(i,j)]=F(raw if raw else 9,29)
        distances=[]; paths=[]
        for start,stop in EDGES:
            allpaths=[]
            def visit(path):
                if path[-1]==stop: allpaths.append(path); return
                for nxt in range(4):
                    if nxt not in path and tuple(sorted((path[-1],nxt))) in weights: visit(path+[nxt])
            visit([start]); distance=min(len(p)-1 for p in allpaths)
            distances.append(distance); paths.append([p for p in allpaths if len(p)-1==distance])
        matrix=[[F(0)]*6 for _ in range(6)]; targets=[]
        for i in range(6):
            for j in range(6):
                series={}
                for exp,coef in numeric.items():
                    e=list(exp); coef*=e[i]; e[i]-=1
                    if not coef: continue
                    coef*=e[j]; e[j]-=1
                    if not coef: continue
                    for k,power in enumerate(e):
                        if power: coef*=weights.get(EDGES[k],F(0))**power
                    if coef: add(series,sum(e),coef)
                scale=distances[i]+distances[j]
                assert all(k>=scale for k in series)
                matrix[i][j]=series.get(scale,F(0))
            expect=F(0)
            for path in paths[i]:
                term=F(-6)
                for v in path: term*=w[v]
                for u,v in zip(path,path[1:]): term*=weights[tuple(sorted((u,v)))]**2
                expect+=term
            assert matrix[i][i]==expect
            targets.append(dict(edge=EDGES[i],distance=distances[i],coefficient=str(expect)))
        L=[[F(int(i==j)) for j in range(6)] for i in range(6)]; pivots=[]
        for i in range(6):
            pivot=-matrix[i][i]-sum(L[i][k]**2*pivots[k] for k in range(i)); assert pivot>0
            pivots.append(pivot)
            for j in range(i+1,6): L[j][i]=(-matrix[j][i]-sum(L[j][k]*L[i][k]*pivots[k] for k in range(i)))/pivot
        assert list(map(str,pivots))==records[salt]['ldl_pivots_of_negative_scaled_matrix']
        ledger.append(dict(edges=chosen,weights=[str(weights[e]) for e in chosen],targets=targets,pivots=list(map(str,pivots))))
    return ledger

def main():
    start=time.time(); R=likelihood_terms(); ent=entropy_formal(R); atoms=mobius_gate(R)
    matrix=[]; violations=[]; gradients=[]; sanity=[]
    x=[F(1,5),F(1,3),F(3,5),F(3,4)]; weights=[F(1,3),-F(2,5),F(3,7)]
    for i in range(6):
        grad=jet_at_path(ent,(i,)); low={k:v for k,v in grad.items() if k[0]<=DIST[i]}
        gradients.append(dict(edge=EDGES[i],first_order=min((k[0] for k in grad),default=None),forbidden_terms=str(low)))
        assert not low
        row=[]; sanityrow=[]
        for j in range(6):
            jet=jet_at_path(ent,(i,j)); threshold=DIST[i]+DIST[j]
            low={k:v for k,v in jet.items() if k[0]<threshold}
            at={k:v for k,v in jet.items() if k[0]==threshold}
            if low or (i!=j and at): violations.append(dict(i=i,j=j,low=str(low),at=str(at)))
            row.append(dict(scale=threshold,first_order=min((k[0] for k in jet),default=None),scaled_terms=[dict(power=k[0],weights=k[1],moments=k[2],coefficient=str(v)) for k,v in at.items()]))
            numeric=eval_term_map(at,x,weights); sanityrow.append(str(numeric.get(threshold,F(0))))
        matrix.append(row); sanity.append(sanityrow)
    assert not violations
    for i,(a,b) in enumerate(EDGES):
        wexp=tuple(int(a<=v<=b) for v in range(4))+(0,)*4
        aexp=tuple(2*int(a<=v<b) for v in range(3))
        expected={(2*DIST[i],aexp,wexp):F(-6)}
        got=jet_at_path(ent,(i,i)); got={k:v for k,v in got.items() if k[0]==2*DIST[i]}
        assert got==expected,(i,got,expected)
    graphs=graph_count(); author=json.loads((HERE.parent/'scout_results.json').read_text())
    graph_report=author['n4_all_connected_scaled_matrix_scout']; distances=author['exact_distance_coefficient_scout']
    import ast
    recorded=[tuple(ast.literal_eval(e) for e in r['support_edges']) for r in graph_report['records']]
    assert len(graphs)==len(recorded)==38 and set(graphs)==set(recorded)
    assert all(len(r['ldl_pivots_of_negative_scaled_matrix'])==6 and min(map(F,r['ldl_pivots_of_negative_scaled_matrix']))>0 for r in graph_report['records'])
    assert distances['n4_total_pair_targets']==228
    n5=distances['n5_selected_graphs']; assert len(n5)==4 and sum(len(r['targets']) for r in n5)==40
    assert sanity==author['p4_exact_scaled_offdiag']['scaled_constant_matrix']
    n4_replay=replay_n4(ent,x,graphs,graph_report['records'])
    files=list(HERE.parent.glob('*.md'))+[HERE.parent/'connected_distance_scout.py',HERE.parent/'scout_results.json']
    report=dict(status='INDEPENDENT_FORMAL_IDENTITY_CHECK_PASSED',entropy_symbolic_terms=len(ent),likelihood_terms=len(R),mobius_gate_atoms=atoms,
        formal_entropy=[dict(edge_exponents=e,moment_exponents=m,coefficient=str(c)) for (e,m),c in sorted(ent.items())],
        formal_likelihood=[dict(edge_exponents=e,character_exponents=m,coefficient=str(c)) for (e,m),c in sorted(R.items())],
        offdiag_matrix=matrix,mixed_gradient_orders=gradients,sanity_matrix=sanity,violations=violations,
        counts=dict(n4_graphs=38,n4_reported_targets=228,n5_graphs=4,n5_targets=40),n4_replay=n4_replay,
        hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),elapsed=time.time()-start,exit_code=0)
    (HERE/'independent_formal_results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status=report['status'],terms=len(ent),sanity=sanity,gradients=gradients,elapsed=report['elapsed']),indent=2))

if __name__=='__main__': main()
