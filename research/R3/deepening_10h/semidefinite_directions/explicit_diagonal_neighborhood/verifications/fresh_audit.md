# D10-S6 fresh non-author audit

STATUS: CORRECT.

Scope audited: `explicit_diagonal_neighborhood/frozen_problem.md`,
`proof_candidate.md`, and `verdict.md`, plus an independent small-dimensional
sanity script in this `verifications/` directory.  I did not modify the author
files or any shared index.

## Verdict

The explicit-radius theorem is correct as stated, with the intended natural-log
Shannon entropy convention and with the strict DPP kernel domain
`0<K<I` retained.  The radius is extremely conservative and proves only a local
diagonal-box neighborhood, not any global PSD/NSD concavity theorem.

The proof's most load-bearing estimates all check:

1. the exact atom determinant formula follows from Möbius inversion;
2. `||A_S(K)||_op <= 1` holds for strict contractions;
3. the first, second, and third mixed determinant derivative counts are
   `n`, `n(n-1)`, and `n(n-1)(n-2)` with no missing factorial;
4. the third chain rule for `f(p)=-p log p` has the stated coefficients;
5. summing over all `2^n` atoms gives the advertised `L`;
6. the segment atom floor follows from `||K-X||_F <= q/(2n)`;
7. the PSD/NSD diagonal trace inequality is valid, including singular
   directions;
8. `delta=min(q/(2n),2/(nL))` gives
   `H''_K[D,D] <= -2||D||_F^2/n`.

## Details checked

### Exact atom formula

For `C=S^c`, Möbius inversion of inclusion probabilities gives

```text
p_S(K) = sum_{A subset C} (-1)^|A| det K_{S union A}.
```

Expanding `det(K-I_C)` by choosing the `-1` diagonal entries on indices in
`C\A` gives

```text
det(K-I_C) = sum_{A subset C} (-1)^{|C|-|A|} det K_{S union A}.
```

Multiplication by `(-1)^|C|` yields the author's formula
`p_S(K)=(-1)^|S^c| det(K-I_{S^c})`.

### Operator norm bound

For `A_S(K)=K-I_{S^c}` and a unit vector `v`,

```text
v^T A_S(K) v = v^T K v - ||P_{S^c}v||^2.
```

Since `0<K<I`, the right side is between `-1` and `1`.  As `A_S(K)` is
symmetric, this proves `||A_S(K)||_op <= 1`.  The same argument applies all
along the segment `X+u(K-X)` because the strict contraction cone is convex.

### Determinant derivative counts

Column multilinearity gives the following ordered replacement counts for
Frechet derivatives:

```text
Dp[E]        : n choices;
D^2p[E,D]   : n(n-1) ordered choices;
D^2p[D,D]   : n(n-1) ordered choices;
D^3p[E,D,D] : n(n-1)(n-2) ordered choices.
```

Hadamard's determinant bound then gives the author's estimates because every
unchanged column has norm at most `1`, while every replaced column has norm at
most the Frobenius norm of its direction.  The second and third derivative
counts already include the factorials from differentiating the polynomial
coefficient, so there is no missing factor of `2` or `6`.

### Chain-rule coefficient

For `f(p)=-p log p`,

```text
f'(p)=-(1+log p),  f''(p)=-1/p,  f'''(p)=1/p^2.
```

The mixed third derivative is

```text
D^3(f∘p)[E,D,D]
 = f''' p_E p_D^2
 + f''(2 p_ED p_D + p_E p_DD)
 + f' p_EDD.
```

This matches the proof.  On `m <= p <= 1`, the absolute values are bounded by
`1/m^2`, `1/m`, and
`ell=max(1, |1+log m|)`, so the stated one-atom bound follows.  Summing over
`2^n` exact atoms gives exactly the displayed `L`.

### Segment floor and final radius

At `X=diag(x)`, every atom is at least
`q=s^n`, where `s=min(a,1-b)`.  Along the segment from `X` to `K`,

```text
|Dp_S[E]| <= n||E||_F,
```

so `||E||_F <= q/(2n)` implies every segment atom is at least `m=q/2`.  This
is the only place where positivity of all exact atoms is needed before applying
the log derivative bound.

The Hessian comparison is then

```text
|H''_K[D,D]-H''_X[D,D]| <= L ||K-X||_F ||D||_F^2.
```

The second part of the radius, `||K-X||_F <= 2/(nL)`, makes this at most
`2||D||_F^2/n`.

### PSD/NSD diagonal margin

At a diagonal kernel,

```text
H''_X[D,D] = - sum_i D_ii^2/(x_i(1-x_i)).
```

For `D >= 0`,

```text
sum_i D_ii^2 >= (tr D)^2/n >= tr(D^2)/n = ||D||_F^2/n.
```

The same applies to `-D` when `D <= 0`.  Since `x_i(1-x_i) <= 1/4`,

```text
H''_X[D,D] <= -4||D||_F^2/n.
```

Combining this with the perturbation loss above proves

```text
H''_K[D,D] <= -2||D||_F^2/n < 0
```

for every nonzero PSD or NSD direction.

## Boundary and vulnerability audit

- The theorem is local: `K` must be both strict (`0<K<I`) and within the
  explicit Frobenius ball.  The ball itself is not claimed to lie inside the
  strict kernel domain.
- The diagonal box must be understood as nonempty; if not, the statement is
  vacuous.  With `0<a<=x_i<=b<1`, the used quantity `s=min(a,1-b)` is positive.
- The proof uses only worst-case atom and determinant bounds.  No finite
  experiment is used as proof.
- Singular PSD/NSD directions are covered by the trace argument; no invertibility
  of `D` is used.
- No extension to indefinite directions follows from this argument.

No critical gap was found.

## Independent sanity

I wrote and ran `fresh_sanity.py` using only standard-library exact rational
arithmetic for determinants and exact symbolic cancellation at diagonal kernels.

Command:

```text
python fresh_sanity.py
```

Actual run used the bundled workspace Python from the repo root and wrote
`fresh_sanity_results.json`.

Checks performed:

- Möbius exact atoms equal `(-1)^|S^c| det(K-I_{S^c})` for generic rational
  `n=2,3,4` examples.
- At diagonal kernels, the `p'' log p` part cancels exactly through total mass
  and singleton marginal second-derivative identities for `n=2,3,4`; the
  remaining rational Hessian equals
  `-sum_i D_ii^2/(x_i(1-x_i))`.
- Nontrivial rational `n=2,3` kernels inside the explicit radius satisfy the
  advertised PSD curvature bound.

Result file: `fresh_sanity_results.json`, status `PASS`.
