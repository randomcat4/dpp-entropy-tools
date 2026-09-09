# Narrow fixture arithmetic plan

Purpose: independently check only the endpoint discriminant/root-separation
claims for the fixed PR54 fixture at frozen head
`c3b9e968c0b4557546c7b10137ef4fff295338b4`.

Inputs:

- `A,C,U,V` as displayed in
  `research/I05-23-20260909/code/verify_local_and_matching.py:15-29`.
- `B=UV^T`.

Checks:

1. Recompute `M_K=B^T A^{-1}B`, `S_K=C^{-1}M_K`,
   `Delta_K=2 tr(S_K^2)-tr(S_K)^2`.
2. Recompute `M_IK=B^T(I-A)^{-1}B`,
   `S_IK=(I-C)^{-1}M_IK`,
   `Delta_IK=2 tr(S_IK^2)-tr(S_IK)^2`.
3. Verify the exact inequalities used by the author script:
   `rho_K < 1/25 < 1/20 < rho_IK`, via the same rational square comparisons,
   not by floating point eigenvalues.

Limits:

- One local process, one thread.
- No GPU, no search, no scan.
- 4 GiB target memory, 15-minute ceiling.
- Preserve any failure output in this owned directory.
- Do not run or rely on the author verifier as the certificate.
