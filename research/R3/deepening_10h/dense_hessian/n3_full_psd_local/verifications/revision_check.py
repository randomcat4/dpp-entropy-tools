"""S5 short revised recheck; preserves all original audit artifacts."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
os.environ['MKL_NUM_THREADS']='1'
from pathlib import Path
import hashlib
import json
import random
import time
import ast
import numpy as np

HERE=Path(__file__).resolve().parent
AUTHOR=HERE.parent

def main():
    start=time.time()
    names=('full_psd_hessian.py','hessian_scout.json','analysis.md','frozen_problem.md','verdict.md','run_log.md')
    before={name:hashlib.sha256((AUTHOR/name).read_bytes()).hexdigest() for name in names}
    source=(AUTHOR/'full_psd_hessian.py').read_text()
    tree=ast.parse(source)
    routine=next(node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name=='projected_power_scout')
    normalized=ast.unparse(routine)
    assert 'grad_matrix_coords = grad_x.copy()' in normalized
    assert 'grad_matrix_coords[3:] *= 0.5' in normalized
    assert 'G = matrix_from_np_coords(grad_matrix_coords)' in normalized
    assert normalized.index('grad_matrix_coords[3:] *= 0.5')<normalized.index('G = matrix_from_np_coords(grad_matrix_coords)')

    # Re-execute our independent polynomial/interval proof, not author Hessian
    # code. Only output filename and historical scout diagnosis are adjusted.
    independent=(HERE/'independent_check.py').read_text()
    independent=independent.replace("HERE/'independent_results.json'","HERE/'revision_core_results.json'")
    independent=independent.replace('SCOUT_ONLY_WITH_GRADIENT_METRIC_DEFECT','SCOUT_ONLY_GRADIENT_FIXED_IN_REVISED_SOURCE')
    independent=independent.replace('scout_frobenius_gradient_offdiagonal_error_at_I_over_3','historical_unfixed_gradient_error_at_I_over_3')
    namespace={'__file__':str(HERE/'independent_check.py'),'__name__':'revision_core_replay'}
    exec(compile(independent,str(HERE/'independent_check.py'),'exec'),namespace)
    namespace['main']()

    saved=json.loads((AUTHOR/'hessian_scout.json').read_text())
    A=np.array(saved['entropy_hessian_matrix_decimal'],dtype=float)
    pairs=((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))
    def coords(D): return np.array([D[i,j] for i,j in pairs])
    def matrix(x):
        out=np.zeros((3,3))
        for val,(i,j) in zip(x,pairs): out[i,j]=out[j,i]=val
        return out
    def objective(D):
        x=coords(D); return float(x@A@x)
    def project(D):
        eig,Q=np.linalg.eigh((D+D.T)/2)
        out=(Q*np.maximum(eig,0))@Q.T
        norm=np.linalg.norm(out,'fro')
        return out/norm if norm else np.eye(3)/np.sqrt(3)
    # Riesz identity on all six basis perturbations at a deterministic point.
    x=np.array([.2,.3,.4,.05,-.02,.07]); g=2*A@x
    gc=g.copy(); gc[3:]/=2; G=matrix(gc)
    riesz_errors=[]
    for j in range(6):
        e=np.eye(6)[j]; E=matrix(e)
        riesz_errors.append(abs(float(np.sum(G*E))-float(g@e)))
    assert max(riesz_errors)<1e-14

    seed=20260908; starts=400; steps=300; rng=random.Random(seed)
    best=-1e100; bestD=None; rankbest=-1e100; rankD=None
    for _ in range(4000):
        u=np.array([rng.gauss(0,1) for _ in range(3)])
        D=np.outer(u,u)/float(u@u); val=objective(D)
        if val>rankbest: rankbest=val; rankD=D.copy()
        if val>best: best=val; bestD=D.copy()
    for _ in range(starts):
        M=np.array([[rng.gauss(0,1) for _ in range(3)] for _ in range(3)])
        D=M@M.T; D/=np.linalg.norm(D,'fro')
        for step in range(steps):
            g=2*A@coords(D); g[3:]/=2
            D=project(D+(0.35/(1+step/60))*matrix(g))
        val=objective(D)
        if val>best: best=val; bestD=D.copy()
    scout=saved['projected_psd_scout']
    assert scout['seed']==seed and scout['starts']==starts and scout['steps']==steps
    assert abs(best-scout['best_value'])<1e-13
    assert abs(rankbest-scout['rank1_best_value'])<1e-13
    assert np.max(np.abs(bestD-np.array(scout['best_D'])))<1e-13
    assert np.max(np.abs(rankD-np.array(scout['rank1_best_D'])))<1e-13
    assert best==rankbest
    after={name:hashlib.sha256((AUTHOR/name).read_bytes()).hexdigest() for name in names}
    assert before==after,'revision drift'
    report=dict(status='CORRECT_REVISED_CORE_AND_GRADIENT; FINITE_OPTIMIZATION_SCOUT_ONLY',
        author_hashes_before=before,author_hashes_after=after,gradient_riesz_errors=riesz_errors,
        replay=dict(seed=seed,rank_one_proposals=4000,projected_starts=starts,steps_per_start=steps,
            projected_updates=starts*steps,best_value=best,rank1_best_value=rankbest,best_D=bestD.tolist(),
            maximum_from_rank_one_scan=bool(best==rankbest),matches_saved_output=True),
        old_issue='missing off-diagonal factor 1/2 is fixed; initial audit remains valid for initial hash',
        core_results='revision_core_results.json',elapsed_seconds=time.time()-start,exit_code=0,
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (HERE/'revision_results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__': main()
