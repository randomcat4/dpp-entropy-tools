# R1 verdict

## Outcome

No real-symmetric strict counterexample was found.  Global concavity is now
proved in dimension two, but remains unresolved for a general connected
real-symmetric kernel in dimension three or higher.

Five explicit results are independently verified:

1. If the midpoint `D` is a diagonal strict contraction, every nontrivial
   feasible real-symmetric chord `D+-tV` has
   `(H(D-tV)+H(D+tV))/2-H(D)<0`.
2. At such a diagonal midpoint,
   `D^2H(D)[V,V]=-sum_i V_ii^2/(d_i(1-d_i))<=0`; purely off-diagonal
   directions are flat at second order even though their nontrivial finite
   chord gap is strictly negative.
3. More generally, if the midpoint is block diagonal for a nontrivial
   partition and `V` has zero restriction to every diagonal block, every
   nonzero feasible chord `K_0+-tV` has strictly negative midpoint gap.
4. For every strict real symmetric `2 x 2` kernel, complete-event DPP Shannon
   entropy is globally concave as a function of the marginal kernel; every
   nontrivial feasible chord has strict midpoint gap.
5. For a block-diagonal midpoint and arbitrary real symmetric direction, the
   global midpoint gap is at most the sum of the principal-block gaps, with a
   strict loss for any cross-block entry.  Therefore every midpoint assembled
   from `1 x 1` and `2 x 2` blocks has nonpositive gap in every direction,
   strict for every nontrivial chord.

## Evidence and limits

- Bounded formal optimizer denominator: 55,780 objective calls, 240 restarts,
  dimensions `3,...,10`, zero values above the `1e-6` promotion threshold.
- The second-stage search added 42,578 formal calls and 823 validation calls.
  Its maximum `5.930937647366978e-15` was at residual scale; its two direct
  chord gaps were negative. It was not promoted.
  A non-author commit-bound audit returned `STATUS: CORRECT` for the fixed
  phase-2 source and compact evidence.
- Independent exact-event and derivative checks passed.
- The phase-3 `n=2` attack added 122,832 formal calls, 32 optimization
  restarts, and two successful 90-digit rechecks.  The apparent floating
  maximum `1.46e-11` became `-5.23e-12`; no object crossed the `1e-8` gate.
- The rational certificate tool passed strict-negative, exact-zero-uncertain,
  and infeasible-endpoint tests, plus a near-boundary phase-2 stress suite. It
  received no positive candidate.

The two structural proofs were frozen in local commit
`a49051d2f768ec2b926a2e4d68d5286b054f9656`, tree
`c282e54a8221dc8546b5c8da3c23a768038b9025`. Separate reviewers read the Git
blobs from that commit and returned `STATUS: CORRECT`; their reports record the
exact blob IDs. The public API transport commit
`8ae16152670e768acc4bd5792b5db71822c42c86` has the identical tree and blob
IDs; see `verification/freeze_transport.md`. No novelty claim is made for these
elementary entropy inequalities.

The phase-3 theorem/proof commit is
`603300c06059518961766c724377c3b9d1198fc5`, tree
`9c1a4db5462dddaf4a3b7cc37c010927254cbda4`.  Two non-author reviewers read
the fixed Git objects.  The `n=2` and block-composition reviews both returned
`CORRECT` and record every relevant blob ID.

General real-symmetric DPP entropy concavity in dimension at least three
remains unresolved by R1.
