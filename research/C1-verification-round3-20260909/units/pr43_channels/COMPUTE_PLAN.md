# PR43 channel/extension compute plan

Reviewer workspace: `this unit directory`.
Optional private server workspace: `[isolated owned execution directory]`.

## Public compute delegated to C2 and not repeated here

- Full author continuation-verifier replay.
- Full 3+5 `t in {1/5, 1/2, 1}` enumeration over all 256 events/conditioned events/refreshed features.
- Two-point obstruction replay if already covered in public C2 issue output.
- Task-D/nonreversible LP search.

## Local analytic-first checks

1. Read the frozen v3.1 statement, v2 verification tasks, continuation proofs, proof files `01`, `02`, `03`, `04_diagonal_active_sector`, `05_exterior_markov`, `06_quantum_measurement_obstruction`, and `07_markov_adjoint_and_reversible_obstruction`.
2. Read the C3 dependency statement/proof and record exactly which hypotheses the PR43 D/I/J claims need.
3. Rebuild small exact formulas from definitions when they are short and decisive: two-point DPP laws, occupation-channel distributions, the reversible obstruction scalar, and finite symbolic sign/coefficient identities whose inputs are explicitly specified in the proof.
4. For 3+5 and arbitrary-rank I, inspect proof logic and code inputs; rely on C2 for full public enumeration, while recording any missing bridge that remains independent of computation.

## Short-check execution rules

- Use only this child directory for scripts and outputs.
- One numerical thread, 8 GiB effective ceiling, 600 seconds per job.
- Freeze every script's mathematical input, algorithm, expected exact/rational output, and stopping condition before running it.
- Keep the script, stdout/stderr, version, start/end time, exit code, and any failure notes.
- Before using the private server, check only this server directory for existing jobs and do not install system dependencies.

## Heavy-check handoff trigger

If a necessary check exceeds the short exact scope above, write a precise handoff object for C2/main: mathematical object, input parameters, algorithm, resource needs, exact/numeric error standard, and stopping condition. Do not launch the heavier computation here.
