# S3: interior diamond cross-gain optimization

Status: `INCOMPLETE`; bounded optimization completed, no positive candidate.
The high gain found here is a strong shared Fisher mode, not an entropy
counterexample or a soft single-column obstruction.

## Scope and actual execution

The initial 54 objects combine three column geometries (nearly collinear,
nearly orthogonal, conflicting signs), six leaf-diagonal pairs
`(.05,.2),(.05,.95),(.2,.8),(.5,.5),(.8,.95),(.95,.95)`, and three coupling
fractions `.75,.96,.9995`. The two parent diagonals start at `.31,.67`.
Each off-diagonal template includes the parent edge and both leaf columns,
but the leaf-leaf entry is zero. Scaling uses the positive-ray strict
contraction radius, so the templates can approach either Schur boundary.

For each geometry, its highest initial gain starts an adaptive Nelder-Mead
optimization in the four diagonal entries, five nonzero off-diagonal entries,
and coupling fraction. The objective is exactly minus the two-column gain.
The three optimizers each exhausted their 80-call limit; they did not claim
convergence. There were 54 initial and 240 adaptive objective evaluations,
294 retained kernels, 0 failed evaluations, and 0 nonnegative single-column
blocks. This includes repeated optimizer starting points; it is an evaluation
count, not a claim of 294 unique matrices.

All 294 full 10 by 10 Hessians were actually evaluated. Each record retains
its 4 by 4 restriction, both single-column defect spectra, the full top
eigenvalue, Schur margins, three chosen directions, and three K-affine chords
per direction. Total: 882 direction evaluations, 2646 chords, 5586 entropy
calls. The successful process PID was 159251; outer-shell exit was 0, elapsed
time 1.436 seconds, all thread limits 1, no GPU. Source hashes and optimizer
exit reasons are in [batch3/manifest.json](batch3/manifest.json).

## Best frozen point

The final conflicting-sign run reached gain `0.9989720185177737` at case 293.
An 80-digit inverse-trace calculation gives
`0.99897201851777021585718777600414` on the exact stored binary64 matrix.

Its spectrum is approximately
`(9.25346e-6, .340903, .749161, .877363)`.
Its lower and upper Schur minimum eigenvalues are `1.47394e-5` and `.181762`.
The single-column defect spectra are
`(3.1987223,10594.7087)` and `(9.7409437,12063.9833)`.
The restricted top curvature is `-2.4354016`; the full top is `-.5472551`.
The latter saved direction has 80-digit curvature
`-.54725512419830568322`, and its three replayed chords are negative.
Thus neither single-column block is soft at this point.

The initial-to-final gain values by optimizer were:

| Column geometry | Initial leader | Final best |
|---|---:|---:|
| Nearly collinear | .9816598208 | .9989123723 |
| Nearly orthogonal | .9613781578 | .9983245958 |
| Conflicting signs | .9816591125 | .9989720185 |

## Event diagnosis at the one frozen point

At 80 digits the smallest event is full inclusion, `S=15`, with
`p_all=det(K)=2.0734325227089758e-6`. Its positive Fisher matrix is exactly
the rank-one matrix `p'_all p'_all^T/p_all` in the four actual-entry coordinates.
Its trace is `22632.3102049160`; the total Fisher trace is `22650.0892907797`.
Along the two stiff single-column modes it supplies respectively
`99.8622803309%` and `99.9022597848%` of their negative-Hessian defect.

Write `B=-Hessian(H)=F-acceleration`. After subtracting this one rare-event
Fisher matrix from B, the remaining 4 by 4 matrix has eigenvalues
`(2.43308637,8.32455162,11.83765209,16.72613274)`.
Its two diagonal blocks have spectra `(2.66521538,15.12390392)` and
`(9.72111037,11.81119315)`. They are all positive in the 80-digit diagnostic.
The artifact also separately records removing the entire event Hessian term;
these two operations are not conflated.

This accounts for the apparent approach to gain 1: a large rank-one Fisher
term couples both columns while the residual still has a definite positive
margin. It does not establish an asymptotic theorem or a general lower bound.
Every event probability, four-coordinate probability gradient, negative
Fisher contribution, and acceleration contribution is retained in
[batch3/best_event_diagnostic.json](batch3/best_event_diagnostic.json).
The frozen object is [batch3/best_gain.json](batch3/best_gain.json).

## Failed run retained separately

The first S3 process, PID 159210, exited 1. A NumPy Boolean in the output
record was not JSON serializable. This caused every attempted record write
to return the objective's error penalty, and final best-record serialization
also failed. The failed source, traceback, original RUNNING manifest, and empty
case file are retained under `diamond_interior_failed_serialization.py`,
`batch3_failed_serialization.log`, and `batch3_failed_serialization/`.
The source was fixed once by converting the Boolean, writing before appending
to successful records, and persisting failures immediately.

Failed-runtime Hessian and entropy counters were not persisted before the
exception; exact values are therefore unavailable and are not invented.
The objective invocation count is reconstructible: the same SciPy version,
same initial leaders, and the constant error objective reproduce 80 calls in
each optimizer, hence 294 attempted objective calls including initialization.
That control-flow replay did not evaluate any kernel or entropy. It is
explicitly labeled reconstructed accounting, not surviving runtime telemetry.
The failed run contributes zero retained numerical coverage and is not added
to the successful batch's 294 objects. See
[failure_accounting.json](batch3_failed_serialization/failure_accounting.json).

## Stop boundary

There is no supported reason to extend this scan or increase dimension.
The remaining nonradial mathematical obligation is to pay the possible
acceleration contribution using the available Cauchy-Schwarz slack after
the shared Fisher contribution is accounted for. A finite gain near one does
not discharge or refute that obligation. All arithmetic here is author-side
diagnostic evidence, not an interval certificate or independent theorem audit.
