# I05-30 independent review handoff

This file is a review request specification, not evidence that review or computation has started.

Author branch: `research/I05-30-multiple-endpoint-20260910`.
Branch was created from then-current main `8f4acd31d0ce4d37defafbfcff22fa2b21356f72`. Main advanced during the author task; later main commits are not silently incorporated into the author proof.

All claims below are **author claims, PENDING_REVIEW**. Novelty is separate.

## Mathematical review units

1. **General finite affine endpoint theorem (`RESULT.md` Sections 1–2).** Check the compression of the affine direction to endpoint zero/one eigenspaces, the true cardinality generating polynomial, the `Theta(epsilon)` forbidden-cardinality argument, the inference that at least one complete atom has first-order vanishing, and the complete Fisher-versus-acceleration asymptotics. Verify that repeated zero eigenvalues, repeated one eigenvalues, and simultaneous K / I-K singularity are genuinely included.
2. **Rank-two vanishing-order refinement (`RESULT.md` Section 3).** Check the exact double-root form `q=(1-s/s_*)^2`, its bounded Fisher and adverse logarithmic acceleration term, and the forced simple-order group. Distinguish the unrealizable pure-double likelihood mechanism from an entropy counterexample.
3. **First dense 3+3 repeated-K fixture (`RESULT.md` Sections 4–7).** Check exact legality/maximal chord, channel noncoverage statement, all compact moment inequalities, count-five grouped Fisher, complete logarithm budget, and the whole-chord constant `1/100`.
4. **Uniform two-scale stability (`ADDENDUM_TWO_SCALE_STABILITY.md`).** Check the split parameter `eta`, full-event factor `delta[eta+(1-eta)delta]`, neighboring-cardinality bounds, the `c1/(eta+delta)+c2(eta+delta)/delta >= C/sqrt(delta)` estimate, simultaneous-side logic, the all-event probability/log lower bound, and the final moving-maximal-chord compactness argument. This is the key step removing PR95's simple-endpoint assumption for rank two.
5. **Simultaneous double K / double complement fixture (`ADDENDUM_SIMULTANEOUS_ENDPOINT.md`).** Check the exact Schur identities, both endpoint nullities, 13 complete likelihood types, compact interval sign budgets, `|X|=1,5` grouped Fisher, complete acceleration/log budget, and the final `H''<=-(1/10)t^2` whole-chord bound. Check the limited PR94 noncoverage wording.

## Independent finite/source unit, only if separately assigned

Do not treat execution of author scripts as independent implementation. Reconstruct the two exact 3+3 inputs independently from `input/*.json`, derive complete probabilities from the defining Mobius law, and check only the finite claims needed by the proof. The simultaneous fixture is particularly small algebraically because A,C,B are rational P/Q combinations.

Existing PR95 S2 authorization and its 417-item object are separate and must not be reused or expanded silently for this branch.

## Scope that must remain open

- universal compact-interior sign for arbitrary dense correlated rank-two blocks;
- general dense rank-two whole-chord concavity;
- cross-rank greater than two uniform split-endpoint hierarchy;
- entropy-rate transfer;
- novelty/priority.

A reviewer should freeze the exact PR head being read. A request or issue assignment does not count as a completed review, and mathematical proof, independent arithmetic, integration, and novelty should receive separate dispositions.
