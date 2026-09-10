# First-moment response and the true entropy-rate conclusion

Status: **AUTHOR PROOF / PENDING REVIEW**.

This file proves exactly the finite response needed by the `H^1_F` theorem. It does not invoke the false statement that summable variation automatically gives fourth-order response. The proof uses the explicit Bressaud--Fernandez--Galves coupling and two different observable spaces.

## 1. Moment variation spaces

For `F` on `X={0,1}^N`, let

\[
\operatorname{var}_mF
=\sup\{|F(x)-F(y)|:x_1^m=y_1^m\}.
\]

Define

\[
\begin{aligned}
\mathcal V_0
&=\left\{F:\|F\|_{\mathcal V_0}
:=\|F\|_\infty+\sum_{m\ge0}\operatorname{var}_mF<\infty\right\},\\
\mathcal V_1
&=\left\{F:\|F\|_{\mathcal V_1}
:=\|F\|_\infty+\sum_{m\ge0}(m+1)\operatorname{var}_mF<\infty\right\}.
\end{aligned}
\tag{1.1}
\]

The localization proof supplies one nonincreasing sequence `rho_m` such that, uniformly for `s` in a small physical interval and for `j=0,1,2`,

\[
\operatorname{var}_m(\partial_s^j\ell_s)
\le C_j\rho_m,
\qquad
\sum_{m\ge0}(m+1)\rho_m<\infty.
\tag{1.2}
\]

Uniform non-nullness transfers the same statement from `ell_s=log G_s` to `G_s` and its first two derivatives.

For the normalized transfer operator

\[
(\mathcal L_sF)(x)=
\sum_{\xi=0}^1G_s(\xi|x)F(\xi x),
\tag{1.3}
\]

put

\[
A_{j,s}=\partial_s^j\mathcal L_s,\qquad j=1,2.
\]

The elementary product/prepend estimate gives

\[
A_{j,s}:\mathcal V_i\to\mathcal V_i
\quad(i=0,1),
\qquad
A_{j,s}:C(X)\to C(X),
\tag{1.4}
\]

locally uniformly. Also `A_{j,s}1=0` by normalization.

## 2. The exact coupling input

If two futures agree through coordinate `m`, (1.2) and non-nullness give the ratio bound

\[
\frac{G_s(\xi|x)}{G_s(\xi|y)}
\ge\exp[-C\rho_m]
=1-\gamma_m,
\tag{2.1}
\]

where

\[
\gamma_m:=1-e^{-C\rho_m}.
\tag{2.2}
\]

After replacing finitely many entries by a decreasing envelope below one, we may assume `gamma_m` is decreasing. It satisfies

\[
\sum_m(m+1)\gamma_m<\infty.
\tag{2.3}
\]

Run the Bressaud--Fernandez--Galves maximal coupling with this common majorant. Their matched-suffix process is compared to the age chain

\[
S_{n+1}=\begin{cases}
S_n+1,&\text{with probability }1-\gamma_{S_n},\\
0,&\text{with probability }\gamma_{S_n}.
\end{cases}
\tag{2.4}
\]

Let

\[
u_n=P_0(S_n=0).
\]

The first positive return law is

\[
f_{n+1}=\gamma_n\prod_{j=0}^{n-1}(1-\gamma_j).
\tag{2.5}
\]

Because `sum gamma_j<infinity`,

\[
\theta:=\sum_{n\ge1}f_n
=1-\prod_{j\ge0}(1-\gamma_j)<1.
\tag{2.6}
\]

The defective renewal relation is

\[
u_0=1,
\qquad
u_n=\sum_{k=1}^nf_k u_{n-k}.
\tag{2.7}
\]

Summing finite triangular regions first gives

\[
\sum_{n\ge0}u_n=\frac1{1-\theta}<\infty.
\tag{2.8}
\]

No polynomial asymptotic is needed in this theorem.

For every continuous `F`, the explicit BFG coupling inequality gives

\[
\operatorname{osc}(\mathcal L_s^nF)
\le\sum_{k=0}^n\operatorname{var}_k(F)u_{n-k}.
\tag{2.9}
\]

This is the only load-bearing external coupling conclusion. We do not identify `V_0` or `V_1` with the narrower observable norm used in one displayed specialization of the source.

## 3. First Poisson bound: `V_0 -> C`

Let `nu_s` be the compatible stationary DPP future law and put

\[
\Pi_sF=F-\nu_sF.
\]

Stationarity implies

\[
\|\mathcal L_s^n\Pi_sF\|_\infty
\le\operatorname{osc}(\mathcal L_s^nF).
\]

For `F in V_0`, summing (2.9) and exchanging nonnegative sums yields

\[
\sum_{n\ge0}\|\mathcal L_s^n\Pi_sF\|_\infty
\le\left(\sum_ku_k\right)
\left(\sum_m\operatorname{var}_mF\right).
\tag{3.1}
\]

Therefore

\[
\mathcal R_sF
:=\sum_{n\ge0}\mathcal L_s^n\Pi_sF
\tag{3.2}
\]

converges uniformly and

\[
\boxed{\mathcal R_s:\mathcal V_0\to C(X)}
\tag{3.3}
\]

is locally uniformly bounded. Moreover

\[
(I-\mathcal L_s)\mathcal R_sF=\Pi_sF,
\qquad
\nu_s(\mathcal R_sF)=0.
\tag{3.4}
\]

## 4. Refined Poisson bound: `V_1 -> V_0`

Suppose two initial futures agree through `m`. Couple their generated symbols and let `sigma` be the first generated disagreement. Before generation `r`, the current histories agree through at least `m+r`; hence

\[
P(\sigma=r)\le\gamma_{m+r}.
\tag{4.1}
\]

If no disagreement occurs before time `n`, the terminal values differ by at most `var_{m+n}F`. If the first disagreement is at `r<n`, the remaining difference is bounded by `osc(L_s^{n-r-1}F)`. Thus

\[
\operatorname{var}_m(\mathcal L_s^nF)
\le\operatorname{var}_{m+n}F
+\sum_{r=0}^{n-1}\gamma_{m+r}
\operatorname{osc}(\mathcal L_s^{n-r-1}F).
\tag{4.2}
\]

For `F in V_1`, sum first over `n`. Equations (2.8)--(2.9) imply

\[
\sum_{l\ge0}\operatorname{osc}(\mathcal L_s^lF)
\le C\|F\|_{\mathcal V_0}.
\tag{4.3}
\]

Therefore

\[
\sum_{n\ge0}\operatorname{var}_m(\mathcal L_s^nF)
\le
\sum_{k\ge m}\operatorname{var}_kF
+C\|F\|_{\mathcal V_0}\sum_{r\ge m}\gamma_r.
\tag{4.4}
\]

Summing in `m` gives

\[
\begin{aligned}
\sum_{m,n\ge0}\operatorname{var}_m(\mathcal L_s^nF)
&\le
\sum_{k\ge0}(k+1)\operatorname{var}_kF\\
&\quad+C\|F\|_{\mathcal V_0}
\sum_{r\ge0}(r+1)\gamma_r<\infty.
\end{aligned}
\tag{4.5}
\]

Centering changes no variation. Combining (3.1) and (4.5),

\[
\boxed{\mathcal R_s:\mathcal V_1\to\mathcal V_0}
\tag{4.6}
\]

locally uniformly.

The two successive response spaces are therefore

\[
\mathcal V_1\xrightarrow{\mathcal R_s}
\mathcal V_0\xrightarrow{\mathcal R_s}C(X).
\tag{4.7}
\]

## 5. Continuity and explicit correlation-tail errors

The bounds above are uniform in `s`. For a `V_1`-continuous family `F_s`, every finite partial sum in (3.2) is continuous in `s`. Its tail tends to zero uniformly in `V_0`: from (4.2), the no-disagreement tail is bounded by

\[
\sum_{m\ge0}\sum_{n\ge N}\operatorname{var}_{m+n}F_s,
\tag{5.1}
\]

which tends to zero uniformly by the `V_1` tail, while the disagreement part is a tail of the convolution of the summable sequences

\[
\left(\sum_{m\ge0}\gamma_{m+r}\right)_{r\ge0}
\quad\text{and}\quad
\left(\operatorname{osc}(L_s^lF_s)\right)_{l\ge0}.
\tag{5.2}
\]

Thus

\[
s\longmapsto R_sF_s
\quad\text{is continuous in }V_0.
\tag{5.3}
\]

For a `V_0`-continuous family `H_s`, (2.9)--(3.1) similarly show

\[
s\longmapsto R_sH_s
\quad\text{is continuous in the sup norm.}
\tag{5.4}
\]

These estimates also provide a directly checkable boundary certificate. If every Poisson sum is cut at time `N`, the first-response error is bounded by the tail of the nonnegative convolution in (2.9). The nested second-response error is bounded by the sum of the `V_0` tail in (5.1)--(5.2) for the inner inverse and the sup-norm convolution tail for the outer inverse. Both moduli tend to zero uniformly. No sign from a finite DPP window is extrapolated.

## 6. Finite second-order response

For nearby parameters `u,s`, invariance and (3.4) give the exact identity

\[
(\nu_u-\nu_s)(F)
=\nu_u(\mathcal L_u-\mathcal L_s)\mathcal R_sF.
\tag{6.1}
\]

Indeed `Pi_sF=(I-L_s)R_sF`, while `nu_u I=nu_uL_u`.

Let `F in V_1`. Divide (6.1) by `u-s`. The `C^2` dependence of `L_s` in the moment spaces and (5.3) give

\[
D\nu_s(F)=\nu_s(A_{1,s}\mathcal R_sF).
\tag{6.2}
\]

The fixed observable

\[
H_s:=A_{1,s}\mathcal R_sF
\]

lies in `V_0`. Apply (6.1) once more to this fixed observable and use (3.3), (5.4). This gives

\[
D^2\nu_s(F)
=\nu_s(A_{2,s}\mathcal R_sF)
+2\nu_s\left(
A_{1,s}\mathcal R_s
(A_{1,s}\mathcal R_sF)
\right).
\tag{6.3}
\]

For a moving `C^2(V_1)` family `F_s`, ordinary Leibniz expansion yields

\[
\begin{aligned}
\frac{d^2}{ds^2}\nu_s(F_s)
={}&\nu_s(F_s'')
+2\nu_s(A_{1,s}\mathcal R_sF_s')\\
&+\nu_s(A_{2,s}\mathcal R_sF_s)\\
&+2\nu_s\left(
A_{1,s}\mathcal R_s
(A_{1,s}\mathcal R_sF_s)
\right).
\end{aligned}
\tag{6.4}
\]

All four terms are continuous by Section 5. This proves `C^2` response in `s`. No derivative of `R_s` is postulated, and no general claim about arbitrary summable-variation chains is used beyond the explicit hypotheses proved here.

## 7. DPP weak continuity and invariance

For every finite coordinate set `I` and complete word `x`,

\[
\nu_t(X_I=x)
=(-1)^{|Z_x|}
\det(T_I(c+t g)-I_{Z_x}).
\tag{7.1}
\]

This is a polynomial in the physical parameter `t`; complete-event parity conjugacy makes it even, hence a polynomial in `s=t^2`. Cylinder probabilities therefore vary continuously in `s`, which gives weak continuity of `nu_s` on the compact configuration space.

The infinite-future `G_s` constructed from complete-event Schur complements is the true future conditional. Consequently

\[
\nu_sL_s=\nu_s
\tag{7.2}
\]

by the tower property. Uniqueness also follows from (2.9): two compatible invariant laws agree on every cylinder after letting `n` tend to infinity.

## 8. True entropy deficit and curvature

For a stationary finite-alphabet process with the bounded continuous future conditional above,

\[
h_s=-\nu_s(\ell_s),
\qquad \ell_s=\log G_s.
\tag{8.1}
\]

At `s=0`, the half-period-even center has no cross-parity kernel entries, so the even and odd coordinate processes are independent. For every physical `s=t^2`, the restriction to either parity is unchanged because `g` has only odd Fourier modes. The zero-parameter conditional at the origin depends only on the origin-parity future. Hence

\[
\nu_s(\ell_0)=\nu_0(\ell_0).
\tag{8.2}
\]

The exact true entropy deficit is therefore

\[
D(s):=h_0-h_s
=\nu_s(\ell_s-\ell_0).
\tag{8.3}
\]

The observable `ell_s-ell_0` is `C^2(V_1)` by the complete-event localization file, so Section 6 makes `D` a `C^2` function. At zero the moving observable vanishes. Put

\[
U_0=\partial_s\ell_s|_{s=0}.
\]

Normalization gives pointwise

\[
(\mathcal L_0U_0)(x)
=\sum_\xi G_0(\xi|x)
\frac{\partial_sG_s(\xi|x)|_0}{G_0(\xi|x)}
=\sum_\xi\partial_sG_s(\xi|x)|_0=0.
\tag{8.4}
\]

Thus `nu_0(U_0)=nu_0(L_0U_0)=0`, and

\[
D'(0)=0.
\tag{8.5}
\]

Write

\[
D(s)=A s^2+o(s^2).
\tag{8.6}
\]

The regularity-free matching/negative-association inequality accepted with PR53 gives, for every legal physical `t` and every odd `k` with `g_hat(k)!=0`,

\[
D(t^2)\ge\frac12 d_{\rm Ber}
\left(
\mu^2-|\widehat g(k)|^2t^2
\,\middle\|\,
\mu^2
\right).
\tag{8.7}
\]

The binary relative-entropy expansion and (8.6) imply

\[
A\ge
\frac{|\widehat g(k)|^4}
{4\mu^2(1-\mu^2)}
=2\alpha_k.
\tag{8.8}
\]

Since `D` is `C^2`, with `s=t^2`,

\[
\begin{aligned}
\frac{d^2}{dt^2}h(c+t g)
&=-2D'(s)-4sD''(s)\\
&=-12A t^2+o(t^2).
\end{aligned}
\tag{8.9}
\]

Therefore

\[
\frac{d^2}{dt^2}
\left[h(c+t g)+\alpha_k t^4\right]
=-12(A-\alpha_k)t^2+o(t^2)<0
\tag{8.10}
\]

for all sufficiently small nonzero `t`; at `t=0` the second derivative is zero. Shrinking the legal interval proves concavity on a nonempty symmetric neighborhood.

This concludes the theorem for the true stationary configuration Shannon entropy rate and the true affine DPP kernel.