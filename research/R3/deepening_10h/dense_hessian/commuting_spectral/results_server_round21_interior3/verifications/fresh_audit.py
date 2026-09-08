"""Independent round21 audit. No author modules imported; 120-digit Mobius jets.

Run from repository root with Python; numpy is used only to load frozen NPZ
and report non-rigorous floating diagnostics. All determinant arithmetic below
is independently implemented using Decimal or Fraction.
"""
import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[name] = '1'
import sys
sys.dont_write_bytecode = True
sys.set_int_max_str_digits(0)
import csv, hashlib, json, time
from pathlib import Path
from decimal import Decimal as R, getcontext
from fractions import Fraction as Q
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
getcontext().prec = 120
ZERO, ONE = R(0), R(1)

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def mul(a,b):
    return (a[0]*b[0], a[0]*b[1]+a[1]*b[0], a[0]*b[2]+a[1]*b[1]+a[2]*b[0])

def div(a,b):
    x=a[0]/b[0]
    y=(a[1]-x*b[1])/b[0]
    return (x,y,(a[2]-x*b[2]-y*b[1])/b[0])

def det_jet(K,D,ids):
    # Coefficients through t^2, not raw second derivatives.
    a=[[(K[i][j],D[i][j],ZERO) for j in ids] for i in ids]
    ans=(ONE,ZERO,ZERO)
    for k in range(len(ids)):
        # Principal SPD matrices have nonzero unpivoted pivots.
        ans=mul(ans,a[k][k])
        for i in range(k+1,len(ids)):
            ratio=div(a[i][k],a[k][k])
            for j in range(k+1,len(ids)):
                b=mul(ratio,a[k][j])
                a[i][j]=tuple(a[i][j][z]-b[z] for z in range(3))
    return ans

def det(a):
    a=[row[:] for row in a]
    ans=ONE
    for k in range(len(a)):
        r=max(range(k,len(a)),key=lambda i:abs(a[i][k]))
        if not a[r][k]: return ZERO
        if r!=k: a[r],a[k]=a[k],a[r]; ans=-ans
        ans*=a[k][k]
        for i in range(k+1,len(a)):
            ratio=a[i][k]/a[k][k]
            for j in range(k+1,len(a)): a[i][j]-=ratio*a[k][j]
    return ans

def mobius_jets(K,D):
    n=len(K)
    a=[det_jet(K,D,[i for i in range(n) if mask>>i&1]) for mask in range(1<<n)]
    for i in range(n):
        for mask in range(1<<n):
            if not mask>>i&1:
                a[mask]=tuple(a[mask][z]-a[mask|1<<i][z] for z in range(3))
    return [(p,d,2*e) for p,d,e in a]

def event_probs(K):
    n=len(K); ans=[]
    for mask in range(1<<n):
        a=[row[:] for row in K]
        for i in range(n):
            if not mask>>i&1: a[i][i]-=ONE
        ans.append((-1 if (n-mask.bit_count())%2 else 1)*det(a))
    assert min(ans)>0
    return ans

def entropy(p): return -sum(x*x.ln() for x in p)

def ldl(a):
    a=[r[:] for r in a]; out=[]
    for k in range(len(a)):
        pivot=a[k][k]; assert pivot>0, (k,pivot)
        out.append(pivot)
        for i in range(k+1,len(a)):
            for j in range(i,len(a)):
                a[j][i]=a[i][j]=a[i][j]-a[i][k]*a[k][j]/pivot
    return {'all_positive':True,'count':len(out),'min_float':float(min(out)),
            'exact_pivots':[str(v) for v in out]}

def main():
    started=time.time()
    files=sorted(p for p in ROOT.iterdir() if p.is_file())
    for s in range(4): files+=sorted(p for p in (ROOT/f'results_{s}').iterdir() if p.is_file())
    frozen={str(p.relative_to(ROOT)):sha(p) for p in files}
    result={'precision':120,'frozen_sha256':frozen,'audit_source_sha256':sha(Path(__file__)),
            'interpretation':'numpy-symmetrized entries, shortest decimal strings, exact rational values',
            'full_seed_regeneration':'INCOMPLETE: not executed', 'shards':[]}
    allrows=[]
    for s in range(4):
        folder=ROOT/f'results_{s}'
        rows=list(csv.DictReader((folder/'candidate_ledger.csv').open(encoding='utf-8')))
        m=json.loads((folder/'manifest.json').read_text())
        logs=[json.loads(line) for line in (ROOT/f'run_{s}.log').read_text().splitlines() if line.startswith('{')]
        assert len(rows)==5001 and [int(r['index']) for r in rows]==list(range(-1,5000))
        assert rows[0]['label']=='source_base' and m['proposal_count']==5000
        assert m['ledger_rows_including_source']==5001 and m['margin_floor']==.1
        assert m['seed']==2026090874+s and m['exit_code']==0 and m['positive_count']==0
        assert logs[-1]==m
        assert [r['completed'] for r in logs[:-1]]==list(range(5,5001,5))
        rolling=float(rows[0]['rho_psd'])
        for idx,row in enumerate(rows[1:]):
            rolling=max(rolling,float(row['rho_psd']))
            if (idx+1)%5==0: assert logs[idx//5]['best_rho_psd']==rolling
        assert abs(float(rows[0]['spectrum_margin'])-.12)<1e-15
        assert sum(r['accepted']=='True' for r in rows[1:])==m['accepted_count']
        assert all(r['status']=='NO_HIT' and float(r['rho_psd'])<1 and float(r['rho_unrestricted'])<1
                   and float(r['chord_gap'])<0 and float(r['total_psd_fisher_normalized'])<0 for r in rows)
        assert all(float(r['spectrum_margin'])>=.1-5e-17 for r in rows[1:])
        assert all(abs(float(r['total_psd_fisher_normalized'])-(float(r['rho_psd'])-1))<1e-14 for r in rows)
        best=max(rows,key=lambda r:float(r['rho_psd']))
        bj=json.loads((folder/'best_case.json').read_text())
        assert int(best['index'])==bj['index'] and float(best['rho_psd'])==bj['rho_psd']==m['best_rho_psd']
        result['shards'].append({'shard':s,'rows':len(rows),'source_rows':1,'proposals':5000,
          'manifest':m,'log_progress_rows':len(logs)-1,'best_index':int(best['index']),
          'min_ledger_margin':min(float(r['spectrum_margin']) for r in rows),
          'max_gap':max(float(r['chord_gap']) for r in rows),'best_rho':float(best['rho_psd'])})
        allrows += [dict(r,shard=s) for r in rows]
    best=max(allrows,key=lambda r:float(r['rho_psd']))
    assert best['shard']==0 and best['index']=='70' and float(best['rho_psd'])==.5313886643536545
    result['denominator']={'rows':len(allrows),'proposals':20000,'source_copies':4,
                           'positive_curvature_or_gap':0,'rho_ge_one':0}
    result['best_row']=best
    z=np.load(ROOT/'results_0/best_case.npz')
    k=(z['kernel']+z['kernel'].T)/2
    d=(z['direction']+z['direction'].T)/2
    result['float_structure']={'n':len(k),'K_min':float(np.linalg.eigvalsh(k)[0]),
      'K_max':float(np.linalg.eigvalsh(k)[-1]),'D_min':float(np.linalg.eigvalsh(d)[0]),
      'commutator_F':float(np.linalg.norm(k@d-d@k)),
      'K_basis_reconstruction_error':float(np.linalg.norm(k-z['eigenvectors']@np.diag(z['spectrum'])@z['eigenvectors'].T)),
      'D_basis_reconstruction_error':float(np.linalg.norm(d-z['eigenvectors']@np.diag(z['rates'])@z['eigenvectors'].T))}
    src=np.load(ROOT/'interior_source_margin012.npz')
    result['source']={'margin_from_spectrum':float(np.min(np.minimum(src['spectrum'],1-src['spectrum']))),
                     'metadata':json.loads((ROOT/'interior_source_margin012.json').read_text())}
    assert abs(result['source']['margin_from_spectrum']-.12)<1e-15
    h10path=ROOT.parent/'results_server_round18_boundary1/results_2/best_case.npz'
    h10=np.load(h10path)
    scale=(.5-.12)/np.max(abs(h10['spectrum']-.5))
    assert np.array_equal(src['eigenvectors'],h10['eigenvectors'])
    assert np.array_equal(src['spectrum'],.5+scale*(h10['spectrum']-.5))
    result['source']['H10_npz_sha256']=sha(h10path)
    result['source']['affine_spectral_contraction_reproduced']=True
    result['margin_profile']=[]
    for round_name,tag in [('results_server_round18_boundary1','H10'),
                           ('results_server_round19_interior1','H11'),
                           ('results_server_round20_interior2','H12'),
                           (ROOT.name,'H13')]:
        candidates=[]
        for s in range(4):
            path=ROOT.parent/round_name/f'results_{s}/best_case.json'
            rec=json.loads(path.read_text())
            candidates.append((rec['rho_psd'],s,rec,path))
        rho,s,rec,path=max(candidates,key=lambda v:v[0])
        result['margin_profile'].append({'tag':tag,'best_rho':rho,'best_shard':s,
          'best_center_spectrum_margin':rec['spectrum_margin'],
          'best_json_sha256':sha(path),'relative_source':str(path.relative_to(ROOT.parent))})
    K=[[R(str(float(x))) for x in r] for r in k]
    D=[[R(str(float(x))) for x in r] for r in d]
    result['exact_decimal_K']=[[str(x) for x in r] for r in K]
    result['exact_decimal_D']=[[str(x) for x in r] for r in D]
    kq=[[Q(x) for x in r] for r in K]; dq=[[Q(x) for x in r] for r in D]
    cert={'D':ldl(dq),'endpoints':[]}
    for t in (Q(-1,200),Q(1,200)):
        low=[[kq[i][j]+t*dq[i][j]-Q(i==j,2000) for j in range(len(k))] for i in range(len(k))]
        high=[[Q(i==j)-kq[i][j]-t*dq[i][j]-Q(i==j,2000) for j in range(len(k))] for i in range(len(k))]
        cert['endpoints'].append({'t':str(t),'K_minus_margin':ldl(low),'I_minus_K_minus_margin':ldl(high)})
    result['rational_LDL']=cert
    print('Ledger and Fraction LDL passed; computing 4096 independent inclusion jets',flush=True)
    jets=mobius_jets(K,D); p=[x[0] for x in jets]
    pe=event_probs(K)
    err=max(abs(a-b) for a,b in zip(p,pe))
    assert err<R('1e-110') and min(p)>0
    H=entropy(p); F=sum(d*d/p for p,d,e in jets); A=-sum(e*p.ln() for p,d,e in jets)
    result['mobius_120']={key:str(value) for key,value in dict(H=H,Fisher=F,acceleration=A,H2=A-F,rho=A/F,
      min_atom=min(p),sum_p=sum(p),sum_p1=sum(x[1] for x in jets),sum_p2=sum(x[2] for x in jets),
      signed_event_max_error=err).items()}
    assert A<F and abs(A/F-R(best['rho_psd']))<R('1e-13')
    result['chords']=[]
    for denom in (200,1000,10000):
        t=ONE/denom
        hm=entropy(event_probs([[K[i][j]-t*D[i][j] for j in range(len(k))] for i in range(len(k))]))
        hp=entropy(event_probs([[K[i][j]+t*D[i][j] for j in range(len(k))] for i in range(len(k))]))
        gap=(hm+hp)/2-H
        assert gap<0
        result['chords'].append({'step':f'1/{denom}','Hminus':str(hm),'Hplus':str(hp),
                                'gap':str(gap),'central_H2':str(2*gap/t**2)})
        print('Chord',denom,'gap',str(gap)[:28],flush=True)
    result['frozen_files_unchanged']=all(sha(ROOT/name)==h for name,h in frozen.items())
    assert result['frozen_files_unchanged']
    result['verdict']={'frozen_point_and_accounting':'CORRECT','finite_search':'SCOUT',
                       'full_seed_regeneration':'INCOMPLETE','general_concavity':'INCOMPLETE'}
    result['exit_code']=0;result['elapsed_seconds']=time.time()-started
    (HERE/'fresh_audit.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({'H2':str(A-F),'rho':str(A/F),'elapsed':result['elapsed_seconds'],'exit_code':0}),flush=True)

if __name__=='__main__': main()
