# PR77 successor 8de8 static code review

Scope: static delta code review only. I did not run the new checker or any mathematical computation.

Overall static verdict: the new Fisher checker is a useful, source-level improvement for finite covariance-polynomial support, but the committed output is not the literal JSON that the script appears to emit, and no independent quantitative acceptance follows from author PASS records.

## Findings

### P1. `pair_fisher_exact.json` does not match the script's emitted schema

Status: `NEEDS_FIX` for reproducible evidence packaging.

`check_pair_fisher_projection.py` writes `output/pair_fisher_exact.json` with coefficient-list fields: `pair_mean_coefficients`, `covariance_coefficients`, `variance_density_coefficients`, endpoint values, and `uniform_Fisher_lower_bound` (`source-snapshots/pr77_delta_8de8/code/check_pair_fisher_projection.py:152-172`). The committed `pair_fisher_exact.json` instead contains pretty polynomial strings, `lag_at_least_4`, and `exit_status`, and omits the coefficient-list fields (`source-snapshots/pr77_delta_8de8/output/pair_fisher_exact.json:1-19`).

Why it matters: the output is substantively aligned with the checker assertions, but it is not a literal generated artifact from the displayed script. That limits reproducibility and keeps the artifact in the same "author PASS summary" class as the earlier short certificates.

Minimal repair: either commit the literal script output for the frozen head, or label the current file as a summary and add a generated raw JSON artifact with source and output hashes.

### P2. The supplemental run record partially fixes point curvature but lacks hashes and raw outputs

Status: `PARTIAL_FIX` / `NEEDS_FIX`.

The new run record lists the point-curvature command and the pair-Fisher checker command, both with exit status zero (`source-snapshots/pr77_delta_8de8/output/run_record_round2.json:8-18`). It also keeps `ci_claim` and `independent_review_claim` false and `continuum_curvature_claim` false (`source-snapshots/pr77_delta_8de8/output/run_record_round2.json:20-22`).

Why it matters: this closes the specific omission of the point-curvature command from the execution ledger, but it still lacks source hashes, output hashes, raw interval file paths, and full generated outputs. It cannot by itself certify the point-curvature inequalities.

Minimal repair: include hashes and full-output references for every recorded command.

### P3. Checker coverage is finite-polynomial only

Status: `ACCEPTED_SCOPED` as finite support; not a full Fisher theorem checker.

The checker correctly confines itself to exact inclusion determinants over at most four sites using pure `Fraction` polynomial arithmetic (`source-snapshots/pr77_delta_8de8/code/check_pair_fisher_projection.py:1-17`, `source-snapshots/pr77_delta_8de8/code/check_pair_fisher_projection.py:68-76`). It statically covers the pair mean, lags `0` through `3`, variance density, endpoint variances, and endpoint lower bound (`source-snapshots/pr77_delta_8de8/code/check_pair_fisher_projection.py:98-151`).

It does not check the analytic passage from finite scores to the true conditional Fisher rate. In particular, it does not verify the finite Cauchy-Schwarz score projection, two-dependence reasoning, right-to-left score decomposition, bounded boundary remainder, reverse-martingale orthogonality, or `lim I_n/n=nu(psi^2)`, all of which are listed as review duties in `verification_round2.md` (`source-snapshots/pr77_delta_8de8/verification_round2.md:21-35`).

Minimal repair: keep the script described as a finite covariance-polynomial checker. C2 should deliver only independent finite evidence under the original contract; FIRST/SECOND mathematical acceptance of the projection and limit steps is handled by C1/C3 review, not by C2.

## Non-findings

I found no static sign/scaling mismatch in the checker setup: the script explicitly uses `u=t/16` as the nearest-neighbor kernel entry (`source-snapshots/pr77_delta_8de8/code/check_pair_fisher_projection.py:57-65`) and converts the endpoint `t` values to `u=1/32` and `u=3/32` before evaluating the variance density (`source-snapshots/pr77_delta_8de8/code/check_pair_fisher_projection.py:141-150`).

I found no static dependency on the previous midpoint or point checker modules. The new script builds its own polynomial operations, kernel entries, and Leibniz determinant (`source-snapshots/pr77_delta_8de8/code/check_pair_fisher_projection.py:20-91`).

I found no new code path that claims whole-interval curvature or issue-level continuum certification. The supplemental run record explicitly sets `continuum_curvature_claim` to false (`source-snapshots/pr77_delta_8de8/output/run_record_round2.json:20-22`).
