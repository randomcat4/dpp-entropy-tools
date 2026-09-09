# PR58 presentation repair review

Overall verdict: `CORRECT / ACCEPTED_SCOPED`; both presentation-only repairs are closed.

Unless a longer alias is written explicitly, source paths below are under `source-snapshots/pr58_presentation_repair/`.

The binding records exactly two changed files and one addition/one deletion in each at `source-snapshots/pr58_presentation_repair/SOURCE_BINDING.json:2-16`. I verified this bound file has 22 lines. It records parent `5ab3cae1c49da8334057596f46a4bd8fc449b98c`, commit `ce9ade6d57469f0a4a67365604c66eb4cc290fc5`, file count 2, and the stated scope of two presentation sentences with no formula/code/output change at `SOURCE_BINDING.json:18-21`.

The corridor endpoint wording concern is closed. The repaired `RESULT.md` now says the exact rational upper endpoint is negative and is “printed approximately as” the decimal value at `source-snapshots/pr58_presentation_repair/RESULT.md:248`. This directly resolves the earlier concern that a rounded string had been presented as the exact endpoint.

The additive table-order presentation concern is closed. The repaired addendum now states that rows and columns both use subset-mask order `0,1,...,7`, with bit `i` recording coordinate `i+1`, at `source-snapshots/pr58_presentation_repair/ADDENDUM_JOINT_ADDITIVE.md:171`. This matches the PR76 compute request’s table convention and the independent checker’s row-major event order.

This closure does not repair the separate PR76 additive literal-bound defect in equation (3.5). It also does not certify the corrected author-W decimal in equation (3.6). Those remain governed by the separate additive machine-evidence review.
