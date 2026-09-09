# Frozen scope - PR43 rank-two E-H second review

Reviewer role: fresh non-author second mathematical reviewer for PR #43 clauses E-H. No descendant agents were used. No other reviewer reports were read.

## Source binding

PR43 source snapshot:

`source-snapshots/pr43_7bd5962`

Binding file: `SOURCE_BINDING.json`

- PR: 43
- Commit: `7bd5962bbb2020ce47fbe286adda7dfe02f9645d`
- Prefix: `research/I05-W1-20260909-R2/`
- Previous commit: `4e1369ef2a59ccfaba3ca8fce95d85e78857bf78`

Imported C3 diagonal-anchor dependency:

`source-snapshots/dependency_c3`

Binding file: `C1_SOURCE_BINDING.json`

- PR: 29
- Commit: `648f1906468e3e548410f98a6b1a53a978f2ea11`
- Prefix: `research/C3/`
- Origin: GitHub Git data API, public immutable commit

## Instructions read

- `workflow/math-theorem/SKILL.md`
- `workflow/math-theorem/references/prompt-library.md`
- `workflow/math-theorem/references/openai-workflow.md`
- `review-worktree/AGENTS.md`
- `inherited-worktree/AGENTS.md`
- `source-snapshots/main/AGENTS.md`


## Mathematical files reviewed

Current frozen continuation:

- `continuation/frozen_statement_v3.md`, version v3.1, especially lines 20-169 for clauses E-H.
- `continuation/proof_v3.md`, proof index and dependency map.

Standing PR43 definitions and inherited assumptions:

- `frozen_statement.md`, especially lines 23-45 for strict kernels, block setup, strict legal interval, and closed legal interval; lines 49-86 for conditional Schur and radial lifting; lines 112-162 for rank-two exterior likelihood.

Root proof dependencies:

- `proof/01_conditioning.md`
- `proof/02_two_point_input.md`
- `proof/03_lifting_and_exterior.md`
- `proof/04_three_point_indefinite_rank2.md`
- `proof/05_diagonal_and_feature_routes.md`
- `proof/06_correlated_3plus3_family.md`

Imported C3 dependency:

- `dependency_c3/frozen_statement_v2.md`
- `dependency_c3/proof.md`

## Files intentionally not used


## Frozen claim scope

The reviewed PR43 claims are:

- E: real strict three-point DPP entropy is concave along every real indefinite rank-two affine direction, with boundary extension.
- F: rank-two exterior likelihood gives exact sufficient statistics under `(G_A,G_C)`, preserves KL/mutual information, and yields the exact compressed Hessian with full event Fisher plus one exterior acceleration scalar.
- G: for right block size three and `rank(B) <= 2`, if every conditional direction `M_S` is rank at most one, indefinite rank two, or lies on a line through a strict diagonal kernel, then the radial cross-block entropy is concave; strict if `B != 0`.
- H: the specified `3+3` family with `A=alpha P+beta nn^T`, `rank(B)=2`, `n^T B=0`, and `C=D_0+eta B^T B` strict satisfies G for all eight left configurations, hence has strict radial concavity when `B != 0`; the explicit dense rational example has the stated exact radius.

## Scope verdict

No critical gap was found in the E-H concavity proofs. I found one non-critical descriptive quantifier error: the sentence saying `A,C` are both non-diagonal when `alpha != beta` and `M_0` has a nonzero off-diagonal entry is false if the allowed parameter `eta` is zero. The theorem remains true; the descriptive sentence should add `eta != 0` or be weakened.
