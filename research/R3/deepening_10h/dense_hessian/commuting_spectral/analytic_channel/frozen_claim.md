# D10-M3 frozen claim: commuting spectral channel reduction

Author status: **PROOF_CANDIDATE_PENDING_FRESH_REVIEW**.  This file freezes the
claim for later non-author verification; it does not certify the general
PSD/NSD semidefinite-direction problem.

## Domain

Let \(Q\in O(n)\) be a fixed real orthogonal matrix.  Let

\[
K(t)=Q\operatorname{diag}(\theta_1(t),\ldots,\theta_n(t))Q^\top,\qquad
\theta_i(t)=\lambda_i+t v_i,
\]

on an open interval \(J_0\), with \(0<\theta_i(t)<1\) for every \(i,t\).
If all \(v_i\ge0\), then \(D=Q\operatorname{diag}(v_i)Q^\top\succeq0\); if all
\(v_i\le0\), then \(D\preceq0\).  All entropies use natural logarithms and
all DPP event probabilities are exact atom probabilities, not inclusion
probabilities.

## Claim A: fixed projection-DPP channel representation

Let \(Z_t\subseteq[n]\) be the latent spectral subset with independent
Bernoulli coordinates

\[
\mathbb P(Z_t=R)=\mu_t(R)
=\prod_{i\in R}\theta_i(t)\prod_{i\notin R}(1-\theta_i(t)).
\]

Conditional on \(Z_t=R\), let \(Y_t\) be drawn from the projection DPP with
kernel \(P_R=Q_RQ_R^\top\).  Equivalently,

\[
T_Q(S\mid R)=
\begin{cases}
\det(Q_{S,R})^2,& |S|=|R|,\\
0,& |S|\ne |R|.
\end{cases}
\]

Then the exact atom law of the DPP with kernel \(K(t)\) is

\[
p_t(S)=\mathbb P(Y_t=S)=\sum_{R\subseteq[n]}T_Q(S\mid R)\mu_t(R).
\]

The channel \(T_Q\) is fixed in \(t\) and preserves cardinality:
\(|Y_t|=|Z_t|\) almost surely.

## Claim B: checkable Hessian split

For \(R\subseteq[n]\), define

\[
a_R(t)=\sum_{i\in R}\frac{v_i}{\theta_i(t)}
       -\sum_{i\notin R}\frac{v_i}{1-\theta_i(t)}
\]

and

\[
b_R(t)=2\sum_{i<j}v_iv_j
\left({\bf1}_{i\in R}\theta_i(t)^{-1}
      -{\bf1}_{i\notin R}(1-\theta_i(t))^{-1}\right)
\left({\bf1}_{j\in R}\theta_j(t)^{-1}
      -{\bf1}_{j\notin R}(1-\theta_j(t))^{-1}\right).
\]

Then

\[
\mu'_t(R)=\mu_t(R)a_R(t),\qquad
\mu''_t(R)=\mu_t(R)b_R(t),
\]

and hence

\[
p'_t(S)=\sum_R T_Q(S\mid R)\mu_t(R)a_R(t),\qquad
p''_t(S)=\sum_R T_Q(S\mid R)\mu_t(R)b_R(t).
\]

The output entropy satisfies

\[
H(Y_t)''
=-\sum_S\frac{p'_t(S)^2}{p_t(S)}
 -\sum_S p''_t(S)\log p_t(S).
\]

Equivalently, because \(N_t=|Z_t|=|Y_t|\),

\[
H(Y_t)=H(N_t)+\Psi_Q(t),\qquad
\Psi_Q(t)=H(Y_t\mid N_t).
\]

The Poisson-binomial term \(H(N_t)\) is concave by the Shepp--Olkin theorem
for affine Bernoulli parameters.  Therefore any positive curvature along this
commuting spectral PSD/NSD route must come from the conditional channel term
\(\Psi_Q(t)\).

## Claim C: usable sufficient condition

For a fixed \(Q,\lambda,v\), the following checkable condition is sufficient:

\[
\Psi_Q''(t)\le -H(N_t)''\quad\text{on }J_0.
\]

The stronger condition \(\Psi_Q''(t)\le0\) on \(J_0\) is also sufficient.

In posterior notation,

\[
H(Y_t)=H(Z_t)+\mathbb E[H(Y_t\mid Z_t)]-H(Z_t\mid Y_t).
\]

Since \(H(Z_t)=\sum_i h(\theta_i(t))\) is explicitly concave, the unclosed
posterior/channel correction is

\[
R_Q(t)=\mathbb E[H(Y_t\mid Z_t)]-H(Z_t\mid Y_t).
\]

It is not safe to discard either summand separately; the controlled object is
the combined conditional term, or equivalently \(\Psi_Q(t)=H(Y_t\mid |Y_t|)\).

## Claim D: closed sufficient subclasses

1. **Signed-permutation channel.**  If \(Q\) is a signed permutation matrix,
   \(Y_t\) is a relabeling of \(Z_t\), so
   \(H(Y_t)=\sum_i h(\theta_i(t))\) and
   \(H(Y_t)''=-\sum_i v_i^2/[\theta_i(t)(1-\theta_i(t))]\le0\).

2. **Every two-dimensional fixed spectral block.**  For \(n=2\), every
   real orthogonal \(Q\), every strict path
   \(Q\operatorname{diag}(\theta_1(t),\theta_2(t))Q^\top\), and same-sign
   rates \(v_1v_2\ge0\), the observed DPP entropy is concave.  Consequently,
   any observation-coordinate direct sum of \(1\times1\) signed-permutation
   blocks and \(2\times2\) fixed spectral blocks is concave when all spectral
   rates in all blocks are nonnegative, or when all are nonpositive.  This gives
   a nontrivial exclusion family with within-block off-diagonal
   kernels/directions, but it is still a direct-sum family.

3. **Cardinality-uniform projection channel.**  Suppose that for every
   cardinality \(k\), every \(k\times k\) squared minor satisfies
   \[
   \det(Q_{S,R})^2=\binom{n}{k}^{-1}
   \quad\text{whenever } |S|=|R|=k.
   \]
   Then \(Y_t\mid N_t=k\) is uniform on \(k\)-subsets, independent of
   \(\lambda,v,t\), and
   \[
   H(Y_t)=H(N_t)+\mathbb E\log\binom{n}{N_t}.
   \]
   If all \(v_i\ge0\) or all \(v_i\le0\), this entropy is concave in \(t\).

The cardinality-uniform condition gives a non-permutation analytic channel
class where it exists.  In real dimension \(n=2\), the normalized
Hadamard/equal-diagonal case satisfies it and permits heterogeneous positive
spectral rates.  No classification or high-dimensional abundance of this
condition is claimed.

## Non-claim

The above does **not** prove concavity for arbitrary fixed \(Q\) and
heterogeneous \(v_i\ge0\).  The exact remaining obstruction is the curvature of
\(\Psi_Q(t)=H(Y_t\mid |Y_t|)\), equivalently the combined posterior/channel
correction \(R_Q(t)\).  Finite scans in neighbouring folders are not used as
theorem evidence.
