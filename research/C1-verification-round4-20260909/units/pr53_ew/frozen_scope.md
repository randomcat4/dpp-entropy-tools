# Frozen scope for PR53 EW first review

Reviewer: `C1 Theorem EW first reviewer`
Role: non-author FIRST proof review for PR53 exponential-Wiener successor only.

Comparison frozen for this review:

```text
base: abdd660a6c7761c7a8a53cb8671b4d2543530a5c
head: 73cdbd09ad9aa975354a116a01f1e0f4955a8c27
prefix: research/I05-DPP-21-20260909/
```

Local head source: `source-snapshots/pr53_ew_73cdbd09`.
Local finite-range author source for inheritance only: `source-snapshots/pr53_abdd660/finite_range_local_theorem.md`.

This review covers only the exponential-Wiener extension and its seven companion source changes. It does not repeat the previous PR53 bridge review, does not repeat a full finite-range audit, does not inspect later second-review artifacts, and does not review PR54 appendices.

## Source files under review

The seven head files and binding are:

- `exponential_wiener_extension.md`
- `RESULT.md`
- `verification.md`
- `code/check_rudin_shapiro_example.py`
- `output/rudin_shapiro_exact.json`
- `README.md`
- `sources.md`
- `SOURCE_BINDING.json`

The finite-range file may be read only to verify that EW inherits the finite parity identity, matching/KL lower bound, transfer-operator rate formula, vanishing linear term, and quartic coefficient rather than silently assuming a new theorem.

## Main theorem frozen for review

For `beta>0`, define

```text
A_beta={u:T->C : ||u||_beta=sum_{j in Z} exp(beta|j|)|u_hat(j)|<infinity}.
```

Let real `c,g in A_beta` satisfy

```text
c(theta+1/2)=c(theta),
g(theta+1/2)=-g(theta),
g != 0,
delta <= c(theta) <= 1-delta
```

for some `delta>0`. Put `mu=integral_T c`. For any odd Fourier mode `k` with `g_hat(k)!=0`, set

```text
gamma=|g_hat(k)|^2,
alpha_k=gamma^2/[8 mu^2(1-mu^2)].
```

The EW claim is that there is `epsilon=epsilon(c,g,k,beta,delta)>0` such that

```text
t -> h(c+t g)+alpha_k t^4
```

is concave on `[-epsilon,epsilon]`. Consequently `h(c+t g)` is strictly concave there. No smallness assumption is imposed on the ordinary or weighted Wiener norm of `c-1/2`. Finite Fourier support is a special case.

If the chosen odd `k` is negative, the inherited matching argument is understood with step `|k|`; for real `g`, the coefficient magnitude and `gamma` are unchanged.

## Claims under review

1. Weighted event-inverse theorem.

   For every finite interval `Lambda` and zero set `Z`, with `M_Z=K_c|_Lambda-I_Z`, the strict margin gives `||M_Z^{-1}||<=delta^{-1}` and the exponential-Wiener truncation argument gives common constants `a>0`, `B<infinity` such that

   ```text
   sup_{Lambda,Z} ||M_Z^{-1}||_a <= B
   ```

   in the exponentially weighted Schur norm.

2. No-smallness finite-band truncation mechanism.

   The proof may choose a truncation width `W` depending on `c,beta,delta`. It must justify the least-singular-value estimate for `B_Z=K_{c^(W)}|_Lambda-I_Z`, the weighted inverse bound `C_delta(1+W)` at

   ```text
   a_W=min(beta/2,-log(1-(3delta/4)^2)/(8W)),
   ```

   and the fact that the exponentially small tail of `c-c^(W)` beats this growth. It may not assume a small ordinary or weighted Wiener norm.

3. Common complex event-inverse disk.

   For `M_Z(z)=K_{c+zg}|_Lambda-I_Z`, the weighted Neumann argument must give a radius independent of volume and configuration, with all complete-event matrices invertible for `|z|<r_0`.

4. Infinite-range one-sided conditional localization.

   The Schur-complement conditional

   ```text
   q_{r,z}(x)=P_z(X_0=1 | X_1...X_r=x)
   ```

   must converge uniformly and exponentially to a one-sided limit `q_z`. The near/far block identity must support the estimate despite infinite tails. The proof must supply a fixed Holder-space setting, possibly with a weaker exponent than the raw decay rate, and not rely on scalar uniform convergence alone.

5. Valid inheritance of the finite-range rate proof.

   Once Claim 4 supplies a positive normalized Holder `g`-function that depends holomorphically on `s=t^2`, the finite-range Ruelle/eigenmeasure/rate formula, vanishing of the linear term in `s`, matching/KL lower bound, and quartic curvature constant may be inherited only if their hypotheses still hold for `A_beta`.

6. Companion source and checker scope.

   `README.md`, `RESULT.md`, `verification.md`, `sources.md`, `SOURCE_BINDING.json`, the exact checker script, and recorded output must state the scope literally, keep author output separate from C1 execution, avoid upgrading finite arithmetic to entropy-rate proof, and preserve the global-open boundary.

## Explicit exclusions

This review does not certify whole-legal-interval concavity, arbitrary measurable-symbol concavity, arbitrary fixed scalar symbol chords, a true entropy-rate counterexample, a new Lean theorem, novelty or publication priority, PR54 appendices, or any result from later reviewers.

## Success standard

Each claim receives `CORRECT` or `CRITICAL_GAPS`. The overall verdict is one of `ACCEPTED_SCOPED`, `NEEDS_FIX`, `INCOMPLETE`, or `REFUTED`.
