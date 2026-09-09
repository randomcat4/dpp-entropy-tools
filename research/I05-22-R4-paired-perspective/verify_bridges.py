"""I05-22 R4: new exact identities, not a proof of Shannon concavity.
Run: python verify_bridges.py --out outputs
Python 3.11+, SymPy 1.14.0. No network, old verifier, or private input.
"""
import argparse, json, itertools, pathlib, time
import sympy as s

def atoms(K):
    n=K.rows; inc=[]
    for mask in range(1<<n):
        ids=[i for i in range(n) if mask>>i&1]
        inc.append(K.extract(ids,ids).det() if ids else s.Integer(1))
    return [s.expand(sum((-1)**(t.bit_count()-mask.bit_count())*inc[t]
                        for t in range(1<<n) if t&mask==mask))
            for mask in range(1<<n)]

def zero(expr):
    assert s.cancel(expr)==0, str(expr)

def matrix_zero(M):
    for entry in M: zero(entry)

def blocks(x,y,A,B,ell,k,lam,n,J):
    v=x*(1-x); w=y*(1-y); mu=2*x-1; nu=2*y-1
    L=s.Matrix([[A*ell/(2*v),J],[J,B*k/(2*w)]])
    C=s.Matrix([[-ell,mu*ell/2,w*lam,-w*lam*mu/2],
                [-k,v*lam,nu*k/2,-v*lam*nu/2]])
    R=s.zeros(4)
    R[1,1]=v*ell/(2*A);R[2,2]=w*k/(2*B);R[3,3]=v*w*n/(2*A*B)
    R[1,3]=R[3,1]=-v*w*lam/(2*A)
    R[2,3]=R[3,2]=-v*w*lam/(2*B)
    return L,C,R

def run():
    results={}; start=time.monotonic()
    x,y,z,a,b,c,t,scale=s.symbols('x y z a b c t scale')
    d,e,j,h,k,l=s.symbols('d e j h k l')
    K=s.Matrix([[x,a,b],[a,y,c],[b,c,z]])
    D=s.Matrix([[d,h,k],[h,e,l],[k,l,j]])
    allp=atoms(K+t*D)
    zero(sum(allp)-1)
    P=[allp[i]+allp[i+4] for i in range(4)]
    r=allp[4:]
    v=x*(1-x);w=y*(1-y)
    for idx in range(4):
        i=idx&1; jj=idx>>1
        phi=(i-x)/v;psi=(jj-y)/w
        ref=j+b*b*d*phi*phi+c*c*e*psi*psi-2*b*k*phi-2*c*l*psi+2*b*c*h*phi*psi
        actual=s.diff(r[idx]/P[idx],t).subs({t:0,a:0})
        zero(actual-ref)
        zero(s.diff(P[idx],t,2).subs({t:0,a:0})-2*(d*e-h*h)*(-1)**(i+jj))
    results['all_eight_event_conditional_jets']='PASS'
    # Coefficient identity, without treating transcendental logs as indeterminates incorrectly.
    L00,L10,L01,L11=s.symbols('L00 L10 L01 L11')
    lam=L00-L10-L01+L11
    lhs=sum(s.diff(r[i],t,2).subs(t,0)*L for i,L in enumerate([L00,L10,L01,L11]))
    rhs=-2*(L00-L01)*(e*j-l*l)-2*(L00-L10)*(d*j-k*k)+2*lam*s.trace(K*D.adjugate())
    zero(lhs-rhs)
    # At an arrow center the perspective P'' term cancels for phi(t)=t log t.
    cond=[z-b*b*((i-x)/v)-c*c*((jj-y)/w) for jj in range(2) for i in range(2)]
    zero(sum(2*(d*e-h*h)*(-1)**((i&1)+(i>>1))*cond[i] for i in range(4)))
    results['one_sided_cofactor_formula']='PASS'
    S=s.diag(1,1,scale)
    scaled=atoms(S*K*S)
    orig=atoms(K)
    for i in range(4):
        zero(scaled[i+4]-scale**2*orig[i+4])
        zero(scaled[i]+scaled[i+4]-orig[i]-orig[i+4])
    results['kernel_congruence_scale_identity']='PASS'
    # Verify the complete log block in conditional-score coordinates, with generic arrow N.
    m,f,g,hc,ell,kap,la,nn=s.symbols('m f g hc ell kap la nn')
    A=b*b/v;B=c*c/w;mu=2*x-1;nu=2*y-1
    Dc=s.Matrix([[d,b*c*hc/(2*A*B),b*((1-2*x)*d/v-f/A)/2],
                 [b*c*hc/(2*A*B),e,c*((1-2*y)*e/w-g/B)/2],
                 [b*((1-2*x)*d/v-f/A)/2,c*((1-2*y)*e/w-g/B)/2,m-A*d-B*e]])
    N=s.Matrix([[kap,0,-la*b],[0,ell,-la*c],[-la*b,-la*c,nn]])
    JJ=A*kap+B*ell-nn+la*(A*mu+B*nu)
    LL,CC,RR=blocks(x,y,A,B,ell,kap,la,nn,JJ)
    dd=s.Matrix([d,e]);tt=s.Matrix([m,f,g,hc])
    expr=-2*s.trace(N*Dc.adjugate())-(dd.T*LL*dd)[0]-2*(dd.T*CC*tt)[0]-(tt.T*RR*tt)[0]
    matrix_zero(s.hessian(expr,[d,e,m,f,g,hc]))
    V=s.Matrix([[0,-c/(2*B),0],[-b/(2*A),0,0],[0,0,-b*c/(2*A*B)]])
    matrix_zero(RR[1:,1:]-2*V.T*N*V)
    results['six_direction_LCR_and_positive_edge_congruence']='PASS'
    # Squared perspective sum: exact full Hessian and complete squares.
    AA,BB=s.symbols('A B',positive=True)
    D33=m-AA*d-BB*e
    d13sq=AA*v*((1-2*x)*d/v-f/AA)**2/4
    d23sq=BB*w*((1-2*y)*e/w-g/BB)**2/4
    d12sq=v*w*hc**2/(4*AA*BB)
    quad=2*(m*m+v*f*f+w*g*g+v*w*hc*hc)-4*AA*(d*D33-d13sq)-4*BB*(e*D33-d23sq)-4*AA*BB*(d*e-d12sq)
    squares=2*(m-AA*d-BB*e)**2+3*v*(f+AA*mu*d/(3*v))**2+3*w*(g+BB*nu*e/(3*w))**2+2*AA**2*(1-v)*d*d/(3*v)+2*BB**2*(1-w)*e*e/(3*w)+3*v*w*hc*hc
    zero(quad-squares)
    results['quadratic_perspective_full_six_squares']='PASS'
    # Algebra of the complete four-point Gram inverse, at general positive table weights.
    a00,a10,a01,a11=s.symbols('a00 a10 a01 a11',nonzero=True)
    rows=[];probs=[]
    for jj in range(2):
        for i in range(2):
            rows.append([1,i-x,jj-y,(i-x)*(jj-y)])
            probs.append((x if i else 1-x)*(y if jj else 1-y))
    E=s.Matrix(rows);PP=s.diag(*probs);DD=s.diag(1,v,w,v*w)
    matrix_zero(E.T*PP*E-DD)
    matrix_zero(E*DD.inv()*E.T-PP.inv())
    # These two identities imply F_w^{-1}=D^{-1}E^T diag(P/w) E D^{-1}
    # for all positive w; no entrywise inverse is substituted for a matrix inverse.
    results['complete_Gram_inverse_basis_identity']='PASS'
    # Generic noncommuting 2x2 test is an algebra transport check, not the proof.
    U=s.Matrix([[3,1],[1,2]]);Vv=s.Matrix([[2,-1],[-1,4]])
    Ca=s.Matrix([[1,2,0,-1],[3,0,1,2]]);Cb=s.Matrix([[0,1,2,0],[1,-1,0,3]])
    par=(U.inv()+Vv.inv()).inv();diff=U.inv()*Ca-Vv.inv()*Cb
    matrix_zero(Ca.T*U.inv()*Ca+Cb.T*Vv.inv()*Cb-(Ca+Cb).T*(U+Vv).inv()*(Ca+Cb)-diff.T*par*diff)
    results['parallel_sum_transport_fixture']='PASS; universal proof is in proof.md'
    results['seconds']=round(time.monotonic()-start,4)
    return results

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='outputs');args=ap.parse_args()
    result=run();out=pathlib.Path(args.out);out.mkdir(parents=True,exist_ok=True)
    (out/'bridge_checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2));print('ALL NEW EXACT BRIDGE CHECKS PASSED')
