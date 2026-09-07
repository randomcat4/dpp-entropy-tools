# Small-kernel two-point strict concavity theorem

Status: PROVED.

## Statement

Let `A_+` and `A_-` be fixed real symmetric positive semidefinite `n x n`
matrices, and let

```text
A_0 = (A_+ + A_-)/2.
```

For all sufficiently small `eps>0`, the matrices `eps A_sigma` are DPP
marginal kernels because

```text
0 <= eps A_sigma <= I
```

whenever

```text
eps <= 1 / max_sigma ||A_sigma||_op
```

with the zero-matrix case interpreted in the obvious way.

If `A_+ != A_-`, then for all sufficiently small positive `eps`,

```text
[H(eps A_+) + H(eps A_-)]/2 - H(eps A_0) < 0.
```

Here `H` is the full exact-event DPP Shannon entropy.

## Exact small-kernel expansion

For a fixed PSD matrix `A=(a_ij)`, write

```text
a_i = a_ii,
T = sum_i a_i,
d_ij = a_i a_j - a_ij^2 >= 0.
```

The Mobius exact-event law gives

```text
p_empty
  = 1 - eps T + eps^2 sum_{i<j} d_ij + O(eps^3),

p_i
  = eps a_i - eps^2 sum_{j != i} d_ij + O(eps^3),

p_ij
  = eps^2 d_ij + O(eps^3),

sum_{|S|>=3} p_S = O(eps^3).
```

All constants depend only on the fixed matrix `A` and `n`.

If `a_i=0`, PSD implies the entire `i`-th row and column of `A` vanish:
`|a_ij|^2 <= a_i a_j=0`.  Thus every event containing `i` has zero leading
terms, and the convention `0 log 0=0` is continuous.  If `d_ij=0` with
`a_i a_j>0`, then `d_ij log(a_i a_j/d_ij)` is interpreted by its limit `0`.
If `a_i a_j=0`, PSD again forces `d_ij=0`.

Therefore

```text
H(eps A)
 = eps [ T log(1/eps) + T - sum_i a_i log a_i ]
   + eps^2 [
       -T^2/2
       + sum_{i<j} d_ij (1 + log(a_i a_j / d_ij))
     ]
   + O(eps^3 log(1/eps)).                            (1)
```

The remainder is uniform for the fixed triple `A_+,A_-,A_0`: take the maximum
of the three fixed constants after choosing `eps` small enough that all
nonzero leading singleton and pair probabilities stay within a fixed relative
neighborhood of their leading terms; all zero-leading events are bounded by
`O(eps^3)` and contribute `O(eps^3 log(1/eps))`.

## Case 1: diagonals differ

The terms `eps T log(1/eps)` and `eps T` are affine in `A`, so they cancel in
the midpoint gap.  The first non-affine term is

```text
-eps sum_i a_i log a_i.
```

The function `f(a)=a log a`, with `f(0)=0`, is strictly convex on
`[0,infty)`.  If the diagonal vectors of `A_+` and `A_-` differ, then

```text
sum_i f((a_i^+ + a_i^-)/2)
  < (1/2) sum_i [f(a_i^+) + f(a_i^-)].
```

Hence

```text
[H(eps A_+) + H(eps A_-)]/2 - H(eps A_0)
  = -eps * positive_constant + O(eps^2 log(1/eps)) < 0
```

for all sufficiently small `eps`.

This includes boundary cases where one diagonal entry is zero and the other is
positive; strict convexity remains valid at the endpoint by continuity and the
right derivative `f'(a)=1+log a` tends to `-infty` as `a downarrow 0`.

## Case 2: diagonals agree

Assume now `a_i^+=a_i^-=a_i^0=a_i` for every `i`.  Then `T` and
`sum_i a_i log a_i` are the same for all three matrices, so the order-`eps`
terms in (1) cancel exactly.

For a fixed pair `(i,j)`, put `Aij=a_i a_j`.  If `Aij=0`, PSD forces
`a_ij^+=a_ij^-=a_ij^0=0`, so the pair contributes nothing and cannot hide a
boundary exception.

Assume `Aij>0`.  Let

```text
d_ij^sigma = Aij - (a_ij^sigma)^2,
d_ij^0     = Aij - (a_ij^0)^2,
a_ij^0     = (a_ij^+ + a_ij^-)/2.
```

Then

```text
(d_ij^+ + d_ij^-)/2
  = d_ij^0 - ((a_ij^+ - a_ij^-)/2)^2
  <= d_ij^0.                                           (2)
```

Define

```text
g_A(d)=d(1+log(A/d)) for 0<d<=A,  g_A(0)=0.
```

On `(0,A]`,

```text
g_A'(d)=log(A/d) >=0,
g_A''(d)=-1/d <0.
```

Thus `g_A` is increasing and strictly concave on `[0,A]`, with the endpoint
`d=0` handled by continuity.  Using concavity and then monotonicity,

```text
[g_A(d_ij^+) + g_A(d_ij^-)]/2
  <= g_A((d_ij^+ + d_ij^-)/2)
  <= g_A(d_ij^0).                                      (3)
```

If `a_ij^+ != a_ij^-`, then the second inequality in (3) is strict because
`Aij>0` and (2) is strict.  Therefore the pair's averaged second-order
coefficient is strictly smaller than the midpoint coefficient.

Since `A_+ != A_-` and the diagonals agree, some off-diagonal pair differs.
For that pair `Aij` must be positive by PSD, otherwise the off-diagonal entry
would be forced to zero.  Summing (3) over all pairs gives a strictly negative
second-order entropy gap:

```text
[H(eps A_+) + H(eps A_-)]/2 - H(eps A_0)
  = -eps^2 * positive_constant + O(eps^3 log(1/eps)) < 0
```

for all sufficiently small `eps`.

This proves the theorem in all PSD cases, including singular matrices and
vanishing `2 x 2` determinants.


