# n=3 full-Hessian program: U8 and U10a–g

**Global status: INCOMPLETE.** This directory studies Shannon entropy of all
eight exact events of a real symmetric strict DPP kernel, `0<K<I`.
Probabilities are obtained by Möbius inversion of inclusion minors; they are
not `det(K_S)`. Hessian directions range over all `Sym(3)`, not just PSD,
commuting, or family-tangent directions. See the [frozen problem](frozen_problem.md).

## Reviewed structure and the remaining threshold

For connected support, U8 gives `N>0` and an exact representation

```text
B = -Hess H = A - δ ηηᵀ,
A = Fisher + δ G_N > 0,   δ = det N,
ρ(K) = δ ηᵀ A⁻¹η.
```

Thus `ρ<1` is equivalent to `B>0`; `ρ=1` gives one null direction;
`ρ>1` gives one positive entropy-curvature direction. On the five-dimensional
hyperplane `tr(N⁻¹D)=0`, entropy curvature is strictly negative. There is at
most one remaining nonnegative Hessian eigenvalue. These are reviewed
structural results, **not a proof that `ρ≤1` globally**.
[Derivation](derivation.md) · [main audit](verifications/main/fresh_main_audit.md)

The reviewed dense rank-one boundary subclass and its complement have
eventual full-Hessian negativity, with `ρ→1` from below. Consequently no
uniform bound `ρ≤c<1` can hold over the whole connected strict domain.
[Boundary proof](boundary_asymptotic.md) · [boundary audit](verifications/boundary/fresh_boundary_audit.md)

## Route navigation

| Route | Reviewed outcome and status | Read first |
|---|---|---|
| **U8** | **CORRECT, scoped:** rank-one-defect reduction, five-dimensional strict subspace, and stated boundary subclass. General n=3: **INCOMPLETE**. | [Verdict](verdict.md), [remaining inequality](proof_or_blocker.md) |
| **U10a — direct scalar** | **CORRECT, scoped:** score-projection identities, sufficient tests, and exact proxy blockers. The three retained conditional-score corrections recover the full scalar exactly. | [Derivation](scalar_direct/derivation.md), [non-author audit](scalar_direct/audit_nonauthor/verdict.md) |
| **U10b — information** | **CORRECT_SCOPED:** ridge/Bessel equivalence and a Fisher-only shortcut blocker; no global energy bound constructed. | [Reformulation](scalar_information/proof_or_blocker.md), [non-author audit](scalar_information/audit_nonauthor/verdict.md) |
| **U10c — falsification** | **SCOUT after fresh repair recheck:** corrected p0 jet; 445 reconstructed attempts, 444 strict valid points, one exact rejection, zero credible `ρ>1`. | [Fresh recheck](scalar_falsification/fresh_repair_audit/verdict.md), [results](scalar_falsification/fresh_repair_audit/results.json) |
| **U10d — symmetric paths** | **CORRECT for the centered full-Hessian theorem:** `K(1/2,a)` for every `0<8a²<1`. General `K(x,a)`: **INCOMPLETE**. | [Proof](symmetric_path_subfamily/derivation.md), [non-author audit](symmetric_path_subfamily/audit_nonauthor/verdict.md) |
| **U10e — general symmetric path** | Reflection-odd strictness and reduction of the even block to one scalar `σ(x,a)`; boundary/double-scale analysis is **author-side INCOMPLETE/SCOUT**, with fresh audit pending. | [General reduction](symmetric_path_global/derivation.md), [full-atom boundary](symmetric_path_global/boundary_full_atom/analysis.md) |
| **U10f — exchangeable triangle** | **CORRECT, scoped:** exact `S3` split, automatic strictness on the four-dimensional standard block, and a punctured-diagonal compact-neighborhood theorem. The full two-parameter determinant inequality is **INCOMPLETE**. | [Reduction](exchangeable_triangle_subfamily/proof_or_blocker.md), [fresh audit](exchangeable_triangle_subfamily/fresh_audit.md) |
| **U10g — connected `Λ=0`** | Weighted-Cauchy `L` parameterization, exact field-score identities, a retained `3×3` Schur gate, and an explicit full-Hessian ball are **proof candidates pending fresh audit**; the whole submanifold is **INCOMPLETE**. | [Derivation](lambda_zero_subfamily/derivation.md), [explicit neighborhood](lambda_zero_subfamily/proof_or_blocker.md) |

The linked non-author reports determine reviewed scope; older author notes
may retain their pre-review “pending” labels. Same-author self-review is not
used as independent certification.

## What the information reformulation does—and does not—prove

With `M_S=∇_F p_S`, the reviewed ridge identity is

```text
ρ(K) = min_g { ||I - N½(Σ_S g_S M_S)N½||²_F
              + det(N) Σ_S p_S g_S² }.
```

This is equivalent to the original scalar problem; writing the minimum does
not bound it by one. Universal Fisher-only/trace-capacity shortcuts have
been ruled out. Even the complement-adaptive five-category proxy fails at
an explicit strict rational path: its proxy has `B_T(D)<0`, while the actual
`B(D)>28.680`. **These are failures of proof shortcuts, not entropy
nonconcavity counterexamples.** The six-category test's 29/29 finite passes
remain **SCOUT**. [Exact blocker and retained score contrasts](scalar_direct/derivation.md)

U10c's repaired best values are approximately `0.9950999446` and, for unequal
soft rates, `0.9932525031`; a float apparent threshold near one reconstructs
as approximately `0.5`. Its `38436 / 22023` float totals are compact-accounting
checks, not full seed regeneration. The fresh report records the corrected
near-threshold count **69**, and distinguishes 15 top-float attempts from
14 valid points. [Coverage and metadata caveats](scalar_falsification/fresh_repair_audit/verdict.md)

## Exact open endpoints

- **General connected n=3:** prove `ρ(K)≤1` (strict `<1` for definiteness).
  U10a equivalently writes `ρ=R_T−c₁−c₂−c₃`; when `R_T>1`, the missing
  inequality is `c₁+c₂+c₃≥R_T−1`. This is an **equivalent blocker**, not a
  solved weaker lemma. [Equation (27)](scalar_direct/derivation.md)
- **General symmetric path:** for
  `K(x,a)=[[x,a,0],[a,x,a],[0,a,x]]`, strict feasibility is
  `0<√2|a|<min(x,1−x)`. The reflection-odd block is strict; the remaining
  exact condition is the even-block Schur scalar `σ(x,a)>0`. The centered
  line and the stated compact-neighborhood thickening are reviewed, but the
  full two-parameter domain is not. [Equation (10) and scope](symmetric_path_subfamily/derivation.md)
- **Exchangeable triangle:** for `K=xI+a(J-I)`, the standard four-dimensional
  representation block is settled.  The remaining global question is exactly
  positivity of the explicit `2×2` invariant-block determinant
  `Delta_T(alpha,beta)`.  Compact punctured neighborhoods of the disconnected
  diagonal are proved; the rest of the square is open.
- **Connected `Lambda=0`:** after sign gauge, the candidate Cauchy
  parameterization is `L_ij=w_iw_j/(z_i+z_j)`.  The full-Hessian question is
  reduced to a retained `3×3` Schur gate.  An explicit small ball around the
  centered path blocker is author-proved and awaiting independent review; no
  global sign over this submanifold is claimed.

For replay files and older U8 data, see [artifact navigation](ARTIFACTS.md).
Finite non-hits anywhere in this directory are not global concavity proofs.
