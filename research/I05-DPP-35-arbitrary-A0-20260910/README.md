# I05-DPP-35 — arbitrary strict `A_0` center via finite-range complete-event preconditioning

Status: **PROVED AS AN AUTHOR THEOREM / PENDING FINAL INDEPENDENT DELTA/CROSS-REVIEW.**

This is a successor to PR113. It started from `main@bcbf7016e2abc6401b66f39ac9202d235ee32fad` and does not alter predecessor sources. No older verdict transfers automatically.

## Theorem

Let real `c,g in A_0` satisfy

- `c(theta+1/2)=c(theta)`;
- `g(theta+1/2)=-g(theta)`, `g!=0`;
- `delta <= c <= 1-delta` a.e. for some `delta>0`.

Put `mu=c_hat(0)`. For every odd `k` with `g_hat(k)!=0`, there exists `epsilon>0` such that the true stationary DPP complete-configuration Shannon entropy rate for the physical affine path

`K_t=T(c)+t T(g)`

satisfies concavity of

`h(c+t g)+|g_hat(k)|^4 t^4/[8 mu^2(1-mu^2)]`

on `[-epsilon,epsilon]`, with strict negative second derivative away from zero after shrinking the interval.

Every complete occupied/vacant event is retained. Fisher, atom acceleration, and thermodynamic response remain inside the exact complete-law differentiation. No spectral/von-Neumann entropy is substituted.

## Authoritative proof order

The initial checkpoint version of this README contained two exploratory claims that are now explicitly superseded: a common inverse-`ell^1`-envelope contraction and an `O(mR)` local-support count. Neither is part of the final proof.

Read the mathematical chain in this order:

1. `arbitrary_A0_C4_proof.md` — finite-range reference factorization, localization, relative-KL and reference-cross-entropy `C^4` bridge;
2. `support_count_correction.md` — authoritative safe support count `O(m^2 R)` and corresponding polynomial-in-`m` correction;
3. `operator_vs_absolute_sum_audit.md` — authoritative separation between signed operator trace-log convergence and the later absolute localized/displacement sums, including the fixed-center-tail quantifier order;
4. `arbitrary_A0_concavity.md` — parity mutual information, accepted matching floor, and the quadratic/quartic two-case curvature proof;
5. `source_and_failure_audit.md` — corrected source scope and failure ledger;
6. `review_contract.md` — independent audit units.

## Final preconditioning mechanism

Choose a half-period-even finite Fourier truncation `c^0` of the fixed strict `A_0` center, with the same mean, and write

`r=c-c^0`, `e_t=r+t g`.

For every finite complete word `x`,

`M_x^0=T(c^0)-I_{Z_x}`, `R_x^0=(M_x^0)^(-1)`.

Complete-event coercivity gives the event/volume-uniform operator bound

`||R_x^0||_{2->2} <= delta_0^(-1)`.

Because `M_x^0` is finite-band Hermitian with a uniform two-sided spectral gap, the elementary geometric inverse expansion gives event/volume-uniform exponential off-diagonal decay and exponentially accurate configuration-local approximants `R_x^[R]`.

The exact atom factorization is

`p_t(x)=p_0(x) det(I+R_x^0 T(e_t))`.

Two estimates are deliberately separated.

### A. Signed trace-log existence

The series for `log det(I+R_x^0 T(e_t))` exists from the operator inequality

`||R_x^0 T(e_t)|| <= delta_0^(-1)||e_t||_W < 1`.

This alone is **not** used to claim absolute convergence of a spatially expanded walk sum.

### B. Absolute localized/displacement domination

After replacing inverse factors by configuration-local approximants, normalized trace products are bounded using only

`B := sup ||R_x^[R]||_{2->2} <= delta_0^(-1)+1`.

The inverse family is not assigned a common `ell^1` diagonal-envelope norm in the final proof. The Toeplitz perturbations alone are expanded into shifts; absolute displacement summation pays only

`sum_d |e_t(d)| = ||e_t||_W`, `sum_d |g_hat(d)|=||g||_W`.

The safe localized support cardinality is

`|J| <= C m^2(R+1)`,

independent of the magnitudes of the Fourier displacements. Complete-event Bell differentiation therefore adds only polynomial factors. For fixed derivative order `q<=4` the coarse length bound is

`C_q m^(3q+1) B^(m-1) eta^(m-q)(1+||g||_W)^q`,

where `eta=sup_|t|<=tau ||e_t||_W`.

The geometric constant after absolute summation is `B eta`, with `B` an **operator-norm** bound, not an inverse `ell^1` norm.

## Quantifier order for the center tail

Shrinking `t` cannot shrink the frozen center tail. The proof uses the following order.

1. Given `c` and its strict margin `delta`, choose the finite truncation so far out that `epsilon_0=||c-c^0||_W<delta/2` and, with `delta_0=delta-epsilon_0`,
   `B epsilon_0<1/4`, where `B=delta_0^(-1)+1<=2/delta+1`.
2. Freeze that truncation and all of its localization constants.
3. Only then choose `tau>0` so that `B tau ||g||_W<1/4`.
4. Hence `B eta<1/2` on the fixed interval.

Thus arbitrary slow Wiener tails are allowed; there is no attempt to repair a fixed uncontrolled `B*tail` by shrinking `t` afterward.

## Source correction

The initial checkpoint also stated too strongly that the unweighted `p=1` BGS algebra lacks norm-controlled inversion in `B(ell^2)`. That literature statement is withdrawn. Fang--Shin (2020) explicitly recalls Baskakov norm-control results in the classical `p=1`, `ell^2` BGS setting.

This correction is non-load-bearing: PR117 neither needs nor establishes a BGS norm-control theorem for the complete-event family. The final proof uses the direct finite-range-reference operator/localization argument above. See `source_and_failure_audit.md` for the corrected exact source boundary.

## Review state

At author head `7a960926e44f2a81ea43ba2c35e3d7534e76bad5`, S3 fresh SECOND independently audited the seven-file mathematical packet and returned `CORRECT_WITHIN_SCOPE`, including the operator-vs-absolute-sum transition, corrected support count, complete-event Bell bounds, `C^4` thermodynamic passage, and parity/matching curvature step. That SECOND also found the non-load-bearing BGS source wording error corrected after its freeze.

S1 FIRST had separately frozen the same mathematical head. The present README/source blobs are later author source corrections and therefore require an exact delta/cross-review before any integration claim. No acceptance is inherited merely from the earlier frozen-head reports.

## Nonclaims

No whole-legal-interval result, arbitrary measurable-symbol result, general finite real-kernel concavity theorem, entropy counterexample, analytic entropy-rate theorem, or novelty claim is made. Failure or non-use of an inverse/response method is not an entropy counterexample.