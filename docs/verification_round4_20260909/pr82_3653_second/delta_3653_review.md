# PR82 delta 3653 SECOND review

## Overall verdict

The delta substantially closes the p4 finite-response proof inside the author source packet. The new PR66 dependency audit, defective-renewal closure, DPP measure-continuity supplement, and two-loss continuity supplement remove the main "only as an unreviewed premise" weakness I recorded for the earlier `6ecc` packet.

Mathematical verdict: **CORRECT for the stated p>4 local corrected-concavity theorem**, with the same high-level dependency boundary that PR53's matching inequality remains an imported source result rather than something reproved in this delta.

One source wording issue remains: `README.md` line 191 still says "independently accepted regularity-free PR53 matching inequality". That is a prior-review-status phrase and should be removed or replaced by source-only wording, consistent with the delivered delta's stated redaction policy.

No novelty, formal proof, computation, whole-legal-interval theorem, or entropy counterexample is assessed.

## Binding and redaction status

**CORRECT with one text residual.** The delivered SHA-256 values and line counts match `delta_3653_input_binding.json` for all seven files. The binding also records original and delivered SHA-256 values separately for the redacted README and `one_loss` file.

The intended nonmathematical review-status redactions are visible in key places:

- `README.md` line 7 now says the proof depends on PR66 estimates "in their stated conditional scope" and on the "regularity-free PR53 matching inequality", not on review acceptance.
- `c4_response_p4_one_loss.md` line 525 says "regularity-free parity/matching bound from PR53", not "accepted".
- `c4_response_p4_one_loss.md` lines 604--608 explicitly frame the result as author-proof level/pending review and withdraw old p8 `(6.7)`.

**NEEDS_FIX.** `README.md` line 191 still says "The independently accepted regularity-free PR53 matching inequality implies". This is exactly the kind of prior-review-status adjective the delta says was removed. Suggested replacement: "The regularity-free PR53 matching inequality implies". The mathematical premise and line count can be preserved by deleting the review-status words.

`README.md` line 221 says "independently proved memory truncation estimate". I do not treat this as a prior-review-status claim if it refers to a separate mathematical proof inside the packet/source chain, but if the redaction policy is meant to remove all "independently" qualifiers, this line should also be normalized.

## PR66 dependency rederivation

**CORRECT.** `c4_response_p4_pr66_dependency_audit.md` rederives the PR66 inputs actually used by the p4 response repair and stops before the rejected Dobrushin/pressure bridge; see lines 1--7 and 295--304.

The singular-gap proof is closed: lines 11--56 give the complete-event matrix, the `J` accretivity identity, the uniform inverse bound, and inclusion of rare words. The weighted inverse localization is closed at lines 58--127: the band approximation gives `B^{-1}` in the weighted Schur norm, the tail estimate is `W^{q-p}`, and the product exponent `2q+1-p=(4-p)/2<0` closes exactly when `p>4` for `q=(p+2)/4`.

The common complex disk is correctly obtained by a weighted Neumann series, with no Hermiticity claim for complex `z`; see lines 129--151. The two-leg remote influence is correctly tied to a rank-one diagonal perturbation and two weighted legs; see lines 153--195. The infinite-future limit and full-future conditional identification are supplied at lines 197--229. Non-null logarithms and the `B_a` memory bound are supplied at lines 231--267. Complete-event parity/evenness is supplied at lines 269--293.

This is enough to treat the PR66 complete-event material as rederived source input for this delta, rather than merely an unreviewed bibliographic pointer. It still does not import the old interval-interaction/Dobrushin analytic pressure step, which the file explicitly excludes at lines 295--304.

## Defective renewal and Cauchy closure

**CORRECT.** `c4_response_p4_selfcontained_closures.md` closes the polynomial renewal tail without needing to rely on BFG Proposition 2(iv) as a black box. Lemma 1.1 at lines 9--95 proves that a defective renewal sequence with `sum f_n<1` and `f_n=O(n^-b)`, `b>1`, has finite total mass and `u_n=O(n^-b)`.

The application to the BFG age chain at lines 97--138 is correct: for summable `gamma_m`, the first-return law has total mass below one and polynomial tail, so `P(S_n=0)=O(n^-b)`. Lines 140--168 then rerun the BFG coupling inequality for arbitrary `B_b` observables without identifying `B_b` with BFG's printed `V_phi` observable class.

**CORRECT.** The Banach-valued Cauchy lemma at lines 169--238 is adequate for the needed derivative-memory claim. Pointwise holomorphy plus uniform `B_a` bounds on compact subdisks imply `B_a`-valued holomorphy and Cauchy estimates for every fixed derivative order. The DPP application at lines 217--238 supplies the uniform `B_a` bound for `ell_z=log G_z`.

## One-power Poisson response

**CORRECT.** `c4_response_p4_one_loss.md` replaces the old first-disagreement summation by an excursion/occupation-potential proof. The key BFG majorant is set up at lines 152--184. Lemma 3.1 at lines 186--266 proves both the relaxation tail and the occupation potential bound

`V_b(m)=sum_n E_m(1+S_n)^(-b) <= C(1+m)^(1-b)`.

This directly yields the one-power Poisson inverse

`Q_s:B_b -> B_{b-1}`

at lines 270--317. The proof avoids the old mistake of charging a reset event independently at every later time; this is explicitly identified at line 268.

**CORRECT.** The time/correlation cutoff is exactly what is needed and no more. Lines 319--345 prove finite Poisson-sum cutoff errors `(4.6)--(4.7)`, not a finite-window curvature extrapolation.

## DPP measure continuity and uniqueness

**CORRECT.** `c4_response_p4_measure_continuity.md` supplies the missing DPP-specific continuity and uniqueness closure. Lines 7--36 prove weak continuity from complete-event cylinder probabilities, which are polynomials in the physical parameter and even in `t`. Lines 38--57 prove invariance from the exact full-future conditional. Lines 59--73 prove uniqueness from the same coupling relaxation. Lines 75--91 then justify the response identity before derivatives are taken.

This correctly avoids a general, unproved continuity theorem for arbitrary summable-variation `g`-measures; see the explicit scope statement at lines 93--95.

## Two interpolation losses and moving-observable response

**CORRECT.** `c4_response_p4_continuity_detail.md` supplies the missing continuity details in the nested response formula. The one-Poisson continuity step at lines 48--89 proves sup-norm convergence by finite cutoff plus tail, then upgrades to `B_{b-1-eta}` by interpolation.

The two-loss accounting at lines 91--145 is the main point. It chooses `eta_1, eta_2>0` with `eta_1+eta_2<a-2`, first gets `R_sF_s` continuous in `B_{a-1-eta_1}`, then applies the second Poisson inverse at exponent `a-1-eta_1>1`, ending in `B_{a-2-eta_1-eta_2}`. The final exponent is positive, so the nested response expectation is continuous.

**CORRECT.** The exact difference-quotient derivation at lines 161--214 does not differentiate `R_s`; it uses the invariant-measure identity twice and applies the first derivative formula to the fixed observable `A_{1,s}R_sF`. Moving-observable terms are then ordinary scalar chain-rule terms; see lines 146--157 and 214.

The threshold summary at lines 216--230 is accurate: the continuity step hides no stronger condition than `a>2`, i.e. `p>4`.

## Local corrected concavity

**CORRECT.** `c4_response_p4_one_loss.md` applies the C2 response to true DPP entropy at lines 441--463. The proof that the linear term in `s` vanishes is strengthened: lines 465--513 use finite-volume complete-event mutual information, right-to-left chain rule, uniform non-nullness, and a Bernoulli relative-entropy quadratic bound to show `0<=H(0)-H(s)<=Cs^2`, hence `H'(0)=0`.

The quartic coefficient step at lines 515--578 is correct given the PR53 matching inequality as a source input. With `H(s)=H(0)-A s^2+o(s^2)` and `A>=C_k=2 alpha_k`, the corrected second derivative is

`12(alpha_k-A)t^2+o(t^2) <= -12 alpha_k t^2+o(t^2)`

for sufficiently small nonzero `t`, while it is zero at the center. This proves local concavity of `h(c+tg)+alpha_k t^4` on a smaller symmetric interval.

This does not claim full classical `C^4` regularity at nonzero parameters; `README.md` lines 197--203 and `one_loss.md` lines 550--578 correctly frame it as a centered Peano/fourth-coefficient conclusion from `C^2` response in `s`.

## p8 withdrawal and boundary priority

**CORRECT.** The delta explicitly withdraws the old p8 finite-memory second-derivative bridge:

- `c4_response_p4_one_loss.md` line 7 says p8 `(6.7)` is withdrawn as unproved and is not used.
- `c4_response_p4_one_loss.md` lines 580--600 state that the p>4 proof uses direct infinite-volume response plus time/correlation cutoff, and that polynomial spatial memory rates are not claimed for `4<p<=6`.
- `README.md` lines 205--221 state the same boundary priority and distinguish raw normalized-conditional truncation from stationary second-response convergence.
- `README.md` lines 223--233 give an authoritative file order: old `c4_response_p4_repair.md` equations `(7.3)--(7.5)` must be read as withdrawn by the boundary correction; p8 remains a preserved coarse proof only.

This fixes the over-reading risk I flagged in the previous p8-extra note.

## Optional p>6 spatial truncation

**CORRECT as an optional stronger-range estimate, with a compressed but adequate moving-observable clause.** `c4_response_spatial_truncation_p6.md` assumes `b>3` and common one-power Poisson estimates. The exact comparison identities at lines 38--80 correctly compare invariant expectations and Poisson inverses modulo constants killed by derivative operators.

The first-response block at lines 82--119 and the nested second-response block at lines 121--181 correctly spend one additional memory power in the kernel comparison. The condition `b-2>1` is the exact reason for the stronger range.

The canonical memory-truncation application at lines 185--227 uses the source estimate

`||partial_s^j(log G_s-log G_s^[N])||_{B_r} <= C N^{r-a}`

and takes the largest required `r` to be `b-1`. Choosing `b=3+eta`, `0<eta<a-3`, gives the rate `N^{-(a-2-eta)}` and requires `a>3`, i.e. `p>6`.

The moving-observable statement at line 183 and lines 216--224 is accurate when `F_s`, `F_s'`, and `F_s''` have the same `B_a` memory-truncation control; this is the intended entropy setting with `F_s=ell_s`. It is not used for the p>4 theorem and should remain optional.

## Source-priority and over-strong wording

**NEEDS_FIX.** `README.md` line 191 should remove "independently accepted". This is the only concrete residual source-status wording issue I found in the delta files.

**WATCH.** `README.md` line 221's "independently proved memory truncation estimate" is acceptable if meant as "proved separately as a mathematical estimate", but it should not be read as review acceptance.

**CORRECT.** The file priority order in `README.md` lines 223--233 is clear and should be followed:

1. Main one-loss author proof and related supplements control the p>4 theorem.
2. Boundary correction withdraws stale stationary frozen-memory response assertions.
3. p8 remains only a coarse historical route.

## Final delta unit verdicts

| Unit | Verdict | Evidence |
|---|---|---|
| Delivered SHA/line binding | CORRECT | All seven match `delta_3653_input_binding.json`. |
| Prior-review-status redaction | NEEDS_FIX | `README.md` line 191 still says "independently accepted". |
| PR66 dependency rederivation | CORRECT | `pr66_dependency_audit.md` lines 9--293, with exclusions at 295--304. |
| Defective renewal | CORRECT | `selfcontained_closures.md` lines 7--138. |
| Banach Cauchy derivative closure | CORRECT | `selfcontained_closures.md` lines 169--238. |
| BFG arbitrary `B_b` relaxation | CORRECT | `selfcontained_closures.md` lines 140--168; `one_loss.md` lines 152--184. |
| One-power Poisson inverse | CORRECT | `one_loss.md` lines 186--317. |
| Time/correlation cutoff | CORRECT | `one_loss.md` lines 319--345. |
| DPP measure continuity/invariance/uniqueness | CORRECT | `measure_continuity.md` lines 7--91. |
| Two interpolation losses | CORRECT | `continuity_detail.md` lines 48--160. |
| C2 response difference quotients | CORRECT | `continuity_detail.md` lines 161--214; `one_loss.md` lines 347--435. |
| Local corrected concavity | CORRECT | `one_loss.md` lines 441--578. |
| Old p8 `(6.7)` withdrawal | CORRECT | `one_loss.md` lines 7 and 604--608; README lines 205--221. |
| Optional p>6 spatial truncation | CORRECT as optional stronger-range result | `spatial_truncation_p6.md` lines 185--227. |
| Novelty | NOT_ASSESSED | Out of scope. |
| Formal/machine verification | NOT_PERFORMED | Forbidden by task scope. |
