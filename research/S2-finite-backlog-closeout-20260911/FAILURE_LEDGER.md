# Failure ledger

1. PR104 independent attempt 1 completed every mathematical assertion, then
   exited 1 while converting an exact fraction with more than Python's default
   4300 integer digits to text.  The retry changed output summarization only
   and exited 0.
2. Frozen PR112 `check_exact.py` exits 1 by design as
   `RETIRED_KNOWN_FAILING`.  Its diagnostic reproduces the earliest historical
   recurrence error `3/4096`; no historical pass is inferred.
3. Frozen PR116 `check_endpoint_phase.py` exits 1 at line 43.  It uses SymPy
   structural `==` for two algebraically equal expressions.  Independent
   factorization proves their difference is zero, but that does not change the
   source-checker FAIL verdict.
4. PR116 moments/rays independent attempt 1 incorrectly identified a
   simultaneous two-scale logarithmic coefficient with a fixed-parameter
   endpoint coefficient.  The retry used each of the 13 likelihood types'
   epsilon-vanishing order and passed all three ray coefficients.
5. PR116 Bernstein independent attempt was terminated by the agreed cap after
   600.298 seconds wall / 531.766 seconds CPU.  It remained single-threaded,
   peaked at 1,547,706,368 bytes, and had not finished the exact common
   numerator.  Status is `EVIDENCE_INSUFFICIENT`, not PASS.

PR136's earlier input-endpoint auditor failure and Windows telemetry-header
build failure are preserved in the already merged PR139 history and summarized
in `FINITE_BACKLOG_CLOSEOUT.md`.
