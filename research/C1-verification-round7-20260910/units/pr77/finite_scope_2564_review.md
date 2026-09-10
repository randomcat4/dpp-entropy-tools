# PR77 2564 finite-scope delta-FIRST review

Delta verdict: `CLOSED_BY_NARROWING` for the original Section 9 over-broad true-rate derivative wording; `CLOSED_DISCLOSURE` for the README/output-summary labeling problem; `STILL_PENDING_C2` for raw finite certificate evidence, source/output hashes, and independent reconstruction. This text delta does not change code, outputs, constants, parameters, thresholds, or finite arithmetic status.

Novelty: `NOT_ASSESSED`.

Formal verification: `NOT_PERFORMED`.

Arithmetic/computation: `NOT_PERFORMED`.

## 1. Section 9 finite-block narrowing

Status: `CLOSED_BY_NARROWING`.

The compare changes the Section 9 title from a true-rate-looking second-order comparison to `Beam-splitter comparison: finite-block second order` (`source-snapshots/pr77_delta_2564/COMPARE.json:1-1`; `source-snapshots/pr77_delta_2564/proof.md:540-540`). It replaces the old unindexed `Q_u`, `I_out`, and `E_occ` statements with fixed-block objects `Q_{u,n}`, `I_out,n`, and `E_occ,n`, and states the exact finite entropy identity

`2H_n(t_*)-H_n(t_*-u)-H_n(t_*+u)=I_out,n(u)+E_occ,n(u)`

for each fixed block (`source-snapshots/pr77_delta_2564/proof.md:548-553`).

The revised text then explicitly says that dividing by `n` gives only the true-rate value identity and does not justify differentiating the limits (`source-snapshots/pr77_delta_2564/proof.md:555`). This is the needed narrowing: the value identity may be retained because it is an entropy-rate limit of finite entropy identities, while the derivative passage is no longer claimed from that limit.

## 2. Finite `O_n` and second derivatives

Status: `ACCEPTED_SCOPED`.

The revised text correctly changes the local expansion statements to finite-block estimates with constants allowed to depend on `n`:

`Q_{u,n}-Q_{0,n}=O_n(u^2)` and `I_out,n(u)=D(Q_{u,n}||Q_{0,n})=O_n(u^4)` (`source-snapshots/pr77_delta_2564/proof.md:557-562`).

It then restricts the derivative conclusions to the finite block:

`I_out,n''(0)=0` and `E_occ,n''(0)=-2H_n''(t_*)` (`source-snapshots/pr77_delta_2564/proof.md:564-569`).

This closes the earlier defect where finite-block evenness and finite-block relative-entropy expansion were too easily read as true-rate derivative claims. The revised statement does not require a missing rate theorem.

## 3. True-rate derivative boundary

Status: `CLOSED_BY_NARROWING`; no new theorem accepted.

The revised proof states that true-rate derivative assertions would require an additional uniform-in-volume fourth-order remainder or an analytic response bridge for the doubled output process, and that this bridge is not established in Section 9 (`source-snapshots/pr77_delta_2564/proof.md:571`). It also states that no such assertion is used in the fixed midpoint and point-curvature certificate route in Sections 6-8 (`source-snapshots/pr77_delta_2564/proof.md:571`).

This is the correct resolution of the prior Section 9 finding. The old over-broad true-rate derivative implication is closed by narrowing and disclosure, not by proving the missing rate bridge. The true-rate derivative bridge remains `INCOMPLETE`, but it is no longer a premise for the main finite-certificate route.

## 4. README evidence-packaging clarification

Status: `CLOSED_DISCLOSURE`; evidence still `STILL_PENDING_C2`.

The new README section explicitly says the committed `output/*.json` files are abbreviated, curated author summaries, not literal full JSON payloads emitted by every displayed checker, and that PASS fields are not independent certificates (`source-snapshots/pr77_delta_2564/README.md:69-73`). It identifies the precise issues previously found:

1. midpoint and point-curvature `.full.json` raw intervals and tails are not included;
2. the pair-Fisher summary uses display polynomials instead of the checker's coefficient-list schema;
3. the supplemental run record lists commands but does not replace source/output hashes or raw interval evidence;
4. independent reconstruction is still required before finite claims receive external acceptance.

This closes the mislabeling/non-disclosure part of the prior code-review findings. It does not close the underlying evidence gap: no raw midpoint intervals, raw point-curvature intervals, determinant histograms, source/output hashes, or independent C2 artifacts are added by this delta.

## 5. Point run-record issue

Status: `CLOSED_DISCLOSURE`; `PARTIAL_FIX` from the prior 8de8 supplemental run record remains; full evidence `STILL_PENDING_C2`.

The 2564 README accurately discloses the limited role of the supplemental run record: it lists author commands but does not replace source/output hashes or raw interval evidence (`source-snapshots/pr77_delta_2564/README.md:71-71`). This closes the remaining disclosure issue around the point-run listing. It does not convert the point-curvature author PASS into independent acceptance.

## 6. Pair-Fisher display-vs-schema issue

Status: `CLOSED_DISCLOSURE`; quantitative acceptance `STILL_PENDING_C2`.

The README now discloses that the pair-Fisher output summary uses display polynomials rather than the checker's coefficient-list schema (`source-snapshots/pr77_delta_2564/README.md:71-71`). This closes the public-labeling defect found in the 8de8 delta code review.

The underlying quantitative Fisher status is unchanged. The checker and output were not modified in this delta; author PASS remains author evidence only, and independent finite reconstruction would still be required before external quantitative acceptance.

## 7. Unchanged materials and non-effects

Status: `UNCHANGED`.

`SOURCE_BINDING.json` records only README and proof changes, with 21 other files unchanged (`source-snapshots/pr77_delta_2564/SOURCE_BINDING.json:1-29`). Therefore this delta does not affect:

1. midpoint or point-curvature code;
2. output JSON content;
3. certificate parameters, constants, thresholds, or depths;
4. Fisher checker implementation;
5. original Sections 1-8 analytic gates;
6. whole-interval curvature status.

The README still says the whole-interval curvature statement is incomplete and that no positive true-rate counterexample is obtained (`source-snapshots/pr77_delta_2564/README.md:65-73`). The proof conclusion still says the fixed midpoint theorem is author proof only and the requested whole-interval curvature theorem remains incomplete (`source-snapshots/pr77_delta_2564/proof.md:575-579`).

## Delta finding table

| Prior finding or risk | 2564 delta ruling | Reason |
| --- | --- | --- |
| Section 9 finite `O(u^4)` read as true-rate derivative proof | `CLOSED_BY_NARROWING` | Now fixed-block `O_n`, fixed-block derivatives, true-rate derivative bridge explicitly incomplete. |
| True-rate value identity in Section 9 | `ACCEPTED_SCOPED` | Retained only as value-rate limit; no derivative passage claimed. |
| Missing Section 9 rate theorem | `NO_LONGER_LOAD_BEARING` | The proof now says the bridge is not established and not used for Sections 6-8. |
| Curated author summaries not labeled as such | `CLOSED_DISCLOSURE` | README explicitly labels them as abbreviated curated summaries, not literal full JSON or independent certificates. |
| Pair-Fisher display polynomial output differs from checker schema | `CLOSED_DISCLOSURE` | README explicitly discloses display-polynomial vs coefficient-list schema. |
| Missing raw midpoint/point intervals and tails | `STILL_PENDING_C2` | No raw full JSON or independent reconstruction added. |
| Missing source/output hashes | `STILL_PENDING_C2` | README discloses absence; it does not supply hashes. |
| Point run-record omission | `PARTIAL_FIX` / `CLOSED_DISCLOSURE` | Prior supplemental record listed command; README now states its limited evidentiary role. |
| Whole-interval curvature | `INCOMPLETE_UNCHANGED` | Delta keeps the boundary and adds no continuum proof. |

## Final delta disposition

The 2564 text delta successfully repairs the two management/scope problems it targets: Section 9 is now finite-block second order with true-rate derivatives explicitly incomplete, and the README now discloses that output JSON files are curated author summaries rather than raw independent certificates.

It does not supply finite C2 evidence. Midpoint, point-curvature, and quantitative Fisher external acceptance remain pending independent reconstruction and raw evidence under the existing finite-evidence contract.
