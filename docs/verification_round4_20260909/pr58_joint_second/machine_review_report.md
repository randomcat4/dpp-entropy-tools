# Independent finite SECOND review: PR58 machine witness

Overall verdict:

- Finite witness machine packet: `CORRECT` as a raw independent machine certificate, with the first-stop limitation below.
- Original author literal equation (3.4): `CORRECT`.
- Original author literal equation (3.5): `REJECTED` at the printed upper bound `166.44125195305153`.
- Original author literal equation (3.6): `INCOMPLETE` for the author-W decimal in this PR76 machine run; the run's failed comparison is a request-label W/V mismatch, not an author error.
- Original author literal equation (3.7): `CORRECT`.
- Repaired joint-bounds patch to head `89aa874c24dd5a3ea98f8474826392560b1d0397`: `CORRECT`.

The repaired text supports the finite non-necessity witness for the joint-additive sufficient criterion and the qualitative negative author-W sign. It does not imply an entropy-concavity counterexample, a general whole-chord theorem, novelty, formal verification, or a new all-literals machine PASS.

## Binding

`machine_input_binding.json` records PR76 head `a7979c33b6e82431b6ddf1d39ac69e254d7b655a`, executable head `bbc9bc19b915ebad0ea8e8bea00580d4eebc5246`, and author numerical head `a4f05cc962985015b71635bf633acce9dfe76866`. I recomputed all 28 SHA-256 hashes in `machine_input/`; every file matched the binding.

The new repair is bound by `joint_bounds_delta_binding.json`: parent `ce9ade6d57469f0a4a67365604c66eb4cc290fc5`, head `89aa874c24dd5a3ea98f8474826392560b1d0397`, one changed file, and patch SHA-256 `37fa9e025008591a0e8e4d99a464e2f100339a6214d33a43c0f49ff6a6eb8c68`. The earlier table-order patch remains bound by SHA-256 `2dbdee1f7d1b0c395849027acf1a503a26580516da05439c85a06f599257bdaf`.

## Implementation and inputs

Verdict: `CORRECT`.

Relevant sources:

- `machine_input/implementation/independent_pr58_additive52_checker.py` lines 1-72, 205-238, and 830-848.
- `machine_input/inputs/REQUEST.md` lines 1-32.
- `machine_input/inputs/SOURCE_BINDING.json`.

The checker is self-contained. It uses Python standard-library `Fraction`, embeds the requested rational matrices and dual table literally, and states that it does not import, read, or execute the author checker. The metadata output also records `author_checker_read_import_execute=false` and `reference_files_accessed=false`.

The literal request asks for the finite section-3 witness only. It does not extend the original compact-corridor contract or the whole-chord problem. It also states that a finite witness refutes necessity of the sufficient condition while preserving true favorable curvature, so it is not an entropy-concavity counterexample.

## Execution chronology

Verdict: `CORRECT`.

Relevant sources:

- `machine_input/execution/RUN_LEDGER.json`.
- `machine_input/execution/run_guard.sh` lines 1-53.
- `machine_input/execution/CONTRACT_CORRECTION.md` lines 1-26.
- `machine_input/outputs/run01/00_metadata.json`, `exit.json`, `stdout.log`, `stderr.log`, `start_utc.txt`, `deadline_utc.txt`, `arithmetic_pid.txt`, `timeout_pid.txt`, `cpu_affinity.txt`, and `final.json`.

The raw execution record shows exactly one run. It started at `2026-09-09T16:21:24Z`, had deadline `2026-09-09T16:31:24Z`, stopped at `2026-09-09T16:22:48Z`, exited with code `20`, and wrote `LITERAL_BOUND_CERTIFIED_FALSE`. The guard script enforces one active owner lock, exports one-thread BLAS settings, pins one CPU, sets a 600-second absolute deadline, records PIDs, and writes the exit record.

The post-launch correction was published at `2026-09-09T16:22:08Z`, after run01 began. The ledger and correction file state that no corrected arithmetic was launched and the original deadline was not reset. Therefore the retained scalar/comparison files are raw run01 artifacts, not a corrected rerun.

## Legality and all 64 events

Verdict: `CORRECT`.

Relevant sources:

- checker lines 413-445, 511-538, 849-891, 893-996, and 1140-1204.
- `outputs/run01/02_linear_algebra.json`, `03_block_marginals.json`, and `04_events.json`.

The checker verifies exact principal-minor positivity for `A`, `I-A`, `C`, `I-C`, the Schur complement `C-s B^T A^{-1}B`, and the Schur complement for `I-K`. The recorded output has `B_rank=2`, `B_dense=true`, and all six positivity checks true.

The event layer contains `event_count=64`, event indices `0..63`, all `q>0`, and all atom probabilities `P>0`. The event construction uses subset masks, checks the complete-event polynomial degree, checks that the constant term equals the product marginal, rejects odd or degree-six terms, reconstructs the normalized quadratic `q_s=1-sa+s^2b`, and records each event row.

This supports strict legality and complete-event coverage for the finite point `s=9/10` as a raw machine certificate.

## Marginals and cancellations

Verdict: `CORRECT`.

Relevant sources:

- checker lines 999-1066 and 1174-1208.
- `outputs/run01/03_block_marginals.json` and `05_cancellations.json`.

The block marginals contain eight positive complete-event probabilities on each side and both sums are exactly one. The cancellation output records total probability one, fixed row and column marginals, zero `a` and `b` conditional means on every row and column, zero direct-log coefficient marginals, and zero dual row and column sums.

The dual-table row/column zero statement is therefore supported by the retained machine output and the earlier table-order patch makes the prose ordering match the checker ordering.

## Fisher, acceleration, and scalar forms

Verdict: `CORRECT`.

Relevant sources:

- checker lines 893-996 and 1069-1138.
- `outputs/run01/04_events.json` and `06_forms.json`.

At each event, the checker records both the direct differentiated Fisher/log-acceleration coefficients and the decomposed `Phi + A2 + W` coefficients. It requires equality of the eventwise rational pieces and eventwise log coefficients. It then builds aggregate forms for `P0`, the run's field named `W`, direct curvature, and `sum_cpsi`, and requires the aggregate direct form to equal `P0 + A2 + W`.

The run reached scalar comparison, so these exact identity checks passed before the first-stop failure.

Important notation point: the run's field named `W` is actually `V=E_mu[y psi]`, because the request accidentally named `E_mu[y psi]` as W. The author defines `W=E_mu[b psi]`. This is stated in `REQUEST_CORRECTION.md` lines 1-3 and `CONTRACT_CORRECTION.md` lines 5-13. The request-label error is not an author discrepancy.

## Dual residual lower bound

Verdict: `CORRECT`.

Relevant sources:

- checker lines 1069-1093 and 701-714.
- `outputs/run01/06_forms.json`, `07_scalar_enclosures_N80.json`, and `08_comparisons_N80.json`.

The checker builds `sum_cpsi` from `sum c_ST psi_ST` and `dual_denominator` from `sum c_ST^2/P_s(S,T)`. It encloses `L=(sum c psi)^2/dual_denominator` and `T=4(P0+A2)^2/A2`, then compares `L>T`.

The retained `N=80` scalar packet gives:

- `L` in `[192.456447546638183766230914, 192.456447546638183766230915]`;
- `T` in `[166.441251953051540106785812, 166.441251953051540106785813]`.

The qualitative comparison `L>T` is `PASS`, so the joint-additive sufficient criterion fails strictly at this finite point.

## Rational logarithm interval mechanism

Verdict: `CORRECT` by static inspection of implementation and retained packet structure.

Relevant sources:

- checker lines 538-642, 701-714, and 736-783.
- `outputs/run01/07_scalar_enclosures_N80.json`.

The checker reduces positive rational `q` as `x=2^k z` with `1<=z<2`, uses `r=(z-1)/(z+1)`, encloses the nonnegative atanh series with a rational tail, and combines with a shared log-2 enclosure. The scalar payload records `terms=80`, `widths_ok=true`, width target `1e-18`, and 64 event log-audit entries. I did not rerun or formally verify this mechanism; I inspected the source and the retained JSON structure/leaves.

## Original printed claims

Verdict by displayed equation:

| Original equation | Original text checked | Machine SECOND classification |
| --- | --- | --- |
| (3.4) | `R_add > 192.45644754663817` | `CORRECT`; `L` lower endpoint is above the printed bound. |
| (3.5) | `4(P+A2)^2/A2 < 166.44125195305153` | `REJECTED`; retained `T` interval is disjoint above the printed upper bound. |
| (3.6) | `W(9/10) < -2.253552138695407` | `INCOMPLETE` for author-W in PR76; run01 compared the request-labelled field `W`, actually `V=E_mu[y psi]`, so the failed literal comparison is request-induced and is not an author-W falsehood. |
| (3.7) | `t^2 I''(t) > 4.653598245398841 > 0` | `CORRECT`; retained true/direct curvature interval is above the printed bound. |

The original sentence "All inequalities above are certified..." is no longer acceptable literally, because the machine run stopped at the first exact mismatch in (3.5), and (3.6)'s decimal was not certified for author-W by this run.

## Repaired text at head `89aa874c24dd5a3ea98f8474826392560b1d0397`

Verdict: `CORRECT`.

Relevant sources:

- `joint_bounds_patch.diff` lines 1-37.
- `joint_bounds_delta_binding.json`.
- `outputs/run01/07_scalar_enclosures_N80.json` and `08_comparisons_N80.json`.
- `execution/CONTRACT_CORRECTION.md`.

The repair changes (3.5) to the coarser strict upper bound `166.441251953051541`, which is supported by the retained `T` interval whose upper endpoint is `166.441251953051540106785813`.

The repair changes (3.6) to the qualitative statement `W(9/10)<0`. The run's negative scalar is the signed curvature contribution `V=E_mu[y psi]`, with retained enclosure

`[-1.825377232343279850885156, -1.825377232343279850885155]`.

Since the frozen point has `s^2>0`, the sign of `V=s^2 W_author` supports the qualitative author-W sign. It does not support the withdrawn author-W decimal as a PR76-certified literal.

The repair also states that the original PR76 run stopped at the first false literal upper bound, that the `W` field followed the original request label, that the direct curvature interval supports (3.7), and that these are deductions from retained rational enclosures rather than a rerun or a new all-literals machine PASS. Those statements match the raw ledger, correction record, and retained output files.

## Final accepted scope

Accepted:

- independent finite machine reconstruction of the fixture inputs, mask-order table, rank-two dense `B`, strict legality at `s=9/10`, product marginals, all 64 complete events, fixed marginals, `a/b` cancellations, dual row/column cancellations, complete Fisher-plus-acceleration decomposition, dual residual lower bound, and rational-log scalar enclosures as raw PR76 evidence;
- qualitative finite separation: the joint-additive sufficient criterion is not necessary at this point, while the complete curvature remains positive;
- qualitative `W(9/10)<0` after applying the W/V correction;
- repaired numerical text in the joint-bounds patch.

Rejected:

- original equation (3.5)'s upper bound `166.44125195305153`;
- original blanket wording that all displayed numeric inequalities were certified exactly as printed.

Incomplete / not certified:

- original author-W decimal in (3.6) as a PR76 machine-certified literal;
- any rerun after the correction;
- any claim that PR76 ended in an all-literals machine PASS;
- entropy-concavity counterexample status;
- general dense correlated whole legal chord;
- novelty, priority, or formal verification;
- original `[3,15]` / `s=10` corridor computation.

## Execution limits for this review

I performed no new arithmetic, no checker execution, no SymPy, no interval recomputation, no entropy computation, no formal proof, no remote computation, and no GitHub mutation. I used static source reads, JSON inspection, and SHA-256 hash checks only.
