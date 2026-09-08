# D10-S8b preconditioned expansion

AUTHOR STATUS: PROOF_CANDIDATE_PENDING_FRESH_REVIEW.

This file is additive to the S8 certificate.  It does not weaken, overwrite, or
replace the already preserved `[-6/25,6/25]` proof.  The new claim is a larger
continuous interval for the same M8 Section 5 rational line:

\[
K(t)=K_0+tR,\qquad
K_0=\frac15U+\frac12V+\frac45W,\qquad
R=\frac15U+\frac13V+\frac23W .
\]

## Expanded candidate theorem

For every

\[
t\in[-29/100,29/100],
\]

the full exact-event Shannon entropy Hessian is strictly negative definite on
the entire observation-coordinate space `Sym(3)`.

Equivalently, with

\[
B(t)=-D^2H(K(t)),
\]

the `6 x 6` matrix of \(B(t)\) in the coordinate order
`(11,22,33,12,13,23)` is positive definite for every `t` in the interval.

The endpoint `29/100` is close to the first positive spectral feasibility
degeneration at `3/10`, where the third eigenvalue of `K(t)` reaches `1`.
On the certified interval, the strict spectral margin is still

\[
\min_i \{\theta_i(t),1-\theta_i(t)\}\ge 1/150.
\]

## What changed from S8

The original S8 certificate used raw coordinate Gershgorin diagonal dominance.
That closed `6/25` but failed at `49/200` and `1/4` even though float eigenvalue
scouts showed no positive curvature signal.

S8b keeps the same exact-event atom jets and log intervals, but changes the
positive-definiteness gate on hard leaves:

1. First try the old coordinate Gershgorin test on \(B(t)\).
2. If it fails on a rational subinterval \(I\), take the midpoint \(m\), compute
   a numerical Cholesky preconditioner for \(B(m)\), and rationalize it to an
   upper-triangular matrix \(P\).
3. The numerical step is only proposal generation.  The actual certificate uses
   the fixed rational \(P\).
4. Since \(P\) is upper triangular with positive rational diagonal, it is
   invertible.  If interval arithmetic proves
   \[
   P^\top B(t)P\succ0
   \]
   for every \(t\in I\), then \(B(t)\succ0\) on \(I\).
5. Positive definiteness of \(P^\top B(t)P\) is again certified by strict
   Gershgorin diagonal dominance using rational interval entries.

For the largest certified radius `29/100`, every leaf interval and every fixed
rational preconditioner \(P\) is saved in
`s8b_preconditioned_certificate.json`.

## Expansion results

Final scripted attempts:

| radius | result | leaves | method summary | min displayed margin | spectral margin |
|---:|---|---:|---|---:|---:|
| `49/200` | certified | 34 | 33 preconditioned, 1 plain | `0.07096334040982199670860796156` | `11/300` |
| `1/4` | certified | 34 | 34 preconditioned | `0.03749267285783075401730722536` | `1/30` |
| `7/25` | certified | 49 | 48 preconditioned, 1 plain | `0.0002105394761927160290971484924` | `1/75` |
| `29/100` | certified | 67 | 65 preconditioned, 2 plain | `0.0004096514363704310530437057056` | `1/150` |

For the largest radius, denominator usage among the 67 leaves was:

| preconditioner denominator | leaf count |
|---:|---:|
| plain/no \(P\) | 2 |
| `64` | 61 |
| `256` | 3 |
| `4096` | 1 |

No finite grid is used in the proof.  Float grids are kept only as attack
diagnostics.

## Remaining boundary

The script records a manual attempt at `299/1000`.  This is still strictly
feasible, with spectral margin `1/1500`, and float grid probes remain negative.
However, the preconditioned interval run with `log_terms=20`, `max_depth=12`,
and denominators `[64,256,1024]` did not finish in roughly 150 seconds and was
interrupted.  This is a computational-cost blocker, not a failed mathematical
certificate and not a positive-curvature candidate.

Thus S8b proves a much larger continuous interval up to `29/100`, but does not
reach the actual endpoint `3/10` or prove a one-sided interval all the way to
the feasibility boundary.
