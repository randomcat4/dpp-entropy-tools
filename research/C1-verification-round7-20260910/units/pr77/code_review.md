# PR77 static code review

Scope: static source review only. I did not execute Python, run the submitted checkers, rebuild outputs, or perform independent arithmetic. That no-execution boundary leaves independent finite evidence `PENDING_C2`; by itself it is not a code defect and not an author mathematical error.

Overall static verdict: `NEEDS_FIX` for certification packaging. I did not find a clear source-level bug that reverses the analytic logic, but the committed output artifacts are too summarized and not traceable enough to serve as public checkable certificates.

## Findings

### P1. Committed PASS summaries omit raw intervals and do not match the scripts' full default outputs

Status: `NEEDS_FIX` for source-package auditability.

The midpoint script returns detailed fields such as `finite_details`, `tail_bound_exact`, `tail_bound_upper_decimal`, `true_midpoint_gap_lower`, and comparison constants (`source-snapshots/pr77/code/certify_midpoint_rate_gap.py:356-377`) and defaults to writing `midpoint_rate_certificate.full.json` (`source-snapshots/pr77/code/certify_midpoint_rate_gap.py:380-389`). The committed frozen output is instead a short summary with no final interval, no determinant histogram, no exact event-count evidence, and no margin above `1/10000` (`source-snapshots/pr77/output/midpoint_rate_certificate.json:1-16`).

The point-curvature script likewise returns detailed finite and true curvature intervals, tails, and comparison data (`source-snapshots/pr77/code/certify_point_curvatures.py:422-463`) and defaults to `point_curvature_certificate.full.json` (`source-snapshots/pr77/code/certify_point_curvatures.py:466-475`). The committed output is again only a short PASS summary (`source-snapshots/pr77/output/point_curvature_certificate.json:1-21`).

Why it matters: a reviewer cannot check the exact margin, tail direction, or interval arithmetic from these frozen outputs. The source code may be capable of producing the needed evidence, but the public frozen artifact does not contain it. This is a packaging/evidence defect, not a finding that the finite inequalities are false.

Minimal repair: commit or otherwise publish the full machine-readable outputs generated from the frozen scripts, including raw intervals, exact tails, event counts, distinct numerator/jet counts, and final margins. Include hashes tying outputs to the exact source.

### P1. Point-curvature execution is missing from the run record

Status: `NEEDS_FIX` for source-package consistency.

`point_curvature.md` says the recorded execution of `certify_point_curvatures.py --depth 18` exited zero (`source-snapshots/pr77/point_curvature.md:218-224`), and the output summary claims exit status zero (`source-snapshots/pr77/output/point_curvature_certificate.json:17-20`). But the frozen `run_record.json` lists only the midpoint certificate, band automaton check, and analytic constants check (`source-snapshots/pr77/output/run_record.json:8-23`). It does not list the point-curvature command.

Why it matters: the point-curvature claims are stronger than the midpoint value theorem and are entirely certificate-driven. The frozen record is inconsistent about whether the point-curvature run is part of the recorded execution set. This does not show the point-curvature arithmetic is wrong; it means the submitted record is incomplete.

Minimal repair: regenerate or amend the run record to include the point-curvature command, exact source hash, output hash, environment, exit status, and path to the full output.

### P2. The "independent" small checks share code and matrix construction with the main certificates

Status: `NEEDS_FIX` for outward certification; acceptable as internal consistency checks.

`check_band_automaton.py` imports `certify_midpoint_rate_gap.py` and uses the module's direct signed-event numerator function (`source-snapshots/pr77/code/check_band_automaton.py:18-25`, `source-snapshots/pr77/code/check_band_automaton.py:28-38`). The midpoint certificate's Mobius check also uses the same `scaled_kernel`, direct determinant routine, and signed-event convention as the main source module (`source-snapshots/pr77/code/certify_midpoint_rate_gap.py:79-145`).

`certify_point_curvatures.py` imports the midpoint certificate module and uses its signed-event numerator in the interpolation-based jet check (`source-snapshots/pr77/code/certify_point_curvatures.py:35-42`, `source-snapshots/pr77/code/certify_point_curvatures.py:326-387`).

Why it matters: these are useful self-consistency checks, but they are not fully independent literal reconstructions of the mathematical event specification. A shared sign convention, scaling convention, or kernel-construction mistake could pass across all of them. This is a limit on certification strength, not an observed mismatch.

Minimal repair: C2 should implement the event matrices from the frozen mathematical statement without importing the author modules, then compare exact event probabilities/jets against the author outputs.

### P2. Author output summaries do not preserve enough environment and arithmetic metadata

Status: `NEEDS_FIX` for reproducibility metadata.

The code relies on `Decimal.ln` at precision 100, widening by `1e-90`, and directed floor/ceiling arithmetic (`source-snapshots/pr77/code/certify_midpoint_rate_gap.py:41-46`, `source-snapshots/pr77/code/certify_midpoint_rate_gap.py:244-281`; `source-snapshots/pr77/code/certify_point_curvatures.py:27-31`, `source-snapshots/pr77/code/certify_point_curvatures.py:149-158`). The official Python documentation supports the key premise that `Decimal.ln()` is correctly rounded using `ROUND_HALF_EVEN`, but the frozen summaries record only Python version and no libmpdec version, flag/trap policy, full interval payload, or output hash (`source-snapshots/pr77/output/midpoint_rate_certificate.json:9-15`, `source-snapshots/pr77/output/point_curvature_certificate.json:14-20`, `source-snapshots/pr77/output/run_record.json:1-27`).

Why it matters: the proof is intentionally a narrow interval certificate. Reproducibility and auditability require exact arithmetic metadata and raw interval endpoints, not only method prose.

Minimal repair: include full arithmetic context in generated JSON: Python implementation/version, decimal backend/libmpdec version if available, precision, rounding contexts, widening value, final lower/upper bounds, and output/source hashes. C2 may alternatively use a separate interval-log library and record its own proof certificate.

### P3. The code's output path convention and committed filenames are easy to confuse

Status: `NEEDS_FIX` if these artifacts are meant to be public certificates.

The midpoint and point scripts default to `.full.json` outputs (`source-snapshots/pr77/code/certify_midpoint_rate_gap.py:380-389`, `source-snapshots/pr77/code/certify_point_curvatures.py:466-475`), while the frozen committed files use shorter names without the full payload. This may be intentional curation, but it makes the frozen source packet look more certified than it is.

Minimal repair: either commit the `.full.json` files, rename the summary files as summaries, or state in `README.md`/`RESULT.md` that the committed output files are abbreviated and not raw certificates.

## Non-findings

I found no static evidence that the midpoint script omits complete events: the recursive determinant-count routine branches over zero/occupied diagonals, verifies positivity, normalization, and total event count (`source-snapshots/pr77/code/certify_midpoint_rate_gap.py:207-241`).

I found no static evidence that the point-curvature script uses `H_n/n` in place of the finite conditional curvature: it computes `H_n''` and returns `H_{n+1}''-H_n''` (`source-snapshots/pr77/code/certify_point_curvatures.py:161-213`).

I found no static evidence that the RPF/curvature formulas intentionally drop Fisher, acceleration, or invariant-measure response terms; the author proof and status files repeatedly keep those terms (`source-snapshots/pr77/proof.md:381-405`, `source-snapshots/pr77/RESULT.md:43-52`, `source-snapshots/pr77/attempts.md:33-42`).

## C2 code expectations

C2 should not be an author rerun. It should build a fresh checker from the frozen mathematical specification, verify author outputs only as comparison data, and publish raw evidence sufficient for a reviewer to recompute the final inequalities from the JSON alone.
