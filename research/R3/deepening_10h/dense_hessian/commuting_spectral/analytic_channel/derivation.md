# D10-M3 derivation: spectral subset through a fixed projection-DPP channel

Author status: **PROOF_CANDIDATE_PENDING_FRESH_REVIEW**.

## 1. Channel representation

Let \(Q_R\) denote the columns of \(Q\) indexed by \(R\).  For fixed \(R\), the
rank-\(|R|\) projection kernel \(P_R=Q_RQ_R^\top\) defines a projection DPP.
It has exactly \(|R|\) points, and for \(|S|=|R|\)

\[
\mathbb P(Y=S\mid R)=\det(P_R[S,S])
=\det(Q_{S,R}Q_{S,R}^\top)
=\det(Q_{S,R})^2.
\]

For \(|S|\ne |R|\), the probability is zero.  Cauchy--Binet gives
\(\sum_{|S|=|R|}\det(Q_{S,R})^2=\det(Q_R^\top Q_R)=1\), so each column is a
probability vector.  Similarly, for fixed \(S\),
\(\sum_{|R|=|S|}\det(Q_{S,R})^2=\det(Q_SQ_S^\top)=1\), so each cardinality
block is doubly stochastic.

Now choose \(R\) by independent Bernoulli eigenvalue variables with law
\(\mu_t(R)\).  The inclusion probability of \(A\subseteq Y\) under the mixture is

\[
\sum_R \mu_t(R)\det(P_R[A,A]).
\]

Using Cauchy--Binet inside \(P_R[A,A]\),

\[
\det(P_R[A,A])
=\sum_{\substack{L\subseteq R\\ |L|=|A|}}\det(Q_{A,L})^2.
\]

Taking expectation over \(R\), the event \(L\subseteq R\) has probability
\(\prod_{i\in L}\theta_i(t)\).  Therefore

\[
\mathbb P(A\subseteq Y)
=\sum_{|L|=|A|}\det(Q_{A,L})^2\prod_{i\in L}\theta_i(t)
=\det(Q_A\operatorname{diag}(\theta_i(t))Q_A^\top)
=\det K(t)_A.
\]

The inclusion probabilities match those of the DPP kernel \(K(t)\); finite
Möbius inversion then gives the exact atom formula in `frozen_claim.md`.

## 2. Output Hessian by latent scores

Write \(x_i={\bf1}_{i\in R}\).  Since each factor
\(\theta_i^{x_i}(1-\theta_i)^{1-x_i}\) is affine in \(t\),

\[
\frac{d}{dt}\log \mu_t(R)
=a_R(t)
=\sum_i v_i\left(\frac{x_i}{\theta_i(t)}
-\frac{1-x_i}{1-\theta_i(t)}\right).
\]

The second derivative of the log cancels exactly with the square's diagonal
terms, leaving only pair interactions:

\[
\mu_t''(R)=\mu_t(R)b_R(t),
\]

where

\[
b_R(t)=2\sum_{i<j} v_iv_j
\left(\frac{x_i}{\theta_i(t)}-\frac{1-x_i}{1-\theta_i(t)}\right)
\left(\frac{x_j}{\theta_j(t)}-\frac{1-x_j}{1-\theta_j(t)}\right).
\]

Because the channel \(T_Q\) is fixed,

\[
p_t(S)=\sum_R T_Q(S\mid R)\mu_t(R),\quad
p_t'(S)=\sum_R T_Q(S\mid R)\mu_t(R)a_R(t),\quad
p_t''(S)=\sum_R T_Q(S\mid R)\mu_t(R)b_R(t).
\]

All atoms are positive when \(0<K(t)<I\), so differentiating
\(-\sum_Sp_t(S)\log p_t(S)\) is legitimate and gives

\[
H(Y_t)''
=-\sum_S\frac{p_t'(S)^2}{p_t(S)}
 -\sum_Sp_t''(S)\log p_t(S).
\]

This is the spectral-channel counterpart of the signed-determinant Hessian
formula used by D10-H; it computes the same exact event law.

## 3. Cardinality split and the remaining obstruction

The projection-DPP channel preserves cardinality.  Let

\[
N_t=|R|=|Y_t|,\qquad \pi_k(t)=\mathbb P(N_t=k).
\]

Then

\[
H(Y_t)=H(N_t)+\Psi_Q(t),\qquad
\Psi_Q(t)=H(Y_t\mid N_t).
\]

The first term is the entropy of a Poisson-binomial sum of independent
Bernoulli variables with affine parameters \(\theta_i(t)\).  By the
Shepp--Olkin theorem, \(H(N_t)''\le0\).

The second term is explicitly computable from the atom probabilities:

\[
\Psi_Q(t)
=-\sum_Sp_t(S)\log p_t(S)+\sum_k\pi_k(t)\log\pi_k(t).
\]

Thus

\[
\Psi_Q''(t)
=-\sum_S\left(\frac{p_t'(S)^2}{p_t(S)}+p_t''(S)\log p_t(S)\right)
+\sum_k\left(\frac{\pi_k'(t)^2}{\pi_k(t)}+\pi_k''(t)\log\pi_k(t)\right).
\]

This formula is a finite, exact, checkable certificate target.  It also gives
the clean obstruction:

\[
H(Y_t)''>0
\quad\Longrightarrow\quad
\Psi_Q''(t)>-H(N_t)''\ge0.
\]

So after the spectral-channel reduction, any PSD/NSD flip must be created by
the conditional observation distribution inside fixed cardinality layers.

## 4. Posterior form

Let \(h_Q(R)=H(T_Q(\cdot\mid R))\).  The joint law
\(\mathbb P(R,S)=\mu_t(R)T_Q(S\mid R)\) gives

\[
H(Y_t)=H(R_t)+\mathbb E_{\mu_t}h_Q(R)-H(R_t\mid Y_t).
\]

Here

\[
H(R_t)=\sum_i h(\theta_i(t)),\qquad
H(R_t)''=-\sum_i\frac{v_i^2}{\theta_i(t)(1-\theta_i(t))}\le0.
\]

Therefore the only unclosed correction after the explicit spectral Bernoulli
term is

\[
R_Q(t)=\mathbb E_{\mu_t}h_Q(R)-H(R_t\mid Y_t).
\]

This is equivalent to the cardinality conditional term up to the already
controlled components.  One must not claim that posterior entropy alone has a
favourable sign: \(\mathbb E h_Q(R)\) is itself generally multi-affine in the
\(\theta_i\) and may have nonzero second derivative along heterogeneous
directions.

## 5. Sufficient channel conditions

The exact reduction immediately gives the sufficient condition

\[
\Psi_Q''(t)\le -H(N_t)''
\]

for concavity at \(t\), and the stronger easy-to-check condition
\(\Psi_Q''(t)\le0\).

A closed analytic subcase is available when the channel makes the conditional
output law depend only on cardinality.  More generally, suppose
\(Y_t\mid N_t=k\) is independent of \(t\) with entropy \(c_k\).  Then

\[
\Psi_Q(t)=\mathbb E c_{N_t}.
\]

If the sequence \(c_k\) is discretely concave,

\[
c_{k+2}-2c_{k+1}+c_k\le0,
\]

and all \(v_i\) have the same sign, then \(\Psi_Q''(t)\le0\).  Indeed, writing
\(N_{-ij}\) for the sum with coordinates \(i,j\) removed,

\[
\frac{d^2}{dt^2}\mathbb E c_{N_t}
=2\sum_{i<j}v_iv_j\,
\mathbb E\left[c_{N_{-ij}+2}-2c_{N_{-ij}+1}+c_{N_{-ij}}\right]\le0.
\]

For the cardinality-uniform projection channel,

\[
T_Q(S\mid R)=\binom nk^{-1}\quad(|S|=|R|=k),
\]

we have \(c_k=\log\binom nk\).  This sequence is discretely concave because

\[
\Delta^2\log\binom nk
=\log\frac{\binom n{k+2}\binom nk}{\binom n{k+1}^2}
=\log\frac{(n-k-1)(k+1)}{(k+2)(n-k)}\le0.
\]

Hence this channel class is concave for PSD and NSD spectral-rate directions.

Signed-permutation \(Q\) gives another closed case: the channel is a relabeling,
so \(H(Y_t)=H(R_t)=\sum_i h(\theta_i(t))\).

## 6. A nontrivial closed 2D spectral block

For \(n=2\), let \(Q\) be any real orthogonal matrix.  Squared entries in a
column have the form \((\alpha,1-\alpha)\), while the other column has
\((1-\alpha,\alpha)\), with \(0\le\alpha\le1\).  Set

\[
r(t)=\theta_1(t)(1-\theta_2(t)),\qquad
s(t)=(1-\theta_1(t))\theta_2(t).
\]

The two cardinality-one output atoms are

\[
u(t)=\alpha r(t)+(1-\alpha)s(t),\qquad
w(t)=(1-\alpha)r(t)+\alpha s(t).
\]

The empty and full atoms depend only on the count \(N\).  Hence

\[
H(Y_t)=H(N_t)+G(r(t),s(t)),
\]

where

\[
G(r,s)
=-u\log\frac{u}{r+s}-w\log\frac{w}{r+s},
\quad
u=\alpha r+(1-\alpha)s,\quad
w=(1-\alpha)r+\alpha s.
\]

The function \((u,w)\mapsto -u\log(u/(u+w))-w\log(w/(u+w))\) is the perspective
of the binary entropy and is concave on \(u,w>0\).  Composing with the positive
linear map \((r,s)\mapsto(u,w)\) shows \(G\) is concave in \((r,s)\).
Moreover

\[
\partial_rG=\alpha\log\frac{r+s}{u}
 +(1-\alpha)\log\frac{r+s}{w}\ge0,
\]

and similarly \(\partial_sG\ge0\), because \(0<u,w\le r+s\).

If the spectral rates have one sign, then \(v_1v_2\ge0\), so

\[
r''(t)=s''(t)=-2v_1v_2\le0.
\]

The chain rule gives

\[
\frac{d^2}{dt^2}G(r(t),s(t))
=
\begin{bmatrix}r'&s'\end{bmatrix}
\nabla^2G
\begin{bmatrix}r'\\s'\end{bmatrix}
+\partial_rG\,r''+\partial_sG\,s''\le0.
\]

Together with \(H(N_t)''\le0\), this proves concavity for every 2D fixed
spectral block with PSD or NSD spectral rate direction.

If a higher-dimensional kernel and direction decompose as an
observation-coordinate direct sum of such \(2\times2\) blocks and \(1\times1\)
blocks, the DPP law is a product across blocks and entropy is additive.  The
same concavity follows blockwise.  This block direct-sum result is useful as an
exclusion family but, by itself, cannot generate a coupled \(n\ge11\)
counterexample seed.

## 7. What failed to close generally

For a generic fixed \(Q\), the cardinality-block channel \(T_{Q,k}\) is
doubly stochastic but not column-identical and not entropy-constant on arbitrary
input laws.  Doubly stochasticity only gives a pointwise entropy increase
\(H(T_{Q,k}\nu)\ge H(\nu)\); it does not control the second derivative of
\(H(T_{Q,k}\nu_t)\) as the posterior spectral law \(\nu_t=R_t\mid |R_t|=k\)
moves through the simplex.

Thus the nontrivial unresolved analytic target is:

\[
\text{control the curvature of }H(T_{Q,k}\nu_t)
\text{ for the special Poisson-binomial conditional paths }\nu_t.
\]

This is strictly weaker than the original all-direction Hessian problem, but it
is still not closed by the present argument.
