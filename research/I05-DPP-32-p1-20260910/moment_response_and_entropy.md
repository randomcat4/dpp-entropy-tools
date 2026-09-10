# Moment response and the `A_p`, `p>=1`, entropy-rate theorem

Status: **PROVED AS AN AUTHOR PROOF / PENDING INDEPENDENT REVIEW**.

This file proves finite second response at the endpoint where a pointwise
polynomial-space argument would land in `B_1`. It keeps the full summable
moment sequence instead of replacing it by the borderline statement
`var_n F=O(n^{-2})`.

The DPP input is the common complete-event influence moment proved in
`beurling_complete_event_localization.md`.

## 1. Variation moment spaces

Let `X={0,1}^N`. For continuous `F`, set

\[
\operatorname{var}_mF
=\sup\{|F(x)-F(y)|:x_1^m=y_1^m\}.
\]

Define

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

The endpoint distinction matters: a fixed finite first moment of the variation
sequence is stronger than a bare pointwise `O(m^{-2})` estimate.

Let `G_s(xi|x)` be a normalized, uniformly non-null binary kernel on a compact
real `s` interval, and define

\[
(\mathcal L_sF)(x)=\sum_{\xi=0}^1G_s(\xi|x)F(\xi x).
\tag{1.3}
\]

Let `nu_s` be its compatible invariant law.

## 2. Moment and parameter hypotheses

Assume there are fixed nonincreasing sequences `rho_m` and `v_m` with

\[
\sum_{m\ge0}(m+1)\rho_m<\infty,
\qquad
\sum_{m\ge0}(m+1)v_m<\infty,
\tag{2.1}
\]

such that, uniformly in `s`,

\[
\operatorname{var}_m(\partial_s^j\log G_s)
\le\rho_m,
\qquad j=0,1,2,
\tag{2.2}
\]

and for a moving observable `F_s`,

\[
\operatorname{var}_m(\partial_s^jF_s)
\le v_m,
\qquad j=0,1,2.
\tag{2.3}
\]

Assume moreover that `s -> log G_s` and `s -> F_s` are `C^2` in the
corresponding `V_1` norms. In the DPP application this follows from the common
complex complete-event disk and the Banach-valued Cauchy estimate; take
`F_s=ell_s=log G_s` and one common envelope.

Uniform non-nullness transfers (2.2) to `G_s` and its first two derivatives.
Multiplication and the prepend map then show that

\[
A_{j,s}:=\partial_s^j\mathcal L_s,
\qquad j=1,2,
\tag{2.4}
\]

act boundedly and continuously on `V_1`, `V_0`, and `C(X)`. Normalization gives
`A_{j,s}1=0`.

## 3. BFG coupling without a black-box response theorem

Set

\[
\Gamma_m=1-e^{-\rho_m}.
\tag{3.1}
\]

This sequence is decreasing, `Gamma_0<1`, and histories agreeing through `m`
satisfy

\[
\frac{G_s(\xi|x)}{G_s(\xi|y)}
\ge e^{-\rho_m}=1-\Gamma_m.
\tag{3.2}
\]

Moreover

\[
\sum_m(m+1)\Gamma_m<\infty.
\tag{3.3}
\]

We use only the explicit maximal coupling and matched-suffix process of
Bressaud--Fernandez--Galves (BFG). Their auxiliary age chain has transitions

\[
k\longmapsto k+1\quad\text{with probability }1-\Gamma_k,
\qquad
k\longmapsto0\quad\text{with probability }\Gamma_k.
\tag{3.4}
\]

Its first positive return law is

\[
f_1=\Gamma_0,
\qquad
f_n=\Gamma_{n-1}\prod_{j=0}^{n-2}(1-\Gamma_j),
\quad n\ge2.
\tag{3.5}
\]

Since `sum Gamma_m<infinity`,

\[
\theta:=\sum_{n\ge1}f_n
=1-\prod_{m\ge0}(1-\Gamma_m)<1.
\tag{3.6}
\]

Let `r_0=1` and let the renewal return sequence satisfy

\[
r_n=\sum_{k=1}^n f_k r_{n-k},
\qquad n\ge1.
\tag{3.7}
\]

Thus `r_n=P(S_n=0)`. Summing the finite triangular recurrence gives

\[
\sum_{n=0}^N r_n
\le1+\theta\sum_{n=0}^N r_n.
\]

Monotone convergence, followed by the exact infinite triangular identity,
yields

\[
R_*:=\sum_{n\ge0}r_n=\frac1{1-\theta}<\infty.
\tag{3.8}
\]

BFG equations (5.4)--(5.5), before the specialization to their `V_phi` norm,
give for every continuous `F`

\[
\operatorname{osc}(\mathcal L_s^nF)
\le\sum_{k=0}^n\operatorname{var}_k(F)r_{n-k}.
\tag{3.9}
\]

Consequently, for `F in V_0`, Tonelli gives

\[
\sum_{n\ge0}\operatorname{osc}(\mathcal L_s^nF)
\le R_*\sum_{k\ge0}\operatorname{var}_kF<\infty.
\tag{3.10}
\]

No statement that summable variation itself implies `C^2` parameter response
is imported.

## 4. Poisson inversion: `V_1 -> V_0 -> C`

Put

\[
\Pi_sF=F-\nu_sF,
\qquad
\mathcal R_sF=\sum_{n\ge0}\mathcal L_s^n\Pi_sF.
\tag{4.1}
\]

For `F in V_0`, stationarity and (3.9) give

\[
\|\mathcal L_s^n\Pi_sF\|_\infty
\le\operatorname{osc}(\mathcal L_s^nF).
\]

Hence the series converges uniformly and

\[
\|\mathcal R_sF\|_\infty
\le C\|F\|_{\mathcal V_0}.
\tag{4.2}
\]

Now let `F in V_1`. Couple two chains whose initial futures agree through
`m`, and let `sigma` be the first generated disagreement. Before generation
step `j`, the current futures agree through at least `m+j`, so

\[
P(\sigma=j)\le\Gamma_{m+j}.
\tag{4.3}
\]

If `sigma>=n`, the terminal values differ by at most `var_{m+n}F`. If
`sigma=j<n`, the difference after the remaining generations is at most
`osc(L_s^{n-j-1}F)`. Therefore

\[
\operatorname{var}_m(\mathcal L_s^nF)
\le\operatorname{var}_{m+n}F
 +\sum_{j=0}^{n-1}\Gamma_{m+j}
  \operatorname{osc}(\mathcal L_s^{n-j-1}F).
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

A second Tonelli summation yields

\[
\sum_m\operatorname{var}_m(\mathcal R_sF)
\le
\sum_k(k+1)\operatorname{var}_kF
+C\|F\|_{\mathcal V_0}\sum_k(k+1)\Gamma_k.
\tag{4.6}
\]

Thus

\[
\boxed{
\mathcal R_s:\mathcal V_1\longrightarrow\mathcal V_0,
\qquad
\mathcal R_s:\mathcal V_0\longrightarrow C(X)
}
\tag{4.7}
\]

boundedly and locally uniformly in `s`. Also

\[
(I-\mathcal L_s)\mathcal R_sF=F-\nu_sF,
\qquad
\nu_s(\mathcal R_sF)=0,
\tag{4.8}
\]

because the partial sums telescope and the remainder tends to zero in sup
norm. These are the endpoint mappings `2 -> 1 -> 0` in variation-moment order.

## 5. Uniform tails and continuity

The response proof needs continuity of the Poisson terms, not merely their
existence.

For a `V_1` family controlled by (2.3), the tail after time `N` in (4.1)
tends uniformly to zero in `V_0`. Indeed, the no-disagreement part of the sum
of (4.4) is bounded by

\[
\sum_{k>N}(k+1)v_k\longrightarrow0.
\tag{5.1}
\]

For the disagreement part, put

\[
B_j=\sum_{m\ge0}\Gamma_{m+j},
\qquad
C_l^*=\sup_s\operatorname{osc}(\mathcal L_s^lF_s).
\]

The first sequence is summable by (3.3), and the second is dominated by the
convolution in (3.9), hence is summable. The remaining variation tail is
bounded by

\[
\sum_{j,l\ge0:\ j+l\ge N}B_jC_l^*,
\tag{5.2}
\]

the tail of a convolution of two `l^1` sequences. It tends to zero.

Finite partial sums depend continuously on `s` in `V_0`; therefore

\[
s\longmapsto\mathcal R_sF_s
\quad\text{is continuous in }\mathcal V_0.
\tag{5.3}
\]

Then

\[
H_s=A_{1,s}\mathcal R_sF_s
\]

is a continuous `V_0` family. Equations (4.5), (2.2) and the product variation
bound give one fixed summable envelope for `var_m H_s`. Applying (3.9) once
more gives a common summable sup-norm tail, so

\[
s\longmapsto\mathcal R_sH_s
\quad\text{is continuous in }C(X).
\tag{5.4}
\]

The same statements hold with `F_s'` in place of `F_s`. These are exactly the
continuity statements needed for the second difference quotient.

## 6. Finite second response

Assume `nu_s` is weakly continuous. For nearby `u,s`, invariance and (4.8)
give the exact identity

\[
(\nu_u-\nu_s)(F)
=\nu_u(\mathcal L_u-\mathcal L_s)\mathcal R_sF.
\tag{6.1}
\]

For fixed `F in V_1`, divide by `u-s`. The operator quotient converges on
`V_0`, and weak continuity gives

\[
D\nu_s(F)=\nu_s(A_{1,s}\mathcal R_sF).
\tag{6.2}
\]

The observable on the right lies in `V_0`. Apply (6.1) again to this fixed
observable. Its Poisson inverse exists in `C(X)` by (4.7). Expanding

\[
\mathcal L_{s+h}-\mathcal L_s
=hA_{1,s}+\frac{h^2}{2}A_{2,s}+o(h^2)
\]

on the relevant spaces gives

\[
D^2\nu_s(F)
=\nu_s(A_{2,s}\mathcal R_sF)
+2\nu_s\left(
 A_{1,s}\mathcal R_s(A_{1,s}\mathcal R_sF)
\right).
\tag{6.3}
\]

For a moving `C^2(V_1)` family `F_s`, ordinary Leibniz expansion gives

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

Equations (5.3)--(5.4) prove continuity of every term. Thus
`s -> nu_s(F_s)` is `C^2` on the physical interval, with a continuous right
second derivative at zero. No derivative of `R_s` is assumed or hidden.

## 7. DPP verification for `p>=1`

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

The common complete-event localization theorem supplies, on one complex disk
and for `k=0,...,4`, fixed single-coordinate envelopes `beta_j^{(k)}` with

\[
\sum_j(1+j)^{2p}\beta_j^{(k)}<\infty.
\tag{7.2}
\]

Hence

\[
\operatorname{var}_n(\partial_z^k\ell_z)
\le\sum_{j>n}\beta_j^{(k)}
\tag{7.3}
\]

and, because `2p>=2`,

\[
\sum_n(n+1)\operatorname{var}_n(\partial_z^k\ell_z)
\le C\sum_j(1+j)^2\beta_j^{(k)}<\infty.
\tag{7.4}
\]

The envelopes are uniform on smaller disks. Complete-event parity makes
`ell_z` even and factors it through `s=z^2`; the derivatives
`ell_s,ell_s',ell_s''` satisfy (2.2) and are `C^2(V_1)` by the Cauchy formula.

For every finite complete word,

\[
\nu_t(X_I=x)
=(-1)^{|Z_x|}\det\{T_I(c+tg)-I_{Z_x}\}.
\tag{7.5}
\]

This is an even polynomial in `t`, hence a polynomial in `s=t^2`. Cylinder
convergence proves weak continuity of the true DPP future law. The full-future
Schur limit is its conditional, so `nu_s L_s=nu_s`. If two compatible
invariant laws existed, (3.9) applied to cylinder functions and then `n->infty`
would identify them. Thus the required invariant law is unique and all
hypotheses of Section 6 are verified from complete events.

## 8. True entropy-rate deficit

Put

\[
\ell_s=\log G_s,
\qquad
h_s=-\nu_s(\ell_s).
\tag{8.1}
\]

This is the Shannon entropy rate of the configuration process, not a
quasi-free von Neumann entropy.

At `s=0`, the half-period-even kernel is block diagonal between even and odd
coordinates, so the parity sublattices are independent. Along the physical
path, restriction to either parity is unchanged because `g` has no even
Fourier modes. The zero-parameter origin conditional depends only on the
origin-parity future. Hence

\[
\nu_s(\ell_0)=\nu_0(\ell_0).
\tag{8.2}
\]

Therefore the exact true-rate deficit is

\[
D(s):=h_0-h_s
=\nu_s(\ell_s-\ell_0).
\tag{8.3}
\]

Section 6 gives `D in C^2`. Since the moving observable in (8.3) vanishes at
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

Since `D` is `C^2` in `s`,

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
center. Shrinking the legal interval proves concavity.

## 9. New theorem

**Theorem.** Let `p>=1`. Let real `c,g in A_p` obey (7.1). For every odd
`k` with `\widehat g(k)\ne0`, there exists `epsilon>0` such that `c+tg` is
legal and

\[
t\longmapsto
h(c+tg)+
\frac{|\widehat g(k)|^4}{8\mu^2(1-\mu^2)}t^4
\]

is concave on `[-epsilon,epsilon]`.

This is a true stationary DPP configuration-entropy theorem for the physical
affine kernel. It strictly enlarges the frozen PR82 range `p>4`, including the
endpoint `p=1`. It does not assert sharpness, local concavity for `p<1`, a
whole legal interval, full analytic stationary response, or novelty.
