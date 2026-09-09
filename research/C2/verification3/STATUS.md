# Status

2026-09-09 10:30 UTC: initial computations complete; directed-flow candidate remains in fresh review.

- Sources downloaded at the two frozen commits in README.md.
- Three independent bounded computational units assigned: PR41 symbolic/event checks, PR43 full-event fixtures, PR43 directed-flow LP.
- Resource preflight passed. Reused environment: Python 3.12.3, SymPy 1.14.0, NumPy 2.5.3, SciPy 1.18.1. Initial arithmetic allocation is one thread per unit.
- PR43 D produced a rational feasible-flow candidate: 33 nonzero directed flows out of 56, all 40 equations checked with exact residual zero. The candidate is frozen at local review commit `f249f897c212e49e66ec62a34fba715c47b9bce5`; its files are in `pr43_flow/`. Status is `CANDIDATE_EXACT_SELF_CHECKED` until the fresh nonauthor review finishes.
- The flow author's final exact verifier job exited 0 (PID 171148). Its initial discovery succeeded; a redundant metadata-recapture discovery attempt aborted under a memory wrapper and is retained in the failure record. No flow-author job remains live. No additional input was tried.
- A new nonauthor reviewer uses the freed slot to rebuild the law and generator independently from the frozen rational candidate. It does not rerun the LP discovery.
- PR41 independent symbolic unit passed: complete eight-event probabilities and six-direction affine jets, full Fisher/acceleration decomposition, strong-family block/minor identities, block-decoupling cancellations and missing-edge coordinate reduction. Final runner PID 171670 / Python PID 171674 exited 0 in 23.59 seconds. An earlier slow symbolic simplification was interrupted after seven preserved objects; the optimized final run completed. See `pr41/REPORT.md` and `pr41/evidence.json`. This is computational evidence for C1's analytic review, not acceptance of general three-dimensional concavity.
- PR43 B/C passed: both nested author verifiers exited 0, and independent Mobius reconstruction certified all 256 events plus all 8 x 32 conditional events at each of t = 1/5, 1/2, 1. Exact strict legality, diagonal refresh, the two-mode occupation obstruction (91/400 versus 99/400), and the reversible obstruction (-125/78) passed. Final wrapper PID 172003 / Python PID 172008 exited 0. A first launch failed on JSON serialization after the three per-t objects had completed; that failure and checkpoints are retained. See `pr43_events/output/REPORT.md` and its certificate files.
- All three initial author/computation units have finished; only the fresh flow-certificate review remains active. No full theorem is certified by this packet.
- C1's proof review and author clarification of dependent task E/F contracts are separate.

This file will be updated with exact run outcomes, nonauthor review and remaining obligations. No prior single-box work is resumed.
