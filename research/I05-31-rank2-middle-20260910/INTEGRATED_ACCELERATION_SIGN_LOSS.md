# I05-31 result — the integrated acceleration itself changes sign, but endpoint Fisher still wins

Status: **AUTHOR ANALYTIC PROOF / AUTHOR EXACT FINITE CHECK; PENDING_INDEPENDENT_REVIEW; novelty NOT_ASSESSED.** This result concerns the complete-configuration Shannon entropy of the true physical affine kernel. All 64 events, every Fisher term and every acceleration term are retained. A negative acceleration contribution is not called an entropy counterexample.

Use the natural family

`A=alpha P+beta Q`, `C=I-A`, `B=sqrt(alpha(1-alpha)) P`,

`Q=11^T/3`, `P=I-Q`, `0<alpha,beta<1`, and

`K(t)=[[A,tB],[tB,C]]`.

Put `s=t^2`, `delta=1-s`. For the 13 exact complete-event likelihood types write

`p_E(t)=mu_E q_E(s)`, `q_E=1-a_E s+b_E s^2`,

`v_E=a_E-2s b_E`, `z_E=(a_E-sb_E)(a_E-6sb_E)`.

The complete normalized acceleration and Fisher terms are

`A_norm=2 sum_E mu_E z_E log(q_E)/(q_E-1)`,

`F_norm=4 sum_E mu_E v_E^2/q_E`,

and `Gamma=-H''(t)/t^2=F_norm+A_norm`.

## 1. Exact endpoint logarithmic coefficient

For fixed strict `(alpha,beta)`, exactly four generic likelihood types vanish at `s=1`: one has `q=delta^2`, and three have `q=delta r_i(s)` with `r_i(1)>0`. Every other type has a positive endpoint limit. Since

`A_norm=-(2/s) sum_E mu_E (a_E-6s b_E) log q_E`,

the coefficient of `log(1/delta)` is obtained by summing the exact vanishing orders of these four types. Direct simplification gives

`A_norm(alpha,beta,1-delta)`

` = C_A(alpha,beta) log(1/delta)+O(1)`,                       (1.1)

where

`C_A=(8/3) alpha(1-alpha) L(alpha,beta)`,                    (1.2)

and

`L(alpha,beta)`

` =(6alpha^2-6alpha-2) beta^2`

`  +(-6alpha^2+4alpha+3) beta`

`  +alpha(2alpha-1)`.                                       (1.3)

The `O(1)` is for each fixed strict parameter pair; no uniformity at a beta boundary is asserted here.

Thus the **integrated** complete acceleration, not merely the auxiliary pointwise `u`-kernel, genuinely becomes negative near the legal endpoint whenever `L<0`:

`L(alpha,beta)<0  ==>  A_norm -> -infinity as s -> 1-`.      (1.4)

This is the requested failure of aggregate-acceleration positivity.

## 2. Exact sign-loss wedge

The quadratic coefficient of `L` in beta is always negative. For `0<alpha<1/2`,

`L(alpha,0)=alpha(2alpha-1)<0`,

`L(alpha,1)=(alpha-1)(2alpha-1)>0`.

Hence there is exactly one root in `(0,1)`,

`beta_c(alpha)`

` =[-6alpha^2+4alpha+3-sqrt(Delta(alpha))]`

`   /[4(-3alpha^2+3alpha+1)]`,                               (2.1)

`Delta=-12alpha^4+24alpha^3-28alpha^2+16alpha+9`,

and

`A_norm -> -infinity` for every fixed `0<beta<beta_c(alpha)`. (2.2)

At `alpha=1/2`, `L=(7/2)beta(1-beta)>0` in the strict interval. For `1/2<alpha<1`, the complementary wedge follows from the exact block-swap symmetry

`(alpha,beta) <-> (1-alpha,1-beta)`.

Therefore acceleration sign loss is not an isolated rational fixture: it occurs along a nonempty open parameter wedge for every `alpha !=1/2`, on the beta boundary selected by complement symmetry.

## 3. Full Fisher has a stronger positive pole

The three simple endpoint likelihood types give the exact leading Fisher coefficient

`F_norm(alpha,beta,1-delta)`

` = C_F(alpha,beta)/delta+O(1)`,                              (3.1)

where

`C_F=(16/3) alpha(1-alpha) G(alpha,beta)`,                    (3.2)

`G=alpha-2alpha beta-2beta^2+3beta`.                          (3.3)

As a function of beta, `G` is concave and its endpoint values are

`G(alpha,0)=alpha>0`, `G(alpha,1)=1-alpha>0`.

Thus `C_F>0` throughout the entire strict open square. Consequently

`Gamma=F_norm+A_norm -> +infinity` as `s ->1-`,               (3.4)

including every parameter in the negative-acceleration wedge. The `delta^-1` Fisher pole dominates the adverse logarithm. This is consistent with, but does not use to infer the middle from, the accepted general endpoint theorem.

## 4. One exact rational discriminator

Take

`alpha=1/5`, `beta=1/200`, `s=1-10^-100`.

Here

`L=-51137/500000<0`,

`C_A=-51137/1171875<0`,

while `C_F=8518/46875>0`. A fresh standard-library exact reconstruction of all 64 events, grouped only after reconstruction into the 13 identical likelihood types, gives directed rational logarithm bounds

`-127/1000 < A_norm < -126/1000`,                             (4.1)

and the exact complete Fisher sum satisfies

`F_norm>10^99`.                                               (4.2)

Hence the integrated acceleration is rigorously negative at an exact physical point, but

`Gamma=F_norm+A_norm>0`.                                      (4.3)

The checker uses 384-bit directed fixed-point `atanh` logarithm enclosures with 140 terms and an explicit positive tail. Its minimum likelihood is exactly `10^-200`; no probability floor is inserted.

## 5. Consequence and remaining problem

The failed statement is now precise:

- `R(alpha,beta,s,u)>=0` pointwise is false;
- even `A_norm(alpha,beta,s)>=0` after integrating over `u` is false;
- neither failure is a Shannon-entropy counterexample, because the complete Fisher term controls the displayed point and the entire endpoint asymptotic.

The unresolved question is therefore the true compact-interior sign of

`Gamma=F_norm+A_norm`

for the natural two-parameter family. Endpoint strong concavity is not being used to assert that middle sign. The exact negative point is valuable because any universal proof must combine Fisher and acceleration before the final sign step; a proof based on aggregate acceleration alone cannot work.