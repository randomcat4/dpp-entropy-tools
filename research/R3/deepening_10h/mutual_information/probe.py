"""Bounded FT-C rank-two information-geometric probe; no remote configuration."""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key]='1'
import csv, json, math, time, traceback
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal, localcontext
import numpy as np

SEED=202609081903
OUT=Path(__file__).resolve().parent/'results'

def arr(A): return np.array([[float(x) for x in row] for row in A])
def combine(M,D,t): return [[M[i][j]+t*D[i][j] for j in range(len(M))] for i in range(len(M))]
def baseline(n,gamma):
    M=[[F(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        M[i][i]=F(1,3)+F(i+1,3*(n+1))
        for j in range(i+1,n):
            M[i][j]=M[j][i]=gamma*((-1)**(i*j+i+j))*F(3+((i+1)*7+(j+1)*11)%5,20*n)
    return M

def certificate(M):
    K=arr(M); eig=np.linalg.eigvalsh(K); ef=float(min(eig[0],1-eig[-1])); n=len(M)
    m=F(max(1,math.floor(ef*500000)),10**6); minimum=[]
    for complement in (False,True):
        A=[[F(int(i==j))-M[i][j] if complement else M[i][j] for j in range(n)] for i in range(n)]
        for i in range(n): A[i][i]-=m
        L=[[F(0) for _ in range(n)] for _ in range(n)]; d=[]
        for j in range(n):
            dj=A[j][j]-sum(L[j][r]**2*d[r] for r in range(j))
            if dj<=0: raise ArithmeticError('exact rational LDL failed')
            d.append(dj); L[j][j]=1
            for i in range(j+1,n): L[i][j]=(A[i][j]-sum(L[i][r]*L[j][r]*d[r] for r in range(j)))/dj
        minimum.append(str(min(d)))
    return dict(margin=str(m),margin_float=float(m),positive_ldl_minima=minimum,float_spectral_margin=ef)

def entropy(p): return float(-p@np.log(p))
class Events:
    def __init__(self,n):
        self.n=n; self.na=n//2; self.nb=n-self.na
        self.bits=((np.arange(1<<n)[:,None]>>np.arange(n))&1).astype(float)
        self.sign=(-1.)**(n-self.bits.sum(axis=1))
    def evaluate(self,K,inverse=False):
        A=np.broadcast_to(K,(1<<self.n,self.n,self.n)).copy()
        A[:,np.arange(self.n),np.arange(self.n)]-=1-self.bits
        sg,lp=np.linalg.slogdet(A)
        if not np.array_equal(sg,self.sign): raise ArithmeticError('event sign failed')
        p=np.exp(lp)
        if abs(p.sum()-1)>1e-11: raise ArithmeticError('normalization failed')
        return (p,np.linalg.inv(A)) if inverse else p
    def mobius(self,K):
        p=np.ones(1<<self.n)
        for mask in range(1,1<<self.n):
            ids=np.flatnonzero(self.bits[mask]); p[mask]=np.linalg.det(K[np.ix_(ids,ids)])
        for i in range(self.n):
            for mask in range(1<<self.n):
                if not(mask>>i&1): p[mask]-=p[mask|(1<<i)]
        return p
    def marginals(self,p):
        grid=p.reshape(1<<self.nb,1<<self.na); return grid.sum(axis=0),grid.sum(axis=1)
    def info(self,p):
        a,b=self.marginals(p); he,ha,hb=entropy(p),entropy(a),entropy(b)
        prod=(b[:,None]*a[None,:]).ravel(); ik=float(p@np.log(p/prod))
        return dict(E=he,A=ha,B=hb,I=ik,chain_residual=he-ha-hb+ik)

def rank_two_direction(u,v,c,na):
    n=len(u); u=np.array(u,dtype=np.int64); v=np.array(v,dtype=np.int64)
    gram=lambda x,y:int(x@x)*int(y@y)-int(x@y)**2
    if gram(u[:na],v[:na])==0 or gram(u[na:],v[na:])==0: raise ValueError('block vector dependence')
    uu,vv=int(u@u),int(v@v)
    D=[[F(int(u[i]*u[j]),uu)-c*F(int(v[i]*v[j]),vv) for j in range(n)] for i in range(n)]
    Df=arr(D); eig=np.linalg.eigvalsh(Df); nz=eig[abs(eig)>1e-10]
    if len(nz)!=2 or not(nz[0]<0<nz[1]): raise ArithmeticError('rank or inertia mismatch')
    ratio=float(min(abs(nz))/max(abs(nz)))
    if ratio<.15: raise ValueError('rank-two singular value ratio below 0.15')
    return D,dict(rank=2,inertia=[1,1,n-2],nonzero_eigenvalue_ratio=ratio,direction_norm_A=float(np.linalg.norm(Df[:na,:na])),direction_norm_B=float(np.linalg.norm(Df[na:,na:])),direction_norm_X=float(np.linalg.norm(Df[:na,na:])))

def coupling_min_exact(M,D,t,na):
    pairs=[(i,j) for i in range(na) for j in range(na,len(M))]
    q0=sum(M[i][j]**2 for i,j in pairs); q1=sum(M[i][j]*D[i][j] for i,j in pairs); q2=sum(D[i][j]**2 for i,j in pairs)
    vertex=-q1/q2; vertex=max(-t,min(t,vertex))
    value=q0+2*vertex*q1+vertex**2*q2
    if value<F(8,100)**2: raise ArithmeticError('exact cross-block norm floor failed')
    return float(value)**.5

def limit(M,D,na):
    K=arr(M); V=arr(D); X=K[:na,na:]; VX=V[:na,na:]
    bounds=[1.,(np.linalg.norm(X)-.08)/np.linalg.norm(VX),(np.linalg.svd(X,compute_uv=False)[1]-.03)/np.linalg.norm(VX,2)]
    for i in range(len(M)):
        for j in range(i):
            diff=abs(V[i,i]-V[j,j])
            if diff>1e-14: bounds.append((abs(K[i,i]-K[j,j])-.001)/diff)
    lo,hi=0.,min(bounds)
    if hi<=0: raise ValueError('no nondegenerate step interval')
    for _ in range(42):
        t=(lo+hi)/2; v0=np.linalg.eigvalsh(K-t*V); v1=np.linalg.eigvalsh(K+t*V)
        if min(v0[0],1-v0[-1],v1[0],1-v1[-1])>2e-5: lo=t
        else: hi=t
    return lo

def decimal_det(A):
    A=[row[:] for row in A]; n=len(A); d=Decimal(1)
    for j in range(n):
        k=max(range(j,n),key=lambda k:abs(A[k][j]))
        if A[k][j]==0: return Decimal(0)
        if k!=j: A[j],A[k]=A[k],A[j]; d=-d
        pivot=A[j][j]; d*=pivot
        for i in range(j+1,n):
            scale=A[i][j]/pivot
            for l in range(j+1,n): A[i][l]-=scale*A[j][l]
    return d

def high_precision(M,D,t,precision):
    with localcontext() as ctx:
        ctx.prec=precision; hs=[]; norms=[]
        for sign in (-1,0,1):
            A=combine(M,D,sign*t); n=len(A)
            K=[[Decimal(x.numerator)/Decimal(x.denominator) for x in row] for row in A]; p=[]
            for mask in range(1<<n):
                B=[row[:] for row in K]; missing=0
                for i in range(n):
                    if not(mask>>i&1): B[i][i]-=1; missing+=1
                value=(-1)**missing*decimal_det(B)
                if value<=0: raise ArithmeticError('high precision event sign')
                p.append(value)
            hs.append(-sum(x*x.ln() for x in p)); norms.append(sum(p)-1)
        return dict(precision=precision,gap=str((hs[0]+hs[2])/2-hs[1]),entropies=[str(x) for x in hs],normalization_residuals=[str(x) for x in norms])

def main():
    if OUT.exists(): raise FileExistsError('Existing results: bounded run will not overwrite or repeat')
    OUT.mkdir(parents=True); (OUT/'parameters').mkdir(); rng=np.random.default_rng(SEED); start=time.time()
    manifest=dict(seed=SEED,planned_proposals=78,maximum_chords=234,threads=1,numpy=np.__version__,pid=os.getpid(),start=start,exit_code=None)
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    fields=['id','n','gamma','proposal','c','kind','status','reason','rank','eigenvalue_ratio','step','Delta_E','Delta_A','Delta_B','I_minus','I_0','I_plus','MI_bump','marginal_deficit_sum','bump_to_deficit_ratio','information_identity_residual','geometry_term','KL_cost','JS_cost','geometry_identity_residual','curvature_E','curvature_A','curvature_B','curvature_I','min_probability','normalization_residual','mobius_max_error','marginal_kernel_max_error','quadratic_event_max_error','cross_norm_min','second_cross_singular_lower_bound','margin_min','direction_norm_A','direction_norm_B','direction_norm_X']
    rows=[]; validation=[]; failures=0
    with (OUT/'candidate_ledger.csv').open('w',newline='',encoding='utf-8') as fp:
        writer=csv.DictWriter(fp,fieldnames=fields); writer.writeheader()
        def append(row): rows.append(row); writer.writerow(row); fp.flush()
        for n,count in ((6,6),(8,8),(11,12)):
            E=Events(n); EA=Events(E.na); EB=Events(E.nb)
            for gi,gamma in enumerate((F(1),F(2),F(5,2))):
                M=baseline(n,gamma); K=arr(M); cert0=certificate(M); p0,inv=E.evaluate(K,True); info0=E.info(p0)
                pa,pb=E.marginals(p0); marginal_error=max(float(max(abs(pa-EA.evaluate(K[:E.na,:E.na])))),float(max(abs(pb-EB.evaluate(K[E.na:,E.na:])))))
                base_mob=float(max(abs(E.mobius(K)-p0))) if n<=8 else None
                if base_mob is not None and base_mob>1e-11: raise ArithmeticError('base Mobius gate failed')
                validation.append(dict(n=n,gamma=str(gamma),base_mobius_error=base_mob,marginal_kernel_error=marginal_error,certificate=cert0))
                for j in range(count):
                    key=f'n{n}_g{gi}_p{j:02d}'; c=(F(1,2),F(1),F(2))[j%3]
                    u=rng.choice([-3,-2,-1,1,2,3],n).tolist(); v=rng.choice([-3,-2,-1,1,2,3],n).tolist()
                    core=dict(id=key,n=n,gamma=str(gamma),proposal=j,c=str(c)); data=dict(u=u,v=v,c=str(c),gamma=str(gamma),n=n,proposal=j,certificate_center=cert0,chords=[])
                    try:
                        D,meta=rank_two_direction(u,v,c,E.na); V=arr(D); bound=limit(M,D,E.na)
                        Q=np.einsum('qij,jk->qik',inv,V); tr=np.trace(Q,axis1=1,axis2=2)
                        a=p0*tr; b=.5*p0*(tr**2-np.einsum('qij,qji->q',Q,Q))
                        aa,ab=E.marginals(a); ba,bb=E.marginals(b)
                        curv=lambda p,alpha,beta:float(-np.sum(alpha**2/p)-2*beta@np.log(p))
                        ce=curv(p0,a,b); ca=curv(pa,aa,ba); cb=curv(pb,ab,bb)
                        data.update(meta=meta,step_limit=bound,curvature=dict(E=ce,A=ca,B=cb,I=ca+cb-ce))
                        append(core|dict(kind='DIRECTION',status='ACCEPTED',rank=2,eigenvalue_ratio=meta['nonzero_eigenvalue_ratio'],curvature_E=ce,curvature_A=ca,curvature_B=cb,curvature_I=ca+cb-ce,direction_norm_A=meta['direction_norm_A'],direction_norm_B=meta['direction_norm_B'],direction_norm_X=meta['direction_norm_X']))
                        for fraction in (.2,.5,.85):
                            t=F(math.floor(bound*fraction*10**6),10**6)
                            if t<=0: raise ArithmeticError('rounded zero step')
                            Mm,Mp=combine(M,D,-t),combine(M,D,t); cm,cp=certificate(Mm),certificate(Mp)
                            pm,pp=E.evaluate(arr(Mm)),E.evaluate(arr(Mp)); im,ip=E.info(pm),E.info(pp)
                            gap=(im['E']+ip['E'])/2-info0['E']; da=(im['A']+ip['A'])/2-info0['A']; db=(im['B']+ip['B'])/2-info0['B']; bump=info0['I']-(im['I']+ip['I'])/2
                            q=(pm+pp)/2; r=q-p0; geom=float(-r@np.log(p0)); kl=float(q@np.log(q/p0)); js=entropy(q)-(im['E']+ip['E'])/2
                            pe=max(float(max(abs(pm-(p0-float(t)*a+float(t)**2*b)))),float(max(abs(pp-(p0+float(t)*a+float(t)**2*b)))))
                            mob=None
                            if n<=8 and fraction==.85:
                                mob=max(float(max(abs(E.mobius(arr(Mm))-pm))),float(max(abs(E.mobius(arr(Mp))-pp))))
                                if mob>1e-11: raise ArithmeticError('endpoint Mobius gate failed')
                            crossmin=coupling_min_exact(M,D,t,E.na)
                            svlower=float(np.linalg.svd(K[:E.na,E.na:],compute_uv=False)[1]-float(t)*np.linalg.norm(V[:E.na,E.na:],2))
                            record=core|dict(kind='CHORD',status='FLOAT_CANDIDATE' if gap>0 else 'NO_SIGNAL',rank=2,eigenvalue_ratio=meta['nonzero_eigenvalue_ratio'],step=str(t),Delta_E=gap,Delta_A=da,Delta_B=db,I_minus=im['I'],I_0=info0['I'],I_plus=ip['I'],MI_bump=bump,marginal_deficit_sum=-da-db,bump_to_deficit_ratio=bump/(-da-db) if -da-db>0 else None,information_identity_residual=gap-da-db-bump,geometry_term=geom,KL_cost=kl,JS_cost=js,geometry_identity_residual=gap-(geom-kl-js),curvature_E=ce,curvature_A=ca,curvature_B=cb,curvature_I=ca+cb-ce,min_probability=float(min(pm.min(),p0.min(),pp.min())),normalization_residual=max(float(abs(p.sum()-1)) for p in (pm,p0,pp)),mobius_max_error=mob,marginal_kernel_max_error=marginal_error,quadratic_event_max_error=pe,cross_norm_min=crossmin,second_cross_singular_lower_bound=svlower,margin_min=min(cert0['margin_float'],cm['margin_float'],cp['margin_float']),direction_norm_A=meta['direction_norm_A'],direction_norm_B=meta['direction_norm_B'],direction_norm_X=meta['direction_norm_X'])
                            chord=dict(step=str(t),fraction=fraction,minus_certificate=cm,plus_certificate=cp,record=record)
                            if gap>0: chord['high_precision']=[high_precision(M,D,t,60),high_precision(M,D,t,100)]
                            data['chords'].append(chord); append(record)
                    except ValueError as ex:
                        append(core|dict(kind='PROPOSAL',status='FILTER_REJECT',reason=str(ex))); data['filter_reject']=str(ex)
                    except Exception as ex:
                        failures+=1; append(core|dict(kind='FAILURE',status='FAILED',reason=repr(ex))); data['failure']=traceback.format_exc()
                        if n<=8: raise
                    finally:
                        (OUT/'parameters'/f'{key}.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
                print(json.dumps(dict(n=n,gamma=str(gamma),elapsed=time.time()-start,failures=failures)),flush=True)
    chords=[r for r in rows if r['kind']=='CHORD']; directions=[r for r in rows if r['kind']=='DIRECTION']
    summary=dict(status='INCOMPLETE',proposals=78,accepted_directions=len(directions),filtered_proposals=sum(r['status']=='FILTER_REJECT' for r in rows),failures=failures,chords=len(chords),float_candidates=sum(r['status']=='FLOAT_CANDIDATE' for r in rows),positive_MI_bumps=sum(r['MI_bump']>0 for r in chords),max_gap=max(r['Delta_E'] for r in chords),max_MI_bump=max(r['MI_bump'] for r in chords),max_bump_deficit_ratio=max(r['bump_to_deficit_ratio'] for r in chords if r['bump_to_deficit_ratio'] is not None),min_exact_margin=min(r['margin_min'] for r in chords),min_cross_norm=min(r['cross_norm_min'] for r in chords),min_second_cross_singular_lower_bound=min(r['second_cross_singular_lower_bound'] for r in chords),min_direction_rank=2,max_mobius_error=max([v['base_mobius_error'] for v in validation if v['base_mobius_error'] is not None]+[r['mobius_max_error'] for r in chords if r['mobius_max_error'] is not None]),max_information_identity_residual=max(abs(r['information_identity_residual']) for r in chords),max_geometry_identity_residual=max(abs(r['geometry_identity_residual']) for r in chords),max_quadratic_event_error=max(r['quadratic_event_max_error'] for r in chords))
    manifest.update(complete=True,exit_code=0,elapsed=time.time()-start)
    for name,data in (('manifest',manifest),('summary',summary),('validation',validation)):
        (OUT/f'{name}.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
    print(json.dumps(summary),flush=True)

if __name__=='__main__': main()
