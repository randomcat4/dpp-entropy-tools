# I05-DPP-31 — PR66 low-regularity repair

## Current status

**Original `p>4` theorem: PROVED BY A NEW AUTHOR FINITE-RESPONSE ARGUMENT / PENDING_REVIEW.**

This is not an independent acceptance. The proof depends on the PR66 complete-event inverse and two-leg conditional estimates in their previously reviewed conditional scope, and on the independently accepted regularity-free PR53 matching inequality. The rejected Dobrushin A1/A2 import is not used. FIRST, SECOND, formal verification, machine recomputation and novelty are separate and unclaimed.

Role: theory reviser for PR66, not an independent reviewer. This branch starts from `main@65e59a46b49cd2dbb5c779a4cfae8cef26441984`, preserves PR66 at author head `af1edaad69c4e1f5e4bbd1239b8463b56bf64075`, and continues issue #44 / PR66 without treating old author labels or old RUNNING states as acceptance.

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

and assume a strict pointwise spectral margin `delta<=c<=1-delta`. Put `mu=\widehat c(0)`. For any odd `k` with `\widehat g(k)\ne0`, define

\[
\alpha_k=\frac{|\widehat g(k)|^4}{8\mu^2(1-\mu^2)}.
\]

Then there is `epsilon>0` such that `c+t g` is legal and the true stationary DPP configuration Shannon entropy rate satisfies

\[
t\longmapsto h(c+t g)+\alpha_k t^4
\]

is concave on `[-epsilon,epsilon]`.

The path is the physical affine kernel `K_t=T(c)+tT(g)`. Every complete event enters through the exact one-sided DPP conditional. The transfer operator sums both emitted states and integrates over the full future law, so no rare event or conditional Fisher contribution is deleted. No spectral entropy, fermionic von Neumann entropy, observation-basis rotation, finite-window extrapolation or `L`-affine surrogate is used.

## Why the old import remains invalid

The full Dobrushin 1974 source is available. Its printed pp. 14--15 define classes A1/A2: A1 carries an exponential support-cardinality factor, while A2 removes that factor only for a null-state interaction. PR66's polynomial interval telescope proved an ordinary first-moment bound but neither requirement. The source-access issue was resolved; applicability was not.

This packet does not relabel that first moment as sufficient. It bypasses the interaction-pressure theorem and proves only the finite order of response needed for local concavity.

## Complete-event input and differentiated memory

Set

\[
q=\frac{p+2}{4},\qquad a=2q-1=\frac p2>2.
\]

The re-audited PR66 input gives a single complex parameter disk, uniform over every finite conditioning set and complete configuration, on which the complete-event inverses are bounded in a weighted Schur algebra. A remote conditioned-bit flip is a rank-one diagonal perturbation and the origin conditional has two propagator legs, hence

\[
\sup_{x\stackrel{\ne j}=y}
|\log G_z(\xi|x)-\log G_z(\xi|y)|
\le C(1+j)^{-2q}.
\]

The finite-future conditionals converge uniformly and holomorphically to the true full-future conditional. Strict non-nullness supplies a common logarithm branch. A Banach-valued Cauchy lemma then gives, for `r=0,...,4`,

\[
\operatorname{var}_n(\partial_z^r\log G_z)
=O(n^{1-2q})=O(n^{-a}).
\]

Parameter differentiation consumes no memory exponent. Half-period diagonal conjugacy holds for every complete-event determinant and Schur complement, so `G_z` and `log G_z` are even and factor through `s=z^2`. Only second-order response in `s` is needed.

## Coupling, renewal and one-power Poisson loss

On

\[
\mathcal B_b=\{F:\|F\|_\infty+\sup_n(1+n)^b\operatorname{var}_nF<\infty\},
\]

the explicit Bressaud--Fernandez--Galves ratio coupling applies with the larger monotone majorant

\[
\gamma_m^{(b)}=1-\exp[-C_b(1+m)^{-b}],\qquad 1<b\le a.
\]

The needed polynomial return estimate is reproved internally from the defective renewal equation. If `f_n` is the first-return law of the auxiliary age chain, then `sum f_n<1`, `f_n=O(n^{-b})`, and the renewal sequence obeys

\[
u_0=1,\qquad u_n=\sum_{k=1}^n f_k u_{n-k}.
\]

Finite partial sums give `sum u_n<infinity`; a small/large return-time split then gives `u_n=O(n^{-b})`. Together with the BFG matched-suffix coupling inequality this yields

\[
\operatorname{osc}(\mathcal L_s^nF)
\le C_b\|F\|_b(1+n)^{-b}.
\]

Tracking the first generated mismatch, rather than replacing it by the event that some mismatch occurred, gives

\[
\operatorname{var}_m(\mathcal L_s^nF)
\le C_b\|F\|_b\left[(1+m+n)^{-b}
+\sum_{r=0}^{n-1}(1+m+r)^{-a}(1+n-r)^{-b}\right].
\]

Summing in `n` and exchanging the nonnegative double sum proves the load-bearing estimate

\[
\boxed{\mathcal R_s:\mathcal B_b\to\mathcal B_{b-1}},
\qquad
\mathcal R_sF=\sum_{n\ge0}\mathcal L_s^n(F-\nu_sF),
\qquad b>1.
\]

The earlier `B_b -> B_{b-2}` estimate remains a valid but coarse historical attempt.

## Exact threshold accounting for this route

The weighted inverse construction requires

\[
2q+1<p,
\]

while two finite-response Poisson inverses require

\[
2q-1>2,
\quad\text{equivalently }q>3/2.
\]

A `q` satisfying both inequalities exists exactly when `p>4`; the displayed choice `q=(p+2)/4` lies strictly between the two endpoints. Thus `p>4` is the exact threshold of this particular weighted-inverse plus two-Poisson route. This is not a claim that the entropy theorem itself fails at `p=4` or below.

## Finite second-order response

The exact invariant-measure identity is

\[
(\nu_u-\nu_s)(F)
=\nu_u(\mathcal L_u-\mathcal L_s)\mathcal R_sF.
\]

It gives, by difference quotients,

\[
D\nu_s(F)=\nu_s(A_{1,s}\mathcal R_sF),
\]

\[
D^2\nu_s(F)=
\nu_s(A_{2,s}\mathcal R_sF)
+2\nu_s\bigl(A_{1,s}\mathcal R_s(A_{1,s}\mathcal R_sF)\bigr).
\]

For a moving observable add `nu_s(F_s'')+2 nu_s(A_{1,s}R_sF_s')`. The two response orders use

\[
\mathcal B_a\xrightarrow{\mathcal R_s}\mathcal B_{a-1}
\xrightarrow{\mathcal R_s}\mathcal B_{a-2},
\]

which is legal exactly when `a>2`.

No generic assertion that summable variation implies fourth-order response is used. Weak continuity of the invariant law follows directly from the DPP complete-event determinant formula: every cylinder probability is an even polynomial in `t`, hence a polynomial in `s=t^2`. Invariance follows from the exact full-future conditional, and uniqueness follows from the same coupling relaxation.

For continuity of the nested response choose `eta_1,eta_2>0` with

\[
\eta_1+\eta_2<a-2.
\]

Sup-norm continuity of each Poisson series plus a common `B_{b-1}` bound yields continuity in `B_{b-1-eta}` by interpolation. Applying this first to `R_sF_s` and then to `R_s(A_{1,s}R_sF_s)` leaves the positive final exponent `a-2-eta_1-eta_2`. Thus no stronger hidden threshold occurs in the remainder argument.

## Entropy and quartic coefficient

For `ell_s=log G_s`, parity independence at the center and fixed parity marginals give the exact true-rate deficit

\[
D(s):=h(c)-h(c+\sqrt s\,g)
=\nu_s(\ell_s-\ell_0).
\]

Normalization gives `D'(0)=0`, so the finite-response result gives

\[
D(s)=A s^2+o(s^2).
\]

The independently accepted regularity-free PR53 matching inequality implies

\[
A\ge\frac{|\widehat g(k)|^4}{4\mu^2(1-\mu^2)}=2\alpha_k.
\]

Consequently

\[
h''(t)=-12A t^2+o(t^2),
\]

and the corrected entropy has negative second derivative for every sufficiently small nonzero `t`, with second derivative zero at the center. This is the centered Peano/fourth-coefficient conclusion supplied by `C^2` response in `s`; full classical `C^4` regularity at every nonzero parameter is not claimed.

## Boundary and remainder statement

The first p4 draft claimed that the stationary second response of a frozen-future memory-`N` kernel converged at the raw kernel norm rate. That stronger statement was not proved and is explicitly withdrawn in `c4_response_p4_boundary_correction.md`; the failed assertion remains visible in the historical main-file section and commit record.

The proved uniform remainder is a finite time-correlation/Poisson cutoff. For every

\[
0<\eta<a-2,
\]

all terms in the second-response formula are approximated by correlation times below `N` with scalar error

\[
O(N^{-\eta}).
\]

This is sufficient for the response argument. It is not a finite-volume curvature extrapolation and not a claim about the stationary law of the frozen-memory approximation. The raw normalized conditional itself still has the independently proved memory truncation estimate `O(N^{b-a})` in `B_b`, `b<a`; only the unsupported transfer of that exact rate to stationary second response was withdrawn.

## Authoritative file order and failure ledger

1. `c4_response_p4_repair.md`: main author proof. Its equations (7.3)--(7.5) must be read as withdrawn by item 2.
2. `c4_response_p4_boundary_correction.md`: valid Poisson/correlation cutoff and exact withdrawal.
3. `c4_response_p4_pr66_dependency_audit.md`: rederivation of the complete-event singular gap, weighted inverse, common complex disk, two-leg influence, full-future limit, non-null logarithm and parity input; stops before the invalid Dobrushin step.
4. `c4_response_p4_selfcontained_closures.md`: internal defective-renewal polynomial estimate and `B_a`-valued Cauchy lemma.
5. `c4_response_p4_source_audit.md`: direct map to BFG equations and response difference quotients.
6. `c4_response_p4_measure_continuity.md`: DPP cylinder continuity, invariance and uniqueness without a general parameter-continuity theorem for `g`-measures.
7. `c4_response_p4_continuity_detail.md`: two explicit interpolation losses and complete second-response remainder proof.
8. `c4_response_p8.md` and `c4_response_p8_correction.md`: preserved earlier coarse proof. Its two-power Poisson loss is valid but non-sharp and yielded only `p>8`.
9. Earlier PR82 commits preserve the inverse-localization obstruction, finite determinant Möbius/closed-walk A2 candidate and exact Dobrushin failure record.

The A2 closed-walk route remains a backup and is not advanced in parallel in this unit. The proof makes no claim for `p<=4`, a whole legal interval, arbitrary measurable symbols, a DPP entropy counterexample, or novelty/priority.

Independent review status: **PENDING_REVIEW**. Issue #92 is the version-bound audit contract. No review or Codex job is considered started unless the issue is explicitly claimed.