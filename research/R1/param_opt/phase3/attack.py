"""Bounded n=2 boundary/flat/general attack, with pre-reserved call IDs."""
import n2core as core
import argparse
import contextlib
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import sys
import time
import numpy as np

ROOT=Path(__file__).resolve().parent

class Stop(Exception):pass

@contextlib.contextmanager
def lock(path):
    f=path.open("a+b")
    if os.name=="nt":
        import msvcrt
        f.write(b"0");f.flush();f.seek(0);msvcrt.locking(f.fileno(),msvcrt.LK_NBLCK,1)
    else:
        import fcntl
        fcntl.flock(f.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
    try:yield
    finally:f.close()

def js(x):return json.dumps(x,allow_nan=False,separators=(",",":"))

def atomic(path,data):
    temp=path.with_suffix(".tmp")
    temp.write_text(json.dumps(data,indent=2,allow_nan=False))
    os.replace(temp,path)

def point(seed,idx):
    rng=np.random.default_rng(np.random.SeedSequence([seed,idx]))
    mode=idx%4
    if mode==0:
        return np.r_[rng.uniform(-6,6,2),rng.uniform(-6,2.5)]
    if mode==1:
        return np.r_[rng.uniform(-14,14,2),rng.uniform(-32,-8)]
    if mode==2:
        return np.r_[rng.uniform(-14,14,2),rng.uniform(2,np.log(24))]
    return np.r_[rng.choice([-1,1],2)*rng.uniform(9,14,2),rng.uniform(-24,np.log(24))]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",default="formal")
    ap.add_argument("--smoke",action="store_true")
    ap.add_argument("--resume",action="store_true")
    args=ap.parse_args()
    out=(ROOT/args.out).resolve()
    if not out.is_relative_to(ROOT) or out==ROOT:raise ValueError("invalid output scope")
    out.mkdir(exist_ok=True)
    cfg=dict(seed=20260908301,samples=64 if args.smoke else 120000,restarts=0 if args.smoke else 32,
             per_restart=800,max_calls=64 if args.smoke else 160000,max_mp=2 if args.smoke else 128,
             seconds=120 if args.smoke else 1800,cpu_threads=1,memory_bytes=8*1024**3,
             candidate_threshold=1e-8,scaled_trigger=1e-9,
             source_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/"attack.py",ROOT/"n2core.py")})
    if not args.smoke and os.name!="nt":
        import resource
        resource.setrlimit(resource.RLIMIT_AS,(8*1024**3,8*1024**3))
        resource.setrlimit(resource.RLIMIT_CPU,(1790,1800))
    with lock(out/"run.lock"):
        db=sqlite3.connect(out/"ledger.sqlite",isolation_level=None)
        db.executescript("""PRAGMA journal_mode=WAL; PRAGMA synchronous=FULL;
        CREATE TABLE IF NOT EXISTS meta(k TEXT PRIMARY KEY,v TEXT);
        CREATE TABLE IF NOT EXISTS calls(id INTEGER PRIMARY KEY,stage TEXT,seq INTEGER,theta TEXT,status TEXT,record TEXT);
        CREATE INDEX IF NOT EXISTS by_stage ON calls(stage,seq);
        CREATE TABLE IF NOT EXISTS done(stage TEXT PRIMARY KEY,reason TEXT);
        CREATE TABLE IF NOT EXISTS mpchecks(id INTEGER PRIMARY KEY,call_id INTEGER,status TEXT,record TEXT);
        """)
        def meta(k,default=None):
            row=db.execute("SELECT v FROM meta WHERE k=?",(k,)).fetchone()
            return json.loads(row[0]) if row else default
        if meta("config") is None:
            if args.resume:raise ValueError("no checkpoint")
            db.execute("BEGIN IMMEDIATE")
            for k,v in (("config",cfg),("used",0),("started",time.time())):
                db.execute("INSERT INTO meta VALUES(?,?)",(k,js(v)))
            db.execute("COMMIT")
            atomic(out/"config.json",cfg)
        elif not args.resume:raise ValueError("existing run; inspect before explicit resume")
        elif js(meta("config"))!=js(cfg):raise ValueError("configuration/source mismatch")
        if meta("terminal"):
            print(js(dict(status="ALREADY_TERMINAL",terminal=meta("terminal"))));return 0
        db.execute("UPDATE calls SET status='INTERRUPTED_UNKNOWN' WHERE status='RESERVED'")
        deadline=meta("started")+cfg["seconds"]
        best=None;bestscaled=None
        for (record,) in db.execute("SELECT record FROM calls WHERE status='OK'"):
            item=json.loads(record)
            if best is None or item["raw_max_hessian"]>best["raw_max_hessian"]:best=item
            if bestscaled is None or item["scaled_max_hessian"]>bestscaled["scaled_max_hessian"]:bestscaled=item
        stop_reason=None;hit=False
        def snapshot(status="RUNNING",rc=None):
            states=dict(db.execute("SELECT status,COUNT(*) FROM calls GROUP BY status"))
            result=dict(status=status,config=cfg,calls=meta("used"),states=states,elapsed_seconds=time.time()-meta("started"),
                        deadline_epoch=deadline,remaining_seconds=max(0,deadline-time.time()),exit_code=rc,
                        best_raw=best,best_scaled=bestscaled,mp_calls=db.execute("SELECT COUNT(*) FROM mpchecks").fetchone()[0],
                        process_id=os.getpid(),finished_optimizer_restarts=db.execute("SELECT COUNT(*) FROM done").fetchone()[0])
            atomic(out/"checkpoint.json",result)
            return result
        def verify(item):
            nonlocal hit
            count=db.execute("SELECT COUNT(*) FROM mpchecks").fetchone()[0]
            if count>=cfg["max_mp"]:raise Stop("high-precision quota exhausted")
            checkid=db.execute("INSERT INTO mpchecks(call_id,status) VALUES(?,?)",(item["call_id"],"RESERVED")).lastrowid
            try:
                check=core.mp_review(item["theta"])
                db.execute("UPDATE mpchecks SET status='OK',record=? WHERE id=?",(js(check),checkid))
                atomic(out/f"mp_{checkid:03d}.json",check)
                if check["robust_candidate"]:
                    atomic(out/"candidate.json",check);hit=True;raise Stop("robust positive candidate; independent review required")
            except Stop:raise
            except Exception as exc:
                db.execute("UPDATE mpchecks SET status='FAILED',record=? WHERE id=?",(js(dict(error=str(exc))),checkid))
        def evaluate(theta,stage,seq):
            nonlocal best,bestscaled
            db.execute("BEGIN IMMEDIATE")
            used=meta("used")
            local=db.execute("SELECT COUNT(*) FROM calls WHERE stage=?",(stage,)).fetchone()[0]
            if used>=cfg["max_calls"] or time.time()>=deadline or (stage.startswith("opt_") and local>=cfg["per_restart"]):
                db.execute("ROLLBACK");raise Stop("registered objective or time limit")
            callid=db.execute("INSERT INTO calls(stage,seq,theta,status) VALUES(?,?,?,?)",(stage,seq,js(list(map(float,theta))),"RESERVED")).lastrowid
            db.execute("UPDATE meta SET v=? WHERE k='used'",(js(used+1),));db.execute("COMMIT")
            try:
                item=core.model(theta);item.update(call_id=callid,stage=stage,seq=seq)
                db.execute("UPDATE calls SET status='OK',record=? WHERE id=?",(js(item),callid))
                if best is None or item["raw_max_hessian"]>best["raw_max_hessian"]:best=item
                if bestscaled is None or item["scaled_max_hessian"]>bestscaled["scaled_max_hessian"]:bestscaled=item
                if item["raw_max_hessian"]>cfg["candidate_threshold"] and item["scaled_max_hessian"]>cfg["scaled_trigger"]:
                    verify(item)
                value=-item["scaled_max_hessian"]
            except (FloatingPointError,np.linalg.LinAlgError,ValueError) as exc:
                db.execute("UPDATE calls SET status='FAILED',record=? WHERE id=?",(js(dict(error=str(exc))),callid));value=1e8
            if callid%2000==0:
                snap=snapshot();print(js(dict(calls=snap["calls"],states=snap["states"],best_scaled=bestscaled["scaled_max_hessian"])),flush=True)
            return value
        status="INCOMPLETE";rc=0
        try:
            for idx in range(cfg["samples"]):
                if db.execute("SELECT 1 FROM calls WHERE stage='scan' AND seq=?",(idx,)).fetchone():continue
                evaluate(point(cfg["seed"],idx),"scan",idx)
            if cfg["restarts"]:
                from scipy.optimize import minimize
                for restart in range(cfg["restarts"]):
                    stage=f"opt_{restart:02d}"
                    if db.execute("SELECT 1 FROM done WHERE stage=?",(stage,)).fetchone():continue
                    theta=np.array(bestscaled["theta"]) if restart%4==0 else point(cfg["seed"]+1,restart)
                    reason=""
                    try:
                        sol=minimize(lambda x:evaluate(x,stage,0),theta,method="L-BFGS-B",
                                     bounds=[(-14,14),(-14,14),(-32,float(np.log(24)))],
                                     options=dict(maxiter=150,maxfun=cfg["per_restart"],ftol=1e-14,gtol=1e-10,maxls=20))
                        reason=str(sol.message)
                    except Stop as exc:
                        if hit or time.time()>=deadline:raise
                        reason=str(exc)
                    db.execute("INSERT OR REPLACE INTO done VALUES(?,?)",(stage,reason))
            # Explicit high precision checks of both raw and scale-normalized extrema.
            for item in (best,bestscaled):
                if item is not None and not db.execute("SELECT 1 FROM mpchecks WHERE call_id=?",(item["call_id"],)).fetchone():verify(item)
            status="INCOMPLETE_FINITE_ATTACK_COMPLETE"
        except Stop as exc:
            stop_reason=str(exc);status="DISPROVED_CANDIDATE" if hit else "INCOMPLETE_BUDGET_STOP"
        except Exception as exc:
            stop_reason=repr(exc);status="FAILED_RECOVERABLE";rc=1
        final=snapshot(status,rc);final["stop_reason"]=stop_reason
        final["mp_states"]=dict(db.execute("SELECT status,COUNT(*) FROM mpchecks GROUP BY status"))
        final["unique_call_ids"]=db.execute("SELECT COUNT(DISTINCT id) FROM calls").fetchone()[0]
        if rc==0:
            db.execute("INSERT OR REPLACE INTO meta VALUES('terminal',?)",(js(status),));atomic(out/"summary.json",final)
        print(js(dict(status=status,calls=final["calls"],states=final["states"],mp_states=final["mp_states"],exit_code=rc,elapsed=final["elapsed_seconds"])),flush=True)
        db.close();return rc

if __name__=="__main__":raise SystemExit(main())
