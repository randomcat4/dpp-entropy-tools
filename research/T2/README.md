# T2 finite-block entropy transfer tool

Status: VERIFIED for frozen v1 by fresh independent review; see [verdict](verdict.md) and [report](verifications/fresh_v1.md). No Lean verification is claimed. This package concerns finite full-subset Shannon entropy, with natural logarithms.

The [frozen theorem](frozen_theorem_v1.md) bounds the entropy cost of deleting off-block kernel entries. Its signed Jensen interval permits transferring either sign only when the corresponding explicit error is smaller than the seed gap. The [complete proof](proofs/construction_v1.md) includes all boundary limits and a connected finite-graph application. [Boundary families](boundaries/boundary_families.md) explain why dimension and block spectral margin cannot be omitted.

## Reproduce the exact helper

From the checkout root, with Python 3.10 or newer (standard library only):

```sh
python3 research/T2/artifacts/demo_checks.py
python3 research/T2/artifacts/block_transfer.py research/T2/artifacts/chain4_input.json
python3 research/T2/artifacts/boundary_examples.py
```

The first two entry points use real rational input, exact determinant arithmetic and proved finite-series logarithm enclosures. They accept a sufficient Gershgorin feasibility certificate and positive block buffer; rejection is inconclusive. The analytic theorem covers complex Hermitian kernels and arbitrary finite n, while this helper caps n at 256 and block size at 8. It uses strings for rational/decimal input and refuses binary floats. It returns an interval, not an estimate of the exact full entropy.

The logarithm enclosure uses log x=2 sum_{k>=0} z^(2k+1)/(2k+1), z=(x-1)/(x+1), after rational range reduction to [1,2]. After N terms, the omitted nonnegative tail is at most 2 z^(2N+1)/((2N+1)(1-z^2)). Values below one use negation of log(1/x). Entropy terms are p log(1/p), then interval addition/subtraction uses coefficient signs. Decimal output is rounded outward by integer division. No hardware floating-point logarithm enters these enclosures.

The connected path example uses 2-site seed blocks and coupling 3/100. The 64-coordinate case evaluates 384 block masses instead of the full 2^64 subset space. Its candidate-theorem-backed exact enclosure is [4.812262390708765909, 5.974762390708765910] nats, strictly positive. This is a positive Jensen-gap demonstration, not a concavity counterexample. The proof independently gives the weaker closed-form lower bound (73m+27)/1200 for every path length m, and covers nonperiodic bounded-degree graphs subject to its explicit inequalities.

The boundary script uses exact rational probability checks but floating-point entropy diagnostics; those diagnostics are not interval certificates. The two all-parameter boundary proofs remain separate mathematical artifacts.

## Coverage and limits

13 deterministic helper checks passed; two exact large-example evaluations completed (8 and 64 coordinates), with direct full-law crosschecks only at dimensions 2 and 4 (60 mass evaluations). Boundary contribution: ten preselected exact probability cases, five scaling diagnostics. Zero random search draws; no large scan; no GPU. The exact frozen theorem, stated boundaries and computational interface have now received independent review; see the report for its scope. See rounds.md and provenance.md for status updates.

No stationary entropy-rate conclusion, global concavity conclusion, Hessian control, realification theorem or novelty claim is made. The helper demonstrates a reusable consequence of standard entropy machinery.

The historical pre-proof [definition audit](audits/definition_contract.md) is a generic contract, not a list of additional theorem premises. Its derivative-specific positivity checklist does not restrict the selected value-bound theorem: the proof separately justifies its classical-to-spectral inequality and handles singular K.

Two reporting conventions from the independent audit: `full_system_subsets_enumerated` counts separate full-law enumeration calls, while `block_subsets_evaluated` counts actual block enumeration work. If the partition contains only the whole ground set, block enumeration is full-system enumeration; no saving is claimed in that case. The reported resource limit in demo_results.json was imposed by the original external launcher, not by demo_checks.py itself. For an equivalent Linux run, set OMP_NUM_THREADS=1, OPENBLAS_NUM_THREADS=1 and MKL_NUM_THREADS=1 and impose `ulimit -v 8388608` in that command shell before running the script. Plain reruns do not inherit the recorded cap automatically.
