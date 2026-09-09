# C2 independent formula review

Task: I05-C2-20260909, reviewer C2/review.

Status: PARTIAL FORMULA/CERTIFICATE CHECK. This is an independent algebraic and numerical sanity check of the five-point rank-three formulas and one rational non-commuting jet sample. It is not a proof of concavity, not a proof of a compensation theorem, and not a validation of any author-side candidate proof.

## Files

- `independent_c2_verify.py`: self-contained verifier.
- `exact_input.json`: exact rational input U, A, V, and q values.
- `event_jets.tsv`: exact p, p_prime, p_second for all 32 events.
- `output.txt`: server output with support counts, formula checks, entropy decomposition, and finite-difference calibration.

All auxiliary computation was run in the server review directory with BLAS/OpenMP thread limits set to 1. The local copies in this directory were synchronized back from that run.

## Exact setup

The verifier rebuilds U as the first three columns of H(a)H(b), with

```text
a = (1,2,3,4,5)
b = (2,-1,3,-2,1)
H(v) = I - 2 vv^T/(v^T v)
```

The independent rational test direction is

```text
A = diag(1/5, 1/3, 1/2)

V =
[ 1/50    1/200  -1/180 ]
[ 1/200   1/30    1/210 ]
[ -1/180  1/210   1/20  ]
```

This V does not commute with A:

```text
||[A,V]||_F^2 = 15289/1984500000 > 0.
```

For the largest finite-difference step used, h = 2^-8, Gershgorin bounds certify both A +/- hV and I-(A +/- hV) are positive definite, so the sampled path points are strictly valid.

## Algebraic coverage

The verifier constructs K(t)=U(A+tV)U^T over Q[t]. For every event S subset {1,...,5}, it computes

```text
p_S(t) = sum_{T superset S} (-1)^(|T|-|S|) det K_T(t)
```

as an exact rational polynomial. It then independently computes the provided low-order formulas:

```text
p_empty = det(I-A)
p_i     = r_i^T [A^2 + (1-tr A)A + det(A)I] r_i
p_ij    = w_ij^T [adj(A) - det(A)I] w_ij
p_ijk   = det(A) det(U_ijk)^2
p_S     = 0 for |S| >= 4
```

with A replaced by A+tV. These two polynomial constructions agree exactly for all 32 events.

Coverage result:

```text
positive support count = 26
zero event count       = 6
zero event bad jets    = none
formula mismatches     = none
```

The 10 q values reconstructed from U match the q values in the prompt exactly and sum to 1. The computed top entropy constant is

```text
c = -sum q log q
  = 1.9001618764609496439699529684601415549857825175720736391228390816002999466128551
```

which lies inside the stated interval.

## Normalization jet

Summing the exact event jets over all 32 events gives

```text
sum p        = 1
sum p_prime  = 0
sum p_second = 0
```

This checks the full event partition through second order for the chosen non-commuting rational direction.

## Entropy curvature by cardinality

Using the convention

```text
Fisher_cost = sum (p_prime)^2 / p
log_accel   = -sum p_second log(p)
curvature   = -Fisher_cost + log_accel
```

the server run gives:

```text
size  pos zero  Fisher_cost            log_accel              curvature
0       1    0  0.00816666666666667    0.00603280191906669   -0.00213386474759997
1       5    0  0.000550824329816457  -0.0164395236804262    -0.0169903480102426
2      10    0  0.00598960578652416    0.00199029734415239   -0.00399930844237176
3      10    0  0.003                 0.0103130181773465     0.00731301817734647
4       0    5  0                      0                      0
5       0    1  0                      0                      0
```

Total analytic curvature for this test is

```text
H_second = -0.0158105030228678979424508645854895860530329703232218693798777.
```

The top layer is positively curved in this sample, but the lower layers overcompensate it. This sample is only a calibration example and should not be used as evidence for a general theorem.

## Top determinant check

For d(t)=det(A+tV), the exact jet is

```text
d        = 1/30
d_prime  = 1/100
d_second = 926533/476280000
```

The top Fisher and top entropy-constant terms are

```text
F_top = (d_prime)^2/d = 0.003
c*d_second             = 0.0036964866966553142195271949981655335839540649058403
(2c/3)*F_top           = 0.0038003237529218992879399059369202831099715650351441
```

The checked sample satisfies the stated inequality

```text
c*d_second <= (2c/3)*F_top.
```

This is a sample check of the formula and bound value, not a proof of the inequality for arbitrary A,V.

## Finite-difference calibration

The analytic H_second was compared with direct high-precision central differences from the exact event polynomials:

```text
h      finite_difference              finite_difference - H_second
2^-8   -0.0158105034182877797370      -3.95419881794552682265e-10
2^-12  -0.0158105030244125067516      -1.54460880917967347498e-12
2^-16  -0.0158105030228739315706      -6.03362815926996035393e-15
2^-20  -0.0158105030228679215113      -2.35688599971240495521e-17
```

This confirms the second-jet entropy formula numerically for the exact rational non-commuting path.

## Not covered

- No author-side new implementation was read before this independent reconstruction.
- No round2 source review was read in this pass.
- No anonymous candidate compensation proof has been received or reviewed.
- No general concavity theorem, compensation theorem, or counterexample certificate is certified here.
- The rational A,V sample is a local calibration example only. It must not be promoted to a main conclusion about all five-point rank-three faces.

## Reviewer verdict

The provided low-order event formulas for the fixed five-point U pass this independent exact-polynomial check through second order along a non-commuting rational direction. The support statement also passes: exactly the 26 events with |S| <= 3 are positive at the chosen interior A, and the 6 events with |S| >= 4 are identically zero with zero first and second jets.

Further review should wait for a frozen candidate compensation proof or a claimed counterexample certificate. The next review should check that candidate proof against the exact event table and should not rely on this one calibration sample as the main mathematical evidence.
