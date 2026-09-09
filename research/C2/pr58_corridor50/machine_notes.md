# Machine notes: PR58 corridor independent source

Prepared an independent finite verifier source at `research/C2/pr58_corridor50/implementation/independent_pr58_certificate.py`.

Scope:

- Frozen source commit: `1770ed29e8487b8f39aebb4c9466406c7493e580`.
- Public claim: `https://github.com/randomcat4/dpp-entropy-tools/issues/50#issuecomment-5604628245`.
- Included objects: original RESULT section 4 fixture, the four rational corridor intervals `[3,9]`, `[8,12]`, `[11,14]`, `[14,15]`, and the `s=10` W/true-curvature sign checks.
- Excluded objects: `a4f05cc` joint-additive material, the different `s=9/10` fixture, issue63 whole-chord work, theorem review, novelty review, and Lean work.

Implementation summary:

- The verifier parses literal rational `A,C,U,V` from `inputs/RESULT.md` and constructs `B=UV^T`.
- It reconstructs all 64 complete-event determinant polynomials directly from the 6x6 kernel `K(t)` over `QQ[t]`, using only standard-library `Fraction` arithmetic and a permutation determinant.
- It derives `pA`, `pC`, `mu=pA*pC`, and each `q(t)=1-a*t^2+b*t^4` from those direct event polynomials, then checks normalization and global/fiber cancellations.
- It verifies Mobius principal and complementary minor identities as exact polynomial equalities, so positivity of all complete events on the corridor certifies legality through exact finite sums.
- It computes corridor extrema by endpoints plus rational vertices and applies the displayed `Psi`, `M2lower`, `left`, and squared-margin inequality with exact rational comparisons.
- At `s=10`, it checks the frozen exact value `min q = 121400093597/249280204050`, encloses each `log(q)` with a one-sided signed rational atanh tail, and sums the W interval and true scaled curvature interval from rational endpoints.
- The true curvature is reconstructed first from derivatives of `p=mu*q`, then checked against the displayed `u,y` normal form. The s10 output also records per-left and per-right derivative log-coefficient cancellations explaining why the `log(mu)` terms drop.

Run boundary:

- I did not run the verifier, Python, SymPy, CAS, or remote arithmetic.
- The source never reads, imports, or executes `author_checker_reference.py`.
- The source reads `author_output_reference.txt` only after independent reconstruction. The downstream exact-fraction comparison requires all 26 frozen corridor values: `Amax`, `Bmax`, and for each of `[3,9]`, `[8,12]`, `[11,14]`, `[14,15]`, the `qminus`, `qplus`, `Psi`, `M2`, `left`, and `squared strict margin` fractions. It also compares the s10 `min q` fraction. The comparison record is written before any mismatch failure is raised.
- Rounded decimal displays are not promoted to exact outward endpoints.
- Runtime options are `--input-root`, `--out`, and `--wall-seconds`; wall time is capped at 2700 seconds and additionally bounded by `C2_ABSOLUTE_DEADLINE_EPOCH` when present.

## Run01 result

Root-run01 passed from the frozen public source `86617882b7db97f5db39bf613d876a5d5bcf9107` / local source `ab02c1750efa8634cfe7df2be08f9d45c6fd739e`.

Run metadata from `research/C2/pr58_corridor50/outputs/run01`:

- Guard start marker: `2026-09-09T16:09:13Z`.
- Guard finish marker: `2026-09-09T16:09:18Z`.
- Absolute deadline marker: `2026-09-09T16:54:13Z`.
- Exit status: `0`.
- Arithmetic PID: `174584`; timeout PID: `174582`; wrapper PID `174568` per root run record.
- Root confirmed the arithmetic PID absent around `2026-09-09T16:09:55Z`; root owns the precise absence timestamp.
- No exact checker-elapsed metadata is available. The guard UTC markers span 5 seconds at 1-second resolution; no finer runtime is inferred here.

Saved artifacts:

- All six progress layers were emitted: `inputs`, `events`, `identities`, `corridor`, `s10`, `reference_compare`.
- `MACHINE_PASS.json` reports status `MACHINE_PASS`, no failures, source commit `1770ed29e8487b8f39aebb4c9466406c7493e580`, and the expected one-process, one-thread, no-GPU bound.
- The output directory contains 9 JSON artifacts validated by root, including `events.json`, `identities.json`, `corridor.json`, `s10.json`, and `reference_compare.json`.
- `s10.json` is about 14 MB and stores the full 64 events with 6400 one-sided atanh log terms.

Finite certificate facts recorded by the artifacts:

- `events.json`: 64 complete-event determinant polynomials were reconstructed directly over `QQ[t]`; the Schur-complement trace/e2 formula was used only as a posthoc cross-check.
- `identities.json`: product weights sum to `1`, global `sum mu*a` and `sum mu*b` are both `0`, and all 64 principal/complementary Mobius polynomial identities are verified exactly.
- `corridor.json`: each of the four intervals has 64 event extrema, strictly positive `q_minus`, and strictly positive squared margin:
  - `[3,9]`: `q_minus = 745404441907/1384890022500`, squared-margin floor `0.000002115899093896045867781879411802214246581840219249767271937690274330601621019035655865`.
  - `[8,12]`: `q_minus = 399437021266/1038667516875`, squared-margin floor `0.001055547360765217901145508654034145071973349945051536497047477991309660461039381995161377`.
  - `[11,14]`: `q_minus = 1758582028579/6232005101250`, squared-margin floor `0.001061334831726561495214625142657240521529357877895619238045638365022883331449579089839312`.
  - `[14,15]`: `q_minus = 1535668823/6647472108`, squared-margin floor `0.001114562525621531545890297076887913277059670745623859787734506782408556187478017573468095`.
- `s10.json`: `min q = 121400093597/249280204050`, matching the frozen value. `W(10)` has negative upper endpoint, with width ceiling below `5.83e-83`. The true scaled curvature lower endpoint is greater than `0.17037745196806863130550498470533808479721333392335`, with width ceiling below `8.71e-79`.
- `reference_compare.json`: all 27 required exact fractions matched author output: the 26 corridor values (`Amax`, `Bmax`, and six interval quantities for each of four intervals) plus `s10.q_min`. No required reference value was missing and no mismatch was recorded.

Rounded display limitation:

- The original output prints identical-looking decimal endpoints for `W(10)` and curvature. Those are treated only as rounded display text. The machine certificate uses the exact rational interval endpoints and width checks in `s10.json`.

Interpretation boundary:

- This is a C2 machine pass for the finite original PR58 corridor and s10 signs only. It does not assert theorem acceptance, novelty, full-chord coverage, entropy counterexample status, or publication integration. C1/C3 analytical gates remain separate.
