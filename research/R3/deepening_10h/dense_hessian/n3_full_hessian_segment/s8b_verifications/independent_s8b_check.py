"""Independent S8b leaf audit; imports only the already audited NONAUTHOR S8 helper.

No author S8/S8b module is imported or executed. Every atom jet and interval
Hessian is reconstructed; all stored rational P matrices are treated as data.
"""
import sys
sys.dont_write_bytecode=True
sys.set_int_max_str_digits(0)
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
from fractions import Fraction as F
from pathlib import Path
from math import prod
from collections import Counter
import importlib.util
import hashlib
import json
import time

HERE=Path(__file__).resolve().parent
BASE=HERE.parent
FILES=('s8b_expansion.md','s8b_verdict.md','s8b_run_log.md','s8b_preconditioned_expansion.py','s8b_preconditioned_certificate.json')
def hashes(): return {name:hashlib.sha256((BASE/name).read_bytes()).hexdigest() for name in FILES}
def compact(interval):
    den=10**24; a,b=interval
    return F((a*den).__floor__(),den),F((b*den).__ceil__(),den)
def rational_congruence(B,P):
    T=[]; negative_weights=0
    for a in range(6):
        row=[]
        for b in range(6):
            lo=hi=F(0)
            for i in range(6):
                for j in range(6):
                    weight=P[i][a]*P[j][b]
                    if weight<0: negative_weights+=1
                    lo+=weight*(B[i][j][0] if weight>=0 else B[i][j][1])
                    hi+=weight*(B[i][j][1] if weight>=0 else B[i][j][0])
            row.append((lo,hi))
        T.append(row)
    assert T==list(map(list,zip(*T)))
    return T,negative_weights
def margins(T):
    return [T[i][i][0]-sum(max(abs(T[i][j][0]),abs(T[i][j][1])) for j in range(6) if j!=i) for i in range(6)]
def main():
    start=time.time(); before=hashes()
    helper_path=BASE/'verifications'/'fresh_s8_audit.py'
    helper_hash=hashlib.sha256(helper_path.read_bytes()).hexdigest()
    spec=importlib.util.spec_from_file_location('non_author_s8',helper_path)
    verifier=importlib.util.module_from_spec(spec); spec.loader.exec_module(verifier)
    author=json.loads((BASE/'s8b_preconditioned_certificate.json').read_text())
    assert author['script_sha256']==before['s8b_preconditioned_expansion.py']
    K0,R=verifier.m8_line(); jets=verifier.build_jets(K0,R)
    assert K0==[[F(x) for x in row] for row in author['line']['K0']]
    assert R==[[F(x) for x in row] for row in author['line']['R']]
    assert all(sum(jets['p0'][s][k] for s in range(8))==F(k==0) for k in range(4))
    assert all(sum(jets['p1'][i][s][k] for s in range(8))==0 for i in range(6) for k in range(4))
    assert all(sum(jets['pij'][i][j][s][k] for s in range(8))==0 for i in range(6) for j in range(6) for k in range(4))
    radius=F(29,100); rawleaves=author['largest_certified_leaf_ledger']
    assert len(rawleaves)==67
    leaves=sorted(rawleaves,key=lambda row:F(row['interval'][0]))
    intervals=[tuple(map(F,row['interval'])) for row in leaves]
    assert intervals[0][0]==-radius and intervals[-1][1]==radius
    assert all(a<b for a,b in intervals)
    assert all(intervals[i][1]==intervals[i+1][0] for i in range(66))
    methods=Counter(); dens=Counter(); output=[]
    for index,(saved,interval) in enumerate(zip(leaves,intervals)):
        B,pints=verifier.B_interval(jets,interval,20)
        assert min(p[0] for p in pints)>0
        method=saved['method']; methods[method]+=1
        if method=='plain_gershgorin':
            assert saved['max_den'] is None and saved['preconditioner_upper_triangular'] is None
            P=[[F(i==j) for j in range(6)] for i in range(6)]; dens['plain']+=1
        else:
            assert method=='preconditioned_gershgorin'
            P=[[F(x) for x in row] for row in saved['preconditioner_upper_triangular']]
            assert len(P)==6 and all(len(row)==6 for row in P)
            assert all(P[i][j]==0 for i in range(6) for j in range(i))
            assert all(P[i][i]>0 for i in range(6))
            assert [P[i][i] for i in range(6)]==list(map(F,saved['preconditioner_diag']))
            cap=saved['max_den']; assert all(x.denominator<=cap for row in P for x in row)
            dens[str(cap)]+=1
        determinant=prod(P[i][i] for i in range(6)); assert determinant>0
        T,neg=rational_congruence(B,P); rowm=margins(T)
        assert min(rowm)>0
        assert min(rowm)==F(saved['min_margin'])
        assert min(p[0] for p in pints)==F(saved['min_atom_lower'])
        Tc=[[compact(x) for x in row] for row in T]
        compact_margins=margins(Tc); assert min(compact_margins)>0
        pfrob=sum(x*x for row in P for x in row)
        original_B_margin=min(compact_margins)/(pfrob if method!='plain_gershgorin' else F(1))
        output.append(dict(index=index,interval=interval,method=method,max_den=saved['max_den'],P=P,
            determinant_P=determinant,atom_intervals=pints,B_interval_outward_24digits=[[compact(x) for x in row] for row in B],
            transformed_interval_outward_24digits=Tc,exact_row_margins=rowm,compact_row_margins=compact_margins,
            min_atom_lower=min(p[0] for p in pints),negative_multiplication_weights_checked=neg,
            raw_B_uniform_lower_bound=original_B_margin))
    assert dict(methods)=={'preconditioned_gershgorin':65,'plain_gershgorin':2}
    assert dict(dens)=={'64':61,'256':3,'4096':1,'plain':2}
    minimum=min(min(row['exact_row_margins']) for row in output)
    atomfloor=min(row['min_atom_lower'] for row in output)
    assert minimum==F(author['largest_certified_min_margin'])
    assert atomfloor==F(author['largest_certified_min_atom_lower'])==F(15168331,7680000000)
    summary=next(a for a in author['attempts_summary'] if F(a['radius'])==radius)
    assert summary['passed']==67 and summary['failed']==0 and summary['splits']==66 and summary['success']
    assert summary['method_counts']==dict(methods)
    structure=verifier.structural_checks(K0,R,radius)
    assert structure['spectral_margin']==F(1,150)
    assert all(structure[k] for k in ('connected_on_closed_interval','heterogeneous_diagonal_on_closed_interval','distinct_spectrum_on_closed_interval'))
    affineabs=lambda a,b:min(abs(a-radius*b),abs(a+radius*b))
    structure['min_abs_offdiagonal']=min(affineabs(K0[i][j],R[i][j]) for i in range(3) for j in range(i+1,3))
    structure['min_diagonal_gap']=min(affineabs(K0[i][i]-K0[j][j],R[i][i]-R[j][j]) for i in range(3) for j in range(i+1,3))
    theta=(F(1,5),F(1,2),F(4,5)); rates=(F(1,5),F(1,3),F(2,3))
    structure['min_spectral_gap']=min(affineabs(theta[i]-theta[j],rates[i]-rates[j]) for i in range(3) for j in range(i+1,3))
    blocker=next(b for b in author['manual_blockers'] if F(b['radius'])==F(299,1000))
    assert blocker['status']=='TIMEOUT_INTERRUPTED' and F(blocker['spectral_margin'])==F(1,1500)
    assert hashes()==before,'author version drift'
    report=dict(status='CORRECT_FOR_29_OVER_100; EXTENSION_299_OVER_1000_INCOMPLETE',
        author_hashes_before=before,author_hashes_after=hashes(),non_author_helper_sha256=helper_hash,
        reconstructed_jets=jets,structure=structure,leaves=output,
        accounting=dict(leaves=67,preconditioned=65,plain=2,splits=66,denominator_caps=dict(dens),
                        atom_leaf_intervals=536,hessian_entry_leaf_intervals=2412,grid_points_used_for_proof=0),
        min_transformed_margin=minimum,min_transformed_margin_decimal=verifier.dec(minimum),
        min_atom_lower=atomfloor,uniform_raw_B_bound=min(row['raw_B_uniform_lower_bound'] for row in output),
        manual_extension_status='INCOMPLETE_NOT_REPLAYED_TIMEOUT_NOT_COUNTEREXAMPLE',
        elapsed_seconds=time.time()-start,exit_code=0,script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (HERE/'independent_s8b_results.json').write_text(json.dumps(verifier.serialize(report),indent=2)+'\n')
    print(json.dumps(verifier.serialize({k:report[k] for k in ('status','accounting','min_transformed_margin_decimal','min_atom_lower','structure','elapsed_seconds','exit_code')}),indent=2))
if __name__=='__main__': main()
