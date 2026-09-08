CORRECT

# Commit-bound non-author review: block composition

The reviewer read only fixed Git objects from commit
`603300c06059518961766c724377c3b9d1198fc5`, tree
`9c1a4db5462dddaf4a3b7cc37c010927254cbda4`.

| Role | Committed path | Git blob ID |
|---|---|---|
| Frozen statement | `research/R1/frozen_block_composition_v1.md` | `c1360cb384b8ca2745d69d2f6d4d68792d5244e6` |
| Proof | `research/R1/proofs/block_composition.md` | `bcd7a3292cd7a2a042c042d5204e1c0abe2afcbd` |
| Sanity record | `research/R1/prob_deriv/phase3/sanity_checks.json` | `e93800acafce6dbbbbddaa354efcf259c392d3b3` |
| `n=2` dependency | `research/R1/proofs/n2_concavity.md` | `7d652eae8d745d2289713db82b590d0c41c04bc7` |

The reviewer did not author the block-composition proof and did not use
working-tree copies as evidence.

## Verdict

The proof establishes exactly the frozen upper bound, strictness for any
nonzero cross-block entry, and equality when all cross-block entries vanish.
Its one- and two-dimensional block corollary correctly uses the strict
two-dimensional conclusion in the same fixed commit.  No critical gap was
found.

## Checks performed

### Principal-block marginals and feasibility

For every `S subset B_a`, the event `S subset Y_a` equals `S subset Y`, so its
probability is `det K_S`, the inclusion probability supplied by `K[B_a]`.
Uniqueness of Boolean Mobius inversion identifies the complete marginal law
with the principal-block DPP.  Positivity of `K` and `I-K`, tested on vectors
supported in the block, passes strict feasibility to every principal block.

### Product center and endpoint subadditivity

At a block-diagonal center, every inclusion determinant over a union of block
subsets factors.  The product Mobius transform therefore gives mutual
independence of all block random vectors, not merely pairwise independence,
and `H(K_0)=sum_a H(K_0[B_a])`.

At each endpoint, the block tuple determines the full subset bijectively.
Shannon subadditivity bounds its joint entropy by the verified marginal
entropies.  Averaging the two endpoint inequalities and subtracting the exact
center factorization gives the claimed gap bound.  Equivalently, the deficit
is the average of two nonnegative endpoint multi-informations, so opposite
signs cannot cancel.

### Strictness and the `m>2` case

If `V_ij!=0` across two blocks, then at both endpoint signs

```text
P(i,j in Y)=P(i in Y)P(j in Y)-t^2 V_ij^2
            < P(i in Y)P(j in Y).
```

Thus the two containing block vectors are dependent.  For `m>2`, mutual
independence of all blocks would imply independence of that pair, so one
dependent pair rules it out.  Equality in finite-vector subadditivity is
equivalent to mutual independence; both endpoint deficits are therefore
strictly positive.

If `V` has no cross-block entries, both endpoints remain block diagonal and
the product factorization holds at each sign, giving exact equality.

### `1 x 1` / `2 x 2` corollary

All principal chords meet the required strict-feasibility hypotheses.  Binary
entropy is strictly concave on a nonzero one-dimensional direction, and the
fixed two-dimensional proof gives a nonpositive gap, strict for every nonzero
two-dimensional direction.  Therefore all block gaps are nonpositive.  A
cross-block component makes the composition inequality strict; without one,
any nontrivial chord has a nonzero diagonal block and hence a strictly
negative block gap.  The global gap is strict exactly as claimed for a
nontrivial chord.

The compact sanity JSON is consistent with the theorem, including an `m=3`
case and the no-cross equality case, but the structural proof—not a finite
example—is the basis of this verdict.

