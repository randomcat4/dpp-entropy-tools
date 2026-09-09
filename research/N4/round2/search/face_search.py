"""F1: 72 fixed rational 4x3 faces/centers; 60-digit numerical scout only."""
import os
for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[key] = '1'
import argparse
from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path
import platform
import sys
import time
import mpmath as mp
import numpy as np
import scipy

mp.mp.dps = 60
SEED = 202609090427
PAIRS = [(0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2)]
SCALES = np.array([1., 1., 1., 2**.5, 2**.5, 2**.5])
FRAMES = [(1,1,1,1), (1,2,3,4), (1,1,1,5), (1,2,4,1), (1,1,4,4), (1,2,2,2)]
SPECTRA = [
    ('isotropic', ['2/5','2/5','2/5']),
    ('moderate', ['1/8','1/2','7/8']),
    ('sparse', ['1/10000','1/500','1/20']),
    ('dense', ['19/20','499/500','9999/10000']),
    ('one_zero', ['1/10000','1/3','4/5']),
    ('two_zero', ['1/10000','1/1000','3/4']),
    ('one_one', ['1/5','2/3','9999/10000']),
    ('two_one', ['1/4','999/1000','9999/10000']),
    ('split_extreme', ['1/10000','1/2','9999/10000']),
    ('split_low', ['1/10000','1/100','999/1000']),
    ('split_high', ['1/1000','99/100','9999/10000']),
    ('cluster_mid', ['49/100','1/2','51/100']),
]
COUNTS = dict(center_attempts=0, center_completed=0, proper_event_jet_calls=0,
              hessian_calls=0, entropy_calls=0, proper_entropy_determinants=0,
              chord_calls=0, exact_endpoint_pd_checks=0, exact_jet_selfchecks=0)

def eye(n): return [[Q(i == j) for j in range(n)] for i in range(n)]
def trans(a): return list(map(list, zip(*a)))
def mul(a,b): return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def add(a,b,c=Q(1)): return [[x+c*y for x,y in zip(r,s)] for r,s in zip(a,b)]
def hh(w):
    d=sum(x*x for x in w)
    return [[Q(i==j)-Q(2*w[i]*w[j],d) for j in range(len(w))] for i in range(len(w))]
def mpq(x): return mp.mpf(x.numerator)/x.denominator
def mpmat(a): return mp.matrix([[mpq(x) for x in row] for row in a])
def asfloat(a): return np.array([[float(x) for x in row] for row in a])
def rational_strings(a): return [[str(x) for x in row] for row in a]
def decimals(a):
    if isinstance(a, mp.matrix): return [[mp.nstr(a[i,j],55) for j in range(a.cols)] for i in range(a.rows)]
    return [mp.nstr(x,55) for x in a]
def trace(a): return sum(a[i,i] for i in range(a.rows))
def trprod(a,b): return sum(a[i,j]*b[j,i] for i in range(a.rows) for j in range(a.cols))

BASES=[]
for i,j in PAIRS:
    b=[[Q(0)]*3 for _ in range(3)]
    b[i][j]=b[j][i]=Q(1)
    BASES.append(b)

def exactdet(a):
    n=len(a)
    return sum((-1)**sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))
               * product(a[i][p[i]] for i in range(n)) for p in itertools.permutations(range(n)))
def product(xs):
    r=Q(1)
    for x in xs: r*=x
    return r
def positive_definite(a):
    COUNTS['exact_endpoint_pd_checks']+=1
    return all(exactdet([row[:k] for row in a[:k]])>0 for k in (1,2,3))

def entropy(u,a):
    COUNTS['entropy_calls']+=1
    k=mpmat(mul(mul(u,a),trans(u)))
    terms=[]
    for s in range(15):
        mat=k.copy()
        for i in range(4):
            if not (s>>i)&1: mat[i,i]-=1
        p=(-1)**(4-s.bit_count())*mp.det(mat)
        COUNTS['proper_entropy_determinants']+=1
        if p<=0: raise ArithmeticError('proper event not positive')
        terms.append(-p*mp.log(p))
    return sum(terms)

def hessian(u,a):
    COUNTS['hessian_calls']+=1
    k=mpmat(mul(mul(u,a),trans(u)))
    ds=[mpmat(mul(mul(u,b),trans(u))) for b in BASES]
    ps=[]; gs=[]; js=[]
    fisher=mp.zeros(6); acceleration=mp.zeros(6)
    for s in range(15):
        mat=k.copy()
        for i in range(4):
            if not (s>>i)&1: mat[i,i]-=1
        p=(-1)**(4-s.bit_count())*mp.det(mat)
        if p<=0: raise ArithmeticError('proper event not positive')
        inverse=mat**-1
        bs=[inverse*d for d in ds]
        ts=[trace(b) for b in bs]
        g=mp.matrix([p*t for t in ts]); j=mp.zeros(6)
        for x in range(6):
            for y in range(x,6):
                j[x,y]=j[y,x]=p*(ts[x]*ts[y]-trprod(bs[x],bs[y]))
                f=g[x]*g[y]/p; ac=-mp.log(p)*j[x,y]
                fisher[x,y]+=f; acceleration[x,y]+=ac
                if x!=y: fisher[y,x]+=f; acceleration[y,x]+=ac
        ps.append(p); gs.append(g); js.append(j)
        COUNTS['proper_event_jet_calls']+=1
    err_p=abs(sum(ps)-1)
    err_g=max(abs(sum(g[i] for g in gs)) for i in range(6))
    err_j=max(abs(sum(j[i,l] for j in js)) for i in range(6) for l in range(6))
    assert max(err_p,err_g,err_j)<mp.mpf('1e-42')
    return acceleration-fisher,fisher,acceleration,ps,gs,js,dict(
        normalization_error=mp.nstr(err_p,8),gradient_sum_error=mp.nstr(err_g,8),
        hessian_sum_error=mp.nstr(err_j,8),full_event='structural zero; never evaluated or divided by')

def detjet(a,d):
    """Independent exact Leibniz jet, only used as execution selfcheck."""
    ans=[Q(0)]*3
    for perm in itertools.permutations(range(4)):
        sign=(-1)**sum(perm[i]>perm[j] for i in range(4) for j in range(i+1,4))
        v=[Q(1),Q(0),Q(0)]
        for i,j in enumerate(perm):
            v=[v[0]*a[i][j],v[1]*a[i][j]+v[0]*d[i][j],v[2]*a[i][j]+v[1]*d[i][j]]
        ans=[x+sign*y for x,y in zip(ans,v)]
    return [ans[0],ans[1],2*ans[2]]

def exact_selfcheck(u,a,ps,gs,js):
    k=mul(mul(u,a),trans(u))
    # Mixed direction challenges cross Hessian entries.
    v=[[Q(2),Q(-1),Q(3)],[Q(-1),Q(1),Q(-2)],[Q(3),Q(-2),Q(-3)]]
    d=mul(mul(u,v),trans(u)); c=mp.matrix([mpq(v[i][j]) for i,j in PAIRS])
    errors=[]; full=None
    for s in range(16):
        mat=[[k[i][j]-Q(i==j and not (s>>i)&1) for j in range(4)] for i in range(4)]
        exact=[(-1)**(4-s.bit_count())*x for x in detjet(mat,d)]
        COUNTS['exact_jet_selfchecks']+=1
        if s==15:
            assert exact==[0,0,0];full=list(map(str,exact));continue
        got=[ps[s],(gs[s].T*c)[0],(c.T*js[s]*c)[0]]
        errors.extend(abs(mpq(x)-y) for x,y in zip(exact,got))
    assert max(errors)<mp.mpf('1e-42')
    return dict(max_absolute_error=mp.nstr(max(errors),10),full_event_jet_exact=full,
                scope='one mixed rational direction at first center, not independent review')

def radius(a,v):
    a=asfloat(a);v=asfloat(v);rr=[]
    for m in (a,np.eye(3)-a):
        e,q=np.linalg.eigh(m); w=(q/np.sqrt(e))@q.T
        rr.append(1/max(abs(np.linalg.eigvalsh(w@v@w))))
    return float(min(rr))

def centers():
    rng=np.random.default_rng(SEED)
    for fi,w in enumerate(FRAMES):
        frame=hh(w);u=[row[:3] for row in frame];z=[row[3] for row in frame]
        assert mul(trans(u),u)==eye(3) and all(z)
        for si,(name,spec) in enumerate(SPECTRA):
            rotvecs=[];rot=eye(3)
            if si:
                for _ in range(2):
                    r=list(map(int,rng.integers(-5,6,3)))
                    if not any(r): r[0]=1
                    rotvecs.append(r);rot=mul(rot,hh(r))
            eig=[Q(x) for x in spec]
            a=mul(mul(rot,[[eig[i] if i==j else Q(0) for j in range(3)] for i in range(3)]),trans(rot))
            yield u,a,z,dict(frame_index=fi,householder_w=list(w),spectrum_index=si,
                            spectrum_name=name,spectrum=spec,rotation_vectors=rotvecs)

def assess(index,u,a,z,meta,out):
    COUNTS['center_attempts']+=1
    h,f,ac,ps,gs,js,diag=hessian(u,a)
    if index==0: diag['exact_selfcheck']=exact_selfcheck(u,a,ps,gs,js)
    hf=np.array(h.tolist(),float)/np.outer(SCALES,SCALES)
    ev,evec=np.linalg.eigh(hf); cc=evec[:,-1]/SCALES
    v=[[Q(0)]*3 for _ in range(3)]
    for (i,j),x in zip(PAIRS,cc): v[i][j]=v[j][i]=Q(round(float(x)*10**9),10**9)
    c=mp.matrix([mpq(v[i][j]) for i,j in PAIRS]);r=radius(a,v)
    p1=[(g.T*c)[0] for g in gs];p2=[(c.T*j*c)[0] for j in js]
    eventf=[-d*d/p for d,p in zip(p1,ps)]
    eventa=[-d*mp.log(p) for d,p in zip(p2,ps)]
    layers=[]
    for size in range(4):
        ids=[s for s in range(15) if s.bit_count()==size]
        fs=sum(eventf[s] for s in ids);acs=sum(eventa[s] for s in ids)
        layers.append(dict(cardinality=size,mass=float(sum(ps[s] for s in ids)),
                           negative_fisher=float(fs),acceleration=float(acs),curvature=float(fs+acs)))
    h0=entropy(u,a);chords=[]
    for factor in (.03,.25,.75):
        t=Q(round(r*factor*10**12),10**12)
        assert t>0
        am=add(a,v,-t);ap=add(a,v,t)
        assert all(positive_definite(m) for m in (am,ap,add(eye(3),am,-1),add(eye(3),ap,-1)))
        gap=(entropy(u,am)+entropy(u,ap))/2-h0
        COUNTS['chord_calls']+=1
        chords.append(dict(radius_fraction=factor,t=str(t),gap=mp.nstr(gap,55),
                           exact_endpoint_sylvester_positive=True))
    vf=asfloat(v);af=asfloat(a)
    record=dict(index=index,meta=meta,U=rational_strings(u),A=rational_strings(a),z=list(map(str,z)),
                full_event_jet=['0','0','0'],basis_pairs=PAIRS,basis_normalization='raw symmetric, Frobenius scales [1,1,1,sqrt2,sqrt2,sqrt2]',
                hessian=decimals(h),fisher_positive=decimals(f),acceleration=decimals(ac),
                hessian_eigenvalues=ev.tolist(),lambda_max=float(ev[-1]),min_event=float(min(ps)),
                event_p=decimals(ps),event_gradient=[decimals(g.T)[0] for g in gs],
                event_hessian=[decimals(j) for j in js],diagnostic=diag,
                top_direction=dict(V=rational_strings(v),symmetric_radius_float=r,
                    curvature=mp.nstr((c.T*h*c)[0],55),negative_fisher=mp.nstr(-(c.T*f*c)[0],55),
                    acceleration=mp.nstr((c.T*ac*c)[0],55),commutator_norm=float(np.linalg.norm(af@vf-vf@af)),
                    event_dp=decimals(p1),event_ddp=decimals(p2),event_negative_fisher=decimals(eventf),
                    event_acceleration=decimals(eventa),cardinality_layers=layers,chords=chords))
    COUNTS['center_completed']+=1
    if (c.T*h*c)[0]>0 or any(mp.mpf(x['gap'])>0 for x in chords):
        record['status']='NUMERICAL_POSITIVE_CANDIDATE_NOT_CERTIFIED'
        candidate=out/f'candidate_{index:03d}.json'
        candidate.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
        print(json.dumps(dict(CANDIDATE=str(candidate),index=index,lambda_max=float(ev[-1]))),flush=True)
    return record

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',default='F1');args=parser.parse_args()
    out=Path(args.out);out.mkdir(parents=True,exist_ok=False)
    start=time.time();records=[];failures=[]
    manifest=dict(status='RUNNING',pid=os.getpid(),seed=SEED,source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  python=sys.version,numpy=np.__version__,scipy=scipy.__version__,mpmath=mp.__version__,
                  precision_digits=mp.mp.dps,platform=platform.platform(),argv=sys.argv,
                  thread_limits={k:os.environ[k] for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS')},
                  prescribed_centers=72,full_event_handling='structural zero excluded before all arithmetic',
                  classification='high precision numerical scout, no rigorous log enclosure, no class conclusion')
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    with (out/'cases.jsonl').open('w',encoding='utf-8') as handle:
        for index,(u,a,z,meta) in enumerate(centers()):
            try:
                rec=assess(index,u,a,z,meta,out);records.append(rec)
                handle.write(json.dumps(rec)+'\n');handle.flush()
                print(json.dumps(dict(index=index,frame=meta['frame_index'],spectrum=meta['spectrum_name'],
                      lambda_max=rec['lambda_max'],top_acceleration=float(rec['top_direction']['acceleration']))),flush=True)
            except Exception as exc:
                failures.append(dict(index=index,meta=meta,error=repr(exc)))
                print(json.dumps(failures[-1]),flush=True)
    manifest.update(status='COMPLETED' if not failures else 'COMPLETED_WITH_FAILURES',counts=COUNTS,
                    elapsed_seconds=time.time()-start,exit_status=0 if not failures else 1,
                    candidate_files=[p.name for p in out.glob('candidate_*.json')],failures=failures)
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    if records:
        for name,key in [('highest_curvature',lambda r:r['lambda_max']),
                         ('highest_top_acceleration',lambda r:float(r['top_direction']['acceleration']))]:
            (out/f'{name}.json').write_text(json.dumps(max(records,key=key),indent=2)+'\n',encoding='utf-8')
    print(json.dumps(manifest),flush=True)
    return manifest['exit_status']

if __name__=='__main__': raise SystemExit(main())
