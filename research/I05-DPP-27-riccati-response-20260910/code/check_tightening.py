#!/usr/bin/env python3
"""Post-handoff exact rational verification of tighter response constants."""
from fractions import Fraction as F
from datetime import datetime,timezone
from pathlib import Path
import json
k=F(34,81); r=F(32,9); M=F(19,160)
P=F(2); Pt=F(7,64); Ptt=F(1,32); PtQ=F(3,8)
a=F(1,6); b=F(1,8)
assert F(1169,82944)<M*M
assert F(1,2)+2*F(3,32)**2<F(3,4)**2
assert F(3,4)+F(3,16)<1
assert 2*(F(3,16)+F(9,64))<1
beta=k+2*M
hess_gamma=k*k+2*P*k*M+2*k*r*M+2*M*M
assert beta<F(2,3) and hess_gamma<F(19,25)
R1=F(3); RH=F(25,6)
Ct=M*Pt+a; Ctt=M*Ptt+2*Pt*a+b
b2=4*M+2*P*k+2*k*r
assert Ct<F(9,50) and Ctt<F(1,6) and b2<F(26,5)
assert M*PtQ+Pt*k+P*a+F(1,2)<1
cH=(a*a+2*Ct*R1*k*a)/2
E02=cH/(1-k*k)
E01=(Ctt*R1+2*Ct*R1*R1)/2+E02*b2*R1
E11=Ct*R1
assert E01<3 and E02<F(1,15) and E11<F(11,20)
CtH=Pt*M*M/2+a*M
CttH=Ptt*M*M/2+2*Pt*a*M+a*a+b*M
CgradH=PtQ*M*M/2+Pt*k*M+P*a*M+k*a+M/2
pure02=RH*(CttH+2*F(9,50)*R1*CgradH)/2
pure12=RH*CtH
assert pure02<F(1,2) and pure12<F(9,100)
d={'status':'AUTHOR_EXACT_CONSTANTS_PASS_NOT_INDEPENDENT_REVIEW',
   'utc':datetime.now(timezone.utc).isoformat(),
   'arithmetic':'fractions.Fraction; no floating proof comparisons',
   'constants':{key:str(val) for key,val in {
      'image_F_radius':M,'TV_Lipschitz':F(1),'beta':beta,
      'beta_gap_to_2_3':F(2,3)-beta,'state_Hessian_contraction':hess_gamma,
      'Hessian_gap_to_19_25':F(19,25)-hess_gamma,'Ct':Ct,'Ctt':Ctt,'b2':b2,
      'mixed_error_e01':E01,'mixed_error_e02':E02,'mixed_error_e11':E11,
      'CtH':CtH,'CttH':CttH,'CgradH':CgradH,
      'pure_Hessian_error_e02':pure02,'pure_Hessian_error_e12':pure12,
      'pure02_gap_to_1_2':F(1,2)-pure02,'pure12_gap_to_9_100':F(9,100)-pure12
   }.items()},'curvature_sign_certified':False,'failure_ledger':[]}
s=json.dumps(d,indent=2)+'\n'
Path(__file__).with_name('tightening_output.json').write_text(s)
print(s,end='')
