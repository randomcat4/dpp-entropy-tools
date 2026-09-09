# Frozen statement: polynomial Fourier class

## Definitions

Let `\mathbb T=\mathbb R/\mathbb Z`, with Fourier convention

\[
\widehat u(m)=\int_{\mathbb T}u(\theta)e^{-2\pi i m\theta}\,d\theta.
\]

For `p>0`, define the polynomially weighted Wiener class

\[
\mathcal A_p
:=
\left\{u:\mathbb T\to\mathbb C:
\|u\|_{\mathcal A_p}:=
\sum_{m\in\mathbb Z}(1+|m|)^p|\widehat u(m)|<\infty
\right\}.
\]

For a real measurable symbol `f:\mathbb T\to[0,1]`, let

\[
K_f(i,j)=\int_{\mathbb T}f(\theta)e^{2\pi i(i-j)\theta}\,d\theta
=\widehat f(j-i),
\]

and let `\mathbf P_f` be the stationary determinantal process on `\mathbb Z` with this kernel. Its configuration Shannon entropy rate is

\[
h(f)=\lim_{n\to\infty}\frac1n
H_{\mathbf P_f}(X_1,\ldots,X_n).
\]

The complete event probabilities are always understood as

\[
\mathbf P_f(X_I=x)
=(-1)^{|Z_x|}\det\bigl(K_f|_I-I_{Z_x}\bigr),
\qquad Z_x=\{i\in I:x_i=0\},
\]

not as inclusion probabilities `\det K_T`.

## Theorem

Fix `p>4`. Let `c,g\in\mathcal A_p` be real-valued and satisfy, almost everywhere,

\[
c(\theta+\tfrac12)=c(\theta),
\qquad
 g(\theta+\tfrac12)=-g(\theta).
\]

Assume that for some `\delta>0`,

\[
\delta\le c(\theta)\le1-\delta
\quad\text{a.e.},
\]

and assume `g\not\equiv0`. Put `\mu=\widehat c(0)`. Then every nonzero Fourier coefficient of `g` occurs at an odd index. Choose any odd `k` such that `\widehat g(k)\ne0`, and set

\[
C_k:=\frac{|\widehat g(k)|^4}{4\mu^2(1-\mu^2)},
\qquad
\alpha_k:=\frac{C_k}{2}
=\frac{|\widehat g(k)|^4}{8\mu^2(1-\mu^2)}.
\]

There exists `\varepsilon>0` such that

1. `0\le c+t g\le1` almost everywhere for every real `|t|\le\varepsilon`;
2. the true stationary configuration entropy rate is real analytic in `t` on `(-\varepsilon,\varepsilon)`;
3. the function

\[
t\longmapsto h(c+t g)+\alpha_k t^4
\]

is concave on `[-\varepsilon,\varepsilon]`.

No hypothesis `\mu=1/2`, no smallness hypothesis on `\|g\|`, and no evenness of the real symbols is imposed. In particular, non-even real symbols and the resulting complex Hermitian Toeplitz kernels are covered.

The interval is existential and nonempty. It depends on `p,\delta,c,g,k`; no uniform radius over an unbounded class is claimed.

## Strict extension beyond exponential weighted Wiener classes

Every exponentially weighted Wiener class is contained in every `\mathcal A_p`, since exponential decay dominates polynomial weights. The containment is strict.

For a concrete power-law example, fix `p>4` and put

\[
\begin{aligned}
c_p(\theta)
&=\frac12+
\frac1{16}\sum_{m\ge1}m^{-(p+2)}\cos(4\pi m\theta),\\
g_p(\theta)
&=\frac1{32}\sum_{m\ge0}(2m+1)^{-(p+2)}
\cos\bigl(2\pi(2m+1)\theta\bigr).
\end{aligned}
\]

Then `c_p,g_p\in\mathcal A_p`, the required half-period symmetries hold, and

\[
\frac38<c_p<\frac58,
\qquad
\|g_p\|_\infty<\frac1{16}.
\]

Hence `c_p+t g_p` is legal at least for `|t|\le1`. Moreover
`\widehat g_p(1)=1/64\ne0`. Neither `c_p-1/2` nor `g_p` lies in any exponentially weighted Wiener class, because their infinitely many nonzero Fourier coefficients decay only as a power. Thus the theorem covers a genuine slow-decay family not contained in the accepted PR53 regularity class.

The same construction can be made real and non-even by replacing selected cosine coefficient pairs by conjugate Fourier pairs with nonzero phases, while preserving even/odd index support.

## Status label

**PROVED (author proof; independent review pending).**
