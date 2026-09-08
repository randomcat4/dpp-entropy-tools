"""U10i author sanity: standard library, no imported author gate/cache.
Stable positive-matrix Sherman--Morrison, plus direct rational Mobius gates.
Run python sanity.py. Numerical profiles remain SCOUT.
"""
import hashlib
import json
import sys
from decimal import Decimal as D, getcontext
from fractions import Fraction as Q
from pathlib import Path

sys.dont_write_bytecode=True
sys.set_int_max_str_digits(0)
getcontext().prec=180
getcontext().Emin=-999999999
getcontext().Emax=999999999
ROOT=Path(__file__).resolve().parent

def dec(v): return D(v.numerator)/D(v.denominator) if isinstance(v,Q) else D(v)
def transpose(a): return list(map(list,zip(*a)))
def mul(a,b): return [[sum(x*y for x,y in zip(r,c)) for c in transpose(b)] for r in a]
def mv(a,b): return [sum(x*y for x,y in zip(r,b)) for r in a]
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def add(a,b,c=1): return [[x+c*y for x,y in zip(r,s)] for r,s in zip(a,b)]
def outer(a,b): return [[x*y for y in b] for x in a]
def det(a):
    if not a: return 1
    return sum((-1)**j*a[0][j]*det([r[:j]+r[j+1:] for r in a[1:]]) for j in range(len(a)))
def inv(a):
    n=len(a); zero=a[0][0]*0
    m=[r[:]+[zero+int(i==j) for j in range(n)] for i,r in enumerate(a)]
    for j in range(n):
        k=max(range(j,n),key=lambda i:abs(m[i][j])); m[j],m[k]=m[k],m[j]
        p=m[j][j]; assert p
        m[j]=[t/p for t in m[j]]
        for i in range(n):
            if i!=j:
                q=m[i][j]; m[i]=[v-q*w for v,w in zip(m[i],m[j])]
    return [r[n:] for r in m]
def ldl(a):
    a=[r[:] for r in a]; out=[]
    for k in range(len(a)):
        p=a[k][k]; out.append(p)
        if p<=0: return out
        for i in range(k+1,len(a)):
            for j in range(k+1,len(a)): a[i][j]-=a[i][k]*a[k][j]/p
    return out
def to_matrix(v):
    d,e,h,k=v; return [[d,h,k],[h,e,h],[k,h,d]]
BASIS=[to_matrix([Q(i==j) for j in range(4)]) for i in range(4)]
BD=[[[dec(x) for x in r] for r in b] for b in BASIS]
L=D(2).ln(); SQRT2=D(2).sqrt()
def phi(b): return (b+L+2)*(b+L)**4/(2*b*b*L*L)

def calculate(x,s):
    assert 0<x<D('.5') and 0<s<1
    a=x*((1-s)/2).sqrt(); t=a*a
    E=(1-x)*(1-2*x+x*x*s)
    U=x*((1-x)**2+(1-2*x)*x*(1-s)/2)
    W=x*(1-x)*(1-x*s)
    V=x*x*(1+(1-2*x)*s)/2
    Z=x*x*(1-x*s); F=x*x*x*s
    assert min(E,U,W,V,Z,F)>0
    assert abs(E+2*U+W+2*V+Z+F-1)<D('1e-165')
    ell=(E*V/(U*W)).ln(); kap=(E*Z/(U*U)).ln()
    lam=s.ln()+(U*U*W/(E*(V/(x*x))**2*(Z/(x*x))*x**3)).ln()
    # Powers cancelled above: F U^2 W/(E V^2 Z)=s U^2 W/(E x^3 (V/x^2)^2(Z/x^2)).
    n=-ell-x*lam; m=-kap-x*lam
    nn=[[n,-lam*a,D(0)],[-lam*a,m,-lam*a],[D(0),-lam*a,n]]
    ni=inv(nn); delta=det(nn)
    assert len(ldl(nn))==3 and min(ldl(nn))>0
    eta=[sum(mul(ni,b)[i][i] for i in range(3)) for b in BD]
    gram=[[sum(mul(mul(mul(ni,bi),ni),bj)[k][k] for k in range(3)) for bj in BD] for bi in BD]
    w=[1+s,D(1),-2*SQRT2*(1-s).sqrt(),1-s]
    jf=[x*x*v for v in w]
    jq=[x,x,-2*a,D(0)]
    je=[4*x-2-jf[0],2*x-1-jf[1],-4*a-jf[2],-jf[3]]
    ju=[1-3*x+jf[0],-x+jf[1],2*a+jf[2],jf[3]]
    jw=[-2*x+jf[0],1-2*x+jf[1],4*a+jf[2],jf[3]]
    jv=[q-r for q,r in zip(jq,jf)]
    jz=[2*x-jf[0],-jf[1],-jf[2],-jf[3]]
    rest=[[sum(mu*g[i]*g[j]/p for mu,g,p in zip([1,2,1,2,1],[je,ju,jw,jv,jz],[E,U,W,V,Z])) for j in range(4)] for i in range(4)]
    a0=add(rest,gram,delta); ai=inv(a0)
    aieta=mv(ai,eta); aiw=mv(ai,w)
    denominator=s/x+dot(w,aiw)
    assert denominator>0
    constrained_inverse=[v-u*dot(w,aieta)/denominator for v,u in zip(aieta,aiw)]
    tt=dot(eta,constrained_inverse); assert tt>0
    sigma=eta[1]**2*(1/tt-delta)
    zmin=[eta[1]*v/tt for v in constrained_inverse]
    h=eta[1]/(eta[2]+2*SQRT2*eta[3]/(1-s).sqrt())
    trial=[D(0),D(0),h,2*SQRT2*h/(1-s).sqrt()]
    assert abs(dot(eta,trial)-eta[1])<D('1e-150')
    assert abs(dot(w,trial))<D('1e-150')
    trial_energy=dot(trial,mv(a0,trial))-delta*eta[1]**2
    assert trial_energy-sigma > -D('1e-140')
    mineig=x*s/(1+(1-s).sqrt())
    assert mineig>0 and x*(1+(1-s).sqrt())<1
    return {'sigma':sigma,'eta':eta,'delta':delta,'a0':a0,'w':w,
            'minimizer':zmin,'trial_energy':trial_energy,
            'atoms':[E,U,W,V,U,Z,V,F],'minimum_kernel_eigenvalue':mineig,
            'Lambda':lam,'n':n,'m':m}

def atoms_mobius(k):
    inc=[]
    for mask in range(8):
        ix=[i for i in range(3) if mask>>i&1]
        inc.append(det([[k[i][j] for j in ix] for i in ix]))
    return [sum((-1)**((s^t).bit_count())*inc[t] for t in range(8) if t&s==s) for s in range(8)]

def direct_gate(x,a):
    k=[[x,a,Q(0)],[a,x,a],[Q(0),a,x]]
    p=atoms_mobius(k)
    g=transpose([[(u-v)/2 for u,v in zip(atoms_mobius(add(k,b)),atoms_mobius(add(k,b,-1)))] for b in BASIS])
    hh=[[[Q(0) for _ in range(4)] for _ in range(4)] for _ in range(8)]
    for i,bi in enumerate(BASIS):
        for j,bj in enumerate(BASIS):
            pp=atoms_mobius(add(add(k,bi),bj)); pm=atoms_mobius(add(add(k,bi),bj,-1))
            mp=atoms_mobius(add(add(k,bi,-1),bj)); mm=atoms_mobius(add(add(k,bi,-1),bj,-1))
            for z in range(8): hh[z][i][j]=(pp[z]-pm[z]-mp[z]+mm[z])/4
    direct=[[sum(dec(g[z][i]*g[z][j]/p[z])+dec(hh[z][i][j])*dec(p[z]).ln() for z in range(8)) for j in range(4)] for i in range(4)]
    s=1-2*a*a/(x*x); r=calculate(dec(x),dec(s))
    full=add(add(r['a0'],outer(r['w'],r['w']),dec(x/s)),outer(r['eta'],r['eta']),-r['delta'])
    err=max(abs(direct[i][j]-full[i][j]) for i in range(4) for j in range(4))
    assert max(abs(dec(p[i])-r['atoms'][i]) for i in range(8))<D('1e-160')
    assert err<D('1e-145')
    eta=r['eta']
    t0=[[D(1),D(0),D(0)],[-eta[0]/eta[1],-eta[2]/eta[1],-eta[3]/eta[1]],
        [D(0),D(1),D(0)],[D(0),D(0),D(1)]]
    c=mul(mul(transpose(t0),direct),t0)
    b=[sum(t0[i][j]*direct[i][1] for i in range(4)) for j in range(3)]
    sigdirect=direct[1][1]-dot(b,mv(inv(c),b))
    assert abs(sigdirect-r['sigma'])<D('1e-145')
    ik=[[Q(i==j)-k[i][j] for j in range(3)] for i in range(3)]
    assert min(ldl(k))>0 and min(ldl(ik))>0
    return {'x':str(x),'a':str(a),'s':str(s),'atoms_exact':list(map(str,p)),
            'K_LDL':list(map(str,ldl(k))),'I_minus_K_LDL':list(map(str,ldl(ik))),
            'matrix_identity_error':str(err),'sigma':str(r['sigma']),
            'direct_schur_error':str(abs(sigdirect-r['sigma']))}

gates=[direct_gate(x,a) for x,a in [(Q(1,10),Q(1,20)),(Q(1,4),Q(1,10)),(Q(2,5),Q(3,20))]]
rows=[]
for beta in map(D,['.01','.1','.3','.58','1','3','10']):
    for x in map(D,['.01','.001','.0001','.000001']):
        s=(-beta/x).exp(); out=calculate(x,s)
        ph=phi(beta)
        h0=-(beta+L)**2/(2*SQRT2*beta*L); z0=[D(0),D(0),h0,2*SQRT2*h0]
        assert out['sigma']>0
        rows.append({'beta':str(beta),'x':str(x),'log_s':str(-beta/x),
                     'sigma':str(out['sigma']),'phi':str(ph),'sigma_minus_phi':str(out['sigma']-ph),
                     'absolute_error_over_sqrt_x':str(abs(out['sigma']-ph)/x.sqrt()),
                     'minimizer':list(map(str,out['minimizer'])),'limiting_minimizer':list(map(str,z0)),
                     'trial_energy':str(out['trial_energy']),
                     'minimum_kernel_eigenvalue':str(out['minimum_kernel_eigenvalue']),
                     'status':'SCOUT_ONLY'})
bestbeta=(((L+4)**2+24*L*(L+2)).sqrt()-(L+4))/6
assert abs(3*bestbeta**2+(L+4)*bestbeta-2*L*(L+2))<D('1e-170')
sources={}
for file in ['frozen_problem.md','proof_candidate.md','sanity.py',
             '../derivation.md','../boundary_full_atom/analysis.md']:
    sources[file]=hashlib.sha256((ROOT/file).read_bytes()).hexdigest()
result={'status':'AUTHOR_PROOF_CANDIDATE_PENDING_REVIEW_GLOBAL_PATH_INCOMPLETE',
        'precision':180,'denominators':{'direct_rational_Mobius_gates':3,'fixed_exponential_points':28,
                                       'failures':0,'positive_curvature_candidates':0},
        'execution_history':[
            {'stage':'initial run','exit_code':1,'reason':'generic determinant empty base returned Fraction(1), incompatible with Decimal multiplication; no case completed'},
            {'stage':'after scalar-type repair','exit_code':0,'repair':'empty determinant returns integer 1, valid for both Fraction and Decimal'},
            {'stage':'final clean replay','exit_code':0}],
        'phi_formula':'(beta+log(2)+2)*(beta+log(2))^4/(2*beta^2*log(2)^2)',
        'beta_star':str(bestbeta),'phi_minimum':str(phi(bestbeta)),
        'global_phi_lower_bound':str(8*(L+2)),
        'small_beta_scaled_limit':str(L*L*(L+2)/2),'large_beta_scaled_limit':str(1/(2*L*L)),
        'uniform_scope':'beta in every fixed compact subset of (0,infinity); constants depend on its endpoints',
        'direct_gates':gates,'exponential_rows':rows,'source_hashes':sources}
(ROOT/'sanity.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:result[k] for k in ['status','denominators','beta_star','phi_minimum','global_phi_lower_bound']},indent=2))
