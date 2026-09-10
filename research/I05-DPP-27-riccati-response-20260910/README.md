# I05 / DPP27 — Riccati response successor, PR91

Date: 2026-09-10. Base: main@65e59a46b49cd2dbb5c779a4cfae8cef26441984. Parent issue 65; compute issue 74; predecessor PR79. Branch: research/I05-DPP-27-riccati-response-20260910. No main, PR77 or PR79 source is modified.

## PROVED (AUTHOR PROOF), PENDING_REVIEW

For exactly f_t=1/2+cos(4*pi*theta)/4+t*cos(2*pi*theta)/8, t in [1/2,3/2]:

- The complete-event correction-state operator is positive and normalized on the explicit convex domain ||Q||_2<=1/8. Each of its four weights is at least 81/1024. Branch contraction is 34/81; probability-law W1 contraction, INCLUDING changing weights, is 4363/5184.
- Its true infinite reachable attractor is homeomorphic to the four-symbol one-sided space, and its unique invariant law is non-atomic with full support. This is a fact about this representation, not a proof that every alternative finite HMM representation is impossible.
- The true rate per original coordinate is h=(1/2)eta B. The coding jets satisfy ||Q'||_2<=1/5, ||Q''||_2<=3/4 and explicit geometric-polynomial forgetting. Quantitative C1/C2 Poisson bounds justify the FULL invariant-measure second response, and a finite-complete-score argument identifies the full Fisher rate.
- For three arbitrary smooth Poisson trial functions, let e01,e02,e11,e20 bound respectively ||Dr0||,||D2r0||,||Dr1||,||r2|| on the ENTIRE state domain. Then

      |h''-c2/2| <= 13e01+e02/8+6e11/5+e20/2.

  This is an explicit true-curvature approximation theorem, including invariant-law response. It does not assume a finite discretization equals the DPP or require numerical differentiation of an approximate invariant measure.
- Exact stationary moments satisfy eta Q=eta det Q=0. The finite m-cell conditional entropy rate has value error at most (9/16)(34/81)^(2m). This value bound cannot be differentiated to infer a curvature bound.

## INCOMPLETE

The whole-interval inequality h''(t)<0 is not certified. Its remaining sufficient gate is a gap-free parameter cover with the four specified uniform residual bounds and a strictly negative c2/2 plus the error above. No sampled maximum, finite difference, author PASS or previously certified point fills that gap.

Three executed polynomial scouts at t=5/4, degrees6/8/10, give candidate c2/2 near -0.00333008. Their diagnostic residual budgets are explicitly NON-CERTIFYING. All trials and failures are retained. Novelty is UNASSESSED. Independent review is REQUESTED/PENDING_REVIEW, not presumed running.

## Evidence map

`proof.md`: complete-event representation, invariant domain, weighted law contraction, true-rate normalization, jets, smooth resolvent and second response.

`curvature_certificate.md`: explicit three-Poisson residual theorem, proof of all response errors, optional finite-state W1 defect, and correct differentiation conventions.

`coding_and_fisher.md`: disjoint branch images, non-atomic law, exact moments, quantitative C2 forgetting, full Fisher limit and separate value error.

`code/exact_checks.py`, `output/exact_output.json`: actual bounded Fraction reconstruction of 252 complete event values and both t-derivative layers against independent inclusion/Mobius enumeration; all four branches, exact normalization, state/jet bounds and rational constants. This is author computation, not an independent reviewer.

`code/poisson_scout.py`, `output/scout_summaries.json`: all three non-rigorous trial-generation runs. Complete coefficient records are preserved in the private connected-Drive raw-data fallback linked in `sources_and_attempts.md`; the chat also supplies the original raw-execution ZIP. Two corrupt archive text transcriptions were withdrawn and retained only as failures in Git history. No claim of successful public coefficient mirroring is made.

`sources_and_attempts.md`: primary-source comparison, PR79 upper-budget scope repair, actual run metadata, exact provenance boundaries, failures and raw-data location.

`compute_contract.md`: the issue74 original continuum job's three-Poisson alternative. REQUESTED to Codex/local agent in issue74 comment 5612135254, not a duplicate budget or a running-job claim. Explicit input, algorithm, 7200s/4CPU/16GiB cap, outward-error gate, stopping and authorized resumption conditions.

All probabilities are complete events, derivatives refer to the genuine affine K direction, and all four branches/Fisher/acceleration/invariant-law responses remain. The previous comment-only 4096-box computation and any unreviewed PR77 finite conclusion are not premises. Main's accepted limited theorems retain their original quantifiers.
