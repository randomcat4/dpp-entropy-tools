# D10-S4 author verdict

STATUS: **PROVED_CANDIDATE_PENDING_FRESH_REVIEW**

The scalar-ridge formula upgraded cleanly to every diagonal kernel

\[
K_0=\operatorname{diag}(x_1,\ldots,x_n),\qquad 0<x_i<1.
\]

The proved candidate is

\[
H''_{K_0}[D,D]
=
-\sum_i\frac{D_{ii}^2}{x_i(1-x_i)}
\]

for every real symmetric direction \(D\), using exact-event atoms obtained by
Möbius inversion.

Off-diagonal second-order determinant acceleration may appear in exact atoms,
but its entropy contribution cancels at \(K_0\) because \(\log p_S(0)\) is
affine in singleton indicators and each singleton inclusion probability
\(\mathbb P(i\in Y)=K_{ii}(t)\) is affine in \(t\).

For PSD or NSD \(D\ne0\), the diagonal cannot vanish identically, hence the
Hessian is strictly negative.  On a compact diagonal box
\([a,b]^n\subset(0,1)^n\),

\[
H''_{K_0}[D,D]
\le
-\frac{\|D\|_F^2}{n\,\max_{u\in[a,b]}u(1-u)}.
\]

Compactness and continuity then give a neighborhood of that diagonal box where
strict negativity persists uniformly for all nonzero PSD/NSD directions.

Exact-event rational sanity checks for scalar and heterogeneous \(n=2,3\)
cases passed with exit code `0`.

This is an author result, not an independent verification.  It does not prove
full DPP entropy concavity and does not cover arbitrary indefinite directions,
which can be second-order flat at diagonal kernels.
