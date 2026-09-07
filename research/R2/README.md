# R2: real DPP entropy near projection faces

Status: `VERIFIED` for frozen theorems v1 and v2.  The frozen-v2 general
boundary coefficient theorem is bound to candidate commit
`3ae3323ae958feb733b78f5b425c6d9b540524e9` by two independent `CORRECT`
reviews. The unrestricted real question is `INCOMPLETE`. No real-symmetric
counterexample is claimed.

This route studies a frozen multiscale family whose center approaches a
projection while its chord half-length is of order `sqrt(epsilon)`.  The first
target is an asymptotic sign theorem which either excludes this family or
produces a concrete candidate for fresh verification.

Round 2 allows mixed longitudinal/transverse directions, feasible singular
Schur residuals, unequal scalar approach rates, and the first two escape
layers of the zero-transverse branch. See `boundary_theorems_v2.md` for the
historical result map.

Round 3 resolves the formerly unsigned ordinary `epsilon^2` coefficient for
every fixed non-paired tomography-kernel frame.  See
`boundary_theorems_v3.md`, `proofs/tomography_components_v3.md`, and
`proofs/component_pair_C2_v3.md`.

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

The intermediate v2 subfamilies deliberately received no repeated formal
gate.  The general v2 coefficient closure is a major result and received one
commit-bound gate after its candidate proof was fixed.  See
`verifications/round3_logic_review.md` and
`verifications/round3_domain_review.md`.

## Scope boundary

This route distinguishes:

- an affine chord at each fixed `epsilon`, with fixed center and direction;
- the outer family in which the center and chord half-length vary with
  `epsilon`.

A negative result for these fixed families is not a theorem for all
real-symmetric kernels or all near-projection paths.  The fixed-data two-term
projection-boundary hierarchy is sealed, but moving frames, varying data,
other approach geometries, and arbitrary interior chords remain outside it.
