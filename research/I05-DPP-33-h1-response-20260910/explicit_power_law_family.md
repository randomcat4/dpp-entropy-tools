# Explicit non-`A_1` power-law family

Status: **AUTHOR VERIFICATION / PENDING REVIEW**.

This file verifies that the `H^1_F` theorem is not merely a reformulation of the weighted-Wiener `A_p, p>=1` theorem or of an already accepted constant-center/mean-one-half special case.

## 1. Definition

Let

\[
\begin{aligned}
C_{\rm even}(\theta)
&=\sum_{m\ge1}(2m)^{-7/4}\cos(4\pi m\theta),\\
G_{\rm odd}(\theta)
&=\sum_{m\ge0}(2m+1)^{-7/4}
\cos(2\pi(2m+1)\theta).
\end{aligned}
\tag{1.1}
\]

Both series converge absolutely and uniformly. Choose `eta>0` so small that

\[
\eta\|C_{\rm even}\|_\infty<\frac1{12},
\tag{1.2}
\]

and set

\[
c(\theta)=\frac13+\eta C_{\rm even}(\theta),
\qquad
g(\theta)=\eta G_{\rm odd}(\theta).
\tag{1.3}
\]

Then

\[
\frac14<c(\theta)<\frac5{12}<1
\tag{1.4}
\]

for every `theta`, so the center has a strict spectral margin. Since `g` is bounded, `c+t g` is legal for all sufficiently small real `t`.

## 2. Half-period symmetry

Every frequency of `C_even` is even. Thus

\[
c(\theta+1/2)=c(\theta).
\tag{2.1}
\]

Every frequency of `G_odd` is odd, and

\[
\cos(2\pi(2m+1)(\theta+1/2))
=-\cos(2\pi(2m+1)\theta).
\]

Hence

\[
g(\theta+1/2)=-g(\theta).
\tag{2.2}
\]

The direction is nonzero, and `mu=hat c(0)=1/3`.

## 3. Membership in `H^1_F`

Apart from harmless factors `eta/2`, the nonzero Fourier coefficients have size `|n|^{-7/4}`. Therefore

\[
\sum_n(1+|n|)^2|\widehat c(n)|^2
+\sum_n(1+|n|)^2|\widehat g(n)|^2
\le C\sum_{n\ge1}n^{2-7/2}
=C\sum_{n\ge1}n^{-3/2}<\infty.
\tag{3.1}
\]

Thus `c,g in H^1_F`.

## 4. Failure of `A_1` and exponential classes

For each symbol, along its nonzero parity subsequence,

\[
\sum_n(1+|n|)|\widehat u(n)|
\ge c_0\sum_{n\ge1}n^{1-7/4}
=c_0\sum_{n\ge1}n^{-3/4}=\infty.
\tag{4.1}
\]

Hence neither `c` nor `g` lies in `A_1`; a fortiori they do not lie in `A_p` for any `p>=1`. Their exact power-law tails also exclude every exponentially weighted Fourier class.

On the other hand,

\[
\sum_n(1+|n|)^p|\widehat u(n)|<\infty
\quad\Longleftrightarrow\quad p<\frac34
\tag{4.2}
\]

for the displayed tails. Thus the same pair belongs simultaneously to every `A_p` with `0<=p<3/4`, including `p=1/2`, while lying outside all `A_p` with `p>=3/4`.

## 5. Separation from accepted special cases

This example is not covered by the previously accepted special classes for the following exact reasons.

1. The center is nonconstant, so the constant-center theorem does not apply.
2. Its mean is `1/3`, not `1/2`, so the accepted Wiener-small mean-one-half theorem does not apply even when `eta` is small.
3. The symbols have no exponential Fourier decay, so the accepted exponential-regularity theorem and its compact-tube successor do not apply.
4. They are outside `A_1`, hence outside PR82's `A_p, p>4` scope and the separate PR106 author scope `A_p, p>=1`.

No assertion is made that these earlier theorems are false outside their scopes; this is only a coverage separation.

## 6. Entropy conclusion

Choose any odd `k` with `hat g(k)!=0`; every displayed odd frequency works. The `H^1_F` theorem gives an `epsilon>0` such that

\[
t\longmapsto h(c+t g)
+\frac{|\widehat g(k)|^4}
{8(1/3)^2(1-(1/3)^2)}t^4
\tag{6.1}
\]

is concave on `[-epsilon,epsilon]`, with strict negative second derivative for `0<|t|<=epsilon` after shrinking the interval.

This is a true stationary DPP configuration-entropy statement for a nonconstant, non-exponentially-local center and a power-law direction. It is not a finite-window positive sample or a method-only observation.