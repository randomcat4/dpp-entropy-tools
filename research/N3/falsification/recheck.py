"""Higher precision repeat plus independent Mobius event/jet evaluation."""
import hashlib,json,os,time
from pathlib import Path
import mpmath as mp
from unequal_sparse_probe import BASELINE,PAIRS,kernel,events,evaluate
from conditional_q_attack import objects

def mobius(K):
    x,y,z=K[0,0],K[1,1],K[2,2]; a,b,c=K[0,1],K[0,2],K[1,2]
    q12=x*y-a*a; q13=x*z-b*b; q23=y*z-c*c
    r=x*y*z+2*a*b*c-x*c*c-y*b*b-z*a*a
    return [1-x-y-z+q12+q13+q23-r,x-q12-q13+r,y-q12-q23+r,q12-r,
            z-q13-q23+r,q13-r,q23-r,r]

def main():
    start=time.time(); mp.mp.dps=550
    old=json.loads(Path('research/N3/falsification/batch.json').read_text())
    opt=json.loads(Path('research/N3/falsification/optimal_direction.json').read_text())
    specs=[old['rows'][0]['spec'],old['best'][0]['spec'],opt['best']['A']['spec']]
    rows=[]
    for spec in specs:
        K=kernel(spec); p,J=events(K); alt=mobius(K)
        p_err=max(abs(a-b)/a for a,b in zip(p,alt))
        j_err=mp.mpf(0)
        for col,(i,j) in enumerate(PAIRS):
            E=mp.zeros(3); E[i,j]=1; E[j,i]=1
            for mask in range(8):
                altj=mp.diff(lambda t:mobius(K+t*E)[mask],0)
                j_err=max(j_err,abs(altj-J[mask,col]))
        rho=evaluate(K)['rho']; Q,G,eta,det,_=objects(K)
        F=J.T*mp.diag([1/a for a in p])*J; v=mp.lu_solve(F+G,eta); d=v/(eta.T*v)[0]
        C=det-(d.T*G*d)[0]; gap=max(((d.T*q*d)[0]-C)/det for q in Q)
        rows.append(dict(spec=spec,rho=rho,A_max_gap=mp.nstr(gap,70),
                         event_relative_error=mp.nstr(p_err,8),jet_absolute_error=mp.nstr(j_err,8)))
        assert p_err<mp.mpf('1e-350') and j_err<mp.mpf('1e-350')
    out=dict(status='SCOUT_RECHECK_PASSED',baseline=BASELINE,pid=os.getpid(),dps=550,
             source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             kernel_calls=3,rho_calls=3,A_direction_calls=3,independent_event_calls=3,
             independent_derivative_calls=144,rejected=0,rows=rows,elapsed_seconds=time.time()-start,exit_status=0)
    Path('research/N3/falsification/recheck.json').write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out))

if __name__=='__main__':main()
