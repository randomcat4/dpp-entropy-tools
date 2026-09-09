"""Second predefined unit: missing-harmonic mixing at sparse even centers."""
import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[name]='1'
import argparse,datetime,hashlib,json,resource,sys,time
from fractions import Fraction
import numpy as np
from phase_probe import hessian

def run():
    centers=[]
    for p in map(Fraction,('1/2','1/4')):
        for strength in map(Fraction,('1/2','9/10','49/50')):
            centers.append((p,[p*strength,Fraction(0),Fraction(0),Fraction(0)],'pure nearest neighbor'))
    for distance in (2,3):
        for sign in (-1,1):
            a=list(map(Fraction,('9/20','0','0','0')))
            a[distance-1]=Fraction(sign,100)
            centers.append((Fraction(1,2),a,'hierarchical nonzero harmonic'))
    output=[]
    for p,a,label in centers:
        item={'p':str(p),'a':list(map(str,a)), 'kind':label,
              'center_triangle_margin':str(min(p,1-p)-sum(map(abs,a))), 'diagnostics':[]}
        for n in (6,8,10):
            d=hessian(n,float(p),np.array(a,dtype=float))
            h=np.array(d['hessian']);block=h[np.ix_([1,3],[1,3])]
            d['absent_even_block_2_4']=block.tolist()
            d['even_block_eigenvalues']=np.linalg.eigvalsh(block).tolist()
            d['opposite_parity_max']=float(abs(h[np.ix_([0,2],[1,3])]).max())
            d['even_block_coupling_ratio']=float(abs(block[0,1])/np.sqrt(abs(block[0,0]*block[1,1])))
            item['diagnostics'].append(d)
        output.append(item)
    return output

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
    resource.setrlimit(resource.RLIMIT_AS,(4*1024**3,4*1024**3))
    start=time.time()
    meta={'status':'RUNNING','pid':os.getpid(),'seed':0,'randomness':'none; deterministic predefined coverage',
          'utc_start':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':sys.version,'numpy':np.__version__,
          'source_sha256':{name:hashlib.sha256(open(os.path.join(os.path.dirname(__file__),name),'rb').read()).hexdigest() for name in ('sparse_probe.py','phase_probe.py')},
          'argv':sys.argv,'threads':{name:os.environ[name] for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS')},
          'address_space_limit_bytes':4*1024**3}
    print(json.dumps(meta),flush=True)
    try:
        results=run();meta.update(status='COMPLETED',exit_status=0,elapsed_seconds=time.time()-start,
                                 max_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        with open(args.output,'w') as out:json.dump({'centers':results,'metadata':meta},out,indent=2)
        print(json.dumps(meta),flush=True)
    except BaseException as e:
        meta.update(status='FAILED',exit_status=1,error=repr(e))
        with open(args.output,'w') as out:json.dump({'metadata':meta},out,indent=2)
        raise
