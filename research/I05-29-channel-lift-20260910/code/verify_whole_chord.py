#!/usr/bin/env python3
"""Author rational certificate: original PR58 difficult point, maximal whole chord.
Every finite sign uses Fraction arithmetic and outward analytic log remainders.
A single full interval plus one singular-endpoint inequality covers the continuum.
The direct Mobius check is a second author algebra route, not independent review.
"""
import os
for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']:os.environ[key]='1'
import time,json,platform
from pathlib import Path
import sympy as sp
from exact_core import *
from fixtures import *
START=time.perf_counter()

def main():
    A,C,U,V=original();B=U*V.T
    assert all(x!=0 for x in B)
    assert all(K[i,j]!=0 for K in (A,C) for i in range(3) for j in range(i))
    pa,pc,rows=coefficients(A,C,U,V)
    counts=direct_mobius_check(A,C,B,rows)
    print('SOURCE: immutable PR58 89aa874c, all 30 rational entries embedded')
    print('EXACT ALGEBRA: principal minors',counts[0],'; complete Mobius events',counts[1])
    print('STRICT BLOCKS: A,C,I-A,I-C positive; rank B=2; dense and correlated')
    print('COEFFICIENT CANCELLATIONS: global and both full fibers exact')
    p=rows[-1][5];empty=rows[0][5]
    L,R,cut=F(9999,10000),F(12499,12500),F(9993,10000)
    assert at(p,L)>0>at(p,R)
    assert max(p[1],p[1]+2*p[2]*R)<0
    assert qrange(empty,F(0),R)[0]>0
    print('MAXIMAL LEGAL ROOT: full event (7,7), bracket (9999/10000,12499/12500)')
    print('full determinant polynomial coefficients p0,p1,p2:',*[str(x) for x in p])
    fineL,fineR=L,R
    for _ in range(100):
        mid=(fineL+fineR)/2
        if at(p,mid)>0:fineL=mid
        else:fineR=mid
    print('s* outward display:',disp((fineL,fineR),20))
    # One interval, not a grid. The lower endpoint of every signed product
    # is chosen according to its sign before multiplying the secant envelope.
    lower=F(0);fisher_lower=F(0);log_lower=F(0);minq=F(1);summaries=[]
    for i,j,mu,a,b,pr in rows:
        qlo,qhi=qrange((F(1),-a,b),F(0),cut)
        assert qlo>0;minq=min(minq,qlo)
        vmin=qrange((a*a,-4*a*b,4*b*b),F(0),cut)[0]
        zmin=qrange((a*a,-7*a*b,6*b*b),F(0),cut)[0]
        lm,lp=lamiv(qhi)[0],lamiv(qlo)[1]
        fl=mu*4*vmin/qhi
        al=2*mu*zmin*(lm if zmin>=0 else lp)
        fisher_lower+=fl;log_lower+=al
        term=dyadic_interval((fl+al,fl+al))[0]
        lower+=term
        summaries.append([i,j,*[fraction_json(x) for x in (mu,a,b,qlo,qhi,vmin,zmin,term)]])
    assert lower>F(1,5)
    assert fisher_lower>F(311,400) and log_lower>-F(72,125)
    print('INTERIOR [0,9993/10000]: exact Gamma lower',disp((lower,lower),20),'> 1/5')
    print('INTERIOR min q lower:',disp((minq,minq),20))
    print('FULL FISHER lower:',disp((fisher_lower,fisher_lower),20),'> 311/400')
    print('SIGNED LOG lower:',disp((log_lower,log_lower),20),'> -72/125')
    print('311/400 - 72/125 = 403/2000 > 1/5; negative contributions retained')
    # Terminal interval: delta=s*-s. Complete full-event derivatives and
    # all 63 other complete events enter the documented bounds.
    d0=min(-(p[1]+2*p[2]*x) for x in (cut,R))
    d1=max(-(p[1]+2*p[2]*x) for x in (cut,R));assert d0>0
    E0=max(abs(p[1]+6*p[2]*x) for x in (cut,R))
    AA=4*cut*d0*d0/d1;BB=2*E0
    CC=BB*max(F(0),-logiv(d0)[0]);minother=F(1)
    for row in rows[:-1]:
        pr=row[5];mn,mx=qrange(pr,cut,R)
        assert 0<mn<=mx<1;minother=min(minother,mn)
        E=max(abs(pr[1]+6*pr[2]*x) for x in (cut,R))
        CC+=2*E*(-logiv(mn)[0])
    assert AA>F(1,100) and BB<F(3,50) and CC<14
    assert R-cut<F(1,1600)
    assert logiv(F(1600))[1]<8
    print('ENDPOINT [9993/10000,s*): A>',F(1,100),'B<',F(3,50),'C<14')
    print('A,B,C directed displays:',*[disp((x,x),20) for x in (AA,BB,CC)])
    print('all 63 nonrare events positive on [cut,12499/12500], min:',disp((minother,minother),20))
    print('ENDPOINT PROOF: -H_second >= 1/(100 delta)-(3/50)log(1/delta)-14 > 3/2')
    print('GLOBAL: H_second(t) <= -t^2/5 on the whole strict legal chord; H_second(0)=0')
    print('CLOSED CHORD: H(t)+t^4/60 concave; strict Jensen concavity for H')
    # Preserve comparison with the accepted s=.9 full value, not its old
    # additive-residual conventions or a new pairwise-positivity claim.
    s=F(9,10);curv=(F(0),F(0))
    for i,j,mu,a,b,_ in rows:
        q=1-s*a+s*s*b;u=q-1;y=s*s*b
        curv=ivadd(curv,ivscale(mu,ivadd((4*(u+y)**2/q,)*2,ivscale(2*(u+5*y),logiv(q)))))
    assert curv[0]>F(4653,1000)
    print('s=.9 full t^2 I_second:',disp(curv,16))
    evidence={'status':'AUTHOR_PROOF_AND_CERTIFICATE_PENDING_REVIEW','input':{name:[[str(x) for x in row] for row in mat.tolist()] for name,mat in [('A',A),('C',C),('U',U),('V',V)]},
      'cut':fraction_json(cut),'root_coarse':[fraction_json(L),fraction_json(R)],'root_fine':[fraction_json(fineL),fraction_json(fineR)],
      'full_polynomial':[fraction_json(x) for x in p], 'interior_lower':fraction_json(lower),'fisher_lower':fraction_json(dyadic_interval((fisher_lower,fisher_lower))[0]),'signed_log_lower':fraction_json(dyadic_interval((log_lower,log_lower))[0]),
      'endpoint':{key:fraction_json(val) for key,val in [('d0',d0),('d1',d1),('A',AA),('B',BB),('C_upper',CC),('min_other_p',minother)]},
      'interior_table_columns':['left_mask','right_mask','mu','a','b','q_min','q_max','min_v_squared','min_z','weighted_lower'],
      'interior_table':summaries,
      'log_error_rule':{'atanh_terms':28,'mantissa_outward_bits':56,'output_outward_bits':112},
      'execution':{'python':platform.python_version(),'sympy':sp.__version__,'elapsed_seconds':time.perf_counter()-START,'process_threads':1}}
    out=Path(__file__).resolve().parent.parent/'output'/'whole_chord_certificate.json'
    out.write_text(json.dumps(evidence,indent=2)+'\n')
    print('PASS (author only); saved whole_chord_certificate.json')
    print('Python',platform.python_version(),'SymPy',sp.__version__,'elapsed seconds',round(time.perf_counter()-START,3))

if __name__=='__main__':main()
