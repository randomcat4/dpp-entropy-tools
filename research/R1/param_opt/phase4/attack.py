"""Bounded n=3 falsification. Every float/MP Hessian reserves a durable ID first."""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[key]='1'
os.environ['CUDA_VISIBLE_DEVICES']=''
import argparse,json,time,sqlite3,traceback,sys
from pathlib import Path
import numpy as np
from n3core import evaluate,sample,mp_review

class StopBudget(Exception):pass
class Found(Exception):pass
def dump(path,obj):
    temp=path.with_suffix(path.suffix+'.tmp');temp.write_text(json.dumps(obj,indent=2,allow_nan=False));temp.replace(path)
class Run:
    def __init__(self,args):
        self.a=args;self.out=Path(args.out);self.out.mkdir(exist_ok=True,parents=True)
        self.db=sqlite3.connect(self.out/'state.sqlite');self.db.execute('PRAGMA journal_mode=WAL');self.db.execute('PRAGMA synchronous=FULL')
        self.db.execute('CREATE TABLE IF NOT EXISTS calls(id INTEGER PRIMARY KEY,kind TEXT,stage TEXT,stamp REAL,status TEXT,detail TEXT)')
        self.db.commit();self.best=None;self.best_raw=None;self.pool=[];self.mp_checks=0;self.raw_positive=0;self.start=time.time()
        # This unit does not automatically resume. Existing ledgers are never overwritten.
        if self.db.execute('SELECT count(*) FROM calls').fetchone()[0]:raise RuntimeError('existing ledger: refuse duplicate unit')
    def reserve(self,kind,stage):
        self.db.execute('BEGIN IMMEDIATE')
        n=self.db.execute('SELECT count(*) FROM calls').fetchone()[0]
        if n>=self.a.cap or time.time()>=self.a.deadline:self.db.rollback();raise StopBudget()
        ident=n+1;self.db.execute('INSERT INTO calls VALUES(?,?,?,?,?,?)',(ident,kind,stage,time.time(),'RESERVED','{}'));self.db.commit();return ident
    def finish(self,ident,status,detail):
        self.db.execute('UPDATE calls SET status=?,detail=? WHERE id=?',(status,json.dumps(detail,allow_nan=False),ident));self.db.commit()
    def stats(self):
        rows=dict(self.db.execute('SELECT status,count(*) FROM calls GROUP BY status').fetchall())
        return dict(used=sum(rows.values()),statuses=rows,unique_ids=self.db.execute('SELECT count(DISTINCT id) FROM calls').fetchone()[0],
          min_id=self.db.execute('SELECT min(id) FROM calls').fetchone()[0],max_id=self.db.execute('SELECT max(id) FROM calls').fetchone()[0])
    def checkpoint(self):
        dump(self.out/'checkpoint.json',dict(seed=self.a.seed,deadline=self.a.deadline,cap=self.a.cap,wall_seconds=time.time()-self.start,
          raw_positive=self.raw_positive,mp_checks=self.mp_checks,best=self.best,best_raw=self.best_raw,**self.stats()))
    def review(self,obj,stage):
        reports=[]
        for dps in (90,140):
            ident=self.reserve('MP_HESSIAN',stage)
            try:res=mp_review(obj['K'],dps);res.update(call_id=ident,source_call=obj.get('call_id'));self.finish(ident,'OK',res);reports.append(res)
            except Exception as e:self.finish(ident,'FAILED',dict(error=repr(e),K=obj['K']));return
        self.mp_checks+=1
        with (self.out/'high_precision.jsonl').open('a') as f:f.write(json.dumps(reports)+'\n')
        if all(z['positive_gate'] for z in reports):
            dump(self.out/'candidate.json',dict(status='DISPROVED_CANDIDATE',source=obj,reviews=reports));raise Found()
    def call(self,x,kind,signs,o,stage):
        ident=self.reserve('FLOAT_HESSIAN',stage)
        try:obj=evaluate(x,kind,signs,o);obj['call_id']=ident
        except Exception as e:
            self.finish(ident,'FAILED',dict(error=repr(e),parameters=list(map(float,x)),kind=kind,signs=list(map(int,signs)),orientation=int(o)))
            return -1e6
        self.finish(ident,'OK',obj)
        score=obj['scaled_max_hessian']
        if self.best is None or score>self.best['scaled_max_hessian']:self.best=obj;dump(self.out/'best.json',obj)
        if self.best_raw is None or obj['raw_max_hessian']>self.best_raw['raw_max_hessian']:self.best_raw=obj
        if obj['raw_max_hessian']>1e-8:self.raw_positive+=1
        if stage=='scan' and ident%3000==0:self.review(obj,'scheduled_precision_audit')
        if obj['raw_max_hessian']>1e-8 and score>1e-9 and self.mp_checks<60:self.review(obj,'positive_screen')
        if ident%500==0:self.checkpoint()
        if stage=='scan':
            self.pool.append(obj)
            # Retain separate path/triangle and weak/general seeds, not only flat seeds.
            grouped={}
            for z in self.pool:
                key=(z['kind'],min(z['edge_magnitudes'][j] for j in range(3) if z['edge_magnitudes'][j]>0)<1e-7)
                grouped.setdefault(key,[]).append(z)
            self.pool=[z for group in grouped.values() for z in sorted(group,key=lambda z:z['scaled_max_hessian'],reverse=True)[:6]]
        return score

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--seed',type=int,default=20260908411)
    ap.add_argument('--scan',type=int,default=100000);ap.add_argument('--restarts',type=int,default=24);ap.add_argument('--optcalls',type=int,default=1000)
    ap.add_argument('--cap',type=int,default=150000);ap.add_argument('--deadline',type=float,required=True);a=ap.parse_args();r=Run(a)
    dump(r.out/'config.json',dict(**vars(a),python=sys.version,numpy=np.__version__,start_epoch=r.start,threads=1,positive_threshold=1e-8,
      objective='largest eigenvalue of positive-diagonally congruent full 6x6 entropy Hessian',notes='Finite samples are not a proof. All high-precision calls count.'))
    reason='plan_complete';exitcode=0
    try:
        # Parent-provided S3 near-I false-positive object, fixed decimal interpretation.
        probe=dict(K=[['0.9999999999999885' if i==j else '-1.1102230246251565e-16' for j in range(3)] for i in range(3)])
        r.review(probe,'parent_s3_probe')
        for i in range(a.scan):r.call(*sample(a.seed,i),'scan')
        from scipy.optimize import minimize
        pool=list(r.pool)
        bounds=[(-4,4)]*3+[(-30,4)]*3+[(float(np.log(1e-12)),float(np.log(.25))),(-18,18)]
        for obj in pool[:a.restarts]:
            local=[0]
            def fun(x):
                if local[0]>=a.optcalls:raise StopIteration()
                local[0]+=1;return -r.call(x,obj['kind'],obj['signs'],obj['orientation'],'optimize')
            try:minimize(fun,obj['parameters'],method='Nelder-Mead',bounds=bounds,options=dict(maxfev=a.optcalls,xatol=1e-9,fatol=1e-12))
            except StopIteration:pass
        for obj in (r.best,r.best_raw):
            if obj:r.review(obj,'final_best_precision')
    except Found:reason='robust_positive_pause'
    except StopBudget:reason='budget_or_deadline'
    except Exception as e:reason='unexpected_error';exitcode=1;dump(r.out/'error.json',dict(error=repr(e),traceback=traceback.format_exc()))
    finally:
        r.checkpoint();dump(r.out/'summary.json',dict(status='DISPROVED_CANDIDATE' if reason=='robust_positive_pause' else 'INCOMPLETE',
          reason=reason,seed=a.seed,exit_code=exitcode,wall_seconds=time.time()-r.start,raw_positive=r.raw_positive,mp_checks=r.mp_checks,
          best=r.best,best_raw=r.best_raw,**r.stats()));r.db.close()
    return exitcode
if __name__=='__main__':sys.exit(main())
