# Execution coverage and verification boundaries

Counts below distinguish unique mathematical objects from repeated verification. All floating calculations remain diagnostics even where an event is called an exact event (a fully specified binary configuration).

| Work | Distinct centres/chords | Windows or past lengths | Actual author coverage | Kind |
|---|---:|---|---:|---|
| Main B1 | 1 | window 6, 8 | 2 full Hessians; 1,280 event evaluations including the three endpoint/centre entropy distributions | floating |
| Phase coefficient unit | 12 | window 6, 8 | 24 full Hessians; 3,840 event determinant/inverse evaluations | floating |
| Phase spectral-factor unit | 6 | window 6, 8 | 12 full Hessians; 1,920 event determinant/inverse evaluations | floating |
| B1 rate precheck | same B1 | past 4, 6, 8, 10 | 288, 1,152, 4,608, 18,432 event evaluations, respectively | floating, using the separately authored outer-factor method |
| B1 boundary certificate | same B1, 3 symbols and 2 complement choices each | residual support 64 | 6 kernels; 1,206 exact complex residual entries | rational residual bounds |
| B1 rate certificate | same B1 | past 4 | 288 exact rational event determinants and interval logarithms | strict three-symbol rate gap |

Thus the phase search did not run window ten. The fixed B1 rate precheck did run past length ten; it is not a new centre, a full-Hessian search window, or the final strict rate calculation. The strict calculation stopped at past length four because it already separated zero.

The independent B1 reviewer rebuilt the window-six/eight calculations using a separate implementation; these repeated objects add no unique centres. Main integration also replayed all 36 phase Hessians with the frozen author programs. Their complete numerical result arrays agreed exactly under the same server runtime. That replay adds 5,760 repeated event evaluations, not 36 new search matrices. See [replay record](main/phase_replay.json).

The [exact distinctness record](main/integration_check.json) checks that all 19 triples of mean, Fourier degree and positive-frequency squared magnitude sum differ. Each triple is invariant under translation and conjugation, so no two of the counted centres are related by those operations. This exact identity check does not certify a Hessian sign.

The finite proof, numerical replication and strict rate certificate have separate audit records in [review](review/). They are not multiple independent reviewers merely because the same reviewer produced more than one report. No positive counterexample, continuous-family exclusion or novelty certification is inferred from these counts.
