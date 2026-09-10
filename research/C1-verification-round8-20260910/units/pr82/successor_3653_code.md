# PR82 successor 3653 static source and evidence report

Status: **static coverage complete; no execution performed**.

## Frozen evidence coverage

The frozen binding at `source-snapshots/pr82_delta_3653/SOURCE_BINDING.json:L1-L79` records base `6ecc004a3f99f97369ea5af53f1136b59cf2129c`, head `365347e9933f30af64e63c33fc403b3c4fbdb3fa`, the public compare URL, and seven changed files. I read all seven changed files listed in `SOURCE_BINDING.json:L4-L72`.

The pure dependency binding at `source-snapshots/pr82_dependencies/SOURCE_BINDING.json:L1-L59` records the frozen PR66 author sources and accepted-main PR53 sources used for dependency checks. I used only the theorem/proof sources needed for the complete-event inverse, non-nullness, parity, entropy-rate identification, and matching lower-bound imports.

One external primary source was checked because it is load-bearing for the coupling step: Bressaud--Fernandez--Galves, arXiv `math/9806132`, <https://arxiv.org/abs/math/9806132>. The check was limited to the ratio condition, maximal agreement coupling, agreement-length chain, and return/renewal objects cited by `c4_response_p4_one_loss.md:L152-L268` and `c4_response_p4_selfcontained_closures.md:L97-L167`.

## Source/output inventory

| Source | Static role | FIRST coverage |
|---|---|---|
| `source-snapshots/pr82_delta_3653/research/I05-DPP-31-20260910/README.md` | Current theorem statement, route priority, nonclaims, failure ledger | Read fully, lines 1--237. |
| `source-snapshots/pr82_delta_3653/research/I05-DPP-31-pr66-lowreg-20260910/c4_response_p4_one_loss.md` | Current consolidated one-power finite-response proof | Read fully, lines 1--618. |
| `source-snapshots/pr82_delta_3653/research/I05-DPP-31-pr66-lowreg-20260910/c4_response_p4_measure_continuity.md` | DPP cylinder continuity, invariance and uniqueness | Read fully, lines 1--95. |
| `source-snapshots/pr82_delta_3653/research/I05-DPP-31-pr66-lowreg-20260910/c4_response_p4_continuity_detail.md` | Two-scale continuity and difference-quotient remainder details | Read fully, lines 1--230. |
| `source-snapshots/pr82_delta_3653/research/I05-DPP-31-pr66-lowreg-20260910/c4_response_p4_selfcontained_closures.md` | Defective renewal proof and Banach Cauchy closure | Read fully, lines 1--258. |
| `source-snapshots/pr82_delta_3653/research/I05-DPP-31-pr66-lowreg-20260910/c4_response_p4_pr66_dependency_audit.md` | PR66 complete-event dependency rederivation and boundary | Read fully, lines 1--304. |
| `source-snapshots/pr82_delta_3653/research/I05-DPP-31-pr66-lowreg-20260910/c4_response_spatial_truncation_p6.md` | Optional stronger-range spatial memory truncation rate | Read fully, lines 1--231. |

No source file, author file, dependency file, executable artifact, or generated output was modified. No tests, scripts, checkers, imports, compiles, finite computations, interval jobs, entropy jobs, numerical reconstructions, symbolic algebra systems, or formal tools were run.

## Static findings

### NEEDS_FIX_STATIC: README authoritative file order omits the current operative proof file

`source-snapshots/pr82_delta_3653/SOURCE_BINDING.json:L34-L42` includes the newly added `c4_response_p4_one_loss.md`, and that file declares at `c4_response_p4_one_loss.md:L1-L7` that it supersedes the earlier `p>8` threshold conclusion and gives the direct infinite-volume one-loss proof. The theorem proof reviewed and accepted in `successor_3653_review.md` is this one-loss file.

However, the README’s “Authoritative file order and failure ledger” at `README.md:L223-L232` lists `c4_response_p4_repair.md` as “main author proof” and then lists boundary correction, dependency audit, self-contained closures, source audit, measure continuity, continuity detail, and the older `p>8` files. It does not list `c4_response_p4_one_loss.md` at all.

Impact: the mathematical route can still be reviewed from the frozen binding and source file, but the packet’s own navigation/priority text is stale. A reader following only the README index could treat the old repair file as the operative main proof and miss the actual 3653 replacement proof. The README should add `c4_response_p4_one_loss.md` as the current consolidated one-loss proof, or explicitly state how it supersedes the historical `c4_response_p4_repair.md` route.

### MINOR_TEXT: one TeX/Markdown typo in the operative proof

At `c4_response_p4_one_loss.md:L525`, the condition is written as ``widehat g(k) != 0`` rather than the surrounding TeX style `\widehat g(k)\ne0`. This is editorial only; the theorem statement in `README.md:L26-L30` has the intended condition.

## Evidence classifications

- **ACCEPTED_SCOPED:** current one-loss proof source, DPP continuity supplements, PR66 pure complete-event imports, PR53 matching import, and optional `p>6` truncation lemma in its stated scope.
- **INCOMPLETE_EXTRA:** old `p>8` finite-memory stationary second-response bridge, preserved but not imported.
- **OPEN / NOT USED:** old PR66 Dobrushin A1/A2 applicability route.
- **NOT REVIEWED:** novelty/priority, formalization, machine recomputation, exact arithmetic, or any live-head changes after `365347e9933f30af64e63c33fc403b3c4fbdb3fa`.
