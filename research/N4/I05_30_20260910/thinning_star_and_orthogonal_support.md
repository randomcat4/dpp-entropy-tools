# Independent thinning gives a strict entropy star inequality

Status: **PROVED (author proof after the edge checkpoint), PENDING_EXTERNAL_REVIEW**. The result is finite and classical-probabilistic; it is then specialized to the complete DPP law. It does not settle overlapping moving rank-two supports, and no novelty or priority claim is made.

## 1. A theorem for arbitrary random subsets

Let `X` be an arbitrary random subset of `[n]`. Independently of `X`, retain each coordinate with probability `theta`, where `0<theta<1`; write `R` for the random retention set and

\[
Y=X\cap R.
\]

**Theorem 1 (strict thinning-star inequality).**

\[
H(Y)\ge \theta H(X). \tag{1}
\]

If `P(X is nonempty)>0`, the inequality is strict.

**Proof.** Condition on the complete retention pattern. Given `R`, the nonconstant part of `Y` is exactly the coordinate restriction `X_R`, so

\[
H(Y\mid R)=\mathbb E_R H(X_R). \tag{2}
\]

Fix the physical coordinate order `1,...,n`. For every deterministic set `R`, the ordinary entropy chain rule gives

\[
H(X_R)=\sum_{i\in R}H(X_i\mid X_{R\cap\{1,\ldots,i-1\}}).
\]

Removing conditioning variables can only increase conditional entropy. Therefore

\[
H(X_R)\ge
\sum_{i\in R}H(X_i\mid X_1,\ldots,X_{i-1}). \tag{3}
\]

Taking expectation over the independent Bernoulli retention indicators gives

\[
\mathbb E_RH(X_R)
\ge\theta\sum_iH(X_i\mid X_1,\ldots,X_{i-1})
=\theta H(X). \tag{4}
\]

Finally, conditioning cannot increase entropy, so
`H(Y)>=H(Y|R)`. This proves (1), with no independence or negative-dependence assumption on `X`.

For strictness, choose `i` with `P(X_i=1)>0`. Then

\[
P(Y_i=1,R_i=1)=\theta P(X_i=1)
\ne\theta^2P(X_i=1)=P(Y_i=1)P(R_i=1).
\]

Thus `Y` and `R` are not independent, so
`H(Y)>H(Y|R)`. Combining this strict first step with (4) completes the proof. Notice that no lower bound on rare event probabilities is needed. QED.

The proof also records the exact nonnegative decomposition

\[
H(Y)-\theta H(X)
=I(Y;R)+
\mathbb E_R\sum_{i\in R}
 I\bigl(X_i;X_{\{1,\ldots,i-1\}\setminus R}
       \mid X_{R\cap\{1,\ldots,i-1\}}\bigr). \tag{5}
\]

This makes clear where strictness comes from and why the result is not a spectral-entropy statement.

## 2. DPP specialization in the original coordinates

Let `K` be a finite legal DPP kernel and let `X` have its complete event law. The independently thinned set `Y` is the DPP with kernel `theta K`. Indeed, for every coordinate set `T`,

\[
P(T\subseteq Y)
=\theta^{|T|}P(T\subseteq X)
=\theta^{|T|}\det K_T
=\det(\theta K)_T. \tag{6}
\]

Finite Möbius inversion uniquely determines all complete events from these inclusion probabilities. Thus Theorem 1 yields

\[
\boxed{H(\theta K)\ge\theta H(K),} \tag{7}
\]

strictly when `K` is nonzero. For a positive semidefinite kernel, `K!=0` implies some diagonal inclusion probability is positive, hence the strictness condition is exactly the expected one.

Taking complements gives an equally exact high-occupation version. Since the complement of a DPP with kernel `K` has kernel `I-K` and complementing every bit preserves Shannon entropy,

\[
H((1-\theta)I+\theta K)
=H(\theta(I-K))
\ge\theta H(I-K)=\theta H(K), \tag{8}
\]

strictly unless `K=I`.

Equations (7)--(8) are statements about the complete observation-coordinate law. They do not replace it by the Bernoulli eigenvalue count or by von Neumann entropy.

## 3. Orthogonal coordinate-support endpoint exclusion

**Theorem 2.** Partition the actual observation coordinates into disjoint sets `C,L,R`. Let `K_C,A,B` be legal kernels on those coordinate blocks and define

\[
K_-=K_C\oplus A\oplus0_R,
\qquad
K_+=K_C\oplus0_L\oplus B. \tag{9}
\]

Then their genuine arithmetic midpoint is

\[
K_0=K_C\oplus\frac12A\oplus\frac12B,
\]

and

\[
H(K_0)-\frac{H(K_-)+H(K_+)}2
=\left[H(A/2)-\frac12H(A)\right]
 +\left[H(B/2)-\frac12H(B)\right]\ge0. \tag{10}
\]

The inequality is strict unless `A=B=0`.

**Proof.** A block-diagonal DPP on actual coordinate blocks is the independent union of the block DPPs: its complete generating determinant factors. Hence configuration entropy is additive across the displayed blocks. The common `K_C` entropy cancels from the Jensen difference, and (10) follows from (7) with `theta=1/2`. Strictness follows from Theorem 1. QED.

More generally, at any fixed interpolation weight `0<t<1`,

\[
H\bigl(K_C\oplus(1-t)A\oplus tB\bigr)
>(1-t)H(K_C\oplus A)+tH(K_C\oplus B) \tag{11}
\]

whenever at least one moving block is nonzero. This is a direct weighted Jensen comparison for the true affine kernel combination. It does not claim that the scalar function `theta -> H(theta K)` is concave between arbitrary positive values.

Theorem 2 covers, in every dimension and every rank, endpoint ranges supported on disjoint **actual coordinate blocks**, with an optional common independent block. In particular it excludes all rank-two endpoint pairs with zero coordinate-support intersection after a common coordinate permutation. It does not cover two geometrically orthogonal spectral ranges that are dense in the same observation coordinates; an observation-basis rotation is not permitted.

## 4. Relation to the two new fixed-family edges

At the `t1=t2=1` corner of the canonical family, the two endpoint supports are disjoint coordinate blocks, so Theorem 2 gives the sign without any polynomial certificate. The full `t2=1` edge proved in `fresh_recheck_and_edge_extension.md` is strictly larger: except at that corner its two ranges are not supported on disjoint coordinate blocks, and the rank-four midpoint proof needs the complete sixteen-event Fisher/Bernstein identity.

Likewise, the full `t2=0` edge has a shared physical coordinate and correlated interactions through it; Theorem 2 does not imply that result. Thus the thinning route is structurally independent rather than a renaming of either edge proof.

## 5. Source and scope audit

The only DPP input needed is the defining inclusion identity and finite Möbius inversion; equation (6) proves the thinning closure directly. HKPV, *Determinantal Processes and Independence* (arXiv:math/0503110), is background for finite DPP representations but is not used as an entropy theorem. The entropy proof is the elementary chain-rule argument above. A repository code search before adding this file found no existing theorem under `independent thinning entropy`, `thinning DPP entropy`, or `H(lambda K)`; that search is not a literature novelty certificate.

No computation is required for Theorems 1--2. Their correctness still requires external review before acceptance. The unrestricted moving-rank-two problem, dense observation-coordinate orthogonal ranges, and interior of the canonical two-angle square remain INCOMPLETE.
