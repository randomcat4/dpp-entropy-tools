"""S8d exact left-boundary jets and bounded interval certificates."""
import sys,os
sys.dont_write_bytecode=True
sys.set_int_max_str_digits(0)
os.environ['OPENBLAS_NUM_THREADS']='1'
from fractions import Fraction as F
from pathlib import Path
import importlib.util,json,hashlib,time
import numpy as np

HERE=Path(__file__).resolve().parent
HELPER=HERE.parent/'verifications'/'fresh_s8_audit.py'
spec=importlib.util.spec_from_file_location('verified_s8_helper',HELPER)
s8=importlib.util.module_from_spec(spec); spec.loader.exec_module(s8)

def cross(u,v,den): return [[F(u[i]*v[j]+v[i]*u[j],den) for j in range(3)] for i in range(3)]
def transform(raw,basis):
    coords=[[D[i][j] for i,j in s8.COORDS] for D in basis]
    p1=[[[sum(coords[a][i]*raw['p1'][i][ev][k] for i in range(6)) for k in range(4)] for ev in range(8)] for a in range(6)]
    p2=[[[[sum(coords[a][i]*coords[b][j]*raw['pij'][i][j][ev][k] for i in range(6) for j in range(6)) for k in range(4)] for ev in range(8)] for b in range(6)] for a in range(6)]
    return dict(p0=raw['p0'],p1=p1,pij=p2)

def congruence(B,P):
    n=len(P); out=[]
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
        out.append(row)
    return out
def margins(B): return [B[i][i][0]-sum(max(map(abs,B[i][j])) for j in range(len(B)) if i!=j) for i in range(len(B))]
def propose(M,cap=4096):
    proposal=np.linalg.inv(np.linalg.cholesky(M).T); n=len(M)
    P=[[F(float(proposal[i,j])).limit_denominator(cap) if i<=j else F(0) for j in range(n)] for i in range(n)]
    assert all(P[i][i]>0 for i in range(n))
    return P

def regular(jets,interval):
    p=[s8.peval_interval(poly,interval) for poly in jets['p0']]
    assert min(p[i][0] for i in range(7))>0
    logs=[s8.ilog_pos(p[i],24) for i in range(7)]
    B=[]
    for i in range(6):
        row=[]
        for j in range(6):
            acc=(F(0),F(0))
            for ev in range(7):
                pi=s8.peval_interval(jets['p1'][i][ev],interval)
                pj=s8.peval_interval(jets['p1'][j][ev],interval)
                pij=s8.peval_interval(jets['pij'][i][j][ev],interval)
                acc=s8.iadd(acc,s8.idiv_pos(s8.imul(pi,pj),p[ev]))
                acc=s8.iadd(acc,s8.imul(pij,logs[ev]))
            row.append(acc)
        B.append(row)
    return B,p

def tail_bound(jets,h):
    reg,p=regular(jets,(F(0),h))
    a0,b0,kappa=F(1,6),F(2,15),F(1,5)
    amax,bmax=a0+h/3,b0+2*h/3; c0=a0*b0*kappa; k0=a0*b0/kappa
    w0=-s8.log_bounds_point(c0*h,24)[0]
    Lmin=-s8.log_bounds_point(amax*bmax*kappa*h,24)[1]; assert Lmin>2
    v=[F(0),F(0),bmax,amax,F(0)]
    u=[max(map(abs,reg[0][i+1]))+v[i] for i in range(5)]
    correction=[[h/k0*(u[i]+v[i]*w0)*(u[j]+v[j]*w0) for j in range(5)] for i in range(5)]
    d=[2*b0*F(6,7)*Lmin,2*a0*F(126,121)*Lmin,F(0),F(0),F(0)]
    e=kappa*h*(1+w0)
    M=[]
    for i in range(5):
        row=[]
        for j in range(5):
            lo,hi=reg[i+1][j+1]
            if i==j: lo+=d[i]-correction[i][i]; hi+=d[i]
            else:
                extra=correction[i][j]+(e if {i,j}=={2,3} else 0)
                lo-=extra; hi+=extra
            row.append((lo,hi))
        M.append(row)
    P=T=rows=None; failure=None
    try:
        midpoint=np.array([[(float(lo)+float(hi))/2 for lo,hi in row] for row in M])
        P=propose(midpoint); T=congruence(M,P); rows=margins(T)
    except np.linalg.LinAlgError as error: failure=str(error)
    return dict(h=h,regular_matrix=reg,regular_atom_intervals=p[:7],w_upper_at_h=w0,log_floor=Lmin,
        u=u,v=v,correction=correction,lower_model=M,plain_rows=margins(M),P=P,transformed_model=T,transformed_rows=rows,
        passed=rows is not None and min(rows)>0,proposal_failure=failure)

def bridge(jets,lo,hi):
    queue=[(lo,hi,0)]; accepted=[]; rejected=[]; failed=[]; nodes=0
    while queue:
        a,b,depth=queue.pop(); nodes+=1
        assert nodes<=4095
        try:
            B,p=s8.B_interval(jets,(a,b),24); P=propose(s8.B_point_float(jets,(a+b)/2))
            T=congruence(B,P); rows=margins(T)
            record=dict(interval=(a,b),depth=depth,P=P,rows=rows,min_atom_lower=min(q[0] for q in p))
            if min(rows)>0:
                accepted.append(record); continue
            record['failure']='interval margin nonpositive'
        except (ArithmeticError,np.linalg.LinAlgError) as error:
            record=dict(interval=(a,b),depth=depth,failure=str(error))
        if depth<14:
            rejected.append(record); mid=(a+b)/2; queue.extend(((mid,b,depth+1),(a,mid,depth+1)))
        else: failed.append(record)
    accepted.sort(key=lambda x:x['interval'][0])
    if not failed:
        assert accepted[0]['interval'][0]==lo and accepted[-1]['interval'][1]==hi
        assert all(accepted[i]['interval'][1]==accepted[i+1]['interval'][0] for i in range(len(accepted)-1))
    return dict(accepted=accepted,rejected=rejected,failed=failed,nodes=nodes,passed=not failed)

def main():
    start=time.time(); U,V,W=s8.projectors(); K0,R=s8.m8_line(); left=s8.mat_add(K0,R,-F(1))
    basis=[U,cross((1,1,1),(1,2,-3),7),cross((1,1,1),(5,-4,-1),11),V,W,cross((1,2,-3),(5,-4,-1),24)]
    raw=s8.build_jets(left,R); jets=transform(raw,basis)
    gram=[[sum(A[i][j]*B[i][j] for i in range(3) for j in range(3)) for B in basis] for A in basis]
    assert all(gram[i][j]==0 for i in range(6) for j in range(6) if i!=j) and min(gram[i][i] for i in range(6))>0
    aa=s8.pt_affine(F(1,6),F(1,3)); bb=s8.pt_affine(F(2,15),F(2,3)); cc=s8.pt_affine(F(0),F(1,5))
    assert jets['p0'][7]==s8.pt_mul(s8.pt_mul(aa,bb),cc)
    expected_g=[s8.pt_mul(aa,bb),s8.pt_zero(),s8.pt_zero(),s8.pt_mul(bb,cc),s8.pt_mul(aa,cc),s8.pt_zero()]
    assert [jets['p1'][i][7] for i in range(6)]==expected_g
    hess=[[s8.pt_zero() for _ in range(6)] for _ in range(6)]
    for i,j,p in ((0,3,bb),(0,4,aa),(3,4,cc)): hess[i][j]=hess[j][i]=p
    for i,p,r in ((1,bb,F(6,7)),(2,aa,F(126,121)),(5,cc,F(49,48))): hess[i][i]=s8.pt_scale(-2*r,p)
    assert [[jets['pij'][i][j][7] for j in range(6)] for i in range(6)]==hess
    assert all(c==0 for poly in jets['pij'][0][0] for c in poly)
    atoms=[poly[0] for poly in jets['p0']]; assert atoms[7]==0 and min(atoms[:7])>0
    orders=[next(i for i,c in enumerate(poly) if c) for poly in jets['p0']]
    scouts=[]
    for s in [F(1,10000),F(1,1000),F(1,100),F(1,10),F(1,5),F(3,10),F(2,5),F(1,2),F(3,5),F(71,100)]:
        eig=np.linalg.eigvalsh(s8.B_point_float(jets,s)); scouts.append(dict(s=s,t=s-1,min_eigenvalue=float(eig[0]),max_eigenvalue=float(eig[-1])))
    reg,_=regular(jets,(F(0),F(0))); finite=[[reg[i][j] for j in (3,4,5)] for i in (3,4,5)]
    print('atoms',atoms,'finite',list(map(float,margins(finite))),'scouts',scouts,flush=True)
    tails=[tail_bound(jets,h) for h in (F(1,100),F(1,1000),F(1,10000))]
    print('tails',[(x['h'],x['passed'],None if x['transformed_rows'] is None else float(min(x['transformed_rows']))) for x in tails],flush=True)
    usable=[x for x in tails if x['passed']]
    bridge_result=bridge(jets,max(x['h'] for x in usable),F(71,100)) if usable else None
    report=dict(status='PROOF_CANDIDATE_PENDING_REVIEW' if bridge_result and bridge_result['passed'] else 'INCOMPLETE',
        parameter='s=t+1',left_kernel=left,direction=R,basis=basis,gram=gram,atoms_at_left=atoms,atom_orders_at_left=orders,atom_polynomials=jets['p0'],
        boundary_finite_block=finite,boundary_finite_rows=margins(finite),scouts=scouts,tail_attempts=tails,bridge=bridge_result,
        helper_sha256=hashlib.sha256(HELPER.read_bytes()).hexdigest(),script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        elapsed_seconds=time.time()-start,exit_code=0)
    (HERE/'negative_results.json').write_text(json.dumps(s8.serialize(report),indent=2)+'\n')
    print('done',report['status'],'bridge leaves',len(bridge_result['accepted']) if bridge_result else None,'seconds',report['elapsed_seconds'])

if __name__=='__main__': main()
