# Frozen auxiliary statements v3: uniform estimates and crossover

Frozen by A2 on 2026-09-08. These auxiliary statements are separate from
v2, which remains unchanged. Proof and review roles must not change the
premises. Full-event entropy and actual arithmetic midpoint conventions are
those of v1. No arbitrary orthogonal entropy invariance is assumed.

## 1. Zero-safe finite-law and matrix estimates

Let N=2^n and w_-=w_+=1/2,w_0=-1. For three genuine finite event laws
p_j(S;t,z) arising from a feasible chord and its true midpoint, suppose real
approximants q_j obey |p_j-q_j|<=R(t)<=1 uniformly in j,S,z, with R(t)>0.
Write qbar=min(1,max(0,q)), omega(d)=d(2+log(1/d)), omega(0)=0, and
Dhat=sum w_j h(qbar_j), h(p)=-p log p, h(0)=0. Claim:

    |Delta-Dhat|<=2N omega(R).

For two feasible triples K_j,L_j, each with its own arithmetic midpoint,
max_j ||K_j-L_j||op<=delta and L_n delta<=1, L_n=n 2^n, claim:

    |Delta(K)-Delta(L)|<=2^(n+1) omega(L_n delta).

No common positive lower bound on event masses is assumed.

## 2. Bounded moving mixed data

Fix n, 1<=r<n, and M>=1. At each epsilon, W=[U,V] is real orthogonal,
and symmetric A,X (r by r), C,Y (n-r by n-r), and B (r by n-r) have
operator norms at most M. Put H_sigma=A-sigma X, L_sigma=C+sigma Y,

    K_sigma=W [[I-epsilon H_sigma,sigma sqrt(epsilon)B],
               [sigma sqrt(epsilon)B^T,epsilon L_sigma]] W^T,
    K_0=(K_-+K_+)/2=W diag(I-epsilon A,epsilon C)W^T.

Assume actual endpoints are feasible at the evaluated epsilon, and for each
sigma assume the additional frozen-data Schur conditions

    H_sigma-BB^T >=0, L_sigma-B^T B>=0,
    ker(H_sigma-BB^T) subset ker B^T,
    ker(L_sigma-B^T B) subset ker B.

Let psi_S=det U_S, phi_S=d/da det((U+aVB^T)_S)|_(a=0),
F=||B||F^2, Z=sum_(|S|=r,psi_S=0)phi_S^2, and
m=min_(|S|=r,psi_S!=0)psi_S^2. No support set is assumed constant.

Claim: constants c,C,epsilon_0>0 depending only on n,r,M exist such that
0<epsilon<min(epsilon_0,c m) implies

    |Delta-(Z-2F)epsilon log(1/epsilon)|
      <=C epsilon(1+log(1/m))
        +C epsilon^(3/2)(1+log(1/epsilon)).

Consequently Delta<0 eventually if F>=f_*>0 and
log(1/m)=o(log(1/epsilon)). A sufficient more general condition is

    [1+log(1/m)+sqrt(epsilon)(1+log(1/epsilon))]
      /[F log(1/epsilon)] ->0,

together with the other assumptions and epsilon<c m. This is only a
sufficient condition, not a statement for all shrinking directions.

## 3. Exact shrinking-direction crossover

Fix kappa>0 and 0<epsilon<1/2. Put b=epsilon^kappa and

    K_sigma=[[1-epsilon,sigma b sqrt(epsilon(1-epsilon))],
             [sigma b sqrt(epsilon(1-epsilon)),epsilon]],
    K_0=diag(1-epsilon,epsilon).

The endpoints and true midpoint are strict positive contractions. With
u=epsilon(1-epsilon), v=(1-epsilon)^2, w=epsilon^2, delta=b^2 u, the full
endpoint law on empty,{1},{2},full is (u-delta,v+delta,w+delta,u-delta),
and the midpoint law is (u,v,w,u). Claim:

    Delta=-[(w+delta)log(1+delta/w)-delta]+E,
    E<=0, |E|<=delta^2/[u(1-b^2)]+delta^2/(2v).

It follows, with kappa fixed, that

    0<kappa<1/2: Delta=-(1-2kappa)epsilon^(1+2kappa)log(1/epsilon)
                       +O(epsilon^(1+2kappa));
    kappa=1/2:   Delta=-(2log 2-1)epsilon^2+o(epsilon^2);
    kappa>1/2:   Delta=-(1/2)epsilon^(4kappa)(1+o(1)).

This is an explicit obstruction to substituting a shrinking direction into a
fixed-data leading term. It does not contradict the old fixed-data theorem,
and it is not a new two-dimensional sign exclusion or a positive example.
No uniformity in kappa across 1/2 is asserted. Author proof Sections 1--4
are the certification target; Sections 5--7 are context and limitations.
