# Presentation and Identity Supplement

Status: SUPPLEMENT_COMPLETE. This file does not modify the original review
artifacts. It corrects interval presentation and separates the finite
polynomial execution check from the general algebraic identity review.

## Outward Rational Interval Endpoints

Executable artifact: `interval_presentation_supplement.py`.

Run artifact: `interval_presentation_supplement.json`.

Run metadata: PID `64800`, exit status `0`, script SHA-256
`786556aeb55bab6c2aba3fe2874bbc062d5e6b130ca36d7196946484a378ad5a`,
output SHA-256 `597a4338fc459d387aa523df3043cacc27c7a059bfc955f93ae697c906dbf854`,
Python `3.12.14`.

The original JSON `lower_decimal` and `upper_decimal` fields were approximate
float-format display values, not certified outward decimal endpoints. The
supplement recomputes the exact Fraction log intervals and stores outward
rational endpoints using

```text
lower = floor(exact_lower * 10^18) / 10^18
upper = ceil(exact_upper * 10^18) / 10^18.
```

The exact log Fraction endpoints themselves are intentionally not saved.

For the n5 projection entropy,

```text
H(q) in [1.900161876460949643,
         1.900161876460949644]
```

with outward rational endpoints at scale `10^18`. Therefore
`H(q)-3/2 >= 0.400161876460949643 > 0`.

For the low-denominator noncommuting face chord,

```text
Delta_face in [-0.000086555894403772,
               -0.000086555894403771]
```

so the sign is strictly negative.

For the common BSC lift of that chord,

```text
Delta_lift in [-0.000079835082773969,
               -0.000079835082773968]
```

so the lifted sign is also strictly negative.

The original markdown/JSON displayed values are now treated only as approximate
printing. The supplement also records coarser display envelopes at scale
`10^15`; those envelopes contain the previously printed values and still prove
the same strict signs.

## General Coarse Identity Review

The finite noncommuting fixture in `coarse_identity_check.json` is an execution
check only. The general scoped identity is certified by the following algebraic
review of the author derivation, for a fixed four-point rank-three face
`K=UAU^T` with `U^TU=I_3` and `0<A<I_3`.

1. L-ensemble reduction is valid. With
   `B=A(I_3-A)^(-1)` and `L=UBU^T`, the nonzero eigenvalues of `L` are those
   of `B`, so `det(I_4+L)^(-1)=det(I_3-A)`. Multiplying
   `K-D_{S^c}` by `I+L` gives a block matrix whose determinant sign cancels
   the frozen signed event convention, yielding
   `p_A(S)=det(I_3-A)det(L_S)`.

2. The singleton formula is valid. For one row `r_i`,
   `p_i=det(I-A) r_i^T B r_i = r_i^T A adj(I-A) r_i`. In dimension three,
   Cayley-Hamilton gives
   `A adj(I-A)=A^2+(1-tr A)A+det(A)I`.

3. The pair formula is valid. For two rows `r_i,r_j` and
   `w_ij=r_i x r_j`, the compound/cross-product identity gives
   `det((UBU^T)_{ij})=w_ij^T adj(B) w_ij`. Since
   `det(I-A) adj(B)=det(A)B^-1=adj(A)-det(A)I`, the stated pair polynomial
   follows.

4. The triple formula is valid. For `T=[4]\{i}`,
   `det(U_T B U_T^T)=det(U_T)^2 det(B)`. The cofactor vector of the
   `4 x 3` isometry spans `ker U^T` and has unit norm, so
   `det(U_T)^2=z_i^2`; after multiplying by `det(I-A)`, this gives
   `p_T=z_i^2 det(A)`.

5. The entropy merge and Fisher accounting are valid. The four triple events
   are `q_i d`, with `q_i=z_i^2`, `sum q_i=1`, and `d=det(A)`. Therefore
   their entropy contribution is `-d log d + d H(q)`. Merging them into one
   symbol of mass `d` gives exactly
   `H_face=H_12+dH(q)`. Along any affine latent chord, the original triple
   Fisher sum is
   `sum_i (q_i d')^2/(q_i d)=(d')^2/d`, equal to the grouped Fisher term.

Thus the general identity review remains `CORRECT_IDENTITY_ONLY`. It does not
prove face concavity, because the coarse probability vector is constrained
polynomial data in `A`, not an affine free-simplex chord.
