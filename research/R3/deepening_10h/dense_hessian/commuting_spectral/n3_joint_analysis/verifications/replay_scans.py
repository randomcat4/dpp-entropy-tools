"""Read-only author-code replay; separate from independent mathematics checks."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import time

sys.dont_write_bytecode = True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key] = '1'
HERE=Path(__file__).resolve().parent
AUTHOR=HERE.parent

def load(name):
    spec=importlib.util.spec_from_file_location(name,AUTHOR/(name+'.py'))
    module=importlib.util.module_from_spec(spec)
    sys.modules[name]=module
    spec.loader.exec_module(module)
    return module

def main():
    started=time.time()
    frozen=json.loads((HERE/'initial_author_hashes.json').read_text())
    for name in ('joint_copositive_probe.py','sphere_support_probe.py'):
        observed=hashlib.sha256((AUTHOR/name).read_bytes()).hexdigest()
        if observed!=frozen[name]:
            raise RuntimeError('VERSION_DRIFT: restore the audited source before replay; saved replay results remain bound to initial hashes')
    joint=load('joint_copositive_probe')
    sphere=load('sphere_support_probe')
    for label,module,filename in [('joint',joint,'joint_probe_results.json'),('sphere',sphere,'sphere_probe_results.json')]:
        result=module.scan()
        original=json.loads((AUTHOR/filename).read_text())
        (HERE/(label+'_replay.json')).write_text(json.dumps(result,indent=2)+'\n')
        fields=['base_points_checked','positive_total_candidates']
        fields+=['candidate_vectors_evaluated'] if label=='sphere' else ['copositive_mismatches']
        checks={field:result[field]==original[field] for field in fields}
        print(json.dumps(dict(scan=label,checks=checks,base_points=result['base_points_checked'],elapsed_seconds=time.time()-started)),flush=True)
        assert all(checks.values())
    print('EXIT_CODE=0',flush=True)

if __name__=='__main__':
    main()
