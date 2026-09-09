# PR41 independent compute plan

## Purpose

Use short, fixed, independently written checks for specific load-bearing
algebraic points that arise during the mathematical review. The implementation
must rebuild any checked object from definitions rather than importing author
formulas.

After this plan was first written, coordination issue 45 assigned C2 the public
full author-script replay and full independent all-event/jet/block/missing-edge
calculation within an initial 45 minute bound. This review will therefore not
start a duplicate full replay or long symbolic reconstruction. If full-compute
evidence is needed, this review may inspect the public issue-45 evidence after
it is available, without reading any private C2 directory.

## Local and server roles

- Windows local workspace: read source files, write this review's scripts,
  inputs, logs, and final report only under the owned `children/pr41`
  directory.
- Server: run any heavier symbolic or exact-rational computation only under
  `[isolated owned execution directory]`.

## Resource limits

- One CPU thread per job.
- Memory target at most 8 GiB.
- Wall clock limit 600 seconds per job.
- No GPU.
- No system package installation.
- Do not start computations expected to run longer than 60 minutes; instead
  record the exact handoff requirement.

## Checks to run, if needed

1. Environment and duplicate-job check: record Python, SymPy, NumPy, mpmath
   versions; list running commands in the owned server directory before
   launching a job.
2. Check the `G_s` derivative and Sylvester principal minors directly as a
   short one-variable symbolic calculation.
3. Check the two-point conditional-entropy reduction identities that carry the
   concavity proof: the `delta` identity, square completion, and determinant
   certificate.
4. If the prose review finds a concrete doubt in R2-T1, R2-T2, or the
   missing-edge coordinate identities, run only the smallest exact calculation
   needed to resolve that doubt.

## Artifacts to retain

- Scripts and exact inputs.
- Logs with flush after each phase.
- PID, command, versions, exit status, and elapsed time.
- Failed or partial outputs.
- A final review report with source path and line references.
