# Status

2026-09-09 10:24 UTC: RUNNING; directed-flow candidate frozen for fresh review.

- Sources downloaded at the two frozen commits in README.md.
- Three independent bounded computational units assigned: PR41 symbolic/event checks, PR43 full-event fixtures, PR43 directed-flow LP.
- Resource preflight passed. Reused environment: Python 3.12.3, SymPy 1.14.0, NumPy 2.5.3, SciPy 1.18.1. Initial arithmetic allocation is one thread per unit.
- PR43 D produced a rational feasible-flow candidate: 33 nonzero directed flows out of 56, all 40 equations checked with exact residual zero. The candidate is frozen at local review commit `f249f897c212e49e66ec62a34fba715c47b9bce5`; its files are in `pr43_flow/`. Status is `CANDIDATE_EXACT_SELF_CHECKED` until the fresh nonauthor review finishes.
- The flow author's final exact verifier job exited 0 (PID 171148). Its initial discovery succeeded; a redundant metadata-recapture discovery attempt aborted under a memory wrapper and is retained in the failure record. No flow-author job remains live. No additional input was tried.
- A new nonauthor reviewer uses the freed slot to rebuild the law and generator independently from the frozen rational candidate. It does not rerun the LP discovery.
- PR41 and PR43 event units remain active; no full theorem is certified by this packet.
- C1's proof review and author clarification of dependent task E/F contracts are separate.

This file will be updated with exact run outcomes, nonauthor review and remaining obligations. No prior single-box work is resumed.
