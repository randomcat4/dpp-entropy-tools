"""Exact checks of score Gram, fixed-direction coupling and t=u^4 normalization.
Author self-check, not independent review. No sampled sign test.
"""
import sympy as s
from certificate import reduced_matrix,mu,nu,r,t
u0=s.symbols('u',positive=True)
a=(1+r)/2;b=(1-r)/2;v=(1-mu**2)/4;w=(1-nu**2)/4
x=(1+mu)/2;y=(1+nu)/2;J=1-u0**4;L=1-r*r*u0**4
Delta=s.diag(1,v,w,v*w)
S=s.Matrix([[mu*nu,2*v*nu,2*w*mu,4*v*w],[2*v*nu,-mu*nu*v,4*v*w,-2*mu*v*w],[2*w*mu,4*v*w,-mu*nu*w,-2*nu*v*w],[4*v*w,-2*mu*v*w,-2*nu*v*w,mu*nu*v*w]])
d0=(1/J+1/L)/2;d1=(1/J-1/L)/2;G=d0*Delta+d1*S

def zero(A):
    for q in A:
        assert s.cancel(q)==0

zero(S*Delta.inv()*S-Delta)
GF=s.zeros(4)
for i in (0,1):
 for j in (0,1):
  P=(x if i else 1-x)*(y if j else 1-y)
  ev=i-x;fv=j-y;V=s.Matrix([1,ev,fv,ev*fv])
  GF+=P/(J if i==j else L)*V*V.T
zero(G-GF)

n1=4*u0*(1/J-r/L);n2=4*u0*(1/J+r/L);n3=4*u0**3*(1-r*r)/(J*L)
Q=s.zeros(6)
for i,j,val in [(0,1,-n3*v*w),(0,2,-n2*v),(1,2,-n1*w)]:Q[i,j]=Q[j,i]=val
Q[3,3]=2*n3*a*b*v*w;Q[4,4]=2*n2*a*v;Q[5,5]=2*n1*b*w
# zeta from W=(alpha,beta,m,p,q,h), formed only after differentiating.
T=s.zeros(6);T[0,0]=T[1,1]=1
T[2,0]=-u0**2*a*v;T[2,1]=-u0**2*b*w;T[2,2]=1
T[3,5]=1/(2*u0**2*a*b)
T[4,0]=-u0*mu/2;T[4,3]=-1/(2*u0*a)
T[5,1]=-u0*nu/2;T[5,4]=-1/(2*u0*b)
R=s.diag(0,1/u0,1/u0,2/u0)
A=s.Matrix([2*u0*a*v,-u0*a*mu,0,0]);B=s.Matrix([2*u0*b*w,0,-u0*b*nu,0])
Mf=s.zeros(6);Mf[2:6,2:6]=4*(R*G+G*R+G.diff(u0))
fa=8*G*A;fb=8*G*B
for j in range(4):
 Mf[0,j+2]=Mf[j+2,0]=fa[j]/2
 Mf[1,j+2]=Mf[j+2,1]=fb[j]/2
M=Mf+T.T*Q*T
ca=n2*a*u0**2*v/2;cb=n1*b*u0**2*w/2
la=s.Matrix([-2*b,a*nu+b*mu,0,2*a*w]);lb=s.Matrix([-2*a,0,a*nu+b*mu,2*b*v])
ea=8*u0*v*d1*la;eb=8*u0*w*d1*lb
zero(M[:2,:2]-s.diag(ca,cb))
zero(2*M[2:6,0]-ea);zero(2*M[2:6,1]-eb)
R0=4*(R*G+G*R+G.diff(u0))+s.diag(0,n2*v/(2*u0**2*a),n1*w/(2*u0**2*b),n3*v*w/(2*u0**4*a*b))
zero(M[2:6,2:6]-R0)
RS=R0-ea*ea.T/(4*ca)-eb*eb.T/(4*cb)
RB,_,_=reduced_matrix()
zero(u0*RS/4-RB.subs(t,u0**4))
print('ALL SCORE, FIXED-DIRECTION SCHUR AND NORMALIZATION IDENTITIES PASSED')
