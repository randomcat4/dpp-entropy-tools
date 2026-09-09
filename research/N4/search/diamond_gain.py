"""S2: 24 structured unequal-leaf diamond kernels, two-column coupling gain."""
import os
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
import hashlib,json,time
from pathlib import Path
import numpy as np
import bounded_search as core

ROOT=Path(__file__).parent
def families():
    for r in (1/3,1/5,1/10):
        for family in range(8):
            if family==0:
                a12=.1;u=np.array([1/5,1/6]);v=np.array([1/7,-1/8]);label='fixed_control'
            elif family<6:
                pa,pu,pv={1:(1,1,1),2:(2,2,2),3:(3,1,2),4:(2,3,1),5:(1,3,3)}[family]
                a12=.1*r**pa;u=np.array([1/5,r**pu/6]);v=np.array([r**pv/7,-1/8]);label=f'axis_soft_A{pa}_u{pu}_v{pv}'
            elif family==6:
                a12=.1*r*r;u=np.array([r/5,r*r/6]);v=np.array([r**3/7,-r*r/8]);label='amplitude_and_axis_soft'
            else:
                u=np.array([1/5,r*r/6]);v=np.array([r*r/7,-1/8]);a12=float((np.outer(u,u)+np.outer(v,v))[0,1])+r**3/10;label='schur_offdiagonal_soft'
            A=np.array([[.5,a12],[a12,1/3]])
            B=np.column_stack([r*u,r*r*v]);K=np.block([[A,B],[B.T,np.diag([r*r,r**4])]])
            yield K,{'family':label,'r':r,'A':A.tolist(),'u':u.tolist(),'v':v.tolist(),'lower_schur_min':float(np.linalg.eigvalsh(A-np.outer(u,u)-np.outer(v,v))[0])}

def run():
    out=ROOT/'batch2';out.mkdir(exist_ok=False);start=time.time()
    manifest={'status':'RUNNING','pid':os.getpid(),'command':'OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 /root/i05-successors-20260909/N4/venv/bin/python research/N4/search/diamond_gain.py','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'core_sha256':hashlib.sha256((ROOT/'bounded_search.py').read_bytes()).hexdigest(),'start_time':start,'seed':None,'random_calls':0,'numpy':np.__version__,'dimensions':[4],'threads':1}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2))
    rows=[];fails=[]
    # Actual entries E=(e_03,e_13,e_04,e_14), i.e. Python (02,12,03,13).
    ids=[core.PAIRS.index(p) for p in ((0,2),(1,2),(0,3),(1,3))]
    T=np.eye(10)[:,ids]*np.sqrt(2)
    for index,(K,meta) in enumerate(families()):
        core.COUNTS['kernel_proposals']+=1
        if core.margin(K)<=0 or meta['lower_schur_min']<=0:
            fails.append({'index':index,'meta':meta,'K':K.tolist(),'reason':'feasibility'});continue
        H,F,A,data,diagnostic=core.hessian(K);M=T.T@H@T
        M33=M[:2,:2];M44=M[2:,2:];M34=M[:2,2:]
        e3,Q3=np.linalg.eigh(-M33);e4,Q4=np.linalg.eigh(-M44)
        gain=None;coordinates=None
        if min(e3[0],e4[0])>0:
            W3=(Q3/np.sqrt(e3))@Q3.T;W4=(Q4/np.sqrt(e4))@Q4.T
            U,s,Vt=np.linalg.svd(W3@M34@W4)
            gain=float(s[0]);coordinates=np.r_[W3@U[:,0],W4@Vt.T[:,0]]
        es,Qs=np.linalg.eigh(M);ef,Qf=np.linalg.eigh(H)
        rec={'index':index,'meta':meta,'K':K.tolist(),'margin':core.margin(K),'spectrum':np.linalg.eigvalsh(K).tolist(),'restriction_coordinate_order':['K02','K12','K03','K13'],'restricted_Hessian':M.tolist(),'restricted_Fisher':(-T.T@F@T).tolist(),'restricted_acceleration':(T.T@A@T).tolist(),'M33_defect_eigenvalues':e3.tolist(),'M44_defect_eigenvalues':e4.tolist(),'cross_gain':gain,'restricted_max_eigenvalue':float(es[-1]),'full_max_eigenvalue':float(ef[-1]),'full_Hessian':H.tolist(),'diagnostic':diagnostic,'directions':[]}
        vs=[('restricted_top',T@Qs[:,-1]),('full_top',Qf[:,-1])]
        if coordinates is not None:vs.append(('gain_direction',T@coordinates))
        h0=core.entropy(K)
        for name,vv in vs:
            vv=vv/np.linalg.norm(vv);D=np.einsum('a,aij->ij',vv,core.BASIS);radius=core.radius(K,D)
            chords=[]
            for fraction in (.025,.2,.7):
                t=radius*fraction;gap=(core.entropy(K-t*D)+core.entropy(K+t*D))/2-h0
                chords.append({'t':t,'Delta':gap,'endpoint_margin':min(core.margin(K-t*D),core.margin(K+t*D))})
            p,lp,dp,ddp=data;event_f=-(dp@vv)**2/p;event_a=-np.einsum('sij,i,j->s',ddp,vv,vv)*lp
            dr={'name':name,'D':D.tolist(),'curvature':float(vv@H@vv),'fisher':float(-vv@F@vv),'acceleration':float(vv@A@vv),'event_fisher':event_f.tolist(),'event_acceleration':event_a.tolist(),'commutator_norm':float(np.linalg.norm(K@D-D@K)),'symmetric_feasible_radius_float':radius,'chords':chords}
            rec['directions'].append(dr)
            if dr['curvature']>1e-8 or any(c['Delta']>1e-10 for c in chords):
                (out/f'candidate_{index}_{name}.json').write_text(json.dumps({'status':'FLOAT_CANDIDATE','K':K.tolist(),'D':D.tolist(),'t':chords[1]['t'],'record':rec},indent=2));print('CANDIDATE',index,name,flush=True)
        rows.append(rec)
        print(json.dumps({'index':index,'family':meta['family'],'r':meta['r'],'cross_gain':gain,'defect3':e3[0],'defect4':e4[0],'full_top':ef[-1]}),flush=True)
    (out/'cases.jsonl').write_text(''.join(json.dumps(row)+'\n' for row in rows));(out/'failures.json').write_text(json.dumps(fails,indent=2))
    (out/'best_gain.json').write_text(json.dumps(max(rows,key=lambda x:x['cross_gain'] if x['cross_gain'] is not None else -1),indent=2))
    manifest.update(status='SCOUT_COMPLETE',exit_code=0,completed=len(rows),failures=len(fails),counts=core.COUNTS,max_gain=max(row['cross_gain'] for row in rows if row['cross_gain'] is not None),max_full_curvature=max(row['full_max_eigenvalue'] for row in rows),candidate_files=[p.name for p in out.glob('candidate_*.json')],elapsed_seconds=time.time()-start)
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2));print(json.dumps(manifest),flush=True)

if __name__=='__main__':run()
