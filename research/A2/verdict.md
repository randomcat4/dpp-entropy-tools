# A2 first-milestone verdict

## Correctness

- Frozen v2 claims 1--3: PROVED, independently reviewed CORRECT at immutable
  candidate ab4d57cdbdc782fd033178795da9873db01bf7be.
- Frozen v3 claims 1--3: PROVED, independently reviewed CORRECT at immutable
  candidate 5084d3966a3eccc3ad5b497f1da6eab08fe7554a. Only Sections 1--4 of
  its author proof are certified.
- The reviewer is one separate non-author context producing two reports,
  not two independent reviewers of the same theorem.
- The original finite real positive-contraction entropy question remains
  INCOMPLETE. No counterexample with Delta>0 has been obtained.

## Minimal scope and remaining gaps

The new four-dimensional path has noncommuting midpoints and cannot be
represented directly by the old fixed-data midpoint forms, even after a
common scalar reparameterization. Its negative leading coefficient and
remainder are uniform on compact x intervals inside (0,1). The proof does
not establish uniformity as x tends to zero or one, or cover all finite t.

The moving mixed-data theorem is conditional on bounded blocks, actual
endpoint feasibility, the explicitly frozen residual/kernel conditions and
the quantitative relation between epsilon, the active probability minimum m,
and the direction size F. Arbitrary moving paths do not automatically satisfy
these conditions. The crossover example demonstrates a precise failure of
fixed-data leading-term substitution, rather than a failure of the old theorem.

## Computation and formal coverage

Seven unique rational chords received exact event/feasibility checks and
strict rational log enclosures. A separate reviewer checked the same seven
chords with an independent rational implementation and high-precision entropy
evaluation; that replay is auxiliary and not an additional universal claim.
Forty-eight symbolic event functions were recorded. All author-side bounded
jobs exited zero; the reviewer retained a local missing-SymPy execution failure
before using its independent standard-library check.

Lean 4.32.0 checked five integer matrix identities only, with propext as their
printed axiom dependency. The real entropy, feasibility and asymptotic claims
are not fully Lean-formalized.

## Value and provenance

The first milestone is met by a checked path exclusion beyond the old direct
representation, a reusable uniform-error interface, and an explicit scaling
obstruction. Novelty is UNCONFIRMED. The entropy modulus is elementary and the
two-dimensional sign is already known; the claimed value is precise coverage
and protection against invalid asymptotic extrapolation. These are scoped
research tools/auxiliary results, not a claimed resolution of the main problem
or an audited paper-level contribution.

See README.md for direct links to frozen statements, proofs, independent
reports, reproduction records and failed-inference ledgers.
