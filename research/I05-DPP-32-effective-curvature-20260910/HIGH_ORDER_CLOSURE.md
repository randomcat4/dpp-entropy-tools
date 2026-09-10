# DPP32: effective high-order closure of the true-curvature Neumann bridge

Status: AUTHOR_PROOF / PENDING_INDEPENDENT_REVIEW. Date: 2026-09-10.

Fresh successor from current main. The only external mathematical dependency is accepted PR91 at c7a072ec4eea0c5b0f445bca5796873a9e234948, as scoped by docs/verification_round5_20260910/accepted_pr91.md. No PR112 interval, PR115 finite-window sign, withdrawn S2 output, generic spectral-gap theorem, or finite-HMM assumption is used. This note supplies the higher-state estimates missing in the PR115 Neumann bridge, and restates that bridge so its scope is inspectable here.

The physical family is f_t=1/2+cos(4*pi*theta)/4+t*cos(2*pi*theta)/8, t in I=[1/2,3/2]. Its correlation kernel is affine in t. Shannon entropy uses all complete occupation/vacancy events and natural logarithms, per original lattice coordinate.

## 1. Definitions and accepted low-order inputs

On the real symmetric state ball B={||Q||_op<=1/8}, let q=t/16,

    D_ab=[[a/2,q],[q,b/2]], E=[[1/8,0],[q,1/8]],
    g_ab(Q)=ab det(D_ab-Q), T_ab(Q)=E(D_ab-Q)^(-1)E^T,
    L A=sum_(a,b) g_ab A(T_ab), B_t=-sum_(a,b) g_ab log g_ab.

All four branches are included. State seminorms |A|_j are suprema of j-linear derivative operator norms in Frobenius coordinates. Operator t derivatives hold A fixed; t-dependent trial coefficients are NOT differentiated inside L' or L''.

Use

    k=34/81, rho=32/9, M=19/160, beta=2/3, gamma=19/25,
    epsilon=81/1024,
    P=2, P2=4, Pt=7/64, Pt1=3/8, Ptt=1/32,
    a0=1/6, b0=1/8, u0=352/729, v0=5, w0=1/2.

PR91 proves |LA|_1<=beta|A|_1, |LA|_2<=gamma|A|_2, LQ=0, and branch image norm <=M. The constants P,P2,Pt,Pt1,Ptt bound the respective sums of absolute weight derivatives g_Q,g_QQ,g_t,g_tQ,g_tt. Each individual state derivative of g and its state Hessian has norm <=1; |g_t|<=7/256. Also g_QQQ=g_tQQ=g_ttQ=0, directly from its degree-two formula.

Map derivatives obey ||T_Q||<=k, ||T_QQ||<=d:=2k rho, ||T_QQQ||<=e:=6k rho^2, ||T_t||<=a0, ||T_tt||<=b0, ||T_tQ||<=u0, ||T_tQQ||<=v0, ||T_ttQ||<=w0. These are local inverse-derivative estimates already displayed in PR91, not unproved high-order resolvent bounds.

The accepted low-order fixed-observable response bound is

    |L'A|_1 <= Cg |A|_2,
    Cg=17618609/99532800.

The full physical response is

    h_tt=(1/2) eta [B_tt+L''u+2L'v],
    u=R B, v=R(B_t+L'u).

Here B_t in the last expression means the derivative of the entropy observable; below it is written partial_t B to avoid collision with the family subscript.

## 2. New triangular C3 state estimate

For A in C3, subtract its affine Taylor polynomial at Q=0. Since LQ=0, this changes LA only by a constant. On every branch image the remaining gradient is bounded by M|A|_2. Differentiate the full changing-weight operator three times. The terms multiplying |A|_3 are g D3A[T_Q,T_Q,T_Q]. The terms multiplying |A|_2 are the three map-Hessian terms, three first-weight terms, and all gradient terms, centered using the affine cancellation. Thus

    |LA|_3 <= k^3 |A|_3+C32 |A|_2,
    C32=3dk+3Pk^2+M(e+3Pd+3P2k)
       =4456907/393660.                                      (1)

No third weight term is missing: g_QQQ=0 identically. This proof includes changing weights.

For a finite sum u_m=sum_(j=0)^(m-1) L^j B, the explicit triangular recurrence, together with |L^j B|_2<=gamma^j|B|_2, yields for every m>=1

    |u_m|_2 <= U2=b2/(1-gamma),
    |u_m|_3 <= U3=(b3+C32 U2)/(1-k^3).                       (2)

This is a direct sum of nonnegative geometric series. It asserts no arbitrary parameter differentiability of a spectral projection.

## 3. New C3-to-C2 first response bound

Twice state-differentiate L'A=sum[g_t A(T)+g DA(T)T_t]. The complete coefficients are

    J21=2Pt1 k+Pt d+P2 a0+2P u0+v0,
    J22=Pt k^2+2P k a0+d a0+2k u0,
    J23=k^2 a0.

Before affine cancellation these multiply |A|_1,|A|_2,|A|_3 respectively. Because L' annihilates affine observables, replace |DA(T)| by M|A|_2 in the J21 terms. Consequently

    |L'A|_2 <= D22 |A|_2+D23 |A|_3,
    D22=J22+M J21=41199667/18895680,
    D23=J23=578/19683.                                      (3)

The identities g_tQQ=0 and L'ell=0 are exact. Neither cancels a Hessian evaluated at varying kernels; they apply only to fixed affine observables in the state operator.

## 4. The second-response gradient, also modulo affine observables

A direct state derivative of

    L''A=sum[g_tt A(T)+2g_t DA(T)T_t
             +g D2A(T)[T_t,T_t]+g DA(T)T_tt]

gives

    |L''A|_1 <= H21 |A|_1+H22 |A|_2+H23 |A|_3,
    H21=Ptt k+2Pt1 a0+2Pt u0+P b0+w0=11591/11664,
    H22=2Pt k a0+P a0^2+2u0 a0+k b0=19895/69984,
    H23=k a0^2=17/1458.

Again subtract the affine Taylor part, since L''ell=0. This sharpens the estimate to

    |L''A|_1 <= Hmod |A|_2+H23 |A|_3,
    Hmod=H22+M H21=2252287/5598720.                          (4)

All Fisher, map-motion, acceleration and changing-weight contributions remain in the displayed L'' formula.

## 5. Complete-Shannon observable bounds

Set ell=log(1024/81)<127/50. The latter rational inequality may be checked by the rational atanh series after writing 1024/81=16*(64/81): log(1024/81)=4log2-log(81/64), with atanh arguments 1/3 and 17/145, and geometric remainder bounds.

Using weight normalization to remove the +1 in derivatives of -g log g gives

    b1=127/25 >= |B|_1,
    b2=4096/81+254/25 >= |B|_2,
    b3=2/epsilon^2+6/epsilon=2594816/6561 >= |B|_3,
    bt1=381/400+112/81 >= |partial_t B|_1,
    bt2=(2Pt1+Pt)/epsilon+Pt/epsilon^2
       =185968/6561 >= |partial_t B|_2,
    btt1=(Ptt+2*(7/256)*Pt1)/epsilon+(7/256)*Pt/epsilon^2
        =7429/6561 >= |partial_t^2 B|_1.                     (5)

For b3, the cubic product sum is <=2, using the individual bound <=1 and the summed first-weight bound P=2. Each of the three Hessian-gradient products has absolute sum <=2, using the individual Hessian bound <=1. For bt2, differentiate -sum g_t log g twice; g_tQQ=0. For btt1, differentiate -sum(g_t^2/g+g_tt log g) once; g_ttQ=0. These bounds concern complete Shannon entropy, not spectral entropy.

## 6. Missing constants now closed, uniformly in m

Define

    F_m=partial_t B+L'u_m,
    v_m=sum_(j=0)^(m-1) L^j F_m,
    A_m=partial_t^2 B+L''u_m+2L'v_m.

Equations (2)-(5) prove

    U2=61487/243 <254,
    U3=311874257989/88584660 <3521,
    |F_m|_2 <= F2=bt2+D22 U2+D23 U3,
    |v_m|_2 <= V2=F2/(1-gamma)
          =7721874498279275225/2711665168995456 <2848,
    |A_m|_1 <= G=btt1+Hmod U2+H23 U3+2Cg V2
          =6219117226570786605333361/5397992538651818459136
          <1153.                                           (6)

These inequalities hold for ALL m>=1 and ALL t in [1/2,3/2], on the ENTIRE state ball. In particular G_40 is no longer an unspecified interval-supremum gate.

## 7. Fully explicit long-memory error and the sole scalar gate

For clarity restate the finite-trial residual argument. The first two residuals are exactly L^mB-c0 and L^mF_m-c1, so valid bounds are

    e01=beta^m b1, e02=gamma^m b2,
    e11=beta^m[bt1+Cg b2(1-gamma^m)/(1-gamma)].

The accepted mixed PR91 response error uses

    E12(m)=3e01+e02/15+(11/20)e11.

Take w_(m,r)=sum_(j=0)^(r-1)L^j A_m and c_(m,r)(t)=(L^r A_m)(0). The last residual is exactly L^r A_m-c_(m,r). Its sup norm is <=(3/8)beta^r G by the accepted C1 contraction. Hence

    |h_tt(t)-c_(m,r)(t)/2|
       <= E12(m)+(3/16)beta^r G.                            (7)

At m=r=40 the right side is strictly below 93/10^6. Thus

    sup_(t in J) c_(40,40)(t)/2 < -93/10^6                  (8)

is by itself sufficient for h_tt<0 on J. Both nested invariant-law response terms are included through the PR91 residual theorem. This is not a finite-volume-curvature extrapolation, not a proof that D''(s)>=0, and not yet a claim that (8) has been certified.

## 8. Honest computational boundary

A literal four-branch evaluation of the longest term L^r L' L^(m-1) L' L^(m-1)B has depth r+2m, namely 120 for m=r=40. Therefore a bare finite formula is NOT automatically a feasible computation. The scalar in (8) needs certified function compression, an alternative analytic bulk inequality, or a sharper truncation argument; enumerating 4^120 words is not proposed.

This checkpoint is uploaded before continuing the same task. No old finite-window checks or scouts were rerun. A new tiny Fraction calculation evaluated only the displayed high-order constants. No >60-minute job has been started, no old budget reused, and no independent reviewer outcome is claimed.
