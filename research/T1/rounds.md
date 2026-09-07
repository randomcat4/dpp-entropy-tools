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
