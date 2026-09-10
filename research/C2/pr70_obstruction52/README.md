# C2 independent finite reconstruction: PR70 fixed paired-resolvent witness

Status: **MACHINE_PASS for the fixed PR70 object**, run01, exit 0. All 178 ordered checks passed. Mathematical FIRST/SECOND acceptance is separate.

Frozen author source: PR70 at `f7be60759fd4d65184803b6585965dc7e5ccd624`. Scope is exactly the fixed K, D, tau in section 1 of `post_checkpoint.md`, and the complete-event/perspective definitions in sections 1–2 of `proof.md`. The independent executable does not import author code. Literal comparison targets are separate from computational inputs.

`inputs/REQUEST.md` is the controlling C3 execution contract. `inputs/object.json` supplies the sole object; `inputs/expected.json` supplies post-construction comparison literals. `inputs/author_SOURCE.json` binds the author source blobs. The independent implementation was publicly frozen at `29d4d77d7dba65de933d196a89b4db2616234991` before its first execution. `outputs/run01/` retains raw arithmetic, log certificates, comparisons and process evidence. `execution/RUN_LEDGER.json` binds the sole run and its closed budget.

One arithmetic process, one CPU thread, at most 16 GiB memory, no GPU, a single 600-second absolute deadline beginning before Python/package loading. Fixed N=80 rational atanh logarithms; no pilot, adaptive precision, timer reset, extension, new parameter, or post-mathematical-mismatch continuation. A mechanical repair, if needed, must retain its original failure and share the same still-live deadline. The first mathematical mismatch is terminal. The implementation and inputs will be published before execution.

This packet is independent computation evidence for isolated FIRST and SECOND reviewers. It is not either mathematical review. A negative paired-resolvent curvature is an auxiliary-method obstruction; a negative complete-entropy Jensen difference is locally concave behavior. Neither is an entropy-concavity counterexample or a proof of a universal sign. PR77, issue73, and issue74 remain outside execution scope.
