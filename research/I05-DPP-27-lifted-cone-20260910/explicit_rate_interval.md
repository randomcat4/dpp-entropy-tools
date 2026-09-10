# An explicit, conservative continuous physical-parameter interval

Status: PROVED (AUTHOR PROOF), PENDING_REVIEW. This is a weak fallback, not the main structural advance and not the original full interval. It uses the already independently accepted PR77 anchor h''(1)<-1/1000, plus a new explicit complex-analytic continuation argument. It does not interpolate sampled values or differentiate a real entropy-value error inequality. No polynomial scout or numerical residual is a premise.

## Statement

For the unchanged fixed symbol f_t=1/2+cos(4*pi*theta)/4+t*cos(2*pi*theta)/8, put

 J=[1-2^(-27),1+2^(-27)].

Then for every t in J the TRUE complete-occupation Shannon entropy rate per original coordinate satisfies

 h''(t)<-1/2000.                                      (1)

In particular h(t)+t^2/4000 is concave on J. For u,v in J and 0<=lambda<=1,

 h(lambda*u+(1-lambda)*v)-lambda*h(u)-(1-lambda)*h(v)
 >=lambda*(1-lambda)*(u-v)^2/4000.                    (2)

This width is deliberately disclosed: its half-width is only 2^(-27), so it is not evidence for the remaining macroscopic interval [1/2,3/2]. The point of this appendix is to close an actual continuous rate statement with every constant fixed, rather than leave an unspecified continuity neighborhood.

## Complex complete-event bounds

Work on |z-1|<=1/8, so |z|<=9/8. A signed complete-event matrix has diagonal +/-1/2, first off-diagonal z/16 and second off-diagonal 1/8. Its absolute comparison matrix is strictly diagonally dominant with margin 7/64. Hence, uniformly over every finite complete word and its length,

 ||M(z)^(-1)||_infinity<=64/7.

The complete-event one-site predictor is q_r(z)=1/2-b_r^T M_r(z)^(-1)b_r, with b_r supported on its first two entries (z/16,1/8). Thus

 |q_r(z)-1/2| <= (25/128)*(64/7)*(1/8)=25/112<1/4.  (3)

The empty-future predictor is exactly 1/2. All these analytic predictors therefore lie in the disk centered at 1/2 of radius 1/4. Neither q_r nor 1-q_r vanishes. Every full word determinant is also nonzero on this disk by diagonal dominance. The logarithms below use the continuation of the real positive branches.

For any w with |w-1/2|<=1/4, elementary ellipse geometry gives

 |w|+|1-w|<=sqrt(5)/2<9/8=:sigma.

Repeated complete-event chain factorization, always summing both branches, therefore proves

 sum_{omega of length n}|p_z(omega)| <=sigma^n.       (4)

This is a bound for complex total variation, not an assumption of complex probability positivity.

## A summable analytic entropy series

The accepted PR77 comparison proof at t=1 supplies rho=2/3, C=288/85, A=11/64, B=49/192 and, for R>r>=3,

 |q_R(z)-q_r(z)| <= C^3*A^2*B^2*rho^(2r-6).

The constants can be bounded without a numerical run:

 C<7/2, A<7/40, B<13/50,
 C^3*A^2*B^2 <2840383/32000000<1/10.                (5)

All four comparison residuals on the disk are positive, as in the accepted source. No PR91 finite constant is a premise here.

Let F(w)=w log w+(1-w)log(1-w). On the convex disk in (3), |F''(w)|<=8. The analytic Bregman identity then gives

 |d(a||b)|<=4|a-b|^2

for a,b in that disk. Define h_r(z) by the FULL finite conditional entropy and d_r(z)=h_r(z)-h_{r+1}(z). The usual conditional relative-entropy identity is an algebraic identity of the complete-event chain and extends analytically to this disk. Applying (4)-(5),

 |d_r(z)| <= (1/25)*sigma^(r+1)*rho^(4r-12), r>=3.   (6)

The ratio sigma*rho^4 is exactly 2/9. Thus

 h(z):=h_3(z)-sum_{r=3}^infinity d_r(z)               (7)

converges normally and is analytic. On the real slice it equals the stationary Shannon entropy rate because finite conditional entropies converge to that rate. In particular (7) is a justified analytic continuation of the TRUE rate; no volume-normalized finite Hessian is being used.

For w in the same disk, |log w| and |log(1-w)| are at most log4<3/2. Hence the binary entropy has modulus at most (9/8)*(3/2)=27/16, and

 |h_3(z)| <=(9/8)^3*(27/16)=19683/8192.

The tail of (6) is at most 59049/716800. Consequently

 |h(z)| <=3562623/1433600<5/2                       (8)

throughout |z-1|<=1/8. The exact numerator gap in (8) is 21377.

## Third derivative and the continuous sign

For real |t-1|<=1/16, apply Cauchy's formula on the radius-1/16 circle about t, entirely inside the preceding analytic domain. From (8),

 |h'''(t)| <=3!*(5/2)*16^3=61440.                   (9)

The independently accepted anchor is h''(1)<-1/1000. For |t-1|<=2^(-27), integrate the actual third derivative in (9):

 h''(t)<-1/1000+61440/2^27
        =-1/1000+15/32768<-1/2000,

where 15*2000=30000<32768. This proves (1). The physical t parameter has not been replaced by s in this argument, so the bound is on the true affine correlation-kernel direction. Integrating (1) twice yields (2).

## What remains

This small interval is a completed quantitative author theorem, not the desired macroscopic/global conclusion. The determinant-lift cone theorem in lifted_cone.md supplies a different structural advance and isolates the remaining mixed physical response. A proposed wider interval using the original degree10 trial data still needs actual outward coefficient and tail certification; sampled residuals do not meet that obligation. Independent review and novelty remain separate.
