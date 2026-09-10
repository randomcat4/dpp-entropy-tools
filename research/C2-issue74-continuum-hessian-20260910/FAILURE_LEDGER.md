# Failure ledger

The original deadline remains `2026-09-10T11:26:19Z`.

## Attempt 1

- Waiting launcher PID: `58116`.
- Released: `2026-09-10T09:53:12Z`.
- Result: mechanical interpreter-resolution failure before Python started.
- Retained files: `run.stdout.txt` (empty), `run.stderr.txt` (Microsoft
  Store alias error).
- Mathematical work performed: none.

## Attempt 2

- Waiting launcher PID: `46408`; Python child PID: `54628`.
- Executable commit: `5d69af786a73a99e5a96e3a6ca94fa947c304a5a`.
- Result: exact-rational/interval evaluation reached final result
  serialization, then `json.dumps` rejected a `Decimal` value in the copied
  PR98 metadata.  Atomic output was not installed.
- Retained files: `run2.stdout.txt` (empty), `run2.stderr.txt` (complete
  traceback).
- Patch allowed under the live clock: add `default=str` only to final JSON
  serialization.  No input, formula, gate, precision, branch map, derivative,
  point, or interpretation changes.
