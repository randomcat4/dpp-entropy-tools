"""F2 frozen 5x3 support probe; direct 26-event jets, not a log certificate."""
import face_search as core
from face_search import Q, mp, np, scipy, Path, json, os, time, hashlib, sys, platform
from face_search import mul, trans, hh, eye, mpmat, mpq, trace, trprod, add, exactdet
from face_search import BASES, PAIRS, SCALES, rational_strings, decimals, radius, positive_definite, asfloat
import argparse
import itertools

SEED=202609090529
SUPPORT=[s for s in range(32) if s.bit_count()<=3]
EXCLUDED=[s for s in range(32) if s.bit_count()>3]
BS=[(2,-1,3,-2,1),(2,-1,4,-2,1),(3,-1,3,-2,1)]
SPECTRA=[core.SPECTRA[i] for i in (1,2,3,4,5,6,8,11)]
COUNTS=dict(center_attempts=0,center_completed=0,hessian_calls=0,proper_event_jet_calls=0,
            entropy_calls=0,entropy_determinants=0,chord_calls=0,direction_evaluations=0,
            rational_frame_checks=0,exact_top_determinant_jet_calls=0)

def detjet3(a,v):
    ans=[Q(0)]*3
    for perm in itertools.permutations(range(3)):
        sign=(-1)**sum(perm[i]>perm[j] for i in range(3) for j in range(i+1,3))
        x=[Q(1),Q(0),Q(0)]
        for i,j in enumerate(perm):
            x=[x[0]*a[i][j],x[1]*a[i][j]+x[0]*v[i][j],x[2]*a[i][j]+x[1]*v[i][j]]
        ans=[z+sign*y for z,y in zip(ans,x)]
    COUNTS['exact_top_determinant_jet_calls']+=1
    return [ans[0],ans[1],2*ans[2]]

def entropy(u,a):
    COUNTS['entropy_calls']+=1;k=mpmat(mul(mul(u,a),trans(u)));terms=[]
    for s in SUPPORT:
        mat=k.copy()
        for i in range(5):
            if not (s>>i)&1:mat[i,i]-=1
        p=(-1)**(5-s.bit_count())*mp.det(mat)
        assert p>0
        terms.append(-p*mp.log(p));COUNTS['entropy_determinants']+=1
    return sum(terms)

def hessian(u,a):
    COUNTS['hessian_calls']+=1
    k=mpmat(mul(mul(u,a),trans(u)))
    ds=[mpmat(mul(mul(u,b),trans(u))) for b in BASES]
    ps=[];gs=[];js=[];f=mp.zeros(6);ac=mp.zeros(6)
    for s in SUPPORT:
        mat=k.copy()
        for i in range(5):
            if not (s>>i)&1:mat[i,i]-=1
        p=(-1)**(5-s.bit_count())*mp.det(mat)
        assert p>0
        inv=mat**-1;bb=[inv*d for d in ds];tt=[trace(b) for b in bb]
        g=mp.matrix([p*t for t in tt]);j=mp.zeros(6)
        for x in range(6):
            for y in range(x,6):
                j[x,y]=j[y,x]=p*(tt[x]*tt[y]-trprod(bb[x],bb[y]))
                ff=g[x]*g[y]/p;aa=-mp.log(p)*j[x,y]
                f[x,y]+=ff;ac[x,y]+=aa
                if x!=y:f[y,x]+=ff;ac[y,x]+=aa
        ps.append(p);gs.append(g);js.append(j);COUNTS['proper_event_jet_calls']+=1
    diag=dict(normalization_error=mp.nstr(abs(sum(ps)-1),10),
              gradient_sum_error=mp.nstr(max(abs(sum(g[i] for g in gs)) for i in range(6)),10),
              hessian_sum_error=mp.nstr(max(abs(sum(j[i,l] for j in js)) for i in range(6) for l in range(6)),10))
    assert all(mp.mpf(x)<mp.mpf('1e-40') for x in diag.values())
    return ac-f,f,ac,ps,gs,js,diag

def centers():
    rng=np.random.default_rng(SEED)
    for fi,b in enumerate(BS):
        frame=mul(hh([1,2,3,4,5]),hh(b));u=[row[:3] for row in frame]
        assert mul(trans(u),u)==eye(3)
        q={s:exactdet([u[i] for i in range(5) if (s>>i)&1])**2 for s in SUPPORT if s.bit_count()==3}
        assert all(x>0 for x in q.values()) and sum(q.values())==1
        COUNTS['rational_frame_checks']+=1
        for si,(name,spec) in enumerate(SPECTRA):
            rot=eye(3);rotvecs=[]
            for _ in range(2):
                w=list(map(int,rng.integers(-5,6,3)))
                if not any(w):w[0]=1
                rotvecs.append(w);rot=mul(rot,hh(w))
            eig=[Q(x) for x in spec]
            a=mul(mul(rot,[[eig[i] if i==j else Q(0) for j in range(3)] for i in range(3)]),trans(rot))
            yield u,a,q,dict(frame_index=fi,householder_a=[1,2,3,4,5],householder_b=list(b),
                            spectrum_index=si,spectrum_name=name,spectrum=spec,rotation_vectors=rotvecs)

def assess(index,u,a,q,meta,out):
    COUNTS['center_attempts']+=1
    h,f,ac,ps,gs,js,diag=hessian(u,a)
    hv,he=np.linalg.eigh(np.array(h.tolist(),float)/np.outer(SCALES,SCALES))
    av,ae=np.linalg.eigh(np.array(ac.tolist(),float)/np.outer(SCALES,SCALES))
    c_entropy=-sum(mpq(x)*mp.log(mpq(x)) for x in q.values())
    rec=dict(index=index,meta=meta,U=rational_strings(u),A=rational_strings(a),
        support_masks=SUPPORT,structural_zero_masks=EXCLUDED,structural_zero_event_jets={s:['0','0','0'] for s in EXCLUDED},
        q_triple={s:str(x) for s,x in q.items()},entropy_q=mp.nstr(c_entropy,55),
        basis_pairs=PAIRS,hessian=decimals(h),fisher_positive=decimals(f),acceleration=decimals(ac),
        hessian_eigenvalues=hv.tolist(),lambda_max=float(hv[-1]),acceleration_eigenvalues=av.tolist(),
        event_p=decimals(ps),event_gradient=[decimals(g.T)[0] for g in gs],
        event_hessian=[decimals(j) for j in js],diagnostic=diag,directions=[])
    h0=entropy(u,a)
    for name,vec in [('hessian_top',he[:,-1]),('acceleration_top',ae[:,-1])]:
        v=[[Q(0)]*3 for _ in range(3)]
        for (i,j),x in zip(PAIRS,vec/SCALES):v[i][j]=v[j][i]=Q(round(float(x)*10**9),10**9)
        cc=mp.matrix([mpq(v[i][j]) for i,j in PAIRS]);r=radius(a,v)
        p1=[(g.T*cc)[0] for g in gs];p2=[(cc.T*j*cc)[0] for j in js]
        negf=[-d*d/p for d,p in zip(p1,ps)];acc=[-d*mp.log(p) for d,p in zip(p2,ps)]
        layers=[]
        for k in range(4):
            ids=[i for i,s in enumerate(SUPPORT) if s.bit_count()==k]
            ff=sum(negf[i] for i in ids);aa=sum(acc[i] for i in ids)
            layers.append(dict(cardinality=k,negative_fisher=mp.nstr(ff,55),acceleration=mp.nstr(aa,55),curvature=mp.nstr(ff+aa,55)))
        exactjets=detjet3(a,v);d,dp,ddp=map(mpq,exactjets)
        ft=dp*dp/d;geom=c_entropy*ddp;base=-ddp*mp.log(d);total=geom+base-ft
        errors=[]
        for i,s in enumerate(SUPPORT):
            if s.bit_count()==3:
                errors.extend(abs(x-mpq(q[s])*y) for x,y in zip((ps[i],p1[i],p2[i]),(d,dp,ddp)))
        errors.append(abs(total-mp.mpf(layers[3]['curvature'])))
        assert max(errors)<mp.mpf('1e-40')
        chords=[]
        for frac in (.03,.25,.75):
            t=Q(round(r*frac*10**12),10**12);assert t>0
            am=add(a,v,-t);ap=add(a,v,t)
            assert all(positive_definite(m) for m in (am,ap,add(eye(3),am,-1),add(eye(3),ap,-1)))
            gap=(entropy(u,am)+entropy(u,ap))/2-h0
            chords.append(dict(radius_fraction=frac,t=str(t),gap=mp.nstr(gap,55),exact_endpoint_sylvester_positive=True))
            COUNTS['chord_calls']+=1
        af=asfloat(a);vf=asfloat(v)
        dr=dict(name=name,V=rational_strings(v),curvature=mp.nstr((cc.T*h*cc)[0],55),
            negative_fisher=mp.nstr(-(cc.T*f*cc)[0],55),acceleration=mp.nstr((cc.T*ac*cc)[0],55),
            commutator_norm=float(np.linalg.norm(af@vf-vf@af)),symmetric_radius_float=r,
            determinant_jets_exact=list(map(str,exactjets)),top_layer=dict(
                entropy_q=mp.nstr(c_entropy,55),geometry_c_ddet=mp.nstr(geom,55),
                fisher_positive=mp.nstr(ft,55),base_acceleration_minus_ddet_logdet=mp.nstr(base,55),
                total=mp.nstr(total,55),geometry_exceeds_top_fisher=bool(geom>ft),
                direct_formula_max_error=mp.nstr(max(errors),10)),
            cardinality_layers=layers,event_dp=decimals(p1),event_ddp=decimals(p2),
            event_negative_fisher=decimals(negf),event_acceleration=decimals(acc),chords=chords)
        rec['directions'].append(dr);COUNTS['direction_evaluations']+=1
        if mp.mpf(dr['curvature'])>0 or any(mp.mpf(x['gap'])>0 for x in chords):
            path=out/f'candidate_{index:03d}_{name}.json'
            path.write_text(json.dumps(dict(status='NUMERICAL_CANDIDATE_NOT_CERTIFIED',record=rec,direction=dr),indent=2)+'\n')
            print(json.dumps(dict(CANDIDATE=path.name,index=index,direction=name)),flush=True)
    COUNTS['center_completed']+=1
    return rec

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default='F2');args=p.parse_args()
    out=Path(args.out);out.mkdir(parents=True,exist_ok=False);start=time.time()
    manifest=dict(status='RUNNING',pid=os.getpid(),seed=SEED,precision_digits=mp.mp.dps,
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        helper_source_sha256=hashlib.sha256(Path(core.__file__).read_bytes()).hexdigest(),
        python=sys.version,numpy=np.__version__,scipy=scipy.__version__,mpmath=mp.__version__,
        platform=platform.platform(),argv=sys.argv,prescribed_centers=24,
        support_masks=SUPPORT,structural_zero_masks=EXCLUDED,
        thread_limits={k:os.environ[k] for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS')},
        classification='numerical scout only; no rigorous log enclosure or general theorem')
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    failures=[];records=[]
    with (out/'cases.jsonl').open('w') as handle:
        for i,(u,a,q,meta) in enumerate(centers()):
            try:
                rec=assess(i,u,a,q,meta,out);records.append(rec)
                handle.write(json.dumps(rec)+'\n');handle.flush()
                print(json.dumps(dict(index=i,frame=meta['frame_index'],spectrum=meta['spectrum_name'],lambda_max=rec['lambda_max'],entropy_q=rec['entropy_q'])),flush=True)
            except Exception as exc:
                failures.append(dict(index=i,error=repr(exc)));print(json.dumps(failures[-1]),flush=True)
    manifest.update(status='COMPLETED' if not failures else 'COMPLETED_WITH_FAILURES',counts=COUNTS,
        exact_endpoint_pd_checks=core.COUNTS['exact_endpoint_pd_checks'],elapsed_seconds=time.time()-start,
        failures=failures,candidate_files=[p.name for p in out.glob('candidate_*.json')],exit_status=0 if not failures else 1)
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    if records:
        (out/'highest_curvature.json').write_text(json.dumps(max(records,key=lambda x:x['lambda_max']),indent=2)+'\n')
    print(json.dumps(manifest),flush=True)
    return manifest['exit_status']

if __name__=='__main__':raise SystemExit(main())
