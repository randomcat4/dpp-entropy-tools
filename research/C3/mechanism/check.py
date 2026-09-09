import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key]='1'
import sys, json, platform, time
from fractions import Fraction
import numpy as np
import sympy as sp
from pathlib import Path

def realval(z):
    if abs(z.imag)>2e-10: raise ArithmeticError('nonreal jet')
    return float(z.real)

def matrices(n,c,a):
    K=np.eye(n,dtype=complex)/2
    D=np.zeros_like(K)
    for i in range(n):
        for j in range(n):
            k=i-j
            if 0<abs(k)<=len(c):
                v=c[abs(k)-1]; w=1j*a[abs(k)-1]*v
                K[i,j]=v if k>0 else v.conjugate()
                D[i,j]=w if k>0 else w.conjugate()
    return K,D,K-np.eye(n)/2

def event_jet(K,D,E):
    n=len(K); out=[]
    for mask in range(1<<n):
        signs=np.array([1 if (mask>>i)&1 else -1 for i in range(n)])
        M=signs[:,None]*K+np.diag((1-signs)/2)
        V=signs[:,None]*D; W=signs[:,None]*E
        p=realval(np.linalg.det(M))
        B=np.linalg.solve(M,V); C=np.linalg.solve(M,W)
        t=np.trace(B)
        p1=realval(p*t); p2=realval(p*(t*t-np.trace(B@B)))
        pe=realval(p*np.trace(C))
        out.append([mask,p,p1,p2,pe])
    return np.array(out)

def entropy(K):
    rows=event_jet(K,np.zeros_like(K),np.zeros_like(K))
    p=rows[:,1]
    return float(-np.dot(p,np.log(p))),p

def exact_three(c,a):
    x=sp.Rational(3,25); z=(99+20*sp.I)/101
    cs=[x,x*z]; n=3
    K=sp.eye(n)/2; D=sp.zeros(n)
    for i in range(n):
        for j in range(n):
            k=i-j
            if k:
                v=cs[abs(k)-1]; w=sp.I*a[abs(k)-1]*v
                K[i,j]=v if k>0 else sp.conjugate(v)
                D[i,j]=w if k>0 else sp.conjugate(w)
    t=sp.Symbol('t',real=True); rows=[]
    for mask in range(8):
        M=K+t*D
        for i in range(3):
            if not ((mask>>i)&1):
                for j in range(3): M[i,j]=(1 if i==j else 0)-M[i,j]
        p=sp.expand(M.det())
        rows.append({'mask':mask,'p_polynomial':str(p),'p0':str(p.subs(t,0)),
                     'p1':str(sp.diff(p,t).subs(t,0)), 'p2':str(sp.diff(p,t,2).subs(t,0))})
    # Algebraic all-three inclusion check, not a floating assertion.
    C=cs[0]**2*sp.conjugate(cs[1])
    detpoly=sp.expand((K+t*D).det())
    expected=sp.Rational(1,8)-sp.Rational(1,2)*3*x*x*(1+t*t)+2*sp.re(C*(1+sp.I*t)**3)
    assert sp.simplify(detpoly-expected)==0
    assert sum(sp.sympify(r['p0']) for r in rows)==1
    assert sum(sp.sympify(r['p1']) for r in rows)==0
    assert sum(sp.sympify(r['p2']) for r in rows)==0
    return rows

def main():
    data=json.loads(Path('input.json').read_text(encoding='utf-8-sig'))
    c=[complex(float(Fraction(data[k][0])),float(Fraction(data[k][1]))) for k in ('c1','c2')]
    a=data['phase_velocity']; n=data['window']; step=float(Fraction(data['step']))
    K,D,E=matrices(n,c,a)
    rows=event_jet(K,D,E); p,p1,p2,pe=rows[:,1:].T
    fisher=float(np.sum(p1*p1/p)); acceleration=float(-np.dot(p2,np.log(p)))
    radial=float(-np.dot(pe,np.log(p)))
    phase_acceleration=float(-np.dot(p2-pe,np.log(p)))
    h0=float(-np.dot(p,np.log(p)))
    hm,pm=entropy(K-step*D); hp,pp=entropy(K+step*D)
    # independent determinant finite differences, diagnostic only
    delta=1e-4
    hsmallm,_=entropy(K-delta*D); hsmallp,_=entropy(K+delta*D)
    hs=[]
    for s in (-delta,delta):
        cc=[v*np.exp(1j*s*w) for v,w in zip(c,a)]
        kk,_,_=matrices(n,cc,a); hs.append(entropy(kk)[0])
    np.savetxt('events_n8.csv',np.column_stack([rows,pm,pp]),delimiter=',',
        header='mask,p_center,p_first,p_second,p_radial_first,p_minus,p_plus',comments='',fmt=['%d']+['%.17g']*6)
    report={'status':'FLOATING_DIAGNOSTIC_NOT_CERTIFICATE','input':data,
      'pid':os.getpid(),'versions':{'python':sys.version,'numpy':np.__version__,'sympy':sp.__version__,'platform':platform.platform()},
      'thread_environment':{k:os.environ[k] for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS')},
      'spectral_margin_proven_lower':0.5-3*np.sqrt(17)/25,
      'fisher':fisher,'affine_acceleration':acceleration,'affine_H_second':acceleration-fisher,
      'radial_H_first':radial,'phase_acceleration':phase_acceleration,'phase_H_second':phase_acceleration-fisher,
      'affine_second_fd_delta_1e4':(hsmallm+hsmallp-2*h0)/delta**2,
      'phase_second_fd_delta_1e4':(sum(hs)-2*h0)/delta**2,
      'H_minus':hm,'H_center':h0,'H_plus':hp,'finite_gap':(hm+hp)/2-h0,
      'checks':{'sum_p':float(p.sum()),'sum_p_first':float(p1.sum()),'sum_p_second':float(p2.sum()),'sum_p_radial':float(pe.sum()),'min_event_probability':float(p.min()),'max_abs_score':float(abs(p1).max()),
                'eigenvalue_intervals':[[float(np.linalg.eigvalsh(M).min()),float(np.linalg.eigvalsh(M).max())] for M in (K-step*D,K,K+step*D)]},
      'elapsed_seconds':time.monotonic()-started}
    Path('exact_n3.json').write_text(json.dumps(exact_three(c,a),indent=2)+'\n')
    Path('output.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    started=time.monotonic()
    main()
