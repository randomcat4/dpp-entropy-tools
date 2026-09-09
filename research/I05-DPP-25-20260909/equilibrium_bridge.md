# Authoritative equilibrium bridge

This note replaces the informal argument in `proof.md`, Section 5. It is the load-bearing identification of the DPP with the finite-first-moment interaction constructed there. No hereditary-uniqueness hypothesis and no spectral entropy formula are used.

## Setup

For real sufficiently small `t`, let

\[
\nu_t=\mathbf P_{c+tg}.
\]

The complete-event Schur complements in `proof.md`, Section 3, converge uniformly to a non-null future conditional

\[
G_t(a\mid x_1,x_2,\ldots)
=\nu_t(X_0=a\mid X_1=x_1,X_2=x_2,\ldots)
\]

and `\phi_t=\log G_t`. Section 4 constructs

\[
\phi_t=\sum_{n\ge0}\psi_{n,t}
\]

uniformly and defines the translation-invariant interval interaction

\[
U_{t,[i,i+n]}=-\psi_{n,t}\circ T^i,
\qquad
U_{t,A}=0
\quad\text{otherwise}.
\]

The strong first-moment estimate

\[
\sum_{A\ni0}\operatorname{diam}(A)\|U_{t,A}\|_\infty<\infty
\tag{B.1}
\]

holds locally uniformly in the complex parameter. In particular all sums below are absolutely convergent.

## 1. Conditional cross-entropy inequality

Let `\rho` be any shift-invariant probability measure on `\{0,1\}^{\mathbb Z}`. Let

\[
r_\rho(a\mid x_1,x_2,\ldots)
\]

be a regular conditional law of `X_0` given the infinite future. For a stationary finite-alphabet process,

\[
h(\rho)
=
H_\rho(X_0\mid X_1,X_2,\ldots),
\tag{B.2}
\]

because

\[
H_\rho(X_0\mid X_1,\ldots,X_n)
=H_\rho(X_0,\ldots,X_n)-H_\rho(X_1,\ldots,X_n)
\longrightarrow h(\rho).
\]

Therefore

\[
\begin{aligned}
h(\rho)+\rho(\phi_t)
&=
-\int
D_{\mathrm{KL}}
\left(
 r_\rho(\cdot\mid x_1^\infty)
 \,\middle\|\,
 G_t(\cdot\mid x_1^\infty)
\right)
\,d\rho(x)\\
&\le0.
\end{aligned}
\tag{B.3}
\]

Equality holds if and only if the future conditional of `\rho` agrees with `G_t` almost surely. In particular equality holds for `\rho=\nu_t`.

## 2. The specific energy is exactly minus the log conditional

Use the standard specific-energy representative

\[
e_{U_t}(x)
=
\sum_{A\ni0}\frac{1}{|A|}U_{t,A}(x).
\]

For the interval interaction above and every invariant `\rho`, stationarity and absolute convergence give

\[
\begin{aligned}
\rho(e_{U_t})
&=
\sum_{n\ge0}\frac1{n+1}
\sum_{i=-n}^{0}
\rho\bigl(U_{t,[i,i+n]}\bigr)\\
&=-\sum_{n\ge0}\rho(\psi_{n,t})\\
&=-\rho(\phi_t).
\end{aligned}
\tag{B.4}
\]

Combining (B.3) and (B.4),

\[
h(\rho)-\rho(e_{U_t})\le0
\tag{B.5}
\]

for every invariant `\rho`, with equality at `\nu_t`.

## 3. Exact equilibrium identification

The variational principle for absolutely summable interactions states

\[
P(U_t)
=
\sup_{\rho\ {m invariant}}
\left[h(\rho)-\rho(e_{U_t})\right].
\]

Equations (B.5) and the equality case at `\nu_t` imply

\[
\boxed{
P(U_t)=0,
\qquad
\nu_t\text{ is an equilibrium state for }U_t.
}
\tag{B.6}
\]

For finite-first-moment one-dimensional interactions, the Dobrushin–Cassandro–Olivieri theorem supplies the unique Gibbs/equilibrium state and analytic dependence of pressure and local expectations. Thus the equilibrium branch selected by that theorem is exactly the DPP branch `\nu_t`.

This proves the identification needed in `proof.md`, Sections 6–8. Fernández–Maillard's LIS-to-specification theorem is consistent with the construction—our variation is summable—but is not needed for (B.6).

## 4. Entropy as an analytic pressure derivative

The parity gauge proves that `U_t` is an even holomorphic interaction curve. Write it as `U_s`, `s=t^2`, and define

\[
F(s,\lambda)=P(\lambda U_s).
\]

The finite-first-moment analyticity theorem makes `F` holomorphic near `(0,1)`. Pressure differentiation at the unique equilibrium state gives

\[
\partial_\lambda F(s,1)
=-\nu_s(e_{U_s}).
\]

By (B.4), (B.6), and `h(\nu_s)=-\nu_s(\phi_s)=\nu_s(e_{U_s})`,

\[
\boxed{
h(\nu_s)=F(s,1)-\partial_\lambda F(s,1).}
\tag{B.7}
\]

Thus this is the true configuration Shannon entropy rate, and it is analytic in `s`.

## 5. Relative-entropy pressure identity and sign audit

For two real interactions `U_s,U_0` under the convention

\[
P(U)=\sup_\rho[h(\rho)-\rho(e_U)],
\]

the specific relative entropy of their equilibrium states is

\[
\begin{aligned}
d(\nu_s\|\nu_0)
&=P(U_0)-h(\nu_s)+\nu_s(e_{U_0})\\
&=P(U_0)-P(U_s)+\nu_s(e_{U_0}-e_{U_s}).
\end{aligned}
\]

Since

\[
DP(U_s)[V]=-\nu_s(e_V),
\]

putting `\Delta_s=U_s-U_0` yields

\[
\boxed{
d(\nu_s\|\nu_0)
=P(U_0)-P(U_s)+DP(U_s)[\Delta_s].}
\tag{B.8}
\]

At `s=0`, `\Delta_0=0`, so differentiation gives

\[
-DP(U_0)[U'_0]+DP(U_0)[U'_0]=0.
\]

This verifies the cancellation used to obtain the `t^4+O(t^6)` entropy deficit.

## Scope

The argument is real-probabilistic only where a probability law is required. Complex parameters are used solely to obtain a holomorphic interaction and pressure neighborhood. The complete-event determinant formula is retained throughout. This bridge concerns the true stationary configuration entropy rate, not a finite-window or spectral surrogate.
