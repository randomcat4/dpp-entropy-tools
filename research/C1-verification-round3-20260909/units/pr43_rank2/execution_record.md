# Execution record for independent PR43 rank-two check

No arithmetic rerun was performed while writing this record.

## Locations

- Local review directory: `this unit directory`
- Server run directory: `[isolated owned execution directory]`
- Script: `independent_pr43_rank2_check.py`
- Input: `continuation_fixture.json`
- Output: `exact_check_output.txt`

## Retained command record

File: `exact_check_command.txt`

The command record was saved as line-separated tokens:

```text
OMP_NUM_THREADS=1
OPENBLAS_NUM_THREADS=1
MKL_NUM_THREADS=1
NUMEXPR_NUM_THREADS=1
timeout
600
/opt/venv/bin/python
independent_pr43_rank2_check.py
continuation_fixture.json
```

## Time record

- Started: `2026-09-09T10:17:15+00:00`
- Finished: `2026-09-09T10:17:19+00:00`

## Runtime versions from output

```text
python=3.12.3 platform=Linux-6.8.0-79-generic-x86_64-with-glibc2.39
sympy=1.13.3 numpy=2.1.2 mpmath=1.3.0
```

## PID provenance

- Runner shell PID: unavailable.
- Python child PID: unavailable.
- Retained file `exact_check_shell.pid` is polluted and contains only bytes `5c 0a`, i.e. a backslash followed by newline. It is not a numeric PID.
- A later process check found no active process in the assigned server directory.

## Exit provenance

- Original wrapper exit file: `exact_check_exit.txt`.
- Original wrapper exit content is polluted and contains only bytes `5c 0a`, i.e. a backslash followed by newline. It is not a numeric exit code.
- The Codex command wrapper itself returned failure after the Python output because the final shell `exit` received the polluted backslash value and printed `exit: \\: numeric argument required`.
- This wrapper failure happened after `exact_check_output.txt` had been written and printed.

## Corrected verification

File: `exact_check_verified_exit.txt`

Value:

```text
0
```

Reason: `exact_check_output.txt` reaches the final line

```text
ALL INDEPENDENT PR43 RANK-TWO CHECKS PASSED
```

The correction records that the saved mathematical check output reached its own PASS terminus. It does not replace the polluted wrapper-exit evidence; both are retained.
