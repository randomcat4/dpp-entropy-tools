# PR77 independent second mathematical review

## Verdict

The analytic interface is mostly sound, but the submitted frozen source is not a complete independently certified proof package under this review's constraints.

The fixed legality proof is CORRECT. The complete-event conditional formulas, Schur derivative formulas, comparison-inverse mechanism, true-rate tail interface, normalized RPF/Poisson response formula, finite-to-rate Fisher projection argument, and finite-block beam-splitter identity are CORRECT as analytic reductions, within the accepted complete-event/RPF machinery.

The midpoint Jensen theorem, the three point-curvature threshold claims, and the quantitative Fisher covariance lower bound remain CRITICAL_GAPS for independent acceptance here because the finite exact constants and directed logarithm/determinant computations require separate C2 raw artifacts. The author PASS summaries are useful provenance but not independent certification.

The whole continuum claim `h''(t)<0` for `1/2<=|t|<=3/2` remains CRITICAL_GAPS/INCOMPLETE, and the source correctly does not claim it. The chord result, six isolated curvature signs by evenness, and the Fisher projection do not imply the continuum sign.

Novelty: NOT_ASSESSED. Formal verification: NOT_PERFORMED.

## Unit statuses

| Unit | Status | Reason |
| --- | --- | --- |
| Fixed legality of `f_t` for `|t|<=3/2` | CORRECT | The quadratic reduction in `input/proof.md:15`-`38` proves `119/512<=f_t<=15/16`; the compression bound follows from the scalar symbol margin. |
| Complete events and Schur conditional derivatives | CORRECT | The signed event matrix and Schur formula in `input/proof.md:56`-`93` are algebraically consistent, including `q_r'` and `q_r''`. |
| Uniform inverse decay and conditional tail form | CORRECT as an analytic interface; C2 needed for constants | The comparison M-matrix argument in `input/proof.md:95`-`220` is structurally valid. The exact residuals and strict rational inequalities are numerical certificate obligations. |
| True-rate limit before derivatives | CORRECT | `input/proof.md:222`-`258` uses decreasing finite-future conditional entropy and the binary relative-entropy identity before invoking derivative tails. |
| Midpoint true-rate Jensen gap | CRITICAL_GAPS pending C2 | The implication from (5.5) and (6.6) is correct (`input/proof.md:260`-`317`), but this review did not certify the depth-18 determinant/logarithm arithmetic or the `>1/10000` margin. |
| RPF/Poisson response identity | CORRECT | The normalized transfer-operator derivation in `input/proof.md:319`-`405` keeps Fisher, acceleration, and invariant-measure response terms with consistent signs. |
| CMI derivative-tail interface | CORRECT as an analytic interface; C2 needed for constants | The Bregman and score-tail derivation in `input/proof.md:407`-`538` gives a valid acceptance gate for true-rate curvature certificates. |
| Three fixed point curvatures | CRITICAL_GAPS pending C2 | `input/point_curvature.md:23`-`226` has the right finite conditional curvature plus point-specific tail structure, but the threshold inequalities require independent raw arithmetic. |
| Fisher projection and finite-to-rate score argument | CORRECT analytically; covariance constants pending C2 | `input/fisher_projection.md:7`-`177` gives a valid projection argument from finite Fisher to the true conditional Fisher rate. The exact covariance polynomial is a separate arithmetic artifact. |
| Beam-splitter finite-block identity | CORRECT | The finite identity follows from output marginals and the definition of the occupation entropy gain; see `input/proof.md:540`-`569` and accepted finite bookkeeping in `accepted_input/proof.md:229`-`308`. |
| Beam-splitter true-rate second derivative | CRITICAL_GAPS | The source states the true-rate version in `input/proof.md:548`-`566`, but does not provide a doubled-process rate limit/analytic derivative passage or a uniform tail showing the output mutual-information rate has zero second derivative. |
| Whole continuum sign | CRITICAL_GAPS/INCOMPLETE | The source itself excludes this claim in `input/README.md:61`-`67`, `delta_input/FINAL_RESULT.md:84`-`94`, and `input/proof.md:571`-`575`. |
| Code/output ledger | CRITICAL_GAPS | Several frozen JSON summaries do not match the schemas their frozen scripts would emit, and recorded commands omit output paths needed to create the frozen summary filenames. See `code_review.md`. |

## Mathematical review

### Fixed legality

This part is correct. With `x=cos(2 pi theta)`, `input/proof.md:15`-`18` rewrites

```text
f_t=1/4+x^2/2+(t/8)x.
```

For `|t|<=3/2`, the convex quadratic has its minimum at `x=-t/8`, inside `[-1,1]`, giving `1/4-t^2/128>=119/512` (`input/proof.md:21`-`25`). The maximum is attained at an endpoint and is at most `15/16` (`input/proof.md:27`-`38`). Hence `min(f_t,1-f_t)>=1/16`. The Toeplitz coefficient list in `input/proof.md:46`-`52` is consistent with the Fourier coefficients of the two cosines.

No PR59 tube radius is used or needed.

### Complete-event conditional formula and derivatives

This part is correct. The future event matrix `M_r=K_t|_[1,r]-I_Z` and vector `b_r=(t/16,1/8,0,...)` in `input/proof.md:56`-`73` give the occupied-site Schur complement

```text
q_r=1/2-b_r^T M_r^{-1} b_r.
```

The derivative formulas in `input/proof.md:84`-`90` follow from `R'=-RAR` and `b'=d`. They include the derivative of the event matrix itself and do not freeze the complete future event.

### Inverse decay and true-rate tail

The comparison-M-matrix interface is sound. On the complex `1/8`-neighborhood of `[1/2,3/2]`, `input/proof.md:97`-`123` compares every complete-event inverse to a pentadiagonal M-matrix with diagonal `1/2` and off-diagonal magnitudes `13/128` and `1/8`. The entrywise domination step is valid because the diagonal entries have modulus `1/2` and the off-diagonal entries are bounded by the comparison magnitudes.

The supersolution `rho^|i-j|` and the near/far Schur propagation in `input/proof.md:125`-`220` give the intended configuration-uniform bound

```text
|q_R-q_r| <= C0 rho^(2r-6).
```

I did not independently recompute the rational residuals, the `C0` inequality, or the depth-18 tail values. Those are C2 arithmetic obligations.

### True rate before derivative use

The order of limits is correct. `input/proof.md:222`-`258` first identifies `h_r=H(X_0|X_1,...,X_r)` and uses finite-alphabet martingale convergence to get `h_r downarrow h`. The identity

```text
h_r-h = E d(q_infinity || q_r)
```

is the standard conditional binary relative-entropy identity. The chi-square bound is valid once the conditional probabilities are uniformly bounded in `[1/16,15/16]`, which follows from the strict complete-event DPP margin machinery.

This gives a true entropy-rate error bound, not a trend fit to `H_n/n`.

### Midpoint Jensen certificate

The analytic implication is correct: if the directed depth-18 inequality in `input/proof.md:302`-`308` is independently certified, then the true-rate Jensen gap in `input/proof.md:310`-`315` follows. The midpoint subtracts the tail because `h(f_1)>=h_18(1)-E_18`; the endpoints use `h(f_t)<=h_18(t)`.

This review cannot mark the numerical theorem independently CORRECT. The exact determinant enumeration, decimal log enclosures, and `>1/10000` comparison are not reproduced here and require C2 raw artifacts. The frozen summary `input/output/midpoint_rate_certificate.json` also omits the actual directed interval values, so it is not enough by itself to audit the numerical margin.

### RPF/Poisson response

The response formula is correct under the normalized positive Holder `g`-function assumptions supplied by the accepted machinery and the PR77 complete-event estimates. `input/proof.md:319`-`405` derives

```text
h''=-nu(psi^2)+nu((psi^2-xi)v)-2nu(psi R(psi v)).
```

The signs are consistent: differentiating `h'=-nu(psi v)`, using linear response, and differentiating the Poisson equation gives the displayed formula. Expanding `R=sum L^n Pi` also gives the correlation form in `input/proof.md:395`-`400`, where the `n=0` part changes `nu((psi^2-xi)v)` into `-nu((xi+psi^2)v)`.

The formula is not a sign proof. The source correctly retains the acceleration and invariant-measure response terms (`input/proof.md:403`-`405`).

### Curvature-tail interface

The conditional-mutual-information tail interface is correct as an acceptance gate. `input/proof.md:407`-`538` writes

```text
d_r=h_r-h_{r+1}=I(X_0;X_{r+1}|X_1,...,X_r)
```

and differentiates a Bregman integral for the binary relative entropy. The bounds in `input/proof.md:456`-`498` correctly account for value, first derivative, and second derivative errors of the conditionals. The later score bounds in `input/proof.md:500`-`515` give the polynomial-times-geometric tail required to justify

```text
h''(t)=h_R''(t)-sum_{r>=R}d_r''(t).
```

Again, the exact constants and closed sums are arithmetic certificate material for C2.

### Point-curvature claims

The point-curvature interface in `input/point_curvature.md` is structurally valid. It uses the finite conditional curvature `H_19''-H_18''`, not `H_n''/n` (`input/point_curvature.md:23`-`70`), and gives point-specific complex disks and derivative tails (`input/point_curvature.md:74`-`214`). If the recorded directed upper intervals are independently certified, then the three threshold inequalities follow.

This review cannot certify the actual inequalities

```text
h''(1/2)<-1/2500, h''(1)<-1/1000, h''(3/2)<-1/500.
```

They require independent raw C2 artifacts for event jets, directed logarithms, tail constants, and threshold comparisons. The source correctly states that these isolated points do not prove the continuum sign (`input/point_curvature.md:224`-`226`).

### Fisher projection

The Fisher projection argument is correct analytically. `input/fisher_projection.md:7`-`46` uses the adjacent-pair statistic and finite Cauchy-Schwarz to lower-bound the full finite Fisher information without projecting away events. `input/fisher_projection.md:95`-`131` then identifies the finite Fisher rate with `nu_t(psi_t^2)` through the right-to-left score decomposition and reverse-martingale orthogonality. The bounded boundary remainder argument is plausible and sufficient: summable finite-future score errors leave only an `O(1)` remainder.

The covariance polynomial and uniform bound `16/286141` are exact arithmetic claims and need C2 raw verification. They do not sign the full curvature formula because the acceleration and invariant-measure response terms remain (`input/fisher_projection.md:167`-`177`).

### Beam-splitter comparison

At the finite-block level, the identity is correct. For endpoint kernels `K_{t_*-u}` and `K_{t_*+u}`, the balanced output covariance in `input/proof.md:542`-`546` has both occupation marginals equal to the DPP at `t_*`. Therefore

```text
2H(t_*)-H(t_*-u)-H(t_*+u)=I_out(u)+E_occ(u)
```

is just the decomposition into output occupation mutual information plus the occupation entropy gain.

At the true-rate second-derivative level, the proof is incomplete. `input/proof.md:548`-`566` states the identity at finite and true-rate levels together and then concludes `I_out''(0)=0`. The finite-block `O(u^4)` argument follows from layer-sign conjugation and strict positivity. To pass this to entropy rates and derivatives, the proof still needs a doubled-process version of the complete-event/RPF analytic limit or an explicit uniform finite-to-rate derivative tail for the output law. That passage is not supplied in Section 9.

This gap does not damage the midpoint certificate or point-curvature certificate, because Section 9 is presented as a comparison/obstruction route rather than the source of those numerical claims.

## Minimal repairs

1. Supply C2 raw artifacts for the finite exact constants, depth-18 midpoint margin, three point-curvature thresholds, and covariance/Fisher polynomial. The artifacts should include the actual directed intervals and enough raw integer/rational data to audit them independently.

2. Repair the frozen output ledger so every JSON certificate is either generated by its frozen script with the recorded command, or explicitly marked as a hand-written summary of a separate full output. The current summary files are not schema-consistent with the scripts.

3. For Section 9 true-rate second derivatives, add a doubled-output process proof: define the finite-block output occupation process, prove entropy-rate existence, prove a uniform analytic neighborhood in `u`, and justify differentiating the rate limit to obtain `I_out,rate''(0)=0`.

4. Keep the continuum curvature statement marked incomplete unless an interval certificate includes the explicit true-rate derivative tail from `input/proof.md:407`-`538`. The three point signs, the chord, and the Fisher projection are insufficient by themselves.

