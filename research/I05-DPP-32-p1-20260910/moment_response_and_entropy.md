# Moment response and the `A_p`, `p>=1`, entropy-rate theorem

Status: **PROVED AS AN AUTHOR PROOF / PENDING INDEPENDENT REVIEW**.

This file proves a finite second-response lemma at the endpoint where a
pointwise polynomial-space argument would land in `B_1`.  The proof retains the
full summable moment sequence instead of replacing it by the borderline bound
`O(n^{-2})`.

The DPP input is the common complete-event influence moment proved in
`beurling_complete_event_localization.md`.

## 1. Variation spaces

Let `X={0,1}^N`.  For a continuous function `F` define

\[
\operatorname{var}_mF
=\sup\{|F(x)-F(y)|:x_1^m=y_1^m\}.
\]

Use the two spaces

\[
\mathcal V_0
=\left\{F:\|F\|_{\mathcal V_0}
 :=\|F\|_\infty+\sum_{m\ge0}\operatorname{var}_mF<\infty\right\},
\tag{1.1}
\]

\[
\mathcal V_1
=\left\{F:\|F\|_{\mathcal V_1}
 :=\|F\|_\infty+\sum_{m\ge0}(m+1)
 \operatorname{var}_mF<\infty\right\}.
\tag{1.2}
\]

The distinction between `V_1` and the pointwise class `B_2` is essential at
the endpoint: a common finite first moment of the variation sequence is
stronger than merely knowing `var_m F=O(m^{-2})`.

Let `G_s(xi|x)` be a normalized, uniformly non-null binary kernel on a compact
real `s` interval, and define

\[
(\mathcal L_sF)(x)=\sum_{\xi=0}^1G_s(\xi|x)F(\xi x).
\tag{1.3}
\]

Assume that `G_s` has a unique compatible invariant law `nu_s`.

## 2. The moment hypotheses

Assume there are fixed nonincreasing sequences `rho_m` and `v_m` such that

\[
\sum_{m\ge0}(m+1)\rho_m<\infty,
\qquad
\sum_{m\ge0}(m+1)v_m<\infty,
\tag{2.1}
\]

and, uniformly in `s`,

\[
\operatorname{var}_m(\partial_s^j\log G_s)
\le\rho_m,
\qquad j=0,1,2.
\tag{2.2}
\]

For a moving observable `F_s`, assume it is `C^2` in sup norm and

\[
\operatorname{var}_m(\partial_s^jF_s)\le v_m,
\qquad j=0,1,2.
\tag{2.3}
\]

The DPP application has `F_s=ell_s=log G_s`, so one can take `v=rho`.

Uniform non-nullness converts (2.2) into the same type of bounds for the first
two derivatives of `G_s`.  Multiplication and the prepend map then show that

\[
A_{j,s}:=\partial_s^j\mathcal L_s
\]

acts boundedly on `V_0`, `V_1`, and `C(X)` for `j=1,2`, locally uniformly in
`s`.  Normalization gives `A_{j,s}1=0`.

## 3. BFG coupling with no polynomial-rate substitution

Choose a common ratio-loss sequence

\[
\Gamma_m
=1-\exp[-C\rho_m].
\tag{3.1}
\]

After enlarging finitely many entries if necessary, it is decreasing,
`Gamma_0<1`, and histories agreeing through `m` satisfy

\[
\frac{G_s(\xi|x)}{G_s(\xi|y)}\ge1-\Gamma_m.
\tag{3.2}
\]

Moreover

\[
\sum_m(m+1)\Gamma_m<\infty.
\tag{3.3}
\]

We use only the explicit maximal coupling and matched-suffix process of
Bressaud--Fernandez--Galves (BFG), not a general differentiability theorem.
Their auxiliary age chain has transitions

\[
k\longmapsto k+1\quad\text{with probability }1-\Gamma_k,
\qquad
k\longmapsto0\quad\text{with probability }\Gamma_k.
\tag{3.4}
\]

Its first positive return law is

\[
f_{k+1}=\Gamma_k\prod_{j=0}^{k-1}(1-\Gamma_j).
\tag{3.5}
\]

Because `sum Gamma_m<infinity`,

\[
\theta:=\sum_{n\ge1}f_n
=1-\prod_{m\ge0}(1-\Gamma_m)<1.
\tag{3.6}
\]

Let `u_0=1` and

\[
u_n=\sum_{k=1}^n f_k u_{n-k}.
\tag{3.7}
\]

Summing the finite triangular recurrence and passing monotonically to the
limit gives

\[
U:=\sum_{n\ge0}u_n=\frac1{1-\theta}<\infty.
\tag{3.8}
\]

BFG's elementary coupling inequality, before its specialization to their
`V_phi` observable norm, gives for every continuous `F`

\[
\operatorname{osc}(\mathcal L_s^nF)
\le\sum_{k=0}^n\operatorname{var}_k(F)u_{n-k}.
\tag{3.9}
\]

Therefore, for `F in V_0`,

\[
\sum_{n\ge0}\operatorname{osc}(\mathcal L_s^nF)
\le U\sum_{k\ge0}\operatorname{var}_kF<\infty.
\tag{3.10}
\]

This is the only relaxation estimate needed below.  No assertion of the form
“summable variation implies `C^2` response” is imported.

## 4. Poisson inversion: `V_1 -> V_0` and `V_0 -> C`

Put

\[
\Pi_sF=F-\nu_sF,
\qquad
\mathcal R_sF=\sum_{n\ge0}\mathcal L_s^n\Pi_sF.
\tag{4.1}
\]

For `F in V_0`, equations (3.9)--(3.10) give uniform convergence and

\[
\|\mathcal R_sF\|_\infty
\le C\|F\|_{\mathcal V_0}.
\tag{4.2}
\]

Now suppose `F in V_1`.  Couple two chains whose initial futures agree through
`m`, and let `sigma` be the first generated disagreement.  Before step `r`,
the current futures agree through at least `m+r`, hence

\[
P(\sigma=r)\le\Gamma_{m+r}.
\tag{4.3}
\]

If `sigma>=n`, the terminal values differ by at most `var_{m+n}F`.  If
`sigma=r<n`, the remaining difference is at most
`osc(L_s^{n-r-1}F)`.  Thus

\[
\operatorname{var}_m(\mathcal L_s^nF)
\le\operatorname{var}_{m+n}F
 +\sum_{r=0}^{n-1}\Gamma_{m+r}
  \operatorname{osc}(\mathcal L_s^{n-r-1}F).
\tag{4.4}
\]

Summing in `n` and using (3.10),

\[
\operatorname{var}_m(\mathcal R_sF)
\le
\sum_{k\ge m}\operatorname{var}_kF
+C\|F\|_{\mathcal V_0}\sum_{k\ge m}\Gamma_k.
\tag{4.5}
\]

A second summation in `m` yields

\[
\sum_m\operatorname{var}_m(\mathcal R_sF)
\le
\sum_k(k+1)\operatorname{var}_kF
+C\|F\|_{\mathcal V_0}\sum_k(k+1)\Gamma_k.
\tag{4.6}
\]

Hence

\[
\boxed{
\mathcal R_s:\mathcal V_1\longrightarrow\mathcal V_0,
\qquad
\mathcal R_s:\mathcal V_0\longrightarrow C(X)
}
\tag{4.7}
\]

boundedly and uniformly.  Also

\[
(I-\mathcal L_s)\mathcal R_sF=F-\nu_sF,
\qquad
\nu_s(\mathcal R_sF)=0.
\tag{4.8}
\]

This is the moment analogue of two one-power Poisson losses.  It remains valid
at the exact endpoint where the polynomial exponents are `2 -> 1 -> 0`.

## 5. Continuity of the Poisson terms

This paragraph supplies the remainder control needed for response rather than
assuming it.

For a family satisfying (2.3), the time tail of (4.1) converges uniformly in
sup norm by the tail of the convolution in (3.9).  It also converges uniformly
in `V_0` when the input lies in `V_1`.  Indeed, summing (4.4) over `m` and over
times `n>N`, the no-disagreement part is bounded by

\[
\sum_{k>N}(k+1)\operatorname{var}_kF,
\]

while the disagreement part is a tail of the convolution of the two summable
sequences

\[
r\longmapsto\sum_{m\ge0}\Gamma_{m+r},
\qquad
l\longmapsto\operatorname{osc}(\mathcal L_s^lF).
\]

Both tails tend to zero uniformly under (2.1)--(2.3).  Finite partial sums are
continuous in `V_0`; consequently

\[
s\longmapsto\mathcal R_sF_s
\quad\text{is continuous in }\mathcal V_0.
\tag{5.1}
\]

Then

\[
H_s=A_{1,s}\mathcal R_sF_s
\]

is a continuous `V_0` family whose variations have one fixed summable
majorant obtained from (4.5), `rho`, and `v`.  Applying (3.9) once more shows
that

\[
s\longmapsto\mathcal R_sH_s
\quad\text{is continuous in }C(X).
\tag{5.2}
\]

The same statements hold for `F_s'`.  These are the exact continuity facts
used in the second difference quotient.

## 6. Finite second response

Assume `nu_s` is weakly continuous.  For nearby `u,s`, invariance and (4.8)
give the exact identity

\[
(\nu_u-\nu_s)(F)
=\nu_u(\mathcal L_u-\mathcal L_s)\mathcal R_sF.
\tag{6.1}
\]

For fixed `F in V_1`, divide by `u-s` and use the `C^2` operator expansion of
`L_s` on `V_0` to obtain

\[
D\nu_s(F)=\nu_s(A_{1,s}\mathcal R_sF).
\tag{6.2}
\]

The observable on the right belongs to `V_0`.  Apply (6.1) again to that fixed
observable; its Poisson inverse exists by (4.7).  This gives

\[
D^2\nu_s(F)
=\nu_s(A_{2,s}\mathcal R_sF)
+2\nu_s\left(
 A_{1,s}\mathcal R_s(A_{1,s}\mathcal R_sF)
\right).
\tag{6.3}
\]

For a moving `F_s`, ordinary Leibniz expansion gives

\[
\begin{aligned}
\frac{d^2}{ds^2}\nu_s(F_s)
={}&\nu_s(F_s'')
+2\nu_s(A_{1,s}\mathcal R_sF_s')
+\nu_s(A_{2,s}\mathcal R_sF_s)\\
&+2\nu_s\left(
 A_{1,s}\mathcal R_s(A_{1,s}\mathcal R_sF_s)
\right).
\end{aligned}
\tag{6.4}
\]

Equations (5.1)--(5.2) prove continuity of every term.  Thus
`s -> nu_s(F_s)` is `C^2` on the physical interval, with continuous right
second derivative at zero.  No derivative of `R_s` is assumed.

## 7. DPP verification of the hypotheses for `p>=1`

Let `p>=1`, and let real `c,g in A_p` satisfy

\[
c(\theta+1/2)=c(\theta),
\qquad
g(\theta+1/2)=-g(\theta),
\qquad g\ne0,
\qquad
\delta\le c\le1-\delta.
\tag{7.1}
\]

By `beurling_complete_event_localization.md`, the true complete-event
conditional has, for `z` in a common complex disk and `k=0,...,4`,
single-coordinate envelopes `beta_j^{(k)}` such that

\[
\sum_j(1+j)^{2p}\beta_j^{(k)}<\infty.
\tag{7.2}
\]

Therefore

\[
\operatorname{var}_n(\partial_z^k\ell_z)
\le\sum_{j>n}\beta_j^{(k)}
\tag{7.3}
\]

and, since `2p>=2`,

\[
\sum_n(n+1)\operatorname{var}_n(\partial_z^k\ell_z)
\le C\sum_j(1+j)^2\beta_j^{(k)}<\infty.
\tag{7.4}
\]

The bounds come from fixed sequences, uniformly on smaller disks.  The parity
conjugacy makes `ell_z` even and it factors through `s=z^2`; hence
`ell_s,ell_s',ell_s''` meet (2.2).

For every finite complete word,

\[
\nu_t(X_I=x)
=(-1)^{|Z_x|}\det\{T_I(c+tg)-I_{Z_x}\}.
\tag{7.5}
\]

This is an even polynomial in `t`, hence a polynomial in `s=t^2`.
Cylinder convergence proves weak continuity of the true DPP future law.  The
full-future Schur limit is its conditional, so `nu_s L_s=nu_s`.  Uniqueness
also follows from (3.9), since cylinder functions have summable variations.
Thus all hypotheses of Section 6 are verified from complete events.

## 8. True entropy-rate deficit

Put

\[
\ell_s=\log G_s,
\qquad
h_s=-\nu_s(\ell_s).
\tag{8.1}
\]

This is the Shannon entropy rate of the configuration process, not the
quasi-free von Neumann entropy.

At `s=0`, the half-period-even kernel is block diagonal between even and odd
coordinates, so the parity sublattices are independent.  Along the physical
path, the restriction to either parity is unchanged because `g` has no even
Fourier modes.  The zero-parameter origin conditional depends only on the
origin-parity future.  Hence

\[
\nu_s(\ell_0)=\nu_0(\ell_0).
\tag{8.2}
\]

The exact true-rate deficit is therefore

\[
D(s):=h_0-h_s
=\nu_s(\ell_s-\ell_0).
\tag{8.3}
\]

Section 6 gives `D in C^2`.  Since the moving observable in (8.3) vanishes at
zero,

\[
D'(0)=\nu_0(\ell'_0).
\]

Normalization gives pointwise

\[
(\mathcal L_0\ell'_0)(x)
=\sum_\xi G_0(\xi|x)
 \frac{G'_0(\xi|x)}{G_0(\xi|x)}
=\sum_\xi G'_0(\xi|x)=0.
\tag{8.4}
\]

Invariance implies

\[
D'(0)=0.
\tag{8.5}
\]

Write

\[
D(s)=A s^2+o(s^2).
\tag{8.6}
\]

The accepted regularity-free PR53 parity/matching inequality gives, for every
odd `k` with `\widehat g(k)\ne0`,

\[
D(t^2)\ge\frac12 d_{Ber}
\left(\mu^2-|\widehat g(k)|^2t^2\,\middle\|\,\mu^2\right),
\qquad \mu=\widehat c(0).
\tag{8.7}
\]

Its elementary expansion and (8.6) imply

\[
A\ge
\frac{|\widehat g(k)|^4}{4\mu^2(1-\mu^2)}
=2\alpha_k,
\qquad
\alpha_k=
\frac{|\widehat g(k)|^4}{8\mu^2(1-\mu^2)}.
\tag{8.8}
\]

Because `D` is `C^2` in `s`,

\[
\frac{d^2}{dt^2}h(c+tg)
=-2D'(t^2)-4t^2D''(t^2)
=-12A t^2+o(t^2).
\tag{8.9}
\]

Consequently

\[
\frac{d^2}{dt^2}\{h(c+tg)+\alpha_k t^4\}
=-12(A-\alpha_k)t^2+o(t^2)<0
\tag{8.10}
\]

for all sufficiently small nonzero `t`; the second derivative is zero at the
center.  Shrinking the legal interval proves concavity.

## 9. New theorem

**Theorem.**  Let `p>=1`.  Let real `c,g in A_p` obey (7.1).  For every odd
`k` with `\widehat g(k)\ne0`, there exists `epsilon>0` such that `c+tg` is
legal and

\[
t\longmapsto
h(c+tg)+
\frac{|\widehat g(k)|^4}{8\mu^2(1-\mu^2)}t^4
\]

is concave on `[-epsilon,epsilon]`.

This is a true stationary DPP configuration-entropy theorem for the physical
affine kernel.  It strictly enlarges the frozen PR82 range `p>4`, including the
endpoint `p=1`.  It does not assert sharpness, `p<1`, a whole legal interval,
full analytic stationary response, or novelty.
