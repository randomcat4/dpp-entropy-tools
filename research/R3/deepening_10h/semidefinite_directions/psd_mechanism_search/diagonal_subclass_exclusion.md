# D10-S3 diagonal PSD/NSD subclass exclusion

Status: **PROVED_SUBCLASS_ONLY**.  This is a narrow coordinate-product
subclass, not a proof of the general PSD/NSD direction question.

## Claim

Let

\[
K(t)=\operatorname{diag}(x_1(t),\ldots,x_n(t)),\qquad
x_i(t)=k_i+t d_i,
\]

on an open interval \(J\), with \(0<x_i(t)<1\) for every \(i\) and
\(t\in J\).  Equivalently \(0<K(t)<I\).  Then the DPP configuration
entropy \(H(K(t))\) is concave in \(t\).  More precisely,

\[
\frac{d^2}{dt^2}H(K(t))
=-\sum_{i=1}^n \frac{d_i^2}{x_i(t)(1-x_i(t))}\le 0.
\]

The inequality is strict at every \(t\in J\) unless \(D=\operatorname{diag}(d_i)=0\).
It applies to diagonal PSD directions \(d_i\ge0\) and diagonal NSD directions
\(d_i\le0\), but the sign condition is stronger than needed: the formula only
uses the real affine diagonal path staying in the open cube.

## Proof

For a diagonal kernel, inclusion probabilities are

\[
\mathbb P(A\subseteq Y)=\det K_A=\prod_{i\in A}x_i(t).
\]

The Boolean Möbius inversion for the exact atom \(S\) gives

\[
p_{K(t)}(S)
=\sum_{A\supseteq S}(-1)^{|A|-|S|}
  \prod_{i\in A}x_i(t)
=\prod_{i\in S}x_i(t)\prod_{i\notin S}(1-x_i(t)).
\]

Thus the point process is a product of independent Bernoulli variables in the
original observation coordinates.  Its full configuration Shannon entropy is

\[
H(K(t))=\sum_{i=1}^n h(x_i(t)),\qquad
h(x)=-x\log x-(1-x)\log(1-x).
\]

Since \(h''(x)=-1/[x(1-x)]\) on \(0<x<1\), the displayed second derivative
formula follows by the chain rule.  If some \(d_i\ne0\), the corresponding
summand is strictly negative; if all \(d_i=0\), the entropy is constant.

The same concavity implies every symmetric feasible chord has

\[
\frac{H(K(t-h))+H(K(t+h))}{2}-H(K(t))\le0,
\]

with strict inequality for \(h\ne0\) whenever \(D\ne0\) and both endpoints lie
in the strict positive-contraction region.

## Scope boundary

This proof is only for kernels diagonal in the **fixed observation basis**.
It must not be read as covering arbitrary pairs \(K,D\) that commute after an
orthogonal change of basis.  DPP configuration entropy is tied to the original
coordinate events; rotating the kernel changes those event probabilities.

The result is therefore a small PSD/NSD exclusion zone and a sanity anchor for
D10-S3, not a replacement for the unresolved general semidefinite-direction
problem.
