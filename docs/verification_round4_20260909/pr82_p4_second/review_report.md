# PR82 p4/p8 finite-response SECOND review

## Overall verdict

The new p>4 finite-response route is **CORRECT within its stated local-concavity scope**, conditional on the PR66 complete-event inverse/two-leg/complex non-null input and the PR53 matching lower bound as source premises. The new argument does not use the rejected Dobrushin A1/A2 import, and it does not claim a finite-window stationary Hessian limit.

The p>8 checkpoint remains a separate, older sufficient route. Its two-Poisson-loss proof is still p>8 only, and its finite-memory derivative convergence `(6.7)` and analytic wording are not automatically supplied by the p>4 finite-response repair.

No novelty, formal proof certificate, machine recomputation, whole-legal-interval theorem, or entropy counterexample is assessed.

## Source binding

**CORRECT.** `input_binding.json` binds the PR82 files to head `6ecc004a3f99f97369ea5af53f1136b59cf2129c`, PR66 source files to `af1edaad69c4e1f5e4bbd1239b8463b56bf64075`, and PR53 source files to `65e59a46b49cd2dbb5c779a4cfae8cef26441984`. All listed SHA-256 values and git blob identifiers matched the local frozen packet.

## README scope and theorem statement

**CORRECT.** The README states a local corrected-entropy concavity theorem for `p>4`, strict half-period center/direction, physical affine path `K_t=T(c)+tT(g)`, and true stationary configuration Shannon entropy; see `README.md` lines 13--40. It also correctly marks the result as author proof pending review and lists its source dependencies at lines 5--7.

**CORRECT.** The README does not reuse the old Dobrushin import. Lines 42--46 state that the old polynomial interval telescope gives ordinary first moment but not Dobrushin's printed A1/A2 hypotheses, and that this packet bypasses the interaction-pressure theorem.

**NEEDS_FIX only if reused outside this packet.** The README's sentence at lines 5--7 says the theorem is "PROVED BY A NEW AUTHOR FINITE-RESPONSE ARGUMENT"; for independent review purposes this should continue to be read with the same line-7 caveat: the theorem is conditional on the PR66 and PR53 source premises and still pending external acceptance. The packet itself carries that caveat, so no mathematical correction is required inside this review scope.

## PR66 inherited complete-event inputs

**CORRECT as source premises, not independently re-proved here.** PR66 source gives the complete-event signed determinant convention in `frozen_statement.md` lines 36--44 and the theorem target at lines 48--86. The inverse proof in `proof.md` establishes uniform complete-event inverse control by a dimension-free singular-value gap and weighted Schur Neumann argument at lines 50--179, then a common complex parameter disk at lines 181--205.

**CORRECT as the load-bearing two-leg input.** The one-sided Schur complement formula appears in `proof.md` lines 207--226. A single remote future-bit flip is a rank-one diagonal perturbation, giving two long legs and the bound `(1+j)^(-2q)` in lines 228--263. Adding a final conditioned site and passing to the infinite future is handled at lines 264--317. Uniform non-nullness and the logarithmic normalized conditional are recorded at lines 319--333.

**CORRECT but conditional.** The equilibrium/entropy bridge identifies the DPP branch with the complete-event conditional and true configuration entropy, not a spectral entropy surrogate. See `equilibrium_bridge.md` lines 44--89 for the conditional cross-entropy inequality, lines 90--123 for the sign of the specific energy, lines 124--149 for exact equilibrium identification, and lines 151--174 for the true entropy formula. In this p4 review I treated those files as source premises, not as a new independent theorem acceptance.

## BFG primary-source use

**CORRECT.** The p4 proof does not simply apply BFG's displayed observable class to arbitrary `B_b` observables. It constructs a larger polynomial coupling majorant for each `1<b<=a`; see `c4_response_p4_repair.md` lines 141--202 and the author source-audit explanation at `c4_response_p4_source_audit.md` lines 7--93.

Direct primary check: BFG arXiv `math/9806132` contains the ratio/coupling condition around its equation `(4.1)`, the maximal coupling construction and suffix/matching process in Section 4, the elementary coupling inequality and renewal decomposition around equations `(5.4)`--`(5.11)`, and Proposition 2(iv) for polynomial renewal tails. Those are the exact ingredients used here. The proof's rerun with an enlarged `gamma^(b)` is a derivation from the primary coupling equations, not a black-box invocation of BFG Theorem 1 outside its stated norm class.

**CORRECT.** The "arbitrary `B_b`" step requires `b>1` so that the product in the return law is bounded away from zero. This condition is explicit in `c4_response_p4_repair.md` lines 155--169 and in the source-audit derivation at lines 60--88.

## One-power Poisson loss

**CORRECT.** The p4 repair improves the old two-power loss by tracking the first generated mismatch rather than the event that at least one mismatch occurs. The decisive estimate is `c4_response_p4_repair.md` lines 204--239 and its source-audit version at lines 95--143.

The logic is valid: if initial futures agree through memory `m`, then before a first mismatch at generated time `r` they agree through `m+r`, so the first-disagreement probability uses the full DPP exponent `a` while the post-mismatch relaxation uses the chosen observable exponent `b`. Summing in time gives `R_s:B_b -> B_{b-1}` for every `b>1`, as stated in `c4_response_p4_repair.md` lines 241--300.

This is the central mathematical distinction between the p4 and old p8 routes.

## Difference-quotient response and continuity

**CORRECT within the finite-response scope.** The second response formula in `c4_response_p4_repair.md` lines 303--400 only needs two Poisson solves:

`F in B_a -> R_s F in B_{a-1} -> A_1 R_sF in B_{a-1} -> R_s(A_1R_sF) in B_{a-2}`.

The second Poisson input exponent is `a-1`, so it remains above one exactly when `a>2`, i.e. `p>4`; see lines 365--372. The proof does not require differentiating `R_s`; the nested Poisson term is generated by the exact difference-quotient identity, as emphasized in lines 374--389.

**INCOMPLETE if read as analyticity.** This p4 finite-response unit proves the C2 response needed for local quartic curvature. It does not by itself supply the old frozen PR66 real-analytic entropy statement in `pr66_source/frozen_statement.md` lines 72--82. The p4 README avoids that stronger analytic claim; see `README.md` lines 32--38.

## Boundary correction and Poisson cutoff

**CORRECT.** `c4_response_p4_boundary_correction.md` explicitly supersedes only the old stationary boundary estimates `(7.3)`--`(7.5)` of `c4_response_p4_repair.md`; see correction lines 1--7. Its proved replacement is a finite time-correlation/Poisson cutoff, not a finite-memory stationary response theorem; see lines 9--33 for the one-Poisson cutoff, lines 35--85 for the interpolation tail, and lines 86--143 for the nested two-Poisson cutoff.

**CORRECT.** The unclaimed statement is also explicit: frozen-future stationary response convergence at the same exponent is not proved and needs a separate multiscale perturbation argument; see `c4_response_p4_boundary_correction.md` lines 145--156 and `c4_response_p4_source_audit.md` lines 268--279.

**NEEDS_FIX only for standalone reuse of `c4_response_p4_repair.md`.** If `c4_response_p4_repair.md` is read without the correction file, its old boundary subsection at lines 402--448 is stale. The packet's priority rule fixes the issue, but future readers should keep the correction file colocated or annotate the stale lines directly.

## True entropy, parity, deficit, and quartic floor

**CORRECT.** The entropy identity uses the one-sided complete-event conditional: `h_s=-nu_s(ell_s)` in `c4_response_p4_repair.md` lines 450--457. This matches the PR66 complete-event bridge in `pr66_source/equilibrium_bridge.md` lines 151--174.

**CORRECT.** The parity argument is source-consistent. PR66 proves half-period gauge invariance of complete-event determinants in `proof.md` lines 469--487. The p4 repair uses fixed parity marginals and the fact that `ell_0` depends only on the origin-parity future to get `nu_s(ell_0)=nu_0(ell_0)`; see `c4_response_p4_repair.md` lines 459--471 and `c4_response_p4_source_audit.md` lines 209--229.

**CORRECT.** The first `s`-derivative of the deficit vanishes by normalized-kernel cancellation, not by finite-window extrapolation. See `c4_response_p4_repair.md` lines 474--492 and the analogous PR53 finite-range derivation in `finite_range_local_theorem.md` lines 343--371.

**CORRECT as a source-based import.** PR53 supplies the matching lower bound for the entropy deficit using complete configurations, negative association, and a matching of odd edges. The key statements are `finite_range_local_theorem.md` lines 88--143 and lines 373--397, plus the non-small-norm route comparison at lines 457--473. In this review, that floor is treated as an allowed source premise; it was not upgraded into a new independent proof of PR53.

**CORRECT.** With `D(s)=A s^2+o(s^2)` and `A>=2 alpha_k`, the corrected curvature computation in `c4_response_p4_repair.md` lines 519--546 gives

`(h(t)+alpha_k t^4)'' = -12(A-alpha_k)t^2+o(t^2) <= -12 alpha_k t^2+o(t^2) < 0`

for sufficiently small nonzero `t`, with second derivative zero at the center. This proves local concavity of the corrected entropy on a smaller symmetric interval.

## p8 checkpoint and its extra scope

**CORRECT as p>8 only.** The old p8 file explicitly says it repairs only response regularity and does not repair the original p>4 quantifier; see `c4_response_p8.md` lines 3--7. Its Poisson inverse loses two powers, `R:B_b -> B_{b-2}`, so two nested solves require `a>4`, i.e. `p>8`; see lines 158--217 and lines 259--321.

**CORRECT after correction.** `c4_response_p8_correction.md` fixes the too-compressed BFG relaxation paragraph by rerunning BFG with an enlarged polynomial majorant for arbitrary `B_b`; see lines 1--7 and 18--86. The correction explicitly keeps the p>8 threshold unchanged at lines 88--96.

**NOT COVERED BY p4.** The p8 finite-memory derivative convergence statement `(6.7)` in `c4_response_p8.md` lines 323--342 is an extra p>8 finite-memory approximation claim. The p4 boundary correction proves only finite Poisson cutoff, so `(6.7)` should not be cited as a p>4 consequence.

**NOT COVERED BY p4.** The p8 analytic/even-analytic framing in `c4_response_p8.md` lines 219--243 and lines 361--367 is stronger than the p4 finite C2 response needed for curvature. The p4 README correctly avoids claiming full analyticity from the finite-response repair.

## Tanaka primary-source use

**CORRECT.** The packet does not use Tanaka as a black-box p>4 repair. `c4_response_p4_repair.md` lines 548--562 and `c4_response_p8.md` lines 425--440 correctly identify the gap: Tanaka's abstract perturbation theorems require reduced inverse/bounded-resolvent assumptions on a Banach scale that are not supplied by the present polynomial-memory transfer operator.

Direct primary check: Tanaka arXiv `2205.12561` states assumptions (I)--(IV), Theorem 2.10, Theorem 2.14, weak boundedness Proposition 2.13, and the Gouezel--Liverani setup in Section 3.5. Those assumptions require same-scale reduced inverse/Lasota--Yorke type structure beyond the one-power polynomial Poisson loss proved here. The packet's direct difference-quotient proof is therefore the right source-bound route.

## Final unit verdicts

| Unit | Verdict | Notes |
|---|---|---|
| Hash/blob binding | CORRECT | All listed local files matched `input_binding.json`. |
| README p>4 local corrected-concavity scope | CORRECT | Conditional caveats are present in lines 5--7. |
| Rejection of old Dobrushin A1/A2 import | CORRECT | README lines 42--46. |
| PR66 inverse/two-leg/complex non-null input | CORRECT as source premise | Not independently re-proved here. |
| BFG arbitrary `B_b` coupling bridge | CORRECT | Requires the enlarged majorant and `b>1`. |
| One-power Poisson loss | CORRECT | Main p>4 improvement. |
| Two difference-quotient response formula | CORRECT | C2 in `s`, not full analyticity. |
| Boundary correction priority rule | CORRECT | Old `(7.3)`--`(7.5)` withdrawn/superseded. |
| Frozen-memory stationary response convergence | INCOMPLETE | Explicitly not proved for p4. |
| True entropy identification | CORRECT as source premise | Complete-event conditional, not spectral entropy. |
| Parity and `D'(0)=0` | CORRECT | Uses fixed parity marginals and normalization. |
| PR53 matching quartic floor | CORRECT as source premise | Not a new independent PR53 acceptance. |
| Corrected curvature coefficient | CORRECT | Needs `A>=2 alpha_k`, which is the imported floor. |
| p8 checkpoint | CORRECT as p>8 only | `(6.7)` and analytic differences remain p8-only extras. |
| Tanaka citation role | CORRECT | Not sufficient by itself for p>4. |
| Novelty | NOT_ASSESSED | Out of scope. |
| Formal/machine verification | NOT_PERFORMED | Explicitly forbidden. |
