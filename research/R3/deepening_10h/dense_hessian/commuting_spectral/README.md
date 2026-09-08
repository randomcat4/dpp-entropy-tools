# Fixed-eigenvector spectral-rate route

This directory studies affine paths

\[
K(t)=Q\operatorname{diag}(\lambda_i+t v_i)Q^T
\]

with fixed real orthogonal `Q` and one-sign spectral rates.  It combines three
separate evidence levels:

- `analytic_channel/`: a verified exact projection-DPP channel reduction and
  closed sufficient subclasses;
- `low_dim_exact/`: a verified strict-negative theorem in dimension two and a
  precise dimension-three proof-method blocker;
- `results_server_round9/`: a 20,000-center float64 scout plus a high-precision
  gate for its strongest frozen point.

The generic fixed-`Q` problem in dimension at least three remains open.  A
finite search miss is not a concavity theorem, and `rho<1` is not a positive
counterexample.

