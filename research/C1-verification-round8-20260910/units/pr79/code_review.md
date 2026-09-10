# PR79 C1 FIRST static code and evidence review

Line references use the public-clean aliases in `frozen_scope.md`.

Scoped code status: static source is deterministic and suitable for exact-arithmetic review, but its function and result naming should be changed from actual tail to upper-budget tail. No program was executed in this source-only lane.

## Files reviewed

- `source-snapshots/pr79/SOURCE_BINDING.json`
- `source-snapshots/pr79/research/I05-DPP-27-rate-curvature-20260910/RESULT.md`
- `source-snapshots/pr79/research/I05-DPP-27-rate-curvature-20260910/tail_budget.py`
- `source-snapshots/pr79/research/I05-DPP-27-rate-curvature-20260910/run_record.txt`
- Permitted predecessor context: `source-snapshots/pr77/proof.md` and `source-snapshots/pr77/SOURCE_BINDING.json`

## Binding and evidence coverage

`SOURCE_BINDING.json` binds PR79 to head `bee0e5b5264ced09feb6403a718e25f835e91d21`, base `65e59a46b49cd2dbb5c779a4cfae8cef26441984`, and exactly three files. The line counts match the assignment: `RESULT.md` has 126 lines, `tail_budget.py` has 55 lines, and `run_record.txt` has 17 lines.

The evidence covers only the analytic tail-budget continuation. It does not contain:

- finite-depth outward interval enclosures for `h_R''` on cells covering the target interval;
- a Riccati invariant set, branch-probability proof, contraction/spectral-gap certificate, parameter-jet bounds, or invariant-measure response bound;
- a primary-source verification of external RPF/HMM theorem hypotheses;
- an independent reviewer execution of the exact arithmetic.

This matches the nonclaim in `RESULT.md:L120-L126` that the whole-interval curvature theorem remains incomplete.

## `tail_budget.py`

Static positives:

- `tail_budget.py:L1` uses only the Python standard-library `Fraction` type.
- `tail_budget.py:L3-L10` declares the constants used in PR77 section 8: `rho`, `C0`, `M2`, `M3`, `M4`, `U1`, and `U2`, matching `source-snapshots/pr77/proof.md:L128`, `source-snapshots/pr77/proof.md:L200-L201`, `source-snapshots/pr77/proof.md:L452-L475`.
- `tail_budget.py:L11-L15` implements PR77's `A0`, `A1`, `A2`, and `q=rho^4`, matching `source-snapshots/pr77/proof.md:L495-L497` and `source-snapshots/pr77/proof.md:L525`.
- `tail_budget.py:L17-L20` forms the RHS prefactor of PR77 equation (8.14), with `e_r^2 = C0^2 rho^(4r-12) = C0^2 rho^(-12) q^r`.
- `tail_budget.py:L23-L37` reconstructs the quadratic polynomial in `r` and applies the three closed geometric sums from `source-snapshots/pr77/proof.md:L525-L535`.
- `tail_budget.py:L48-L54` keeps the author-facing acceptance comparisons as exact `Fraction` assertions, so the decimal output at `tail_budget.py:L46` is display-only.

Code/text defect:

The function `tail(R)` returns the sum of the explicit PR77 upper majorant, not the actual tail `sum_{r>=R}|d_r''(t)|`. This should be reflected in both code and prose. Suggested names:

- `tail_budget(R)`
- `upper_tail_budget(R)`
- `B_R`

The comments at `tail_budget.py:L48-L50` are otherwise correct that these are tail-only statements and not curvature certificates, but they should say "tail upper-budget statements" to avoid the same ambiguity.

## `run_record.txt`

`run_record.txt:L1-L4` records the command and labels the expected output as exact `Fraction` arithmetic with decimal display only. `run_record.txt:L8-L15` lists the expected decimals and `PASS`. `run_record.txt:L17` correctly says the record is author output, not independent C2 execution.

The record intentionally omits exact rational numerators and denominators at `run_record.txt:L17`. That is acceptable for an author checkpoint, but final acceptance of threshold signs should come from C2 independently reconstructing the PR77 majorant and closed geometric sums. The author script and its `PASS` should be used only as comparison material.

## C2 exact-arithmetic checklist

Frozen comparison sources:

- `source-snapshots/pr79/research/I05-DPP-27-rate-curvature-20260910/tail_budget.py`
- `source-snapshots/pr79/research/I05-DPP-27-rate-curvature-20260910/run_record.txt`
- `source-snapshots/pr77/proof.md:L511-L535`

Required result:

- Independently rebuild the exact upper-budget formula from PR77 equations (8.14)--(8.16), including the displayed constants and geometric sums.
- Record exact rational values for `B_R`, `R=18,19,20,21,22,23,24`.
- Record exact rational threshold differences for `B_20-1/2500`, `1/2500-B_21`, `B_21-1/5000`, and `1/10000-B_22`.
- Record source and execution binding: PR77 source hash, PR79 source hash, independent checker hash if any checker file is created, command, runtime environment summary, and exit status.
- Compare the independent exact values to the author `tail_budget.py` output and `run_record.txt`; do not treat the author script's `PASS` as the accepted computation.
- Report the accepted object as the PR77 upper budget `B_R`, not as the actual tail unless a revised source computes the actual `d_r''` tail.

This checklist is only a future independent-reconstruction contract. It does not authorize any new entropy, interval, depth-18--24, or author-script execution job.

## Final static-code status

No blocking implementation bug was found in the algebraic structure of the exact-budget script. The blocking issue is semantic labeling: the script computes an exact closed form for an upper bound inherited from PR77, while the result text presents those values as the actual curvature tail. Exact threshold signs remain pending independent C2 arithmetic.
