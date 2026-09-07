# R1 P2-01 final result

STATUS: INCOMPLETE

The same registered formal batch completed normally: **42,578 objective calls, all 64 restarts, zero formal numerical failures, and zero values above the 1e-6 promotion threshold**. The actual subprocess exit code was 0. The worker and supervisor both exited. No new job, resumption, or budget extension occurred during monitoring.

This is a finite non-hit, not an exclusion theorem for general real-symmetric kernels. Small positive values at floating-point zero were not promoted.

## Actual denominators

The formal seed was 20260908210. Each call computed the full real-symmetric Hessian and its largest eigenpair at a spectral-parameter kernel. The columns below are **actual minimum spectral-margin bands**, not merely nominal regularization parameters.

| n | (0.2,0.4) | (0.05,0.2) | (0.01,0.05) | (0.001,0.01) | Total |
|---|---:|---:|---:|---:|---:|
| 3 | 446 | 509 | 230 | 797 | 1982 |
| 4 | 1189 | 1221 | 1182 | 1104 | 4696 |
| 5 | 1414 | 1500 | 1486 | 1500 | 5900 |
| 6 | 1500 | 1500 | 1500 | 1500 | 6000 |
| 7 | 1500 | 1500 | 1500 | 1500 | 6000 |
| 8 | 1500 | 1500 | 1500 | 1500 | 6000 |
| 9 | 1500 | 1500 | 1500 | 1500 | 6000 |
| 10 | 1500 | 1500 | 1500 | 1500 | 6000 |
| Total | 10549 | 10730 | 10398 | 10901 | 42578 |

The 64 restarts ended as follows: 15 optimizer-convergence terminations and 49 registered per-restart call-limit terminations. Each of the latter had a 750-call limit. The total did not reach the 48,000-call ceiling because converged restarts stopped early. The unspent 5,422 formal calls were not reallocated.

These are objective-call counts, including finite-difference optimizer calls and possible repeated parameter values. Unique call IDs do not assert that all matrices were distinct.

The separate validation denominator was 823 attempts, including two preserved pre-stabilization failures. Thus the actual second-stage total was **43,401 attempts**: 42,578 formal plus 823 validation. The complete validation list remains in `validation_ledger.json`; its failures are not silently removed.

## Best recorded object

The global best object is in `formal_final/best.json` and the full audit. It occurred at call 32449, n=3, band (0.001,0.01), restart 1, using the upper-endpoint orientation and complement-stabilized Mobius evaluation.

- Largest Hessian eigenvalue: 5.930937647366978e-15.
- Alternate directional formula: 8.881784197001252e-16.
- Eigenvector residual: 6.0037609269151225e-15.
- Frobenius norm of V: 1.
- Actual spectral margin: 0.0066515971422715925.
- Smallest complete-event probability: 6.597633953642937e-5.

The estimated eigenvalue is at the scale of its eigenvector residual and far below the promotion threshold. Its spectrum is approximately (0.8757896226394173, 0.9201445801599365, 0.9933484028577284), and the kernel is close to a 1+2 block decomposition. It is an optimization endpoint, not a counterexample.

The two recorded feasible numerical chords gave:

| t | Delta = average endpoint entropy minus midpoint entropy | Minimum endpoint spectral margin |
|---:|---:|---:|
| 0.00047033894450213036 | -1.138755756358023e-12 | 0.006651320067137645 |
| 0.0018813557780085215 | -2.9154478831117103e-10 | 0.0066471635500175985 |

These floating-point gap values are not rigorous interval certificates. No object reached the numerical-candidate gate, so none was promoted for independent counterexample certification.

## Ledger and terminal-process audit

The final SQLite audit found exactly 42,578 rows and 42,578 distinct IDs, with minimum ID 1 and maximum ID 42578. The durable spent counter was also 42,578. All rows were OK; FAILED=0, RESERVED=0, INTERRUPTED_UNKNOWN=0. SQLite `quick_check` returned `ok`. The full final failure list is empty.

The stopped SQLite ledger remains in the task's remote `formal/state.sqlite`. Its SHA256 is `91580af731055418d4ff81314a014fca17e61f3c03240a8d581c0d36b916ec2e`; its WAL was zero bytes when this hash was collected. The approximately 64 MiB raw ledger is retained there. Local compact evidence is `final_audit.json` and `final_ledger_audit.json`, with complete state counts, per-cell results, restart reasons, and the full best object.

The program reported 705.8111944198608 seconds elapsed wall time. The supervisor measured 705.912392616272 seconds from child launch to exit. The original absolute deadline remained epoch 1788811983.331578, or 2026-09-07 20:13:03.331578 UTC; no recovery changed it. The batch finished well before this 5,400-second ceiling.

The actual supervisor-recorded child exit code was 0. Final read-only process checks found that worker PID 141145 and supervisor PID 141144 no longer existed in `/proc`; a separate process listing returned no matching rows. There is **no surviving job to continue**.

## Validation and reproducibility

The probability pipeline differentiates inclusion determinants and applies Boolean Mobius inversion to full-event probabilities and first/second derivatives. For high occupancy it uses the exact complement identity, including the first-derivative sign change, and maps events back. The signed-determinant formula is only a diagnostic.

The local 43-call stabilized self-test passed all 32 stratum/orientation examples, complete-event mapping, entropy identity, gradient reversal, mass checks, and finite differences. The final local pause/resume test used exactly 17+47 calls and IDs 1 through 64. The remote self-test also passed, and the remote optimizer pilot completed 512 calls with zero failures and exit code 0. Their compact records and the preserved original failure are linked in `validation_ledger.json`.

Local validation used Python 3.12.14 and NumPy 2.3.5. The remote existing environment used Python 3.12.3, NumPy 2.1.2, and SciPy 1.14.1. The formal worker used one numerical CPU thread, no GPU, and a 12 GiB address-space ceiling. The source/configuration hashes are frozen in `formal_final/config.json`.

The executed command, from the remote phase2 task directory, was:

```text
/opt/venv/bin/python engine.py --out formal --mode formal --seed 20260908210
```

It was launched and supervised by `/opt/venv/bin/python launch_phase2.py`. This command is recorded for reproducibility; the existing formal run is terminal and must not be restarted or given more budget. Source copies and historical startup instructions are retained in `launch_record.md`.

## Files

- `formal_final/summary.json`: final search status and per-cell denominators.
- `formal_final/process_exit.json`: actual subprocess return code and launch/end timestamps.
- `formal_final/best.json`: complete best K,V, parameters, spectrum, and chords.
- `formal_final/checkpoint.json`, `formal_final/config.json`: terminal checkpoint and immutable configuration.
- `final_audit.json`, `final_ledger_audit.json`: SQL/process audit and compact summary.
- `validation_ledger.json`, `initial_failure_audit.json`, `selftest_result.json`, `remote_selftest_result.json`, `checkpoint_audit_final.json`, `remote_pilot_summary.json`: separate validation evidence.
- `plan.md`, `numerics.py`, `engine.py`, `launch_phase2.py`: mathematical computation and durable bounded-run implementation.

No heartbeat was created by this subtask. The R1 parent was notified that the registered job is now complete and requires no resumption.
