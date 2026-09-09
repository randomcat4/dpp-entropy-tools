# Frozen Scope: PR60 Second Mathematical Review

Reviewer: independent second reviewer for PR60 frozen author packet.
Date: 2026-09-10, Asia/Singapore.

## Binding

Input directory: `research/I05-22-R3-lambda-zero-global`

Adjacent binding file: `input_binding.json`

Frozen PR: 60.

Frozen head: `f869fd251c0d6fdad737b6d5efa287307795a87d`.

Base named by task: `9dcb6e9079ca57f94e0e30d63161cda89ca61fae`.

Author prefix: `research/I05-22-R3-lambda-zero-global/`.

The input packet contains exactly the eight bound author files listed in `input_binding.json`: `README.md`, `bridge_checks.py`, `certificate.py`, `continuation.md`, `continuation_exact.py`, `proof.md`, `sources_routes.md`, and `verification.md`.

## Review Rules Used

I did not run arithmetic, SymPy, entropy jobs, formal tools, remote jobs, or author assertions. I used static proof inspection, static source inspection, public accepted-scope notes explicitly cited by the author, and file hashes. I did not use PR57 as a premise for the full-r result. I did not open prior PR60 reviews, PR discussions, or C1 review reports.

The accepted public repository premises I used were limited to the actual stated scopes in:

- `docs/verification_round3_20260909/accepted_pr51.md`
- `docs/verification_round3_20260909/archived_pr55.md`

Those notes accept the general missing-edge identities and Lambda-zero handoff algebra only within their stated scope; they explicitly do not accept the global four-dimensional Schur positivity or the r=0/full-r positivity theorem.

## Units and Verdicts

| Unit | Verdict | Accepted Scope | Exclusions |
| --- | --- | --- | --- |
| U1. Full Lambda-zero missing-edge family, all r and unequal diagonals | INCOMPLETE | The analytic chain from complete events through fixed-direction Hessian, Schur reduction, determinant nonvanishing, inertia, and integration is coherent conditional on an exact determinant/chart certificate. The accepted PR51/PR55 scopes cover the event/Fisher/handoff/Schur algebra but not positivity. | I did not certify the determinant identity or the 1731-positive-coefficient chart because the frozen packet contains only author scripts and assertions, not the raw finite certificate or an independent exact run packet. |
| U2. Conditional-entropy strictness on the Lambda-zero family | INCOMPLETE | The reduction from complete entropy to conditional entropy is correct conditional on U1: the leaf marginal negative Hessian is constant in the fixed coordinates, so the radial derivative is the same M. | Absolute proof depends on U1, so it cannot be marked CORRECT from this packet alone. |
| U3. Explicit center-dependent nonzero-Lambda continuation band | INCOMPLETE | The perturbation proof, constants, derivative formula, and quantifiers are correct conditional on the Lambda-zero conditional Hessian being positive at the center. | Absolute proof depends on U2/U1. No uniform band is accepted or claimed. |
| U4. Fixed-diagonal radial obstruction witness around K*,D* | EXCLUDED FROM THIS REVIEW | Recorded only as excluded scope. | Not used as theorem evidence, not treated as an entropy counterexample, and not reviewed as an exact unit here. |
| U5. One-sided perspective identities and remaining inequality | CORRECT | The identities `-H(X3|X1,X2)=G1(K)+G1(I-K)`, the one-sided Hessian formula, the congruence scaling law, and the statement of the remaining inequality are correct as a bridge. | The coupled inequality `F1(D) >= 2 tr(N1 adj D)` remains INCOMPLETE and is not proved by the bridge. |

## Source Lines

U1 source lines:

- Main frozen statements and scope: `proof.md` lines 5-42.
- Complete events, legality, entropy Hessian, Lambda-zero grouping: `proof.md` lines 44-92.
- Fixed-direction derivative, score Gram, Schur elimination, determinant prefactor: `proof.md` lines 94-165.
- Rbar, t=u^4 reduction, leaf-exchange symmetry: `proof.md` lines 167-178.
- Determinant identity and P: `proof.md` lines 180-203.
- Positive chart certificate as author claim: `proof.md` lines 205-241.
- Seed, inertia continuation, and integration to entropy Hessian: `proof.md` lines 243-263.
- Static certificate algorithm: `certificate.py` lines 20-107.
- Static bridge identity checker: `bridge_checks.py` lines 17-53.
- Accepted-scope limits: `accepted_pr51.md` lines 24-30 and `archived_pr55.md` lines 7-13, 21-33.

U2 source lines:

- Conditional strictness statement and proof: `continuation.md` lines 7-18.
- Prior accepted leaf marginal subtraction: `accepted_pr51.md` line 28.

U3 source lines:

- Band statement and definitions: `continuation.md` lines 19-41.
- Eigenvalue lower bound, legality, derivative jets, constants, and integration: `continuation.md` lines 43-70.

Excluded U4 source lines:

- Radial obstruction text: `continuation.md` lines 72-158.
- Exact obstruction script: `continuation_exact.py` lines 1-107.

U5 source lines:

- One-sided perspective identity, Hessian formula, scaling bridge, and remaining inequality: `continuation.md` lines 160-205.
- Final remaining scope: `continuation.md` lines 207-211.

## Required Artifact Before Upgrading U1

To upgrade U1 without running arithmetic myself, I require a raw finite certificate packet bound to the same frozen input. The minimum useful packet is:

1. Complete `P.json`, `Q.json`, and `summary.json` emitted from the frozen `certificate.py --out ...`.
2. A run transcript or manifest binding those outputs to SHA256 `602DBD54E9DD17ECAC04E1347C3E44DAC7FE3DA0053A7AC3CC1D49755BEFDC66` for `certificate.py`.
3. A raw determinant-residual artifact, if available, showing the expanded residual term list is empty or all zero after clearing denominators.
4. The Python and SymPy versions, plus output file hashes.

Without that raw finite certificate or an independent exact arithmetic result supplied by the computation owner, the determinant identity and positive chart remain author-script assertions for this no-execution review.
