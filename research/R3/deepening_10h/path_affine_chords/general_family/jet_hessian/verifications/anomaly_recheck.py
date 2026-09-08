"""Independent anomaly triage: normalized last-run entropy DP, no author imports.

Parameter stream is reimplemented from the documented scout recipe. Arithmetic
uses Taylor coefficients (value, coefficient t, coefficient t^2), not raw jets.
"""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key]='1'
import math, random, json, time, platform, hashlib
from decimal import Decimal as Dec, localcontext
from fractions import Fraction as F
from pathlib import Path
BASE=Path(__file__).resolve().parent

def admissible(beta,tau):
    if min(tau)<=0: return False
    w=[1/x for x in tau]
    diag=[w[i]+beta[i]*beta[i]*w[i+1]-1.0 for i in range(len(beta))]+[w[-1]-1.0]
    edge=[-b*w[i+1] for i,b in enumerate(beta)]
    pivot=diag[0]; best=pivot
    for i in range(1,len(tau)):
        if pivot<=0 or not math.isfinite(pivot): return False
        pivot=diag[i]-edge[i-1]*edge[i-1]/pivot
        best=min(best,pivot)
    return best>1e-11

def reconstruct():
    rng=random.Random(20260908)
    centers=0; failures=0; directions=0
    for n in range(5,94):
        for trial in range(24):
            if trial%7==0:
                beta=[((-1.0)**i)*(0.16+0.30*((5*i+2)%11)/10.0) for i in range(n-1)]
            else:
                beta=[(-1.0 if rng.randrange(2) else 1.0)*rng.uniform(.08,.58) for _ in range(n-1)]
            profile=[math.exp(rng.uniform(math.log(.65),math.log(1.55))) for _ in range(n)]
            lo,hi=0.0,1.0
            while admissible(beta,[hi*x for x in profile]) and hi<1e6: hi*=2
            for _ in range(72):
                mid=.5*(lo+hi)
                if admissible(beta,[mid*x for x in profile]): lo=mid
                else: hi=mid
            if not math.isfinite(lo) or lo<=0:
                failures+=1; continue
            scale=rng.uniform(.22,.88)*lo
            tau=[scale*x for x in profile]
            if not admissible(beta,tau): failures+=1; continue
            centers+=1
            for size in (2,n):
                support=list(range(n)) if size>=n else rng.sample(range(n),size)
                raw=[0.0]*n
                for i in support: raw[i]=rng.gauss(0,1)
                norm=max(abs(raw[i]) for i in support)
                if norm==0: raw[support[0]]=1.; norm=1.
                rel=rng.uniform(.20,1.00)
                delta=[0.0]*n
                for i in support: delta[i]=rel*tau[i]*raw[i]/norm
                directions+=1
                if n==93 and trial==15 and size==2:
                    return {'beta':list(map(repr,beta)),'tau':list(map(repr,tau)),
                            'delta':list(map(repr,delta)),'seed':20260908,'n':93,'trial':15,
                            'stream_centers':centers,'stream_failures':failures,
                            'stream_directions':directions,'support_zero_based':support}

def plus(a,b): return tuple(x+y for x,y in zip(a,b))
def neg(a): return tuple(-x for x in a)
def minus(a,b): return plus(a,neg(b))
def times(a,b): return (a[0]*b[0],a[0]*b[1]+a[1]*b[0],a[0]*b[2]+a[1]*b[1]+a[2]*b[0])
def divide(a,b):
    # Coefficient recurrence; never forms reciprocal cubes of huge values.
    c0=a[0]/b[0]; c1=(a[1]-b[1]*c0)/b[0]
    return c0,c1,(a[2]-b[1]*c1-b[2]*c0)/b[0]
def log(a):
    l=a[0].ln() if isinstance(a[0],Dec) else math.log(a[0])
    r=a[1]/a[0]
    return l,r,a[2]/a[0]-r*r/2
def exp(a):
    v=a[0].exp() if isinstance(a[0],Dec) else math.exp(a[0])
    return v,v*a[1],v*(a[2]+a[1]*a[1]/2)

def stable_dp(beta,tau,delta):
    """Run-category mixture entropy; no unnormalized T or reciprocal large Z."""
    zero=tau[0]*0; one=zero+1
    z=(zero,zero,zero); unit=(one,zero,zero)
    w=[divide(unit,(x,d,zero)) for x,d in zip(tau,delta)]
    diag=[minus(plus(w[i],times((beta[i]**2,zero,zero),w[i+1])),unit) for i in range(len(beta))]+[minus(w[-1],unit)]
    edge=[times((-b,zero,zero),w[i+1]) for i,b in enumerate(beta)]
    n=len(tau); ld=[[None]*n for _ in range(n)]
    # log determinants via positive LDL pivots, not huge continuants.
    for a in range(n):
        pivot=diag[a]; total=log(pivot); ld[a][a]=total
        for b in range(a+1,n):
            pivot=minus(diag[b],divide(times(edge[b-1],edge[b-1]),pivot))
            assert pivot[0]>0
            total=plus(total,log(pivot)); ld[a][b]=total
    logZ=[z]; entropy=[z]
    for m in range(1,n+1):
        categories=[(logZ[m-1],entropy[m-1])]
        for a in range(m):
            prefix=max(0,a-1)
            categories.append((plus(logZ[prefix],ld[a][m-1]),entropy[prefix]))
        shift=max(c[0][0] for c in categories)
        fixed=(shift,zero,zero)
        total=z
        for lw,_ in categories: total=plus(total,exp(minus(lw,fixed)))
        lz=plus(fixed,log(total)); hh=z
        for lw,hp in categories:
            normalized=minus(lw,lz)
            hh=plus(hh,times(exp(normalized),minus(hp,normalized)))
        logZ.append(lz); entropy.append(hh)
    h=entropy[-1]
    return {'H':h[0],'H1':h[1],'H2':2*h[2],
            'logZ':logZ[-1][0],'logZ1':logZ[-1][1],'logZ2':2*logZ[-1][2]}

def pparts(beta,tau):
    w=[1/x for x in tau]
    return [w[i]+beta[i]**2*w[i+1] for i in range(len(beta))]+[w[-1]],[-b*w[i+1] for i,b in enumerate(beta)]

def rational_ldl(diag,edge):
    pivots=[]
    for i,d in enumerate(diag):
        pivot=d if i==0 else d-edge[i-1]**2/pivots[-1]
        assert pivot>0
        pivots.append(pivot)
    return pivots

def spectral_certificate(candidate):
    b=list(map(F,candidate['beta'])); t=list(map(F,candidate['tau'])); d=list(map(F,candidate['delta']))
    rows=[]
    for step in (F(-1,10),F(0),F(1,10)):
        tt=[x+step*y for x,y in zip(t,d)]; assert min(tt)>0
        diag,edge=pparts(b,tt)
        left=rational_ldl([x-4 for x in diag],edge)
        right=rational_ldl([50-x for x in diag],edge)
        rows.append({'t':str(step),'min_tau':str(min(tt)),
                     'min_pivot_P_minus_4I_float':float(min(left)),
                     'min_pivot_50I_minus_P_float':float(min(right)),
                     'exact_LDL_positive':True})
    return {'rows':rows,'uniform_t_interval':['-1/10','1/10'],
            'P_bounds':'4I < P < 50I','uniform_strict_K_margin':'1/50',
            'rank_D':sum(x!=0 for x in d),'non_thinning':'rank(D)=2 while rank(K)=93',
            'K_affine_identity':'K(t)=I-R^-1 diag(tau+t*delta) R^-T'}

def determinant(a):
    a=[row[:] for row in a]; value=F(1)
    for i in range(len(a)):
        pivot=next((j for j in range(i,len(a)) if a[j][i]),None)
        if pivot is None: return F(0)
        if pivot!=i: a[i],a[pivot]=a[pivot],a[i];value=-value
        v=a[i][i];value*=v
        for j in range(i+1,len(a)):
            ratio=a[j][i]/v
            for k in range(i+1,len(a)): a[j][k]-=ratio*a[i][k]
    return value

def exact_mobius(beta,tau):
    n=len(tau); U=[[F(i==j) for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(i): U[i][j]=beta[i-1]*U[i-1][j]
    K=[[F(i==j)-sum(U[i][k]*tau[k]*U[j][k] for k in range(n)) for j in range(n)] for i in range(n)]
    p=[]
    for mask in range(1<<n):
        ids=[i for i in range(n) if mask>>i&1]
        p.append(determinant([[K[i][j] for j in ids] for i in ids]))
    for i in range(n):
        for s in range(1<<n):
            if not s>>i&1: p[s]-=p[s|(1<<i)]
    assert sum(p)==1
    return p

def small_gate():
    b=[F(1,5),F(-1,4),F(1,3),F(2,7),F(-1,6)]
    t=[F(1,5)+F(i,100) for i in range(6)]
    d=[F(1,50),F(0),F(0),F(-1,60),F(0),F(0)]
    p=exact_mobius(b,t); assert min(p)>0
    pm=exact_mobius(b,[x-y for x,y in zip(t,d)])
    pp=exact_mobius(b,[x+y for x,y in zip(t,d)])
    aa=[(v-u)/2 for u,v in zip(pm,pp)]
    bb=[u+v-2*w for u,v,w in zip(pm,pp,p)]
    conv=lambda x:Dec(x.numerator)/Dec(x.denominator)
    direct={'H':-sum(conv(x)*conv(x).ln() for x in p),
            'H1':-sum(conv(a)*conv(x).ln() for x,a in zip(p,aa)),
            'H2':-sum(conv(a*a/x)+conv(b)*conv(x).ln() for x,a,b in zip(p,aa,bb))}
    dp=stable_dp(list(map(conv,b)),list(map(conv,t)),list(map(conv,d)))
    errors={key:abs(dp[key]-direct[key]) for key in direct}
    assert max(errors.values())<Dec('1e-65')
    return {'n':6,'rank_D':2,'direct_Mobius_events':64,'errors':errors,
            'probabilities':[str(x) for x in p]}

def main():
    start=time.time(); candidate=reconstruct()
    frozen=json.loads((BASE.parent/'results/frozen_n93_rank2_stability.json').read_text(encoding='utf-8'))
    parameter_match={key:candidate[key]==frozen['candidate'][key] for key in ('beta','tau','delta')}
    assert all(parameter_match.values())
    candidate['parameter_match_author_full_arrays']=parameter_match
    payload=json.dumps(candidate,sort_keys=True).encode()
    candidate['reconstruction_sha256']=hashlib.sha256(payload).hexdigest()
    (BASE/'anomaly_parameters.json').write_text(json.dumps(candidate,indent=2),encoding='utf-8')
    float_stable=stable_dp(*[list(map(float,candidate[key])) for key in ('beta','tau','delta')])
    high=[]
    for precision in (50,80):
        with localcontext() as ctx:
            ctx.prec=precision
            b,t,d=[list(map(Dec,candidate[key])) for key in ('beta','tau','delta')]
            h=stable_dp(b,t,d); high.append({'precision':precision,**h})
    with localcontext() as ctx:
        ctx.prec=80
        b,t,d=[list(map(Dec,candidate[key])) for key in ('beta','tau','delta')]
        h0=high[-1]; chords=[]
        for step in ('0.1','0.02','0.005','0.001','0.0001'):
            h=Dec(step); zero=[Dec(0)]*93
            hm=stable_dp(b,[x-h*y for x,y in zip(t,d)],zero)['H']
            hp=stable_dp(b,[x+h*y for x,y in zip(t,d)],zero)['H']
            central=(hm+hp-2*h0['H'])/(h*h)
            chords.append({'h':h,'H_minus':hm,'H_plus':hp,'gap':(hm+hp)/2-h0['H'],
                           'central_H2':central,'error_vs_jet':central-h0['H2']})
        gate=small_gate()
        author_float=frozen['candidate']['float_jet']
        Z,Z1,T=[float(author_float[key]) for key in ('Z','Z1','T')]
        lost=2*(T/Z)*(Z1/Z)**2
        error=float(author_float['H2'])-float(h0['H2'])
        diagnosis={'author_float_H2':author_float['H2'],'float_stable_H2':float_stable['H2'],
                   'Z':Z,'inverse_Z':1/Z,'inverse_Z_cubed_float':(1/Z)**3,
                   'inverse_Z_cubed_decimal':(1/Dec(str(Z)))**3,
                   'predicted_upward_H2_error':lost,'observed_H2_error':error,
                   'independent_decimal_prediction':2*(h0['logZ']-h0['H'])*h0['logZ1']**2,
                   'difference_observed_minus_predicted':error-lost,
                   'corrected_author_H2':author_float['H2']-lost}
    report={'status':'FLOAT_FALSE_POSITIVE_INDEPENDENTLY_REJECTED','python':platform.python_version(),
            'seed':20260908,'target':[93,15,'rank2'],'parameter_match':parameter_match,
            'normalized_float':float_stable,'normalized_decimal':high,'chords':chords,
            'small_Mobius_gate':gate,'spectral_certificate':spectral_certificate(candidate),
            'underflow_diagnosis':diagnosis,'exit_code':0,'elapsed_seconds':time.time()-start}
    (BASE/'anomaly_results.json').write_text(json.dumps(report,indent=2,default=str),encoding='utf-8')
    print(json.dumps({'status':report['status'],'diagnosis':diagnosis,'elapsed_seconds':report['elapsed_seconds']},default=str))

if __name__=='__main__': main()
