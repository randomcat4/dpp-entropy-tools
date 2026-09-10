# Self-contained closures for the `p>4` response proof

Status: **AUTHOR PROOF SUPPLEMENT / PENDING_REVIEW**.

This supplement removes two possible ambiguities from the main proof:

1. it proves the polynomial return bound for the BFG auxiliary chain directly from its defective renewal equation, so Proposition 2(iv) is no longer load-bearing;
2. it proves the required Banach-valued Cauchy step in `B_a`, rather than inferring norm differentiability from pointwise holomorphy.

## 1. A defective-renewal polynomial lemma

### Lemma 1.1

Let `(f_n)_{n>=1}` be nonnegative and satisfy

\[
\theta:=\sum_{n\ge1}f_n<1,
\qquad
f_n\le C_f(1+n)^{-b}
\tag{1.1}
\]

for some `b>1`. Define the renewal sequence

\[
u_0=1,
\qquad
u_n=\sum_{k=1}^nf_k u_{n-k}\quad(n\ge1).
\tag{1.2}
\]

Then

\[
\sum_{n\ge0}u_n=\frac1{1-\theta}<\infty
\tag{1.3}
\]

and there is `C_u<infinity` such that

\[
\boxed{u_n\le C_u(1+n)^{-b}.}
\tag{1.4}
\]

#### Proof

All terms are nonnegative. Put `U_N=sum_{n=0}^N u_n`. Summing (1.2) over `1<=n<=N` and retaining only the available triangular region gives

\[
U_N
=1+\sum_{k=1}^N f_k\sum_{j=0}^{N-k}u_j
\le1+\theta U_N.
\tag{1.5}
\]

Thus `U_N<=1/(1-theta)` for every `N`. Monotone convergence gives a finite `U=sum_n u_n`; now passing to the limit in the exact triangular identity yields `U=1+theta U`, proving (1.3) without subtracting infinities.

Choose `epsilon in (0,1)` so small that

\[
\rho:=\theta(1-\epsilon)^{-b}<1.
\tag{1.6}
\]

This is possible because `theta<1`. Enlarge a constant to absorb the finitely many indices with `epsilon n<1`. For all remaining `n`, split (1.2) at `k<=epsilon n`:

\[
\begin{aligned}
u_n
&=\sum_{1\le k\le\epsilon n}f_k u_{n-k}
 +\sum_{\epsilon n<k\le n}f_k u_{n-k}\\
&\le
\theta\max_{j<n}\bigl((1+j)^bu_j\bigr)
(1+(1-\epsilon)n)^{-b}
+C_f(1+\epsilon n)^{-b}\sum_{j\ge0}u_j.
\end{aligned}
\tag{1.7}
\]

Because `1+(1-epsilon)n >= (1-epsilon)(1+n)`, multiplication by `(1+n)^b` gives

\[
(1+n)^bu_n
\le \rho\max_{j<n}(1+j)^bu_j+C_0.
\tag{1.8}
\]

Induction implies

\[
\sup_n(1+n)^bu_n
\le \max\left\{\max_{n<n_0}(1+n)^bu_n,\frac{C_0}{1-\rho}\right\}<\infty.
\]

This is (1.4). QED.

### Application to the BFG chain

For the majorant

\[
\gamma_m=1-\exp[-C_b(1+m)^{-b}],
\qquad b>1,
\tag{1.9}
\]

BFG equation (5.11) gives the first-return law

\[
f_1=\gamma_0,
\qquad
f_n=\gamma_{n-1}\prod_{j=0}^{n-2}(1-\gamma_j),\quad n\ge2.
\tag{1.10}
\]

Since `sum gamma_j<infinity`,

\[
\prod_{j\ge0}(1-\gamma_j)>0.
\]

Thus the total first-return mass is

\[
\theta=P(\tau<\infty)
=1-\prod_{j\ge0}(1-\gamma_j)<1,
\tag{1.11}
\]

and `f_n=O(n^{-b})`. Lemma 1.1 therefore gives directly

\[
P(S_n=0)=u_n=O(n^{-b}).
\tag{1.12}
\]

This proves the particular content needed from BFG Proposition 2(iv) without relying on how the phrase “decreases polynomially” is formalized.

## 2. Relaxation from the coupling equations alone

Let `F in B_b`. BFG equations (5.4)--(5.5), which follow from their maximal coupling and matched-suffix variable, give

\[
\operatorname{osc}(\mathcal L_s^nF)
\le \sum_{k=0}^n\operatorname{var}_k(F)u_{n-k}.
\tag{2.1}
\]

Here `var_0(F)` is bounded by `2||F||_infty`. Both sequences

\[
(1+k)^{-b}
\quad\text{and}\quad
u_k
\]

are summable and are `O((1+k)^{-b})`. Split their convolution at `k=n/2`:

\[
\begin{aligned}
\sum_{k=0}^n(1+k)^{-b}u_{n-k}
&\le
\left(\sup_{j\ge n/2}u_j\right)
\sum_{k\le n/2}(1+k)^{-b}\\
&\quad+
\left(1+n/2\right)^{-b}
\sum_{j\le n/2}u_j\\
&\le C(1+n)^{-b}.
\end{aligned}
\tag{2.2}
\]

Consequently

\[
\boxed{
\operatorname{osc}(\mathcal L_s^nF)
\le C_b\|F\|_b(1+n)^{-b}.}
\tag{2.3}
\]

The only imported BFG facts now used for (2.3) are the ratio-coupling construction, the suffix comparison leading to (2.1), and the explicit first-return formula (1.10). The polynomial renewal estimate itself is internal.

## 3. Banach-valued Cauchy lemma

### Lemma 3.1

Let `D` be a complex disk and let `z -> F_z(x)` be holomorphic for every `x in X={0,1}^N`. Suppose that on every compact subdisk `D'`,

\[
\sup_{z\in D'}\|F_z\|_{B_a}<\infty.
\tag{3.1}
\]

Then `z -> F_z` is holomorphic as a `B_a`-valued map. In particular, on a smaller concentric disk of Cauchy radius `r`,

\[
\|\partial_z^mF_z\|_{B_a}
\le \frac{m!}{r^m}
\sup_{|w-z|=r}\|F_w\|_{B_a}.
\tag{3.2}
\]

#### Proof

Fix `z_0` and a circle `|w-z_0|=r` contained in `D`. Define pointwise Cauchy coefficients

\[
a_m(x)=\frac1{2\pi i}\int_{|w-z_0|=r}
\frac{F_w(x)}{(w-z_0)^{m+1}}\,dw.
\tag{3.3}
\]

The sup-norm estimate is standard. If two futures agree through `n`, apply (3.3) to their difference and take the supremum:

\[
\operatorname{var}_n(a_m)
\le r^{-m}\sup_{|w-z_0|=r}\operatorname{var}_n(F_w).
\tag{3.4}
\]

Hence

\[
\|a_m\|_{B_a}
\le r^{-m}\sup_{|w-z_0|=r}\|F_w\|_{B_a}.
\tag{3.5}
\]

For every `rho<r`, the series

\[
\sum_{m\ge0}a_m(z-z_0)^m
\]

therefore converges absolutely in `B_a` for `|z-z_0|<=rho`, and pointwise equals `F_z`. This proves Banach holomorphy and (3.2). QED.

### Application to the DPP conditional

The retained PR66 common complex disk gives pointwise holomorphy of

\[
\ell_z(\xi x)=\log G_z(\xi|x),
\]

uniform non-nullness, and the coordinate influence

\[
\sup_{x\stackrel{\ne j}=y}
|\ell_z(\xi x)-\ell_z(\xi y)|
\le C(1+j)^{-2q}
\tag{3.6}
\]

on each smaller closed disk. Telescoping coordinates beyond `n` gives

\[
\operatorname{var}_n(\ell_z)
\le C(1+n)^{1-2q}
=C(1+n)^{-a},
\qquad a=2q-1.
\tag{3.7}
\]

Uniform non-nullness also bounds `||ell_z||_infty`. Thus (3.1) holds with `F_z=ell_z`. Lemma 3.1 proves `B_a`-valued holomorphy and gives the same variation exponent for derivatives through every fixed finite order. In particular the derivatives through order four required for the even factorization `s=z^2` are controlled without a hidden pointwise-to-norm step.

## 4. Consequence for the theorem threshold

The one-power Poisson estimate in the main proof uses only (2.3) and the first-generated-disagreement hazard at the full exponent `a`. The response scale remains

\[
B_a\xrightarrow{R}B_{a-1}\xrightarrow{R}B_{a-2}.
\]

Lemma 3.1 supplies the `C^2(B_a)` dependence in `s`; Lemma 1.1 and (2.3) supply the uniform summability used by both Poisson inverses. Therefore the threshold remains

\[
a>2\iff p>4.
\]

No statement in this supplement changes the post-upload boundary correction: the valid finite approximation is the time-correlation cutoff in `c4_response_p4_boundary_correction.md`, not the withdrawn raw frozen-memory stationary-response rate.