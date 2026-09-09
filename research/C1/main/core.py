"""C1 direct eight-atom reconstruction; six real symmetric coordinates.

This numerical module is a diagnostic, never an interval certificate.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
os.environ.setdefault('OMP_NUM_THREADS','1')
import itertools
import numpy as np

PAIRS=[(0,0),(1,1),(2,2),(0,1),(0,2),(1,2)]
E=np.zeros((6,3,3))
for k,(i,j) in enumerate(PAIRS): E[k,i,j]=E[k,j,i]=1
SIG=np.array([(-1)**(3-s.bit_count()) for s in range(8)])
STAT=np.array([[int(s>>i&1) for i in range(3)]+[int((s>>i&1) and (s>>j&1)) for i,j in PAIRS[3:]] for s in range(8)])

def det3(A):
    return (A[0,0]*(A[1,1]*A[2,2]-A[1,2]*A[2,1])
          - A[0,1]*(A[1,0]*A[2,2]-A[1,2]*A[2,0])
          + A[0,2]*(A[1,0]*A[2,1]-A[1,1]*A[2,0]))

def atoms(K):
    """Differentiate permutation expansion, not inverse determinants."""
    p=np.zeros(8); J=np.zeros((8,6)); Q=np.zeros((8,6,6))
    for s in range(8):
        A=K-np.diag([1-int(s>>i&1) for i in range(3)])
        for perm in itertools.permutations(range(3)):
            sign=SIG[s]*(-1)**sum(perm[i]>perm[j] for i in range(3) for j in range(i+1,3))
            val=np.array([A[i,perm[i]] for i in range(3)])
            der=np.array([E[:,i,perm[i]] for i in range(3)])
            p[s]+=sign*np.prod(val)
            for r in range(3):
                J[s]+=sign*der[r]*np.prod(np.delete(val,r))
                for t in range(3):
                    if r!=t: Q[s]+=sign*np.outer(der[r],der[t])*val[3-r-t]
    return p,J,Q

def data(K,full=True):
    K=np.asarray(K,dtype=float); p,J,Q=atoms(K)
    if min(p)<=0: raise ValueError('nonpositive event')
    F=J.T@(J/p[:,None]); logp=np.log(p)
    g=J.T@(SIG/p); Z=np.sum(1/p); v=g/np.sqrt(Z)
    ell=np.array([logp[0]+logp[6]-logp[2]-logp[4],logp[0]+logp[5]-logp[1]-logp[4],logp[0]+logp[3]-logp[1]-logp[2]])
    lam=SIG@logp; N=-np.diag(ell)-lam*K
    d=det3(N); W=np.linalg.inv(N)
    eta=np.einsum('ij,kji->k',W,E)
    G=np.array([[np.trace(W@e@W@f) for f in E] for e in E])
    Fpair=F-np.outer(v,v); M=Fpair+d*G
    h=np.linalg.solve(M,eta); alpha=eta@h; beta=v@h
    dm=h/alpha; B=F+np.einsum('s,sij->ij',logp,Q)
    out=dict(p=p,J=J,Q=Q,F=F,g=g,Z=Z,v=v,ell=ell,Lambda=lam,N=N,d=d,eta=eta,G=G,Fpair=Fpair,M=M,alpha=alpha,beta=beta,dalpha=d*alpha,dm=dm,B=B,
             D=np.einsum('k,kij->ij',dm,E),Hpp=-dm@B@dm)
    if full:
        means=p@STAT; C=STAT.T@(p[:,None]*STAT)-np.outer(means,means)
        jm=STAT.T@J
        out.update(Cov=C,Jmom=jm,Fpair_cov=jm.T@np.linalg.solve(C,jm),
          identity_residual=np.max(abs(B-(F+d*G-d*np.outer(eta,eta)))),
          pair_residual=np.max(abs(Fpair-jm.T@np.linalg.solve(C,jm))))
    return out
