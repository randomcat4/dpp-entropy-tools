# D10-U2 author verdict

STATUS: **PROOF_CANDIDATE_PENDING_FRESH_REVIEW**

The fixed-diagonal DPP fiber has a clean entropy maximum theorem, and the
heterogeneous diagonal zero-Hessian ridge has an explicit fourth-order contact
classification.

First, if a strict real DPP kernel \(K\) has fixed diagonal \(K_{ii}=x_i\),
then all coordinate marginals are fixed Bernoulli\((x_i)\).  Shannon
subadditivity gives

For

\[
X=\operatorname{diag}(x_1,\ldots,x_n),\qquad 0<x_i<1,
\]

\[
H(K)\le \sum_i h(x_i)=H(X).
\]

Equality requires independent coordinates.  DPP pair inclusion gives
\(\mathbb P(i,j\in Y)=x_ix_j-K_{ij}^2\), so equality forces all off-diagonal
entries to vanish.  Thus \(X\) is the unique global entropy maximizer on its
strict fixed-diagonal feasible section.

Second, for every real symmetric zero-diagonal direction \(D\),

\[
K(t)=X+tD
\]

has exact-event atom derivatives \(p_S'(0)=0\).  The total mass and singleton
inclusion identities make the linear logarithmic entropy terms vanish through
orders two, three, and four.  With \(q_S=p_S''(0)\),

\[
H'(0)=H''(0)=H'''(0)=0,\qquad
H^{(4)}(0)=-3\sum_S\frac{q_S^2}{p_S(0)}.
\]

The exact atom jet has the explicit score form

\[
\frac{q_S}{p_S(0)}
=
-2\sum_{i<j}D_{ij}^2\zeta_i(S)\zeta_j(S),
\]

where \(\zeta_i(S)=1/x_i\) for \(i\in S\) and
\(\zeta_i(S)=-1/(1-x_i)\) otherwise.  Independent centered singleton scores
kill all distinct-edge cross terms, yielding

\[
H^{(4)}(0)
=
-12\sum_{i<j}
\frac{D_{ij}^4}{x_i(1-x_i)x_j(1-x_j)}.
\]

Therefore \(H^{(4)}(0)<0\) whenever \(D\ne0\).  Thus the second-order flat
diagonal directions are strict fourth-order entropy descent directions.

On a compact diagonal box \(x_i\in[a,b]\subset(0,1)\), the proof gives the
explicit quantitative bound

\[
H^{(4)}(0)
\le
-\frac{6\,\|D\|_F^4}{n(n-1)M^2},
\qquad
M=\max_{u\in[a,b]}u(1-u),
\qquad(n\ge2).
\]

For \(\|D\|_F=1\), compactness and continuity also give a uniform strict
small-\(t\) radial entropy descent interval.  This is deliberately not a claim
that the Hessian is negative on a full neighborhood.

Relation to old U1: when \(x_i=1/2\) for all \(i\), this reduces to

\[
H(I/2+tD)
=
n\log2-8t^4\sum_{i<j}D_{ij}^4+O(t^6),
\]

because complement symmetry restores evenness.  In the heterogeneous case the
general statement should be read as a negative fourth derivative, with possible
order-five terms in the expansion.

Sanity:

```text
C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe research\R3\deepening_10h\dense_hessian\diagonal_flat_ridge\flat_ridge_sanity.py
```

Actual result: `PASS`, exit code `0`.  The script checks exact rational
\(n=2,3,4\) heterogeneous cases plus a uniform \(n=3\) U1-reduction case.
It also verifies the explicit
\(p_S''(0)/p_S(0)=-2\sum_{i<j}D_{ij}^2\zeta_i(S)\zeta_j(S)\) formula and the
edge-sum fourth derivative.

This is an author result and must not be marked `CORRECT` until a non-author
verification is completed.
