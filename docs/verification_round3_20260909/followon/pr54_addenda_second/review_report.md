# PR54 three-addenda second review

Reviewed PR/head: PR54 at `c3b9e968c0b4557546c7b10137ef4fff295338b4`.

Reviewed files:

- `research/I05-23-20260909/ADDENDUM_ARBITRARY_RANK.md`
- `research/I05-23-20260909/ADDENDUM_ENDPOINT_RARE_EVENT.md`
- `research/I05-23-20260909/ADDENDUM_RANK2_ENDPOINT_SPECTRUM.md`
- permitted endpoint comparison slice: `code/verify_local_and_matching.py:148-172` and `output/verify_local_and_matching.txt:12-14`

I did not read the prior first-review report/checker/output for this unit, did not use private packets, did not run broad mathematics, did not solve LPs, and did not touch the C2 issue52 arithmetic path.

Verdict: `ACCEPTED_SCOPED_FOR_DPP_CLAIMS`, with `NEEDS_WORDING_FIX` on two presentation clauses. The arbitrary-rank local curvature theorem, the DPP simple-endpoint rare-event theorem, and the rank-two endpoint spectral/discriminant test are independently sound in their stated DPP scopes. The addenda preserve the whole-chord, multiple-endpoint, and global-rate questions as open. The two wording fixes below concern an abstract analytic parenthetical and the rational-radius wording; they do not undermine the DPP polynomial proofs.

## Required wording corrections

1. `ADDENDUM_ENDPOINT_RARE_EVENT.md:12-13` says “probability polynomials (more generally, real-analytic probabilities) on a left neighborhood of `b`.” Real-analyticity only on the open left interval is not enough to justify the finite integer vanishing-order expansion used at `ADDENDUM_ENDPOINT_RARE_EVENT.md:33-39`; one needs analytic extension to the endpoint, or the expansion in (B.2) as an explicit hypothesis. The DPP application is sound because DPP atom probabilities are polynomials in `t` and therefore extend through the endpoint (`ADDENDUM_ENDPOINT_RARE_EVENT.md:116-118`). Suggested replacement:

   “Let `p_omega(t)` be probability polynomials, or more generally probabilities that extend real-analytically to a neighborhood of `b`, positive for `t<b`, with `sum p_omega(t)=1`.”

   An equally good fix is to keep one-sided language but assume directly that every vanishing atom has a finite expansion `p_omega(b-x)=a_omega x^{m_omega}(1+O(x))`.

2. `ADDENDUM_ARBITRARY_RANK.md:38-41` says the rational-input certificate can be made wholly rational except for `log 2`, with `log 2` replaceable by `1`. The displayed radius also uses spectral quantities `epsilon` and `beta` (`ADDENDUM_ARBITRARY_RANK.md:103-140`), which need rational lower/upper substitutes if the radius itself is to be rational. The theorem is correct with the displayed real/algebraic constants. Suggested clarification:

   “For rational input, choose certified rational lower bounds for the four spectral margins and a certified rational upper bound for `||B||_op` (for example via exact root isolation or conservative rational matrix-norm bounds), and replace `log 2` by `1`; with those replacements the radius can be chosen rational.”

## Per-claim review

| Claim | Source lines | Verdict | Review notes |
|---|---:|---|---|
| Arbitrary-rank likelihood polynomial degree | `ADDENDUM_ARBITRARY_RANK.md:43-73` | `ACCEPTED_SCOPED` | Schur complementation gives the complete-law likelihood ratio `det(I - s Y_T^{-1} B^T X_S^{-1} B)`. The perturbation rank is at most `rank(B)=r`, so the determinant has degree at most `r`. Normalization over the full law gives `E_mu w_k=0` for every coefficient. The first coefficient is the negative trace of the same finite-rank matrix. |
| Full-law score lower bound | `ADDENDUM_ARBITRARY_RANK.md:75-101` | `ACCEPTED_SCOPED` | For any nonzero entry `B_ij`, the two-coordinate inclusion probability along the radial path is exactly `A_ii C_jj - s B_ij^2`. Differentiating the complete-law likelihood at zero gives `E_mu[Z_ij w_1] = -B_ij^2`. Since `Z_ij` is Bernoulli with variance `A_ii C_jj(1-A_ii C_jj)` under the product law, Cauchy--Schwarz gives the displayed positive lower bound for `E_mu w_1^2`. No event is removed. |
| Explicit local radius and true `t` curvature | `ADDENDUM_ARBITRARY_RANK.md:103-215` | `ACCEPTED_SCOPED_WITH_RATIONAL_RADIUS_CLARIFICATION` | The bounds on `q_s`, `q_s'`, `q_s''`, and `q_s'''` are valid for `0<=s<=delta_0`; `|log q_s|<=log 2` follows from `1/2<=q_s<=3/2`. The formula for `I'''` includes the extra `q_s''' log q_s` term needed in arbitrary rank. With `J(s)=2I'(s)+4sI''(s)=-H''(sqrt s)`, the estimate `J'(s)>=3 underline_sigma_ij^2` on the chosen interval gives `H''(t)<=-3 underline_sigma_ij^2 t^2<0`. Weyl's inequality gives strict legality near zero. The rational-radius claim needs the wording clarification above. |
| Scope of arbitrary-rank lemma | `ADDENDUM_ARBITRARY_RANK.md:217-224` | `ACCEPTED_SCOPED` | The theorem is explicitly local near `t=0`; it does not prove whole-chord concavity and does not replace the unresolved four-cycle or nonreversible-entropy mechanisms. |
| Abstract rare-event lemma | `ADDENDUM_ENDPOINT_RARE_EVENT.md:10-76` | `NEEDS_WORDING_FIX_FOR_ABSTRACT_GENERALITY`; DPP use accepted | The Fisher term from a simple atom is `-a/x+O(1)`, while finite-order atoms of order at least two contribute at worst logarithmic size and positive-limit atoms remain bounded. This proves `H'' -> -infinity` under polynomial or endpoint-analytic finite-order hypotheses. The written “real-analytic on a left neighborhood” phrase alone is too weak unless it means analytic at/through `b` or includes (B.2) as a hypothesis. |
| Simple full-atom endpoint | `ADDENDUM_ENDPOINT_RARE_EVENT.md:78-150` | `ACCEPTED_SCOPED` | If `dim ker K(t_*)=1`, Schur complementation through strict `A` reduces the full atom to `det(C-sB^T A^{-1}B)`. A kernel vector `v` satisfies `s_* v^T M v = v^T C v >0`, so the zero eigenvalue crosses linearly with negative derivative in `s`. Because `t_*>0`, the zero is also simple in `t`. Lemma B.1 then applies in the polynomial DPP setting. |
| Simple empty-atom endpoint and negative endpoint | `ADDENDUM_ENDPOINT_RARE_EVENT.md:152-166`, `ADDENDUM_ENDPOINT_RARE_EVENT.md:111-112` | `ACCEPTED_SCOPED` | The empty-atom proof is the same Schur argument with `I-A` and `I-C`. The complete law is even under `t -> -t` for this block radial path, so the negative endpoint has the same conclusion. |
| Endpoint exact checkability and multiple-endpoint boundary | `ADDENDUM_ENDPOINT_RARE_EVENT.md:168-181` | `ACCEPTED_SCOPED` | In the DPP setting the endpoint determinants are rational polynomials in `s=t^2`, so square-free factorization/resultant plus isolating intervals can certify simple endpoints. The addendum correctly leaves multiple spectral endpoints outside the theorem; a quadratic vanishing atom can have a logarithmically divergent acceleration term, so the simple-root hypothesis is material. |
| Rank-two active endpoint location | `ADDENDUM_RANK2_ENDPOINT_SPECTRUM.md:8-53`, `ADDENDUM_RANK2_ENDPOINT_SPECTRUM.md:84-99` | `ACCEPTED_SCOPED` | Schur complements give `K(t)>=0 iff I-sR_0>=0` and `I-K(t)>=0 iff I-sR_1>=0`, so `s_*=1/max(rho_0,rho_1)`. At the endpoint, nullity equals the multiplicity of the active top eigenvalue. Since `rank(B)=2` and the whitening factors are positive definite, each active `R_nu` has exactly two positive eigenvalues; nullity two occurs exactly at a tie between those two positive eigenvalues. |
| Rank-two discriminant/tie criterion | `ADDENDUM_RANK2_ENDPOINT_SPECTRUM.md:55-82` | `ACCEPTED_SCOPED` | For a rank-two PSD operator with positive eigenvalues `lambda_1,lambda_2`, `2 tr(R^2)-(tr R)^2=(lambda_1-lambda_2)^2`. Thus `Delta>0` means the active top eigenvalue is simple, giving a simple full or empty atom and hence `H'' -> -infinity`. If `rho_0=rho_1`, either active side with `Delta>0` suffices; evasion requires every active side to satisfy the isotropy equation. |
| Exact arithmetic interface for rank-two endpoint | `ADDENDUM_RANK2_ENDPOINT_SPECTRUM.md:101-116` | `ACCEPTED_SCOPED` | The square root is unnecessary because the nonzero eigenvalues of `R_0` are the generalized eigenvalues of `B^T A^{-1}B v = rho C v`, and similarly for `R_1`. For rational inputs, the quadratic factor, active-side comparison, and discriminant sign are exact algebraic/rational tasks with isolating intervals. The compact interior and exceptional double-endpoint locus remain open. |
| Endpoint fixture comparison | `verify_local_and_matching.py:148-172`, `verify_local_and_matching.txt:12-14` | `ACCEPTED_SCOPED_AS_FIXTURE_OUTPUT` | The permitted code slice computes the trace discriminants without matrix square roots and then certifies `rho_K < 1/25 < 1/20 < rho_I-K`. The permitted output reports both endpoint discriminants positive and the active endpoint simple for `I-K`. This matches the addendum's rank-two endpoint test. I did not use this illustrative fixture as a proof of any global family claim. |

## Attack notes and preserved limitations

- Polynomial degree/full law: The arbitrary-rank likelihood is a complete-event determinant ratio, not a projected statistic. The score lower bound uses one two-point inclusion only to prove the complete-law first score is nonzero.
- True `t` curvature: The proof correctly converts from `s` to the physical affine parameter `t`; it proves strict negativity only for `0<|t|<=sqrt(delta)` and makes no whole-chord claim.
- Endpoint analyticity: The endpoint DPP theorem is sound because DPP complete atom probabilities are polynomials. The abstract real-analytic parenthetical needs the wording fix above if retained.
- Vanishing orders: The simple atom's `-a/x` Fisher divergence dominates all finite-order nonsimple atoms, whose worst acceleration contribution is logarithmic. This justifies both full-atom and empty-atom endpoint signs under the corrected analytic hypothesis.
- Endpoint signs: The positive endpoint proof uses `t_*>0`; the negative endpoint follows from evenness of complete probabilities in the block radial parameter.
- Rank-two root/tie: The discriminant criterion handles the active-side tie correctly; if both `rho_0` and `rho_1` are active, one simple active side is enough, and only all-active isotropy remains exceptional.
- Open scope: whole-chord concavity, multiple endpoints, compact-middle interval certification, and global entropy-rate curvature remain open.

No exact mathematical counterexample was found to the DPP claims. With the two wording corrections above, the three addenda are merge-eligible as scoped appendices.
