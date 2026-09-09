# Search-child checkpoint

State: `STOPPED_SUBSTANTIVE` for the general nonradial cross-gain search.
No automatic rerun, dimension expansion, background task, or heartbeat.
Mathematical status: `INCOMPLETE`; no real positive entropy-gap candidate.

## Retained coverage

| Unit | Retained kernel evaluations | Full Hessian calls | Entropy calls | Directions | Chords |
|---|---:|---:|---:|---:|---:|
| S1 structural 4D scout | 160 | 160 | 2080 | 320 | 960 |
| S1 self-test | 1 fixed test | 1 | 3 | 1 finite difference | 1 |
| S2 moving unequal leaf scales | 24 | 24 | 456 | 72 | 216 |
| S3 interior gain objective | 294 | 294 | 5586 | 882 | 2646 |

The research batches comprise 478 kernel evaluations and 3822 chords;
repeated optimizer starting points are included, so these are not unique-input
counts. The separate self-test brings measured full Hessian calls to 479 and
entropy calls to 8125.

Additional retained arithmetic: S1 100-digit replay, 4 directional curvatures
and 28 entropy calls; S2 80-digit replay, 2 restricted Hessians, 2 directional
curvatures and 14 entropy calls; S3 80-digit replay, 1 restricted Hessian,
1 directional curvature and 7 entropy calls; S3 event diagnosis, 1 restricted
Hessian and 16 events. These are author checks, not independent review.

Failed S3 run: PID 159210, outer exit 1, no retained cases. Its 294 objective
invocations are reconstructed from deterministic constant-penalty optimizer
control flow. Its exact Hessian/entropy counter values were lost on exception
and are excluded from measured counts. Source, traceback, original manifest,
and separate accounting remain available. One corrected run followed.

## Evidence and remaining obligation

S1 general cycle-sign/full-Hessian batch found maximum acceleration/Fisher
ratio .361822; near-zero curvature came only from a known near-product control.
S2 softening two single-column defects did not amplify the two-column gain.
S3 reached .998972, but the maximizer is dominated by the rank-one Fisher term
of `p_all=detK`, and the negative-Hessian residual after removing that term is
still numerically positive definite at 80 digits. The full top curvature is
-.547255, not a positive candidate.

The concrete remaining obligation is to show that the nonradial acceleration
is paid by Cauchy-Schwarz slack, or produce a configuration where that fails.
None of these finite samples proves a universal inequality. No new object
currently justifies further sampling of the same families or n=5--8 expansion.

## Run status and locations

Successful research PIDs 158332 (S1), 158733 (S2), and 159251 (S3) ended.
Failed PID 159210 ended. Arithmetic replays and event diagnosis also ended
with outer-shell exit 0; event-diagnostic PID was 159599. S1's outer exit
capture had a malformed suffix, explicitly documented in README; its Python
manifest self-reports completion/0. There are no active child jobs.

All artifacts are confined to `research/N4/search/` on branch
`research/N4-search-20260909`. S1 commit: `6059922`; S2 commit: `8f5bf8b`.
The final child commit contains S3, the failed-run archive, event diagnosis,
and this checkpoint. No issue/PR was posted by the child; the route owner
receives commits for integration and independent review.
