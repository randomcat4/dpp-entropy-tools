# I05-22 R4 final author packet

Research PR: [70](https://github.com/randomcat4/dpp-entropy-tools/pull/70). New bounded calculation request: [issue73](https://github.com/randomcat4/dpp-entropy-tools/issues/73), linked to earlier #20/#52. New branch starts from main `9dcb6e9079ca57f94e0e30d63161cda89ca61fae`; no main or another author's files were changed.

## Verdict and scope

**INCOMPLETE:** whether G1''>=0 for all strict connected missing-edge centers, the entire general-Lambda missing-edge Shannon Hessian sign, and general real three-point concavity. No positive full-entropy Jensen counterexample is supplied. The absence of a negative G1 point in bounded exploration is not a theorem.

**PROVED (author complete proofs; NOT independently reviewed):** the full-event one-sided identities and scaling law; positive four-dimensional side/paired pivots; exact parallel-sum compensation with marginal Fisher; the equivalent 2x2 full-arrow core and its symmetries; strict six-direction quadratic-perspective convexity; a quantified one-sided large-q tail; and the thinning equivalence/conditional-versus-full-entropy separation theorem. These are scoped identities, auxiliary results and reductions, not a hidden proof of the general Shannon claim.

**DISPROVED (author exact certificate; NOT independently reviewed):** universal convexity of the COMPLEMENT-PAIRED conditional resolvent. At the exact rational object in post_checkpoint.md its Hessian is less than -4.8046, but both G1'' and G0'' are positive and the actual legal full-entropy Jensen gap is negative. This refutes neither G1''>=0 nor entropy concavity.

Novelty and publication priority are unassessed. No proof-assistant formalization or CI success is claimed.

## Review entrypoints

`proof.md` contains the complete events, all six physical directions, the perspective calculation, both positive blocks, parallel-sum compensation, the 2x2 core, and exact Fisher inverse formulas. In particular the full target is det E_H>=0 with BOTH sides and the marginal Fisher. Positivity of the pivot alone does not close it.

`post_checkpoint.md` gives the exact new resolvent obstruction, all event jets, exact legality, logarithm error bounds and negative genuine Jensen gap. It also proves the complement/leaf-swap fundamental domain. The absent-side N0 decomposition's face0 typo was corrected to face1 after the first checkpoint; the correction is explicitly retained, not hidden.

`tail_bound.md` gives an explicit all-six-direction tail for fixed auxiliary shape. Its threshold may exceed the complete legal q interval for strong shapes, so it is not marketed as full-arrow coverage.

`thinning_bridge.md` proves that the GLOBAL one-sided claim and GLOBAL conditional-entropy concavity are equivalent, without proving either. It also shows, with an explicit third-order error bound, why a hypothetical negative side cannot be promoted to a full-entropy counterexample: at sufficiently thinned corresponding directions the positive leaf marginal Fisher survives. No negative-side example is asserted.

`verification.md` records the actual computations, failed routes, review updates, source roles and publication limits. `inputs.json` reproduces issue73's 273 fixed future inputs; those filaments have NOT been run by this author.

## Reproduction and the one blocked code upload

The public repository contains `verify_bridges.py`. Run it with ordinary Python 3.11+ and SymPy 1.14.0, NOT `python -O`, which would disable its assert gates:

    python verify_bridges.py --out outputs

The delivered local packet additionally contains the actually executed `certify_obstruction.py`, `post_checks.py`, their exact outputs, and bounded exploratory source. Run, from that packet:

    python certify_obstruction.py --out outputs
    python post_checks.py --out outputs

The first of those two code-file creations was blocked by the GitHub tool's safety-state check. That file was not retried via another GitHub endpoint. The existing Drive upload fallback was actually used successfully and metadata read back; sharing permissions were not changed. The new short post-check script is included in the delivered package rather than represented as a public GitHub file. Do not assume a private Drive object is publicly accessible. The public proofs contain the full literal rational input, derivative rules, event table and error formula needed for an independent reconstruction without either script.

Expected and actually observed final lines are, respectively:

    ALL NEW EXACT BRIDGE CHECKS PASSED
    ALL EXACT PAIRED-OBSTRUCTION CHECKS PASSED
    ALL POST-HANDOFF ALGEBRA CHECKS PASSED

The first and third are exact symbolic algebra; the second uses rational arithmetic plus proved rational logarithm tails and outward decimal rounding. All are author checks, not independent reviews.

## Prior-review update; no inherited acceptance

At task start PR60's comments supplied no requested source correction. Later C1's full mathematical FIRST and static code reports at `a48817033149b82f69519dc3c1800fe4841b8f97` were read in full. They report no source analytic defect; the one-sided identities pass at their scoped source-review level. The main Lambda-zero claims still had the separate C2 evidence gate in that frozen report, and the old radial obstruction required its own exact gate. C2 subsequently announced a MACHINE_PASS at PR64, not a mathematical adjudication. This packet does not infer that PR60's full theorem is accepted and does not use it as a premise. No 1731-term or old r=0 author replay occurred.

All new PR70 results remain separately unreviewed. The local author face-index correction is not an independent audit. Later changes are outside any earlier freeze unless a reviewer explicitly adopts them.

## Remaining work

The exact full-domain obligation and negative-vector back-map are in proof.md (16)-(17) and post_checkpoint.md (P12). Issue73 freezes an independent derivation, a 273-point structured falsification path and optional bounded fixed-filament interval work under one shared 2700-second budget. It is a request, not a claim of an active job or a global certificate. After sending it, this author continued and proved the tail and thinning results. No waiting, repeated large expansion or discarded event was used to close the gap.
