# PR77 successor 8de8 delta-FIRST review

Delta verdict: `PARTIAL_FIX_ACCEPTED_SCOPED` for boundary cleanup and Fisher finite-checker source additions; `PENDING_C2` for independent finite acceptance; `NEEDS_FIX` for remaining certificate packaging gaps. The five added files do not alter the original 18 files and do not upgrade author exact PASS outputs to independent quantitative acceptance.

Novelty: `NOT_ASSESSED`.

Formal verification: `NOT_PERFORMED`.

Arithmetic/computation: `NOT_PERFORMED`.

## Delta claim-by-claim audit

### 1. Source binding and pure-additive scope

Status: `ACCEPTED_SCOPED`.

The delta binding records five added files over base `6ebe38dc6503120d47e9d644cfac78cfb43666f5`, with 18 original files unchanged and successor head `8de8b0007f9374b7a5decb9b0a2f1c939fe897be` (`source-snapshots/pr77_delta_8de8/SOURCE_BINDING.json:1-47`). I treated this as the frozen delta scope and did not use live state.

### 2. `FINAL_RESULT.md` boundary consistency

Status: `ACCEPTED_SCOPED` for boundary wording; no independent theorem upgrade.

The file keeps the fixed amplitude and strict legality statement unchanged (`source-snapshots/pr77_delta_8de8/FINAL_RESULT.md:7-22`). It repeats the midpoint Jensen and three point-curvature assertions as true-rate author claims (`source-snapshots/pr77_delta_8de8/FINAL_RESULT.md:24-43`) and states that all new statements are author proof, not independently reviewed (`source-snapshots/pr77_delta_8de8/FINAL_RESULT.md:5-5`). It also preserves the continuum boundary: six point signs and one Jensen chord do not imply whole-interval curvature, no positive true-rate counterexample is obtained, and the continuum certificate remains outside the present evidence (`source-snapshots/pr77_delta_8de8/FINAL_RESULT.md:84-98`).

This is consistent with the original frozen boundary. The title `FINAL RESULT` should not be read as independent acceptance; the file itself disclaims that status.

Closed by delta: public-facing boundary summary is clearer and does not claim the whole-interval curvature theorem.

Still open: midpoint and point claims remain certificate-driven author claims pending C2; no raw interval/hash evidence is added.

### 3. Point-curvature run-record repair

Status: `PARTIAL_FIX`; still `NEEDS_FIX` for full auditability.

The new supplemental run record now lists the point-curvature command and exit status (`source-snapshots/pr77_delta_8de8/output/run_record_round2.json:8-18`). This partially repairs the original omission where point curvature was not present in the original run record.

Limits of the repair: the new record still gives only command, environment, scope, and exit status. It does not add output hashes, source hashes, raw true-curvature intervals, point-specific tails, or the full generated JSON needed to audit the strict point inequalities. The point-curvature exact claims therefore remain `PENDING_C2`, not independently accepted.

### 4. Fisher covariance checker

Status: `ACCEPTED_SCOPED` for static finite-polynomial coverage; `PENDING_C2` for independent quantitative acceptance.

The new checker is materially more independent than the earlier small checks because it does not import the midpoint or point certificate modules. It implements polynomial arithmetic over `Fraction`, constructs Toeplitz inclusion determinants by the Leibniz formula over at most four sites, and uses `u=t/16` as the nearest-neighbor kernel entry (`source-snapshots/pr77_delta_8de8/code/check_pair_fisher_projection.py:1-17`, `source-snapshots/pr77_delta_8de8/code/check_pair_fisher_projection.py:57-76`).

The static formulas covered by the checker match the finite inclusion algebra needed for the Fisher projection constants: pair mean, covariance lags `0` through `3`, variance density, endpoint variance values, and the endpoint Fisher lower bound (`source-snapshots/pr77_delta_8de8/code/check_pair_fisher_projection.py:98-151`). This closes the previous source-material gap that no finite polynomial checker was supplied for the displayed Fisher covariance formulas.

Coverage limits: the checker covers local inclusion determinant polynomials only. It does not by itself prove two-dependence, the finite Cauchy-Schwarz score projection, the right-to-left score decomposition, the bounded boundary remainder, reverse-martingale orthogonality, or the limit `lim I_n/n=nu(psi^2)`. Those remain analytic arguments in the unchanged source and review contract (`source-snapshots/pr77_delta_8de8/verification_round2.md:21-35`). The checker also does not create independent acceptance in C1 because it was not executed by this reviewer.

Closed by delta: finite source support for the covariance polynomial is improved.

Still open: independent C2 implementation/reconstruction under the original finite-evidence contract is needed before the exact lower bound `16/286141` is outwardly certified. The new 8de8 checker is an author-side delta artifact that may be compared against later; it is not itself a C2 input and rerunning it is not sufficient.

### 5. Fisher output and record consistency

Status: `NEEDS_FIX`.

The committed `pair_fisher_exact.json` is consistent in substance with the formulas asserted in the new checker and final result (`source-snapshots/pr77_delta_8de8/output/pair_fisher_exact.json:1-19`; `source-snapshots/pr77_delta_8de8/FINAL_RESULT.md:62-69`). However, it does not match the JSON schema the script would emit. The script emits coefficient-list fields such as `pair_mean_coefficients`, `covariance_coefficients`, and `variance_density_coefficients`, and does not include `exit_status` (`source-snapshots/pr77_delta_8de8/code/check_pair_fisher_projection.py:152-168`). The committed output instead contains display-polynomial strings, a `lag_at_least_4` field, and `exit_status` (`source-snapshots/pr77_delta_8de8/output/pair_fisher_exact.json:1-19`).

This does not show the Fisher formulas are false. It means the frozen output appears to be a curated PASS summary rather than the literal JSON emitted by the script at this head. Public certification still needs raw generated output or a clear statement that this file is an abbreviated summary.

### 6. Section 9 beam-splitter rate bridge

Status: `UNCHANGED`; original `INCOMPLETE_BRIDGE` remains.

The five added files do not supply a uniform-in-volume fourth-order remainder or a doubled-process RPF/Holder derivative bridge for the original Section 9 true-rate beam-splitter statement. `FINAL_RESULT.md` does not rely on that bridge for the midpoint or point certificates. Therefore the prior Section 9 finite/rate split remains unchanged: finite-block algebra can be accepted scoped, but the true-rate second-order bridge remains incomplete unless a separate author/coordinator analytic delta is added.

### 7. Raw interval/hash evidence

Status: `UNCHANGED`; still `NEEDS_FIX` / `PENDING_C2`.

The delta does not add full midpoint certificate output, full point-curvature certificate output, raw interval margins, determinant histograms, true-curvature interval endpoints, or source/output hashes tying the generated artifacts to the frozen source. The original raw-output/hash gap remains open for midpoint and point certification.

## Delta C2 implications

Necessary C2 finite-evidence contract remains focused on:

1. midpoint Jensen certificate raw intervals and exact event reconstruction;
2. point-curvature raw intervals, exact jets, and point tails;
3. rational analytic constants needed by those finite-to-rate passages;
4. source/output hash and run-record audit.

The new pair Fisher checker may be used as helpful author-side comparison data, but quantitative Fisher acceptance would require independent C2 finite reconstruction under the original contract. The 8de8 checker is not a C2 input, and rerunning it is not sufficient. Section 9 true-rate bridge is not a C2 finite-evidence task.
