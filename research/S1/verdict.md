# S1 final bounded-round verdict

Status: STOPPED_SUBSTANTIVE. Lyons–Steif Conjecture 9.2 remains INCOMPLETE.

Two fixed rational scalar trigonometric pairs are rigorously excluded as counterexamples:

- **B0:** true rate gap lies in the rational interval summarized by [-2.620484904e-5,-2.605148085e-5] nats. The [frozen proof](main/rate_certificate_proof.md) and exact/interval implementation passed [rate audit](rate/author_certificate_audit.md) and [independent definition/recomputation audit](review/review_report.md). The latter rebuilt all event determinants and the boundary residual without importing the author's implementation.
- **P0:** the first phase task's actual fixed two-relative-phase candidate has true rate gap in the rational interval summarized by [-5.826508825e-6,-4.724191221e-6] nats. Its [variational residual refinement and application](main/variational_boundary_proof.md) passed [non-author audit](rate/phase_variational_audit.md). This is one review of the refinement, not a claim of two fresh P0 reviewers.

The decimal summaries are approximate; exact outward endpoints are in [B0 output](main/rational_rate_n8.json) and [P0 output](main/phase_rate_n8.json). Their upper endpoints are strictly negative. Both use fixed symbols, genuine infinite-past bounds and a finite conditioning partition; neither uses a rate Hessian or a fitted limit.

The single-imaginary-edge finite exclusion and odd/even parity block restriction also passed independent review. Their hypotheses and scope are preserved in [phase proof](phase/proof_or_blocker.md), [sparse unit](phase/sparse_unit.md), and the review report. Author-pending labels remain in frozen historical proof files; this verdict and the review commits record their later acceptance.

Two different phase units evaluated 54 finite harmonic Hessians and 30 chord distributions without a positive direction. This is finite evidence only. It neither excludes all odd multiharmonic directions nor proves a coefficient-family theorem.

The substantive remaining obligation is a controlled mixed-edge phase mechanism that overcomes the single-edge negative contributions, or a different fixed feasible scalar pair with certified L_endpoint-U_center>0. The two tested mechanisms and both selected pairs do not provide it. Repeating the same scans at larger windows has no positive evidence to justify it, so this round stops rather than widening the scan.

All three child tasks have completed and all recorded route-owned jobs have exited. No automatic retry, heartbeat or new main instance was created. The [checkpoint](checkpoint.json) records frozen objects, completed units, remaining obligations and job status for a later substantively new dispatch.

Correctness: the stated pair certificates and structural restrictions passed the reviews above. Formal verification: no Lean or proof-assistant certificate. Original conjecture: unresolved. Novelty and publication strength: unclaimed; these are scoped research elimination results, not a claimed new general theorem.
