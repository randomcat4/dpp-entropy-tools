# PR91 C1 FIRST code/evidence review

Scoped verdict: `SOURCE_ONLY / PENDING_C2` for all author scripts and outputs. I performed static reading only; I did not run, import, compile, or reconstruct any checker, scout, finite enumeration, interval arithmetic, entropy calculation, or formal verification.

## Files reviewed

| Public alias | Lines | Evidence role |
|---|---:|---|
| `source-snapshots/pr91/research/I05-DPP-27-riccati-response-20260910/code/exact_checks.py` | 187 | Author exact Fraction checker for finite complete events, derivatives, branch/state bounds, and constants. |
| `source-snapshots/pr91/research/I05-DPP-27-riccati-response-20260910/code/check_tightening.py` | 47 | Author exact Fraction checker for post-handoff tightened constants. |
| `source-snapshots/pr91/research/I05-DPP-27-riccati-response-20260910/code/poisson_scout.py` | 142 | Author floating polynomial scout; explicitly non-certifying. |
| `source-snapshots/pr91/research/I05-DPP-27-riccati-response-20260910/output/exact_output.json` | 45 | Author output from exact checks; not independent evidence. |
| `source-snapshots/pr91/research/I05-DPP-27-riccati-response-20260910/output/tightening_output.json` | 28 | Author output from tightened constant checks; not independent evidence. |
| `source-snapshots/pr91/research/I05-DPP-27-riccati-response-20260910/output/scout_summaries.json` | 56 | Author scout summaries; explicitly invalid as certificates. |

## Static findings

`exact_checks.py` is a standard-library author checker. It defines exact value/first/second derivative jets with `fractions.Fraction` in lines 13-40, signed determinant and Mobius event construction in lines 66-92, the Riccati branch step in lines 58-64, and the bounded finite checks in lines 94-175. It checks exact constants, normalization, weighted state/determinant identities, finite complete-event probabilities, and both derivative layers at three parameter values and event lengths 2, 4, and 6. The committed output in `output/exact_output.json` lines 1-45 records status `AUTHOR_MACHINE_CHECK_PASS_NOT_INDEPENDENT_REVIEW`, 252 event matches, 252 branch checks, and explicit “not certified” fields.

`check_tightening.py` is a short exact Fraction checker for the post-handoff refinements. Lines 7-32 contain the tightened constant comparisons; lines 33-44 construct the JSON record; lines 45-47 write and print it. The committed `output/tightening_output.json` lines 1-28 records `AUTHOR_EXACT_CONSTANTS_PASS_NOT_INDEPENDENT_REVIEW` and `curvature_sign_certified: false`. One provenance caveat: the script as published writes `tightening_output.json` next to the script file at line 46, while the frozen packet stores the committed output under `output/tightening_output.json`. That does not affect the analytic proof, but it means the committed output path should be treated as a curated/moved author artifact unless an executor independently reproduces the exact file placement.

`poisson_scout.py` is correctly labeled as non-rigorous. Lines 1-4 say no sampled residual is a supremum certificate and no `h''` sign is asserted. Lines 98-140 perform floating least squares and finite-difference diagnostics at `t=5/4`; lines 123-135 report sampled residuals and explicitly include missing outward arithmetic, continuum residual suprema, and parameter-interval coverage. `output/scout_summaries.json` lines 1-56 preserves all degree 6/8/10 summaries and marks `invalid_as_certificate_sampled_budget`, so these scout values cannot certify any curvature sign.

The scripts rely heavily on `assert` for validation: `exact_checks.py` uses assertions throughout lines 94-175, and `check_tightening.py` uses them in lines 10-32. Any future independent execution should run with assertions enabled. This is a reproducibility note, not a mathematical acceptance.

The private raw coefficient archive mentioned in `sources_and_attempts.md` line 38 is not part of the public frozen evidence needed for the analytic theorems. I did not download it, link it, or rely on it.

## Evidence classification

- Analytic derivations in `proof.md`, `coding_and_fisher.md`, `curvature_certificate.md`, and `post_handoff_cancellation.md`: reviewed in `review_report.md` and accepted only as scoped analytic implications with their constant gates propagated.
- Exact Fraction outputs and rational comparisons: `SOURCE_ONLY / PENDING_C2`.
- Finite 252-event matching claims: `SOURCE_ONLY / PENDING_C2`.
- Scout samples, candidate polynomial coefficients, sampled finite differences, and diagnostic budgets: `SOURCE_ONLY / NON_CERTIFYING`.
- Compute contract resource limits and 7200-second request: author request only; no execution authorization or new C2 budget follows from this FIRST.

No code/evidence item in this packet closes the whole-interval continuum gate.
