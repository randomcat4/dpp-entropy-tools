# T1 verdict

Stage status: VERIFIED for the frozen bridge-direction theorem and exact rational
applicability checker. The first bounded tool objective is complete.

For every real symmetric strict contraction K and D=iA supported on existing
bridge edges of K's off-diagonal support graph, H''(K)[D] < 0 when D is nonzero;
the zero direction gives zero. This is a finite Shannon-entropy statement in
natural logarithms, at t=0 on the affine path K+tD.

Two separate fresh GPT-5.5 xhigh contexts returned CORRECT on the unchanged
candidate `a71d52bc8c5b45df9ea4795343c290899a2d1f84`:

- [Proof and checker review](verifications/fresh_v1.md), report commit
  `6cdeaf556870426beb41e8bb7436d84fa2656b32`.
- [Independent domain review](verifications/domain_v1.md), report commit
  `c4b756937f30035b08f54c510fef649fcaccbf19`. This reviewer did not receive the first verdict.

The main instance did not rewrite the proof. The frozen proof's original
"independent verification pending" header is intentionally preserved as part
of the pinned object; these reports and this verdict give the subsequent status.
[Integrity record](artifacts/frozen_objects.json) verifies unchanged bytes.

## Usefulness

The checker gives the sign using exact rational positivity tests and graph
bridges, with zero event probabilities evaluated. It uses O(n^3) rational
arithmetic operations and O(n^2) storage; bit costs are not claimed constant.
Arbitrary dense blocks linked by single bridges give an unbounded non-seed
application. The concrete n=30 case avoids enumerating its 2^30 possible events.
The [README](README.md) gives command-line and programmatic entry points.

Main validation completed two structural inputs, seven additional interface
cases, 75 graph regressions, and one 64-event floating diagnostic, in about
0.027 seconds and 12 MiB maximum RSS on one thread. Author, boundary, and fresh
reviewer checks have separate denominators/logs in rounds.md and their artifacts.
Numerical values are diagnostics, not rigorous magnitude intervals.

## Limits and closure

Only bridge-supported imaginary directions at real strict-interior kernels are
covered. Cyclic active edges, absent active edges, arbitrary real directions,
boundary kernels, and entropy rates need separate tools. INCONCLUSIVE supplies
no sign. Boundary and other exploratory lemmas are not certified by this verdict.
The proved criterion can be useful even when it is not applicable to a dense
graph with no bridges; that explicit boundary is part of its interface.

Correctness: the frozen proof passed two independent mathematical audits; the
exact checker passed source review and bounded adversarial testing. No Lean or
other formal proof certificate is claimed. Prior-art attribution is maintained;
novelty is not a requirement for this stage and remains unclaimed. No all-kernel
concavity problem has been solved here. The next action is downstream use of the
checked interface, not an automatic expansion into a broad scan.
