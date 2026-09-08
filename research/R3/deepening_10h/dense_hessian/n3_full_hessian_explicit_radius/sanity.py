"""S7 standard-library exact constants and bounded mixed-jet sanity."""
from fractions import Fraction as F
from decimal import Decimal, localcontext
from itertools import permutations
from pathlib import Path
from math import factorial
import json
import hashlib
import time

HERE=Path(__file__).resolve().parent
def add(*polys):
    out={}
    for p in polys:
        for e,x in p.items(): out[e]=out.get(e,F(0))+x
    return {e:x for e,x in out.items() if x}
def scale(c,p): return {e:c*x for e,x in p.items() if c*x}
def mul(a,b):
    out={}
    for e,x in a.items():
        for f,y in b.items():
            ef=(e[0]+f[0],e[1]+f[1]); out[ef]=out.get(ef,F(0))+x*y
    return {e:x for e,x in out.items() if x}
def determinant(a):
    out={}
    for perm in permutations(range(len(a))):
        sign=(-1)**sum(perm[i]>perm[j] for i in range(len(a)) for j in range(i+1,len(a)))
        term={(0,0):F(sign)}
        for i,j in enumerate(perm): term=mul(term,a[i][j])
        out=add(out,term)
    return out
def exact_atoms(K,E,D):
    matrix=[[{(0,0):K[i][j],(1,0):E[i][j],(0,1):D[i][j]} for j in range(3)] for i in range(3)]
    inc=[]
    for mask in range(8):
        ids=[i for i in range(3) if mask>>i&1]
        inc.append(determinant([[matrix[i][j] for j in ids] for i in ids]))
    atoms=[]
    for mask in range(8):
        mob=add(*(scale((-1)**(sup.bit_count()-mask.bit_count()),inc[sup]) for sup in range(8) if sup&mask==mask))
        shifted=[[add(matrix[i][j],{(0,0):-F(i==j and not (mask>>i&1))}) for j in range(3)] for i in range(3)]
        direct=scale((-1)**(3-mask.bit_count()),determinant(shifted))
        assert direct==mob
        atoms.append(mob)
    assert add(*atoms)=={(0,0):F(1)}
    return atoms
def dec(x): return Decimal(x.numerator)/Decimal(x.denominator)
def frob2(a): return sum(x*x for row in a for x in row)
def serial(x):
    if isinstance(x,(F,Decimal)): return str(x)
    if isinstance(x,(list,tuple)): return [serial(v) for v in x]
    if isinstance(x,dict): return {k:serial(v) for k,v in x.items()}
    return x
def main():
    start=time.time()
    q=F(87,1250); m=q/2; ell=F(3)
    L=8*(27/m**2+54/m+6*ell)
    choices=[F(1,10),q/6,F(43,100)/L]; delta=min(choices)
    assert L==F(160561104,841) and delta==F(36163,16056110400)
    exp4_lower=sum(F(4**j,factorial(j)) for j in range(5))
    assert exp4_lower==F(103,3) and exp4_lower>1/m
    assert L*delta==F(43,100) and q-3*delta>=m
    K=[[F(151,280),-F(6,35),-F(47,280)],[-F(6,35),F(94,175),-F(29,175)],[-F(47,280),-F(29,175),F(747,1400)]]
    zero=[[F(0)]*3 for _ in range(3)]
    base=exact_atoms(K,zero,zero)
    base_atoms=[a[(0,0)] for a in base]; assert min(base_atoms)==q
    # Exact characteristic-root checks, including multiplicities via distinctness.
    eigenvalues=[F(1,5),F(7,10),F(71,100)]
    for lam in eigenvalues:
        polynomial=determinant([[{(0,0):K[i][j]-F(i==j)*lam} for j in range(3)] for i in range(3)])
        assert not polynomial
    assert len(set(eigenvalues))==3 and min(min(x,1-x) for x in eigenvalues)==F(1,5)
    perturbations=[]
    for i,j in ((0,0),(1,1),(2,2),(0,1),(0,2),(1,2)):
        E=[[F(0)]*3 for _ in range(3)]; E[i][j]=E[j][i]=F(1) if i==j else F(1,2)
        assert frob2(E)<=1; perturbations.append(E)
    off=[[F(0),F(1),F(0)],[F(1),F(0),F(0)],[F(0)]*3]
    indefinite=[[F(1),F(0),F(0)],[F(0),-F(1),F(0)],[F(0)]*3]
    Dstar=[[F(307,630),-F(64,315),-F(53,630)],[-F(64,315),F(131,315),-F(4,315)],[-F(53,630),-F(4,315),F(187,630)]]
    directions=[perturbations[0],off,indefinite,Dstar]
    records=[]
    with localcontext() as ctx:
        ctx.prec=70
        for ei,E in enumerate(perturbations):
            en=frob2(E)
            for sign in (-1,1):
                point=[[K[i][j]+sign*delta*E[i][j] for j in range(3)] for i in range(3)]
                for di,D in enumerate(directions):
                    dn=frob2(D); atoms=exact_atoms(point,E,D)
                    H2=Decimal(0); H3=Decimal(0); jets=[]
                    for atom in atoms:
                        p=atom.get((0,0),F(0)); pe=atom.get((1,0),F(0)); pd=atom.get((0,1),F(0))
                        ped=atom.get((1,1),F(0)); pdd=2*atom.get((0,2),F(0)); pedd=2*atom.get((1,2),F(0))
                        assert m<=p<=1
                        assert pe**2<=9*en and pd**2<=9*dn
                        assert ped**2<=36*en*dn and pdd**2<=36*dn**2 and pedd**2<=36*en*dn**2
                        H2-=dec(pd*pd/p)+dec(pdd)*dec(p).ln()
                        H3+=dec(pe*pd*pd/p**2)-dec((2*ped*pd+pe*pdd)/p)-(1+dec(p).ln())*dec(pedd)
                        jets.append(dict(p=p,p_E=pe,p_D=pd,p_ED=ped,p_DD=pdd,p_EDD=pedd))
                    bound=dec(L)*dec(en).sqrt()*dec(dn)
                    assert abs(H3)<=bound
                    assert H2<=-dec(F(43,100)*dn)
                    records.append(dict(perturbation_index=ei,sign=sign,direction_index=di,K=point,E=E,D=D,
                        E_frob2=en,D_frob2=dn,atom_jets=jets,H2=H2,H3=H3,third_derivative_bound=bound))
        report=dict(status='AUTHOR_EXACT_SANITY_PENDING_REVIEW',constants=dict(q=q,m=m,ell=ell,L=L,
            delta_candidates=choices,delta=delta,delta_decimal=dec(delta),exp4_partial_lower=exp4_lower,
            atom_floor_bound=q-3*delta,spectral_floor_bound=F(1,5)-delta,curvature_loss=L*delta,
            final_negative_margin=F(43,100)),base_atoms=base_atoms,eigenvalues=eigenvalues,cases=records,
            counts=dict(base_atom_checks=8,perturbed_kernels=12,directions_per_kernel=4,mixed_jet_cases=len(records),
                        exact_atom_jet_checks=8*len(records),failed_checks=0,random_draws=0),
            finite_scope='SCOUT sanity, not proof of continuum coverage',seed=None,
            elapsed_seconds=time.time()-start,exit_code=0,
            script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (HERE/'sanity_results.json').write_text(json.dumps(serial(report),indent=2)+'\n')
    print(json.dumps(serial({k:report[k] for k in ('constants','counts','elapsed_seconds','exit_code')}),indent=2))
if __name__=='__main__': main()
