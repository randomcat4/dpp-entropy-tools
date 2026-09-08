# R1 phase-three preregistration

- Start date: 2026-09-08.
- User wall-clock authorization: at most nine hours.
- Initial status: `RUNNING_PHASE3 / INCOMPLETE`.
- The original objective is unchanged: seek a strict real-symmetric
  counterexample first; absent one, promote only a precisely delimited
  exclusion family with a complete proof and independent review.
- Event semantics are unchanged: `det(K_A)` is an inclusion probability; the
  exact event law is obtained by Boolean Mobius inversion.

## P3-01: global two-dimensional concavity

- Frozen statement: `frozen_n2_concavity_v1.md`.
- Attack boundary and general counterexamples before attempting a Hessian or
  finite-chord proof.
- A finite scan is only a falsification probe.  Success requires a
  self-contained proof or an explicit feasible counterexample.

## P3-02: block-composition inequality

- Frozen statement: `frozen_block_composition_v1.md`.
- Bound the full gap by the sum of the principal-block gaps and characterize
  strict loss caused by cross-block coupling.
- Together with P3-01, this would cover every block-diagonal midpoint whose
  blocks have size at most two, in every feasible real-symmetric direction.

## P3-03: symbolic and computational certificate

- Use event coordinates, the negative-association constraint, Hessian minors,
  or a sum-of-squares reduction, while also searching for a smallest
  counterexample.
- Cap: 4 CPU, 16 GiB, no GPU; at most 120 minutes per batch.  Record seeds,
  actual call counts, failures, exit codes, and exact identities.
- Continue only after an explicit counterexample, symbolic identity, strictly
  stronger lemma, or complete proof appears.

## Stop rules

- A counterexample satisfying every premise stops the proof route and is sent
  to strict certification.
- Retire a route after two units repeat the same blocker without a new object.
- At the nine-hour boundary, start no new job; only collect existing terminal
  artifacts.

