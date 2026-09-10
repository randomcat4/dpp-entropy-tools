# PR70 FIRST source-only mathematical review

Overall verdict: `ACCEPTED_SCOPED` for the analytic identities, reductions, pivots, symmetries, quadratic auxiliary theorem, tail theorem, and thinning theorem as source-level mathematics. `INCOMPLETE` for any independently certified finite disproof from the fixed rational paired-resolvent object, because this FIRST review was expressly source-only and did not reconstruct the rational/log arithmetic. The general determinant sign, universal one-sided statement, full missing-edge Shannon Hessian sign, and general real three-point theorem remain open in this packet.

Novelty: `NOT_ASSESSED`. Formal verification: `NOT_PERFORMED`. Finite computation: `NOT_PERFORMED`.

All source pins below use the public alias `source-snapshots/pr70/...`. The immutable public URL base is:

`https://github.com/randomcat4/dpp-entropy-tools/blob/f7be60759fd4d65184803b6585965dc7e5ccd624/research/I05-22-R4-paired-perspective/`

## Per-claim review

### 1. Complete events, domain, and six physical directions

Status: `CORRECT`; verdict: `ACCEPTED_SCOPED`.

Pins: `proof.md:7-58` and `README.md:17`.

The eight exact atoms are presented by inclusion-exclusion from inclusion minors, and the strict center domain is reduced to `0<x,y<1` with positive `A,B,q,qbar`. The formulas for `q` and `qbar` are the Schur complements of the arrow kernel and its complement. The six-coordinate map from a real symmetric direction `D` to `(d,e,m,f,g,h)` is invertible when `b c != 0`, so no physical direction is dropped. The marginal second derivative term `Pij''` is explicitly retained, which is load-bearing because it prevents a false fixed-measure perspective argument.

No PR60 premise is used here.

### 2. Perspective formula, one-sided cofactor formula, and scaling

Status: `CORRECT`; verdict: `ACCEPTED_SCOPED`.

Pins: `proof.md:62-114`, `verify_bridges.py:40-69`, and `verification.md:7`.

The scalar second-derivative formula includes the `r''` and `P''` acceleration terms. For `phi(t)=t log t`, the `+1` term cancels after summing selected atoms because the total selected mass is affine, and the `P'' t` term cancels by the double difference of the additive `t_ij` table. The cofactor formula is then an algebraic regrouping of the four selected atom accelerations against four log weights.

The congruence scaling is also scoped correctly: scaling the third coordinate scales selected third-bit masses and the transformed direction together, while leaving the two-leaf marginal table fixed. This proves sign equivalence for the auxiliary one-sided domain and legal connected arrows, but not for full entropy.

### 3. Positive `L_s`, `R_s`, `Y_s`, and paired `Y`

Status: `CORRECT`; verdict: `ACCEPTED_SCOPED`.

Pins: `proof.md:117-199`, `post_checkpoint.md:147-149`, and `verification.md:27-29`.

The side block formulas retain the original table and define the side quantities before elimination. Lemma 1 is acceptable: the double integral for `J_s` and the strict trapezoid inequality for the positive strictly convex functions `phi_s''` give the determinant bound for `L_s`. Lemma 2 is acceptable: `N_1` is positive by adding a positive diagonal part to a positive multiple of `K`, and the corrected `N_0` decomposition uses absent-side face 1 plus a positive multiple of `I-K`. The lower three-by-three block of `R_s` is a congruence of `N_s`, and `F_s` is positive definite because four positive weighted evaluations on the two-by-two grid determine the bilinear score.

The face-index correction is explicit and does not hide the earlier typo.

### 4. Parallel-sum compensation and marginal Fisher

Status: `CORRECT`; verdict: `ACCEPTED_SCOPED`.

Pins: `proof.md:200-229`, `verification.md:25`, and `README.md:17`.

The identity for `S_cond` is a direct completion-of-squares/parallel-sum identity for positive `L_0,L_1`; it does not require commutativity. The full Shannon Schur formula correctly adds the leaf marginal Fisher through `M=diag(1/v,1/w)`, and the difference `L^{-1}-(L+M)^{-1}` is positive semidefinite. This is the correct compensation retained by the paired full-entropy target.

This section proves a reduction and compensation identity, not the sign of the final two-by-two target.

### 5. Two-by-two target, determinant equivalence, and back-map

Status: `CORRECT`; verdict: `ACCEPTED_SCOPED`.

Pins: `proof.md:231-259`, `post_checkpoint.md:136-145`, and `README.md:54-56`.

Since the four conditional-score block `Y_s` or `Y` is positive definite, Schur complement reduction to a two-by-two matrix is valid. The inertia argument is also sound: the cofactor quadratic form for positive definite `N` has a five-dimensional positive subspace and one negative direction; adding the relevant Fisher terms preserves at least five positive eigenvalues. After removing the four positive `Y` directions, each two-by-two target has at least one positive eigenvalue. Therefore nonnegativity of the full six-direction form is equivalent to nonnegative determinant of the corresponding two-by-two matrix.

The negative-vector back-map `U=-Y^{-1}C^T delta` is the Schur minimizer and gives a physical direction through the already invertible coordinate map. This is an exact pointwise equivalence, not a proof that the determinant is nonnegative.

### 6. Fisher inverse formulas

Status: `CORRECT`; verdict: `ACCEPTED_SCOPED`.

Pins: `proof.md:261-291` and `verify_bridges.py:95-107`.

The inverse identity follows from the invertible four-evaluation matrix and the independent Bernoulli product table. The formulas for `F_1^{-1}`, `F_0^{-1}`, and `(F_0+F_1)^{-1}` are consistent with the table weights. The text correctly states that `(F_0^{-1}+F_1^{-1})^{-1}=Dv` does not imply `F_0+F_1=Dv`.

### 7. Complement and leaf-exchange symmetry

Status: `CORRECT`; verdict: `ACCEPTED_SCOPED`.

Pins: `post_checkpoint.md:111-134`.

Complementation maps `x,y,q` to `1-x,1-y,qbar` with the transformed direction and conditional coordinates described in the packet. Leaf exchange conjugates the two-by-two core by the swap matrix. These transformations preserve inertia and determinant. The proposed fundamental domain with `A>=B` and `q<=qbar` is therefore valid, and equality surfaces are correctly included rather than discarded.

The single-side target is not complement invariant; the packet correctly maps it to the other side.

### 8. Strict six-direction quadratic-perspective convexity

Status: `CORRECT`; verdict: `ACCEPTED_SCOPED`.

Pins: `proof.md:294-319`, `verify_bridges.py:84-94`, and `tail_bound.md:29-36`.

The theorem is explicitly auxiliary and not a Shannon theorem. Applying the same perspective derivative to `phi(t)=t^2` gives a full six-direction expression, and the displayed sum of squares has positive coefficients on the stated auxiliary domain. Vanishing of all squares forces all six direction coordinates to vanish through the inverse map, so strict positivity follows for nonzero physical `D`.

The large-`q` limit statement is scoped to fixed shape and fixed physical direction.

### 9. Fixed-shape large-`q` tail

Status: `CORRECT`; verdict: `ACCEPTED_SCOPED`.

Pins: `tail_bound.md:3-93`.

The tail theorem is fixed-shape and auxiliary-domain only. The proof uses the strict positive quadratic limit from the previous unit, a Frobenius-norm lower bound for the limit form, a direct bound on the side Fisher error, and an operator/nuclear-norm bound for the cofactor error. The threshold depends on the fixed shape and may degenerate near boundary regimes. The packet explicitly notes that the resulting legal-domain coverage can be empty for strong legal shapes, so this does not close the intermediate-`q` one-sided problem or the paired full-entropy target.

### 10. Thinning equivalence and conditional-versus-full distinction

Status: `CORRECT`; verdict: `ACCEPTED_SCOPED`.

Pins: `thinning_bridge.md:7-44`, `thinning_bridge.md:48-75`, `thinning_bridge.md:78-106`, and `README.md:23`.

The global equivalence between the universal one-sided sign and universal conditional-entropy concavity is correct. One direction is immediate by complementing all bits; the converse thins the third coordinate, uses the exact scaling of the selected side, and expands the complemented side as a higher-order perturbation. The explicit remainder bound keeps all four leaf configurations and the `P_i''` terms.

The hypothetical negative-side analysis is also correctly scoped. If a negative `G1''` point existed, sufficiently thinning it would refute conditional concavity while the corresponding full-entropy curvature in that same direction remains positive because the leaf marginal Fisher survives. This does not assert a negative-side example and does not prove full Hessian positivity in every direction.

### 11. Fixed rational paired-resolvent obstruction certificate

Status: `CRITICAL_GAPS` for independent C1 acceptance; verdict: `INCOMPLETE` pending C2 finite reconstruction.

Pins: `post_checkpoint.md:14-54`, `post_checkpoint.md:58-66`, `post_checkpoint.md:68-98`, `post_checkpoint.md:100-109`, `verification.md:9`, `verification.md:21`, and `README.md:33-46`.

The analytic relationship is correctly separated: a negative second derivative of the complement-paired conditional resolvent would refute universal convexity of that auxiliary method, and the packet explicitly says it does not refute `G1''>=0`, conditional concavity, or full entropy concavity. The public text gives a literal rational `K,D`, event jets, quotient differentiation rule, Sylvester-minor legality witnesses, side/full entropy sign intervals, a legal Jensen interval, and a logarithm enclosure method.

However, this source-only review did not reconstruct the exact rational fractions, signs, Sylvester minors, or logarithm intervals. Therefore the claimed exact obstruction remains author-certified rather than independently established here. Minimal repair is not a prose change: a C2 reviewer must independently reconstruct the finite certificate from the public literals and produce raw outward-bounded artifacts.

### 12. Literal scope claims and source-index correction

Status: `CORRECT`; verdict: `ACCEPTED_SCOPED`.

Pins: `README.md:5-13`, `README.md:48-56`, `verification.md:3-13`, `verification.md:15-25`, `verification.md:27-45`, and `SOURCE_BINDING.json:2-68`.

The packet repeatedly states that the main determinant sign, one-sided universal sign, and general Shannon/real-three-point claims remain incomplete. It does not promote PR60, old `r=0`, or a C2 machine pass to an accepted premise. It also records that `inputs.json` is a future/requested C2 input set, not an executed filament run. The source-index correction is explicitly retained and not represented as independent review.

## External theorem assumptions

No external theorem is load-bearing for the accepted mathematical steps beyond standard calculus and finite-dimensional linear algebra. The scalar perspective citation supplies background, but the needed second derivative is derived in `proof.md:64-76`. The Phi-entropy citations are route context and are explicitly not used to bridge the nonlinear DPP event map. The Anderson-Duffin parallel-sum source supplies terminology/background; the nonsingular positive-matrix hypothesis is met internally by Lemma 1, and the actual DPP compensation identity is derived in `proof.md:202-217`.

## C2 finite-evidence obligations

To upgrade the paired-resolvent obstruction from author certificate to independent finite evidence, C2 should reconstruct from public literals only, without importing author verifier code or author outputs.

Required inputs:

- Frozen commit `f7be60759fd4d65184803b6585965dc7e5ccd624`.
- Event order from `inputs.json:4` and atom formulas from `proof.md:7-21`.
- Rational `K,D` from `post_checkpoint.md:14-19`.
- Quotient derivative rule from `post_checkpoint.md:37-54`.
- `tau=1/100000`, endpoint-minor data target, and Jensen target from `post_checkpoint.md:79-96`.
- Log enclosure method from `post_checkpoint.md:100-107`.

Required raw artifacts:

- Literal parse record showing every rational input matches the public text.
- Complete eight-atom jets `(p,p',p'')` and marginal jets, in the public mask order.
- Exact rational `Phi0''`, `Phi1''`, and `Phi_pair''`, with a sign proof for the paired value.
- Exact Sylvester minors for `K-tau D`, `K`, `K+tau D`, and their complements, with positivity separated by endpoint.
- Exact or outward-rational intervals for `G0''`, `G1''`, `-Hconditional''`, and `-Hfull''`.
- Complete log argument inventory, normalization data, truncation parameter, rational lower/upper log bounds, and final outward decimal/rational Jensen enclosure.
- Machine/environment record, source hash record, and command transcript sufficient to reproduce the artifacts.

Acceptance criteria:

- All literal inputs match the frozen public source.
- Every denominator used in the exact certificate is positive.
- Every outward interval excludes zero with the claimed sign.
- Endpoint legality plus convexity certifies the whole affine segment used for Jensen.
- The Jensen interval is negative and is reported as a legal local full-entropy curvature/Jensen witness, not as a positive entropy-concavity counterexample.
- No private script, private upload, author output, old PR60 certificate, or previous review verdict is used as evidence.

For the 273 requested issue inputs, C2 should treat `inputs.json:2-9` as requested future data only. If those are run, the acceptance standard should require independently reconstructed `E_H` formulas from `proof.md:233-259` and `post_checkpoint.md:138-145`, determinant intervals, exact bad-vector back-maps when negative, and legal full-entropy Jensen certificates before any counterexample language is used.

## Final classification

- Analytic PR70 source packet: `ACCEPTED_SCOPED`.
- Fixed rational paired-resolvent obstruction: `INCOMPLETE` for independent finite acceptance in this C1 review; no source prose repair required beyond C2 evidence.
- General one-sided sign: `INCOMPLETE`.
- General paired full-entropy determinant sign: `INCOMPLETE`.
- General real three-point theorem: `INCOMPLETE`.
- Positive full-entropy Jensen counterexample: `NOT_SUPPLIED`.
- Novelty: `NOT_ASSESSED`.
- Formal verification: `NOT_PERFORMED`.
