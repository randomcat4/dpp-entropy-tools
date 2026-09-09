# PR53 exponential Wiener extension — independent second review

Frozen head: `73cdbd09ad9aa975354a116a01f1e0f4955a8c27`

Overall verdict: `ACCEPTED_SCOPED`.

This review covers the exponential-Wiener extension and its seven-file companion delta at the frozen head. It does not certify any later source change.

Files read:

- `research/I05-DPP-21-20260909/exponential_wiener_extension.md`
- `research/I05-DPP-21-20260909/RESULT.md`
- `research/I05-DPP-21-20260909/verification.md`
- `research/I05-DPP-21-20260909/code/check_rudin_shapiro_example.py`
- `research/I05-DPP-21-20260909/output/rudin_shapiro_exact.json`
- `research/I05-DPP-21-20260909/README.md`
- `research/I05-DPP-21-20260909/sources.md`
- dependency files `finite_range_local_theorem.md` and `proof.md`

I did not read first-review reports, C3 follow-up reports, issue comments, or reviewer artifacts. I did not run arithmetic, CAS, scout, formal, or checker jobs. The file `exponential_wiener_extension.md` has 175 lines in this frozen snapshot.

## Verdict table

| Item | Status | Source anchors |
|---|---:|---|
| Theorem EW statement: arbitrary mean, strict `A_beta`, no small Wiener norm, local quartic correction | `ACCEPTED_SCOPED` | `exponential_wiener_extension.md:7-43`; `RESULT.md:7-32`; `README.md:13-47` |
| Uniform event inverse localization in exponentially weighted Wiener norm | `ACCEPTED_SCOPED` | `exponential_wiener_extension.md:45-154`; `finite_range_local_theorem.md:145-205`; `verification.md:78-91` |
| Common complex disk and complex weighted norms | `ACCEPTED_SCOPED` | `exponential_wiener_extension.md:156-183`; `finite_range_local_theorem.md:207-250` |
| Far-boundary conditional convergence and fixed Hölder holomorphy | `ACCEPTED_SCOPED` | `exponential_wiener_extension.md:185-231`; `finite_range_local_theorem.md:252-303`; `verification.md:93-102` |
| Ruelle--Perron--Frobenius and rate formula identification | `ACCEPTED_SCOPED` | `finite_range_local_theorem.md:305-341`; `exponential_wiener_extension.md:242-249`; `sources.md:27-37` |
| Vanishing of the `s=t^2` linear term | `ACCEPTED_SCOPED` | `finite_range_local_theorem.md:343-377`; `exponential_wiener_extension.md:242-254`; `verification.md:106-113` |
| Matching/KL coefficient and local curvature conclusion | `ACCEPTED_SCOPED` | `finite_range_local_theorem.md:88-143`, `379-397`; `exponential_wiener_extension.md:233-262`; `verification.md:114-128` |
| Rudin--Shapiro exact example checker/output, static review only | `ACCEPTED_SCOPED` | `finite_range_local_theorem.md:399-455`; `code/check_rudin_shapiro_example.py:1-80`; `output/rudin_shapiro_exact.json:1-64`; `verification.md:5-45` |
| Scope and novelty boundaries | `ACCEPTED_SCOPED` | `RESULT.md:42-54`; `README.md:72-93`; `sources.md:1-4`, `63-65`; `verification.md:130-136` |

## Main theorem check

The theorem’s quantifiers are coherent. For `beta>0`, `c,g in A_beta` are real, satisfy half-period even/odd symmetry, `g` is nonzero, and `delta <= c <= 1-delta` (`exponential_wiener_extension.md:7-24`). This gives `mu=int c in (0,1)`, so the denominator in
`alpha_k=|g_hat(k)|^4/[8 mu^2(1-mu^2)]` is positive. Since `g` is half-period anti-invariant and nonzero, it has at least one odd nonzero Fourier coefficient. The theorem only claims existence of a local interval, not a whole legal interval (`exponential_wiener_extension.md:31-43`, `264-268`).

The result is genuinely outside the small-Wiener condition used by PR39. The source explicitly removes smallness of the ordinary or weighted Wiener norm of `c-1/2`, while retaining the strict pointwise margin and exponential Fourier summability (`exponential_wiener_extension.md:39-43`; `README.md:21-47`). This is not an `L`-ensemble interpolation, not a spectral-basis rotation, and not a finite-window fit (`exponential_wiener_extension.md:264-268`).

## Uniform truncation and inverse bounds

The extension’s key replacement for finite range is sound. For every finite interval and every complete zero set, the accretivity lemma gives
`||M_Z^{-1}|| <= delta^{-1}` with no lower bound on event probability (`exponential_wiener_extension.md:45-59`; finite-range proof at `finite_range_local_theorem.md:145-185`). This covers rare and far-boundary configurations.

The band truncation argument is valid. Choose `W` so that the Fourier tail operator `E_W` has ordinary norm `< delta/4`; then `B_Z=M_Z-E_W` has singular values at least `3delta/4` and norm `<1` (`exponential_wiener_extension.md:80-111`). Because `B_Z` is Hermitian and banded, the finite Neumann identity for `B_Z^{-1}` gives exponential entry decay (`exponential_wiener_extension.md:111-130`; finite-range proof at `finite_range_local_theorem.md:187-205`). Choosing
`a_W=min{beta/2,-log(q)/(8W)}` makes the weighted inverse norm grow at most linearly in `W`, while the weighted tail obeys
`||E_W||_{a_W} <= exp(-beta W/2)||c||_beta` (`exponential_wiener_extension.md:118-143`). The exponential decay beats the linear growth, so the final Neumann series gives a uniform weighted inverse bound independent of volume and complete configuration (`exponential_wiener_extension.md:140-154`).

The complex part is also controlled. Since `g in A_beta` and `a<=beta/2`, all finite Toeplitz restrictions of `g` have bounded weighted Schur norm, and the disk
`|z| < [2B||g||_a]^{-1}` works simultaneously for every volume and complete event matrix (`exponential_wiener_extension.md:156-183`). The proof uses positivity only on the real legal slice; the complex disk is an analytic inverse estimate.

## Far-boundary conditionals and Hölder holomorphy

The one-sided conditional formula is the exact complete-event Schur complement:

```text
q_{r,z}(x)=c_hat(0)+z g_hat(0)-b_r(z)M_{r,x}(z)^{-1}d_r(z).
```

This retains the full configuration-dependent inverse (`exponential_wiener_extension.md:185-194`; finite-range analogue at `finite_range_local_theorem.md:252-260`).

For infinite range, the near/far block identity

```text
[M_R^{-1}]_NN-M_N^{-1}
 =M_N^{-1}E_NF S_F^{-1}E_FN M_N^{-1}
```

is the correct Schur-complement inverse formula (`exponential_wiener_extension.md:196-210`). The weighted inverse bound controls `S_F^{-1}` as a block of the full inverse, and the two propagations from site zero to the far block carry an exponential distance penalty. Direct Fourier tails from `b_F,d_F` have the same exponential order. This gives the stated uniform estimate
`sup_x |q_{R,z}(x)-q_{r,z}(x_1,...,x_r)| <= A exp(-a' r)` on each smaller complex disk (`exponential_wiener_extension.md:211-220`; `verification.md:93-102`).

Uniform convergence and Cauchy estimates give a Hölder-space holomorphic limit `q_z`. For real small `t`, the strict margin for `c+tg` and the event-matrix accretivity argument bound both `q_t` and `1-q_t` away from zero, so
`g_t(1x)=q_t(x)`, `g_t(0x)=1-q_t(x)` is a strictly positive normalized Hölder `g`-function (`exponential_wiener_extension.md:220-229`). The diagonal gauge symmetry gives evenness in `t`, so the holomorphic family can be written in `s=t^2` (`exponential_wiener_extension.md:229-231`; finite-range proof at `finite_range_local_theorem.md:297-303`).

## RPF and entropy-rate identification

The Ruelle--Perron--Frobenius input is used with the right hypotheses: a mixing full shift on the finite alphabet `{0,1}`, a strictly positive normalized Hölder `g`-function, and a Banach-holomorphic perturbation of the transfer operator (`finite_range_local_theorem.md:305-325`; `sources.md:27-37`). The proof also supplies the needed analytic perturbation mechanism directly through a Riesz projection around the simple isolated eigenvalue (`finite_range_local_theorem.md:311-317`).

The entropy and relative-entropy rate formulas are not obtained by differentiating finite-volume limits. The finite right-to-left chain rules are written first; the logarithms are uniformly Lipschitz because the conditionals are bounded away from zero and one, and the conditional replacement error is exponentially summable. Thus the total finite-block error is `O(1)`, and division by volume gives

```text
h(c+tg)=-nu_s(log G_s),
R(t)=nu_s(log(G_s/G_0)).
```

This proves the rate formula before any derivative is taken (`finite_range_local_theorem.md:327-341`; `sources.md:35-37`; `verification.md:102-104`).

## Vanishing linear term, KL coefficient, and curvature

The linear term in `s` vanishes correctly. In
`mathcal R(s)=nu_s(log(G_s/G_0))`, the derivative of `nu_s` at zero multiplies the zero observable `log 1`, and the remaining term integrates to zero from the normalization
`G_s(0x)+G_s(1x)=1` (`finite_range_local_theorem.md:343-365`; `verification.md:106-113`). Hence `R(t)=A t^4+O(t^6)`.

The matching/KL lower bound is also valid. For a step-`k` matching with `k` odd, each matched edge crosses the two parity blocks, and its two-point inclusion probability changes from `mu^2` to `mu^2-gamma t^2` (`finite_range_local_theorem.md:88-101`). Determinantal negative association applies to the nonnegative decreasing edge functions on disjoint edge-coordinate sets, giving the product moment bound. The entropy variational inequality optimized over the nonpositive tilt gives

```text
D(P_{n,t}||P_{n,0})
 >= |M_n| d(mu^2-gamma t^2 || mu^2).
```

Dividing by volume and using `|M_n|/n -> 1/2` gives the true rate inequality
`R(t) >= (1/2)d(mu^2-gamma t^2 || mu^2)` for each fixed legal `t` (`finite_range_local_theorem.md:103-129`; `exponential_wiener_extension.md:233-240`). The binary expansion then yields
`A >= gamma^2/[4mu^2(1-mu^2)]` (`finite_range_local_theorem.md:131-143`, `373-377`; `exponential_wiener_extension.md:249-254`).

The final curvature constant is consistent. With
`C_k=gamma^2/[4mu^2(1-mu^2)]` and `alpha_k=C_k/2`, reducing the interval gives
`R''(t)>=6C_k t^2`; the second derivative of `alpha_k t^4` is also `6C_k t^2`, so
`h(c+tg)+alpha_k t^4` is concave locally (`finite_range_local_theorem.md:379-397`; `exponential_wiener_extension.md:256-262`; `verification.md:116-128`). Since `t^4` is strictly convex, this also implies strict concavity of `h(c+tg)` on nontrivial subchords of the accepted local interval.

## Static example checker/output

The checker is correctly scoped as an exact constants check only, not an entropy or rate computation (`code/check_rudin_shapiro_example.py:1-7`; `verification.md:5-45`; `output/rudin_shapiro_exact.json:59-60`).

The Rudin--Shapiro recurrence and displayed `P_4` coefficients agree with the finite-range theorem (`finite_range_local_theorem.md:399-420`; `code/check_rudin_shapiro_example.py:29-44`; `output/rudin_shapiro_exact.json:2-55`). The combined autocorrelation cancellation proves `|P_4|^2+|Q_4|^2=32` on the unit circle. The margin check `(7-4sqrt(2))/16>0` is reduced to the exact inequality `49>32` (`finite_range_local_theorem.md:422-433`; `code/check_rudin_shapiro_example.py:50-51`; `output/rudin_shapiro_exact.json:61`).

The Wiener and quartic constants are consistent. The 15 nonconstant monomials in `P_4-1`, after taking real parts and multiplying by `1/16`, contribute total absolute Fourier mass `15/16`, so `2||c-1/2||_W=15/8>1`. For
`g(theta)=cos(2pi theta)/64`, `g_hat(1)=1/128`, `gamma=1/16384`, and with `mu=1/2`,
`alpha=1/(3*2^27)=1/402653184`
(`finite_range_local_theorem.md:436-447`; `code/check_rudin_shapiro_example.py:46-57`; `output/rudin_shapiro_exact.json:56-64`). This verifies that the example lies outside PR39’s small-Wiener hypothesis while receiving only an unspecified positive local interval, not the full legal interval (`finite_range_local_theorem.md:449-455`; `README.md:58-70`).

## Companion delta and source/novelty boundary

Compared with the `pr53_abdd660a6c77` snapshot, the pre-existing docs changed only in `README.md` and `sources.md`; `finite_range_local_theorem.md` and `proof.md` are unchanged dependencies. The new files `RESULT.md`, `verification.md`, `exponential_wiener_extension.md`, `code/check_rudin_shapiro_example.py`, and `output/rudin_shapiro_exact.json` were added.

The modified `README.md` accurately reframes the branch from an incomplete interface checkpoint to a scoped local theorem while preserving the original gaps: no whole-legal-interval theorem, no full PR39-interval result, no arbitrary measurable-symbol theorem, and no entropy-rate counterexample (`README.md:5-11`, `72-93`). The modified `sources.md` separates bibliography from acceptance, names the precise RPF/g-measure role, and states that no cited source supplies whole-legal-interval concavity or independently reviews the new author proof (`sources.md:1-4`, `27-37`, `63-65`). `RESULT.md` likewise makes no novelty, priority, or main-branch acceptance claim (`RESULT.md:52-54`).

I did not perform an external literature search. Within this source-bound review, the novelty/scope assertions are literal and appropriately limited.

## Limitations

This `ACCEPTED_SCOPED` verdict covers the local exponential-Wiener theorem and static example constants at frozen head `73cdbd09ad9aa975354a116a01f1e0f4955a8c27`. It does not certify whole-legal-interval concavity, the PR39 example on `[-384,384]`, arbitrary measurable symbols, arbitrary fixed scalar symbol chords, or any true entropy-rate counterexample (`RESULT.md:42-50`; `README.md:91-93`; `exponential_wiener_extension.md:264-268`). It also does not upgrade the open beam-splitter/operator route; `proof.md` explicitly keeps that route separate and unproved (`proof.md:229-339`).

No correction is required for the scoped EW theorem.
