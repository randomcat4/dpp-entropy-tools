# PR59 Independent First Review

Reviewer: `C1 fresh PR59 first reviewer`

Role: fresh non-author first reviewer for the entire PR59 packet.

Source alias: `source-snapshots/pr59/`

Accepted-main alias used for inherited inputs: `source-snapshots/accepted_main/`

Frozen head: `892a121a6e26fcf638c75de917e50a4503b5675e`

Frozen base: `9dcb6e9079ca57f94e0e30d63161cda89ca61fae`

## Overall Verdict

`ACCEPTED_SCOPED`

Within the frozen PR59 scope, I find the compact radial-tube theorem, the arbitrary-strict-parameter RPF Hessian identity, the qualitative finite-state true-rate error interface, the beam-splitter second-order obstruction, and the displayed nonconstant mean-`1/3` family `CORRECT`.

This verdict does not certify whole-interval concavity for arbitrary centers, endpoint-uniform center radii, the full PR39 interval, arbitrary measurable symbols, an occupation-entropy gain inequality, or a true entropy-rate counterexample. PR59 correctly marks those items as incomplete in `source-snapshots/pr59/frozen_statement.md:138`, `source-snapshots/pr59/RESULT.md:62`, and `source-snapshots/pr59/proof.md:625`.

No script execution, arithmetic job, finite-size experiment, SymPy run, or formal check was performed in this C1 review. Recorded outputs were inspected as static author artifacts only.

## Packet and Dependency Binding

Status: `CORRECT`

The packet binding lists 14 added files, all marked download-hash-verified, with the expected prefix and frozen head in `source-snapshots/pr59/SOURCE_BINDING.json:1` through `source-snapshots/pr59/SOURCE_BINDING.json:110`. I read all 14 packet files.

The author explicitly separates proof, static code, output, and incomplete scope in `source-snapshots/pr59/README.md:65` through `source-snapshots/pr59/README.md:78`. The self-audit also states that it is not an independent review in `source-snapshots/pr59/verification.md:1` through `source-snapshots/pr59/verification.md:3`.

For inherited theorem scope, I used only accepted-main records and sources. The PR53 accepted record gives local entropy-rate concavity near the parity point, plus event-inverse localization, one-sided conditionals, RPF rate formulas, and the absence of a quadratic term; it explicitly does not give whole-legal-interval curvature in `source-snapshots/accepted_main/docs/verification_round3_20260909/accepted_pr53.md:21` through `source-snapshots/accepted_main/docs/verification_round3_20260909/accepted_pr53.md:25` and `source-snapshots/accepted_main/docs/verification_round3_20260909/accepted_pr53.md:53` through `source-snapshots/accepted_main/docs/verification_round3_20260909/accepted_pr53.md:55`. The W2 PR34 audit supplies the constant-centered whole-feasible-interval quartic correction in `source-snapshots/accepted_main/docs/verification_20260909/w2/radial_quartic_audit.md:6` through `source-snapshots/accepted_main/docs/verification_20260909/w2/radial_quartic_audit.md:28`, with the exact `(4/3)|c_k|^4` constant justified in `source-snapshots/accepted_main/docs/verification_20260909/w2/radial_quartic_audit.md:85` through `source-snapshots/accepted_main/docs/verification_20260909/w2/radial_quartic_audit.md:109`.

## Claim 1: Compact Radial-Tube Theorem

Status: `CORRECT`

The frozen statement fixes `beta`, `mu`, real anti-periodic `g`, an odd nonzero Fourier mode `k`, and a prescribed compact interval with strict radial legality in `source-snapshots/pr59/frozen_statement.md:11` through `source-snapshots/pr59/frozen_statement.md:61`. The center perturbations are restricted to the even, mean-preserving `A_beta` subspace near the constant center in `source-snapshots/pr59/proof.md:171` through `source-snapshots/pr59/proof.md:185`, so the theorem is not claiming arbitrary-center coverage.

The proof of the uniform event inverse is valid after incorporating the clarification. The signed accretivity estimate includes every complete zero/one pattern in `source-snapshots/pr59/proof.md:102` through `source-snapshots/pr59/proof.md:122`. The missing `||B_{t,Z}||<1` justification is supplied in `source-snapshots/pr59/clarifications.md:5` through `source-snapshots/pr59/clarifications.md:46`. The weighted truncation and Neumann restoration in `source-snapshots/pr59/proof.md:124` through `source-snapshots/pr59/proof.md:169` are the compact-radial version of the accepted EW inverse argument in `source-snapshots/accepted_main/research/I05-DPP-21-20260909/exponential_wiener_extension.md:45` through `source-snapshots/accepted_main/research/I05-DPP-21-20260909/exponential_wiener_extension.md:154`.

The Banach-parameter analyticity step is scoped correctly. The perturbation enters the event matrix linearly as `K_{u+(z-t_*)g}` in `source-snapshots/pr59/proof.md:189` through `source-snapshots/pr59/proof.md:205`, with a radius independent of word and volume. The near/far Schur-resolvent estimate and Cauchy-derivative passage in `source-snapshots/pr59/proof.md:209` through `source-snapshots/pr59/proof.md:247` match the accepted EW mechanism in `source-snapshots/accepted_main/research/I05-DPP-21-20260909/exponential_wiener_extension.md:185` through `source-snapshots/accepted_main/research/I05-DPP-21-20260909/exponential_wiener_extension.md:231`.

The parity and normalization cancellation is also valid. The proof uses diagonal gauge invariance to get evenness in `source-snapshots/pr59/proof.md:253` through `source-snapshots/pr59/proof.md:257`, but does not rely on evenness alone. It derives the relative-entropy rate formula in `source-snapshots/pr59/proof.md:261` through `source-snapshots/pr59/proof.md:273`, then differentiates in `s=t^2` and uses normalization of the one-step conditional to remove the `s`-linear term in `source-snapshots/pr59/proof.md:275` through `source-snapshots/pr59/proof.md:291`. This is the same accepted cancellation mechanism as `source-snapshots/accepted_main/research/I05-DPP-21-20260909/finite_range_local_theorem.md:343` through `source-snapshots/accepted_main/research/I05-DPP-21-20260909/finite_range_local_theorem.md:377`.

The analytic division by `t^2` is justified by the even analytic expansion and the vanished quadratic coefficient, yielding `Psi` in `source-snapshots/pr59/proof.md:293` through `source-snapshots/pr59/proof.md:300`. The constant-centered radial theorem then gives the exact margin `Psi(0,t)<=-16 lambda_k` on the prescribed compact interval in `source-snapshots/pr59/proof.md:304` through `source-snapshots/pr59/proof.md:321`. Continuity on the compact set `{0}x[-T,T]` gives one transverse center radius in `source-snapshots/pr59/proof.md:323` through `source-snapshots/pr59/proof.md:329`. The final correction has second derivative `8 lambda_k t^2`, so the corrected function is concave, and strict Jensen concavity of `h` follows after subtracting the strictly convex quartic correction in `source-snapshots/pr59/proof.md:331` through `source-snapshots/pr59/proof.md:343`.

The accepted PR34 theorem is stated for a bounded symbol `f` and its radial parameter, but its correction is scale-invariant under replacing `f-p` by a nonzero scalar multiple. Therefore it applies to the constant-centered line `mu+t g` over its feasible interval with coefficient `(4/3)|g_hat(k)|^4`, as summarized in `source-snapshots/pr59/sources.md:11` through `source-snapshots/pr59/sources.md:19`.

## Claim 2: Arbitrary-Center RPF Hessian

Status: `CORRECT`

The frozen statement gives the exact five-term identity in `source-snapshots/pr59/frozen_statement.md:72` through `source-snapshots/pr59/frozen_statement.md:105`. The proof defines the normalized transfer operator, centered projection, resolvent, entropy observable, and Poisson solution in `source-snapshots/pr59/proof.md:400` through `source-snapshots/pr59/proof.md:437`. The notational typo in the displayed definition is resolved by the operative frozen definitions and clarification in `source-snapshots/pr59/clarifications.md:64` through `source-snapshots/pr59/clarifications.md:83`.

The linear-response identity is correctly derived from `nu L=nu` and `(I-L)RA=Pi A` in `source-snapshots/pr59/proof.md:421` through `source-snapshots/pr59/proof.md:427`. The derivatives of `B=-L phi`, including the local Fisher term `-L(psi^2)`, are retained in `source-snapshots/pr59/proof.md:439` through `source-snapshots/pr59/proof.md:446`. Differentiating the Poisson equation and using `R(LA)=RA-Pi A` gives the two response terms and the final `-nu(psi^2u)` term in `source-snapshots/pr59/proof.md:448` through `source-snapshots/pr59/proof.md:476`.

I checked the displayed derivation step by step at the natural-language algebra level, without running the author script, and found the coefficients and signs consistent. The formula is a proof identity for any compact strict normalized Holder `g`-function chord satisfying the stated RPF hypotheses; it is not itself a curvature sign theorem.

The sufficient norm bound in `source-snapshots/pr59/proof.md:478` through `source-snapshots/pr59/proof.md:495` is correctly one-sided and is not promoted to a universal sign result.

## Claim 3: Finite-State True-Rate Error Interface

Status: `CORRECT`

Section 7 claims a qualitative, exponentially accurate finite-state transfer approximation for compact strict `A_beta` chords, not an executed interval certificate. The finite-future conditionals and their first two derivatives are asserted to converge in one weaker Holder norm in `source-snapshots/pr59/proof.md:497` through `source-snapshots/pr59/proof.md:504`. The common spectral contour and resolvent convergence appear in `source-snapshots/pr59/proof.md:506` through `source-snapshots/pr59/proof.md:510`, and substitution into the five-term Hessian gives the volume-independent error interface in `source-snapshots/pr59/proof.md:513` through `source-snapshots/pr59/proof.md:528`.

This is enough for the claimed interface because Lemma 2.2 has already established the volume-uniform conditional approximation and RPF rate formula before differentiation. No finite-window curvature sample is used as a rate theorem; the author explicitly says no interval computation was run in `source-snapshots/pr59/proof.md:522` through `source-snapshots/pr59/proof.md:528` and `source-snapshots/pr59/verification.md:117` through `source-snapshots/pr59/verification.md:123`.

The constants in (7.3) are existential. Any future interval certificate based on (7.4) would need C2-style independently frozen inputs: the symbol, interval, conditional depth, spectral-contour bound, directed rounding rules, and the geometric tail constant, as already required in `source-snapshots/pr59/verification.md:198` through `source-snapshots/pr59/verification.md:208`.

## Claim 4: Beam-Splitter Second-Order Obstruction

Status: `CORRECT`

The covariance calculation starts with genuine endpoint kernels and gives the balanced output covariance in `source-snapshots/pr59/proof.md:530` through `source-snapshots/pr59/proof.md:545`. The occupation marginals are both the DPP law with kernel `M`, and the finite classical decomposition of the midpoint gap into output mutual information plus occupation-entropy gain is derived in `source-snapshots/pr59/proof.md:547` through `source-snapshots/pr59/proof.md:566`.

At `u=0`, the output law is a product law. Diagonal sign conjugation on the second layer sends `u` to `-u`, making every complete occupation event even. Since the first nonzero change in the law is order `u^2`, the relative entropy/mutual information is order `u^4`; this proves `i_out''(0)=0` in `source-snapshots/pr59/proof.md:568` through `source-snapshots/pr59/proof.md:594`. The true-rate version is justified by the same strict exponentially local RPF argument after grouping two modes per site in `source-snapshots/pr59/proof.md:575` through `source-snapshots/pr59/proof.md:587`.

The conclusion is correctly negative in scope: nonnegative output mutual information alone cannot determine the quadratic curvature, and von-Neumann entropy inequalities cannot replace the fixed occupation-basis Shannon entropy term. This boundary is stated in `source-snapshots/pr59/proof.md:597` through `source-snapshots/pr59/proof.md:599` and `source-snapshots/pr59/attempts.md:69` through `source-snapshots/pr59/attempts.md:77`.

## Claim 5: Explicit Nonconstant Mean-`1/3` Family

Status: `CORRECT`

The family is defined in `source-snapshots/pr59/proof.md:351` through `source-snapshots/pr59/proof.md:394`. It has a constant center mean `1/3`, odd direction `cos(2 pi theta)/8`, prescribed interval `[-2,2]`, and even nonconstant center perturbation `epsilon cos(4 pi theta)`. The theorem supplies a nonzero amplitude range through the positive radius `rho(beta)`, while the extra pointwise bound gives a simple strict legality margin. The path does not pass through a constant symbol when `epsilon` is nonzero, and the mean places it outside PR39's mean-`1/2` scope.

The recorded exact-family script output is consistent with the displayed constants and correctly says it checks only constants and pointwise margins in `source-snapshots/pr59/output/explicit_family_exact.json:1` through `source-snapshots/pr59/output/explicit_family_exact.json:21`. I did not independently execute or reconstruct that arithmetic in C1.

## Claim 6: Scope and Status Boundaries

Status: `CORRECT`

The author does not infer whole-interval arbitrary-center coverage from mixing or analyticity alone. The failed-route ledger explicitly rejects re-centering at nonzero parameters, analyticity-plus-maximum arguments, differentiating an entropy-deficit lower bound, dropping RPF response terms, pointwise conditional concavity, beam-splitter quantum-entropy substitution, finite-window curvature diagnostics, and endpoint continuation by compactness in `source-snapshots/pr59/attempts.md:5` through `source-snapshots/pr59/attempts.md:93`.

The result summary and frozen statement correctly keep the broader problem incomplete in `source-snapshots/pr59/RESULT.md:62` through `source-snapshots/pr59/RESULT.md:73` and `source-snapshots/pr59/frozen_statement.md:138` through `source-snapshots/pr59/frozen_statement.md:140`.

## C2 / Independent-Execution Boundary

No load-bearing finite certificate is required for Theorem CT as reviewed here; its proof is analytic and imports accepted theorem inputs.

The two recorded checker outputs remain author-generated exact certificates. If C2 is asked to reconstruct them, the exact objects are:

- `source-snapshots/pr59/code/check_explicit_family.py`: rational check of the displayed family constants, radial legality interval, quartic coefficients, and the elementary `|epsilon|<=1/24` pointwise margin. It does not compute DPP entropy, curvature, an RPF operator, or an entropy rate.
- `source-snapshots/pr59/code/check_rpf_hessian.py`: symbolic check for the finite-memory normalized conditional family `P_t(X_0=1|X_1=0)=1/3+t/20`, `P_t(X_0=1|X_1=1)=2/3-t/30`, verifying that the five-term RPF Hessian equals the direct second derivative of `nu_t(B_t)` in that finite model. It is not a proof of Theorem CT or a DPP curvature computation.

## Final Status Table

| Claim | Status | Notes |
| --- | --- | --- |
| Packet/source binding | `CORRECT` | 14-file frozen packet read; accepted-main cache used only for inherited theorem scope. |
| Compact radial-tube theorem | `CORRECT` | Valid under accepted PR53 analytic/RPF input and accepted PR34 constant-centered radial quartic margin. |
| RPF Hessian identity | `CORRECT` | Five-term formula retains Fisher, acceleration, and stationary response terms. |
| Finite-state true-rate interface | `CORRECT` | Qualitative exponential interface accepted; no interval certificate executed. |
| Beam-splitter obstruction | `CORRECT` | Mutual information is quartic at midpoint; occupation-entropy gain remains the missing term. |
| Explicit mean-`1/3` family | `CORRECT` | Nonconstant center range is existential through `rho`; static output is author arithmetic only. |
| Broader whole-interval/arbitrary-center claims | `CORRECT` | Correctly marked incomplete, not promoted by this PR. |
