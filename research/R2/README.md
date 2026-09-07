# R2: real DPP entropy near projection faces

Status: `VERIFIED` for frozen theorem v1; `PROVED_HERE` without a new formal
gate for the broader v2 boundary theorems. The unrestricted real question is
`INCOMPLETE`. No real-symmetric counterexample is claimed.

This route studies a frozen multiscale family whose center approaches a
projection while its chord half-length is of order `sqrt(epsilon)`.  The first
target is an asymptotic sign theorem which either excludes this family or
produces a concrete candidate for fresh verification.

Round 2 allows mixed longitudinal/transverse directions, feasible singular
Schur residuals, unequal scalar approach rates, and the first two escape
layers of the zero-transverse branch. See `boundary_theorems_v2.md` for the
result map and exact remaining blocker.

The exact-event convention throughout is

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

The first command's Decimal entropies are probes. The second command produces
rational outward enclosures for two fixed examples.  The family theorem is
certified by the frozen proof plus two commit-bound fresh reviews, not by a
finite diagnostic.

The v2 results are analytic working theorems and deliberately retain
`PROVED_HERE` status. No repeated SHA/certificate gate was run for their
intermediate subfamilies.

## Scope boundary

This route distinguishes:

- an affine chord at each fixed `epsilon`, with fixed center and direction;
- the outer family in which the center and chord half-length vary with
  `epsilon`.

A negative result for these fixed families is not a theorem for all
real-symmetric kernels or all near-projection paths. In particular, the
ordinary second-order coefficient on a general non-paired, invisible
longitudinal measurement kernel remains unsigned.
