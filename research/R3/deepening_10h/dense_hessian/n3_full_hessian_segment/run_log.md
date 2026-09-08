# D10-S8 run log

AUTHOR STATUS: PROOF_CANDIDATE_PENDING_FRESH_REVIEW.

No server was used.  No GPU was used.  No system dependencies were installed.
BLAS/OpenMP thread environment variables were set to `1` for the final Python
run.  No randomness is used in the certificate.

## Files read

- `repo/AGENTS.md`
- `dense_hessian/commuting_spectral/n3_complement_barrier_refine/frozen_problem.md`
- `dense_hessian/commuting_spectral/n3_complement_barrier_refine/proof_or_blocker.md`
- `dense_hessian/commuting_spectral/n3_complement_barrier_refine/run_log.md`
- `dense_hessian/commuting_spectral/n3_complement_barrier_refine/verifications/fresh_audit.md`
- S5 `n3_full_psd_local/full_psd_hessian.py` for the prior single-point
  exact-event/log-interval pattern

## Final command

From the repository root:

```powershell
$env:OMP_NUM_THREADS='1'; $env:OPENBLAS_NUM_THREADS='1'; $env:MKL_NUM_THREADS='1'; $env:NUMEXPR_NUM_THREADS='1'; & 'C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'research\R3\deepening_10h\dense_hessian\n3_full_hessian_segment\segment_hessian_certificate.py'
```

Exit code: `0`.

Output summary:

```json
{
  "status": "PROOF_CANDIDATE_PENDING_FRESH_REVIEW",
  "largest_certified_radius": "6/25",
  "largest_certified_interval": ["-6/25", "6/25"],
  "largest_certified_min_margin_decimal": "0.0002662575324700432790390645911",
  "largest_certified_min_atom_lower": "63029/5000000"
}
```

The full output is saved in `segment_certificate.json`.

## Expansion ledger

Final scripted attempts:

| radius | result | pass leaves | failed leaves | spectral margin |
|---:|---|---:|---:|---:|
| `1/100` | certified | 8 | 0 | `29/150` |
| `1/50` | certified | 16 | 0 | `14/75` |
| `1/20` | certified | 32 | 0 | `1/6` |
| `1/10` | certified | 62 | 0 | `2/15` |
| `1/5` | certified | 142 | 0 | `1/15` |
| `6/25` | certified | 173 | 0 | `1/25` |
| `49/200` | certificate failed | 174 | 10 | `11/300` |
| `1/4` | certificate failed | 175 | 20 | `1/30` |

Additional manual boundary probe before final scripting:

- `21/100`, `11/50`, `23/100`, and `6/25` passed at `log_terms=20`,
  `max_depth=10`.
- `49/200` failed again at `max_depth=12` with `181` passed leaves and `29`
  failed leaves.
- `1/4` failed at `max_depth=14` despite positive float grid eigenvalue.

These failures are failures of the current rational-interval/Gershgorin
certificate, not counterexamples.

## Sanity checks

The final script checked, as exact polynomial identities:

- atom probabilities sum to one along the whole line;
- all first total-mass derivatives vanish;
- all bilinear second total-mass derivatives vanish.

Float grid probes on failed radii:

- at `49/200`, the worst sampled minimum eigenvalue of `B=-Hess H` was about
  `0.7183236368`;
- at `1/4`, the worst sampled minimum eigenvalue of `B=-Hess H` was about
  `0.7175799845`.

The float probes are attack diagnostics only and are not used to certify the
continuous theorem.
