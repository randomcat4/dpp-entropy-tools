# Verification and independence

## Author self-check

The main author derived proof.md and froze its v2 statement before reviews.
The server main_precheck.py run verifies 8 rational three-site gauge atoms
exactly and 6 finite product-channel/curvature diagnostics. It is not a
formal or interval proof of the general theorem. The theorem's proof is
the finite argument in proof.md, independent of these computations.

## Two actual nonauthor theorem reviews

1. First verifier: an independently initialized GPT-5.5 xhigh child. It first
   reconstructed gauge identities without author code, then received the
   frozen radial statement/proof. It did not create or revise that proof.
   Status **CORRECT**, report verifications/first_v2.md.
2. Second verifier: a replacement GPT-5.5 xhigh child in a fresh context,
   after the first review passed and the mechanism child ended. It received
   only the frozen statement, anonymous proof and hazards, without earlier
   author reasoning or reviewer conclusions. Status **CORRECT**, report
   verifications/second_fresh_v2.md, with exact input hashes.

They separately checked the absence of a hidden equal-marginal hypothesis,
the same-channel DPI sign, the exact affine DPP identity, negative parameters,
the join at zero, feasible boundaries and the true entropy-rate limit.

The initial author commit was 509ac053b49e61c4de8112a424578a5affa61f57.
Publication may change the Git ancestry to isolate C3 from unmerged source
work; the reviewed proof and v2 statement bytes are unchanged. File hashes,
not the number of reviewer votes, identify the accepted mathematical object.

## Other coverage

The gauge reconstruction is independently checked by small exact objects.
The mechanism child's additional phase/weak-coupling theorem is an auxiliary
author proof with its own narrower scope; it is not automatically covered
by the two radial theorem reviews. The fixed numerical rate certificate
has a separate **CORRECT_SCOPED** nonauthor report in verifications/fixed_rate.md.
That reviewer independently recomputed all 288 small event determinants
with permutation arithmetic, all six residual/corner certificates and the
exact negative gate. Interval-log source was inspected and the author
scripts were also rerun once; the latter is explicitly not an independent
implementation of interval logarithms. None of these is counted as a third
proof of the full conjecture.

Formal status: only an actual Lean/Lake version feasibility check was run;
no C3 theorem was mechanically verified. See formal_status.md.

Novelty is a separate question and remains unconfirmed.
