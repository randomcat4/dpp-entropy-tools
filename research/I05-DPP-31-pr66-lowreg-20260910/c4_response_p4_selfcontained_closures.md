# Self-contained closures for the `p>4` response proof

Status: **AUTHOR PROOF SUPPLEMENT / PENDING_REVIEW**.

This supplement proves the polynomial return estimate internally and carries out the parameter Cauchy argument in the polynomial variation Banach space.

## 1. Defective-renewal polynomial lemma

### Lemma 1.1

Let `(f_n)_{n>=1}` be nonnegative and suppose

\[
\theta:=\sum_{n\ge1}f_n<1,
\qquad
f_n\le C_f(1+n)^{-b},
\qquad b>1.
\tag{1.1}
\]

Define the Latin-letter sequence `(u_n)_{n>=0}` by

\[
u_0=1,
\qquad
u_n=\sum_{k=1}^n f_k u_{n-k}\quad(n\ge1).
\tag{1.2}
\]

To remove any rendering ambiguity, equation (1.2) is exactly

```text
u_0 = 1,
u_n = sum_{k=1}^n f_k u_{n-k}.
```

Then

\[
\sum_{n\ge0}u_n=\frac1{1-\theta}<\infty,
\qquad
u_n\le C_u(1+n)^{-b}.
\tag{1.3}
\]

#### Proof

Let `U_N=sum_{n=0}^N u_n`. Summing the recurrence over the finite triangular region gives

\[
U_N
=1+\sum_{k=1}^N f_k\sum_{j=0}^{N-k}u_j
\le1+\theta U_N.
\tag{1.4}
\]

Thus `U_N<=1/(1-theta)`. Monotone convergence gives a finite `U=sum_n u_n`; passage to the limit in the exact triangular identity yields `U=1+theta U`.

Choose `epsilon in (0,1)` so small that

\[
\rho:=\theta(1-\epsilon)^{-b}<1.
\tag{1.5}
\]

For large `n`, split the recurrence at `k<=epsilon n`. With

\[
M_{n-1}:=\max_{0\le j<n}(1+j)^bu_j,
\]

we have

\[
u_n
\le \theta M_{n-1}(1+(1-\epsilon)n)^{-b}
+C_f(1+\epsilon n)^{-b}U.
\tag{1.6}
\]

Equivalently, the left side of (1.6) is the Latin variable `u_n`. Multiplication by `(1+n)^b` gives

\[
(1+n)^bu_n\le\rho M_{n-1}+C_0.
\tag{1.7}
\]

After absorbing finitely many initial indices, induction gives

\[
\sup_n(1+n)^bu_n
\le\max\left\{M_{n_0},\frac{C_0}{1-\rho}\right\}<\infty.
\]

This proves (1.3). QED.

### Application to the BFG age chain

For

\[
\gamma_m=1-\exp[-C_b(1+m)^{-b}],\qquad b>1,
\tag{1.8}
\]

BFG equation (5.11) gives

\[
f_1=\gamma_0,
\qquad
f_n=\gamma_{n-1}\prod_{j=0}^{n-2}(1-\gamma_j),\quad n\ge2.
\tag{1.9}
\]

Since `sum_m gamma_m<infinity`, the infinite product is positive. Hence

\[
\theta=P(\tau<\infty)
=1-\prod_{m\ge0}(1-\gamma_m)<1,
\qquad
f_n=O(n^{-b}).
\tag{1.10}
\]

The Markov renewal equation is (1.2) with

\[
u_n=P(S_n=0).
\]

In plain text: `u_n=P(S_n=0)`. Lemma 1.1 therefore gives

\[
P(S_n=0)=u_n=O(n^{-b}).
\tag{1.11}
\]

BFG Proposition 2(iv) is now only a cross-check.

## 2. Relaxation for every `B_b` observable

Let `F in B_b`. BFG equation (5.4), before its specialization to `V_phi`, gives

\[
|L_s^nF(x)-L_s^nF(y)|
\le\sum_{k\ge0}\operatorname{var}_k(F)P(T_n^{x,y}=k).
\tag{2.1}
\]

Because variations decrease, the split and suffix comparison used in BFG equation (5.5) gives directly

\[
|L_s^nF(x)-L_s^nF(y)|
\le\sum_{k=0}^n\operatorname{var}_k(F)u_{n-k}.
\tag{2.2}
\]

No identification of `B_b` with `V_phi` is made. Both `(1+k)^{-b}` and `u_k` are summable and have order `O((1+k)^{-b})`; splitting their convolution at `n/2` yields

\[
\boxed{
\operatorname{osc}(L_s^nF)
\le C_b\|F\|_{B_b}(1+n)^{-b}.}
\tag{2.3}
\]

The only imported BFG ingredients are the ratio coupling, the matched-suffix comparison behind (2.1)--(2.2), and the explicit first-return formula (1.9).

## 3. Banach-valued Cauchy lemma

### Lemma 3.1

Let `D` be a complex disk. Suppose `z -> F_z(x)` is holomorphic for every future `x` and, on every compact subdisk `D'`,

\[
\sup_{z\in D'}\|F_z\|_{B_a}<\infty.
\tag{3.1}
\]

Then `z -> F_z` is holomorphic as a `B_a`-valued map. On every smaller Cauchy circle of radius `r`,

\[
\|\partial_z^mF_z\|_{B_a}
\le \frac{m!}{r^m}
\sup_{|w-z|=r}\|F_w\|_{B_a}.
\tag{3.2}
\]

#### Proof

For a circle about `z_0`, define

\[
a_m(x)=\frac1{2\pi i}\int_{|w-z_0|=r}
\frac{F_w(x)}{(w-z_0)^{m+1}}\,dw.
\tag{3.3}
\]

If two futures agree through `n`, apply (3.3) to their difference:

\[
\operatorname{var}_n(a_m)
\le r^{-m}\sup_{|w-z_0|=r}\operatorname{var}_n(F_w).
\tag{3.4}
\]

Together with the usual sup bound this gives

\[
\|a_m\|_{B_a}
\le r^{-m}\sup_{|w-z_0|=r}\|F_w\|_{B_a}.
\tag{3.5}
\]

The Taylor series converges absolutely in `B_a` on every smaller disk and agrees pointwise with `F_z`. QED.

### DPP application

The retained PR66 disk gives pointwise holomorphy, uniform non-nullness, and

\[
\sup_{x\stackrel{\ne j}=y}
|\ell_z(\xi x)-\ell_z(\xi y)|
\le C(1+j)^{-2q}.
\tag{3.6}
\]

Telescoping beyond coordinate `n` gives

\[
\operatorname{var}_n(\ell_z)
\le C(1+n)^{1-2q}
=C(1+n)^{-a},
\qquad a=2q-1.
\tag{3.7}
\]

Uniform non-nullness bounds `||ell_z||_infty`, so Lemma 3.1 applies. Parameter derivatives through every fixed order, in particular orders zero through four, retain the same memory exponent.

## 4. Threshold consequence

The response scale is

\[
B_a\xrightarrow{R}B_{a-1}\xrightarrow{R}B_{a-2}.
\]

The weighted inverse step permits a `q` satisfying

\[
q>3/2,
\qquad
2q+1<p
\]

if and only if `p>4`. Thus the finite-response route closes at the original threshold `p>4`.

The valid finite approximation remains the time-correlation cutoff in `c4_response_p4_boundary_correction.md`, not the withdrawn frozen-memory stationary-response rate.