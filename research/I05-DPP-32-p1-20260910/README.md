# I05-DPP-32 — low-regularity entropy response below the PR82 threshold

## Status

**The `A_p` theorem is proved here for every `p>=1` as an author proof.**

Independent review: **PENDING_REVIEW / not assumed started**.

This is a successor to PR82, not an edit of its frozen theorem evidence.  The
PR82 theorem at frozen head `6ecc004a...` has scoped FIRST and isolated SECOND
for `p>4`.  Those reviews do not transfer to this new theorem.

## Theorem

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

Put `mu=\widehat c(0)`.  For every odd `k` with
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
It makes no assertion for `0<p<1`, a whole legal interval, arbitrary measurable
symbols, or optimality.

## New proof mechanism

The old PR82 threshold had two avoidable losses.

1. A band-truncation proof spent Fourier regularity in order to obtain a common
   inverse norm.
2. The two propagator legs were separately replaced by pointwise power bounds,
   discarding their weighted `l^1` moments.

The replacement proof applies Fang--Shin norm-controlled inversion to one
block-diagonal matrix containing every finite window and complete word.  This
gives a common complete-event inverse envelope `d in l^1_p`.  The two
conditional legs have a common envelope `e in l^1_p`, hence their rank-one
product satisfies

\[
\sum_j(1+j)^{2p}e(j)^2<\infty.
\]

Cauchy's formula preserves this doubled moment for all parameter derivatives
needed through order four.

At `p=1`, the conditional derivative variations therefore have a finite first
moment.  The BFG coupling is then used on the moment spaces

\[
\mathcal V_1
=\left\{F:\sum_m(m+1)\operatorname{var}_mF<\infty\right\},
\qquad
\mathcal V_0
=\left\{F:\sum_m\operatorname{var}_mF<\infty\right\}.
\]

The two exact Poisson mappings are

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

fixed parity marginals and normalization give `D'(0)=0`.  Thus
`D(s)=A s^2+o(s^2)`.  The accepted regularity-free PR53 matching inequality
gives `A>=2 alpha_k`, and hence

\[
h''(t)=-12A t^2+o(t^2).
\]

## Files

1. `beurling_complete_event_localization.md` — direct-sum BGS inversion,
   common complex complete-event envelope, two-leg doubled moment, and
   derivative memory bounds.
2. `moment_response_and_entropy.md` — self-contained defective-renewal and
   Poisson estimates, finite second response on moment spaces, and the true
   entropy-rate conclusion.
3. `sources_scope_failures.md` — primary theorem/page map, comparison with BFG,
   Fernandez--Maillard, Tanaka and Dobrushin, and the exact remaining `p<1`
   gap.

## Object and evidence control

All finite conditional inputs are ratios of complete-event determinants for
`K_t=T(c)+tT(g)`.  Both emitted states and the full invariant future law are
retained.  No spectral or fermionic entropy, basis rotation, `L`-affine path,
finite-window sign extrapolation, omitted rare event, or truncated Fisher term
is used.

No code, numerical search, or external machine certificate is used.  The
result is an author theorem pending independent source/proof review; novelty is
separate and unassessed.
