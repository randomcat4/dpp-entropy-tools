"""N4 P1: bounded gauge-inequivalent signed-cycle pilot; float scout only."""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key] = '1'
import argparse, hashlib, importlib.util, itertools, json, platform, sys, time
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT/'research/R3/deepening_10h/dense_hessian/dense_hessian.py'
spec = importlib.util.spec_from_file_location('baseline_dense', SOURCE)
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)

def radius(k,d):
    bounds=[]
    for a in (k,np.eye(len(k))-k):
        w,v=np.linalg.eigh(a)
        if w[0]<=0: raise ArithmeticError('infeasible midpoint')
        z=(v/np.sqrt(w))@v.T
        bounds.append(1/np.max(np.abs(np.linalg.eigvalsh(z@d@z))))
    return float(min(bounds))

def atoms_direction(k,d):
    p,lp,a=base.atoms_and_logs(k)
    b=np.linalg.solve(a,np.broadcast_to(d,a.shape))
    g=np.trace(b,axis1=1,axis2=2)
    p1=p*g
    p2=p*(g*g-np.einsum('qij,qji->q',b,b))
    f=-p1*p1/p
    acc=-p2*lp
    return [dict(mask=s,p=float(p[s]),p1=float(p1[s]),p2=float(p2[s]),
                 fisher=float(f[s]),acceleration=float(acc[s]),total=float(f[s]+acc[s]))
            for s in range(len(p))]

def analyze(k,meta,index):
    h,f,a,diag=base.entropy_hessian_components(k)
    basis,pairs=base.symmetric_basis(len(k))
    weights=np.array([1 if i==j else 1/np.sqrt(2) for i,j in pairs])
    w,v=np.linalg.eigh(weights[:,None]*h*weights[None,:])
    coord=weights*v[:,-1]
    d=np.einsum('p,pij->ij',coord,basis)
    r=radius(k,d)
    events=atoms_direction(k,d)
    gaps=[]
    for fraction in (.1,.5,.9):
        t=fraction*r
        gaps.append(dict(fraction=fraction,t=t,delta=(base.entropy(k-t*d)[0]+base.entropy(k+t*d)[0])/2-diag['entropy'],
                         margin=min(base.margin(k-t*d),base.margin(k+t*d))))
    ratio,rc,rf,ra,rt=base.acceleration_fisher_mechanism(f,a)
    rd=np.einsum('p,pij->ij',rc,basis)
    rd/=np.linalg.norm(rd,'fro')
    complementary=[dict(masks=[s,15-s],fisher=events[s]['fisher']+events[15-s]['fisher'],
                        acceleration=events[s]['acceleration']+events[15-s]['acceleration'],
                        total=events[s]['total']+events[15-s]['total']) for s in range(8)]
    return dict(index=index,parameters=meta,K=k.tolist(),D=d.tolist(),radius=r,
                lambda_max_frobenius=float(w[-1]),fisher=float(coord@f@coord),
                acceleration=float(coord@a@coord),mechanism_ratio=ratio,
                mechanism_D=rd.tolist(),mechanism_radius=radius(k,rd),
                eigenvalues=np.linalg.eigvalsh(k).tolist(),direction_eigenvalues=np.linalg.eigvalsh(d).tolist(),
                commutator_norm=float(np.linalg.norm(k@d-d@k)),
                event_derivative_sums=[sum(x['p1'] for x in events),sum(x['p2'] for x in events)],
                events=events,complement_pairs=complementary,gaps=gaps,diagnostics=diag)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out',required=True); args=ap.parse_args()
    out=Path(args.out);out.mkdir(parents=True,exist_ok=False)
    start=time.time()
    manifest=dict(status='RUNNING',pid=os.getpid(),python=platform.python_version(),numpy=np.__version__,
                  baseline='fa504ec74e16843fafc395880d7ba99b4c1d2129',seed=None,
                  deterministic=True,threads=1,command='python research/N4/pilot.py --out '+args.out,
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  baseline_source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),start_unix=start)
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2))
    smoke=base.self_test()
    (out/'smoke.json').write_text(json.dumps(smoke,indent=2))
    diagonal=np.array([.13,.37,.63,.86]); center=np.diag(diagonal)
    edges=[(0,1,.11),(0,2,.07),(0,3,.09),(1,2,.13),(1,3,.08),(2,3,.12)]
    rows=[]
    with (out/'cases.jsonl').open('w') as handle:
        for graph in ('K4','diamond'):
            chords=3 if graph=='K4' else 2
            for signs in itertools.product((-1,1),repeat=chords):
                off=np.zeros((4,4))
                for j,(u,v,x) in enumerate(edges[:3+chords]):
                    value=x*(1 if j<3 else signs[j-3]);off[u,v]=off[v,u]=value
                edge_radius=radius(center,off)
                for fraction in (.2,.7,.97):
                    k=center+fraction*edge_radius*off
                    row=analyze(k,dict(graph=graph,chord_signs=signs,edge_fraction=fraction,
                                      edge_radius=edge_radius,diagonal=diagonal.tolist()),len(rows))
                    rows.append(row);handle.write(json.dumps(row)+'\n');handle.flush()
        # An analytic radius, not the radius of an arbitrary numerical line in eigen-parameters.
    best=max(rows,key=lambda z:z['lambda_max_frobenius'])
    ratio_best=max(rows,key=lambda z:z['mechanism_ratio'])
    (out/'best_curvature.json').write_text(json.dumps(best,indent=2))
    (out/'best_mechanism.json').write_text(json.dumps(ratio_best,indent=2))
    manifest.update(status='SCOUT_COMPLETE',exit_code=0,completed_kernels=len(rows),
                    actual_hessian_calls=len(rows)+1,actual_chords=3*len(rows),event_rows=16*len(rows),
                    gauge_classes={'K4':8,'diamond':4},elapsed_seconds=time.time()-start,
                    largest_curvature=best['lambda_max_frobenius'],largest_ratio=ratio_best['mechanism_ratio'],
                    largest_gap=max(x['delta'] for z in rows for x in z['gaps']),
                    positive_curvatures=sum(z['lambda_max_frobenius']>1e-9 for z in rows),
                    warning='Finite float scout only. No universal exclusion or strict certificate.')
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2));print(json.dumps(manifest))

if __name__=='__main__': main()
