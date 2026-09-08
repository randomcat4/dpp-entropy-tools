"""Independent round-9 audit: principal-minor jets -> direct Mobius inversion.

No author module is imported. Writes only next to this script. Decimal logs
are convergence checks, not directed-rounding interval certificates.
"""
from __future__ import annotations
import csv
import hashlib
import json
import math
import os
import time
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[name] = '1'
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def determinant_jet(matrix, velocity=None):
    """SPD principal-minor determinant using elimination; derivatives via solve."""
    n = len(matrix)
    if not n:
        return [Decimal(1), Decimal(0), Decimal(0)]
    a = [row[:] for row in matrix]
    b = None if velocity is None else [row[:] for row in velocity]
    det = Decimal(1)
    # All input matrices here are principal submatrices of a positive kernel.
    # No pivoting or mixed-event matrix is used.
    for j in range(n):
        assert a[j][j] > 0
        det *= a[j][j]
        for i in range(j + 1, n):
            multiplier = a[i][j] / a[j][j]
            for k in range(j + 1, n):
                a[i][k] -= multiplier * a[j][k]
            if b is not None:
                for k in range(n):
                    b[i][k] -= multiplier * b[j][k]
    if b is None:
        return [det, Decimal(0), Decimal(0)]
    x = [[Decimal(0)] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(n):
            x[i][j] = (b[i][j] - sum(a[i][k] * x[k][j] for k in range(i + 1, n))) / a[i][i]
    trace = sum(x[i][i] for i in range(n))
    trace_square = sum(x[i][j] * x[j][i] for i in range(n) for j in range(n))
    return [det, det * trace, det * (trace * trace - trace_square)]

def atoms_by_mobius(k, d=None):
    n = len(k)
    jets = []
    for mask in range(1 << n):
        indices = [i for i in range(n) if mask >> i & 1]
        a = [[k[i][j] for j in indices] for i in indices]
        b = None if d is None else [[d[i][j] for j in indices] for i in indices]
        jets.append(determinant_jet(a, b))
    for i in range(n):
        for mask in range(1 << n):
            if not mask >> i & 1:
                jets[mask] = [a-b for a,b in zip(jets[mask], jets[mask | (1 << i)])]
    assert all(row[0] > 0 for row in jets)
    return jets

def summaries(jets):
    h = -sum(p * p.ln() for p, _, _ in jets)
    h1 = -sum(p1 * p.ln() for p, p1, _ in jets)
    f = sum(p1 * p1 / p for p, p1, _ in jets)
    acc = -sum(p2 * p.ln() for p, _, p2 in jets)
    return dict(H=h, H1=h1, F=f, acceleration=acc, H2=acc-f, rho=acc/f,
                min_p=min(row[0] for row in jets), sum_p=sum(row[0] for row in jets),
                sum_p1=sum(row[1] for row in jets), sum_p2=sum(row[2] for row in jets))

def ledger_audit():
    allrows = []
    shards = []
    hashes = {}
    original=np.load(ROOT/'source.npz')['kernel']
    original_spectrum,original_q=np.linalg.eigh((original+original.T)/2)
    for shard in range(4):
        folder = ROOT / f'results_{shard}'
        with (folder/'candidate_ledger.csv').open(newline='', encoding='utf-8') as handle:
            rows = list(csv.DictReader(handle))
        manifest = json.loads((folder/'manifest.json').read_text())
        saved = json.loads((folder/'best_case.json').read_text())
        assert len(rows) == 5000
        assert [int(row['index']) for row in rows] == list(range(5000))
        numeric = [key for key in rows[0] if key not in ('label','status','unrestricted_same_sign')]
        assert all(math.isfinite(float(row[key])) for row in rows for key in numeric)
        candidates = sum(row['status']=='FLOAT_CANDIDATE' for row in rows)
        assert candidates == manifest['positive_count'] == 0
        assert all(row['status']=='NO_HIT' for row in rows)
        assert manifest['centers']==5000 and manifest['n']==12 and manifest['exit_code']==0
        assert manifest['seed']==2026090816+shard
        assert all(float(row['margin']) >= .01-1e-14 for row in rows)
        assert all(float(row['direction_min_rate'])>0 for row in rows)
        assert all(float(row['rho_psd']) <= float(row['rho_unrestricted'])+1e-10 for row in rows)
        assert all(abs(float(row['total_psd_fisher_normalized'])-(float(row['rho_psd'])-1))<1e-13 for row in rows)
        best = max(rows,key=lambda row:float(row['rho_psd']))
        assert int(best['index'])==saved['index']
        for key in numeric:
            assert float(best[key]) == float(saved[key])
        assert float(best['rho_psd'])==manifest['best_rho_psd']
        assert float(best['chord_gap'])==manifest['best_gap']
        logrows=[json.loads(line) for line in (ROOT/f'run_{shard}.log').read_text().splitlines() if line.strip()]
        assert [entry['completed'] for entry in logrows[:-1]]==list(range(5,5001,5))
        assert logrows[-1]==manifest
        frozen=np.load(folder/'best_case.npz')
        rng=np.random.default_rng(manifest['seed'])
        maximum_margin_error=0.0
        best_spectrum_error=None
        for index,row in enumerate(rows):
            mode=index%4
            if mode==0:
                epsilon=(index//4%9)/1000
                spec=(1-2*epsilon)*original_spectrum+epsilon+rng.normal(0,.025,12)
            elif mode==1:
                spec=np.concatenate((rng.uniform(.01,.18,6),rng.uniform(.82,.99,6)))
                rng.shuffle(spec)
            elif mode==2:
                spec=1/(1+np.exp(-rng.uniform(-4.4,4.4,12)))
            else:
                spec=rng.choice(np.array([.03,.12,.5,.88,.97]),size=12)+rng.normal(0,.012,12)
            spec=np.clip(spec,.01,.99)
            # The optimizer consumes exactly this initial-seed draw per center.
            rng.normal(0,1.2,(8,12))
            error=abs(float(np.minimum(spec,1-spec).min())-float(row['margin']))
            maximum_margin_error=max(maximum_margin_error,error)
            if index==int(best['index']):
                best_spectrum_error=float(np.max(abs(spec-frozen['spectrum'])))
        assert maximum_margin_error<2e-14 and best_spectrum_error<2e-14
        fk=frozen['kernel']; fd=frozen['direction']; fq=frozen['eigenvectors']; fr=frozen['rates']
        assert np.max(abs(fk-(fq*frozen['spectrum'])@fq.T))<2e-14
        assert np.max(abs(fd-(fq*fr)@fq.T))<2e-14
        npz_projection,_=float_projection((fk+fk.T)/2,(fd+fd.T)/2,fq,fr)
        assert abs(npz_projection['rho_stored']-float(best['rho_psd']))<2e-12
        assert abs(npz_projection['rho_max']-float(best['rho_unrestricted']))<2e-12
        mode_counts = {str(i):sum(int(row['mode'])==i for row in rows) for i in range(4)}
        shards.append(dict(shard=shard, rows=len(rows), candidates=candidates, manifest=manifest,
                           mode_counts=mode_counts, best_index=int(best['index']),
                           max_gap=max(float(row['chord_gap']) for row in rows),
                           max_unrestricted=max(float(row['rho_unrestricted']) for row in rows),
                           same_sign_count=sum(row['unrestricted_same_sign']=='True' for row in rows),
                           seed_replay_margin_max_error=maximum_margin_error,
                           best_spectrum_seed_replay_max_error=best_spectrum_error,
                           best_npz_projection=npz_projection))
        allrows.extend(dict(row, shard=shard) for row in rows)
        for name in ('candidate_ledger.csv','manifest.json','best_case.json','best_case.npz'):
            hashes[f'results_{shard}/{name}']=sha(folder/name)
        hashes[f'run_{shard}.log']=sha(ROOT/f'run_{shard}.log')
    for name in ('README.md','recheck_best.py','recheck_best.json','source.npz'):
        hashes[name]=sha(ROOT/name)
    hashes['../commuting_spectral_search.py']=sha(ROOT.parent/'commuting_spectral_search.py')
    best=max(allrows,key=lambda row:float(row['rho_psd']))
    return dict(rows=len(allrows), shards=shards,best=best,hashes=hashes,
                max_unrestricted=max(float(row['rho_unrestricted']) for row in allrows),
                max_gap=max(float(row['chord_gap']) for row in allrows),
                positive_gap_count=sum(float(row['chord_gap'])>0 for row in allrows))

def ldl(a):
    """Exact rational Schur complements; returns every positive pivot."""
    a=[row[:] for row in a]
    pivots=[]
    for i in range(len(a)):
        pivot=a[i][i]
        assert pivot>0
        pivots.append(pivot)
        for j in range(i+1,len(a)):
            for k in range(j,len(a)):
                a[j][k]-=a[j][i]*a[k][i]/pivot
                a[k][j]=a[j][k]
    return [str(p) for p in pivots]

def exact_certificate(k,d):
    k=[[Fraction(x) for x in row] for row in k]
    d=[[Fraction(x) for x in row] for row in d]
    n=len(k)
    result={'radius':'1/200','margin':'1/2000','D_LDL':ldl(d),'endpoints':[]}
    for t in (Fraction(-1,200),Fraction(1,200)):
        a=[[k[i][j]+t*d[i][j] for j in range(n)] for i in range(n)]
        lower=[[a[i][j]-Fraction(i==j,2000) for j in range(n)] for i in range(n)]
        upper=[[Fraction(1999,2000)*(i==j)-a[i][j] for j in range(n)] for i in range(n)]
        result['endpoints'].append(dict(t=str(t),lower_LDL=ldl(lower),upper_LDL=ldl(upper)))
    comm=[[sum(k[i][r]*d[r][j]-d[i][r]*k[r][j] for r in range(n)) for j in range(n)] for i in range(n)]
    result['exact_commutator_nonzero_entries']=sum(x!=0 for row in comm for x in row)
    result['exact_commutator_max_abs']=str(max(abs(x) for row in comm for x in row))
    result['entry_denominators']=dict(K=sorted(set(str(x.denominator) for row in k for x in row)),
                                      D=sorted(set(str(x.denominator) for row in d for x in row)))
    return result

def float_projection(k,d,q,rates):
    # Direct coordinate diagonalization Q^T A_event^{-1} Q, independent of
    # the author's batch tensor contractions.
    n=len(k); f=np.zeros((n,n)); acc=np.zeros((n,n)); p_all=[]; scores=[]; seconds=[]
    for mask in range(1<<n):
        a=k-np.diag([1-(mask>>i&1) for i in range(n)])
        p=float(np.linalg.det(a))*(-1)**(n-mask.bit_count())
        c=q.T@np.linalg.solve(a,q)
        s=np.diag(c)
        second=np.outer(s,s)-c*c.T
        f+=p*np.outer(s,s)
        acc-=p*math.log(p)*second
        p_all.append(p); scores.append(p*(s@rates)); seconds.append(p*(rates@second@rates))
    vals,vecs=np.linalg.eigh((f+f.T)/2)
    w=vecs/np.sqrt(vals)
    eigenvalues,eigenvectors=np.linalg.eigh(w.T@acc@w)
    v=w@eigenvectors[:,-1]
    return dict(rho_max=float(eigenvalues[-1]),rho_stored=float(rates@acc@rates/(rates@f@rates)),
                fisher=float(rates@f@rates), acceleration=float(rates@acc@rates),
                top_same_sign=bool(np.all(v>0) or np.all(v<0)),
                fisher_min_eig=float(vals[0]),fisher_condition=float(vals[-1]/vals[0])),np.array([p_all,scores,seconds]).T

def main():
    started=time.time()
    ledgers=ledger_audit()
    shard=ledgers['best']['shard']
    data=np.load(ROOT/f'results_{shard}'/'best_case.npz')
    rawk=data['kernel']; rawd=data['direction']; q=data['eigenvectors']; rates=data['rates']; spectrum=data['spectrum']
    k=(rawk+rawk.T)/2; d=(rawd+rawd.T)/2
    integrity=dict(K_rebuild_max=float(np.max(abs(rawk-(q*spectrum)@q.T))),
                   D_rebuild_max=float(np.max(abs(rawd-(q*rates)@q.T))),
                   Q_orthogonality_max=float(np.max(abs(q.T@q-np.eye(len(k))))),
                   K_symmetry=float(np.max(abs(rawk-rawk.T))),D_symmetry=float(np.max(abs(rawd-rawd.T))),
                   K_spectrum=np.linalg.eigvalsh(k).tolist(),D_spectrum=np.linalg.eigvalsh(d).tolist(),
                   rates=rates.tolist(),spectrum=spectrum.tolist())
    assert integrity['K_rebuild_max']<1e-14 and integrity['D_rebuild_max']<1e-14
    assert abs(float(rates.min())-float(ledgers['best']['direction_min_rate']))<1e-14
    assert abs(float(min(spectrum.min(),1-spectrum.max()))-float(ledgers['best']['margin']))<1e-14
    expected_step=min(.1*float(np.min(np.minimum(spectrum,1-spectrum)/rates)),.02)
    assert expected_step==float(ledgers['best']['chord_step'])
    projection,mixed=float_projection(k,d,q,rates)
    kd=[[Decimal(repr(float(x))) for x in row] for row in k]
    dd=[[Decimal(repr(float(x))) for x in row] for row in d]
    precision_runs=[]; old=None
    for precision in (50,80):
        with localcontext() as ctx:
            ctx.prec=precision
            jets=atoms_by_mobius(kd,dd)
            stats=summaries(jets)
            agreement=None if old is None else [str(max(abs(a[i]-b[i]) for a,b in zip(jets,old))) for i in range(3)]
            precision_runs.append(dict(precision=precision,events=len(jets),**{key:str(v) for key,v in stats.items()},max_atom_jet_change=agreement))
            old=jets
        print(f'precision {precision} rho {stats["rho"]} H2 {stats["H2"]}',flush=True)
    with localcontext() as ctx:
        ctx.prec=80
        chord_rows=[]
        for step in (ledgers['best']['chord_step'],'0.001','0.0001'):
            t=Decimal(step)
            ent=[]
            for sign in (-1,1):
                shifted=[[x+sign*t*y for x,y in zip(a,b)] for a,b in zip(kd,dd)]
                events=atoms_by_mobius(shifted)
                ent.append(-sum(p*p.ln() for p,_,_ in events))
            gap=sum(ent)/2-stats['H']
            chord_rows.append(dict(t=step,Hminus=str(ent[0]),Hplus=str(ent[1]),gap=str(gap),central_H2=str(2*gap/t**2)))
            assert gap<0
            print(f'chord {step} gap {gap}',flush=True)
    (HERE/'atom_jets_80.json').write_text(json.dumps([[str(x) for x in row] for row in jets],indent=1)+'\n',encoding='utf-8')
    certificate=exact_certificate(kd,dd)
    author=json.loads((ROOT/'recheck_best.json').read_text())
    last=author['decimal_directional'][-1]
    mapping={'H':'entropy','F':'fisher','acceleration':'acceleration','H2':'H2','rho':'rho'}
    differences={key:str(abs(stats[key]-Decimal(last[alias]))) for key,alias in mapping.items()}
    report=dict(ledger=ledgers,integrity=integrity,projection=projection,decimal=precision_runs,chords=chord_rows,
                author_comparison_abs=differences,exact_certificate=certificate,
                mixed_float_vs_mobius80_jet_max=np.max(abs(mixed-np.array([[float(x) for x in row] for row in jets])),axis=0).tolist(),
                denominator=dict(scout_rows=20000,high_precision_centers=1,events_per_center=4096,precision_passes=2,
                                 actual_chords=3,endpoint_event_evaluations=24576,exact_LDL_matrices=5),
                hashes=dict(script=sha(Path(__file__)),atom_jets_80=sha(HERE/'atom_jets_80.json')),
                exit_code=0,elapsed_seconds=time.time()-started)
    (HERE/'fresh_check.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'rows':20000,'best':ledgers['best'],'elapsed_seconds':report['elapsed_seconds'],'exit_code':0},indent=2))

if __name__=='__main__':
    main()
