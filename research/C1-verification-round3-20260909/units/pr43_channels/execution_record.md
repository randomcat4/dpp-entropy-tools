# Execution record for `short_exact_checks.py`

This record was added after the arithmetic run, at parent request. No arithmetic was rerun while preparing this file.

## Scope

- Current report-binding commit: `7bd5962bbb2020ce47fbe286adda7dfe02f9645d`.
- Historical unchanged proof/code/input commit: `4e1369ef2a59ccfaba3ca8fce95d85e78857bf78`.
- Local owned directory: `this unit directory`.
- Server owned directory: `[isolated owned execution directory]`.
- Arithmetic script: `short_exact_checks.py`.
- Runner script: `run_short_checks.sh`.

## Pre-run failed launch attempt

Before creating `run_short_checks.sh`, I attempted one inline remote shell launch that failed before running the arithmetic script.

- Persisted command file: unavailable; the failed command was not written to disk.
- Persisted PID: unavailable.
- Persisted start/end/elapsed: unavailable.
- Tool-level exit code: `1`.
- Tool-level stderr summary: `bash: -c: line 8: syntax error: unexpected end of file`.
- Arithmetic rerun impact: none; the syntax error happened in the outer shell before `short_exact_checks.py` executed.

## Successful outer launch

Exact outer launch command used:

```text
[Private transport command omitted; execution result retained.]
```

Execution guard actually retained in the command:

- SSH connection guard: `BatchMode=yes`, `ConnectTimeout=10`.
- Thread guard: unavailable; no `OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, or equivalent was retained in the launch command.
- Memory guard: unavailable; no `ulimit` or cgroup memory guard was retained in the launch command.
- Time guard: unavailable; no `timeout` wrapper was retained in the launch command.
- Planned limits from `COMPUTE_PLAN.md`: one numerical thread, 8 GiB effective ceiling, 600 seconds per job. These were planning constraints, not enforced by the successful launch command.

## PID and timing provenance

- Runner PID: unavailable; the runner did not record `$$`, and no PID file was written.
- Python child PID: unavailable; the Python process did not record its PID.
- Version-record timestamp: `2026-09-09T10:17:55+00:00` from `short_exact_checks.version.txt:1`.
- Arithmetic start timestamp: `2026-09-09T10:17:56+00:00` from `short_exact_checks.out:1`.
- Arithmetic end timestamp: `2026-09-09T10:17:56+00:00` from `short_exact_checks.out:19`.
- Elapsed time: less than one second at the recorded timestamp resolution; exact subsecond elapsed time unavailable.

## Exit provenance and outputs

- Script-level exit code: `0`, recorded as `EXIT_CODE=0` in `short_exact_checks.out:20`.
- Tool-level outer SSH launch exit code: `0` in the execution transcript; not separately persisted on disk.
- `short_exact_checks.out`: copied back locally, 1174 bytes.
- `short_exact_checks.err`: copied back locally, 0 bytes.
- `short_exact_checks.version.txt`: copied back locally, 78 bytes.
- `short_exact_checks.version.err`: copied back locally after parent request, 0 bytes.

Version output:

```text
2026-09-09T10:17:55+00:00
Python 3.12.3
sympy 1.13.3
numpy 2.1.2
mpmath 1.3.0
```

## Remaining owned processes

Process check command used after the run:

```text
[Private transport command omitted; execution result retained.]
```

Result:

- Exit code: `1`.
- Output: empty.
- Interpretation: no remaining process matched this child server directory at check time.
