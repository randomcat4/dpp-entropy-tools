# R1 verdict

## Outcome

No real-symmetric strict counterexample was found. This is a finite non-hit,
not a proof of global concavity.

Two explicit structural results are independently verified:

1. If the midpoint `D` is a diagonal strict contraction, every nontrivial
   feasible real-symmetric chord `D+-tV` has
   `(H(D-tV)+H(D+tV))/2-H(D)<0`.
2. At such a diagonal midpoint,
   `D^2H(D)[V,V]=-sum_i V_ii^2/(d_i(1-d_i))<=0`; purely off-diagonal
   directions are flat at second order even though their nontrivial finite
   chord gap is strictly negative.

## Evidence and limits

- Bounded optimizer denominator: 13,202 objective calls, 176 restarts,
  dimensions `3,...,10`, zero values above the `1e-6` promotion threshold.
- Best numerical Hessian: `-6.245093781582534e-15`; its direct chord gap was
  `-3.960165528837933e-12`. It was not promoted.
- Independent exact-event and derivative checks passed.
- The rational certificate tool passed strict-negative, exact-zero-uncertain,
  and infeasible-endpoint tests. It received no positive candidate.

The two structural proofs were frozen in local commit
`a49051d2f768ec2b926a2e4d68d5286b054f9656`, tree
`c282e54a8221dc8546b5c8da3c23a768038b9025`. Separate reviewers read the Git
blobs from that commit and returned `STATUS: CORRECT`; their reports record the
exact blob IDs. The public API transport commit
`8ae16152670e768acc4bd5792b5db71822c42c86` has the identical tree and blob
IDs; see `verification/freeze_transport.md`. No novelty claim is made for these
elementary entropy inequalities.

General real-symmetric DPP entropy concavity remains unresolved by R1.
