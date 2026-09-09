# PR54: exact accepted scope after separate dual reviews

Final source head: `d5c55447a0f7377dae085b8074f557e4f673b5a4`. Merge commit: `24ae88bf14b540b66490e3266a75849e6e258bad`. All nine source files are under `research/I05-23-20260909/`. [Original result](../../research/I05-23-20260909/RESULT.md), [independent review archive](followon/README.md), and [original-unit fresh second review](followon/pr54_original_second/review_report.md).

Three independent first/second pairs cover distinct units: original RESULT and original fixture; the three near-zero/endpoint addenda plus endpoint fixture extension; and the later outer-wedge/flow/rate appendix with its own checker. A repair closure is not counted as a new reviewer. The original first review's Section5 findings and the addendum second review's wording findings are preserved and explicitly closed below.

## Arbitrary finite cross rank: strict curvature near decoupling

For arbitrary finite strict real kernels `0<A<I`, `0<C<I` and any nonzero real cross block `B`, put `K(t)=[[A,tB],[tB^T,C]]`. There is an explicitly computable positive `delta` such that the path is strict and

`H''(t)<=-3 sigma_ij^2 t^2<0` for `0<abs(t)<=sqrt(delta)`,

where any nonzero entry `B_ij` supplies the positive lower certificate

`sigma_ij^2=B_ij^4/[A_ii C_jj(1-A_ii C_jj)]`.

The original rank-two result has a quadratic complete likelihood and sharper constants. The [arbitrary-rank appendix](../../research/I05-23-20260909/ADDENDUM_ARBITRARY_RANK.md) uses the degree-at-most-rank(B) full likelihood, every coefficient bound, the extra third-derivative term and the complete Fisher. For rational data, certified positive rational spectral-margin lower bounds and an operator-norm upper bound, together with `log 2<=1`, give a rational radius. This is a local theorem; arbitrary internal correlation is allowed, but it does not prove whole-chord concavity.

## Simple legal endpoints

For the same strict blocks and nonzero B, let `t_*>0` be a legal endpoint with strict interior. If either `dim ker K(t_*)=1` or `dim ker(I-K(t_*))=1`, then

`H''(t) -> -infinity` as `t -> t_*` from the interior.

The negative endpoint has the same conclusion by evenness. A simple full or empty complete atom supplies a negative Fisher divergence of order `1/(t_*-t)`, dominating all remaining finite-order atom terms. No rare atom is removed. The [abstract lemma](../../research/I05-23-20260909/ADDENDUM_ENDPOINT_RARE_EVENT.md) now explicitly requires analytic extension through the endpoint; DPP atom polynomials satisfy it.

For rank(B)=2, define `R0=C^(-1/2) B^T A^(-1) B C^(-1/2)` and its `I-A,I-C` counterpart R1. The squared legal endpoint is `1/max(rho0,rho1)`, where rho denotes the top eigenvalue. Any active operator with `Delta=2tr(R^2)-(tr R)^2>0` gives a simple endpoint. If both sides are active, either simple side suffices. Only when every active rank-two operator has equal positive eigenvalues does this criterion fail. [Exact spectral test](../../research/I05-23-20260909/ADDENDUM_RANK2_ENDPOINT_SPECTRUM.md).

The rational dense 3+3 fixture has independently checked endpoint discriminants and exact separation `rho_K<1/25<1/20<rho_I-K`. It is one illustrative fixture, not a global certificate. Multiple/isotropic endpoints and the compact middle interval remain unproved by these endpoint results.

## Full-law matching deficit and two-layer stationary rate

For any cross matching M, let `W_M=sum_(i,j in M) B_ij^2` and `N=m+ell`. With arbitrary rank B and every legal t, including feasible boundaries,

`H(K(0))-H(K(t)) >= t^4 W_M^2/(2N)`.

This is a full-law relative-entropy inequality. The matching observable is a variational test, and SCP concentration is applied to the complete decoupled product law. No projected entropy replaces the joint entropy. A nonzero B permits a matching with W_M>0, so the decoupled center is the unique entropy maximizer along the legal radial family.

For the stationary two-layer Toeplitz setting, h is normalized **per cell containing two observed coordinates**: `h(t)=lim H_n(t)/n`. For a fixed cross offset d,

`h(0)-h(t) >= t^4 abs(b_d)^4/4`.

The finite matching contains `n-abs(d)` pairs and `2n` coordinates; the proof preserves the boundary loss `abs(d)/n` before taking the true stationary rate limit. A nonzero cross symbol gives a nonzero coefficient and strict rate deficit. This is not monotonicity or whole-chord curvature, and it does not supply concave approximants.

## Outer-wedge form and a stronger visible-state obstruction

For the rank-two full likelihood `q_s=1-sa+s^2b`, `s=t^2`, `u=q_s-1`, `y=s^2b`, the [outer-wedge appendix](../../research/I05-23-20260909/ADDENDUM_OUTER_WEDGE_FLOW_RATE.md) proves

`t^2 I''(t)=E[Phi(u)+4y^2/(1+u)+y psi(u)]`,

with `Phi(u)=4u^2/(1+u)+2u log(1+u)>=0` and increasing `psi(u)=8u/(1+u)+10log(1+u)`. The expected contribution not already forced nonnegative is `s^2 W(s)`, `W=E[b psi(u_s)]`. Thus W>=0 and the specified four-sign stochastic-order tests are sufficient only. The universal sign is open.

For every strict correlated two-point real C with nonzero off-diagonal c and invertible real feature frame V, `G_T=V^T(C-E_(T^c))^(-1)V` has `det G_T` equal pointwise to a nonzero linear combination of its three entries. No visible-state linear operator can give degree-one scaling theta and degree-two scaling theta^2 for `0<theta<1`; the same collision rules out generator eigenvalues -1 and -2. Positivity and reversibility are unnecessary for this obstruction. The standard two-point fixture yields the exact rational Farkas right-hand side -1.

This strengthens the earlier reversible-only obstruction in that two-point scope. It does not contradict the accepted fixed three-point nonreversible generator, the m-by-2 entropy theorem, or a possible hidden-state dilation, and is not an entropy counterexample.

## Conditional interfaces retained as conditional

The elementary-imset cone, directed-flow feasibility and second-order entropy-production conditions are accepted as exact interfaces. Pairwise stochastic covering alone does not imply one common square coupling. A floating imset infeasibility artifact was corrected and is not a rational Farkas disproof of the DPP cone.

The original Section5 local rate criterion now explicitly assumes `I_n(0)=I_n'(0)=0`, `I_n''(0)>=c n`, `abs(I_n'''(s))<=L n` with `c>0`, `0<L<infinity` uniformly in n. It transfers finite local curvature to the rate. The extensive first-score lower bound is proved; the uniform third-derivative upper bound remains open.

A separate outer-wedge criterion proves finite Jensen defect at most `(T^2 rho_n/2)*lambda(1-lambda)*(x-y)^2` if `W_n>=-rho_n` uniformly on a common strict legal interval. Pointwise entropy-rate limits and `rho_n/N_n->0` imply concavity, without interchanging derivatives and the volume limit. Generic scalar Toeplitz cuts have growing cross rank, so this rank-two criterion alone is not a new scalar rate theorem.

## Frozen heads, repairs and limits

- Original first head `203f7044`; original RESULT is unchanged through `c8486bcd`. C3's `a1e7f720` implements exactly three Section5 repairs; C1's original reviewer closed them, and C3's fresh second reviewed repaired RESULT at `d5c55447`.
- Three-addendum first/second head `c3b9e968`; `d5c55447` only clarifies endpoint analytic extension and rational spectral substitutes. The independent second reviewer explicitly closed both. Displayed formulas, endpoint code and outputs are unchanged.
- Outer-wedge unit first/second head `c8486bcd`; all its three files are unchanged in the final head. Its historical PR43-open phrase is not the current main status. The expected-contribution wording above resolves the reviewer's nonblocking pointwise-versus-expectation precision note.

All mathematical claims retain the complete configuration law, Fisher and acceleration. The original author fixtures were inspected as exact consistency artifacts, and the endpoint comparison was independently recomputed; this is not an assertion of an independent full author-suite rerun. No broad scan or duplicate C2 issue52 job was run. General correlated whole-chord concavity, global scalar entropy-rate concavity, novelty, CI and formal proof certification remain unclaimed.
