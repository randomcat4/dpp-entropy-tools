"""Exact arithmetic for one analytic monotonicity endpoint; no scan."""
from fractions import Fraction as Q
from math import factorial
import json

rho=Q(25)
ar=(2*rho+1)**2/(3*rho*(rho+2))
br=(rho+2)**2/(3*(2*rho+1))
assert ar==Q(289,225) and br==Q(81,17)
ratio=br**4/ar
lower=sum((Q(6**k,factorial(k)) for k in range(17)),Q(0))
assert ratio==Q(9685512225,24137569)
assert lower-ratio==Q(44297548672294,21141493247875)>0
lam=Q(1,2); mu=Q(1,26)
q=lam*(lam+2*mu)/3; p=lam*lam*mu
assert lam*(1-mu)/(mu*(1-lam))==rho
assert q==Q(5,52) and p==Q(1,104)
assert Q(5,4)<ar and br/ar>3
old_lower=(1-q)/5+(1-p)
assert old_lower==Q(609,520)>1
print(json.dumps({
  'status':'PASS_EXACT_ARITHMETIC_ONLY',
  'method':'one endpoint justified by analytic monotonicity; no scan',
  'rho_endpoint':str(rho),
  'exp6_positive_difference':str(lower-ratio),
  'old_test_lower_bound':str(old_lower),
  'remaining_global_phi_sign':'INCOMPLETE'
},indent=2))
