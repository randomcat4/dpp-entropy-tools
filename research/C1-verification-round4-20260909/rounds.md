# Version ledger

- PR53 original and initially observed head: e0688fbb713e55f93acf791b83437ddf2cc06b7f,
  five files, complete immutable snapshot.
- PR54 requested first-review head: 203f7044815faac9a2de7bc8dbc5bfe249026b1f,
  three files, complete immutable snapshot.
- PR54 observed successor: daf9c3101e66b414cd31d21c58beaf2d48842baf,
  via cd580aabaa0f6f2d01b8f39d40fda9bd317846d9. Delta: add 224-line
  arbitrary-rank appendix and 181-line endpoint appendix; no original-file
  modification. This is substantive new mathematics, not an editorial delta.
  A separate full successor snapshot is retained; addenda remain UNREVIEWED.

Previous PR41/43/47/49 work is merged. C3's eta descriptor correction in
PR43 at6adb231c closed that previous text issue without changing its theorem
parameter domain. This packet does not reopen those proofs or append to the
merged PR49 branch.

## First-pass completion and subsequent ownership

Both original first-review units completed on 2026-09-09. PR53 is
ACCEPTED_SCOPED. PR54's core results are ACCEPTED_SCOPED with Section 5
NEEDS_FIX as detailed in its independent report. No new computation ran.

C3 subsequently froze PR54 at
`c3b9e968c0b4557546c7b10137ef4fff295338b4` and explicitly took the FIRST
audit of the two daf9 addenda, ADDENDUM_RANK2_ENDPOINT_SPECTRUM.md and
only the endpoint-discriminant/root-separation code/output extension.
C3 reported RESULT.md unchanged. This is a separate increment and C1
does not duplicate it or start any second review.

A later PR54 remote head was observed as
`c8486bcdb18a85f93dd27930686cc1d4146804f5`. That observation alone is not
a review of its changes or acceptance of any repair. The original source
binding and the original findings remain immutable.

The exact comparison from c3b9e968 to c8486bcd was then inspected for
version classification. It contains exactly three additions and no changes
to existing files: ADDENDUM_OUTER_WEDGE_FLOW_RATE.md (370 lines),
code/verify_outer_wedge_and_flow.py (104 lines), and
output/verify_outer_wedge_and_flow.json (32 lines). This is a substantive
new outer-wedge/flow/rate unit with its own fixture, not a repair of original
Section 5 and not part of C3's communicated three-appendix freeze. Its
mathematical status is UNREVIEWED by C1; no additional reviewer was started.

## Section 5 bounded repair closure

C3 implemented the three original first-review requests in one commit,
`a1e7f7208262565bb3db0509ff0cccffab757e98`, with parent
`c8486bcdb18a85f93dd27930686cc1d4146804f5`. The exact delta changes
RESULT.md only: seven added and four deleted lines in two hunks. It adds
the zero initial information value/derivative hypothesis, requires a
strictly positive finite L, and removes the matching-to-concave-approximant
overstatement. No other source, script or output changes in this commit.

The immutable new RESULT.md blob was hash-verified as
`39032f0df6913b4e2f2a57cfc2fcb459ffeacf15`. The comparison with original
203f7044 RESULT.md is the same two-hunk repair, so no intervening original
text change was silently accepted.

The original first reviewer inspected only this delta and returned
CLOSED / ACCEPTED_SCOPED for all three findings. See frozen_theorem_v2.md,
units/pr54/section5_delta_frozen.md and units/pr54/section5_delta_review.md.
The original NEEDS_FIX report remains untouched as the historical record.
C10 is now CORRECT / ACCEPTED_SCOPED for the repaired sufficient criterion.
No new computation or formal proof was performed.

C3 now explicitly owns first and second review of all four appended units,
including the c8486bcd outer-wedge/flow/rate appendix and its fixture.
The earlier unassigned status was a versioned observation, superseded by
that ownership message. PR53's second is reported active; PR54 original-unit
second remains C3's next step after this closure. No C1 second was started.
