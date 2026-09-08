# Proof candidate and distance notes

AUTHOR STATUS: PROOF_CANDIDATE_FOR_P4; GENERAL_CONNECTED_INCOMPLETE.

## 1. Imported base from U4

At a strict diagonal `X=diag(x)`, with zero-diagonal off-diagonal coordinates
`z_ij`, write

```text
a_S = prod_{i in S} x_i prod_{i notin S}(1-x_i),
zeta_i(S) = 1/x_i              if i in S,
          = -1/(1-x_i)         if i notin S.
```

The exact atom likelihood has the character expansion

```text
p_S(X+Z)/a_S = 1 + R_S(Z),
R_S(Z) = sum_{|T|>=2} det(Z_T) zeta_T(S).
```

The entropy expansion begins

```text
H(X+Z)-H(X)
  = -1/2 E R^2 + 1/6 E R^3 - 1/12 E R^4 + ...
```

because exact atom mass and all singleton marginals are fixed by
zero-diagonal perturbations.  U4 proved the complete degree-six part and the
diameter-two theorem.

## 2. P4 off-diagonal scales

Consider the path support

```text
1 -- 2 -- 3 -- 4
```

with nonzero weights

```text
z_12 = epsilon a,   z_23 = epsilon b,   z_34 = epsilon c.
```

The upper-triangle off-diagonal coordinates have graph distances

```text
d(12)=d(23)=d(34)=1,
d(13)=d(24)=2,
d(14)=3.
```

Use the anisotropic scaling

```text
S_epsilon = diag(
  I_x,
  |epsilon|^-1 on {12,23,34},
  |epsilon|^-2 on {13,24},
  |epsilon|^-3 on {14}
).
```

The diagonal-coordinate block is `-diag(w_i)+O(epsilon^4)`, and the
diagonal/off-diagonal blocks vanish after this scaling.  Thus the new task is
the scaled off-diagonal Hessian.

## 3. The P4 scaled limit

The scaled off-diagonal limit is diagonal:

```text
lim_{epsilon->0} S_off^T Hess_off H(X+epsilon A) S_off

= -diag(
  6 w1 w2 a^2,
  6 w1 w2 w3 a^2 b^2,
  6 w1 w2 w3 w4 a^2 b^2 c^2,
  6 w2 w3 b^2,
  6 w2 w3 w4 b^2 c^2,
  6 w3 w4 c^2
)
```

in edge order

```text
(12), (13), (14), (23), (24), (34).
```

All entries are strictly negative because `0<x_i<1` and `a,b,c` are nonzero.
The congruence scaling is invertible for `epsilon != 0`, so for all sufficiently
small nonzero `epsilon` the full Hessian is negative definite.

Consequently P4 support succeeds.  Since every connected graph on four
vertices is either diameter at most two or a relabelled P4, U4 plus this
candidate gives the `n=4` connected iff classification.

## 4. Why the endpoint coefficient is `-6`

For the endpoint chord `y=z_14`, restrict temporarily to the four-cycle
variables

```text
z_12=a, z_23=b, z_34=c, z_14=y
```

only to compute the leading monomial.  For the four vertices,

```text
R2 = -(a^2 zeta12 + b^2 zeta23 + c^2 zeta34 + y^2 zeta14),
R4 = (a^2 c^2 + b^2 y^2 - 2abcy) zeta1234.
```

The coefficient of `a^2 b^2 c^2 y^2` in the entropy expansion is:

- from `-1/2 E R4^2`: `-3 prod_i w_i`;
- from `+1/6 E R^3`, equivalently `+1/2 E R2^2 R4`: `+2 prod_i w_i`;
- from `-1/12 E R2^4`: `-2 prod_i w_i`.

The total entropy coefficient is therefore `-3 prod_i w_i`, and two
derivatives in `y` give

```text
H_{14,14} = -6 w1 w2 w3 w4 a^2 b^2 c^2 epsilon^6
            + O(epsilon^7).
```

The distance-two and supported-edge coefficients are exactly the U4
`epsilon^4` and `epsilon^2` formulas.  The exact extraction in
`connected_distance_scout.py` checks that no off-diagonal mixed entry has a
nonzero coefficient at the scale `epsilon^(d(e)+d(f))` for P4.

## 5. General shortest-path diagonal rule

The P4 endpoint computation suggests the following rule.  Let `ij` be any
coordinate pair and let `d=d_G(i,j)`.  Then the first nonzero diagonal Hessian
term in the `ij` coordinate should be

```text
-6 epsilon^(2d)
  sum_{P in SP_d(i,j)}
    (prod_{v in P} w_v) (prod_{e in P} A_e^2).
```

Heuristic derivation:

1. A monomial containing one marked `z_ij` must close a cycle consisting of
   `ij` plus an `i`-to-`j` support path.  Therefore its support degree is at
   least `d`.
2. In the entropy second derivative, the first possible `z_ij^2` term uses two
   copies of a shortest path, hence order `epsilon^(2d)`.
3. Character orthogonality kills cross terms whose shortest paths use different
   vertex sets.  For shortest paths, the surviving contributions are squares
   of path-weight products and hence have the sign above.
4. Exact checks through distance four match the universal coefficient `-6`.

This is not yet a theorem.  The missing general proof is a diagram identity:
for every simple shortest cycle, the connected entropy coefficient of the
product of all squared cycle edges should be `-3 prod_v w_v`, and all mixed
same-scale diagrams must assemble into a negative-definite block.

## 6. Why the general connected theorem remains open

Negative diagonal entries at the distance scale are not enough.  The
multi-scale congruence for a general connected graph would require, for every
distance level `r`, a limiting block indexed by all pairs at distance `r`.
This block may have off-diagonal entries from overlapping shortest-path
diagrams.  I do not yet have a proof that every such block is negative
definite for arbitrary connected support and arbitrary nonzero real weights.

Thus the current state is:

- P4 full Hessian: proof candidate closed.
- `n=4` connected iff: proof candidate, relying on U4 plus P4.
- General connected support: INCOMPLETE.
