# Frozen theorem v2: the remaining non-paired `C_2` sign

Status: frozen by the R2 main instance on 2026-09-08.  Proof, counterexample,
and verification instances may not modify, supplement, or reinterpret the
assumptions.

## Objects and definitions

Let `E={1,...,n}`, `1<=r<=n-1`, and `s=n-r`.  Let

```text
U in R^(n x r),  V in R^(n x s),  W=[U V] in O(n).
```

Let `A,X in Sym_r` and `C,Y in Sym_s` satisfy

```text
A-X>=0,  A+X>=0,  C-Y>=0,  C+Y>=0.
```

For every `(r-1)`-set `R`, let `alpha_R` be the signed one-hole cofactor
vector of `U_R`.  For every `(r+1)`-set `T`, let `beta_T` be the signed
one-particle cofactor vector defined from `[U,V]_T`.  Assume the full
tomography equalities

```text
alpha_R^T X alpha_R=0  for every |R|=r-1,
beta_T^T Y beta_T=0    for every |T|=r+1.
```

For `sigma in {-1,+1}` set

```text
G_sigma=A-sigma X,  R_sigma=C+sigma Y,
K_(epsilon,sigma)=W diag(I-epsilon G_sigma,
                         epsilon R_sigma) W^T,
K_(epsilon,0)=W diag(I-epsilon A,epsilon C) W^T.
```

For all sufficiently small positive `epsilon` these matrices are positive
contractions.  Let `p_K(S)` be the exact DPP event law and let

```text
H(K)=-sum_(S subset E) p_K(S) log p_K(S),
Delta_epsilon=[H(K_(epsilon,+))+H(K_(epsilon,-))]/2
              -H(K_(epsilon,0)),
```

with natural logarithms and `0 log 0=0`.

The proved expansion in `proofs/b_zero_c2_decomposition_v2.md` is

```text
Delta_epsilon=C_2 epsilon^2+O(epsilon^3 log(1/epsilon)).
```

Here `C_2` is the finite exterior-minor expression in that file.

## Frozen decision problem

Decide exactly one of the following:

1. prove `C_2<=0` for every datum satisfying all assumptions above; or
2. give explicit finite real data satisfying every assumption and `C_2>0`.

A counterexample must include exact or interval-certified feasibility,
tomography residuals, and coefficient sign.  A proof must cover singular
`A,C`, singular endpoints, zero Pluecker coordinates, simultaneous nonzero
`X,Y`, and non-paired frames.

Strict negativity is not part of the frozen claim.  It may be proved as a
separate strengthening only after the nonpositive decision problem is closed.

## Explicit non-claims

- This version does not decide global entropy concavity away from a projection
  boundary.
- Finite searches and floating-point non-hits do not prove `C_2<=0`.
- Paired frames, rank-two one-sided kernels, and coordinate reductions are
  already proved subfamilies, not substitutes for the quantified statement.
- Proof instances may not add genericity, full-support, uniform-weight, or
  nonsingularity assumptions.
