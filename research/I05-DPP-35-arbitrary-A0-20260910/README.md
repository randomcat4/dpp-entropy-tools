# I05-DPP-35 — arbitrary strict A0 center via finite-range complete-event preconditioning

Status: **AUTHOR PROOF IN PROGRESS / PENDING INDEPENDENT REVIEW.**

This is a successor to PR113. It starts from `main@bcbf7016e2abc6401b66f39ac9202d235ee32fad` and does not alter PR82, PR106, PR110, or PR113. No review verdict transfers.

## Target theorem

Let real `c,g in A_0` satisfy

- `c(theta+1/2)=c(theta)`;
- `g(theta+1/2)=-g(theta)`, `g!=0`;
- `delta <= c <= 1-delta` a.e. for some `delta>0`.

Put `mu=c_hat(0)`. For every odd `k` with `g_hat(k)!=0`, the target is to prove that there exists `epsilon>0` such that the true stationary DPP configuration entropy rate for the physical affine path

`K_t=T(c)+t T(g)`

satisfies concavity of

`h(c+t g)+|g_hat(k)|^4 t^4/[8 mu^2(1-mu^2)]`

on `[-epsilon,epsilon]`.

Every complete occupied/vacant event is retained. This is configuration Shannon entropy, not spectral/von-Neumann entropy.

If completed, this removes PR113's small-Wiener center condition rather than merely lowering a positive moment exponent.

## New mechanism

The unweighted convolution-dominated algebra `C_{1,0}` is inverse-closed but does not admit norm-controlled inversion from only the algebra norm and the `ell^2` inverse norm. Therefore PR106/PR110's common-envelope step cannot simply be pushed to bare `A_0` by citing inverse-closedness.

Instead, for the **fixed** strict `A_0` center, choose a half-period-even finite Fourier truncation `c^(L)` with the same mean such that

`r=c-c^(L)`

has arbitrarily small Wiener norm and `c^(L)` remains uniformly strict. For every finite complete word `x`, write

`M_x^0=T(c^(L))-I_{Z_x}`.

Because `M_x^0` is self-adjoint, uniformly gapped away from zero, and finite-band, polynomial approximation of `1/x` on the two spectral intervals gives an event- and volume-uniform exponential off-diagonal bound for `(M_x^0)^(-1)`. In particular there is one summable diagonal envelope `u` with

`sup_x |(M_x^0)^(-1)(i,j)| <= u(i-j)`, `u in ell^1`.

After increasing `L` and shrinking `|t|`, arrange

`||u||_1 ||r+t g||_W < rho < 1`.

Then every full atom has the exact non-product-reference factorization

`p_t(x)=p_0(x) det(I+(M_x^0)^(-1) T(r+t g))`,

where `p_0` is the finite-range reference DPP complete-event law. This supplies a genuine event-uniform trace-log expansion without assuming that the original center is Wiener-small.

## Two load-bearing lemmas being closed

### Lemma A — configuration quasilocality of finite-range event inverses

For two complete words that agree on an `R`-neighborhood of coordinates `i,j`, the corresponding inverse entries satisfy

`|R_x(i,j)-R_y(i,j)| <= C exp(-a R)`

uniformly in the finite volume. The proof uses the resolvent identity under one-site diagonal flips together with the uniform exponential inverse bound. A telescoping local approximation then has shell increments with exponentially summable norm. The support cardinality of an `R`-local approximation is `O(m R)` for an `m`-step trace term and is independent of the physical diameter of the visited vertices.

This cardinality point is essential: complete-event Bell differentiation costs support **size**, not spatial diameter, so no positive Fourier moment is introduced.

### Lemma B — C4 thermodynamic passage relative to the finite-range DPP

Split the true entropy density as

`h_t = - ell_0(t) - d_0(t)`,

where `d_0` is the relative-entropy rate of `p_t` with respect to the finite-range reference `p_0`, and `ell_0(t)` is the reference cross-entropy density `lim n^{-1} E_t log p_0`.

For `d_0`, expand the exact log likelihood ratio into preconditioned closed walks. Use the common `ell^1` diagonal envelope, the shell-localization from Lemma A, and the complete-event derivative bound

`|partial_t^r p_{J,t}(x)| <= p_{J,t}(x) C_r |J|^r`, `r<=4`,

to obtain a derivative majorant summable first in localization shells, then in walk displacements, then in walk length.

For `ell_0`, use the accepted finite-range complete-event conditional potential of the strict reference DPP, whose variations are exponential. Decompose it into local shell increments; the same Bell bound makes `sum_R R^r exp(-aR)` the only differentiation loss.

The intended conclusion is `h(c+t g) in C^4` on a common real interval, with normalized finite-volume derivatives converging through order four. Fisher, atom acceleration, and invariant-law movement are not discarded; they are retained inside the exact complete-event differentiation before the limit.

## Final curvature step once Lemmas A/B close

Half-period symmetry makes the even and odd parity marginals fixed in `t` and independent at `t=0`. Hence

`J(t)=h(c)-h(c+t g)`

is the true parity mutual-information rate, is even and nonnegative, and the accepted regularity-free PR53 matching floor gives the same quartic lower coefficient used in PR113. `C^4` then yields the two-case local corrected-concavity argument.

## Evidence boundary

- New statements here: author proof in progress; no independent review.
- PR53 matching floor and finite-range local conditional regularity: accepted scoped inputs only where explicitly used.
- PR82/PR106/PR110/PR113: comparison/predecessor context, not theorem premises.
- arXiv:1809.04097: comparison source for norm-controlled inversion; it is not used as a black-box theorem for the nonnormal complete-event family.
- No computation, finite-window extrapolation, entropy counterexample, or novelty claim.

## Precise current obstacle

The remaining proof obligation is not inverse existence. It is to write the preconditioned trace terms as exponentially quasilocal complete-event observables with a localization-shell decomposition whose derivative bound is uniform in volume and summable after the `ell^1` displacement sums. Inverse-closedness alone does not supply this common differentiated envelope.