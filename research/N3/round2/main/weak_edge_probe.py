"""Fixed weak-edge sign mechanism check, distinct from root scanning."""
from beta_probe import *

def main():
    start=time.time();rows=[]
    for diagonal in ((Q(1,2),)*3,(Q(1,5),Q(2,5),Q(7,10)),(Q(1,10),Q(1,4),Q(2,5))):
        for sign in (-1,1):
            for scale in (Q(1,100),Q(1,1000)):
                K=[[diagonal[i] if i==j else Q(0) for j in range(3)] for i in range(3)]
                for edge,(i,j) in zip((1,2,3*sign),g.COORDS[3:]):K[i][j]=K[j][i]=scale*edge
                rec=quantities(K,120);rec.update(diagonal=diagonal,sign=sign,scale=scale);rows.append(rec)
    report=dict(status='SCOUT_SIGN_MECHANISM_ONLY',pid=os.getpid(),threads=1,seed=None,deterministic=True,
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                dependency_sha256=hashlib.sha256((HERE/'beta_probe.py').read_bytes()).hexdigest(),
                command='python research/N3/round2/main/weak_edge_probe.py',executed_centers=len(rows),rows=rows,
                elapsed_seconds=time.time()-start,exit_code=0)
    (HERE/'weak_edge_probe.json').write_text(json.dumps(g.encode(report),indent=2)+'\n')
    for row in rows:print(row['diagonal'],row['sign'],row['scale'],'beta',str(row['beta']),'dalpha',str(row['d_alpha']),flush=True)
    print('PID',os.getpid(),'executed',len(rows),'exit',0,flush=True)
if __name__=='__main__':main()
