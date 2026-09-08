# R1 hazards

- Confusing inclusion probabilities det K[A] with exact events p_K(S).
- Reporting the concave-sign quantity `H(K0)-average endpoints` as a
  counterexample. R1 needs `average endpoints - H(K0) > 0`.
- Reusing complex Hermitian examples whose direction has imaginary
  skew-symmetric part. R1 requires real symmetric K and real symmetric chord
  direction.
- Treating a finite no-hit as proof of global real-symmetric concavity.
- Trusting tiny positive floating values. Candidate promotion requires a
  stable positive Hessian or direct chord gap well above numerical error, then
  independent exact/interval verification.
- Failing to certify strict interior endpoints.
- Omitting the denominator, seed, rejected candidate counts, or exit status.
- Applying the proved `2 x 2` concavity theorem to a conditional DPP kernel
  whose dependence on the original chord parameter is non-affine.
- Treating negative semidefiniteness of the Hessian only at a symmetric
  midpoint as a finite midpoint theorem; a line integral needs curvature on
  the whole chord, or a separate finite-event inequality.
- Using a large raw Hessian eigenvalue near a spectral/event boundary without
  high-precision replay.  Phase 4 retained raw values as large as `0.01197`
  that became strictly negative at 140 digits.
