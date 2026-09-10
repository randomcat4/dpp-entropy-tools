# PR82 successor 6ecc delta-FIRST review

Verdict: **ACCEPTED_SCOPED for the main qualitative p>4 corrected-local-concavity repair**, with a static source fix required to mark the superseded boundary equations in the main repair file.

The accepted result is local and qualitative: for the stated strict-margin half-period `A_p` hypotheses with `p>4`, the corrected true stationary DPP configuration entropy `h(c+t g)+alpha_k t^4` is locally concave near `t=0`. This review does not accept whole-legal-interval concavity, `p<=4`, novelty, formalization, numerical verification, or the withdrawn frozen-memory stationary response rate.

## 1. README and scope control

README lines 5--7 correctly identify the new p>4 proof as an author proof pending review, not independent acceptance. They also identify its dependencies: PR66 complete-event inverse/two-leg estimates in their conditional scope and the PR53 regularity-free matching inequality. This is consistent with the earlier dependency follow-up.

README lines 11--40 state the repaired theorem in the right qualitative form: `p>4`, strict margin, half-period-even center, half-period-odd nonzero direction, physical affine kernel, true stationary DPP configuration entropy, and local corrected concavity. The README no longer tries to claim a full Dobrushin pressure theorem or a spectral/von-Neumann entropy substitute.

README lines 42--46 preserve the Dobrushin failure: A1/A2 applicability is still not repaired, and the new proof bypasses that interaction-pressure route. Lines 138--154 correctly say the old frozen-memory stationary response rate is withdrawn and replaced by a finite time-correlation/Poisson cutoff. Lines 156--166 keep the p8 proof as a coarse checkpoint and keep the usual nonclaims.

Status: **ACCEPTED_SCOPED**.

## 2. Inherited PR66 inputs and parameter derivatives

`c4_response_p4_repair.md` lines 49--65 use only the retained PR66 input: a common complex disk, nonzero complete-event Schur complements, and the two-leg conditional variation bound. These were already bound to PR66 source in the dependency follow-up and are not Dobrushin pressure consequences.

Lines 67--101 correctly transfer this input to parameter derivatives through order four. The Cauchy argument is legitimate in this source setting because line 69 uses holomorphic differences on a smaller common disk with the same spatial bound, and lines 80--86 sum the single-coordinate tail to get `B_a` variation. Lines 89--101 use half-period gauge evenness to pass from `z` to `s=z^2`, so only two `s` derivatives are needed.

Status: **ACCEPTED_SCOPED**.

## 3. BFG relaxation for `B_b` observables

The main repair file lines 141--202 and the source-audit file lines 7--93 correctly avoid over-citing BFG as a ready-made linear-response theorem. They use the printed coupling mechanism instead.

The route is:

* enlarge the DPP ratio continuity bound to a decreasing summable majorant `gamma_m^(b)` for any `1<b<=a` (`c4_response_p4_repair.md` lines 145--161);
* use BFG's dominating chain and first-return renewal law (`lines 163--175`);
* compare `B_b` variations with the first-return law (`lines 177--183`);
* use the renewal convolution and BFG polynomial return estimate to get `osc(L_s^n F) <= C ||F||_b (1+n)^(-b)` (`lines 185--199`).

The source-audit file lines 23--93 makes the same point more explicitly: this is a derived consequence of BFG's coupling equations, not a claim that BFG's displayed `V_phi` theorem already contains every `B_b` observable.

Status: **ACCEPTED_SCOPED**.

## 4. One-power Poisson loss

`c4_response_p4_repair.md` lines 204--239 prove the first-disagreement estimate. The argument keeps the time `r` of the first generated mismatch: before that time, the coupled histories have memory `m+r`, so the full DPP exponent `a` applies; after the mismatch, the remaining time is controlled by the BFG relaxation at exponent `b`.

Lines 241--300 then sum the estimate over `n` to prove the Poisson operator bound
`R_s:B_b -> B_{b-1}` for `b>1`. This is the key threshold change. Two Poisson inverses now require
`B_a -> B_{a-1} -> B_{a-2}` with the second input exponent above one, so `a>2`, equivalently `p>4`.

The source-audit file lines 95--142 independently rederives the same estimate and identifies the earlier two-power bound as a coarse artifact of forgetting the first mismatch time.

Status: **ACCEPTED_SCOPED**.

## 5. Difference-quotient response lemma

`c4_response_p4_repair.md` lines 303--321 state Lemma 6.1 with the correct threshold: normalized uniformly non-null finite-alphabet kernels, `B_a` control of two `s` derivatives of `log G_s`, uniform ratio coupling, and `a>2`.

Lines 354--369 give the exact first-difference identity
`(nu_u-nu_s)(F)=nu_u(L_u-L_s)R_sF`, then divide by `u-s` using the operator Taylor expansion. Lines 371--387 apply the same identity to the fixed observable `A_1R_sF`; the one-power loss makes this legal because `A_1R_sF in B_{a-1}` and the second Poisson input still has exponent greater than one.

Lines 389--398 give a plausible and sufficient continuity argument: uniform sup convergence of the Poisson series, uniform weaker-space bounds from Lemma 5.2, and interpolation leave a positive margin below `a-2`. The source-audit file lines 144--207 repeats the same difference-quotient derivation and correctly notes that no derivative of `R_s` is assumed.

I do not find a concrete gap in Lemma 6.1 under the stated inputs.

Status: **ACCEPTED_SCOPED**.

## 6. Entropy response and p>4 curvature

`c4_response_p4_repair.md` lines 450--456 use the true one-sided conditional entropy identity `h_s=-nu_s(ell_s)`, which was already accepted from PR66 conditional-limit sources. Lines 459--463 use parity independence at the center and fixed parity marginals to get `nu_s(ell_0)=nu_0(ell_0)`, and lines 466--471 rewrite the true entropy deficit as
`D(s)=nu_s(ell_s-ell_0)`.

Lines 474--492 use Lemma 6.1 plus normalization to prove `D'(0)=0`. The normalization step is correct: differentiating `G_s(0|x)+G_s(1|x)=1` makes `L_0 ell'_0=0`, and invariance gives `nu_0(ell'_0)=0`.

Lines 495--516 combine `D(s)=A s^2+o(s^2)` with the already accepted PR53 regularity-free matching lower bound to obtain `A>=2 alpha_k`. Lines 519--546 then perform the correct local calculus:
`h''(t)=-12A t^2+o(t^2)`, so the corrected functional has second derivative `-12(A-alpha_k)t^2+o(t^2)<0` for sufficiently small nonzero `t`, and second derivative zero at the center.

The source-audit file lines 209--266 tracks the same argument. It does not introduce a finite-window curvature extrapolation.

Status: **ACCEPTED_SCOPED for the main qualitative p>4 corrected-local-concavity claim**.

## 7. Boundary correction and priority

The main repair file still contains a Section 7 finite-memory estimate at lines 402--448. Its equations (7.3)--(7.5), lines 422--445, claim a stationary frozen-memory second-response convergence rate that the correction later withdraws.

`c4_response_p4_boundary_correction.md` line 5 explicitly supersedes only those equations and says the raw rate was asserted too quickly and is not used in the entropy-concavity proof. Lines 9--33 prove the one-Poisson cutoff; lines 35--84 give the interpolated inner-tail estimate; lines 86--143 prove the two-Poisson time-correlation cutoff; lines 145--156 state the stronger frozen-memory stationary response convergence remains unclaimed.

This correction is mathematically coherent and does not change the theorem threshold or entropy conclusion. It does, however, leave a static readability problem in the main repair file.

Status: **ACCEPTED_SCOPED for the corrected cutoff; NEEDS_FIX_STATIC for the stale main-file equations**.

## 8. Tanaka, Dobrushin, and nonclaims

`c4_response_p4_repair.md` lines 548--562 correctly refuse to use Tanaka as a black box: Tanaka's same-space reduced-resolvent and GL Lasota-Yorke hypotheses are not met by the polynomial one-power-loss scale. Lines 564--570 correctly state that Dobrushin 1974 A1/A2 is deliberately unused and that the old p8 proof is only a coarse checkpoint.

README lines 164--166 make no claim for `p<=4`, whole legal interval, arbitrary measurable symbols, entropy counterexample, novelty, or started independent review. This is the right scope.

Status: **ACCEPTED_SCOPED**.

## Final status buckets

### ACCEPTED_SCOPED

* Main qualitative p>4 corrected-local-concavity repair under the README theorem hypotheses and boundary-correction priority.
* BFG coupling-to-`B_b` relaxation bridge as a derived source argument, not a generic response theorem.
* One-power Poisson loss `R:B_b -> B_{b-1}` for `b>1`.
* Lemma 6.1 finite second-order response at threshold `a=p/2>2`.
* True entropy-rate conditional formula, `D'(0)=0`, and PR53 matching floor application.
* Corrected finite time-correlation/Poisson cutoff in the boundary correction file.
* Nonuse of Dobrushin A1/A2 and Tanaka black-box routes.

### NEEDS_FIX_STATIC

* `c4_response_p4_repair.md` lines 422--445 should be marked superseded in place or replaced with the corrected cutoff. The separate correction file and README priority prevent this from blocking the main theorem, but the main file alone is currently misleading.

### INCOMPLETE / not accepted

* The withdrawn frozen-memory stationary second-response convergence at the raw kernel norm rate.
* Whole-legal-interval concavity, `p<=4`, arbitrary measurable symbols, entropy counterexample, novelty, formal verification, and machine recomputation.

### PENDING_C2

None. No finite arithmetic comparison is part of this delta.
