"""Reconstruct failed optimizer call control flow; does not evaluate any kernel.

The failed serializer returned penalty 1000 on every objective invocation.
This recovers objective invocation counts, not lost floating arithmetic records.
"""
import os
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
import json,hashlib
from pathlib import Path
import numpy as np
import scipy
from scipy.optimize import minimize
root=Path(__file__).parent
initial=[json.loads(line) for line in (root/'batch3'/'cases.jsonl').read_text().splitlines()][:54]
counts=[]
for family in ('nearly_collinear','nearly_orthogonal','conflicting_signs'):
    leader=max([r for r in initial if r['meta']['family']==family],key=lambda r:r['cross_gain'])
    trace=[]
    def objective(x):trace.append(x.tolist());return 1000.
    result=minimize(objective,np.array(leader['x']),method='Nelder-Mead',options={'maxfev':80,'xatol':1e-6,'fatol':1e-8,'adaptive':True})
    counts.append({'family':family,'parent_index':leader['index'],'nfev':int(result.nfev),'counted_control_invocations':len(trace),'status':int(result.status)})
record={'status':'FAILED_RUN_ACCOUNTING_RECONSTRUCTED','failed_pid':159210,'failed_outer_shell_exit_code':1,'original_manifest_retained_unchanged':True,'failure':'numpy.bool_ in single_blocks_negative could not be JSON serialized; same error affected final best output','failed_source_sha256':hashlib.sha256((root/'diamond_interior_failed_serialization.py').read_bytes()).hexdigest(),'initial_objective_invocations':54,'reconstructed_optimizer_calls':counts,'reconstructed_total_objective_invocations':54+sum(c['nfev'] for c in counts),'count_provenance':'Deterministic constant-penalty optimizer control-flow replay using same scipy and initial leaders; NOT surviving per-call runtime telemetry','retained_successful_cases':0,'exact_failed_hessian_and_entropy_counts':'not persisted; do not merge into measured successful arithmetic counts','this_control_replay_new_hessian_calls':0,'this_control_replay_new_entropy_calls':0,'scipy':scipy.__version__,'exit_code':0}
(root/'batch3_failed_serialization'/'failure_accounting.json').write_text(json.dumps(record,indent=2));print(json.dumps(record))
