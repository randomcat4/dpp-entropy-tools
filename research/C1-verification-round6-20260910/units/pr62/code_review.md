# PR62 static code review

Static code verdict: `CORRECT/ACCEPTED_SCOPED` for consistency with the documented claims. I found no blocking code issue from source inspection. Independent computation status remains `INCOMPLETE` because this C1 review was not allowed to execute the scripts or arithmetic checks.

## Files reviewed

- `source-snapshots/pr62/code/verify_rank1_midpoint.py`, head `2ab69f71d4d36a2734beed83680dd3d9dc1f0a77`, blob `dbb9fa96cff42f98403817fe2984f96d22262a10`.
- `source-snapshots/pr62/code/probe_multiring_fixture.py`, head `2ab69f71d4d36a2734beed83680dd3d9dc1f0a77`, blob `fd476d5d12240943ad5e24eb0e4e8c1693b4704c`.
- Saved outputs `verify_rank1_midpoint.txt` and `probe_multiring_fixture.txt`, blobs `3429b53381dec9ca952cc977584bb2defe9da633` and `595f3680b4caa95765f25b6c50f61dff4a2f40ae`.

## Findings

No blocking findings.

## `verify_rank1_midpoint.py`

The script implements the advertised six-coordinate fixture and does not appear to broaden it into a theorem. It reconstructs complete DPP atoms using the signed event determinant (`verify_rank1_midpoint.py:L26-L43`), builds the rational Householder frame and endpoint kernels (`L90-L105`), verifies rank-one endpoint support and midpoint pair mass (`L107-L129`), checks the exact mass-transfer bridge for the fixture (`L130-L152`), verifies the exact bit-flip channel identity atom-by-atom (`L154-L166`), and evaluates the Fannes-Audenaert margin with `mpmath` after setting high precision (`L174-L191`). Lines `L174-L191` are high-precision evaluations, not outward-rounded enclosures, so this static consistency check is not a rigorous finite sign certificate for the displayed margin. The printed output fields match the documented fixture purpose (`L193-L213`) and the saved output (`output/verify_rank1_midpoint.txt:L1-L21`).

The script's finite derivative checks at three `r` values are correctly labeled as fixture checks, while the markdown proof supplies the full interval proof (`verify_rank1_midpoint.py:L144-L146`). I do not see a source-level mismatch between this script and `moving_rank1_theorem.md`.

## `probe_multiring_fixture.py`

The multiring script also stays within its documented diagnostic scope. It builds exact rational `A,C,B` and checks dense rank-two coupling (`probe_multiring_fixture.py:L46-L65`), constructs all 64 Schur-likelihood atom polynomials and normalization identities (`L67-L100`), cross-checks the `t=1` atom values against the full signed `6x6` event determinant (`L103-L109`), evaluates entropy curvature and cardinality layers from all atoms (`L112-L134`), and records exact Schur/Sylvester legality and endpoint-bracket checks (`L137-L165`). Source inspection finds these finite setup checks consistent with the prose, but independent finite evidence remains pending because C1 did not reconstruct them. The output explicitly prints `MOTIVATED_110_DIGIT_DIAGNOSTIC_NOT_INTERVAL_CERTIFICATE` and the final nonclaim (`L167-L202`; `output/probe_multiring_fixture.txt:L1-L2` and `L89-L91`).

The endpoint code uses symmetric Schur complements and Sylvester leading-minor checks in the places where positive definiteness is being asserted (`probe_multiring_fixture.py:L38-L39`, `L144-L165`). From source inspection, that is consistent with the prose claim in `multiring_fixture.md:L54-L90`.

## Hardening note

Both scripts use Python `assert` statements as the certificate mechanism. That is fine for the documented `python ...` reproduction command under ordinary interpreter settings, but a future CI or archival certificate should avoid optimized mode (`python -O`) or replace assertions with explicit checks that cannot be disabled. This is a hardening note, not a PR62 mathematical blocker.

## Execution status

Not executed by this reviewer. The exact rational checks, high-precision values, and byte comparison of saved outputs remain author evidence. C2 should independently reconstruct the finite fixture from the literal matrices and markdown formulas, use author runs only for comparison, and certify rational atom/channel identities plus outward logarithm enclosures for `G`, `omega`, and `G-2 omega>0`; a high-precision rerun alone is not a rigorous strict-sign certificate.
