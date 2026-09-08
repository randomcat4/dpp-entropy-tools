import csv, json
from pathlib import Path
from structure_search import Family
import numpy as np

root=Path(__file__).resolve().parent
rows=[]; batches=[]; families={}
for batch in ('batch01','batch02','batch03'):
    batches.append(json.loads((root/batch/'run_manifest.json').read_text()))
    for row in csv.DictReader((root/batch/'candidate_ledger.csv').open()):
        row['batch']=batch
        key=row['sizes']
        if key not in families: families[key]=Family(json.loads(key))
        f=families[key]
        _,C=f.unpack(json.loads(row['parameters']))
        off=C-np.diag(np.diag(C)); row['cross_coupling_norm']=float(np.linalg.norm(off))
        reached={0}
        for _ in range(f.g):
            reached.update(j for i in list(reached) for j in range(f.g) if abs(off[i,j])>1e-10)
        row['connected_at_1e-10']=len(reached)==f.g
        if row['direction']:
            _,dc=f.unpack(json.loads(row['direction']))
            row['cross_direction_norm']=float(np.linalg.norm(dc-np.diag(np.diag(dc))))
        rows.append(row)
with (root/'candidate_ledger.csv').open('w',newline='') as fp:
    writer=csv.DictWriter(fp,fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
valid=[r for r in rows if r['status']=='NO_HIT']
coupled=[r for r in valid if r['connected_at_1e-10']]
summary=dict(status='INCOMPLETE',attempts=len(rows),failures=sum(r['status']=='FAILED' for r in rows),candidate_count=sum(r['status']=='CANDIDATE' for r in rows),connected_count=len(coupled),numerically_disconnected_count=len(valid)-len(coupled),max_gap=max(float(r['gap']) for r in valid),best_curvature=max(float(r['largest_hessian_eigenvalue']) for r in valid),best_connected_curvature=max(float(r['largest_hessian_eigenvalue']) for r in coupled),max_connected_gap=max(float(r['gap']) for r in coupled),min_endpoint_margin=min(float(r['endpoint_margin']) for r in valid),sizes=sorted(set(r['sizes'] for r in rows)),batches=batches)
(root/'summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
