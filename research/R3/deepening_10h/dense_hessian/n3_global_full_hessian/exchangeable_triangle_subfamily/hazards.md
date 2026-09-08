# Hazards for the exchangeable triangle unit

1. Exact-event semantics.  The atoms in this directory are exact event
   probabilities obtained by Mobius inversion.  Principal minors are inclusion
   probabilities and must not be substituted for `p_S`.

2. Off-diagonal coordinates.  The observation coordinate `ij` means the full
   symmetric perturbation `E_ij+E_ji`; forgetting the factor two changes the
   six-coordinate Hessian.

3. Derivative table.  The most likely hand-copy error is

```text
partial_alpha p2 = beta(2-3 beta)/3.
```

It is not `2 beta(1-beta)/3`.

4. Irrep reduction scope.  The `S3` split proves the four-dimensional standard
   part positive and reduces the remaining question to the two-dimensional
   invariant block.  It does not by itself prove the two-dimensional determinant
   inequality.

5. Diagonal ridge.  At `alpha=beta` the kernel is diagonal and off-diagonal
   Hessian directions are exactly flat.  The triangle task excludes this line,
   but numerical calculations arbitrarily close to it suffer cancellation and
   cannot be used as sign gates without higher precision or interval control.

6. Local theorem scope.  The punctured diagonal result is existential and local:
   for `x` in a compact subinterval of `(0,1)`, sufficiently small nonzero `a`
   gives `B>0`.  It does not cover fixed-size `a`, spectral boundaries, or the
   entire open square `0<alpha,beta<1`.

7. Scout scope.  `sanity_results.json` is a deterministic finite scout.  It can
   expose formula or implementation mistakes, but a no-hit ledger is not a
   theorem.

