# C2 round 3: completed exact verification

Status: READY_SCOPED for issue 45 and PR47.

| Object | Result | Evidence |
|---|---|---|
| PR41 eight-event symbolic computation | PASS within the frozen identity scope | `pr41/REPORT.md`, `pr41/evidence.json` |
| PR43 B/C full-event fixtures | PASS for every specified rational fixture | `pr43_events/output/REPORT.md`, complete event and conditional tables |
| PR43 D directed-flow LP | Exact rational feasible flow, independently accepted `CORRECT_WITH_SCOPE` | `pr43_flow/flow_certificate.json`, `pr43_flow_review/REVIEW.md` |

The flow certificate has 33 positive directed edges among all 56 ordered pairs. An independent reconstruction verifies the complete law, strict C and I-C, all 40 linear equations, and the explicit density-adjoint generator. It is not reversible: one exact difference is

```
r_000_001 - r_001_000 = -10820517324948991/539204267981520000.
```

Thus this fixed input admits a stationary finite Markov generator whose density adjoint contracts G11, G12 and G22 at rate 1 and det(G) at rate 2. This is the complete accepted scope of the new certificate. It does not prove the required entropy-dissipation curvature inequality, general block-radial entropy concavity, or a true stationary entropy-rate statement.

The symbolic and event checks retain all configurations and the full Fisher terms wherever claimed. The two nested PR43 author verifiers and PR41 author verifier replayed successfully. The independently reconstructed occupation-channel obstruction gives 91/400 versus 99/400; the reversible obstruction gives -125/78. These mechanism obstructions are not entropy counterexamples.

Three initial units and one subsequent fresh certificate-review unit were completed, with no more than three children active at once and no descendants. Failed/interrupted launches and their checkpoints are retained. All recorded job PIDs were absent at the final check. No additional C,V input, old single-box expansion or counterexample scan was run.

Correctness of these exact computations and the finite generator is accepted at the stated scope. Full upstream theorem review belongs to C1/C3. Novelty is unreviewed by C2. Old task E's endpoint/error contract and any bounded task F inputs remain outstanding in issue 45; no dependent computation has been claimed by guessing those parameters.
