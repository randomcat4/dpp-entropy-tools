# I05-DPP-31 — PR66 low-regularity repair

## Evidence status

The qualitative theorem below was proved by the author at frozen head
`6ecc004a3f99f97369ea5af53f1136b59cf2129c` and received a scoped FIRST and an
isolated SECOND.  The public integration checkpoint is
`docs/verification_round4_20260909/pr82_6ecc_checkpoint.md` on `main`.

This does **not** transfer review to later PR82 additions.  In particular the
current-head quantitative frozen-memory files, including the multiscale rate at
`3209ee27a03366909d74b812fb06de3391b3ce54`, remain author proofs pending a
fresh version-bound review.  Novelty, formal verification and machine
recomputation are not assessed.

The source PR is not merged.  The rejected Dobrushin A1/A2 import remains
invalid and is not used: A1 has an exponential support-cardinality condition;
A2 requires a controlled null-state representation.

## Scoped qualitative theorem

For `p>4`, let

\[
\mathcal A_p=\left\{u:\sum_{m\in\mathbb Z}(1+|m|)^p|\widehat u(m)|<\infty\right\}.
\]

Let real `c,g in A_p` satisfy

\[
c(\theta+1/2)=c(\theta),\qquad
 g(\theta+1/2)=-g(\theta),\qquad g\ne0,
\]

and assume `delta<=c<=1-delta`.  Put `mu=\widehat c(0)`.  For every odd
`k` with `\widehat g(k)\ne0`, set

\[
\alpha_k=\frac{|\widehat g(k)|^4}{8\mu^2(1-\mu^2)}.
\]

Then there is `epsilon>0` such that the physical affine kernel
`K_t=T(c)+tT(g)` is legal and

\[
t\longmapsto h(c+t g)+\alpha_k t^4
\]

is concave on `[-epsilon,epsilon]`, where `h` is the true stationary DPP
configuration Shannon entropy rate.

The proof keeps every complete event through the exact one-sided conditional,
uses the full invariant future law, and does not replace the problem by spectral
or fermionic entropy, an observation-basis rotation, an `L`-affine path, or a
finite-window curvature extrapolation.

## Authoritative qualitative reading order

1. `c4_response_p4_repair.md` — integrated qualitative proof.  Its historical
   frozen-memory equations `(7.3)--(7.5)` are not authoritative; see item 2.
2. `c4_response_p4_boundary_correction.md` — withdraws those equations and
   proves the valid finite time-correlation/Poisson cutoff
   `O(N^{-eta})`, `0<eta<p/2-2`.
3. `c4_response_p4_pr66_dependency_audit.md` — complete-event singular gap,
   normed inverse, common complex disk, two-leg influence, full-future limit,
   non-null logarithm and parity; it stops before the invalid Dobrushin step.
4. `c4_response_p4_selfcontained_closures.md` — defective-renewal estimate and
   Banach-valued Cauchy lemma.
5. `c4_response_p4_source_audit.md` — direct Bressaud--Fernandez--Galves
   equation map and response difference quotients.
6. `c4_response_p4_measure_continuity.md` and
   `c4_response_p4_continuity_detail.md` — DPP cylinder continuity and the two
   explicit interpolation losses.

The scoped FIRST/SECOND apply only to the frozen qualitative packet and the
correction priority just stated.  They do not certify a raw stationary
frozen-memory derivative rate or full analytic stationary entropy response.

## Qualitative proof spine

Set `q=(p+2)/4` and `a=2q-1=p/2>2`.  The complete-event inverse argument gives
one common complex disk and the two-leg bound.  Cauchy's formula preserves the
single-coordinate decay through the required parameter derivatives, hence

\[
\operatorname{var}_n(\partial_z^r\log G_z)=O(n^{-a}),\qquad r=0,\ldots,4.
\]

On

\[
\mathcal B_b=\{F:\|F\|_\infty+\sup_n(1+n)^b\operatorname{var}_nF<\infty\},
\]

the explicit BFG coupling and defective-renewal calculation give polynomial
relaxation for `1<b<=a`.  Keeping the first generated mismatch time gives

\[
\mathcal R_s:\mathcal B_b\longrightarrow\mathcal B_{b-1},\qquad b>1,
\]

where `\mathcal R_s=\sum_{n\ge0}\mathcal L_s^n\Pi_s`.

Complete-event parity makes the law even in `t`, so put `s=t^2`.  Two response
orders use

\[
\mathcal B_a\xrightarrow{\mathcal R_s}\mathcal B_{a-1}
\xrightarrow{\mathcal R_s}\mathcal B_{a-2},
\]

which is legal for `a>2`.  The exact identity

\[
(\nu_u-\nu_s)(F)=\nu_u(\mathcal L_u-\mathcal L_s)\mathcal R_sF
\]

gives the two difference-quotient response formulas.

For `\ell_s=\log G_s`, fixed parity marginals give

\[
D(s):=h(c)-h(c+\sqrt s\,g)=\nu_s(\ell_s-\ell_0).
\]

Normalization gives `D'(0)=0`, so `D(s)=A s^2+o(s^2)`.  The accepted
regularity-free PR53 matching bound gives `A>=2\alpha_k`.  Therefore

\[
h''(t)=-12A t^2+o(t^2),
\]

which proves the stated local corrected concavity.

## Boundary statements

The valid qualitative proof uses no finite-memory stationary derivative limit.
The accepted replacement boundary statement is the finite correlation-time
cutoff in `c4_response_p4_boundary_correction.md`.

Later author supplements are separate:

- `c4_response_p4_one_loss.md` gives a second occupation-potential derivation.
- `c4_response_spatial_truncation_p6.md` gives a direct stronger-range
  comparison.
- `c4_response_spatial_truncation_p4_multiscale.md` claims, for all `p>4`, a
  two-cutoff error
  \[
  C_\eta\{M^{-\eta}+N^{-p/2}M^3\},\qquad 0<\eta<p/2-2,
  \]
  and a balanced positive polynomial rate.  This is a current-head author
  result, not part of the frozen FIRST/SECOND.

The earlier `p>8` files are retained as coarse proof history.  The finite
Möbius/closed-walk A2 candidate and inverse-localization obstruction are backup
routes and are not inputs to the finite-response theorem.

## Nonclaims

No result here asserts a whole legal interval, `p<=4`, arbitrary measurable
symbols, full analytic stationary response, an entropy counterexample, or
novelty.  Issue #92 is the current-head review contract; a request or stale
label is not a running review without an explicit claim and version binding.
