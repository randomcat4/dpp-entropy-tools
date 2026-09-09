from independent_sparse_check import metrics, Ccoef, lam
import mpmath as mp
mp.mp.dps = 80
for eps_s in ['1e-20','1e-30','1e-40']:
    eps=mp.mpf(eps_s); L=mp.log(1/eps)
    for kap_s in ['1','4','10']:
        kap=mp.mpf(kap_s)
        *_,g,Zsum,Fpair,N,Ninv,ddet,eta,G,M,h,alpha,beta = metrics(eps,kap)
        # above starred unpack is wrong if relied on names, so recompute by positions below in robust form
        vals = metrics(eps,kap)
        g=vals[3]; h=vals[12]; alpha=vals[13]; beta=vals[14]; ddet=vals[8]
        print('CHECK', eps_s, kap_s, 'L*gTh', mp.nstr(L*(g.T*h)[0],20), 'C', mp.nstr(Ccoef(kap),20), 'err*L', mp.nstr((L*(g.T*h)[0]-Ccoef(kap))*L,12), 'beta_scaled', mp.nstr(beta*L/(eps*mp.sqrt(lam)),20), 'L1dalpha', mp.nstr(L*(1-ddet*alpha),20))
