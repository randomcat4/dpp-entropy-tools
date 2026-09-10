# PR81 d995 SECOND code/static artifact review

## Verdict

`CORRECT` for the bounded static artifact review. The allowed packet contains Markdown proof sources and `input_binding.json`; it does not contain executable checker code. I did not run, import, compile, or inspect any external author script.

## Binding and file integrity

`source_binding.json` records machine-computed SHA-256, byte count and line count for:

- `input_binding.json`
- `input/coupled_gram_fixed_shape.md`
- `input/proof.md`
- `input/shared_corner_cell_theorem.md`
- `pr70_source/proof.md`
- `pr70_source/thinning_bridge.md`

Result: 5/5 bound source files present, 0 delivered SHA mismatches, 0 line-count mismatches.

The binding distinguishes original public source identity from the redacted delivered packet. Three files have different `original_sha256` and `delivered_sha256` because nonmathematical review-history/status prose was withheld with line counts preserved. I used the delivered hashes for packet integrity and did not treat original Git/blob SHA as the local file digest.

## Executable code status

No executable code file was in the allowed source list. Mentions of author checkers occur only as prose:

- `shared_corner_cell_theorem.md` says `verify_shared_corner_cell.py` verifies identities and minors and passed under Python/SymPy, but marks it as same-author supporting evidence only: [shared_corner_cell_theorem.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md#L353)–[shared_corner_cell_theorem.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/shared_corner_cell_theorem.md#L365).
- `coupled_gram_fixed_shape.md` labels direct evaluations, chain-rule diagnostics, relaxed searches and stress tests as diagnostics rather than interval certificates or theorems: [coupled_gram_fixed_shape.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/coupled_gram_fixed_shape.md#L184)–[coupled_gram_fixed_shape.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/coupled_gram_fixed_shape.md#L220), [coupled_gram_fixed_shape.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/coupled_gram_fixed_shape.md#L366)–[coupled_gram_fixed_shape.md](https://github.com/randomcat4/dpp-entropy-tools/blob/d99550bfd9eee623ec80edbca1da17ff0ddbe4bf/research/I05-22-R5-logmean-imbalance/coupled_gram_fixed_shape.md#L393).
- PR70 proof source states its exact checker is author evidence, not independent review or proof-assistant certification: [pr70_source/proof.md](https://github.com/randomcat4/dpp-entropy-tools/blob/f7be60759fd4d65184803b6585965dc7e5ccd624/research/I05-22-R4-paired-perspective/proof.md#L321)–[pr70_source/proof.md](https://github.com/randomcat4/dpp-entropy-tools/blob/f7be60759fd4d65184803b6585965dc7e5ccd624/research/I05-22-R4-paired-perspective/proof.md#L332).

I therefore did not accept checker PASS, diagnostic floating values, relaxed-search output, or printed minors as independent machine evidence. The positive review rests on the handwritten analytic proof path in `shared_corner_cell_theorem.md`.

## Static artifact issues

No blocking artifact issue found.

One non-blocking writing issue: formula (6), the shared-corner cell decomposition, is introduced as “A direct transformation” rather than expanded line-by-line. It is structurally traceable from the supplied PR70 `L,C,F,R` formulas at `x=y=1/2`, and the surrounding formulas retain the correct shared-corner terms, so this is not a correctness blocker. It is still the densest point in the paper text and would benefit from an explicit derivation paragraph.

## Exclusions

This review did not perform determinant/log/entropy/interval/Gram/finite arithmetic; did not certify the large rational Sylvester minors; did not run `verify_shared_corner_cell.py`; and did not review any sibling, FIRST/SECOND/C3, public comments, later live sources, or private directories.
