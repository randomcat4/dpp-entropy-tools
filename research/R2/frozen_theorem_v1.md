# Frozen theorem v1

Status: frozen by the R2 main instance on 2026-09-08.  Proof and verification
instances may not modify, supplement, or reinterpret the assumptions.

## Objects and definitions

Let `E={1,...,n}`, `1 <= r <= n-1`, and `s=n-r`.  Let `P` be a fixed rank-`r`
real orthogonal projection, `Q=I-P`, and choose fixed real orthonormal frames
`U in R^(n x r)` and `V in R^(n x s)` for their ranges.  For fixed
`B in R^(r x s)`, put

```text
D = U B V^T + V B^T U^T.
```

Fix `tau >= 0` with `tau ||B||_op < 1`.  For `0<epsilon<1/2`, define

```text
M_epsilon = (1-epsilon)P + epsilon Q,
t_epsilon = tau sqrt(epsilon(1-epsilon)),
K_epsilon,sigma = M_epsilon + sigma t_epsilon D, sigma in {-1,+1}.
```

For every subset `S subset E`, define the exact-event probability

```text
p_K(S) = sum_{T: S subset T subset E}
           (-1)^(|T|-|S|) det(K_T),
```

and `H(K)=-sum_S p_K(S) log p_K(S)`, with natural logarithms and
`0 log 0=0`.  Define the counterexample-oriented chord difference

```text
Delta_epsilon = (H(K_epsilon,+)+H(K_epsilon,-))/2 - H(M_epsilon).
```

For each `r`-subset `S`, set

```text
psi_S = det(U_S),
phi_S = d/da det((U+a V B^T)_S) at a=0,
Z = sum_{|S|=r, psi_S=0} phi_S^2.
```

## Claims

1. For every `0<epsilon<1/2`, both endpoints are strict real-symmetric
   contractions.  More generally, `M_epsilon+tD` is a positive contraction
   exactly when

   ```text
   |t| ||B||_op <= sqrt(epsilon(1-epsilon)).
   ```

   (With `B=0`, the condition is vacuous.)

2. The zero-coordinate Plucker leakage satisfies

   ```text
   0 <= Z <= ||B||_F^2.
   ```

3. As `epsilon -> 0+`,

   ```text
   Delta_epsilon
     = tau^2 (Z - 2||B||_F^2)
         epsilon log(1/epsilon) + O(epsilon).
   ```

4. Consequently, if `tau B` is nonzero, then `Delta_epsilon<0` for all
   sufficiently small positive `epsilon`.  If `tau B=0`, then
   `Delta_epsilon=0` identically.

## Success standard

A self-contained proof must derive the exact feasibility interval, obtain all
event-mass scales from the full DPP law, prove the coefficient and the stated
`O(epsilon)` remainder for the fixed finite data, and cover Plucker zeros.
Independent fresh-context review is required before `VERIFIED`.

## Explicit non-claims

- No assertion for arbitrary real-symmetric chords.
- No assertion for a center fixed while `epsilon` changes.
- No assertion for longitudinal or mixed diagonal/off-diagonal directions.
- No uniform remainder over growing dimension or varying `(P,B,tau)`.
- No global DPP entropy-concavity theorem and no entropy-rate theorem.
