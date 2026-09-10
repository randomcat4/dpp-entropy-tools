# Static code review of `verify_bridges.py`

Scope: static read only. The script was not executed.

Verdict: CORRECT as a source-level bridge checker for the identities it encodes. Its successful execution is not independently certified here.

## Findings

No blocking static code defect was found in the checked identity coverage.

The `atoms(K)` routine at lines 8-15 implements inclusion-exclusion from inclusion minors. Lines 40-52 cover the complete eight-event conditional jets and leaf marginal accelerations at the missing-edge center. Lines 53-62 encode the one-sided cofactor formula and the cancellation of the `P''` term for the additive `t_ij` table. Lines 63-69 encode the simultaneous kernel/direction scaling law for selected masses and marginals.

Lines 70-84 verify the generic `L/C/R` coefficient transport for a symmetric arrow `N`, using the displayed relation for `J`. This is a coefficient-collection check, not a replacement for the positivity proof of the pivots. Lines 85-94 verify the six-direction quadratic-perspective sum of squares. Lines 95-107 check the complete four-evaluation Gram identities behind the Fisher inverse formulas. Lines 108-113 give only a noncommuting fixture for the parallel-sum transport; the universal identity still rests on the algebraic proof in `proof.md`.

## Limits

The script uses `assert`; running it under optimized Python would not be a valid check. This review did not run it, did not inspect any generated outputs, and did not use it as independent arithmetic evidence for the fixed rational signs in `post_checkpoint.md`.

