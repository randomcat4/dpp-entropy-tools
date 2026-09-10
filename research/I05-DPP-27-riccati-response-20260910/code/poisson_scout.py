#!/usr/bin/env python3
"""Non-rigorous polynomial scout for the three-Poisson certificate.
No sampled residual is a supremum certificate. No h'' sign is asserted.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
os.environ.setdefault('OMP_NUM_THREADS','1')
import numpy as np
import json, sys, time
from pathlib import Path
from datetime import datetime, timezone


def powers(deg):
    return [(i,j,k) for d in range(1,deg+1) for i in range(d+1)
            for j in range(d-i+1) for k in [d-i-j]]

def features(Q, exponents, J=None, H=None):
    X=8*Q; deg=max(sum(a) for a in exponents)
    N=len(X); P=len(exponents)
    pw=[np.stack([X[:,d]**k for k in range(deg+1)],axis=1) for d in range(3)]
    V=np.empty((N,P)); D=np.zeros_like(V) if J is not None else None
    DD=np.zeros_like(V) if H is not None else None
    if J is not None: J=8*J
    if H is not None: H=8*H
    for k,e in enumerate(exponents):
        V[:,k]=pw[0][:,e[0]]*pw[1][:,e[1]]*pw[2][:,e[2]]
        if J is None: continue
        for i in range(3):
            if not e[i]: continue
            ei=list(e); ei[i]-=1
            part=e[i]*pw[0][:,ei[0]]*pw[1][:,ei[1]]*pw[2][:,ei[2]]
            D[:,k]+=part*J[:,i]
            if H is None: continue
            DD[:,k]+=part*H[:,i]
            for j in range(3):
                if not ei[j]: continue
                eij=ei.copy(); eij[j]-=1
                DD[:,k]+=(e[i]*ei[j]*pw[0][:,eij[0]]*pw[1][:,eij[1]]*
                          pw[2][:,eij[2]]*J[:,i]*J[:,j])
    return V,D,DD


def data(Q,t,exponents, need_dd=True):
    N=len(Q); q=t/16
    E=np.array([[.125,0],[q,.125]])
    C=np.array([[0.,0.],[1/16,0.]])
    Vmat=np.array([[0.,1/16],[1/16,0.]])
    g=np.empty((N,4)); gt=g.copy(); gtt=g.copy()
    T=np.empty((N,4,3)); Tt=T.copy(); Ttt=T.copy()
    for k,(a,b) in enumerate(((-1,-1),(-1,1),(1,-1),(1,1))):
        u=a/2-Q[:,0]; v=b/2-Q[:,1]; w=q-Q[:,2]
        det=u*v-w*w
        g[:,k]=a*b*det; gt[:,k]=-a*b*w/8; gtt[:,k]=-a*b/128
        R=np.empty((N,2,2)); R[:,0,0]=v/det; R[:,1,1]=u/det
        R[:,0,1]=R[:,1,0]=-w/det
        Rp=-R@Vmat@R; Rpp=2*R@Vmat@R@Vmat@R
        Ts=E@R@E.T
        Tds=C@R@E.T+E@R@C.T+E@Rp@E.T
        Tdds=2*C@R@C.T+2*C@Rp@E.T+2*E@Rp@C.T+E@Rpp@E.T
        for Z,M in ((T,Ts),(Tt,Tds),(Ttt,Tdds)):
            Z[:,k,0]=M[:,0,0]; Z[:,k,1]=M[:,1,1]; Z[:,k,2]=M[:,0,1]
    if not np.all(g>0): raise ValueError('nonpositive scout probability')
    BT=-np.sum(gt*np.log(g),axis=1)
    B=-np.sum(g*np.log(g),axis=1)
    BTT=-np.sum(gt*gt/g+gtt*np.log(g),axis=1)
    F,Ft,Ftt=features(T.reshape(-1,3),exponents,Tt.reshape(-1,3),Ttt.reshape(-1,3))
    P=F.shape[1]; F=F.reshape(N,4,P); Ft=Ft.reshape(N,4,P); Ftt=Ftt.reshape(N,4,P)
    LF=np.einsum('na,nap->np',g,F)
    L1F=np.einsum('na,nap->np',gt,F)+np.einsum('na,nap->np',g,Ft)
    L2F=(np.einsum('na,nap->np',gtt,F)+2*np.einsum('na,nap->np',gt,Ft)+
         np.einsum('na,nap->np',g,Ftt))
    V,_,_=features(Q,exponents)
    return V-LF,L1F,L2F,B,BT,BTT


def sample(rng,n):
    Q=rng.normal(size=(n,3)); Q[:,2]/=np.sqrt(2)
    cen=(Q[:,0]+Q[:,1])/2
    rad=np.sqrt(((Q[:,0]-Q[:,1])/2)**2+Q[:,2]**2)
    norm=np.maximum(abs(cen+rad),abs(cen-rad))
    radius=rng.random(n)**(1/3)
    radius[::4]=1  # deliberately retain boundary points
    Q*=((radius/8)/norm)[:,None]
    Q[0,:]=0
    return Q


def residual(Q,t,ex,sol):
    D,L1,L2,B,Bt,Btt=data(Q,t,ex)
    c0,u,c1,v,c2,w=sol
    r0=B-c0-D@u
    r1=Bt+L1@u-c1-D@v
    r2=Btt+L2@u+2*L1@v-c2-D@w
    return np.stack((r0,r1,r2),axis=1)


def main(degree=6):
    start=time.monotonic(); rng=np.random.default_rng(270074)
    t=1.25; ntrain=1800; ntest=600
    ex=powers(degree); Q=sample(rng,ntrain)
    D,L1,L2,B,Bt,Btt=data(Q,t,ex)
    M=np.column_stack((np.ones(ntrain),D))
    su=np.linalg.lstsq(M,B,rcond=1e-12)[0]; c0,u=su[0],su[1:]
    sv=np.linalg.lstsq(M,Bt+L1@u,rcond=1e-12)[0]; c1,v=sv[0],sv[1:]
    sw=np.linalg.lstsq(M,Btt+L2@u+2*L1@v,rcond=1e-12)[0]; c2,w=sw[0],sw[1:]
    sol=(c0,u,c1,v,c2,w); X=sample(rng,ntest)
    rr=residual(X,t,ex,sol); eps=1/2048
    gr=np.zeros((ntest,3,2)); hess=np.zeros((ntest,3,3))
    # Finite differences in an orthonormal symmetric-matrix basis; DIAGNOSTIC ONLY.
    basis=np.diag([1.,1.,1/np.sqrt(2)])
    for i in range(3):
        p=residual(X+eps*basis[i],t,ex,sol)
        m=residual(X-eps*basis[i],t,ex,sol)
        gr[:,i,:]=(p[:,:2]-m[:,:2])/(2*eps)
        hess[:,i,i]=(p[:,0]+m[:,0]-2*rr[:,0])/eps**2
        for j in range(i):
            pp=residual(X+eps*basis[i]+eps*basis[j],t,ex,sol)[:,0]
            pm=residual(X+eps*basis[i]-eps*basis[j],t,ex,sol)[:,0]
            mp=residual(X-eps*basis[i]+eps*basis[j],t,ex,sol)[:,0]
            mm=residual(X-eps*basis[i]-eps*basis[j],t,ex,sol)[:,0]
            hess[:,i,j]=hess[:,j,i]=(pp-pm-mp+mm)/(4*eps**2)
    e01=np.max(np.linalg.norm(gr[:,:,0],axis=1))
    e11=np.max(np.linalg.norm(gr[:,:,1],axis=1))
    e02=np.max(np.linalg.norm(hess,ord=2,axis=(1,2)))
    e20=np.max(abs(rr[:,2]))
    result={'status':'SCOUT_ONLY_NOT_A_CERTIFICATE', 'utc':datetime.now(timezone.utc).isoformat(),
            'elapsed_seconds':time.monotonic()-start,'numpy':np.__version__,
            't':'5/4','degree':degree,'basis':'(8Q11)^i(8Q22)^j(8Q12)^k; nonconstant total degree',
            'seed':270074,'train_points':ntrain,'test_points':ntest,'finite_difference_step':'1/2048',
            'candidate_h_second':float(c2/2),'sampled_e01':float(e01),'sampled_e02':float(e02),
            'sampled_e11':float(e11),'sampled_e20':float(e20),
            'invalid_as_certificate_sampled_budget':float(13*e01+e02/8+6*e11/5+e20/2),
            'sampled_value_residuals':np.max(abs(rr),axis=0).tolist(),
            'missing':['outward arithmetic','continuum residual suprema','parameter-interval coverage'],
            'coefficients':{'exponents':ex,'c0':float(c0),'u':u.tolist(),'c1':float(c1),'v':v.tolist(),
                            'c2':float(c2),'w':w.tolist()}}
    path=Path(__file__).with_name(f'scout_degree{degree}.json')
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='coefficients'},indent=2))

if __name__=='__main__': main(int(sys.argv[1]) if len(sys.argv)>1 else 6)
