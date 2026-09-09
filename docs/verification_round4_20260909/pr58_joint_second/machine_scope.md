# PR58 finite-witness machine SECOND: frozen scope

Reviewer role: bounded independent finite SECOND over the supplied C2 computation-owner packet for the PR58 joint-additive section-3 witness.

Owned outputs for this follow-up:

- `machine_scope.md`
- `machine_review_report.md`
- `machine_source_binding.json`

Earlier reports in this directory are preserved and not revised.

## Bound machine packet

Machine packet root:

`research/C2/pr58_additive52`

Adjacent binding:

`machine_input_binding.json`

The binding records:

- PR: `76`
- PR76 head: `a7979c33b6e82431b6ddf1d39ac69e254d7b655a`
- executable head: `bbc9bc19b915ebad0ea8e8bea00580d4eebc5246`
- author numerical head: `a4f05cc962985015b71635bf633acce9dfe76866`
- source prefix: `research/C2/pr58_additive52/`

I recomputed SHA-256 hashes for all 28 packet files and all matched `machine_input_binding.json`.

## Bound author repairs

Previously reviewed table-order patch:

- parent: `5ab3cae1c49da8334057596f46a4bd8fc449b98c`
- head: `ce9ade6d57469f0a4a67365604c66eb4cc290fc5`
- patch SHA-256: `2dbdee1f7d1b0c395849027acf1a503a26580516da05439c85a06f599257bdaf`

New joint-bounds patch:

- parent: `ce9ade6d57469f0a4a67365604c66eb4cc290fc5`
- head: `89aa874c24dd5a3ea98f8474826392560b1d0397`
- changed path: `research/I05-23-middle-20260909/ADDENDUM_JOINT_ADDITIVE.md`
- patch SHA-256: `37fa9e025008591a0e8e4d99a464e2f100339a6214d33a43c0f49ff6a6eb8c68`
- changed files: `1`
- code/output/fixture changed: `false`

## Sources inspected

Allowed raw machine sources inspected:

- `machine_input/implementation/independent_pr58_additive52_checker.py`
- `machine_input/inputs/REQUEST.md`
- `machine_input/inputs/REQUEST_CORRECTION.md`
- `machine_input/inputs/SOURCE_BINDING.json`
- `machine_input/inputs/ADDENDUM_JOINT_ADDITIVE.md`
- `machine_input/inputs/author_checker_reference.py`
- `machine_input/inputs/author_output_reference.txt`
- `machine_input/execution/CONTRACT_CORRECTION.md`
- `machine_input/execution/RUN_LEDGER.json`
- `machine_input/execution/run_guard.sh`
- `machine_input/outputs/run01/*.json`
- `machine_input/outputs/run01/*.log`
- `machine_input/outputs/run01/*_utc.txt`
- `machine_input/outputs/run01/*_pid.txt`
- `joint_bounds_patch.diff`
- `joint_bounds_delta_binding.json`
- `table_order_patch.diff`

I did not inspect FIRST or reviewer conclusions, top README files, machine notes, C1 material, other reviewer material, PR76 remote pages, or `[excluded private directory]`.

## Execution scope

I did not run the checker, author scripts, SymPy, interval arithmetic, entropy computation, formal tools, remote computation, or any GitHub mutation. I used only static file reads, JSON inspection, and SHA-256 hash checks.

Large fraction JSON files were inspected by structure and selected scalar leaves; megabyte rational numerator/denominator strings were not used as quoted evidence.

## Certification boundary

This review concerns the finite witness machine packet and repaired section-3 numerical text only. It does not certify:

- the general dense correlated whole legal chord;
- any entropy-concavity counterexample;
- novelty or publication priority;
- formal proof;
- the original `[3,15]` / `s=10` corridor computation.
