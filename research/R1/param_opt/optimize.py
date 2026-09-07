"""A separate, finite full-coordinate spectral-parameter optimization batch."""
import search
import json
import os
from pathlib import Path
import resource
import time
import numpy as np
from scipy.optimize import minimize

resource.setrlimit(resource.RLIMIT_AS, (10*1024**3, 10*1024**3))
resource.setrlimit(resource.RLIMIT_CPU, (330, 340))
root = Path(__file__).resolve().parent
out = root / "batch02"
out.mkdir(exist_ok=True)
if (out / "pid.json").exists():
    raise SystemExit("Batch exists; inspect before any explicit resumption")
(out / "pid.json").write_text(json.dumps(dict(pid=os.getpid(),seed=202609082,threads=1,
    seconds=300,maximum_evaluations_per_restart=600,dimensions=list(range(3,11)),restarts_per_dimension=2)))
rng = np.random.default_rng(202609082)
started = time.monotonic()
total = failed = positive = 0
best = None
results = []

class BudgetStop(Exception):
    pass

with (out / "evaluations.jsonl").open("w",buffering=1) as log:
    for n in range(3,11):
        _,_,_,e = search.basis(n)
        for restart in range(2):
            if time.monotonic()-started > 300:
                break
            initial = rng.normal(size=len(e)) * (1.5 if restart==0 else 4) / np.sqrt(n)
            calls = [0]
            local_best = [-np.inf]
            def objective(x):
                global total,failed,positive,best
                if calls[0]>=600 or time.monotonic()-started>300:
                    raise BudgetStop()
                calls[0] += 1; total += 1
                rec = dict(n=n,restart=restart,evaluation=calls[0],global_evaluation=total,margin=0.001)
                try:
                    raw = np.einsum("a,aij->ij",x,e)
                    value,k,v,residual,pmin = search.evaluate(raw,0.001)
                    if not np.isfinite(value) or residual>1e-7:
                        raise FloatingPointError("Hessian diagnostic failed")
                    rec.update(max_hessian=value,mass_second_residual=residual,probability_min=pmin)
                    if value>local_best[0]:
                        local_best[0]=value
                    if best is None or value>best["value"]:
                        eig=np.linalg.eigvalsh(k)
                        t=0.05*min(eig[0],1-eig[-1])/np.linalg.norm(v,2)
                        delta=(search.entropy(k-t*v)+search.entropy(k+t*v))/2-search.entropy(k)
                        best=dict(value=value,K=k.tolist(),V=v.tolist(),raw=raw.tolist(),eigenvalues=eig.tolist(),
                                  t=t,delta=delta,record=rec)
                        (out / "best.json").write_text(json.dumps(best,indent=2))
                    if value>1e-6:
                        positive+=1
                        (out / f"candidate_{total:08d}.json").write_text(json.dumps(dict(K=k.tolist(),V=v.tolist(),record=rec)))
                    log.write(json.dumps(rec)+"\n")
                    return -value
                except (FloatingPointError,np.linalg.LinAlgError,ValueError) as exc:
                    failed+=1;rec["failure"]=str(exc);log.write(json.dumps(rec)+"\n")
                    return 1e8
            try:
                sol=minimize(objective,initial,method="L-BFGS-B",bounds=[(-8,8)]*len(e),
                             options=dict(maxiter=50,maxfun=600,ftol=1e-13,gtol=1e-8,maxls=15))
                termination=str(sol.message)
            except BudgetStop:
                termination="explicit objective-evaluation or wall-time budget reached"
            rec=dict(n=n,restart=restart,evaluations=calls[0],best=local_best[0],termination=termination)
            results.append(rec)
            (out / "checkpoint.json").write_text(json.dumps(dict(total=total,failed=failed,positive=positive,
                                                                 completed_restarts=results,best=best),indent=2))
            print(json.dumps(rec),flush=True)
summary=dict(status="DISPROVED_CANDIDATE" if positive else "INCOMPLETE",seed=202609082,total=total,failed=failed,
             positive=positive,positive_threshold=1e-6,restarts=results,elapsed_seconds=time.monotonic()-started,
             exit_code=0,best=best,limitations="Finite numerical optimization; no certification or continuous exclusion.")
(out / "summary.json").write_text(json.dumps(summary,indent=2))
print(json.dumps({k:v for k,v in summary.items() if k not in ("best","restarts")}),flush=True)
