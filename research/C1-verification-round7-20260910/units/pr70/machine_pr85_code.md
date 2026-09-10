# PR85 machine static code review

Scope: static review of the independent finite checker and run guard for the fixed PR70 paired-resolvent object. I did not execute any code or recompute arithmetic.

Overall static verdict: `ACCEPTED_SCOPED`; no blocking implementation defect found for the stated single-object finite gate. This supports the C1 source/evidence FIRST conclusion in `machine_pr85_review.md`; the PR85 `MACHINE_PASS` status is raw machine output, not a reviewer verdict by itself.

Public alias: `source-snapshots/pr85_machine/...`

Immutable URL base: `https://github.com/randomcat4/dpp-entropy-tools/blob/611d5f70e8bb70237755ca4fdbe8ab14c8b715c1/research/C2/pr70_obstruction52/`

## Independent checker

Status: `CORRECT`; verdict: `ACCEPTED_SCOPED`.

Pins: `implementation/independent_pr70_checker.py:1-19`, `implementation/README.md:3-11`, and `inputs/PREPARATION_SHA256.json`.

The checker imports only Python standard-library modules. It uses `fractions.Fraction`, disables integer-string digit caps for large exact output, fixes N=80 and width `1e-32`, and writes packed JSON artifacts. The implementation README states that no author executable or output is imported.

## Gate and stop behavior

Status: `CORRECT`; verdict: `ACCEPTED_SCOPED`.

Pins: `implementation/independent_pr70_checker.py:40-64`, `implementation/independent_pr70_checker.py:442-485`, `execution/RUN_PLAN.md:5-13`, and `execution/run_guard.sh:1-43`.

Every gate ticks the immutable deadline, appends a compact `CHECKS.jsonl` row, writes `FIRST_FAILURE.json` on failure, and raises a terminal halt. The main function records mechanical exceptions separately, writes `STATUS.json`, hashes outputs, and exits nonzero for failure modes. The guard enforces a single deadline, lock, one CPU, thread variables set to 1, UTF-8 output, a 16 GiB virtual-memory cap, timeout kill, start/deadline files, PID files, stdout/stderr, and exit status.

## Event and legality code

Status: `CORRECT`; verdict: `ACCEPTED_SCOPED`.

Pins: `implementation/independent_pr70_checker.py:102-154`, `implementation/independent_pr70_checker.py:291-346`, and `outputs/run01/CHECKS.jsonl:1-110`.

The checker implements two independent event constructions: inclusion minors by permutation expansion with Mobius inversion, and signed complete-event determinants by recursive Laplace expansion after subtracting absent diagonals. Jets use ascending powers of physical `t` and multiply the quadratic coefficient by 2 for the second derivative. The code constructs marginal polynomials, independent two-leaf polynomials, normalization checks, literal atom comparisons, endpoint/complement Sylvester-minor checks, and endpoint/center probability positivity checks.

## P2 code

Status: `CORRECT`; verdict: `ACCEPTED_SCOPED`.

Pins: `implementation/independent_pr70_checker.py:154-169`, `implementation/independent_pr70_checker.py:351-369`, `outputs/run01/phi_rows.json`, `outputs/run01/phi_exact.json`, and `outputs/run01/CHECKS.jsonl:111-123`.

The reciprocal/product jet helpers are used to compute `P^2/r` second derivatives, and each row is checked against the displayed P3 formula. The code then sums exact side values, checks the three literal P2 fractions, and separately checks the paired negative interval containment.

## P5 code

Status: `CORRECT`; verdict: `ACCEPTED_SCOPED`.

Pins: `implementation/independent_pr70_checker.py:190-217`, `implementation/independent_pr70_checker.py:262-270`, `implementation/independent_pr70_checker.py:371-417`, and `outputs/run01/CHECKS.jsonl:124-158`.

The `LinearLogs` representation keeps rational constants separate from rational coefficients of logarithms. The curvature helper implements the negative-entropy Hessian as Fisher plus acceleration-log terms. The side calculations retain both `r''` and `P''`, compare direct and perspective differentiations row by row, and gate the conditional structural identity. Full, leaf, conditional, side, Fisher, and acceleration components are written to raw artifacts.

## Log and interval code

Status: `CORRECT`; verdict: `ACCEPTED_SCOPED`.

Pins: `implementation/independent_pr70_checker.py:177-185`, `implementation/independent_pr70_checker.py:218-257`, `implementation/independent_pr70_checker.py:277-286`, `implementation/independent_pr70_checker.py:410-417`, `implementation/independent_pr70_checker.py:421-430`, and `outputs/run01/log_inventory.json:2-37`.

The code normalizes each positive rational log argument to `2^k*y`, computes the N=80 atanh partial sum and nonnegative tail bound, combines with log2 intervals, reverses endpoints for negative scaling coefficients, and emits 40-place outward decimal displays. `compare_interval` gates width, broad sign, and literal containment separately. `Phi_pair` uses exact equal bounds and disables the width gate as intended.

## Jensen code

Status: `CORRECT`; verdict: `ACCEPTED_SCOPED`.

Pins: `implementation/independent_pr70_checker.py:270-275`, `implementation/independent_pr70_checker.py:419-430`, `outputs/run01/jensen_exact_form.json`, and `outputs/run01/jensen_assembly.json`.

The entropy function implements complete entropy as a linear-log form for `-p log p`. The Jensen quantity is constructed as the average of minus/plus entropy minus center entropy. The code also assembles the same interval from separately evaluated three-entropy intervals and gates overlap before width/sign/containment checks.

## Limitations

- This review did not run the checker or independently recalculate any fraction or interval.
- `STATUS.json` is not used alone; the checks ledger, source gates, interval files, log inventory, and execution records are all needed.
- The checker proves no universal determinant, one-sided, full-entropy, or real-three-point theorem.
- Independent SECOND review is outside this code report.
- The public output-hash manifest still lists the redacted private invocation filename, while the file itself is absent from the public raw tree. The run ledger explicitly allows that hash name to remain; no mathematical data is missing because of this redaction.

No `NEEDS_FIX` or `CRITICAL_GAPS` item was found in the static code review.
