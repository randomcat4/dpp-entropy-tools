"""Rational elementary operations for author certificates, not an independent review."""
from fractions import Fraction as F
from functools import lru_cache
from math import isqrt

def ivadd(a,b): return a[0]+b[0],a[1]+b[1]
def ivscale(c,a):
    return (c*a[0],c*a[1]) if c>=0 else (c*a[1],c*a[0])
def ivmul(a,b):
    z=[x*y for x in a for y in b];return min(z),max(z)
def ivsum(xs):
    a=(F(0),F(0))
    for x in xs:a=ivadd(a,x)
    return a

def qrange(coef,l,r):
    c0,c1,c2=coef
    v=[c0+c1*l+c2*l*l,c0+c1*r+c2*r*r]
    if c2:
        z=-c1/(2*c2)
        if l<z<r:v.append(c0+c1*z+c2*z*z)
    return min(v),max(v)
def at(p,x):return p[0]+p[1]*x+p[2]*x*x

def dyadic_interval(iv,bits=112):
    d=1<<bits
    return F((iv[0]*d).__floor__(),d),F((iv[1]*d).__ceil__(),d)

def roundpoint(x,bits=56):
    d=1<<bits;return F((x*d).__floor__(),d),F((x*d).__ceil__(),d)

def unitlog(x,N=28):
    # Valid for x>=1; intended for 1<=x<=2.
    z=(x-1)/(x+1);zz=z*z;term=z;sm=F(0)
    for j in range(N):sm+=term/(2*j+1);term*=zz
    tail=2*term/((2*N+1)*(1-zz))
    return 2*sm,2*sm+tail
LOG2=unitlog(F(2))

@lru_cache(maxsize=200000)
def logiv(x):
    x=F(x);assert x>0
    k=0;m=x
    while m<1:m*=2;k-=1
    while m>2:m/=2;k+=1
    ml,mr=roundpoint(m)
    lo=unitlog(ml)[0];hi=unitlog(mr)[1]
    return dyadic_interval(ivadd((lo,hi),ivscale(F(k),LOG2)))

@lru_cache(maxsize=200000)
def lamiv(x):
    x=F(x);assert x>0
    if F(1,2)<=x<=2:
        # lambda = 2/(q+1)*sum z^(2j)/(2j+1). No division by q-1.
        lo,hi=roundpoint(x)
        def direct(q):
            z=(q-1)/(q+1);zz=z*z;term=F(1);sm=F(0);N=28
            for j in range(N):sm+=term/(2*j+1);term*=zz
            tail=term/((2*N+1)*(1-zz))
            return 2*sm/(q+1),2*(sm+tail)/(q+1)
        return dyadic_interval((direct(hi)[0],direct(lo)[1]))
    return dyadic_interval(ivscale(1/(x-1),logiv(x)))

def disp(iv,n=16):
    d=10**n;lo=(iv[0]*d).__floor__();hi=(iv[1]*d).__ceil__()
    def fmt(v):return ('-' if v<0 else '')+str(abs(v)//d)+'.'+str(abs(v)%d).zfill(n)
    return '['+fmt(lo)+', '+fmt(hi)+']'

def entropy_iv(ps):
    return ivsum(ivscale(-p,logiv(p)) for p in ps if p)

def fraction_json(x):return str(x.numerator)+'/'+str(x.denominator)
