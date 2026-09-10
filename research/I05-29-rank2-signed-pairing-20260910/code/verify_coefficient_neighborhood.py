#!/usr/bin/env python3
"""Author exact membership check for the correlated continuum theorem."""
import contextlib
import io
with contextlib.redirect_stdout(io.StringIO()):
    from verify_fiber_obstruction_family import (
        sp, Q, F, reconstruct, point, log_iv, disp
    )

I = sp.eye(2)
X = sp.Matrix([[0,1],[1,0]])
R = sp.Matrix([[1,1],[1,-1]])
A0, C0, B0 = I/2, I/2+Q(1,8)*X, R/4
base = reconstruct(A0,C0,B0,I,Q(1))
new = reconstruct(A0+Q(1,100000)*X,C0,B0,I,Q(1))
delta = F(1,40000)
dpa = max(abs(x-y) for x,y in zip(new[0],base[0]))
dpc = max(abs(x-y) for x,y in zip(new[1],base[1]))
da = max(abs(new[2][ij][0]-base[2][ij][0]) for ij in base[2])
db = max(abs(new[2][ij][1]-base[2][ij][1]) for ij in base[2])
assert max(dpa,dpc,da,db) < delta
assert dpa == F(1,10**10) and dpc == 0
assert da < F(18823624,10**12)
assert db < F(107,10**12)
assert log_iv(F(6))[0] > 1 and log_iv(F(6))[1] < F(15,8)
L, M = F(41052,25), F(2976,25)
assert L+8*M == F(12972,5)
assert F(1,4)*(L+4*M) == F(13239,25)
gamma_lower = F(175,304)-(L+8*M)*delta
assert gamma_lower == F(242629,475000) and gamma_lower > F(1,2)
bad_upper = -F(1,34)+F(1,4)*(L+4*M)*delta
assert bad_upper == -F(274937,17000000) and bad_upper < 0
schur_lower=Q(3,8)-Q(1,8)/(Q(1,2)-Q(1,100000))
assert schur_lower > 0
vals,gi,lf,rf,full = point(*new,F(1,2))
assert lf[1][1] < 0 and full[0] > 0
print('EXPLICIT CORRELATED KERNEL:')
print('A=[[1/2,1/100000],[1/100000,1/2]]; C=[[1/2,1/8],[1/8,1/2]]')
print('B=(1/4)[[1,1],[1,-1]]; strict legal on |t|<=1')
print('coefficient radius delta=1/40000; exact rational membership PASS')
print('max marginal-weight changes:',dpa,dpc)
print('max a difference:',disp((da,da)))
print('max b difference:',disp((db,db),16))
print('uniform normalized-curvature lower bound:',gamma_lower,'>1/2')
print('uniform bad-fiber upper bound at s=1/2:',bad_upper,'<0')
print('direct bad-fiber enclosure at s=1/2:',disp(lf[1],16))
print('direct full t^2 I\'\' enclosure at s=1/2:',disp(full,16))
print('PASS: exact coefficient membership, not a grid; continuum proof is author-only/PENDING_REVIEW')
