"""DISCARDED: symbolic diagnostic of an incomplete limiting system.

The radial/off-diagonal Fisher entry omits common events. Retained as a
failure record; never use it for the true optimizer. The output filename
was separated after the failure so rerunning it cannot replace the fix.
"""
import os,json,sys
from pathlib import Path
import sympy as S
import mpmath as mp

lam,k,m=S.symbols('lam k m',positive=True)
a=1-lam; C=a+lam*k; R=1+lam*k; H=1/C+1/lam
# Unknown V=v/sqrt(k), z, so all coefficients are rational in k.
A11=4*lam**2*k*H+2*m
A12=2*lam*(a/C-1)
A21=k*A12
A22=a*a/C+lam
b1=2*lam*R*H/m
b2=1-R*(1-a/C)/m
sol=S.simplify(S.Matrix([[A11,A12],[A21,A22]]).inv()*S.Matrix([b1,b2]))
raw=(-k-R/C+1/a)/m+(2*k*R/C)*sol[0]-(lam*k/C)*sol[1]
expr=S.factor(raw)
out={'status':'SYMBOLIC_LIMIT_SYSTEM_ONLY','pid':os.getpid(),'python':sys.version,'sympy':S.__version__,'coefficient':str(expr),'V':str(S.factor(sol[0])),'z':str(S.factor(sol[1])),'determinant':str(S.factor(A11*A22-A12*A21)),'fixed_values':[]}
mp.mp.dps=70
f=S.lambdify((lam,k,m),expr,'mpmath')
for kk in [mp.mpf(1)/10,mp.mpf(1),mp.mpf(10)]:
    ll=mp.mpf(7)/10; mm=mp.log((1-ll+ll*kk)/(1-ll))
    out['fixed_values'].append({'lambda':'7/10','kappa':str(kk),'coefficient':mp.nstr(f(ll,kk,mm),60)})
Path('sparse_limit_algebra_failed_v1.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps(out,indent=2))
