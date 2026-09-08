# Proof candidate for D10-U2

Author status: **PROOF_CANDIDATE_PENDING_FRESH_REVIEW**.

Let

\[
X=\operatorname{diag}(x_1,\ldots,x_n),\qquad 0<x_i<1.
\]

All probabilities below are exact-event DPP probabilities.  Inclusion
probabilities are converted to atoms by Möbius inversion:

\[
p_S(K)=
\sum_{A\supseteq S}(-1)^{|A|-|S|}\det K[A,A].
\]

## 1. Global maximum on a fixed diagonal fiber

Let \(K\) be any strict real DPP kernel with diagonal \(K_{ii}=x_i\), and let
\(Y=(1_{\{i\in Y\}})_{i=1}^n\) be its exact subset indicator vector.  Each
coordinate has fixed Bernoulli marginal

\[
\mathbb P(i\in Y)=K_{ii}=x_i.
\]

By Shannon subadditivity,

\[
H(Y)\le\sum_i H(Y_i)=\sum_i h(x_i),
\]

where

\[
h(u)=-u\log u-(1-u)\log(1-u).
\]

The diagonal kernel \(X\) gives independent Bernoulli coordinates, so

\[
H(X)=\sum_i h(x_i).
\]

Equality in Shannon subadditivity holds only when the coordinates are mutually
independent.  If a DPP with this diagonal were independent, then for every
\(i\ne j\)

\[
\mathbb P(i,j\in Y)=x_ix_j.
\]

But the DPP pair inclusion probability is

\[
\mathbb P(i,j\in Y)
=
\det
\begin{pmatrix}
x_i & K_{ij}\\
K_{ij} & x_j
\end{pmatrix}
=
x_ix_j-K_{ij}^2.
\]

Thus independence forces \(K_{ij}=0\) for every \(i\ne j\), hence \(K=X\).
Conversely \(K=X\) is exactly the independent Bernoulli DPP.  Therefore

\[
H(K)\le H(X),
\]

with equality if and only if \(K=X\).  This proves that the diagonal kernel is
the unique global entropy maximizer on its strict fixed-diagonal feasible
section.

## 2. Zero first atom derivative along zero-diagonal directions

Now take a real symmetric zero-diagonal direction \(D\), and set

\[
K(t)=X+tD
\]

for \(t\) in a sufficiently small strict-feasible interval.  For any nonempty
\(A\),

\[
\left.\frac{d}{dt}\det(X[A,A]+tD[A,A])\right|_{t=0}
=
\det X[A,A]\operatorname{tr}\!\left(X[A,A]^{-1}D[A,A]\right)
=0,
\]

because \(D_{ii}=0\).  The empty determinant also has zero derivative.
Möbius inversion therefore gives

\[
p_S'(0)=0
\]

for every exact atom \(S\).

At \(t=0\),

\[
p_S(0)=a_S
=
\prod_{i\in S}x_i\prod_{i\notin S}(1-x_i)>0.
\]

## 3. Explicit formula for \(q_S=p_S''(0)\)

Define

\[
\zeta_i(S)=
\begin{cases}
1/x_i,& i\in S,\\
-1/(1-x_i),& i\notin S.
\end{cases}
\]

We claim

\[
\frac{q_S}{a_S}
=
-2\sum_{i<j}D_{ij}^2\,\zeta_i(S)\zeta_j(S).
\]

It is enough to compute the contribution of a fixed unordered pair \(i<j\).
For an inclusion set \(A\), the second derivative at the diagonal comes only
from transposing that pair in the determinant expansion.  If \(i,j\in A\), then

\[
\left.\frac{d^2}{dt^2}\det(X[A,A]+tD[A,A])\right|_{t=0}
=
-2D_{ij}^2\prod_{k\in A\setminus\{i,j\}}x_k.
\]

If either \(i\) or \(j\) is absent from \(A\), this pair contributes zero.
Insert this pair contribution into Möbius inversion:

\[
-2D_{ij}^2
\sum_{A\supseteq S\cup\{i,j\}}
(-1)^{|A|-|S|}
\prod_{k\in A\setminus\{i,j\}}x_k.
\]

The remaining sum factors coordinatewise.  Comparing the four cases
\((i,j)\subseteq S\), exactly one of \(i,j\) in \(S\), and neither in \(S\),
one gets respectively

\[
\frac{-2D_{ij}^2a_S}{x_ix_j},\qquad
\frac{+2D_{ij}^2a_S}{x_i(1-x_j)}
\quad\text{or}\quad
\frac{+2D_{ij}^2a_S}{(1-x_i)x_j},
\qquad
\frac{-2D_{ij}^2a_S}{(1-x_i)(1-x_j)}.
\]

These four signs are exactly

\[
-2D_{ij}^2a_S\,\zeta_i(S)\zeta_j(S).
\]

Summing over pairs proves the explicit atom-jet formula.

As an immediate consistency check, summing this formula over all atoms
containing a fixed pair gives

\[
\sum_{S\supseteq\{i,j\}}q_S
=
-2D_{ij}^2,
\]

which is also obtained directly from the pair inclusion determinant

\[
\det
\begin{pmatrix}
x_i & tD_{ij}\\
tD_{ij} & x_j
\end{pmatrix}
=x_ix_j-t^2D_{ij}^2.
\]

## 4. Entropy expansion through fourth order

For any \(B\subseteq[n]\),

\[
\sum_{S\supseteq B}p_S(t)=\mathbb P(B\subseteq Y)=\det K(t)[B,B].
\]

For \(B=\varnothing\) and singleton \(B=\{i\}\),

\[
\sum_Sp_S(t)=1,\qquad
\sum_{S\ni i}p_S(t)=K_{ii}(t)=x_i.
\]

Hence for every \(m\ge1\),

\[
\sum_S p_S^{(m)}(0)=0,\qquad
\sum_{S\ni i} p_S^{(m)}(0)=0.
\]

Let

\[
r_S=p_S'''(0),\qquad s_S=p_S^{(4)}(0).
\]

Since \(p_S'(0)=0\),

\[
p_S(t)=
a_S+\frac{q_S}{2}t^2+\frac{r_S}{6}t^3+\frac{s_S}{24}t^4+O(t^5).
\]

For \(h(u)=-u\log u\),

\[
h(a_S+\Delta)
=
h(a_S)
+(-\log a_S-1)\Delta
-\frac{\Delta^2}{2a_S}
+O(\Delta^3).
\]

Here \(\Delta=O(t^2)\), so the only quadratic contribution through order four
is \(q_S^2t^4/4\).  Therefore

\[
H(t)-H(0)
=
-\sum_S(\log a_S+1)
\left(\frac{q_S}{2}t^2+\frac{r_S}{6}t^3+\frac{s_S}{24}t^4\right)
-\sum_S\frac{q_S^2}{8a_S}t^4
+O(t^5).
\]

The logarithm of the base atom is affine in singleton indicators:

\[
\log a_S
=
\sum_i\log(1-x_i)
+
\sum_{i\in S}\log\frac{x_i}{1-x_i}.
\]

The total-mass and singleton-marginal derivative identities therefore kill

\[
\sum_S(\log a_S+1)p_S^{(m)}(0)
\]

for \(m=2,3,4\).  Thus

\[
H'(0)=H''(0)=H'''(0)=0
\]

and

\[
H^{(4)}(0)
=
-3\sum_S\frac{q_S^2}{a_S}.
\]

This is the promised cancellation of the \(p^{(m)}\log p(0)\) linear terms.

## 5. Explicit fourth derivative from centered edge characters

Under the product law \(a_S\), the variables \(\zeta_i(S)\) are independent and
centered:

\[
\mathbb E[\zeta_i]=0,\qquad
\mathbb E[\zeta_i^2]=\frac1{x_i(1-x_i)}.
\]

Using the formula from Section 3,

\[
\sum_S\frac{q_S^2}{a_S}
=
\mathbb E\left[
\left(
-2\sum_{i<j}D_{ij}^2\zeta_i\zeta_j
\right)^2
\right].
\]

All cross terms vanish.  If two different edges are disjoint, some centered
\(\zeta\) appears to the first power.  If they share one endpoint, the two
non-shared endpoints each appear to the first power.  Thus only identical-edge
terms survive, giving

\[
\sum_S\frac{q_S^2}{a_S}
=
4\sum_{i<j}
\frac{D_{ij}^4}{x_i(1-x_i)x_j(1-x_j)}.
\]

Consequently,

\[
H^{(4)}(0)
=
-12\sum_{i<j}
\frac{D_{ij}^4}{x_i(1-x_i)x_j(1-x_j)}.
\]

If \(D\ne0\), at least one off-diagonal \(D_{ij}\ne0\), so the displayed sum is
positive and \(H^{(4)}(0)<0\).

## 6. Uniform fourth-order bound on compact diagonal boxes

Assume \(x_i\in[a,b]\subset(0,1)\), and define

\[
M=\max_{u\in[a,b]}u(1-u).
\]

Then \(x_i(1-x_i)\le M\), and the explicit formula gives

\[
H^{(4)}(0)
\le
-\frac{12}{M^2}\sum_{i<j}D_{ij}^4.
\]

Let \(N=n(n-1)/2\).  Since \(D\) has zero diagonal,

\[
\sum_{i<j}D_{ij}^2=\frac{\|D\|_F^2}{2}.
\]

Cauchy's inequality gives

\[
\sum_{i<j}D_{ij}^4
\ge
\frac{\left(\sum_{i<j}D_{ij}^2\right)^2}{N}
=
\frac{\|D\|_F^4}{2n(n-1)}.
\]

Therefore

\[
H^{(4)}(0)
\le
-\frac{6\,\|D\|_F^4}{n(n-1)M^2}.
\]

For \(\|D\|_F=1\), this is a uniform negative fourth-order bound over the
compact box.

## 7. Small-\(t\) consequences

The global fixed-diagonal theorem from Section 1 already implies that, whenever
\(D\ne0\) and \(X+tD\) is strict feasible with \(t\ne0\),

\[
H(X+tD)<H(X),
\]

because \(X+tD\) has the same diagonal as \(X\) but is not equal to \(X\).

There is also a local quantitative bound.  Fix \(n\) and
\(0<a\le b<1\).  On the compact set

\[
\mathcal C=
\{(x,D):x\in[a,b]^n,\ D=D^\top,\ \operatorname{diag}D=0,\ \|D\|_F=1\},
\]

the fourth derivative at zero is at most

\[
-C_4,\qquad C_4=\frac{6}{n(n-1)M^2}.
\]

Since \(\|D\|_{\mathrm{op}}\le1\), the line remains strict for

\[
|t|\le \frac12\min(a,1-b).
\]

The fourth derivative of \(s\mapsto H(X+sD)\) is continuous on this compact
strict-feasible tube.  By uniform continuity, after shrinking to some
\(0<\rho\le\frac12\min(a,1-b)\),

\[
\frac{d^4}{ds^4}H(X+sD)\le -\frac{C_4}{2}
\]

for every \((x,D)\in\mathcal C\) and every \(|s|\le\rho\).  Taylor's theorem,
using \(H'(0)=H''(0)=H'''(0)=0\), yields

\[
H(X+tD)
\le
H(X)-\frac{C_4}{48}t^4
=
H(X)-\frac{t^4}{8n(n-1)M^2}
\]

for \(0<|t|\le\rho\).  This is still a radial contact-order statement, not a
nearby-Hessian sign theorem.

## 8. Relation to the older uniform-flat-ridge result

The older `uniform_flat_ridge` result is the special case \(x_i=1/2\) for all
\(i\).  Then \(a_S=2^{-n}\) and

\[
\zeta_i(S)=2z_i,\qquad z_i=
\begin{cases}
1,&i\in S,\\
-1,&i\notin S.
\end{cases}
\]

The explicit atom jet becomes

\[
\frac{p_S''(0)}{a_S}
=
-8\sum_{i<j}z_iz_jD_{ij}^2.
\]

The edge characters \(z_iz_j\) are orthogonal under the uniform Rademacher law,
so

\[
\sum_S\frac{p_S''(0)^2}{p_S(0)}
=
64\sum_{i<j}D_{ij}^4.
\]

Hence

\[
H^{(4)}(0)=-192\sum_{i<j}D_{ij}^4,
\]

and the Taylor coefficient is

\[
\frac{H^{(4)}(0)}{24}
=
-8\sum_{i<j}D_{ij}^4,
\]

matching U1 exactly.  U1 additionally has complement symmetry
\(H(I/2+tD)=H(I/2-tD)\), so its remainder can be expressed as \(O(t^6)\).  A
heterogeneous diagonal \(X\) generally lacks that evenness, so D10-U2 does not
claim the \(O(t^6)\) improvement in general.
