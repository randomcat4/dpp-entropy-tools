# PR58 original corridor finite-evidence first review

Role: bounded non-author FIRST source/evidence review of independent PR72 evidence for original PR58 head `1770ed29e8487b8f39aebb4c9466406c7493e580`.

Overall status: CRITICAL_GAPS, narrowly due to source wording in original `RESULT.md` (5.1).

Finite-evidence verdict: ACCEPTED_SCOPED. PR72 supplies adequate independent machine evidence, at C1 source/evidence scope, for the original PR58 compact corridor `3<=t^2<=15`, all 27 author rational comparisons, and the `s=10` separation `W(10)<0` while the full scaled entropy curvature quantity `t^2(-H'')` is positive.

Remaining minimal repair: `source-snapshots/pr72_corridor/inputs/RESULT.md:248`-`250` should not say the rounded decimal string "is" the exact upper endpoint. Replace with wording such as: "whose exact rational upper endpoint has a negative outward decimal display, printed approximately as ..." or "whose rounded printed upper endpoint is approximately ...". This is a precision wording gap only; it does not change the independent rational sign certificate. The strict lower bound in (5.2), `source-snapshots/pr72_corridor/inputs/RESULT.md:254`-`258`, is separate and remains acceptable as a strict displayed lower bound.

## Source binding and provenance

CORRECT / ACCEPTED_SCOPED. The PR72 packet binding records `file_count: 30`, the machine-branch base, the "C1 source/evidence review only; no arithmetic execution" scope, PR72 commit `e557d93e864582c9f9e7bd4384ed21d6ae2f66e2`, and the `research/C2/pr58_corridor50/` prefix at `source-snapshots/pr72_corridor/SOURCE_BINDING.json:1`-`7`. It binds the independent verifier, copied PR58 inputs, run artifacts, and logs at `source-snapshots/pr72_corridor/SOURCE_BINDING.json:8`-`189`, with origin recorded at `source-snapshots/pr72_corridor/SOURCE_BINDING.json:190`.

The copied input binding freezes the original PR58 source commit at `source-snapshots/pr72_corridor/inputs/SOURCE_BINDING.json:2`, binds the original four PR58 files at `source-snapshots/pr72_corridor/inputs/SOURCE_BINDING.json:5`-`21`, and states that construction uses literal rational matrices and displayed definitions while not importing or executing the author checker at `source-snapshots/pr72_corridor/inputs/SOURCE_BINDING.json:23`.

The run provenance is bounded and reproducible as a source artifact: `source-snapshots/pr72_corridor/execution/RUN_LEDGER.json:2`-`6` records MACHINE_PASS and the checker source, `source-snapshots/pr72_corridor/execution/RUN_LEDGER.json:17`-`30` records runtime, single run, exit code, and no live arithmetic, and `source-snapshots/pr72_corridor/execution/RUN_LEDGER.json:31`-`41` records the one-process/one-thread/no-GPU bound and 27 required rational comparisons. The final machine-pass artifact has no failures and lists the six pass files at `source-snapshots/pr72_corridor/outputs/run01/MACHINE_PASS.json:23`-`47`.

## Per-claim review

| Claim | Status | Scoped verdict | Evidence lines | Review conclusion |
| --- | --- | --- | --- | --- |
| The finite evidence is tied to the original fixed rational fixture. | CORRECT | ACCEPTED_SCOPED | `source-snapshots/pr72_corridor/inputs/RESULT.md:148`-`158`; `source-snapshots/pr72_corridor/implementation/independent_pr58_certificate.py:865`-`886`; `source-snapshots/pr72_corridor/inputs/SOURCE_BINDING.json:2`-`23` | The copied PR58 input states the exact `A,C,U,V` fixture and its accepted PR54 provenance. The independent source parses those literal matrices from RESULT section 4, constructs `B=UV^T`, and checks rank/nonzero cross-block structure before building events. |
| The PR72 verifier is independent from the author checker. | CORRECT | ACCEPTED_SCOPED | `source-snapshots/pr72_corridor/implementation/independent_pr58_certificate.py:1`-`9`, `865`-`920`; `source-snapshots/pr72_corridor/outputs/run01/inputs.json:200`-`203`; `source-snapshots/pr72_corridor/machine_notes.md:14`-`27` | The source states and implements a direct reconstruction from RESULT matrices. The author checker is recorded as not opened, executed, or imported. Author output is used only after independent reconstruction for exact-fraction comparison. |
| All 64 complete `6x6` event polynomials are reconstructed directly. | CORRECT | ACCEPTED_SCOPED | `source-snapshots/pr72_corridor/implementation/independent_pr58_certificate.py:529`-`563`, `924`-`992`; `source-snapshots/pr72_corridor/outputs/run01/events.json:2`, `6119`, `6219` | The source builds the full block kernel polynomial and complete-event determinant matrices directly, extracts `q(t)=1-a t^2+b t^4`, and only then performs a posthoc Schur/resolvent cross-check. The raw artifact records `event_count: 64`, the direct-construction method, and status OK. I did not recompute any determinant. |
| Global and fiber cancellations are retained. | CORRECT | ACCEPTED_SCOPED | `source-snapshots/pr72_corridor/implementation/independent_pr58_certificate.py:1039`-`1057`; `source-snapshots/pr72_corridor/outputs/run01/identities.json:1`-`40`, `300`-`314`, `2688`-`2704` | The source checks global `sum mu*a` and `sum mu*b` and both left/right fiber cancellations. The raw identity artifact records zero fraction entries in the fiber tables and status OK. This supports the fixed-marginal cancellation structure used by the accepted analytic proof. |
| Principal and complementary Mobius identities support legality from complete events. | CORRECT | ACCEPTED_SCOPED | `source-snapshots/pr72_corridor/implementation/independent_pr58_certificate.py:1059`-`1077`, `1127`-`1139`; `source-snapshots/pr72_corridor/outputs/run01/identities.json:312`-`314`; `source-snapshots/pr72_corridor/outputs/run01/corridor.json:1273`-`1278` | The source checks both principal and complementary Mobius identities as polynomial equalities for all 64 subsets. The corridor artifact then uses positive complete-event probabilities plus those identities as the legality bridge. |
| The four original intervals cover the compact corridor and use exact extrema, not samples. | CORRECT | ACCEPTED_SCOPED | `source-snapshots/pr72_corridor/inputs/RESULT.md:174`-`178`, `204`-`224`; `source-snapshots/pr72_corridor/implementation/independent_pr58_certificate.py:623`-`640`, `1143`-`1224`; `source-snapshots/pr72_corridor/outputs/run01/corridor.json:2`-`10` | The author theorem specifies the four overlapping intervals and the exact quadratic-extrema rule. The independent source implements endpoints plus rational vertex candidates and checks that the interval union covers `[3,15]`. |
| Exact interval certificates and squared margins pass on `[3,9]`, `[8,12]`, `[11,14]`, `[14,15]`. | CORRECT | ACCEPTED_SCOPED | `source-snapshots/pr72_corridor/implementation/independent_pr58_certificate.py:1191`-`1204`; `source-snapshots/pr72_corridor/outputs/run01/corridor.json:54`-`63`, `4993`-`5018`, `5069`-`5078`, `10008`-`10033`, `10084`-`10093`, `15059`-`15084`, `15135`-`15144`, `20074`-`20099`; `source-snapshots/pr72_corridor/machine_notes.md:55`-`60` | Each interval artifact stores exact rational `q_minus`, `q_plus`, `left`, and `squared_margin` data, and sets both strict positivity flags. This closes the prior C1 finite-evidence gap for the original compact corridor, subject only to the wording repair noted above. |
| All 27 author rational comparisons match. | CORRECT | ACCEPTED_SCOPED | `source-snapshots/pr72_corridor/inputs/author_output_reference.txt:3`-`26`; `source-snapshots/pr72_corridor/implementation/independent_pr58_certificate.py:763`-`773`, `1467`-`1548`; `source-snapshots/pr72_corridor/outputs/run01/reference_compare.json:4`-`541`, `544`-`582` | The source defines the required comparison keys as `Amax`, `Bmax`, six quantities for each of the four intervals, and `s10.q_min`. The raw comparison artifact records 27 matches, no missing required own/reference values, no mismatches, and status `MATCHED_REQUIRED_EXACT_FRACTIONS`. |
| At `s=10`, `W(10)<0` is certified, while `t^2(-H'')>0` remains favorable. | CORRECT | ACCEPTED_SCOPED | `source-snapshots/pr72_corridor/inputs/RESULT.md:230`-`258`; `source-snapshots/pr72_corridor/implementation/independent_pr58_certificate.py:1282`-`1407`; `source-snapshots/pr72_corridor/outputs/run01/s10.json:2`-`22`, `32795`-`32815`, `33045`-`33061`; `source-snapshots/pr72_corridor/STATUS.md:14`-`18` | The source encloses every log by one-sided rational atanh tails, checks `W(10)` has negative upper endpoint and width below the target, and separately checks the direct complete scaled curvature lower endpoint exceeds the stated strict lower bound with certified width. The sign convention is explicit: `I=H(A)+H(C)-H(K)`, so positive `t^2 I''` is positive `t^2(-H'')`, hence negative entropy `H''`. |
| Derivative identities and log-constant cancellations are included in the `s=10` curvature check. | CORRECT | ACCEPTED_SCOPED | `source-snapshots/pr72_corridor/implementation/independent_pr58_certificate.py:1316`-`1327`, `1357`-`1368`, `1402`-`1430`; `source-snapshots/pr72_corridor/machine_notes.md:19`-`20` | The source computes the curvature from derivatives of `p=mu*q`, records the derivative log coefficient, checks the `u,y` normal-form equality, and checks the global/per-fiber log-coefficient cancellations. This addresses the earlier concern that full-event acceleration or log terms might have been silently omitted. |
| Raw outward log evidence is retained. | CORRECT | ACCEPTED_SCOPED | `source-snapshots/pr72_corridor/implementation/independent_pr58_certificate.py:658`-`696`, `1428`-`1465`; `source-snapshots/pr72_corridor/outputs/run01/s10.json:24`, `32802`-`32815`; `source-snapshots/pr72_corridor/machine_notes.md:46`-`49` | The s10 artifact stores all 64 events and declares 80 log terms per event. A structural source/evidence read of the artifact found 64 event records, 80 stored terms per event, and 5120 stored atanh terms. This was an artifact-completeness read only, not an arithmetic verification of the terms. |
| The result does not cover whole chord, PR76, novelty, or formal proof. | CORRECT | ACCEPTED_SCOPED for the exclusion | `source-snapshots/pr72_corridor/frozen_contract.md:7`-`9`; `source-snapshots/pr72_corridor/README.md:24`-`28`; `source-snapshots/pr72_corridor/STATUS.md:23`-`27`; `source-snapshots/pr72_corridor/outputs/run01/MACHINE_PASS.json:18`-`22` | The packet explicitly excludes the joint-additive `s=9/10` witness, issue63 whole-chord work, entropy counterexample claims, novelty, and Lean/formal coverage. This prevents over-integration of the finite machine pass. |

## RESULT (5.1) decimal wording

Status: CRITICAL_GAPS.

Scoped verdict: NEEDS_FIX.

The original `RESULT.md` says that the `W(10)` interval has width `<5.83e-83` and that its upper endpoint "is" the displayed decimal at `source-snapshots/pr72_corridor/inputs/RESULT.md:244`-`250`. The independent packet states that rounded decimal endpoint displays are not exact enclosures at `source-snapshots/pr72_corridor/README.md:24`-`25`, `source-snapshots/pr72_corridor/machine_notes.md:63`-`65`, and `source-snapshots/pr72_corridor/outputs/run01/reference_compare.json:544`.

This sentence should be repaired because the exact rational endpoint governs the certificate, while the printed decimal is display text. The minimal repair is to say that the exact rational upper endpoint is negative and is printed approximately by the displayed decimal, or to say that the rounded displayed upper endpoint is approximately the displayed value.

The strict lower-bound sentence in (5.2) is different. `source-snapshots/pr72_corridor/inputs/RESULT.md:254`-`258` asserts a strict lower bound for `t^2 I''`; the independent source checks the lower endpoint against that bound at `source-snapshots/pr72_corridor/implementation/independent_pr58_certificate.py:1375`-`1378`, and the artifact records `lower_check_passed: true` and the same lower-bound target at `source-snapshots/pr72_corridor/outputs/run01/s10.json:33057`-`33061`. No wording repair is required there.

## W/V convention

The original author source uses `W=E[b psi]` and states `E[y psi]=s^2 W` at `source-snapshots/pr72_corridor/inputs/RESULT.md:44`. This review therefore treats `W(10)` as the `E[b psi]` sign claim and the full curvature claim as the separate `t^2(-H'')>0` certificate. Any later compute-contract label correction between `W` and `V=E[y psi]=s^2 W` is not an author defect in original PR58.

## Final separated statuses

General analytic proof: unchanged from the previous C1 accepted scopes.

Original finite corridor evidence: ACCEPTED_SCOPED, using PR72 independent evidence and raw artifacts.

Original `s=10` `W(10)<0` plus positive `t^2(-H'')`: ACCEPTED_SCOPED, using PR72 independent evidence and raw artifacts.

Static code/evidence review: ACCEPTED_SCOPED; see `corridor_code_review.md`.

Formal coverage: INCOMPLETE. This is exact finite machine evidence, not Lean or a formal proof artifact.

Novelty: NOT_ASSESSED. No priority certification is performed.

Remaining source repair before clean publication: NEEDS_FIX only for the (5.1) rounded decimal wording described above.
