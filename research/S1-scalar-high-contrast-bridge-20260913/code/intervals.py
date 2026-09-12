"""Small directed dyadic interval kernel; standard library only.
Every endpoint is an integer / 2**BITS. All algebraic operations round
outwards by Python's exact integer arithmetic. log/sin/cos/pi use explicitly
bounded rational Taylor series, never the host libm.
"""
from fractions import Fraction
from functools import lru_cache
from math import factorial
BITS=256
S=1<<BITS

def ceildiv(x,y): return -((-x)//y)

def set_precision(bits):
 global BITS,S
 BITS=int(bits);S=1<<BITS
 ln2.cache_clear();pi.cache_clear();phase.cache_clear()

class R:
 __slots__=('lo','hi')
 def __init__(self,lo,hi=None,raw=False):
  if raw: self.lo=int(lo);self.hi=int(hi);return
  if isinstance(lo,R): self.lo=lo.lo;self.hi=lo.hi;return
  if hi is not None:
   a=Fraction(lo);b=Fraction(hi)
   self.lo=(a.numerator*S)//a.denominator
   self.hi=ceildiv(b.numerator*S,b.denominator)
  else:
   a=Fraction(lo);self.lo=(a.numerator*S)//a.denominator;self.hi=ceildiv(a.numerator*S,a.denominator)
  if self.lo>self.hi: raise ValueError('reversed interval')
 def __add__(self,o):
  o=asr(o);return R(self.lo+o.lo,self.hi+o.hi,raw=True)
 __radd__=__add__
 def __neg__(self): return R(-self.hi,-self.lo,raw=True)
 def __sub__(self,o): return self+-asr(o)
 def __rsub__(self,o): return asr(o)+-self
 def __mul__(self,o):
  o=asr(o);t=(self.lo*o.lo,self.lo*o.hi,self.hi*o.lo,self.hi*o.hi)
  return R(min(t)//S,ceildiv(max(t),S),raw=True)
 __rmul__=__mul__
 def inv(self):
  if self.lo<=0<=self.hi: raise ArithmeticError('denominator interval contains zero')
  return R((S*S)//self.hi,ceildiv(S*S,self.lo),raw=True)
 def __truediv__(self,o): return self*asr(o).inv()
 def __rtruediv__(self,o): return asr(o)*self.inv()
 def sq(self):
  lo=0 if self.lo<=0<=self.hi else min(self.lo*self.lo,self.hi*self.hi)
  hi=max(self.lo*self.lo,self.hi*self.hi)
  return R(lo//S,ceildiv(hi,S),raw=True)
 def __pow__(self,n):
  if n<0:return self.inv()**(-n)
  out=R(1);x=self
  while n:
   if n&1:out=out*x
   x=x.sq();n>>=1
  return out
 def contains(self,x=0):
  x=Fraction(x);return self.lo*x.denominator<=x.numerator*S<=self.hi*x.denominator
 def overlaps(self,o):o=asr(o);return max(self.lo,o.lo)<=min(self.hi,o.hi)
 def intersection(self,o):
  o=asr(o);lo=max(self.lo,o.lo);hi=min(self.hi,o.hi)
  if lo>hi:raise ArithmeticError('empty intersection')
  return R(lo,hi,raw=True)
 def floats(self):return [self.lo/S,self.hi/S]
 def data(self):return [str(self.lo),str(self.hi)]
 def __repr__(self):return str(self.floats())

def asr(x):return x if isinstance(x,R) else R(x)

def _log_unit(m):
 # m in [1,2], z in [0,1/3]. Positive tail bounded geometrically.
 z=(m-1)/(m+1);z2=z.sq();term=z;out=R(0)
 N=BITS//3+15
 for j in range(N):
  out=out+term/(2*j+1);term=term*z2
 tail=2*term/((2*N+1)*(1-z2))
 return 2*out+R(0,max(0,tail.hi),raw=True)

@lru_cache(None)
def ln2():return _log_unit(R(2))

def _log_endpoint(x):
 if x<=0:raise ArithmeticError('log of nonpositive enclosure')
 b=x.bit_length()-1;k=b-BITS
 m=R(Fraction(x,1<<b))
 return _log_unit(m)+k*ln2()

def log(x):
 x=asr(x)
 if x.lo<=0:raise ArithmeticError('log enclosure includes zero')
 a=_log_endpoint(x.lo);b=_log_endpoint(x.hi)
 return R(a.lo,b.hi,raw=True)

def h(x):
 """Binary entropy range for any interval intersected with [0,1]."""
 x=asr(x).intersection(R(0,1))
 def point(v):
  if v==0 or v==S:return R(0)
  p=R(v,v,raw=True)
  return -p*log(p)-(1-p)*log(1-p)
 a=point(x.lo);b=point(x.hi)
 lo=min(a.lo,b.lo)
 hi=ln2().hi if x.lo*2<=S<=x.hi*2 else max(a.hi,b.hi)
 return R(max(0,lo),hi,raw=True)

def atan_small(q):
 z=R(q);z2=z.sq();term=z;out=R(0);N=BITS//4+15
 for j in range(N):
  out=out+(term/(2*j+1) if j%2==0 else -term/(2*j+1));term=term*z2
 e=(term/(2*N+1)).hi
 return out+R(-e,e,raw=True)

@lru_cache(None)
def pi():return 16*atan_small(Fraction(1,5))-4*atan_small(Fraction(1,239))

def sincos_fraction(q):
 q=Fraction(q)%1
 if q==0:return R(0),R(1)
 if q==Fraction(1,4):return R(1),R(0)
 if q==Fraction(1,2):return R(0),R(-1)
 if q==Fraction(3,4):return R(-1),R(0)
 if q>Fraction(1,2):q-=1
 x=2*pi()*R(q);x2=x.sq();N=BITS//4+15
 ts=x;tc=R(1);ss=R(0);cc=R(0)
 for j in range(N):
  ss=ss+ts;cc=cc+tc
  ts=-ts*x2/((2*j+2)*(2*j+3))
  tc=-tc*x2/((2*j+1)*(2*j+2))
 # Lagrange bounds since |x| <= pi < 4.
 es=R(Fraction(4**(2*N+1),factorial(2*N+1))).hi
 ec=R(Fraction(4**(2*N),factorial(2*N))).hi
 return ss+R(-es,es,raw=True),cc+R(-ec,ec,raw=True)

class C:
 __slots__=('re','im')
 def __init__(self,re=0,im=0):
  if isinstance(re,C):self.re=re.re;self.im=re.im
  else:self.re=asr(re);self.im=asr(im)
 def __add__(self,o):o=asc(o);return C(self.re+o.re,self.im+o.im)
 __radd__=__add__
 def __neg__(self):return C(-self.re,-self.im)
 def __sub__(self,o):return self+-asc(o)
 def __rsub__(self,o):return asc(o)+-self
 def __mul__(self,o):
  if isinstance(o,(R,int,Fraction)):return C(self.re*o,self.im*o)
  o=asc(o);return C(self.re*o.re-self.im*o.im,self.re*o.im+self.im*o.re)
 __rmul__=__mul__
 def __truediv__(self,o):
  if isinstance(o,(R,int,Fraction)):return self*asr(o).inv()
  o=asc(o);return self*o.conj()/(o.re.sq()+o.im.sq())
 def conj(self):return C(self.re,-self.im)
 def abs2(self):return self.re.sq()+self.im.sq()
 def approx(self):return complex(sum(self.re.floats())/2,sum(self.im.floats())/2)

def asc(x):return x if isinstance(x,C) else C(x)
@lru_cache(None)
def phase(q):
 sn,cs=sincos_fraction(q);return C(cs,sn)

def jmul(x,y):return (x[0]*y[0],x[0]*y[1]+x[1]*y[0],x[0]*y[2]+x[1]*y[1]+x[2]*y[0])
def jinv(q):
 r=q[0].inv();return (r,-q[1]*r*r,q[1]*q[1]*r*r*r-q[2]*r*r)
def jadd(x,y):return tuple(x[i]+y[i] for i in range(3))
def jneg(x):return tuple(-v for v in x)
def jsub(x,y):return jadd(x,jneg(y))
def jconj(x):return tuple(v.conj() for v in x)
