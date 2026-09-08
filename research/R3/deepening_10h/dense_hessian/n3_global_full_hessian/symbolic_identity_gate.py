"""Exact all-parameter conditional-odds polynomial identities, no CAS."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import importlib.util,json,hashlib
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('own_global_probe',HERE/'global_probe.py'); g=importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
def mul(a,b):
    out={}
    for e,c in a.items():
        for f,d in b.items(): g.put(out,tuple(x+y for x,y in zip(e,f)),c*d)
    return out
def var(i,j): return g.term((g.COORDS.index((min(i,j),max(i,j))),))
def main():
    records=[]; p=g.POLYS
    for i,j in g.COORDS[3:]:
        k=3-i-j; a=var(i,j); b=mul(var(i,k),var(j,k)); z=var(k,k)
        absent=g.combine((mul(g.combine((g.term(()),1),(z,-1)),a),1),(b,1))
        present=g.combine((mul(z,a),1),(b,-1))
        lhs0=g.combine((mul(p[0],p[(1<<i)|(1<<j)]),1),(mul(p[1<<i],p[1<<j]),-1))
        lhs1=g.combine((mul(p[1<<k],p[7]),1),(mul(p[(1<<i)|(1<<k)],p[(1<<j)|(1<<k)]),-1))
        assert g.combine((lhs0,1),(mul(absent,absent),1))=={}
        assert g.combine((lhs1,1),(mul(present,present),1))=={}
        records.append(dict(pair=(i,j),both_polynomial_identities=True,absent_square_terms=len(mul(absent,absent)),present_square_terms=len(mul(present,present))))
    assert g.combine(*[(poly,1) for poly in p])==g.term(())
    assert all(g.combine(*[(g.GRAD[s][i],1) for s in range(8)])=={} for i in range(6))
    assert all(g.combine(*[(g.HESS[s][i][j],1) for s in range(8)])=={} for i in range(6) for j in range(6))
    assert all(g.HESS[s][i][i]=={} for s in range(8) for i in range(3))
    report=dict(status='EXACT_SYMBOLIC_IDENTITIES_PASSED_NOT_GLOBAL_CONCAVITY',records=records,atom_mass=True,first_second_mass=True,diagonal_rank_one_atom_acceleration_zero=True,
        artificial_non_DPP_pair=dict(N='I',Fisher='Frobenius identity',rho=F(3,2),B_on_identity=-3,claim='algebraic nonimplication only, not DPP realizability'),
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),dependency_sha256=hashlib.sha256((HERE/'global_probe.py').read_bytes()).hexdigest(),exit_code=0)
    (HERE/'symbolic_identity_results.json').write_text(json.dumps(g.encode(report),indent=2)+'\n')
    print('six conditional-odds identities and all mass/rank-one checks passed')
if __name__=='__main__': main()
