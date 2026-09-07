# T1 definitions and condition audit

Status: bounded audit only. This file records definitions, identities, and proof obligations for finite DPP entropy curvature. It does not certify any T1 sign criterion or final theorem.

I used only the public repository instructions, the T1 prompt, and external primary/standard references listed in `prior_art_conditions.md`. I did not read sibling route drafts.

## 1. Finite DPP event probabilities

Let `E={1,...,n}`. A finite marginal-kernel DPP is a probability law on subsets `Y subset E` with

```text
Pr[A subset Y] = det(K_A)             for all A subset E,
```

where `K` is Hermitian and `0 <= K <= I`. This is the standard finite positive-contraction condition. For exact atoms,

```text
p_S(K) := Pr[Y=S]
       = sum_{B subset E\S} (-1)^|B| det(K_{S union B})
       = (-1)^|E\S| det(K - I_{E\S}).
```

Here `I_{E\S}` means the diagonal matrix with `1` on the complement of `S` and `0` on `S`. The first equality after `p_S` is just Möbius inversion from the inclusion probabilities; the determinant formula is the same inversion packed into one determinant.

If `0 < K < I`, one can also set

```text
L = K(I-K)^(-1),       p_S(K) = det(L_S) / det(I+L).
```

This `L`-ensemble formula is often the safest way to reason about positivity, because a positive definite `L` has all principal minors positive.

Classification for T1:

- `Pr[A subset Y]=det(K_A)` is the DPP definition.
- The exact atom formula for `p_S(K)` is an identity once the DPP is fixed.
- The `L`-ensemble formula is an identity on the open set `0<K<I`; it should not be used at boundary points without a limiting argument.

## 2. Interior positivity

For a finite Hermitian DPP,

```text
p_S(K)>0 for every S subset E     iff     0 < K < I.
```

Proof check:

- If `0<K<I`, then `L=K(I-K)^(-1)` is positive definite. Every principal minor `det(L_S)` is positive, with `det(L_emptyset)=1`, so every atom is positive.
- If all atoms are positive, then `p_E=det(K)>0`, so `K` has no zero eigenvalue. Also `p_emptyset=det(I-K)>0`, so `K` has no eigenvalue `1`. Since a marginal DPP already has `0<=K<=I`, this gives `0<K<I`.

Classification for T1: this is a basic condition check, not a new entropy-curvature tool.

## 3. Hermitian affine feasible directions

For an affine path

```text
K(t) = K0 + tD,
```

the path remains inside the Hermitian marginal-kernel domain only if `D` is Hermitian. If `0<K0<I`, then every Hermitian `D` is locally feasible: by Weyl eigenvalue continuity, `K0+tD` stays between `0` and `I` for all sufficiently small `|t|`.

At boundary points, this is no longer true. For a two-sided affine interval around `0`, the PSD constraints force `D` to stay in the minimal face of both cones:

```text
D v = 0 for v in ker(K0),
D v = 0 for v in ker(I-K0).
```

Equivalently, `D` may act only on the spectral subspace where `0<lambda(K0)<1`. A one-sided path has tangent-cone inequalities instead of these equalities, but off-face blocks still need checking; a diagonal first-order inequality alone is not enough.

Classification for T1:

- Interior local feasibility is a matrix-convexity fact.
- Boundary feasibility is a separate condition and must be checked before using entropy asymptotics.
- A proposed curvature theorem that quantifies over "all Hermitian directions" is valid only at interior kernels unless it states the boundary tangent condition.

## 4. Entropy and the second derivative identity

On the open atom simplex, define

```text
H(K) = - sum_{S subset E} p_S(K) log p_S(K).
```

For any smooth path `K(t)` whose atoms stay positive,

```text
H'(t)  = - sum_S p'_S(t) log p_S(t),
H''(t) = - sum_S (p'_S(t))^2 / p_S(t)
          - sum_S p''_S(t) log p_S(t).
```

The missing `+1` terms vanish because `sum_S p_S(t)=1`, hence `sum_S p'_S(t)=sum_S p''_S(t)=0`.

The first term is the negative Fisher quadratic form of the induced curve in the full atom simplex. The second term is the acceleration term of the DPP atom map. It disappears only when the probability vector itself is affine in `t`, not merely when `K(t)` is affine.

Classification for T1:

- This decomposition is an identity and is explicitly marked by the T1 prompt as not a new tool.
- A structural criterion must control or eliminate the acceleration term under stated DPP/kernel/direction hypotheses.
- Concavity of Shannon entropy in mixture coordinates does not imply concavity of `H(K0+tD)` for a nonlinear DPP atom map.

## 5. Real center and pure-imaginary Hermitian directions

Suppose

```text
K0 is real symmetric,
D = iA, where A is real skew-symmetric.
```

Then `D` is Hermitian and

```text
K0 - tD = conjugate(K0 + tD).
```

For every principal determinant, and therefore for every exact atom from the Möbius formula,

```text
p_S(-t) = p_S(t).
```

Thus each atom has zero first derivative at the center:

```text
p'_S(0)=0.
```

If the center is interior, this gives

```text
H''(0) = - sum_S p''_S(0) log p_S(K0).
```

There is no Fisher-square contribution at `t=0`, but this does not determine the sign. The signs and weights of the second derivatives remain a genuine structural problem.

Classification for T1:

- The evenness and first-derivative cancellation are determinant/conjugation identities.
- The sign of `H''(0)` is not settled by the identity.
- The hypothesis is pointwise: it applies at real centers along pure-imaginary Hermitian directions. It does not apply to a general complex Hermitian kernel or a direction with a real component.

## 6. Boundary zero probabilities

At atoms with `p_S(K0)=0`, the open-simplex derivative formula cannot be used by substitution. The entropy convention `0 log 0=0` gives continuity of the term, but derivatives depend on the leading asymptotic of the atom probability.

If along an allowed one-sided or two-sided path

```text
p_S(t) = a t^r + higher order,       a>0,
```

then

```text
-p_S(t) log p_S(t)
  = -a t^r (log a + r log|t|) + higher order/log terms.
```

Consequences:

- If a one-sided path opens a zero atom linearly, first and second derivatives can have logarithmic and reciprocal singular terms.
- If a two-sided nonnegative path opens a zero atom quadratically, the second derivative can have a logarithmic divergence.
- If boundary feasibility forces the atom to remain zero to the relevant order, the singular term is absent.

Classification for T1:

- Boundary handling is not a cosmetic extension of the interior formula.
- Real-direction and pure-imaginary-direction boundary asymptotics must be separated.
- Any criterion using `p'_S` or `p''_S` at zero-probability atoms needs a leading-order support lemma, not just the interior identity.

## 7. Finite-window entropy versus entropy rate

For a finite window `Lambda`, the relevant object is

```text
H_Lambda = - sum_{S subset Lambda} p_S log p_S.
```

For a stationary infinite process, the entropy rate is a limit such as

```text
h = lim_{n->infty} H(Y_1,...,Y_n)/n,
```

when the limit exists. A finite-window curvature identity gives information about `H_Lambda` for fixed `Lambda`. It does not by itself prove a statement about the entropy rate as the window grows.

To transfer a curvature sign or second-derivative formula to an entropy rate, one needs extra analytic conditions, for example uniform convergence of difference quotients or a theorem justifying interchange of the window limit and differentiation. The T1 prompt's warning on this point is mathematically necessary.

Classification for T1:

- Finite-window formulas are finite-dimensional DPP identities.
- Entropy-rate claims are asymptotic process claims and need separate limit arguments.

## 8. Audit verdict on definition layer

The current safe baseline is:

```text
finite Hermitian K with 0<K<I,
Hermitian affine direction D,
small two-sided interval preserving 0<K(t)<I,
exact atoms from Möbius/L-ensemble formulas,
entropy differentiated only while all atoms remain positive.
```

Under these assumptions the event probabilities and entropy second derivative are well-defined and smooth. They provide a correct calculation framework, but not a sign criterion.

The following are not yet proved by definitions alone:

- any global sign of `H''(0)`;
- any sign from pure-imaginary symmetry beyond `p'_S(0)=0`;
- any boundary curvature rule without leading asymptotic control;
- any entropy-rate result from fixed-window calculations;
- any novelty claim relative to information geometry or known DPP Fisher-geometry literature.
