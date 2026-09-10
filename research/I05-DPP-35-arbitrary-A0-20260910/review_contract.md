# Independent review contract for PR117

State: **UNCLAIMED / PENDING_REVIEW until an explicit reviewer claim appears.**

Freeze one exact PR117 head before review. No verdict from PR53/82/106/110/113 transfers to the new proof. PR53 is used only for the already accepted regularity-free matching inequality.

## U1 — scope and finite-range truncation

Verify that every strict half-period-even `c in A_0` admits a same-mean half-period-even finite Fourier truncation `c^0` with a uniform strict spectral margin, and that `e_t=c-c^0+t g` can be made arbitrarily small in Wiener norm on a nonempty real parameter interval.

Do not insert a positive weighted Fourier moment.

## U2 — complete-event reference inverses

For every finite complete word reproduce the coercive estimate

`||(T_Lambda(c^0)-I_Z)^(-1)|| <= delta_0^(-1)`.

Then verify the finite-band inverse expansion and obtain an event- and volume-uniform exponential off-diagonal bound. Check the indefinite Hermitian sign carefully: positivity of `T(c^0)-I_Z` is not assumed.

## U3 — configuration-local inverse approximation

Audit the construction of `R^[R]` from local complete-event submatrices. Reproduce a uniform operator error

`||R^0-R^[R]|| <= C exp(-aR)`

by the resolvent identity and boundary propagation. Verify that the localized entries depend only on complete-event bits near their endpoints.

Use `support_count_correction.md` as authoritative: a safe support bound is `C m^2(R+1)`. The earlier sharper `O(mR)` line is not required.

## U4 — non-product reference trace-log

For every complete word reproduce

`p_t(x)=p_0(x) det(I+R_x^0 E_t)`.

Check positivity/branch selection and the operator contraction. In particular, confirm that trace-log convergence uses only

`||R_x^0||_(2->2) ||E_t||_(2->2) < 1`

and not an unproved common `ell^1` inverse envelope.

The `m=1` term is present and must not be dropped.

## U5 — full complete-event derivatives

Reproduce for `q<=4`

`|partial_t^q p_J,t(x)| <= p_J,t(x) A_q |J|^q`.

Check that summation over complete atoms retains rare events and that the finite Shannon Hessian contains both Fisher and acceleration terms. No event subset or inclusion probability may replace the complete law.

## U6 — localized trace derivative majorant

Expand `E_t` into partial shifts using the absolutely summable Fourier coefficients. For fixed displacement tuple, verify the operator-norm product localization and shell bound. Then combine the corrected support cardinality with U5.

A sufficient target bound is the deliberately coarse form

`C_q m^(3q+1) B^(m-1) eta^(m-q) (1+||g||_W)^q`.

Check summability in localization radius, displacements, and walk length under `B eta<rho<1`. Physical displacement magnitudes must not enter the Bell support cost.

## U7 — thermodynamic/differentiated limit for relative KL

Check the order of limits:

1. fixed walk length/displacements/localization radius and volume limit;
2. localization shells;
3. displacement sums;
4. walk length.

Verify local uniform convergence through derivative order four of

`|Lambda|^(-1) D(p_Lambda,t || p^0_Lambda)`.

## U8 — fixed-reference cross entropy

For the finite-range reference DPP, reproduce the exponentially convergent one-sided complete-event conditional and uniform nonnullness. Decompose `phi_0=log G_0` into exponentially small cylinder shells.

Use the complete-event Bell bound to justify four derivatives of `E_t phi_0` and check that the finite chain-rule boundary discrepancy and its differentiated expectations are `O(1)` before division by volume.

## U9 — true entropy identification

From the exact finite identity

`D(p_t||p_0)=-H(p_t)-E_t log p_0`

verify

`h(c+t g)=-d_0(t)-ell_0(t)`

and `C^4` regularity. Confirm that this is classical complete-configuration Shannon entropy, not spectral entropy.

## U10 — parity/matching curvature step

Verify fixed parity marginals, independence at `t=0`, complete-law evenness, and

`J(t)=h(c)-h(c+t g)>=0`.

Bind the exact accepted PR53 matching coefficient and check both curvature cases `J''(0)>0` and `J''(0)=0`. Confirm the coefficient

`alpha_k=|g_hat(k)|^4/[8 mu^2(1-mu^2)]`.

## U11 — source/failure boundary

Read `source_and_failure_audit.md`. Confirm that unweighted inverse-closedness is not used to assert norm-controlled inversion and that the first-checkpoint `ell^1`-envelope-times-tail route is explicitly superseded.

A failure of U3/U6/U8 is a failure of the current proof, not an entropy counterexample.

## Verdict discipline

If the earliest load-bearing failure is found, stop dependent conclusions and report the exact equation, whether repair is local/fatal, and the last passing unit. If all units pass, the strongest possible mathematical status is `ACCEPTED_SCOPED` for the exact arbitrary-strict-`A_0` local theorem. Keep mathematical review, source verification, machine evidence (none), novelty, and general real-kernel concavity separate.