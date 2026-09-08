# D10-S5 revised recheck

Date: 2026-09-08. STATUS: **CORRECT for the revised gradient conversion and
unchanged local full-Hessian certificate; finite optimization remains SCOUT.**

The initial report and its hash-bound evidence are preserved. Its conditional
INCORRECT finding about the Frobenius gradient applied to the original source
hash. That defect is now repaired in the revised source below.

## Frozen revised author hashes

`full_psd_hessian.py`:
`92697514aeaa7c40c5ed8bd21137635f7aa5033698b7a0e7793b6c8b9df38166`

`hessian_scout.json`:
`b2ce1b3d4ebf6cb8c4eecad86587cae04a84b32fe18e0aa0f198738c260fac7f`

The JSON is byte-identical to the initially audited output despite the rerun;
this is consistent with its best retained point still coming from the unchanged
rank-one scan. All six author-file hashes were checked before and after this
recheck, with no drift. Full hashes are in `revision_results.json`.

## Gradient repair

The source now copies g=2Ax, multiplies coordinates 3: by 0.5, and only then
constructs the symmetric matrix G. Thus the diagonal entries are g_ii and
off-diagonal entries are g_ij/2, exactly as required by

    df(D)[E] = g dot x(E) = <G,E>_F.

The new source ordering was checked structurally. An independent calculation
of this identity for all six basis perturbations at a deterministic point
returned zero discrepancy. The former factor-of-two issue no longer applies.
This repairs the gradient, not a general convergence guarantee: the fixed
step schedule and finite projected search still do not certify an optimizer.

## Full replay of frozen scout parameters

An independently written replay, without importing the author's Hessian or
search module, ran seed 20260908 with 4000 rank-one proposals and 400 projected
starts of 300 steps (120000 projected updates), using the corrected Frobenius
gradient. Its best value was -2.285098038212576, exactly the saved scalar
result, and the best matrix matched within 1e-13. The best still came from
the rank-one scan. These are the complete replay denominator and provenance,
not a global PSD-cone optimization certificate.

## Core certificate rechecked

The original independent multivariate-polynomial/Mobius calculation and
unscaled rational logarithm enclosure were re-executed with a new output file;
no author Hessian module was used. All eight atoms, the 6-coordinate Hessian,
D_* curvature, and the rationalized PSD point passed again. The independent
minimum Gershgorin lower bound remains exactly

    1.7200075505038613350333965767 > 43/25.

Consequently the previously certified full-space inequality remains

    H''_{K_*}[D,D] <= -(43/50)||D||_F^2, for every real symmetric D.

It includes noncommuting PSD/NSD directions. The existential open-neighborhood
consequence remains valid by matrix continuity; no numerical radius or global
concavity claim is added. The matrix discrepancy from the author remains
2.2910981477e-89, and D_* curvature remains -2.264361218158924839989580424355...

## Reproduction

Command from the repository root, local bundled Python 3.12:

```
python research/R3/deepening_10h/dense_hessian/n3_full_psd_local/verifications/revision_check.py
```

Exit 0; 2.556760787963867 seconds; no failed checks. Numerical library thread
counts were limited to one in the subprocess. New outputs are
`revision_results.json` and `revision_core_results.json`; the old audit files
were not overwritten. The core replay's historical-gradient field is explicitly
labelled historical and is not a diagnosis of the repaired code.

Replay script SHA256:
`e6f61b0961bf98dff1a1aa06b30b4ce08a2f4079d9180094a52126de1a4d7ba3`

No author file or shared index was modified. Final layered conclusion:
core theorem CORRECT; gradient correction CORRECT; reproduced finite search
SCOUT; exact PSD optimizer and global concavity remain uncertified.
