# Machine Evidence Closure

Date: 2026-09-10, Asia/Singapore.

This is an addendum to the unchanged initial second-review files:

- `frozen_scope.md`
- `review_report.md`
- `source_binding.json`

The initial blocker was the absence of a raw finite determinant/chart certificate. The supplied `machine_input/` packet now discharges that blocker for U1. I did not run arithmetic or formal tools; I inspected the independent implementation, raw outputs, execution history, source bindings, and file hashes.

## Closure Verdicts

| Unit | Closure Verdict | Reason |
| --- | --- | --- |
| U1. Full Lambda-zero missing-edge family | CORRECT | The supplied machine packet independently reconstructs the Gram/Rstar/Rbar/Ahat chain, extracts a fresh determinant quotient P, records zero exact division remainder, supplies the full integer Q chart box, checks seed minors, leaf-swap congruence, and determinant scaling to `det Rstar`. This closes the only blocker in my initial report. |
| U2. Conditional-entropy strictness | CORRECT | My initial review found the reduction correct conditional on U1. With U1 closed, the fixed-coordinate integration of the same positive M closes the conditional-entropy theorem. |
| U3. Center-dependent nonzero-Lambda band | CORRECT | My initial review found the perturbation constants, derivative formula, legality, and quantifiers correct conditional on U2. With U2 closed, the center-dependent band closes. |
| U4. Fixed-diagonal radial obstruction witness | EXCLUDED | Still excluded pending its separate exact gate. I did not use it as theorem evidence or as an entropy counterexample. |
| U5. One-sided perspective bridge | CORRECT, unchanged | The initial verdict already accepted the identities and exact remaining-obligation statement. The stronger coupled inequality remains unproved as stated by the author. |

## Machine Packet Binding

The machine packet is bound by `machine_input_binding.json`: PR64 packet head `5b40617fe7172aa266614aa28688d310218cb387`, executed implementation head `ee33372042d27911a97a14aefc6cb068404d190b`, and PR60 author head `f869fd251c0d6fdad737b6d5efa287307795a87d` (`machine_input_binding.json` lines 2-5).

The machine input source binding ties the PR60 inputs to the same author source commit and main base as the initial review (`machine_input/inputs/SOURCE_BINDING.json` lines 3-5). It identifies the PR60 `certificate.py` and `proof.md` copies by source path (`SOURCE_BINDING.json` lines 17-23), and records that the author P components were extracted as text only and used downstream after fresh determinant construction (`SOURCE_BINDING.json` lines 42-45).

The packet says C2 supplied raw computation-owner artifacts only, no mathematical FIRST/SECOND review, no C1 material, no C3 adjudication, and no `machine_notes`, `FINAL_HANDOFF`, or summary README (`machine_input_binding.json` lines 372-373). I used the artifacts themselves, not a review verdict.

## Independent Implementation Inspection

The implementation states that it constructs `Rstar`, `Rbar`, and `Ahat`, extracts P from `det(Ahat)`, and only then compares with author component strings. It explicitly does not import or execute PR60 `certificate.py` or `bridge_checks.py` (`implementation/pr60_independent_certificate.py` lines 2-7; `implementation/README.md` lines 3-9). The run metadata repeats that construction guard and names the forbidden author scripts (`outputs/run02/run_metadata.json` lines 11-18).

The implementation reconstructs the common scalar objects, the Bernoulli Gram matrix, the qdot reductions, and the reflection identity (`pr60_independent_certificate.py` lines 317-445). It builds `Rstar` in u, builds the short `Rbar` in t, and checks `Rbar(t=u^4)=u*Rstar(u)/4` entrywise (`pr60_independent_certificate.py` lines 357-399 and 830-846). It then forms `Ahat` by the displayed row scaling and checks each entry is a polynomial over QQ (`pr60_independent_certificate.py` lines 448-463 and 848-852).

For the determinant, the source uses two independent polynomial paths: a fraction-free Bareiss determinant and an independent 24-product determinant. It divides by the exact divisor `8*T*(1-T)^3*(1-r^2*T)^3*(1-r^2*T^2)^3`, rejects a nonzero remainder, enforces P term count and degrees, and records that P has integer coefficients (`pr60_independent_certificate.py` lines 483-572).

For the chart, the source first enforces integer P coefficients, then constructs Q by bounded integer coefficient loops matching the author binomial chart. It cross-checks that loop construction against an independent homogeneous-polynomial construction over ZZ, and writes every exponent position in the full `[0..4] x [0..4] x [0..10] x [0..6]` box (`pr60_independent_certificate.py` lines 306-314, 640-721, and 724-767).

For seed and symmetry, the source checks the four seed leading principal minors, the Rbar leaf-swap congruence, and the determinant scaling from `det(Ahat)` to `det Rstar` (`pr60_independent_certificate.py` lines 770-810 and 910-914).

I also compared the stored `Rstar_u_entries` and `Rbar_short_t_entries` strings for row/column symmetry and found no asymmetric entry pairs. `Ahat` is row-scaled by design and is used only for its determinant.

## Raw Artifact Inspection

The run02 layer record shows all eight layers passed, with the determinant layer reporting two determinant methods, zero remainder, P degree `(4,4,10,6)`, 279 P terms, and QQ domain (`outputs/run02/layer_results.json` lines 43-546, especially lines 374-406). The separate `determinant_and_P.json` contains the full P coefficient list, P expression, determinant summary, divisor summary, empty division remainder, and `remainder_zero=true` (`outputs/run02/determinant_and_P.json` lines 2-2551).

The chart artifact `Q_full_box.json` contains the full coefficient array beginning at line 2 and continuing through line 17328, followed by the summary fields. It records variables `X,Y,R,T`, degrees `(4,4,10,6)`, 1731 positive coefficients, 194 zero coefficients, minimum positive coefficient 192, and constant 432 (`Q_full_box.json` lines 17329-17442). The homogeneous-polynomial cross-check records both constructions over ZZ with 1731 terms (`Q_full_box.json` lines 17410-17433). A text scan found no negative `"coeff": -` entries and no object-valued noninteger Q coefficients.

The seed/scaling artifact records the seed minors

```text
1009/7200, 743633/6480000, 1137143/12150000, 9016/253125
```

and records both `Rbar_leafswap_congruence` and `detAhat_scaling_to_Rstar` (`outputs/run02/seed_leafswap_scaling.json`). These are the exact seed and scaling obligations left open in the initial review.

The P author comparison is downstream only: `P_author_component_comparison.json` records `assembled_after_fresh_P=true`, sign-flip and leaf-swap symmetry, and exact agreement with the six text component strings after the fresh P was extracted. This confirms the author P literal is not the source of the determinant quotient.

## Run Chronology

Run01 is a preserved implementation failure, not evidence for or against the mathematics. The ledger states that run01 completed input presence, Bernoulli Gram/reflection, Rstar/Rbar identity, and Ahat entries, then failed in the determinant layer because `mat[row, col]` was used on a list of lists (`execution/LEDGER.md` lines 14-30). `outputs/run01/FAILURE.json` records the same TypeError and traceback.

Run02 repaired only that indexing access and completed inside the original shared window. The ledger records UTC 2026-09-09 15:31:39 to 15:32:32, exit0, Python 3.12.3, SymPy 1.14.0, one CPU/thread, 16 GiB, no GPU, empty stdout/stderr, and no process left running (`execution/LEDGER.md` lines 35-68). `outputs/run02/run_metadata.json` records status PASS, elapsed 52.957 seconds, deadline 2026-09-09 16:13:03 UTC, thread caps, and applied memory limit (`run_metadata.json` lines 19-90). `outputs/run02/exit.json` records exit code 0, and `PASS.json` records the machine boundary as C2 machine arithmetic only.

The packet-to-final delta listed in `machine_input_binding.json` adds the run02 artifacts and modifies only public ledger/status packaging; it does not list the implementation source as changed after the executed head (`machine_input_binding.json` lines 278-373). I infer from that binding that the executed implementation is unchanged through the packet head.

## Mathematical Closure

With the finite machine certificate supplied, the determinant/chart proof now has the missing bridge:

1. `Ahat` is constructed from the short `Rbar` formula with polynomial entries over QQ.
2. `det(Ahat)` is independently computed two ways.
3. Exact division by `8 t J^3 L^3 C^3` gives a P with zero remainder.
4. Fresh P agrees with the author P literal only after extraction.
5. The chart transform gives an integer Q over the full positive-orthant box, with no negative coefficients and positive constant.
6. Therefore P is positive on the `0 <= r < 1` chart; leaf exchange covers `r < 0`.
7. The positive seed and global nonsingularity fix the inertia of `Rbar`, hence `Rstar`.
8. The accepted Schur prefactor then gives `M>0`, and the fixed-direction integration gives the complete entropy Hessian theorem.

This closes U1. Since U2 and U3 were already checked as correct conditional deductions from U1/U2, they now close as CORRECT as well.

## Coverage Boundaries

Independent execution by me: none.

Formal proof-assistant coverage: none.

Novelty and publication priority: not assessed.

General Lambda-nonzero missing-edge Schur positivity outside the explicit band remains incomplete. The fixed-diagonal radial obstruction remains excluded from this closure and is not used as theorem evidence.
