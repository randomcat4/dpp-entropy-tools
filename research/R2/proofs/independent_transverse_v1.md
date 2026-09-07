# Independent proof of the frozen transverse asymptotic

Status: PROVED for the public frozen theorem v1, with fixed finite
`(n,r,P,U,V,B,tau)`.

The proof below does not use the public author proof.

## 1. Exact event probabilities

Let `z=(z_1,...,z_n)` and `Z=diag(z_i)`.  Starting from the required
inclusion-exclusion event law,

```text
p_K(S) = sum_{T: S subset T subset E} (-1)^(|T|-|S|) det(K_T),
```

the probability generating polynomial is

```text
G_K(z) = sum_S p_K(S) prod_{i in S} z_i
       = sum_T det(K_T) prod_{i in T} (z_i-1)
       = det(I + K(Z-I)).
```

If `K=W Lambda W^T`, with `W` orthogonal and
`Lambda=diag(lambda_1,...,lambda_n)`, Sylvester's identity and Cauchy-Binet
give

```text
G_K(z)
 = det(I - Lambda + Lambda W^T Z W)
 = sum_J prod_{j in J} lambda_j prod_{j notin J}(1-lambda_j)
       det((W^T Z W)_J)
 = sum_J prod_{j in J} lambda_j prod_{j notin J}(1-lambda_j)
       sum_{|S|=|J|} det(W_{S,J})^2 prod_{i in S} z_i.
```

Therefore

```text
p_K(S) =
  sum_{J subset [n], |J|=|S|}
    det(W_{S,J})^2
    prod_{j in J} lambda_j
    prod_{j notin J} (1-lambda_j).          (1)
```

This is an exact-event formula equivalent to inclusion-exclusion.

## 2. Feasibility

Use the orthogonal basis `[U,V]`.  In this basis

```text
M_epsilon + tD =
 [ (1-epsilon) I_r    t B       ]
 [ t B^T              epsilon I_s ].
```

Take an SVD of `B`; orthogonal changes inside the `P` and `Q` ranges reduce
the matrix to independent `2 x 2` blocks

```text
[ 1-epsilon   t b_j ]
[ t b_j       epsilon ]
```

plus unpaired scalar blocks `1-epsilon` or `epsilon`.  A `2 x 2` block is
positive semidefinite exactly when

```text
t^2 b_j^2 <= epsilon(1-epsilon).
```

The complementary block `I-(M_epsilon+tD)` has the same determinant condition:

```text
[ epsilon     -t b_j     ]
[ -t b_j       1-epsilon ].
```

Hence

```text
0 <= M_epsilon+tD <= I
  iff |t| ||B||_op <= sqrt(epsilon(1-epsilon)).
```

Since the frozen endpoints use `t=t_epsilon=tau sqrt(epsilon(1-epsilon))`
and `tau ||B||_op < 1`, the endpoints are strict contractions.  If `B=0`, the
condition is vacuous and the endpoints equal `M_epsilon`.

## 3. The bound `Z <= ||B||_F^2`

Let

```text
xi = u_1 wedge ... wedge u_r
```

in `wedge^r R^n`.  Its coordinate on `e_S` is `psi_S=det(U_S)`.
The tangent vector induced by `U -> U+aVB^T` is

```text
eta =
  sum_{j=1}^r
    u_1 wedge ... wedge u_{j-1}
    wedge (V B^T e_j)
    wedge u_{j+1} wedge ... wedge u_r.
```

Its coordinate on `e_S` is exactly `phi_S`.  Expanding
`VB^T e_j = sum_alpha B_{j alpha} v_alpha`, the wedge vectors obtained by
replacing one `u_j` by one `v_alpha` form an orthonormal family.  Therefore

```text
sum_{|S|=r} phi_S^2 = ||eta||^2 = sum_{j,alpha} B_{j alpha}^2 = ||B||_F^2.
```

Since `Z` sums only the non-negative terms with `psi_S=0`,

```text
0 <= Z <= ||B||_F^2.
```

## 4. Spectral scales of the transverse endpoints

Put `F=||B||_F^2`.  In the same SVD blocks as above, for the endpoint
`t=t_epsilon`, the determinant of a paired `2 x 2` block is

```text
epsilon(1-epsilon) - t_epsilon^2 b_j^2
 = epsilon(1-epsilon)(1 - tau^2 b_j^2).
```

The two eigenvalues in that block sum to `1`.  Thus the large eigenvalue has
hole size

```text
1-lambda_j^large = epsilon(1 - tau^2 b_j^2) + O(epsilon^2),
```

and the small eigenvalue is

```text
lambda_j^small = epsilon(1 - tau^2 b_j^2) + O(epsilon^2).
```

Unpaired large or small directions correspond to `b_j=0`.  Summing over all
large and small directions gives

```text
sum_large (1-lambda_j) = epsilon (r - tau^2 F) + O(epsilon^2),
sum_small lambda_j     = epsilon (s - tau^2 F) + O(epsilon^2).      (2)
```

The top spectral subspace is the graph of a map from `P R^n` to `Q R^n`.
Since the gap between the top and bottom clusters tends to `1`, the canonical
orthonormal frame has the expansion

```text
W_top,sigma = U + sigma tau sqrt(epsilon) V B^T + O(epsilon),       (3)
```

where the `O(epsilon)` is in operator norm for fixed data.  Consequently, for
each `r`-subset `S`,

```text
det((W_top,sigma)_S)
  = psi_S + sigma tau sqrt(epsilon) phi_S + O(epsilon).             (4)
```

## 5. Entropy of the midpoint

For `M_epsilon`, the eigenvectors are exactly the columns of `U` and `V`, with
large eigenvalues `1-epsilon` and small eigenvalues `epsilon`.

By (1), events of sizes `r-1` and `r+1` have total masses

```text
epsilon r + O(epsilon^2),   epsilon s + O(epsilon^2),
```

respectively.  Events with cardinality farther from `r` have total mass
`O(epsilon^2)`.  For `r`-subsets with `psi_S=0`, the all-large spectral term
vanishes and any nonzero term must omit at least one large eigenvector and
include at least one small eigenvector, hence has mass `O(epsilon^2)`.

The active `r`-subsets have probabilities `psi_S^2+O(epsilon)`.  Let

```text
H_P = - sum_{|S|=r, psi_S != 0} psi_S^2 log(psi_S^2).
```

Using the finite-family entropy scale lemma,

```text
H(M_epsilon)
  = H_P + n epsilon log(1/epsilon) + O(epsilon).                    (5)
```

## 6. Entropy of the endpoints

The total mass of endpoint events with size `r-1` is the probability that the
spectral Bernoulli set omits exactly one top eigenvector and includes no
bottom eigenvector, up to `O(epsilon^2)`.  By (2), this is

```text
epsilon (r - tau^2 F) + O(epsilon^2).
```

Similarly, size `r+1` has total mass

```text
epsilon (s - tau^2 F) + O(epsilon^2).
```

All sizes other than `r,r-1,r+1` have total mass `O(epsilon^2)`.

For `r`-subsets, first take the all-top spectral selection in (1).  Its
Bernoulli weight is `1+O(epsilon)`.  Equation (4) gives:

- If `psi_S != 0`, then

```text
p_{K_epsilon,sigma}(S)
  = psi_S^2 + 2 sigma tau sqrt(epsilon) psi_S phi_S + O(epsilon).
```

  These coordinates stay bounded away from zero for small `epsilon`; after
  averaging the two signs, their entropy contribution is `H_P+O(epsilon)`.

- If `psi_S=0`, then

```text
p_{K_epsilon,sigma}(S)
  = tau^2 epsilon phi_S^2 + O(epsilon^(3/2)) + O(epsilon^2).
```

  Hence all zero-Plucker `r`-subsets contribute

```text
tau^2 Z epsilon log(1/epsilon) + O(epsilon).
```

Combining the cardinality leakage and zero-Plucker leakage,

```text
(H(K_epsilon,+)+H(K_epsilon,-))/2
  = H_P
    + (n - 2 tau^2 F + tau^2 Z)
        epsilon log(1/epsilon)
    + O(epsilon).                                                  (6)
```

Subtracting (5) from (6) proves

```text
Delta_epsilon
  = tau^2 (Z - 2 ||B||_F^2) epsilon log(1/epsilon) + O(epsilon).
```

## 7. Sign

By Section 3,

```text
Z - 2 ||B||_F^2 <= - ||B||_F^2.
```

Therefore, if `tau B` is nonzero, the coefficient of
`epsilon log(1/epsilon)` is strictly negative, and this term dominates the
`O(epsilon)` remainder.  Thus `Delta_epsilon<0` for all sufficiently small
positive `epsilon`.

If `tau B=0`, then `t_epsilon D=0`; both endpoints equal `M_epsilon`, so
`Delta_epsilon=0` identically.

This proves all frozen claims for fixed finite data.

