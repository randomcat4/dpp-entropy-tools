# Provenance

Task: PR43 `CODEX_VERIFICATION_TASKS_v2.md` task D only.

Frozen source commit: `4e1369ef2a59ccfaba3ca8fce95d85e78857bf78`.

Author role: this unit reconstructed the exact task-D input, built the directed/nonreversible stationary-flow LP, discovered a feasible numerical basis with SciPy, recovered an exact rational flow with SymPy, and wrote the portable standard-library verifier.

Verification role: this unit also ran the exact verifier on its own candidate, both on the C2 server and locally. That is a self-check, not independent acceptance.

Frozen candidate files for review:

- `instance.json`
- `flow_certificate.json`
- `verify_pr43_flow.py`
- `discover_pr43_flow.py`
- `verify_local_summary.json`
- `verify_final_summary.json`
- `REPORT.md`

Private run metadata and raw server logs are stored outside the public artifact set under `runs/C2/verification3/pr43_flow`.

No task E/F computation, counterexample search enlargement, commit, PR publication, or author-source edit was performed.
