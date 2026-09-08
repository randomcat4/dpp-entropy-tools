"""Same 180 centers; test conditional Q only on actual Fisher/A minimizers."""
import hashlib,json,os,time
from pathlib import Path
import mpmath as mp
from unequal_sparse_probe import BASELINE,events,kernel
from conditional_q_attack import objects

def main():
    start=time.time(); old=json.loads(Path('research/N3/falsification/batch.json').read_text())['rows']; rows=[]
    for oldrow in old:
        spec=oldrow['spec']; mp.mp.dps=110+3*spec['digits']*max(spec['rates'])
        K=kernel(spec); Q,G,eta,det,E=objects(K); p,J=events(K); F=J.T*mp.diag([1/x for x in p])*J
        row=dict(spec=spec)
        for name,M in [('F',F),('A',F+G)]:
            v=mp.lu_solve(M,eta); d=v/(eta.T*v)[0]; C=det-(d.T*G*d)[0]
            gaps=[((d.T*q*d)[0]-C)/det for q in Q]
            D=sum((d[i]*E[i] for i in range(6)),mp.zeros(3)); D/=max(abs(x) for x in D)
            row[name]=dict(max_gap=mp.nstr(max(gaps),55),gaps=[mp.nstr(x,55) for x in gaps],
                           cofactor_scaled=mp.nstr(C/det,55), Q_scaled=[mp.nstr((d.T*q*d)[0]/det,55) for q in Q],
                           B_scaled=mp.nstr(((d.T*F*d)[0]-C)/det,55),
                           D=[[mp.nstr(D[i,j],70) for j in range(3)] for i in range(3)])
        rows.append(row)
    out=dict(status='INCOMPLETE',baseline=BASELINE,pid=os.getpid(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             kernel_calls=len(rows),direction_calls=2*len(rows),rejected=0,rows=rows,
             best={n:min(rows,key=lambda r:mp.mpf(r[n]['max_gap'])) for n in ['F','A']},
             negative_counts={n:sum(mp.mpf(r[n]['max_gap'])<0 for r in rows) for n in ['F','A']},
             elapsed_seconds=time.time()-start,exit_status=0)
    Path('research/N3/falsification/optimal_direction.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['status','pid','kernel_calls','direction_calls','negative_counts','elapsed_seconds']}))
    for n in ['F','A']: print(n,json.dumps(out['best'][n]))

if __name__=='__main__':main()
