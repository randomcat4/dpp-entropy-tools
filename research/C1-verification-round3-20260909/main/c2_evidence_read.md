# C2 public evidence alignment

Evidence read at immutable PR47 commit
`1ddc775d8ceebf46ddd0335f04df282b58c1e8f7`:

- [PR41 report](https://github.com/randomcat4/dpp-entropy-tools/blob/1ddc775d8ceebf46ddd0335f04df282b58c1e8f7/research/C2/verification3/pr41/REPORT.md),
  `evidence.json`, saved stdout and exit code.
- [PR43 event report](https://github.com/randomcat4/dpp-entropy-tools/blob/1ddc775d8ceebf46ddd0335f04df282b58c1e8f7/research/C2/verification3/pr43_events/output/REPORT.md),
  machine-readable checklist, both author replay records, run status and exit status.
- The packet STATUS at that same commit.

PR41's source is exactly C1's frozen 6fd61dcd commit. The evidence reports
PASS for eight-event Möbius reconstruction, all six-direction first/second
jets, full Fisher/acceleration, strong-family derivative/minors, sign
conjugation, two-point conditional algebra, isolated-block cancellations and
missing-edge identities. The eight checks are marked PASS; the saved author
subprocess and final verifier exits are 0. C2 used SymPy 1.14.0, matching the
author requirement; C1's independent small checks used 1.13.3 and make no
claim to be the requirements-matched author replay.

PR43's computation remains frozen at 4e1369ef. The subsequently inspected
7bd5962b and a7da3951 documentation changes did not alter its mathematical
proof, input or verifier object. Both nested author scripts exited 0. The
independent checklist reports all 256 joint events and 8×32 conditional events
at t=1/5, 1/2 and 1; strict legality; all eight refresh states and 64 transitions;
and the four-state obstruction values. The final run and process exit are PASS/0.
Its old theorem letters/line ranges belong to its explicitly old source, not
the new v3.1 line numbering.

C1 read these published reports and machine-readable result records; it did
not independently replay or re-audit C2's entire verifier implementation.
They are supplemental bounded computation evidence, not the basis for a new
universal theorem. C1's proof verdicts remain those of its independent reviews.
Earlier slow/interrupted or serialization failures are acknowledged in C2's
report; they are not silently treated as successful runs.

At this evidence commit the fixed directed-flow LP was a rational feasible
candidate under fresh nonauthor review, not an accepted C1 certificate. C1
does not certify that LP or infer the full entropy-curvature inequality from
its existence. C2 retains its certificate-review ownership and unresolved
endpoint/error/search-contract questions under issue #45.
