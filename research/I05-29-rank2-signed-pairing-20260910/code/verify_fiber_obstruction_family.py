#!/usr/bin/env python3
"""PR80 author-side exact checks. No independent review or novelty claim.

All signs use Fraction endpoints and a rational atanh remainder, followed by
outward dyadic rounding. Decimal endpoints printed below are also outward.
The continuum theorem is proved in ADDENDUM_CROSS_FIBER_OBSTRUCTION.md;
this script checks its algebra and finite examples, not a sampled substitute.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations
import platform
import sympy as sp
import time

Q = sp.Rational
START = time.perf_counter()

def ff(x):
    x = sp.cancel(x)
    return F(int(sp.numer(x)), int(sp.denom(x)))

def add(a, b):
    return a[0] + b[0], a[1] + b[1]

def scale(c, a):
    c = F(c)
    return (c*a[0], c*a[1]) if c >= 0 else (c*a[1], c*a[0])

def rounded(a, bits=96):
    d = 1 << bits
    return F((a[0]*d).__floor__(), d), F((a[1]*d).__ceil__(), d)

def log_unit(x, n=40):
    assert 1 <= x <= 2
    z = (x-1)/(x+1)
    z2 = z*z
    term, total = z, F(0)
    for j in range(n):
        total += term/F(2*j+1)
        term *= z2
    tail = 2*term/F(2*n+1)/(1-z2)
    return 2*total, 2*total+tail

LOG2 = log_unit(F(2))

@lru_cache(None)
def log_iv(x):
    x = F(x)
    assert x > 0
    k = 0
    while x < 1:
        x *= 2
        k -= 1
    while x > 2:
        x /= 2
        k += 1
    return rounded(add(log_unit(x), scale(k, LOG2)))

def disp(iv, n=12):
    d = 10**n
    lo, hi = (iv[0]*d).__floor__(), (iv[1]*d).__ceil__()
    def fmt(v):
        return ('-' if v < 0 else '') + str(abs(v)//d) + '.' + str(abs(v)%d).zfill(n)
    return '['+fmt(lo)+', '+fmt(hi)+']'

def em(K, mask):
    return K-sp.diag(*[1-((mask>>i)&1) for i in range(K.rows)])

def prob(K, mask):
    return (-1)**(K.rows-mask.bit_count())*em(K, mask).det()

def pd(K):
    # Sylvester criterion for these exact real symmetric matrices.
    assert K == K.T
    return all(K[:j,:j].det() > 0 for j in range(1, K.rows+1))

def reconstruct(A, C, U, V, smax):
    B = U*V.T
    assert B.rank() == 2
    for K in (A, sp.eye(A.rows)-A, C, sp.eye(C.rows)-C,
              C-smax*B.T*A.inv()*B,
              sp.eye(C.rows)-C-smax*B.T*(sp.eye(A.rows)-A).inv()*B):
        assert pd(K)
    pa = [ff(prob(A,i)) for i in range(1<<A.rows)]
    pc = [ff(prob(C,j)) for j in range(1<<C.rows)]
    assert all(x > 0 for x in pa+pc) and sum(pa) == sum(pc) == 1
    GA = [U.T*em(A,i).inv()*U for i in range(len(pa))]
    GC = [V.T*em(C,j).inv()*V for j in range(len(pc))]
    ab = {(i,j):(ff(sp.trace(GA[i]*GC[j])), ff(GA[i].det()*GC[j].det()))
          for i in range(len(pa)) for j in range(len(pc))}
    for i in range(len(pa)):
        for c in (0,1):
            assert sum(pc[j]*ab[i,j][c] for j in range(len(pc))) == 0
    for j in range(len(pc)):
        for c in (0,1):
            assert sum(pa[i]*ab[i,j][c] for i in range(len(pa))) == 0
    return pa,pc,ab

def point(pa, pc, ab, s):
    vals = {}
    for ij,(a,b) in ab.items():
        u, y = -s*a+s*s*b, s*s*b
        q = 1+u
        assert q > 0
        vals[ij] = q,u,y
    def g(z):
        q,u,y = z
        return add((4*(u+y)**2/q,)*2, scale(2*(u+5*y),log_iv(q)))
    gi = {ij:g(z) for ij,z in vals.items()}
    lf = [sum_ivs(scale(pc[j],gi[i,j]) for j in range(len(pc))) for i in range(len(pa))]
    rf = [sum_ivs(scale(pa[i],gi[i,j]) for i in range(len(pa))) for j in range(len(pc))]
    full = sum_ivs(scale(pa[i],lf[i]) for i in range(len(pa)))
    assert full == sum_ivs(scale(pc[j],rf[j]) for j in range(len(pc)))
    return vals,gi,lf,rf,full

def sum_ivs(it):
    out = (F(0), F(0))
    for a in it:
        out = add(out,a)
    return out

def secant(q):
    return (F(1),F(1)) if q == 1 else scale(1/(q-1),log_iv(q))

def window_bound(zs,ws):
    qmin,qmax = min(z[0] for z in zs),max(z[0] for z in zs)
    lp,lm = secant(qmin),secant(qmax)
    ez = sum(w*u*(u+5*y) for w,(q,u,y) in zip(ws,zs))
    eabs = sum(w*abs(u*(u+5*y)) for w,(q,u,y) in zip(ws,zs))
    ev = sum(w*(u+y)**2 for w,(q,u,y) in zip(ws,zs))
    # 2c Ez - 2delta E|z| = lambda(qmin)(Ez-E|z|) + lambda(qmax)(Ez+E|z|).
    return sum_ivs([(4*ev/qmax,)*2,scale(ez-eabs,lp),scale(ez+eabs,lm)])

# Reconstruct the exact public PR58 s=9/10 input, not a substitute fixture.
A = sp.Matrix([[Q(219,500),-Q(47,1000),Q(73,1000)],
               [-Q(47,1000),Q(461,1000),Q(23,1000)],
               [Q(73,1000),Q(23,1000),Q(43,100)]])
C = sp.Matrix([[Q(231,500),Q(1,50),-Q(49,1000)],
               [Q(1,50),Q(43,100),Q(11,200)],
               [-Q(49,1000),Q(11,200),Q(3,5)]])
U = sp.Matrix([[Q(7,40),-Q(22,125)],[Q(339,1000),Q(13,250)],
               [Q(229,500),-Q(231,500)]])
V = sp.Matrix([[Q(141,200),Q(981,1000)],[-Q(343,1000),Q(113,250)],
               [Q(187,250),Q(577,1000)]])
pa,pc,ab = reconstruct(A,C,U,V,Q(9,10))
zs,gi,lf,rf,full = point(pa,pc,ab,F(9,10))
assert all(x[0] > 0 for x in lf+rf)
assert [ij for ij,iv in gi.items() if iv[1]<0] == [(0,6),(1,5),(2,5),(3,0)]
counts = []
for left in (True,False):
    neg,pos,zero_du = 0,0,0
    for f in range(8):
        for i,j in combinations(range(8),2):
            q,u,y = zs[f,i] if left else zs[i,f]
            Qp,up,yp = zs[f,j] if left else zs[j,f]
            du = u-up
            if not du:
                zero_du += 1
                continue
            ratio = (y-yp)/du
            L = scale(1/du,(log_iv(q)[0]-log_iv(Qp)[1],log_iv(q)[1]-log_iv(Qp)[0]))
            rat = 2*(1+ratio*ratio)/(q+Qp)+4*ratio/(q*Qp)
            fi = add((rat,rat),scale(1+5*ratio,L))
            assert fi[1] < 0 or fi[0] > 0, 'undecided sign'
            neg += fi[1] < 0
            pos += fi[0] > 0
    assert neg+pos+zero_du == 224
    counts.append(neg)
assert counts == [75,66]
wl = [window_bound([zs[i,j] for j in range(8)],pc) for i in range(8)]
wr = [window_bound([zs[i,j] for i in range(8)],pa) for j in range(8)]
assert all(iv[0] > 0 for iv in wl+wr)
print('FROZEN s=9/10: all 64 events, both sets of 224 pairs checked')
print('negative ratio-cone counts:',counts)
print('negative complete event integrands:',[ij for ij,iv in gi.items() if iv[1]<0])
print('min left/right window bounds:',disp(min(wl)),disp(min(wr)))
print('full t^2 I\'\':',disp(full))

# Exact symbolic derivation of the continuum family's three Gram moments.
r,z = sp.symbols('r z', positive=True)
I,X,H = sp.eye(2),sp.Matrix([[0,1],[1,0]]),sp.Matrix([[1,1],[1,-1]])
A,C = I/2,I/2+r*X
Ma,Mab,Mb = sp.Integer(0),sp.Integer(0),sp.Integer(0)
for i in range(4):
    D = -r/2*H.T*em(A,i).inv()*H
    for j in range(4):
        p0 = prob(C,j)
        qp = sp.Poly(sp.expand(prob(C+z*D,j)/p0),z)
        a,b = -qp.nth(1),qp.nth(2)
        Ma += p0*a*a/4
        Mab += p0*a*b/4
        Mb += p0*b*b/4
assert sp.simplify(Mab) == 0
assert sp.simplify(Ma-16*r*r*(1+12*r*r)/(1-16*r**4)) == 0
assert sp.simplify(Mb-256*r**4/(1-16*r**4)) == 0
assert sp.simplify(Mb/Ma-16*r*r/(1+12*r*r)) == 0
assert sp.simplify((sp.Rational(4,19)-Mb/Ma)+4*(8*r-1)*(8*r+1)/(19*(12*r*r+1))) == 0
assert log_iv(F(5))[1] < F(81,50)
assert log_iv(F(7,3))[0] > F(5,6)
assert F(12,7)+F(5,4)-F(22,7)*F(4,19) == F(175,76)
print('CONTINUUM ALGEBRA: Eab=0; Ma=16r^2(1+12r^2)/(1-16r^4); Mb/Ma=16r^2/(1+12r^2)')
print('LOG CONSTANTS: log(5)<81/50; log(7/3)>5/6; both rationally certified')
print('ANALYTIC LOWER BOUND: H\'\'(t) <= -(700/19) r^2 t^2, 0<r<=1/8, |t|<=1')

# Finite rational member, full conditional averages, including the bad fiber.
rr=Q(1,8)
pa,pc,ab = reconstruct(I/2,I/2+rr*X,H/4,I,Q(1))
zs,gi,lf,rf,full = point(pa,pc,ab,F(1,2))
badformula = scale(-16*ff(rr)**2,log_iv((1+4*ff(rr)**2)/(1-4*ff(rr)**2)))
assert lf[1][1]<0 and full[0]>0
assert max(lf[1][0],badformula[0]) <= min(lf[1][1],badformula[1])
for j in range(4):
    q,u,y=zs[1,j]
    assert u+y == 0
print('RATIONAL r=1/8: strict legal on |t|<=1; full left fibers:')
for i,iv in enumerate(lf): print(i,disp(iv))
print('negative-fiber exact form: -(1/4) log(17/15)')
print('global t^2 I\'\':',disp(full))

# A fully correlated rational obstruction; no diagonal marginal hypothesis.
AA=sp.Matrix([[Q(1,2),Q(3,8)],[Q(3,8),Q(1,2)]])
HH=sp.Matrix([[1,2],[2,-1]])
assert HH.T*em(AA,1).inv()*HH == 8*X
k=Q(1,16); rr=4*k*k
assert Q(1,2)-44*k*k>0
pa,pc,ab = reconstruct(AA,I/2+rr*X,k*HH,I,Q(1))
zs,gi,lf,rf,full = point(pa,pc,ab,F(1,2))
assert lf[1][1]<0 and full[0]>0
for j in range(4):
    q,u,y=zs[1,j]
    assert u+y==0
print('BOTH BLOCKS CORRELATED: A12=3/8, C12=1/64, B=(1/16)[[1,2],[2,-1]]')
print('strict legal on |t|<=1; negative fiber:',disp(lf[1],16))
print('full t^2 I\'\' at s=1/2:',disp(full,16))
print('PASS: author-side exact checks only; continuum proof and novelty require separate review')
print('Python',platform.python_version(),'SymPy',sp.__version__)
print('Elapsed seconds:',format(time.perf_counter()-START,'.3f'))
