# PR81 code-review style findings

No executable code was reviewed. This is a static mathematical source review of the four bound markdown inputs.

## Findings

### P1: Keep large rational and diagnostic claims as SOURCE_ONLY/PENDING

Locations:

- `input/coupled_gram_fixed_shape.md` lines 39-54
- `input/coupled_gram_fixed_shape.md` lines 184-220
- `input/coupled_gram_fixed_shape.md` lines 235-259
- `input/coupled_gram_fixed_shape.md` lines 338-379

The fixed-shape rational derivative values, diagnostic determinant sensitivities, relaxed Sylvester minors, relaxed determinant, numerical secant display, and two-axis relaxed stress test are not independently certified in this SECOND review. They may be useful author diagnostics, but without an independent C2/checker artifact they should remain `SOURCE_ONLY/PENDING`. The surrounding text mostly says this already; this report preserves that classification.

### P2: Treat PR70 as a formula source, not as independent evidence in this packet

Locations:

- `input/proof.md` lines 27-35
- `pr70_source/proof.md` lines 231-259

The `E_H` reduction and determinant target are inherited from PR70. This review was explicitly limited to the local source package and did not read FIRST/C3/public-comment material, so PR70 is used here only as a formula source. The distinction matters: the equivalence reduction identifies the determinant target, but it is not itself a sign proof for `det E_H>=0`.

### P2: Relaxed negative determinant is not a DPP counterexample

Locations:

- `input/coupled_gram_fixed_shape.md` lines 222-294

The relaxed tuple is useful as a non-sufficiency witness for the currently listed scalar/Gram constraints, but the text correctly proves it is not realizable by the same DPP rectangle. The determinant negativity in the relaxation must therefore not be reported as an entropy counterexample. The nonrealizability mechanism is the missing same-q edge placement and then the shared four-corner constraint.

## Non-findings

- The paired scalar compression keeps all complete entropy terms through the PR70 core and does not drop the marginal Fisher term.
- The rectangle FTC identities and complement imbalance bounds are coherent.
- The half-leaf Gram inequality and same-q secant inequalities are valid analytic constraints on actual half-leaf rectangles.
- The manuscripts consistently leave `det E_H>=0` and the general missing-edge entropy theorem incomplete.

Formal/C2 verification: NOT_PERFORMED.

Novelty review: NOT_ASSESSED.

