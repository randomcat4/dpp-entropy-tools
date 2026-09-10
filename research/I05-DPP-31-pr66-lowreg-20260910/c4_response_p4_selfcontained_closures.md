# Self-contained closures for the `p>4` response proof

Status: **AUTHOR PROOF SUPPLEMENT / PENDING_REVIEW**.

This supplement closes two possible ambiguities in the main proof:

1. the polynomial return bound for the BFG auxiliary chain is proved directly from its defective renewal equation, so BFG Proposition 2(iv) is only a cross-check;
2. the required Cauchy argument is carried out in the polynomial variation Banach space itself.

## 1. Defective-renewal polynomial lemma

### Lemma 1.1

Let `(f_n)_{n>=1}` be nonnegative and satisfy

\[
\theta:=\sum_{n\ge1}f_n<1,
\qquad
f_n\le C_f(1+n)^{-b}
\tag{1.1}
\]

for some `b>1`. Define

\[
u_0:=1,
\qquad
u_n:=\sum_{k=1}^n f_k u_{n-k}\quad(n\ge1).
\tag{1.2}
\]

The plain-text form of (1.2), avoiding any font ambiguity, is

```text
u[0] = 1,
u[n] = sum_{k=1}^n f[k] u[n-k].
```

Throughout this file the renewal sequence is denoted by the Latin letter `u`; the displayed TeX should be read as `u_0,u_n`, not the Greek letter nu. Then

\[
\sum_{n\ge0}u_n=\frac1{1-\theta}<\infty
\tag{1.3}
\]

and

\[
\boxed{u_n\le C_u(1+n)^{-b}}
\tag{1.4}
\]

for a finite constant `C_u`.

#### Proof

Let `U_N=sum_{n=0}^N u_n`. Summing the renewal equation over the finite triangular region gives

\[
U_N
=1+\sum_{k=1}^N f_k\sum_{j=0}^{N-k}u_j
\le1+\theta U_N.
\tag{1.5}
\]

Hence `U_N<=1/(1-theta)`. Monotone convergence gives a finite `U=sum_n u_n`; passage to the limit in the exact triangular identity yields `U=1+theta U`, proving (1.3) without subtracting divergent quantities.

Choose `epsilon in (0,1)` so small that

\[
\rho:=\theta(1-\epsilon)^{-b}<1.
\tag{1.6}
\]

For all sufficiently large `n`, split the renewal sum into `k<=epsilon n` and `k>epsilon n`. With

\[
M_{n-1}:=\max_{0\le j<n}(1+j)^b u_j,
\]

we obtain

\[
u_n
\le \theta M_{n-1}(1+(1-\epsilon)n)^{-b}
+C_f(1+\epsilon n)^{-b}\sum_{j\ge0}u_j.
\tag{1.7}
\]

In plain text, the left side of (1.7) is `u[n]`. Multiplication by `(1+n)^b` gives

\[
(1+n)^bu_n\le\rho M_{n-1}+C_0.
\tag{1.8}
\]

After enlarging the bound over finitely many initial indices, induction gives

\[
\sup_n(1+n)^bu_n
\le\max\left\{M_{n_0},\frac{C_0}{1-\rho}\right\}<\infty.
\]

This proves (1.4). QED.

### Application to the BFG auxiliary chain

For

\[
\gamma_m=1-\exp[-C_b(1+m)^{-b}],\qquad b>1,
\tag{1.9}
\]

BFG equation (5.11) gives the first positive return law of the age chain:

\[
f_1=\gamma_0,
\qquad
f_n=\gamma_{n-1}\prod_{j=0}^{n-2}(1-\gamma_j),\quad n\ge2.
\tag{1.10}
\]

Since `sum_m gamma_m<infinity`,

\[
\prod_{m\ge0}(1-\gamma_m)>0.
\]

Therefore

\[
\theta=P(\tau<\infty)
=1-\prod_{m\ge0}(1-\gamma_m)<1,
\qquad
f_n=O(n^{-b}).
\tag{1.11}
\]

The Markov renewal identity is

```text
u[0] = 1,
u[n] = sum_{k=1}^n f[k] u[n-k] = P(S_n=0).
```

Again `u[n]` denotes the Latin renewal sequence. Lemma 1.1 gives

\[
\boxed{P(S_n=0)=u_n=O(n^{-b}).}
\tag{1.12}
\]

Thus no interpretation of the phrase “decreases polynomially” in BFG Proposition 2(iv) is load-bearing.

## 2. Relaxation for every `B_b` observable

Let `F in B_b`. BFG's coupling identity (their equation (5.4), before inserting the printed `V_phi` comparison) gives

\[
|L_s^nF(x)-L_s^nF(y)|
\le\sum_{k\ge0}\operatorname{var}_k(F)P(T_n^{x,y}=k).
\tag{2.1}
\]

Variations are decreasing. Repeating the elementary split and suffix comparison in BFG equation (5.5), now with `var_k(F)` itself, yields

\[
|L_s^nF(x)-L_s^nF(y)|
\le\sum_{k=0}^n\operatorname{var}_k(F)u_{n-k}.
\tag{2.2}
\]

This step does not identify `B_b` with BFG's printed space `V_phi`.

Both sequences `(1+k)^{-b}` and `u_k` are summable and are `O((1+k)^{-b})`. Splitting the convolution at `k=n/2` gives

\[
\sum_{k=0}^n(1+k)^{-b}u_{n-k}\le C_b(1+n)^{-b}.
\tag{2.3}
\]

Consequently

\[
\boxed{
\operatorname{osc}(L_s^nF)
\le C_b\|F\|_{B_b}(1+n)^{-b}.}
\tag{2.4}
\]

The imported BFG content is limited to the ratio coupling, the matched-suffix comparison producing (2.1)--(2.2), and the explicit first-return formula (1.10). The polynomial renewal estimate is internal.

## 3. Banach-valued Cauchy lemma

### Lemma 3.1

Let `D` be a complex disk and suppose `z -> F_z(x)` is holomorphic for every future `x`. If, on each compact subdisk `D'`,

\[
\sup_{z\in D'}\|F_z\|_{B_a}<\infty,
\tag{3.1}
\]

then `z -> F_z` is holomorphic as a `B_a`-valued map. On every smaller Cauchy circle of radius `r`,

\[
\|\partial_z^mF_z\|_{B_a}
\le \frac{m!}{r^m}
\sup_{|w-z|=r}\|F_w\|_{B_a}.
\tag{3.2}
\]

#### Proof

For a circle about `z_0`, define the pointwise Cauchy coefficients

\[
a_m(x)=\frac1{2\pi i}\int_{|w-z_0|=r}
\frac{F_w(x)}{(w-z_0)^{m+1}}\,dw.
\tag{3.3}
\]

The usual sup bound holds. If two futures agree through `n`, applying (3.3) to their difference gives

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

The Taylor series therefore converges absolutely in `B_a` on every smaller disk and agrees pointwise with `F_z`. This proves Banach holomorphy and (3.2). QED.

### Application to the DPP conditional

The retained PR66 complex disk gives pointwise holomorphy, uniform non-nullness, and

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

Uniform non-nullness bounds `||ell_z||_infty`; thus (3.1) holds. Lemma 3.1 proves `B_a`-valued holomorphy and preserves the memory exponent through every fixed parameter derivative, in particular through order four.

## 4. Threshold consequence

The one-power Poisson estimate uses only (2.4) and the first-generated-disagreement hazard at the full exponent `a`. The response scale is

\[
B_a\xrightarrow{R}B_{a-1}\xrightarrow{R}B_{a-2}.
\]

The weighted inverse construction permits a `q` with

\[
q>3/2,
\qquad
2q+1<p
\]

if and only if `p>4`. Therefore the finite-response route closes at the original threshold `p>4`.

This supplement does not alter the boundary correction: the valid finite approximation is the time-correlation cutoff in `c4_response_p4_boundary_correction.md`, not the withdrawn frozen-memory stationary-response rate.