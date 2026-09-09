# Non-Author Review: Support and BSC-Lift Proof v2

Status: CORRECT.

Reviewed source: proof-child `research/N4/round2/proof/support_lift_proof_v2.md`
at commit `6126b5639e659c4a58710062e86540479614bed9`, blob
`35dad0f51073b8617d01814222629534ccddf007`.

## Verdict

No critical gaps found for the scoped support, analyticity, Hessian formula,
and BSC-lift gate.

The support proof correctly derives the L-ensemble formula on the rank-three
face. The block determinant sign cancels the frozen signed event convention,
giving

```text
p_A(S)=det(I_3-A) det(U_S B U_S^T),     B=A(I_3-A)^(-1).
```

For every proper `S`, the argument `U_S^T x=0 => x=0` is valid because an
extension by zero must lie in `ker U^T=span(z)`, while a coordinate outside
`S` and the hypothesis `z_i != 0` force the scalar to vanish. Thus every
proper event is strictly positive, and the full event is identically zero by
`rank K(A)<=3`.

The analyticity and Hessian formula are also correct: the 15 proper masses are
positive polynomials on `0<A<I_3`; differentiating the finite entropy sum
produces the displayed Hessian after using

```text
sum_proper p_S = 1,
sum_proper p'_S = 0,
sum_proper p''_S = 0.
```

The BSC lift proof is correct. Independent bit flips with rate `e` send a DPP
kernel `K` to

```text
K_e=eI_4+(1-2e)K,
```

as verified by the generating function calculation. For `0<e<1/2`, a boundary
contraction with eigenvalues in `[0,1]` becomes strict, and the midpoint of a
common chord is preserved.

The entropy gate follows from the bit-flip channel:

```text
0 <= H(K_e)-H(K) <= 4 h_b(e),
Delta(e) >= Delta_face - 4 h_b(e).
```

Therefore a certified boundary gap `g>0` and rational `e` with `4h_b(e)<g`
give a strict interior positive-gap chord. This remains only a lift gate; it
does not produce a positive boundary gap and does not prove face concavity.
