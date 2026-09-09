# I05-C3-20260909

**PROVED — scoped continuous-family theorem.**

For every constant p in (0,1) and every fixed bounded measurable real g on
R/Z, the true stationary DPP Shannon entropy rate

    t -> h(p+t g)

is concave on the entire interval where 0<=p+t g<=1 almost everywhere,
including feasible boundary symbols. No evenness, zero-mean, finite-bandwidth,
or entropy-rate differentiability assumption is required.

The finite theorem covers every affine ray B+tA through an interior
diagonal B, with arbitrary Hermitian A, including noncommuting B and A.
The proof identifies an exact independent-replacement channel, controls
its relative-entropy mixed derivatives by data processing, and passes
finite Jensen inequalities directly to the actual entropy rate.

The frozen statement is frozen_statement_v2.md and the complete proof is
proof.md. Two nonauthor contexts independently returned **CORRECT**; the
second started with no author or previous-review context. See verification.md.

**The full Lyons–Steif conjecture remains unresolved.** General scalar
chords need not lie on a line through a constant symbol. No positive
entropy-rate counterexample is claimed. Novelty is unconfirmed and there
is no Lean theorem-certification claim.

The separate fixed coherent-cycle experiment and its rate certificate are
reported in mechanism/ and rate/. Its true midpoint gap lies strictly in
(-0.000951846792,-0.0000008403727) nats, excluding that fixed chord as a
counterexample. This one-object certificate also passed a separate nonauthor
audit; its exact intervals appear in final_rate_summary.md.
The theorem above does not depend on those computations.

Public task: https://github.com/randomcat4/dpp-entropy-tools/issues/27

Draft PR: https://github.com/randomcat4/dpp-entropy-tools/pull/29
