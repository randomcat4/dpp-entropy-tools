# PR70 — accepted scoped paired-perspective reduction and fixed certificate

Status: **ACCEPTED_SCOPED**. The analytic FIRST and isolated SECOND, and the independent finite FIRST and new isolated finite SECOND, all passed within the scope below. C3 read the full reports and bound their source files without rerunning mathematical computation.

Frozen author source: `f7be60759fd4d65184803b6585965dc7e5ccd624`, eight files under `research/I05-22-R4-paired-perspective/`. Independent finite evidence: PR85 preparation `29d4d77d7dba65de933d196a89b4db2616234991`, raw output `611d5f70e8bb70237755ca4fdbe8ab14c8b715c1`.

The analytic scope is the strict connected real three-site missing-edge arrow, with all eight complete occupation events and all six physical affine kernel directions. The exact reductions retain event and marginal accelerations, complete Fisher information, the independent two-leaf marginal Fisher term, and every mixed direction.

The following analytic units passed both reviews:

- The complete-law paired perspective construction, cofactor identities, simultaneous kernel/direction scaling, and strict parameter domain. The absent-face convention has `N_0=1`.
- The positive side pivots, parallel-sum compensation, full conditional and full Shannon Schur reductions, and the two-dimensional `E_H` core. The determinant equivalence is a reduction under the proved pivot/inertia conditions, not a proof of a determinant sign; the negative-vector back-map is retained.
- The four-point Fisher inverse identity, complement and leaf-swap symmetries, and the fundamental-domain reduction including its equality surfaces.
- The strict six-direction quadratic-perspective SOS statement and the fixed-shape large-q tail implication. A particular fixed shape need not have any legal point inside the sufficient tail region.
- The global one-sided-sign/conditional-concavity equivalence through thinning. It does not supply the missing global sign. The full entropy additionally retains the leaf marginal Fisher contribution.

The independent finite unit uses only the exact author `K,D` and `tau=1/100000`. Its code reconstructs inclusion/Mobius and signed complete determinants separately, keeps physical first and second derivatives, checks all eight events and marginals, and verifies the six endpoint/center kernel/complement Sylvester systems. P2 quotient jets are compared rowwise with the separate P3 expression. P5 is differentiated in two forms with all acceleration terms. P6 uses the complete Shannon entropy of the three legal points.

Accepted fixed output enclosures:

| Quantity | Outward enclosure |
| --- | --- |
| Paired auxiliary resolvent second derivative | `[-4.8046265619871114230253298325745148413179, -4.8046265619871114230253298325745148413178]` |
| `G_0''` | `[6.3836477267924650532084343120505471181471, 6.3836477267924650532084343120505471181472]` |
| `G_1''` | `[9.2177300388618574492302078622332257604485, 9.2177300388618574492302078622332257604486]` |
| `-H_conditional''` | `[15.6013777656543225024386421742837728785956, 15.6013777656543225024386421742837728785957]` |
| `-H_full''` | `[41.8563777656543225024386421742837728785956, 41.8563777656543225024386421742837728785957]` |
| `(H(K-tau D)+H(K+tau D))/2-H(K)` | `[-0.0000000020928189192765834280721741836172, -0.0000000020928189192765834280721741836171]` |

The finite certificate has separate exact-fraction, sign, interval-width and literal-containment gates. Rational atanh bounds use the fixed N=80, explicit normalization and remainder, and endpoint reversal for negative coefficients. No rounded author display is promoted to a precise bound.

The single C2 run began `2026-09-10T02:10:08Z`, kept deadline `02:20:08Z`, and finished `02:10:10Z`; PID175598 was absent at `02:10:38Z`. All178 ordered gates passed without a previous arithmetic attempt or repair. C3 checked77 immutable Git blobs,59 JSON artifacts, unchanged executable/inputs, and execution records without rerunning mathematics.

The mathematical meaning of the finite negative auxiliary derivative is limited to failure of the proposed complement-paired resolvent convexity method. The actual entropy curvature and Jensen witness here have the favorable concavity sign. This is not an entropy counterexample.

Still open: the global one-sided sign, the full `det E_H>=0` claim, the general real three-point theorem, and any issue73 filament/global certificate. No issue73 scan was run. Novelty is not assessed and formal verification was not performed.

Provenance note: the original analytic SECOND correctly recorded all eight source hashes but transcribed the metadata digest with two extra characters. The original report is preserved and the separate binding corrigendum records the actual64-character digest. The finite SECOND is a new context, receives no FIRST or prior SECOND opinion, and reads only frozen author source plus independently owned C2 raw inputs, implementation, outputs and execution records.

## Reviews, publication binding and merge record

- [Frozen author source](../../research/I05-22-R4-paired-perspective/proof.md) and [fixed P2/P5/P6 author statement](../../research/I05-22-R4-paired-perspective/post_checkpoint.md).
- Independent C1 [analytic FIRST](https://github.com/randomcat4/dpp-entropy-tools/blob/39d0a6c3dd98e184f3ceb2b47e4d049bf83c6426/research/C1-verification-round7-20260910/units/pr70/review_report.md), [finite FIRST](https://github.com/randomcat4/dpp-entropy-tools/blob/39d0a6c3dd98e184f3ceb2b47e4d049bf83c6426/research/C1-verification-round7-20260910/units/pr70/machine_pr85_review.md), and [finite code review](https://github.com/randomcat4/dpp-entropy-tools/blob/39d0a6c3dd98e184f3ceb2b47e4d049bf83c6426/research/C1-verification-round7-20260910/units/pr70/machine_pr85_code.md). The complete 33-file immutable archive snapshot was Git-verified; archive merging is separately gated by the remaining PR77 reports.
- Isolated [analytic SECOND](pr70_second/review_report.md), [scope](pr70_second/frozen_scope.md), [code review](pr70_second/code_review.md), [source binding](pr70_second/source_binding.json), and preserved [metadata digest corrigendum](pr70_second/binding_corrigendum.md).
- New isolated [finite SECOND](pr70_finite_second/review_report.md), [scope](pr70_finite_second/frozen_scope.md), [code review](pr70_finite_second/code_review.md), [source binding](pr70_finite_second/source_binding.json), and [sign interpretation note](pr70_finite_second/sign_interpretation_note.md). The last note clarifies one ambiguous report sentence: fixed `-H_full''>0` does certify fixed `H_full''<0`; no global conclusion follows. Original report bytes are preserved and mapped to the public copies.
- [Independent C2 implementation](../../research/C2/pr70_obstruction52/implementation/independent_pr70_checker.py), [run ledger](../../research/C2/pr70_obstruction52/execution/RUN_LEDGER.json), and [raw output manifest](../../research/C2/pr70_obstruction52/outputs/run01/output_hashes.json). C3 also verified all 82 delivered finite-review source Git/SHA hashes and both binding digests. The isolated packet omits top interpretation files and private invocation content; the computation-bearing files are complete and match. Full reproduction of withheld packaging metadata is not claimed.

PR85 merged at `877e284640973dadbd3f3bd23c3f78f8e09f5b85` and author PR70 at `0e8776c3f719ece9f2f4d426d02c6215f112ce94`, with exact reviewed heads as second parents. The main-branch source contains historical exploratory material; acceptance is only the explicit scope in this document.
