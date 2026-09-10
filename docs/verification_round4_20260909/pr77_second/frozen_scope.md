# Frozen scope for PR77 independent second review

## Review identity

This is an isolated non-author second review for PR77, C3 verification round 4. The mathematical source scope is the frozen PR77 original source set plus the exact five delta additions, with three previously accepted PR53 source files available only for their stated machinery.

Novelty: NOT_ASSESSED.

Formal verification: NOT_PERFORMED.

Computation: NOT_PERFORMED. I did not run the author scripts, determinant enumerations, logarithm enclosures, tests, jobs, or resource probes. Numerical certificate claims are therefore treated as author evidence unless separately supplied by C2 raw artifacts.

## Files in scope

The source binding is machine-hashed in `source_binding.json`. The scope consists of:

- `input/`: 18 original PR77 files at head `6ebe38dc6503120d47e9d644cfac78cfb43666f5`, as recorded in `input_binding.json`.
- `delta_input/`: 5 additions at head `8de8b0007f9374b7a5decb9b0a2f1c939fe897be`, as recorded in `delta_input_binding.json`. The binding states that the 18 original files are byte-identical.
- `accepted_input/`: 3 previously accepted original PR53 source files at head `9dcb6e9079ca57f94e0e30d63161cda89ca61fae`, as recorded in `accepted_input_binding.json`.

No FIRST/SECOND/C3 review conclusions, PR bodies/comments, PR78, live successor material, private handoffs, remote scripts, or files under `[excluded private directory]` were read or used.

## Exact final mathematical source scope

The final PR77 source scope is:

- the 18 original files under `input/`;
- plus the exact 5 additions under `delta_input/`;
- plus the accepted PR53 sources under `accepted_input/` only for the precise accepted machinery listed below.

The five delta additions are:

- `delta_input/FINAL_RESULT.md`
- `delta_input/verification_round2.md`
- `delta_input/code/check_pair_fisher_projection.py`
- `delta_input/output/pair_fisher_exact.json`
- `delta_input/output/run_record_round2.json`

## Accepted-input premises used

The accepted files support only machinery, not the fixed-amplitude PR77 conclusion.

1. Complete-event DPP formulas and parity bookkeeping.
   - `accepted_input/proof.md:62`-`119` gives the signed complete-event determinant likelihood, Schur complement, Fisher and acceleration terms, and the exact finite sign obligation.
   - `accepted_input/finite_range_local_theorem.md:54`-`87` gives the parity identity, diagonal gauge evenness, and the rate identity for half-period families.

2. Configuration-uniform complete-event inverse control and locality.
   - `accepted_input/proof.md:147`-`227` and `accepted_input/finite_range_local_theorem.md:145`-`205` give the event-matrix accretivity and finite-range inverse decay machinery.
   - `accepted_input/exponential_wiener_extension.md:45`-`231` gives the corresponding exponentially weighted localization and common complex-disk machinery.

3. Normalized one-sided complete-event conditionals and RPF/true-rate passage.
   - `accepted_input/finite_range_local_theorem.md:207`-`341` constructs holomorphic Holder one-sided complete-event conditionals and derives exact entropy-rate formulas before differentiating the rate.
   - `accepted_input/exponential_wiener_extension.md:185`-`262` extends the same analytic input beyond finite range.

4. Balanced beam-splitter finite bookkeeping.
   - `accepted_input/proof.md:229`-`308` gives the finite balanced beam-splitter occupation decomposition and the warning that quasifree von Neumann entropy is not the classical occupation Shannon entropy.

## Accepted-input exclusions

The accepted inputs do not supply:

- any PR59/PR60 theorem for PR77;
- any quantitative proof that the fixed amplitude `1/4` lies in a local tube;
- any whole-interval sign for `h''(t)` on `1/2<=|t|<=3/2`;
- any approval of PR77's finite exact constants, midpoint numerical margin, point-curvature thresholds, or Fisher covariance polynomial;
- any novelty, priority, or formal-proof verdict.

