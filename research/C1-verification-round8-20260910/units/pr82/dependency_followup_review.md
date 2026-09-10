# PR82 dependency follow-up FIRST review

Verdict: **ACCEPTED_SCOPED for the main qualitative p>8 corrected-local-concavity claim**, under the standing hypotheses and correction priority stated below. Formula (6.7) remains an unproved finite-memory boundary/remainder claim, but after line-level clarification it is not the load-bearing gate for Section 7 as written.

This follow-up reads only the frozen pure author/proof sources listed in `source-snapshots/pr82_dependencies/SOURCE_BINDING.json`. It does not use old review opinions, C3 opinions, verification logs, live heads, or any execution result.

## 1. PR66 complex-disk inverse and non-nullness

5e08 uses the inherited PR66 inputs at `source-snapshots/pr82_delta/research/I05-DPP-31-pr66-lowreg-20260910/c4_response_p8.md` lines 18--30: a common complex disk, complete-event inverse control in `S_q`, future-bit influence `O((1+j)^(-2q))`, and tail variation `O((1+n)^(1-2q))`.

The dependency sources do contain those ingredients.

PR66 proof lines 50--105 define complete-event matrices `M_{I,x}=T_I(c)-I_{Z_x}` and prove a dimension-free singular-value gap and inverse operator bound. The proof uses the signed complete-event matrix structure and the spectral margin, and it explicitly says the estimates are uniform in volume and configuration and remain valid for complex Hermitian Toeplitz kernels from real non-even symbols.

PR66 proof lines 106--180 give the weighted Schur inverse bound. The band truncation plus weighted Neumann argument yields `sup_{I,x} ||M_{I,x}^{-1}||_{S_q}<infinity`, with the fixed truncation chosen independently of the event. This is the internal polynomial-localization estimate needed for the two-leg bounds.

PR66 proof lines 181--205 extend this to `f_z=c+zg`, giving a common complex disk and a uniform `S_q` inverse bound for all complete-event matrices. This directly supports the 5e08 derivative argument at lines 55--72, where derivatives of Schur complements are built from uniformly bounded `S_q` inverse factors.

PR66 proof lines 207--318 derive the complete-event one-sided Schur complement, future-bit flip estimate, added-last-site estimate, uniform convergence of finite-future conditionals, and tail variation. PR66 proof lines 319--333 then provide the uniform non-nullness and a common logarithm branch on a smaller disk.

Status: **ACCEPTED_SCOPED**. These are internal matrix/conditional estimates. They are not defeated by the separate external Dobrushin applicability gap in PR66 Section 6.

## 2. Parameter derivatives through order four

The dependency sources themselves prove the base `r=0` inverse/conditional influence estimates, while 5e08 lines 34--80 add the derivative-through-order-four claim by differentiating the same Schur-complement and resolvent identities inside the uniform complex disk.

Given the accepted PR66 common disk and uniform `S_q` algebra bound above, the 5e08 derivative transfer is analytically reasonable: differentiating `M_t^{-1}` inserts bounded `T(g)M_t^{-1}` factors, while a bit flip remains a rank-one diagonal perturbation, so the two long legs from the origin to the flipped site and back are retained. The common non-nullness from PR66 lines 319--333 then supports differentiating `log G_t`.

Status: **ACCEPTED_SCOPED as a source-level derivative import**, subject to the already recorded 5e08 proof details. This follow-up finds no missing PR66 source dependency for this step.

## 2a. True conditional entropy identification `h=-nu(logG)`

The source-level identification used at 5e08 lines 346--350 is legitimate. PR66 proof lines 391--397 identify the finite Schur-complement limit as the true future conditional law
`G_t(a | x_1,x_2,...) = nu_t(X_0=a | X_1=x_1,X_2=x_2,...)`. PR66 proof lines 400--404 then use the stationary finite-alphabet formula
`h(rho)=H_rho(X_0 | X_1,X_2,...)`. PR66 equilibrium bridge lines 13--20 restate the same complete-event conditional limit, and lines 52--67 give the same entropy formula from the right-to-left chain rule.

Together with the uniform non-nullness/log branch in PR66 proof lines 319--333, this gives exactly the input `h(t)=-nu_t(ell_t)`, `ell_t=log G_t`, used by 5e08 at lines 346--350. This step is `C^0`/identificational; it does not require the finite-memory comparison estimate (6.7).

Status: **ACCEPTED_SCOPED**.

## 3. Parity, evenness, and `H'(0)=0`

The parity/evenness input is source-supported. PR66 proof lines 469--487 use the diagonal gauge `D_{jj}=(-1)^j` to get `K_{c-zg}=DK_{c+zg}D`, invariance of event determinants and Schur complements, and `G_{-z}=G_z`, `phi_{-z}=phi_z`, `U_{-z}=U_z`. Lines 487--513 then factor the even holomorphic curve through `s=z^2` and write the entropy rate through the pressure derivative.

The `H'(0)=0` input has support, but it is not standalone. PR66 proof lines 515--558 identify the entropy deficit with specific relative entropy and then show the first derivative in `s` cancels in the pressure identity. PR66 equilibrium bridge lines 175--215 gives the same sign audit. PR53 finite-range source lines 343--397 gives an independent normalized-conditional version: in `R(t)=mathcal R(t^2)`, the derivative of the measure multiplies a zero observable, and the remaining term vanishes because `G_s(0x)+G_s(1x)=1`.

For 5e08, this means `H'(0)=0` is not an inherited-source hole, provided the p>8 replacement mechanism supplies the true entropy-rate representation and the differentiability needed to make the normalized-conditional argument legal. The line-level dependency is `h=-nu(logG)` at 5e08 lines 346--350 plus Lemma 6.1's `C^2` response at lines 261--321, applied at lines 353--367. It is not the later finite-memory estimate (6.7), which appears after Lemma 6.1 has already ended.

Status: **ACCEPTED_CONDITIONAL**. Parity/evenness is accepted. `H'(0)=0` is accepted conditional on the 5e08 true entropy-rate formula and Lemma 6.1 response, not conditional on (6.7).

## 4. PR53 matching quartic lower bound and regularity

5e08 lines 383--389 imports a regularity-free matching/negative-association lower bound from PR53 to obtain
`A >= |g_hat(k)|^4/[4 mu^2(1-mu^2)] = 2 alpha_k`.

The PR53 sources support that import.

PR53 finite-range theorem lines 54--87 establish the exact finite parity identity: the two parity marginals are fixed in `t`, independence holds at `t=0`, and the entropy deficit equals relative entropy after passing to the rate, without differentiating finite-window entropies.

PR53 finite-range theorem lines 88--143 prove the matching lower bound. The ingredients are parity, a vertex-disjoint odd-step matching, fixed one-site means, DPP negative association for disjoint decreasing edge observables, and the relative-entropy variational inequality. The argument yields a rate lower bound and then a quartic lower coefficient for the entropy deficit. None of these steps uses finite Fourier range or exponential Fourier decay.

PR53 exponential extension lines 233--253 makes that regularity separation explicit: the finite parity identity and matching argument do not require finite range, and the exponential/Hölder machinery is used only to get the analytic input. PR66 proof lines 560--589 imports exactly this matching bound and names the same coefficient `C_k`.

Status: **ACCEPTED_SCOPED**. The matching quartic floor should not be restricted to the finite-range or exponentially weighted theorem. Its role in 5e08 is as a regularity-free lower bound, while the missing regularity/response work lies elsewhere.

## 5. What (6.7) is and is not

The dependency follow-up does not close 5e08 lines 323--342. Formula (6.7) asserts a uniform comparison between finite-memory approximants and the true infinite-memory quantity through two `s` derivatives. The frozen PR66/PR53 sources do not provide that comparison in the polynomial-memory BFG setting.

That gap remains real for (6.7) itself. If the author keeps (6.7), it still needs a precise definition of the canonical truncation, a comparison between the finite-memory stationary law and the true law, and uniform constants after two parameter derivatives.

But (6.7) is not the Section 7 load-bearing route as written. Lemma 6.1 is stated and proved at 5e08 lines 261--321, ending with QED before the boundary paragraph starts. Section 7 then uses `h(t)=-nu_t(ell_t)` at lines 346--350 and applies Lemma 6.1 directly at lines 353--367. The following steps use `H'(0)=0` at lines 369--373 and the PR53 matching floor at lines 383--389. None of those lines cite or require the finite-memory approximants from lines 323--342.

Therefore (6.7) should be classified as **INCOMPLETE_EXTRA**, not as the dependency gate that kills the main p>8 application. This classification leaves the main qualitative Section 7 path available for the explicit scoped verdict below, while preserving (6.7) as an additional unproved quantitative comparison claim.

Status: **INCOMPLETE_EXTRA for (6.7); not a load-bearing blocker for Section 7 as written**.

## 5a. Main qualitative p>8 corrected-local-concavity claim

After this dependency clarification, the main qualitative claim is accepted at scoped FIRST level.

Standing hypotheses and scope:

* `p>8`, so 5e08 lines 353--358 give `a=p/2>4`.
* The PR66 strict-margin half-period setup is in force, with half-period-even center `c`, half-period-odd nonzero direction `g`, and an odd `k` with `g_hat(k) != 0`.
* The corrected BFG relaxation proof in `c4_response_p8_correction.md` has priority over the stale Lemma 4.1 proof paragraph in `c4_response_p8.md`.
* The accepted claim is qualitative local corrected concavity for `h(c+t g)+alpha_k t^4` on a nonempty symmetric interval around zero, strict away from the center.
* The accepted claim excludes the separate finite-memory comparison (6.7), whole-legal-interval concavity, explicit-radius/numerical claims, formalization, novelty, and any stronger real-analyticity assertion beyond the `C^2` response actually used in 5e08.

The proof chain is now source-supported:

1. PR66 gives the true conditional entropy identity `h=-nu(logG)`, as reviewed above.
2. 5e08 Lemma 6.1, lines 261--321, gives `C^2` response for `s -> nu_s(F_s)` under `a>4`, once the corrected BFG/Poisson inputs are used.
3. 5e08 lines 353--367 apply Lemma 6.1 with `a=p/2>4`, giving `C^2` regularity of `H(s)=h(c+sqrt(s)g)`.
4. PR66/PR53 source support gives `H'(0)=0`, as reviewed in Section 3.
5. PR53's regularity-free matching lower bound gives `A >= 2 alpha_k`, as reviewed in Section 4.
6. 5e08 lines 392--417 then perform the local calculus from `H(s)=H(0)-A s^2+o(s^2)` to the strict corrected concavity of `h(c+tg)+alpha_k t^4` for sufficiently small nonzero `t`.

I do not find a remaining concrete gap in this main qualitative path using the already accepted/limited sources. The only source-side caution is wording: 5e08 line 421 says the frozen PR66 statement is valid with `p>8`; that is broader than the accepted qualitative `C^2` local corrected-concavity result if read to include the frozen statement's real-analyticity bullet.

Status: **ACCEPTED_SCOPED for the main qualitative p>8 corrected-local-concavity claim**.

## 6. Original PR66 `p>4` status

PR66 proof lines 457--467 and equilibrium bridge lines 147--159 still rely on the imported Dobrushin finite-first-moment analyticity theorem. This dependency follow-up does not audit that external theorem and does not re-evaluate the original arbitrary-center `p>4` theorem.

The external Dobrushin applicability gap should not be used to discard PR66's independent internal matrix estimates, but it also is not repaired here.

Status: **unchanged INCOMPLETE for original `p>4`**.

## Import map for 5e08

| 5e08 import | Dependency source support | Status | Effect |
| --- | --- | --- | --- |
| Common complex disk and uniform complete-event inverse | PR66 proof lines 50--205 | ACCEPTED_SCOPED | Supports 5e08 lines 18--20 and derivative setup |
| Future-bit and tail variation estimates | PR66 proof lines 207--318 | ACCEPTED_SCOPED | Supports 5e08 lines 21--30 |
| Uniform non-nullness/log branch | PR66 proof lines 319--333 | ACCEPTED_SCOPED | Supports derivative of `log G_t` in 5e08 lines 70--72 |
| True entropy identity `h=-nu(logG)` | PR66 proof lines 391--404; equilibrium bridge lines 13--20 and 52--67 | ACCEPTED_SCOPED | Supports 5e08 lines 346--350 |
| Parity/evenness in `t` and `s=t^2` | PR66 proof lines 469--513; PR53 finite-range lines 54--87 | ACCEPTED_SCOPED | Supports 5e08 lines 361--367 |
| `H'(0)=0` | PR66 proof lines 515--558; equilibrium bridge lines 175--215; PR53 finite-range lines 343--397 | ACCEPTED_CONDITIONAL | Valid once 5e08 has `h=-nu(logG)` and Lemma 6.1 response |
| Regularity-free matching quartic floor | PR53 finite-range lines 88--143; exponential extension lines 233--253; PR66 proof lines 560--589 | ACCEPTED_SCOPED | Supports 5e08 lines 383--389 |
| Finite-memory boundary/remainder estimate (6.7) | Not supplied by dependency sources | INCOMPLETE_EXTRA | Separate quantitative finite-memory claim; not cited by Section 7 as written |
| Main qualitative p>8 corrected local concavity | Rows above plus 5e08 lines 392--417 | ACCEPTED_SCOPED | Accepted locally under standing hypotheses and correction priority |

## Final status buckets

### ACCEPTED_SCOPED

* Main qualitative p>8 corrected-local-concavity claim under the standing hypotheses and correction priority.
* PR66 internal complex-disk inverse and complete-event non-nullness inputs.
* PR66 true conditional entropy identity `h=-nu(logG)`.
* PR66/PR53 parity and evenness inputs.
* PR53 matching quartic lower bound as a regularity-free lower bound.

### ACCEPTED_CONDITIONAL

* `H'(0)=0`, conditional on 5e08's true entropy-rate formula and Lemma 6.1 response.

### INCOMPLETE_EXTRA

* 5e08 finite-memory boundary/remainder estimate (6.7), as a separate quantitative claim.

### INCOMPLETE_UNCHANGED

* Original PR66 arbitrary-center `p>4` theorem and external Dobrushin applicability.
* Any reading of 5e08 line 421 that claims the full frozen PR66 statement with real analyticity, rather than the qualitative `C^2` corrected-local-concavity consequence reviewed here.
* Original PR66 arbitrary-center `p>4` theorem and external Dobrushin applicability.

### PENDING_C2

None. No numerical comparison or arithmetic contract is needed for this dependency follow-up.

### NEEDS_FIX

The existing static correction-ordering issue remains as previously reported: the main 5e08 file should make the correction file's priority explicit or merge it. If (6.7) remains in the source, it should be proved or labeled as an additional quantitative comparison claim rather than treated as an implicit theorem gate. If line 421 is intended to claim the full frozen PR66 statement including real analyticity, it should be narrowed to the qualitative `C^2` corrected-local-concavity result accepted here.
