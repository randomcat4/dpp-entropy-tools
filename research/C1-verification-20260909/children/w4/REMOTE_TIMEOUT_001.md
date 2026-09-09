# Remote timeout record 001

This records the failed full-center certificate attempt and keeps it separate from later minimized checks.

- Script: `independent_w4_certificate.py`
- Runner: `run_certificate.sh`
- Remote shell PID recorded by the run: `167814`
- Resource envelope: one computational thread, no GPU, `ulimit -v 8388608`, `timeout 600`
- Exit status: `124`
- Meaning: the command hit the 600-second timeout.
- Saved stdout/stderr status at inspection: both files were empty, consistent with Python block buffering before `-u` was added.

This timeout is not mathematical evidence for or against the theorem. It only shows that the original full 16-center exact-fraction interval LDL run was too heavy for the assigned first job envelope.
