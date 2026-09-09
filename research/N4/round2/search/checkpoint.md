# Search checkpoint

Status: **STOPPED_SUBSTANTIVE**. F1 and F2 are complete. No third batch,
dimension increase, child agent, issue or PR was started by this search task.
No server research job remains alive.

| Work unit | Centers attempted/completed | Full 6D Hessians | Frozen rational directions with chords | Chords | Failed centers | Positive numerical candidates |
|---|---:|---:|---:|---:|---:|---:|
| F1, n4 rank3 | 72/72 | 72 | 72 | 216 | 0 | 0 |
| F2, n5 rank3 | 24/24 | 24 | 48 | 144 | 0 | 0 |
| Total | 96/96 | 96 | 120 | 360 | 0 | 0 |

F1 PID 161087 exited 0 after 5.626 seconds. F2 PID 161588 exited 0 after
6.512 seconds. Both processes were checked absent afterward. All OMP,
OpenBLAS, MKL and NumExpr thread settings were one; no GPU was used.
Additional eigenvector/layer diagnoses only read saved Hessians/event jets;
they add no center, entropy or determinant calls. Source hashes, dependency
versions, seeds and individual counters remain in each original manifest.

F1's weak curvature is dominated by nearly coordinate geometry with both
Fisher and acceleration negative. F2 genuinely breaches the top-only
geometry/Fisher budget in 10 noncommuting directions, including 4 on the
certified baseline frame; lower layers still compensate. In the opposite
regime, top-layer negativity compensates positive lower-layer contributions.

`F2/selected_mechanism_cases.json` freezes exact U,A,V,t for the strongest
geometry-budget failure and highest total curvature, with both the globally
allocated layer contributions C_k and literal subentropy second derivatives
H_k''=C_k-P_k''. This distinction corrects the initially abbreviated layer
terminology; the full Hessian and all signs of total curvature were unaffected.

Remaining mathematical obligation: prove the coupled all-layer inequality
for the full frozen scope, or exhibit a strictly positive rational finite
chord and certify its strict-kernel lift. The reports spell out the still
equivalent inequality, without presenting it as a new proved lemma. No
finite non-hit, budget failure, or source normalization check resolves it.

Local work is confined to branch `research/N4-r2-search` and
`research/N4/round2/search/`. Local and server commits may differ, so compare
the search subtree hash rather than rewriting either history.
