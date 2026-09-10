# C4 finite-response repair at the original `p>4` threshold

Status: **QUALITATIVE THEOREM ACCEPTED_SCOPED AT FROZEN FIRST AND ISOLATED SECOND; THIS CURRENT-HEAD STATIC INTEGRATION IS NOT A NEW REVIEW.**

This path is now the authoritative integrated index for the qualitative PR82
proof.  The exact pre-fix source, including the withdrawn boundary equations
`(7.3)--(7.5)`, is preserved without alteration at

`archive/c4_response_p4_repair_with_withdrawn_7_3_7_5.md`.

Those three equations are **not part of the theorem**.  Their valid replacement
is the time-correlation/Poisson cutoff proved in
`c4_response_p4_boundary_correction.md`.  The archived source remains evidence
of the failed extra claim; it is not silently erased.

The scoped FIRST/SECOND apply to the qualitative theorem at frozen head
`6ecc004a3f99f97369ea5af53f1136b59cf2129c`, read together with the correction
priority.  Later quantitative files and this static integration do not inherit
that review automatically.

## 1. The qualitative theorem

For `p>4`, let

\[
\mathcal A_p=
\left\{u:\sum_{m\in\mathbb Z}(1+|m|)^p|\widehat u(m)|<\infty\right\}.
\]

Let real `c,g in A_p` satisfy

\[
c(\theta+1/2)=c(\theta),\qquad
 g(\theta+1/2)=-g(\theta),\qquad g\ne0,
\]

and assume a strict spectral margin

\[
\delta\le c\le1-\delta.
\]

Put `mu=\widehat c(0)`.  For every odd `k` with
`\widehat g(k)\ne0`, define

\[
\alpha_k=
\frac{|\widehat g(k)|^4}{8\mu^2(1-\mu^2)}.
\]

Then there is `epsilon>0` such that the physical affine kernel

\[
K_t=T(c)+tT(g)
\]

is legal and

\[
t\longmapsto h(c+t g)+\alpha_k t^4
\]

is concave on `[-epsilon,epsilon]`, where `h` is the true stationary DPP
configuration Shannon entropy rate.

Every emitted state, complete event and full future is retained.  No spectral
or fermionic entropy, observation-basis rotation, `L`-affine path, finite-window
curvature extrapolation, or deleted Fisher/acceleration term is used.

## 2. Complete-event input

Set

\[
q=\frac{p+2}{4},\qquad a=2q-1=\frac p2>2.
\]

The complete-event calculation gives one complex parameter disk, uniform in
the conditioning window and complete word, on which the one-sided conditional
`G_z` is non-null and

\[
\sup_{x\stackrel{\ne j}=y,\xi}
|\log G_z(\xi|x)-\log G_z(\xi|y)|
\le C(1+j)^{-2q}.
\]

Cauchy's formula on a smaller disk preserves this estimate through the needed
parameter derivatives.  Therefore

\[
\operatorname{var}_n(\partial_z^r\log G_z)
=O(n^{-a}),\qquad r=0,\ldots,4.
\]

The source derivation of the complete-event singular gap, weighted inverse,
common disk, two-leg rank-one influence, full-future Schur limit and non-null
logarithm is preserved in
`c4_response_p4_pr66_dependency_audit.md`.

## 3. Parity and the response parameter

With `D_{jj}=(-1)^j`,

\[
T(c-zg)=D\,T(c+zg)D.
\]

Every complete-event diagonal commutes with `D`.  Thus every complete-event
probability and Schur-complement conditional is even in `z`.  Write

\[
s=z^2.
\]

Only second-order response in `s` is needed; no full pressure analyticity is
used.

## 4. BFG coupling and the one-power Poisson loss

For

\[
\mathcal B_b=
\left\{F:\|F\|_\infty+\sup_n(1+n)^b\operatorname{var}_nF<\infty\right\},
\]

the explicit Bressaud--Fernandez--Galves ratio coupling and its defective
renewal equation give, for `1<b<=a`,

\[
\operatorname{osc}(\mathcal L_s^nF)
\le C_b\|F\|_b(1+n)^{-b}.
\]

Keeping the time of the first generated mismatch gives

\[
\operatorname{var}_m(\mathcal L_s^nF)
\le C_b\|F\|_b\left[(1+m+n)^{-b}
+\sum_{r=0}^{n-1}(1+m+r)^{-a}(1+n-r)^{-b}\right].
\]

Summing in `n` and exchanging the nonnegative double sum proves

\[
\boxed{\mathcal R_s:\mathcal B_b\to\mathcal B_{b-1}},
\qquad
\mathcal R_sF=
\sum_{n\ge0}\mathcal L_s^n(F-\nu_sF),
\qquad b>1.
\]

The source-bound BFG map and the self-contained renewal proof are in
`c4_response_p4_source_audit.md` and
`c4_response_p4_selfcontained_closures.md`.

## 5. Two finite response orders

Invariance and the Poisson identity give the exact formula

\[
(\nu_u-\nu_s)(F)
=\nu_u(\mathcal L_u-\mathcal L_s)\mathcal R_sF.
\]

Difference quotients yield

\[
D\nu_s(F)=\nu_s(A_{1,s}\mathcal R_sF),
\]

\[
D^2\nu_s(F)=
\nu_s(A_{2,s}\mathcal R_sF)
+2\nu_s\bigl(A_{1,s}\mathcal R_s(A_{1,s}\mathcal R_sF)\bigr).
\]

For a moving observable `F_s`, add

\[
\nu_s(F_s'')+2\nu_s(A_{1,s}\mathcal R_sF_s').
\]

Thus the operator acceleration `A_2`, the nested response/Fisher term and the
moving-observable terms are all present.  The two Poisson inverses use

\[
\mathcal B_a\xrightarrow{\mathcal R_s}\mathcal B_{a-1}
\xrightarrow{\mathcal R_s}\mathcal B_{a-2},
\]

which is legal exactly when `a>2`, i.e. `p>4`.  Continuity of all terms is
proved with two explicit interpolation losses in
`c4_response_p4_continuity_detail.md`.  DPP cylinder continuity, invariance and
uniqueness are proved in `c4_response_p4_measure_continuity.md`.

## 6. True entropy-rate bridge

Let

\[
\ell_s=\log G_s,
\qquad h_s=-\nu_s(\ell_s).
\]

At the center the two parity sublattices are independent, and each parity
marginal is fixed along the physical path.  Hence

\[
D(s):=h(c)-h(c+\sqrt s\,g)
=\nu_s(\ell_s-\ell_0).
\]

Normalization gives

\[
\mathcal L_0\ell'_0=0,
\qquad D'(0)=0.
\]

Second response gives

\[
D(s)=A s^2+o(s^2).
\]

The accepted regularity-free PR53 matching inequality yields

\[
A\ge
\frac{|\widehat g(k)|^4}{4\mu^2(1-\mu^2)}
=2\alpha_k.
\]

Therefore

\[
h''(t)=-12A t^2+o(t^2)
\]

and

\[
\frac{d^2}{dt^2}
\{h(c+t g)+\alpha_k t^4\}
=-12(A-\alpha_k)t^2+o(t^2)<0
\]

for sufficiently small nonzero `t`; the second derivative is zero at the
center.  This proves the local qualitative theorem.

## 7. Correct boundary statement

The following old assertion is withdrawn and absent from this integrated
source:

```text
raw frozen-memory stationary second-response error = O(N^{b-a}).
```

What is proved, and what the qualitative theorem may use as a checkable
finite-response remainder, is a **time-correlation cutoff**.  If

\[
\mathcal R_s^{<N}F
=\sum_{n=0}^{N-1}\mathcal L_s^n(F-\nu_sF),
\]

then for every `0<eta<a-2`, all terms in the second-response formula are
approximated by their time-`N` Poisson cutoffs with scalar error

\[
\boxed{O(N^{-\eta})}.
\]

The full proof, including the interpolated inner-tail estimate and nested-term
decomposition, is `c4_response_p4_boundary_correction.md`.

This is not a finite-window entropy Hessian sign extrapolation.  It does not
identify the memory-frozen compatible chain with a finite Toeplitz-section
DPP.  Later spatial-memory convergence files are separate current-head author
results and do not inherit the frozen qualitative reviews.

## 8. Source and scope ledger

The invalid Dobrushin 1974 import is not used.  A1 carries an exponential
support-cardinality condition; A2 requires a controlled null-state
interaction.  The ordinary first moment of PR66's interval telescope proves
neither.

Tanaka's perturbation theory is only an assumptions check: its same-space
reduced-resolvent/Lasota--Yorke hypotheses are not inferred from summable
variation.  The finite response above is derived directly.

Not claimed here: a whole legal interval, `p<=4`, arbitrary measurable
symbols, an entropy counterexample, the withdrawn raw frozen-memory rate,
novelty, or review of later PR82 additions.
