"""Exact-rational audit of saved node enclosures and the continuum bridge.
Does not execute or repeat any DPP node enumeration.
"""
from fractions import Fraction as F
from pathlib import Path
import json,time,resource
ROOT=Path(__file__).parent
start=time.perf_counter();cpu=time.process_time()

def hx(x):return F.from_float(float.fromhex(x))
def add(a,b):return (a[0]+b[0],a[1]+b[1])
def scale(a,c):return (a[0]*c,a[1]*c) if c>=0 else (a[1]*c,a[0]*c)
def mul(a,b):
    z=[a[0]*b[0],a[0]*b[1],a[1]*b[0],a[1]*b[1]]
    return min(z),max(z)
def p_add(*ps):
    out=[F(0)]*max(map(len,ps))
    for p in ps:
        for j,v in enumerate(p):out[j]+=v
    return out
def p_scale(p,c):return [c*v for v in p]
def p_mul(p,q):
    out=[F(0)]*(len(p)+len(q)-1)
    for i,x in enumerate(p):
        for j,y in enumerate(q):out[i+j]+=x*y
    return out

inputs=json.loads((ROOT/'certificate_inputs.json').read_text())
assert inputs['N']==32 and inputs['r']==9 and inputs['rho']==3
cos=[tuple(map(hx,v)) for v in inputs['cos_pi_j_over_64']]
rows={}; all_norm=True
for line in (ROOT/'node_output.tsv').read_text().splitlines():
    if not line or line.startswith('#'):continue
    p=line.split(); i=int(p[0]); assert i not in rows
    assert len(p)==11 and int(p[10])==4**9
    values=[hx(x) for x in p[1:9]]
    assert values[0]<=values[1]
    assert values[2]<=1<=values[3]
    assert values[4]<=0<=values[5] and values[6]<=0<=values[7]
    rows[i]=(values[0],values[1])
assert set(rows)==set(range(128))

# Reconstruct, rather than merely copy, the KL second-tail polynomial.
eps=F(81,1024); k=F(34,81); lam=k*k
M0=F(33,400);J0=F(285,2704);H0=F(1077,17576)
A=[2*M0]
B=[2*(J0+F(63,160)*M0),3*M0/k]
C=[2*(H0+F(63,80)*J0+F(9,8)*M0),
   2*((3*J0+10*M0)/k-F(9,4)*M0/k**2+F(63,80)*F(3,2)*M0/k),
   F(9,2)*M0/k**2]
u=F(1,3);v=F(4,3)
F0=p_scale(p_mul(A,A),1/(2*eps))
F1=p_add(p_scale(p_mul(A,B),1/eps),p_scale(p_mul(A,A),u/(2*eps**2)))
F2=p_add(p_scale(p_add(p_mul(B,B),p_mul(A,C)),1/eps),
         p_scale(p_mul(A,B),2*u/eps**2),
         p_scale(p_mul(A,A),u*u/eps**3+v/(2*eps**2)))
P=p_add(F2,p_mul([F(4),F(1)],F1),p_mul([F(9),F(9)],F0))
a0,a1,a2=P
assert P==[F(342449808326286961,15178486401000000),F(154889893499,5135349375),F(1809918,180625)]
r=9
E9=(lam**r/2)*(a2*(F(r*r)/(1-lam)+2*r*lam/(1-lam)**2+lam*(1+lam)/(1-lam)**3)
                 +a1*(F(r)/(1-lam)+lam/(1-lam)**2)+a0/(1-lam))
assert E9<F(115,10**6)
Mexact=sum((F(4,3)**n*F(144,25)*(3*n**3+4*n**2) for n in [20,18]),F(0))/2
assert Mexact==F(318159082659774464,9685512225) and Mexact<40000000
Echeb=F(6*40000000,3**32)

cells=[]
for cell in range(4):
    coeff=[]
    for degree in range(32):
        acc=(F(0),F(0))
        for j in range(32):
            ix=(degree*(2*j+1))%128
            if ix>64:ix=128-ix
            acc=add(acc,mul(rows[32*cell+j],cos[ix]))
        coeff.append(scale(acc,F(1,32) if degree==0 else F(1,16)))
    poly_hi=coeff[0][1]+sum((max(abs(a),abs(b)) for a,b in coeff[1:]),F(0))
    finite_hi=poly_hi+Echeb
    true_hi=finite_hi+E9
    assert true_hi < -F(1,3000)
    item={'cell':[str(F(2+cell,4)),str(F(3+cell,4))],
          'polynomial_upper':str(poly_hi),'finite_curvature_upper':str(finite_hi),
          'true_curvature_upper':str(true_hi),
          'display_true_upper':float(true_hi),
          'chebyshev_coefficients':[[str(a),str(b)] for a,b in coeff]}
    cells.append(item)
    print('cell',item['cell'],'poly upper',float(poly_hi),'finite upper',float(finite_hi),'TRUE upper',float(true_hi))

result={'status':'AUTHOR_CERTIFICATE_PASS_PENDING_INDEPENDENT_REVIEW',
        'scope':'Complete-configuration Shannon rate for f_t=1/2+cos(4pi theta)/4+t cos(2pi theta)/8 on t in [1/2,3/2]',
        'conclusion':'h_tt < -1/3000 on the entire closed interval',
        'node_count':len(rows),'future_complete_words_per_node':4**9,'complete_current_future_atoms_per_node':4**10,
        'tail_E9':str(E9),'display_tail_E9':float(E9),'interpolation_error':str(Echeb),
        'display_interpolation_error':float(Echeb),'complex_M_exact':str(Mexact),
        'cells':cells,'audit_wall_seconds':time.perf_counter()-start,'audit_cpu_seconds':time.process_time()-cpu,
        'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(ROOT/'certificate_result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['cells']}))
