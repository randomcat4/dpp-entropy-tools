# S1 independent review: exact events, phase symmetry, and boundary residuals

Status: `CRITICAL_GAPS` for any claim that the current benchmark gives a positive entropy-rate counterexample.  Status: `CORRECT` for the exact-event determinant semantics, the even-center/odd-direction first-derivative cancellation, the finite entropy parity identity, the M64 boundary residual enclosure, the final n=8 negative rate certificate excluding this one fixed baseline pair, and the two finite-scope phase restriction lemmas.

This review is scoped to the frozen fixed scalar Toeplitz DPP setting.  It is not an audit of the global open status of Lyons-Steif Conjecture 9.2, and it does not certify any entropy-rate sign.

## Public sources used

- Lyons-Steif, "Stationary Determinantal Processes: Phase Multiplicity, Bernoullicity, Entropy, and Domination", arXiv/Duke version: https://arxiv.org/pdf/math/0204324 and HTML mirror https://arxiv.org/html/math/0204324v5.
- Lyons-Steif errata PDF, dated 29 Nov. 2025: https://rdlyons.pages.iu.edu/errata/dyn.pdf.  I checked that it mentions Remark 5.12 and Remark 7.16, with no Section 6.12 entry.

## Rebuilt definition and exact-event determinant

For a positive contraction `Q` on a finite coordinate set, the DPP is defined by inclusion probabilities `det Q[A,A]`.  Exact configurations are not inclusion minors.  For a finite window `W` and exact ones set `A`, the exact probability is the determinant of the matrix whose row `i` is `K[i,*]` if `i in A`, and `I[i,*]-K[i,*]` if `i notin A`.  This is equivalent to the Lyons-Steif inclusion-exclusion determinant formula.

For the scalar stationary symbol with Fourier convention `fhat(k)=int f(x) exp(-2 pi i k x) dx`, I used `K_f(i,j)=fhat(i-j)`.  Swapping to the transposed convention does not change finite exact laws.

## First-derivative cancellation

Claim reviewed: for an even real center and a real odd direction, every finite exact-event probability has `p_A'(0)=0`.

Verdict: `CORRECT`.

Reason: if `f_t=f_0+t u`, with `f_0` even and `u` odd, then `f_{-t}(x)=f_t(-x)`.  Reflection sends the Toeplitz kernel to its transpose/conjugate transpose.  Every inclusion determinant is unchanged by transpose, and exact probabilities are inclusion-exclusion combinations of those determinants.  Hence every exact cylinder probability satisfies `p_A(t)=p_A(-t)`, with no invertibility assumption.  All odd derivatives vanish.

The computation independently checked the first derivative exactly over rationals for every exact event with `n=1..6` for four rational families.  All nonzero counts were zero.  A finite-difference check over all exact events for `n=1..8` had maximum absolute residual below `1.0e-19` for the main benchmark.

## Translation and gauge checks

Translation by `s` multiplies Fourier coefficient `c_k` by a phase linear in `k`; diagonal affine gauge gives the same finite DPP law.  Reflection/conjugation also preserves all finite DPP laws.  A finite set of nonzero Fourier coefficients is translatable to an even real symbol iff there is one angle `theta` with `arg(c_k)+k theta in pi Z` for every active `k`.  Infinitesimally at an even center with nonzero `a_k`, an odd direction is pure translation only if `b_k/(k a_k)` is constant across active harmonics.

For the main benchmark

`p=1/2`, `a=(9/50,-3/25,2/25)`, `b=(1/10,2/25,-3/50)`, `tau=1/4`,

the triangle margin is exactly `3/50`.  The tangent translation ratios are `5/9`, `-1/3`, and `-1/4`, so it is not an infinitesimal translate of the center.  The endpoint evenization residual is about `0.1492844001`; the `1+2-3` cycle phase has distance about `0.1582052962` from `pi Z`.  Thus the benchmark has a genuine multi-harmonic phase invariant, but that alone is not an entropy-rate sign certificate.

Endpoint equality is expected: `f_tau` and `f_-tau` are reflection/conjugate equivalent, so their finite entropies agree exactly up to floating error.  This equality should not be counted as independent evidence for a positive chord.

## Finite-window entropy evidence

The main benchmark finite gaps are negative through `n=12`:

| n | finite gap `(H_-+H_+)/2-H_0` | increment gap |
|---:|---:|---:|
| 8 | `-1.745355115572167e-4` | `-2.612417971548098e-5` |
| 10 | `-2.267839005769545e-4` | `-2.612419527281418e-5` |
| 12 | `-2.790322914076881e-4` | `-2.612419540870548e-5` |

The independent `n<=12` exact-event enumeration matched the route-owner baseline to within `3.38e-14` on finite gaps and `3.29e-14` on increment gaps.  Probability normalization errors were at most `2.11e-15`; no exact-event probability was negative below the `1e-10` threshold.

I also used three controls:

| family | n=12 finite gap | n=12 increment gap | gauge note |
|---|---:|---:|---|
| own rational three-harmonic control | `-1.320326988487608e-4` | `-1.290383558050223e-5` | non-translation |
| one-harmonic phase gauge control | `-5.72211685122781e-4` | `-5.203496791938989e-5` | phase removable |
| translation-tangent three-harmonic control | `-1.945177178974689e-5` | `-1.904858118351172e-6` | infinitesimal translation |

These controls do not prove a pattern.  They are included only to check that the implementation is not blindly tuned to the supplied benchmark.

## Rate-bound direction

For a stationary one-dimensional process, `H_n/n` is an upper bound on the entropy rate, and the finite increments `H_n-H_{n-1}` are also upper bounds converging to the rate.  A positive counterexample for

`Delta = (h(f_-tau)+h(f_tau))/2 - h(f_0)`

requires lower bounds on the endpoints and an upper bound on the center:

`(L_-+L_+)/2 - U_0 > 0`.

The available finite data do the opposite sign, and the coarse route-owner rate interval at `n=12` still straddles zero, roughly from `-0.06089116925` to `0.05929037392`.  Thus the benchmark is currently a negative finite diagnostic, not a candidate positive certificate.

Common failure modes to avoid:

- using inclusion minors `det K[A,A]` as exact-event probabilities;
- treating `p_A'(0)=0` as sign information for the second derivative;
- treating endpoint equality under reflection as a separate data point;
- using a conditional or block upper bound as an endpoint lower bound;
- exchanging a finite-window derivative, a random-order limit, or a Schur-limit construction with the entropy-rate limit without an explicit uniform error argument.

## Final n=8 rate certificate audit

Files audited from frozen author commit `a98811c6597577f73128aaed3fd7dde6169af350`: `rate_certificate_proof.md`, `rational_rate_certificate.py`, `rational_rate_n8.json`, `boundary_residual_proof.md`, `boundary_residual.py`, `boundary_residual_M64.json`, and `baseline_candidate.json`.  I checked that the current local artifact contents match that commit by SHA256 before reviewing them.

Verdict for the stated fixed-pair claim: `CORRECT`.

The certified conclusion is only this:

`(h(f_-1/4)+h(f_1/4))/2 - h(f_0) < 0`

for the single frozen rational degree-three baseline.  It excludes that baseline as a positive counterexample.  It does not prove a family theorem or the Lyons-Steif conjecture.

The exact rational gap enclosure in `rational_rate_n8.json` is

- lower: `-299206482628470082967984166428661599036439 / 11417981541647679048466287755595961091061972992`, about `-2.6204849038956574e-5`;
- upper: `-148727663748433704622488410027642662541253 / 5708990770823839524233143877797980545530986496`, about `-2.605148085166224e-5`.

Both endpoints are strictly negative, so the sign certificate is separated from zero.

The main mathematical chain checks out:

- Conditional negative association gives monotonicity after conditioning on a finite `gamma`; all-one earlier past gives the lower one-site probability and all-zero earlier past gives the upper one.  Passing first through finite extreme-past Schur complements and then through the ordinary conditional-probability martingale gives `q_1(gamma) <= P(X_target=1 | entire past) <= q_0(gamma)`.
- The mixed-pattern Schur formula uses `E=Q_PP-diag(1_(gamma=0))`.  The `J=diag(2 gamma-1)` accretivity argument gives `||E^{-1}|| <= 1/a` from the spectral margin, despite `E` being indefinite.
- The conversion from kernel operator error `delta` to one-site probability error is correct: interpolating between the true extreme kernel and the approximate kernel keeps margin at least `epsilon-delta`, and differentiating the finite Schur complement gives a quadratic form `w^* V w`, bounded by `delta [1+((1+delta)/(epsilon-delta))^2]`.
- The entropy lower bound uses only a finite partition by `gamma`: since the entire-past one-site probability lies in `[l_gamma,u_gamma]` and binary entropy is concave, the minimum is at an interval endpoint.  The upper bound is the ordinary finite-conditioning entropy `H(X_target | gamma)`.
- No entropy-rate derivative or finite-window asymptotic fit is used in this certificate.

Implementation audit result: `CORRECT`.

The author code's exact-event determinant uses rows `K` for ones and `K-I` for zeros, then multiplies by `(-1)^(#zeros)`.  This is equivalent to the exact-event determinant with `I-K` zero rows.  The common-denominator Gaussian Bareiss path checks exact divisibility, real determinants, strict positivity, and exact normalization.  The interval log code computes outward rational endpoints from mpmath interval values; the lower-bound endpoint minimum is safe because the minimum of a concave binary entropy on a rational interval occurs at one of its endpoints.

I also wrote an independent low-cost checker that does not import the author certificate code.  It rebuilds direct exact-event matrices with `I-K` zero rows, recomputes all `3 * 2^9` determinants for each of `t=0` and `t=1/4`, checks the rational `delta -> q` error formula from the boundary JSON, verifies zero conditional-order failures over all 256 gammas per `t`, and checks the final gap interval subtraction exactly.  It returned `CORRECT`, PID `66860`, exit status `0`.

Its Decimal sanity recomputation gave:

| t | lower decimal | upper decimal | order failures |
|---|---:|---:|---:|
| `0` | `0.692425018796823287383843794887962148722236069242367035866843663328585841785254109406409198` | `0.692425091509726240933788529248718651257731638363390351248586574972139083488397458898174579` | `0` |
| `1/4` | `0.692398886660687284359837169235966078783693093903112287331331994656932956214936352145557406` | `0.692398967315971625144244117599873113293014002082815558536711746105062061500738855731893129` | `0` |

The remaining caveat is scope, not correctness: the certificate is for one fixed uniformly interior degree-three symbol pair with `n=8` finite partition plus the extreme-past residual enclosure.  It should be cited as `NEGATIVE_PAIR_GAP`, not as evidence that all odd directions have negative rate curvature.

## Boundary residual proof audit

Files audited from the route-owner artifacts: `boundary_residual_proof.md`, `boundary_residual.py`, and `boundary_residual_M64.json`.

Verdict for the stated claim: `CORRECT`.

The semi-infinite indexing is consistent.  With past coordinates `-1,-2,...` and future coordinates `0,1,...`, the code uses

- `T[r,s]=c(s-r)`, the past-past compression;
- `B[r,j]=c(-r-1-j)`, the past-to-future block;
- `C_infinity = C - B^* T^{-1} B`, the Schur complement for all-one past conditioning.

The Schur/Galerkin limit argument is acceptable in this scope: the uniform symbol margin gives `epsilon I <= T`, finite supported past vectors are dense, and `B` is finite rank because the symbol has degree `m=3`.  The residual enclosure also checks out.  If `Y=T^{-1}B` and `R=B-TX`, then `Y-X=T^{-1}R`; because `B^*Y` is Hermitian, using `A=C-sym(B^*X)` gives

`||A-C_infinity|| <= ||B|| ||R|| / epsilon`.

The script replaces operator/Frobenius norms by the entrywise `|Re|+|Im|` sum, which is coarse but safe.

I wrote an independent rational checker that does not import the author script.  It recomputed all four M64 cases from the JSON solution:

| t | complement symbol | status | recomputed delta |
|---|---:|---|---:|
| `0` | false | `CORRECT` | `1.185858141392691e-11` |
| `0` | true | `CORRECT` | `2.357193088863124e-22` |
| `1/4` | false | `CORRECT` | `2.0123568718409805e-11` |
| `1/4` | true | `CORRECT` | `2.5470632056604613e-21` |

The exact rational maximum is below `2.013e-11`.  The checker also matched all reported corner entries, verified Hermitian corners, verified `B` support after the first `m` past rows, and spot-checked exact zero residual rows after the cutoff.

Boundary caveats for downstream use:

- the approximate corner `A` has an operator error; later entropy propagation should use an outward margin such as `epsilon-delta`, not the unperturbed `epsilon`;
- the `complement_symbol=true` cases are all-one conditioned kernels for the complement process, so an all-zero original-past statement needs the final occupation-complement step;
- this enclosure is only for the extreme-past finite corner and its error, not for an entropy-rate sign.

## Parity obstruction audit

File audited: `parity_obstruction.md`.

Verdict: `CORRECT` in the stated scope.

For a center `f_0=1/2+sum_{k odd} a_k cos(2 pi kx)`, the shift `x -> x+1/2` sends the center to `1-f_0` and sends the kth sine by the factor `(-1)^k`.  Complementing occupations preserves finite entropy.  Therefore `H_n(f_t)=H_n(f_R(t))` for every finite `n`, and the entropy-rate value identity follows by taking the already-existing entropy limit.  No derivative is passed through the limit.  The finite Hessian mixed entries between an even-harmonic and odd-harmonic direction vanish by differentiating the finite identity.

The note's warning about testing absent harmonics of opposite parity at the nearest-neighbour sparse center is valid.

## Phase restriction lemmas

Files audited: `research/S1/phase/proof_or_blocker.md` and `research/S1/phase/sparse_unit.md`.

Verdict: `CORRECT` for the two short restriction lemmas in their finite-scope statements.

The single-imaginary-edge lemma is valid for a strictly interior finite real symmetric DPP kernel.  Conditioning on all vertices except `{a,b}` leaves fixed positive weights, and the two-point conditional kernel has fixed diagonals and off-diagonal `z+i t v`.  Its four exact probabilities are

`rs-u`, `r(1-s)+u`, `(1-r)s+u`, `(1-r)(1-s)-u`, with `u=z^2+t^2 v^2`.

The derivative of this conditional entropy with respect to `u` is `log(AD/(BC))`, and `AD-BC=-u`, so it is nonpositive and strictly negative away from the zero-offdiag point while probabilities remain positive.  The entropy chain rule then proves finite-kernel entropy nonincrease under a single imaginary edge perturbation.  This is a structural exclusion only; it does not settle multi-edge windows or entropy rates.

The sparse-center parity block identity is also valid.  For `p=1/2` and no even cosine coefficients, the transformation `K -> U(I-K)U*`, with `U_jj=(-1)^j`, fixes the center and sends the distance-`k` imaginary direction to `(-1)^(k+1)` times itself.  Since complementing occupations and diagonal unitary conjugation preserve finite configuration entropy, the finite Hessian block between opposite parities is zero.  The corresponding entropy-rate value symmetry follows after taking the entropy limit, but no entropy-rate Hessian existence or derivative-limit exchange is asserted.

I also agree with the phase notes' scope limits: the finite negative Hessian batches and the nearest-neighbour sparse obstruction do not imply a universal negative-curvature theorem and do not remove the need for a different fixed candidate plus certified rate bounds if the goal is still to find a positive counterexample.

## Evidence files

- `exact_toeplitz_review.py`, SHA256 `78540D0BAA9E56AB58D15CFE8B52DA80CB56F577ABFDECFF716C9DD26D98B90B`.
- `exact_toeplitz_review_results.json`, SHA256 `E36CE26802C5550BD3E281EF40E6337E75C7B959207FC710D442221832283A3A`.
- `baseline_comparison.json`, SHA256 `5DAD3360B0DBC420085A41F5B263C46935630DA6F881DF53A4DC83A9209DDA6E`.
- `boundary_residual_review.py`, SHA256 `06EAFEC0C2FEB211BA9CE53DE1BF8E3FD2726496AC91FD5556BFBA5ACFD2323F`.
- `boundary_residual_review_result.json`, SHA256 `873F62DC31B5744EF92162670CF40B17723091E3B11CA780C5A6E6767875E4F2`.
- `rate_certificate_decimal_review.py`, SHA256 `0F1858CCBE3D8E5CADF46AF53F19A625F30CB20D8AE1AD954E38DEF418FCD50E`.
- `rate_certificate_decimal_review_result.json`, SHA256 `7B8A572201EA9EEE9FABA13572167FCFFCB52A957B997106468A866DBADF82EE`.

Runs were deterministic with no random seed.  Main exact-event run used PID `51024`, exit status `0`, Python `3.12.14`, NumPy `2.3.5`, and BLAS/OpenMP thread variables set to `1`.  Boundary residual review used PID `50440`, exit status `0`, Python `3.12.14`, and exact rational arithmetic.  Rate-certificate Decimal review used PID `66860`, exit status `0`, Python `3.12.14`, exact rational determinants, and Decimal precision `90`.  Review git head before commit was `fa504ec74e16843fafc395880d7ba99b4c1d2129` on branch `research/S1-review-20260909`; the author object audited was frozen at commit `a98811c6597577f73128aaed3fd7dde6169af350`.
