# W2 PR34 radial quartic audit

Status: ACCEPTED_SCOPED, head-bound to W2 PR34
`838c20b12907d94a9d6e023cc03f48c3f3b36c5c`.

## Accepted scope

Let `f:T=R/Z -> [0,1]` be bounded measurable and real-valued, let
`p = integral f`, and put `u=f-p`. Assume `0<p<1`. For every integer
`k>=1` with `c_k = fhat(k) != 0`, define

```text
I = { s in R : 0 <= p+s u <= 1 almost everywhere }.
```

Then

```text
Phi_k(s) = h(p+s(f-p)) + (4/3) |c_k|^4 s^4
```

is concave on all of `I`, including feasible boundary symbols. Equivalently,
for `m=(1-lambda)s0+lambda s1`,

```text
h(f_m) - (1-lambda)h(f_s0) - lambda h(f_s1)
 >= (4/3)|c_k|^4 ((1-lambda)s0^4 + lambda s1^4 - m^4).
```

If `f` is nonconstant, some nonzero Fourier coefficient exists, so this gives
strict entropy-rate concavity along the nontrivial constant-centered radial
line. If `f` is constant, all such coefficients vanish and the quartic
strengthening is vacuous.

Writing `M=ess sup u` and `m0=ess inf u`, the feasible interval is exactly
`R` when `u=0`. For nonzero mean-zero `u`, one has `M>0` and `m0<0`, and

```text
I = [
  max(-p/M, (1-p)/m0),
  min((1-p)/M, -p/m0)
].
```

The endpoints are understood in the essential-bound sense. At an endpoint the
symbol may touch `0` or `1`; the proof uses finite Jensen inequalities plus
continuity, not boundary derivatives.

## Proof audit

The product-refresh backbone is sound. In W2 lines 31-60, the commuting
idempotents `E_i` give the polynomial identities
`s P_s' = sum_i (I-E_i)P_s` and
`s^2 P_s'' = sum_{i != j}(I-E_i)(I-E_j)P_s`. These identities remain valid
as polynomial identities outside the Markov-channel range; probabilistic
interpretation is only used on `0<=s<=1`.

The Jeffreys-relative-entropy curvature calculation in W2 lines 115-180 has
the right sign and constants. The first derivative is
`D_s' = s^{-1} sum_i J(P_s,E_iP_s)`. Differentiating a fixed `i` term gives
`J + chi^2(E_iP_s || P_s)` in its own coordinate and a nonnegative symmetric
Dirichlet/Jeffreys dissipation in every other coordinate. The `J` term cancels
the derivative of `1/s`, yielding

```text
-H(P_s)'' =
s^{-2} [ sum_i chi^2(E_iP_s||P_s)
       + sum_{i != j} E_j^sym(P_s,E_iP_s) ] >= 0.
```

There is no missing factor `1/2`; the off-diagonal sum is over ordered pairs.
The denominator in the chi-square term is correctly `P_s`.

The finite DPP transfer is also sound. W2 lines 198-245 identify independent
Bernoulli replacement with the affine kernel `A+s(K-A)` through all inclusion
moments, then inclusion-exclusion determines the full event law. The extension
to real `s` is by polynomial identity, while differentiability is used only at
strictly positive finite laws. Strict finite kernels have full event support by
the `L=(I-B)^{-1}B` argument, and feasible boundaries are reached by continuity.

The entropy-rate passage is valid. W2 lines 246-274 use finite-window Jensen
inequalities, divide by `n`, and take three pointwise subadditive entropy-rate
limits. No derivative, infimum, or entropy-rate limit is interchanged.

The quartic estimate in W2 lines 291-333 is correct. For a pair at distance
`k`, the two-point marginal differs from the product Bernoulli pair by

```text
(-s^2 gamma, +s^2 gamma, +s^2 gamma, -s^2 gamma),
gamma = |c_k|^2.
```

Thus its `L1` distance is `4 s^2 gamma`. Marginal contraction of `L1` and
Cauchy-Schwarz give

```text
chi^2(E_iP_s || P_s) >= 16 s^4 gamma^2
```

for every `i=1,...,n-k`. Dropping all other nonnegative curvature terms gives

```text
-H_n(f_s)'' >= 16 (n-k) s^2 gamma^2.
```

Since `d^2/ds^2 [(4/3)(n-k)gamma^2 s^4] = 16(n-k)gamma^2 s^2`, the finite
function `H_n(f_s)+(4/3)(n-k)gamma^2s^4` is concave. Dividing by `n` and
passing to the entropy-rate limit sends `(n-k)/n` to `1`, giving the stated
constant `(4/3)|c_k|^4`. The argument handles `s=0` by finite smoothness and
handles feasible endpoints by continuity of finite event entropies before the
rate limit.

The off-origin issue is clean. W2 proves concavity on the whole strict
feasible interval directly from the curvature formula. C3 PR29 instead proves
one-sided rays from the diagonal center using the product channel and joins the
positive and negative halves at the origin by matching derivatives; that is
enough for C3's finite and rate statements, but it is not a second independent
proof of the W2 quartic bound.

The entrywise-Hessian-versus-PSD trap is avoided. C3 PR29 lines 57-69 use
entrywise nonnegative Hessian entries only along the simultaneous retention
direction, where the second derivative is the sum of entries. C3 explicitly
does not infer positive semidefiniteness for arbitrary signed parameter
directions. W2's quartic argument does not rely on such a PSD inference.

## Shared-backbone accounting with C3 PR29

C3 PR29 and W2 PR34 share the same theorem backbone:

1. independent coordinate replacement by product Bernoulli variables;
2. exact identification of the output law with a DPP affine line through a
   diagonal or constant kernel;
3. finite entropy concavity along that line;
4. entropy-rate concavity by finite Jensen inequalities and subadditive limits.

This shared product-refresh finite/rate concavity theorem should count once,
with C3 PR29 as the main author's scoped radial theorem and W2 PR34 as a later
extension using the same backbone.

W2 PR34 adds a genuine quantitative strengthening over C3 in the mean-preserving
constant-centered scalar case: the Fourier-mode two-point estimate produces the
quartic correction with the exact proof constant `(4/3)|fhat(k)|^4` from the
available curvature lower bound. This audit does not claim that constant is
globally optimal. The strengthening is separate from the shared backbone, but it
depends on the same product-refresh theorem infrastructure.

## Limits and exclusions

This audit does not certify arbitrary scalar chords `h((1-t)f+tg)` when the
line does not pass through a constant symbol. It does not certify affine
directions based at a non-diagonal finite kernel. It also does not establish
the full Lyons-Steif conjecture. No Lean or other formal proof check was run;
the acceptance is a line-by-line natural-language proof audit.
