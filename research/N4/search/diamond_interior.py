"""S3: bounded direct optimization of diamond cross gain, no dimension growth."""
import os
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
import hashlib,json,time
from pathlib import Path
import numpy as np
import scipy
from scipy.optimize import minimize
from scipy.special import expit,logit
import bounded_search as core
ROOT=Path(__file__).parent
EDGES=((0,1),(0,2),(0,3),(1,2),(1,3))
IDS=[core.PAIRS.index(p) for p in ((0,2),(1,2),(0,3),(1,3))]
T=np.eye(10)[:,IDS]*np.sqrt(2)

def positive_radius(center,W):
    d=np.diag(center);L=W/np.sqrt(d[:,None]*d[None,:]);R=W/np.sqrt((1-d[:,None])*(1-d[None,:]))
    a=np.linalg.eigvalsh(L)[0];b=np.linalg.eigvalsh(R)[-1]
    return min(-1/a if a<0 else np.inf,1/b if b>0 else np.inf)

def encode(diag,W,beta):
    return np.r_[logit((np.array(diag)-.001)/.998),[W[i,j] for i,j in EDGES],logit(beta/.999999)]

def decode(x):
    d=.001+.998*expit(x[:4]);center=np.diag(d);W=np.zeros((4,4))
    for value,(i,j) in zip(x[4:9],EDGES):W[i,j]=W[j,i]=value
    beta=.999999*expit(x[9]);r=positive_radius(center,W)
    if not np.isfinite(r):raise ArithmeticError('zero offdiagonal parameter')
    K=center+beta*r*W
    return K,{'diagonal':d.tolist(),'W':W.tolist(),'positive_ray_radius':r,'beta':float(beta)}

def starts():
    pairs=((.05,.2),(.05,.95),(.2,.8),(.5,.5),(.8,.95),(.95,.95))
    cols={'nearly_collinear':([.8,.6],[.8,.63]),'nearly_orthogonal':([.8,.6],[-.6,.8]),'conflicting_signs':([.95,.15],[.65,-.75])}
    for family,(u,v) in cols.items():
        for d3,d4 in pairs:
            for beta in (.75,.96,.9995):
                W=np.zeros((4,4));W[0,1]=W[1,0]=.15
                W[:2,2]=u;W[2,:2]=u;W[:2,3]=v;W[3,:2]=v
                yield encode([.31,.67,d3,d4],W,beta),{'family':family,'leaf_diagonal':[d3,d4],'initial_beta':beta}

def run():
    out=ROOT/'batch3';out.mkdir(exist_ok=False);start=time.time();records=[];failures=[];optimizers=[]
    manifest={'status':'RUNNING','pid':os.getpid(),'command':'OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 /root/i05-successors-20260909/N4/venv/bin/python research/N4/search/diamond_interior.py','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'core_sha256':hashlib.sha256((ROOT/'bounded_search.py').read_bytes()).hexdigest(),'numpy':np.__version__,'scipy':scipy.__version__,'seed':None,'random_calls':0,'dimensions':[4],'start_time':start,'threads':1,'initial_limit':54,'optimization_limit':240}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2))
    handle=(out/'cases.jsonl').open('w')
    def evaluate(x,meta):
        index=core.COUNTS['kernel_proposals'];core.COUNTS['kernel_proposals']+=1
        try:
            K,params=decode(x)
            if core.margin(K)<=0:raise ArithmeticError('non-strict kernel')
            H,F,A,data,diagnostic=core.hessian(K);M=T.T@H@T
            e3,Q3=np.linalg.eigh(-M[:2,:2]);e4,Q4=np.linalg.eigh(-M[2:,2:]);single_ok=bool(min(e3[0],e4[0])>0)
            if single_ok:
                W3=(Q3/np.sqrt(e3))@Q3.T;W4=(Q4/np.sqrt(e4))@Q4.T;U,s,Vt=np.linalg.svd(W3@M[:2,2:]@W4);gain=float(s[0]);gvec=T@np.r_[W3@U[:,0],W4@Vt.T[:,0]]
            else:gain=None;gvec=None
            ef,Qf=np.linalg.eigh(H);er,Qr=np.linalg.eigh(M)
            B=K[:2,2:];d=np.diag(K)[2:]
            rec={'index':index,'meta':meta,'parameters':params,'x':x.tolist(),'K':K.tolist(),'margin':core.margin(K),'spectrum':np.linalg.eigvalsh(K).tolist(),'lower_schur_eigenvalues':np.linalg.eigvalsh(K[:2,:2]-(B/d)@B.T).tolist(),'upper_schur_eigenvalues':np.linalg.eigvalsh(np.eye(2)-K[:2,:2]-(B/(1-d))@B.T).tolist(),'cycle_gauge':core.gauge(K),'restricted_Hessian':M.tolist(),'single_blocks_negative':single_ok,'M33_defect_eigenvalues':e3.tolist(),'M44_defect_eigenvalues':e4.tolist(),'cross_gain':gain,'full_max_eigenvalue':float(ef[-1]),'restricted_max_eigenvalue':float(er[-1]),'diagnostic':diagnostic,'directions':[]}
            vs=[('full_top',Qf[:,-1]),('restricted_top',T@Qr[:,-1])]
            if single_ok:vs.append(('gain_direction',gvec))
            p,lp,dp,ddp=data;h0=core.entropy(K)
            for name,v in vs:
                v=v/np.linalg.norm(v);D=np.einsum('a,aij->ij',v,core.BASIS);rad=core.radius(K,D);chords=[]
                for frac in (.025,.2,.7):
                    t=rad*frac;gap=(core.entropy(K-t*D)+core.entropy(K+t*D))/2-h0
                    chords.append({'t':t,'Delta':gap,'endpoint_margin':min(core.margin(K-t*D),core.margin(K+t*D))})
                efish=-(dp@v)**2/p;eacc=-np.einsum('sij,i,j->s',ddp,v,v)*lp
                dr={'name':name,'D':D.tolist(),'curvature':float(v@H@v),'fisher':float(-v@F@v),'acceleration':float(v@A@v),'event_fisher':efish.tolist(),'event_acceleration':eacc.tolist(),'D_eigenvalues':np.linalg.eigvalsh(D).tolist(),'commutator_norm':float(np.linalg.norm(K@D-D@K)),'symmetric_feasible_radius_float':rad,'chords':chords}
                rec['directions'].append(dr)
                if dr['curvature']>1e-8 or any(c['Delta']>1e-10 for c in chords):
                    (out/f'candidate_{index}_{name}.json').write_text(json.dumps({'status':'FLOAT_CANDIDATE_NOT_CERTIFIED','K':K.tolist(),'D':D.tolist(),'t':chords[1]['t'],'record':rec},indent=2));print('CANDIDATE',index,name,flush=True)
            handle.write(json.dumps(rec)+'\n');handle.flush();records.append(rec)
            if index%25==0:print(json.dumps({'calls':index+1,'gain':gain,'best_gain':max(r['cross_gain'] for r in records if r['cross_gain'] is not None)}),flush=True)
            return -gain if single_ok else 1e3
        except Exception as error:
            core.COUNTS['rejected']+=1;failures.append({'index':index,'meta':meta,'x':x.tolist(),'error':repr(error)})
            (out/'failures.json').write_text(json.dumps(failures,indent=2));return 1e3
    for x,meta in starts():evaluate(x,{'stage':'initial',**meta})
    initial=list(records)
    for family in ('nearly_collinear','nearly_orthogonal','conflicting_signs'):
        candidates=[r for r in initial if r['meta']['family']==family and r['single_blocks_negative']]
        leader=max(candidates,key=lambda r:r['cross_gain'])
        before=core.COUNTS['kernel_proposals']
        result=minimize(lambda x:evaluate(x,{'stage':'adaptive','family':family,'parent_index':leader['index']}),np.array(leader['x']),method='Nelder-Mead',options={'maxfev':80,'xatol':1e-6,'fatol':1e-8,'adaptive':True})
        optimizers.append({'family':family,'parent_index':leader['index'],'initial_gain':leader['cross_gain'],'final_gain':float(-result.fun),'nfev':int(result.nfev),'actual_proposals':core.COUNTS['kernel_proposals']-before,'status':int(result.status),'success':bool(result.success),'message':str(result.message)})
    handle.close()
    best=max([r for r in records if r['single_blocks_negative']],key=lambda r:r['cross_gain'])
    (out/'best_gain.json').write_text(json.dumps(best,indent=2));(out/'failures.json').write_text(json.dumps(failures,indent=2))
    manifest.update(status='SCOUT_COMPLETE',exit_code=0,completed=len(records),failures=len(failures),counts=core.COUNTS,max_gain=best['cross_gain'],max_full_curvature=max(r['full_max_eigenvalue'] for r in records),single_block_failures=sum(not r['single_blocks_negative'] for r in records),optimizers=optimizers,candidate_files=[p.name for p in out.glob('candidate_*.json')],elapsed_seconds=time.time()-start)
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2));print(json.dumps(manifest),flush=True)

if __name__=='__main__':run()
