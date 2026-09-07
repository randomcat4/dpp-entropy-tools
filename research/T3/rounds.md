# Rounds Ledger

## 2026-09-07 Round 0: Startup And Freeze

- Issue state: RUNNING.
- Branch: `research/T3-certificate-tools`.
- Server working directory: private T3 directory registered in issue #3; details
  excluded from public files.
- New object: `frozen_theorem_v1.md`, a pointwise finite DPP entropy chord-gap
  certificate statement.
- Verified range: none yet.
- Unverified range: all implementation and certificate soundness.
- Minimum gap: need a strict arithmetic implementation plus independent
  reference cross-check on at least one rational example.
- Next falsifiable action: produce a certificate or deterministic refusal for a
  tiny rational chord instance and compare against an independent all-subsets
  enumerator.
- Actual compute: only repository checkout, issue comments, and documentation
  edits so far; no heavy computation.
- Failure record: local raw `git clone` to GitHub failed under network/proxy
  conditions; GitHub CLI API worked after clearing per-process proxy variables.

## 2026-09-07 Round 1: Seed Chord Case

- New object: `artifacts/seed_chord_case.json`.
- Status: DIAGNOSTIC_ONLY_NOT_CERTIFIED.
- Input: rational non-diagonal `2 x 2` marginal kernel path
  `K(t) = [[1/5, 1/15], [1/15, 2/5]] + t [[2/5, 1/30], [1/30, -1/5]]`.
- Covered diagnostic points: `t0=0`, `tm=1/2`, `t1=1`.
- Exact mass diagnostic: all four exact event masses are positive at all three
  chord points and sum to 1.
- Floating diagnostic: midpoint chord gap is approximately
  `0.11075606181097264` in the orientation of `frozen_theorem_v1.md`.
- Verified range: none. This is a seed input, not a strict certificate.
- Minimum gap: strict log/entropy enclosures and independent reference
  reproduction still needed before any certificate claim.

## Child Work Allocation

- Child A: strict core and interval algorithms, owns `research/T3/core/` and
  `research/T3/core_notes.md`.
- Child B: independent complete-event enumerator and adversarial checks, owns
  `research/T3/reference/` and `research/T3/reference_notes.md`.
- Child C: certificate schema and complexity design, owns `research/T3/specs/`
  and `research/T3/interface_notes.md`.

No child may validate its own candidate as `VERIFIED`.

## 2026-09-07 Round 2: Core Candidate Rejected For Formula Gap

- Incoming object: Child A strict-core candidate.
- Main review status: returned for revision, not integrated as a certificate
  candidate.
- Critical gap: the first core candidate computed entropy from selected
  principal minors. For a marginal-kernel DPP those minors are inclusion
  probabilities, not exact all-subset event masses. This violates
  `frozen_theorem_v1.md` and T3's central guardrail.
- Required revision: build exact event mass polynomials by Mobius inversion over
  all subsets, update tests with a diagonal Bernoulli case that catches the
  shortcut, and ensure the public seed chord case is checked using exact event
  masses.
- Verified range: none.

## 2026-09-07 Round 3: Interface And Reference Candidates Integrated

- Incoming object: Child C interface/spec candidate.
- Main review status: integrated as a candidate contract, not as mathematical
  verification.
- Files: `interface_notes.md` and `specs/`.
- Reproduced command: isolated local venv ran
  `python research/T3/specs/check_contract.py`.
- Exit code: 0.
- Result: schema/examples smoke check passed, 25 negative cases rejected,
  strict engine requests started 0, certified 0.

- Incoming object: Child B independent reference candidate.
- Main review status: integrated as independent reference/adversarial tooling.
- Files: `reference/` and `reference_notes.md`.
- Reproduced commands:
  - bundled local Python ran `python -m unittest research/T3/reference/test_reference.py`;
    exit code 0, 5 tests passed.
  - server Python ran `python3 -m unittest research/T3/reference/test_reference.py`;
    exit code 0, 5 tests passed.
  - server Python ran
    `python3 research/T3/reference/exact_dpp_reference.py --output-dir research/T3/reference/out-servercheck`;
    exit code 0, 6 cases completed.
- Main caution: reference supports both `marginal` and `l_ensemble`; v1
  certificate claims stay on the marginal-kernel all-exact-events convention.

## 2026-09-07 Round 4: Core Revision Candidate And Cross-Check

- Incoming object: Child A revised strict core.
- Main review status: integrated as CANDIDATE, not `VERIFIED`.
- Critical gap from Round 2 addressed: the core now computes exact outcome mass
  polynomials by Mobius inversion and uses all exact events by default.
- Reproduced commands:
  - bundled local Python ran
    `python -m unittest discover -s research/T3/core -p "test_*.py"`;
    exit code 0, 10 tests passed.
  - bundled local Python ran `python research/T3/core/dpp_core.py --example`;
    exit code 0.
  - bundled local Python ran
    `python research/T3/core/dpp_core.py --input research/T3/artifacts/seed_chord_case.json`;
    exit code 0.
- Candidate strict core output for the seed chord case:
  `CERTIFIED`, sign `positive`, lower gap decimal
  `0.1107560618109726105714089086`.
- Independent reference cross-check on the same seed:
  status `CANDIDATE`, classification `CERTIFIED_POSITIVE`, lower gap decimal
  `0.110756061810972610571408908560280310634681644974`.
- Verified range: no final `VERIFIED` status yet. The next required action is a
  fresh-context verification bound to a frozen commit.
