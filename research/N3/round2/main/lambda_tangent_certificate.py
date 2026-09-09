"""Strict finite obstruction to a pure acceleration-sign shortcut on Lambda tangents."""
from beta_probe import *
sys.path.insert(0,str(ROOT/'research/N3/main'))
import certify_score_obstruction as cert

def main():
    start=time.time()
    K=[[Q(v,100) for v in row] for row in ((50,4,6),(4,50,8),(6,8,50))]
    assert g.feasible(K)
    x=[K[i][j] for i,j in g.COORDS];p=[g.ev(f,x) for f in g.POLYS]
    jac=[[g.ev(f,x) for f in row] for row in g.GRAD]
    ell=[sum(Q((-1)**(3-s.bit_count()))*jac[s][i]/p[s] for s in range(8)) for i in range(6)]
    direction=[Q(1),Q(1),Q(1),-sum(ell[:3])/ell[3],Q(0),Q(0)]
    assert sum(a*b for a,b in zip(ell,direction))==0
    dp=[sum(a*b for a,b in zip(row,direction)) for row in jac]
    pp=[sum(g.ev(M[i][j],x)*direction[i]*direction[j] for i in range(6) for j in range(6)) for M in g.HESS]
    Fisher=sum(a*a/b for a,b in zip(dp,p));lo=Q(0);hi=Q(0)
    for acc,prob in zip(pp,p):
        l,h=cert.log_bounds(prob);coef=-acc
        lo+=coef*(l if coef>=0 else h);hi+=coef*(h if coef>=0 else l)
    assert lo>0 and Fisher-hi>0
    # Entire Rayleigh square coefficients and their t-jets, using polynomial convolution.
    def mul(a,b):
        out=[Q(0)]*(len(a)+len(b)-1)
        for i,u in enumerate(a):
            for j,v in enumerate(b):out[i+j]+=u*v
        return out
    def add(a,b):
        out=[Q(0)]*max(len(a),len(b))
        for i,v in enumerate(a):out[i]+=v
        for i,v in enumerate(b):out[i]+=v
        return out
    squares=[]
    for i,j in g.COORDS[3:]:
        k=3-i-j
        a=[K[i][j],direction[g.COORDS.index((min(i,j),max(i,j)))]]
        b=[K[i][k],direction[g.COORDS.index((min(i,k),max(i,k)))]]
        c=[K[j][k],direction[g.COORDS.index((min(j,k),max(j,k)))]]
        diag=[K[k][k],direction[k]]
        intercept=add(mul(a,diag),[-v for v in mul(b,c)])
        # Delta_ij(det(diag(z)+K(t)))=(a(t) z_k + intercept(t))^2.
        squares.append(dict(pair=[i,j],root_z_coefficient=a,root_constant=intercept,
                            z2_coeff=mul(a,a),z1_coeff=[2*v for v in mul(a,intercept)],
                            z0_coeff=mul(intercept,intercept)))
    report=dict(status='EXACT_SIGN_SHORTCUT_OBSTRUCTION_NOT_B0_COUNTEREXAMPLE',K=K,direction=direction,
                Lambda_direction_derivative='0',Fisher=Fisher,cofactor_interval=cert.compact(lo,hi),
                true_B_interval=cert.compact(Fisher-hi,Fisher-lo),rayleigh_squares=squares,
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                dependency_sha256=hashlib.sha256((HERE/'beta_probe.py').read_bytes()).hexdigest(),
                pid=os.getpid(),threads=1,seed=None,deterministic=True,executed_centers=1,
                command='python research/N3/round2/main/lambda_tangent_certificate.py',elapsed_seconds=time.time()-start,exit_code=0)
    (HERE/'lambda_tangent_certificate.json').write_text(json.dumps(g.encode(report),indent=2)+'\n')
    print(json.dumps(g.encode({k:v for k,v in report.items() if k!='rayleigh_squares'}),indent=2),flush=True)
if __name__=='__main__':main()
