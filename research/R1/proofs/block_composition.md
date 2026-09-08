# Block-composition bound for DPP midpoint gaps

Status: `PROVED / AWAITING COMMIT-BOUND REVIEW`

This proves `frozen_block_composition_v1.md`.

Let `Y` be the DPP random subset for a kernel `K` and put
`Y_a=Y cap B_a`.  For every `S subset B_a`,

```text
P_K(S subset Y_a)=P_K(S subset Y)=det K_S.
```

These are precisely the inclusion probabilities for the DPP with kernel
`K[B_a]`.  Boolean Mobius inversion uniquely determines the exact event law,
so the complete marginal law of `Y_a` is that principal-block DPP.  In
particular,

```text
H(Y_a under K_±)=H(K_±[B_a]).                 (1)
```

Strict feasibility is inherited by principal submatrices.

At the midpoint, block diagonality gives, for arbitrary `S_a subset B_a`,

```text
P_{K_0}(all S_a subset Y_a)
 = det (K_0)_{union_a S_a}
 = product_a det (K_0[B_a])_{S_a}.
```

Mobius inversion identifies the complete event law with the product of the
block laws.  The block random vectors are therefore mutually independent and

```text
H(K_0)=sum_a H(K_0[B_a]).                     (2)
```

For either endpoint `K_sigma=K_0+sigma tV`, Shannon subadditivity and (1)
give

```text
H(K_sigma) <= sum_a H(K_sigma[B_a]).          (3)
```

Averaging (3) for the two signs and subtracting (2) proves

```text
Delta <= sum_a Delta_a.
```

Equivalently, the difference between the right and left sides is the average
of the endpoint multi-informations, hence is nonnegative.

For equality, suppose first that `V` has no cross-block entry.  Both endpoints
are block diagonal, so the same factorization as at the midpoint makes (3) an
equality for each sign.  Thus `Delta=sum_a Delta_a`.

Conversely, suppose `V_ij!=0` for indices in two distinct blocks.  At either
endpoint,

```text
P(i,j in Y)
 = (K_sigma)_ii (K_sigma)_jj-(K_sigma)_ij^2
 = (K_sigma)_ii (K_sigma)_jj-t^2 V_ij^2
 < P(i in Y)P(j in Y).
```

The two indicator events, and hence the two containing block random vectors,
are not independent.  Mutual independence of all `m` block vectors would
imply independence of every such pair even when `m>2`, so it fails.  Equality
in Shannon subadditivity for discrete random vectors holds exactly under
mutual independence; consequently (3) is strict at both endpoints and

```text
Delta < sum_a Delta_a.
```

This completes the frozen theorem.  It does not assert a sign for the
individual block gaps.

## Corollary using the two-dimensional theorem

If `K_0` is block diagonal with every block of size one or two, then every
real symmetric feasible chord has `Delta<=0`: one-dimensional binary entropy
is concave, two-dimensional DPP entropy is concave by `n2_concavity.md`, and
the theorem above adds the block gaps.  Every nontrivial chord is strict.  A
cross-block direction is strict by this theorem; without a cross-block entry,
at least one nonzero block direction is strict in its one- or two-dimensional
entropy.

