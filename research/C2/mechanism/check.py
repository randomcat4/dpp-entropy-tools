"""Single rational noncommuting fixture; calibration, not proof by sampling."""
import sys, platform, itertools, json
import sympy as sp
import mpmath as mp
mp.mp.dps=70
a=sp.Matrix([1,2,3,4,5]); b=sp.Matrix([2,-1,3,-2,1])
I5=sp.eye(5); U=((I5-2*a*a.T/(a.dot(a)))*(I5-2*b*b.T/(b.dot(b))))[:,:3]
B=sp.Matrix([[2,sp.Rational(1,3),0],[sp.Rational(1,3),1,sp.Rational(1,4)],[0,sp.Rational(1,4),sp.Rational(3,2)]])
V=sp.Matrix([[1,sp.Rational(1,2),sp.Rational(-1,3)],[sp.Rational(1,2),-1,sp.Rational(1,4)],[sp.Rational(-1,3),sp.Rational(1,4),sp.Rational(2,3)]])
e,t=sp.symbols('e t'); A=sp.eye(3)-e*B+t*V; C=sp.eye(3)-A
K=U*A*U.T
subsets=[x for k in range(6) for x in itertools.combinations(range(5),k)]
detK={S:sp.expand(K.extract(S,S).det()) if S else sp.Integer(1) for S in subsets}
law={S:sp.expand(sum((-1)**(len(T)-len(S))*v for T,v in detK.items() if set(S)<=set(T))) for S in subsets}
polys={():sp.expand(C.det())}
for i in range(5):
 r=U[i,:].T; polys[(i,)]=sp.expand((r.T*(C.adjugate()-C.det()*sp.eye(3))*r)[0])
for i,j in itertools.combinations(range(5),2):
 w=U[i,:].T.cross(U[j,:].T)
 polys[(i,j)]=sp.expand((w.T*(C+C*C-sp.trace(C)*C+C.det()*sp.eye(3))*w)[0])
for S in itertools.combinations(range(5),3): polys[S]=sp.expand(A.det()*U.extract(S,range(3)).det()**2)
assert U.T*U==sp.eye(3) and B*V!=V*B
assert all(sp.expand(law[S]-polys.get(S,0))==0 for S in subsets)
assert sp.expand(sum(polys.values()))==1
assert sp.expand(sum((3-len(S))*sp.diff(p,t,2) for S,p in polys.items()))==0
jets=[(len(S),p.subs(t,0),sp.diff(p,t).subs(t,0),sp.diff(p,t,2).subs(t,0)) for S,p in polys.items()]
def num(x): return mp.mpf(str(sp.N(x,75)))
rs=[U[i,:].T for i in range(5)]; ws=[rs[i].cross(rs[j]) for i,j in itertools.combinations(range(5),2)]
J=mp.mpf(0); const=mp.mpf(0)
for w in ws:
 bb=(w.T*B*w)[0]; cc=(w.T*(B*B-sp.trace(B)*B)*w)[0]
 ff=(w.T*V*w)[0]; gg=(w.T*(sp.trace(V)*B+sp.trace(B)*V-B*V-V*B)*w)[0]
 hh=2*(w.T*(V*V-sp.trace(V)*V)*w)[0]
 J+=num(ff**2/bb)
 const+=num(2*ff*gg/bb+ff**2*cc/bb**2)-num(hh)*mp.log(num(bb))
DB=(B+t*V).adjugate().diff(t).subs(t,0)
for r in rs:
 aa=(r.T*B.adjugate()*r)[0]; ll=(r.T*DB*r)[0]; kk=2*(r.T*V.adjugate()*r)[0]
 const-=num(ll**2/aa)+num(kk)*mp.log(num(aa))
q=[U.extract(S,range(3)).det()**2 for S in itertools.combinations(range(5),3)]
cU=-sum(num(x)*mp.log(num(x)) for x in q)
const-=num(sp.trace(V)**2)
const+=cU*num(sp.trace(V)**2-sp.trace(V*V))
print(json.dumps({'python':platform.python_version(),'sympy':sp.__version__,'mpmath':mp.__version__,'exact_probability_identity':True,'normalization':True,'weighted_log_cancellation':True,'noncommuting':True,'J':str(J),'constant':str(const)},indent=2))
for ev in [sp.Rational(1,100),sp.Rational(1,1000),sp.Rational(1,10000)]:
 layers={k:[mp.mpf(0),mp.mpf(0)] for k in range(4)}
 for k,p,d,dd in jets:
  p,d,dd=[num(z.subs(e,ev)) for z in [p,d,dd]]
  layers[k][0]-=d*d/p; layers[k][1]-=dd*mp.log(p)
 H2=sum(sum(v) for v in layers.values())
 # Independent direct finite difference of the original 26-event entropy.
 h=num(ev)/mp.mpf(1000000)
 def ent(tv):
  ps=[num(p.subs({e:ev,t:sp.Float(str(tv),75)})) for p in polys.values()]
  return -sum(p*mp.log(p) for p in ps)
 fd=(ent(h)-2*ent(mp.mpf(0))+ent(-h))/(h*h)
 print(json.dumps({'e':str(ev),'layers_Fisher_log_total':{k:[str(v[0]),str(v[1]),str(sum(v))] for k,v in layers.items()},'H2':str(H2),'finite_difference_error':str(fd-H2),'asymptotic_remainder_divided_by_e':str((H2+J/num(ev)-const)/num(ev))},indent=2))
