"""P2 full-event entropy derivatives from inclusion-probability Mobius inversion."""
import os
for _name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_name] = "1"
os.environ["CUDA_VISIBLE_DEVICES"] = ""
from functools import lru_cache
import math
import numpy as np

BANDS = ((0.2, 0.4), (0.05, 0.2), (0.01, 0.05), (0.001, 0.01))


@lru_cache(None)
def layout(n):
    i, j = np.triu_indices(n)
    c = np.where(i == j, 0.5, 1/math.sqrt(2))
    e = np.zeros((len(i), n, n))
    for a, (r, s) in enumerate(zip(i, j)):
        e[a, r, s] += c[a]
        e[a, s, r] += c[a]
    groups = []
    for size in range(1, n+1):
        masks = [s for s in range(1, 2**n) if s.bit_count() == size]
        indices = [[k for k in range(n) if s >> k & 1] for s in masks]
        groups.append((np.array(masks), np.array(indices)))
    return i, j, c, e, groups


def mobius(x, n):
    """In-place upper Boolean-lattice Mobius transform, event axis first."""
    for bit in range(n):
        width = 1 << bit
        view = x.reshape((-1, 2, width) + x.shape[1:])
        view[:, 0] -= view[:, 1]
    return x


def inclusion_derivatives(k, second=True):
    n = len(k)
    i, j, c, e, groups = layout(n)
    q = np.ones(2**n)
    inv = np.zeros((2**n, n, n))
    for masks, idx in groups:
        sub = k[idx[:, :, None], idx[:, None, :]]
        sign, logdet = np.linalg.slogdet(sub)
        if np.any(sign <= 0):
            raise FloatingPointError("nonpositive inclusion determinant")
        q[masks] = np.exp(logdet)
        if second:
            inv[masks[:, None, None], idx[:, :, None], idx[:, None, :]] = np.linalg.inv(sub)
    if not second:
        return q
    g = 2 * c * inv[:, i, j]
    tr = 2*c[None, :, None]*c[None, None, :]*(
        inv[:, j[:, None], i[None, :]]*inv[:, i[:, None], j[None, :]]
        + inv[:, j[:, None], j[None, :]]*inv[:, i[:, None], i[None, :]])
    q1 = q[:, None]*g
    q2 = q[:, None, None]*(g[:, :, None]*g[:, None, :] - tr)
    return q, q1, q2


def events(k):
    n=len(k)
    flipped=bool(np.trace(k)>n/2)
    work=np.eye(n)-k if flipped else k
    p = mobius(inclusion_derivatives(work, second=False), n)
    if flipped:
        p=p[::-1].copy()
    if np.any(p <= 0):
        raise FloatingPointError("nonpositive Mobius event probability")
    return p


def signed_events(k):
    """Independent algebraic event formula, used only for diagnostics."""
    n = len(k)
    absent = 1-((np.arange(2**n)[:, None] >> np.arange(n)) & 1)
    a = np.broadcast_to(k, (2**n,n,n)).copy()
    a[:, np.arange(n), np.arange(n)] -= absent
    sign, lp = np.linalg.slogdet(a)
    return sign*(-1.0)**absent.sum(axis=1)*np.exp(lp), a


def entropy(k):
    p = events(k)
    return -float(p @ np.log(p))


def hessian(k):
    n = len(k)
    flipped=bool(np.trace(k)>n/2)
    work=np.eye(n)-k if flipped else k
    q, q1, q2 = inclusion_derivatives(work)
    p, p1, p2 = (mobius(a, n) for a in (q,q1,q2))
    if flipped:
        # p_K(S)=p_{I-K}(S^c); the kernel direction becomes -V.
        p=p[::-1].copy()
        p1=-p1[::-1].copy()
        p2=p2[::-1].copy()
    if np.any(p <= 0):
        raise FloatingPointError("nonpositive Mobius event probability")
    alt, _ = signed_events(k)
    rel = float(np.max(np.abs(p-alt)/np.maximum(alt, 1e-300)))
    mass = float(abs(p.sum()-1))
    dmass = float(np.max(abs(p1.sum(axis=0))))
    ddmass = float(np.max(abs(p2.sum(axis=0))))
    if rel > 1e-5 or mass > 1e-10 or dmass > 1e-8 or ddmass > 1e-7:
        raise FloatingPointError(f"event diagnostics: rel={rel}, mass={mass}, first={dmass}, second={ddmass}")
    h = -np.einsum("s,sab->ab", 1+np.log(p),p2) - (p1.T/p) @ p1
    return (h+h.T)/2, dict(complement_stabilized=flipped,event_min=float(p.min()), event_relative_error=rel,
                           mass_error=mass, first_mass_error=dmass, second_mass_error=ddmass)


def signed_directional(k,v):
    p,a = signed_events(k)
    if np.any(p <= 0):
        raise FloatingPointError("nonpositive diagnostic signed events")
    b = np.linalg.solve(a, np.broadcast_to(v,a.shape))
    g = np.trace(b,axis1=1,axis2=2)
    tr = np.einsum("sij,sji->s",b,b)
    return -float(np.sum(p*((1+np.log(p))*g*g-np.log(p)*tr)))


def sigmoid(x):
    return 1/(1+np.exp(-np.clip(x,-35,35)))


def decode(x,n,band,complement):
    e=layout(n)[3]
    raw=np.einsum("a,aij->ij",x[:-2],e)
    w,q=np.linalg.eigh(raw)
    span=w[-1]-w[0]
    if span < 1e-12:
        raise FloatingPointError("degenerate raw spectrum")
    lo,hi=BANDS[band]
    delta=lo+(hi-lo)*sigmoid(x[-2])
    width=(1-2*delta)*sigmoid(x[-1])
    lam=delta+width*(w-w[0])/span
    if complement:
        lam=1-lam
    k=(q*lam)@q.T
    k=(k+k.T)/2
    return k


def initial_x(seed,n,band,restart,scout):
    rng=np.random.default_rng(np.random.SeedSequence([seed,n,band,restart,scout]))
    e=layout(n)[3]
    q,_=np.linalg.qr(rng.normal(size=(n,n)))
    mode=scout%4
    lam=(rng.uniform(size=n) if mode==0 else rng.beta(0.4 if mode==1 else 2,
               0.4 if mode==1 else 2,size=n))
    raw=(q*lam)@q.T
    coeff=np.einsum("aij,ij->a",e,raw)
    return np.r_[coeff,rng.uniform(-2,2),rng.choice([-2.,0.,2.,5.])]


def evaluate(x,n,band,complement):
    k=decode(x,n,band,complement)
    eig=np.linalg.eigvalsh(k)
    margin=float(min(eig[0],1-eig[-1]))
    lo,hi=BANDS[band]
    if margin < lo-1e-12 or margin > hi+1e-12:
        raise FloatingPointError("spectral stratum feasibility failure")
    h,diag=hessian(k)
    w,u=np.linalg.eigh(h)
    value=float(w[-1])
    v=np.einsum("a,aij->ij",u[:,-1],layout(n)[3])
    if not np.isfinite(value):
        raise FloatingPointError("nonfinite Hessian eigenvalue")
    diag.update(max_hessian=value,spectral_margin=margin,spectrum=eig.tolist(),
                direction_frobenius=float(np.linalg.norm(v)),eigen_residual=float(np.linalg.norm(h@u[:,-1]-value*u[:,-1])))
    return value,k,v,diag


def chord(k,v):
    eig=np.linalg.eigvalsh(k)
    margin=min(eig[0],1-eig[-1])
    records=[]
    for fraction in (0.05,0.2):
        t=float(fraction*margin/np.linalg.norm(v,2))
        km,kp=k-t*v,k+t*v
        em,ep=np.linalg.eigvalsh(km),np.linalg.eigvalsh(kp)
        mm=float(min(em[0],1-em[-1])); mp=float(min(ep[0],1-ep[-1]))
        if min(mm,mp)<=0:
            raise FloatingPointError("chord endpoint is not a strict contraction")
        delta=(entropy(km)+entropy(kp))/2-entropy(k)
        records.append(dict(t=t,delta=delta,minus_margin=mm,plus_margin=mp))
    return records
