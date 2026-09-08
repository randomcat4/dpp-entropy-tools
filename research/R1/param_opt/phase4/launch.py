import argparse,json,os,resource,subprocess,sys,time
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--out',default='formal');p.add_argument('--scan',default='100000');p.add_argument('--restarts',default='24');p.add_argument('--optcalls',default='1000');p.add_argument('--cap',default='150000');p.add_argument('--seconds',type=int,default=3600);a=p.parse_args()
out=Path(a.out)
if out.exists():raise SystemExit('Existing output: refuse duplicate launch')
out.mkdir();start=time.time();deadline=min(1788864618,start+a.seconds)
os.environ.update(OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1',CUDA_VISIBLE_DEVICES='')
resource.setrlimit(resource.RLIMIT_AS,(10*1024**3,10*1024**3));resource.setrlimit(resource.RLIMIT_CPU,(a.seconds,a.seconds+2))
cmd=[sys.executable,'attack.py','--out',a.out,'--scan',a.scan,'--restarts',a.restarts,'--optcalls',a.optcalls,'--cap',a.cap,'--deadline',str(deadline)]
with (out/'process.log').open('w') as log:
    worker=subprocess.Popen(cmd,stdout=log,stderr=subprocess.STDOUT)
    (out/'launch.json').write_text(json.dumps(dict(supervisor_pid=os.getpid(),worker_pid=worker.pid,command=cmd,start_epoch=start,absolute_deadline=deadline),indent=2))
    code=worker.wait()
(out/'process_exit.json').write_text(json.dumps(dict(exit_code=code,wall_seconds=time.time()-start,end_epoch=time.time()),indent=2))
sys.exit(code)
