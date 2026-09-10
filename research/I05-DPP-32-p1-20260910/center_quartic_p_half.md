# Centered quartic entropy expansion for `p>=1/2`

Status: **PROVED AS A WEAKER AUTHOR THEOREM / PENDING INDEPENDENT REVIEW**.

This result is strictly weaker than local concavity. It records what one can
prove with one invariant-measure response when the doubled complete-event
influence has only a finite first moment.

## 1. Statement

Let `p>=1/2`. Let real `c,g in A_p` satisfy

\[
c(\theta+1/2)=c(\theta),
\qquad g(\theta+1/2)=-g(\theta),
\qquad g\ne0,
\qquad \delta\le c\le1-\delta.
\tag{1.1}
\]

Put `mu=\widehat c(0)`. For the true stationary DPP configuration entropy
rate there is a finite number

\[
\mathcal I_s(0)
=\nu_0\left[
 \left(\left.\partial_s\log G_s(X_0|X_1,X_2,\ldots)
 \right|_{s=0}\right)^2
\right]
\tag{1.2}
\]

such that, as `t->0`,

\[
\boxed{
 h(c+t g)
 =h(c)-\frac12\mathcal I_s(0)t^4+o(t^4).
}
\tag{1.3}
\]

Here `s=t^2`, and `G_s` is the true complete-event one-sided conditional.
The quantity (1.2) is the full conditional Fisher information per lattice site
in the physical even parameter `s`: the expectation sums both emitted states
and the full future law, including rare events.

For every odd `k` with `\widehat g(k)\ne0`, the accepted PR53 matching
inequality further implies

\[
\frac12\mathcal I_s(0)
\ge\frac{|\widehat g(k)|^4}
 {4\mu^2(1-\mu^2)}.
\tag{1.4}
\]

Equation (1.3) alone does **not** imply that
`h(c+t g)+alpha_k t^4` is concave on a neighborhood. That stronger theorem is
proved in the companion file only for `p>=1`.

## 2. Summable-variation input at `p>=1/2`

The common complete-event localization theorem gives, for the derivatives
needed here, fixed single-coordinate envelopes `beta_j^{(r)}` with

\[
\sum_{j\ge1}(1+j)^{2p}\beta_j^{(r)}<\infty,
\qquad r=0,2,
\tag{2.1}
\]

where the `z`-derivative order `r=2` supplies the first `s` derivative after
even factorization. If two futures agree through coordinate `n`, then

\[
\operatorname{var}_n(\partial_s^j\ell_s)
\le\sum_{m>n}\widetilde\beta_m^{(j)},
\qquad j=0,1,
\tag{2.2}
\]

for fixed envelopes with the same `2p` moment. Since `2p>=1`, Tonelli's
theorem gives

\[
\sum_{n\ge0}\operatorname{var}_n(\partial_s^j\ell_s)
\le
\sum_{m\ge1}(m+1)\widetilde\beta_m^{(j)}<\infty,
\qquad j=0,1,
\tag{2.3}
\]

uniformly on a smaller physical interval. Thus `ell_s` and its first `s`
derivative lie in

\[
\mathcal V_0
=\{F:\|F\|_\infty+\sum_n\operatorname{var}_nF<\infty\}.
\]

The BFG coupling/defective-renewal calculation in
`moment_response_and_entropy.md` gives

\[
\mathcal R_s:\mathcal V_0\longrightarrow C(X),
\qquad
\mathcal R_sF=
\sum_{n\ge0}\mathcal L_s^n(F-\nu_sF),
\tag{2.4}
\]

with a common operator bound. The same fixed summable envelopes imply that
`R_sF_s` is continuous in the sup norm for continuous `V_0` families.

## 3. One-response identity

For a fixed `F in V_0`, invariance and the Poisson identity give

\[
(\nu_u-\nu_s)(F)
=\nu_u(\mathcal L_u-\mathcal L_s)\mathcal R_sF.
\tag{3.1}
\]

The quotient `(L_u-L_s)/(u-s)` converges in operator norm on `C(X)` because
`G_s` is `C^1` there. Weak continuity of the DPP law then yields

\[
\frac d{ds}\nu_s(F)
=\nu_s(A_{1,s}\mathcal R_sF),
\qquad A_{1,s}=\partial_s\mathcal L_s.
\tag{3.2}
\]

For a moving `C^1(V_0)` family `F_s`, add `nu_s(F_s')`. No second Poisson
inverse is used.

## 4. Exact derivative of the relative-entropy-rate deficit

Let

\[
f_s=\ell_s-\ell_0,
\qquad
D(s)=h(c)-h(c+\sqrt s\,g)=\nu_s(f_s),
\tag{4.1}
\]

where the equality is the fixed-parity-marginal identity used in PR82. Define
the conditional score

\[
U_s=\partial_s\ell_s.
\tag{4.2}
\]

Normalization gives pointwise

\[
\mathcal L_sU_s=0,
\qquad
\nu_s(U_s)=0.
\tag{4.3}
\]

Applying (3.2) to (4.1),

\[
D'(s)=
\nu_s(A_{1,s}\mathcal R_sf_s)+\nu_s(U_s)
=\nu_s\left(U_s\,\mathcal R_sf_s\right).
\tag{4.4}
\]

The last equality uses

\[
A_{1,s}H=\mathcal L_s(U_sH)
\]

and invariance.

## 5. Fisher coefficient

The `V_0`-valued differentiability of `ell_s` gives

\[
\frac{f_s}{s}\longrightarrow U_0
\quad\text{in }\mathcal V_0.
\tag{5.1}
\]

Continuity of the Poisson operator from `V_0` to `C` implies

\[
\mathcal R_s\left(\frac{f_s}{s}\right)
\longrightarrow
\mathcal R_0U_0
\quad\text{uniformly}.
\tag{5.2}
\]

By (4.3),

\[
\mathcal L_0U_0=0,
\qquad \nu_0(U_0)=0.
\]

Therefore the Poisson series collapses after its zeroth term:

\[
\mathcal R_0U_0=U_0.
\tag{5.3}
\]

Divide (4.4) by `s`, use (5.1)--(5.3), weak continuity of `nu_s`, and uniform
convergence of the scores. Then

\[
\lim_{s\downarrow0}\frac{D'(s)}s
=\nu_0(U_0^2)
=\mathcal I_s(0).
\tag{5.4}
\]

Since `D(0)=0`, integration gives

\[
D(s)=\frac12\mathcal I_s(0)s^2+o(s^2).
\tag{5.5}
\]

Substituting `s=t^2` proves (1.3).

## 6. Matching lower bound and scope

The accepted regularity-free matching inequality gives

\[
D(t^2)\ge\frac12 d_{Ber}
\left(\mu^2-|\widehat g(k)|^2t^2\,\middle\|\,\mu^2\right).
\]

Comparison with (5.5) proves (1.4).

This theorem establishes existence and positivity of the exact centered
quartic coefficient for the true entropy rate in the range `p>=1/2`. It does
not control `D''(s)` for `s>0`, and hence does not prove local concavity in the
range `1/2<=p<1`. A lower bound on the centered deficit and a quartic Peano
expansion do not determine curvature at nearby nonzero parameters; the scalar
approximation obstruction already preserved in PR66/PR82 applies to that
logical inference.
