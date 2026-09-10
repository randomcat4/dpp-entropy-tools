# PR91 C1 FIRST review report

Scoped verdict: `ACCEPTED_SCOPED` for the analytic reductions and implication theorems, with all displayed finite rational/log/constant checks and all author-generated outputs classified as `SOURCE_ONLY / PENDING_C2`. The whole-interval curvature sign is `OPEN`; novelty and formal verification are `NOT_ASSESSED`.

No source-level `NEEDS_FIX` item is raised in this bounded FIRST. The packet is careful to distinguish a proved response/certificate framework from a completed continuum sign proof.

## What is accepted analytically

The fixed physical object and event convention are explicit. `proof.md` lines 7-18 fix exactly `f_t(theta)=1/2+cos(4*pi*theta)/4+t*cos(2*pi*theta)/8`, `t in [1/2,3/2]`, use the genuine affine correlation-kernel direction, and define complete events by the signed determinant/inclusion-exclusion identity. `RESULT.md` lines 7-12 restate the same object, natural logarithms, complete events, and per-original-coordinate normalization.

The correction-state/Riccati representation is accepted for this source review. `proof.md` lines 20-35 group two original coordinates per cell, define the four signed cell matrices `D_alpha`, the off-diagonal block `E`, the correction state `Q=E S^{-1}E^T`, weights `g_alpha=a*beta*det(D_alpha-Q)`, and updates `T_alpha(Q)=E(D_alpha-Q)^{-1}E^T`. The determinant ratio at lines 31-35 identifies the weights with actual finite complete-event conditional probabilities. This is a complete-event Schur complement construction, not a switch to an L-kernel, a spectral basis rotation, or an inclusion-probability surrogate.

The invariant domain and positive Markov operator are accepted subject to the stated constant gates. `proof.md` lines 37-66 give the convex domain `||Q||_2<=1/8`, uniform inverse bounds, the explicit four-weight formula, weight normalization, positivity, and image containment. The rational inequalities behind constants such as `81/1024`, `17/144`, and `34/81` are author exact constants and remain `PENDING_C2`; conditional on those gates, the analytic implication to a positive normalized four-branch operator is sound.

The law-level contraction correctly includes changing weights. `proof.md` lines 80-106 explicitly says branch contraction alone is insufficient, derives a total-variation Lipschitz bound for the four probabilities, couples matching and mismatching labels, and obtains the full `W1` contraction `4363/5184`. The post-handoff supplement strengthens the bound: `post_handoff_cancellation.md` lines 7-25 give a smaller branch-image radius, lines 27-48 improve the total-variation and full law contraction to `4259/6480<2/3`, and lines 156-160 say this is an optional stronger gate rather than a silent replacement of an already frozen compute job. The exact rational comparisons for the improved constants remain `SOURCE_ONLY / PENDING_C2`, but the proof does retain the weight-variation term.

The true entropy-rate factor is correct. `proof.md` lines 114-125 shows `mu_m(B_t)=H(Y_0 | Y_1,...,Y_m)` for two-site cells and then `h(f_t)=(1/2) eta_t(B_t)`. The factor `1/2` is per original coordinate, not per grouped cell. `README.md` lines 11-17 and `RESULT.md` lines 31-34 carry the same normalization.

The coding derivative formulas retain state motion. `proof.md` lines 127-149 differentiate the Riccati map along a fixed observed word and keep both the explicit parameter derivative and the state jets `Q'`, `Q''`. Lines 182-205 define partial operator derivatives at fixed trial observable and include the map-motion terms in `L'A` and `L''A`. `curvature_certificate.md` lines 105-120 separately warns implementations not to differentiate trial coefficients inside operator derivatives and to include all four branches and map-motion terms. This addresses the main risk of confusing fixed-Q local derivatives with the moving coding derivative.

The complete Fisher bridge is accepted as an analytic identity, again with constants pending. `coding_and_fisher.md` lines 86-101 defines total conditional jets `gamma_alpha` and `gamma2_alpha`, includes every branch, and identifies the local total entropy second derivative. Lines 103-132 bridge finite complete-event scores to the infinite conditional Fisher rate using explicit forgetting and reverse-martingale orthogonality, yielding the per-original-coordinate Fisher rate at lines 127-130. The finite-event matching and exact constant values cited in `exact_checks.py` and `output/exact_output.json` are not independently verified here.

The invariant-law second response is accepted. `proof.md` lines 207-234 differentiates the stationary identity through the centered resolvent and obtains

`h''(t)=(1/2) eta_t[ B_t'' + L_t'' u + 2 L_t' v ]`.

The nested invariant-measure response term is present at lines 213-228, and lines 230-234 explicitly say the fixed-Q Fisher piece alone is not the full coding Fisher rate. `curvature_certificate.md` lines 32-71 derives the three-Poisson residual bound from the same full response error, including the nested response term. The post-handoff refinement also preserves it: `post_handoff_cancellation.md` lines 102-129 repeats the full-response error identity before deriving the stronger Hessian-only certificate.

The residual-certificate framework is accepted as a sufficient theorem, not as a completed sign certificate. The original theorem in `curvature_certificate.md` lines 5-30 says that uniform residual bounds over the whole state domain and a parameter cell imply

`|h''(t)-c2/2| <= 13 e01 + e02/8 + 6 e11/5 + e20/2`,

with a whole-interval proof requiring gap-free parameter coverage. `post_handoff_cancellation.md` lines 102-135 strengthens this to the Hessian-only gate

`|h''(t)-c2/2| <= e02/2 + (9/100)e12 + e20/2`,

using `L_t Q=0` and affine-error cancellation. Lines 137-154 also preserve a sharpened mixed-derivative gate and state that the original coarser gate remains correct. These are valid analytic implications conditional on the advertised constants and on future rigorous suprema over the entire domain; sampled maxima do not meet the hypotheses.

The finite-state/HMM limitation is stated correctly. `README.md` line 10, `RESULT.md` line 36, `coding_and_fisher.md` lines 21-29, and `sources_and_attempts.md` lines 7-11 and 44 all avoid claiming that injectivity of this correction-state presentation rules out every different finite HMM representation. The accepted statement is only that this exact non-atomic correction-state presentation cannot be replaced by finitely many of its own states.

## Source-only evidence left pending

The following items remain `SOURCE_ONLY / PENDING_C2`:

- All exact rational constant comparisons and slacks in `proof.md` lines 45-76, 93-100, 137-147, and 163-205; `curvature_certificate.md` lines 52-69; and `post_handoff_cancellation.md` lines 7-48, 50-70, 74-100, and 120-154.
- The author Fraction reconstruction of 252 complete events and derivative layers described in `README.md` line 33, `RESULT.md` lines 102-108, `sources_and_attempts.md` lines 21-27, `exact_checks.py` lines 94-175, and `output/exact_output.json` lines 1-45.
- The post-handoff exact constant check in `check_tightening.py` lines 1-47 and `output/tightening_output.json` lines 1-28.
- The polynomial scouts in `poisson_scout.py` lines 1-142 and `output/scout_summaries.json` lines 1-56. The source correctly labels them non-certifying; `curvature_certificate.md` lines 122-128 and `RESULT.md` lines 102-108 say they do not prove even a single rigorous curvature point.
- The private raw coefficient archive mentioned in `sources_and_attempts.md` line 38. It is not load-bearing for the analytic theorems and was not accessed.

## Open gates and boundaries

The continuum curvature gate is still open. `README.md` lines 19-23, `RESULT.md` lines 94-100, `curvature_certificate.md` lines 24-30 and 122-128, `post_handoff_cancellation.md` lines 131-135, and `sources_and_attempts.md` lines 40-44 all say that the whole interval needs rigorous uniform residual enclosures over the complete state domain and parameter cells. No sampled maximum, finite difference, author PASS, scout candidate, old PR77 point certificate, or PR79 upper budget closes that gate.

The current strongest analytic gate is the post-handoff one in `post_handoff_cancellation.md`; the original proof and compute contract retain their coarser constants. `compute_contract.md` lines 7-13 freeze an earlier author source state and the original `4363/5184` contraction, while lines 39-43 use the original residual gate. `post_handoff_cancellation.md` lines 156-160 says the stronger gates do not add a budget, start a job, or silently change an already claimed job. Any downstream checker must say which source/gate and constants it is certifying.

The 7200-second continuum request is only an author compute contract, not authorization for this C1 review or for a new C2 job. `compute_contract.md` lines 1-3 and 45-59 state requested/not-running status, resource caps, stopping conditions, and deliverables. This FIRST did not run or request that work.

PR77 and PR79 are not premises for PR91 acceptance. `proof.md` line 3 says no unreviewed theorem or numerical output is a premise; `README.md` line 41 excludes the previous comment-only 4096-box computation and unreviewed PR77 finite conclusion; `RESULT.md` lines 110-116 limits PR77 to fixed midpoint/point-curvature context and says it does not certify the continuous interval; `sources_and_attempts.md` lines 15-17 treats PR79 as an upper majorant/background and PR77 C2 as non-continuum. I did not need additional predecessor pure source for the bounded analytic verdict.

Novelty, priority, formalization, merge readiness, and the final sign `h''(t)<0` on `[1/2,3/2]` are not assessed or accepted here.
