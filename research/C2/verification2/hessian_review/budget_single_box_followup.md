# Budget: directed single-box follow-up review

Scope: non-author review of the final `R12_boundary_mid` finite coordinate box only, with radius `1/2048`. This follow-up does not revisit the prior W3 report and does not expand to the other eleven centers.

Resource limits frozen for this follow-up:

- CPU: 1 counted process, BLAS/OpenMP thread variables set to 1 for server rerun.
- Memory: at most 4 GB intended use.
- GPU: none.
- Extra server computation: at most one `--only-center R12_boundary_mid` run, `--max-attempts 1`, no radius search.
- Stop condition: accept only if the official final certificate is complete and a bounded exact-row rerun with the same script/input/center/radius verifies the Gershgorin signs by exact rational fields; otherwise leave the supplement incomplete.

Actual follow-up use: one server single-box rerun with exact Gershgorin rows, PID 169870, exit code 0, stdout `STATUS ACCEPTED_SCOPED` and `OUTPUT_DIR output/run_20260909T071634Z_pid169870`.
