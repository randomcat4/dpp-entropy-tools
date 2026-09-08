# S2: unequal-leaf diamond cross gain

Status: `INCOMPLETE`, finite diagnostic complete; no positive candidate.
The 24 deterministic kernels use
`K=[[A,B],[B^T,diag(r^2,r^4)]]`, `B=[r u,r^2 v]`,
`A11=1/2`, `A22=1/3`, and `r in {1/3,1/5,1/10}`.
All lower Schur complements `A-uu^T-vv^T` and full endpoint numerical margins
are positive. No random calls were used.

The control is `A12=1/10`, `u=(1/5,1/6)`, `v=(1/7,-1/8)`.
Five axis-soft families replace these by
`A12=r^a/10`, `u=(1/5,r^b/6)`, `v=(r^c/7,-1/8)`, with
`(a,b,c)=(1,1,1),(2,2,2),(3,1,2),(2,3,1),(1,3,3)`.
An amplitude-soft family has `A12=r^2/10`, `u=(r/5,r^2/6)`,
`v=(r^3/7,-r^2/8)`. The final family has
`u=(1/5,r^2/6)`, `v=(r^2/7,-1/8)`, and
`A12=(uu^T+vv^T)12+r^3/10`.

We retain the actual-entry 4 by 4 Hessian in coordinate order
`(K02,K12,K03,K13)`, its two diagonal blocks `M33,M44`, cross block `M34`,
and the full Frobenius-orthonormal 10 by 10 Hessian. Whenever both diagonal
blocks are negative definite, the Schur-complement criterion is exactly
`gain=||(-M33)^-1/2 M34 (-M44)^-1/2||op <= 1`.
This separates a two-column failure from any single-column failure.
All 24 samples had both single-column blocks negative definite numerically.

| Family | Gain at r=1/3 | Gain at r=1/5 | Gain at r=1/10 |
|---|---:|---:|---:|
| Fixed control | 4.63889e-4 | 9.67166e-5 | 1.19352e-5 |
| Axis (1,1,1) | 2.24211e-4 | 4.63613e-5 | 5.76243e-6 |
| Axis (2,2,2) | 2.26630e-4 | 4.70648e-5 | 5.79123e-6 |
| Axis (3,1,2) | 2.12495e-4 | 4.07542e-5 | 4.29796e-6 |
| Axis (2,3,1) | 1.73241e-4 | 2.59677e-5 | 1.39614e-6 |
| Axis (1,3,3) | 8.70613e-5 | 4.60284e-6 | 9.38074e-9 |
| Amplitude and axis soft | 3.05096e-7 | 2.84415e-9 | 5.39622e-12 |
| Schur off-diagonal soft | 2.21416e-4 | 4.52715e-5 | 5.51094e-6 |

For the fixed control, gain/r^3 is approximately 0.01253, 0.01209, 0.01194.
The softest full-Hessian sample is amplitude/axis-soft r=1/10. Its two smallest
single-column defects are about `7.57986e-5` and `4.90014e-7`, but the gain is
only `5.39622e-12`; softening the blocks did not amplify the cross interaction.
These observations do not prove a uniform asymptotic statement.

The strongest gain and softest curvature were replayed with an 80-digit
inverse-trace derivative implementation, distinct from the search's polynomial
derivatives. The replay gain values are `0.00046388866138862348` and
`5.396215621257274e-12`. The latter sample's saved full-top direction has
curvature `-1.581812111185347e-10`; all six replayed chords remain negative.
This is an author check on exact stored binary64 inputs, not interval or
independent certification.

Execution: PID 158733, outer shell exit 0, 0.117 seconds, one thread, no GPU,
24 full Hessian calls, 456 entropy calls, 24 valid proposals, 0 failures,
72 retained directions and 216 K-affine chords. Replay adds 2 restricted
Hessians, 2 directional curvatures, and 14 entropy calls (288 event evaluations).
No job remains active. Source hashes and exact command are in
[batch2/manifest.json](batch2/manifest.json); all objects and failures are in
[batch2/cases.jsonl](batch2/cases.jsonl) and
[batch2/selected_replay.json](batch2/selected_replay.json).

The tested moving families provide no exceptional gain growth. The minimum
remaining obligation is to control cross gain while the single-column blocks
soften, or find a different finite interior/strong-coupling configuration.
No n=5--8 expansion is supported by this result.
