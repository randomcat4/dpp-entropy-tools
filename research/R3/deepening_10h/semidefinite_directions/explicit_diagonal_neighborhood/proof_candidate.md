# Explicit diagonal-box PSD/NSD neighborhood

STATUS: CORRECT_AFTER_INDEPENDENT_REVIEW.

All norms below are Frobenius norms unless an operator norm is displayed.
The entropy is the Shannon entropy of all exact DPP events.

## 1. Uniform atom floor along the segment

For an observed subset `S`, write

\[
p_S(K)=(-1)^{|S^c|}\det A_S(K),\qquad
A_S(K)=K-I_{S^c}.
\tag{1}
\]

If `0<K<I`, then `A_S(K)` is symmetric and every Rayleigh quotient lies in
`[-1,1]`; hence `||A_S(K)||_op<=1`.

At `X=diag(x)` the exact event law is the product Bernoulli law, so

\[
p_S(X)=\prod_{i\in S}x_i\prod_{i\notin S}(1-x_i)\ge s^n=q.
\tag{2}
\]

Multilinearity of the determinant in its columns gives, for any symmetric
direction `E`,

\[
|D p_S(K)[E]|\le n\|E\|_F.
\tag{3}
\]

Indeed there are `n` replaced-column determinants; every unchanged column has
norm at most one and the replaced column has norm at most `||E||_F`.

Let `E=K-X` and `K_u=X+uE`.  The strict contraction cone is convex, so every
`K_u` is strict.  Integrating (3), if `||E||_F<=q/(2n)` then

\[
p_S(K_u)\ge q-n\|E\|_F\ge q/2=m
\quad(0\le u\le1).
\tag{4}
\]

## 2. A uniform third-derivative bound

The same column expansion gives the mixed determinant bounds

\[
|p_E|\le n\|E\|,
\quad |p_D|\le n\|D\|,
\]
\[
|p_{ED}|\le n(n-1)\|E\|\|D\|,
\quad |p_{DD}|\le n(n-1)\|D\|^2,
\]
\[
|p_{EDD}|\le n(n-1)(n-2)\|E\|\|D\|^2.
\tag{5}
\]

For `f(p)=-p log p`,

\[
f'(p)=-(1+\log p),\qquad f''(p)=-1/p,\qquad f'''(p)=1/p^2.
\]

The chain rule for one exact atom is

\[
D^3(f\circ p)[E,D,D]
=f'''p_Ep_D^2
+f''(2p_{ED}p_D+p_Ep_{DD})
+f'p_{EDD}.
\tag{6}
\]

On `m<=p<=1`, equations (5)--(6) therefore imply

\[
|D^3(f\circ p)[E,D,D]|
\le\left(\frac{n^3}{m^2}
+\frac{3n^2(n-1)}m+n(n-1)(n-2)\ell\right)
\|E\|\|D\|^2.
\tag{7}
\]

There are `2^n` exact atoms.  Summing (7) proves

\[
|D^3H(K_u)[E,D,D]|\le L\|E\|\|D\|^2.
\tag{8}
\]

No cancellation between events is used in this bound.

## 3. The diagonal curvature margin

The verified exact diagonal formula is

\[
H''_X[D,D]=-
\sum_i\frac{D_{ii}^2}{x_i(1-x_i)}.
\tag{9}
\]

If `D>=0`, then

\[
\sum_iD_{ii}^2\ge\frac{(\operatorname{tr}D)^2}{n}
\ge\frac{\operatorname{tr}(D^2)}n
=\frac{\|D\|_F^2}{n}.
\tag{10}
\]

The same holds after replacing an NSD direction by `-D`.  Since
`x_i(1-x_i)<=1/4`, (9)--(10) give

\[
H''_X[D,D]\le-\frac4n\|D\|_F^2.
\tag{11}
\]

Finally, the fundamental theorem of calculus and (8) yield

\[
|H''_K[D,D]-H''_X[D,D]|
\le L\|K-X\|_F\|D\|_F^2.
\tag{12}
\]

If `||K-X||_F<=delta_{n,a,b}`, then (4) applies and the right side of (12)
is at most `2||D||_F^2/n`.  Combining with (11) proves

\[
H''_K[D,D]\le-\frac2n\|D\|_F^2.
\tag{13}
\]

The theorem is homogeneous in `D`, includes singular PSD/NSD directions, and
does not cover indefinite directions.  The strictness assumption on `K` is
retained; the explicit ball is intersected with the strict kernel domain.

## 4. Scope and weakness of the constant

The radius scales at least as poorly as a multiple of `s^(2n)` because the
argument protects every one of the `2^n` atoms independently.  It is useful as
a fully explicit certificate that the diagonal-box exclusion is genuinely a
neighborhood statement.  It is not presented as a sharp radius, a global
concavity theorem, or a result for arbitrary symmetric directions.

A fresh non-author audit under `verifications/` independently rederived the
exact-event formula, determinant derivative counts, third-order chain rule,
atom floor, PSD trace inequality and final constants, and checked small
rational dimensions without importing an author implementation.
