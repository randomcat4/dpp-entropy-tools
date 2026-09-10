# I05-DPP-33 — Fourier-Sobolev H1 local entropy-rate concavity

## Status

**PROVED AS AN AUTHOR THEOREM / PENDING INDEPENDENT REVIEW.**

This is a successor to PR82 and PR106. It does not modify either proof branch and inherits no review verdict attached to them. The theorem below is a new structural class: weighted Fourier `ell^2`, rather than weighted Fourier `ell^1`.

The path is always the physical affine kernel

\[
K_t=T(c)+tT(g).
\]

All complete configuration events enter through their exact determinant conditionals. No spectral entropy, fermionic von Neumann entropy, observation-basis rotation, finite-window curvature extrapolation, or `L`-affine path is used.

## Theorem

Define

\[
\mathcal H^1_{\rm F}
:=\left\{u:\sum_{m\in\mathbb Z}(1+|m|)^2|\widehat u(m)|^2<\infty\right\}.
\]

Let real `c,g in H^1_F` satisfy

\[
c(\theta+1/2)=c(\theta),\qquad
 g(\theta+1/2)=-g(\theta),\qquad g\ne0,
\]

and assume a strict spectral margin

\[
\delta\le c(\theta)\le1-\delta
\]

for some `delta>0`. Put `mu=\widehat c(0)`. For every odd `k` with `\widehat g(k)\ne0`, set

\[
\alpha_k=\frac{|\widehat g(k)|^4}{8\mu^2(1-\mu^2)}.
\]

Then there exists `epsilon>0` such that `c+t g` is legal and the true stationary DPP configuration Shannon entropy rate obeys

\[
t\longmapsto h(c+t g)+\alpha_k t^4
\]

is concave on `[-epsilon,epsilon]`, and its second derivative is strictly negative away from `t=0` in that interval.

## Why this is genuinely outside the previous A_p theorem

The class `H^1_F` is not contained in `A_1`. For example, with sufficiently small positive `eta`,

\[
\begin{aligned}
c(\theta)&=\frac13+\eta\sum_{m\ge1}(2m)^{-7/4}\cos(4\pi m\theta),\\
g(\theta)&=\eta\sum_{m\ge0}(2m+1)^{-7/4}\cos(2\pi(2m+1)\theta)
\end{aligned}
\]

satisfy the strict margin and the required half-period symmetries. Both lie in `H^1_F`, but neither lies in `A_1`, since the weighted `ell^1` series behaves as `sum n^{-3/4}`. They lie in every `A_p` with `p<3/4`. The center is nonconstant and has mean `1/3`, so this example is not the constant-center theorem and is not the mean-`1/2` Wiener-small theorem.

Thus the theorem supplies explicit power-law symbols in low `A_p` classes, including `p<=1/2`, for which the corrected true entropy rate is locally concave.

## Proof architecture

1. Enumerate all finite complete-event matrices and translate their finite coordinate sets into pairwise disjoint blocks of one subset `Lambda subset Z`. This one-dimensional packing preserves every within-block distance.
2. The single block-direct-sum matrix belongs to the one-dimensional convolution-dominated algebra `C^{2,1}`. Its uniform complete-event coercivity makes the direct sum invertible on `ell^2(Lambda)`.
3. The norm-controlled inverse theorem for `C^{p,r}` matrices applies with ambient dimension `d=1`, matrix exponent `p_mtx=2`, and weight `r=1>1/2`. It produces one common weighted-`ell^2` diagonal envelope for every complete-event inverse. The single direct sum avoids exchanging a supremum over events with an infinite sum.
4. A Banach-algebra Neumann series gives one common complex parameter disk and a common envelope. The origin conditional has two propagator legs. Each leg lies in weighted `ell^2_1`; its square therefore has a finite second moment.
5. Consequently `log G_s` and its first two `s=t^2` derivatives have a common variation majorant whose first moment is finite.
6. A source-bound Bressaud--Fernandez--Galves coupling calculation gives

   \[
   R:V_1\to V_0,\qquad R:V_0\to C,
   \]

   for the reduced Poisson inverse. Two response orders in `s` therefore close without invoking Dobrushin A1/A2 or an unstated high-order theorem for summable variations.
7. The exact complete-event parity identity gives fixed parity marginals and an even family. The true entropy deficit satisfies

   \[
   D(s)=h(c)-h(c+\sqrt{s}g)=\nu_s(\ell_s-\ell_0),\qquad D'(0)=0.
   \]

   Hence `D(s)=A s^2+o(s^2)`. The accepted regularity-free PR53 matching inequality gives `A>=2 alpha_k`, yielding the claimed local curvature sign.

## Files

- `complete_event_H1_localization.md`: one-dimensional packing, exact external theorem map, common inverse/leg envelopes, differentiated memory moments.
- `moment_response_entropy.md`: self-contained moment-space coupling, two Poisson response orders, true entropy-rate conclusion.
- `explicit_power_law_family.md`: full verification that the displayed family lies in `H^1_F`, lies outside `A_1`, and avoids previously accepted special classes.
- `sources_scope_failures.md`: primary-source mapping, alternative route comparison, and exact nonclaims.
- `review_contract.md`: independent audit units and stop conditions.

## Evidence separation

- theorem and all new lemmas: author proofs in this PR;
- PR82 qualitative `p>4` result: separate frozen FIRST/SECOND evidence, not inherited here;
- PR106 `A_p, p>=1` theorem: separate author work, not used as an accepted premise;
- machine computation: none;
- novelty: NOT_ASSESSED;
- independent review: PENDING_REVIEW until a reviewer explicitly claims the companion issue.

No claim is made for every member of `A_p` when `p<1`, for the whole legal interval, for arbitrary measurable symbols, or for an entropy counterexample below this regularity.