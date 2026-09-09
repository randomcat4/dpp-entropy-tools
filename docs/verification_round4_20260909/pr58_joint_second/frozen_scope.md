# PR58 joint-additive second review: frozen scope

Reviewer role: fresh independent SECOND mathematical reviewer for the PR58 joint-additive analytic addendum.

Work directory owned by this review:

`docs/verification_round4_20260909/pr58_joint_second`

## Bound input

I inspected the author-only frozen packet in:

`research/I05-23-middle-20260909`

and the adjacent `input_binding.json`.

The packet binds PR 58 to head:

`5ab3cae1c49da8334057596f46a4bd8fc449b98c`

with source prefix:

`research/I05-23-middle-20260909/`

The seven frozen source files are:

- `ADDENDUM_JOINT_ADDITIVE.md`
- `ADDENDUM_CONDITIONAL_CENTERING.md`
- `RESULT.md`
- `code/verify_joint_additive_failure.py`
- `code/verify_middle_compensation.py`
- `output/verify_joint_additive_failure.txt`
- `output/verify_middle_compensation.txt`

The local SHA-256 hashes I computed match the binding for all seven files. Details are recorded in `source_binding.json`.

## Read sources

Primary review sources:

- `input/ADDENDUM_JOINT_ADDITIVE.md`
- `input/ADDENDUM_CONDITIONAL_CENTERING.md`
- `input/RESULT.md`
- `input/code/verify_joint_additive_failure.py`
- `input/code/verify_middle_compensation.py`

Narrow accepted dependency:

- `docs/verification_round3_20260909/accepted_pr54.md`
- `research/I05-23-20260909/ADDENDUM_OUTER_WEDGE_FLOW_RATE.md`, only for the displayed outer-wedge identity and definitions already accepted in PR54 scope.

Narrow external primary check:

- Erbar and Maas, `arXiv:1111.2687`, only for the reversible finite Markov-kernel / nonlocal transport-geodesic setup cited in the limited comparison.

## Accepted scope

This review accepts, subject to the source-line qualifications in `review_report.md`:

- the two-margin Hilbert projection identity and Cauchy lower bound with factor `1/2`;
- the comparison showing the joint-additive residual gives a lower bound no weaker than either one-sided conditional-centering bound;
- the zero-mean gauge, normal equations, strict contraction, inverse equations, and residual value formula;
- the rank-at-most-four DPP reduction of the conditional expectation operator in the observed complete-event coordinates;
- the analytic dual lower-bound template for arbitrary interaction tables with zero row and column sums;
- the limited Erbar-Maas comparison as a non-import result;
- the explicit statement that the dense correlated general whole-chord target remains incomplete.

## Exclusions

I did not certify:

- the numerical signs or decimal inequalities printed in the author's witness output;
- the claimed strict failure at `s=9/10` as an independent numerical certificate;
- the original fixed-corridor `[3,15]` / `s=10` computation;
- formal verification;
- novelty or publication priority;
- any GitHub issue/PR state beyond the frozen local files and the narrow accepted PR54 local record.

I did not run the author scripts, SymPy, interval arithmetic, entropy computations, formal tools, or any remote computation. I only read files and performed SHA-256 hash checks.
