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
- `n3_complement_barrier_refine/`: a verified larger product region
  `min_a alpha_a beta_a>1/27`, an exact pointwise coefficient test, and a
  connected distinct-spectrum rational interval beyond the earlier box;
- `results_server_round9/`: a 20,000-center float64 scout plus a high-precision
  gate for its strongest frozen point.
- `results_server_round13_refine/`, `results_server_round14_refine2/`,
  `results_server_round15_refine3/`, `results_server_round16_refine4/`, and
  `results_server_round17_refine5/`: five increasingly local joint
  spectrum/basis refinements.  The fifth stored optimum has
  `rho=0.5740468374<1` and independently recomputed
  `H''=-39.3902501599...`; its configured spectrum-margin floor is active.
- `results_server_round18_boundary1/`: a lowered-floor boundary diagnostic.
  Its new strongest has `rho=0.5746069387`, high-precision
  `H''=-40.2752548454...`, and actual spectrum margin `0.0153714`, farther
  inside than the prior `0.01`-margin source despite permitting `0.002`.

The generic fixed-`Q` problem in dimension at least three remains open.  A
finite search miss is not a concavity theorem, and `rho<1` is not a positive
counterexample.
