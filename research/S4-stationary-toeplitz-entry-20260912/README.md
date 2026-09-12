# Stationary Toeplitz entry diagnostics for finite DPP entropy counterexamples

Status: **author computational exploration; finite numerical evidence only**.

This package executes four bounded tasks: transition-spectrum counting, distance
of the exact finite counterexamples to Toeplitz structure, continuation of fixed
near-projection entropy-increment sequences, and direct `n=5,6` searches in
finite-symbol Toeplitz coordinates.  The conclusions and scope limits are in
`REPORT.md`.

## Frozen sources

- stationary family and conditional-DPP jet recursion:
  `randomcat4/icm-conjecture-lab@ee97a7341ac968fc341599aa973d0793497e7db3`,
  `research/I05_info_geometry_independent/nonsmooth_stationary/`;
- exact finite examples:
  `randomcat4/icm-conjecture-results@b2645baeff9fdc3b8c767fc621760bf0d57557eb`,
  `results/I05_lyons_counterexample/`;
- target repository base:
  `randomcat4/dpp-entropy-tools@237097124869b3bb04c139d4c4599e6bda7d344d`.

The upstream stationary script is preserved byte-for-byte under `code/`; its
SHA-256 is `f3f49dd0ed382df7dba1d6eb849fac607023b1de5e21f9679c03f52323fc1b30`.

## Environment

Python 3.12.14 was used with one BLAS thread and one Numba thread.  Install the
isolated dependencies with:

```text
python -m pip install --target python_deps -r requirements.txt
```

## Reproduction

Set `PYTHONPATH` to `python_deps;code` on Windows (use `:` on Unix), then run:

```text
python code/run_c4_c3.py --output-dir outputs --max-curvature-n 22
python code/run_c3_extension.py --output-dir outputs
python code/run_c1a.py --output-dir outputs
python code/run_c2_search.py --output outputs/c2_search_nondegenerate.json --maxiter 60 --popsize 14 --rho-min 0.25
python code/analyze_outputs.py --output-dir outputs
python code/verify_outputs.py --package .
```

`run_c3_extension.py` deliberately stops at `n=26` for the closest-to-zero
case and at `n=24` for the other selected cases.  The recursion visits exactly
`2^n-1` prefix nodes; the recorded `n=26` run took 124.47 seconds, projecting
497.88 seconds for `n=28` and 1991.54 seconds for `n=30` on the same machine.

## Main outputs

- `outputs/transition_spectrum.csv`
- `outputs/transition_fit.csv`
- `outputs/curvature_vs_transition.csv`
- `outputs/extended_curvature.csv`
- `outputs/toeplitz_distance.csv`
- `outputs/sr_hessian_landscape.csv`
- `outputs/c1a_results.json`
- `outputs/c2_search_nondegenerate.json`
- `outputs/correction_fit.csv`

No finite-window sign, fit, or search miss in this package is an entropy-rate
theorem.  No positive finite Toeplitz candidate was found, so no directed
interval sign certificate was triggered.
