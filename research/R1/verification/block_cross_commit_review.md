STATUS: CORRECT

# Commit-bound independent review: block-cross midpoint theorem

Reviewed object:

- commit: `64c5bc0910c10c8baba1208326c799c0d0dffeec`
- tree: `8b75d4f4b5739a3e89fb9fef65d1ce83dc003ed8`
- frozen statement blob: `d8ac10f0faff9e2e504d34159b7be20d14e3c47f`
- proof blob: `91da4ffa9ab2990d8c2b8f9fb0822a68cf81a02e`

The reviewer did not author the proof and read both files from the commit with
`git show <commit>:<path>`, not from the worktree.

## Verdict

The proof establishes the frozen claim under the stated hypotheses. No
critical gap or counterexample satisfying the hypotheses was found.

The block marginal Mobius formula is correct: outside-block elements are
unrestricted, while inclusion-exclusion only over `B_a\S` converts the
within-block inclusion table into the exact block event. Since
`V[B_a,B_a]=0`, both endpoint block laws equal those at `K_0`.

At the block-diagonal center, all joint inclusion probabilities factor over
blocks. Mobius inversion on the product Boolean lattice therefore gives a
product exact law and additive block entropy. At either endpoint, entropy
subadditivity is bounded by this unchanged sum of block marginal entropies.

Strictness is valid at both endpoints. Nonzero `V` with every diagonal block
zero supplies `i,j` in different blocks with `V_ij!=0`, and

```text
P(i,j in Y)-P(i in Y)P(j in Y) = -t^2 V_ij^2 < 0.
```

Thus the containing block variables cannot be independent, so equality in
entropy subadditivity is impossible. The hypotheses `t>0`, `V!=0`, and strict
endpoint feasibility close the relevant equality and validity boundaries.
