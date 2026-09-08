# D10-U8/M10 `n3_global_full_hessian` fresh main audit

STATUS: CORRECT for the main structural reduction in `derivation.md`; INCOMPLETE for the global inequality `rho(K)<=1`.

I audited the main structure theorem only.  I did not import `global_probe.py`, `rank_one_recheck.py`, `point_interval_gate.py`, `symbolic_identity_gate.py`, or any boundary verifier.  I also did not certify the separate moving-boundary asymptotic theorem in `boundary_asymptotic.md`.

The correct reading is:

- the exact rank-one-defect representation is certified;
- the connected-kernel problem is reduced to the scalar threshold `rho(K)<=1`;
- the weighted trace-zero five-dimensional subspace has strict negative entropy curvature at every connected strict kernel;
- finite 510-point evidence remains SCOUT;
- this audit does not prove global concavity or global `rho<=1`.

## Files written by this audit

- `fresh_main_audit.py`
- `fresh_main_audit.json`
- `fresh_main_audit.md`

Final command:

```text
C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe research\R3\deepening_10h\dense_hessian\n3_global_full_hessian\verifications\main\fresh_main_audit.py
exit code: 0
elapsed: 0.024168968200683594 seconds
```

## Frozen input hashes

| input | SHA256 |
|---|---|
| `frozen_problem.md` | `acfe5cbc817616c34994c6bd793367bed80429339641913e10318321091f0241` |
| `derivation.md` | `e809cbd5b69e9e0648d1ff5dee2b5472b39dd31e016eaac9a55e15b00bcf55e5` |
| `boundary_asymptotic.md` | `071b7d14a40128322bf75ba146f5190099838203895615c65512e6de59abc2e4` |
| `proof_or_blocker.md` | `e5fe916565df17af12455f123ed60fbd708b735fda21eda187ba2484e12243eb` |
| `run_log.md` | `c6ec109581527309b962fbed844d35688bed429c3b1a12149a1f6c766185a96f` |
| `verdict.md` | `e6ef5fa5265c1fe128e11a2e7f77270e587b8828a51b210c16344ee7ec3d33c7` |
| `global_probe.py` | `1b171442be0ffa070cfc535e6b3067ca8f3a13ac0861c717a4129d540d52d347` |
| `rank_one_recheck.py` | `5121c566d621d7c66f374ebf9419364aa52f8649187751e7556b32b6d4ba6bd6` |
| `point_interval_gate.py` | `5baff127ef57e369597dcec228f47a0065acda0f3d0ce1190cb9be348895a876` |
| `symbolic_identity_gate.py` | `cc750bf832db9751fb6ce430a1c992c4ba9db52de80c4806b8b53b374b038511` |
| `scout_results.json` | `eec04bb7a6f6f92ccf757ac01e79cac4a74ab081d4001b915dda70a3fd4686d3` |
| `rank_one_results.json` | `7ead2cf4a3b0a254674bd9082c3815da9c5bd200180c51a020ab838cdd2053cb` |
| `point_interval_results.json` | `dbaaefee51ed61b6f1c0fe07558743bc3b4a63d875ea5eab3a8f5fe3247cce88` |
| `symbolic_identity_results.json` | `88924a76e49d9c30aa687090274929b28fa01aea33ac5dcf658083cbdbde65b1` |

## Exact atoms and log coefficients

CORRECT.

Using

```text
K = [[x,a,b],[a,y,c],[b,c,z]],
q12=xy-a^2, q13=xz-b^2, q23=yz-c^2,
r=xyz+2abc-xc^2-yb^2-za^2,
```

I rebuilt the eight exact atoms:

```text
p123=r
p12=q12-r, p13=q13-r, p23=q23-r
p1=x-q12-q13+r
p2=y-q12-q23+r
p3=z-q13-q23+r
p0=1-x-y-z+q12+q13+q23-r
```

These are exactly the Möbius inversion of inclusion minors.  For strict `0<K<I`, all exact atoms are positive by the standard L-ensemble factorization: `L=K(I-K)^(-1)>0`, and exact atoms are positive principal-minor factors times `det(I-K)`.

The fresh symbolic checker verifies:

```text
sum_S p_S = 1
sum_S p_{S,i} = 0 for all six coordinates
sum_S p_{S,ij} = 0 for all coordinate pairs
p_{S,ii}=0 for all events and diagonal rank-one coordinates E11,E22,E33
```

## Conditional-odds square identities and signs

CORRECT.

For each pair `{i,j}` and complement `k`, the fresh polynomial checker proves both identities:

```text
p0*pij - pi*pj      = -((1-Kkk)Kij + Kik*Kjk)^2
pk*p123 - pik*pjk   = -(Kkk*Kij - Kik*Kjk)^2
```

All three pairs pass exactly.  The square-term counts match the author record: 6 terms for the absent-conditioned square and 3 terms for the present-conditioned square.

Because all atoms are positive:

```text
l_ij = log(p0*pij/(pi*pj)) <= 0
l_ij + Lambda = log(p123*pk/(pik*pjk)) <= 0.
```

The `Lambda=0` connected case is also sound.  If `Lambda=0` and `l_ij=0`, both square equations vanish.  Adding

```text
(1-Kkk)Kij + Kik*Kjk = 0
Kkk*Kij - Kik*Kjk = 0
```

gives `Kij=0`, then `Kik*Kjk=0`.  In a connected three-vertex support graph, every pair has either its own edge or a two-edge path, so this simultaneous vanishing cannot occur for any pair.  Hence all three `l_ij<0` and `N` is positive definite in the `Lambda=0` connected branch.

## The matrix `N`

CORRECT.

With

```text
N = -diag(l23,l13,l12) - Lambda K,
```

the two nonzero-`Lambda` branches check analytically:

- If `Lambda>0`, then `-l_ij>=Lambda`, so
  `N - Lambda(I-K) = diag(-(l23+Lambda), -(l13+Lambda), -(l12+Lambda)) >= 0`.
  Since `I-K>0`, this gives `N>0`.
- If `Lambda<0`, then `-l_ij>=0`, so
  `N - (-Lambda)K = diag(-l23,-l13,-l12) >= 0`.
  Since `K>0`, this gives `N>0`.
- If `Lambda=0`, `N` is diagonal nonnegative; it is strictly positive definite under connected support by the square-vanishing argument above.

Fresh Decimal/Fraction samples cover all relevant branches:

| sample | `(x,y,z,a,b,c)` | support | exact Lambda ratio | Lambda branch |
|---|---|---|---|---|
| positive | `(1/4,1/4,1/4,-1/5,-1/5,1/8)` | connected | `404481033/227124233` | `Lambda>0` |
| negative | `(1/4,1/4,1/4,-1/5,-1/5,1/12)` | connected | `176157/480557` | `Lambda<0` |
| zero/disconnected | `(1/3,2/5,3/7,0,0,0)` | disconnected | `1` | `Lambda=0`, `N=0`, inverse-`N` Schur formula not applicable |

For the two connected samples, the direct `B` formula, the cofactor formula, and the Schur formula agree to at least `1e-85` in 110-digit Decimal arithmetic.

## Hessian/cofactor identity

CORRECT.

The author identity

```text
B_K(D,D)
 = Fisher_K(D,D)
   + 2 sum_{i<j} l_ij det(D_ij)
   + 2 Lambda tr(K adj D)
```

is equivalent to

```text
B_K(D,D)=Fisher_K(D,D)-2 tr(N adj D).
```

The factors of two are correct:

- `qij(K+tD)'' = 2 det(D_ij)`;
- `det(K+tD) = det K + t tr(adj K D) + t^2 tr(K adj D) + t^3 det D`, hence the second derivative contributes `2 tr(K adj D)`;
- the exact-event Hessian uses `sum_S p_{S,ij}=0`, so the acceleration term is `sum_S p_{S,ij} log p_S`.

The script verifies this identity directly on connected samples by reconstructing all eight atom jets in the coordinate basis `(11,22,33,12,13,23)`.

## Adjugate congruence and Schur scalar

CORRECT.

For connected kernels, `N>0`, so the inverse-`N` reduction is legitimate.  The exact algebraic identity checked is

```text
tr(N adj D)
 = det(N)/2 * ((tr(N^-1 D))^2 - tr(N^-1 D N^-1 D)).
```

The verifier also checks this identity exactly over Fractions for an independent rational positive definite `N` and rational symmetric `D`.

Define

```text
eta_i = tr(N^-1 E_i)
A_ij = Fisher(E_i,E_j) + det(N) tr(N^-1 E_i N^-1 E_j).
```

Then

```text
B = A - det(N) eta eta^T.
```

`A` is positive definite because `D -> tr(N^-1 D N^-1 D)` is a positive definite quadratic form on `Sym(3)` and Fisher is positive semidefinite.  Therefore the rank-one update has the standard inertia threshold:

```text
rho = det(N) eta^T A^-1 eta
rho<1  iff B>0
rho=1  iff B has one zero mode and five positive modes
rho>1  iff B has exactly one negative mode
```

The bad direction formula is also correct:

```text
d = A^-1 eta,
d^T B d = (eta^T A^-1 eta)(1-rho).
```

This is an equivalence/reduction, not a proof that `rho<=1`.

## Coordinate and Frobenius factors

CORRECT.

The off-diagonal coordinate convention is handled correctly: coordinate `12` means the symmetric matrix `E12+E21`.  Consequently

```text
eta_12 = 2(N^-1)_12,
eta_13 = 2(N^-1)_13,
eta_23 = 2(N^-1)_23.
```

The fresh Decimal checks confirm these residuals vanish on connected samples.

For individual coordinates:

- diagonal rank-one coordinate accelerations satisfy `p_S''=0`, hence `B(Eii,Eii)=F(Eii,Eii)>0`;
- for off-diagonal coordinate `Eij+Eji`, `adj(D)` has `-1` in the complementary diagonal cofactor, giving
  `B(Eij+Eji,Eij+Eji)=F(Eij+Eji,Eij+Eji)+2Nkk`.

Thus every individual observation coordinate is strictly concave at connected strict kernels.  This still does not imply full joint concavity.

## Five-dimensional weighted trace-zero subspace

CORRECT.

At connected strict `K`, `N>0`.  The hyperplane

```text
T_K = {D in Sym(3): tr(N^-1 D)=0}
```

has dimension five.  On it, the negative rank-one term disappears and

```text
B(D,D)
 = Fisher(D,D) + det(N) tr(N^-1 D N^-1 D)
 >= det(N) ||N^-1/2 D N^-1/2||_F^2
 >= det(N)/lambda_max(N)^2 * ||D||_F^2 > 0.
```

Equivalently, the entropy Hessian is strictly negative on this entire five-dimensional subspace.  The bound is pointwise in `K`; it is not a uniform global separation because `N` may degenerate near disconnected or boundary regimes.

## Complement invariance

CORRECT.

The proof's substitution is sound:

```text
p'_S = p_{S^c},
Lambda(I-K) = -Lambda(K),
l'_ij = l_ij + Lambda.
```

Then

```text
N(I-K)
 = -diag(l'23,l'13,l'12) + Lambda(I-K)
 = -diag(l23,l13,l12) - Lambda K
 = N(K).
```

The Hessian/Fisher forms match under the complement map because entropy is invariant under set complement and the affine direction changes sign, which does not affect the second derivative.  This is useful symmetry, not a realification or gap-transfer principle.

## Finite evidence

SCOUT only.

Frozen finite ledgers are internally consistent with the author's stated scope:

```text
scout ledger count: 510
connected: 420
disconnected: 90
status counts: SCOUT = 510
minimum normalized_min_B: 2.2499372909546757e-05
rank-one scalar ledger: 420 connected centers
equal-rate boundary probes: 18
unequal-rate boundary probes: 12
point interval gate: index 241, min atom 1/2000000000000
```

These facts do not prove G1, G2, or `rho<=1`.

## Layered verdict

- Exact atom formulas and positivity domain: CORRECT.
- Conditional-odds square identities: CORRECT.
- `l_ij<=0` and `l_ij+Lambda<=0`: CORRECT.
- `N>=0` for strict kernels and `N>0` for connected strict kernels: CORRECT.
- `Lambda=0` connected strictness via square-vanishing graph argument: CORRECT.
- `B=Fisher-2tr(N adjD)`: CORRECT.
- Adjugate congruence and `B=A-det(N)eta eta^T`: CORRECT.
- `rho` threshold and bad direction: CORRECT.
- Weighted trace-zero five-dimensional strict subspace: CORRECT.
- Coordinate/Frobenius factors: CORRECT.
- Complement invariance: CORRECT.
- Finite 510-point no-hit evidence: SCOUT only.
- Global `rho(K)<=1`, G1, and G2: INCOMPLETE / not proved.

No critical gap found in the main structural theorem as a reduction.  The remaining global problem is exactly the DPP-specific scalar inequality for `rho`, as the author states; this audit does not close it.
