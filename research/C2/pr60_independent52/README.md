# Independent machine reconstruction of the PR60 full-r certificate

**MACHINE_PASS**, for PR60 source
`f869fd251c0d6fdad737b6d5efa287307795a87d`, based on main
`9dcb6e9079ca57f94e0e30d63161cda89ca61fae`.

The independent implementation rebuilt the displayed long and short Schur
matrices, verified their normalization, computed a fresh determinant and
extracted P before comparing any author polynomial. It then constructed the
symmetry-chart Q by integer loops and homogeneous polynomial multiplication.
All 1925 coefficient positions pass: 1731 positive, 194 zero, minimum 192,
constant 432. The seed, polynomial/matrix symmetries and determinant scaling
also pass. The supplied author scripts and old r=0 result were not executed
or used as construction inputs.

Start with [machine_notes.md](machine_notes.md), the
[successful result](outputs/run02/PASS.json),
[full layer records](outputs/run02/layer_results.json), and
[execution ledger](execution/LEDGER.md). The full matrices, determinant/P and
Q coefficient box are preserved beside the result. The failed first run is
retained in [outputs/run01](outputs/run01).

Reproduce from the repository root with Python3.12 and SymPy1.14.0:

```sh
python research/C2/pr60_independent52/implementation/pr60_independent_certificate.py \
  --input-root research/C2/pr60_independent52/inputs \
  --out <new-output-directory> --wall-seconds 2700
```

The executed runs used the [guard](execution/run_guard.sh) with a single
shared hard deadline, one process/CPU/thread,16GiB and no GPU. The script also
honors C2_ABSOLUTE_DEADLINE_EPOCH and rejects floating mathematical objects.
The first run's indexing exception was repaired in one line; the second
completed in52.957seconds. Both processes have exited.

See [frozen_contract.md](frozen_contract.md) and
[inputs/SOURCE_BINDING.json](inputs/SOURCE_BINDING.json) for exact inputs.
C2 supplies machine evidence; C1 owns mathematical bridge FIRST and C3
receives the hand-off. Exact arithmetic does not replace the analytic review
of domain coverage, fixed directions, inertia and integration. This packet
has no separate theorem FIRST/SECOND verdict, novelty or Lean claim.