# Attempts and Obstacles

## Read-only inherited material

The child read the parent task, the C1 frozen statement and claim, and the
round-two verdict/checkpoint/provenance/review/certificate files.  The old
exact beta-root certificate was used only as calibration and formula audit
input.  No parent checkout files were modified.

The originally requested top-level paths

    research/C1/frozen_statement.md
    CLAIM.md

were not present at the root path.  The corresponding files were found and
read at

    runs/C1/repo/research/C1/frozen_statement.md
    runs/C1/repo/research/C1/CLAIM.md.

## Fixed `u=(1,2,3)` twisted-complement table

The script `scripts/mechanism_probe.py` rebuilt all quantities from the eight
events and checked the assigned family

    K(t)=(1-t)A+tS(I-A)S,
    A=epsilon I+(3/5)uu^T,
    u=(1,2,3)/sqrt(14).

For epsilon=10^-2 it reproduced the old left root as high-precision
calibration, with `det(N)alpha=0.661527925989223...`.  For
epsilon=10^-2,10^-3,10^-4,10^-5 it found two beta sign-change roots per
epsilon.  The left-root `t/epsilon` values are

    0.226189936752769,
    13.1823655622027,
    142.490271811763,
    1435.54444106261.

Thus the fixed-ratio roots do not form a finite `t=epsilon*s` branch after
epsilon decreases.  Their `det(N)alpha` values move toward about 0.6446, not
toward 1.  The separate right roots are near the complement end and have the
same scalar values by the observed symmetry.

Two ratio-degeneration probes inside `mechanism_probe.py`,
`u=(small,2,3)` and `u=(1,2,epsilon)`, had no t-root on the bounded t grid and
kept beta positive on the tested checkpoints.  These are scouts only.

## Abandoned square-root interval variant

The first sparse phase script used the non-rational entries

    u_1^2=2/5, u_2^2=3/5, u_3^2=kappa epsilon.

High-precision signs reproduced the parent cue at epsilon=10^-12 and
10^-24, but the naive interval determinant used independent square-root
intervals.  On whole kappa brackets, the rank-one cancellations made the
interval event lower bounds or later solve bounds too wide.  This was an
interval-dependency failure, not mathematical counterevidence.

The final certificate therefore uses the rational finite-epsilon variant

    u=(3/5,4/5,q sqrt(epsilon)).

This variant has the same leading kappa=q^2 sparse cue but is not the same
finite-epsilon kernel as the square-root version.

## Certified rational sparse variant

The script `scripts/sparse_rational_certificate.py` found high-precision q
roots at epsilon=10^-6,10^-8,10^-12 and interval-certified the epsilon=10^-8
root bracket.  This is the strongest object produced by this child.

No entropy chord was produced because all certified beta-zero data stayed
strictly below `det(N)alpha=1`.  Therefore no H'' or finite positive chord
counterexample is claimed.
