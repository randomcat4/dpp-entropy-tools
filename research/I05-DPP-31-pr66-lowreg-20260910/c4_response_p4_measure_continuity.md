# Direct DPP continuity and uniqueness closure

Status: **AUTHOR PROOF SUPPLEMENT / PENDING_REVIEW**.

This note replaces the compactness/uniqueness paragraph in Lemma 6.1 of `c4_response_p4_repair.md` for the actual DPP application.  It is not necessary to cite a general continuity theorem for `g`-measures.

## 1. Weak continuity from complete events

Let `nu_t` be the stationary DPP law with the true affine kernel

\[
K_t=T(c)+tT(g).
\]

For every finite coordinate set `I` and complete word `x in {0,1}^I`, with zero set `Z_x`,

\[
\nu_t(X_I=x)
=(-1)^{|Z_x|}\det\bigl(T_I(c+t g)-I_{Z_x}\bigr).
\tag{1.1}
\]

The right-hand side is a polynomial in the physical parameter `t`.  The half-period diagonal conjugacy makes it even in `t`, hence it is a polynomial in

\[
s=t^2.
\]

Therefore every cylinder probability is continuous, indeed analytic, in `s` at zero and throughout the small physical interval.  On the compact product space `{0,1}^N`, cylinder convergence implies weak convergence.  Thus

\[
s_n\to s\quad\Longrightarrow\quad \nu_{s_n}\Rightarrow\nu_s.
\tag{1.2}
\]

This argument retains every complete event and does not pass through inclusion probabilities alone.

## 2. Invariance of the future law

Let `G_s(x_0|x_1,x_2,...)` be the continuous version of the true right-to-left conditional obtained from the complete-event Schur limits, and define

\[
(\mathcal L_sF)(x_1,x_2,...)
=\sum_{x_0=0}^1G_s(x_0|x_1,x_2,...)F(x_0,x_1,x_2,...).
\]

For bounded continuous `F`, the defining conditional-expectation identity and stationarity give

\[
\nu_s(\mathcal L_sF)
=E_{\nu_s}E_{\nu_s}[F(X_0,X_1,...)\mid X_1,X_2,...]
=E_{\nu_s}F(X_0,X_1,...)
=\nu_s(F).
\tag{2.1}
\]

Hence `nu_s L_s=nu_s` without invoking a Gibbs variational principle or pressure theorem.

## 3. Uniqueness from the same coupling estimate

Suppose `rho` and `eta` are two invariant probability measures compatible with the same normalized kernel `G_s`.  For `F in B_b`, `1<b<=a`, invariance and the relaxation estimate give

\[
\begin{aligned}
|\rho(F)-\eta(F)|
&=|\rho(\mathcal L_s^nF)-\eta(\mathcal L_s^nF)|\\
&\le\operatorname{osc}(\mathcal L_s^nF)\\
&\le C_b\|F\|_b(1+n)^{-b}\to0.
\end{aligned}
\tag{3.1}
\]

Cylinder functions lie in every `B_b` and determine a probability measure.  Thus `rho=eta`.  This is also enough to identify any invariant limit if one chooses a compactness argument, but the DPP cylinder formula (1.1) already supplies direct continuity.

## 4. Consequence for the response identity

The exact perturbation identity

\[
(\nu_u-\nu_s)(F)
=\nu_u(\mathcal L_u-\mathcal L_s)\mathcal R_sF
\tag{4.1}
\]

requires only:

1. invariance (2.1);
2. the Poisson identity `(I-L_s)R_sF=F-nu_sF`;
3. weak continuity (1.2) when taking difference quotients.

All three are now proved in the actual DPP setting before any derivative is taken.  The subsequent first/second response formulas and the `B_a -> B_{a-1} -> B_{a-2}` scale are unchanged.

## 5. Scope

This supplement does not claim that arbitrary normalized complete-connection kernels depend continuously on parameters under only summable variation.  It proves exactly what is needed here from the determinantal finite-dimensional law.  It also does not reintroduce PR66's invalid Dobrushin A1/A2 pressure import.