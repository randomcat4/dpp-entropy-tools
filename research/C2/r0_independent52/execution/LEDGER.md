# New execution ledger

Authorization: issue52 comment 5602242678. This is a new 2700-second window,
not an extension of the archived PR55 allocation.

## Frozen input and executable source

- Main source: `9dcb6e9079ca57f94e0e30d63161cda89ca61fae`.
- Pre-execution public source commit: `0bb970ef0a9d81ff79d4e0f38c28d2922067740e`.
- Corresponding isolated local commit: `78d22c33c286707569be92488bc4e107122c6c6a`.
- Author implementation was prepared without Python/CAS execution, then frozen
  and published before transfer/launch. It was unchanged during this run.
- Exact Git source binding is provenance only; correctness rests on explicit
  polynomial identities and full coefficient comparisons, not a checksum.

## author01

| Field | Recorded value |
|---|---|
| UTC start | 2026-09-09 13:32:37 |
| UTC finish | 2026-09-09 13:32:47 |
| Shared hard deadline | 2026-09-09 14:17:37 |
| Wrapper / timeout / arithmetic PIDs | 173680 / 173694 / 173696 |
| Runtime | Python 3.12.3; SymPy 1.14.0 |
| Arithmetic elapsed | 9.707 seconds |
| Process result | exit 0 and RESULT.json PASS |
| Process state after finish | arithmetic PID absent |
| Allocation | one live arithmetic process, one CPU affinity, one library thread, 16 GiB address-space limit, no GPU |
| Peak memory | not measured |
| Failure/restart | none |

The wrapper records the CPU affinity and PID files. The run manifest records
thread settings and the same external/effective absolute deadline. Every
stage has begin/end checkpoints. Both stdout and stderr were empty. Passing
exit status alone was not treated as proof; every RESULT layer and the full
artifact set were inspected.

The author arithmetic stopped on success. Any first-review arithmetic must
be separately recorded, with no overlap and the unchanged hard deadline.
C3's later SECOND is not assigned or launched by C2.

## Public artifact sanitation

`outputs/author01/` retains all result/checkpoint/math files. The private
invocation file is excluded. The first sanitized argv entry in
`run_manifest.json` is generalized to `<IMPLEMENTATION>`; all mathematical
expressions, coefficients and zero identities are unchanged. All 39 public
JSON files parsed successfully after transfer. No server connection detail
or private absolute path is included.
## first01: fresh nonauthor FIRST

- Reviewed public author candidate: `ba890f6294272849fa0a20d5c7e0e9f97d171d51`.
- Reviewer executable frozen before launch at public
  `591c65bdc354e2880c6ccb2506822275b0e45a12`, local
  `10d05f1ef0c9491da40bbe27c338bfd14ac97194`.
- Author PID 173696 confirmed absent before launch. The same locked budget
  directory and deadline were reused, without overlap or reset.
- UTC start/finish: 2026-09-09 13:48:07–13:48:17.
- Wrapper / timeout / arithmetic PIDs: 173826 / 173838 / 173840.
- Arithmetic elapsed: 9.499 seconds; exit 0; RESULT PASS; stdout/stderr empty.
- Same environment/resource guard as author01; 1770 seconds remained on the
  outer guard at launch. The reviewer's own default 900-second internal cap
  set an earlier effective deadline, 14:03:07 UTC. Both deadlines were met.
- Root alone executed the frozen reviewer source. The fresh nonauthor
  inspected the actual outputs and wrote FIRST CORRECT for the frozen
  candidate, conditional on the already-accepted main Schur reduction.
- Arithmetic PID 173840 was subsequently confirmed absent; no live C2
  arithmetic remains. No failure, restart, resource increase or full-r run.

Two runs used 19.206 seconds of reported arithmetic time. The elapsed span
from initial launch to the second finish was 940 seconds, inside the one
2700-second window; unused time is not a new authorization.

The full reviewer evidence is in `review_first/run01/`. The private invocation
file is excluded; only argv[0] is generalized to `<IMPLEMENTATION>`. All 15
reviewer JSON files parsed after copying. The literal scope-text diagnostic
was false because it expected the extra phrase `full-r attempt`; the reviewer
explicitly read the actual r=0 scope and documented the diagnostic limitation.
This raw field was preserved. See `review_first/REVIEW.md` for the assessment.