ACCEPTED_SCOPED

Official server certificate: one non-scalar finite coordinate box.

- Center: `R12_boundary_mid = R12 diag(1/4,1/2,3/4) R12^T`.
- Center coordinates `[a11,a22,a33,a12,a13,a23]`: `[41/100,17/50,3/4,-3/25,0,0]`.
- Box radius: `1/2048` in every coordinate.
- Whole-box spectral envelope: `[509/2048, 1539/2048]`, so the entire box is inside `0 < A < I`.
- The whole box is not claimed to lie inside `1/4 I <= A <= 3/4 I`; the center lies in that band, so the target-band intersection is nonempty.
- The certificate covers all real symmetric directions `V`.
- Minimum positive event lower bound: event `245`, lower `110463061471749/45802848256000000` (about `0.0024117072557224375`).
- Preconditioned strict Gershgorin margins: approximately `[0.6583454625, 0.5956966167, 0.4842866322, 0.4998976543, 0.1229140912, 0.3194926304]`.

Official server outputs:

- Server run mirror: `server_output/run_20260909T071241Z_pid169650/`
- Certificate: `server_output/run_20260909T071241Z_pid169650/certificate.json`
- Accepted checkpoint: `server_output/run_20260909T071241Z_pid169650/accepted_box_attempt_001_R12_boundary_mid.json`
- Run result: `server_output/run_20260909T071241Z_pid169650/RESULT.md`
- Invocation metadata/log/exit: `server_output/server_invocations/minimal_nonscalar_20260909T071241Z.*`

Method and scripts:

- Method: `certificate_method.md`
- Frozen inputs: `inputs.json`
- Budget and attempt ledger: `budget.md`, `server_radius_plan.json`
- Strict script: `scripts/strict_hessian_certificate.py`
- Server runner: `scripts/run_server_minimal_nonscalar.sh`

Local `output/run_*` directories are implementation debugging records only. They are not official server certificates. The interrupted server runs without final certificates are retained as failed/incomplete attempts, not as accepted final outputs.

This scoped certificate is not a proof over the entire matrix spectral domain.
