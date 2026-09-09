# PR58 joint-additive fixed witness: run01 machine notes

Status: failed run 1, exact author-literal mismatch. No repair, no retry, and no second arithmetic launch.

Run identity:

- Frozen public source: `bbc9bc19b915ebad0ea8e8bea00580d4eebc5246`
- Frozen local source: `de8bb9ff35c9b7854ef4fdb948546095647b1e6c`
- Output directory: `research/C2/pr58_additive52/outputs/run01`
- Start: `2026-09-09T16:21:24Z`
- Finish: `2026-09-09T16:22:48Z`
- Deadline: `2026-09-09T16:31:24Z`
- Wrapper PID: `174671`
- Timeout PID: `174685`
- Arithmetic PID: `174687`, absent by `2026-09-09T16:24:10Z`
- Exit: code `20`, status `LITERAL_BOUND_CERTIFIED_FALSE`

The run completed the exact layers before the stop gate:

- `SOURCE_BINDING.json` source commit matched `a4f05cc962985015b71635bf633acce9dfe76866`; required handoff files were present.
- Exact legality checks passed: `B_rank=2`, `B_dense=True`, and the Schur/complement positivity layer completed.
- Block marginals passed: `sum_p_A=1`, `sum_p_C=1`, and all complete marginal events were positive.
- Complete-event reconstruction passed: `event_count=64`, all `q` and all complete probabilities at `s=9/10` were positive.
- Fixed-marginal and dual cancellations passed: `total_P=1`, all dual row sums were zero, and all dual column sums were zero.
- Form checks passed, including the direct differentiated curvature form matching `P0+A2+V` in the run labels.
- N80 log enclosure completed with `logs=64` and `widths_ok=True`.

First ordered literal failure:

- Equation `(3.4)` passed: `L` in `[192.456447546638183766230914, 192.456447546638183766230915]`, target `L > 192.45644754663817`.
- Equation `(3.5)` failed first: `T` in `[166.441251953051540106785812, 166.441251953051540106785813]`, target `T < 166.44125195305153`. The certified interval is disjoint from the requested strict upper bound, on the false side.

Other scalar intervals computed before the ordered stop gate were preserved in raw output:

- `P0` in `[5.470160108989083549895880, 5.470160108989083549895881]`
- `A2` in `[1.008815368753038113917451, 1.008815368753038113917452]`
- Run-labeled `W` in `[-1.825377232343279850885156, -1.825377232343279850885155]`
- `direct_curvature` in `[4.653598245398841812928176, 4.653598245398841812928177]`
- `true_curvature` in `[4.653598245398841812928176, 4.653598245398841812928177]`

Qualitative comparisons in the run output passed: `L>T`, run-labeled `W<0`, and `true_curvature>0`.

C3 correction note: public issue52 comment `5605146225` at `2026-09-09T16:22:08Z` landed after launch and says the original request mislabeled `V=E[y psi]` as `W`; the correct author `W` is `E[b psi]`, with `V=s^2 W`. Therefore run01's `W` fields are the request's `V`. This does not affect `P0`, `A2`, `L`, `T`, or the first `(3.5)` discrepancy. The request-caused `(3.6)` comparison is not used as a certificate against the corrected author `W` statement, and the author `W` decimal is not certified by run01.

No rerun is warranted under this unit: the first independent author-literal bound has already been certified false at `(3.5)`.
