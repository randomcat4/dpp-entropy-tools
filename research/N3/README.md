# N3: Fisher and conditional covariance coupling

Status: STOPPED_SUBSTANTIVE after the second round; the general real
three-dimensional claim and the exact beta-zero subproblem are INCOMPLETE.
The current result is in `round2/verdict.md`, with execution state in
`round2/checkpoint.json` and fixed reviews in `round2/verifications/index.md`.
Round two preserves a strict beta-zero existence certificate, a restricted
weak-edge nonvanishing mechanism and a new locked-odds dominance obstruction.
The following paragraphs describe the preserved first-round record.
Baseline: `fa504ec74e16843fafc395880d7ba99b4c1d2129`.
Coordination: https://github.com/randomcat4/dpp-entropy-tools/issues/20.

The frozen target is in `frozen_theorem_v1.md`. This route studies all real
symmetric directions at arbitrary strict real symmetric three-point kernels.
It does not repeat the exchange-symmetric family or enter dimension four.

Ownership: main owns this directory's top-level records and `main/`;
three isolated child branches own respectively `inequality/`, `falsification/`,
and `review/`. Author derivations and independent checks remain separate.
Server computation uses the existing Python environment, one BLAS/OpenMP
thread per job, no GPU, at most two simultaneous compute jobs initially.
All public artifacts exclude private handoffs and connection information.

Success means either a complete proof, a strictly feasible positive entropy
chord certificate, or a new exact coupling lemma / explicit obstruction with
the smallest unclosed obligation. Finite non-hits do not certify the target.

This round derived an exact conditional-score decomposition, strictly refuted
its sufficient condition both for arbitrary directions and at the actual
trace optimizer, and found an analytic rare-atom obstruction to the richer
one/two-point Fisher projection. The missing DPP alignment bound remains open.
Read `verdict.md` and `checkpoint.json` for the final status; individual frozen
author versions and early scout non-hits are retained as historical evidence.
