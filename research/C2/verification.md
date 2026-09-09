# Verification status

At this snapshot the formula calibration and author computations have completed. The frozen candidate proof packet is under independent review; do not infer acceptance from this file until the actual review reports are included.

## Author checks

- Main exact 32-event inclusion-exclusion/polynomial identity, all jet sums, all layer curvature contributions, 80-digit finite differences, exact frame lower-bound certificate and cone constants: PASS on the compute server; main_check.exit is 0.
- Mechanism author: independent complementary-polynomial reconstruction, exact cardinality-weighted cancellation, noncommuting jet/difference fixture on the compute server: PASS.
- Search author: independent probability/jet preflight followed by the deterministic 24-record/22-distinct-center design, rational endpoint validity and interval negative-chord certification: PASS. Search definiteness outside these finite evaluations is not certified.

## Non-author work

The first fresh GPT-5.5 xhigh reviewer reconstructed all 32 event polynomials from inclusion-exclusion before seeing author code. Its independent fixture, rational event table, source and server output are in reviews/first. This checks the formula implementation and support, not the universal sign.

Frozen candidate packet for mathematical review: public-history commit 81b0123b7c1bcb4495e99d5707bf2388314f3bbf, main proof blob 0a8cf09210aeddbc03f355143f638069ccfbbe1e and supplemental proof blob 70935232da868f66f70338123ad1907d391c2275. Proof-review outcomes will be recorded separately. No independent reviewer helped author these proof files.

Formal proof status: NOT FORMALIZED. The unrelated source project pins Lean 4.32.0; local Lean 4.32.0 and Lake 5.0.0 run, while the compute host exposes no lean command. This is a version probe only. No C2 theorem is claimed Lean-checked. The rational matrix certificate and interval arithmetic have their stated computational trust boundaries.
