# Explicit `A_0` family lying in no `A_p`, `p>0`

Status: **AUTHOR VERIFICATION / PENDING REVIEW**.

This file gives a concrete nonconstant, non-exponentially-local family to which the small-Wiener theorem applies but no positive polynomial weighted-Wiener theorem applies.

## 1. A summable tail with no positive moment

For `n>=1`, put

\[
w_n=\frac1{n(\log(n+2))^2}.
\tag{1.1}
\]

The series `sum_n w_n` converges by the integral test. For every `p>0`, however,

\[
\sum_{n\ge1}n^p w_n
=\sum_{n\ge1}
\frac{n^{p-1}}{(\log(n+2))^2}
=\infty.
\tag{1.2}
\]

Indeed, for sufficiently large `n`, `(log(n+2))^2<=n^{p/2}`, so the summand is at least `n^{p/2-1}`, whose series diverges.

## 2. Center and direction

Define the uniformly convergent real series

\[
C(\theta)=\sum_{n\ge1}w_n\cos(4\pi n\theta),
\tag{2.1}
\]

and

\[
G(\theta)=\sum_{n\ge0}w_{2n+1}
\cos(2\pi(2n+1)\theta).
\tag{2.2}
\]

Choose `eta>0` so small that

\[
\eta\sum_{n\ge1}w_n<\frac16.
\tag{2.3}
\]

Put

\[
c(\theta)=\frac13+\eta C(\theta),
\qquad
g(\theta)=\eta G(\theta).
\tag{2.4}
\]

Then `c,g in A_0`, `g` is nonzero, and

\[
c(\theta+1/2)=c(\theta),
\qquad
g(\theta+1/2)=-g(\theta).
\tag{2.5}
\]

The center is nonconstant and has mean

\[
\mu=\widehat c(0)=1/3.
\tag{2.6}
\]

Its off-diagonal Wiener norm is

\[
r_c
=\sum_{m\ne0}|\widehat c(m)|
=\eta\sum_{n\ge1}w_n
<1/6<1/3
=\min\{\mu,1-\mu\}.
\tag{2.7}
\]

Thus the small-Wiener hypothesis holds. It also gives the explicit pointwise margin

\[
1/6<c(\theta)<1/2.
\tag{2.8}
\]

## 3. Failure of every positive `A_p` condition

Along the nonzero even Fourier subsequence of `c`, and the nonzero odd subsequence of `g`, the coefficient magnitudes are fixed positive multiples of `w_n`. Therefore, for every `p>0`,

\[
\sum_m(1+|m|)^p|\widehat c(m)|=\infty,
\qquad
\sum_m(1+|m|)^p|\widehat g(m)|=\infty.
\tag{3.1}
\]

Hence neither symbol belongs to any polynomially weighted Wiener class `A_p` with positive exponent. Their logarithmic power-law tails also exclude every exponentially weighted Fourier class.

## 4. Separation from earlier accepted scopes

This pair is not covered by the earlier repository theorems for the following exact reasons.

1. The center is nonconstant, so the constant-center theorem does not apply.
2. Its mean is `1/3`, not `1/2`, so the accepted PR39 small-Wiener theorem does not apply.
3. There is no exponential Fourier decay, so the accepted PR53 and compact-tube exponential theorems do not apply.
4. The pair lies in no positive `A_p`, so PR82's `p>4` theorem and the separate `p>=1` author successor do not apply.
5. The pair is also outside the `H^1_F` successor: since

   \[
   \sum_n n^2w_n^2
   =\sum_n\frac1{(\log(n+2))^4}=\infty,
   \]

   it has no Fourier `H^1` regularity.

This is a scope separation, not a claim that any earlier theorem is false outside its stated class.

## 5. Entropy conclusion

Every odd `k` with `\widehat g(k)\ne0` is allowed. For each such `k`, the small-Wiener theorem gives an `epsilon>0` such that

\[
t\longmapsto h(c+t g)
+\frac{|\widehat g(k)|^4}
{8(1/3)^2(1-(1/3)^2)}t^4
\tag{5.1}
\]

is concave on `[-epsilon,epsilon]` and strictly curved away from the center.

This is a true stationary complete-configuration entropy-rate result for symbols with no positive weighted Fourier moment. It is not a finite numerical sample and not a counterexample to any entropy conjecture.