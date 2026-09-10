# PR79 ae11 delta FIRST review

Line references use `source-snapshots/pr79_delta/research/I05-DPP-27-rate-curvature-20260910/RESULT.md` unless another alias is named.

Overall delta status: `ACCEPTED_DELTA` for closing original RESULT-level F1/F3; `PENDING_C2` for all exact numerical and PR77 finite claims; `INCOMPLETE` for the full curvature theorem; no blocking semantic defect remains in the changed RESULT text.

## F1 closure: actual tail versus explicit upper budget

The original F1 defect was that the result text named the computed values as the actual tail `sum |d_r''(t)|`, even though the source and script only compute the PR77 upper majorant.

The ae11 text closes this defect:

- `RESULT.md:L17-L19` retitles the section as an explicit upper budget and says independent finite checks are pending.
- `RESULT.md:L21-L24` defines `B_R` as the explicit rational sum of the PR77 majorant and separately states `sum_{r>=R} |d_r''(t)| <= B_R`.
- `RESULT.md:L27` says the script sums the explicit majorant and does not compute the actual absolute curvature tail.
- `RESULT.md:L29-L47` labels the displayed decimals and comparisons as author displays/assertions for `B_R`, not for the actual tail.

This is the required semantic repair. Lower comparisons such as `B_20 > 1/2500` and `B_21 > 1/5000` are now visibly comparisons for the upper budget only. They no longer imply, and are not phrased as implying, any lower bound on the actual tail.

## Threshold and depth inference

`RESULT.md:L49` correctly states the conditional inference:

- A finite conditional-curvature upper bound of `-4e-4`, combined with a validated `B_20` larger than that margin, would not certify true-rate negativity via this coarse budget.
- A validated `B_21 < 4e-4` would suffice for that error comparison.
- A validated `B_22 < 1e-4` would suffice with a finite upper bound of `-1e-4`.
- A lower bound on `B_R` is not a lower bound on the actual tail.
- No minimum necessary depth and no finite or true curvature sign follows from the budget alone.

This closes the original overstatement risk. The delta no longer asserts that depth 21 or 22 is intrinsically necessary; it only describes what the displayed author budgets would suffice for after independent arithmetic review and after a finite-cell upper certificate exists.

`RESULT.md:L98` repeats the same corrected posture: retained author budget displays may suggest useful depths, but a proved cell certificate must combine the actual finite upper bound with a validated upper error budget, and the budget alone does not rule out smaller depths with stronger finite margins or sharper errors.

`RESULT.md:L121` also removes the unconditional `R>=21` gate and replaces it with the correct combined condition `sup h_R''(J)+B_R<0` on every cell.

## F3 closure: positive interval and negative interval transfer

The original F3 issue was that the target was stated on `1/2 <= |t| <= 3/2`, while the tail budget discussion was only sourced on the positive interval.

The ae11 text now separates these:

- `RESULT.md:L27` says the budget discussion concerns `t in [1/2,3/2]`.
- `RESULT.md:L27` also says extending a completed sign certificate to the negative interval uses physical gauge evenness of the true entropy rate.
- `RESULT.md:L121` asks for cell coverage only on `[1/2,3/2]`.
- `RESULT.md:L124-L130` still states the absolute-value whole-interval theorem as incomplete.

The evenness transfer is mathematically appropriate for complete-configuration entropy: replacing `t` by `-t` shifts the symbol by a half period, equivalently diagonal-gauge conjugates the Toeplitz kernel, and complete-event probabilities and entropy rate are unchanged. The text does not use evenness to certify a sign without first obtaining a completed positive-interval certificate.

No blocking F3 defect remains in the delta. A future fully formal writeup could add the one-line identity behind the gauge evenness, but it is not required for this scoped text repair.

## Pending numerical and PR77 finite claims

The delta preserves pending status for numerical and finite claims:

- `RESULT.md:L17` says independent finite checks are pending.
- `RESULT.md:L29` says exact rational comparisons are pending independent arithmetic review.
- `RESULT.md:L40` says the author program asserts the comparisons.
- `RESULT.md:L98` says independent constants and finite certificates remain pending.
- `RESULT.md:L112` says the exact comparison remains independently pending.
- `RESULT.md:L115` says PR77's strict midpoint claim still awaits independent finite certification.

This source-only delta review does not accept any decimal, rational threshold sign, PR77 finite determinant/log certificate, or exact tail-budget arithmetic. The original C2 contract should remain an independent reconstruction from PR77's displayed majorant and geometric sums, with author script output used only for comparison.

## Unchanged script naming

The delta did not change `tail_budget.py` or `run_record.txt`. The unchanged script still names its function `tail(R)` in the original frozen source, even though it computes the upper budget. This review did not execute the script.

Because the changed `RESULT.md` now states at `RESULT.md:L27` and `RESULT.md:L40-L47` that the script asserts comparisons for the explicit upper budget, the stale function name does not create a blocking semantic defect in the ae11 RESULT text. The earlier code-review recommendation to rename or document `tail(R)` as an upper-budget function remains valid for any later code cleanup.

## Nonclaims retained

The delta preserves the important nonclaims:

- `RESULT.md:L49`: the budget alone proves no finite or true curvature sign.
- `RESULT.md:L59-L75`: the Riccati route is still an incomplete continuous-state bridge.
- `RESULT.md:L86-L92`: the conditional-mutual-information bridge still requires a rigorous finite-depth conditional-curvature enclosure plus the explicit tail budget.
- `RESULT.md:L108`: external HMM/RPF references remain methodological only.
- `RESULT.md:L117-L122`: the next gate requires either validated finite-cell coverage with a validated upper budget or a Riccati invariant-set/contraction/jet certificate.
- `RESULT.md:L124-L130`: the whole-interval claim remains `INCOMPLETE`.

## Delta verdict

`ACCEPTED_DELTA`: ae11 closes original F1/F3 at the RESULT-text level.

`PENDING_C2`: exact budget values, threshold signs, displayed decimals, PR77 constants, and PR77 finite certificates remain pending independent review.

`INCOMPLETE`: no whole-interval true-rate curvature theorem is certified.

`NO_NEW_NEEDS_FIX`: no new blocking text defect was found in the frozen delta.
