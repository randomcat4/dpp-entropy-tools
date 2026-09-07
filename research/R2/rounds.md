# Rounds

## Round 0: state audit and freeze

- Confirmed an isolated local and remote R2 target; no pre-existing R2 job was
  present.
- Read the repository protocol and neighboring T1/T2/T3 branch artifacts.
- Froze one family before running a broad search.
- Started three isolated work units: multiscale structure, asymptotic
  coefficient/remainder, and independent boundary/certificate attack.
- No random search ran.  The first bounded diagnostic completed 3 planned
  rational fixtures at 10 epsilon values each: 30 chords, 1,200 exact event
  masses, zero failed feasibility/probability/sign checks, exit code 0.
- Public issue/PR publication is pending repository authentication; this is an
  operational state, not a mathematical blocker.

The normalized diagnostics move toward the predicted coefficient on a generic
rank-one fixture, a generic rank-two fixture, and a Plucker-zero coordinate
fixture.  Decimal logarithms are not a strict certificate.

## Round 1: frozen candidate and verification

- Candidate commit: `693c29076943f4aa30aff6bf04b9d2ec26a1f42a`.
- A fresh boundary/certificate verifier returned `CORRECT`, matched the frozen
  file hashes, and certified a Plucker-zero and a generic rational fixture.
- A separate asymptotic worker, which had not read the author proof, produced
  the same coefficient independently.  After the first review passed, it read
  the public proof as a domain-risk reviewer and returned `CORRECT`, bound to
  the same commit and hashes.
- The public copy of the strict fixture runner was rerun under one-thread,
  32-GiB, 120-second caps: exit 0, no stderr, two of two fixtures completed.
- No positive-gap real counterexample was found.  The global real question
  remains open in this route.

This bounded v1 unit is closed. Its verification is not repeated below.

## Round 2: mixed boundary hierarchy

- Proved exact eventual feasibility for the fixed mixed block family,
  including singular Schur residuals and the necessary kernel-annihilation
  conditions.
- Proved the leading coefficient
  `(Z-2||B||_F^2) epsilon log(1/epsilon)` with arbitrary fixed longitudinal
  directions. Every feasible nonzero transverse direction remains negative.
- Extended the transverse result to unequal scalar slacks
  `epsilon^alpha,epsilon^beta`; the coefficient is
  `max(alpha,beta)Z-(alpha+beta)||B||_F^2`, again strictly negative.
- For `B=0`, proved the order-`epsilon` cofactor-measurement Jensen
  obstruction and its equality kernel. On that kernel, proved universal
  cancellation of the `epsilon^2 log(1/epsilon)` layer by an eventwise
  adjugate-rank argument.
- Proved strict small-kernel two-point concavity for every fixed pair of
  distinct PSD matrices, including singular boundaries.
- Computed and signed the complete ordinary `epsilon^2` coefficient for all
  paired frames in every dimension, with arbitrary pair rotations and
  arbitrary fixed PSD inward matrices.  It is the sum of two small-kernel
  coefficients and is strict off the zero direction.  Also sealed rank-two
  one-sided tomography kernels.
- Derived a finite exterior-minor formula for the remaining general `C_2`.
  Its zero-support cross term is nonpositive; the active-support and pure
  deletion/insertion pieces are the exact unresolved terms.
- A corrected bounded search on a rational `n=8,r=4` non-paired frame checked
  65 `C_2` trials after explicitly validating signed cofactor residuals. It
  found no positive coefficient. An earlier exploratory output was discarded
  because it omitted alternating cofactor signs and failed to require the
  order-`epsilon` finite coefficient to vanish.

Round 2 adds no new formal certificate gate. The broad theorems are recorded
as `PROVED_HERE`; the general invisible-kernel `C_2` sign and the global real
question remain `INCOMPLETE`.

## Round 3: complete fixed-data boundary coefficient

- Froze the exact remaining decision problem in `frozen_theorem_v2.md` before
  continuing the proof/counterexample attack.
- Proved that the complete tomography kernel is exactly the off-block space
  between connected components of the coordinate graph of `P`.
- Used the induced product projection law to cancel the nonuniform active
  cross term and to make the zero-support cross term vanish eventwise.
- Collected the active drift, both one-flip corrections, and every two-flip
  term into an exact sum of scalar strictly-convex component-pair defects.
  Therefore `C_2<=0`, strictly for every nonzero admissible `(X,Y)`.
- A separate exterior-algebra route reached the weighted quadratic-form
  blocker but did not sign it before the component theorem removed it.
- The corrected counterexample route checked 892 signed-formula trials under
  every earlier gate and found no positive coefficient.  Its closest nonzero
  value was approximately `-7.36e-11`; exact-event interpolation agreed with
  the finite formula to about `4e-118`.
- Two non-author reviews returned `CORRECT`.  One was a proof-only logic/domain
  audit; the other also reproduced the non-paired `n=8,r=4` coefficient and
  its component-pair sum.  These reviews will be bound once to the fixed
  candidate commit because this is a major closure.

The global real-kernel entropy-concavity question remains outside the frozen
boundary family and is not claimed solved.
