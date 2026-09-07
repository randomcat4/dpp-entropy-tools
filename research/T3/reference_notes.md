# T3 Child B Reference Prototype Notes

Status: CANDIDATE. This is an independently written reference prototype, not a verified certificate stack and not an acceleration result.

## Scope

Owned files only:

- `research/T3/reference/`
- `research/T3/reference_notes.md`

No edits were made under `research/T3/core/` or `research/T3/specs/`.

## Reference Algorithm

Implementation entrypoint: `research/T3/reference/exact_dpp_reference.py`.

The reference enumerates all subsets of `[n]` in deterministic size-then-lexicographic order. For each subset it computes the relevant principal determinant exactly with `fractions.Fraction`, including the empty determinant equal to `1`.

Two explicit event-law modes are supported:

- `l_ensemble`: exact event probability is `det(L_S) / sum_T det(L_T)`. This uses determinant weights for every subset event and checks nonnegative determinant weights.
- `marginal`: `det(K_S)` is treated only as an inclusion probability. Exact subset-event probabilities are then computed by inclusion-exclusion over supersets. This mode is included to catch accidental inclusion-event misuse.

For a rational path `K + tD`, determinant jets are exact. The code evaluates `det(A + xB)` at integer `x=0..m` for a subset of size `m`, interpolates the determinant polynomial exactly, and reads off value, first derivative, and second derivative. L-ensemble probability jets use exact quotient differentiation; marginal probability jets use exact inclusion-exclusion on inclusion jets.

Entropy uses the mathematical zero rule `lim_{p->0+} -p log(p)=0`. Curvature at a zero probability is not patched by epsilon: if the zero probability has nonzero first or second jet, the reference returns `NOT_CERTIFIED` / `not_finite_or_not_certified` and asks for separate one-sided limit analysis.

Logarithms of positive rationals are enclosed by exact rational intervals. The code scales a rational into `[1,2]` and uses
`log(y) = 2 * sum z^(2j+1)/(2j+1)`, where `z=(y-1)/(y+1)`, with an explicit positive-tail remainder bound. Entropy, curvature, and chord-gap signs are decided only from these rational intervals.

Interval feasibility over a rational path interval uses exact event polynomials and Bernstein coefficient enclosures after an affine map to `[0,1]`. A nonnegative Bernstein lower bound is a certificate; an overlapping enclosure is reported as `NOT_CERTIFIED`, not guessed.

Floating results are labeled `diagnostic_only` and never decide certificate status.

## Adversarial Cases

Fixture file: `research/T3/reference/adversarial_cases.json`.

- `near_zero_l_ensemble`: very small but positive determinant weight; verifies no epsilon cutoff erases it.
- `zero_probability_marginal_boundary`: exact zero event probabilities under marginal mode; entropy uses the limit rule.
- `repeated_eigen_diagonal_l_ensemble`: repeated diagonal entries at `t=0`; checks exact probabilities and negative curvature without eigenvector assumptions.
- `tiny_gap_float_misleading`: one-dimensional marginal path with a chord gap around `2e-18`; the rigorous interval certifies positivity while double precision is diagnostic only.
- `invalid_negative_l_weight`: negative determinant weight is rejected exactly.
- `invalid_nonsymmetric_input`: nonsymmetric input is rejected before analysis.

The intentionally false candidate is in `tiny_gap_float_misleading`: it claims a chord-gap lower bound of `1e-15`, which the reference rejects because the certified lower endpoint is far smaller.

Generated deterministic artifacts are under `research/T3/reference/out/`. The manifest hash from the current run is:

`5bc46409fb854255f4c5ae174bb5e02cb0f8b11a0b671d3845f631b9c0afe19d`

## Commands Run

All successful runs used one BLAS/OpenMP/MKL thread, although this code uses only the Python standard library.

- `python -m unittest research\T3\reference\test_reference.py`
  - Exit code: 1
  - Reason: Windows app-alias `python` was not a usable interpreter.
- Bundled Python 3.12.14: `python.exe -m unittest research\T3\reference\test_reference.py`
  - Exit code: 1
  - Reason: initial test import path was too bare from the repo root.
- Bundled Python 3.12.14: `python.exe -m unittest research\T3\reference\test_reference.py`
  - Exit code: 0
  - Result: 5 tests passed.
- Bundled Python 3.12.14: `python.exe research\T3\reference\exact_dpp_reference.py --output-dir research\T3\reference\out`
  - Exit code: 0
  - Result: 6 cases completed; 4 candidate analyses and 2 rejected invalid inputs.

## Mismatch Risks For Main T3

- Kernel convention must be explicit. If the main tool means L-ensemble event probabilities, use `mode: l_ensemble`; if it means a marginal/correlation kernel, use `mode: marginal`. Comparing these modes without conversion will create false mismatches.
- Bernstein feasibility is a rigorous sufficient enclosure, not a complete positivity solver. `NOT_CERTIFIED` means the reference did not prove the sign on that interval.
- The implementation is designed for small `n`; it is a correctness oracle for tiny objects, not a scanner.
- This child-B result should be treated as CANDIDATE until another context checks the implementation and reruns the artifacts.
