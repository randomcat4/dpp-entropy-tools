# Provenance and evidence classes

## Existing results reused

- The conditional-DPP prefix recursion, exact interval Fourier coefficients,
  spectral/coherence decomposition, and original `n<=22` stationary scan come
  from `icm-conjecture-lab@ee97a734...`.
- The canonical and larger-gap rational finite examples come from
  `icm-conjecture-results@b2645ba...`.  This package does not recertify their
  published exact entropy gaps.

## New computations in this package

- transition spectra through `n=2048` for three frozen reflection families;
- comparison of log-only and linear-plus-log transition-count models;
- complete-event increment continuation to `n=24`, and to `n=26` for the
  closest-to-zero fixed object;
- Toeplitz projection, deformation landscapes, and explicit-symbol nearest
  candidates for three finite counterexamples;
- a 57,120-call fixed-seed stochastic search denominator of nondegenerate
  complete-event Hessians in intrinsic n=5,6 Toeplitz coordinates. All four
  optimizers hit the iteration limit, so this is not convergence or coverage.

## Evidence status

All new signs and fits are floating-point finite computations.  The source
binding and output-consistency verifier passed.  There is no new theorem,
certified finite Toeplitz counterexample, stationary entropy-rate sign, or
novelty claim.
