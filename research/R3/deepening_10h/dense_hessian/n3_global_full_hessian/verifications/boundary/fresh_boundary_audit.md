# U8/M10 dense rank-one boundary fresh audit

STATUS: CORRECT for the stated dense rank-one equal-soft-eigenvalue boundary
subclass and its complement.

STATUS: SCOUT for the finite rank-one / unequal-rate numerical probes.

STATUS: INCOMPLETE for the global `n=3` questions `G1/G2`; this audit does
not prove `rho<=1` over the full strict DPP domain.

Only `verifications/boundary/` was written.  I did not import or reuse the
author `rank_one_recheck.py`, `global_probe.py`, or the symbolic/point gates.

## Frozen input hashes

| file | SHA256 |
| --- | --- |
| `frozen_problem.md` | `ACFE5CBC817616C34994C6BD793367BED80429339641913E10318321091F0241` |
| `proof_or_blocker.md` | `E5FE916565DF17AF12455F123ED60FBD708B735FDA21EDA187BA2484E12243EB` |
| `boundary_asymptotic.md` | `071B7D14A40128322BF75BA146F5190099838203895615C65512E6DE59ABC2E4` |
| `derivation.md` | `E809CBD5B69E9E0648D1FF5DEE2B5472B39DD31E016EAAC9A55E15B00BCF55E5` |
| `verdict.md` | `E6EF5FA5265C1FE128E11A2E7F77270E587B8828A51B210C16344EE7EC3D33C7` |
| `run_log.md` | `C6EC109581527309B962FBED844D35688BED429C3B1A12149A1F6C766185A96F` |
| `rank_one_recheck.py` | `5121C566D621D7C66F374EBF9419364AA52F8649187751E7556B32B6D4BA6BD6` |
| `rank_one_results.json` | `7EAD2CF4A3B0A254674BD9082C3815DA9C5BD200180C51A020AB838CDD2053CB` |
| `symbolic_identity_gate.py` | `CC750BF832DB9751FB6CE430A1C992C4BA9DB52DE80C4806B8B53B374B038511` |
| `symbolic_identity_results.json` | `88924A76E49D9C30AA687090274929B28FA01AEA33AC5DCF658083CBDBDE65B1` |

## 1. Strict feasibility and support

For fixed `theta in (0,1)`, unit `u` with all `u_i != 0`, and

```text
K_epsilon = epsilon I + (theta-epsilon) uu^T,
```

the eigenvalues are `theta, epsilon, epsilon`.  Thus `0<K_epsilon<I` whenever
`0<epsilon<1` and `theta in (0,1)`.  The author's smaller range
`0<epsilon<min(theta,1/2)` is valid and also keeps `theta-epsilon` nonzero,
so every off-diagonal entry

```text
K_ij=(theta-epsilon)u_i u_j
```

is nonzero.  The observation support is therefore the full triangle for the
stated dense case.

The complement `I-K_epsilon` is also strict in the same range, with eigenvalues
`1-theta, 1-epsilon, 1-epsilon`; its off-diagonal support is again complete
because the off-diagonal entries only change sign.

## 2. Exact atoms and boundary orders

For any principal subset `T`,

```text
det(K_T)=epsilon^|T| (1+(theta-epsilon)||u_T||^2/epsilon).
```

Möbius inversion gives the exact-event orders used by the proof:

```text
p_123 = theta epsilon^2,
p_0   = det(I-K) = (1-theta)(1-epsilon)^2,
p_ij  = epsilon theta(u_i^2+u_j^2)
        + epsilon^2(1-u_i^2-u_j^2-theta),
p_i   -> theta u_i^2.
```

Since all `u_i` are nonzero and `theta in (0,1)`, the three pair atoms vanish
linearly with positive leading coefficients, the full atom vanishes
quadratically, and the empty/singleton atoms stay positive.  These are exact
DPP atoms, not a spectral count-entropy replacement.

The Fisher pole follows from differentiating the pair atoms.  For a symmetric
direction `D`, the leading pair derivative is

```text
theta(u_i^2 D_jj + u_j^2 D_ii - 2u_i u_j D_ij),
```

and division by `p_ij ~ epsilon theta(u_i^2+u_j^2)` gives

```text
F_{-1}(D,D)
= theta sum_{i<j}
  (u_i^2 D_jj + u_j^2 D_ii - 2u_i u_j D_ij)^2/(u_i^2+u_j^2).
```

The full atom gives no stronger pole because
`adj(K)=theta epsilon(I-uu^T)+epsilon^2 uu^T`, so `(dp_123)^2/p_123` is
bounded.

The kernel of `F_{-1}` is exactly

```text
T = {u v^T + v u^T : v in R^3}.
```

Indeed, the three vanishing equations determine
`D_ij=(u_i/u_j D_jj + u_j/u_i D_ii)/2`, equivalently `D=u v^T+v u^T` with
`v_i=D_ii/(2u_i)`.  Therefore the pole is positive definite on any complement
to this three-dimensional tangent space.

## 3. Full `Sym(3)` block scaling

The logarithms satisfy

```text
l_ij = -L + O(1),
Lambda = L + O(1),
L = log(1/epsilon),
```

and hence

```text
N = -diag(l23,l13,l12) - Lambda K
  = L(I-theta uu^T) + O(1).
```

This matrix is positive definite for fixed `theta in (0,1)`.

The exact `n=3` identity

```text
B(D,D)=F(D,D)-2 tr(N adj D)
```

follows by grouping the second derivatives of the exact atoms in the
coordinates `q12,q13,q23,det(K)`.  The factor two in the determinant term is
correct because

```text
det(K+tD)=det K + t tr(adj K D) + t^2 tr(K adj D) + t^3 det D.
```

Now split

```text
Sym(3)=span(uu^T)  plus two mixing directions  plus a three-dimensional normal complement.
```

In a basis beginning with `u`, a tangent element has block form
`[[alpha,v^T],[v,0]]`.  Its adjugate has support only in the lower `2x2`
block and is independent of `alpha`.  Therefore the cofactor term has no
radial/mixing leading cross term.  It contributes `2L||v||^2+O(||v||^2)` on
the two mixing directions.

After the congruence scaling

```text
radial: 1,
mixing: L^(-1/2),
normal: epsilon^(1/2),
```

the limiting quadratic form is block diagonal and positive:

- radial block: `F_0(uu^T,uu^T)=1/[theta(1-theta)]`;
- mixing block: the positive `2||v||^2` cofactor limit;
- normal block: the positive `F_{-1}` form.

The cross terms vanish at the stated rates: the `epsilon^{-1}` Fisher pole has
exact tangent kernel, bounded Fisher cross terms are killed by the scaling,
normal cofactor terms become `O(epsilon L)`, and normal/tangent cofactor cross
terms become `O(sqrt(epsilon)L)` or `O(sqrt(epsilon L))`.  The scaled matrix
therefore converges to a positive definite block diagonal limit.  Since the
scaling is invertible for `epsilon>0`, this proves full `Sym(3)` negative
entropy Hessian for all sufficiently small positive `epsilon`.

This is a full six-dimensional Hessian conclusion, not a claim only along the
rank-one ray or within PSD/commuting directions.

## 4. Moving tangent/normal Schur scalar and rho asymptotic

The sharper scalar expansion is also consistent.

After congruence by `N^{-1/2}` and division by `det N`, positivity reduces to
the rank-one threshold

```text
rho = <I,(I+Ftilde)^(-1)I>.
```

The moving tangent space is exactly

```text
T_epsilon={v_epsilon h^T+h v_epsilon^T},
v_epsilon=N^(-1/2)u,
```

because `D=N^(1/2) E N^(1/2)` lies in the fixed tangent space `T` iff
`E` lies in this pulled-back tangent space.

The orthogonal projection of `I` onto `T_epsilon` is

```text
P_epsilon = v_epsilon v_epsilon^T / ||v_epsilon||^2,
```

with Frobenius norm squared exactly one.  The corresponding original-space
direction is

```text
D_epsilon = N^(1/2)P_epsilon N^(1/2)
          = uu^T/(u^T N^(-1)u).
```

Using

```text
det N = L^3(1-theta)(1+O(1/L)),
u^T N^(-1)u = 1/[L(1-theta)] + O(L^(-2)),
F(uu^T,uu^T)=1/[theta(1-theta)] + O(epsilon),
```

one gets

```text
F(D_epsilon,D_epsilon)/det N
= 1/(theta L) + O(L^(-2)).
```

The normal inverse block contributes only `O(epsilon L)`, which is
`o(L^(-2))` as `epsilon=e^{-L}`.  Thus

```text
rho(K_epsilon)
= 1 - 1/(theta L) + O(L^(-2)).
```

The sign is important and correct: the family approaches the threshold from
below.  Therefore it rules out any proof strategy that requires a uniform
connected-domain bound `rho<=c<1`, but it does not prove the global conjectural
bound `rho<=1`.

The constants in the `O(...)` terms depend on fixed `theta,u`; no uniformity
is justified or claimed as `theta` approaches `0` or `1`, or as some `u_i`
approaches zero.

## 5. Complement family

The complement DPP maps exact atoms by `p_{I-K}(S)=p_K(S^c)`.  Entropy is
therefore invariant under `K -> I-K`, and Hessian quadratic forms are
unchanged because the affine derivative only changes sign.  The structural
`N`, Fisher form, `B`, and `rho` are correspondingly invariant in the common
observation coordinates.  Hence the same boundary result holds for
`I-K_epsilon`.

This complement transfer does not assert invariance under arbitrary
realifications or other transformations.

## 6. Independent high-precision sanity

I added `fresh_boundary_audit.py`, which imports no author module.  It uses a
second-order 3x3 shifted-determinant jet to rebuild all eight exact atoms,
their gradients and Hessians in coordinates `(11,22,33,12,13,23)`.  It also
independently evaluates the structural `rho` formula and compares
`B` from direct entropy jets against `A-det(N)eta eta^T`.

Command from repository root:

```text
C:\Users\UIO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe research\R3\deepening_10h\dense_hessian\n3_global_full_hessian\verifications\boundary\fresh_boundary_audit.py
```

Exit code: `0`; JSON status: `PASS`.

The script uses 220-digit `Decimal` arithmetic.  It checks
`u=(1,2,2)/3` and the following cases:

| theta | epsilon | rho | theta L(1-rho) | min raw `B` LDL pivot | min scaled-block LDL pivot |
| ---: | ---: | ---: | ---: | ---: | ---: |
| `1/2` | `1e-8` | `0.891939784033903545879281702938879...` | `0.995271369717003455950312600678817...` | `19.2856977133850004130886069740296...` | `0.899999825924513058885031201210437...` |
| `1/2` | `1e-16` | `0.945839403584840020551525143245277...` | `0.997675055465712948667317319653015...` | `19.7363143144179692954297391969594...` | `0.899999999999980301255378981665923...` |
| `9/10` | `1e-16` | `0.969689620778951991332200964177934...` | `1.00500807394629531389364801297268...` | `52.4956345382663251202922522204079...` | `1.61999999999999000321828140927816...` |
| `1/10` | `1e-16` | `0.766979398951056825960233953656030...` | `0.858479619737294780254571084766707...` | `53.4091707911224624781961508928182...` | `0.180000000000009554595382357450296...` |

The `theta=1/10` convergence is visibly slower at `epsilon=1e-16`, which is
not a contradiction: the proof only gives fixed-parameter asymptotics and the
hidden constants may depend on `theta`.

Additional sanity checks:

- all eight atoms are positive in every tested case;
- direct `B` is positive by Decimal LDL;
- the `1+2+3` scaled block matrix is positive by Decimal LDL;
- direct entropy-jet `B` and structural `A-det(N)eta eta^T` agree to at least
  `1e-180`;
- complement rho matches the original rho to tiny Decimal error
  (`~1e-195` or smaller in the tested cases).

These finite checks only guard constants and semantics.  They are not used as
proof of the continuous boundary theorem.

Generated files:

- `fresh_boundary_audit.py`
- `fresh_boundary_audit.json`

## 7. Scope audit

The author scope boundaries are correct:

- The boundary theorem covers equal soft eigenvalues
  `epsilon,epsilon,theta` only.
- Unequal soft-eigenvalue rates remain outside the proof.
- Vanishing coordinates of `u`, `theta -> 0`, and `theta -> 1` are excluded
  from uniform claims.
- The 18 equal-rate plus 12 unequal-rate boundary probes in the author run log
  are SCOUT only.
- The asymptotic `rho -> 1^-` rules out a uniform separation
  `rho<=c<1` on all connected strict kernels.
- It does not prove global `rho<=1`, global Hessian positivity, or connected
  global positive definiteness.

## Final layered verdict

- Strict feasibility and dense support: CORRECT.
- Exact atom asymptotics and event semantics: CORRECT.
- Fisher pole, tangent kernel, and normal positivity: CORRECT.
- `1+2+3` full-`Sym(3)` block scaling proof: CORRECT.
- Moving tangent/normal Schur expansion and
  `rho=1-1/(theta log(1/epsilon))+O(log^-2)`: CORRECT.
- Complement family transfer: CORRECT.
- Finite boundary probes: SCOUT only.
- Global `n=3` full-Hessian questions: INCOMPLETE.

No critical gap requiring author repair was found.
