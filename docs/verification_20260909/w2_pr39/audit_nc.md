# PR39 NC theorem audit

Verdict: ACCEPTED_SCOPED.

This audit is bound to public PR 39, head `5558a6b22ef8eb080d198d4af6b1a5cfe2fb164f`, branch
`research/W2-nonconstant-orbit-20260909`.

Audited theorem only: NC, the nonconstant half-period-even Wiener center theorem
in `frozen_statement.md` lines 7-16 and `proof.md` sections 3-7. This audit
does not certify NC-channel or recertify the earlier PR34 cyclic theorem.

Frozen local inputs:

- `pr39_frozen_statement.md`
- `pr39_proof.md`
- `source_binding.json`

## Scope accepted

For real `c,g in W(T)` with

```text
c(theta+1/2)=c(theta),     int c = 1/2,
g(theta+1/2)=-g(theta),    g != 0,
a=2||c-1/2||_W < 1,       b=2||g||_W > 0,
R=(1-a)/(2b),              rho=(1+a)/2,
M=-log(1-rho)-rho,
```

and for any odd `k >= 1` with

```text
gamma = |hat g(k)|^2 > 0,
T_* = min{ R/2, 2 gamma R^3 / sqrt(27M) },
```

the proof establishes, for every `n >= 2k`,

```text
t -> H_n(c+tg) + (2/3)(n-2k) gamma^2 t^4
```

is concave on `[-T_*,T_*]`. Passing finite Jensen inequalities to entropy
rates gives

```text
t -> h(c+tg) + (2/3)|hat g(k)|^4 t^4
```

concave on the same interval. Since `gamma=|hat g(k)|^2`, the rate correction
is exactly `(2/3) gamma^2 t^4`.

## Load-bearing checks

1. Boolean exact event identity is correct. In `proof.md` lines 143-156, for
`K=(I+B)/2` with `diag B=0`, the signed event formula gives

```text
P_K(X=S)=2^{-n} det(I+D_sigma B).
```

The row extraction is valid: `K-I_{S^c}=(1/2)D_sigma(I+D_sigma B)`, and the
outside sign cancels `det D_sigma`. Lines 158-170 then give the exact Boolean
Fourier identity

```text
sum_sigma p_B(sigma) prod_{i in U} sigma_i = det B_U
```

by character orthogonality. This remains a polynomial identity for complex
`B`; no positivity is used at complex parameters.

2. The log-det walk expansion is sound. Lines 177-190 define `F_n(z)` through
the convergent log-det series when the absolute row sum is at most `rho<1`,
and identify it with `n log 2 - H(K(z))` for real strictly feasible `z`.
Lines 193-199 correctly expand traces into closed walks. The product of
signs along a closed walk is the Boolean character of the set of vertices
visited an odd number of times, so (3.3) contributes `det B_{O(w)}`. Repeated
vertices are handled by parity of visits, not by pretending the walk is
self-avoiding.

3. The analytic volume bound is linear in `n`. Lines 202-213 use Hadamard's
row-norm bound `|det B_U| <= rho^{|U|} <= 1` and the nonnegative matrix
`E=|B|` with row sums at most `rho`. Then

```text
sum closed walks length ell prod |B_edges| = tr E^ell <= n rho^ell,
```

so

```text
|F_n(z)| <= n sum_{ell>=2} rho^ell/ell = nM.
```

This is the needed `nM` bound with radius and constants independent of `n`.

4. The Wiener hypotheses supply the uniform disk. Lines 221-231 set
`B_n(z)=2K_{c-1/2+zg}`. The finite-window row sum is bounded by
`a+b|z|`, hence by `rho` on `|z|<=R`. For real `|t|<=R`, the symbol lies in a
strict subinterval of `(0,1)`, so the Shannon entropy is analytic and all
finite probabilities are positive.

5. The first nonzero relative-entropy term is order four. Lines 237-252 use
the half-period symmetry to show exact evenness in `t`, and the parity-block
marginals are fixed. At `t=0`, the parity blocks are independent, so

```text
D_n(t)=H_n(c)-H_n(c+tg)=D(P_t||P_c).
```

Since `P_t=P_c+O(t^2)` and the first variation of KL at its base point is
zero, `D_n(t)=O(t^4)`. Cauchy's formula applied to `F_n`, not to
`F_n-F_n(0)` with an added factor, gives for `j>=3`

```text
|A_{2j,n}| <= nM R^{-2j}.
```

6. The fourth coefficient uses the exact Bernoulli KL constant. Lines 258-281
apply Lyons negative association to a vertex-disjoint matching of length-`k`
cross-parity edges. For each edge,

```text
E_Q Z_e = 1/4,
E_{P_t} Z_e = 1/4 - gamma t^2.
```

The variational bound gives

```text
D_n(t) >= m_n d(1/4 - gamma t^2 || 1/4).
```

The exact expansion is

```text
d(1/4-delta || 1/4)
  = delta^2 / (2*(1/4)*(3/4)) + O(delta^3)
  = (8/3) delta^2 + O(delta^3),
```

with `delta=gamma t^2`. Therefore lines 285-289 correctly obtain

```text
A_{4,n} >= (8/3)m_n gamma^2 >= (4/3)(n-k)gamma^2.
```

This is the necessary stronger coefficient; the proof does not use the older
Pinsker-level coefficient.

7. The matching count and endpoint `n=2k` are handled. The step-`k` chains
lose at most one vertex per nonempty chain, giving `m_n >= (n-k)/2`. The
theorem assumes `n>=2k`; the final bound becomes nonnegative at the endpoint
`n=2k`, so finite concavity still follows there.

8. The Cauchy tail constant is sufficient. With `x=|t|/R <= 1/2`, lines
297-306 bound

```text
sum_{j>=3}(2j)(2j-1)|A_{2j,n}||t|^{2j-2}
 <= (54 n M/R^6)t^4.
```

The exact endpoint value of the positive coefficient series is
`1424/27<54`, so the stated constant is conservative and valid.

9. The stated `T_*` gives the advertised tail margin. From

```text
|t| <= 2 gamma R^3 / sqrt(27M)
```

one gets

```text
54M t^2/R^6 <= 8 gamma^2.
```

Combining the fourth term and the tail gives lines 311-318:

```text
D_n''(t)
 >= 16(n-k)gamma^2 t^2 - 8n gamma^2 t^2
 = 8(n-2k)gamma^2 t^2.
```

Since `D_n=H_n(c)-H_n(c+tg)`, this is exactly
`-H_n(c+tg)'' >= 8(n-2k)gamma^2 t^2`.

10. The finite correction has the correct second derivative. The added term

```text
(2/3)(n-2k)gamma^2 t^4
```

has second derivative `8(n-2k)gamma^2 t^2`, so line 322 correctly concludes
finite concavity on `[-T_*,T_*]`.

11. The entropy-rate passage does not swap derivatives and limits. Line 324
first applies finite Jensen to the concave corrected finite-window functions,
then divides by `n` and uses the stationary subadditive entropy-rate limit for
the three fixed symbols. Since `(n-2k)/n -> 1`, the finite correction passes to
the rate correction `(2/3)gamma^2`. No `n`-dependent symbol, radius, or
derivative limit is introduced.

## Hazards checked

- Complex parameters are used only for analytic coefficient control, not as
probabilities.
- The walk expansion includes repeated visits through `O(w)`, the odd-visit
set.
- The high-order coefficients are not assumed nonnegative.
- The radius `R`, tail bound `M`, and interval `T_*` do not depend on `n`.
- The proof explicitly uses the exact Bernoulli KL coefficient `8/3`, leading
to `16(n-k)gamma^2 t^2` before the tail subtraction.
- The endpoint `n=2k` is included with zero finite correction.
- The theorem is limited to the small Wiener-norm interval; it does not prove
the whole legal chord.

## External source used

Russell Lyons, "Determinantal Probability Measures", arXiv:math/0204325v4,
Theorem 8.1, for negative association of finite Hermitian positive-contraction
DPPs:

https://arxiv.org/pdf/math/0204325

Final status: ACCEPTED_SCOPED for PR39 theorem NC only. No load-bearing gap was
found in the Boolean event identity, analytic walk bound, fourth coefficient,
Cauchy tail constants, finite-to-rate passage, or the `n>=2k` endpoint.
