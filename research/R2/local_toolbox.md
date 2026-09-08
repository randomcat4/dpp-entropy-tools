# Local toolbox exclusion table

Problem: R2 balanced near-projection transverse chords.  Frozen version: v1.
Date: 2026-09-08.  Owner: R2 main instance.

## Excluded as already used, insufficient, or out of scope

1. **Raw subset enumeration without asymptotics.**  It can test a finite
   point, but it does not separate zero-event logarithmic terms or prove a
   family statement.
2. **Principal-minor entropy.**  Principal minors are inclusion
   probabilities and cannot replace exact event masses.
3. **The fixed-center Hessian formula alone.**  The outer family changes its
   center and samples a half-length of order `sqrt(epsilon)`; substituting it
   into a fixed interior formula without uniform control is invalid.
4. **Purely imaginary bridge-edge criterion.**  The certified T1 result is for
   imaginary Hermitian directions and does not decide this real transverse
   family.
5. **Finite block-transfer error bounds.**  The T2 tool preserves a supplied
   finite gap under controlled coupling; it does not supply the real seed gap
   sought here.
6. **T3 candidate as an oracle.**  It may be cross-checked independently, but
   its positive Jensen-gap example is not the counterexample sign and its
   candidate status cannot certify R2.
7. **Unbounded random search.**  Excluded by the resource and denominator
   contract; only frozen, bounded probes are allowed.

## Still allowed

Exterior algebra, spectral-selection mixtures, Schur complements, singular
perturbation with explicit remainders, information-theoretic latent-variable
representations, algebraic/interval checks, and bounded exact enumeration.
