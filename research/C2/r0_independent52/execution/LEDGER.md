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