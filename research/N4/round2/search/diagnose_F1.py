"""Read-only mechanism diagnosis of the already recorded F1; no new centers."""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key]='1'
import json
from pathlib import Path
from fractions import Fraction
import numpy as np

base=Path(__file__).parent/'F1'
records=[json.loads(x) for x in (base/'cases.jsonl').read_text().splitlines()]
scale=np.array([1,1,1,2**.5,2**.5,2**.5])
def arr(x): return np.asarray(x,dtype=float)
def eigmax(x): return float(np.linalg.eigvalsh(x)[-1])
def split_direction(r,v):
    p=arr(r['event_p']);g=arr(r['event_gradient']);j=arr(r['event_hessian'])
    dp=g@v;ddp=np.einsum('sij,i,j->s',j,v,v)
    negf=-dp*dp/p;acc=-ddp*np.log(p)
    return [dict(cardinality=k,negative_fisher=float(sum(negf[s] for s in range(15) if s.bit_count()==k)),
                 acceleration=float(sum(acc[s] for s in range(15) if s.bit_count()==k)),
                 curvature=float(sum(acc[s]+negf[s] for s in range(15) if s.bit_count()==k)),
                 mass_second=float(sum(ddp[s] for s in range(15) if s.bit_count()==k)),
                 literal_layer_entropy_second=float(sum(acc[s]+negf[s]-ddp[s] for s in range(15) if s.bit_count()==k))) for k in range(4)]

rows=[]
for r in records:
    ac=arr(r['acceleration']);f=arr(r['fisher_positive'])
    ev,q=np.linalg.eigh(ac/np.outer(scale,scale));v=q[:,-1]/scale
    layers=split_direction(r,v)
    top=r['top_direction'];triple=top['cardinality_layers'][3].copy()
    triple['mass_second']=sum(float(top['event_ddp'][s]) for s in range(15) if s.bit_count()==3)
    triple['literal_layer_entropy_second']=triple['curvature']-triple['mass_second']
    rows.append(dict(index=r['index'],frame=r['meta']['frame_index'],spectrum=r['meta']['spectrum_name'],
        lambda_max=r['lambda_max'],top_acceleration=float(top['acceleration']),
        top_negative_fisher=float(top['negative_fisher']),top_triple=triple,
        acceleration_max=float(ev[-1]),acceleration_max_direction_raw_basis=v.tolist(),
        acceleration_max_direction_negative_fisher=-float(v@f@v),
        acceleration_max_direction_curvature=float(v@(ac-f)@v),
        acceleration_max_direction_layers=layers))

frames=[]
for fi in range(6):
    rr=[r for r in records if r['meta']['frame_index']==fi]
    best=max(rr,key=lambda r:r['lambda_max']);z=np.array([float(Fraction(x)) for x in best['z']]);q=z*z
    frames.append(dict(frame=fi,z=best['z'],q=q.tolist(),entropy_q=float(-q@np.log(q)),min_abs_z=float(min(abs(z))),
        best_index=best['index'],best_spectrum=best['meta']['spectrum_name'],lambda_max=best['lambda_max'],
        top_negative_fisher=float(best['top_direction']['negative_fisher']),
        top_acceleration=float(best['top_direction']['acceleration'])))
summary=dict(status='DIAGNOSTIC_ONLY_NO_NEW_CENTERS',centers=len(records),
    layer_convention='curvature C_k=-sum(dp^2/p+ddp*logp); sum C_k=Hsecond; literal layer entropy second=C_k-mass_second',
    max_curvature_record=max(rows,key=lambda r:r['lambda_max']),
    max_top_acceleration_record=max(rows,key=lambda r:r['top_acceleration']),
    max_acceleration_eigenvalue_record=max(rows,key=lambda r:r['acceleration_max']),
    negative_top_acceleration_count=sum(r['top_acceleration']<0 for r in rows),
    positive_top_triple_acceleration_count=sum(r['top_triple']['acceleration']>0 for r in rows),
    positive_top_triple_total_count=sum(r['top_triple']['curvature']>0 for r in rows),
    positive_acceleration_eigenvalue_count=sum(r['acceleration_max']>0 for r in rows),
    frames=frames,all_rows=rows)
(base/'mechanism_diagnostic.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in summary.items() if k!='all_rows'},indent=2))
