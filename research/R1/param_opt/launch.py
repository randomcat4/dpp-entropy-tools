"""Start one bounded CPU-only search without duplicating a live/completed job."""
import json
import os
from pathlib import Path
import resource
import subprocess
import sys

root = Path(__file__).resolve().parent
out = root / "batch01"
out.mkdir(exist_ok=True)
pidfile = out / "pid.json"
if (out / "summary.json").exists():
    raise SystemExit("Batch already finished; refusing to repeat")
if pidfile.exists():
    old = json.loads(pidfile.read_text())
    try:
        os.kill(old["pid"], 0)
    except ProcessLookupError:
        pass
    else:
        raise SystemExit(f"Existing process {old['pid']} may be live; inspect before resuming")
cmd = [sys.executable, str(root / "search.py"), "--out", str(out), "--seed", "202609081",
       "--samples", "20", "--steps", "30", "--nmin", "3", "--nmax", "10", "--seconds", "900"]
env = os.environ.copy()
for name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    env[name] = "1"
env["CUDA_VISIBLE_DEVICES"] = ""

def limits():
    resource.setrlimit(resource.RLIMIT_AS, (10 * 1024**3, 10 * 1024**3))
    resource.setrlimit(resource.RLIMIT_CPU, (960, 970))

with (out / "stdout.log").open("ab") as log:
    proc = subprocess.Popen(cmd, cwd=root, env=env, stdin=subprocess.DEVNULL,
                            stdout=log, stderr=subprocess.STDOUT,
                            start_new_session=True, preexec_fn=limits)
pidfile.write_text(json.dumps(dict(pid=proc.pid, command=cmd, cpu_threads=1, memory_limit_bytes=10*1024**3), indent=2))
print(pidfile.read_text())
