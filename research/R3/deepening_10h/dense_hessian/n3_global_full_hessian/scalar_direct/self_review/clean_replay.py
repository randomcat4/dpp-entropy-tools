"""Same-author clean replay, not a non-author audit. Writes only self_review."""
import sys
sys.dont_write_bytecode=True
sys.set_int_max_str_digits(0)
from pathlib import Path
from fractions import Fraction as Q
import runpy,json,hashlib,time
HERE=Path(__file__).resolve().parent
PARENT=HERE.parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def encode(x):
    if isinstance(x,Q):return str(x)
    if isinstance(x,(tuple,list)):return [encode(v) for v in x]
    if isinstance(x,dict):return {k:encode(v) for k,v in x.items()}
    return x
def determinant(a):
    return (a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])
           -a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])
           +a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]))
def signed_atoms(K):
    ans=[]
    for s in range(8):
        a=[r[:] for r in K]
        for i in range(3):a[i][i]-=int(not(s>>i&1))
        ans.append((-1)**(3-s.bit_count())*determinant(a))
    return ans
def ln_small(q,terms=120):
    y=(q-1)/(q+1);v=y;out=Q(0)
    for i in range(terms):out+=2*v/(2*i+1);v*=y*y
    return out,out+2*v/((2*terms+1)*(1-y*y))
def ln_interval(q):
    if q<1:
        a,b=ln_interval(1/q);return -b,-a
    power=0
    while q>2:q/=2;power+=1
    a,b=ln_small(q);c,d=ln_small(Q(2))
    return a+power*c,b+power*d
def strict_principal_minors(a):
    # Independent Sylvester test, not author LDL.
    out=[a[0][0],a[0][0]*a[1][1]-a[0][1]*a[1][0],determinant(a)]
    assert min(out)>0
    return out
def main():
    started=time.time()
    frozen={p.name:sha(p) for p in PARENT.iterdir() if p.is_file()}
    old=json.loads((PARENT/'sanity.json').read_text())
    g=runpy.run_path(str(PARENT/'sanity.py'),run_name='same_author_clean_replay')
    # Do not execute the writer in the author directory. Redirect only runtime output.
    g['main'].__globals__['HERE']=HERE
    g['main']()
    fresh=json.loads((HERE/'sanity.json').read_text())
    assert fresh['rows']==old['rows']
    assert fresh['exact_surrogate_obstruction']==old['exact_surrogate_obstruction']
    assert fresh['denominator']==old['denominator']==29
    assert fresh['sha256']==sha(PARENT/'sanity.py')
    assert len({json.dumps(row['K']) for row in fresh['rows']})==29
    counts={label:sum(r['family']==label for r in fresh['rows']) for label in sorted({r['family'] for r in fresh['rows']})}
    six_pass=sum(float(r['six_category_rho_upper'])<1 for r in fresh['rows'])
    assert six_pass==29
    ob=fresh['exact_surrogate_obstruction'];K=[[Q(x) for x in r] for r in ob['K']];D=[[Q(x) for x in r] for r in ob['D']]
    h=Q(1,1000);vals={}
    for j in (-2,-1,0,1,2):
        vals[j]=signed_atoms([[K[a][b]+j*h*D[a][b] for b in range(3)] for a in range(3)])
    p=vals[0]
    p1=[(8*(vals[1][s]-vals[-1][s])-(vals[2][s]-vals[-2][s]))/(12*h) for s in range(8)]
    p2=[(vals[1][s]+vals[-1][s]-2*p[s])/h**2 for s in range(8)]
    assert p==list(map(Q,ob['p'])) and p1==list(map(Q,ob['dp']))
    assert sum(p)==1 and sum(p1)==sum(p2)==0 and min(p)>0
    F=sum(p1[s]**2/p[s] for s in range(8));B=[F,F]
    for s in range(8):
        lo,hi=ln_interval(p[s]);w=p2[s]
        B[0]+=w*(lo if w>=0 else hi);B[1]+=w*(hi if w>=0 else lo)
    authorB=list(map(Q,ob['true_B_interval']))
    assert max(B[0],authorB[0])<=min(B[1],authorB[1]) and B[0]>0
    # Direct Taylor-polynomial exact jets and rational log sum verify actual B.
    certificates={'D_principal_minors':strict_principal_minors(D),'endpoints':[]}
    for t in (Q(-1,100),Q(1,100)):
        low=[[K[i][j]+t*D[i][j]-Q(i==j,1000) for j in range(3)] for i in range(3)]
        high=[[Q(i==j)-K[i][j]-t*D[i][j]-Q(i==j,1000) for j in range(3)] for i in range(3)]
        certificates['endpoints'].append({'t':t,'low':strict_principal_minors(low),'high':strict_principal_minors(high)})
    # Re-derive pair-loss coefficients in exact arithmetic from D, not stored literals.
    n=ln_interval(Q(43,7));m=ln_interval(Q(625,301))
    cn=2*((D[1][1]*D[2][2]-D[1][2]**2)+(D[0][0]*D[1][1]-D[0][1]**2))
    cm=2*(D[0][0]*D[2][2]-D[0][2]**2)
    assert cn==Q(142,75) and cm==Q(16,9)
    ft=Q(ob['coarse_Fisher']);bt=[ft-cn*n[1]-cm*m[1],ft-cn*n[0]-cm*m[0]]
    assert bt[1]<0
    unchanged=all(sha(PARENT/name)==digest for name,digest in frozen.items());assert unchanged
    report={'role':'SAME_AUTHOR_INTERNAL_SELF_REVIEW_NOT_NONAUTHOR_AUDIT',
      'status':'CLEAN_REPLAY_PASS_NO_CORE_GAP_FOUND','author_hashes_before_and_after':frozen,'author_files_unchanged':unchanged,
      'exact_row_replay_equal':True,'exact_obstruction_replay_equal':True,'denominator':29,'distinct_K_count':29,
      'families':counts,'six_category_pass':six_pass,'five_category_pass':fresh['coarse_pass_count'],
      'capacity_pass':fresh['capacity_pass_count'],'full_positive_count':fresh['full_positive_count'],
      'direct_signed_event_atoms':p,'exact_polynomial_p1':p1,'exact_polynomial_p2':p2,
      'actual_B_direct_interval':B,'proxy_B_direct_interval':bt,'strict_feasibility':certificates,
      'same_author_reuse':'Author main replayed in fresh runpy namespace with output directory redirected; extra witness calculation reimplements determinant, exact cubic interpolation, log intervals and Sylvester minors.',
      'limits':'No non-author independence, no general proof, no whole-domain interval coverage; dense estimator formula executed at 23/29 points, path affine-estimator branch reviewed on paper only.',
      'exit_code':0,'elapsed_seconds':time.time()-started}
    (HERE/'self_review.json').write_text(json.dumps(encode(report),indent=2),encoding='utf-8')
    print('SELF_REVIEW_PASS',counts,'six_category_pass',six_pass,'author_files_unchanged',unchanged)
if __name__=='__main__':main()
