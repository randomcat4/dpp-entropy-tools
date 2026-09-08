# Main-instance execution ledger

Baseline: fa504ec74e16843fafc395880d7ba99b4c1d2129.
All mathematical jobs below ran in the owned server checkout, foreground,
one thread, no GPU. Python 3.12.3, numpy 2.1.2, scipy 1.14.1, mpmath 1.3.0.
Commands used `/opt/venv/bin/python research/N3/main/<script>` with
OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1; each script also sets
NUMEXPR_NUM_THREADS=1 through its import. All units are deterministic, with
seed null and explicit fixed input arrays. Source/dependency SHA-256 and full
actual coverage are stored in each corresponding JSON result.

| Unit | Script | PID | Executed mathematical work | Exit |
|---|---|---:|---|---:|
| U1 | conditional_score_probe.py | 157836 | 12 centers / A optimizer directions | 0 |
| U2 | projected_metric_probe.py | 158117 | 36 full projected matrices; 20 averaged failures, 14 all-three failures | 0 |
| U3 | certify_score_obstruction.py | 158279 | 1 exact rational/log certificate | 0 |
| U4 | pair_score_probe.py | 158926 | 36 reused centers; 1 all-direction projected failure | 0 |
| U5 | stationary_projection_search.py | 159277 | 512 objective calls, 0 rejections, 164 projected failures | 0 |
| U6 | certify_stationary_obstruction.py | 159559 | 1 exact optimizer interval certificate | 0 |

U5 optimizers intentionally used a bound of 128 calls each. All four reached
that bound; this is recorded as optimizer nonconvergence, not a tool failure
or a global minimum. No positive actual entropy candidate was certified.

Operational checks before execution found no owned N3 jobs and retained
other pre-existing Python processes. The first resource probe stopped early
because the baseline metadata was located at the round root rather than
inside the lane; the corrected read verified the specified baseline. The
default server Python lacked numpy, so the existing `/opt/venv` environment
was used. These checks executed no mathematical centers. An initial local
Git commit failed because no author identity was set; the same staged files
were committed using an explicit per-command identity. No mathematical run
was repeated because of this administrative failure.

All reports were explicitly copied from the owned server output directory.
No server credentials or private handoff contents are included. No other
route's jobs, files or environment were modified. Separate child and reviewer
execution records retain their own runs and coverage rather than inflating
the number of distinct centers in this ledger.
