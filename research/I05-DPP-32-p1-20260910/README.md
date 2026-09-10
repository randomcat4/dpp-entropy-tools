# I05-DPP-32 — low-regularity entropy response below the PR82 threshold

## Status

Two author results are proved in this successor packet:

1. **Local corrected concavity for every `p>=1`.**
2. **The exact centered quartic/Fisher expansion for every `p>=1/2`.**

Independent review: **PENDING_REVIEW / not assumed started**.

This is a successor to PR82, not an edit of its frozen theorem evidence. The
PR82 theorem at frozen head `6ecc004a...` has scoped FIRST and isolated SECOND
for `p>4`. Those reviews do not transfer to either theorem here. Novelty,
formal verification and machine recomputation are unassessed.

## Main theorem: local corrected concavity

For `p>=1`, let

\[
\mathcal A_p=\left\{u:\sum_{m\in\mathbb Z}(1+|m|)^p
 |\widehat u(m)|<\infty\right\}.
\]

Let real `c,g in A_p` satisfy

\[
c(\theta+1/2)=c(\theta),
\qquad g(\theta+1/2)=-g(\theta),
\qquad g\ne0,
\qquad \delta\le c\le1-\delta.
\]

Put `mu=\widehat c(0)`. For every odd `k` with
`\widehat g(k)\ne0`, define

\[
\alpha_k=
\frac{|\widehat g(k)|^4}{8\mu^2(1-\mu^2)}.
\]

Then there exists `epsilon>0` such that the physical affine symbol `c+tg` is
legal and the true stationary DPP configuration Shannon entropy rate obeys

\[
t\longmapsto h(c+tg)+\alpha_k t^4
\]

concave on `[-epsilon,epsilon]`.

This includes the previously open range `1<=p<=4` and the endpoint `p=1`.
It makes no assertion that `p=1` is sharp.

## Weaker theorem below the concavity threshold

For every `p>=1/2` under the same structural and strict-margin hypotheses,
write `s=t^2` and let `G_s` be the true complete-event one-sided conditional.
Then

\[
h(c+t g)
=h(c)-\frac12\mathcal I_s(0)t^4+o(t^4),
\]

where

\[
\mathcal I_s(0)
=\nu_0\left[
 \left(\left.\partial_s\log G_s(X_0|X_1,X_2,\ldots)
 \right|_{s=0}\right)^2
\right].
\]

This is the full conditional Fisher information per site: both emitted states,
all complete events and the full future law are retained. The accepted PR53
matching inequality gives

\[
\frac12\mathcal I_s(0)
\ge\frac{|\widehat g(k)|^4}{4\mu^2(1-\mu^2)}.
\]

For `1/2<=p<1`, this centered expansion is **not** promoted to local concavity:
it gives no control of the curvature at nearby nonzero parameters.

## New proof mechanism

The old PR82 threshold had two avoidable losses.

1. A band-truncation proof spent Fourier regularity in order to obtain a common
   inverse norm.
2. The two propagator legs were separately replaced by pointwise power bounds,
   discarding their weighted `l^1` moments.

The replacement proof applies Fang--Shin norm-controlled BGS inversion to one
block-diagonal matrix containing every finite window and complete word. This
gives a common complete-event inverse envelope `d in l^1_p`. The two
conditional legs have a common envelope `e in l^1_p`, hence their rank-one
product satisfies

\[
\sum_j(1+j)^{2p}e(j)^2<\infty.
\]

The effective coupling used to add the last future site is bounded by
`a+a*d*a`; this term is included explicitly in the integrated localization
proof. Cauchy's formula preserves the doubled moment for all parameter
derivatives needed through order four.

At `p=1`, the conditional derivative variations have a finite first moment.
The BFG coupling is used on

\[
\mathcal V_1
=\left\{F:\sum_m(m+1)\operatorname{var}_mF<\infty\right\},
\qquad
\mathcal V_0
=\left\{F:\sum_m\operatorname{var}_mF<\infty\right\}.
\]

The exact Poisson mappings are

\[
\mathcal R_s:\mathcal V_1\to\mathcal V_0,
\qquad
\mathcal R_s:\mathcal V_0\to C(X).
\]

They give second-order response in `s=t^2` without treating summable variation
as a black-box differentiability theorem.

For the true entropy deficit

\[
D(s)=h(c)-h(c+\sqrt s\,g)
=\nu_s(\log G_s-\log G_0),
\]

fixed parity marginals and normalization give `D'(0)=0`. In the `p>=1` range,
second response gives `D(s)=A s^2+o(s^2)` and a continuous curvature expansion.
The accepted regularity-free PR53 matching inequality gives `A>=2 alpha_k`,
so

\[
h''(t)=-12A t^2+o(t^2).
\]

In the `p>=1/2` range, one response suffices to identify
`A=\mathcal I_s(0)/2`, but not to control nearby curvature.

## Files and reading order

1. `beurling_complete_event_localization.md` — direct-sum BGS inversion,
   common complex complete-event envelope, corrected endpoint coupling,
   two-leg doubled moment and derivative memory bounds.
2. `technical_closures.md` — explicit family-envelope algebra and uniform
   endpoint Poisson tails.
3. `moment_response_and_entropy.md` — defective-renewal and Poisson estimates,
   finite second response on moment spaces, and local concavity for `p>=1`.
4. `center_quartic_p_half.md` — one-response Fisher representation and centered
   quartic expansion for `p>=1/2`; explicitly not a concavity theorem below 1.
5. `sources_scope_failures.md` — primary theorem/page map, comparison with BFG,
   Fernandez--Maillard, Tanaka and Dobrushin, and the exact remaining gaps.

## Object and evidence control

All finite conditional inputs are ratios of complete-event determinants for
`K_t=T(c)+tT(g)`. Both emitted states and the full invariant future law are
retained. No spectral or fermionic entropy, basis rotation, `L`-affine path,
finite-window sign extrapolation, omitted rare event, or truncated Fisher term
is used.

No code, numerical search, or external machine certificate is used. The
results are author theorems pending independent source/proof review. No result
here asserts a whole legal interval, arbitrary measurable symbols, local
concavity for `p<1`, a DPP entropy counterexample, or novelty.
