# PR77 FIRST mathematical review

Verdict: `NEEDS_FIX` for any public acceptance of the frozen PR77 theorem packet as certified. There are two finite-certification reasons. First, under the assigned C1 source-only rules, independent finite certificate evidence is `PENDING_C2`; this is not an author error and not a refutation. Second, the submitted frozen evidence package has real auditability defects: the PASS outputs are abbreviated and the point-curvature run is missing from the run record. The static analytic bridges are mostly `ACCEPTED_SCOPED`, while the added Section 9 true-rate beam-splitter bridge is `INCOMPLETE_BRIDGE`; the whole-interval curvature theorem remains correctly `INCOMPLETE`.

Novelty: `NOT_ASSESSED`.

Formal verification: `NOT_PERFORMED`.

Arithmetic/computation: `NOT_PERFORMED` by this reviewer. Claims explicitly marked `PENDING_C2` require the C2 gate at the end of this report; small finite identities checked by ordinary source review are noted separately.

## Analytic proof gates

These gates are the non-finite-computation parts I could check in C1.

1. Legal-symbol gate: `ACCEPTED_SCOPED`. The quadratic reduction gives the strict pointwise symbol margin and therefore strict finite Toeplitz contractions on the frozen interval (`source-snapshots/pr77/proof.md:15-54`).
2. Complete-event gate: `ACCEPTED_SCOPED`. The signed complete-event determinant, Schur conditional, and first two derivative formulas retain the event-matrix dependence (`source-snapshots/pr77/proof.md:56-93`), consistently with the accepted complete-event bridge (`source-snapshots/accepted_inputs/research/I05-DPP-21-20260909/proof.md:62-92`).
3. True-rate tail gate: `ACCEPTED_SCOPED` modulo exact rational constants. The proof uses complete-word uniform inverse decay, the martingale conditional-entropy limit, and the binary relative-entropy bound in the correct direction (`source-snapshots/pr77/proof.md:95-258`).
4. RPF/linear-response gate: `ACCEPTED_SCOPED`. The load-bearing external hypothesis is not merely "Ruelle theory exists"; the needed premise is a positive normalized Holder `g`-function on the finite-alphabet full shift, with a spectral gap and holomorphic eigenmeasure in a fixed Holder space. The accepted input states this exact theorem shape (`source-snapshots/accepted_inputs/research/I05-DPP-21-20260909/finite_range_local_theorem.md:305-325`). PR77 supplies the fixed-path side by strict conditional positivity, exponential future-tail variation, and Cauchy derivative control (`source-snapshots/pr77/proof.md:213-220`, `source-snapshots/pr77/proof.md:243-255`, `source-snapshots/pr77/proof.md:405`).
5. Curvature-tail interface gate: `ACCEPTED_SCOPED` modulo exact derivative constants. The proof keeps the derivative of the event weights, conditional acceleration, and the full `p''/p` contribution (`source-snapshots/pr77/proof.md:407-538`).

The gates above do not certify the strict midpoint or point-curvature numerical inequalities. Those require C2. A C2 requirement caused by this review's no-execution scope is classified as `PENDING_C2`; a missing raw output, mismatched run record, or non-reproducible certificate package is classified as `NEEDS_FIX`.

## Claim-by-claim audit

### 1. Fixed path and strict legality

Status: `ACCEPTED_SCOPED`.

Claim audited: for

`f_t(theta)=1/2+(1/4)cos(4 pi theta)+(t/8)cos(2 pi theta)`,

the path is legal for `|t|<=3/2`, with `119/512 <= f_t <= 15/16` and `min(f_t,1-f_t)>=1/16`.

Reason: the proof rewrites with `x=cos(2 pi theta)` as `1/4+x^2/2+(t/8)x`, then uses the interior minimum and endpoint maximum (`source-snapshots/pr77/proof.md:15-38`). This proves the pointwise symbol margin. The finite-compression spectral contraction follows from the standard Toeplitz quadratic-form comparison with the symbol bounds (`source-snapshots/pr77/proof.md:40-54`). This part does not use PR59, matching the declared scope (`source-snapshots/pr77/README.md:26-28`, `source-snapshots/pr77/frozen_statement.md:130-132`).

Minimal repair: none for this scoped claim.

### 2. Complete-event conditional formula and derivative interface

Status: `ACCEPTED_SCOPED`.

Claim audited: the finite future conditional has the Schur form

`q_r=1/2-b_r^T M_r^{-1}b_r`

and the displayed first and second derivatives retain the event-matrix response.

Reason: the event matrix definition, signed determinant convention, and Schur complement are stated at `source-snapshots/pr77/proof.md:56-82`; the derivative formulas use `R'=-RAR` and `b'_r=d` at `source-snapshots/pr77/proof.md:84-93`. I found no missing event class or dropped derivative term in the displayed formulas. This also agrees with the accepted complete-event signed determinant framework supplied in `source-snapshots/accepted_inputs/research/I05-DPP-21-20260909/proof.md:62-92`.

Minimal repair: none for the symbolic formula. C2 still has to verify the finite-event implementation literally realizes this formula.

### 3. Configuration-uniform inverse and entropy-rate tail

Status: `ACCEPTED_SCOPED` for the analytic structure; `PENDING_C2` for exact constants.

Claim audited: the comparison matrix gives uniform inverse decay, a complete-word conditional error bound, and the true-rate entropy tail

`0<=h_r(t)-h(f_t)<=(256/15)C0^2 rho^(4r-12)`.

Reason: the M-matrix comparison, nonnegative inverse, exponential supersolution, near/far Schur propagation, and Cauchy derivative bounds are stated at `source-snapshots/pr77/proof.md:95-220`. The entropy-rate passage uses martingale convergence, the conditional relative-entropy identity, and the binary chi-square bound with the `1/16` margin at `source-snapshots/pr77/proof.md:222-258`. The logic is sound as an analytic bridge once the rational residuals and constants are confirmed.

Independent evidence pending: the constants in `source-snapshots/pr77/proof.md:125-152` and `source-snapshots/pr77/proof.md:174-209` are exact rational inequalities. The submitted `source-snapshots/pr77/output/analytic_constants_exact.json:1-24` records PASS but is author output. C1 did not independently recompute those rational identities by design. This is a C2 finite-arithmetic obligation, not a text-level mathematical defect and not theorem falsity.

Minimal repair: provide an independent rational reconstruction of the supersolution residuals, propagation constants, and advertised `C0` inequality, with raw exact values and code hash.

### 4. Fixed true-rate midpoint Jensen theorem

Status: `PENDING_C2` for independent finite evidence; `NEEDS_FIX` for the frozen evidence package.

Claim audited:

`h(f_1)-[h(f_{1/2})+h(f_{3/2})]/2 > 1/10000`.

Reason: the analytic direction from the finite conditional certificate to the true rate is correct: the midpoint lower bound subtracts the tail, while the endpoint upper bounds use `h<=h_18` (`source-snapshots/pr77/proof.md:302-315`). The submitted certificate code enumerates exact signed integer determinants, checks positivity and normalization, widens decimal logarithms, and tests the strict threshold (`source-snapshots/pr77/code/certify_midpoint_rate_gap.py:207-241`, `source-snapshots/pr77/code/certify_midpoint_rate_gap.py:244-281`, `source-snapshots/pr77/code/certify_midpoint_rate_gap.py:310-355`).

Independent evidence pending: the truth of the strict numerical inequality is carried by the exact finite enumeration and directed logarithm certificate. This C1 review did not execute arithmetic and cannot independently certify the PASS by scope.

Evidence-package defect: the frozen output summary records the method and PASS status but not the raw interval values, event counts, determinant histograms, tail decimal, or final margin (`source-snapshots/pr77/output/midpoint_rate_certificate.json:1-16`). That packaging issue must be fixed for public certification.

Minimal repair: C2 must independently reconstruct every complete event at depths 18 and 19 for `t=1/2,1,3/2`, use rigorous outward logarithm intervals, apply the tail in the correct direction, and publish raw interval evidence showing the strict margin above `1/10000`.

### 5. Poisson/RPF response identity

Status: `ACCEPTED_SCOPED`.

Claim audited: for a positive normalized one-sided complete-event `g`-function,

`h'=-nu(psi v)`

and

`h''=-nu(psi^2)+nu((psi^2-xi)v)-2nu(psi R(psi v))`,

with the equivalent correlation expansion retaining acceleration and invariant-measure response.

Reason: the normalization identities are stated at `source-snapshots/pr77/proof.md:323-342`. The linear-response calculation from `nu L=nu`, the Poisson equation, the derivative of `v`, and the Hessian formula are derived at `source-snapshots/pr77/proof.md:344-387`; expanding the resolvent gives the correlation form at `source-snapshots/pr77/proof.md:389-405`. I checked the signs and the `n=0` resolvent contribution: combining it with `nu((psi^2-xi)v)` gives the displayed `-nu((xi+psi^2)v)` term in the correlation form. No Fisher, acceleration, or invariant-measure term is discarded.

Use of accepted input: the RPF/spectral-gap hypothesis is the accepted positive normalized Hölder `g`-function machinery summarized in `source-snapshots/accepted_inputs/research/I05-DPP-21-20260909/finite_range_local_theorem.md:305-325`. PR77 verifies the fixed-path positivity and exponential Hölder control by the complete-event bounds at `source-snapshots/pr77/proof.md:213-220`, `source-snapshots/pr77/proof.md:243-255`, and `source-snapshots/pr77/proof.md:405`.

Minimal repair: none for the identity. Do not promote the identity to a sign theorem; the author correctly says the remaining mathematical issue is the sign (`source-snapshots/pr77/proof.md:403-405`).

### 6. Finite-memory curvature remainder and derivative-limit scope

Status: `ACCEPTED_SCOPED` for the interface; `PENDING_C2` for any finite curvature certificate using it.

Claim audited: the conditional-mutual-information increments satisfy a summable second-derivative tail bound, so a finite `h_R''` interval plus the explicit tail can certify true-rate curvature.

Reason: the proof defines `d_r=h_r-h_{r+1}` as a conditional mutual information and writes it as a complete-event sum at `source-snapshots/pr77/proof.md:407-430`. It then gives uniform bounds for `q_r`, `q_r'`, `q_r''`, binary-entropy derivatives, event scores, and the final summable estimate at `source-snapshots/pr77/proof.md:432-538`. The differentiation of `E[p_t D_t]` keeps the `D''`, score times `D'`, and `p''/p` terms; I found no dropped acceleration term.

Independent evidence pending: exact derivative constants and any finite `h_R''` computation are arithmetic obligations. The interface is acceptable, but it does not certify a sign until C2 supplies independent finite conditional curvature intervals plus the closed tail.

Minimal repair: C2 must independently verify the derivative constants, score bounds, polynomial-geometric tail sums, and the final interval addition for any claimed point or interval sign.

### 7. Three point-curvature claims

Status: `PENDING_C2` for independent finite evidence; `NEEDS_FIX` for the frozen evidence package.

Claim audited:

`h''(1/2)<-1/2500`, `h''(1)<-1/1000`, and `h''(3/2)<-1/500`, plus the same negative-parameter statements by evenness.

Reason: the analytic point-specific tail method is structurally consistent. The file distinguishes finite conditional curvature from `H_n/n`, defines exact event jets, and adds point-specific Cauchy/tail bounds (`source-snapshots/pr77/point_curvature.md:23-73`, `source-snapshots/pr77/point_curvature.md:74-215`). The code builds exact determinant value/first/second jets and forms finite conditional curvature intervals plus the geometric tail (`source-snapshots/pr77/code/certify_point_curvatures.py:53-146`, `source-snapshots/pr77/code/certify_point_curvatures.py:161-213`, `source-snapshots/pr77/code/certify_point_curvatures.py:216-320`, `source-snapshots/pr77/code/certify_point_curvatures.py:389-463`). The negative-parameter transfer follows from the diagonal gauge/evenness already stated for this fixed path (`source-snapshots/pr77/point_curvature.md:21-21`, `source-snapshots/accepted_inputs/research/I05-DPP-21-20260909/finite_range_local_theorem.md:71-78`).

Independent evidence pending: the point claims are certificate-driven, and C1 did not run arithmetic by scope.

Evidence-package defect: the frozen point-curvature certificate is a PASS summary without raw intervals or tails (`source-snapshots/pr77/output/point_curvature_certificate.json:1-21`). The run record does not list the point-curvature script among recorded executions (`source-snapshots/pr77/output/run_record.json:8-23`), although `point_curvature.md` says the recorded execution exited zero (`source-snapshots/pr77/point_curvature.md:218-224`). The point claims therefore cannot be accepted from the frozen packet alone.

Minimal repair: add independent C2 evidence for all three points: exact event jets for lengths 18 and 19, independent small-jet checks, directed log/Fisher/acceleration intervals, point-specific rational tail constants, final true-curvature intervals, and a corrected run record.

### 8. Fisher projection and adjacent-pair lower bound

Status: `ACCEPTED_SCOPED` for the projection argument and the simplest finite identities; `PENDING_C2` for the full exact covariance polynomial and advertised uniform rational bound if used quantitatively.

Claim audited: the adjacent-pair statistic gives a nonzero lower bound on the full conditional Fisher rate but does not sign the full curvature formula.

Reason: the Cauchy-Schwarz projection is standard: differentiating `E_t T_n` gives covariance with the full finite score, hence the Fisher lower bound (`source-snapshots/pr77/fisher_projection.md:7-47`). I also checked the adjacent-pair mean and derivative in ordinary analytic source review: the two-point determinant gives `m(t)=1/4-u^2` and `m'(t)=-t/128` as stated (`source-snapshots/pr77/fisher_projection.md:18-31`). The variance identity `c_0=Var(Z_0)` and the three-consecutive determinant example for `c_1` are likewise consistent with the displayed formulas (`source-snapshots/pr77/fisher_projection.md:48-68`). The identification with the true conditional Fisher rate keeps the full chain-rule score, uses one-sided conditional scores as reverse martingale differences, and treats the finite-boundary remainder as bounded (`source-snapshots/pr77/fisher_projection.md:95-131`). The file correctly does not replace the full Fisher term or discard acceleration and response terms (`source-snapshots/pr77/fisher_projection.md:167-177`).

Independent evidence pending for exact quantitative use: the four-site determinant factorization for `c_2`, the separated-pair contribution for `c_3`, the assembled variance polynomial, and the final interval bound `nu_t(psi_t^2)>=16/286141` are exact finite determinant/rational algebra (`source-snapshots/pr77/fisher_projection.md:70-93`, `source-snapshots/pr77/fisher_projection.md:133-165`). I did not find a textual algebra defect, but C1 did not execute an independent exact reconstruction. Treat the qualitative projection and checked simple identities as accepted, and the advertised final rational constant as `PENDING_C2` if it becomes load-bearing.

Minimal repair: independently reconstruct the adjacent-pair covariance determinants and the asymptotic variance polynomial, then record exact rational evidence for the bound.

### 9. Beam-splitter comparison

Status: finite block `ACCEPTED_SCOPED`; true-rate second-order statement `NEEDS_FIX` / `INCOMPLETE_BRIDGE` as a report-completeness supplement.

Claim audited: the balanced fermionic beam splitter gives the doubled covariance, the occupation marginals at the midpoint, the decomposition into output mutual information plus occupation entropy gain, and the second-order observation that `I_out` starts at fourth order.

Finite-block ruling: the finite covariance transform and marginal statement are consistent with the quasifree beam-splitter construction (`source-snapshots/pr77/proof.md:540-553`) and with the accepted operator bridge for finite kernels (`source-snapshots/accepted_inputs/research/I05-DPP-21-20260909/proof.md:229-307`). For a fixed finite block, the layer-sign conjugation makes complete occupation probabilities even in `u`, so `Q_u-Q_0=O(u^2)`; strict finite positivity then makes finite `I_out(u)=D(Q_u||Q_0)=O(u^4)` (`source-snapshots/pr77/proof.md:555-560`). The finite identity `I_out''(0)=0` follows at this fixed block level.

True-rate gap, added in this final completeness revision: `source-snapshots/pr77/proof.md:548-552` states the decomposition at finite and true-rate levels, and `source-snapshots/pr77/proof.md:562-567` states `I_out''(0)=0` and `E_occ''(0)=-2h''(t_*)`. The frozen Section 9 does not provide a uniform-in-volume fourth-order remainder for `I_out(u)` or an explicit accepted-input bridge applying the one-sided RPF derivative machinery to the doubled beam-splitter output law. A finite-block `O(u^4)` with constants depending on the block does not by itself imply the true-rate second derivative vanishes. This supplement covers only the Section 9 rate-bridge sentence; it is not a retroactive objection to the main midpoint/point certificate route, since Section 9 is explicitly not used to replace the complete-event/RPF proof of those claims.

Minimal repair: either restrict Section 9's second-order statements to finite blocks, or add a true-rate bridge: strict finite-range doubled-process hypotheses, positive normalized one-sided complete-event conditionals, uniform Holder/derivative bounds in `u`, and a justified passage of `I_out(u)=O(u^4)` to the mutual-information rate.

### 10. Scope and non-claims

Status: `ACCEPTED_SCOPED`.

The author correctly preserves the central boundary: no proof of `h''(t)<0` for every `1/2<=|t|<=3/2`, no positive true-rate Jensen counterexample, no PR59 inheritance, and no finite-window sign substitution (`source-snapshots/pr77/README.md:24-28`, `source-snapshots/pr77/README.md:61-67`, `source-snapshots/pr77/RESULT.md:54-68`, `source-snapshots/pr77/frozen_statement.md:130-132`, `source-snapshots/pr77/attempts.md:43-70`).

Minimal repair: keep these boundaries in the public summary after C2, especially if the midpoint and point certificates pass.

## Finite computation gate and C2 handoff

C2 must be independent of the author PASS summaries. It may read the frozen source specification, but it should not rerun the author scripts as its only evidence.

Required C2 inputs:

1. `source-snapshots/pr77/SOURCE_BINDING.json` and the 18 frozen files listed there, all from immutable head `6ebe38dc6503120d47e9d644cfac78cfb43666f5`.
2. The mathematical specifications in `source-snapshots/pr77/frozen_statement.md`, `source-snapshots/pr77/proof.md`, `source-snapshots/pr77/point_curvature.md`, and `source-snapshots/pr77/fisher_projection.md`.
3. The accepted inputs only as supplied in `source-snapshots/accepted_inputs/SOURCE_BINDING.json`; no PR59/PR60 result and no live PR77/PR78 delta.

Required C2 outputs for necessary midpoint/point certification:

1. `c2_binding_audit.json`: exact file list, hashes/blobs checked, source head, and confirmation that no live files were read.
2. `c2_analytic_constants.json`: exact rational residuals, propagation constants, `C0` inequality, entropy derivative constants, score-bound derivation, and geometric-polynomial tail identities.
3. `c2_midpoint_certificate.full.json`: for each of `t=1/2,1,3/2` and lengths 18 and 19, full event count, positivity, normalization, determinant/weight summary sufficient to audit `H_n`; outward `H_18`, `H_19`, `h_18` intervals; exact `E_18`; final lower interval for the Jensen expression; and a separately recorded positive lower bound for `JensenLower-1/10000`.
4. `c2_point_curvature_certificate.full.json`: for each of `t=1/2,1,3/2` and lengths 18 and 19, full event-jet count, checks that `sum N=32^n` and `sum N'=sum N''=0`, outward `H_n''` and `h_18''` intervals, exact point tail, true-curvature interval, threshold, and a separately recorded positive lower bound for `threshold-trueUpper`.
5. `c2_report.md`: human-readable audit tying every output to the frozen source lines and stating final statuses.

Optional/nonblocking C2 outputs:

1. `c2_fisher_projection_optional.json`, if the Fisher lower bound is to be used quantitatively: exact adjacent-pair covariance determinants, asymptotic variance polynomial, positivity range, and final Fisher lower bound.

Section 9 true-rate bridge note: if the author wants the beam-splitter second-order rate statement retained, that is an author/C3-coordinated analytic delta, not a C2 finite-evidence task, and this review does not start it.

Required C2 acceptance standards:

1. Binding acceptance: all 18 frozen files must match the immutable source binding. Any live-file dependency fails the gate.
2. Event acceptance: every enumerated complete event at required depths must have positive numerator, total event count must be exactly `2^n`, and weighted numerator sum must be exactly `32^n`. Independent signed-determinant and Mobius/inclusion implementations must agree at least through the small-size range claimed by the author, and the depth-18/19 production path must be independently implemented rather than imported from the author scripts.
3. Log-interval acceptance: every `log N` enclosure must be outward and justified. If Python `decimal` is used, record the official `Decimal.ln` contract, Python/libmpdec version, precision, rounding mode, per-log widening, and flag/trap policy. A separate interval-log library is acceptable if it records equivalent proof data.
4. Midpoint acceptance: the published lower interval for
   `lower(h_18(1))-E_18-[upper(h_18(1/2))+upper(h_18(3/2))]/2`
   must be strictly greater than `1/10000`, with a positive outward lower bound for the margin.
5. Point-curvature acceptance: for each of `t=1/2,1,3/2`, the published upper interval for `h''(t)` after adding the exact tail must be strictly below the claimed rational threshold, with a positive outward lower bound for the threshold margin.
6. Run-record acceptance: every claimed generated artifact must appear in the run record with command, environment, source hash, output hash, and exit status; point curvature must not be omitted.

Expected C2 statuses:

- If all raw finite intervals check out: midpoint theorem and three point-curvature claims may be upgraded to `ACCEPTED_SCOPED`; whole-interval curvature remains `INCOMPLETE`.
- If an interval does not prove the required strict threshold, or if reconstruction disagrees with an author output but does not rigorously prove the opposite assertion, the affected claim is `INCONCLUSIVE` / `NEEDS_FIX`.
- Mark a finite assertion `REFUTED` only if independent rigorous evidence proves the corresponding strict assertion false, such as a rigorous upper bound at or below the claimed midpoint lower threshold, a rigorous lower bound at or above a claimed negative-curvature upper threshold, or an exact event reconstruction showing the frozen mathematical object is not the object certified.
- If raw evidence remains absent: keep the affected finite claims at `NEEDS_FIX`.
