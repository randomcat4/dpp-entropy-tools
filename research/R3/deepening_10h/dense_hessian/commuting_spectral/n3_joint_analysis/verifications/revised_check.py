"""Hash-bound v3 regression and full-scan recheck. Never invokes author main."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import time

sys.dont_write_bytecode=True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key]='1'
import numpy as np

HERE=Path(__file__).resolve().parent
AUTHOR=HERE.parent
EXPECTED='6d275dc10ffa5466f7ead81277fd622c64378f5e020eeb3dd8345aec3a085b9a'

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    started=time.time()
    source=AUTHOR/'joint_copositive_probe.py'
    assert sha(source)==EXPECTED, 'VERSION_DRIFT'
    initial_hashes={name:sha(AUTHOR/name) for name in ('joint_copositive_probe.py','joint_probe_results_v3.json','copositive_and_sphere_reduction.md','joint_reduction.md','review_response.md','verdict.md','search_report.md','hazards.md')}
    spec=importlib.util.spec_from_file_location('joint_revised_check',source)
    module=importlib.util.module_from_spec(spec)
    sys.modules[spec.name]=module
    spec.loader.exec_module(module)
    regressions={}
    matrices={'singular_zero':np.ones((3,3))-3*np.eye(3),
              'scaled_positive':(6*np.ones((3,3))-16*np.eye(3))*1e14}
    for name,matrix in matrices.items():
        value,v=module.max_quadratic_on_simplex(matrix)
        sphere,w,count=module.max_quadratic_on_positive_sphere(matrix)
        expected=0.0 if name=='singular_zero' else 2e14/3
        expected_sphere=0.0 if name=='singular_zero' else 2e14
        tol=1e-12*max(1,abs(expected))
        assert abs(value-expected)<tol
        assert abs(sphere-expected_sphere)<1e-12*max(1,abs(expected_sphere))
        assert np.all(v>=0) and abs(v.sum()-1)<1e-14
        assert np.all(w>=0) and abs(w@w-1)<1e-14
        # Independent inspection of the raw full-support KKT solve before
        # author's clipping/normalization, to expose the residual's scope.
        kkt=np.zeros((4,4)); kkt[:3,:3]=2*matrix; kkt[:3,3]=-1; kkt[3,:3]=1
        rhs=np.array([0.,0.,0.,1.])
        raw=np.linalg.lstsq(kkt,rhs,rcond=None)[0]
        accepted,residual,scale=module._kkt_residual_ok(kkt,raw,rhs)
        regressions[name]=dict(matrix=matrix.tolist(),simplex_value=float(value),simplex_v=v.tolist(),
                              true_simplex_max='0' if name=='singular_zero' else '200000000000000/3',
                              sphere_value=float(sphere),sphere_v=w.tolist(),support_candidates=count,
                              raw_kkt_solution=raw.tolist(),raw_sum_v=float(raw[:3].sum()),
                              residual=float(residual),residual_scale=float(scale),accepted=bool(accepted),
                              simplex_error=float(abs(value-expected)),passed=True)
    report=dict(hashes=initial_hashes,regressions=regressions,regression_exit_code=0)
    (HERE/'revised_check.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'regressions':'PASS','details':regressions}),flush=True)
    result=module.scan()
    assert all(sha(AUTHOR/name)==digest for name,digest in initial_hashes.items()), 'VERSION_DRIFT_DURING_REPLAY'
    saved=json.loads((AUTHOR/'joint_probe_results_v3.json').read_text())
    assert result['base_points_checked']==saved['base_points_checked']==60384
    assert result['sphere_candidate_vectors_evaluated']==saved['sphere_candidate_vectors_evaluated']==416691
    assert result['positive_total_candidates']==saved['positive_total_candidates']==[]
    assert result['sphere_positive_gate_hits']==saved['sphere_positive_gate_hits']==[]
    assert result['copositive_mismatches']==saved['copositive_mismatches']==[]
    best_errors={key:abs(result[key]['value']-saved[key]['value']) for key in ('best_total_simplex','best_psi_simplex','best_singleton_layer_simplex','best_pair_layer_simplex')}
    assert max(best_errors.values())<1e-12
    assert result['script_sha256']==EXPECTED
    (HERE/'revised_replay_v3.json').write_text(json.dumps(result,indent=2)+'\n')
    report.update(replay=dict(base_points=60384,structured=384,random=60000,support_candidates=416691,
                              positive_total=0,sphere_positive=0,copositive_mismatches=0,
                              best_value_errors=best_errors,elapsed_seconds=time.time()-started,exit_code=0),
                  output_sha256=sha(HERE/'revised_replay_v3.json'),script_sha256=sha(Path(__file__)),exit_code=0)
    (HERE/'revised_check.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report['replay']),flush=True)

if __name__=='__main__': main()
