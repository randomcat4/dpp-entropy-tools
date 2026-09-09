# Independent interval-certificate review

`REVIEW.md` is the unchanged initial INCOMPLETE report. It found missing persisted author certificates; intermediate accepted decimal summaries were not enough for acceptance. The reviewed prior source is retained at `server_author_snapshot/strict_hessian_certificate.py`.

`REVIEW_single_box_R12_boundary_mid.md` is the unchanged directed follow-up, ACCEPTED_SCOPED for exactly one non-scalar box after persistence was repaired. Its reference to `hessian_scope.md` maps to the public frozen statement at `../hessian/frozen_scope.md`. Source line numbers and blob bindings remain unchanged. References to the author final run map to `../hessian/server_output/run_20260909T071241Z_pid169650/`; the duplicate private fetched copy is not needed.

The new nonauthor replay used the same final source/input, one center, one radius, 96 log terms and `--write-exact-gershgorin`. It exited 0. Its complete exact-row certificate is at `remote_single_exact_output/output/run_20260909T071634Z_pid169870/certificate.json`. Exact fraction strings are long; Python readers may need `sys.set_int_max_str_digits(0)` before converting the strings to integers. The duplicate full checkpoint and duplicate center-jet file are omitted here because the complete certificate and official author checkpoint are already included.

Reproduce from this directory:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 remote_single_exact_output/strict_hessian_certificate.py --input remote_single_exact_output/inputs.json --output-root /tmp/c2_independent_box --radius-plan remote_single_exact_output/server_radius_plan.json --only-center R12_boundary_mid --log-terms 96 --max-attempts 1 --write-exact-gershgorin
```

`remote_output/` retains the earlier bounded smoke result (exit 2 because only a partial requested-center batch was completed). It is not the final accepted candidate. No other centers, full spectral band, novelty or Lean formalization are certified.
