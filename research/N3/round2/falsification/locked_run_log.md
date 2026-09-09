# Final bounded locked-odds unit: execution and failure ledger

Target author commit: 99205d9ac552355c148f011bb053731a8b1349f0.
Main round-two theorem baseline: e476db1bb056af57e883a47f470ea0f4443c1837.
This child's previous frozen commit: ab914ec2f73577907314ab3119c4d9f499b17e10.
Only new locked_* files were added; the root certificate and old frozen
objects were not edited. No subagents, issues, PRs or external messages
were created by this unit. Parent coordination is internal to the team.

## Budget and actual execution

Exactly four authorized existing rational kernels were used:
the stationary .01[[51,24,-24],[24,48,-24],[-24,-24,52]], the negative-beta
A, the midpoint of the already-certified root bracket, and the half-fill
main tangent kernel .01[[50,4,6],[4,50,8],[6,8,50]].

At each K an exact rational g was computed and a five-column rational basis
of ker(g^T) formed by one explicit nonzero pivot. All five basis identities
were checked with Fraction arithmetic. Numerical orthonormalization was
used only to condition the subsequent search. Exactly two deterministic
spectral starts per kernel were used, for eight starts in total. The first
is the smallest-eigenvalue vector of the mean of the three restricted
Q_k^lock-C matrices; the second comes from the first restricted matrix.
Each SLSQP run had at most 160 iterations. No random seed was used.

| Execution | PID | Coverage | Exit |
|---|---:|---|---:|
| locked_probe_failed_v1.py (then named locked_probe.py) | not captured | first kernel rational p,J,g,F,Q and nullspace constructed; failed during C assembly before any optimizer call | 1 |
| locked_probe.py | 161752 | 4 full kernels, 8 starts, 196 actual objective calls | 0 |
| locked_certificate.py | 161832 | 1 rational kernel, 1 exact projected direction, 1 strict certificate | 0 |

The initial source and its hash are retained. Its failure was a TypeError
inside mpmath.det/LU on a singular two-by-two cofactor during polarization
of C. Replacing that call with the explicit two-by-two determinant
polynomial resolved it. This is not a failed mathematical inequality or a
domain rejection. The failed run's short-lived PID was not captured; this
execution limitation is disclosed rather than reconstructed. The replay
prints its PID immediately. All optimization success flags and per-start
call counts remain in locked_probe.json.

Commands from the isolated server checkout root were

    /opt/venv/bin/python research/N3/round2/falsification/locked_probe.py
    /opt/venv/bin/python research/N3/round2/falsification/locked_certificate.py

Every invocation set OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=
NUMEXPR_NUM_THREADS=1. Each was foreground and completed before another
started. Runtime: Python 3.12.3, numpy 2.1.2, scipy 1.14.1, mpmath 1.3.0.
The successful scout took approximately 0.047 seconds; the certificate
approximately 0.525 seconds. No GPU, dependency installation, global
configuration edit, or interference with another job occurred.

## Result and stopping state

The small-denominator projected rational direction at A has exact gD=0,
exact equality of all three pairs of slice odds derivatives, and strictly
negative max Qlock-C. The certificate also retains all event Fisher and
proves true B>0; K+/-D/1000 is strictly feasible by exact minors.

DISPROVED_LOCKED_DOMINANCE_ONLY. Neither the valid F>=Qlock bound nor B0
nor entropy concavity is disproved. An additional residual or a different
argument is still necessary for Lambda-tangent concavity.

The final authorized bounded unit is complete. There is no active worker,
unmanaged server job, expanded family, subsequent scan or planned retry.
The parent owns review and integration; this child stops after committing
the new locked_* artifacts.
