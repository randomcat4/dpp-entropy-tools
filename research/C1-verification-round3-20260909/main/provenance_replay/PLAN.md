# Fixed-check execution-record repair

The original independent PR43 E–H check printed all successful exact phases,
but its outer shell PID and exit files were damaged by quoting. Its later
`verified_exit=0` was inferred from the final output marker, not a directly
captured process exit. Retain all those original records and do not describe
that inference as an observed exit code.

Run exactly the same independent script and same continuation_fixture.json
once, in a new owned directory, to obtain a reliable execution record.
No input, theorem, interval, search box, or algorithm is expanded.

Input checks: three-point cycle and odds identities; the specified 3+3
fixture/radius; exterior likelihood and KL identities; all 64 events at
t=1/100 and t=1/50. High-precision curvatures remain diagnostics.

Limits: one arithmetic thread; 8 GiB virtual-memory limit; 600-second wall
timeout with a 10-second kill grace; no GPU; no package installation.
Record wrapper and arithmetic PID, timestamp, thread environment, Python and
library versions, stdout, stderr, and actual process exit. Stop on success,
failure or timeout. Do not retry again automatically. This is C1's own root
3+3 check, not a duplicate of C2's nested 3+5 or LP computation.

Publication uses this portable mathematical script and a portable runner.
Private launch details remain outside the review packet.

## Second fixed record repair: four-state channel check

The original channel runner directly recorded exit 0, but omitted PID and
did not enforce its planned thread/memory/time guards. Replay its identical
short_exact_checks.py once with the same guard and metadata scheme, writing
separate channels_execution/stdout/stderr files. Its inputs are the same
two four-state obstructions and low-cost 3+5 structural facts. No 256-event
enumeration, author verifier or LP is run. Stop after this one guarded run.
