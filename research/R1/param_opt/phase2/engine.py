"""Durable pre-reserved objective-call budget for R1 P2-01 only."""
import numerics as nu
import argparse
import contextlib
import hashlib
import json
import os
from pathlib import Path
import platform
import sqlite3
import sys
import time
import traceback
import numpy as np

ROOT=Path(__file__).resolve().parent

class BudgetStop(Exception):
    pass

@contextlib.contextmanager
def exclusive_lock(path):
    handle=path.open("a+b")
    try:
        if os.name=="nt":
            import msvcrt
            handle.seek(0);handle.write(b"0");handle.flush();handle.seek(0)
            msvcrt.locking(handle.fileno(),msvcrt.LK_NBLCK,1)
        else:
            import fcntl
            fcntl.flock(handle.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
    except (OSError,BlockingIOError):
        handle.close()
        raise RuntimeError("Another process holds this run's exclusive lock")
    try:
        yield
    finally:
        handle.close()

def atomic_json(path,data):
    tmp=path.with_suffix(path.suffix+".tmp")
    with tmp.open("w",encoding="utf-8") as fh:
        json.dump(data,fh,indent=2,allow_nan=False);fh.flush();os.fsync(fh.fileno())
    os.replace(tmp,path)

def dump(value):
    return json.dumps(value,allow_nan=False,separators=(",",":"))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",required=True)
    ap.add_argument("--mode",choices=("formal","smoke","pilot"),default="formal")
    ap.add_argument("--seed",type=int,default=20260908210)
    ap.add_argument("--stop-after-run-calls",type=int,default=0)
    ap.add_argument("--resume",action="store_true")
    args=ap.parse_args()
    out=(ROOT/args.out).resolve()
    if not out.is_relative_to(ROOT) or out==ROOT:
        raise RuntimeError("Output must be a strict child of the phase2 directory")
    out.mkdir(parents=True,exist_ok=True)
    config=dict(mode=args.mode,seed=args.seed,dimensions=([3,10] if args.mode=="pilot" else list(range(3,11))),bands=nu.BANDS,
                restarts=2 if args.mode=="formal" else 1,
                per_restart=750 if args.mode=="formal" else 64 if args.mode=="pilot" else 2,
                scouts=16 if args.mode=="formal" else 4 if args.mode=="pilot" else 2,
                max_calls=48000 if args.mode=="formal" else 512 if args.mode=="pilot" else 64,
                wall_seconds=5400 if args.mode=="formal" else 300,
                threads=1,memory_bytes=12*1024**3,positive_threshold=1e-6,
                deadline_semantics="absolute wall-clock deadline from initial run, including interruptions",
                source_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/"engine.py",ROOT/"numerics.py")})
    if args.mode=="formal" and os.name!="nt":
        import resource
        resource.setrlimit(resource.RLIMIT_AS,(12*1024**3,12*1024**3))
        resource.setrlimit(resource.RLIMIT_CPU,(5390,5400))
    with exclusive_lock(out/"run.lock"):
        db=sqlite3.connect(out/"state.sqlite",timeout=30,isolation_level=None)
        db.execute("PRAGMA journal_mode=WAL")
        db.execute("PRAGMA synchronous=FULL")
        db.executescript("""
        CREATE TABLE IF NOT EXISTS meta(key TEXT PRIMARY KEY,value TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS invocations(id INTEGER PRIMARY KEY,started REAL,ended REAL,pid INTEGER,exit_code INTEGER,status TEXT);
        CREATE TABLE IF NOT EXISTS evaluations(id INTEGER PRIMARY KEY,cell TEXT,restart INTEGER,stage TEXT,x TEXT,status TEXT,record TEXT,started REAL,ended REAL);
        CREATE INDEX IF NOT EXISTS eval_cell ON evaluations(cell,restart);
        CREATE TABLE IF NOT EXISTS finished(cell TEXT,restart INTEGER,reason TEXT,PRIMARY KEY(cell,restart));
        CREATE TABLE IF NOT EXISTS best(cell TEXT PRIMARY KEY,value REAL,object TEXT);
        """)
        def meta(key,default=None):
            row=db.execute("SELECT value FROM meta WHERE key=?",(key,)).fetchone()
            return json.loads(row[0]) if row else default
        stored=meta("config")
        if stored is None:
            if args.resume:
                raise RuntimeError("No existing checkpoint to resume")
            for key,value in (("config",config),("started",time.time()),("used",0)):
                db.execute("INSERT INTO meta VALUES(?,?)",(key,dump(value)))
            atomic_json(out/"config.json",config)
        elif dump(stored)!=dump(config):
            raise RuntimeError("Immutable run configuration/source mismatch")
        elif not args.resume:
            raise RuntimeError("Run exists; inspect and use explicit --resume")
        if meta("terminal_status") is not None:
            print(dump(dict(status="ALREADY_TERMINAL",terminal=meta("terminal_status"),calls=meta("used"))))
            return 0
        now=time.time()
        runid=db.execute("INSERT INTO invocations(started,pid,status) VALUES(?,?,?)",(now,os.getpid(),"RUNNING")).lastrowid
        # Any reservation left by a previous interrupted invocation remains spent.
        db.execute("UPDATE evaluations SET status='INTERRUPTED_UNKNOWN',ended=? WHERE status='RESERVED'",(now,))
        deadline=meta("started")+config["wall_seconds"]
        run_calls=0
        candidate=False
        def snapshot(status="RUNNING",exit_code=None):
            rows=db.execute("SELECT cell,status,COUNT(*) FROM evaluations GROUP BY cell,status").fetchall()
            counts={}
            for cell,state,num in rows:
                counts.setdefault(cell,{})[state]=num
            b=db.execute("SELECT value,object FROM best ORDER BY value DESC LIMIT 1").fetchone()
            best=json.loads(b[1]) if b else None
            result=dict(status=status,seed=args.seed,used_calls=meta("used"),max_calls=config["max_calls"],
                        per_cell=counts,completed_restarts=db.execute("SELECT COUNT(*) FROM finished").fetchone()[0],
                        requested_restarts=len(config["dimensions"])*len(config["bands"])*config["restarts"],
                        remaining_wall_seconds=max(0,deadline-time.time()),elapsed_wall_seconds=time.time()-meta("started"),
                        exit_code=exit_code,latest_invocation_pid=os.getpid(),best=best,
                        limitations="Finite numerical search only; author cross-checks are not independent certification.")
            atomic_json(out/"checkpoint.json",result)
            if best:
                atomic_json(out/"best.json",best)
            return result
        def reserve(cell,restart,stage,x):
            nonlocal run_calls
            db.execute("BEGIN IMMEDIATE")
            try:
                used=meta("used")
                local=db.execute("SELECT COUNT(*) FROM evaluations WHERE cell=? AND restart=?",(cell,restart)).fetchone()[0]
                if used>=config["max_calls"] or local>=config["per_restart"] or time.time()>=deadline:
                    raise BudgetStop("registered total, restart, or wall budget exhausted")
                if args.stop_after_run_calls and run_calls>=args.stop_after_run_calls:
                    raise BudgetStop("explicit checkpoint pause")
                idx=db.execute("INSERT INTO evaluations(cell,restart,stage,x,status,started) VALUES(?,?,?,?,?,?)",
                    (cell,restart,stage,dump(x.tolist()),"RESERVED",time.time())).lastrowid
                db.execute("UPDATE meta SET value=? WHERE key='used'",(dump(used+1),))
                db.execute("COMMIT")
                run_calls+=1
                return idx
            except Exception:
                db.execute("ROLLBACK")
                raise
        def evaluate(x,n,band,restart,stage):
            nonlocal candidate
            cell=f"n{n:02d}_band{band}"
            idx=reserve(cell,restart,stage,x)
            record=dict(seed=args.seed,n=n,band=band,band_bounds=nu.BANDS[band],restart=restart,
                        complement=restart%2,stage=stage,call_id=idx)
            try:
                value,k,v,diag=nu.evaluate(x,n,band,restart%2)
                record.update(diag)
                previous=db.execute("SELECT value FROM best WHERE cell=?",(cell,)).fetchone()
                if previous is None or value>previous[0]:
                    obj=dict(K=k.tolist(),V=v.tolist(),parameters=x.tolist(),record=record)
                    try:
                        obj["chords"]=nu.chord(k,v)
                        obj["alternate_directional"]=nu.signed_directional(k,v)
                    except (FloatingPointError,np.linalg.LinAlgError,ValueError) as exc:
                        obj["chord_or_alternate_failure"]=str(exc)
                    db.execute("INSERT OR REPLACE INTO best VALUES(?,?,?)",(cell,value,dump(obj)))
                if value>config["positive_threshold"]:
                    alt=nu.signed_directional(k,v)
                    record["alternate_directional"]=alt
                    obj=dict(status="NUMERICAL_HIT_AWAITING_INDEPENDENT_RECOMPUTATION",K=k.tolist(),V=v.tolist(),parameters=x.tolist(),record=record,chords=nu.chord(k,v))
                    atomic_json(out/f"hit_{idx:06d}.json",obj)
                    candidate=True
                state="OK"
                result=-value
            except (FloatingPointError,np.linalg.LinAlgError,ValueError) as exc:
                state="FAILED";record["error"]=str(exc);result=1e8
            db.execute("UPDATE evaluations SET status=?,record=?,ended=? WHERE id=?",(state,dump(record),time.time(),idx))
            if idx%100==0 or candidate:
                info=snapshot()
                print(dump({k:info[k] for k in ("status","used_calls","completed_restarts","remaining_wall_seconds")}),flush=True)
            if candidate:
                raise BudgetStop("positive numerical hit; independent review required")
            return result
        status="RUNNING";exit_code=0
        try:
            for band in range(4):
                for n in config["dimensions"]:
                    cell=f"n{n:02d}_band{band}"
                    for restart in range(config["restarts"]):
                        if db.execute("SELECT 1 FROM finished WHERE cell=? AND restart=?",(cell,restart)).fetchone():
                            continue
                        if time.time()>=deadline or meta("used")>=config["max_calls"]:
                            raise BudgetStop("registered global budget exhausted")
                        reason="restart budget exhausted"
                        try:
                            for scout in range(config["scouts"]):
                                stage=f"scout_{scout}"
                                if db.execute("SELECT 1 FROM evaluations WHERE cell=? AND restart=? AND stage=?",(cell,restart,stage)).fetchone():
                                    continue
                                evaluate(nu.initial_x(args.seed,n,band,restart,scout),n,band,restart,stage)
                            if config["per_restart"]>config["scouts"]:
                                from scipy.optimize import minimize
                                rows=db.execute("SELECT x,record FROM evaluations WHERE cell=? AND restart=? AND status='OK'",(cell,restart)).fetchall()
                                if rows:
                                    bx,_=max(rows,key=lambda row:json.loads(row[1])["max_hessian"])
                                    used=db.execute("SELECT COUNT(*) FROM evaluations WHERE cell=? AND restart=?",(cell,restart)).fetchone()[0]
                                    remain=config["per_restart"]-used
                                    if remain>0:
                                        solution=minimize(lambda x:evaluate(x,n,band,restart,"lbfgsb"),np.array(json.loads(bx)),
                                            method="L-BFGS-B",bounds=[(-12,12)]*(len(nu.layout(n)[3])+2),
                                            options=dict(maxiter=100,maxfun=remain,ftol=1e-14,gtol=1e-9,maxls=20))
                                        reason=str(solution.message)
                        except BudgetStop as exc:
                            if candidate or time.time()>=deadline or (args.stop_after_run_calls and run_calls>=args.stop_after_run_calls):
                                raise
                            reason=str(exc)
                        db.execute("INSERT OR REPLACE INTO finished VALUES(?,?,?)",(cell,restart,reason))
                        snapshot()
            status="INCOMPLETE_FINITE_BATCH_COMPLETE"
        except BudgetStop as exc:
            status=("NUMERICAL_HIT_AWAITING_INDEPENDENT_RECOMPUTATION" if candidate else
                    "PAUSED_CHECKPOINT" if args.stop_after_run_calls and run_calls>=args.stop_after_run_calls and time.time()<deadline else
                    "INCOMPLETE_REGISTERED_BUDGET_EXHAUSTED")
            print(dump(dict(reason=str(exc),status=status)),flush=True)
        except Exception:
            status="FAILED_RECOVERABLE";exit_code=1;traceback.print_exc()
        finally:
            db.execute("UPDATE invocations SET ended=?,exit_code=?,status=? WHERE id=?",(time.time(),exit_code,status,runid))
            summary=snapshot(status,exit_code)
            if status not in ("PAUSED_CHECKPOINT","FAILED_RECOVERABLE"):
                db.execute("INSERT OR REPLACE INTO meta VALUES('terminal_status',?)",(dump(status),))
                atomic_json(out/"summary.json",summary)
            atomic_json(out/"invocation_result.json",dict(invocation=runid,status=status,exit_code=exit_code,run_calls=run_calls,total_calls=meta("used")))
            print(dump(dict(status=status,exit_code=exit_code,run_calls=run_calls,total_calls=meta("used"))),flush=True)
            db.close()
        return exit_code

if __name__=="__main__":
    raise SystemExit(main())

