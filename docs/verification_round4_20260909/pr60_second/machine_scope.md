# Machine Scope Addendum

This addendum records the scope change after receiving `machine_input/`. It does not modify or supersede the initial three files; it closes their named machine-evidence blocker.

## Included Machine Evidence

Machine packet directory:

`research/C2/pr60_independent52`

Machine binding:

`machine_input_binding.json`

The packet contains 45 bound files from PR64 head `5b40617fe7172aa266614aa28688d310218cb387`, executed implementation head `ee33372042d27911a97a14aefc6cb068404d190b`, and PR60 author head `f869fd251c0d6fdad737b6d5efa287307795a87d`.

Included in this closure:

- Independent implementation source: `implementation/pr60_independent_certificate.py`.
- Independent implementation README and execution guard/ledger.
- PR60 source copies needed by the machine unit: `inputs/pr60/README.md`, `bridge_checks.py`, `certificate.py`, `proof.md`, `sources_routes.md`, `verification.md`.
- Accepted structure input: `inputs/main/STRUCTURE.md`.
- Author P comparison data: `inputs/reference_P_components.json`, used only after fresh P extraction.
- Run02 raw outputs: `determinant_and_P.json`, `Q_full_box.json`, `Rstar_and_Rbar_entries.json`, `Ahat_entries.json`, `seed_leafswap_scaling.json`, `P_author_component_comparison.json`, `layer_results.json`, `run_metadata.json`, `PASS.json`, `exit.json`, stdout/stderr, PID/deadline/CPU records.
- Run01 retained failure artifacts and execution records.

## Excluded Material

Still excluded:

- Any C1 FIRST report, code, output, conclusion, or PR60 review.
- Any PR discussion, C3 adjudication, `FINAL_HANDOFF`, `machine_notes`, or summary README.
- Any PR57 premise for the full-r theorem.
- Any new arithmetic, SymPy execution, entropy job, remote job, or formal run by this reviewer.
- The fixed-diagonal radial-obstruction witness around `K*` and `D*`, pending its separate exact gate.

## Unit Status After Closure

| Unit | Initial Status | Machine-Closure Status | Scope |
| --- | --- | --- | --- |
| U1. Full Lambda-zero missing-edge family | INCOMPLETE | CORRECT | Full open domain `|mu|,|nu|,|r|<1`, `0<u<1`; all unequal diagonals and all nonzero edge ratios in the strict Lambda-zero missing-edge family, via the author analytic proof plus independent machine determinant/chart certificate. |
| U2. Conditional-entropy strictness | INCOMPLETE | CORRECT | Full six real symmetric directions on the same Lambda-zero family, by fixed-coordinate subtraction of the leaf marginal Hessian and integration of U1's positive M. |
| U3. Center-dependent nonzero-Lambda band | INCOMPLETE | CORRECT | For each fixed strict Lambda-zero arrow center, the explicit center-dependent band in `continuation.md` (25)-(27). No uniform width is claimed. |
| U4. Fixed-diagonal radial obstruction | EXCLUDED | EXCLUDED | Separate exact unit, not theorem evidence here and not an entropy counterexample here. |
| U5. One-sided perspective bridge | CORRECT | CORRECT, unchanged | Identity and scale bridge only; remaining coupled inequality stays incomplete. |

## Source Lines Used For Closure

Implementation source:

- Independence and non-import of author scripts: `implementation/pr60_independent_certificate.py` lines 2-7; `implementation/README.md` lines 3-9.
- JSON safety and Float rejection: `pr60_independent_certificate.py` lines 211-247.
- Polynomial and integer coefficient handling: `pr60_independent_certificate.py` lines 265-314.
- Common scalars, Rstar, Rbar, Bernoulli Gram/reflection: `pr60_independent_certificate.py` lines 317-445.
- Ahat construction: `pr60_independent_certificate.py` lines 448-463.
- Bareiss determinant, 24-product determinant, exact quotient P, zero remainder, P integer check: `pr60_independent_certificate.py` lines 483-572.
- Author component comparison after fresh P: `pr60_independent_certificate.py` lines 600-637 and 869-882.
- Integer chart loops and independent homogeneous-polynomial cross-check: `pr60_independent_certificate.py` lines 640-721.
- Full chart box and coefficient sign checks: `pr60_independent_certificate.py` lines 724-767.
- Seed, leaf swap, and determinant scaling to Rstar: `pr60_independent_certificate.py` lines 770-810 and 910-914.

Machine artifacts:

- Packet binding and independence: `machine_input_binding.json` lines 2-5 and 372-373.
- Source binding to PR60 and downstream comparison data: `machine_input/inputs/SOURCE_BINDING.json` lines 3-5 and 42-45.
- Determinant/P raw artifact: `outputs/run02/determinant_and_P.json` lines 2-2551.
- Q full-box raw artifact: `outputs/run02/Q_full_box.json` lines 2-17442.
- Layer results: `outputs/run02/layer_results.json` lines 43-546.
- Run metadata: `outputs/run02/run_metadata.json` lines 11-90.
- Run01 failure and run02 chronology: `execution/LEDGER.md` lines 14-68.

## Residual Limits

This addendum is not a formal proof-assistant certificate and not a novelty review. It closes only the mathematical and machine-evidence obligations for U1-U3 under the static second-review protocol.
