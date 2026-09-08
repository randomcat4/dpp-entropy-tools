# D10-S4 proof candidate

Author status: **PROOF_CANDIDATE_PENDING_FRESH_REVIEW**.

This is the upgraded diagonal-box version.  The scalar \(xI\) lemma is the
special case \(x_1=\cdots=x_n=x\).

## 1. Exact atoms and first derivative

For a DPP marginal kernel \(K\), the exact atom for \(Y=S\) is

\[
p_S(K)=\sum_{A\supseteq S}(-1)^{|A|-|S|}\det K[A,A].
\]

This is the only exact-event semantics used here.

Set

\[
K_0=\operatorname{diag}(x_1,\ldots,x_n),\qquad
K(t)=K_0+tD,
\]

where \(0<x_i<1\) and \(D=D^\top\).  Since \(K_0\) is an interior strict
positive contraction, all exact atoms are positive for sufficiently small
\(|t|\), so differentiating the entropy is legitimate.

At \(t=0\),

\[
p_S(0)=\prod_{i\in S}x_i\prod_{i\notin S}(1-x_i).
\]

For a nonempty \(A\),

\[
\left.\frac{d}{dt}\det(K_0[A,A]+tD[A,A])\right|_{t=0}
=
\left(\prod_{j\in A}x_j\right)\sum_{i\in A}\frac{D_{ii}}{x_i}.
\]

The empty determinant has derivative zero.  Insert this into Möbius inversion.
For a fixed coordinate \(i\), the coefficient of \(D_{ii}\) in \(p_S'(0)\) is:

- if \(i\in S\),

  \[
  \frac1{x_i}
  \prod_{j\in S}x_j
  \prod_{j\notin S}(1-x_j);
  \]

- if \(i\notin S\),

  \[
  -\frac1{1-x_i}
  \prod_{j\in S}x_j
  \prod_{j\notin S}(1-x_j).
  \]

Therefore

\[
\frac{p_S'(0)}{p_S(0)}
=
\sum_{i\in S}\frac{D_{ii}}{x_i}
-
\sum_{i\notin S}\frac{D_{ii}}{1-x_i}.
\]

Off-diagonal entries of \(D\) do not enter the first derivative of any exact
atom at a diagonal kernel.

## 2. Entropy Hessian and disappearance of the \(p''\)-term

For a smooth positive probability vector \(p(t)\),

\[
H(p(t))''=
-\sum_S\frac{p_S'(t)^2}{p_S(t)}
-\sum_S p_S''(t)\log p_S(t).
\]

At \(t=0\),

\[
\log p_S(0)
=
\sum_i\log(1-x_i)
+
\sum_{i\in S}\log\frac{x_i}{1-x_i}.
\]

The constant part is killed by normalization:

\[
\sum_Sp_S''(0)=0.
\]

For each coordinate \(i\), the coefficient of \(\log(x_i/(1-x_i))\) is killed
by the singleton inclusion identity:

\[
\sum_{S\ni i}p_S(t)=\mathbb P(i\in Y)=K_{ii}(t)=x_i+tD_{ii},
\]

so

\[
\sum_{S\ni i}p_S''(0)=0.
\]

Hence

\[
\sum_Sp_S''(0)\log p_S(0)=0.
\]

This is the precise cancellation.  Off-diagonal determinant acceleration may
make individual \(p_S''(0)\) nonzero, but it is entropy-neutral at every
diagonal kernel because \(\log p_S(0)\) is affine in the singleton indicators.

## 3. Fisher term

Let \(S\) be distributed according to

\[
p_S(0)=\prod_{i\in S}x_i\prod_{i\notin S}(1-x_i),
\]

the independent Bernoulli law with heterogeneous parameters \(x_i\).  Define

\[
\xi_i(S)=
\begin{cases}
1/x_i, & i\in S,\\
-1/(1-x_i), & i\notin S.
\end{cases}
\]

Then

\[
\frac{p_S'(0)}{p_S(0)}=\sum_iD_{ii}\xi_i(S).
\]

The \(\xi_i\)'s are independent centered variables under the product law, with

\[
\mathbb E\xi_i=0,\qquad
\mathbb E[\xi_i\xi_j]=0\ (i\ne j),\qquad
\mathbb E\xi_i^2=\frac1{x_i(1-x_i)}.
\]

Therefore

\[
\sum_S\frac{p_S'(0)^2}{p_S(0)}
=
\sum_i\frac{D_{ii}^2}{x_i(1-x_i)}.
\]

Combining with the vanished \(p''\)-term gives

\[
H''_{K_0}[D,D]
=
-\sum_i\frac{D_{ii}^2}{x_i(1-x_i)}.
\]

## 4. PSD/NSD strictness and Frobenius bound

If \(D\succeq0\) and \(D\ne0\), then at least one diagonal entry is positive.
Equivalently, if every \(D_{ii}=0\), then every \(2\times2\) principal minor
forces \(D_{ij}=0\), so \(D=0\).  Thus

\[
\sum_iD_{ii}^2>0
\]

for every nonzero PSD direction.  The NSD case follows by applying the same
argument to \(-D\succeq0\).  Hence the Hessian is strictly negative on nonzero
PSD or NSD directions.

For \(D\succeq0\),

\[
\|D\|_F^2
=\sum_j\lambda_j(D)^2
\le
\left(\sum_j\lambda_j(D)\right)^2
=
(\operatorname{tr}D)^2
=
\left(\sum_iD_{ii}\right)^2
\le
n\sum_iD_{ii}^2.
\]

The same inequality holds for \(D\preceq0\) after replacing \(D\) by \(-D\).
If every \(x_i\in[a,b]\subset(0,1)\), then

\[
\frac1{x_i(1-x_i)}
\ge
\frac1{\max_{u\in[a,b]}u(1-u)}.
\]

Therefore

\[
H''_{K_0}[D,D]
\le
-\frac{\sum_iD_{ii}^2}{\max_{u\in[a,b]}u(1-u)}
\le
-\frac{\|D\|_F^2}{n\,\max_{u\in[a,b]}u(1-u)}.
\]

## 5. Uniform neighborhood near a compact diagonal box

Fix \(n\) and \(0<a\le b<1\).  Let

\[
\mathcal D_{a,b}=\{\operatorname{diag}(x_1,\ldots,x_n):x_i\in[a,b]\}
\]

and

\[
m=\frac1{n\max_{u\in[a,b]}u(1-u)}>0.
\]

The diagonal-box estimate says that for every \(K_0\in\mathcal D_{a,b}\) and
every PSD or NSD \(D\) with \(\|D\|_F=1\),

\[
H''_{K_0}[D,D]\le -m.
\]

The entropy Hessian is continuous on strict kernels.  On any compact subset
with eigenvalues bounded inside \((0,1)\), all exact atoms are positive and
bounded away from zero: using \(L=K(I-K)^{-1}\), exact atoms are
\(\det L_S/\det(I+L)\), and principal minors of a positive definite \(L\) are
positive.

The set

\[
\{(K_0,D):K_0\in\mathcal D_{a,b},\ \|D\|_F=1,
D\succeq0\text{ or }D\preceq0\}
\]

is compact.  By uniform continuity of the Hessian, there is a neighborhood of
\(\mathcal D_{a,b}\) and a constant \(c>0\), for instance \(c=m/2\) after
shrinking the neighborhood, such that

\[
H''_K[D,D]\le -c
\]

for every kernel \(K\) in that neighborhood and every PSD or NSD
\(\|D\|_F=1\).  Homogeneity gives

\[
H''_K[D,D]\le -c\|D\|_F^2
\]

for every nonzero PSD or NSD direction.

This proves a strict PSD/NSD negative-curvature neighborhood around the compact
diagonal box.  No explicit numerical radius is claimed here.
