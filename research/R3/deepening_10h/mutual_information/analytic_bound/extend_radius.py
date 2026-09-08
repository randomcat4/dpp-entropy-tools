"""Verify an explicit 1/32 radius from already frozen exact coefficient bounds."""
from sanity_certificate import *

target=OUT/'radius_1_over_32.json'
if target.exists(): raise FileExistsError('Radius extension certificate already exists')
c=json.loads((OUT/'certificate.json').read_text(encoding='utf-8'))
L2lo=F(c['L2_interval'][0]); C4=F(c['uniform_fourth_derivative_upper']); maxA=F(c['max_relative_a']); maxB=F(c['max_relative_b'])
radius=F(1,32); m=F(c['base_margin']); trace=F(3,2)
assert L2lo>F(11,20) and C4<941 and maxA<4 and maxB<3
assert radius*4+radius**2*3<F(1,2)
assert F(941,24)*radius**2<F(1,20)
assert m-radius*trace==F(17,320)
M,D=matrices(11); cross_sq=sum(M[i][j]**2 for i in range(5) for j in range(5,11))
assert cross_sq>F(1,16)
cross_bound=F(1,4)-radius*trace
assert cross_bound==F(13,64)
diag_bound=F(1,36)-radius*8*(F(1,58)+F(1,120))
assert diag_bound>F(1,50)
coefs=[json.loads(line) for line in (OUT/'exact_coefficients.jsonl').read_text(encoding='utf-8').splitlines()]
J4lo=J4hi=0
for row in coefs:
    p,a,b=F(row['p']),F(row['a']),F(row['b']); val=b*b/(2*p)
    J4lo+=floor_scaled(val); J4hi+=ceil_scaled(val)
checks=[]
with localcontext() as ctx:
    ctx.prec=70
    dd=lambda x:Decimal(x.numerator)/Decimal(x.denominator)
    for t in (radius/2,radius):
        ps=[[],[],[]]
        for row in coefs:
            p,a,b=F(row['p']),F(row['a']),F(row['b'])
            for k,s in enumerate((-1,0,1)): ps[k].append(p+s*t*a+t*t*b*(s*s))
        hs=[-sum(dd(z)*dd(z).ln() for z in pp) for pp in ps]
        gap=(hs[0]+hs[2])/2-hs[1]
        checks.append(dict(step=str(t),decimal_gap_sanity_only=str(gap),rigorous_upper_bound=str(-dd(t*t/2))))
result=dict(status='PROOF_CANDIDATE_PENDING_INDEPENDENT_REVIEW',radius=str(radius),uniform_gap_bound='Delta(t) <= -t^2/2',equality_cases='t=0 only',uniform_spectral_margin=str(F(17,320)),exact_center_cross_norm_squared=str(cross_sq),uniform_cross_Frobenius_lower_bound=str(cross_bound),uniform_diagonal_separation_lower_bound=str(diag_bound),simplified_diagonal_separation_lower_bound='1/50',L2_lower_simplified='11/20',uniform_H4_upper_simplified='941',remainder_quadratic_cost_upper='1/20',KL_t4_coefficient_interval=[str(F(J4lo,GRID)),str(F(J4hi,GRID))],KL_t4_coefficient_decimal=[display(F(J4lo,GRID)),display(F(J4hi,GRID))],checks=checks,exit_code=0)
target.write_text(json.dumps(result,indent=2),encoding='utf-8'); print(json.dumps(result,indent=2))
