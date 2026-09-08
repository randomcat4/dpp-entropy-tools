"""U10j exact exponent bookkeeping only; no Hessian profile is a proof."""
from fractions import Fraction as Q
from decimal import Decimal as D, getcontext
from pathlib import Path
import hashlib,json

getcontext().prec=70
ROOT=Path(__file__).resolve().parent
# Powers in the displayed energy bounds. Each tuple is (x power, R power).
assert (Q(0)+0+Q(1,2),1+1+4)==(Q(1,2),6)
assert Q(1,2)-6*Q(1,24)==Q(1,4)
assert 1-6*Q(1,12)==Q(1,2)
records=[]
for theta in [Q(1,100),Q(1,24),Q(1,13)]:
    exponent=Q(1,2)-6*theta
    assert exponent>0
    for k in [6,12,24]:
        x=D(10)**(-k); td=D(theta.numerator)/D(theta.denominator)
        low=x**td; high=x**(-td)
        for beta in [low,high]:
            r=2+beta+1/beta
            assert r<=4*x**(-td)
            records.append({'theta':str(theta),'x':str(x),'beta':str(beta),
                            'x_R6':str(x*r**6),'sqrt_x_R6':str(x.sqrt()*r**6),
                            's_le_x_squared':bool(-beta/x<=2*x.ln()),
                            'error_power':str(exponent),
                            'scope':'rate bookkeeping only; no numerical c,C or Hessian sign certified'})
hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in
        ['proof_candidate.md','sanity.py','../boundary_exponential_limit/proof_candidate.md']}
out={'status':'AUTHOR_PROOF_CANDIDATE_PENDING_AUDIT','scope':'EXACT_EXPONENT_SANITY_NOT_HESSIAN_REPLAY',
     'records':records,'denominator':18,'failures':0,'uniform_error_exponent':'1/2-6theta',
     'strict_theta_range':'0<theta<1/12','fixed_choice':'theta=1/24 gives exponent1/4',
     'source_hashes':hashes}
(ROOT/'sanity.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':out['status'],'scope':out['scope'],'denominator':18,'failures':0}))
