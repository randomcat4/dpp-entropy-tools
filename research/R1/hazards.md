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
