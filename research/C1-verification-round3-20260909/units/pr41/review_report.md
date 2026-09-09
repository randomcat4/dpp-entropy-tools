# PR41 C1 verification round 3 review report

Status: `ACCEPTED_SCOPED` as a first fresh non-author mathematical review.

No `CRITICAL_GAPS` were found in the scoped R2-T1, R2-T2, or exact
missing-edge identity claims. Novelty, proof-assistant formalization, and the
unresolved general missing-edge/global three-dimensional concavity problem were
not reviewed.

## Sources read

- Worktree rules:
  `review-worktree/AGENTS.md`.
- Main freeze:
  `../../frozen_theorem_v1.md`.
- PR41 source snapshot:
  `source-snapshots/pr41`.

The specified `AGENTS.md` path under
`repo/research/C1-verification-round3-20260909/` did not exist; the applicable
worktree-level `repo/AGENTS.md` and matching `sources/main/AGENTS.md` were
read instead. I did not read prior review conclusions, did not use author
self-PASS as evidence, and used only the assigned source snapshot.

## Compute evidence retained

Coordination issue 45 assigned C2 the public full author-script replay and full
independent all-event/jet/block/missing-edge computation. I therefore did not
duplicate that long/full computation. I ran only a short targeted server check
for two load-bearing algebraic certificates:

- local script:
  `./targeted_pr41_checks.py`;
- remote log copied locally:
  `./targeted_pr41_checks.remote.log`;
- SHA256:
  `e7536250a0fbfd10d01e394f432d65a34e403d1474c6445b8f04f3a15f2666d5`;
- environment:
  Python 3.12.3, SymPy 1.13.3, one thread, exit 0, elapsed 2.020 seconds.

The targeted check independently verified:

1. every entry of `G_s'`, the three displayed Sylvester certificates
   `Delta_1`, `Delta_2`, and `det(G_s')`, and the limiting matrix
   `G_0=diag(2,4,0)`;
2. the two-point conditional-entropy `delta` identity, square completion,
   `2x2` determinant formula, and the monotonic proof of
   `log t <= (t-1)/sqrt(t)`.

## R2-T1: strong-coupling connected three-point family

Verdict: `CORRECT`; repository status `ACCEPTED_SCOPED`.

Relevant source locations:

- frozen statement:
  `sources/pr41/frozen_statement.md:27-67`;
- proof:
  `sources/pr41/proof.md:52-283`;
- handoff checklist:
  `sources/pr41/HANDOFF.md:5-26`.

Review:

1. The event convention is the complete-configuration DPP convention, not a
   spectral or cardinality entropy substitution. The proof starts from
   `p_K(S)=sum_{T superset S}(-1)^(|T|-|S|)det K_T` and expands all eight
   events at `proof.md:28-38`, matching the freeze at
   `frozen_statement.md:13-25`.
2. At the center with `sigma=+1`, the independent determinant reconstruction
   gives
   `q12=1/4`, `q13=q23=1/4-kappa^2`, and
   `r=1/8-kappa^2`, hence the eight probabilities at
   `proof.md:78-89` and `frozen_statement.md:50-56`. Positivity is exactly
   `0<8 kappa^2<1`, and the rare events are precisely `p0=p123=(1-s)/8`.
3. The six coordinates
   `(P, Delta, Z, R, H, N)` at `proof.md:93-106` are an invertible linear
   change of the six real symmetric directions. The first jets and the three
   grouped second-jet log sums at `proof.md:108-137` retain all eight events;
   the grouping uses only equality of the three log weights.
4. The Fisher and acceleration decomposition at `proof.md:152-213` is
   logically sufficient: the rare-event denominators remain in
   `D_s=(1-s)(1+s)`, while the acceleration uses mass conservation only to
   remove the common `-log 8` shift.
5. The only non-scalar block is `G_s`. The targeted independent check confirms
   the derivative formula at `proof.md:230-245`, the three Sylvester minors at
   `proof.md:247-259`, and `G_0=diag(2,4,0)` at `proof.md:263-267`. Since
   `G_s'=positive definite` on every `0<s<1`, the integral argument at
   `proof.md:269-272` gives `G_s` positive definite for every strict center.
6. The scalar coefficients at `proof.md:206-213` are strictly positive on
   `0<s<1`: `g>0`, `m<0`, `4s/D_s>0`, and `4s>0`.
7. The `sigma=-1` case is covered by the diagonal sign conjugacy at
   `proof.md:281-283`: principal minors, hence all event probabilities and
   entropy, are invariant under `K -> S K S`, and `D -> S D S` is a bijection
   of the six real symmetric directions. This does not shrink the direction
   quantifier.
8. The endpoint `s=1` is not claimed. The proof is pointwise on `0<s<1`, and
   the text explicitly records the rare-event limit at
   `frozen_statement.md:59` and `proof.md:91,312`.

No critical gap found.

## R2-T2: strict two-point block plus isolated point

Verdict: `CORRECT`; repository status `ACCEPTED_SCOPED`.

Relevant source locations:

- frozen statement:
  `sources/pr41/frozen_statement.md:69-96`;
- proof:
  `sources/pr41/proof.md:316-517`;
- handoff checklist:
  `sources/pr41/HANDOFF.md:28-40`.

Review:

1. For a strict real two-point kernel
   `A=[[x,a],[a,y]]`, `0<A<I_2` implies all four event probabilities at
   `proof.md:324-331` are positive. Thus
   `u=x-a^2/y` and `v=x+a^2/(1-y)` satisfy `0<u<=v<1`, with equality only
   at `a=0`.
2. The proof of concavity of `C(A)=H(X1|X2)` is complete. The reduced Fisher
   expression at `proof.md:371-375`, the acceleration log-odds term at
   `proof.md:377-388`, and the square completion at `proof.md:390-401` were
   checked independently in the targeted symbolic run.
3. The displayed log inequality at `proof.md:410-426` is valid for `t>=1`.
   The determinant bound at `proof.md:428-437` then gives a positive definite
   `2x2` matrix in the `a!=0` case. The separate `a=0` calculation at
   `proof.md:439-449` covers the boundary where `w=v-u` vanishes, so the
   proof does not divide by zero at that point.
4. The entropy decomposition `H_2(A)=h(y)+C(A)` at `proof.md:451-460` gives
   `-H_2'' >= 0` for all real two-point directions. This is semidefinite, as
   expected; at diagonal two-point kernels the off-diagonal direction can have
   zero second curvature.
5. For `K=A direct-sum [z]`, the eight event probabilities factor at the
   center as stated at `proof.md:473-479`. Cross-block directions enter
   principal minors only quadratically, so they do not affect first jets; the
   Fisher splitting at `proof.md:481-493` follows from the product score
   decomposition. The second-jet row and column marginal identities at
   `proof.md:495-508` are enough to cancel all cross-block acceleration terms
   in the complete event sum.
6. Therefore the exact six-direction identity at `proof.md:510-517` follows:
   cross-block directions `D13,D23` are included and become exact Hessian-zero
   directions at the block-plus-isolated center. The frozen claim correctly
   asks for nonnegativity, not strict positivity.

No critical gap found.

## General missing-edge event coordinates

Verdict: `CORRECT` as exact scoped identities only; repository status
`ACCEPTED_SCOPED` for the stated reduction, with the global inequality still
`INCOMPLETE`.

Relevant source locations:

- frozen exclusions and identity scope:
  `sources/pr41/frozen_statement.md:108-119`;
- proof:
  `sources/pr41/proof.md:519-612`;
- handoff checklist:
  `sources/pr41/HANDOFF.md:42-49`.

Review:

1. When `K12=0`, the marginal law of `(X1,X2)` is the independent Bernoulli
   product. Dividing the eight complete event probabilities by this marginal
   gives the four conditional probabilities
   `t_ij=z-b^2 phi_i-c^2 psi_j` at `proof.md:528-539`.
2. Differentiating these conditional probabilities along the original six
   real kernel coordinates, including the first-order effect of the missing
   edge direction `h12` through the ratio of event probabilities, gives the
   displayed `T_ij` formula at `proof.md:541-548`.
3. The map from
   `(d1,d2,d3,h12,h13,h23)` to
   `(d1,d2,T00,T10,T01,T11)` is invertible when `bc!=0`. The Jacobian at
   `proof.md:551-569` and inverse formulas at `proof.md:571-600` are
   consistent: double differences recover `h12`, first conditional contrasts
   recover `h13,h23`, and the conditional mean recovers `d3`.
4. The Fisher identity at `proof.md:603-609` follows from the exact
   conditional-score decomposition. The Bernoulli marginal scores have mean
   zero and are orthogonal to the conditional score, leaving
   `d1^2/v1 + d2^2/v2 + sum P0(i,j) T_ij^2/[t_ij(1-t_ij)]`.
5. The proof does not promote the unresolved acceleration/Schur-complement
   inequality to a theorem. The limitation is explicit at
   `proof.md:612`, `frozen_statement.md:112-119`, and
   `RESULT.md:71-87`.

No critical gap found in the exact identity scope.

## Remaining obligations

- Major new theory should still receive the planned risk-appropriate second
  independent review before mainline acceptance.
- C2 issue 45 may add a public full all-event computation ledger; this report
  did not rely on any private C2 directory and did not wait for that evidence.
- No Lean/proof-assistant formalization was performed.
- 新颖性 and literature occupation remain unreviewed.
- The general connected missing-edge family and general strict real
  three-point `K`-affine entropy concavity remain open/incomplete exactly as
  the author source states.
