# Scalar stationary high-contrast DPP: fixed-process bridge and continuation

Status: AUTHOR_PROOF / AUTHOR_FINITE_PASS / PENDING_INDEPENDENT_REVIEW. The universal high-contrast concavity problem and a genuine stationary entropy-rate counterexample are INCOMPLETE. Novelty is NOT ASSESSED.

This is an isolated scalar research packet based on main@237097124869b3bb04c139d4c4599e6bda7d344d. It neither modifies nor imports S4 PR145. No merge or change to accepted research is requested.

## Entry points

`RESULT.md` gives the latest result, execution denominator and limitations. `continuation_proofs.md` proves the new centered Fisher-density limit and the all-contrast sparse-density Jensen wedge. `fixed_process_bridge.md` contains the initial fixed-symbol value/conditional-entropy tail theorem.

Reproduce the fresh continuation, from this directory:

    python code/verify_continuation.py --verify certificate/continuation.json

This entrypoint needs only the Python standard library. All sign comparisons use directed integer/dyadic intervals. The optional numpy spectral-proposal path in `certify.py` is not called.

## Mathematical objects and limits

The object is f=a+c*1_E for ONE fixed measurable E. Every block length compresses the same infinite operator. The target is complete-configuration Shannon entropy per original integer coordinate, not spectral entropy. Quantum entropy is only an upper-bound tool in the value bridge.

The continuation establishes lim F_n((1-c)/2)/n=4/(1-c^2), with explicit finite-size and count-score error bounds. This is Fisher information, NOT entropy curvature. The acceleration term -sum p'' log p is retained and remains the central uniform-in-volume obstacle.

The continuum density theorem proves a specified true-rate Jensen chord for every measurable E in an explicit rho=O((1-c)/log(1/(1-c))) wedge. It does not prove every a-chord or differentiate the entropy-rate limit.

## Checkpoint and evidence boundary

Initial checkpoint d030833c47d0fde9c70007bd55eedd168620fc7d published only the analytic bridge and provenance. The preceding local 50-certificate/2,828-screen archive is identified in `prior_artifact_provenance.json`; its complete raw outputs are NOT imported and its numerical verdicts are NOT premises. A hash is provenance, not public reproduction of absent evidence.

This continuation imports two small arithmetic/complete-event source files and publishes a NEW checker with NEW literal evidence: 9 finite inputs, 2,304 complete atoms per run, 24 exact alternative determinant-jet comparisons, 8 density witnesses and 6 analytic crossover checks. Same-author replay is not independent review. Historical and fresh denominators are not merged.

The user-supplied c<=312/625 finite theorem and historical 26,274 cyclic evaluations remain frozen background, not independently re-proved or re-executed here.
