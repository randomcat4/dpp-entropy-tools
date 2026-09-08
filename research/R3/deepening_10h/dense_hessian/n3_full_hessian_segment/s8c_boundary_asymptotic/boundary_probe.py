"""S8c fixed rational spectral basis and boundary Schur majorant probe."""
import sys,os
sys.dont_write_bytecode=True
sys.set_int_max_str_digits(0)
os.environ['OPENBLAS_NUM_THREADS']='1'
from fractions import Fraction as F
from pathlib import Path
import importlib.util
import json
import hashlib
import time
from decimal import Decimal,localcontext
import numpy as np

HERE=Path(__file__).resolve().parent
HELPER=HERE.parent/'verifications'/'fresh_s8_audit.py'
spec=importlib.util.spec_from_file_location('verified_non_author_s8',HELPER)
s8=importlib.util.module_from_spec(spec); spec.loader.exec_module(s8)

def mat_outer(u,v): return [[F(x*y) for y in v] for x in u]
def symcross(u,v,den): return [[F(u[i]*v[j]+v[i]*u[j],den) for j in range(3)] for i in range(3)]
def transform_jets(raw,basis):
    coords=[[D[i][j] for i,j in s8.COORDS] for D in basis]
    one=[[[sum(coords[a][i]*raw['p1'][i][ev][k] for i in range(6)) for k in range(4)] for ev in range(8)] for a in range(6)]
    two=[[[[sum(coords[a][i]*coords[b][j]*raw['pij'][i][j][ev][k] for i in range(6) for j in range(6)) for k in range(4)] for ev in range(8)] for b in range(6)] for a in range(6)]
    return dict(p0=raw['p0'],p1=one,pij=two)
def regular_interval(jets,interval):
    p=[s8.peval_interval(poly,interval) for poly in jets['p0']]
    assert all(p[ev][0]>0 for ev in range(1,8))
    logs=[None]+[s8.ilog_pos(p[ev],24) for ev in range(1,8)]
    B=[]
    for i in range(6):
        row=[]
        for j in range(6):
            acc=(F(0),F(0))
            for ev in range(1,8):
                pi=s8.peval_interval(jets['p1'][i][ev],interval)
                pj=s8.peval_interval(jets['p1'][j][ev],interval)
                pij=s8.peval_interval(jets['pij'][i][j][ev],interval)
                acc=s8.iadd(acc,s8.idiv_pos(s8.imul(pi,pj),p[ev]))
                acc=s8.iadd(acc,s8.imul(pij,logs[ev]))
            row.append(acc)
        B.append(row)
    return B,p
def congruence(B,P):
    n=len(P); T=[]
    for a in range(n):
        row=[]
        for b in range(n):
            lo=hi=F(0)
            for i in range(n):
                for j in range(n):
                    c=P[i][a]*P[j][b]
                    lo+=c*(B[i][j][0] if c>=0 else B[i][j][1])
                    hi+=c*(B[i][j][1] if c>=0 else B[i][j][0])
            row.append((lo,hi))
        T.append(row)
    return T
def margins(T): return [T[i][i][0]-sum(max(map(abs,T[i][j])) for j in range(len(T)) if i!=j) for i in range(len(T))]
def bridge(jets):
    queue=[(F(29,100),F(299,1000),0)]; passed=[]; failed=[]; processed=0; rejected_nodes=[]
    while queue:
        lo,hi,depth=queue.pop(); processed+=1
        assert processed<=2047
        try:
            B,p=s8.B_interval(jets,(lo,hi),24)
        except ArithmeticError as error:
            rejected_nodes.append(dict(interval=(lo,hi),depth=depth,reason=str(error)))
            if depth<10:
                mid=(lo+hi)/2; queue.extend(((mid,hi,depth+1),(lo,mid,depth+1)))
            else: failed.append(dict(interval=(lo,hi),reason=str(error)))
            continue
        mid=(lo+hi)/2; midpoint=s8.B_point_float(jets,mid)
        chol=np.linalg.cholesky(midpoint); proposal=np.linalg.inv(chol.T)
        P=[[F(float(proposal[i,j])).limit_denominator(4096) if i<=j else F(0) for j in range(6)] for i in range(6)]
        assert all(P[i][i]>0 for i in range(6))
        T=congruence(B,P); rowm=margins(T)
        if min(rowm)>0:
            passed.append(dict(interval=(lo,hi),P=P,row_margins=rowm,min_atom_lower=min(x[0] for x in p)))
        elif depth<10:
            rejected_nodes.append(dict(interval=(lo,hi),depth=depth,margin=min(rowm),reason='nonpositive transformed Gershgorin margin'))
            queue.extend(((mid,hi,depth+1),(lo,mid,depth+1)))
        else: failed.append(dict(interval=(lo,hi),margin=min(rowm)))
    passed.sort(key=lambda item:item['interval'][0])
    if not failed:
        assert passed[0]['interval'][0]==F(29,100) and passed[-1]['interval'][1]==F(299,1000)
        assert all(passed[i]['interval'][1]==passed[i+1]['interval'][0] for i in range(len(passed)-1))
    return dict(passed=passed,failed=failed,rejected_internal_nodes=rejected_nodes,processed=processed,success=not failed)
def main():
    start=time.time(); U,V,W=s8.projectors(); u=(1,1,1); v=(1,2,-3); w=(5,-4,-1)
    basis=[W,symcross(u,w,11),symcross(v,w,24),U,V,symcross(u,v,7)]
    K0,R=s8.m8_line(); raw=s8.build_jets(K0,R); jets=transform_jets(raw,basis)
    gram=[[sum(A[i][j]*B[i][j] for i in range(3) for j in range(3)) for B in basis] for A in basis]
    assert all(gram[i][i]>0 for i in range(6)) and all(gram[i][j]==0 for i in range(6) for j in range(6) if i!=j)
    aa=s8.pt_affine(F(4,5),-F(1,5)); bb=s8.pt_affine(F(1,2),-F(1,3)); cc=s8.pt_affine(F(1,5),-F(2,3))
    assert jets['p0'][0]==s8.pt_mul(s8.pt_mul(aa,bb),cc)
    expected_grad=[s8.pt_scale(-1,s8.pt_mul(aa,bb)),s8.pt_zero(),s8.pt_zero(),s8.pt_scale(-1,s8.pt_mul(bb,cc)),s8.pt_scale(-1,s8.pt_mul(aa,cc)),s8.pt_zero()]
    assert [jets['p1'][i][0] for i in range(6)]==expected_grad
    expected_hess=[[s8.pt_zero() for _ in range(6)] for _ in range(6)]
    for i,j,poly in ((0,3,bb),(0,4,aa),(3,4,cc)):
        expected_hess[i][j]=expected_hess[j][i]=poly
    for i,poly,ratio in ((1,bb,F(126,121)),(2,aa,F(588,576)),(5,cc,F(42,49))):
        expected_hess[i][i]=s8.pt_scale(-2*ratio,poly)
    assert [[jets['pij'][i][j][0] for j in range(6)] for i in range(6)]==expected_hess
    endpoint=F(3,10); pstar=[s8.peval(p,endpoint) for p in jets['p0']]
    assert pstar[0]==0 and min(pstar[1:])>0
    assert all(x==0 for ev in jets['pij'][0][0] for x in ev)
    attempts=[]
    for h in (F(1,100),F(1,1000),F(1,10000)):
        reg,pints=regular_interval(jets,(endpoint-h,endpoint))
        a0,b0,kappa=F(37,50),F(2,5),F(2,3)
        amax,bmax=a0+h/5,b0+h/3
        c0=a0*b0*kappa; k0=a0*b0/kappa
        # w(s)=-log(c0*s); s*w(s)^k increases for k=0,1,2 when w>=2.
        w0=-s8.log_bounds_point(c0*h,24)[0]
        log_min=-s8.log_bounds_point(amax*bmax*kappa*h,24)[1]
        assert log_min>2
        vcoef=[F(0),F(0),bmax,amax,F(0)]
        ucoef=[max(map(abs,reg[0][i+1]))+vcoef[i] for i in range(5)]
        correction=[[h/k0*(ucoef[i]+vcoef[i]*w0)*(ucoef[j]+vcoef[j]*w0) for j in range(5)] for i in range(5)]
        lowdiag=[2*b0*F(126,121)*log_min,2*a0*F(588,576)*log_min,F(0),F(0),F(0)]
        tangent_off=kappa*h*(1+w0)
        M=[]
        for i in range(5):
            row=[]
            for j in range(5):
                lo,hi=reg[i+1][j+1]
                if i==j: lo+=lowdiag[i]-correction[i][i]; hi+=lowdiag[i]
                else:
                    extra=correction[i][j]+(tangent_off if {i,j}=={2,3} else 0)
                    lo-=extra; hi+=extra
                row.append((lo,hi))
            M.append(row)
        plain=margins(M); precondition=None; premargin=None; transformed=None; transformed_rows=None
        midpoint=np.array([[(float(a)+float(b))/2 for a,b in row] for row in M])
        try:
            chol=np.linalg.cholesky(midpoint); proposal=np.linalg.inv(chol.T)
            P=[[F(float(proposal[i,j])).limit_denominator(4096) if i<=j else F(0) for j in range(5)] for i in range(5)]
            assert all(P[i][i]>0 for i in range(5))
            T=congruence(M,P); pm=margins(T)
            precondition=P; premargin=min(pm); transformed=T; transformed_rows=pm
        except np.linalg.LinAlgError: pass
        attempts.append(dict(h=h,regular_B=reg,regular_atom_intervals=pints[1:],w_upper_at_h=w0,log_floor=log_min,
            ucoef=ucoef,vcoef=vcoef,correction_bound=correction,Schur_lower_model=M,plain_margins=plain,
            P=precondition,transformed_model=transformed,transformed_row_margins=transformed_rows,
            preconditioned_margin=premargin,passed=(min(plain)>0 or (premargin is not None and premargin>0))))
        print('h',h,'plain',float(min(plain)),'pre',float(premargin) if premargin is not None else None)
    boundary_reg,_=regular_interval(jets,(endpoint,endpoint)); finite=[[boundary_reg[i][j] for j in (3,4,5)] for i in (3,4,5)]
    finite_margin=margins(finite)
    assert min(finite_margin)>0
    bridge_result=bridge(jets)
    assert next(item for item in attempts if item['h']==F(1,1000))['passed'] and bridge_result['success']
    report=dict(status='PROOF_CANDIDATE_PENDING_INDEPENDENT_REVIEW',basis=basis,basis_gram=gram,endpoint_atoms=pstar,bridge=bridge_result,
        empty_atom_s_polynomial=[F(0),F(74,375),F(49,225),F(2,45)],
        certified_candidate_interval=[F(29,100),F(3,10)],right_endpoint_included=False,
        frozen_failures=['h=1/100 Schur majorant not positive; not a counterexample',
            'initial bridge execution exited 1 on root Horner atom floor; fixed by explicit subdivision and retained as rejected internal node'],
        singular_pole_coefficient=F(111,250),log_coefficients=[2*F(2,5)*F(126,121),2*F(37,50)*F(588,576)],
        finite_block=finite,finite_block_margins=finite_margin,attempts=attempts,
        helper_sha256=hashlib.sha256(HELPER.read_bytes()).hexdigest(),script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        elapsed_seconds=time.time()-start,exit_code=0)
    (HERE/'boundary_probe_results.json').write_text(json.dumps(s8.serialize(report),indent=2)+'\n')
    print('atoms',pstar,'finite_margin',float(min(finite_margin)))
    print('bridge leaves',len(bridge_result['passed']),'failed',len(bridge_result['failed']))
if __name__=='__main__': main()
