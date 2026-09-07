# Fresh proof and boundary verification

STATUS: CORRECT

Candidate commit: `693c29076943f4aa30aff6bf04b9d2ec26a1f42a`.

The verifier received only `frozen_theorem_v1.md`,
`proofs/transverse_v1.md`, and `hazards.md`.  It did not inspect author
history, confidence notes, or non-public proof context.

## Justification

1. **Exact-event law.**  The generating polynomial
   `det(I-K+K diag(z))` expands to the frozen superset Mobius formula.  The
   spectral mixture is derived from this exact law and does not substitute
   inclusion minors for event masses.
2. **Feasibility.**  Schur complements for `K` and `I-K` both give exactly
   `t^2||B||_op^2 <= epsilon(1-epsilon)`.  If `B=0`, then `D=0`, so every `t`
   gives the same strict center.
3. **Comparison kernel.**  In block form, `[J,P]=D` and
   `(1/2)[J,[J,P]]=diag(-BB^T,B^TB)`.  The definition of `N` cancels this
   rotation curvature and leaves the required `diag(-I,I)` second-order term.
4. **Plucker-zero bookkeeping.**  A zero rank-`r` coordinate receives
   `tau^2 phi_S^2 x^2` from the rotated no-flip projection.  The center no-flip
   term is zero, one flip has the wrong cardinality, and a center rank-`r`
   change requires one deletion and one addition, hence order `x^4`.
5. **Remainder.**  Positive quadratic masses give the displayed logarithmic
   term with an `O(x^2)` aggregate remainder.  Two-sided nonnegativity removes
   a cubic leading term when the quadratic coefficient vanishes.  Finite event
   summation and `epsilon=x^2` yield `O(epsilon)`.
6. **Gauge and bound.**  The exterior tangent has squared norm
   `||B||_F^2`; restricting its coordinate-square sum to zero Plucker
   coordinates proves `0<=Z<=||B||_F^2`.  Fixed orthogonal frame changes
   preserve the zero set and this sum.

No critical gap was found.

## Independent strict fixtures

The accompanying implementation independently uses rational determinants,
Mobius inversion, and rational atanh-series logarithm enclosures.

- `plucker_zero_rank2_n3`: `Z=F=5`, `tau=1/4`, predicted coefficient
  `-5/16`; the certified finite-epsilon chord interval is strictly negative,
  with upper endpoint below `-0.0020522331520333500`.
- `generic_rank1_n3`: `Z=0`, `F=2`, `tau=1/3`, predicted coefficient
  `-4/9`; the certified finite-epsilon chord interval is strictly negative,
  with upper endpoint below `-0.0044932361261080070`.

The full generated report records both rational kernels, every rational event
mass, exact normalization/minimum checks, and complete rational endpoints of
the logarithm intervals.  It is deliberately ignored by Git because its raw
integer representation is about 2.4 MB; it is reproduced by:

```text
cd research/R2/verifications/fresh_v1
python verify_transverse_fixtures.py
```

The verifier's first three implementation runs failed respectively on an
overly strict `ln 2` precondition, rectangular minor slicing, and Python's
integer-string safety limit.  Each failure was retained in the private run
ledger; the final run and byte compilation exited 0.  No failed run was counted
as completed.

This verifies only frozen v1.  It is not a global real-symmetric concavity
theorem and does not rule out other chords.

## Frozen byte binding

| File | SHA256 |
| --- | --- |
| `frozen_theorem_v1.md` | `0bbc88f54d9be61ba95cd73b75924dbb24871a95a460f7977ddac6a6a7ed66f2` |
| `proofs/transverse_v1.md` | `7b0aede264e3372cfbd37cc7b7863c9e0fbc01edccaf8bb66478f56b3bfee90d` |
| `hazards.md` | `0aaa845ab7fbe943c48e962b8bf20a519303c2a26a084a85e5877f08fceb6098` |

The fresh verifier recomputed all three hashes after the candidate commit was
named; every observed value matched.
