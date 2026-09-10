# PR86 source/evidence FIRST review

Scoped verdict: **conditional source-level acceptance with evidence/documentation changes requested before PR-level acceptance**. I found no blocking analytic gap in the written complete-event identities, relative sign theorem, qualitative fixed-chord dilute theorem, or thinning/coordinate-block orthogonal theorem. The finite certificate theorems are different: the small angular box, equal-angle diagonal, two full edges, full fixed canonical square, dense dilute example constants, full-intensity example values, Fisher/acceleration intervals, and strict-kernel lift margins all remain **SOURCE_ONLY / PENDING_C2** because I did not execute or independently reconstruct their finite arithmetic.

This review is bound to head `bd12e6094e098499fae7e01729a4b29f021a14e2` over base `65e59a46b49cd2dbb5c779a4cfae8cef26441984`, using `source-snapshots/pr86/` and the immutable compare <https://github.com/randomcat4/dpp-entropy-tools/compare/65e59a46b49cd2dbb5c779a4cfae8cef26441984...bd12e6094e098499fae7e01729a4b29f021a14e2>. No code, tests, author checkers, finite arithmetic, interval arithmetic, entropy computation, or formal tools were run.

## Findings requiring repair or explicit gate

### P1. The full-square certificate promised by the source is not present in the frozen packet

`full_canonical_square.md` says the checker stores the compact certificate with row minima and the minimizing column, then states that the stored result is `full_square_certificate.json`; see `source-snapshots/pr86/research/N4/I05_30_20260910/full_canonical_square.md` lines 133-138 and 157-165, immutable source <https://github.com/randomcat4/dpp-entropy-tools/blob/bd12e6094e098499fae7e01729a4b29f021a14e2/research/N4/I05_30_20260910/full_canonical_square.md#L133-L165>. The generator writes that exact file at `certify_full_square.py` lines 189-193, immutable source <https://github.com/randomcat4/dpp-entropy-tools/blob/bd12e6094e098499fae7e01729a4b29f021a14e2/research/N4/I05_30_20260910/certify_full_square.py#L189-L193>.

However, `SOURCE_BINDING.json` binds only the 18 listed files and does not include `research/N4/I05_30_20260910/full_square_certificate.json` or a corresponding stdout file. Under a source/evidence-only review, the full-square finite cover therefore cannot be audited as an archived certificate; it is only a script plus prose claim. Minimum repair: publish a separately frozen successor containing the generated `full_square_certificate.json` with binding metadata, or revise the text in such a successor so it does not claim a stored certificate. In either case the 4096-box proof remains pending independent C2 before acceptance as an externally verified finite theorem.

### P2. The README is stale relative to the final 18-file theorem packet

The README's final verdict table covers the physical rank-two event formula, relative off-diagonal sign, small angular box, bridge failure, dilute fixed-chord theorem, and unresolved global objects at lines 7-21, immutable source <https://github.com/randomcat4/dpp-entropy-tools/blob/bd12e6094e098499fae7e01729a4b29f021a14e2/research/N4/I05_30_20260910/README.md#L7-L21>. Its proof order and reproduction notes at lines 23-42 mention `rank2_atoms_and_angular_box.md`, `dilute_chord_theorem.md`, `certify.py`, and `dilute.py`, immutable source <https://github.com/randomcat4/dpp-entropy-tools/blob/bd12e6094e098499fae7e01729a4b29f021a14e2/research/N4/I05_30_20260910/README.md#L23-L42>.

The final frozen packet also contains later standalone claims in `fresh_recheck_and_edge_extension.md`, `equal_angle_diagonal.md`, `thinning_star_and_orthogonal_support.md`, and `full_canonical_square.md`; their own status lines are at <https://github.com/randomcat4/dpp-entropy-tools/blob/bd12e6094e098499fae7e01729a4b29f021a14e2/research/N4/I05_30_20260910/fresh_recheck_and_edge_extension.md#L1-L3>, <https://github.com/randomcat4/dpp-entropy-tools/blob/bd12e6094e098499fae7e01729a4b29f021a14e2/research/N4/I05_30_20260910/equal_angle_diagonal.md#L1-L3>, <https://github.com/randomcat4/dpp-entropy-tools/blob/bd12e6094e098499fae7e01729a4b29f021a14e2/research/N4/I05_30_20260910/thinning_star_and_orthogonal_support.md#L1-L3>, and <https://github.com/randomcat4/dpp-entropy-tools/blob/bd12e6094e098499fae7e01729a4b29f021a14e2/research/N4/I05_30_20260910/full_canonical_square.md#L1-L3>. A reader using the README as the theorem ledger will miss these later objects and their evidence gates. Minimum repair: update the README verdict/proof-order section to list every theorem file, every verifier/certificate dependency, and the independent-review status of each finite certificate.

### P2. Finite arithmetic claims remain pending even where the written proof strategy is coherent

The source correctly labels many files as author proof plus pending review; see README line 21, <https://github.com/randomcat4/dpp-entropy-tools/blob/bd12e6094e098499fae7e01729a4b29f021a14e2/research/N4/I05_30_20260910/README.md#L21>. This FIRST review did not run the scripts and did not reconstruct the rational boxes or log intervals. Therefore the following cannot be upgraded from author evidence to accepted finite proof in this report:

- the `G>19/1000` small angular box and its logged constants in `rank2_atoms_and_angular_box.md` lines 122-168;
- the two bridge-failure values, Fisher/acceleration intervals, and bit-flip lift margins in lines 170-203 of the same file;
- the equal-angle 256-box derivative certificate in `equal_angle_diagonal.md` lines 80-125;
- the two full-edge derivative/Bernstein certificates in `fresh_recheck_and_edge_extension.md` lines 89-154 and 156-221;
- the full-square 4096-box certificate in `full_canonical_square.md` lines 93-138 and strict lift in lines 140-155;
- the dense dilute example intervals, radii, and full-intensity values in `dilute_chord_theorem.md` lines 127-156.

Minimum repair for theorem acceptance is not another author PASS label. The independent gate must rebuild the relevant event laws, rational interval logs, box/edge/diagonal/full-square certificates, and embedded rational fixtures from the frozen mathematics and literal source data, treating author scripts and outputs only as comparison material unless a separate reproduction-only task is authorized.

## Mathematical source audit

### Complete-event law, physical midpoint, and mixed terms

The foundational setup uses complete configuration entropy, not inclusion-minor entropy, particle-count entropy, spectral entropy, or quantum entropy; this is explicit in `rank2_atoms_and_angular_box.md` lines 5 and 77-81, <https://github.com/randomcat4/dpp-entropy-tools/blob/bd12e6094e098499fae7e01729a4b29f021a14e2/research/N4/I05_30_20260910/rank2_atoms_and_angular_box.md#L5-L81>. The family is stated in actual coordinates with `K_-=EAE^T`, `K_+=VBV^T`, and true arithmetic midpoint `M=(K_-+K_+)/2`; the source explicitly says no observation-basis rotation is invoked at lines 9-28, <https://github.com/randomcat4/dpp-entropy-tools/blob/bd12e6094e098499fae7e01729a4b29f021a14e2/research/N4/I05_30_20260910/rank2_atoms_and_angular_box.md#L9-L28>.

The displayed midpoint minors retain the mixed pair interference term `-2*r*z*c1*c2`, the triple terms, and the fourth-order determinant at lines 30-52, and then convert inclusion minors to all 16 complete atoms by Möbius inversion at lines 54-64, <https://github.com/randomcat4/dpp-entropy-tools/blob/bd12e6094e098499fae7e01729a4b29f021a14e2/research/N4/I05_30_20260910/rank2_atoms_and_angular_box.md#L30-L64>. I found no source-level omission of mixed terms or rare events in this derivation. The matching script reconstructs the same 11 symbolic minors in `certify.py` lines 79-94 and checks signed-law versus Möbius complete laws in lines 56-67, <https://github.com/randomcat4/dpp-entropy-tools/blob/bd12e6094e098499fae7e01729a4b29f021a14e2/research/N4/I05_30_20260910/certify.py#L56-L94>, but those checks remain author evidence.

### Relative off-diagonal sign theorem

The sign theorem is source-level sound within its stated scope. The theorem fixes diagonal data, absolute off-diagonal entries, and angles, and asserts only that the aligned choice has no larger `G` than the opposite-sign choice; it explicitly does not prove the aligned-sign inequality itself at lines 83-109, <https://github.com/randomcat4/dpp-entropy-tools/blob/bd12e6094e098499fae7e01729a4b29f021a14e2/research/N4/I05_30_20260910/rank2_atoms_and_angular_box.md#L83-L109>. The proof isolates the transfer to `(p_empty,p1,p2,p12)`, uses the complete-event identity `p1*p2-p_empty*p12=det(I-M)^2 L12^2 >= 0`, and integrates the positive odds derivative. Strictness is tied to the positive transfer amount `|r*z| c1 c2`, so the equality cases are also correctly delimited.

### Angular box and bridge failure

The analytic reduction for the small angular box is coherent as a continuous-parameter argument: it bounds the bottom-coordinate deletion cost, compares a two-coordinate marginal to the base midpoint, and then applies a finite-alphabet continuity inequality; see lines 122-152 of `rank2_atoms_and_angular_box.md`, <https://github.com/randomcat4/dpp-entropy-tools/blob/bd12e6094e098499fae7e01729a4b29f021a14e2/research/N4/I05_30_20260910/rank2_atoms_and_angular_box.md#L122-L152>. The final strict lower bound depends on finitely many logarithm enclosures at lines 160-168, so the numerical margin is pending C2.

The mixture-bridge failure is correctly framed as a failure of the rank-one-style method, not an entropy-concavity counterexample. Lines 170-188 give two fixed witnesses with positive actual `G` but negative `H(p_mid)-H((p_-+p_+)/2)`, and state that the curvature values are finite checks, not whole-chord theorems; see <https://github.com/randomcat4/dpp-entropy-tools/blob/bd12e6094e098499fae7e01729a4b29f021a14e2/research/N4/I05_30_20260910/rank2_atoms_and_angular_box.md#L170-L188>. The strict bit-flip lift at lines 190-203 is also a finite-margin consequence and remains pending C2.

### Equal-angle, edge, and full fixed-square theorems

The later fixed-family results are stated with appropriate scope limits. The equal-angle file keeps all 16 atoms, removes the endpoint singularity, and reduces strictness to a 256-box negative derivative certificate; see `equal_angle_diagonal.md` lines 30-78 and 80-125, <https://github.com/randomcat4/dpp-entropy-tools/blob/bd12e6094e098499fae7e01729a4b29f021a14e2/research/N4/I05_30_20260910/equal_angle_diagonal.md#L30-L125>. The scope line correctly says it does not close off-diagonal interior pairs or arbitrary `A,B` at lines 127-139.

The edge file separately treats the full `t2=0` common-line edge and the full `t2=1` zero-intersection edge. Its formulas retain triple and quadruple events, handle one-sided endpoints, and distinguish the true midpoint from a nonlinear path; see `fresh_recheck_and_edge_extension.md` lines 89-154, 156-221, and 223-227, <https://github.com/randomcat4/dpp-entropy-tools/blob/bd12e6094e098499fae7e01729a4b29f021a14e2/research/N4/I05_30_20260910/fresh_recheck_and_edge_extension.md#L89-L227>. The derivative and Bernstein signs are finite certificate claims pending C2.

The full-square file cleanly fixes the canonical matrices `A,B`, the true arithmetic midpoint, and all 16 complete configurations at lines 5-37, <https://github.com/randomcat4/dpp-entropy-tools/blob/bd12e6094e098499fae7e01729a4b29f021a14e2/research/N4/I05_30_20260910/full_canonical_square.md#L5-L37>. Its regularization identity cancels both rare-event logarithms while retaining bottom-coordinate configurations at lines 39-70, <https://github.com/randomcat4/dpp-entropy-tools/blob/bd12e6094e098499fae7e01729a4b29f021a14e2/research/N4/I05_30_20260910/full_canonical_square.md#L39-L70>. The proof of `G>1/100` relies on the 4096-box lower cover and rational log enclosures at lines 93-138, so it is conditional on independent finite review. The line 167 limitation correctly prevents upgrading this fixed `A,B` theorem to arbitrary rank-two endpoints.

### Fixed-chord dilute theorem

The dilute theorem is the strongest unconditional analytic addition in the packet. Its quantifiers are finite-dimensional and fixed-pair: for distinct real symmetric positive contractions `X,Y`, there exists a pair-dependent `lambda_*(X,Y)>0` such that `G(lambda)>0` for all `0<lambda<=lambda_*`; see lines 5-13, <https://github.com/randomcat4/dpp-entropy-tools/blob/bd12e6094e098499fae7e01729a4b29f021a14e2/research/N4/I05_30_20260910/dilute_chord_theorem.md#L5-L13>. The proof removes the apparent `lambda^m log lambda` singularities using the exact complete-law expansion and expected-cardinality identity at lines 17-33, derives the first and second coefficients at lines 35-59, proves strictness by scalar concavity or strict convexity of `Psi` at lines 61-80, and gives a finite all-event Taylor remainder at lines 83-125.

I found no source-level gap in the qualitative fixed-chord implication. The dense examples in lines 127-156 are useful author evidence for explicit radii and full-intensity sample signs, but the numerical intervals and generated q-polynomials remain pending C2. The scope paragraph at lines 158-162 correctly says this theorem does not settle full-intensity moving rank-two pairs or the multiring question.

### Thinning-star and coordinate-block orthogonal support

The thinning theorem is purely analytic and does not require computation. The source proves `H(Y) >= theta H(X)` for arbitrary random subsets by conditioning on the retention pattern, applying the entropy chain rule, and then using `H(Y) >= H(Y|R)`; strictness follows because `Y` and `R` are not independent when some coordinate is occupied with positive probability. See `thinning_star_and_orthogonal_support.md` lines 5-71, <https://github.com/randomcat4/dpp-entropy-tools/blob/bd12e6094e098499fae7e01729a4b29f021a14e2/research/N4/I05_30_20260910/thinning_star_and_orthogonal_support.md#L5-L71>.

The DPP specialization through inclusion probabilities and finite Möbius inversion is correct at lines 73-102, <https://github.com/randomcat4/dpp-entropy-tools/blob/bd12e6094e098499fae7e01729a4b29f021a14e2/research/N4/I05_30_20260910/thinning_star_and_orthogonal_support.md#L73-L102>. The coordinate-block orthogonal support theorem at lines 104-141 is also scoped correctly: it applies to disjoint actual observation-coordinate blocks and explicitly does not permit rotating dense spectral ranges into that form.

## Final FIRST status

- **ACCEPTED_SCOPED at FIRST; isolated SECOND remains separate:** complete-event setup; endpoint marking identities; relative sign comparison; qualitative fixed-chord dilute theorem; thinning-star theorem; coordinate-block orthogonal support theorem.
- **Conditional on independent C2:** every finite rational/log/interval/box/Bernstein/fixture value and every theorem whose strict margin depends on those values.
- **Repair before PR-level acceptance:** add or de-claim the missing `full_square_certificate.json`, and update the README to reflect the final 18-file theorem/evidence packet.
- **Still unresolved by PR86:** arbitrary real moving rank-two endpoints at full intensity, global chord concavity, arbitrary `A,B` canonical pairs, dense spectral orthogonal ranges not supported on actual coordinate blocks, and the strong-correlated multiring route.
