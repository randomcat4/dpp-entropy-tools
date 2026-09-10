# I05 / DPP27 — Riccati response successor

Date: 2026-09-10. Base: main@65e59a46b49cd2dbb5c779a4cfae8cef26441984. Parent issue 65; compute issue 74; predecessor PR79. Branch: research/I05-DPP-27-riccati-response-20260910.

## Status

PROVED (AUTHOR PROOF), PENDING_REVIEW: for exactly f_t=1/2+cos(4*pi*theta)/4+t*cos(2*pi*theta)/8, t in [1/2,3/2], the correction-state construction gives a positive four-branch normalized operator on the convex domain ||Q||_2<=1/8. All weights are at least 81/1024. Branch contraction is 34/81; full probability-law Wasserstein contraction, INCLUDING weight variation, is 4363/5184. The genuine infinite reachable attractor and unique invariant law give the true entropy rate per original coordinate with factor 1/2. Coding jets satisfy ||Q'||_2<=1/5 and ||Q''||_2<=3/4. Quantitative C1/C2 resolvent bounds justify the full second-order invariant-measure response.

The proof does not use the predecessor's unarchived 4096-box computation. It supplies an analytic replacement with exact rational constants. Uploads are checkpoints in this same author task; additional residual-certificate and executable evidence files follow as separate commits.

INCOMPLETE: h''<0 on the entire interval. A polynomial scout, a sampled residual, a single curvature point, or a conditional entropy value cannot certify this. Independent review and novelty are separate and not claimed.

## Source audit

Read main docs/research_status.md and docs/route_ledger.md, issue74's literal model/contract, PR77's original complete-event/Poisson proof, and PR79's current scope repair ae1149f2ed7d657afa494740c3abae83de549d3f and review comments. PR79's explicit B_R is an UPPER BUDGET for a curvature tail. Lower bounds on B_R do not imply lower bounds on the actual tail or a necessary minimum depth. That repair is retained.

Issue74 comment 5611794230 reports completion of the separate PR77 fixed-object C2 run with MACHINE_PASS, and explicitly excludes the continuum. This is read as computation evidence, not as a mathematical verdict or authorization to overlap jobs. The new author analysis does not depend on it.

## Files and conventions

proof.md is self-contained for the operator, law, jets and response. The continuation adds explicit approximation errors, exact small complete-event/jet checks, and polynomial trial generation. All probabilities are complete events, all derivatives are with respect to the genuine affine K parameter t, and all four branches are retained. A finite discretization is only an approximation, never a claimed exact finite HMM.

Independent review: PENDING_REVIEW / REQUESTED, not assumed running. Novelty: UNASSESSED. No coordinator notification is made for routine progress; collaboration stays on the PR/issue.
