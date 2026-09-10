# I05-29: an explicit correlated neighborhood after the cross-fiber upload

Status: AUTHOR PROOF; PENDING_REVIEW. This continuation was derived after uploading the core obstruction and interval-family proof. It is not independent certification.

The preceding [cross-fiber addendum](ADDENDUM_CROSS_FIBER_OBSTRUCTION.md) proves, for its r=1/8 member, a uniform full-entropy bound and a negative true conditional fiber. Here that result is extended to a quantitatively specified neighborhood, including an explicit kernel with both blocks correlated. No new name for a sufficient criterion is used as the conclusion: the explicit rational kernel in Section 3 is covered on every t in [-1,1].

## 1. Remove the apparent endpoint singularity exactly

Use the same complete rank-two law `q=1-sa+s^2b`, `s=t^2`, and actual product reference weights `mu=p_A p_C`. For s in [0,1] put

`w=-a+sb`, `v=-a+2sb`, `h=-a+6sb`, `q=1+sw`,

`phi_s(a,b)=4v^2/q+2wh lambda(q)`, `lambda(q)=log(q)/(q-1)`, `lambda(1)=1`.

The exact normalized full curvature is

`Gamma(s)=E_mu phi_s(a,b)`.

For s>0 this is `t^2 I''/s^2=I''/t^2=-H''/t^2`. At s=0 it is, continuously,

`Gamma(0)=6E_mu a^2`.

Thus stability near t=0 is a regular compact-interval problem, not division of a numerical curvature bound by a vanishing parameter. The individual complete curvature fiber at s>0 is `s^2 E_pC phi_s`.

## 2. Quantitative coefficient neighborhood

Let the reference point be

`A0=I_2/2`, `C0=[[1/2,1/8],[1/8,1/2]]`,

`B0=(1/4)[[1,1],[1,-1]]`.

Subscript 0 denotes its p_A, p_C and complete-event coefficients a,b. Consider any strict real 2+2 rank-two affine path for which, in the same labeled complete-event basis,

`max_S |p_A(S)-p_A0(S)| <= delta`,

`max_T |p_C(T)-p_C0(T)| <= delta`,

`max_{S,T} |a-a0| <= delta`, `max_{S,T} |b-b0| <= delta`,

where `delta=1/40000`. These are coefficient-space bounds; this is not a claimed radius in matrix-entry norm.

### Theorem

Every such path satisfies, on the entire interval |t|<=1,

`H''(t) <= -(1/2)t^2`.                                    (2.1)

At s=1/2 its left mask-1 complete curvature fiber is strictly negative; more specifically,

`C_1(1/2) <= -274937/17000000 <0`.                          (2.2)

### Proof

At the reference point, `|a0|<=16/15`, `|b0|<=4/15`, and `q0 in [1/5,7/3]`. The stated perturbations therefore imply, for all s in [0,1],

`|a|<=6/5`, `|b|<=1/3`, `q in [1/6,5/2]`,

`|v|<=2`, `|w|<=8/5`, `|h|<=16/5`.

The same bounds hold at the reference point. On this likelihood window,

`0<lambda(q)<=9/4`, `|lambda'(q)|<=6`.

For example `lambda(q)=integral_0^1 [1+theta(q-1)]^(-1) dtheta`; the maximum derivative magnitude is at q=1/6 and equals `(36/25)(5-log6)<6`. The upper secant bound follows from `log6<15/8`. Both elementary log comparisons are included in the rational checker.

Write Delta for the difference from the reference coefficients. Uniformly in s,

`|Delta v|<=3delta`, `|Delta w|<=2delta`,

`|Delta h|<=7delta`, `|Delta q|<=2delta`.

The rational term satisfies

`|Delta(4v^2/q)| <= 4[4(3delta)6+4(2delta)36] =1440delta`.

The logarithmic term satisfies

`|Delta(2wh lambda(q))|`

` <=2[(9/4)((16/5)2+(8/5)7)+(128/25)6*2]delta`

` =(5052/25)delta`.

Consequently

`|Delta phi_s| <= L delta`, `L=41052/25`,

`|phi_s| <= M`, `M=2976/25`.

Since both marginal weight vectors have four entries and sum to one,

`||mu-mu0||_1 <= ||p_A-p_A0||_1+||p_C-p_C0||_1 <=8delta`.

Hence

`|Gamma-Gamma0| <= (L+8M)delta = (12972/5)delta`.

The preceding interval theorem gives `Gamma0>=175/304`. Therefore

`Gamma >=175/304-(12972/5)/40000 =242629/475000 >1/2`.

This proves (2.1) for t!=0; the analytic endpoint identity proves it at zero.

For the specified fiber, the reference weight is only p_C, so at s=1/2,

`|C_1-C_1,0| <= (1/4)(L+4M)delta = (13239/25)delta`.

The exact reference value is `C_1,0=-(1/4)log(17/15)`. The elementary bound `log(17/15)>=2/17` gives

`C_1 <= -1/34+13239/1000000 = -274937/17000000 <0`.

Thus full-interval concavity and a negative full conditional fiber coexist throughout the specified neighborhood. QED.

## 3. Explicit rational kernel with both marginals correlated

Take

`A=[[1/2,1/100000],[1/100000,1/2]]`,

`C=[[1/2,1/8],[1/8,1/2]]`,

`B=(1/4)[[1,1],[1,-1]]`.

Both marginal blocks have nonzero off-diagonal entries, and B has rank two and no zero entry. Strict legality on |t|<=1 follows from either the exact Schur check or the bound

`lambda_min(C-B^T A^(-1)B) >= 3/8-(1/8)/(1/2-1/100000)>0`,

with the identical lower bound for the complementary Schur expression. Smaller s only increases those Schur complements.

Exact rational reconstruction gives

`max |Delta p_A|=1/10^10`, `Delta p_C=0`,

`max |Delta a| <0.000018823624`,

`max |Delta b| <0.000000000107`.

All are strictly below 1/40000. Therefore the preceding theorem proves `H''(t)<=-t^2/2` at every point of [-1,1] for this explicit correlated kernel, while its mask-1 complete curvature fiber at s=1/2 remains strictly negative. The finite checker establishes coefficient membership and legality, not a time grid standing in for the continuum theorem.

## 4. Arbitrary finite block dimensions and open correlated classes

For any fixed m,n>=2, append arbitrary strict DPP blocks A_* and C_* as independent spectators on their respective sides, and pad B0 with zero spectator rows/columns. This is an actual direct sum of laws, so full Shannon entropy adds: the t-dependent curvature is exactly that of the four active coordinates. The same negative active fiber persists for every fixed left spectator configuration because the right spectator weights sum to one.

Now parameterize rank-two cross blocks as `B=UV^T` with U,V of full column rank two. For fixed finite dimensions, all full event weights and coefficients are continuous in (A,C,U,V) on a strict neighborhood. The explicit Gamma formula in Section 1 is jointly continuous even at s=0. Compactness of [0,1] and the positive uniform base margin therefore give a nonempty relative-open parameter neighborhood with `Gamma>=1/4`; continuity at s=1/2 preserves one selected negative fiber as well.

Such neighborhoods contain choices with both marginal blocks fully correlated and every entry of B nonzero: these nonvanishing conditions can be obtained by arbitrarily small symmetric and full-column-rank factor perturbations. No observed-coordinate rotation or event deletion is used. Thus, in every fixed pair of block dimensions at least two, there are nonempty open correlated rank-two classes whose whole [-1,1] chord is entropy-concave despite a negative complete curvature fiber.

For this arbitrary-dimensional extension the neighborhood radius is existential and depends on the chosen spectator blocks and dimensions. Only the 2+2 coefficient radius 1/40000 and the explicit matrix in Section 3 are quantitative. No uniform radius as dimension grows, no coverage of all rank-two kernels, and no whole-chord result for the original 3+3 s=.9 fixture is claimed.

## 5. Status

All statements in this addendum are author proofs, PENDING_REVIEW. The accompanying `code/verify_coefficient_neighborhood.py` checks the constants and the exact rational member without temporal sampling. Newness relative to the literature remains NOT_ASSESSED.
