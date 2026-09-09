# PR43 Events Verification Report

STATUS: PASS

Frozen PR commit: `4e1369ef2a59ccfaba3ca8fce95d85e78857bf78`.
Later doc-only PR head noted but not used for this frozen run: `7bd5962bbb2020ce47fbe286adda7dfe02f9645d`.

Scope: continuation task B/C bounded computation only. This report replays the two nested author exact scripts and independently reconstructs the requested event certificates from inclusion determinants by Boolean Mobius inversion. It does not certify the full analytic proof package, the LP task, novelty, or any entropy counterexample.

Resource envelope: one arithmetic thread, no GPU visibility, 45 minute ceiling. The remote runner applies a 4 GiB virtual-memory cap before launching Python.

Event convention: internal mask bit `i` is matrix coordinate `i+1`. Author-style labels print bits in descending coordinate order, so the rightmost label bit is matrix coordinate 1.

## Results

- Author `continuation/code/verify_continuation.py`: `ALL CONTINUATION CHECKS PASSED`
- Author `continuation/code/verify_continuation_v2.py`: `ALL CONTINUATION V2 CHECKS PASSED`
- Independent 3+5 event/conditional reconstruction: `PASS`
- Independent diagonal refresh state/transition table: `PASS`
- Independent two-mode quasi-free obstruction: `PASS`
- Independent reversible obstruction: `-125/78`

## Certificates

- `certificates/frozen_inputs.json`: frozen rational inputs and coordinate convention.
- `certificates/author_replay.json`: commands, stdout, stderr, exit codes, and last-line checks for the two nested author scripts.
- `certificates/active_sector_3plus5.json` plus `active_sector_t_*.json`: all 256 full events for each requested `t`, all 8 x 32 conditional events, exact inclusion determinants, exact Schur residuals, and exact principal-minor legality certificates.
- `certificates/diagonal_refresh.json`: all 8 states, all 64 transition probabilities, stationarity, detailed balance, and exact exterior-degree eigenrelations.
- `certificates/quantum_obstruction.json`: four-event input equality and output separation (`91/400` versus `99/400`).
- `certificates/reversible_obstruction.json`: four `Y_T^{-1}` matrices and exact `E_mu[d G12] = -125/78`.
- `certificates/checklist.json`: machine-readable task checklist and source-line map.

## Reversible Mechanism Note

If `Q` is self-adjoint in `L2(mu)`, `Q G12 = theta G12`, and `Q d = theta^2 d`, then `theta <d,G12> = <d,QG12> = <Qd,G12> = theta^2 <d,G12>`. For `0 < theta < 1`, this forces `<d,G12> = 0`, contradicting the exact value `-125/78`. This excludes the reversible exterior-noise mechanism only.

## Source Lines

- `continuation/CODEX_VERIFICATION_TASKS_v2.md` lines 31-46: author replay and independent Mobius event reconstruction scope.
- `continuation/CODEX_VERIFICATION_TASKS_v2.md` lines 50-63: bounded reversible mechanism obstruction scope.
- `continuation/frozen_statement_v3.md` lines 19-77: diagonal active-sector 3+5 fixture statement.
- `continuation/frozen_statement_v3.md` lines 78-150: rank-two exterior Markov mechanism statement.
- `continuation/frozen_statement_v3.md` lines 151-170: diagonal refresh exterior-degree mechanism.
- `continuation/frozen_statement_v3.md` lines 171-196: reversible two-point obstruction statement.
- `continuation/frozen_statement_v3.md` lines 197-214: two-mode quasi-free measurement obstruction statement.
- `proof/04_diagonal_active_sector.md` lines 103-164: rational 3+5 fixture inputs and legality bounds.
- `proof/06_quantum_measurement_obstruction.md` lines 10-69: two-mode four-probability obstruction arithmetic.
- `proof/07_markov_adjoint_and_reversible_obstruction.md` lines 91-170: reversible obstruction matrices and orthogonality argument.
- `continuation/code/verify_continuation.py` lines 49-239: author continuation exact verifier replayed as a black-box script.
- `continuation/code/verify_continuation_v2.py` lines 7-45: author v2 exact verifier replayed as a black-box script.
