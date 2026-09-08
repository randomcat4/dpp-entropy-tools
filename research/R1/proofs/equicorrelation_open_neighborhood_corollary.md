# P4-09 corollary: full-dimensional strict-concavity neighborhoods

Status: `CANDIDATE_COROLLARY / NONAUTHOR_REVIEW_PENDING`.

Let `K_0` be a strict real-symmetric `3 x 3` equicorrelation kernel with
distinct standard and trivial eigenvalues:

```text
K_0=lambda P_std+mu P_triv,
0<lambda,mu<1,             lambda!=mu.
```

The double-reviewed P4-06/P4-07 result proves

```text
D^2 H(K_0) is negative definite on Sym_3.             (1)
```

For a strict DPP kernel, the L-ensemble matrix
`L=K(I-K)^{-1}` is positive definite, and every complete event probability is

```text
p_K(S)=det(L_S)/det(I+L)>0.
```

Hence the complete-event entropy is real analytic, in particular twice
continuously differentiable, on the open strict-kernel domain

```text
Omega={K in Sym_3: 0<K<I}.
```

Negative definiteness is open in the space of symmetric bilinear forms.  By
continuity of `D^2H` and (1), there is an `epsilon>0` such that

```text
B_epsilon(K_0) subset Omega,
D^2H(K) is negative definite for every K in B_epsilon(K_0),   (2)
```

where the ball is taken in any fixed norm on `Sym_3`.  Shrink `epsilon` if
necessary; norm equivalence in finite dimensions makes the choice immaterial.

The ball is convex.  Therefore, for distinct `K_1,K_2` in the ball, the affine
segment remains in the ball and its entropy restriction has strictly negative
second derivative.  Consequently

```text
H((K_1+K_2)/2)>[H(K_1)+H(K_2)]/2.                    (3)
```

Thus every non-product strict equicorrelation kernel is contained in a
full-dimensional open neighborhood of general strict real-symmetric `3 x 3`
kernels on which complete-event DPP entropy is strictly concave.

This is an existential local-neighborhood theorem.  It does not provide a
uniform radius over the noncompact open parameter domain, does not cover a
whole arbitrary chord leaving the neighborhood, and does not prove concavity
on all connected `3 x 3` kernels.  The product diagonal `lambda=mu` is excluded
because its full Hessian has pure-off-diagonal zero directions; finite chords
centered exactly there are instead covered by the earlier block-diagonal
midpoint theorem.
