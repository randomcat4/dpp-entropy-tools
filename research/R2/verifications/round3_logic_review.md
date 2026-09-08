# Round 3 independent logic review and commit binding

STATUS: CORRECT

## Part I: mathematical review

JUSTIFICATION:

I verified the anonymous component proof only against the frozen v2 statement,
`hazards.md`, `lemma_ledger.md`, `tomography_components.md`, and
`component_pair_C2_proof.md`.  I did not revise the theorem or proof, and I did
not use numerical evidence as a substitute for the argument.

## Scope checked

The proof addresses the frozen decision problem: under the full one-hole and
one-particle tomography equalities, prove the finite coefficient `C2<=0` for
arbitrary finite real orthogonal frames, singular `A,C`, singular endpoints,
zero Pluecker coordinates, simultaneous nonzero `X,Y`, and non-paired
components.  Strict negativity is treated only as an additional strengthening,
not as part of the frozen claim.

## Component/tomography reduction

The inverse-matrix argument in `tomography_components.md` is sound.  The
cofactor identity

```text
tr[X adj(sum_i z_i u_i u_i^T)]
  = sum_{|R|=r-1} z_R alpha_R^T X alpha_R
```

is a Cauchy-Binet/adjugate coefficient identity and includes `r=1`.  Since
`G(1)=I`, division by `det G(z)` is only made on a genuine neighborhood of an
invertible point.  In the resulting Neumann series, the squarefree coefficient
on a shortest nonorthogonality path has no hidden repeated-index terms and no
extra nonzero Hamiltonian orders: the induced graph of a shortest path has only
the forward and reverse Hamiltonian paths.  Hence the coefficient is exactly
twice the nonzero edge product times `u_j^T X u_i`, forcing all within-component
bilinear entries to vanish.  The converse follows because the inverse is block
diagonal when `X` has zero diagonal component blocks.  Thus the tomography
kernel equivalence is valid.

The low-side statement is also valid.  For `Q=VV^T=I-P`, the off-diagonal graph
is the same because `Q_ij=-P_ij` for `i!=j`; isolated vertices cause no
exception.  The one-particle `beta_T` measurements are, up to signs irrelevant
to the quadratic constraints, the complementary one-hole cofactors for `V`.
This gives the same block-kernel conclusion for `Y`.

## Cross terms

The active-support cross cancellation is correct.  On active product events
the replacement matrix is block diagonal; off-component replacements have
incompatible local row counts and vanish.  For every component,

```text
sum_active psi_a T_{a,S_a}=0
```

by exterior orthogonality/Cauchy-Binet.  In the active cross sum, a factor
`log p_S=sum_h log p_h` leaves at least one unweighted local factor of this
form, so both the logarithmic weighted and unweighted active `q(X,Y)` sums are
zero.  This does not require uniform local probabilities or paired frames.

The zero-support cross term is also correctly shown to vanish eventwise.  If
`rank U_S<=r-2`, then `T_S=adj(U_S)V_S=0`.  If `rank U_S=r-1`, writing
`T_S=a b^T`, a nonzero high cofactor from independent rows in `S` is
proportional to `a`, hence tomography gives `a^T X a=0`.  A row
`k notin S` with `u_k^T a!=0` exists by full column rank of `U`; the bordered
minor for `S union {k}` is proportional to `b`, so the low tomography gives
`b^T Y b=0`.  Therefore `q_S(X,C)=q_S(A,Y)=q_S(X,Y)=0` pointwise, including
the cases where one of the factor vectors is zero.

## High-side pair formula

The global cofactor scaling and constants in (11)--(14) check out.

For a one-hole event deficient in component `a`, the global cofactor is
`(prod_{c!=a} psi_c) alpha`.  Consequently

```text
m_R(A)=w g,
m_R(X^2)=w alpha^T (sum_{b!=a} X_ab X_ba) alpha,
sum w log w = -(H_P-H_a).
```

Together with the active drift allocation
`tr X^2/2=sum_{a<b}||X_ab||_F^2` and the local Parseval identities, the
active-plus-one-hole contribution per cofactor pair is exactly

```text
[H_P-H_a-H_b-1-log(gh)] x^2.
```

No global Pluecker scaling factor is lost here.

For two-hole events, the classification is complete: a nonzero global
two-deletion cofactor cannot select more than `r_c` rows from any component,
so the total deficit two is either both holes in one component or one hole in
each of two components.  Same-component holes are unchanged because `X_aa=0`.
For holes in components `a,b`, the compound identity has no missing factor of
two:

```text
<alpha wedge beta, Lambda^2(A-sigma X)(alpha wedge beta)>
  = gh-(u-sigma x)^2.
```

Summing over the remaining active factors gives the two-hole finite term

```text
f(d0)-[f(d+)+f(d-)]/2 -(H_P-H_a-H_b)x^2,
```

because `d0-(d++d-)/2=x^2`.  Adding this to the active/one-hole expression
leaves exactly

```text
f(D-u^2)-[f(D-(u+x)^2)+f(D-(u-x)^2)]/2 -(1+log D)x^2.
```

The identity

```text
f(D-v^2)+(1+log D)v^2 = D log D + Phi_D(v)
```

then converts the term to the claimed scalar Jensen gap `gamma_D(u,x)`.

The low-side derivation is the same with the local `beta` cofactor Parseval
frame.  The entropy weights are still the high projection local entropies
`H_a`, since the other components remain in their active projection
configurations.

## Boundary and sign checks

The singular cases are covered.  From the PSD compressions

```text
[[g,u+x],[u+x,h]] >= 0,
[[g,u-x],[u-x,h]] >= 0,
```

one gets `|u +/- x|<=sqrt(gh)`.  If `g=0`, then the quadratic form of both
`A+X` and `A-X` at `alpha` is zero; PSD implies both matrices annihilate
`alpha`, hence `A alpha=X alpha=0` and therefore `u=x=0`.  The case `h=0` is
identical, so the convention that `D=0` contributes zero introduces no hidden
loss.  If `D>0` but `d0=0`, the two endpoint inequalities force `x=0`.  If
`d+` or `d-` is zero, `f(0)=0` and the continuous boundary value of `Phi_D` is
well-defined.  Thus no logarithm of zero is used.

For `D>0`,

```text
Phi_D''(v)=-2 log(1-v^2/D)+4v^2/(D-v^2) >= 0
```

on the interior, with strict convexity on every nondegenerate interval after
continuous extension to the boundary.  Hence every scalar pair term
`gamma_D` is nonpositive, and the sums in (9) and (16) prove `C2<=0`.

The strictness strengthening is also consistent: if `X` is nonzero then some
off-block `X_ab` is nonzero, and the two local Parseval frames give a cofactor
pair with `x!=0`; the PSD boundary argument rules out `gh=0` for that pair,
so strict convexity gives one strictly negative summand.  The same reasoning
applies to nonzero `Y`.  This is not needed for the frozen nonpositive claim.

## Verdict

I found no critical gap in the component proof.  The proof covers the listed
hazards: exact-event layering, tomography-kernel equivalence, complementary
`V` cofactors, global cofactor scaling, active logarithmic cancellation,
zero-support eventwise cancellation, two-hole classification, constants in
(11)--(14), singular rates/endpoints, and strictness as a separate
strengthening. 

## Part II: commit-bound gate

## Commit-bound scope

Candidate commit:

```text
3ae3323ae958feb733b78f5b425c6d9b540524e9
```

This report is a one-time commit-bound gate for the component-pair proof I
previously reviewed in
the mathematical review in Part I.
No theorem revision, proof extension, numerical search, SHA gate beyond this
binding, or public-checkout edit was performed.

The public checkout
`the public checkout`
was checked before and after the read-only hash operation:

```text
git status --short
<empty>
```

Thus the public working tree remained clean and unchanged during this gate.

## Hash table

All hashes below were computed from git blobs at the fixed commit, without
checking out or modifying the commit.

| Role | Commit path | Expected SHA256 | Observed SHA256 | Result |
|---|---|---:|---:|---|
| frozen v2 | `research/R2/frozen_theorem_v2.md` | `789368b0df3197d8f97f0b200f3a70e6f9a7354f8bc4c97c3d11e45021a77287` | `789368b0df3197d8f97f0b200f3a70e6f9a7354f8bc4c97c3d11e45021a77287` | MATCH |
| b_zero decomposition | `research/R2/proofs/b_zero_c2_decomposition_v2.md` | `c2e9f157158cc6d376101ee12ba794bb1afb21f5b61606f1b48266c93f6e2dbb` | `c2e9f157158cc6d376101ee12ba794bb1afb21f5b61606f1b48266c93f6e2dbb` | MATCH |
| tomography components | `research/R2/proofs/tomography_components_v3.md` | `5641f161415331ee6a9185449f342d64c2f93755f52ea38a821cef9a8285e2eb` | `5641f161415331ee6a9185449f342d64c2f93755f52ea38a821cef9a8285e2eb` | MATCH |
| component C2 proof | `research/R2/proofs/component_pair_C2_v3.md` | `72a8596e58e957c19833eae7284419671ebf9709f6bfdd948165f29ccdbb86ee` | `72a8596e58e957c19833eae7284419671ebf9709f6bfdd948165f29ccdbb86ee` | MATCH |
| hazards | `research/R2/hazards.md` | `792afa93e166d30bf768637585e271dad4a413da546742f8db577b70059777e1` | `792afa93e166d30bf768637585e271dad4a413da546742f8db577b70059777e1` | MATCH |

## Binding verdict

The fixed commit exists and all five supplied SHA256 values match the exact
public blobs at that commit.  These hashes bind the public frozen statement,
the public finite `C2` decomposition relied on by the frozen theorem, the
tomography-component structural proof, the component-pair `C2` proof, and the
hazard list to the content scope of my prior component-pair verification.

Since the commit-bound content matches the supplied hashes and my prior
mathematical conclusion was `STATUS: CORRECT`, the commit-bound conclusion is
unchanged:

```text
STATUS: CORRECT
```

