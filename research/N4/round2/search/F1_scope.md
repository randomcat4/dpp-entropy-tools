# F1 fixed-nullspace scout

Status before execution: 72 prescribed centers, one bounded work unit. No class
conclusion is licensed by a numerical non-hit.

Six rational Householder frames use integer vectors (1,1,1,1), (1,2,3,4),
(1,1,1,5), (1,2,4,1), (1,1,4,4), and (1,2,2,2). The first three columns
of H=I-2ww^T/(w^Tw) form U; its fourth column is z. All z coordinates are
nonzero. Changing w starts a new face, never a direction within a face.

Each face receives 12 exact rational centers with spectra specified in source:
one moderate isotropic control and 11 rotated spectra covering sparse, dense,
near one-zero, near two-zero, near one-one, near two-one, and split scales.
Seed 202609090427 selects products of two rational 3D Householder rotations.
The source, seed, dependency versions and actual invocation counts are saved.

All 15 proper events use the signed determinant identity, evaluated at 60
decimal digits, with direct determinant first/second jets via inverse traces.
Full event p,p',p'' are structural zeros, excluded before Fisher assembly.
All six symmetric directions are retained in the Hessian. Basis coordinates
use diagonal entries and unscaled symmetric off-diagonal pairs; reported
eigenvalues use the Frobenius orthonormal normalization.

At each center the top direction is rounded entrywise to denominator 10^9.
Three rational t values (0.03, 0.25, 0.75 times the symmetric feasible radius,
rounded to denominator 10^12) give fixed-U A-affine chords. No eigenspace
movement enters a chord. Feasibility is checked by rational Sylvester minors.
The direct formula retains every event's Fisher and acceleration and groups
them by cardinality for diagnosis. The principal investigator's new layer
formula is not assumed by the implementation.

Positive numerical curvature or gap triggers immediate freezing of U,A,V,t
and return to the principal investigator; no certificate is inferred from
mpmath output. If no positive candidate exists, diagnose top curvature and
cardinality contributions, commit F1, and stop new batches pending direction.
