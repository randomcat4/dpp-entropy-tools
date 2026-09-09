# C2 hand-off to C1 and C3: PR60 independent machine chain

**MACHINE_PASS**, for frozen PR60
`f869fd251c0d6fdad737b6d5efa287307795a87d` and main
`9dcb6e9079ca57f94e0e30d63161cda89ca61fae`.

C2 has completed the separately authorized independent machine unit. C1 owns
mathematical bridge FIRST; C3 receives the evidence and controls integration.
This document does not supply a mathematical FIRST or SECOND verdict.

## Exact evidence

The checker starts from the displayed Gram and long/short Schur formulas.
It does not import or run PR60's certificate.py or bridge_checks.py, or use
the old r=0 certificate as a premise. It computes the determinant and extracts
fresh P before opening the statically extracted author P component strings.

- All16 long/short matrix normalization identities are zero.
- All16 Ahat entries are exact polynomials.
- Own QQ fraction-free Bareiss and independent24-product determinants agree.
- Exact division by8tJ^3L^3C^3 gives P with279 integer coefficients and
  degrees(4,4,10,6), with zero remainder. All coefficients agree with the
  author's displayed component construction.
- Integer-binomial and homogeneous-polynomial Q constructions agree. All1925
  coefficient positions are present:1731positive,194zero,min192,constant432.
  Every displayed groupcount and group minimum matches.
- The two polynomial symmetries, exact positive seed, full matrix leafswap
  congruence and determinant scaling to Rstar pass.

The P object is stored over QQ, and every denominator is separately checked
to be1; thus integrality is actually tested, not inferred from a domain label.
Intermediate Bareiss pivots are used only in exact polynomial divisions;
this machine evidence does not assume their nonvanishing at every point.

## Frozen executable and retained failure

| Stage | Public commit |
|---|---|
| First executable | `47938e32ebec8f8e39607953efe7040fd9ecf14b` |
| Single-line repaired executable, successful run | `ee33372042d27911a97a14aefc6cb068404d190b` |

Run01 passed Gram, normalization and polynomial entries, then failed on a
list indexing TypeError in the independent determinant cross-check. Run02
changes only that index access and succeeds. The first failure is preserved;
no mathematical residual mismatch or source formula repair is hidden.

Read [machine_notes.md](machine_notes.md),
[run02/PASS.json](outputs/run02/PASS.json),
[full layer records](outputs/run02/layer_results.json),
[full determinant/P](outputs/run02/determinant_and_P.json), and
[complete Q box](outputs/run02/Q_full_box.json).
The [ledger](execution/LEDGER.md) and [run01 failure](outputs/run01/FAILURE.json)
record the preparation and execution history.

## Execution closed and scope

The shared45-minute window began15:28:03UTC and retained the hard16:13:03UTC
deadline. Run01 took28.569seconds; run02 took52.957seconds and ended15:32:32UTC.
Both arithmetic PIDs174230 and174315 were confirmed absent. No jobs remain;
no overlap, expansion or generic scan occurred. The allocation was one
process/CPU/thread,16GiB,noGPU.

C1 must still assess the full analytic bridge at its actual review scope:
physical fixed directions, symmetry-domain coverage, positive denominators,
nonvanishing before inertia, and integration to entropy curvature. The
additional Lambda-nonzero band and radial obstruction in PR60 continuation
are not checked by this C2 machine unit. No PR58 task has been launched;
PR59 finite-memory checks are not interpreted as true DPP entropy-rate output.
Old PR55/PR57 artifacts are untouched. No novelty or Lean claim is made.