# Post-handoff continuation: affine cancellation and a stronger curvature certificate

Status: PROVED (AUTHOR PROOF), PENDING_REVIEW. Derived after the initial PR91 checkpoint and after issuing the bounded compute request. The physical symbol and parameter interval are unchanged. The previous, coarser theorems remain valid; this supplement sharpens them rather than silently changing a running job. No whole-interval curvature sign is claimed.

The key extra information is not merely that the branches contract: the exact complete-event operator satisfies L_t Q=0 for every Q in its convex domain and every t. This makes parameter response blind to affine errors in trial observables.

## 1. Tighter branch-image radius, without changing observation coordinates

For real symmetric R and A=E^T E, the elementary commutator identity gives

    tr(R A R A)<=tr(R^2 A^2)<=||R||_2^2 tr(A^2).

The first difference is one half of the squared Frobenius norm of the commutator [R,A]. Consequently

    ||E R E^T||_F^2<=||R||_2^2 tr((E E^T)^2).

This is only an auxiliary matrix-norm inequality; no DPP observation basis is rotated. For q=t/16<=3/32 and b=1/8,

    tr((E E^T)^2)=2b^4+4b^2q^2+q^4<=1169/1048576.

Since ||R||_2<=32/9, every branch image satisfies

    ||T_alpha(Q)||_F^2<=1169/82944<(19/160)^2.

Write M=19/160. The union of all branch images has Frobenius diameter at most 2M, substantially smaller than the original domain diameter bound 3/8.

## 2. Weight total variation has Lipschitz constant one

Use the exact four-sign formula from proof.md. For a Frobenius-unit U=[[u,w],[w,v]], put

    c=tr((adj Q+q J)U),   J=[[0,1],[1,0]].

The total-variation derivative is

    max(|u|,|v|,2|c|,(|u|+|v|)/2+|c|).

The first two entries are at most one. Also ||adj Q||_F=||Q||_F<=3/16, and ||qJ||_F<=9/64, so 2|c|<=21/32<1.

For the last entry, maximize over the choices of the signs of u,v,c. The resulting Frobenius dual matrix is the sum of +/-adj Q and a matrix diag(+/-1/2,+/-1/2)+/-qJ. The latter has squared Frobenius norm 1/2+2q^2<=265/512<9/16. Hence its norm is at most3/4, and the full dual norm is at most3/4+3/16=15/16<1. Therefore

    TV(g(Q),g(P))<=||Q-P||_F.                       (A1)

Maximal label coupling, now using branch-image diameter 2M, improves the FULL probability-law contraction to

    beta_* = k+2M = 4259/6480 < 2/3,
    k=34/81.

Thus |L A|_1<=(2/3)|A|_1, W1 contracts by at most2/3 per step, and the centered first-derivative resolvent bound is R1<=3. Invariant-law existence, uniqueness, support and the true-rate identity are the same ones already proved, not new assumptions.

## 3. Direct contraction of the state Hessian seminorm

For a C2 observable A, subtract its affine Taylor part at Q=0:

    F(Q)=A(Q)-A(0)-DA(0)[Q].

Since LQ=0, L A and L F differ only by the constant A(0). On every branch image,

    |F(T)|<=(M^2/2)|A|_2,   ||DF(T)||<=M|A|_2.

Use sum|Dg[U]|<=2 from (A1), sum|D2g[U,V]|<=4, ||T_Q||<=k and ||T_QQ||<=2kr, r=32/9. Twice differentiating L F gives

    |L A|_2 <= gamma_* |A|_2,
    gamma_*=k^2+4kM+2krM+2M^2
           =63677321/83980800 <19/25.               (A2)

All four terms arise respectively from the Hessian of A, the mixed weight/map terms, the second derivative of T, and the second derivative of g. Nothing is dropped because of a sign guess.

In particular the centered Poisson series obeys

    |Rcal A|_2<=(25/6)|A|_2.                         (A3)

This is a state-Hessian seminorm statement, not a sign statement for the physical parameter curvature h''.

## 4. Response bounds modulo affine observables

For every fixed affine observable ell, L_t ell=ell(0), so L_t' ell=L_t'' ell=0. Subtract the affine Taylor part as above when estimating operator parameter derivatives.

Let P=2, Pt=7/64, Ptt=1/32, PtQ=3/8, a=1/6, b=1/8. The fixed-Q map derivative bounds from proof.md remain valid. They give

    ||L' A||_infinity<=CtH |A|_2,
    ||L'' A||_infinity<=CttH |A|_2,
    |L' A|_1<=CgradH |A|_2,

where

    CtH=Pt*M^2/2+a*M=202141/9830400,
    CttH=Ptt*M^2/2+2Pt*a*M+a^2+b*M=695569/14745600,
    CgradH=PtQ*M^2/2+Pt*k*M+P*a*M+k*a+M/2
          =17618609/99532800.                       (A4)

For a merely C1 observable, the original Lipschitz response bound is sharpened by centering values on the branch images:

    ||L' A||_infinity<=Ct |A|_1,
    Ct=M*Pt+a=5519/30720<9/50.

Together with R1<=3 this yields

    |eta L' Rcal A|<=(27/50)|A|_1.                  (A5)

The estimates in (A4) require only A in C2. In particular applying the last one to Rcal r0 does not require a third derivative of the unknown exact Poisson solution.

## 5. A three-residual, Hessian-only certificate for the TRUE rate

Use the SAME trial residuals r0,r1,r2 and candidate c2 as in curvature_certificate.md. Suppose the trial functions are smooth enough that r0 and r1 are C2; polynomial trials satisfy this, and C3 u with C2 v suffices. Let

    e02>=sup_B ||D_Q^2 r0||,
    e12>=sup_B ||D_Q^2 r1||,
    e20>=sup_B |r2|.

Then

    |h''(t)-c2/2| <= e02/2+(9/100)e12+e20/2.        (A6)

Proof: the exact full-response error remains

    2h''-eta A=eta L''Rcal r0
                +2eta L'Rcal r1
                +2eta L'Rcal L'Rcal r0.

For the first and nested terms use (A3)-(A5). Their total coefficient after the factor1/2 is at most

    (25/12)[CttH+2*(9/50)*3*CgradH]
      =9762629/19660800<1/2.

The r1 term is at most

    (25/6)CtH e12=(202141/2359296)e12<(9/100)e12.

Finally eta r2 is bounded by e20. This proves (A6), including the invariant-measure response and not just the local Fisher piece. Constants and affine components of r0 and r1 need no certification at all: their stationary parameter responses vanish exactly.

A complete interval cover with

    sup_J(c2/2)+e02/2+(9/100)e12+e20/2<0             (A7)

would prove the target curvature interval. The three residual bounds must be verified over the ENTIRE state domain times J, not a grid. There is still no completed covering here.

## 6. Sharpened version of the original mixed derivative gate

The earlier gate does not require D2r1. It too improves using beta<=2/3, the smaller image radius, and sum|Dg|<=2. Specifically, with

    Ctt=M*Ptt+2Pt*a+b=2537/15360,
    b2=4M+4k+2kr=149851/29160,

the same triangular-resolvent calculation as before yields coefficients

    e01: 56391426133/19924992000 <3,
    e02: 3466341/55347200 <1/15,
    e11: 5519/10240 <11/20.

Hence the alternative valid gate is

    |h''-c2/2|<=3e01+e02/15+(11/20)e11+e20/2.       (A8)

The original 13,1/8,6/5,1/2 gate remains correct. An executor may use whichever fully certified residual gate is more economical, but must state which norms were actually bounded. The sampled scout residuals remain non-certifying under every version.

## Execution, review and budget boundary

`code/check_tightening.py` was executed in this task with exact Fraction arithmetic; `output/tightening_output.json` retains the actual constants and strict rational gaps. It certifies these finite arithmetic comparisons, not whole-interval curvature or independent review. A preliminary, looser affine-cancellation calculation is also retained in the chat raw-execution archive.

The issue74 request issued earlier froze the coarser gate. This supplement adds optional mathematically stronger gates without adding a budget, starting a job, modifying another worker's source, or assuming independent acceptance. An already-claimed job must retain its declared source/gate unless its owner explicitly freezes an amendment.
