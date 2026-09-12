"""Full-configuration, directed-interval certification for ONE fixed symbol.
No repository writes. No omitted atoms. Derivatives are with respect to a,
not to t=a/(1-c). Every a jet stores the coefficient of (da)^j, j=0,1,2.
"""
from fractions import Fraction as F
from pathlib import Path
import json,time,hashlib
import intervals as iv
from intervals import R,C,phase,pi,log,h,jmul,jinv,jsub,jconj

def matrix(spec,n):
 if 'bands' in spec:
  bands=[(F(l),F(r)) for l,r in spec['bands']]
  assert all(0<=l<r<=1 for l,r in bands)
  assert all(bands[i][1]<=bands[i+1][0] for i in range(len(bands)-1))
  coeff=[C(sum((r-l for l,r in bands),F(0)))]
  for d in range(1,n):
   v=C(0)
   for l,r in bands:
    # integral exp(-2pi i d theta) dtheta
    numerator=phase(-d*l)-phase(-d*r)
    v=v+numerator/C(0,2*pi()*d)
   coeff.append(v)
 else:
  m=spec['m'];S=spec['S'];assert n==m
  coeff=[sum((phase(F(-d*s,m)) for s in S),C(0))/m for d in range(n)]
 return [[coeff[i-j] if i>=j else coeff[j-i].conj() for j in range(n)] for i in range(n)]

def tree(Q,a,c,save_leaves=False):
 n=len(Q)
 K=[[(C(a+c*Q[i][j].re) if i==j else Q[i][j]*c,C(1 if i==j else 0),C(0)) for j in range(n)] for i in range(n)]
 stats=[{'H':R(0),'Hp':R(0),'Hpp':R(0),'F':R(0),'A':R(0),'mass':R(0),'d1':R(0),'d2':R(0),'count':0} for _ in range(n+1)]
 leaves=[]; minp=iv.S;minq=iv.S;maxq=0
 def rec(M,p,depth,mask):
  nonlocal minp,minq,maxq
  if depth:
   p0,p1,p2=p
   if p0.lo<=0:raise ArithmeticError('complete-event probability not certified positive')
   lp=log(p0);s=stats[depth]
   s['H']=s['H']-p0*lp;s['Hp']=s['Hp']-p1*lp
   fish=p1.sq()/p0;acc=-2*p2*lp
   s['F']=s['F']+fish;s['A']=s['A']+acc;s['Hpp']=s['Hpp']+acc-fish
   s['mass']=s['mass']+p0;s['d1']=s['d1']+p1;s['d2']=s['d2']+2*p2;s['count']+=1
  if not M:
   minp=min(minp,p[0].lo)
   if save_leaves:leaves.append((mask,p))
   return
  size=len(M);diag=tuple(M[0][0][j].re for j in range(3))
  # The conditional kernels are Hermitian as exact functions of real a.
  outer=[[None]*(size-1) for _ in range(size-1)]
  for i in range(1,size):
   for j in range(i,size):outer[i-1][j-1]=jmul(M[i][0],jconj(M[j][0]))
  for bit in (0,1):
   q=diag if bit else (1-diag[0],-diag[1],-diag[2])
   if q[0].lo<=0 or q[0].hi>=iv.S:raise ArithmeticError('conditional denominator not in (0,1)')
   minq=min(minq,q[0].lo);maxq=max(maxq,q[0].hi)
   iq=jinv(q);T=[[None]*(size-1) for _ in range(size-1)]
   for i in range(1,size):
    for j in range(i,size):
     correction=jmul(outer[i-1][j-1],iq)
     entry=jsub(M[i][j],correction) if bit else tuple(M[i][j][s]+correction[s] for s in range(3))
     if i==j:entry=tuple(C(x.re,0) for x in entry)
     T[i-1][j-1]=entry;T[j-1][i-1]=jconj(entry)
   rec(T,jmul(p,q),depth+1,mask|(bit<<depth))
 rec(K,(R(1),R(0),R(0)),0,0)
 for depth,s in enumerate(stats[1:],1):
  if s['count']!=1<<depth:raise AssertionError('incomplete enumeration')
  if not(s['mass'].contains(1) and s['d1'].contains(0) and s['d2'].contains(0)):raise AssertionError('normalization jet audit failed')
 return stats,leaves,{'min_probability_lower':minp/iv.S,'min_conditional_lower':minq/iv.S,'max_conditional_upper':maxq/iv.S}

def inertia(Q,t):
 """Verified unpivoted Hermitian LDL inertia. Return None if inconclusive."""
 n=len(Q);A=[[Q[i][j]-(t if i==j else 0) for j in range(n)] for i in range(n)]
 neg=0
 for k in range(n):
  d=A[k][k].re
  if d.lo<=0<=d.hi:return None
  neg+=int(d.hi<0)
  for i in range(k+1,n):
   for j in range(i,n):
    v=A[i][j]-A[i][k]*A[j][k].conj()/d
    if i==j:v=C(v.re,0)
    A[i][j]=v;A[j][i]=v.conj()
 return neg

def eigen_proposals(Q):
 import numpy as np
 return [F.from_float(float(x)) for x in np.linalg.eigvalsh(np.array([[z.approx() for z in row] for row in Q]))]

def certify_eigen(Q,proposals=None):
 if proposals is None:proposals=eigen_proposals(Q)
 result=[]
 for i,v in enumerate(proposals):
  for b in (42,36,30,24,18,12,6):
   e=F(1,1<<b);l=v-e;u=v+e
   il=inertia(Q,R(l));iu=inertia(Q,R(u))
   if il is not None and iu is not None and il<=i<iu:
    result.append({'l':str(max(F(0),l)),'u':str(min(F(1),u)),'left_inertia':il,'right_inertia':iu,'test_l':str(l),'test_u':str(u)})
    break
  else:raise ArithmeticError('failed eigenvalue enclosure')
 return result

def serial(s):
 return {k:({'dyadic':v.data(),'display':v.floats()} if isinstance(v,R) else v) for k,v in s.items()}

def certify(spec,n,a,c,bits=256,eigen=True,save=False):
 iv.set_precision(bits);start=time.time();Q=matrix(spec,n)
 aa=R(*a) if isinstance(a,list) else R(a);cc=R(*c) if isinstance(c,list) else R(c)
 if aa.lo<=0 or (aa+cc).hi>=iv.S:raise ValueError('not a common strict spectral strip')
 stats,leaves,details=tree(Q,aa,cc,save)
 out={'schema':'scalar-dpp-certificate-v1','spec':spec,'n':n,'a':a,'c':c,'bits':bits,'stats':[serial(s) for s in stats[1:]],'diagnostics':details,'leaf_count':1<<n,'prefix_atom_count':(1<<(n+1))-2}
 if eigen and 'bands' in spec:
  ee=certify_eigen(Q);rho=sum((F(r)-F(l) for l,r in spec['bands']),F(0))
  S=R(0)
  for z in ee:S=S+h(aa+cc*R(z['l'],z['u']))
  spectrum=(1-rho)*h(aa)+rho*h(aa+cc)
  eps=S/n-spectrum
  block=stats[n]['H']/n
  upper=(stats[n]['H']-stats[n-1]['H']) if n>1 else block
  lower=block-eps
  # A second shape-independent lower bound from conditional channel entropy.
  lower=R(max(lower.lo,spectrum.lo),max(lower.hi,spectrum.hi),raw=True)
  out['eigenvalue_enclosures']=ee
  out['spectral_entropy_density']=serial({'s':spectrum})['s']
  out['boundary_error']=serial({'e':eps})['e']
  out['rate_enclosure']={'lower':str(lower.lo),'upper':str(upper.hi),'display':[lower.lo/iv.S,upper.hi/iv.S]}
 out['seconds']=time.time()-start
 return out,leaves,Q

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--output',required=True);args=p.parse_args()
 spec=json.loads(Path(args.input).read_text())
 out,_,_=certify(**spec)
 Path(args.output).write_text(json.dumps(out,indent=2))
 print(json.dumps({'n':out['n'],'seconds':out['seconds'],'Hpp':out['stats'][-1]['Hpp']['display'],'rate':out.get('rate_enclosure',{}).get('display')}))
