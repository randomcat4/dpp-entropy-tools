# A1 verdict

FIRST_MILESTONE_COMPLETE. The original general connected three-point
counterexample/concavity target remains INCOMPLETE.

## Mathematical results

- **PROVED and independently reviewed:** strict finite-chord concavity on
  every fixed-site radial coupling slice K(A,s)=[[A,sv],[sv^T,c]], with fixed
  c in (0,1), v!=0 and strict feasibility. The theorem includes connected
  triangular midpoints; it permits all three symmetric entries of A to vary.
- **PROVED and independently reviewed:** nonpositive curvature on the entire
  four-dimensional standard-mode subspace at K_r=(1/2)I+r(J-I), abs(r)<1/4.
  It is strict for nonzero r and nonzero direction; the exact r=0 degeneracy
  is retained. This is only a local statement.
- **DISPROVED shortcut, independently reviewed:** conditional acceleration
  need not be nonpositive. The explicit rational witness has
  R>=229172119980517/500000000000000000>0, whereas its total entropy second
  derivative has a strictly negative certified upper bound. This is not an
  entropy counterexample.

The frozen premises are sufficient for these results; their minimal necessity
is not claimed. In particular the acceleration witness invalidates a proof
shortcut, not every possible extension of the radial-slice theorem.

## Verification binding

All statements and proofs were frozen at
`58ee11adcf0afd8d183057d61f0168127093bcad`, tree
`443522e843050cc0024f83e227fadfa2ef9b1d5a`. A fresh GPT-5.5 xhigh verifier,
who had authored none of the proofs, read fixed Git objects and returned
`STATUS: CORRECT` separately for all three objects. Its original review commit
is `e787ad086a8be98335933ca5f8b99f5dd921983c`, integrated as `a35ad53`.
See [the complete review](verifications/a1_fixed_object_review.md) for theorem,
proof and code blob IDs.

The verifier replayed both author symbolic checks and independently passed
15 radial identities, 23 standard-mode checks, and 9 exact acceleration
certificate checks. The first independent output attempt hit Python's large
integer string limit; the unchanged mathematical checks passed after fixing
that output setting. This failure and the successful exit codes are retained.
No Lean proof or novelty audit is claimed.

## Remaining core and finite evidence

At half-filled symmetric triangle centers, the exact full-six-dimensional
decomposition leaves the 2 by 2 trivial block T as an explicit sign problem.
Its diagonal and determinant inequalities are unproved here. For general
centers a conditioning proof still needs to dominate a potentially positive
acceleration term by the negative conditional Hessian terms. Neither gap is
replaced by a finite non-hit claim.

The bounded asymmetric lane has 5048 formal calls, 32 smoke calls, 512
same-center diagnostic calls and 20 manual gradient/certificate evaluations
including rechecks: 5612 conservatively counted evaluations. All 3000
refinement calls are saved, including 80 domain rejections. There are zero
certified positive total-entropy candidates. Some short auxiliary PIDs were
not captured; this is an execution-record limitation, not reconstructed data.

These are reusable restricted theorems and an exact obstruction. Their
correctness is separated from research novelty and publication strength;
neither novelty nor a conference-level contribution has been certified.

All bounded author and verifier computations have ended. No new search,
background continuation, or heartbeat is active for this milestone. R1 and
R3 artifacts and processes were not modified or rerun by A1.
