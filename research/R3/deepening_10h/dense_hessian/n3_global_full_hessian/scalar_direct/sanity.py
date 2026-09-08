"""Standard-library independent exact atoms and high precision projection sanity."""
import sys
sys.dont_write_bytecode=True
sys.set_int_max_str_digits(0)
from fractions import Fraction as Q
from decimal import Decimal as R, localcontext
from itertools import permutations
from pathlib import Path
import hashlib,json,time
HERE=Path(__file__).resolve().parent
COORD=((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))
def dec(q): return R(q.numerator)/R(q.denominator) if isinstance(q,Q) else R(q)
def dot(x,y): return sum(a*b for a,b in zip(x,y))
def mm(a,b): return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def tr(a): return sum(a[i][i] for i in range(len(a)))
def solve(a,b):
    n=len(a);a=[r[:]+[b[i]] for i,r in enumerate(a)]
    for k in range(n):
        j=max(range(k,n),key=lambda j:abs(a[j][k]));a[k],a[j]=a[j],a[k]
        v=a[k][k];assert v
        a[k]=[x/v for x in a[k]]
        for i in range(n):
            if i!=k:
                v=a[i][k];a[i]=[a[i][j]-v*a[k][j] for j in range(n+1)]
    return [r[-1] for r in a]
def inv(a):
    cols=[solve(a,[R(i==j) for i in range(len(a))]) for j in range(len(a))]
    return [list(r) for r in zip(*cols)]
def det3(a):
    return sum((-1)**sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))*a[0][p[0]]*a[1][p[1]]*a[2][p[2]] for p in permutations(range(3)))
def ldl(a):
    a=[r[:] for r in a];out=[]
    for k in range(len(a)):
        d=a[k][k];assert d>0;out.append(d)
        for i in range(k+1,len(a)):
            for j in range(i,len(a)):a[j][i]=a[i][j]=a[i][j]-a[i][k]*a[k][j]/d
    return out
def atoms(K):
    m=[];J=[]
    for mask in range(8):
        ids=[i for i in range(3) if mask>>i&1];v=Q(0);g=[Q(0)]*6
        for p in permutations(ids):
            sign=(-1)**sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))
            factors=[K[i][j] for i,j in zip(ids,p)];term=Q(sign)
            for f in factors:term*=f
            v+=term
            for k,(i,j) in enumerate(zip(ids,p)):
                term=Q(sign)
                for ell,f in enumerate(factors):
                    if ell!=k:term*=f
                g[COORD.index(tuple(sorted((i,j))))]+=term
        m.append(v);J.append(g)
    p=m[:];grad=[r[:] for r in J]
    for i in range(3):
        for mask in range(8):
            if not mask>>i&1:
                p[mask]-=p[mask|1<<i]
                grad[mask]=[a-b for a,b in zip(grad[mask],grad[mask|1<<i])]
    assert sum(p)==1 and min(p)>0
    assert all(sum(g[i] for g in grad)==0 for i in range(6))
    return p,grad,m,J
def calc(K,precision=140):
  p,g,m,J=atoms(K)
  cert=[ldl(K),ldl([[Q(i==j)-K[i][j] for j in range(3)] for i in range(3)])]
  with localcontext() as ctx:
    ctx.prec=precision
    P=list(map(dec,p));kd=[[dec(x) for x in row] for row in K]
    ell=[(P[0]*P[3]/(P[1]*P[2])).ln(),(P[0]*P[5]/(P[1]*P[4])).ln(),(P[0]*P[6]/(P[2]*P[4])).ln()]
    lam=(P[7]*P[1]*P[2]*P[4]/(P[0]*P[3]*P[5]*P[6])).ln()
    N=[[-lam*kd[i][j] for j in range(3)] for i in range(3)]
    for i in range(3):N[i][i]-=ell[2-i]
    delta=det3(N);ni=inv(N);assert delta>0
    E=[]
    for i,j in COORD:
        e=[[R(0)]*3 for _ in range(3)];e[i][j]=e[j][i]=R(1);E.append(e)
    W=[mm(ni,e) for e in E];eta=[tr(w) for w in W]
    F=[[dec(sum(g[s][i]*g[s][j]/p[s] for s in range(8))) for j in range(6)] for i in range(6)]
    A=[[F[i][j]+delta*tr(mm(W[i],W[j])) for j in range(6)] for i in range(6)]
    rho=delta*dot(eta,solve(A,eta))
    V=dot(eta,solve(F,eta));capacity=2*delta*V/3
    # Dense explicit moment-estimator coefficients beta(t), order x,y,z,q12,q13,q23,r.
    order=(1,2,4,3,5,6,7);C=[[dec(m[a|b]-m[a]*m[b]) for b in order] for a in order]
    x,y,z=kd[0][0],kd[1][1],kd[2][2];a,b,c=kd[0][1],kd[0][2],kd[1][2]
    variance_error=None
    if a*b*c:
        pairs=[-eta[3]/(2*a),-eta[4]/(2*b),-eta[5]/(2*c)]
        hp=[b*c/a-z,a*c/b-y,a*b/c-x]
        beta=[eta[0]-y*pairs[0]-z*pairs[1],eta[1]-x*pairs[0]-z*pairs[2],eta[2]-x*pairs[1]-y*pairs[2],*pairs,R(0)]
        h=[-y*hp[0]-z*hp[1]-(y*z-c*c),-x*hp[0]-z*hp[2]-(x*z-b*b),-x*hp[1]-y*hp[2]-(x*y-a*a),*hp,R(1)]
        ch=[dot(row,h) for row in C];cb=[dot(row,beta) for row in C]
        v2=dot(beta,cb)-dot(beta,ch)**2/dot(h,ch)
        variance_error=abs(v2-V)/max(R(1),abs(V));assert variance_error<R(10)**(-precision//2)
    # Four selected events yield five-category coarsening.
    selected=(0,3,5,6);remaining=(1,2,4,7);L=[]
    for s in selected:
        mat=[[R(0)]*3 for _ in range(3)]
        for z,(i,j) in enumerate(COORD):mat[i][j]=mat[j][i]=dec(g[s][z])/(1 if i==j else 2)
        L.append(mat)
    cov=[[P[s]*R(i==j)-P[s]*P[t] for j,t in enumerate(selected)] for i,s in enumerate(selected)]
    NL=[mm(N,l) for l in L];bvec=[tr(a) for a in NL]
    M=[[tr(mm(NL[i],NL[j]))+delta*cov[i][j] for j in range(4)] for i in range(4)]
    coarse=3-dot(bvec,solve(M,bvec))
    pR=sum(p[s] for s in remaining);gR=[sum(g[s][i] for s in remaining) for i in range(6)]
    Fc=[[dec(sum(g[s][i]*g[s][j]/p[s] for s in selected)+gR[i]*gR[j]/pR) for j in range(6)] for i in range(6)]
    Ac=[[Fc[i][j]+delta*tr(mm(W[i],W[j])) for j in range(6)] for i in range(6)]
    coarse2=delta*dot(eta,solve(Ac,eta));err=abs(coarse-coarse2)
    assert err<R(10)**(-precision//2) and coarse+R(10)**(-precision//2)>=rho
    comp_selected=(7,1,2,4);comp_L=[]
    for s in comp_selected:
        mat=[[R(0)]*3 for _ in range(3)]
        for z,(i,j) in enumerate(COORD):mat[i][j]=mat[j][i]=dec(g[s][z])/(1 if i==j else 2)
        comp_L.append(mm(N,mat))
    comp_b=[tr(a) for a in comp_L]
    comp_M=[[tr(mm(comp_L[i],comp_L[j]))+delta*(P[s]*R(i==j)-P[s]*P[t])
             for j,t in enumerate(comp_selected)] for i,s in enumerate(comp_selected)]
    comp_coarse=3-dot(comp_b,solve(comp_M,comp_b))
    # Exact conditional-score orthogonal contrasts inside R.
    fq=[[sum(g[s][i]*g[s][j]/p[s] for s in selected)+gR[i]*gR[j]/pR for j in range(6)] for i in range(6)]
    acur=[row[:] for row in Ac];rhoval=coarse;steps=[]
    for left,right in (((7,),(1,2,4)),((1,),(2,4)),((2,),(4,))):
        pa=sum(p[s] for s in left);pb=sum(p[s] for s in right)
        ga=[sum(g[s][i] for s in left) for i in range(6)]
        gb=[sum(g[s][i] for s in right) for i in range(6)]
        hq=[pb*ga[i]-pa*gb[i] for i in range(6)];weight=1/(pa*pb*(pa+pb))
        hd=list(map(dec,hq));aeta=solve(acur,eta);ah=solve(acur,hd)
        correction=delta*dot(eta,ah)**2/(1/dec(weight)+dot(hd,ah))
        rhoval-=correction
        for i in range(6):
            for j in range(6):
                fq[i][j]+=weight*hq[i]*hq[j]
                acur[i][j]+=dec(weight)*hd[i]*hd[j]
        steps.append({'left':left,'right':right,'contrast':hq,'weight':weight,
                      'rho_correction':correction,'rho_after':rhoval})
    assert all(fq[i][j]==sum(g[s][i]*g[s][j]/p[s] for s in range(8)) for i in range(6) for j in range(6))
    assert abs(rhoval-rho)<R(10)**(-precision//2)
    cd=solve(Ac,eta);cd=[v/max(abs(w) for w in cd) for v in cd]
    return {'K':K,'p':p,'strict_LDL':cert,'rho':rho,'trace_capacity_test':capacity,'coarse_rho_upper':coarse,
            'coarse_bad_direction_coordinates':cd,
            'conditional_score_updates':steps,'six_category_rho_upper':steps[0]['rho_after'],
            'complement_coarse_rho_upper':comp_coarse,'adaptive_coarse_rho_upper':min(coarse,comp_coarse),
            'one_parameter_variance_relative_error':variance_error,'woodbury_error':err,'precision':precision,
            'full_sign':'negative' if rho<1 else 'FLOAT_CANDIDATE','coarse_certificate':coarse<1,'capacity_certificate':capacity<1}
def encode(x):
    if isinstance(x,(Q,R)):return str(x)
    if isinstance(x,(list,tuple)):return [encode(v) for v in x]
    if isinstance(x,dict):return {k:encode(v) for k,v in x.items()}
    return x
def log_interval(q,terms=120):
    assert q>1
    y=(q-1)/(q+1);z=y*y;power=y;low=Q(0)
    for j in range(terms):low+=2*power/(2*j+1);power*=z
    return low,low+2*power/((2*terms+1)*(1-z))
def rational_obstruction():
    K=[[Q(1,2),Q(3,10),Q(0)],[Q(3,10),Q(1,2),Q(3,10)],[Q(0),Q(3,10),Q(1,2)]]
    D=[[Q(1),Q(-3,5),Q(1,3)],[Q(-3,5),Q(5,6),Q(-3,5)],[Q(1,3),Q(-3,5),Q(1)]]
    p,g,_,_=atoms(K);d=[D[i][j] for i,j in COORD];dp=[dot(v,d) for v in g]
    sel=(0,3,5,6);rem=(1,2,4,7)
    fc=sum(dp[s]**2/p[s] for s in sel)+sum(dp[s] for s in rem)**2/sum(p[s] for s in rem)
    ff=sum(dp[s]**2/p[s] for s in range(8))
    assert fc==Q(12487351,3386250) and ff==Q(56578567,1693125)
    ln=log_interval(Q(43,7));lm=log_interval(Q(625,301))
    correction=[Q(142,75)*ln[i]+Q(16,9)*lm[i] for i in range(2)]
    bc=[fc-correction[1],fc-correction[0]];bf=[ff-correction[1],ff-correction[0]]
    pa=p[7];pb=sum(p[s] for s in (1,2,4));ga=dp[7];gb=sum(dp[s] for s in (1,2,4))
    restored=(pb*ga-pa*gb)**2/(pa*pb*(pa+pb))
    b6=[fc+restored-correction[1],fc+restored-correction[0]]
    assert bc[1]<0 and bf[0]>0
    assert b6[0]>0
    cert={'D':ldl(D),'endpoint_pivots':[]}
    for t in (Q(-1,100),Q(1,100)):
        low=[[K[i][j]+t*D[i][j]-Q(i==j,1000) for j in range(3)] for i in range(3)]
        high=[[Q(i==j)-K[i][j]-t*D[i][j]-Q(i==j,1000) for j in range(3)] for i in range(3)]
        cert['endpoint_pivots'].append({'t':t,'low':ldl(low),'high':ldl(high)})
    return {'status':'EXACT_RATIONAL_LOG_CERTIFICATE_OF_SURROGATE_FAILURE_ONLY','K':K,'D':D,
            'p':p,'dp':dp,'coarse_Fisher':fc,'full_Fisher':ff,'log_terms':120,
            'log_43_over_7_interval':ln,'log_625_over_301_interval':lm,
            'coarse_B_interval':bc,'true_B_interval':bf,'coarse_B_float_interval':[float(v) for v in bc],
            'first_restored_conditional_Fisher':restored,'six_category_B_interval':b6,
            'six_category_B_float_interval':[float(v) for v in b6],
            'true_B_float_interval':[float(v) for v in bf],'feasibility':cert}
def main():
    start=time.time();rows=[]
    for t in (Q(1,100),Q(1,20),Q(1,10),Q(1,5)):
        K=[[Q(1,2) if i==j else t for j in range(3)] for i in range(3)]
        rows.append(dict(family='exchangeable_center',parameter=t,**calc(K)))
    for t in (Q(1,20),Q(1,10),Q(1,5),Q(1,4),Q(3,10),Q(1,3)):
        K=[[Q(1,2),t,Q(0)],[t,Q(1,2),t],[Q(0),t,Q(1,2)]]
        rows.append(dict(family='centered_path',parameter=t,**calc(K)))
    for theta in (Q(1,10),Q(1,2),Q(9,10)):
        u=[Q(1,3),Q(2,3),Q(2,3)]
        for exponent in (2,4,8,16,32):
            eps=Q(1,10**exponent);K=[[eps*Q(i==j)+(theta-eps)*u[i]*u[j] for j in range(3)] for i in range(3)]
            rec=calc(K,220)
            with localcontext() as ctx:
                ctx.prec=200;log=-dec(eps).ln()
                rec['capacity_divided_log']=rec['trace_capacity_test']/log
                rec['coarse_deficit_times_log']=(1-rec['coarse_rho_upper'])*log
            rows.append(dict(family='rank_one_boundary',theta=theta,exponent=exponent,**rec))
    for exponent in (2,4,8,16):
        eps=Q(1,10**exponent);theta=Q(1,2);u=[Q(1,3),Q(2,3),Q(2,3)]
        K=[[Q(i==j)-eps*Q(i==j)-(theta-eps)*u[i]*u[j] for j in range(3)] for i in range(3)]
        rows.append(dict(family='complement_boundary',theta=theta,exponent=exponent,**calc(K,220)))
    result={'status':'SCOUT_SANITY_WITH_SEPARATE_EXACT_SURROGATE_OBSTRUCTION','rows':rows,'denominator':len(rows),
            'exact_surrogate_obstruction':rational_obstruction(),
            'full_positive_count':sum(r['rho']>=1 for r in rows),'coarse_pass_count':sum(r['coarse_certificate'] for r in rows),
            'capacity_pass_count':sum(r['capacity_certificate'] for r in rows),'sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'elapsed_seconds':time.time()-start,'exit_code':0}
    (HERE/'sanity.json').write_text(json.dumps(encode(result),indent=2),encoding='utf-8')
    for r in rows:print(r['family'],r.get('parameter',r.get('exponent')),str(r['rho'])[:14],str(r['trace_capacity_test'])[:14],str(r['coarse_rho_upper'])[:14])
    print('exit=0 denominator=',len(rows))
if __name__=='__main__':main()
