# PR53 Theorem FR First Proof Review

Status: `CORRECT`

Overall verdict: `ACCEPTED_SCOPED`

Scope reviewed: the single added file `research/I05-DPP-21-20260909/finite_range_local_theorem.md` at PR53 commit `abdd660a6c7761c7a8a53cb8671b4d2543530a5c`, blob `c65a4e22ed6ee5c69d1b084cfd04d8e77e8d6263`, parent `e0688fbb713e55f93acf791b83437ddf2cc06b7f`. I verified the local frozen copy has 473 lines and git blob hash `c65a4e22ed6ee5c69d1b084cfd04d8e77e8d6263`.

I did not read prior C1 review opinions and did not use the author's self-PROVED status as evidence. I did consult the original PR53 author background files only for definitions and route context. I did not access `excluded unrelated private directories`. No computation or Lean formalization was needed or run; there is no formal coverage claim.

## Primary External Sources Checked

1. Russell Lyons, *Determinantal Probability Measures*, Publ. Math. IHES 98 (2003), arXiv:math/0204325, especially Theorem 8.1 on negative association for determinantal probability measures. Link: https://arxiv.org/abs/math/0204325

2. Benoit Kloeckner, Artur O. Lopes, Manuel Stadlbauer, *Contraction in the Wasserstein metric for some Markov chains, and applications to the dynamics of expanding maps*, arXiv:1412.0848v3. Theorem 1.1 gives normalized transfer-operator contraction for compact iterated contraction systems with Lipschitz potentials; Corollary 1.2 gives an actual spectral gap on the complement of constants; the paper explicitly notes the Holder case follows by replacing the metric by a snowflaked metric. Link: https://arxiv.org/abs/1412.0848

3. Paulo Giulietti, Benoit Kloeckner, Artur O. Lopes, Diego Marcon, *The calculus of thermodynamical formalism*, arXiv:1508.01297. Section 2.1 lists the hypotheses H1-H4; Corollary B / Corollary 3.7 gives analytic dependence of the Gibbs/eigenmeasure map once the RPF spectral-gap hypotheses are supplied. This source assumes the RPF hypotheses, so I used Kloeckner-Lopes-Stadlbauer to verify them in the full-shift case. Link: https://arxiv.org/abs/1508.01297

4. PR39 frozen statement for scope comparison, local frozen copy `sources/pr39_frozen_statement.md`, lines 9-16. It assumes `int c=1/2` and `a=2||c-1/2||_W<1`, and does not freeze the mean-not-one-half or whole-legal-interval conclusions.

## Load-Bearing Chain Check

### 1. Statement and PR39 separation: `CORRECT`

Theorem FR is local in `t`, assumes finite Fourier range and a pointwise spectral margin, and explicitly leaves the whole legal interval open; see lines 17-52 and 471-473. The chosen odd `k` exists because a nonzero half-period anti-invariant trigonometric polynomial has only odd Fourier modes. The local legality radius follows from the strict margin on `c` and boundedness of `g`.

The comparison with PR39 is accurate. PR39 requires mean `1/2` and `2||c-1/2||_W<1` in `sources/pr39_frozen_statement.md`, line 9, while PR53 allows arbitrary mean and no small Wiener norm hypothesis, lines 26 and 52. This is a scope comparison only, not proof of novelty beyond all possible literature.

### 2. Finite parity identity and entropy-rate identity: `CORRECT`

Lines 56-86 are valid. Half-period symmetry kills odd Fourier coefficients of `c` and even Fourier coefficients of `g`, so the even and odd restrictions of `P_{n,t}` are independent of `t`. At `t=0`, the kernel is parity block diagonal, hence the two parity restrictions are independent. Therefore `P_{n,0}` is exactly the product of the two true marginals of `P_{n,t}`, and

```text
D(P_{n,t} || P_{n,0}) = H_n(c)-H_n(c+t g).
```

The diagonal gauge `U=diag((-1)^j)` proves equality of complete event probabilities for `t` and `-t`, because exact-event determinant matrices commute with the diagonal zero-set projection under conjugation. Taking the entropy-rate limit in line 79 uses only existence of stationary finite-alphabet entropy rates and does not exchange derivatives with volume limits.

### 3. Matching KL lower bound: `CORRECT`

Lines 90-143 are valid. The step-`k` matching has density tending to `1/2` because the number of arithmetic chains is at most `k`, giving line 93. For an odd step, each edge crosses the two parity blocks. At `t=0`, the endpoints are independent with mean `mu`; at parameter `t`, the two-point inclusion determinant is

```text
mu^2 - |t g_hat(k)|^2 = mu^2 - gamma t^2,
```

which gives line 100.

For `u<=0`, `exp(u X_i X_{i+k})` is positive and coordinatewise decreasing. Lyons' determinantal negative association theorem applies to disjoint edge-coordinate sets under `P_{n,0}`. Induction over the disjoint matching gives the product moment bound in lines 103-108. The variational inequality and optimization over nonpositive tilts then give the binary KL lower bound in lines 110-123. Since legality implies the two-point determinant is nonnegative, the optimized Bernoulli parameter lies in `[0,mu^2]`, so the sign restriction on the tilt is satisfied. Dividing by `n` and using the exact entropy-rate identity gives line 128, and the coefficient in lines 134-140 is

```text
(1/2) * gamma^2 / (2 mu^2(1-mu^2))
= gamma^2 / (4 mu^2(1-mu^2)) = C_k.
```

### 4. Uniform inverse and weighted Schur norm: `CORRECT`

Lines 147-205 are valid. For any exact zero set `Z`, the matrix `M_x=K-I_Z` is not positive, but the signed gauge `J=I_S direct-sum (-I_Z)` gives the accretive estimate in line 172. This proves a uniform lower singular-value bound without any probability lower bound for rare events.

Lemma 4.2 is also valid. Since `K` and `I_Z` are positive contractions, `-I <= K-I_Z <= I`, so `||M_x||<=1`. Together with Lemma 4.1 this gives `M_x^2 >= eta^2 I` and the Neumann expansion in line 201. Bandwidth of `M_x` and `I-M_x^2` gives the stated off-diagonal exponential decay. The weighted Schur norm bound in lines 217-227 follows because the choice `exp(2aw)(1-delta^2)<1` makes the weighted geometric tail summable uniformly in the word and volume. The finite-range bound on `G_r` in lines 230-234 is immediate from finite Fourier support. The complex Neumann radius and inverse bound in lines 236-250 follow in the same weighted Banach algebra.

### 5. Complex one-sided conditionals and Holder convergence: `CORRECT`, with an exposition repair recommended

The finite Schur complement formula in lines 252-257 is the exact complete-event conditional probability for real legal `t`, and a holomorphic continuation for complex `z`. The denominator matrices are uniformly invertible by Section 4, including rare complete configurations.

The remote-boundary estimate in lines 261-268 is compressed but valid. Eliminating the remote block changes the near block only through rows and columns within bounded distance of the cut. Resolvent identities express the difference in finite conditionals as a product of propagation from site `0` to the cut, a uniformly bounded cut term, and propagation back. The weighted inverse bound in line 247 gives the `A exp(-a r)` estimate uniformly in the extension word and volume.

The phrase "the convergence holds in a Holder norm" at line 276 needs to be read as convergence in a fixed weaker Holder norm. The proof has enough ingredients:

- From (5.8), `||q_R-q_r||_infty <= A e^{-a r}`.
- From (5.8) applied against shorter truncations, the functions `q_r` and the limit `q` have a uniform `a`-Holder variation bound.
- Interpolation gives convergence in every `b`-Holder norm with `0<b<a`.
- Cauchy's formula on a disk `r_1<r_2<r_0` applies to the same estimates and gives Banach-holomorphic dependence in that fixed `b`-Holder space.

This is not a critical gap because line 276 says "a Holder norm," not "the same exponent `a`"; however, the theorem file should spell out the choice `0<b<a` and the interpolation estimate. This is the main place where a reader could otherwise mistake uniform convergence for same-exponent Holder convergence.

For real small `t`, line 287 follows from the strict contraction margin applied to the one-site occupied and one-site empty Schur complements. The normalized `g`-function in lines 290-295 is therefore strictly positive. The evenness claim in lines 297-303 follows from the diagonal gauge already checked in Section 2, so `G_s` is a Banach-holomorphic family in `s=t^2`.

### 6. Ruelle-Perron-Frobenius and analytic entropy-rate formula: `CORRECT`

Lines 307-341 are acceptable once the external fact is sourced as above.

Applicability check:

- Space: the one-sided full shift `{0,1}^N` with metric `d_b(x,y)=exp(-b N(x,y))`, for the same `b<a` selected in Section 5.
- Dynamics: the full shift is mixing; its inverse branches `x -> 0x` and `x -> 1x` are global contractions by `exp(-b)`.
- Potential: for real small `s`, `A_s=log G_s` is Lipschitz in `d_b`, since `G_s` is positive and bounded away from zero. Normalization `G_s(0x)+G_s(1x)=1` gives `L_s 1=1`.
- Spectral gap: Kloeckner-Lopes-Stadlbauer Theorem 1.1 and Corollary 1.2 give unique eigenprobability and norm spectral gap for normalized Lipschitz potentials; the Holder case is included through the snowflaked metric.
- Analytic eigenmeasure: Giulietti-Kloeckner-Lopes-Marcon Section 2.1 plus its analytic Gibbs-map corollary applies after H3-H4 are supplied by the preceding spectral-gap theorem. Equivalently, the Riesz projection argument in lines 311-317 is valid for the complexified Holder space because `L_s` is a holomorphic family of bounded operators and the simple eigenvalue `1` remains isolated for small `s`.

The stationary DPP is a `G_s`-measure: the finite conditional probabilities are exactly (5.7), and (5.8) gives the pointwise uniform infinite-tail limit. The RPF uniqueness then identifies its one-sided law with the eigenmeasure `nu_s`.

The rate formulas in lines 327-341 do not differentiate finite-volume entropies. The right-to-left chain rule writes finite entropy and finite relative entropy as sums of finite future-conditionals. Because the logs are uniformly Lipschitz on the interval in line 287 and the conditional errors are exponentially summable by (5.8), replacing finite future-conditionals by the limiting `G_s` costs `O(1)` over an `n`-block. Dividing by `n` yields the exact formulas (6.3)-(6.4). Analyticity of the true rate follows from these formulas and the analytic eigenmeasure, not from finite-window analyticity.

### 7. Vanishing `s`-linear term and quartic coefficient: `CORRECT`

Lines 343-397 are valid. The section heading says "quadratic term in `s` vanishes," but the actual proof correctly shows `mathcal R'(0)=0`, i.e. the `s`-linear term vanishes and therefore no `t^2` term appears in `R(t)`.

Differentiating `mathcal R(s)=nu_s(log(G_s/G_0))` at zero is justified by Section 6. The derivative of `nu_s` hits the zero observable, and the remaining term integrates to zero because `G_s(0x)+G_s(1x)=1`. Hence `R(t)=A t^4+O(t^6)`. Combining this analytic expansion with the true rate KL lower bound gives `A>=C_k`; no finite-to-rate coefficient exchange is used.

The final curvature calculation is correct:

```text
R''(t) = 12 A t^2 + O(t^4) >= 6 C_k t^2
```

after shrinking `epsilon`, and `12 alpha_k = 6 C_k`. Therefore `h(c+t g)+alpha_k t^4` is concave locally. Since `t^4` is strictly convex, subtracting `alpha_k t^4` gives strict concavity of `h(c+tg)` on every nontrivial subchord in the same interval.

### 8. Rudin-Shapiro example and PR39 exclusion: `CORRECT`

Lines 401-455 are correct. From `|P_4|^2+|Q_4|^2=32`, one has `|P_4|<=4 sqrt(2)`, so the margin in lines 431-433 is positive. Each of the 15 nonconstant monomials contributes Fourier mass `1/16` after taking `(1/16) Re`, giving `||c-1/2||_W=15/16` and `2||c-1/2||_W=15/8>1`. Thus PR39's small-Wiener hypothesis fails.

For `g(theta)=(1/64) cos(2 pi theta)`, `g_hat(1)=1/128`, so `gamma=2^-14`. With `mu=1/2`,

```text
C_k = gamma^2/[4 mu^2(1-mu^2)] = 1/(3*2^26),
alpha_k = C_k/2 = 1/(3*2^27),
```

matching line 446. The elementary legality radius in lines 449-453 is also correct.

## Remaining Scope

The whole-legal-interval problem remains `OPEN`, as the theorem itself states in lines 5, 50, and 471-473. This review accepts only the local finite-range theorem and its local quartic strict concavity conclusion.

No novelty verdict beyond the stated PR39 scope separation is made here. The RPF and negative-association inputs are known tools; the reviewed claim is that the file's assembled proof establishes the local finite-range theorem under the stated assumptions.

Recommended non-critical edits before publication:

1. In Section 5, replace "the convergence holds in a Holder norm" with an explicit `0<b<a` fixed Holder space and one interpolation sentence.
2. In Section 6, cite Kloeckner-Lopes-Stadlbauer for the full-shift spectral gap and Giulietti-Kloeckner-Lopes-Marcon for analytic dependence, while noting that the latter assumes H3-H4 rather than proving them.
3. Rename Section 7 heading to "The linear term in `s` vanishes" or "The `t^2` term vanishes."

These are exposition repairs, not correctness blockers.
