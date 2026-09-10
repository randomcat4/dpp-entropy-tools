#!/usr/bin/env python3
# Imports the frozen exact event reconstruction and rational log enclosure from the
# preceding self-contained certificate. Importing it also reruns/asserts that base certificate.
from verify_s09_signed_fibers import F, pA, pC, data, log_iv, iv_scale


def lambda_iv(q):
    if q==1:
        return (F(1),F(1))
    return iv_scale(F(1,q-1),log_iv(q))


def bound_one(fixed_left,outer):
    weights=pC if fixed_left else pA
    zs=[data[(outer,i)] if fixed_left else data[(i,outer)] for i in range(8)]
    qs=[z[2] for z in zs]
    qmin=min(qs); qmax=max(qs)

    # lambda is decreasing: lambda_- at qmax, lambda_+ at qmin.
    lm=lambda_iv(qmax)
    lp=lambda_iv(qmin)
    assert lm[0]>0 and lp[0]>0 and lp[0]>=lm[0]

    c_iv=((lm[0]+lp[0])/2,(lm[1]+lp[1])/2)
    delta_hi=(lp[1]-lm[0])/2
    assert delta_hi>=0

    Ev2=sum(weights[i]*(zs[i][3]+zs[i][4])**2 for i in range(8))
    Ez=sum(weights[i]*zs[i][3]*(zs[i][3]+5*zs[i][4]) for i in range(8))
    Eabsz=sum(weights[i]*abs(zs[i][3]*(zs[i][3]+5*zs[i][4])) for i in range(8))

    # rigorous lower endpoint for 4 Ev2/qmax + 2 c Ez - 2 delta E|z|
    civ_term=iv_scale(F(2)*Ez,c_iv)
    lo=F(4)*Ev2/qmax + civ_term[0] - F(2)*delta_hi*Eabsz
    hi=F(4)*Ev2/qmax + civ_term[1] - F(2)*delta_hi*Eabsz
    assert lo>0
    return lo,hi,qmin,qmax,Ev2,Ez,Eabsz

left=[bound_one(True,i) for i in range(8)]
right=[bound_one(False,i) for i in range(8)]

print('I05-29 s=9/10 fiber window-moment theorem: PASS')
print('All signs below are exact rational endpoint comparisons; decimals are display only.')
print('left fiber theorem lower/upper approximations:')
for i,z in enumerate(left):
    print(i,float(z[0]),float(z[1]))
print('right fiber theorem lower/upper approximations:')
for i,z in enumerate(right):
    print(i,float(z[0]),float(z[1]))
print('minimum left theorem lower bound approx:',min(float(z[0]) for z in left))
print('minimum right theorem lower bound approx:',min(float(z[0]) for z in right))
print('strict: theorem covers every fiber on either orientation despite known bad events/pairs')
