"""Two-point full-event DPP entropy; real Frobenius-coordinate Hessian."""
import os
for key in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS"):
    os.environ[key]="1"
os.environ["CUDA_VISIBLE_DEVICES"]=""
import math
import numpy as np


def model(theta):
    """Stable closed form of Mobius events from a valid negative-associated law.

    Weights are (1, exp(r), exp(s), exp(r+s-L)), where L=exp(ell)>0.
    Set a=p10+p11, b=p01+p11, c^2=p10*p01-p00*p11. Then det K=p11,
    and Boolean Mobius inversion gives exactly these four event weights.
    """
    r,s,ell=theta
    L=float(np.exp(ell))
    logits=np.array([0.,r,s,r+s-L])
    weights=np.exp(logits-np.max(logits));p=weights/np.sum(weights)
    if np.min(p)<=0:
        raise FloatingPointError("underflowed event")
    a=p[1]+p[3];b=p[2]+p[3]
    u=p[1]*p[2]*(-np.expm1(-L))
    c=np.sqrt(u)
    J=np.array([[b-1,a-1,-math.sqrt(2)*c],[1-b,-a,math.sqrt(2)*c],
                [-b,1-a,math.sqrt(2)*c],[b,a,-math.sqrt(2)*c]])
    F=(J.T/p)@J
    R=np.array([[0.,1.,0.],[1.,0.,0.],[0.,0.,-1.]])
    N=F-L*R
    scales=np.sqrt(np.diag(N))
    if np.min(scales)<=0 or not np.all(np.isfinite(N)):
        raise FloatingPointError("invalid Hessian scale")
    M=N/scales[:,None]/scales[None,:]
    ew,ev=np.linalg.eigh((M+M.T)/2)
    coeff=ev[:,0]/scales;coeff/=np.linalg.norm(coeff)
    V=np.array([[coeff[0],coeff[2]/math.sqrt(2)],[coeff[2]/math.sqrt(2),coeff[1]]])
    raw_max=float(np.linalg.eigvalsh(-N)[-1])
    directional=float(-coeff@N@coeff)
    A=a*(1-a);B=b*(1-b);alpha=1-2*a;beta=1-2*b
    C=A*B-u*alpha*beta-u*u;P=float(np.prod(p))
    det_numerator=2*u+(C+4*u*u)*L-P*L**3
    return dict(theta=list(map(float,theta)),K=[[float(a),float(c)],[float(c),float(b)]],V=V.tolist(),
                events=p.tolist(),u=float(u),L=L,P=P,C=float(C),raw_max_hessian=raw_max,
                scaled_max_hessian=float(-ew[0]),scaled_eigenvalues=ew.tolist(),
                tested_directional=directional,determinant_numerator=float(det_numerator),
                log_bound_slack=float(u*u-P*L*L),matrix_scale=float(np.linalg.norm(N,2)))


def mp_review(theta,dps=90):
    import mpmath as mp
    with mp.workdps(dps):
        r,s,ell=[mp.mpf(repr(float(z))) for z in theta]
        L=mp.exp(ell)
        weights=[mp.mpf(1),mp.exp(r),mp.exp(s),mp.exp(r+s-L)]
        p=[z/sum(weights) for z in weights]
        a=p[1]+p[3];b=p[2]+p[3];u=p[1]*p[2]-p[0]*p[3];c=mp.sqrt(u)
        J=mp.matrix([[b-1,a-1,-mp.sqrt(2)*c],[1-b,-a,mp.sqrt(2)*c],
                     [-b,1-a,mp.sqrt(2)*c],[b,a,-mp.sqrt(2)*c]])
        F=J.T*mp.diag([1/z for z in p])*J
        R=mp.matrix([[0,1,0],[1,0,0],[0,0,-1]])
        H=-F+L*R
        ew,ev=mp.eigsy(H)
        coeff=ev[:,2]
        V=mp.matrix([[coeff[0],coeff[2]/mp.sqrt(2)],[coeff[2]/mp.sqrt(2),coeff[1]]])
        K=mp.matrix([[a,c],[c,b]])
        def events(k):
            q=k[0,0]*k[1,1]-k[0,1]*k[1,0]
            return [1-k[0,0]-k[1,1]+q,k[0,0]-q,k[1,1]-q,q]
        original=events(K)
        event_error=max(abs(original[j]-p[j]) for j in range(4))
        def entropy(k):
            probs=events(k)
            if min(probs)<=0:
                raise ValueError("nonpositive mp chord event")
            return -sum(z*mp.log(z) for z in probs)
        # Independent signed-determinant directional derivative.
        alt=mp.mpf(0)
        for mask in range(4):
            D=mp.diag([int(not(mask&1)),int(not(mask&2))])
            B=(K-D)**-1*V
            g=B[0,0]+B[1,1];tr=(B*B)[0,0]+(B*B)[1,1]
            alt-=p[mask]*((1+mp.log(p[mask]))*g*g-mp.log(p[mask])*tr)
        spectrum=mp.eigsy(K,eigvals_only=True)
        margin=min(spectrum[0],1-spectrum[1])
        t=mp.mpf("0.1")*margin
        gap=(entropy(K-t*V)+entropy(K+t*V))/2-entropy(K)
        def st(v):return mp.nstr(v,dps)
        return dict(dps=dps,theta=list(map(float,theta)),largest_hessian=st(ew[2]),alternate_directional=st(alt),
                    event_identity_error=st(event_error),spectral_margin=st(margin),t=st(t),gap=st(gap),
                    K=[[st(K[i,j]) for j in range(2)] for i in range(2)],
                    V=[[st(V[i,j]) for j in range(2)] for i in range(2)],
                    robust_candidate=bool(ew[2]>mp.mpf("1e-8") and alt>mp.mpf("1e-8") and gap>0))
