"""Read-only ledger audit; no Hessian objective calls."""
import json,sqlite3,sys,os,time
from pathlib import Path
out=Path(sys.argv[1] if len(sys.argv)>1 else 'formal')
db=sqlite3.connect('file:'+str(out/'state.sqlite')+'?mode=ro',uri=True)
rows=db.execute('SELECT id,kind,stage,status,detail FROM calls ORDER BY id').fetchall()
raw_positive_ids=set();reviewed140=set();best_hp=None;rawbest=None;hp_full={}
states={};kinds={};stages={};fails={};modes={};margins={};hp=[]
for ident,kind,stage,status,detail in rows:
    z=json.loads(detail);states[status]=states.get(status,0)+1;kinds[kind]=kinds.get(kind,0)+1;stages[stage]=stages.get(stage,0)+1
    if kind=='FLOAT_HESSIAN' and status=='OK':
        if z['raw_max_hessian']>1e-8:raw_positive_ids.add(ident)
        if rawbest is None or z['raw_max_hessian']>rawbest['raw_max_hessian']:rawbest=z
    if kind=='MP_HESSIAN' and status=='OK' and z['dps']==140:
        reviewed140.add(z.get('source_call'));hp_full[z.get('source_call')]=z
        if best_hp is None or float(z['largest_hessian'])>float(best_hp['largest_hessian']):best_hp=z
    if status=='FAILED':fails[z.get('error','unknown')]=fails.get(z.get('error','unknown'),0)+1
    if kind=='MP_HESSIAN' and status=='OK':hp.append(dict(call_id=ident,stage=stage,dps=z['dps'],max_hessian=z['largest_hessian'],alternate_directional=z['alternate_directional'],chords=z['chords'],gate=z['positive_gate']))
    if kind=='FLOAT_HESSIAN' and status=='OK':
        key=z['kind']+('_weak' if min(v for v in z['edge_magnitudes'] if v>0)<1e-7 else '_general');modes[key]=modes.get(key,0)+1
        margin=z['spectral_margin'];bucket='>=1e-2' if margin>=1e-2 else '1e-6..1e-2' if margin>=1e-6 else '<1e-6';margins[bucket]=margins.get(bucket,0)+1
proc=json.loads((out/'launch.json').read_text());live={}
for key in ('supervisor_pid','worker_pid'):
    try:os.kill(proc[key],0);live[key]=True
    except ProcessLookupError:live[key]=False
result=dict(epoch=time.time(),used=len(rows),unique_ids=len(set(z[0] for z in rows)),continuous_ids=[z[0] for z in rows]==list(range(1,len(rows)+1)),
  states=states,kinds=kinds,stages=stages,failures=fails,modes=modes,margins=margins,high_precision=hp,live=live,
  raw_positive_objects=len(raw_positive_ids),raw_positive_reviewed140=len(raw_positive_ids & reviewed140),raw_positive_unreviewed140=len(raw_positive_ids-reviewed140),
  hp_positive_gates=sum(z['gate'] for z in hp),best_hp=best_hp,rawbest_hp=hp_full.get(rawbest['call_id']) if rawbest else None)
if best_hp and best_hp.get('source_call'):
    result['best_hp_source']=json.loads(db.execute('SELECT detail FROM calls WHERE id=?',(best_hp['source_call'],)).fetchone()[0])
    from fractions import Fraction
    from math import lcm
    vals=[[Fraction(str(v)) for v in row] for row in result['best_hp_source']['K']]
    den=lcm(*(v.denominator for row in vals for v in row))
    result['best_hp_fixed_decimal_kernel']=dict(denominator=str(den),numerator=[[str(int(v*den)) for v in row] for row in vals])
if (out/'precision_launch.json').exists():
    ident=json.loads((out/'precision_launch.json').read_text())['pid']
    try:os.kill(ident,0);result['precision_live']=True
    except ProcessLookupError:result['precision_live']=False
for name in ('summary.json','checkpoint.json','process_exit.json','precision_exit.json'):
    if (out/name).exists():result[name]=json.loads((out/name).read_text())
if '--compact' in sys.argv:
    print(json.dumps({k:v for k,v in result.items() if k not in ('high_precision','summary.json','checkpoint.json')},indent=2))
else:print(json.dumps(result,indent=2))
