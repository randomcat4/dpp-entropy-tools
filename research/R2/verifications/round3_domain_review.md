# Round 3 independent domain review and commit binding

STATUS: CORRECT

## Part I: mathematical and domain review

Verifier: boundary_certificate, independent domain/computation risk pass.

Scope and inputs read only:

- `research/R2/frozen_theorem_v2.md`
- `research/R2/proofs/b_zero_c2_decomposition_v2.md`
- `research/R2/hazards.md`
- `research/R2/proofs/tomography_components_v3.md`
- `research/R2/proofs/component_pair_C2_v3.md`


## Verdict

I find no critical gap in the anonymous component-pair proof relative to the frozen theorem and the public `B=0` C2 decomposition. The proof correctly reduces full-tomography directions to component off-blocks, kills simultaneous/cross and zero-Pluecker contributions, and expresses the remaining high/low one-sided C2 as a sum of nonpositive pairwise convexity defects.

## Main checks

1. Signed cofactor/tomography structure.

   The signed cofactor identity
   `tr(X adj G(z)) = sum_R z_R alpha_R^T X alpha_R`
   uses genuine signed replacement cofactors. The analytic inverse/path argument then forces `X_cc=0` on each coordinate-graph component, and the converse is immediate from block support. This matches the required full constraint `alpha_R^T X alpha_R=0` for all `(r-1)` row subsets. The low-side statement is consistent with complementary minors: the coordinate graph for `I-P` has the same nontrivial off-diagonal edges up to sign, so the same component split applies to `Y`.

2. C1/L2 gate.

   The proof is downstream of `b_zero_c2_decomposition_v2.md` and assumes the full tomography gate. Under that gate, `tr X=tr Y=0`, `L1=0`, `C1=0`, and the zero-r-event logarithmic term `L2` is zero. I checked that the component-pair proof does not use the earlier invalid shortcut “`L1=0` only”; all finite C2 comparisons are made after the full gate.

3. Active and simultaneous cross terms.

   The active law factorizes over components. For a pair of components, the mixed second variation contains a componentwise average of the replacement tensor, and the proof’s identity `sum_active psi_c T_(c,S_c)=0` kills the active `q(X,Y)` term, including the log-weighted part. This is consistent with the public decomposition’s cross bucket.

4. Zero Pluecker / zero-rate terms.

   For `det U_S=0`, the proof splits correctly:

   - if `rank U_S <= r-2`, the relevant adjugate/replacement tensor vanishes;
   - if `rank U_S = r-1`, the tensor is rank one, `T_S=a b^T`, and tomography gives `a^T X a=0`; using a row outside `S` identifies the low-side cofactor vector proportional to `b`, so `b^T Y b=0`.

   Hence `q_S(X,C)`, `q_S(A,Y)`, and `q_S(X,Y)` vanish on zero Pluecker events, and the endpoint-average correction equals the midpoint correction. I see no missing inward rank-r survival correction in this argument.

5. Pairwise C2 formula.

   For a component pair `(a,b)` and local cofactors `alpha,beta`, with
   `g=alpha^T A_aa alpha`, `h=beta^T A_bb beta`, `u=alpha^T A_ab beta`, `x=alpha^T X_ab beta`, `D=gh`,
   the claimed summand
   `gamma_D(u,x)=Phi_D(u)-[Phi_D(u+x)+Phi_D(u-x)]/2`,
   `Phi_D(v)=G_D(v^2)`, `G_D(z)=z+(D-z)log(1-z/D)`,
   has the correct signs and constants.

   The active, one-hole, and two-hole pieces combine to remove the component-local entropy offsets and leave the scalar defect above. I checked the common pitfall here: the two-hole determinant is `gh-(u±x)^2`, with no stray factor of two in the off-block square.

6. Low-side complement signs.

   The low-side proof uses the same scalar defect with low cofactors. Complement signs cancel in the squared determinant/rate expressions, and PSD uses the compressed two-dimensional matrix in the same way. I find no sign reversal in the low-side contribution.

7. Singular endpoints and zero rates.

   If `D=gh=0`, PSD of the endpoint compressions forces `u=x=0`; the proof’s convention that the corresponding pair contribution is zero is therefore safe. The same reasoning handles low-side singular blocks. Terms with zero first rate are not assigned illegal logarithms; they are either in the zero-Pluecker audit or vanish by PSD/tomography.

8. Strictness.

   Since full tomography makes nonzero `X` or `Y` purely off-component, Parseval/local cofactor completeness gives at least one nonzero scalar `x` or `y`. PSD then gives `D>0`, and
   `Phi_D''(v) = -2 log(1-v^2/D) + 4v^2/(D-v^2) >= 0`
   is strict away from the zero direction. Thus every nonzero admissible direction gives at least one strictly negative pair defect; this is compatible with, and stronger than, the frozen nonpositivity claim.

## Targeted computational cross-check

I used my corrected signed-formula/exact-event machinery only as an auxiliary check on the existing non-paired `n=8,r=4` row-rotated frame data. The tested frame was the `H4xR35_rowrot01_r4_0123` case with coordinate components
`[[0,1,4,5],[2,6],[3,7]]`, in one-sided particle mode.

Exact-event interpolation with Möbius probabilities gave:

- `L1 = 0`
- `C1 = 0E-118`
- `L2 = 0`
- exact-event `C2 = -7.35876811689259322431813486473402068688510546023462949278766965706077444110238763678622948811021262639492e-11`

The public finite C2 formula recomputation gave:

- formula `C2 = -7.3587681168925932243181348647340206868851054602346294927876697736570607744411023876367862294881102126263949613738e-11`
- difference from exact-event interpolation: about `4.2e-118`

The tomography residuals for all signed-cofactor measurements were exactly zero for the active direction in the tested side.

A separate local pairwise-gamma evaluation on the same non-paired frame gave component-pair sums:

- pair `(0,1)`: about `-5.5593165082e-11`
- pair `(0,2)`: about `-1.7995890059e-11`
- pair `(1,2)`: `0`

Total pairwise gamma was about `-7.3589e-11`, agreeing with the exact/formula C2 to ordinary floating precision. Every scalar pair defect was nonpositive.

## Conclusion

No critical issue was found in the pairwise formula, C1/L2 gate, low-side complement signs, zero-Pluecker handling, zero-rate/singular endpoint treatment, or strictness argument. The proof is acceptable as a correct verification target for the frozen v2 theorem. 

## Part II: commit-bound gate

Commit-bound gate for the component-pair verification.

Candidate commit:

- `3ae3323ae958feb733b78f5b425c6d9b540524e9`

Scope:

- Read-only commit-object check inside public checkout `dpp-entropy-tools`.
- No public checkout edits.
- No author-file edits.

## Public checkout state

- `git rev-parse --verify 3ae3323ae958feb733b78f5b425c6d9b540524e9^{commit}` exited `0` and resolved to `3ae3323ae958feb733b78f5b425c6d9b540524e9`.
- `git status --porcelain=v1 --untracked-files=all` in `dpp-entropy-tools` produced no output before writing this report, so the public checkout was clean.

## Commit SHA256 binding

Hashes were computed from the exact blob bytes in the fixed commit using `git cat-file blob <commit>:<path>` and SHA256 over stdout bytes.

| Item | Commit path used | Expected SHA256 | Actual SHA256 | Match | Blob read exit |
| --- | --- | --- | --- | --- | --- |
| frozen v2 | `research/R2/frozen_theorem_v2.md` | `789368b0df3197d8f97f0b200f3a70e6f9a7354f8bc4c97c3d11e45021a77287` | `789368b0df3197d8f97f0b200f3a70e6f9a7354f8bc4c97c3d11e45021a77287` | yes | `0` |
| b_zero decomposition | `research/R2/proofs/b_zero_c2_decomposition_v2.md` | `c2e9f157158cc6d376101ee12ba794bb1afb21f5b61606f1b48266c93f6e2dbb` | `c2e9f157158cc6d376101ee12ba794bb1afb21f5b61606f1b48266c93f6e2dbb` | yes | `0` |
| tomography components | `research/R2/proofs/tomography_components_v3.md` | `5641f161415331ee6a9185449f342d64c2f93755f52ea38a821cef9a8285e2eb` | `5641f161415331ee6a9185449f342d64c2f93755f52ea38a821cef9a8285e2eb` | yes | `0` |
| component C2 proof | `research/R2/proofs/component_pair_C2_v3.md` | `72a8596e58e957c19833eae7284419671ebf9709f6bfdd948165f29ccdbb86ee` | `72a8596e58e957c19833eae7284419671ebf9709f6bfdd948165f29ccdbb86ee` | yes | `0` |
| hazards | `research/R2/hazards.md` | `792afa93e166d30bf768637585e271dad4a413da546742f8db577b70059777e1` | `792afa93e166d30bf768637585e271dad4a413da546742f8db577b70059777e1` | yes | `0` |

Path note: the two anonymous files previously reviewed as `research/R2/proofs/tomography_components_v3.md` and `research/R2/proofs/component_pair_C2_v3.md` are not present under those paths in the public commit. The fixed public commit contains the corresponding integrated files at `research/R2/proofs/tomography_components_v3.md` and `research/R2/proofs/component_pair_C2_v3.md`; their blob SHA256 values match the supplied hashes exactly.

## Computation coverage rechecked

I reran one bounded, non-scanning targeted check on the existing non-paired `n=8,r=4` row-rotated frame case. The check imported only the corrected signed-formula/exact-event functions and did not run the search writer.

Checked case:

- source result file: `r3b_c2_formula_results_seed2026090813_structured.json`
- frame: `H4xR35_rowrot01_r4_0123`
- mode: `one_sided_particle`
- coordinate components: `[[0,1,4,5],[2,6],[3,7]]`

Exact-event/formula gate:

- `L1 = 0`
- `C1 = 0E-118`
- `L2 = 0`
- exact-event `C2 = -7.35876811689259322431813486473402068688510546023462949278766977365706077444110238763678622948811021262639492E-11`
- formula `C2 = -7.3587681168925932243181348647340206868851054602346294927876697736570607744411023876367862294881102126263949613738E-11`
- exact minus formula `= 4.13738E-118`
- signed-cofactor tomography residuals: `X_nonzero=0`, `Y_nonzero=0`, `X_max_abs=0`, `Y_max_abs=0`

Pairwise-gamma auxiliary check:

- pair `(0,1)` sum: approximately `-5.559316514301265e-11`
- pair `(0,2)` sum: approximately `-1.7995890104310197e-11`
- pair `(1,2)` sum: `0`
- total pairwise gamma: approximately `-7.358905524732285e-11`
- maximum positive scalar pair defect: `0.0`

Computation exit status:

- blob-hash command: exit `0` after using the corrected public paths;
- targeted n8 exact/formula/pairwise check: `N8_EXACT_FORMULA_PAIRWISE_OK`, exit `0`.

## Conclusion

The fixed commit binds byte-for-byte to the reviewed frozen theorem, decomposition, component tomography proof, component-pair C2 proof, and hazards file through the supplied SHA256 values. The n8 exact-event/formula/pairwise check conclusion still holds. I therefore keep the prior verification verdict:

`STATUS: CORRECT`

