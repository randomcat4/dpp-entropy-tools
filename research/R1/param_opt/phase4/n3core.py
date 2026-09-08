"""Connected n=3 DPP kernels and Mobius entropy jets in six real directions."""
import os
for key in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS"):
    os.environ[key]="1"
os.environ["CUDA_VISIBLE_DEVICES"]=""
import math
import numpy as np

PAIRS=((0,1),(0,2),(1,2))
E=np.zeros((6,3,3))
for i in range(3):E[i,i,i]=1
for z,(i,j) in enumerate(PAIRS,3):E[z,i,j]=E[z,j,i]=1/math.sqrt(2)

def mobius(x):
    for bit in range(3):
        for mask in range(8):
            if not(mask>>bit&1):x[mask]-=x[mask|1<<bit]
    return x

def jets(k):
    """Exact degree<=3 inclusion polynomials, then Boolean Mobius inversion."""
    dt=np.longdouble
    k=np.asarray(k,dtype=dt)
    flipped=bool(np.trace(k)>dt(1.5))
    if flipped:k=np.eye(3,dtype=dt)-k
    a,b,d=np.diag(k);c,e,f=k[0,1],k[0,2],k[1,2]
    rt=dt(2)**dt(.5)
    q=np.ones(8,dtype=dt);g=np.zeros((8,6),dtype=dt);h=np.zeros((8,6,6),dtype=dt)
    for mask,i in ((1,0),(2,1),(4,2)):
        q[mask]=k[i,i];g[mask,i]=1
    for mask,i,j,z in ((3,0,1,3),(5,0,2,4),(6,1,2,5)):
        q[mask]=k[i,i]*k[j,j]-k[i,j]**2
        g[mask,i]=k[j,j];g[mask,j]=k[i,i];g[mask,z]=-rt*k[i,j]
        h[mask,i,j]=h[mask,j,i]=1;h[mask,z,z]=-1
    q[7]=a*b*d+2*c*e*f-a*f*f-b*e*e-d*c*c
    g[7]=[b*d-f*f,a*d-e*e,a*b-c*c,rt*(e*f-d*c),rt*(c*f-b*e),rt*(c*e-a*f)]
    for i,j,v in ((0,1,d),(0,2,b),(1,2,a),(0,5,-rt*f),(1,4,-rt*e),(2,3,-rt*c),
                  (3,4,f),(3,5,e),(4,5,c)):
        h[7,i,j]=h[7,j,i]=v
    h[7,3,3]=-d;h[7,4,4]=-b;h[7,5,5]=-a
    p,p1,p2=mobius(q),mobius(g),mobius(h)
    if flipped:p,p1,p2=p[::-1].copy(),-p1[::-1].copy(),p2[::-1].copy()
    return p,p1,p2,flipped

def signed_probs(k):
    probs=[]
    for mask in range(8):
        absent=np.array([not(mask>>i&1) for i in range(3)],int)
        sign,lp=np.linalg.slogdet(k-np.diag(absent))
        probs.append(sign*((-1)**int(sum(absent)))*np.exp(lp))
    return np.array(probs)

def hessian(k):
    p,g,p2,flipped=jets(k)
    if np.min(p)<=0:raise FloatingPointError("nonpositive polynomial-Mobius event")
    mass=float(abs(p.sum()-1));m1=float(np.max(abs(g.sum(axis=0))));m2=float(np.max(abs(p2.sum(axis=0))))
    if max(mass,m1,m2)>1e-10:raise FloatingPointError("event jet mass failure")
    F=(g.T/p)@g
    H=-F-np.einsum("s,sab->ab",1+np.log(p),p2)
    H=(H+H.T)/2
    H64=np.array(H,dtype=float)
    # A global positive floor prevents division by a roundoff-sized flat diagonal.
    # Congruence still preserves inertia; reported physical curvature is unscaled.
    floor=max(np.max(abs(H))*np.longdouble('1e-12'),np.longdouble('1e-280'))
    scales=np.sqrt(np.maximum(np.maximum(abs(np.diag(H)),np.diag(F)),floor))
    scaled=np.array(H/scales[:,None]/scales[None,:],dtype=float)
    w,q=np.linalg.eigh(scaled)
    coeff=np.asarray(q[:,-1]/scales,dtype=float);coeff/=np.linalg.norm(coeff)
    v=np.einsum("a,aij->ij",coeff,E)
    raw=np.linalg.eigvalsh(H64)[-1]
    directional=float(np.asarray(coeff,dtype=np.longdouble)@H@np.asarray(coeff,dtype=np.longdouble))
    alt=signed_probs(np.asarray(k,dtype=float))
    rel=float(np.max(abs(np.asarray(p,dtype=float)-alt)/np.maximum(abs(alt),1e-300)))
    norm=float(np.linalg.norm(H64,2))
    return dict(raw_max_hessian=float(raw),scaled_max_hessian=float(w[-1]),directional=directional,V=v.tolist(),
                event_min=float(p.min()),event_probabilities=[float(z) for z in p],complement_stabilized=flipped,
                mass_error=mass,first_mass_error=m1,second_mass_error=m2,signed_event_relative_difference=rel,
                hessian_norm=norm,raw_roundoff_scale=float(np.finfo(np.longdouble).eps)*max(1,norm),
                longdouble_bits=int(np.finfo(np.longdouble).nmant+1))

def decode(x,kind,signs,orientation):
    # Affine spectral normalization preserves exact missing path edges.
    raw=np.diag(x[:3]).astype(float)
    logs=x[3:6]
    for j,(r,s) in enumerate(PAIRS):
        val=0. if kind=="path" and j==1 else signs[j]*np.exp(np.clip(logs[j],-30,4))
        raw[r,s]=raw[s,r]=val
    eig=np.linalg.eigvalsh(raw);span=eig[-1]-eig[0]
    if span<=1e-14:raise FloatingPointError("collapsed raw spectrum")
    margin=np.exp(np.clip(x[6],np.log(1e-12),np.log(.25)))
    width=(1-2*margin)/(1+np.exp(-np.clip(x[7],-18,18)))
    k=margin*np.eye(3)+width*(raw-eig[0]*np.eye(3))/span
    if orientation:k=np.eye(3)-k
    return (k+k.T)/2

def evaluate(x,kind,signs,orientation):
    k=decode(x,kind,signs,orientation)
    eig=np.linalg.eigvalsh(k);margin=float(min(eig[0],1-eig[-1]))
    if margin<=0:raise FloatingPointError("nonpositive spectral margin")
    edges=[k[i,j]!=0 for i,j in PAIRS]
    if sum(edges)<2:raise FloatingPointError("disconnected center")
    obj=hessian(k)
    obj.update(K=k.tolist(),parameters=list(map(float,x)),kind=kind,signs=list(map(int,signs)),orientation=int(orientation),
               spectral_margin=margin,spectrum=eig.tolist(),edge_magnitudes=[float(abs(k[i,j])) for i,j in PAIRS])
    return obj

def sample(seed,idx):
    rng=np.random.default_rng(np.random.SeedSequence([seed,idx]))
    group=idx%4
    kind="path" if group%2==0 else "triangle"
    x=np.r_[rng.uniform(-2,2,3),rng.uniform(-4,1,3),rng.uniform(np.log(1e-12),np.log(.25)),rng.uniform(-6,18)]
    if group>=2:
        # Connected but very close to a 1+2 block decomposition.
        x[3]=rng.uniform(-28,-10)
        if kind=="triangle":x[4]=rng.uniform(-28,-10)
    signs=rng.choice([-1,1],3)
    return x,kind,signs,int(rng.integers(2))

def mp_review(k_strings,dps=90):
    import mpmath as mp
    with mp.workdps(dps):
        K=mp.matrix([[mp.mpf(str(z)) for z in row] for row in k_strings])
        spectrum=mp.eigsy(K,eigvals_only=True);margin=min(spectrum[0],1-spectrum[2])
        if margin<=0:raise ValueError("fixed decimal kernel infeasible")
        basis=[]
        for i in range(3):
            e=mp.zeros(3);e[i,i]=1;basis.append(e)
        for i,j in PAIRS:
            e=mp.zeros(3);e[i,j]=e[j,i]=1/mp.sqrt(2);basis.append(e)
        p=[mp.mpf(1)]*8;g=[[mp.mpf(0) for j in range(6)] for i in range(8)]
        hh=[mp.zeros(6) for _ in range(8)]
        for mask in range(1,8):
            ids=[i for i in range(3) if mask>>i&1]
            sub=mp.matrix([[K[i,j] for j in ids] for i in ids]);p[mask]=mp.det(sub);inv=sub**-1
            mats=[inv*mp.matrix([[e[i,j] for j in ids] for i in ids]) for e in basis]
            traces=[sum(m[i,i] for i in range(len(ids))) for m in mats]
            g[mask]=[p[mask]*tr for tr in traces]
            for i in range(6):
                for j in range(6):
                    prod=mats[i]*mats[j]
                    hh[mask][i,j]=p[mask]*(traces[i]*traces[j]-sum(prod[z,z] for z in range(len(ids))))
        for bit in range(3):
            for mask in range(8):
                if not(mask>>bit&1):
                    other=mask|1<<bit;p[mask]-=p[other]
                    for j in range(6):g[mask][j]-=g[other][j]
                    hh[mask]-=hh[other]
        if min(p)<=0:raise ValueError("nonpositive high-precision Mobius event")
        H=mp.zeros(6)
        for s in range(8):
            gv=mp.matrix(g[s]);H-=(1+mp.log(p[s]))*hh[s]+gv*gv.T/p[s]
        ew,ev=mp.eigsy(H);coef=ev[:,5];V=mp.zeros(3)
        for j in range(6):V+=coef[j]*basis[j]
        alt=mp.mpf(0)
        for mask in range(8):
            A=K-mp.diag([int(not(mask>>i&1)) for i in range(3)])
            B=A**-1*V;tr=sum(B[i,i] for i in range(3));BB=B*B;tr2=sum(BB[i,i] for i in range(3))
            alt-=p[mask]*((1+mp.log(p[mask]))*tr*tr-mp.log(p[mask])*tr2)
        def entropy(k):
            pp=[mp.mpf(1)]*8
            for mask in range(1,8):
                ids=[i for i in range(3) if mask>>i&1]
                pp[mask]=mp.det(mp.matrix([[k[i,j] for j in ids] for i in ids]))
            for bit in range(3):
                for mask in range(8):
                    if not(mask>>bit&1):pp[mask]-=pp[mask|1<<bit]
            if min(pp)<=0:raise ValueError("infeasible entropy chord")
            return -sum(z*mp.log(z) for z in pp)
        vnorm=max(abs(z) for z in mp.eigsy(V,eigvals_only=True))
        chords=[]
        for fraction in ("0.01","0.05","0.2"):
            t=mp.mpf(fraction)*margin/vnorm
            gap=(entropy(K-t*V)+entropy(K+t*V))/2-entropy(K)
            chords.append(dict(t=mp.nstr(t,dps),gap=mp.nstr(gap,dps)))
        return dict(dps=dps,largest_hessian=mp.nstr(ew[5],dps),alternate_directional=mp.nstr(alt,dps),
                    spectral_margin=mp.nstr(margin,dps),event_min=mp.nstr(min(p),dps),
                    K=[[mp.nstr(K[i,j],dps) for j in range(3)] for i in range(3)],
                    V=[[mp.nstr(V[i,j],dps) for j in range(3)] for i in range(3)],chords=chords,
                    positive_gate=bool(ew[5]>mp.mpf("1e-8") and alt>mp.mpf("1e-8") and any(mp.mpf(z["gap"])>0 for z in chords)))
