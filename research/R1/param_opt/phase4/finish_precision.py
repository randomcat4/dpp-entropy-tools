"""Terminal-only continuation of the SAME ledger: no additional search calls."""
import argparse,json,os,sqlite3,time,sys,resource
from pathlib import Path
from n3core import mp_review
from attack import dump
p=argparse.ArgumentParser();p.add_argument('--out',default='formal');a=p.parse_args();out=Path(a.out)
launch=json.loads((out/'launch.json').read_text());config=json.loads((out/'config.json').read_text())
resource.setrlimit(resource.RLIMIT_AS,(10*1024**3,10*1024**3))
remaining=max(1,int(launch['absolute_deadline']-time.time()))
resource.setrlimit(resource.RLIMIT_CPU,(remaining,remaining+1))
for key in ('worker_pid','supervisor_pid'):
    try:os.kill(launch[key],0)
    except ProcessLookupError:continue
    raise SystemExit('Original process still exists: refuse concurrent ledger use')
if not(out/'process_exit.json').exists():raise SystemExit('No original terminal exit record')
db=sqlite3.connect(out/'state.sqlite');db.execute('PRAGMA synchronous=FULL')
rows=db.execute('SELECT id,kind,status,detail FROM calls ORDER BY id').fetchall()
reviewed=set();candidates=[]
for ident,kind,status,detail in rows:
    z=json.loads(detail)
    if kind=='MP_HESSIAN' and status=='OK' and z.get('dps')==140:reviewed.add(z.get('source_call'))
    if kind=='FLOAT_HESSIAN' and status=='OK' and z['raw_max_hessian']>1e-8:candidates.append(z)
start=time.time();done=0;failure=0;reason='all_raw_positive_reviewed';found=False
dump(out/'precision_launch.json',dict(pid=os.getpid(),start_epoch=start,absolute_deadline=launch['absolute_deadline'],remaining_cap=config['cap']-len(rows),raw_positive_objects=len(candidates),already_reviewed=len([z for z in candidates if z['call_id'] in reviewed])))
try:
    for obj in sorted(candidates,key=lambda z:z['raw_max_hessian'],reverse=True):
        if obj['call_id'] in reviewed:continue
        reports=[]
        for dps in (90,140):
            db.execute('BEGIN IMMEDIATE');n=db.execute('SELECT count(*) FROM calls').fetchone()[0]
            if n>=config['cap'] or time.time()>=launch['absolute_deadline']:db.rollback();raise TimeoutError()
            ident=n+1;db.execute('INSERT INTO calls VALUES(?,?,?,?,?,?)',(ident,'MP_HESSIAN','terminal_positive_audit',time.time(),'RESERVED','{}'));db.commit()
            try:
                res=mp_review(obj['K'],dps);res.update(call_id=ident,source_call=obj['call_id']);status='OK';reports.append(res)
            except Exception as e:res=dict(error=repr(e),source_call=obj['call_id'],K=obj['K'],dps=dps);status='FAILED';failure+=1
            db.execute('UPDATE calls SET status=?,detail=? WHERE id=?',(status,json.dumps(res),ident));db.commit()
        done+=1
        with (out/'terminal_precision.jsonl').open('a') as f:f.write(json.dumps(reports)+'\n')
        if len(reports)==2 and all(z['positive_gate'] for z in reports):
            dump(out/'candidate.json',dict(status='DISPROVED_CANDIDATE',source=obj,reviews=reports));reason='robust_positive_pause';found=True;break
except TimeoutError:reason='original_budget_or_deadline'
finally:
    statuses=dict(db.execute('SELECT status,count(*) FROM calls GROUP BY status').fetchall())
    dump(out/'precision_exit.json',dict(exit_code=0,status='DISPROVED_CANDIDATE' if found else 'INCOMPLETE',reason=reason,
      wall_seconds=time.time()-start,objects_reviewed=done,additional_failures=failure,used=sum(statuses.values()),statuses=statuses,end_epoch=time.time()))
    db.close()
