# I05-W1 second-round checkpoint

This directory records the existing `I05-W1-20260909-R2` result before the next open-exploration step.

Status of the existing result: **PROVED_WITH_SCOPE / NOT_INDEPENDENTLY_REVIEWED**.

Proved claims: the exact conditional Schur factorization; the radial lifting principle; full-chord concavity when one block has dimension at most two; the coordinate-support-at-most-two extension; and the rank-two exterior-algebra likelihood formula.

Not independently reviewed: every second-round theorem and the exact numerical obstruction examples. The web author’s alternative derivations and reruns are cross-checks only. Codex/server review remains separate.

Failed routes retained here: pointwise nonnegativity of the `Q log(P_s/P_0)` term; exact DPP preservation under whole-block refresh; and unrestricted use of orthogonal changes of observation basis.

The longer Markdown files are split only because the GitHub connector transports bounded UTF-8 blobs. Reconstruct them by concatenation in lexical order:

```sh
cat RESULT.part*.md > RESULT.md
cat frozen_statement.part*.md > frozen_statement.md
cat proof.part*.md > proof.md
cat attempts.part*.md > attempts.md
cat sources.part*.md > sources.md
cat verification.part*.md > verification.md
cat HANDOFF.part*.md > HANDOFF.md
```

The next commit on the same PR will add the continued general rank-two exploration, precise computational review tasks, and an updated self-contained package.