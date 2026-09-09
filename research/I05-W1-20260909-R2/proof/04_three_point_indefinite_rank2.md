# Proof IV — every real three-point indefinite rank-two line is entropy-concave

## Theorem

Let `K` be a strict real symmetric `3 x 3` DPP kernel and let `D` be a real symmetric rank-two matrix whose two nonzero eigenvalues have opposite signs. On every interval on which

\[
0<K+zD<I,
\]

the complete-configuration Shannon entropy `z -> H(K+zD)` is concave.

This is a statement about the original observation coordinates. No orthogonal change of basis is used.

## 1. Quadratic event coefficients

For a complete configuration `S subseteq {1,2,3}`, write

\[
p_z(S)=p_{K+zD}(S)=p(S)+z r(S)+z^2 c(S).
\]

There is no cubic term because `rank(D)=2`. The coefficient law `c` is uniquely determined by its inclusion moments. For a pair `{i,j}`,

\[
\sum_{S\supseteq\{i,j\}}c(S)=\det D_{\{i,j\}}=:\delta_{ij}. \tag{1}
\]

For the full triple, the coefficient of `z^2` in `det(K+zD)` is

\[
\sum_S 1_{S=\{1,2,3\}}c(S)
=\operatorname{tr}(\operatorname{adj}(D)K). \tag{2}
\]

The total and all one-coordinate inclusion moments of `c` vanish, since normalization and one-point inclusion probabilities are affine in `z`.

Because `D` is symmetric of rank two, its adjugate has rank one. Choose a unit null vector `n` of `D`; then

\[
\operatorname{adj}(D)=\gamma nn^T, \tag{3}
\]

where `gamma` is the product of the two nonzero eigenvalues. Indefiniteness gives `gamma<0`. If `{i,j,k}={1,2,3}`, then

\[
\delta_{ij}=\operatorname{adj}(D)_{kk}=\gamma n_k^2,\qquad
\sum_{i<j}\delta_{ij}=\gamma. \tag{4}
\]

Put

\[
\kappa=n^TKn.
\]

Strict contraction gives `0<kappa<1`, and (2) becomes `gamma kappa`.

## 2. Exact conditional four-cycle decomposition

For a pair `{i,j}` with remaining coordinate `k` and `epsilon in {0,1}`, define the signed four-cycle `e^{ij|k=epsilon}` on complete configurations by fixing `x_k=epsilon` and assigning

\[
(+1,-1,-1,+1)
\]

to `(x_i,x_j)=(0,0),(1,0),(0,1),(1,1)` respectively. It has zero total and zero one-point moments. Its only nonzero pair inclusion coefficient is the `{i,j}` coefficient, equal to one. Its triple inclusion coefficient is zero when `epsilon=0` and one when `epsilon=1`.

Consequently the signed measure

\[
\widetilde c
=\sum_{i<j}\delta_{ij}
 \left[(1-\kappa)e^{ij|k=0}+\kappa e^{ij|k=1}\right] \tag{5}
\]

has pair coefficients `delta_ij`, triple coefficient

\[
\kappa\sum_{i<j}\delta_{ij}=\gamma\kappa,
\]

and vanishing lower inclusion moments. Boolean Möbius inversion is injective, so comparison with (1)–(2) proves

\[
\boxed{c=\widetilde c.} \tag{6}
\]

This is the key rank-two identity. It is not a fitted decomposition.

## 3. DPP conditional odds have the required sign

Fix `k=epsilon`. Conditional on that exact value, the remaining two coordinates form a strict real two-point DPP. For any positive two-by-two table `q`,

\[
q_{00}q_{11}-q_{10}q_{01}
=\operatorname{Cov}(1_{i\in X},1_{j\in X}).
\]

For a DPP this covariance is the negative square of the conditional kernel off-diagonal entry. Hence

\[
L_{ij|k=\epsilon}
:=\left\langle e^{ij|k=\epsilon},\log p\right\rangle
=\log\frac{p_{00\epsilon}p_{11\epsilon}}
               {p_{10\epsilon}p_{01\epsilon}}
\le0. \tag{7}
\]

The use of unnormalized joint probabilities in (7) is harmless because the common conditional normalizer cancels.

Pairing (6) with `log p` gives

\[
\langle c,\log p\rangle
=\sum_{i<j}\delta_{ij}
\left[(1-\kappa)L_{ij|k=0}+\kappa L_{ij|k=1}\right]. \tag{8}
\]

Every bracket is nonpositive, while every `delta_ij=gamma n_k^2` is nonpositive. Therefore

\[
\langle c,\log p\rangle\ge0. \tag{9}
\]

## 4. Complete curvature

Differentiating the full finite entropy and using `sum_S r(S)=sum_S c(S)=0` yields

\[
\frac{d^2}{dz^2}H(K+zD)
=-\sum_S\frac{(r(S)+2zc(S))^2}{p_z(S)}
 -2\sum_Sc(S)\log p_z(S). \tag{10}
\]

At any interior point of the legal line, repeat (3)–(9) with that point as the current kernel. The direction `D`, its null vector, and `gamma<0` are unchanged, while `0<n^T(K+zD)n<1`; because `Dn=0`, this scalar is in fact constant. Thus both terms in (10) are nonpositive. Hence the entropy is concave throughout the open legal interval. Continuity of `-x log x` at zero extends the chord inequality to legal boundary endpoints.

## Scope

The proof uses both dimension three and the negative sign of the product of the two nonzero eigenvalues. For positive- or negative-semidefinite rank-two directions, the cycle coefficients have the opposite sign and the acceleration term can be harmful; the Fisher term must then be retained. No claim for those directions is made here.