"""Non-author audit: independent indexed Hessian plus exact-seed report replay.

Author code is imported only for replaying its reported batches, not for the
independent Hessian reconstruction. All replay outputs are redirected here.
"""
import os,sys
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key]='1'
sys.dont_write_bytecode=True
import numpy as np
import json,time,importlib.util
from pathlib import Path
from fractions import Fraction as R
BASE=Path(__file__).resolve().parent
AUTHOR=BASE.parent

def independent(K,D):
    n=len(K); labels=[(i,i) for i in range(n)]+[(i,j) for i in range(n) for j in range(i+1,n)]
    ii=np.array([i for i,j in labels]);jj=np.array([j for i,j in labels])
    c=np.where(ii==jj,.5,1/np.sqrt(2))
    p=[];F=np.zeros((len(c),len(c)));A=F.copy();H=0.;p1=0.;p2=0.;Fd=0.;Ad=0.
    for s in range(1<<n):
        M=K.copy()
        absent=[i for i in range(n) if not s>>i&1]
        M[absent,absent]-=1
        sign,logp=np.linalg.slogdet(M)
        assert sign*((-1)**len(absent))>0
        probability=np.exp(logp);p.append(probability)
        B=np.linalg.inv(M); B=(B+B.T)/2
        score=2*c*B[ii,jj]
        # Closed entry formula for tr(B E_a B E_b), no author einsum code.
        trace=2*np.outer(c,c)*(B[ii[:,None],ii]*B[jj[:,None],jj]+B[ii[:,None],jj]*B[jj[:,None],ii])
        scoresq=np.outer(score,score)
        F+=probability*scoresq;A-=probability*logp*(scoresq-trace)
        X=np.linalg.solve(M,D);g=np.trace(X);w=g*g-np.sum(X*X.T)
        H-=probability*logp;p1+=probability*g;p2+=probability*w
        Fd+=probability*g*g;Ad-=probability*w*logp
    lam,U=np.linalg.eigh((F+F.T)/2);assert lam[0]>0
    W=U/np.sqrt(lam)[None,:]
    rho=np.linalg.eigvalsh(W.T@((A+A.T)/2)@W)[-1]
    return {'n':n,'atoms':len(p),'sum_p_error':sum(p)-1,'min_p':min(p),'H':H,
            'Fisher_positive':Fd,'acceleration':Ad,'H2':Ad-Fd,'rho_frozen':Ad/Fd,
            'rho_generalized':float(rho),'Fisher_min_eigenvalue':float(lam[0]),
            'Fisher_max_eigenvalue':float(lam[-1]),'sum_p1':p1,'sum_p2':p2}

def analytic_diagonal_check():
    # Exact inclusion products followed by Boolean Mobius at one rational point.
    x=[R(1,4),R(1,2),R(2,3)];rates=[R(1,7),R(2,9),R(1,5)]
    p=[]
    for s in range(8):
        v=R(1)
        for i in range(3):
            if s>>i&1:v*=x[i]
        p.append(v)
    for i in range(3):
        for s in range(8):
            if not s>>i&1:p[s]-=p[s|(1<<i)]
    for s in range(8):
        v=R(1)
        for i in range(3):v*=x[i] if s>>i&1 else 1-x[i]
        assert p[s]==v
    h2=-sum(d*d/(v*(1-v)) for v,d in zip(x,rates))
    return {'n':3,'exact_atoms':list(map(str,p)),'H2_PSD':str(h2),
            'H2_NSD':str(h2),'strict_negative':h2<0,'zero_direction_H2':'0'}

def main():
    start=time.time();source=json.loads((AUTHOR/'scout_results.json').read_text(encoding='utf-8'))
    # The source path is explicitly declared by the reviewed author material.
    frozen=np.load(source['fixed_center']['fixed_center_source'])
    K=(frozen['kernel']+frozen['kernel'].T)/2
    D=(frozen['direction']+frozen['direction'].T)/2
    recomputed=independent(K,D)
    assert abs(recomputed['rho_generalized']-source['fixed_center']['full_symmetric_generalized_control']['rho_max'])<1e-12
    spec=importlib.util.spec_from_file_location('reviewed_s3_author',AUTHOR/'psd_mechanism_search.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    module.OUT=BASE/'replay_results.json'
    original_eval=module.evaluate_direction
    stats={'evaluation_calls':0,'nonfinite':0,'nonpositive_Fisher':0,'max_rho':-np.inf,'max_H2':-np.inf}
    def counted_eval(F,A,D):
        value=original_eval(F,A,D);stats['evaluation_calls']+=1
        if value['rho'] is None or not all(np.isfinite(value[k]) for k in ('Fisher_positive','acceleration','H2','rho')):
            stats['nonfinite']+=1
        if value['Fisher_positive']<=0:stats['nonpositive_Fisher']+=1
        if value['rho'] is not None:stats['max_rho']=max(stats['max_rho'],value['rho'])
        stats['max_H2']=max(stats['max_H2'],value['H2'])
        return value
    module.evaluate_direction=counted_eval
    assert module.main()==0
    replay=json.loads((BASE/'replay_results.json').read_text(encoding='utf-8'))
    sb=source['fixed_center']['psd_search_batches'];rb=replay['fixed_center']['psd_search_batches']
    assert sb==rb
    small=[]
    for old,new in zip(source['small_n_random_psd_scout'],replay['small_n_random_psd_scout']):
        for key in ('n','centers','directions_per_center','directions','event_distributions_built','event_denominator','rho_gt_1_and_H2_gt_0'):
            assert old[key]==new[key]
        assert abs(old['best']['stats']['rho']-new['best']['stats']['rho'])<1e-12
        small.append({key:new[key] for key in ('n','centers','directions','event_denominator','rho_gt_1_and_H2_gt_0')})
    assert stats['nonfinite']==stats['nonpositive_Fisher']==0
    assert stats['max_rho']<1 and stats['max_H2']<0
    out={'status':'AUDIT_PASS_WITH_SCOUT_SCOPE','independent_frozen_recheck':recomputed,
         'analytic_diagonal_sanity':analytic_diagonal_check(),
         'exact_fixed_batch_metadata_replay_match':True,'small_batches_replay':small,
         'replay_instrumentation':stats,'source_seed':source['seed'],
         'fixed_proposals':sum(r['draws'] for r in rb),
         'small_centers':sum(r['centers'] for r in small),
         'small_directions':sum(r['directions'] for r in small),
         'small_event_atoms':sum(r['event_denominator'] for r in small),
         'exit_code':0,'elapsed_seconds':time.time()-start}
    (BASE/'fresh_check.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
