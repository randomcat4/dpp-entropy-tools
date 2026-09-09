# PR58 / PR76 additive finite-evidence review

Overall verdict: `CRITICAL_GAPS / NEEDS_FIX` for the PR58 additive section as a literal numerical certificate. The retained PR76 evidence certifies that author equation (3.5) is false at the printed decimal upper bound: the author states `T < 166.44125195305153`, while PR76 retains an outward interval for `T` entirely above that value.

The same packet does support a scoped qualitative finite witness: legality, the 64 complete events, cancellations, the dual lower bound, the qualitative comparison `L>T`, and positive `t^2 I''` all survive the stopped run. Thus the additive sufficient criterion still fails/non-necessity witness survives as a finite source/evidence claim once (3.5)'s printed decimal is repaired. This is not an entropy-concavity counterexample: positive `t^2 I''` means negative entropy curvature `H''` at the point.

The correctly defined author `W` decimal in equation (3.6) remains `INCOMPLETE` from PR76. Run01's field named `W` is actually `V=E_mu[y psi]=s^2 W_author`, because the original compute request used the wrong name. That request-caused comparison failure must not be counted as an author error, but it also does not certify the printed author `W` decimal.

Unless a longer alias is written explicitly, source paths below are under `source-snapshots/pr76_additive/`.

## Source binding and provenance

Verdict: `CORRECT / ACCEPTED_SCOPED`.

The packet binding records PR76 commit `a7979c33b6e82431b6ddf1d39ac69e254d7b655a`, unit `pr76_additive`, file count 33, and hash-verified file entries at `source-snapshots/pr76_additive/SOURCE_BINDING.json:2-8`. I verified this bound file has 209 lines; its file list runs through `SOURCE_BINDING.json:7-205`, and the tail records the public origin and publication base at `SOURCE_BINDING.json:207-208`. The run ledger binds the author source commit, checker source commit, one run, exit code 20, no retry, no repair, and no live arithmetic after the run at `execution/RUN_LEDGER.json:2-31`.

The checker metadata says the independent run did not read/import/execute the author checker, records standard-library runtime, and embeds the author source binding at `outputs/run01/00_metadata.json:2-31` and `outputs/run01/00_metadata.json:50-59`. This matches the PR76 README statement that no author checker was read/imported/executed at `README.md:13-15`.

## Author section 3 fixture and finite claim targets

Verdict: `CORRECT / ACCEPTED_SCOPED` for identifying the target claims; `NEEDS_FIX` for the literal decimal in (3.5); `INCOMPLETE` for the corrected author-W decimal.

The author addendum gives the rational fixture at `inputs/ADDENDUM_JOINT_ADDITIVE.md:134-168`, the dual table at `inputs/ADDENDUM_JOINT_ADDITIVE.md:171-182`, the additive annihilation and Cauchy lower bound at `inputs/ADDENDUM_JOINT_ADDITIVE.md:184-196`, and the numerical claims at `inputs/ADDENDUM_JOINT_ADDITIVE.md:199-223`. The precise failing source sentence is the bound

`R_add < 4(P+A_2)^2/A_2 < 166.44125195305153`

at `inputs/ADDENDUM_JOINT_ADDITIVE.md:205-209`.

The author checker reference and output were inspected only as source/comparison targets. The author checker computes `W` using `mu*b*psi` at `inputs/author_checker_reference.py:84-90`, asserts the qualitative comparison at `inputs/author_checker_reference.py:99-105`, and prints the claimed values at `inputs/author_checker_reference.py:107-117`. The author output reports PASS and prints the same approximate values at `inputs/author_output_reference.txt:1-11`; this is not independent proof.

## Independent construction, legality, events, and cancellations

Verdict: `CORRECT / ACCEPTED_SCOPED` as retained PR76 finite evidence, subject to no C1 recomputation.

The independent checker is standard-library Python with exact `Fraction` arithmetic and rejects JSON floats at `implementation/independent_pr58_additive52_checker.py:8-14` and `implementation/independent_pr58_additive52_checker.py:90-98`. It freezes the author source commit, `s=9/10`, the log enclosure target, and the literal comparison targets at `implementation/independent_pr58_additive52_checker.py:20-34`. It validates the source binding against the frozen author commit at `implementation/independent_pr58_additive52_checker.py:205-238`.

The raw literal-input artifact records the matrix/table inputs, the `s=9/10` point, and the frozen author commit at `outputs/run01/01_literal_inputs.json:1-62`, `outputs/run01/01_literal_inputs.json:260-348`. The raw linear-algebra artifact records dense rank two and six positive-definite/Schur checks as true at `outputs/run01/02_linear_algebra.json:46-47` and `outputs/run01/02_linear_algebra.json:92-494`. The block-marginal artifact records positive block marginals and total marginal sums one at `outputs/run01/03_block_marginals.json:1-79`.

The checker constructs all row-major events for `S_mask,T_mask` in `0,...,7` at `implementation/independent_pr58_additive52_checker.py:893-899`, checks event polynomial shape, constant marginals, `q>0`, and complete probability positivity at `implementation/independent_pr58_additive52_checker.py:900-966`, and stores event data at `implementation/independent_pr58_additive52_checker.py:967-995`. The raw event artifact records `event_count=64`, all `q` positive, all probabilities positive, first event index 0, and final event index 63 with masks `(7,7)` at `outputs/run01/04_events.json:2-4`, `outputs/run01/04_events.json:43`, and `outputs/run01/04_events.json:8096`.

The checker verifies total probability, fixed row/column marginals, conditional `a/b` cancellations, log-coefficient cancellations, and dual row/column sums at `implementation/independent_pr58_additive52_checker.py:999-1066`. The raw cancellation artifact records row/column `a/b` and log-coefficient cancellation arrays at `outputs/run01/05_cancellations.json:36-137` and `outputs/run01/05_cancellations.json:192-293`; it records dual row and column sum arrays and total probability one at `outputs/run01/05_cancellations.json:138-157` and `outputs/run01/05_cancellations.json:294-297`.

## Forms, scalar enclosures, and ordered comparisons

Verdict: mixed.

- `CORRECT / ACCEPTED_SCOPED`: form construction and direct curvature identity as retained evidence.
- `CORRECT / ACCEPTED_SCOPED`: (3.4) lower bound.
- `CRITICAL_GAPS / NEEDS_FIX`: (3.5) printed upper bound.
- `CRITICAL_GAPS / INCOMPLETE`: corrected author (3.6) decimal for `W_author=E_mu[b psi]`.
- `CORRECT / ACCEPTED_SCOPED`: qualitative `L>T`, run-labelled `V<0`, and positive `t^2 I''`.

The independent checker builds `P0`, the run-labelled `W`, direct curvature, `sum c psi`, exact `A2`, and the dual denominator at `implementation/independent_pr58_additive52_checker.py:1069-1094`. It checks the direct differentiated curvature form against `P0+A2+W` in run labels and positivity of `A2` and the dual denominator at `implementation/independent_pr58_additive52_checker.py:1095-1121`. The stored forms are present at `outputs/run01/06_forms.json:2`, `outputs/run01/06_forms.json:266`, and `outputs/run01/06_forms.json:276`.

The run-labelled `W` uses `y=s^2 b`, not author `b`, at `implementation/independent_pr58_additive52_checker.py:939-947` and `implementation/independent_pr58_additive52_checker.py:1087-1088`. The original request made that same naming mistake at `inputs/REQUEST.md:24-28`. The correction note states the author definition and the scaling relation at `execution/CONTRACT_CORRECTION.md:5-13`. It also states that the first failed comparison was (3.5), unaffected by W/V notation, and that later raw comparison entries are not a post-stop verification gate at `execution/CONTRACT_CORRECTION.md:15-21`.

## Rational interval engine source audit

Verdict: `CORRECT / ACCEPTED_SCOPED` as static enclosure logic, subject to the same no-C1-recomputation limitation.

The logarithm enclosure engine uses an atanh series with a nonnegative rational tail bound after requiring `0 <= r < 1` at `implementation/independent_pr58_additive52_checker.py:538-555`. The range reduction first writes positive inputs as `x=2^k z` with `1 <= z < 2`, then uses `r=(z-1)/(z+1)` and adds `k log 2`; this appears at `implementation/independent_pr58_additive52_checker.py:587-639`. The dedicated `log2` enclosure uses the same atanh mechanism with `r=1/3` at `implementation/independent_pr58_additive52_checker.py:600-614`.

The interval arithmetic is endpoint-aware. Exact scaling swaps interval endpoints for negative factors at `implementation/independent_pr58_additive52_checker.py:562-565`; this is load-bearing both for negative log coefficients and for negative powers of two in range reduction. Division is only allowed through `interval_div_positive`, which checks a positive denominator before dividing endpoints at `implementation/independent_pr58_additive52_checker.py:568-575`. Interval squaring handles intervals crossing zero, entirely negative intervals, and entirely positive intervals at `implementation/independent_pr58_additive52_checker.py:578-584`.

Those primitives are used directly for the scalar certificates: forms are evaluated by summing exact constants plus signed log intervals at `implementation/independent_pr58_additive52_checker.py:646-651`; `L` is computed as the squared `sum c psi` interval divided by the dual denominator, and `T` as `4(P0+A2)^2/A2`, at `implementation/independent_pr58_additive52_checker.py:701-714`. The form stage separately requires `A2>0` and positive dual denominator at `implementation/independent_pr58_additive52_checker.py:1111-1121`, so the later interval divisions have the expected legal margin.

Outward decimal display uses exact rational floor/ceil conversion, not binary floating formatting, at `implementation/independent_pr58_additive52_checker.py:118-144`. Literal targets are parsed as exact decimal rationals at `implementation/independent_pr58_additive52_checker.py:654-662`, and comparisons use interval endpoints with disjoint-false detection at `implementation/independent_pr58_additive52_checker.py:665-690`. The scalar payload records these outward endpoints and the log audit records the formula, `log2`, and per-event log enclosures at `implementation/independent_pr58_additive52_checker.py:736-783`.

No source issue was found in this interval method. This supports treating the stored PR76 decimal envelopes as a sound outward-enclosure artifact, while still leaving the already stated (3.5) literal defect and corrected-W obligation unchanged.

The scalar enclosure artifact records 80 log terms and `widths_ok=true` at `outputs/run01/07_scalar_enclosures_N80.json:5054-5059`. It gives, among other entries, `L` in `[192.456447546638183766230914, 192.456447546638183766230915]`, `T` in `[166.441251953051540106785812, 166.441251953051540106785813]`, run-labelled `W=V` in `[-1.825377232343279850885156, -1.825377232343279850885155]`, and `true_curvature` in `[4.653598245398841812928176, 4.653598245398841812928177]` at `outputs/run01/07_scalar_enclosures_N80.json:4917-5047`.

The ordered comparison artifact records (3.4) as PASS at `outputs/run01/08_comparisons_N80.json:4-29`. It records (3.5) as `CERTIFIED_FALSE_DISJOINT`: the target is `166.44125195305153`, while the interval lower/upper decimal fields are `166.441251953051540106785812` and `166.441251953051540106785813` at `outputs/run01/08_comparisons_N80.json:32-57`. The final artifact repeats the first failure at `outputs/run01/final.json:3-34`, and the exit artifact records exit code 20 at `outputs/run01/exit.json:1`.

The qualitative comparisons passed: `L>T`, run-labelled `W<0` under the request label, and `true_curvature>0` at `outputs/run01/08_comparisons_N80.json:116-199`. Since run-labelled `W` is actually `V=E_mu[y psi]`, the retained evidence directly supports `V<0`. It supports the qualitative sign `W_author<0` only through the separately stated positive scaling relation `V=s^2 W_author`; it does not support the printed author-W decimal in (3.6).

## Evidence-supported author repairs

These repairs are directly supported by the retained PR76 evidence without a rerun:

1. Fix the final decimal in author equation (3.5). The formula `4(P+A_2)^2/A_2` can stay, but the printed upper bound `166.44125195305153` must be replaced by a strict upper decimal above the retained outward upper endpoint `166.441251953051540106785813`. A coarser bound such as `166.441251953051541` is supported by the existing interval; any replacement should be chosen above the stored endpoint and presented as an upper bound rather than an exact endpoint.

2. Keep the qualitative additive witness after repairing (3.5). The retained intervals certify `L>T`, so the joint-additive sufficient criterion fails at this fixture even though positive `t^2 I''` gives favorable entropy curvature.

3. Keep the positive-curvature / negative-entropy-curvature claim. The retained `true_curvature` interval is strictly positive, so the source may continue to state positive `t^2 I''` and hence negative `H''`.

4. If no corrected-W certificate is added, replace the literal author-W decimal claim with a qualitative sign statement, or explicitly state a `V` sign instead. The existing raw evidence supports run-labelled `V<0`; it does not certify `W_author(9/10)<-2.253552138695407`.

These obligations remain incomplete:

- A corrected exact comparison for author `W_author=E_mu[b psi]` against the decimal in (3.6), or a source edit that removes/downgrades that literal decimal claim.
- A future full machine-pass packet for the repaired literal list, if C3 wants a single pass artifact for all displayed numerical inequalities after the (3.5) fix and W/V cleanup.

## Non-assessed categories

Independent finite computation by this reviewer: `NOT_PERFORMED`. I audited source and retained raw artifacts only.

Formal coverage: `NOT_ASSESSED`.

Novelty: `NOT_ASSESSED`; this review performs no priority certification.
