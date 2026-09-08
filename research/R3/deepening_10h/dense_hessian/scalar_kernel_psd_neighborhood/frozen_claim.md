# D10-S4 frozen claim: diagonal-kernel Hessian and PSD/NSD box neighborhood

Author status: **PROOF_CANDIDATE_PENDING_FRESH_REVIEW**.

Let \(n\ge1\), let

\[
K_0=\operatorname{diag}(x_1,\ldots,x_n),\qquad 0<x_i<1,
\]

and let \(D=D^\top\) be any real symmetric direction.  For sufficiently small
\(t\),

\[
K(t)=K_0+tD
\]

is a strict real DPP marginal kernel.  Let \(H(K)\) be the Shannon entropy of
the exact-event DPP law, with exact atoms obtained from inclusion probabilities
\(\det K[A,A]\) by Möbius inversion.

The diagonal-kernel Hessian claim is

\[
\left.\frac{d^2}{dt^2}H(K_0+tD)\right|_{t=0}
=
-\sum_{i=1}^n\frac{D_{ii}^2}{x_i(1-x_i)}.
\]

Consequences:

1. If \(D\ne0\) is positive semidefinite or negative semidefinite, then

   \[
   H''_{K_0}[D,D]<0.
   \]

2. If \(D\) is positive semidefinite or negative semidefinite and
   \(x_i\in[a,b]\subset(0,1)\), then

   \[
   H''_{K_0}[D,D]
   \le
   -\frac{\|D\|_F^2}{n\,\max_{u\in[a,b]}u(1-u)}.
   \]

3. For every fixed \(n\) and compact diagonal box
   \([a,b]^n\subset(0,1)^n\), there is a neighborhood of
   \(\{\operatorname{diag}(x):x\in[a,b]^n\}\) on which the Hessian remains
   uniformly strictly negative on every nonzero PSD or NSD direction.

The former scalar-ridge statement is the special case \(x_1=\cdots=x_n=x\).
The claim does not assert strict negativity for arbitrary indefinite
directions.  Zero-diagonal indefinite directions are second-order flat at every
diagonal kernel.
