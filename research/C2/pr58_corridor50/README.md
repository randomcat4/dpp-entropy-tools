# PR58 original64-event corridor and s10 signs

MACHINE_PASS for the original four-file PR58 package frozen at
1770ed29e8487b8f39aebb4c9466406c7493e580.

[Status](STATUS.md), [machine notes](machine_notes.md), and the
[run ledger](execution/RUN_LEDGER.json) record the scope and provenance.
The complete [64events](outputs/run01/events.json),
[polynomial identities](outputs/run01/identities.json),
[four-piece corridor](outputs/run01/corridor.json),
[s10 exact log certificate](outputs/run01/s10.json), and
[27rational comparisons](outputs/run01/reference_compare.json) retain the evidence.

The source constructs complete6x6eventpolynomials directly before any posthoc
Schur cross-check or author-output comparison. It never reads/imports/executes
the author checker. All rational endpoints are stored as numerator/denominator
strings; the s10 artifact also retains every finite atanh term and its rigorous
one-sided tail.

One run completed with exit0,16:09:13–16:09:18UTC, before its unchanged
16:54:13UTC deadline; no repair, rerun or overlapping C2 arithmetic occurred.
The2700second, one-process/CPU/thread,16GiB,noGPU bound was not extended.

The original rounded decimal endpoint display is not an exact enclosure.
The independent rational W sign, true curvature bound and both width targets
pass. C1/C3 analytical review and integration remain separate from this
machine packet. The new joint-additive s9/10 witness is a different unit;
no whole-chord, entropy counterexample, novelty or Lean claim is made here.

See [frozen contract](frozen_contract.md) and [input binding](inputs/SOURCE_BINDING.json).