import sympy as s
from itertools import product
import json
R=s.Rational
t,x,y=s.symbols('t x y', real=True)
C=s.Matrix([[R(1,2),R(2,5)],[R(2,5),R(1,2)]])
u=s.Matrix([1,1]);v=s.Matrix([1,-1])
K=s.Matrix([[R(1,2),R(1,10),R(1,10)],[R(1,10),R(1,2),R(2,5)],[R(1,10),R(2,5),R(1,2)]])
D=s.Matrix([[0,1,-1],[1,0,0],[-1,0,0]])
def probs(A):
 n=A.rows
 return {''.join(map(str,bits)):s.factor((-1)**(n-sum(bits))*(A-s.diag(*[1-i for i in bits])).det()) for bits in product([0,1],repeat=n)}
def grad(A,V):
 p=probs(A+t*V)
 return -sum(s.diff(z,t).subs(t,0)*s.log(z.subs(t,0)) for z in p.values())
def terms(A,V):
 p=probs(A+t*V)
 fisher=sum(s.diff(z,t).subs(t,0)**2/z.subs(t,0) for z in p.values())
 accel=-sum(s.diff(z,t,2).subs(t,0)*s.log(z.subs(t,0)) for z in p.values())
 return s.factor(fisher),s.expand_log(accel,force=True),s.N(accel-fisher,30)
C1=C-R(1,50)*u*u.T;C0=C+R(1,50)*u*u.T
A=2*(grad(C0,v*v.T)-grad(C1,v*v.T))
print('C1',C1,'C0',C0)
print('accel exact',s.expand_log(A,force=True),'numeric',s.N(A,30))
print('K',K,'D',D,'commute',K*D-D*K)
print('p',probs(K+t*D));print('K curvature',terms(K,D))
# Tangential conditional Hessians, holding a fixed
b=R(1,10)*u
V1=-2*(v*b.T+b*v.T);V0=2*(v*b.T+b*v.T)
print('conditional V',V1,V0)
print('C1 tangential',terms(C1,V1));print('C0 tangential',terms(C0,V0))
print('C mixed',s.simplify(s.diff(-sum(p*s.log(p) for p in probs(C+x*u*u.T+y*v*v.T).values()),x,y).subs({x:0,y:0})))
print('Sylvester', [K[:i,:i].det() for i in range(1,4)],[(s.eye(3)-K)[:i,:i].det() for i in range(1,4)])
