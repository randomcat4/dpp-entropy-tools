"""Exact, bounded symbolic replay; no sampling and no sign oracle."""
import os, sys, json
os.environ.update(OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1')
import sympy as s
print(json.dumps({'pid':os.getpid(),'command':'python verify.py','seed':None,
                  'python':sys.version.split()[0],'sympy':s.__version__}),flush=True)
d,r,t,u,v=s.symbols('d r t u v', real=True)
x=s.symbols('x0:3'); y=s.symbols('y0:3')
z=s.symbols('z0:4') # independent formal log-probabilities
K=s.Matrix([[d,r,r],[r,d,r],[r,r,d]])
V=s.Matrix([[x[0],y[2],y[1]],[y[2],x[1],y[0]],[y[1],y[0],x[2]]])
def probs(K):
    out=[]
    for mask in range(8):
        val=0
        for sup in range(8):
            if sup & mask == mask:
                ix=[i for i in range(3) if sup>>i&1]
                val+=(-1)**(len(ix)-mask.bit_count())*(K.extract(ix,ix).det() if ix else 1)
        out.append(s.expand(val))
    return out
checks=0
def eq(a,b):
    global checks
    assert s.cancel(a-b)==0, s.factor(a-b)
    checks+=1
P=[(1-d)**3-3*(1-d)*r*r-2*r**3,
   d*(1-d)**2+(2-3*d)*r*r+2*r**3,
   d*d*(1-d)+(3*d-1)*r*r-2*r**3,
   d**3-3*d*r*r+2*r**3]
pt=probs(K+t*V)
pd=[s.diff(p,t).subs(t,0).expand() for p in pt]
pdd=[s.diff(p,t,2).subs(t,0).expand() for p in pt]
for mask,p in enumerate(pt): eq(p.subs(t,0),P[mask.bit_count()])
eq(sum(pt),1)
a=sum(x)/3; b=sum(y)/3
xc=[w-a for w in x]; yc=[w-b for w in y]
XX=sum(w*w for w in xc); YY=sum(w*w for w in yc)
XY=sum(j*k for j,k in zip(xc,yc))
Tfirst=[-3*((1-d)**2-r*r)*u-6*r*(1-d+r)*v,
        ((1-d)*(1-3*d)-3*r*r)*u+(2*r*(2-3*d)+6*r*r)*v,
        (d*(2-3*d)+3*r*r)*u+(2*r*(3*d-1)-6*r*r)*v,
        3*(d*d-r*r)*u+6*r*(r-d)*v]
stdSquares=[0,2*((1-d)*u-2*r*v)**2,2*(d*u+2*r*v)**2,0]
def lift(poly):
    p=s.Poly(s.expand(poly),u,v)
    return (p.coeff_monomial(u*u)*XX+p.coeff_monomial(u*v)*XY+p.coeff_monomial(v*v)*YY)/2
for k,multiplicity in enumerate([1,3,3,1]):
    actual=sum(pd[m]**2 for m in range(8) if m.bit_count()==k)
    expected=multiplicity*Tfirst[k].subs({u:a,v:b})**2+lift(stdSquares[k])
    eq(actual,expected)
M=(1-d)*z[0]+(3*d-2)*z[1]+(1-3*d)*z[2]+d*z[3]
Lg=z[0]-3*z[1]+3*z[2]-z[3]
Tlog=6*M*u*u+12*r*Lg*u*v+(-6*M-12*r*Lg)*v*v
Slog=-2*M*u*u+8*r*Lg*u*v+(-4*M+4*r*Lg)*v*v
actual=sum(pdd[m]*z[m.bit_count()] for m in range(8))
eq(actual,Tlog.subs({u:a,v:b})+lift(Slog))
q=s.symbols('q',positive=True)
for actual,expected in zip(P,[(1+q)**2*(1-2*q)/8,
 (1+q)*(1-q+2*q*q)/8,(1-q)*(1+q+2*q*q)/8,(1-q)**2*(1+2*q)/8]):
    eq(actual.subs({d:s.Rational(1,2),r:q/2}),expected)
Mq=s.log((1-q*q)*(1-4*q*q)/(1+3*q*q+4*q**4))/2
Lq=s.log((1-q)*(1-2*q)*(1+q+2*q*q)**3/((1+q)*(1+2*q)*(1-q+2*q*q)**3))
E=(1-q*q)*(1-4*q*q)*(1+3*q*q+4*q**4)
eq(s.diff(Mq,q),8*q*(2*q*q-1)*(2*q*q+1)/E)
eq(s.diff(Lq,q),48*q*q*(2*q*q-1)/E)
eq(s.diff(Lq,q)/s.diff(Mq,q),6*q/(1+2*q*q))
eq(s.diff(6*q/(1+2*q*q),q),6*(1-2*q*q)/(1+2*q*q)**2)
m,ell=s.symbols('m ell')
eq((2*m)*(4*m-4*ell)-16*ell*ell,8*(m-2*ell)*(m+ell))
Sf=2*(((1-d)*u-2*r*v)**2/P[1]+(d*u+2*r*v)**2/P[2])+Slog
eq(Sf.subs({d:s.Rational(1,2),r:0,z[0]:0,z[1]:0,z[2]:0,z[3]:0}),8*u*u)
print(json.dumps({'status':'PASS','exact_identity_checks':checks,'exit_code':0}),flush=True)
