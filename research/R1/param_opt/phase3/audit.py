"""Read-only audit of the stopped formal n=2 attack ledger."""
import json
import math
from pathlib import Path
import sqlite3

root=Path(__file__).resolve().parent
folder=root/"formal"
db=sqlite3.connect(f"file:{(folder/'ledger.sqlite').as_posix()}?mode=ro",uri=True)
db.execute("PRAGMA query_only=ON")
db.execute("BEGIN")
meta={k:json.loads(v) for k,v in db.execute("SELECT k,v FROM meta")}
count,distinct,first,last=db.execute("SELECT COUNT(*),COUNT(DISTINCT id),MIN(id),MAX(id) FROM calls").fetchone()
states=dict(db.execute("SELECT status,COUNT(*) FROM calls GROUP BY status"))
stage_counts=dict(db.execute("SELECT stage,COUNT(*) FROM calls GROUP BY stage"))
mp_states=dict(db.execute("SELECT status,COUNT(*) FROM mpchecks GROUP BY status"))
mp_checks=[dict(check_id=i,call_id=c,status=s,record=json.loads(r) if r else None) for i,c,s,r in db.execute("SELECT id,call_id,status,record FROM mpchecks")]
mins=dict(event=1.,margin=1.,u=1.,L=1e300)
maxs=dict(event=0.,margin=0.,u=0.,L=0.)
margin_hist={"<1e-15":0,"1e-15..1e-12":0,"1e-12..1e-9":0,"1e-9..1e-6":0,"1e-6..1e-3":0,">=1e-3":0}
raw_positive=scaled_positive=negative_log_slack=0
for (txt,) in db.execute("SELECT record FROM calls WHERE status='OK'"):
    obj=json.loads(txt);p=obj["events"];a=obj["K"][0][0];b=obj["K"][1][1];u=obj["u"]
    disc=math.sqrt((a-b)**2+4*u)
    margin=min(2*p[3]/(a+b+disc),2*p[0]/(2-a-b+disc))
    values=dict(event=min(p),margin=margin,u=u,L=obj["L"])
    for key,value in values.items():mins[key]=min(mins[key],value);maxs[key]=max(maxs[key],value)
    thresholds=(1e-15,1e-12,1e-9,1e-6,1e-3)
    index=next((i for i,v in enumerate(thresholds) if margin<v),5)
    margin_hist[list(margin_hist)[index]]+=1
    raw_positive+=obj["raw_max_hessian"]>1e-8
    scaled_positive+=obj["scaled_max_hessian"]>1e-9
    negative_log_slack+=obj["log_bound_slack"]<0
quick=db.execute("PRAGMA quick_check").fetchone()[0]
db.execute("COMMIT");db.close()
summary=json.loads((folder/"summary.json").read_text())
pid=summary["process_id"]
result=dict(status=summary["status"],exit_code=summary["exit_code"],elapsed_seconds=summary["elapsed_seconds"],
            seed=meta["config"]["seed"],calls=count,distinct_call_ids=distinct,min_id=first,max_id=last,
            unique_contiguous=(count==distinct==last==meta["used"] and first==1),states=states,stage_counts=stage_counts,
            mp_states=mp_states,mp_checks=mp_checks,sqlite_quick_check=quick,process_id=pid,
            process_exists=(Path("/proc")/str(pid)).exists(),sample_ranges=dict(minimum=mins,maximum=maxs),
            spectral_margin_histogram=margin_hist,raw_hessian_above_1e_minus8_count=raw_positive,
            scaled_hessian_above_1e_minus9_count=scaled_positive,floating_negative_log_bound_slack_count=negative_log_slack,
            best_raw=summary["best_raw"],best_scaled=summary["best_scaled"],
            note="Raw and near-equality floating signs are not certificates.")
(root/"formal_audit.json").write_text(json.dumps(result,indent=2))
print(json.dumps({k:v for k,v in result.items() if k not in ("mp_checks","best_raw","best_scaled","stage_counts")},indent=2))
