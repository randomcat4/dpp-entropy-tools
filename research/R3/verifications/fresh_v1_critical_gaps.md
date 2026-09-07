STATUS: CRITICAL_GAPS

# Frozen v1 verification summary

Fixed commit: `19a8271375e457a0fe74c52f880bc32b0a69c2e7`.

This is the public, path-redacted summary of the independent verifier's first
report. The full internal report is retained by the R3 audit task.

The verifier found no fatal algebraic error in the exact-event generating
function, multiplication order in `L=K(I-K)^{-1}`, group-specific `ell_g` and
`D_c` determinant formula, zero-count Sylvester identity, orbit multiplicities,
or stated arithmetic complexity.

The critical gap was implementation coverage. Frozen v1 quantifies over
nonconstant group-specific `a_g`, while the exact rational reference and its
tests at this commit implemented only a scalar `a`. The NumPy implementation
did exercise nonconstant `a_g`, but floating tolerances and underflow-to-zero
behavior make it diagnostic rather than an exact independent verifier.

Required repair: add an exact vector-`a_g` implementation; compare direct
Möbius atoms, full L-ensemble atoms, and reduced count atoms on at least one
nonconstant and one near-boundary `n<=8` case; verify orbit sizes and keep
floating entropy values diagnostic. Until a revised frozen commit passes a
new audit, v1 is not `CORRECT` or `VERIFIED`.
