# One non-scalar all-direction Hessian box

The final computation certifies only `R12_boundary_mid` at six-coordinate radius `1/2048`, as stated in `RESULT.md` and `frozen_scope.md`. The complete successful server run is `server_output/run_20260909T071241Z_pid169650/`, with its invocation metadata, log and exit code alongside in `server_output/server_invocations/`.

From this directory, using Python 3.12 and numpy:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 scripts/strict_hessian_certificate.py --input inputs.json --output-root /tmp/c2_hessian_box --radius-plan server_radius_plan.json --only-center R12_boundary_mid --max-attempts 1
```

`inputs.json` fixes the exact U, the original 12 centers, and the radius schedule. The final command selects one of those centers; the final scope does not cover the other eleven. It uses the frozen 96-term rational logarithm enclosure. The result is an all-position/all-direction interval certificate for the selected box, not a pointwise floating Hessian test.

The checkpoint and summary store the rational preconditioner and outward decimal rational bounds for the full matrices, event probabilities and Gershgorin rows. These are backed by exact rational interval operations with explicit log tails; decimal display precision does not change the underlying proof comparisons. See `certificate_method.md` and the independent review in `../hessian_review/`.

The independent main-instance event reconstruction is checked against the final selected-center jets with:

```sh
python3 ../compare_event_implementations.py --reference ../main_output/independent_centers.json --candidate server_output/run_20260909T071241Z_pid169650/center_event_jets.json --allow-subset --output /tmp/c2_final_jet_comparison.json
```

That check passed on the server for all 896 rational event/gradient/Hessian values at this center. It supports implementation correctness and is not itself the box-sign proof.

`debug_records/` contains local implementation logs only. Earlier `server_output/` runs preserve interruptions and the checkpoint exception. Their intermediate ACCEPTED rows are not final certificates. Their original pre-fix code versions were not all frozen; no reproducibility or acceptance claim is made for those intermediate statuses. The official final source and complete output are the accepted candidate.

The corrected attempt ledger is in `attempt_accounting.json`: 73 distinct recorded attempts, conservatively charged as 87 status records out of 128. The correction affects accounting only, not the certificate.

An independent exact check of the persisted outward Hessian bounds and rational preconditioner is also supplied:

```sh
python3 ../check_persisted_box.py --certificate server_output/run_20260909T071241Z_pid169650/certificate.json --output /tmp/c2_persisted_box_check.json
```

That server check recomputed the congruence directly from the saved rational decimal endpoints and found every Gershgorin margin above 1/10. True-Hessian containment still relies on the independently audited interval/log algorithm. This margin is in preconditioned coordinates and is not asserted as a Frobenius curvature constant in the original coordinates.
