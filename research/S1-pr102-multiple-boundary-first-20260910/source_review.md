# Primary-source and repository-premise audit

## Cardinality generating determinant

J. Ben Hough, Manjunath Krishnapur, Yuval Peres, and Balint Virag, *Determinantal Processes and Independence*, Probability Surveys 3 (2006), arXiv:math/0503110:

https://arxiv.org/pdf/math/0503110

The source proves that the number of points in a finite region has the law of a sum of independent Bernoulli variables with parameters equal to the restricted-kernel eigenvalues.  PR102 directly derives the equivalent generating function

\[
\mathbf E[z^{|X|}]=\det(I-K+zK),
\]

then uses it only to estimate probabilities of true observed cardinality groups.  It does not evaluate configuration entropy in an eigenbasis.

## Pointwise L-ensemble identity

Alex Kulesza and Ben Taskar, *Determinantal Point Processes for Machine Learning*, Foundations and Trends in Machine Learning 5 (2012), arXiv:1207.6083, equations (13), (15), and (25):

https://arxiv.org/pdf/1207.6083

For strict finite `K`, the source gives

\[
L=K(I-K)^{-1},
\qquad
P(X=E)=\frac{\det L_E}{\det(I+L)}
=\det(I-K)\det L_E.
\]

This supports the all-event lower bound in the two-scale addendum.  PR102 does not make `L` affine in the path parameter.

## Accepted rank-two premise

The compact-interior continuation uses the accepted PR58 complete-likelihood framework:

- `docs/verification_round4_20260909/accepted_pr58.md`, blob `dadf6976fb422700789bf7fdd2eb045dfe0aee51`;
- PR58 author head `89aa874c24dd5a3ea98f8474826392560b1d0397`;
- `research/I05-23-middle-20260909/RESULT.md`, blob `7e981841708a117a2f07852f10eb7b4a53f93515`.

That premise retains `q=1-sa+s^2b`, all complete events, the Fisher term, and the atom-acceleration term.  It does not provide a universal compact-interior sign, and this FIRST does not claim one.
