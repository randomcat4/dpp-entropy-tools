#!/usr/bin/env python3
"""Author-side exact finite certificate for the accompanying continuum proof.

Python standard library only. Every comparison deciding a claim is rational.
Complete laws are obtained from principal minors and Mobius inclusion-exclusion,
then independently cross-checked against event Schur coefficients. Three entire
intervals are certified by quadratic extrema, not by temporal sampling.
No independent-review or novelty status is implied by executing this code.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import permutations, combinations
from pathlib import Path
import csv
import json
import platform
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
START = time.perf_counter()
CHECKS = 0

def require(ok: bool, message: str) -> None:
    global CHECKS
    CHECKS += 1
    if not ok:
        raise AssertionError(message)

def transpose(a):
    return [list(x) for x in zip(*a)]

def mm(a, b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]

def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]

def sub(a, b):
    return [[x-y for x,y in zip(ar,br)] for ar,br in zip(a,b)]

def determinant(a):
    n = len(a)
    out = F(0)
    for perm in permutations(range(n)):
        term = F((-1)**sum(perm[i] > perm[j] for i in range(n) for j in range(i+1,n)))
        for i,j in enumerate(perm):
            term *= a[i][j]
        out += term
    return out

def inverse(a):
    n = len(a)
    z = [list(row)+eye(n)[i] for i,row in enumerate(a)]
    for j in range(n):
        k = next((k for k in range(j,n) if z[k][j]), None)
        require(k is not None, 'singular exact event matrix')
        z[j], z[k] = z[k], z[j]
        pivot = z[j][j]
        z[j] = [x/pivot for x in z[j]]
        for i in range(n):
            if i != j:
                c = z[i][j]
                z[i] = [x-c*y for x,y in zip(z[i],z[j])]
    return [row[n:] for row in z]

def pd(a):
    return a == transpose(a) and all(determinant([r[:k] for r in a[:k]]) > 0
                                    for k in range(1,len(a)+1))

def event_matrix(a, mask):
    return [[x-F(i == j and not ((mask >> i) & 1)) for j,x in enumerate(row)]
            for i,row in enumerate(a)]

def marginal(a):
    n = len(a)
    dets = []
    for mask in range(1 << n):
        inds = [i for i in range(n) if (mask >> i) & 1]
        dets.append(determinant([[a[i][j] for j in inds] for i in inds]))
    return [sum(((-1)**(t.bit_count()-s.bit_count())*dets[t]
                 for t in range(1 << n) if t & s == s), F(0))
            for s in range(1 << n)]

def poly_value(p, x):
    ans = F(0)
    for c in reversed(p):
        ans = ans*x+c
    return ans

def qranges(p, left, right):
    c0,c1,c2 = p
    points = [left,right]
    if c2:
        vertex = -c1/(2*c2)
        if left < vertex < right:
            points.append(vertex)
    vals = [poly_value(p,x) for x in points]
    return min(vals),max(vals)

def dec_interval(lo, hi=None, digits=15):
    hi = lo if hi is None else hi
    scale = 10**digits
    low = (lo*scale).__floor__()
    high = (hi*scale).__ceil__()
    def fmt(z):
        return ('-' if z < 0 else '')+str(abs(z)//scale)+'.'+str(abs(z)%scale).zfill(digits)
    return '['+fmt(low)+', '+fmt(high)+']'

def log_unit(x, n=40):
    require(F(1) <= x <= F(2), 'log range reduction')
    z = (x-1)/(x+1)
    term,total = z,F(0)
    for k in range(n):
        total += term/F(2*k+1)
        term *= z*z
    tail = 2*term/F(2*n+1)/(1-z*z)
    return 2*total,2*total+tail

LOG2 = log_unit(F(2))

def log_interval(x):
    require(x > 0, 'log domain')
    k = 0
    while x < 1:
        x *= 2
        k -= 1
    while x > 2:
        x /= 2
        k += 1
    lo,hi = log_unit(x)
    return ((lo+k*LOG2[0], hi+k*LOG2[1]) if k >= 0
            else (lo+k*LOG2[1], hi+k*LOG2[0]))

source = json.loads((ROOT/'input/fixture.json').read_text())
A,C,U,V = ([[F(x) for x in row] for row in source[k]] for k in ('A','C','U','V'))
B = mm(U,transpose(V))
I = eye(3)
for name,a0 in [('A',A),('C',C)]:
    require(pd(sub(a0,[[F(3,10)*x for x in row] for row in I])), name+' lower spectral margin')
    require(pd(sub([[F(7,10)*x for x in row] for row in I],a0)), name+' upper spectral margin')
require(determinant(B) == 0, 'cross rank at most two')
require(determinant([r[:2] for r in B[:2]]) != 0, 'cross rank at least two')
require(all(x != 0 for row in B for x in row), 'all nine cross entries active')
require(all(A[i][j] and C[i][j] for i in range(3) for j in range(i)), 'both marginal graphs complete')
pa,pc = marginal(A),marginal(C)
require(sum(pa) == sum(pc) == 1 and min(pa+pc) > 0, 'full marginal laws')

# Independent complete-event construction from every principal minor of K(t).
# Each nonzero matrix entry is exactly a constant times t^0 or t^1.
K = [A[i]+B[i] for i in range(3)]+[transpose(B)[i]+C[i] for i in range(3)]
principal = []
for mask in range(64):
    inds = [i for i in range(6) if (mask >> i) & 1]
    p = [F(0)]*7
    for perm in permutations(inds):
        inversions = sum(perm[i] > perm[j] for i in range(len(perm)) for j in range(i+1,len(perm)))
        term,degree = F((-1)**inversions),0
        for i,j in zip(inds,perm):
            term *= K[i][j]
            degree += (i < 3) != (j < 3)
        p[degree] += term
    principal.append(p)
law = []
for mask in range(64):
    p = [sum(((-1)**(sup.bit_count()-mask.bit_count())*principal[sup][k]
              for sup in range(64) if sup & mask == mask), F(0)) for k in range(7)]
    require(all(p[k] == 0 for k in (1,3,5,6)), 'even quadratic-in-s full event')
    law.append((p[0],p[2],p[4]))

GA = [mm(mm(transpose(U),inverse(event_matrix(A,j))),U) for j in range(8)]
GC = [mm(mm(transpose(V),inverse(event_matrix(C,j))),V) for j in range(8)]
data = []
for i in range(8):
    for j in range(8):
        p0,p1,p2 = law[i+8*j]
        mu = pa[i]*pc[j]
        require(p0 == mu, 'decoupled complete product law')
        a,b = -p1/mu,p2/mu
        prod = mm(GA[i],GC[j])
        require(a == prod[0][0]+prod[1][1], 'Mobius versus Schur first coefficient')
        require(b == determinant(GA[i])*determinant(GC[j]), 'Mobius versus Schur second coefficient')
        data.append((i,j,mu,a,b))
for i in range(8):
    for column in (3,4):
        require(sum(pc[j]*data[8*i+j][column] for j in range(8)) == 0, 'right fiber cancellation')
        require(sum(pa[j]*data[8*j+i][column] for j in range(8)) == 0, 'left fiber cancellation')

EPS = F(1,10**6)
require(max(abs(d[3]) for d in data)+EPS < 2, 'coefficient a neighborhood bound')
require(max(abs(d[4]) for d in data)+EPS < 1, 'coefficient b neighborhood bound')
# Columns: interval, retained events, likelihood bounds, moment bounds, negative budget, lambda bounds.
phases = [
    (F(0),F(9,10),False,F(1,30),F(3),F(109,200),F(109,200),F(29,250),F(1,2),F(18,5)),
    (F(9,10),F(99,100),False,F(1,400),F(31,10),F(83,100),F(49,50),F(27,200),F(1,2),F(61,10)),
    (F(99,100),F(1),True,F(1,50),F(31,10),F(89,100),F(109,100),F(14,125),F(1,2),F(41,10)),
]
records = []
for k,(left,right,omit,qlo,qhi,evlo,ezlo,nhi,ll,lh) in enumerate(phases,1):
    group = [d for d in data if not (omit and d[:2] == (7,7))]
    ma = sum(mu*a*a for _,_,mu,a,b in group)
    mab = sum(mu*a*b for _,_,mu,a,b in group)
    mb = sum(mu*b*b for _,_,mu,a,b in group)
    actual_qlo = min(qranges((1,-a,b),left,right)[0] for _,_,mu,a,b in group)
    actual_qhi = max(qranges((1,-a,b),left,right)[1] for _,_,mu,a,b in group)
    ev = qranges((ma,-4*mab,4*mb),left,right)[0]
    ez = qranges((ma,-7*mab,6*mb),left,right)[0]
    nn = sum(mu*max(F(0),qranges((-a*a,7*a*b,-6*b*b),left,right)[1])
             for _,_,mu,a,b in group)
    require(actual_qlo-2*EPS > qlo, 'robust lower likelihood, phase '+str(k))
    require(actual_qhi+2*EPS < qhi, 'robust upper likelihood, phase '+str(k))
    require(ev-280*EPS > evlo, 'robust Fisher numerator moment, phase '+str(k))
    require(ez-421*EPS > ezlo, 'robust signed moment, phase '+str(k))
    require(nn+421*EPS < nhi, 'robust negative budget, phase '+str(k))
    lower = 4*evlo/qhi+2*ll*ezlo-2*(lh-ll)*nhi
    require(lower > F(1,2), 'whole-interval normalized curvature margin')
    records.append(dict(phase=k,left=str(left),right=str(right),retained=len(group),
        exact_q_min=str(actual_qlo),exact_q_max=str(actual_qhi),exact_v2_min=str(ev),
        exact_z_min=str(ez),exact_negative_budget=str(nn),certified_gamma_lower=str(lower)))
    print('PHASE',k,'s in',str(left),str(right),'retained events',len(group))
    for name,value in [('qmin',actual_qlo),('qmax',actual_qhi),('Ev2_min',ev),('Ez_min',ez),('N_upper',nn)]:
        print(' ',name,dec_interval(value))
    print('  robust Gamma lower:',lower,dec_interval(lower))

# Six scalar logarithm comparisons certify the fixed lambda windows and rare term.
for x,lower,upper in [(F(3),F(1),None),(F(30),None,F(87,25)),
                      (F(31,10),F(21,20),None),(F(400),None,F(6)),
                      (F(50),None,F(4)),(F(300),None,F(6))]:
    iv = log_interval(x)
    require(lower is None or iv[0] > lower, 'lower logarithm comparison')
    require(upper is None or iv[1] < upper, 'upper logarithm comparison')
require(F(400,399)*6 < F(61,10), 'second lambda upper')
require(F(50,49)*4 < F(41,10), 'third lambda upper')

_,_,rare_mu,rare_a,rare_b = data[-1]
rare_q = (F(1),-rare_a,rare_b)
require(rare_b-EPS > 0, 'rare quadratic stays convex')
require(poly_value(rare_q,F(1))+2*EPS < 0, 'root stays below one')
require(rare_a-2*rare_b-3*EPS > F(1,4), 'uniform rare derivative reserve')
rare_z_min,rare_z_max = qranges((rare_a**2,-7*rare_a*rare_b,6*rare_b**2),F(99,100),F(1))
require(max(abs(rare_z_min),abs(rare_z_max))+37*EPS < 3, 'rare signed log coefficient')
require(poly_value(rare_q,F(99,100))+2*EPS < F(1,300), 'rare small likelihood')
require(F(1,4)-F(36,299) == F(155,1196), 'rare analytic pole coefficient')
print('RARE atom (7,7): mu=',rare_mu,'a=',rare_a,'b=',rare_b)
print('  q(1)=',poly_value(rare_q,F(1)),dec_interval(poly_value(rare_q,F(1))))
print('  phi_rare >= 155/(1196 q_rare) on 99/100 <= s < s_star')

# Exact monotone root isolation, not curvature sampling.
def bisect_root(f,left,right,steps=80):
    require(f(left) > 0 and f(right) < 0, 'root bracket signs')
    for _ in range(steps):
        midpoint = (left+right)/2
        if f(midpoint) > 0:
            left = midpoint
        else:
            right = midpoint
    return left,right
sroot = bisect_root(lambda s:poly_value(rare_q,s),F(99,100),F(1))
troot = bisect_root(lambda t:poly_value(rare_q,t*t),F(99,100),F(1))
print('MAXIMAL squared endpoint s_star:',dec_interval(*sroot,digits=18))
print('MAXIMAL physical endpoint t_star:',dec_interval(*troot,digits=18))

# Quantitative matrix-factor box: |Delta(A,C,U,V)_ij| <= 10^-12.
# Frobenius bounds imply U0<9/10, V0<19/10 and give room for factor perturbations.
eta = F(1,10**12)
require(sum(x*x for row in U for x in row) < F(81,100), 'U Frobenius margin')
require(sum(x*x for row in V for x in row) < F(361,100), 'V Frobenius margin')
require(F(3,10)-3*eta > F(1,4), 'spectral margin throughout matrix box')
require(F(9,10)+3*eta < 1 and F(19,10)+3*eta < 2, 'factor norm bounds throughout box')
require(9*eta < EPS and 4224*eta < EPS and 270336*eta < EPS, 'matrix box maps inside coefficient box')
require(min(abs(x) for row in B for x in row) > 9*eta, 'cross entries stay nonzero')
require(min(abs(M[i][j]) for M in (A,C) for i in range(3) for j in range(i)) > eta,
        'both marginal blocks stay correlated')
for frame in (U,V):
    minor = determinant([r[:2] for r in frame[:2]])
    require(abs(minor) > 4*eta+2*eta*eta, 'two-column factor rank stays two')

# This input is outside the listed full-fiber diagonal-anchor test on either orientation.
for ref,direction in [(C,mm(mm(transpose(B),inverse(A)),B)),
                      (A,mm(mm(B,inverse(C)),transpose(B)))]:
    off = [(0,1),(0,2),(1,2)]
    require(any(ref[i][j]*direction[k][l] != ref[k][l]*direction[i][j]
                for (i,j),(k,l) in combinations(off,2)), 'full-fiber PSD rank-two direction has no diagonal anchor')

out = ROOT/'output'
out.mkdir(exist_ok=True)
with (out/'complete_event_coefficients.csv').open('w',newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['left_mask','right_mask','mu','a','b'])
    writer.writerows([[i,j,str(mu),str(a),str(b)] for i,j,mu,a,b in data])
(out/'rational_certificate.json').write_text(json.dumps(dict(
    status='AUTHOR_EXACT_CHECK_PENDING_INDEPENDENT_REVIEW',
    input='input/fixture.json',method='principal-minor Mobius law; exact quadratic extrema; rational log tails',
    coefficient_radius=str(EPS),matrix_factor_radius=str(eta),phases=records,
    rare=dict(mu=str(rare_mu),a=str(rare_a),b=str(rare_b),pole_lower='155/1196'),
    s_star_interval=[str(x) for x in sroot],t_star_interval=[str(x) for x in troot]),indent=2)+'\n')
print('CONCLUSION: H(t)+t^4/24 is concave on the entire maximal legal closed chord.')
print('SCOPE: fixed dense correlated 3+3 source, coefficient radius 10^-6, factor-entry box radius 10^-12.')
print('STATUS: AUTHOR PROOF / AUTHOR EXACT CHECK; PENDING_REVIEW; novelty NOT_ASSESSED.')
print('CHECKS:',CHECKS,'Python:',platform.python_version(),'elapsed seconds:',format(time.perf_counter()-START,'.6f'))
