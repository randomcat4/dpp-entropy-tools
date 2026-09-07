"""Single supervised formal job; preserve actual subprocess exit status."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from engine import atomic_json,exclusive_lock

root=Path(__file__).resolve().parent
ap=argparse.ArgumentParser()
ap.add_argument("--supervise",action="store_true")
ap.add_argument("--resume",action="store_true")
args=ap.parse_args()
formal=root/"formal"
formal.mkdir(exist_ok=True)
if (formal/"summary.json").exists():
    raise SystemExit("Formal run already terminal; do not repeat or extend")

if args.supervise:
    with exclusive_lock(root/"supervisor.lock"):
        with exclusive_lock(formal/"run.lock"):
            pass
        cmd=[sys.executable,str(root/"engine.py"),"--out","formal","--mode","formal","--seed","20260908210"]
        if args.resume:
            cmd.append("--resume")
        with (formal/"stdout.log").open("ab") as log:
            proc=subprocess.Popen(cmd,cwd=root,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT)
            record=dict(supervisor_pid=os.getpid(),pid=proc.pid,command=cmd,started=time.time(),threads=1,
                        memory_limit_bytes=12*1024**3,maximum_objective_calls=48000,wall_seconds=5400)
            atomic_json(formal/"process.json",record)
            rc=proc.wait()
            record.update(exit_code=rc,ended=time.time())
            atomic_json(formal/"process_exit.json",record)
            print(json.dumps(record),flush=True)
            raise SystemExit(rc)
else:
    # Kernel locks, rather than PID reuse assumptions, check that neither the
    # worker nor its supervisor is currently running before requesting a launch.
    with exclusive_lock(root/"supervisor.lock"):
        with exclusive_lock(formal/"run.lock"):
            pass
    cmd=[sys.executable,str(Path(__file__).resolve()),"--supervise"]
    if args.resume:
        cmd.append("--resume")
    with (root/"supervisor_stdout.log").open("ab") as log:
        proc=subprocess.Popen(cmd,cwd=root,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
    print(json.dumps(dict(supervisor_pid=proc.pid,command=cmd)),flush=True)
