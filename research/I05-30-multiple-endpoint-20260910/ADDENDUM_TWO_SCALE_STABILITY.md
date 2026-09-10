# I05-30 addendum — uniform two-scale stability through split rank-two endpoints

Status: **PROVED (author analytic proof); PENDING_REVIEW.** This is a continuation after the first I05-30 upload, not an edit of PR95.

The fixed-path endpoint theorem in `RESULT.md` proves favorable sign at every multiple endpoint. This addendum addresses the harder stability question: if a repeated endpoint is perturbed and splits, can the favorable endpoint strip be chosen uniformly, so that compact-interior continuity closes each nearby path's own maximal chord?

For rank two the answer is yes.

## 1. Setup and the exact two-scale full/empty atom

Consider a real rank-two radial path

`K_theta(t)=[[A_theta,t B_theta],[t B_theta^T,C_theta]]`,

with strict `A_theta,C_theta` and `rank B_theta=2`. Define the two rank-two legality operators

`R_0=C^(-1/2) B^T A^(-1) B C^(-1/2)`,

`R_1=(I-C)^(-1/2) B^T (I-A)^(-1) B (I-C)^(-1/2)`.

Let their positive eigenvalues be

`rho_(h,1)>=rho_(h,2)>0`, `h=0,1`.

The positive maximal endpoint satisfies

`s_*=T^2=1/rho_*`, `rho_*=max_(h,j) rho_(h,j)`.              (1.1)

Suppose side `h=0` is actually active, so `rho_(0,1)=rho_*`. Put

`delta=1-s/s_*=1-s rho_(0,1)`,

`eta=1-rho_(0,2)/rho_(0,1)`, `x=1-eta`.                     (1.2)

Then the full-event likelihood relative to its decoupled full-event weight is exactly

`q_full(s)=det(I-s R_0)`
` =delta [eta+x delta]`.                                     (1.3)

Thus a repeated endpoint is `eta=0`; after splitting, `eta>0`. The complementary active side has the identical formula for the empty event after replacing `K` by `I-K`.

For `eta>=eta_0>0`, (1.3) already gives the ordinary simple-root Fisher pole `C/delta`. The only new regime is `eta ->0` together with `delta->0`.

## 2. The neighboring cardinality group supplies the missing scale

Assume first that a seed `theta_0` has a double `K`-active endpoint: `rho_(0,1)=rho_(0,2)=rho_*` there. At that endpoint `rank K=N-2`, so

`G_0(s):=P_theta0(|X|=N-1)`

vanishes. By Lemma 2.2 of `RESULT.md`, this forbidden cardinality has a simple zero. Normalize by the moving endpoint as in (1.2), and write

`G_theta(delta)=P_theta(|X|=N-1)`.

Because every complete probability is a quadratic polynomial in `s` for cross rank two, `G_theta` is itself quadratic in `delta`, with coefficients continuous in the finite kernel parameters and in `s_*`. Therefore, after shrinking a parameter neighborhood and a fixed endpoint strip,

`partial_delta G_theta(delta) >= g_1>0`,                    (2.1)

uniformly whenever the `K` side is active and `eta` is small.

At the actual endpoint `delta=0`, if `eta=0` then `G_theta(0)=0`. If `eta>0`, `K(T)` has exactly one zero eigenvalue and its second formerly active eigenvalue is `O(eta)`. This follows from the Schur congruence

`C-s_* B^T A^-1 B`
` =C^(1/2) diag(0,eta,1) C^(1/2)`                           (2.2)

on the active two-dimensional range plus the untouched complement, with uniformly bounded congruence condition numbers in a small neighborhood.

The exact count formula

`G_theta(0)=sum_i (1-lambda_i) product_(j!=i) lambda_j`       (2.3)

then shows

`0<=G_theta(0)<=g_2 eta`,                                   (2.4)

because only the term omitting the zero eigenvalue survives at the endpoint, and its product contains the `O(eta)` second small eigenvalue. The remaining eigenvalues stay uniformly bounded.

Together with an upper derivative bound, (2.1)-(2.4) give

`G_theta(delta)<=g_3(eta+delta)`,

`partial_delta G_theta(delta)>=g_1`.                         (2.5)

Since

`|d delta/dt|=2t/T^2`

is uniformly bounded below on a sufficiently short endpoint strip, weighted Cauchy over the **complete size-(N-1) event group** gives

`F_(N-1):=sum_(|E|=N-1) (p_E')^2/p_E`
` >=(G_theta')^2/G_theta`
` >=c_1/(eta+delta)`.                                       (2.6)

No spectral-mode entropy or rotated complete event is used: the eigenvalues only estimate the true observed cardinality probability in (2.3).

## 3. Full-event Fisher plus cardinality Fisher is uniform across the split

Let

`d_theta=det A_theta det C_theta`.

It stays uniformly positive. From (1.3), for the small-split regime `eta<=1/2`,

`p_full=d_theta delta(eta+x delta)`,

`partial_delta p_full=d_theta(eta+2x delta)`.                (3.1)

The physical derivative factor `|d delta/dt|` is again uniformly positive. Since `x>=1/2`,

`F_full=(p_full')^2/p_full`
` >=c_2 (eta+delta)/delta`.                                  (3.2)

Combining (2.6) and (3.2),

`F_full+F_(N-1)`
` >=c_1/(eta+delta)+c_2(eta+delta)/delta`
` >=2 sqrt(c_1 c_2) delta^(-1/2)`.                           (3.3)

The last inequality is AM-GM. It is the key two-scale estimate. It is uniform whether

* `eta=0` (the endpoint remains double),
* `eta<<delta`,
* `eta` is comparable to `delta`, or
* `delta<<eta` (the split endpoint looks simple at the very last scale).

If the second generalized eigenvalue stays separated instead, the full atom alone gives the stronger `C/delta` pole.

For a double `I-K` endpoint, complement configurations. The empty event replaces the full event, and the true size-one cardinality group replaces size `N-1`.

If `K` and `I-K` are simultaneously active at the seed, a sufficiently small neighborhood contains only the finitely many seed-active clusters as candidates for the first endpoint. Whichever side attains (1.1) is handled by its corresponding argument. Constants are replaced by the minimum over those finitely many clusters. Thus simultaneous activity causes no new sign ambiguity.

## 4. All acceleration logarithms remain only logarithmic, even at a simultaneous endpoint

The preceding Fisher estimate must be compared with **all** complete acceleration terms, including atoms made rare by the opposite spectral constraint.

Let `r=t/T`. Since the physical path is affine in `t`,

`K(rT)=(1-r)K(0)+rK(T)`,

`I-K(rT)=(1-r)(I-K(0))+r(I-K(T))`.                           (4.1)

In a fixed parameter neighborhood the strict center has uniform margins, so for some `kappa>0`,

`K(rT)>=kappa(1-r)I`, `I-K(rT)>=kappa(1-r)I`.                (4.2)

Because

`delta=1-r^2=(1-r)(1+r)<=2(1-r)`,

both matrices are at least `(kappa/2) delta I`.

For every strict interior point use the exact atomic identity

`p_E=det(I-K) det L_E`, `L=K(I-K)^(-1)`.                     (4.3)

This use of `L` is pointwise only; no L-affine path is introduced. Since `I-K<=I`, `L>=K`. Hence, after reducing `kappa` if necessary so that `kappa delta/2<=1`,

`p_E >=[(kappa/2)delta]^N [(kappa/2)delta]^|E|`
`     >=c_0 delta^(2N)`                                     (4.4)

for every complete event, including simultaneous zero/one endpoint sectors.

Therefore

`|log p_E|<=C_0+2N log(1/delta)`.                            (4.5)

The finite rank-two coefficients vary continuously, so in a fixed parameter neighborhood

`sum_E |p_E''(t)|<=M`.                                      (4.6)

Equations (4.5)-(4.6) give the full acceleration bound

`sum_E p_E'' log p_E >=-M[C_0+2N log(1/delta)]`.             (4.7)

Combining (3.3) and (4.7), in every split-double or simultaneous regime,

`-H''(t)>=c delta^(-1/2)-M[C_0+2N log(1/delta)] -> +infinity` (4.8)

**uniformly in the nearby path**. The new `delta^(-1/2)` rate is weaker than a fixed simple endpoint's `delta^(-1)` pole but is still more than enough to dominate every complete logarithmic acceleration term.

## 5. Moving maximal-chord stability without any endpoint simplicity assumption

### Theorem 5.1

Fix a finite real rank-two radial seed

`K_0(t)=[[A_0,tB_0],[tB_0^T,C_0]]`

with strict center, maximal legal interval `[-T_0,T_0]`, and `B_0!=0`. Assume its exact normalized full curvature has a positive whole-interior margin

`Gamma_0(t^2):=-H_0''(t)/t^2 >=g>0`                         (5.1)

for every `0<|t|<T_0`, with the usual continuous value at zero.

No assumption is made on the endpoint multiplicities. `K(T_0)` and `I-K(T_0)` may each have nullity one or two and may be simultaneously singular.

Then there is a relative-open neighborhood of `(A_0,C_0,B_0)` in the real rank-two parameter manifold such that every nearby path, on **its own maximal legal chord**, satisfies

`H''(t)<=-(g/2)t^2`                                         (5.2)

throughout the strict interior. Consequently

`H(t)+(g/24)t^4`                                             (5.3)

is concave on its whole closed maximal legal chord.

#### Proof

The four positive generalized endpoint eigenvalues `rho_(h,j)` vary continuously. The maximal endpoint (1.1) therefore varies continuously, and only clusters active at the seed can become first-active after a sufficiently small perturbation.

For a seed-active cluster whose second eigenvalue is separated from its top eigenvalue, the full/empty atom supplies a uniform simple `C/delta` Fisher pole. For a seed-active repeated cluster, Sections 2-4 supply the uniform split estimate (4.8). Take the minimum endpoint width over the finitely many seed-active clusters. Shrink it so that the right side of (4.8), or the simple analogue, is at least `(g/2)T_+^2`. This proves (5.2) on a common normalized endpoint strip for every nearby path.

On the complementary normalized interval, all kernels and complements are uniformly strict. The exact rank-two normalized complete-law formula

`Gamma=E_mu[4(a-2sb)^2/q+2(a-sb)(a-6sb)lambda(q)]`

is jointly continuous in the finite parameters and the normalized path coordinate, including at `t=0`. Compactness and (5.1) therefore allow a final shrinking of the same parameter neighborhood so that `Gamma>=g/2` there. The endpoint estimate survives shrinking. Evenness handles the negative endpoint, and continuity of `x log x` extends the conclusion to the closed chord. QED.

This removes the endpoint-simplicity and one-active-side assumptions from the PR95 stability mechanism in **cross rank two**. It does not prove the seed margin (5.1); compact-interior curvature remains the substantive kernel-dependent obligation.

## 6. Consequence for the I05-30 double-endpoint seed

`RESULT.md` proves for the explicit dense correlated 3+3 seed

`Gamma_0>=1/100`

on its full strict maximal chord, while `K(1)` has nullity two. Therefore Theorem 5.1 yields a nonempty relative-open class of dense correlated 3+3 rank-two paths containing arbitrarily small generic perturbations of that seed such that every member obeys

`H''(t)<=-(1/200)t^2`                                       (6.1)

on its own maximal chord, even though the repeated seed endpoint generically splits under perturbation.

This open-class conclusion is not obtained by the PR94 local-channel lift: the seed itself has no proportional pair of rows or columns in its dense cross block, as certified in `RESULT.md`, and that nonproportionality persists under small perturbations.

No numerical radius is claimed here. The new content is the two-scale uniform endpoint argument, not another tiny explicit stability ball.

## 7. Limits

The theorem is a stability result around an already favorable rank-two seed. It does not establish the whole-interior margin (5.1) for arbitrary rank-two kernels, so general dense correlated rank-two whole-chord concavity remains open. For cross rank greater than two, a repeated endpoint can have larger clusters; the analogous multi-scale cardinality hierarchy is plausible but not proved here.
