# PR82 successor 3653 source-only FIRST review

Verdict: **ACCEPTED_SCOPED for the main qualitative `p>4` corrected-local-concavity claim**, with standing hypotheses exactly as stated in the frozen README and with the current one-loss proof as the operative route. The acceptance does not cover novelty, formal verification, `p<=4`, whole-interval concavity, arbitrary measurable symbols, finite-window curvature extrapolation, or the withdrawn memory-`N` stationary second-response bridge.

There is one non-mathematical source-order defect recorded in `successor_3653_code.md`: the README authoritative file-order list omits the new `c4_response_p4_one_loss.md`, even though that file is the current consolidated proof. That defect should be fixed for navigability, but it does not block the mathematical FIRST conclusion because the bound source itself is present and reviewed.

## Status by claim

| Claim or dependency | FIRST status | Reason |
|---|---|---|
| Original corrected-local-concavity theorem for every `p>4` | **ACCEPTED_SCOPED** | The 3653 source supplies the complete-event DPP input, one-power Poisson loss, two-loss `C^2` response in `s=t^2`, true entropy-rate identification, vanishing linear term, and PR53 quartic floor. |
| Old PR66 Dobrushin pressure route | **OPEN / NOT USED** | README keeps the A1/A2 applicability failure explicit at `README.md:L42-L46`, and the current proof bypasses it. |
| PR66 complete-event inverse/common disk/two-leg/non-null/parity imports | **ACCEPTED_SCOPED** | The 3653 dependency audit matches the frozen PR66 pure-source sections and stops before the invalid Dobrushin bridge. |
| PR53 matching lower bound and quartic floor | **ACCEPTED_SCOPED** | The regularity-free finite matching/lower-bound part is used at the rate level, not as finite-window curvature extrapolation. |
| Direct DPP weak continuity, invariance and uniqueness | **ACCEPTED_SCOPED** | Cylinder determinant continuity plus the true full-future conditional give the needed invariant laws before differentiating. |
| Nested response continuity at `p>4` | **ACCEPTED_SCOPED** | The two interpolation losses are explicitly chosen with total below `a-2`; no hidden `p>6` or `p>8` threshold remains in the main response step. |
| Optional spatial memory truncation rate | **ACCEPTED_SCOPED_EXTRA for `p>6`** | The abstract comparison spends one extra memory power and is correctly stated as optional, not as a premise of the `p>4` theorem. |
| Old `p>8` finite-memory equation (6.7) | **INCOMPLETE_EXTRA, not load-bearing** | The current sources explicitly withdraw it and replace it for the main theorem by direct infinite-volume response and correlation/time cutoffs. |
| Old `p>8` coarse response | **SUPERSEDED** | Its two-power Poisson route may remain a valid coarse argument, but it is no longer the current route. |

## Line-pinned proof review

### 1. Frozen theorem and hypotheses

The README states the theorem for real `c,g in A_p`, `p>4`, half-period even/odd symmetry, `g!=0`, and strict spectral margin `delta<=c<=1-delta` at `README.md:L13-L30`. It defines the correction coefficient `alpha_k=|g_hat(k)|^4/[8 mu^2(1-mu^2)]` for odd `k` with nonzero Fourier coefficient and claims concavity of `h(c+tg)+alpha_k t^4` on a small symmetric legal interval at `README.md:L32-L40`. The file also rules out spectral/von-Neumann entropy, rotated observation bases, finite-window extrapolation, and `L`-affine surrogates at `README.md:L40`.

This scope is precise enough for a source-only FIRST review. The conclusion is local in `t`; it is not a whole legal interval statement.

### 2. Complete-event inverse, non-nullness, and differentiated memory

The current dependency audit reconstructs the complete-event matrix singular gap at `c4_response_p4_pr66_dependency_audit.md:L9-L57`, weighted inverse localization at `L58-L128`, common complex disk at `L129-L151`, two-leg conditioned-bit influence at `L153-L195`, full-future convergence at `L197-L229`, and non-null logarithm with `B_a` variation at `L231-L267`. These items match the frozen PR66 pure source: the singular gap and uniform inverse are in `source-snapshots/pr82_dependencies/research/I05-DPP-25-20260909/proof.md:L50-L205`; the one-sided Schur complement, flip rank-one identity, two-leg bound, full-future limit, and non-null logarithm are in `proof.md:L207-L333`.

The audit’s boundary is also correct. It says the new proof imports only Sections 1--7 and excludes the interval-interaction/Dobrushin pressure bridge at `c4_response_p4_pr66_dependency_audit.md:L295-L304`. The PR66 pure source itself enters Dobrushin-dependent material after the complete-event construction, for example `proof.md:L465-L468`, so the 3653 route is right to avoid using those lines as a premise.

The one-loss proof then uses the same input at `c4_response_p4_one_loss.md:L13-L55` and proves that parameter derivatives retain the two-leg decay at `L56-L97`. The evenness/factorization through `s=t^2` is recorded at `L99-L111` and is mirrored in the dependency audit at `c4_response_p4_pr66_dependency_audit.md:L269-L293`. The Banach-valued Cauchy supplement at `c4_response_p4_selfcontained_closures.md:L169-L238` supplies the needed upgrade from pointwise holomorphy and uniform `B_a` bounds to Banach-space derivatives. I find this chain closed in the stated strict-margin `A_p` scope.

### 3. BFG coupling and one-power Poisson loss

The proof uses BFG only for the ratio-coupling/agreement-chain machinery, not for a higher-order response theorem. The ratio condition and decreasing majorant are stated at `c4_response_p4_one_loss.md:L152-L172`; the agreement-length chain and initial-agreement variant are stated at `L174-L184`. The load-bearing relaxation and occupation-potential estimates are proved at `L186-L268`, with the Poisson inverse conclusion `Q_s:B_b->B_{b-1}` at `L270-L317` and the correlation/time cutoff at `L319-L345`.

The self-contained closure file removes the fragile renewal citation: it proves the defective-renewal polynomial lemma at `c4_response_p4_selfcontained_closures.md:L7-L95`, applies it to the BFG age chain at `L97-L138`, and derives relaxation for every `B_b` observable at `L140-L167`. The renewal equation uses the corrected Latin `u_n` notation and the finite triangular summation is legitimate. The primary BFG paper was checked for the ratio condition, maximal coupling/agreement-chain transition, and return estimate citation; the 3653 proof’s use is consistent with those primary objects and does not import Tanaka or Dobrushin as substitutes.

I accept the one-power Poisson loss in this scoped source review. The threshold bookkeeping is also correct: inverse localization needs `2q+1<p`, while two Poisson inverses need `2q-1>2`; with `q=(p+2)/4`, this is exactly `p>4`, as stated in `README.md:L119-L134` and `c4_response_p4_selfcontained_closures.md:L240-L258`.

### 4. Response identity, `C^2` response, and continuity

The finite second-order response lemma assumes normalized non-null kernels with `partial_s^j log G_s` in `B_a`, `C^2` Banach dependence, and weak continuity of `nu_s`; see `c4_response_p4_one_loss.md:L347-L370`. It then derives the exact first and second response formulas at `L372-L393` from the invariant-measure identity at `L396-L430`, using two applications of `Q` on the scale `B_b -> B_{b-1} -> B_{b-2}` at `L415-L435`. No derivative of `Q_s` and no same-space spectral resolvent is inserted.

The previously thin continuity step is now supplied. Direct DPP weak continuity from complete-event determinant cylinder probabilities is proved at `c4_response_p4_measure_continuity.md:L7-L36`; invariance of the future law is proved at `L38-L57`; uniqueness follows from the same coupling relaxation at `L59-L73`; and the exact response identity needs only these pieces plus the Poisson equation at `L75-L91`.

The two-scale continuity supplement closes the nested terms when `a=p/2` is only slightly above two. It records uniform operator input at `c4_response_p4_continuity_detail.md:L7-L46`, continuity of one Poisson inverse with interpolation at `L48-L89`, continuity of two successive inverses with losses `eta_1+eta_2<a-2` at `L91-L159`, and exact difference-quotient remainders at `L161-L214`. The threshold accounting at `L216-L230` is sharp for this route: only `a>2` is required. I therefore do not see a main-path continuity gap.

### 5. True entropy-rate identification and vanishing linear term

For the true DPP law, the current proof identifies the entropy rate as `h(t)=-nu_t(ell_t)` at `c4_response_p4_one_loss.md:L441-L462`. This does not need the invalid PR66 pressure analyticity step. The underlying stationary-chain entropy identity appears in the frozen PR66 bridge at `source-snapshots/pr82_dependencies/research/I05-DPP-25-20260909/equilibrium_bridge.md:L52-L67`; combined with the fact that the DPP law has the true full-future conditional `G_t` at `equilibrium_bridge.md:L13-L20`, the equality case `h(nu_t)+nu_t(log G_t)=0` is explicit at `equilibrium_bridge.md:L69-L88`. The DPP-specific invariance statement in the new supplement gives the same identification without invoking Gibbs pressure at `c4_response_p4_measure_continuity.md:L38-L57`.

The proof of `H'(0)=0` is now independent of pressure theory. It uses finite-volume parity marginals and independence at the center at `c4_response_p4_one_loss.md:L476-L482`, right-to-left chain rule with uniformly non-null complete-event conditionals at `L484-L495`, obtains `0<=H(0)-H(s)<=Cs^2` after dividing by volume at `L497-L508`, and uses differentiability from the response lemma at `L511`. This is enough for the right derivative at the physical side and hence for the two-sided derivative of the constructed `C^2` even extension. I accept this step.

### 6. Quartic coefficient and corrected local concavity

The quartic part is source-supported. The finite parity identity and rate-level matching lower bound are in the accepted PR53 source at `source-snapshots/pr82_dependencies/research/I05-DPP-21-20260909/finite_range_local_theorem.md:L54-L87` and `L88-L143`; the same file records normalization and conversion to corrected concavity at `L343-L397`. The regularity-free extension states that the finite parity and matching argument do not require finite range at `source-snapshots/pr82_dependencies/research/I05-DPP-21-20260909/exponential_wiener_extension.md:L233-L253`.

The 3653 one-loss proof uses the matching bound at `c4_response_p4_one_loss.md:L525-L539`, sets `alpha_k=C_k/2` at `L542-L547`, computes the Peano second derivative of `h(t)=H(t^2)` at `L550-L565`, and obtains the corrected negative second derivative near every small nonzero `t` at `L568-L578`. Since the second derivative is continuous and equals zero at the center, this gives concavity on a sufficiently small symmetric legal interval. This proves the stated qualitative local theorem in the scoped sense.

### 7. Boundary withdrawal and old `p>8` material

The current source separates the main theorem from the old finite-memory bridge. `c4_response_p4_one_loss.md:L7` withdraws the full finite-memory second-derivative estimate from the earlier `p>8` file and says it is not used. The same file states that the main proof is direct in infinite volume and that spatial memory truncation is optional and stronger-range only at `L580-L600`. The README records the withdrawal and the valid replacement by correlation/Poisson time cutoffs at `README.md:L205-L221`, while the failure ledger preserves the old `p>8` file as coarse and superseded at `README.md:L223-L235`.

I therefore classify the old `p>8` finite-memory equation (6.7) as **INCOMPLETE_EXTRA**. It is not a load-bearing premise of the accepted `p>4` proof. This is an important separation: the extra estimate remains unproved, but it no longer blocks the main corrected-local-concavity claim.

### 8. Optional `p>6` spatial truncation proposition

The spatial truncation addendum says at `c4_response_spatial_truncation_p6.md:L1-L6` that it is optional and not needed for the original `p>4` theorem. Its abstract assumptions are one-power Poisson estimates for both kernels and a uniform operator perturbation bound on the needed scales at `L7-L37`. The two exact comparison identities are correct at `L38-L80`: constants may remain in the Poisson comparison, but every derivative operator kills constants.

The first Poisson/derivative block is controlled at `L82-L119`, the nested second-response block at `L121-L184`, and the canonical memory-truncation rate is derived at `L185-L227`. The loss accounting is honest: comparing full second-response formulas spends one extra memory power, so the displayed rate is available only with `b>3`, equivalently `a=p/2>3` or `p>6`. The scope paragraph at `L229-L231` correctly says this does not create finite-window entropy signs and does not turn memory-truncated chains into DPP claims.

I accept this as **ACCEPTED_SCOPED_EXTRA** for canonical memory freezing and uniformly `B_a` moving observables whose frozen versions have the stated `B_r` approximation. It should not be cited as evidence for the main `p>4` theorem, where direct infinite-volume response already suffices.

## Remaining open or excluded items

- **INCOMPLETE_EXTRA:** the earlier `p>8` finite-memory stationary second-response equation (6.7), preserved only as a failed extra bridge.
- **OPEN / NOT USED:** the old PR66 Dobrushin A1/A2 pressure import. Current success of the finite-response route does not repair that external theorem application.
- **OUT OF SCOPE:** novelty/priority, formal verification, machine recomputation, exact arithmetic, finite-window curvature signs, whole legal intervals, arbitrary measurable symbols, and `p<=4`.
- **NEEDS_FIX_STATIC:** README route index omits the new operative one-loss file; see `successor_3653_code.md`.
