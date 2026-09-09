# W1 frozen verification scope

Verifier: W1 independent non-author check.
Date: 2026-09-09.

## Fixed sources

- Local checkout constraints: `verification_20260909/repo/AGENTS.md`.
- C1 frozen verification claim: `verification_20260909/repo/research/C1-verification-20260909/CLAIM.md`.
- PR32 frozen first-round author package, fixed at commit `7c6e40bb3ba6dd0537f3c49bba83c718f86462fb`, from `verification_20260909/sources/pr32/result/`.

## Included author material before independent judgment

- `frozen_statement.md`
- `proof.md`
- `code/`
- `inputs/`
- `data/`

## Excluded material before independent judgment

- Any older review directory, old PR30 material, or `INDEPENDENT_REVIEW.md` opinion.
- Any source under `C:/canglan/`.
- Any claim that PR32 first-round rank-one evidence proves the later rank-two or general `m x 2` statement.

## Questions to certify

1. For W1 first round, independently check the full-configuration Schur probability identity
   `p_t(S,T)=a_S c_T-t^2 alpha_S gamma_T` for the stated fixed rank-one cross block, including every event, signs, invertibility, fixed marginals, degeneracies, and boundary passage.
2. Check whether the proof of entropy concavity follows from that identity on the full legal interval, distinguishing strict Jensen concavity from pointwise `H''<0`.
3. For the pending W1 second round, record that no author artifact has yet been supplied here, and separately analyze the stated target: fixed real symmetric strict contractions `A` (`m x m`) and `C` (`2 x 2`), fixed real `B` (`m x 2`), and `K(t)=[[A,tB],[tB^T,C]]`; claimed strict concavity on the full legal interval when `B != 0`.
4. For the `m x 2` target, check rank-two algebra, endpoints, degeneracy, coordinate support, and whether any argument improperly treats arbitrary orthogonal rotations as coordinate relabelings.
5. Separately track any second-round extension saying the general cross block has at most two nonzero coordinate columns. This is not the same condition as `rank(B) <= 2`, because coordinate-column support is measured in the original configuration basis.

## Output standard

The final review will use one of:

- `ACCEPTED_SCOPED`
- `NEEDS_FIX`
- `REFUTED`
- `INCOMPLETE`

The report must give exact scope, source line references, and reproducible evidence. PR32 first round receives an independent scoped verdict now. If no second-round author manuscript appears, its status must be separated from the PR32 first-round review and tied only to the transcribed claim, not to a completed proof.
