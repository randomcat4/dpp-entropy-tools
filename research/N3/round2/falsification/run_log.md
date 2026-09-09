# Round-two run and failure ledger

Frozen theorem baseline: e476db1bb056af57e883a47f470ea0f4443c1837.
This child's unchanged author checkout entered the round at
f8a75e077c4ca449307e251ceef5f5c2bb6d218c, branch
research/N3-falsification-20260909. The new theorem file was read from the
parent's round-two checkout; author history was not reset to its integration
commit. These distinct provenance roles must not be conflated.

Responsibility is only research/N3/round2/falsification/. No child agents
were spawned; no issue or PR was created. Private connection information
and private reassessment documents are not copied into this artifact.

## Executed coverage

All actual computations used the assigned isolated server checkout and
/opt/venv/bin/python. Before the batch, process metadata was checked using
PID, comm, CPU and RSS only; no other process was stopped. Each job was
foreground, one at a time, with OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=
MKL_NUM_THREADS=NUMEXPR_NUM_THREADS=1. Python 3.12.3; mpmath 1.3.0. No GPU,
new dependency installation or global configuration change was used.

| Script | PID | Real calls | Exit |
|---|---:|---|---:|
| beta_affine_probe.py | 160926 | 12 segments x 9 parameters =108 full beta/dalpha/rho evaluations | 0 |
| beta_root_certificate.py | 161034 | 42 full beta bisection evaluations +5 rational interval evaluations | 0 |

Both commands used their repository-relative script paths under this
directory. The first took about 0.993 seconds; the second 3.544 seconds.
The batch used 160 decimal digits. The certificate used 240-bit outward
dyadic rational rounding, with 80-term exact log series and rigorous tails.
All mathematical evaluations were accepted; no domain rejection, zero
interval pivot, numerical anomaly or failed launch occurred in this unit.
The interval input [L,U] counts as one interval evaluation, not infinitely
many point calls; its mathematically uniform bound is proved by interval
inclusion, not inferred from sampling.

Source SHA-256 values are embedded in each result; source_manifest.json
also binds both new scripts and the two read-only round-one dependencies
unequal_sparse_probe.py and rank2_projection_check.py.

## Failure and limitation ledger

- beta>0 throughout the connected strict domain is refuted by the strict
  negative endpoint interval. That conjecture was a diagnostic idea, not
  an assumption of the frozen theorem.
- No sampled d alpha exceeded one; this finite non-hit is not a proof of B0.
- A beta root was proved to exist, but its bracket has d alpha<1, so it
  supplies no positive entropy-curvature or finite-chord counterexample.
- Root uniqueness and all other beta-zero components are unproved.
- The author interval certificate is not a fresh independent review.
- There was no scan expansion after the sign mechanism was found, and no
  second blind unit was launched. The new exact partial object is handed to
  the parent; continued universal proof work needs a distinct explicit task.
