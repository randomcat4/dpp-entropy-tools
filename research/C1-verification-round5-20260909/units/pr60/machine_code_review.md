# PR60 machine code/evidence addendum

Reviewer: C1 fresh non-author first reviewer for PR60, machine-evidence follow-up.

Verdict: `CORRECT / ACCEPTED_SCOPED` for the C2 PR64 machine implementation and retained raw evidence as a source-audited finite certificate for PR60 Claims 1-3. This is not a C1 rerun and not a formal verification. I did not run the checker, PR60 scripts, SymPy, entropy jobs, coefficient diagnostics, or reconstruction code.

## Files and binding

The reviewed machine packet is `source-snapshots/pr64_machine`, frozen at C2 PR64 head `5b40617fe7172aa266614aa28688d310218cb387`. I read the root status and handoff documents, implementation README, full implementation script, input bindings, PR60 copied inputs, the accepted-main structure input, run guard, execution ledger, run01 failure outputs, and run02 raw determinant/P/Q/layer/seed/provenance outputs. I locally checked all 52 local packet files against their recorded Git blob hashes in `source-snapshots/pr64_machine/SOURCE_BINDING.json`; there were zero mismatches.

The packet states the successful `MACHINE_PASS` for PR60 head/base and summarizes the full independent determinant/chart coverage (`source-snapshots/pr64_machine/README.md:3-14`, `source-snapshots/pr64_machine/STATUS.md:3-16`). The packet also states its role as machine evidence only, leaving C1/C3 to judge mathematical integration (`source-snapshots/pr64_machine/README.md:39-42`, `source-snapshots/pr64_machine/FINAL_HANDOFF.md:7-9`).

The parent-provided source-to-packet comparison shows that the repaired executable commit to the frozen PR64 head changed only new run02 outputs plus final status/handoff/ledger/machine-note documents, not implementation formulas, inputs, mathematical expressions, or guard code ([public PR64 comparison](https://github.com/randomcat4/dpp-entropy-tools/compare/ee33372042d27911a97a14aefc6cb068404d190b...5b40617fe7172aa266614aa28688d310218cb387)). That supports treating the frozen packet outputs as produced by the repaired implementation reviewed here.

## Static implementation consistency

The implementation is structured as an independent checker rather than as an author-script wrapper. Its module header says it constructs `Rstar` and `Rbar`, extracts `P` from `Ahat`, compares author static component strings only afterward, and deliberately does not import or execute the PR60 author checkers (`source-snapshots/pr64_machine/implementation/pr60_independent_certificate.py:1-8`). The provenance note agrees: PR60 files are frozen inputs, author component strings are comparison data, and the fresh implementation starts from displayed formulas (`source-snapshots/pr64_machine/provenance.md:3-14`). The run metadata records the construction guard and the successful source commit/status (`source-snapshots/pr64_machine/outputs/run02/run_metadata.json:11-13`, `source-snapshots/pr64_machine/outputs/run02/run_metadata.json:78-82`).

The formula pipeline matches the PR60 proof route at the level C2 was assigned to check:

- `build_rstar_u` and `build_rbar_t` construct the long and short Schur matrices from common rational scalars (`source-snapshots/pr64_machine/implementation/pr60_independent_certificate.py:357-400`).
- `verify_bernoulli_gram` uses the six physical direction variables `alpha,beta,gamma,eta,xi,omega`, the four Bernoulli leaves, the Gram entries, and a reflection identity (`source-snapshots/pr64_machine/implementation/pr60_independent_certificate.py:402-445`).
- `build_ahat` applies the stated denominator/sign-clearing scale to each short-matrix entry and requires each entry to be a polynomial over QQ (`source-snapshots/pr64_machine/implementation/pr60_independent_certificate.py:448-463`).
- `extract_p_from_determinant` computes the determinant by exact fraction-free Bareiss and by an independent 24-product determinant, divides exactly by `8*T*J^3*L^3*C^3`, checks P integrality, term count, degree vector, and zero remainder (`source-snapshots/pr64_machine/implementation/pr60_independent_certificate.py:531-572`).
- `load_author_components` parses only stored expression strings and assembles the author's component form after fresh P has already been computed (`source-snapshots/pr64_machine/implementation/pr60_independent_certificate.py:575-628`, `source-snapshots/pr64_machine/implementation/pr60_independent_certificate.py:854-878`).
- `verify_p_symmetries`, `transform_p_to_q_by_loops`, and `verify_q_homogeneous_polynomial` cover the sign-flip/leaf-swap and the two independent Q transformations (`source-snapshots/pr64_machine/implementation/pr60_independent_certificate.py:631-721`).
- `verify_q_box` explicitly iterates all 1925 positions, rejects negatives, and checks the expected 1731 positive, 194 zero, minimum 192, constant 432, group counts, and group minima (`source-snapshots/pr64_machine/implementation/pr60_independent_certificate.py:724-767`).
- `verify_seed_and_leafswap` and `verify_det_scaling_summary` check the positive seed, full matrix leaf-swap congruence, and determinant scaling back to `Rstar` (`source-snapshots/pr64_machine/implementation/pr60_independent_certificate.py:770-810`).

The run function enforces the intended order. It writes `determinant_and_P.json` immediately after the fresh determinant quotient and before loading author components; only after that does it compare the fresh P with author component strings. It then writes the Q box and seed/scaling artifact (`source-snapshots/pr64_machine/implementation/pr60_independent_certificate.py:813-916`). This order is the key reason I distinguish the author literals as comparison inputs, not as derivation sources.

## Raw run evidence

Run02 completed with PASS under the recorded run metadata (`source-snapshots/pr64_machine/outputs/run02/PASS.json:1-5`, `source-snapshots/pr64_machine/outputs/run02/run_metadata.json:19-21`, `source-snapshots/pr64_machine/outputs/run02/run_metadata.json:80-82`). The layer record shows all eight steps passing: input presence, score bridge, `Rstar/Rbar`, `Ahat`, determinant/P, author comparison, Q, and seed/scaling (`source-snapshots/pr64_machine/outputs/run02/layer_results.json:14-16`, `source-snapshots/pr64_machine/outputs/run02/layer_results.json:43-55`, `source-snapshots/pr64_machine/outputs/run02/layer_results.json:304-306`, `source-snapshots/pr64_machine/outputs/run02/layer_results.json:404-418`, `source-snapshots/pr64_machine/outputs/run02/layer_results.json:527-546`).

The determinant/P artifact stores the fresh P coefficients, P summary, determinant summary, divisor summary, empty division remainder, and `remainder_zero: true` (`source-snapshots/pr64_machine/outputs/run02/determinant_and_P.json:2-2551`). The Q artifact stores the complete 1925-position coefficient box and the summary values needed for the positivity certificate (`source-snapshots/pr64_machine/outputs/run02/Q_full_box.json:2-17442`). The seed/scaling artifact stores the leaf-swap congruence PASS, scaling PASS, determinant formulas, and four positive seed leading minors (`source-snapshots/pr64_machine/outputs/run02/seed_leafswap_scaling.json:1-12`).

## Run01 failure and repair

Run01 is correctly preserved as a failed attempt. The failure was a Python list-indexing error in the determinant cross-check, not a determinant residual or sign mismatch (`source-snapshots/pr64_machine/outputs/run01/FAILURE.json:3-5`). The run01 layer record shows determinant extraction failed before any P/Q acceptance (`source-snapshots/pr64_machine/outputs/run01/layer_results.json:304-313`). Earlier layers had passed, but they are not used here as acceptance evidence for the full certificate (`source-snapshots/pr64_machine/outputs/run01/layer_results.json:14-16`, `source-snapshots/pr64_machine/outputs/run01/layer_results.json:43-55`).

The repair is static and bounded: the fixed determinant cross-check indexes `mat[row][col]` (`source-snapshots/pr64_machine/implementation/pr60_independent_certificate.py:531-540`). The ledger records that the repair was a single-line indexing change, no PR60 inputs changed, the deadline was not reset or expanded, and run02 then passed all layers (`source-snapshots/pr64_machine/execution/LEDGER.md:35-68`). I found no code-review issue requiring an author fix.

## Limits

This code/evidence audit accepts the C2 machine packet only for the finite algebraic certificate behind PR60 Claims 1-3. It does not check Claim 4's radial obstruction, PR58/PR59, novelty, Lean/formal proof, or any broader entropy-rate theorem. The C2 handoff itself states that the Lambda-nonzero band and radial obstruction in the PR60 continuation are outside this machine unit (`source-snapshots/pr64_machine/FINAL_HANDOFF.md:63-67`).
