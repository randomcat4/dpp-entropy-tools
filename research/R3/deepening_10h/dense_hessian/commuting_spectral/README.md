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
- `n3_complement_barrier/`: a verified explicit near-uniform conditional-layer
  region with strict negative curvature for every nonzero one-sign fixed-Q
  spectral direction, including a connected distinct-spectrum rational
  whole-interval certificate;
- `results_server_round9/`: a 20,000-center float64 scout plus a high-precision
  gate for its strongest frozen point.
- `results_server_round13_refine/`, `results_server_round14_refine2/`, and
  `results_server_round15_refine3/`: three increasingly local joint
  spectrum/basis refinements.  The latest stored optimum has
  `rho=0.5725909001<1` and independently recomputed
  `H''=-45.3758897236...`.

The generic fixed-`Q` problem in dimension at least three remains open.  A
finite search miss is not a concavity theorem, and `rho<1` is not a positive
counterexample.
