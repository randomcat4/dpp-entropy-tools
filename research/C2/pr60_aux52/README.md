# PR60 fixed radial obstruction and true curvature

MACHINE_PASS. The independently reconstructed eight-event certificate matches
PR60 source f869fd251c0d6fdad737b6d5efa287307795a87d.

[Status](STATUS.md), [machine notes](machine_notes.md),
[run ledger](execution/RUN_LEDGER.json), and the
[complete exact certificate](outputs/run01/certificate.json) give the result
and execution provenance. Per-layer checkpoints retain full event polynomials,
mixed jets, rational log intervals, Sylvester minors and comparison results.
The author reference checker was neither executed nor imported.

Run01 completed with exit0 in0.57009441 recorded checker seconds. The independent
source was frozen before launch; no repair or rerun was needed. The separate
600-second, one-process/CPU/thread,16GiB,noGPU window was not extended. Both
this arithmetic and the earlier full-r unit are stopped.

The fixed-diagonal radial derivative is strictly negative, while the actual
entropy curvature and complete Jensen gap have the concave sign. C2 supplies
machine evidence for C1's Claim4 FIRST and C3's later gate; this is not theorem
acceptance, an entropy counterexample, or a general Lambda-nonzero result.

See [frozen contract](frozen_contract.md) and
[source binding](inputs/SOURCE_BINDING.json). This unit does not include PR58,
whole-chord scans, novelty, or Lean formalization.