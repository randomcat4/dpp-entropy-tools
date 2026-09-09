# Ready batch 03: W1 round two

Verdict: **ACCEPTED_SCOPED**.

Frozen input: PR32 commit `a8c337826ec87cf09a0cf63ea5dcd4de5de70dc8`,
`research/I05-W1-20260909-R2/`. Its separate first-round source directory
was unchanged by this commit and is covered by batch 01.

For fixed strict real symmetric contractions A (m by m), C (2 by 2), and
arbitrary real B (m by 2), complete configuration entropy along
`K(t)=[[A,tB],[tB^T,C]]` is concave throughout its feasible interval.
For nonzero B it is strictly concave in the Jensen sense, including the
stated closed-endpoint extension. `H''(0)=0` is fully compatible with that
statement. Exchanging the two blocks gives the symmetric version.

The accepted extension allows arbitrary block sizes when B has at most
two nonzero actual coordinate columns, or at most two such rows. This
condition is not interchangeable with arbitrary `rank(B)<=2`: a rotation
changes the complete configuration entropy. The proof also supplies the
two-coordinate principal-block affine lifting lemma used in the extension.

[The separate fresh nonauthor review](children/w1/W1_ROUND2_INDEPENDENT_REVIEW.md)
checks all-event Schur conditioning, strict conditional kernels, the
self-contained two-dimensional entropy lemma, the fixed-weight entropy
chain rule, monotonicity and concavity of G(s), the strict G(t^2) lift,
endpoints, exterior-power identities and the displayed obstruction examples.
This evidence does not certify unrestricted real affine entropy concavity,
dense rank-two support in two large blocks, complex kernels, stationary
entropy rates, or novelty.

Independent fixed computation passed 32 events in the m-by-2 example and
64 events with two active columns inside a four-dimensional right block.
It also checked conditional support, strict kernels, zero-point derivative
cancellation, two-dimensional Hessian and matrix-pencil formulas, and the
harmful-Q example whose total curvature is still negative. PID 168104
exited 0. Script, exact inputs embedded in the script, complete output and
runtime record are under `children/w1/`; finite probes corroborate the
proof and do not replace its universal argument.

A separate bounded symbolic check subsequently verified the general
matrix-pencil identity (3.9), using free A0,A1,A2 and
`A3=1-A0-A1-A2`. After subtracting the manuscript's expression from
`det(G-lambda Q)`, the rational numerator simplifies exactly to zero.
PID 168340 exited 0; its prewritten plan, script and complete records are
also retained. This is a general-parameter check, not a second fixed point.

The review's later scope and plan are archived as `round2_frozen_scope.md`
and `ROUND2_COMPUTE_PLAN.md`, preserving the earlier batch's files. The
author statement has one nonblocking corrupted glyph at
`frozen_statement.part02.md:1`: the zero-column condition should use
`zero` (Chinese `零`) in place of `雰`. The proof itself states the correct
condition unambiguously. Bind any editorial fix to its new source commit.

Batch 03 is a follow-up to the already merged review PR36. W4 remains a
separate pending unit; only the designated integrator may merge to main.
