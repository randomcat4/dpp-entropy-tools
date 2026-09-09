# W2 fixed independent arithmetic checks

Author input: PR34 head 838c20b12907d94a9d6e023cc03f48c3f3b36c5c, `research/W2/nonconstant_orbit/previous_proof.md`, equations (3.5), (6.3), (8.4), and (9.2).

This check is written by the nonauthor integration reviewer independently of W2's unavailable author scripts. It is finite deterministic arithmetic supporting the analytic review, not a proof of an entropy-rate theorem or an outward interval certificate.

Frozen cases: an unequal four-coordinate diagonal reference with a real noncommuting direction; a three-coordinate constant reference with a non-real Hermitian direction; and six-coordinate Toeplitz windows of `f_s=1/2+(s/6)cos(2 pi theta)`. Test parameters are -3/2, -1/2, 0, 1/2, 3/2. All centers are safely feasible by row-sum bounds. Exact symbolic principal minors and Mobius inversion construct the full event polynomials, and exact derivatives are compared with the refresh identity. Entropy and dissipation are evaluated with 100 decimal digits. The Toeplitz case checks the quartic bound, parity-block entropy gap and the disjoint matching lower bound.

Stop after these 15 fixed cases, or immediately on a failed identity, infeasibility or negative residual beyond 1e-80. One CPU thread, at most 32 GiB, no GPU, 15-minute external timeout. No adaptive search or additional symbols. Analytic reviewers independently decide universal statements and boundary limits.
