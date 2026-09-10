# Exact DPP score-moment obstruction for the present response route

Status: **PROVED AS AN AUTHOR METHOD-OBSTRUCTION LEMMA / PENDING REVIEW**.

This is not an entropy counterexample. In fact the constant-center line has
stronger entropy concavity by another argument. The purpose of the calculation
is narrower: it shows that the `p=1` threshold of the present **generic
moment-space second-response route** cannot be lowered merely by improving an
upper-bound constant. Within legal DPPs, the true center score can fail the
required second variation moment for every `p<1`.

## 1. Constant center and exact score

Fix `0<a<1` and let

\[
c(\theta)=a.
\]

Let `g` be a real half-period-odd symbol with zero mean. Then

\[
K_t=aI+tT(g).
\]

At `t=0` the configuration process is i.i.d. Bernoulli(`a`). For a finite
future word `x` on `F_R={1,...,R}`, the complete-event matrix at the center is
diagonal:

\[
M_{R,x}(0)=\operatorname{diag}(m_j(x_j)),
\]

where

\[
m_j(1)=a,
\qquad m_j(0)=a-1.
\tag{1.1}
\]

Put

\[
d(1)=a^{-1},
\qquad d(0)=-(1-a)^{-1}.
\tag{1.2}
\]

The occupied-origin conditional is

\[
q_{R,t}(x)=a-u_tM_{R,x}(t)^{-1}v_t.
\]

Since `u_t` and `v_t` are linear in `t`, differentiation at the center gives,
with `s=t^2`,

\[
\left.\partial_s q_{R,s}(x)\right|_{s=0}
=-\sum_{j=1}^R|\widehat g(j)|^2d(x_j).
\tag{1.3}
\]

The sum converges uniformly as `R->infinity` because `g in A_0` implies
`sum_j|g_hat(j)|^2<infinity`. Thus for the full future

\[
Q(x):=\left.\partial_sq_s(x)\right|_{s=0}
=-\sum_{j\ge1}|\widehat g(j)|^2d(x_j).
\tag{1.4}
\]

The conditional score `U_0=partial_s log G_s|_0` is

\[
U_0(1x)=\frac{Q(x)}a,
\qquad
U_0(0x)=-\frac{Q(x)}{1-a}.
\tag{1.5}
\]

Every term is a complete-event conditional contribution. Under the center law,
`E[d(X_j)]=0`, which is the normalization cancellation.

## 2. Exact coordinate influence and moment equivalence

If futures `x,y` differ only at coordinate `j`, then (1.4) gives

\[
|Q(x)-Q(y)|
=\frac{|\widehat g(j)|^2}{a(1-a)}.
\tag{2.1}
\]

Choosing the emitted state that maximizes the prefactor in (1.5), there are
constants `0<C_-(a)<=C_+(a)<infinity` such that

\[
C_-(a)|\widehat g(j)|^2
\le
\sup_{x\stackrel{\ne j}=y,\xi}
|U_0(\xi x)-U_0(\xi y)|
\le
C_+(a)|\widehat g(j)|^2.
\tag{2.2}
\]

Because all coefficients in the tail variation can be aligned by choosing the
future bits independently, one in fact has

\[
\operatorname{var}_nU_0
\asymp_a\sum_{j>n}|\widehat g(j)|^2.
\tag{2.3}
\]

Tonelli therefore gives the exact equivalences

\[
U_0\in\mathcal V_0
\quad\Longleftrightarrow\quad
\sum_{j\ge1}j|\widehat g(j)|^2<\infty,
\tag{2.4}
\]

\[
U_0\in\mathcal V_1
\quad\Longleftrightarrow\quad
\sum_{j\ge1}j^2|\widehat g(j)|^2<\infty.
\tag{2.5}
\]

Thus the variation moments of the exact DPP score are governed by the square
of the Fourier tail, not merely bounded above by it.

## 3. Sparse legal examples for every `p<1`

Fix `0<=p<1`. Choose odd integers

\[
N_m=2^{m^2}+1
\]

and define a real half-period-odd symbol by

\[
\widehat g(\pm N_m)=\varepsilon m^{-2}N_m^{-p},
\]

with all other coefficients zero. Then

\[
\sum_n(1+|n|)^p|\widehat g(n)|
\le C\varepsilon\sum_m m^{-2}<\infty,
\]

so `g in A_p`. Taking `epsilon` sufficiently small makes `a+t g` legal on a
nonempty real interval.

But

\[
\sum_jj^2|\widehat g(j)|^2
\ge
\varepsilon^2\sum_m m^{-4}N_m^{2-2p}=\infty.
\tag{3.1}
\]

By (2.5), the exact center score is not in `V_1`. Hence the generic response
chain

```text
score in V_1 -> first Poisson inverse in V_0 -> second inverse in C
```

cannot cover every `A_p` symbol when `p<1` without an additional
entropy-specific cancellation or a different function space.

For `p<1/2`, the same example also has

\[
\sum_jj|\widehat g(j)|^2
\ge
\varepsilon^2\sum_m m^{-4}N_m^{1-2p}=\infty,
\tag{3.2}
\]

so the true score is not even in `V_0`, the input space of the general
one-response Fisher proof.

## 4. Scope

This is a DPP-internal response-regularity obstruction: it computes the true
complete-event conditional score and its coordinate influences exactly. It is
not an abstract `g`-chain example.

It is also not a DPP entropy counterexample. The constant-center entropy line
has separate strong concavity results. The lemma proves only that extending the
**current moment-space mechanism** below `p=1` requires a new cancellation,
not merely a sharper generic inequality.
