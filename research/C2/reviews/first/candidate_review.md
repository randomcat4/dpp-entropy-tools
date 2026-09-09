# Candidate proof review

Verdict: CORRECT.

This verdict is limited to the frozen auxiliary claims listed below. It does not certify the global five-point rank-three concavity problem, does not certify absence of counterexamples outside the stated upper-face regimes, and does not claim novelty.

## Binding

Public commit reviewed:

```text
81b0123b7c1bcb4495e99d5707bf2388314f3bbf
```

The original frozen commit `3f2be12c6523c600c2497d7229bed7915f9b37c4` was read first. The public commit has the same proof blobs reported by the coordinator:

```text
research/C2/proof.md                 blob 0a8cf09210aeddbc03f355143f638069ccfbbe1e
research/C2/mechanism/proof.md       blob 70935232da868f66f70338123ad1907d391c2275
research/C2/frozen_statement.md      blob 9b3cc75260c43abf41201b36e80fe4cf8f7084d1
research/C2/frozen_supplement.md     blob dc77c9507a03d67b387cb350a8ec42316d0d10f3
research/C2/main_check.py            blob e59fe09e5cb86b941fdbfeb2360a890d71b0eefd
research/C2/main_check.json          blob 1b9ed5b4385113a8c9d357fb1f74e06017cdb4f0
```

## Independent computation

Before reading the candidate proof I independently rebuilt the fixed five-point U, all 32 event probability polynomials, the low-order formulas, and the second jets. That check is recorded in:

```text
review.md
independent_c2_verify.py
event_jets.tsv
output.txt
```

After reading the candidate proof I ran a separate constant check, independent of the author `main_check.py`, in the server review directory with BLAS/OpenMP thread limits set to 1. It is recorded in:

```text
candidate_constant_check.py
candidate_constant_check.json
candidate_constant_check.out
```

It verifies:

```text
U^T U = I
all three-row determinants are nonzero
sum q = 1
sum_i r_i r_i^T = I
sum_{i<j} w_ij w_ij^T = I
G - (1/22)D has all six leading principal minors positive
1/tr(D G^{-1}) > 1/22
min_{|S|<=3} gamma_S/4^|S| = 441/1092025 > 2^-14
(8/3)^10 > 2^14
1/(176e)-5600 = 1/(352e) at e = 1/1971200
```

## Claim 1: upper-face compensation cone

I find the proof correct for the stated range

```text
A = I - eB,  I <= B <= 2I,  0 < e <= 1/1971200.
```

The rare-event logarithm is handled correctly. At a fixed center, writing `p_S=e^(3-|S|)g_S` is only a logarithmic split, not a differentiated reparametrization. The coefficient of `log e` cancels by the exact affine identity

```text
sum_S (3-|S|) p_S'' = 0.
```

The pair Fisher lower bound is valid for all symmetric V, including non-commuting directions. In the eigenbasis of A, `DC[V]+V` has Frobenius norm at most `4 delta ||V||_F` with `delta=2e`, while `p_ij <= delta ||w_ij||^2`; combining this with the exact frame certificate gives

```text
F_pair >= ||V||_F^2/(176e).
```

The all-layer logarithmic acceleration bound is conservative but sufficient:

```text
|sum p_S'' log g_S| <= 5600 ||V||_F^2.
```

The radius arithmetic then gives

```text
H'' <= [-1/(176e)+5600] ||V||_F^2
    <= -||V||_F^2/(352e).
```

No discarded layer or hidden commutation assumption was found.

## Claim 2: low-event derivative injectivity

I find the injectivity argument correct for the fixed U. If all pair derivatives vanish, the frame inequality forces `DC[V]=0`. The differential identity

```text
DC[V] = d [ s(A^{-1}-I) - A^{-1} V A^{-1} ],
s = tr(A^{-1}V)
```

then gives

```text
V = s A(I-A).
```

Taking the trace gives `s=s(3-tr A)`, hence either `V=0` or `tr A=2`. In the exceptional nonzero pair-null direction, the empty derivative equals

```text
p_empty' = -2s det(I-A),
```

so adding `p_empty'=0` eliminates the exception. This proves the frozen statement as written.

## Claim 3: exceptional pair-null curvature

I find this proof correct. Under `tr A=2` and `V=sA(I-A)`, A and V commute, so the affine eigenvalue path may be used. For each eigenvalue component of the pair matrix C(A), the relative first derivatives sum to zero, and the second derivative is

```text
c_i'' = -s^2 c_i(lambda_i^2 + mu_j^2 + mu_k^2) < 0.
```

Every pair normal w_ij is nonzero because the frame is full spark, so every pair probability has `p_ij''<0`. Since each supported probability lies in `(0,1)`, the pair log-acceleration contribution

```text
-p_ij'' log p_ij
```

is strictly negative. The zero Fisher term in this exceptional direction therefore does not create a compensation gap.

## Supplemental anisotropic theorem

I find the anisotropic upper-face result in `mechanism/proof.md` correct under its stated assumptions:

```text
0 < delta <= 1/8,  rho I <= R <= I,  A = I - delta R.
```

The probability formulas in C-coordinates are consistent with the DPP event law. The bounds on the scaled probabilities g_S are correct:

```text
g_0      in [rho^3, 1]
g_i      >= rho^2(1-delta) ell_i
g_ij     >= rho(1-delta)^2 z_ij
g_ijk    >= (1-delta)^3 q_ijk
```

The acceleration estimate sums correctly to

```text
|sum p_S'' log g_S|
 <= [(14+12delta)L+(15+24delta)x+(27+18delta)y] ||V||_F^2
 <= [16L+18log(1/rho)+4] ||V||_F^2.
```

The anisotropic pair Fisher lower bound

```text
F_pair >= kappa ||V||_F^2/(4delta)
```

also checks out. The proof that `kappa>0` for full-spark n by 3 frames with n>=4 is valid: after choosing three independent rows as coordinates, a fourth full-spark row with all three coordinates nonzero forces the off-diagonal entries from the three additional pair measurements.

The sequence corollaries follow directly from

```text
delta [16L + 18log(1/rho) + 4] < kappa/4.
```

In particular, `rho >= exp(-eta/delta)` is eventually covered for every fixed `eta < kappa/72`.

## Fixed-B asymptotic

I find the fixed-B full expansion and remainder statement correct for fixed positive B, and uniformly for B in compact subsets of the positive definite cone. The signs in the pair, singleton, and top-layer constants match the exact entropy Hessian formula:

```text
H'' = -J_B(V)/e + C_B(V) + O(e)||V||_F^2.
```

The layerwise `log e` terms cancel in the total curvature:

```text
sum_pairs h = -2 k_det,
sum_singletons k = k_det.
```

This agrees with the exact all-orders cancellation from the scaled probability identity. The proof does not claim uniformity as `lambda_min(B)->0`, and that limitation is stated explicitly.

## Minor wording note

The fixed-frame computation certifies the usable lower-bound constant `1/22` for the frame inequality. I did not verify that `1/22` is the exact optimizer value of the variational minimum kappa, and the proof does not need that stronger statement. Public wording should call it a certified frame constant or lower bound unless an exact-minimum certificate is added.

## Final review

CORRECT for:

```text
1. the upper-face compensation cone in frozen_statement.md;
2. low-event derivative injectivity with the stated exceptional pair-null family;
3. strict negative pair log curvature on the exceptional family;
4. the anisotropic supplemental upper-face inequality;
5. the fixed-B asymptotic expansion and uniform remainder in its stated scope.
```

No critical gaps found in the reviewed claims.
