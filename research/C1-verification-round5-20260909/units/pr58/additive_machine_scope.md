# PR58 / PR76 additive finite-evidence review scope

This is a bounded first-reviewer source/evidence audit of the PR76 machine packet for the PR58 joint-additive finite witness. It reviews PR76 head `a7979c33b6e82431b6ddf1d39ac69e254d7b655a`, executed source `bbc9bc19b915ebad0ea8e8bea00580d4eebc5246`, publication base `28c24dee643f8a2049c143f79d4d63798907d2f1`, and frozen author numeric source `a4f05cc962985015b71635bf633acce9dfe76866`.

Public references:

- PR76: https://github.com/randomcat4/dpp-entropy-tools/pull/76
- Publication-base comparison: https://github.com/randomcat4/dpp-entropy-tools/compare/28c24dee643f8a2049c143f79d4d63798907d2f1...a7979c33b6e82431b6ddf1d39ac69e254d7b655a
- Executed-source-to-packet comparison: https://github.com/randomcat4/dpp-entropy-tools/compare/bbc9bc19b915ebad0ea8e8bea00580d4eebc5246...a7979c33b6e82431b6ddf1d39ac69e254d7b655a

Read evidence, using the public-ready alias `source-snapshots/pr76_additive/`:

- `SOURCE_BINDING.json`, `README.md`, `STATUS.md`, `frozen_contract.md`, and `machine_notes.md`.
- `execution/RUN_LEDGER.json`, `execution/run_guard.sh`, and `execution/CONTRACT_CORRECTION.md`.
- `inputs/REQUEST.md`, `inputs/REQUEST_CORRECTION.md`, `inputs/SOURCE_BINDING.json`, `inputs/ADDENDUM_JOINT_ADDITIVE.md`, `inputs/author_checker_reference.py`, and `inputs/author_output_reference.txt`.
- `implementation/independent_pr58_additive52_checker.py`.
- All retained `outputs/run01/` artifacts, including `00_metadata.json` through `08_comparisons_N80.json`, `final.json`, `exit.json`, logs, and marker files. The two large scalar/comparison JSON files were inspected structurally and through selected status/decimal leaves only.

This review did not run arithmetic, SymPy, author scripts, independent scripts, tests, formal checks, finite diagnostics, or new reconstruction. The author checker and author output were treated as source/comparison targets only. Stored author output is not promoted to independent verification.

This review is limited to the PR58 joint-additive finite evidence and source text affected by PR76. It does not reopen the PR72 corridor closure, PR60, PR69, whole-chord computation, general theorem proof, Lean/formal coverage, novelty, or later PR76 repairs.

The post-launch W/V correction is part of the reviewed packet. It is treated as a request-notation correction, not as an author defect: author `W=E_mu[b psi]`, while run01 fields labelled `W` denote `V=E_mu[y psi]=s^2 W_author`.
