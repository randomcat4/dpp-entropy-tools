import os, sys, platform
import mpmath as mp
mp.mp.dps = 80

lam = mp.mpf('0.7')
spar = mp.mpf('0.4')

def tr(M):
    return mp.fsum([M[i,i] for i in range(M.rows)])

def mat_from_coords(q):
    x,y,z,a,b,c = q
    return mp.matrix([[x,a,b],[a,y,c],[b,c,z]])

def coords_from_mat(M):
    return [M[0,0],M[1,1],M[2,2],M[0,1],M[0,2],M[1,2]]

def outer(u,v):
    return mp.matrix([[u[i]*v[j] for j in range(3)] for i in range(3)])

def event_p(q):
    x,y,z,a,b,c = q
    q12 = x*y-a*a
    q13 = x*z-b*b
    q23 = y*z-c*c
    r = x*y*z+2*a*b*c-x*c*c-y*b*b-z*a*a
    return [1-x-y-z+q12+q13+q23-r,
            x-q12-q13+r,
            y-q12-q23+r,
            z-q13-q23+r,
            q12-r,q13-r,q23-r,r]

def event_dp(q,dq):
    x,y,z,a,b,c = q
    dx,dy,dz,da,db,dc = dq
    dq12 = y*dx+x*dy-2*a*da
    dq13 = z*dx+x*dz-2*b*db
    dq23 = z*dy+y*dz-2*c*dc
    dr = (y*z-c*c)*dx + (x*z-b*b)*dy + (x*y-a*a)*dz + (2*b*c-2*z*a)*da + (2*a*c-2*y*b)*db + (2*a*b-2*x*c)*dc
    return [-dx-dy-dz+dq12+dq13+dq23-dr,
            dx-dq12-dq13+dr,
            dy-dq12-dq23+dr,
            dz-dq13-dq23+dr,
            dq12-dr,dq13-dr,dq23-dr,dr]

def det3(M):
    return (M[0,0]*(M[1,1]*M[2,2]-M[1,2]*M[2,1])
            -M[0,1]*(M[1,0]*M[2,2]-M[1,2]*M[2,0])
            +M[0,2]*(M[1,0]*M[2,1]-M[1,1]*M[2,0]))

def K_family(eps,kappa):
    u = [mp.sqrt(spar*(1-kappa*eps)), mp.sqrt((1-spar)*(1-kappa*eps)), mp.sqrt(kappa*eps)]
    K = eps*mp.eye(3) + lam*outer(u,u)
    return K,u

def basis_mats():
    w = [mp.sqrt(spar), mp.sqrt(1-spar), mp.mpf('0')]
    n = [mp.sqrt(1-spar), -mp.sqrt(spar), mp.mpf('0')]
    e = [mp.mpf('0'),mp.mpf('0'),mp.mpf('1')]
    U = outer(w,w)
    T = outer(w,n)+outer(n,w)
    Q = outer(n,n)
    V = outer(w,e)+outer(e,w)
    W = outer(n,e)+outer(e,n)
    Z0 = outer(e,e)
    return [('U',U),('T',T),('Q',Q),('V',V),('W',W),('Z0',Z0)]

def metrics(eps,kappa):
    K,u = K_family(eps,kappa)
    q = coords_from_mat(K)
    p = event_p(q)
    dirs = basis_mats()
    dp = []
    for name,D in dirs:
        dp.append(event_dp(q, coords_from_mat(D)))
    signs = [-1,1,1,1,-1,-1,-1,1]
    F = mp.matrix(6,6)
    for i in range(6):
        for j in range(6):
            F[i,j] = mp.fsum([dp[i][r]*dp[j][r]/p[r] for r in range(8)])
    g = mp.matrix(6,1)
    for i in range(6):
        g[i] = mp.fsum([signs[r]*dp[i][r]/p[r] for r in range(8)])
    Zsum = mp.fsum([1/pi for pi in p])
    Fpair = F - (g*g.T)/Zsum
    p0,p1,p2,p3,p12,p13,p23,p123 = p
    ell12 = mp.log(p0*p12/(p1*p2))
    ell13 = mp.log(p0*p13/(p1*p3))
    ell23 = mp.log(p0*p23/(p2*p3))
    Lam = mp.log(p123*p1*p2*p3/(p0*p12*p13*p23))
    N = mp.matrix([[-ell23,0,0],[0,-ell13,0],[0,0,-ell12]]) - Lam*K
    Ninv = N**-1
    ddet = det3(N)
    eta = mp.matrix(6,1)
    G = mp.matrix(6,6)
    for i,(ni,Di) in enumerate(dirs):
        eta[i] = tr(Ninv*Di)
        for j,(nj,Dj) in enumerate(dirs):
            G[i,j] = tr(Ninv*Di*Ninv*Dj)
    M = Fpair + ddet*G
    h = M**-1 * eta
    alpha = (eta.T*h)[0]
    beta = ((g/mp.sqrt(Zsum)).T*h)[0]
    return dirs,p,F,g,Zsum,Fpair,N,Ninv,ddet,eta,G,M,h,alpha,beta

def Ccoef(kappa):
    a = 1-lam
    A = a+lam*kappa
    R = 1+lam*kappa
    m = mp.log(A/a)
    D = a+lam*lam*kappa
    J = 2*lam*kappa + m*D
    return kappa*((2*lam-1)-lam*a*m)/(a*J)

def kstar():
    return (mp.mpf(3)/7)*(mp.e**(mp.mpf(40)/21)-1)

print('PID', os.getpid())
print('PYTHON', sys.version.replace('\n',' '))
print('PLATFORM', platform.platform())
print('MPMATH', getattr(mp, '__version__', 'unknown'))
print('THREAD_ENV', {k: os.environ.get(k) for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']})
print('lam,s,kstar,C(kstar)', mp.nstr(lam,20), mp.nstr(spar,20), mp.nstr(kstar(),30), mp.nstr(Ccoef(kstar()),30))

for eps_s,kappa_s in [('1e-20','2.45'),('1e-30','2.45'),('1e-40','2.45'),('1e-30', str(kstar()))]:
    eps=mp.mpf(eps_s); kap=mp.mpf(kappa_s); L=mp.log(1/eps)
    dirs,p,F,g,Zsum,Fpair,N,Ninv,ddet,eta,G,M,h,alpha,beta = metrics(eps,kap)
    print('\nPOINT eps',eps_s,'kappa',mp.nstr(kap,18),'L',mp.nstr(L,18))
    print('p rare', [mp.nstr(p[i],12) for i in [3,5,6,7]])
    print('N det scale d/(m^2*a*L)', mp.nstr(ddet/(mp.log(((1-lam)+lam*kap)/(1-lam))**2*(1-lam)*L),20))
    print('L*gTh', mp.nstr(L*(g.T*h)[0],30),'C',mp.nstr(Ccoef(kap),30),'diff*L',mp.nstr((L*(g.T*h)[0]-Ccoef(kap))*L,20))
    print('beta scaled', mp.nstr(beta*L/(eps*mp.sqrt(lam)),30))
    print('dalpha correction L*(1-dalpha)', mp.nstr(L*(1-ddet*alpha),30),'target',mp.nstr(1/lam,30))
    print('h scaled [U,T,Q,V,W,Z0]', [mp.nstr(h[i]*([L, L**2, 1/eps, L/(mp.sqrt(eps)), L**2/(mp.sqrt(eps)), L/(eps)][i]), 12) for i in range(6)])
    names=[n for n,D in dirs]
    idx={n:i for i,n in enumerate(names)}
    checks=[('M_U_T', M[idx['U'],idx['T']]),('M_U_Q',M[idx['U'],idx['Q']]),('M_T_W',M[idx['T'],idx['W']]),('M_U_W',M[idx['U'],idx['W']]),('M_Q_V',M[idx['Q'],idx['V']]),('M_Q_W',M[idx['Q'],idx['W']]),('M_Q_Z0',M[idx['Q'],idx['Z0']])]
    for label,val in checks:
        print(label, mp.nstr(val,20))
    a0=1-lam; A=a0+lam*kap; R=1+lam*kap; m=mp.log(A/a0); D=a0+lam*lam*kap; J=2*lam*kap+m*D
    H=1/A+1/lam
    Fvv=4*lam*lam*kap*H
    Fvz=2*lam*mp.sqrt(kap)*(a0/A-1)
    Fzz=a0*a0/A+lam
    Fav=-2*mp.sqrt(kap)*R*R/A+2*mp.sqrt(kap)/a0
    Faz=R*(1-a0/A)
    A2=mp.matrix([[Fvv+2*m,Fvz],[Fvz,Fzz]])
    rhs=mp.matrix([-Fav/m,1-Faz/m])
    sol=A2**-1*rhs
    print('S11 det matrix/formula', mp.nstr((Fvv+2*m)*Fzz-Fvz*Fvz,30), mp.nstr(2*J/A,30))
    print('S11 sol v,z', mp.nstr(sol[0],30), mp.nstr(sol[1],30))
    print('actual v,z', mp.nstr(h[idx['V']]*L/mp.sqrt(eps),30), mp.nstr(h[idx['Z0']]*L/eps,30))

for eps_s in ['1e-10','1e-20','1e-30']:
    eps=mp.mpf(eps_s)
    def bfun(k):
        return metrics(eps, mp.mpf(k))[-1]
    lo=mp.mpf(1); hi=mp.mpf(10)
    flo=bfun(lo); fhi=bfun(hi)
    print('\nBRACKET eps', eps_s, 'beta1', mp.nstr(flo,12), 'beta10', mp.nstr(fhi,12))
    for _ in range(100):
        mid=(lo+hi)/2; fm=bfun(mid)
        if flo*fm<=0:
            hi=mid; fhi=fm
        else:
            lo=mid; flo=fm
    root=(lo+hi)/2
    L=mp.log(1/eps)
    dirs,p,F,g,Zsum,Fpair,N,Ninv,ddet,eta,G,M,h,alpha,beta = metrics(eps,root)
    print('ROOT eps',eps_s,'root',mp.nstr(root,30),'delta*L',mp.nstr((root-kstar())*L,30),'dalpha',mp.nstr(ddet*alpha,30),'L*(1-dalpha)',mp.nstr(L*(1-ddet*alpha),30),'beta',mp.nstr(beta,20))
