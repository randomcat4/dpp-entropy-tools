# Frozen scope

## Source

- Repository: `randomcat4/dpp-entropy-tools`
- PR: #94
- Exact reviewed author commit: `a9db9f98dc6dac766dd9b214f056ee9b30109b23`
- Included author files: `CHANNEL_LIFT.md`, `MODE_FAMILY.md`, the channel portions of `README.md` and `FAILURE_LEDGER.md`, `code/exact_core.py`, `code/fixtures.py`, `code/verify_channels.py`, and the channel output artifacts.
- Excluded author unit: `WHOLE_CHORD.md`, `code/verify_whole_chord.py`, and all whole-chord output artifacts.

No later PR94 head or older review opinion is inherited.

## Imported premise

The only imported concavity theorem is the accepted real finite-dimensional m-by-2 radial result, including concavity of `G(s)=H(K(sqrt(s)))`, at:

`research/C1-verification-20260909/children/w1/W1_ROUND2_INDEPENDENT_REVIEW.md`

blob `b7804d6c9267cc7d2428765cf344e72470444b56`.

The present FIRST does not re-prove or broaden that premise.

## Reviewed claims

1. Every finite binary-input channel admits the stated selector refinement, with selector independent of the input and an affine marginal correction in the entropy identity.
2. For DPP input, each refined binary law is a DPP with truly affine kernel `A_j+D_j K D_j` and all complete-event Fisher/acceleration contributions retained.
3. Disjoint-support observed-coordinate mode expansions implement those channels exactly, including singular event matrices by polynomial continuation.
4. Expanding an accepted m-by-2 radial path preserves its maximal legal chord and yields whole-chord concavity; a positive all-revealing selector supplies strictness.
5. The quantitative normalized-curvature transfer, the half-filled complement formula, and its explicit `kappa_i` are correct.
6. `MODE_FAMILY.md` is reviewed as a specialization, with its exact rational calculations left to the separate finite/source gate.

## Exclusions

- No arbitrary observed-coordinate rotation is used or accepted.
- The grouped-channel construction does not cover arbitrary dense rank-two cross blocks or the original PR58 fixture.
- The failed uniform complement-pair shortcut away from half filling remains disproved.
- Explicit rational output identities and signs are not independently recomputed here.
- Novelty, formal verification, entropy rates, author edits, SECOND review, and merge are outside scope.
