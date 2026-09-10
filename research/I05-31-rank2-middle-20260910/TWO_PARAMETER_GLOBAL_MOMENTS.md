# I05-31 — full two-parameter exchangeable rank-two signed-moment theorem

Status: **AUTHOR ANALYTIC PROOF / PENDING_REVIEW; novelty NOT_ASSESSED.** This theorem concerns the complete-event quantities entering the true physical affine Shannon curvature. It is not yet a proof that the logarithm-weighted acceleration is nonnegative, and it is not an entropy counterexample.

Let

`Q=11^T/3`, `P=I_3-Q`,

`A=alpha P+beta Q`, `C=I-A`,

`B=sqrt(alpha(1-alpha)) P`, with `0<alpha,beta<1`, and

`K(t)=[[A,tB],[tB,C]]`.

For every such pair the true maximal legal chord is `[-1,1]`: on the two-dimensional P sector the repeated physical block is

`[[alpha, t sqrt(alpha(1-alpha))], [t sqrt(alpha(1-alpha)),1-alpha]]`,

with determinant `alpha(1-alpha)(1-t^2)` and trace one, while the Q sector consists of the fixed strict scalars `beta,1-beta`. Thus at each endpoint both `K` and `I-K` have nullity two. Entropy is never evaluated in that spectral basis.

The complete observed law is invariant under simultaneous permutations of the three left/right coordinate labels, so its 64 atoms lie in the 20 actual-coordinate orbits indexed by

`(|S|,|T|,|S intersect T|)`.

Direct signed-determinant expansion of one representative per orbit gives

`p_E(t)=mu_E(1-a_E s+b_E s^2)`, `s=t^2`,

and summing over the actual orbit multiplicities gives the following three exact global moments:

`M_a=sum_E mu_E a_E^2`

`=6 N_a(alpha,beta)^2 / D(alpha,beta)^2`,

where

`N_a=5 alpha^2 beta^2-5 alpha^2 beta+alpha^2-2 alpha beta^3-2 alpha beta^2+2 alpha beta+beta^3`,

`D=(3 alpha beta-2 alpha-beta)(3 alpha beta-alpha-2 beta)`,

and

`M_ab=sum_E mu_E a_E b_E`

`=2 alpha beta^2 (alpha-1)(alpha-beta)^2(beta-1)^2 / D^2 <=0`,

while

`M_b=sum_E mu_E b_E^2`

`=N_b(alpha,beta)^2/D^2`,

`N_b=7 alpha^2 beta^2-7 alpha^2 beta+2 alpha^2-4 alpha beta^3-alpha beta^2+alpha beta+2 beta^3`.

All denominators are nonzero in the strict open square because the displayed factors are exactly nonzero strict marginal-event factors; equivalently the complete decoupled marginal atoms are positive.

Consequently, for every `0<alpha,beta<1` and every `0<=s<=1`,

`sum mu (a-2sb)^2 = M_a-4s M_ab+4s^2 M_b >=0`,

and, crucially,

`sum mu (a-sb)(a-6sb)=M_a-7s M_ab+6s^2 M_b >=0`.

Away from the degenerate case where all relevant coefficients vanish, the latter is strict. Thus the **unweighted aggregate affine-acceleration polynomial is favorable on the entire natural two-parameter family and whole legal chord**.

The remaining sign problem is exactly the logarithmic secant reweighting

`A_norm(alpha,beta,s)=2 sum_E mu_E z_E lambda(q_E)`,

`z_E=(a_E-sb_E)(a_E-6sb_E)`, `lambda(q)=log(q)/(q-1)`.

Some individual `z_E` are negative, so positivity of `sum mu z_E` alone does not settle `A_norm`. Any failure must therefore come from a sufficiently adverse covariance between `z_E` and the decreasing event weight `lambda(q_E)`. This is the precise remaining mechanism to prove or break.

The full Fisher term remains untouched:

`Gamma=-H''/t^2=sum mu[4(a-2sb)^2/q+2z lambda(q)]`.

A physical matching-coordinate occupancy statistic already supplies for this family

`F_complete(t) >= (256/81) alpha^2(1-alpha)^2 t^2`,

because `B_ii=(2/3)sqrt(alpha(1-alpha))` and `d/dt P(X_i=X_{3+i}=1)=-2t B_ii^2`; the Bernoulli Fisher denominator is at most `1/4`. Hence even if `A_norm` eventually becomes negative, a true entropy counterexample requires it to beat this explicit full-Fisher floor.

A mechanism-directed numerical scout over the new family, including alpha down to `10^-4`, found no negative `A_norm`; the observed minimum shrinks toward zero as alpha approaches the degenerate boundary. This scout is not a proof, certificate, or finite-sample theorem and is recorded only to identify the remaining analytic target.
