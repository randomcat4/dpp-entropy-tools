"""N4 one-unit scout: exact event formula, polynomial derivatives, full Hessian.

Float64 search only. Frozen arrays are binary64 exact inputs, not certificates.
"""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key]='1'
import argparse, hashlib, itertools, json, platform, sys, time
from pathlib import Path
import numpy as np
import scipy
from scipy.linalg import expm

N=4
PAIRS=list(itertools.combinations_with_replacement(range(N),2))
BASIS=np.zeros((10,4,4))
for a,(i,j) in enumerate(PAIRS):
    BASIS[a,i,j]=BASIS[a,j,i]=1 if i==j else 1/np.sqrt(2)
BITS=np.array([[(s>>i)&1 for i in range(4)] for s in range(16)])
SIGNS=(-1.)**(4-BITS.sum(1))
PERMS=[(p,(-1)**sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))) for p in itertools.permutations(range(4))]
COUNTS={'hessian_calls':0,'entropy_calls':0,'polynomial_derivative_calls':0,'kernel_proposals':0,'rejected':0}

def atoms(K):
    mats=np.broadcast_to(K,(16,4,4)).copy()
    mats[:,np.arange(4),np.arange(4)]-=1-BITS
    signs,logs=np.linalg.slogdet(mats)
    if np.any(signs!=SIGNS): raise ArithmeticError('event sign mismatch')
    p=np.exp(logs)
    if abs(p.sum()-1)>1e-9: raise ArithmeticError('event normalization')
    return p,logs,mats

def derivatives(K):
    COUNTS['polynomial_derivative_calls']+=1
    p,logs,mats=atoms(K)
    dp=np.zeros((16,10)); ddp=np.zeros((16,10,10)); ppoly=np.zeros(16)
    # Differentiate the exact Leibniz determinant polynomial. No matrix inverse.
    for perm,sgn in PERMS:
        vals=mats[:,np.arange(4),perm]
        b=BASIS[:,np.arange(4),perm].T
        ppoly+=sgn*np.prod(vals,axis=1)
        for i in range(4):
            dp+=sgn*np.prod(vals[:,[k for k in range(4) if k!=i]],axis=1)[:,None]*b[i]
            for j in range(4):
                if i!=j:
                    ddp+=sgn*np.prod(vals[:,[k for k in range(4) if k not in (i,j)]],axis=1)[:,None,None]*np.outer(b[i],b[j])
    dp*=SIGNS[:,None];ddp*=SIGNS[:,None,None];ppoly*=SIGNS
    return p,logs,dp,ddp,{'p_polynomial_error':float(np.max(abs(p-ppoly))),'dp_sum_error':float(np.max(abs(dp.sum(0)))),'ddp_sum_error':float(np.max(abs(ddp.sum(0))))}

def hessian(K):
    COUNTS['hessian_calls']+=1
    p,logs,dp,ddp,diag=derivatives(K)
    F=np.einsum('si,sj,s->ij',dp,dp,1/p)
    A=-np.einsum('sij,s->ij',ddp,logs)
    H=A-F
    return (H+H.T)/2,F,(A+A.T)/2,(p,logs,dp,ddp),diag

def entropy(K):
    COUNTS['entropy_calls']+=1
    p,lp,_=atoms(K)
    return float(-p@lp)

def margin(K):
    e=np.linalg.eigvalsh(K)
    return float(min(e[0],1-e[-1]))

def radius(K,D):
    bounds=[]
    for M in (K,np.eye(4)-K):
        e,q=np.linalg.eigh(M)
        R=(q/np.sqrt(e))@q.T
        bounds.append(1/max(abs(np.linalg.eigvalsh(R@D@R))))
    return float(min(bounds))

def gauge(K):
    # All initial graph families have the first-row spanning tree nonzero.
    signs=np.where(K[0,:]>=0,1.,-1.);signs[0]=1
    G=signs[:,None]*K*signs[None,:]
    return ''.join('+' if G[i,j]>0 else '-' if G[i,j]<0 else '0' for i,j in ((1,2),(1,3),(2,3)))

def assess(K,meta,index,out):
    COUNTS['kernel_proposals']+=1
    H,F,A,data,diagnostic=hessian(K)
    ev,U=np.linalg.eigh(H)
    fv,Q=np.linalg.eigh(F); keep=fv>max(1.,fv[-1])*1e-12
    W=Q[:,keep]/np.sqrt(fv[keep])
    rv,R=np.linalg.eigh(W.T@A@W)
    coords=[('hessian_top',U[:,-1]),('fisher_ratio',W@R[:,-1])]
    p,logs,dp,ddp=data
    record={'index':index,'meta':meta,'K':K.tolist(),'spectrum':np.linalg.eigvalsh(K).tolist(),'margin':margin(K),'cycle_gauge':gauge(K),'lambda_max_frobenius':float(ev[-1]),'hessian_spectrum':ev.tolist(),'fisher_spectrum':fv.tolist(),'fisher_supported_rank':int(keep.sum()),'mechanism_ratio':float(rv[-1]),'min_atom':float(p.min()),'diagnostic':diagnostic,'directions':[]}
    h0=entropy(K)
    for name,v in coords:
        v=v/np.linalg.norm(v); D=np.einsum('a,aij->ij',v,BASIS)
        r=radius(K,D);ts=[r*.025,r*.2,r*.7]
        pp=dp@v; ppp=np.einsum('sij,i,j->s',ddp,v,v)
        f=-pp**2/p; acc=-ppp*logs
        chords=[{'t':t,'Delta':(entropy(K+t*D)+entropy(K-t*D))/2-h0,'endpoint_margin':min(margin(K+t*D),margin(K-t*D))} for t in ts]
        dr={'name':name,'D':D.tolist(),'curvature':float(v@H@v),'fisher':float(-v@F@v),'acceleration':float(v@A@v),'commutator_norm':float(np.linalg.norm(K@D-D@K)),'D_eigenvalues':np.linalg.eigvalsh(D).tolist(),'symmetric_feasible_radius_float':r,'chords':chords,'event_p':p.tolist(),'event_dp':pp.tolist(),'event_ddp':ppp.tolist(),'event_fisher':f.tolist(),'event_acceleration':acc.tolist(),'complement_pairs':[{'S':s,'Sc':15-s,'fisher':float(f[s]+f[15-s]),'acceleration':float(acc[s]+acc[15-s])} for s in range(8)]}
        record['directions'].append(dr)
        if dr['curvature']>1e-8 or any(c['Delta']>1e-10 for c in chords):
            candidate={'status':'FLOAT_CANDIDATE_NOT_CERTIFIED','K':K.tolist(),'D':D.tolist(),'t':ts[1],'record':record,'direction':dr}
            path=out/f'candidate_{index}_{name}.json';path.write_text(json.dumps(candidate,indent=2))
            print(json.dumps({'CANDIDATE':str(path),'index':index,'curvature':dr['curvature']}),flush=True)
    return record

def kernels(rng):
    diagonals=[[.17,.38,.61,.83],[.02,.19,.73,.97],[.0001,.03,.91,.999],[.11,.26,.47,.72]]
    for sg in itertools.product((-1,1),repeat=3):
        for dindex,d in enumerate(diagonals):
            W=np.zeros((4,4));weights=[.7,1.1,.9,.8,1.3,.6]
            for (i,j),weight,sign in zip(itertools.combinations(range(4),2),weights,(1,1,1,*sg)):
                W[i,j]=W[j,i]=weight*sign
            center=np.diag(d);r=radius(center,W)
            for beta in (.25,.88):
                yield center+beta*r*W,{'family':'dense_cycle_classes','signs':sg,'diagonal_index':dindex,'beta':beta}
    for sg in itertools.product((-1,1),repeat=2):
        for di in (0,2):
            W=np.array([[0,.7,1.1,.9],[.7,0,sg[0]*.8,sg[1]*1.3],[1.1,sg[0]*.8,0,0],[.9,sg[1]*1.3,0,0]])
            center=np.diag(diagonals[di]);r=radius(center,W)
            for beta in (.25,.88):
                yield center+beta*r*W,{'family':'diamond_two_cycles','signs':sg,'diagonal_index':di,'beta':beta}
    for frame in range(4):
        Q0,_=np.linalg.qr(rng.normal(size=(4,4)))
        B=rng.normal(size=(4,4));B=(B-B.T)/4
        C=rng.normal(size=(4,4));C=(C-C.T)/4
        for eps in (.1,.02,.002,.0001):
            Q=Q0@expm(eps**.25*B)@expm(eps**.7*C)
            for profile,e in enumerate(([eps**2,eps,1-eps**.7,1-eps**1.5],[eps**1.7,.23,.79,1-eps**.6],[eps**.7,eps**1.4,eps**2,1-eps])):
                yield (Q*np.array(e))@Q.T,{'family':'moving_frame_unequal_scales','frame':frame,'epsilon':eps,'profile':profile}
    for di,d in enumerate(diagonals):
        for eps in (.03,.003,.0003,.00003):
            W=rng.normal(size=(4,4));W=(W+W.T)/2;np.fill_diagonal(W,0)
            center=np.diag(d)
            yield center+eps*radius(center,W)*W,{'family':'near_product_control','diagonal_index':di,'epsilon':eps}

def selftest():
    K=np.array([[.3,.03,-.02,.01],[.03,.5,.04,-.025],[-.02,.04,.6,.05],[.01,-.025,.05,.7]])
    H,F,A,_,diagnostic=hessian(K)
    inc=np.ones(16)
    for s in range(1,16):
        ids=np.where(BITS[s])[0];inc[s]=np.linalg.det(K[np.ix_(ids,ids)])
    mob=inc.copy()
    for i in range(4):
        for s in range(16):
            if not (s>>i)&1:mob[s]-=mob[s|(1<<i)]
    event_error=float(np.max(abs(mob-atoms(K)[0])))
    v=np.arange(1,11,dtype=float);v/=np.linalg.norm(v);D=np.einsum('a,aij->ij',v,BASIS);t=1e-4
    fd=(entropy(K+t*D)+entropy(K-t*D)-2*entropy(K))/t**2
    error=abs(fd-v@H@v)
    assert event_error<1e-14 and error<2e-6,(event_error,error)
    return {'event_mobius_error':event_error,'curvature_finite_difference_error':float(error),**diagnostic}

def run(out):
    out.mkdir(parents=True,exist_ok=False)
    manifest={'status':'RUNNING','pid':os.getpid(),'seed':2026090904,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'base_commit':'fa504ec74e16843fafc395880d7ba99b4c1d2129','command':'OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 /root/i05-successors-20260909/N4/venv/bin/python research/N4/search/bounded_search.py --out research/N4/search/batch1','python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,'threads':{k:os.environ[k] for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS')},'start_time':time.time(),'dimensions':[4]}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2))
    manifest['selftest']=selftest();manifest['selftest_counts']=COUNTS.copy()
    rng=np.random.default_rng(manifest['seed']);results=[];failures=[]
    with (out/'cases.jsonl').open('w') as f:
        for i,(K,meta) in enumerate(kernels(rng)):
            try:
                rec=assess(K,meta,i,out);results.append(rec);f.write(json.dumps(rec)+'\n');f.flush()
            except Exception as e:
                COUNTS['rejected']+=1;failures.append({'index':i,'meta':meta,'error':repr(e),'K':K.tolist()})
            if (i+1)%16==0: print(json.dumps({'completed':i+1,'best_ratio':max(x['mechanism_ratio'] for x in results),'best_lambda':max(x['lambda_max_frobenius'] for x in results)}),flush=True)
        # Adaptive 16 proposals: exploit two highest well-conditioned mechanism ratios.
        eligible=[r for r in results if r['fisher_supported_rank']==10 and r['margin']>1e-6 and r['meta']['family']!='near_product_control']
        leaders=sorted(eligible,key=lambda r:r['mechanism_ratio'],reverse=True)[:2]
        nextindex=i+1
        for leader in leaders:
            K=np.array(leader['K'])
            for trial in range(8):
                X=rng.normal(size=(4,4));X=(X+X.T)/2;X/=np.linalg.norm(X)
                step=radius(K,X)*(.05 if trial<4 else .25)
                proposal=K+step*X;meta={'family':'adaptive_mechanism_neighborhood','parent_index':leader['index'],'trial':trial,'step':step}
                try:
                    rec=assess(proposal,meta,nextindex,out);results.append(rec);f.write(json.dumps(rec)+'\n');f.flush()
                except Exception as e:
                    COUNTS['rejected']+=1;failures.append({'index':nextindex,'meta':meta,'error':repr(e),'K':proposal.tolist()})
                nextindex+=1
    (out/'failures.json').write_text(json.dumps(failures,indent=2))
    for key,field in [('best_curvature','lambda_max_frobenius'),('best_mechanism','mechanism_ratio')]:
        (out/f'{key}.json').write_text(json.dumps(max(results,key=lambda r:r[field]),indent=2))
    coverage={family:sum(r['meta']['family']==family for r in results) for family in sorted({r['meta']['family'] for r in results})}
    manifest.update(status='SCOUT_COMPLETE',exit_code=0,counts=COUNTS,successful_kernel_assessments=len(results),coverage=coverage,failures=len(failures),candidate_files=[p.name for p in out.glob('candidate_*.json')],elapsed_seconds=time.time()-manifest['start_time'],max_curvature=max(r['lambda_max_frobenius'] for r in results),max_mechanism_ratio=max(r['mechanism_ratio'] for r in results),max_gap=max(c['Delta'] for r in results for d in r['directions'] for c in d['chords']))
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2));print(json.dumps(manifest),flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True);args=parser.parse_args();run(args.out)
