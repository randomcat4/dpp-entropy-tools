# Work-unit ledger

## 0: baseline and scope audit

Read current public R1 phase3 artifacts and fixed-object reviews. Confirmed
the connected three-point target remains publicly unresolved. Created an
independent branch from R1's current public head. No R1/R3 mutation.

Initial execution uses one CPU thread per computational lane. No GPU or
global dependency changes. Total lane limit: eight threads and 32 GiB.
Commands, PIDs and bounded-job exit states are recorded privately; public
artifacts include sanitized seed, version, denominator and result records.

The initial local combined setup command was rejected by automatic review
without a specific reason; fixed-path setup succeeded. A stale local proxy
was disabled only for affected command processes. Neither affects math.
