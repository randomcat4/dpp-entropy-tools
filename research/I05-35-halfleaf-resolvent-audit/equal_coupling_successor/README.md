# I05-35 successor packet: independent resolvent audit and equal-coupling theorem

Status: **AUTHOR PROOF / PENDING INDEPENDENT REVIEW**. Novelty is not assessed.

This packet continues public draft PR #120 in `randomcat4/dpp-entropy-tools`. It was prepared after the exact pointwise-resolvent checkpoint had already been uploaded, and is now committed to that same successor branch as a post-checkpoint continuation. The statements below remain author proofs / pending independent review.

## Results

1. The PR120 exact physical witness independently confirms that the old pointwise claim `Phi_r''>0` for every `r>0` and every six-dimensional half-leaf direction is false. This is a certificate-method counterexample, not an entropy counterexample.
2. The full retained decomposition is

   `-H''=4(D11^2+D22^2)+G1''+G0''`.

3. New theorem: every strict half-leaf with equal squared couplings `A=B` has `G1''>0` and `G0''>0` in all six physical directions. Therefore its complete eight-event Shannon Hessian is strictly negative for every legal `q`.
4. Every such center has an open neighborhood in the full missing-edge parameter space containing unequal leaf diagonals and unequal coupling strengths; compact equal-coupling families have a uniform neighborhood.

## Files

- `independent_audit.md`: exact independent reconstruction of the pointwise obstruction and retained entropy values.
- `equal_coupling_one_sided_theorem.md`: analytic proof of the new theorem.
- `code/verify_equal_coupling_one_sided.py`: exact SymPy reconstruction of the six-coordinate block and determinant identities.
- `output/verify_equal_coupling_one_sided.txt`: literal output of one exact symbolic run.
- `failure_ledger.md`: exact nonclaims and remaining obstacle.

No finite sample is promoted to a theorem. No PR81/PR104 checker was executed. No spectral entropy or non-affine physical path is used.
