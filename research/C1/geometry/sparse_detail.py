from probe import *
import inspect
source=inspect.getsource(calc).replace('def calc(K):','def calc_h(K):').replace('return d*alpha,b/mp.sqrt(Z),b,min(p)','return h,g,N,M')
exec(source)
eps=mp.mpf('1e-24'); lam=mp.mpf('.7'); kap=mp.mpf(1); L=-mp.log(eps)
u0=mp.matrix([mp.sqrt(mp.mpf('.4')),mp.sqrt(mp.mpf('.6')),0]); n=mp.matrix([u0[1],-u0[0],0]); e3=mp.matrix([0,0,1])
u=mp.sqrt(1-kap*eps)*u0+mp.sqrt(kap*eps)*e3
h,g,N,M=calc_h(eps*mp.eye(3)+lam*u*u.T)
hmat=sum((h[i]*E[i] for i in range(6)),mp.zeros(3))
coords=lambda D:mp.matrix([D[0,0],D[1,1],D[2,2],D[0,1],D[0,2],D[1,2]])
R=u0*u0.T; V=u0*e3.T+e3*u0.T; Z=e3*e3.T
A=1-lam+lam*kap; rr=1+lam*kap; m=mp.log(A/(1-lam)); H=1/A+1/lam
mat=mp.matrix([[4*lam**2*kap*H+2*m,2*lam*mp.sqrt(kap)*((1-lam)/A-1)],[2*lam*mp.sqrt(kap)*((1-lam)/A-1),(1-lam)**2/A+lam]])
rhs=mp.matrix([2*lam*mp.sqrt(kap)*rr*H/m,1-rr*(1-(1-lam)/A)/m])
sol=mp.lu_solve(mat,rhs)
print(json.dumps(dict(pid=os.getpid(),hA=st((u0.T*hmat*u0)[0]*L),v=st((u0.T*hmat*e3)[0]*L/mp.sqrt(eps)),z=st(hmat[2,2]*L/eps),
    theory_v=st(sol[0]),theory_z=st(sol[1]),gA=st((g.T*coords(R))[0]),gV=st((g.T*coords(V))[0]*mp.sqrt(eps)),gZ=st((g.T*coords(Z))[0]*eps),
    theory_gA=st(-kap-rr/A+1/(1-lam)),theory_gV=st(2*mp.sqrt(kap)*rr/A),theory_gZ=st(-lam*kap/A),
    Mvv=st((coords(V).T*M*coords(V))[0]),Mvz=st((coords(V).T*M*coords(Z))[0]*mp.sqrt(eps)),Mzz=st((coords(Z).T*M*coords(Z))[0]*eps),
    mav=st((coords(R).T*M*coords(V))[0]/mp.sqrt(eps)),maz=st((coords(R).T*M*coords(Z))[0]),raw=st((g.T*h)[0]*L)),indent=2))
