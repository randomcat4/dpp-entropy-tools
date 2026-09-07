# R2: balanced near-projection transverse chords

Status: RUNNING.  No real-symmetric counterexample is claimed.

This route studies a frozen multiscale family whose center approaches a
projection while its chord half-length is of order `sqrt(epsilon)`.  The first
target is an asymptotic sign theorem which either excludes this family or
produces a concrete candidate for fresh verification.

The exact-event convention is

```text
p_K(S) = sum_{T: S subset T subset E} (-1)^(|T|-|S|) det(K_T).
```

Principal minors are inclusion probabilities, not exact-event masses.

## Reproduction

The bounded diagnostic will live in `artifacts/`.  Floating output is only a
probe; the mathematical status is controlled by the frozen statement, proof,
and fresh reviews.

## Scope boundary

This route distinguishes:

- an affine chord at each fixed `epsilon`, with fixed center and direction;
- the outer family in which the center and chord half-length vary with
  `epsilon`.

A negative result for this family is not a theorem for all real-symmetric
kernels or all near-projection paths.
