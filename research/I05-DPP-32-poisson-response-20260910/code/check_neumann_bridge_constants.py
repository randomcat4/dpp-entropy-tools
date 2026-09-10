#!/usr/bin/env python3
from fractions import Fraction as F

# Prove log(1024/81) < 127/50 by the positive atanh series with a geometric tail.
x=F(1024,81)
y=(x-1)/(x+1)
N=20
S=sum(F(2)*y**(2*k+1)/F(2*k+1) for k in range(N+1))
tail=F(2)*y**(2*N+3)/F(2*N+3)/(1-y*y)
log_upper=S+tail
assert log_upper < F(127,50)

epsilon=F(81,1024)
beta=F(2,3)
gamma=F(19,25)
Cgrad=F(17618609,99532800)
b1=F(127,25)
b2=F(4096,81)+F(254,25)
bt1=F(381,400)+F(112,81)

assert b1 == 2*F(127,50)
assert b2 == 4/epsilon + 4*F(127,50)
assert bt1 == F(3,8)*F(127,50)+F(7,64)/epsilon

def tail_budget(m):
    e01=beta**m*b1
    e02=gamma**m*b2
    um2=b2*(1-gamma**m)/(1-gamma)
    e11=beta**m*(bt1+Cgrad*um2)
    E=3*e01+F(1,15)*e02+F(11,20)*e11
    return e01,e02,e11,E

checks=[(32,F(717,10**6)),(36,F(227,10**6)),(40,F(73,10**6))]
for m,cap in checks:
    e01,e02,e11,E=tail_budget(m)
    assert E < cap
    print(m, 'E12=', E, 'decimal=', float(E), 'cap=', cap)

print('log_upper=', log_upper, 'decimal=', float(log_upper))
print('PASS')
