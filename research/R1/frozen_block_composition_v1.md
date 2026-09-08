# Frozen theorem: block-composition upper bound for midpoint gaps

Version: v1 (2026-09-08)

Let `[n]=B_1 sqcup ... sqcup B_m`, `m>=2`, be a partition into nonempty
blocks.  Let `K_0` be a real symmetric strict-contraction kernel that is block
diagonal for this partition.  Let `V` be any real symmetric matrix, let `t>0`,
and assume `K_±=K_0±tV` are strict-contraction kernels.

Define

```text
Delta   = [H(K_-)+H(K_+)]/2-H(K_0),
Delta_a = [H(K_-[B_a])+H(K_+[B_a])]/2-H(K_0[B_a]).
```

Every entropy is that of the complete event law reconstructed from inclusion
probabilities by Mobius inversion.  Prove

```text
Delta <= sum_a Delta_a.
```

If `V` has a nonzero cross-block entry, prove the inequality is strict.  If
`V` has no cross-block entry, prove equality.  The proof must check block
marginals, endpoint feasibility, the strict equality condition, and the
`m>2` mutual-independence case without changing the premises.

