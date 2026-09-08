# N3: Fisher and conditional covariance coupling

Status: ACTIVE_RESEARCH; the general real three-dimensional claim is INCOMPLETE.
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
