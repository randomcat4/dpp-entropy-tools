"""Read-only, same-job monitoring and final ledger audit."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sqlite3
import time

ap=argparse.ArgumentParser()
ap.add_argument("--full",action="store_true")
ap.add_argument("--output")
args=ap.parse_args()
root=Path(__file__).resolve().parent
formal=root/"formal"
db=sqlite3.connect(f"file:{(formal/'state.sqlite').as_posix()}?mode=ro",uri=True)
db.execute("PRAGMA query_only=ON")
db.execute("BEGIN")
meta={key:json.loads(value) for key,value in db.execute("SELECT key,value FROM meta")}
row_count,distinct_count,min_id,max_id=db.execute("SELECT COUNT(*),COUNT(DISTINCT id),MIN(id),MAX(id) FROM evaluations").fetchone()
states=dict(db.execute("SELECT status,COUNT(*) FROM evaluations GROUP BY status"))
per_cell={}
for cell,state,count in db.execute("SELECT cell,status,COUNT(*) FROM evaluations GROUP BY cell,status"):
    per_cell.setdefault(cell,{})[state]=count
best_rows=db.execute("SELECT cell,value,object FROM best ORDER BY value DESC").fetchall()
best=json.loads(best_rows[0][2]) if best_rows else None
invocations=[dict(zip(("id","started","ended","pid","exit_code","status"),r)) for r in db.execute("SELECT id,started,ended,pid,exit_code,status FROM invocations ORDER BY id")]
restarts=[dict(zip(("cell","restart","reason"),r)) for r in db.execute("SELECT cell,restart,reason FROM finished ORDER BY cell,restart")]
failures=[dict(call_id=idx,cell=cell,restart=restart,stage=stage,status=status,record=json.loads(record) if record else None)
          for idx,cell,restart,stage,status,record in db.execute("SELECT id,cell,restart,stage,status,record FROM evaluations WHERE status!='OK' ORDER BY id")]
integrity=db.execute("PRAGMA quick_check").fetchone()[0] if args.full else "not requested during running monitor"
db.execute("COMMIT")
db.close()

process=json.loads((formal/"process.json").read_text())
process_states=[]
for label in ("pid","supervisor_pid"):
    pid=process[label]
    path=Path("/proc")/str(pid)
    if not path.exists():
        process_states.append(dict(role=label,pid=pid,exists=False,live=False))
        continue
    stat=(path/"stat").read_text()
    state=stat[stat.rfind(")")+2:].split()[0]
    command=(path/"cmdline").read_bytes().replace(b"\0",b" ").decode(errors="replace").strip()
    expected=str(root/"engine.py") if label=="pid" else str(root/"launch_phase2.py")
    owned=expected in command
    process_states.append(dict(role=label,pid=pid,exists=True,state=state,command=command,
                               matches_expected_job=owned,live=state!="Z" and owned))
now=time.time()
deadline=meta["started"]+meta["config"]["wall_seconds"]
terminal=meta.get("terminal_status")
result=dict(observed_at_epoch=now,observed_at_utc=datetime.fromtimestamp(now,timezone.utc).isoformat(),
            status=terminal or "RUNNING_OR_RECOVERABLE",seed=meta["config"]["seed"],
            total_reserved_calls=meta["used"],rows=row_count,distinct_call_ids=distinct_count,
            min_call_id=min_id,max_call_id=max_id,unique_contiguous_ids=(row_count==distinct_count==meta["used"] and (row_count==0 or min_id==1 and max_id==row_count)),
            states=states,per_cell=per_cell,finished_restarts=len(restarts),requested_restarts=64,
            max_calls=meta["config"]["max_calls"],remaining_calls=meta["config"]["max_calls"]-meta["used"],
            started_epoch=meta["started"],absolute_deadline_epoch=deadline,
            absolute_deadline_utc=datetime.fromtimestamp(deadline,timezone.utc).isoformat(),
            remaining_wall_seconds=max(0,deadline-now),elapsed_wall_seconds=now-meta["started"],
            process_states=process_states,sqlite_quick_check=integrity,
            best_hessian=best["record"]["max_hessian"] if best else None,
            best_chords=best.get("chords") if best else None,
            invocation_exit_codes=[r["exit_code"] for r in invocations])
if args.full:
    result.update(best=best,best_by_cell=[dict(cell=c,value=v,record=json.loads(o)["record"],chords=json.loads(o).get("chords")) for c,v,o in best_rows],
                  failures=failures,invocations=invocations,restarts=restarts,config=meta["config"])
    for name in ("summary.json","process_exit.json"):
        path=formal/name
        result[name.replace(".json","")]=json.loads(path.read_text()) if path.exists() else None
if args.output:
    target=(root/args.output).resolve()
    if target.parent!=root:
        raise RuntimeError("Audit output must be a file directly in this phase2 directory")
    target.write_text(json.dumps(result,indent=2,allow_nan=False),encoding="utf-8")
    compact={k:result[k] for k in ("status","total_reserved_calls","states","finished_restarts","unique_contiguous_ids","sqlite_quick_check","best_hessian","best_chords","process_states")}
    if args.full:
        compact.update(actual_exit_code=result["process_exit"]["exit_code"] if result["process_exit"] else None,
                       completed_wall_seconds=result["summary"]["elapsed_wall_seconds"] if result["summary"] else None)
    print(json.dumps(compact,indent=2,allow_nan=False))
else:
    print(json.dumps(result,indent=2,allow_nan=False))

