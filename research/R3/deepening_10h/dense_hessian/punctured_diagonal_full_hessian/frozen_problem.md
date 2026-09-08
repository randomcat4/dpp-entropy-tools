# D10-U3/S9 frozen problem

AUTHOR STATUS: PROOF_CANDIDATE_PENDING_INDEPENDENT_REVIEW.

Let `X=diag(x_1,...,x_n)` be any strict diagonal DPP kernel, `n>=2`, and let
`A` be a real symmetric zero-diagonal matrix with

\[
A_{ij}\ne0\qquad(i<j).
\]

The candidate statement is that there exists `epsilon_0(X,A)>0` such that
for every `0<|epsilon|<epsilon_0`,

\[
K_\epsilon=X+\epsilon A
\]

is a strict DPP kernel and its complete observation-coordinate entropy
Hessian is negative definite:

\[
H''_{K_\epsilon}[D,D]<0
\quad\text{for every nonzero real symmetric }D.
\]

Consequently every such `K_epsilon` has an open neighborhood on which the
full Hessian remains negative definite.  If `X` is heterogeneous, these are
heterogeneous kernels; because all off-diagonal entries are nonzero, they are
fully connected.

The uniform version fixes a compact diagonal box, normalizes `||A||_F=1`, and
imposes `min_{i<j}|A_ij|>=eta>0`.  One common `epsilon_0` then works for the
whole compact family.

This is a punctured-neighborhood theorem candidate.  It does not claim full
Hessian negativity at the diagonal ridge itself, where every zero-diagonal
direction is a second-order null direction.  It does not address sparse A
with missing edges or the global strict-kernel domain.

