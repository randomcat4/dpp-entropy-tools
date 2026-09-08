# D10-S4 exact-event sanity report

Status: **PASS_FOR_LISTED_EXACT_CHECKS**.

Script:

```text
research/R3/deepening_10h/dense_hessian/scalar_kernel_psd_neighborhood/scalar_hessian_sanity.py
```

Command:

```text
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe
research\R3\deepening_10h\dense_hessian\scalar_kernel_psd_neighborhood\scalar_hessian_sanity.py
```

Exit code: `0`.

Output:

```text
research/R3/deepening_10h/dense_hessian/scalar_kernel_psd_neighborhood/scalar_hessian_sanity_results.json
```

## What was checked exactly

The script uses rational arithmetic for \(n=2,3\).  For each listed case it:

1. builds determinant polynomials for inclusion probabilities
   \(\det K[A,A]\);
2. applies Möbius inversion to get exact-event atom polynomials \(p_S(t)\);
3. checks

   \[
   p'_S(0)=p_S(0)\left[
   \sum_{i\in S}\frac{D_{ii}}{x_i}
   -
   \sum_{i\notin S}\frac{D_{ii}}{1-x_i}
   \right];
   \]

4. checks \(\sum_Sp_S''(0)=0\) and, for every coordinate \(i\),
   \(\sum_{S\ni i}p_S''(0)=0\);
5. checks

   \[
   \sum_S\frac{p'_S(0)^2}{p_S(0)}
   =
   \sum_i\frac{D_{ii}^2}{x_i(1-x_i)}.
   \]

## Cases

- `n2_zero_diag_offdiag_flat`, \(x=(2/5,2/5)\),
  \(D=\begin{pmatrix}0&3/7\\3/7&0\end{pmatrix}\).
  Here \(p_S''(0)\) is nonzero for all four atoms, but the entropy Hessian is
  exactly `0` because the diagonal is zero and the \(p''\)-weighted entropy
  term vanishes.

- `n2_psd_mixed`, \(x=(3/8,3/8)\), with a positive definite rational \(D\).
  The checked Hessian is `-1088/1323`.

- `n2_heterogeneous_zero_diag_offdiag_flat`, \(x=(2/7,5/8)\), with the same
  zero-diagonal off-diagonal \(D\).  The checked Hessian is again `0`.

- `n3_general_symmetric`, \(x=(3/7,3/7,3/7)\), with a mixed-sign rational
  symmetric \(D\).  The checked Hessian is `-6517/15552`.

- `n3_heterogeneous_general_symmetric`, \(x=(2/7,3/5,5/11)\), with the same
  mixed-sign rational symmetric \(D\).  The checked Hessian is `-18343/38880`.

- `n3_psd_rational`, \(x=(5/11,5/11,5/11)\), with a positive definite rational
  \(D\).  The checked Hessian is `-61331149/41067000`.

- `n3_heterogeneous_psd_rational`, \(x=(1/4,1/2,4/5)\), with the same positive
  definite rational \(D\).  The checked Hessian is `-25165/13689`.

For the PSD rational \(3\times3\) matrix, the one-by-one principal minors are

```text
5/13, 7/18, 4/15
```

the two-by-two principal minors are

```text
19/156, 361/3900, 209/2160
```

and the determinant is

```text
1343/46800
```

so it is strictly positive definite.

## Interpretation

The exact checks support the proof's key distinction:

- off-diagonal acceleration generally exists in \(p_S''(0)\);
- it contributes zero to \(H''\) at a diagonal kernel, because
  \(\log p_S(0)\) is affine in singleton indicators, while total mass and every
  singleton inclusion probability have zero second derivative along any affine
  kernel direction.

These finite checks are sanity tests only; the general proof is in `proof.md`.
