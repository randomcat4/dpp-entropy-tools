"""Exact first-unit checks; run with Python 3 + sympy, mpmath, numpy.
No network, private paths, or inherited research output required.
"""
import itertools as it
import json
import os
import platform
from pathlib import Path
import sympy as s
import mpmath as mp
import numpy as np

Q = s.Rational
I = s.eye(3)
t = s.Symbol('t')
a, b = s.Matrix([1,2,3,4,5]), s.Matrix([2,-1,3,-2,1])
U = ((s.eye(5)-2*a*a.T/(a.dot(a)))*(s.eye(5)-2*b*b.T/(b.dot(b))))[:, :3]
assert U.T*U == I
subsets = [tuple(z) for k in range(6) for z in it.combinations(range(5), k)]
r = [U[i,:].T for i in range(5)]
w = {(i,j):r[i].cross(r[j]) for i,j in it.combinations(range(5),2)}
A = s.Matrix([[Q(3,5),Q(1,20),Q(1,30)],[Q(1,20),Q(2,3),Q(-1,40)],[Q(1,30),Q(-1,40),Q(1,2)]])
V = s.Matrix([[Q(1,10),Q(1,7),Q(-1,11)],[Q(1,7),Q(-1,8),Q(1,13)],[Q(-1,11),Q(1,13),Q(1,12)]])
At = A+t*V
K = U*At*U.T
inc = {z:s.expand(K.extract(z,z).det()) if 0<len(z)<=3 else s.Integer(1 if len(z)==0 else 0) for z in subsets}
p = {z:s.expand(sum((-1)**(len(T)-len(z))*inc[T] for T in subsets if set(z)<=set(T))) for z in subsets}
d = s.expand(At.det())
C = At.adjugate()-d*I
E = At*At+(1-s.trace(At))*At+d*I
form = {():s.expand((I-At).det())}
for i in range(5): form[(i,)]=s.expand((r[i].T*E*r[i])[0])
for z,x in w.items(): form[z]=s.expand((x.T*C*x)[0])
for z in subsets:
    if len(z)==3: form[z]=s.expand(d*U.extract(z,range(3)).det()**2)
    elif len(z)>3: form[z]=s.Integer(0)
assert all(s.expand(p[z]-form[z])==0 for z in subsets)
assert s.expand(sum(p.values()))==1
jets = {z:[p[z].subs(t,0),s.diff(p[z],t).subs(t,0),s.diff(p[z],t,2).subs(t,0)] for z in subsets}
assert [sum(j[k] for j in jets.values()) for k in range(3)]==[1,0,0]
assert sum((3-len(z))*j[2] for z,j in jets.items())==0
assert A*V != V*A
for Z in (A,I-A,A+Q(1,10)*V,I-A-Q(1,10)*V,A-Q(1,10)*V,I-A+Q(1,10)*V):
    assert all(Z[:k,:k].det()>0 for k in range(1,4))
mp.mp.dps=80
def m(x):return mp.mpf(str(s.N(x,85)))
layers=[]
for k in range(4):
    js=[j for z,j in jets.items() if len(z)==k]
    fisher=sum(m(j[1])**2/m(j[0]) for j in js)
    accel=-sum(m(j[2])*mp.log(m(j[0])) for j in js)
    layers.append({'cardinality':k,'mass':str(sum(j[0] for j in js)),'fisher':str(fisher),'log_acceleration':str(accel),'curvature':str(accel-fisher)})
def entropy(tau):
    return -sum(m(pp.subs(t,tau))*mp.log(m(pp.subs(t,tau))) for pp in p.values() if pp!=0)
curv=sum(mp.mpf(x['curvature']) for x in layers)
diffs=[]
for h in [Q(1,1000),Q(1,10000),Q(1,100000)]:
    fd=(entropy(h)+entropy(-h)-2*entropy(0))/m(h)**2
    diffs.append({'h':str(h),'finite_difference':str(fd),'analytic':str(curv),'error':str(fd-curv)})

# Rational frame lower bound in coordinates (X11,X22,X33,X12,X13,X23).
G=s.zeros(6)
for x in w.values():
    row=s.Matrix([x[0]**2,x[1]**2,x[2]**2,2*x[0]*x[1],2*x[0]*x[2],2*x[1]*x[2]])
    G+=row*row.T/x.dot(x)
D=s.diag(1,1,1,2,2,2)
rough=1/s.trace(D*G.inv())
den=int(s.ceiling(1/rough))
kappa=Q(1,den)
minors=[(G-kappa*D)[:i,:i].det() for i in range(1,7)]
assert all(x>0 for x in minors)
g={z:U.extract(z,range(3)).multiply(U.extract(z,range(3)).T).det() if z else s.Integer(1) for z in subsets if len(z)<=3}
# For I<=B<=2I and e<=1/16, g_S >= det Gram / 4^|S|,
# g_S <=8. Rational bounds exp(-10)<1/2^14 and exp(10)>2^14
# follow e>8/3, (8/3)^10 > 2^14. Hence use L=10 if g/4^s>2^-14.
assert Q(8,3)**10 > 2**14
assert min(g[z]/4**len(z) for z in g)>Q(1,2**14)
# The explicit cone radius follows e<=kappa/(4480*M*L).
radius=Q(1,int(s.ceiling(4480*2*10/kappa)))
out={'status':'PASS','python':platform.python_version(),'sympy':s.__version__,'mpmath':mp.__version__,'numpy':np.__version__,'pid':os.getpid(),
     'U':str(U),'A':str(A),'V':str(V),'noncommutator_squared':str(s.trace((A*V-V*A).T*(A*V-V*A))),
     'identity_event_count':32,'positive_support':26,'jet_sums':['1','0','0'],'weighted_second_sum':'0',
     'jets':{','.join(str(i+1) for i in z) or 'empty':[str(x) for x in j] for z,j in jets.items()},
     'layers':layers,'differences':diffs,
     'frame':{'G':[[str(x) for x in G.row(i)] for i in range(6)],'kappa':str(kappa),'positive_sylvester_minors':[str(x) for x in minors],'trace_inverse_bound':str(rough)},
     'uniform_cone':{'m':1,'M':2,'log_bound':10,'min_normalized_mass_lower':str(min(g[z]/4**len(z) for z in g)),'radius':str(radius),'curvature_upper':'-kappa/(16*e) * ||V||_F^2'}}
Path('main_check.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in out.items() if k not in ['jets','frame','U','A','V']},indent=2))
print('kappa',kappa,'radius',radius)
