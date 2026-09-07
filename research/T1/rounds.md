# Rounds and actual coverage

## Round 1: bounded scouting and tool construction

- Prepared: repository protocol and route read; independent checkouts and three
  direct subagents created. No subagent may spawn descendants.
- Started: criterion exploration, independent boundary attacks, and independent
  definitions/prior-art conditions audit.
- Frozen: bridge-only imaginary-direction curvature theorem v1, after scouting
  yielded a conditional two-site closure route. No later hypothesis repair yet.
- Completed computationally: two non-seed structural examples (n=6, n=30),
  seven additional interface cases, all 75 labeled simple graphs with 1<=n<=4
  for graph-algorithm regression, and one 64-event n=6 floating diagnostic.
- Certified: none yet; independent frozen-commit proof review pending.

The checker is exact rational and evaluates zero event probabilities. The
floating diagnostic found H''=-2.2231429935248154e-05, with probability mass 1
and negligible first derivatives; this is not a rigorous numerical sign interval.
Actual run: Python 3.12.3, one thread, about 0.027 seconds, 12,324 KiB maximum
RSS, successful exit. Machine-readable PID, command, timing and counts are in
artifacts/validation.json. This is a finite regression denominator, not a
search-coverage claim for all kernels.

Failure log: an initial optional diagnostic import failed because NumPy was
absent (exit 1); replaced it with standard-library complex Gaussian elimination,
then reran successfully. No dependency installation was needed. Repository
transport required a local API snapshot and object-hash verification; no
credentials or global configuration were changed. No broad scan was run.

Next falsifiable action: a fresh independent reviewer attempts to break the
single-bridge conditioning step and multi-bridge phase reduction at a pinned
candidate commit. An exact critical gap prevents VERIFIED status.


## Round 2: frozen-commit review and closure

- Candidate pinned at `a71d52bc8c5b45df9ea4795343c290899a2d1f84` before either fresh review.
- First independent proof/checker review: CORRECT, report commit
  `6cdeaf556870426beb41e8bb7436d84fa2656b32`. The verifier additionally checked
  1,099 small graph cases, adversarial interfaces, and reran the bundled validator
  in verifier-owned copies. No kernel search was added.
- Second independent domain proof review: CORRECT, report commit
  `c4b756937f30035b08f54c510fef649fcaccbf19`. It received no first-review verdict and did not coauthor
  or revise the proof. Its exact scope and reasoning are in domain_v1.md.
- Certified scope: frozen bridge lemma v1 and exact rational applicability checker.
  Boundary exploration and the block-Hessian scout remain unreviewed candidates.
- Other initial computation, recorded separately: criterion author 11 tests and
  4 fixed diagnostics / 84 events; boundary attacker 7 fixtures / 80 event values /
  23 assertions. These denominators are not universal search coverage.
- Theorem, proof, hazards, dependency ledger, main code and input examples are
  byte-identical to the candidate. Integrity is in artifacts/frozen_objects.json.
- No critical gap required a theorem or proof repair. No Lean toolchain/project
  was available; no formal-verification claim or installation was made.
- User priority is usefulness, correctness and scope, with no novelty gate.

This closes the first bounded tool target. No broader scan is scheduled. The
next falsifiable downstream action is to apply the interface to a candidate
kernel/direction and either obtain its bridge certificate or a specific
unsupported edge; cyclic cases require a separate argument, not extrapolation.
