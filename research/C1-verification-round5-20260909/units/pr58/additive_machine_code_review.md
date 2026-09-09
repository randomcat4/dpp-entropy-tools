# PR58 / PR76 additive machine code review

Overall static-code verdict: `ACCEPTED_SCOPED` for the PR76 checker as a first-mismatch detector and retained-evidence generator. It is not a proof that all original PR58 literal additive claims pass, because it correctly stops with `LITERAL_BOUND_CERTIFIED_FALSE` at author equation (3.5), and because its run-labelled `W` is the request's `V=E_mu[y psi]`, not the author `W=E_mu[b psi]`.

No C1 execution, arithmetic rerun, SymPy run, test, formal check, or numerical reconstruction was performed.

Unless a longer alias is written explicitly, source paths below are under `source-snapshots/pr76_additive/`.

## Dependency and isolation review

Verdict: `CORRECT / ACCEPTED_SCOPED`.

The independent checker imports only standard-library modules and `Fraction` at `source-snapshots/pr76_additive/implementation/independent_pr58_additive52_checker.py:8-14`. It rejects JSON floats at `implementation/independent_pr58_additive52_checker.py:94-98`. The run metadata records `runtime_dependency` as Python standard library only and says the author checker was not read/imported/executed at `outputs/run01/00_metadata.json:2-31`.

The run guard records one 600-second budget window, a single active owner lock, one-thread environment variables, a 16 GiB virtual-memory cap, CPU pinning, timeout execution, and exit-code capture at `execution/run_guard.sh:21-53`. The run ledger records one launch, no repair, no retry, exit code 20, and no live arithmetic after completion at `execution/RUN_LEDGER.json:17-31` and `execution/RUN_LEDGER.json:50-61`.

## Binding and literal-input review

Verdict: `CORRECT / ACCEPTED_SCOPED`.

The checker freezes the expected author commit and target decimals at `implementation/independent_pr58_additive52_checker.py:20-34`. It requires the input binding and checks the observed source commit against the frozen commit at `implementation/independent_pr58_additive52_checker.py:205-238`.

The literal inputs are in the checker source, not imported from author code. The output packet records the matrix/table literals and frozen commit at `outputs/run01/01_literal_inputs.json:1-62` and `outputs/run01/01_literal_inputs.json:260-348`. This matches the stated independent-source construction role.

## Event, cancellation, and form implementation

Verdict: `CORRECT / ACCEPTED_SCOPED` as static source, with raw artifact support.

The checker uses the requested row-major mask order: `S_mask` outer loop, `T_mask` inner loop, event index `8*S_mask+T_mask` at `implementation/independent_pr58_additive52_checker.py:893-899`. It checks event-polynomial shape, constant/product marginal agreement, positivity of `q` and `P`, and stores all event cores at `implementation/independent_pr58_additive52_checker.py:900-995`. The raw event artifact records 64 events with all `q` and all probabilities positive at `outputs/run01/04_events.json:2-4`, with event 0 and event 63 present at `outputs/run01/04_events.json:43` and `outputs/run01/04_events.json:8096`.

The cancellation routine checks total probability, fixed marginals, conditional `a/b` cancellations, log-coefficient cancellations, and dual row/column sums at `implementation/independent_pr58_additive52_checker.py:999-1066`. The raw cancellation artifact records zero dual row/column sums and total probability one at `outputs/run01/05_cancellations.json:138-157` and `outputs/run01/05_cancellations.json:294-297`.

The form routine builds `P0`, run-labelled `W`, direct curvature, `sum_cpsi`, `A2`, and the dual denominator, then checks the direct form against `P0+A2+W` in run labels at `implementation/independent_pr58_additive52_checker.py:1069-1121`. The raw forms artifact stores the combined curvature form, exacts, and forms at `outputs/run01/06_forms.json:2`, `outputs/run01/06_forms.json:266`, and `outputs/run01/06_forms.json:276`.

## Rational interval engine review

Verdict: `CORRECT / ACCEPTED_SCOPED`.

The log enclosure code requires `0 <= r < 1`, uses a rational atanh partial sum plus nonnegative tail bound, and builds `log 2` through the same `r=1/3` mechanism at `implementation/independent_pr58_additive52_checker.py:538-614`. General logs are range-reduced with powers of two and then recombined using signed exact interval scaling at `implementation/independent_pr58_additive52_checker.py:617-639`.

The interval primitives handle signed scaling, positive-denominator division, and squaring with zero-crossing cases at `implementation/independent_pr58_additive52_checker.py:558-584`. Scalar assembly uses those primitives for `P0`, run-labelled `W`, direct curvature, `sum c psi`, `L`, `T`, and true curvature at `implementation/independent_pr58_additive52_checker.py:701-714`. The preceding form checks require positive `A2` and positive dual denominator at `implementation/independent_pr58_additive52_checker.py:1111-1121`, so the divisions used for `L` and `T` are guarded.

The outward decimal and comparison layer also reads correctly in source: floor/ceil decimal rendering is exact rational endpoint conversion at `implementation/independent_pr58_additive52_checker.py:118-144`; target decimals are parsed exactly at `implementation/independent_pr58_additive52_checker.py:654-662`; and interval comparisons distinguish PASS, certified-disjoint false, and insufficient precision at `implementation/independent_pr58_additive52_checker.py:665-690`. I found no static source bug in this enclosure engine.

## Comparison and stop-gate implementation

Verdict: `CORRECT / ACCEPTED_SCOPED` for detecting the first false literal bound.

The comparison routine builds qualitative checks and the ordered literal comparisons for equations (3.4)-(3.7) at `implementation/independent_pr58_additive52_checker.py:786-827`. The run loop writes scalar and comparison artifacts before selecting the first non-pass, and it raises `LITERAL_BOUND_CERTIFIED_FALSE` when the first literal failure is disjoint from the target at `implementation/independent_pr58_additive52_checker.py:1214-1253`. The exception path writes `final.json` and returns the failure exit code at `implementation/independent_pr58_additive52_checker.py:1292-1309`.

The retained raw comparison artifact shows (3.4) PASS, (3.5) `CERTIFIED_FALSE_DISJOINT`, run-labelled (3.6) `CERTIFIED_FALSE_DISJOINT`, and (3.7) PASS at `outputs/run01/08_comparisons_N80.json:2-113`. The final artifact records (3.5) as the first failure and status `LITERAL_BOUND_CERTIFIED_FALSE` at `outputs/run01/final.json:3-34`; `exit.json` records exit code 20 at `outputs/run01/exit.json:1`.

## Known W/V limitation

Verdict: `CRITICAL_GAPS / INCOMPLETE` for author-W literal verification, but not a C2 implementation defect for the launched request.

The original request asked the checker to compute `W=E_mu[y psi]` at `inputs/REQUEST.md:24-28`. In the source, `y=s^2 b`, and the run-labelled `W` terms are built from `y` at `implementation/independent_pr58_additive52_checker.py:939-947` and `implementation/independent_pr58_additive52_checker.py:1087-1088`. The correction note later states that this field is actually `V=E_mu[y psi]=s^2 W_author`, and that author `W=E_mu[b psi]` is not certified by this run at `execution/CONTRACT_CORRECTION.md:5-13`.

A corrected future checker or packet should either rename this field to `V` throughout and add a separate exact `W_author=E_mu[b psi]` scalar/comparison, or provide a separately certified exact scaling comparison from `V` to author `W`. Until then, the code supports the qualitative `V<0` evidence and the true-curvature identity in run labels, but not the printed author-W decimal in equation (3.6).

## Actionable code-review conclusion

No source-code change is requested to PR76 as an evidence packet: it faithfully preserves the stopped first mismatch. For any repaired author text that keeps literal (3.6), the next evidence packet must include a corrected author-W comparison and should not reuse the run01 `W` field name without explanation.
