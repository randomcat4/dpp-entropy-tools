# PR53 EW first proof review

Reviewer: `C1 Theorem EW first reviewer`
Scope: PR53 exponential-Wiener successor only, base `abdd660a6c7761c7a8a53cb8671b4d2543530a5c` to head `73cdbd09ad9aa975354a116a01f1e0f4955a8c27`.
Frozen scope: `frozen_scope.md`.

## Verdict

Overall verdict: `ACCEPTED_SCOPED`.

The exponential-Wiener extension checks out within its stated local-in-`t`, strict-center, exponentially weighted Fourier scope. I found no critical gap in the weighted event-inverse algebra, the common complex inverse disk, the infinite-range one-sided conditional estimate, or the inheritance of the finite-range RPF/KL/quartic argument. The proof still does not address the whole legal interval, arbitrary measurable symbols, or the open beam-splitter occupation inequality.

| Claim | Status | Review result |
| --- | --- | --- |
| Weighted complete-event inverse in `A_beta` | `CORRECT` | Band truncation plus accretivity and a weighted Neumann algebra gives volume/configuration-uniform constants. |
| No-smallness truncation mechanism | `CORRECT` | The inverse bound grows at most linearly in `W`, while the weighted Fourier tail decays exponentially; no Wiener-smallness is used. |
| Common complex event-inverse disk | `CORRECT` | The disk radius depends on `c,g,beta,delta`, but not on volume or configuration. |
| Infinite-range one-sided conditional localization | `CORRECT` | The displayed near/far Schur identity supports the estimate; use a fixed weaker Holder exponent for Banach-space holomorphy. |
| Inheritance of finite-range RPF/KL/quartic proof | `CORRECT` | EW supplies the only finite-range input that FR needed, and the remaining arguments do not require finite Fourier support. |
| Companion source, binding, checker, output | `CORRECT` | Scope language, blob bindings, script/output consistency, and non-proof boundaries are literal and consistent. |

## Source Integrity

`SOURCE_BINDING.json` records the expected scope, base/head commits, unchanged finite-range blob, and seven changed files (`SOURCE_BINDING.json` lines 1-59). I recomputed the local Git blob hashes of the seven downloaded head files; every hash matched the binding.

The compare snapshot `pr53_fr_successor_delta.json` also records the same seven changed paths and head blob hashes. The source set under review is therefore the intended PR53 EW successor, not the earlier five-file bridge snapshot.

## Claim 1: weighted complete-event inverse

Status: `CORRECT`.

EW starts with `c,g in A_beta`, half-period symmetry, `g!=0`, and a strict center margin `delta<=c<=1-delta` (`exponential_wiener_extension.md` lines 9-24). For any finite interval `Lambda`, the Toeplitz compression of `K_c` inherits the spectral margin because

```text
<v,K_c v> = integral_T c(theta) |sum_{j in Lambda} v_j exp(2 pi i j theta)|^2 dtheta.
```

Thus the finite-range accretivity proof applies without any range assumption and gives `||M_Z^{-1}||<=delta^{-1}` for every zero set (`exponential_wiener_extension.md` lines 45-59).

The stronger weighted claim is Lemma 2.1 (`exponential_wiener_extension.md` lines 63-76). The truncation proof is sound. With `E_W=K_{c-c^(W)}|_Lambda`, Young's inequality gives `||E_W||<=sum_{|j|>W}|c_hat(j)|` (`exponential_wiener_extension.md` lines 80-91). After choosing `W` with this tail below `delta/4`, singular-value perturbation gives `sigma_min(B_Z)>=3delta/4` for `B_Z=M_Z-E_W` (`exponential_wiener_extension.md` lines 93-103). Since `M_Z` has spectrum in `[-(1-delta),1-delta]`, the estimate `||B_Z||<1` is also valid (`exponential_wiener_extension.md` lines 105-111).

The banded inverse estimate for `B_Z^{-1}` is the same polynomial inverse expansion used in the finite-range source (`finite_range_local_theorem.md` lines 187-205), now with half-bandwidth `W` and `eta=3delta/4` (`exponential_wiener_extension.md` lines 111-116). This yields the displayed pointwise decay.

## Claim 2: no-smallness truncation mechanism

Status: `CORRECT`.

The weighted norm bound at

```text
a_W=min(beta/2,-log(q)/(8W)),     q=1-(3delta/4)^2,
```

is justified by summing the banded inverse estimate over distance shells of size `W` (`exponential_wiener_extension.md` lines 118-130). The row and column sums have only `O(W)` near-field contribution and a geometrically decaying tail, so the stated `C_delta(1+W)` form is valid.

The tail estimate

```text
||E_W||_{a_W} <= exp(-beta W/2)||c||_beta
```

follows because `a_W<=beta/2` (`exponential_wiener_extension.md` lines 132-138). The product of `C_delta(1+W)` and this exponential tail tends to zero as `W` grows, so the weighted Neumann inverse in lines 140-152 is uniform over every volume and zero set.

This is the key no-smallness point: `W` is allowed to depend on `c,beta,delta`, and the final constants may depend on `||c||_beta`, but no bound of the form `||c-1/2||_W` small or `||c-1/2||_beta` small is assumed. The README states this correctly (`README.md` lines 21-47), and the theorem statement repeats it (`exponential_wiener_extension.md` lines 31-43).

## Claim 3: common complex inverse disk

Status: `CORRECT`.

For `M_Z(z)=M_Z+zG_Lambda`, the weighted Schur bound on `G_Lambda` follows from `g in A_beta` and `a<=beta/2` (`exponential_wiener_extension.md` lines 156-169). Lemma 2.1 gives a uniform bound `B` for `M_Z^{-1}` in the weighted algebra, so the Neumann formula is valid for

```text
|z| < [2B||g||_a]^{-1}.
```

The resulting inverse bound is uniform in `Lambda`, `Z`, and `z` in the disk (`exponential_wiener_extension.md` lines 171-183). This step is complex analytic; positivity is needed only later on the real legal slice. No hidden finite-range or small-Wiener assumption appears here.

## Claim 4: infinite-range conditionals

Status: `CORRECT`.

The one-sided finite conditional formula

```text
q_{r,z}(x)=c_hat(0)+zg_hat(0)-b_r(z)M_{r,x}(z)^{-1}d_r(z)
```

is the exact complete-event Schur complement (`exponential_wiener_extension.md` lines 185-194). Since `c,g in A_beta`, the coupling row and column have uniformly bounded weighted `l^1` norms and exponentially small direct tails.

The near/far identity in lines 196-207 is correct. For the block decomposition `N=[1,r]`, `F=[r+1,R]`,

```text
[M_R^{-1}]_{NN}-M_N^{-1}
 = M_N^{-1}E_NF S_F^{-1}E_FN M_N^{-1},
S_F=M_F-E_FN M_N^{-1}E_NF.
```

The phrase in line 209 is slightly compressed, but not a mathematical gap. The exact block inverse formula gives `S_F^{-1}=[M_R^{-1}]_{FF}` when the Schur complement is taken over `N`; the opposite Schur formula also writes it as `M_F^{-1}` plus a standard correction. In either form, all factors are blocks of complete-event matrices already covered by the common inverse bound from Section 3.

The estimate in lines 211-218 follows in the weighted Schur algebra. If a row has bounded weighted mass relative to site `0`, then its ordinary mass on `F` is at most `O(exp(-ar))`, since every `F` index is at distance at least `r`. The same is true for the right column, while direct tails `b_F` and `d_F` are exponentially small from the `A_beta` norm. This gives the uniform estimate

```text
sup_x |q_{R,z}(x)-q_{r,z}(x_1,...,x_r)| <= A exp(-a' r)
```

on each closed smaller disk `|z|<=r_1<r_0`.

For the Holder-space conclusion (`exponential_wiener_extension.md` lines 220-231), scalar uniform convergence alone would be too weak. The proof has enough decay to choose a fixed weaker Holder exponent, say any exponent strictly below the decay rate obtained in (4.4). The same near/far estimate gives uniform variation bounds, and Cauchy's formula on a slightly larger disk gives the corresponding parameter-derivative bounds in that fixed weaker Holder norm. With that standard interpretation, `z -> q_z` is Banach-holomorphic as needed.

For real small `t`, strict legality of `c+tg` follows from the strict margin for `c` and boundedness of `g`; the complete-event accretivity argument keeps the limiting conditional bounded away from `0` and `1` (`exponential_wiener_extension.md` lines 222-229). Half-period diagonal gauge symmetry gives evenness in `t`, so the family is holomorphic in `s=t^2`.

Non-blocking exposition recommendations:

- For EW line 209, add the exact identity

  ```text
  S_F(z)^{-1}=[M_R(z)^{-1}]_{FF}.
  ```

  A clean replacement sentence is: "With `S_F=M_F-E_FN M_N^{-1}E_NF`, the block inverse formula gives exactly `S_F^{-1}=[M_R^{-1}]_{FF}`; using the opposite Schur complement also writes `S_F^{-1}` as `M_F^{-1}` plus the standard correction. Both forms are controlled by the uniform complete-event inverse bound."

- For EW lines 220-231, state the fixed Holder space explicitly. A concise addition is: "Choose a Holder exponent `0<b<a'` and work in `C^b` on the one-sided full shift. The estimate (4.4), the same estimate for variations, and interpolation between the sup norm and the uniform stronger variation bound make `q_{r,z}` Cauchy in `C^b`; Cauchy's formula on disks `|z|<=r_1<r_2<r_0` gives the same `C^b` convergence for difference quotients, hence `z -> q_z` is Banach-holomorphic in `C^b`." This is presentation support, not an added theorem assumption.

## Claim 5: finite-range inheritance and quartic constant

Status: `CORRECT`.

EW explicitly inherits only the finite-range proof components that do not require finite Fourier support once Claim 4 supplies the analytic conditional input (`exponential_wiener_extension.md` lines 43 and 231-262).

The finite parity identity uses half-period Fourier vanishing and block marginals, not finite range (`finite_range_local_theorem.md` lines 54-86). This remains valid for `A_beta`.

The matching/KL lower bound also does not require finite range. For an odd mode `k`, the step-`|k|` matching is vertex-disjoint, and for each matched edge the two-point determinant gives

```text
E_t(X_iX_{i+k})=mu^2-|g_hat(k)|^2 t^2.
```

This is exactly the computation in the finite-range source (`finite_range_local_theorem.md` lines 88-128). Negative association is applied under the DPP law at `t=0` to nonnegative decreasing functions on disjoint edge-coordinate sets (`finite_range_local_theorem.md` lines 103-120). The cited Lyons theorem is the right external input for this use (`sources.md` lines 11-13).

The transfer-operator passage is inherited correctly. FR states the needed finite-alphabet Ruelle-Perron-Frobenius fact for a strictly positive normalized Holder `g`-function (`finite_range_local_theorem.md` lines 305-325), and EW Section 4 supplies precisely such a function for real small `t`. The rate formulas are then derived from right-to-left chain rules plus exponentially summable conditional errors, not by differentiating `H_n/n` through a limit (`finite_range_local_theorem.md` lines 327-341).

The external Ruelle source match is valid when restricted to the Holder theorem, not a general Walters-class assertion. Cioletti-Silva's Theorem 2.1 gives the simple maximal eigenvalue and spectral gap for `0<gamma<1` Holder spaces, and their Lemma 2.4, Proposition 2.6, and Corollary 2.7 give the relevant operator/dual analyticity framework. For the normalized sum operator in FR line 322, take the uniform prior on `{0,1}` and potential `f=log(2G_s)`, so the source's integral operator reproduces `sum_a G_s(ax)F(ax)`. The broader Walters-class no-gap phenomena in that paper are not used.

The vanishing linear term and quartic constant are also inherited correctly. FR differentiates

```text
mathcal R(s)=nu_s(log(G_s/G_0))
```

and the derivative of `nu_s` drops out because the observable is zero at `s=0`; the remaining term integrates to zero from normalization `G_s(0x)+G_s(1x)=1` (`finite_range_local_theorem.md` lines 343-365). The matching/KL lower bound gives

```text
A >= C_k = gamma^2/[4mu^2(1-mu^2)].
```

Then `R''(t)>=6C_k t^2` after shrinking the interval, and `alpha_k=C_k/2` contributes exactly `12 alpha_k t^2=6C_k t^2` (`finite_range_local_theorem.md` lines 373-397; `exponential_wiener_extension.md` lines 249-262). Thus `h(c+tg)+alpha_k t^4` is concave locally, and subtracting the strictly convex `alpha_k t^4` gives strict concavity of `h(c+tg)`.

## Claim 6: companion files and exact checker

Status: `CORRECT`.

Per-file disposition:

| File | Change type | Disposition |
| --- | --- | --- |
| `exponential_wiener_extension.md` | added | `CORRECT`; mathematical proof accepted within the frozen EW local scope, with whole-interval claims explicitly excluded. |
| `README.md` | modified delta | `CORRECT`; the delta states the new theorem, route, explicit example, file map, and global-open boundary without treating the author proof as already accepted. |
| `sources.md` | modified delta | `CORRECT`; the delta adds negative-association, mixing-background, Ruelle/g-measure, and transfer-operator sources with limited roles and no source promoted to a proof of whole-interval concavity. |
| `RESULT.md` | added | `CORRECT`; compact theorem statement and incomplete list match the frozen scope. |
| `verification.md` | added | `CORRECT`; author self-audit only, with review obligations accurately mapped and no independent-review claim. |
| `code/check_rudin_shapiro_example.py` | added | `CORRECT`; static inspection shows exact integer/rational checks only, with no entropy computation. I did not execute it. |
| `output/rudin_shapiro_exact.json` | added | `CORRECT`; static inspection matches the script's asserted constants and is author-recorded output, not a C1 execution. |
| `SOURCE_BINDING.json` | binding metadata | `CORRECT`; all seven local head-file blob hashes were recomputed and matched the binding. |

`README.md` states the new theorem as author proof, keeps the original arbitrary-symbol and whole-legal-interval target incomplete, and says open-PR author claims are not treated as accepted theorems (`README.md` lines 5-12). It also states the new exponential-Wiener domain, the KL lower bound, the transfer-operator route, the explicit Rudin-Shapiro example, and the remaining gap without overclaiming (`README.md` lines 13-93).

`RESULT.md` gives the same theorem statement and exclusions in compact form (`RESULT.md` lines 5-54). Its explicit incomplete list matches the frozen exclusions.

`verification.md` is correctly labeled as an author self-audit, not an independent review (`verification.md` lines 1-4). Its review checklist matches the actual load-bearing proof steps, including the EW truncation, infinite-range near/far identity, Holder/Ruelle passage, rate formulas, vanishing linear term, and curvature constant (`verification.md` lines 47-128). It does not claim that the listed obligations have already been checked by a nonauthor.

`sources.md` separates bibliography from acceptance (`sources.md` lines 1-3). Its new Ruelle/g-measure and transfer-operator source roles are scoped correctly (`sources.md` lines 27-37), and it correctly states that psi-mixing or Gibbs background is not used to replace the explicit event-matrix argument (`sources.md` lines 19-25).

The exact checker script is dependency-free and uses integer/rational arithmetic only (`code/check_rudin_shapiro_example.py` lines 1-7 and 11-57). By static inspection, the recorded JSON output matches the script's asserted constants: `2||c-1/2||_W=15/8`, `g_hat_1=1/128`, `gamma=1/16384`, and `alpha=1/(3*2^27)=1/402653184` (`output/rudin_shapiro_exact.json` lines 56-63). I did not execute the checker in this C1 review. The output is author-recorded exact arithmetic, not a C1 run and not an entropy-rate certificate; both the script and output state that boundary (`code/check_rudin_shapiro_example.py` lines 2-6; `output/rudin_shapiro_exact.json` lines 58-60).

## Remaining Gaps And Exclusions

No critical gap was found inside EW's stated theorem. The remaining open problem is exactly outside this theorem's quantifiers:

- concavity on the whole legal interval, including the PR39 full interval;
- arbitrary measurable half-period symbols;
- arbitrary fixed scalar symbol chords;
- a true entropy-rate counterexample;
- the beam-splitter occupation entropy inequality from the earlier bridge route.

The source states these boundaries in `exponential_wiener_extension.md` lines 5 and 264-268, `README.md` lines 91-93, and `RESULT.md` lines 42-54.

## External Sources Checked

Primary-source checks were limited to theorem matching, not broad prior-art search:

- Direct theorem-hypothesis check: Cioletti-Silva, "Spectral Properties of the Ruelle Operator on the Walters Class over Compact Spaces", [arXiv:1511.01579](https://arxiv.org/html/1511.01579). The inspected text states the compact-alphabet setup and Ruelle operator (lines 61-73), Theorem 2.1 for Holder potentials with `0<gamma<1` and a simple maximal eigenvalue plus spectral gap (lines 74-88), and operator/dual analyticity in Lemma 2.4, Proposition 2.6, and Corollary 2.7 (lines 105-139). The EW proof must use this Holder theorem, not a general Walters-class gap claim; the same source also discusses Walters-class no-gap examples.
- Source-page check for the matching input: Lyons, "Determinantal Probability Measures", [arXiv:math/0204325](https://arxiv.org/abs/math/0204325). The inspected arXiv page identifies negative association among the paper's main results. The branch's `sources.md` cites Theorem 8.1 for the precise theorem used in the matching/KL step.
- Bibliographic/source-role confirmation only: Walters, "Ruelle's Operator Theorem and g-Measures", Trans. AMS 214 (1975), [DOI 10.1090/S0002-9947-1975-0412389-8](https://doi.org/10.1090/S0002-9947-1975-0412389-8). I did not rely on an independently inspected Walters theorem text for the verdict; the direct theorem-hypothesis check used Cioletti-Silva plus the contour Riesz-projection argument on the fixed Holder space written in the proof.

The review does not rely on Fan-Liao-Qiu psi-mixing as a substitute for EW's weighted complete-event inverse estimate.

## Formal And Computational Status

No new theorem-proving, Lean check, entropy computation, or finite-size diagnostic was run. No load-bearing arithmetic question arose, so no `COMPUTE_PLAN.md` was created.
