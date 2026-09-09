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
