# I05-DPP-36 — strict `L^infinity` symbols: true entropy-rate central second-difference bounds

Status: **PROVED AS AN AUTHOR THEOREM / PENDING INDEPENDENT REVIEW.**

This successor starts from current `main@b3ada9f6bb23e3efd2e1a4d2a2977d50b61fb4d7`. It does not modify PR117 or inherit any review verdict from PR113/117. No computation or novelty claim is made.

The result is deliberately weaker than local `C^4` concavity but applies far beyond the Wiener algebra. It gives a genuine uniform central second-difference bound for the true complete-configuration Shannon entropy rate.

## 1. Theorem

Let real measurable `c,g in L^infinity(T)` satisfy

\[
c(\theta+1/2)=c(\theta),\qquad
 g(\theta+1/2)=-g(\theta),\qquad g\ne0,
\]

and suppose

\[
\delta\le c(\theta)\le1-\delta
\quad\text{a.e.}
\tag{1.1}
\]

for some `0<delta<1/2`. Put

\[
\mu=\int_T c(\theta)d\theta.
\]

Choose `tau>0` so that

\[
\delta/2\le c+t g\le1-\delta/2
\quad\text{a.e. for }|t|\le\tau.
\tag{1.2}
\]

Then for every such `t`, writing

\[
J(t)=h(c)-h(c+t g),
\]

one has

\[
0\le J(t)
\le
\frac{t^2\|g\|_{L^2(T)}^2}
{\delta(1-\delta/2)}.
\tag{1.3}
\]

Moreover, for every odd integer `k` with `\widehat g(k)\ne0`, the accepted regularity-free parity matching bound gives

\[
J(t)\ge
\frac12 d_{\rm Ber}
\left(
\mu^2-|\widehat g(k)|^2t^2\,\middle\|\,\mu^2
\right).
\tag{1.4}
\]

Since the complete laws at `t` and `-t` coincide,

\[
\Delta_t^2 h(0)
:=h(c+t g)+h(c-t g)-2h(c)
=-2J(t).
\tag{1.5}
\]

Therefore the true entropy-rate second difference satisfies the explicit sandwich

\[
\boxed{
-\frac{2t^2\|g\|_2^2}{\delta(1-\delta/2)}
\le \Delta_t^2h(0)
\le
-d_{\rm Ber}
\left(
\mu^2-|\widehat g(k)|^2t^2\,\middle\|\,\mu^2
\right)
\le0.}
\tag{1.6}
\]

In particular,

\[
\Delta_t^2 h(0)=O(t^2),
\]

uniformly over finite windows and after passage to the true rate, while the matching side forces a negative quartic scale whenever the selected odd Fourier coefficient is nonzero.

This theorem requires no Wiener summability, positive Fourier moment, finite range, hidden-Markov representation, or differentiability of the entropy rate.

## 2. Exact parity/KL identity for complete laws

Let `Lambda_n={1,...,n}` and let `P_{n,t}` be the full DPP occupation law for the compressed kernel

\[
K_{n,t}=T_{\Lambda_n}(c+t g).
\]

Because `c` has only even Fourier modes and `g` only odd Fourier modes, the restrictions to even and odd lattice sites are independent of `t`, and at `t=0` the cross-parity kernel block vanishes. Therefore

\[
P_{n,0}=P_{E_n}\otimes P_{O_n}
\]

where `P_{E_n},P_{O_n}` are the actual fixed parity marginals of `P_{n,t}`. Hence, using every complete occupied/vacant word,

\[
D(P_{n,t}\|P_{n,0})
=H_n(c)-H_n(c+t g).
\tag{2.1}
\]

The diagonal gauge `U_j=(-1)^j` gives

\[
K_{n,-t}=U K_{n,t}U^*,
\]

and `U` commutes with every occupied/vacant diagonal mask. Thus every complete atom is unchanged and

\[
P_{n,-t}=P_{n,t}.
\tag{2.2}
\]

Dividing (2.1) by `n` and using existence of stationary entropy rates yields

\[
J(t)=\lim_{n\to\infty}\frac1nD(P_{n,t}\|P_{n,0})\ge0.
\tag{2.3}
\]

No entropy derivative is interchanged with this limit.

## 3. The DPP law as one fixed occupation measurement

For every finite Hermitian contraction `0<K<I`, let `rho_K` be the gauge-invariant quasi-free fermionic density matrix with one-particle covariance `K`. Its occupation number moments satisfy

\[
\operatorname{Tr}(\rho_K\, n_{i_1}\cdots n_{i_r})
=\det K_{\{i_1,\ldots,i_r\}}.
\tag{3.1}
\]

Measuring all occupation number operators in their common occupation basis therefore produces a binary law whose inclusion moments are exactly the DPP principal minors. Möbius inversion on the Boolean lattice shows that the measurement probabilities are exactly the complete DPP probabilities. Thus the map

\[
\mathcal M:\rho_K\mapsto P_K
\]

is one fixed projective quantum measurement, independent of `K`.

By monotonicity/data processing of quantum relative entropy under measurements,

\[
D(P_A\|P_B)
\le D_{\rm q}(\rho_A\|\rho_B).
\tag{3.2}
\]

This is an inequality only. No fermionic/von-Neumann entropy is substituted for the configuration Shannon entropy.

## 4. Finite-dimensional quasi-free relative entropy

For strict finite-dimensional covariance matrices `0<A,B<I`, the gauge-invariant quasi-free relative entropy is

\[
D_{\rm q}(\rho_A\|\rho_B)
=
\operatorname{Tr}\Bigl[
A(\log A-\log B)
+(I-A)(\log(I-A)-\log(I-B))
\Bigr].
\tag{4.1}
\]

Equivalently, with

\[
\Phi(X)=\operatorname{Tr}
\{X\log X+(I-X)\log(I-X)\},
\]

(4.1) is the Bregman divergence

\[
D_{\rm q}(\rho_A\|\rho_B)
=\Phi(A)-\Phi(B)-D\Phi(B)[A-B].
\tag{4.2}
\]

Let all matrices on the segment `B+s(A-B)`, `0<=s<=1`, have spectrum in `[a,1-a]`. For the scalar function

\[
\phi(x)=x\log x+(1-x)\log(1-x),
\]

one has

\[
\phi''(x)=\frac1{x(1-x)}
\le\frac1{a(1-a)}.
\tag{4.3}
\]

The standard divided-difference formula for the Hessian of a trace spectral function gives

\[
D^2\Phi(X)[V,V]
\le\frac1{a(1-a)}\|V\|_{\rm HS}^2.
\tag{4.4}
\]

Integrating the Hessian along the segment in (4.2),

\[
\boxed{
D_{\rm q}(\rho_A\|\rho_B)
\le\frac1{2a(1-a)}\|A-B\|_{\rm HS}^2.}
\tag{4.5}
\]

For the path (1.2), take `a=delta/2`.

## 5. Toeplitz Hilbert-Schmidt density and thermodynamic passage

Apply (3.2) and (4.5) with

\[
A=K_{n,t},\qquad B=K_{n,0},
\qquad A-B=tT_{\Lambda_n}(g).
\]

Then

\[
\frac1nD(P_{n,t}\|P_{n,0})
\le
\frac{t^2}{2a(1-a)}
\frac1n\|T_{\Lambda_n}(g)\|_{\rm HS}^2.
\tag{5.1}
\]

The Toeplitz Hilbert-Schmidt identity is exact:

\[
\frac1n\|T_{\Lambda_n}(g)\|_{\rm HS}^2
=
\sum_{|j|<n}\left(1-\frac{|j|}{n}\right)|\widehat g(j)|^2
\le\sum_j|\widehat g(j)|^2
=\|g\|_2^2.
\tag{5.2}
\]

Therefore

\[
\frac1nD(P_{n,t}\|P_{n,0})
\le
\frac{t^2\|g\|_2^2}{\delta(1-\delta/2)}
\tag{5.3}
\]

for every `n`. Passing to (2.3) proves (1.3) with no derivative limit and no finite-sample extrapolation.

## 6. Matching lower bound and strict scope

The already accepted regularity-free matching argument applies directly to the full complete laws and yields (1.4). Combining it with (1.3) and exact evenness proves (1.6).

The result is genuinely outside `A_0`: any bounded half-period-odd `g` with non-absolutely summable Fourier coefficients is admitted, provided the path is kept in the strict spectral strip. For example, one may choose any real bounded half-period-odd symbol with a jump discontinuity and nonzero selected odd Fourier coefficient; its Fourier coefficients are typically `O(1/|j|)` and need not be in `ell^1`, while it is in `L^2` automatically.

This does **not** assert local concavity on an interval away from zero, `C^2` or `C^4` regularity, or a passage of the PR117 local radius by density. It supplies only the stated true central second-difference control.

## 7. Source boundaries

Primary source checks used only for the following standard external facts:

1. finite-dimensional gauge-invariant quasi-free relative entropy formula (4.1): Brunetti--Fredenhagen--Pinamonti, *Thermodynamical aspects of fermions in external electromagnetic fields*, Proposition 11 / discussion of the finite-dimensional compact formula, arXiv:2505.22413 and CMP (2025/2026 version);
2. monotonicity of quantum relative entropy under coarse-graining/measurement: Petz, *Monotonicity of quantum relative entropy revisited*, arXiv:quant-ph/0209053, tracing the standard Uhlmann/Petz monotonicity theorem.

The HMM analyticity papers Han--Marcus `math/0507235` and Tadic--Doucet `1806.09589` are **not used**. Their theorems concern hidden-Markov models satisfying model-specific positivity/analytic-continuation/filter-stability hypotheses. No finite- or continuous-state HMM realization of the present DPP is asserted.

## 8. Evidence and nonclaims

- theorem/proof: author analytic proof, pending independent review;
- machine computation: none;
- PR117 `A_0` `C^4` theorem: not a premise;
- accepted parity matching theorem: imported only for the lower bound (1.4);
- configuration entropy: always complete Shannon occupation entropy;
- quantum relative entropy: upper-bound device only;
- general real-kernel concavity, whole legal interval, arbitrary-center local concavity outside `A_0`, and novelty: unclaimed.