# I05-DPP-31 — PR66 low-regularity repair

## Current status

**Original `p>4` theorem: PROVED BY A NEW AUTHOR FINITE-RESPONSE ARGUMENT / PENDING_REVIEW.**

This is not an independent acceptance.  The proof still depends on the PR66 complete-event inverse and two-leg conditional estimates in their previously reviewed conditional scope, and on the independently accepted regularity-free PR53 matching inequality.  The rejected Dobrushin A1/A2 import is not used.  FIRST, SECOND, formal verification, machine recomputation and novelty are all separate and presently unclaimed.

Role: theory reviser for PR66, not an independent reviewer.  This branch starts from `main@65e59a46b49cd2dbb5c779a4cfae8cef26441984`, preserves PR66 at author head `af1edaad69c4e1f5e4bbd1239b8463b56bf64075`, and continues issue #44 / PR66 without treating old author labels or old RUNNING states as acceptance.

## Repaired theorem

For `p>4`, let

\[
\mathcal A_p=\left\{u:\sum_{m\in\mathbb Z}(1+|m|)^p|\widehat u(m)|<\infty\right\}.
\]

Let real `c,g in A_p` satisfy

\[
c(\theta+1/2)=c(\theta),\qquad
g(\theta+1/2)=-g(\theta),\qquad g\ne0,
\]

and assume a strict pointwise spectral margin `delta<=c<=1-delta`.  Put `mu=\widehat c(0)`.  For any odd `k` with `\widehat g(k)\ne0`, define

\[
\alpha_k=\frac{|\widehat g(k)|^4}{8\mu^2(1-\mu^2)}.
\]

Then there is `epsilon>0` such that `c+t g` is legal and the true stationary DPP configuration Shannon entropy rate satisfies

\[
t\longmapsto h(c+t g)+\alpha_k t^4
\]

is concave on `[-epsilon,epsilon]`.

The path is the physical affine kernel `K_t=T(c)+tT(g)`.  All complete events enter through the exact one-sided DPP conditional.  No spectral entropy, fermionic von Neumann entropy, observation-basis rotation, finite-window extrapolation or `L`-affine surrogate is used.

## Why the old import remains invalid

The full Dobrushin 1974 source is available.  Its printed pp. 14--15 define classes A1/A2: A1 carries an exponential support-cardinality factor, while A2 replaces that requirement only for a null-state interaction.  PR66's polynomial interval telescope proved an ordinary first-moment bound but neither requirement.  The source-access issue was resolved; applicability was not.

This packet does not relabel that first moment as sufficient.  Instead it bypasses the interaction-pressure theorem and proves only the finite order of response needed for local concavity.

## Finite-response spine

Set

\[
q=\frac{p+2}{4},\qquad a=2q-1=\frac p2>2.
\]

The retained PR66 two-leg estimate gives a common complex parameter disk and

\[
\sup_{x\stackrel{\ne j}=y}
|\log G_z(\xi|x)-\log G_z(\xi|y)|
\le C(1+j)^{-2q}.
\]

Cauchy's formula shows that parameter derivatives through order four retain the same single-coordinate decay.  Agreement through memory `n` therefore gives

\[
\operatorname{var}_n(\partial_z^r\log G_z)
=O(n^{1-2q})=O(n^{-a}),\qquad r=0,\ldots,4.
\]

Half-period conjugacy makes every complete event invariant under `z -> -z`, so the normalized conditional factors through `s=z^2`.  Only second-order response in `s` is needed.

On

\[
\mathcal B_b=\{F:\|F\|_\infty+\sup_n(1+n)^b\operatorname{var}_nF<\infty\},
\]

the Bressaud--Fernandez--Galves coupling gives polynomial relaxation for every `1<b<=a`.  Tracking the first generated mismatch, rather than replacing it by the event that some mismatch occurred, proves the sharp estimate used here:

\[
\boxed{\mathcal R_s:\mathcal B_b\to\mathcal B_{b-1}},
\qquad
\mathcal R_sF=\sum_{n\ge0}\mathcal L_s^n(F-\nu_sF).
\]

Thus two response orders use

\[
\mathcal B_a\xrightarrow{\mathcal R_s}\mathcal B_{a-1}
\xrightarrow{\mathcal R_s}\mathcal B_{a-2},
\]

which is legal exactly when `a>2`, hence at the original threshold `p>4`.

The exact perturbation identity

\[
(\nu_u-\nu_s)(F)
=\nu_u(\mathcal L_u-\mathcal L_s)\mathcal R_sF
\]

gives

\[
D\nu_s(F)=\nu_s(A_{1,s}\mathcal R_sF),
\]

\[
D^2\nu_s(F)=
\nu_s(A_{2,s}\mathcal R_sF)
+2\nu_s\bigl(A_{1,s}\mathcal R_s(A_{1,s}\mathcal R_sF)\bigr).
\]

These formulas are proved by difference quotients on the displayed scale; no generic claim that summable variation automatically implies fourth-order response is made.

For `ell_s=log G_s`, parity independence at the center and fixed parity marginals give the exact true-rate deficit

\[
D(s):=h(c)-h(c+\sqrt s\,g)
=\nu_s(\ell_s-\ell_0).
\]

Normalization gives `D'(0)=0`, so `D(s)=A s^2+o(s^2)`.  The accepted PR53 matching inequality implies

\[
A\ge\frac{|\widehat g(k)|^4}{4\mu^2(1-\mu^2)}=2\alpha_k.
\]

Consequently

\[
h''(t)=-12A t^2+o(t^2),
\]

and the corrected entropy has negative second derivative for every sufficiently small nonzero `t`, with second derivative zero at the center.

## Boundary and remainder statement

The original p4 draft briefly claimed that the stationary second response of a frozen-future memory-`N` kernel converged at the raw kernel norm rate.  That stronger statement was not proved and is explicitly withdrawn in `c4_response_p4_boundary_correction.md`.

The proved uniform remainder is a finite time-correlation/Poisson cutoff.  For every

\[
0<\eta<a-2,
\]

all terms in the second-response formula are approximated by correlation times below `N` with scalar error

\[
O(N^{-\eta}).
\]

This is sufficient for the response argument.  It is not a finite-volume curvature extrapolation and not a claim about the stationary law of the frozen-memory approximation.

## File and failure ledger

- `c4_response_p4_repair.md`: complete author proof at the original `p>4` threshold.
- `c4_response_p4_boundary_correction.md`: withdrawal of the overstrong frozen-memory response rate and proof of the valid Poisson cutoff bound.
- `c4_response_p4_source_audit.md`: fresh author re-derivation tied directly to BFG equations and the response difference quotient.
- `c4_response_p8.md` and `c4_response_p8_correction.md`: preserved earlier coarse proof.  Its two-power Poisson loss is valid but non-sharp; it yielded only the weaker `p>8` threshold.
- this directory's earlier commits preserve the inverse-localization obstruction, finite determinant Möbius/closed-walk A2 candidate, and the exact Dobrushin failure record.

The A2 closed-walk route remains a backup and is not advanced in parallel in this unit.  The proof makes no claim for `p<=4`, a whole legal interval, arbitrary measurable symbols, a DPP entropy counterexample, or a novelty/priority result.

Independent review status: **PENDING_REVIEW**.  No review or Codex job is considered started unless a corresponding issue is explicitly claimed.