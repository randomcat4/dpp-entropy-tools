# R2: balanced near-projection transverse chords

Status: VERIFIED for frozen theorem v1; route closed after this bounded unit.
No real-symmetric counterexample is claimed.

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

Run the deterministic rational-law diagnostic from the checkout root:

```text
python research/R2/artifacts/check_balanced_family.py
```

Run the independent strict logarithm-enclosure fixtures with:

```text
cd research/R2/verifications/fresh_v1
python verify_transverse_fixtures.py
```

The first command's Decimal entropies are probes.  The second command produces
rational outward enclosures for two fixed examples.  The family theorem is
certified by the frozen proof plus two commit-bound fresh reviews, not by a
finite diagnostic.

## Scope boundary

This route distinguishes:

- an affine chord at each fixed `epsilon`, with fixed center and direction;
- the outer family in which the center and chord half-length vary with
  `epsilon`.

A negative result for this family is not a theorem for all real-symmetric
kernels or all near-projection paths.
